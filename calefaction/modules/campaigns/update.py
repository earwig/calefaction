# -*- coding: utf-8  -*-

import sys
import textwrap

from flask import g

from .._provided import config, logger

__all__ = ["update_operation"]

def _save_operation(cname, opname, primary, secondary, key=None):
    """Save the given campaign/operation overview info in the database."""
    secstr = "" if secondary is None else (" secondary=%d" % secondary)
    logger.debug("Setting overview primary=%d%s campaign=%s operation=%s",
                 primary, secstr, cname, opname)
    g.campaign_db.set_overview(cname, opname, primary, secondary)
    g.campaign_db.touch_operation(cname, opname, key=key)

def _build_filter(qualifiers):
    """Given a qualifiers string from the config, return a filter function.

    This function is extremely sensitive since it executes arbitrary Python
    code. It should never be run with a user-provided argument! We trust the
    contents of a config file because it originates from a known place on the
    filesystem.
    """
    namespace = {}
    body = "def _func(kill):\n" + textwrap.indent(qualifiers, " " * 4)
    exec(body, namespace)
    return namespace["_func"]

def _store_kill(cname, opnames, kill):
    """Store the given kill and its associations into the database."""
    kid = kill["killID"]
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
        filters.append((_build_filter(qualif), opname))

    args = ["kills", "corporationID", g.config.get("corp.id"), "no-items",
            "no-attackers", "orderDirection", "asc"]
    if min_kill_id > 0:
        args += ["afterKillID", min_kill_id]

    max_kill_id = min_kill_id
    for kill in g.eve.zkill.iter_killmails(*args):
        kid = kill["killID"]
        ktime = kill["killTime"]
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

def _update_collection_operations(cname, opnames):
    """Update all collection-type operations in the given campaign subset."""
    campaign = config["campaigns"][cname]
    for opname in opnames:
        operation = campaign["operations"][opname]
        show_isk = operation.get("isk", True)

        # store per-user counts; update for all users in corp who have fresh
        # API keys and leave other data stale
        ...
        primary = __import__("random").randint(10, 99)
        secondary = __import__("random").randint(10000000, 5000000000) / 100 \
            if show_isk else None

        _save_operation(cname, opname, primary, secondary)

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
        for opname in opnames:
            last_updated, key = g.campaign_db.check_operation(cname, opname)
            if new and last_updated is None:
                opsubset.append(opname)
            elif not new and last_updated is not None:
                min_key = min(min_key, key)
                opsubset.append(opname)
        _update_killboard_operations(cname, opsubset, min_key)
    elif optype == "collection":
        _update_collection_operations(cname, opnames)
    else:
        raise RuntimeError("Unknown operation type: %s" % optype)
