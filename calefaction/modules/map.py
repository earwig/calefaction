# -*- coding: utf-8  -*-

from flask_mako import render_template

from ._provided import blueprint

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
