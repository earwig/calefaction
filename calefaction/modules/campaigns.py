# -*- coding: utf-8  -*-

from flask import abort, g, redirect, request, url_for
from flask_mako import render_template

from ._provided import blueprint, config

def get_current():
    """Return the name of the currently selected campaign, or None."""
    if not config["enabled"]:
        return None
    setting = g.auth.get_character_modprop("campaigns", "current")
    if not setting or setting not in config["enabled"]:
        return config["enabled"][0]
    return setting

def home():
    """Render and return the main campaign page."""
    current = get_current()
    if current:
        campaign = config["campaigns"][current]
        return render_template(
            "campaigns/campaign.mako", name=current, campaign=campaign)
    return render_template("campaigns/empty.mako")

def navitem():
    """Render and return the navigation item for this module."""
    current = get_current()
    if current:
        result = render_template("campaigns/navitem.mako", current=current)
        return result.decode("utf8")

@blueprint.rroute("/campaign")
def campaign():
    """Render and return the current campaign page."""
    return home()

@blueprint.rroute("/settings/campaign", methods=["POST"])
def set_campaign():
    """Update the user's currently selected campaign."""
    campaign = request.form.get("campaign")
    if campaign not in config["enabled"]:
        abort(400)
    g.auth.set_character_modprop("campaigns", "current", campaign)
    return redirect(url_for(".campaign"), 303)
