# -*- coding: utf-8  -*-

from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock

from flask import g

from .database import CampaignDB
from .._provided import app, config, logger
from ...database import Database as MainDB

__all__ = ["get_current", "get_overview", "get_summary", "get_unit"]

_MAX_STALENESS = 60 * 60

CampaignDB.path = str(Path(MainDB.path).parent / "db_campaigns.sqlite3")

app.before_request(CampaignDB.pre_hook)
app.teardown_appcontext(CampaignDB.post_hook)

_lock = Lock()

def _update_operation(cname, opname, new):
    """Update a campaign/operation."""
    ...

    operation = config["campaigns"][cname]["operations"][opname]
    optype = operation["type"]
    qualifiers = operation["qualifiers"]
    show_isk = operation.get("isk", True)

    primary = __import__("random").randint(10, 99)
    secondary = __import__("random").randint(100000, 50000000)
    g.campaign_db.set_overview(cname, opname, primary, secondary)

def get_current():
    """Return the name of the currently selected campaign, or None."""
    if not config["enabled"]:
        return None
    setting = g.auth.get_character_modprop("campaigns", "current")
    if not setting or setting not in config["enabled"]:
        return config["enabled"][0]
    return setting

def get_overview(cname, opname):
    """Return overview information for the given campaign/operation.

    The overview is a 2-tuple of (primary_count, secondary_count). The latter
    may be None, in which case it should not be displayed.

    Updates the database if necessary, so this can take some time.
    """
    maxdelta = timedelta(seconds=_MAX_STALENESS)
    with _lock:
        last_updated = g.campaign_db.check_operation(cname, opname)
        if last_updated is None:
            logger.debug("Adding campaign=%s operation=%s", cname, opname)
            _update_operation(cname, opname, new=True)
            g.campaign_db.add_operation(cname, opname)
        elif datetime.utcnow() - last_updated > maxdelta:
            logger.debug("Updating campaign=%s operation=%s", cname, opname)
            _update_operation(cname, opname, new=False)
            g.campaign_db.touch_operation(cname, opname)
        else:
            logger.debug("Using cache for campaign=%s operation=%s",
                         cname, opname)
        return g.campaign_db.get_overview(cname, opname)

def get_summary(name, opname, limit=5):
    """Return a sample fraction of results for the given campaign/operation."""
    ...
    return []

def get_unit(operation, num, primary=True):
    """Return the correct form of the unit tracked by the given operation."""
    if not primary:
        return "ISK"

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
