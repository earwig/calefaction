# -*- coding: utf-8  -*-

from flask import g, json
from flask_mako import render_template

from ._provided import app, blueprint

def home():
    """Render and return the main map page."""
    return render_template("map/map.mako")

def navitem():
    """Render and return the navigation item for this module."""
    return render_template("map/navitem.mako").decode("utf8")

@blueprint.rroute("/map")
def map():
    """Render and return the main map page."""
    return home()

@blueprint.rroute("/map/data.json")
def mapdata():
    """Render and return the map data as a JSON object."""
    payload = {
        "systems": {
            system.id: {
                "name": system.name,
                "region": system.region.id,
                "security": system.security,
                "coords": system.coords,
                "gates": [dest.id for dest in system.gates],
                "faction": system.faction.id if system.faction else -1
            }
            for system in g.eve.universe.systems() if not system.is_whspace
        },
        "regions": {
            region.id: {
                "name": region.name,
                "faction": region.faction.id if region.faction else -1
            }
            for region in g.eve.universe.regions() if not region.is_whspace
        },
        "factions": {
            faction.id: {
                "name": faction.name
            }
            for faction in g.eve.universe.factions() if faction.territory
        }
    }
    resp = app.response_class(response=json.dumps(payload), status=200,
                              mimetype="application/json")
    resp.cache_control.private = True
    resp.cache_control.max_age = 24 * 60 * 60
    return resp
