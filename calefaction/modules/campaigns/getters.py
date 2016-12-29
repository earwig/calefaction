# -*- coding: utf-8  -*-

from datetime import datetime
from pathlib import Path
from threading import Lock

from flask import g

from .database import CampaignDB
from .update import update_operation
from .._provided import app, config, logger
from ...database import Database as MainDB

__all__ = ["get_current", "get_overview", "get_summary", "get_unit"]

_MAX_STALENESS = 60 * 60

CampaignDB.path = str(Path(MainDB.path).parent / "db_campaigns.sqlite3")

app.before_request(CampaignDB.pre_hook)
app.teardown_appcontext(CampaignDB.post_hook)

_lock = Lock()

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
    with _lock:
        last_updated, _ = g.campaign_db.check_operation(cname, opname)
        if last_updated is None:
            logger.debug("Adding campaign=%s operation=%s", cname, opname)
            update_operation(cname, opname, new=True)
        else:
            age = (datetime.utcnow() - last_updated).total_seconds()
            if age > _MAX_STALENESS:
                logger.debug("Updating (stale cache age=%d) campaign=%s "
                             "operation=%s", age, cname, opname)
                update_operation(cname, opname, new=False)
            else:
                logger.debug("Using cache (age=%d) for campaign=%s "
                             "operation=%s", age, cname, opname)
    return g.campaign_db.get_overview(cname, opname)

def get_summary(cname, opname, limit=5):
    """Return a sample fraction of results for the given campaign/operation."""
    optype = config["campaigns"][cname]["operations"][opname]["type"]
    if optype == "killboard":
        kills = g.campaign_db.get_associated_kills(cname, opname, limit=limit)
        return kills, "killboard_recent"
    elif optype == "collection":
        ...
        return [], None
    else:
        raise RuntimeError("Unknown operation type: %s" % optype)

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
