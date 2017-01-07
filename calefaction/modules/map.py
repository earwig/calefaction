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
        "galaxy": {
            system.id: {
                "name": system.name,
                "coords": system.coords,
                "security": system.security
            }
            for system in g.eve.universe.systems() if not system.is_whspace
        }
    }
    resp = app.response_class(response=json.dumps(payload), status=200,
                              mimetype="application/json")
    resp.cache_control.private = True
    resp.cache_control.max_age = 24 * 60 * 60
    return resp
