# -*- coding: utf-8  -*-

from flask import abort, g
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
    return render_template("campaigns/campaign.mako", current=get_current())

def navitem():
    current = get_current()
    if current:
        result = render_template("campaigns/navitem.mako", current=current)
        return result.decode("utf8")

@blueprint.rroute("/campaign")
def campaign():
    return home()

@blueprint.rroute("/settings/campaign/<campaign>", methods=["POST"])
def set_campaign(campaign):
    if campaign not in config["enabled"]:
        abort(404)
    g.auth.set_character_modprop("campaigns", "current", campaign)
    return "", 204
