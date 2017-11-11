# -*- coding: utf-8  -*-

import gzip
from threading import Lock

import yaml

__all__ = ["Universe"]

def _cache(func):
    """Wrap a no-argument method to cache its return value in the object."""
    def inner(self):
        key = func.__name__
        if key in self._cache:
            return self._cache[key]
        value = func(self)
        self._cache[key] = value
        return value
    return inner


class _UniqueObject:
    """Base class for uniquely ID'd objects in the universe."""

    def __init__(self, universe, id_, data):
        self._universe = universe
        self._id = id_
        self._data = data
        self._cache = {}

    @property
    def id(self):
        """The object's unique ID, as an integer."""
        return self._id


class _SolarSystem(_UniqueObject):
    """Represents a solar system."""

    @property
    def name(self):
        """The solar system's name, as a string."""
        return self._data["name"]

    @property
    @_cache
    def constellation(self):
        """The solar system's constellation, as a _Constellation object."""
        return self._universe.constellation(self._data["constellation"])

    @property
    @_cache
    def region(self):
        """The solar system's region, as a _Region object."""
        return self._universe.region(self._data["region"])

    @property
    def security(self):
        """The solar system's security status, as a float."""
        return self._data["security"]

    @property
    def coords(self):
        """The solar system's coordinates, as a 3-tuple of floats (x, y, z)."""
        return tuple(self._data["coords"])

    @property
    @_cache
    def gates(self):
        """The solar system's adjacent systems, via stargate.

        A list of _SolarSystem objects.
        """
        return [self._universe.system(sid) for sid in self._data["gates"]]

    @property
    @_cache
    def faction(self):
        """The solar system's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return self.constellation.faction

    @property
    def is_nullsec(self):
        """Whether the solar system is in nullsec."""
        return self.security <= 0.0

    @property
    def is_lowsec(self):
        """Whether the solar system is in nullsec."""
        return self.security > 0.0 and self.security < 0.45

    @property
    def is_highsec(self):
        """Whether the solar system is in nullsec."""
        return self.security >= 0.45

    @property
    def is_whspace(self):
        """Whether the solar system is in wormhole space."""
        return self.region.is_whspace


class _Constellation(_UniqueObject):
    """Represents a constellation."""

    @property
    def name(self):
        """The constellation's name, as a string."""
        return self._data["name"]

    @property
    @_cache
    def region(self):
        """The constellation's region, as a _Region object."""
        return self._universe.region(self._data["region"])

    @property
    @_cache
    def faction(self):
        """The constellation's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return self.region.faction

    @property
    def is_whspace(self):
        """Whether the constellation is in wormhole space."""
        return self.region.is_whspace


class _Region(_UniqueObject):
    """Represents a region."""

    @property
    def name(self):
        """The region's name, as a string."""
        return self._data["name"]

    @property
    @_cache
    def faction(self):
        """The region's faction, as a _Faction object, or None."""
        if "faction" in self._data:
            return self._universe.faction(self._data["faction"])
        return None

    @property
    def is_whspace(self):
        """Whether the region is in wormhole space."""
        return self._id >= 11000000


class _Faction(_UniqueObject):
    """Represents a faction."""

    @property
    def name(self):
        """The faction's name, as a string."""
        return self._data["name"]

    @property
    @_cache
    def territory(self):
        """The faction's controlled territory.

        A list of _SolarSystems.
        """
        return [system for system in self._universe.systems()
                if system.faction and system.faction.id == self.id]


class _Type(_UniqueObject):
    """Represents any type, including ships and materials."""

    @property
    def name(self):
        """The item's name, as a string."""
        return self._data["name"]

    @property
    def group_id(self):
        """The item's group ID, as an integer."""
        return self._data["group_id"]

    @property
    def market_group_id(self):
        """The item's market group ID, as an integer, or None."""
        return self._data.get("market_group_id")


class _Killable(_UniqueObject):
    """Represents a killable object, like a ship, structure, or fighter."""

    def __init__(self, universe, kid, cat, data):
        super().__init__(universe, kid, data)
        self._cat = cat

    @property
    def name(self):
        """The killable object's name, as a string."""
        return self._data["name"]

    @property
    def group(self):
        """The killable object's group, as a string."""
        return self._data["group"]

    @property
    def is_ship(self):
        """Whether the killable object is a ship."""
        return self._cat == "ships"

    @property
    def is_structure(self):
        """Whether the killable object is a structure."""
        return self._cat == "structures"

    @property
    def is_fighter(self):
        """Whether the killable object is a fighter."""
        return self._cat == "fighters"


class _DummySolarSystem(_SolarSystem):
    """Represents an unknown or invalid solar system."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown",
            "constellation": -1,
            "region": -1,
            "security": 0.0,
            "coords": (0.0, 0.0, 0.0),
            "gates": []
        })


class _DummyConstellation(_Constellation):
    """Represents an unknown or invalid constellation."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown",
            "region": -1
        })


class _DummyRegion(_Region):
    """Represents an unknown or invalid region."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown"
        })


class _DummyFaction(_Faction):
    """Represents an unknown or invalid faction."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown"
        })


class _DummyType(_Type):
    """Represents an unknown or invalid type."""

    def __init__(self, universe):
        super().__init__(universe, -1, {
            "name": "Unknown",
            "group_id": -1,
            "market_group_id": -1
        })


class _DummyKillable(_Killable):
    """Represents an unknown or invalid killable object."""

    def __init__(self, universe):
        super().__init__(universe, -1, None, {
            "name": "Unknown",
            "group": "Unknown"
        })


class Universe:
    """EVE API module for static universe data."""

    def __init__(self, datadir):
        self._dir = datadir

        self._lock = Lock()
        self._loaded = False

        self._systems = {}
        self._constellations = {}
        self._regions = {}
        self._factions = {}
        self._types = {}
        self._killable_idx = {}
        self._killable_tab = {}

    @staticmethod
    def _load_yaml(path):
        """Load in and return a YAML file with the given path."""
        with gzip.open(str(path), "rb") as fp:
            return yaml.load(fp, Loader=yaml.CLoader)

    def _load(self):
        """Load in universe data. This can be called multiple times safely."""
        if self._loaded:
            return

        with self._lock:
            if self._loaded:
                return

            galaxy = self._load_yaml(self._dir / "galaxy.yml.gz")
            self._systems = galaxy["systems"]
            self._constellations = galaxy["constellations"]
            self._regions = galaxy["regions"]
            del galaxy

            entities = self._load_yaml(self._dir / "entities.yml.gz")
            self._factions = entities["factions"]
            del entities

            self._types = self._load_yaml(self._dir / "types.yml.gz")

            killables = self._load_yaml(self._dir / "killables.yml.gz")
            self._killable_idx = {kid: cat for cat, kids in killables.items()
                                  for kid in kids}
            self._killable_tab = killables
            del killables

            self._loaded = True

    def system(self, sid):
        """Return a _SolarSystem with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if sid not in self._systems:
            return _DummySolarSystem(self)
        return _SolarSystem(self, sid, self._systems[sid])

    def systems(self):
        """Return an iterator over all _SolarSystems."""
        self._load()
        for sid in self._systems:
            yield self.system(sid)

    def constellation(self, cid):
        """Return a _Constellation with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if cid not in self._constellations:
            return _DummyConstellation(self)
        return _Constellation(self, cid, self._constellations[cid])

    def constellations(self):
        """Return an iterator over all _Constellations."""
        self._load()
        for cid in self._constellations:
            yield self.constellation(cid)

    def region(self, rid):
        """Return a _Region with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if rid not in self._regions:
            return _DummyRegion(self)
        return _Region(self, rid, self._regions[rid])

    def regions(self):
        """Return an iterator over all _Regions."""
        self._load()
        for rid in self._regions:
            yield self.region(rid)

    def faction(self, fid):
        """Return a _Faction with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if fid not in self._factions:
            return _DummyFaction(self)
        return _Faction(self, fid, self._factions[fid])

    def factions(self):
        """Return an iterator over all _Factions."""
        self._load()
        for fid in self._factions:
            yield self.faction(fid)

    def type(self, tid):
        """Return a _Type with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if tid not in self._types:
            return _DummyType(self)
        return _Type(self, tid, self._types[tid])

    def killable(self, kid):
        """Return a _Killable with the given ID.

        If the ID is invalid, return a dummy unknown object with ID -1.
        """
        self._load()
        if kid not in self._killable_idx:
            return _DummyKillable(self)
        cat = self._killable_idx[kid]
        return _Killable(self, kid, cat, self._killable_tab[cat][kid])
