# -*- coding: utf-8  -*-

from flask import g

from .._provided import config

__all__ = ["get_current", "get_count", "get_summary", "get_unit"]

def get_current():
    """Return the name of the currently selected campaign, or None."""
    if not config["enabled"]:
        return None
    setting = g.auth.get_character_modprop("campaigns", "current")
    if not setting or setting not in config["enabled"]:
        return config["enabled"][0]
    return setting

def get_count(cname, opname):
    """Return the primary operation count for the given campaign/operation."""
    key = cname + "." + opname
    operation = config["campaigns"][cname]["operations"][opname]
    optype = operation["type"]
    qualifiers = operation["qualifiers"]

    ...
    import random
    return [random.randint(0, 500), random.randint(10000, 500000), random.randint(10000000, 50000000000)][random.randint(0, 2)]

def get_summary(name, opname, limit=5):
    """Return a sample fraction of results for the given campaign/operation."""
    ...
    return []

def get_unit(operation, num):
    """Return the correct form of the unit tracked by the given operation."""
    types = {
        "killboard": "ship|ships",
        "collection": "item|items"
    }
    if "unit" in operation:
        unit = operation["unit"]
    else:
        unit = types[operation["type"]]

    if "|" in unit:
        return unit.split("|")[0 if num == 1 else 1]
    return unit
