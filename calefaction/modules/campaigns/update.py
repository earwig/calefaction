# -*- coding: utf-8  -*-

import sys
import textwrap

from flask import g

from .._provided import config, logger
from ...exceptions import EVEAPIForbiddenError

__all__ = ["update_operation"]

def _save_operation(cname, opname, primary, secondary, key=None):
    """Save the given campaign/operation overview info in the database."""
    secstr = "" if secondary is None else (" secondary=%d" % secondary)
    logger.debug("Setting overview primary=%d%s campaign=%s operation=%s",
                 primary, secstr, cname, opname)
    g.campaign_db.set_overview(cname, opname, primary, secondary)
    g.campaign_db.touch_operation(cname, opname, key=key)

def _build_filter(qualifiers, arg):
    """Given a qualifiers string from the config, return a filter function.

    This function is extremely sensitive since it executes arbitrary Python
    code. It should never be run with a user-provided argument! We trust the
    contents of a config file because it originates from a known place on the
    filesystem.
    """
    namespace = {"g": g}
    body = ("def _func(%s):\n" % arg) + textwrap.indent(qualifiers, " " * 4)
    exec(body, namespace)
    return namespace["_func"]

def _store_kill(cname, opnames, kill):
    """Store the given kill and its associations into the database."""
    kid = kill["killmail_id"]
    if g.campaign_db.has_kill(kid):
        current = g.campaign_db.get_kill_associations(cname, kid)
        opnames -= set(current)
        if opnames:
            logger.debug("Adding operations=%s to kill id=%d campaign=%s",
                         ",".join(opnames), kid, cname)
    else:
        logger.debug("Adding kill id=%d campaign=%s operations=%s", kid, cname,
                     ",".join(opnames))
        g.campaign_db.add_kill(kill)

    g.campaign_db.associate_kill(cname, kid, opnames)

def _update_killboard_operations(cname, opnames, min_kill_id):
    """Update all killboard-type operations in the given campaign subset."""
    operations = config["campaigns"][cname]["operations"]
    filters = []
    for opname in opnames:
        qualif = operations[opname]["qualifiers"]
        filters.append((_build_filter(qualif, "kill"), opname))

    args = ["kills", "corporationID", g.config.get("corp.id"), "no-items",
            "no-attackers"]

    max_kill_id = min_kill_id
    for kill in g.eve.zkill.iter_killmails(*args, extended=True):
        kid = kill["killmail_id"]
        if min_kill_id > 0 and kid == min_kill_id:
            # TODO: This fails if ZKill receives kills out of order.
            # Should look ahead for kills within, say, 12 hours of the
            # min_kill_id, and extend code below to ignore kills aleady
            # included instead of re-adding.
            break

        ktime = kill["killmail_time"]
        logger.debug("Evaluating kill date=%s id=%d for campaign=%s "
                     "operations=%s", ktime, kid, cname, ",".join(opnames))
        max_kill_id = max(max_kill_id, kid)
        ops = set()
        for filt, opname in filters:
            if filt(kill):
                ops.add(opname)
        if ops:
            _store_kill(cname, ops, kill)

    for opname in opnames:
        primary, secondary = g.campaign_db.count_kills(cname, opname)
        show_isk = operations[opname].get("isk", True)
        if not show_isk:
            secondary = None
        _save_operation(cname, opname, primary, secondary, key=max_kill_id)

def _get_prices():
    """Return a dict mapping type IDs to ISK prices."""
    pricelist = g.eve.esi().v1.markets.prices.get()
    return {entry["type_id"]: entry["average_price"]
            for entry in pricelist if "average_price" in entry}

def _save_collection_overview(cname, opnames, data):
    """Save collection overview data to the database."""
    operations = config["campaigns"][cname]["operations"]
    for opname in opnames:
        primary = sum(count for d in data[opname].values()
                      for (count, _) in d.values())
        show_isk = operations[opname].get("isk", True)
        if show_isk:
            secondary = sum(value for d in data[opname].values()
                            for (_, value) in d.values())
        else:
            secondary = None
        _save_operation(cname, opname, primary, secondary)

def _update_collection_operations(cname, opnames):
    """Update all collection-type operations in the given campaign subset."""
    operations = config["campaigns"][cname]["operations"]
    filters = []
    for opname in opnames:
        qualif = operations[opname]["qualifiers"]
        filters.append((_build_filter(qualif, "asset"), opname))

    prices = _get_prices()
    data = {opname: {} for opname in opnames}

    for char_id, token in g.auth.get_valid_characters():
        logger.debug("Fetching assets for char id=%d campaign=%s "
                     "operations=%s", char_id, cname, ",".join(opnames))
        try:
            assets = g.eve.esi(token).v1.characters(char_id).assets.get()
        except EVEAPIForbiddenError:
            logger.debug("Asset access denied for char id=%d", char_id)
            continue

        for opname in opnames:
            data[opname][char_id] = {}

        logger.debug("Evaluating %d assets for char id=%d",
                     len(assets), char_id)
        for asset in assets:
            for filt, opname in filters:
                if filt(asset):
                    typeid = asset["type_id"]
                    count = 1 if asset["is_singleton"] else asset["quantity"]
                    value = prices.get(typeid, 0.0)
                    char = data[opname][char_id]
                    if typeid in char:
                        char[typeid][0] += count
                        char[typeid][1] += count * value
                    else:
                        char[typeid] = [count, count * value]

    g.campaign_db.update_items(cname, data)
    _save_collection_overview(cname, opnames, data)

def update_operation(cname, opname, new=False):
    """Update a campaign/operation. Assumes a thread-exclusive lock is held."""
    campaign = config["campaigns"][cname]
    operations = campaign["operations"]
    optype = operations[opname]["type"]
    opnames = [opn for opn in campaign["enabled"]
               if operations[opn]["type"] == optype]

    if optype == "killboard":
        opsubset = []
        min_key = 0 if new else sys.maxsize
        for opn in opnames:
            last_updated, key = g.campaign_db.check_operation(cname, opn)
            if new and last_updated is None:
                opsubset.append(opn)
            elif not new and last_updated is not None:
                min_key = min(min_key, key)
                opsubset.append(opn)
        _update_killboard_operations(cname, opsubset, min_key)
    elif optype == "collection":
        _update_collection_operations(cname, opnames)
    else:
        raise RuntimeError("Unknown operation type: %s" % optype)
