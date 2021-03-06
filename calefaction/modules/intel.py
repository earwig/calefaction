# -*- coding: utf-8  -*-

from flask_mako import render_template

from ._provided import blueprint

def home():
    """Render and return the main intel page."""
    return render_template("intel/intel.mako")

def navitem():
    """Render and return the navigation item for this module."""
    return render_template("intel/navitem.mako").decode("utf8")

@blueprint.rroute("/intel")
def intel():
    """Render and return the main intel page."""
    return home()
