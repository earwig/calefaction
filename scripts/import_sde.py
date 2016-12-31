#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import gzip
from pathlib import Path
import shutil
import sys

import yaml

_SHIP_CAT = 6
_FIGHTER_CAT = 87
_STRUCT_CATS = [22, 23, 40, 46, 65]

_REGION = 3
_CONSTELLATION = 4
_SOLAR_SYSTEM = 5

def _load_yaml(filename):
    with filename.open("rb") as fp:
        return yaml.load(fp, Loader=yaml.CLoader)

def _save_yaml(filename, data):
    with filename.open("w") as fp:
        fp.write(yaml.dump(data, Dumper=yaml.CDumper))

def _verify_categoryids(sde_dir):
    print("Verifying categoryIDs... ", end="", flush=True)

    data = _load_yaml(sde_dir / "fsd" / "categoryIDs.yaml")

    assert data[_SHIP_CAT]["name"]["en"] == "Ship"

    print("done.")

def _load_groupids(sde_dir):
    print("Loading groupIDs... ", end="", flush=True)

    data = _load_yaml(sde_dir / "fsd" / "groupIDs.yaml")

    groups = {cid: {} for cid in [_SHIP_CAT, _FIGHTER_CAT] + _STRUCT_CATS}
    for gid, group in data.items():
        cat = group["categoryID"]
        if cat in groups:
            name = group["name"]["en"]
            assert isinstance(gid, int)
            assert isinstance(name, str)
            groups[cat][gid] = name

    print("done.")
    return groups

def _load_typeids(sde_dir, groups):
    print("Loading typeIDs... ", end="", flush=True)

    data = _load_yaml(sde_dir / "fsd" / "typeIDs.yaml")

    assert data[_REGION]["groupID"] == _REGION
    assert data[_REGION]["name"]["en"] == "Region"
    assert data[_CONSTELLATION]["groupID"] == _CONSTELLATION
    assert data[_CONSTELLATION]["name"]["en"] == "Constellation"
    assert data[_SOLAR_SYSTEM]["groupID"] == _SOLAR_SYSTEM
    assert data[_SOLAR_SYSTEM]["name"]["en"] == "Solar System"

    types = {"ships": {}, "structures": {}, "fighters": {}}
    cat_conv = {_SHIP_CAT: "ships", _FIGHTER_CAT: "fighters"}
    cat_conv.update({cid: "structures" for cid in _STRUCT_CATS})
    group_conv = {gid: cid for cid, gids in groups.items() for gid in gids}

    for tid, type_ in data.items():
        gid = type_["groupID"]
        if gid in group_conv:
            cid = group_conv[gid]
            cname = cat_conv[cid]
            name = type_["name"]["en"]
            group = groups[cid][gid]
            assert isinstance(tid, int)
            types[cname][tid] = {"name": name, "group": group}

    print("done.")
    return types

def _load_ids(sde_dir):
    print("Loading itemIDs... ", end="", flush=True)

    data = _load_yaml(sde_dir / "bsd" / "invItems.yaml")

    ids = {_REGION: [], _CONSTELLATION: [], _SOLAR_SYSTEM: []}
    for entry in data:
        if entry["typeID"] in ids:
            ids[entry["typeID"]].append(entry["itemID"])

    print("done.")
    return ids

def _load_names(sde_dir):
    print("Loading itemNames... ", end="", flush=True)

    data = _load_yaml(sde_dir / "bsd" / "invNames.yaml")

    names = {}
    for entry in data:
        name = entry["itemName"]
        assert isinstance(name, str)
        names[entry["itemID"]] = name

    print("done.")
    return names

def _build_galaxy_skeleton(ids, names):
    print("Building galaxy skeleton... ", end="", flush=True)

    galaxy = {"regions": {}, "constellations": {}, "systems": {}}

    d = galaxy["regions"]
    for rid in ids[_REGION]:
        assert isinstance(rid, int)
        d[rid] = {
            "name": names[rid]
        }

    d = galaxy["constellations"]
    for cid in ids[_CONSTELLATION]:
        assert isinstance(cid, int)
        d[cid] = {
            "name": names[cid],
            "region": -1
        }

    d = galaxy["systems"]
    for sid in ids[_SOLAR_SYSTEM]:
        assert isinstance(sid, int)
        d[sid] = {
            "name": names[sid],
            "constellation": -1, "region": -1, "security": 0.0
        }

    print("done.")
    return galaxy

def _load_assoc_for_system(galaxy, system, rid, cid):
    data = _load_yaml(system / "solarsystem.staticdata")
    sid = data["solarSystemID"]
    sec = data["security"]

    assert isinstance(sid, int)
    assert isinstance(sec, float)
    assert sid >= 0
    assert sec >= -1.0 and sec <= 1.0

    galaxy["systems"][sid]["constellation"] = cid
    galaxy["systems"][sid]["region"] = rid
    galaxy["systems"][sid]["security"] = sec

    if "factionID" in data:
        facid = data["factionID"]
        assert isinstance(facid, int)
        assert facid >= 0
        galaxy["systems"][sid]["faction"] = facid

def _load_assoc_for_constellation(galaxy, constellation, rid):
    data = _load_yaml(constellation / "constellation.staticdata")
    cid = data["constellationID"]

    assert isinstance(cid, int)
    assert cid >= 0

    galaxy["constellations"][cid]["region"] = rid

    if "factionID" in data:
        facid = data["factionID"]
        assert isinstance(facid, int)
        assert facid >= 0
        galaxy["constellations"][cid]["faction"] = facid

    for system in constellation.iterdir():
        if not system.is_dir():
            continue

        _load_assoc_for_system(galaxy, system, rid, cid)

def _load_assoc_for_region(galaxy, region):
    data = _load_yaml(region / "region.staticdata")
    rid = data["regionID"]

    assert isinstance(rid, int)
    assert rid >= 0

    if "factionID" in data:
        facid = data["factionID"]
        assert isinstance(facid, int)
        assert facid >= 0
        galaxy["regions"][rid]["faction"] = facid

    for constellation in region.iterdir():
        if not constellation.is_dir():
            continue

        _load_assoc_for_constellation(galaxy, constellation, rid)

def _load_galaxy_associations(sde_dir, galaxy):
    print("Loading galaxy staticdata... ", end="", flush=True)

    univdir = sde_dir / "fsd" / "universe"
    for base in univdir.iterdir():
        if not base.is_dir():
            continue

        for region in base.iterdir():
            if not region.is_dir():
                continue

            _load_assoc_for_region(galaxy, region)

    print("done.")

    for cid, constellation in galaxy["constellations"].items():
        if constellation["region"] < 0:
            print("[WARNING] Orphaned constellation: %d=%s" % (
                cid, constellation["name"]))

    for sid, system in galaxy["systems"].items():
        if system["region"] < 0 or system["constellation"] < 0:
            print("[WARNING] Orphaned system: %d=%s" % (sid, system["name"]))

def _load_factions(sde_dir):
    print("Loading factions... ", end="", flush=True)

    data = _load_yaml(sde_dir / "bsd" / "chrFactions.yaml")

    factions = {}
    for entry in data:
        fid = entry["factionID"]
        name = entry["factionName"]

        assert isinstance(fid, int)
        assert isinstance(name, str)
        assert fid >= 0

        factions[fid] = {"name": name}

    print("done.")
    return factions

def _dump_types(out_dir, types):
    print("Dumping types... ", end="", flush=True)

    _save_yaml(out_dir / "types.yml", types)

    print("done.")

def _dump_galaxy(out_dir, galaxy):
    print("Dumping galaxy... ", end="", flush=True)

    _save_yaml(out_dir / "galaxy.yml", galaxy)

    print("done.")

def _dump_entities(out_dir, factions):
    print("Dumping entities... ", end="", flush=True)

    entities = {"factions": factions}
    _save_yaml(out_dir / "entities.yml", entities)

    print("done.")

def _compress(out_dir):
    targets = ["types", "galaxy", "entities"]
    for basename in targets:
        print("Compressing %s... " % basename, end="", flush=True)

        fn_src = out_dir / (basename + ".yml")
        fn_dst = out_dir / (basename + ".yml.gz")

        with fn_src.open("rb") as f_in:
            with gzip.open(str(fn_dst), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print("done.")

def _cleanup(out_dir):
    print("Cleaning up... ", end="", flush=True)

    targets = ["types", "galaxy", "entities"]
    for basename in targets:
        (out_dir / (basename + ".yml")).unlink()

    print("done.")

def import_sde(sde_dir, out_dir):
    """Import the SDE unzipped at sde_dir to out_dir."""
    print("EVE Online static data import")
    print("- from: %s" % sde_dir)
    print("- to:   %s" % out_dir)

    _verify_categoryids(sde_dir)
    groups = _load_groupids(sde_dir)
    types = _load_typeids(sde_dir, groups)
    _dump_types(out_dir, types)
    del groups, types

    ids = _load_ids(sde_dir)
    print("Counts: regions=%d, constellations=%d, systems=%d" % (
        len(ids[_REGION]), len(ids[_CONSTELLATION]), len(ids[_SOLAR_SYSTEM])))
    names = _load_names(sde_dir)

    galaxy = _build_galaxy_skeleton(ids, names)
    del ids, names
    _load_galaxy_associations(sde_dir, galaxy)
    _dump_galaxy(out_dir, galaxy)
    del galaxy

    factions = _load_factions(sde_dir)
    _dump_entities(out_dir, factions)
    del factions

    _compress(out_dir)
    _cleanup(out_dir)

def main():
    if len(sys.argv) < 2:
        print("usage: %s <sde_directory>" % sys.argv[0])
        exit(1)

    sde_dir = Path(sys.argv[1]).resolve()
    out_dir = Path(__file__).resolve().parent.parent / "data" / "universe"
    import_sde(sde_dir, out_dir)

if __name__ == "__main__":
    main()
