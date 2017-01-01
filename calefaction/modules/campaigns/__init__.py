# -*- coding: utf-8  -*-

from .getters import get_current, get_overview, get_summary, get_unit
from .routes import home, navitem
from .._provided import config

def _get_scopes():
    """Determine the required scopes, depending on enabled operations."""
    for cname in config["enabled"]:
        campaign = config["campaigns"][cname]
        for opname in campaign["enabled"]:
            optype = campaign["operations"][opname]["type"]
            if optype == "collection":
                return {"esi-assets.read_assets.v1"}
    return {}

SCOPES = _get_scopes()
