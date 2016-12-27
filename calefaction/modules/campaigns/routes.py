# -*- coding: utf-8  -*-

from flask import abort, g, redirect, request, url_for
from flask_mako import render_template

from .getters import get_current
from .._provided import blueprint, config

__all__ = ["home", "navitem", "current_campaign", "campaign", "operation",
           "set_campaign"]

def home():
    """Render and return the main campaign page."""
    current = get_current()
    if current:
        campaign = config["campaigns"][current]
        return render_template("campaigns/campaign.mako",
                               name=current, campaign=campaign, enabled=True)
    return render_template("campaigns/empty.mako")

def navitem():
    """Render and return the navigation item for this module."""
    current = get_current()
    if current:
        result = render_template("campaigns/navitem.mako", current=current)
        return result.decode("utf8")

@blueprint.rroute("/campaign")
def current_campaign():
    """Render and return the current campaign page."""
    current = get_current()
    if current:
        return redirect(url_for(".campaign", name=current), 303)
    return render_template("campaigns/empty.mako")

@blueprint.rroute("/campaigns/<name>")
def campaign(name):
    """Render and return a campaign page."""
    if name not in config["campaigns"]:
        abort(404)
    campaign = config["campaigns"][name]
    enabled = name in config["enabled"]
    return render_template("campaigns/campaign.mako",
                           name=name, campaign=campaign, enabled=enabled)

@blueprint.rroute("/campaigns/<cname>/operations/<opname>")
def operation(cname, opname):
    """Render and return an operation page."""
    if cname not in config["campaigns"]:
        abort(404)
    campaign = config["campaigns"][cname]
    if opname not in campaign["operations"]:
        abort(404)
    operation = campaign["operations"][opname]
    enabled = cname in config["enabled"] and opname in campaign["enabled"]
    return render_template("campaigns/operation.mako",
                           cname=cname, campaign=campaign, opname=opname,
                           operation=operation, enabled=enabled)

@blueprint.rroute("/settings/campaign", methods=["POST"])
def set_campaign():
    """Update the user's currently selected campaign."""
    campaign = request.form.get("campaign")
    if campaign not in config["enabled"]:
        abort(400)
    g.auth.set_character_modprop("campaigns", "current", campaign)
    return redirect(url_for(".campaign", name=campaign), 303)
