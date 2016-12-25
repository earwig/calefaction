# -*- coding: utf-8  -*-

from collections import namedtuple

from flask import g
from flask_mako import render_template

from ._provided import blueprint

SCOPES = {"esi-corporations.read_corporation_membership.v1"}

_Member = namedtuple("_Member", ["id", "name", "roles"])

def _weight(role):
    """Return an integer weight for the given role for sorting purposes."""
    if role == "CEO":
        return 0
    return 100

def get_members():
    """Return a list of the members of the user's corporation.

    Members are returned as 3-namedtuples of (id, name, roles). An empty list
    is returned if there was some error with tokens.
    """
    token = g.auth.get_token()
    if not token:
        return []

    corp_id = g.config.get("corp.id")
    resp = g.eve.esi(token).v2.corporations(corp_id).members.get()
    cids = ",".join(str(item["character_id"]) for item in resp)
    ceo_id = g.eve.esi(token).v2.corporations(corp_id).get()["ceo_id"]
    resp = g.eve.esi(token).v1.characters.names.get(character_ids=cids)

    members = [_Member(item["character_id"], item["character_name"],
                       "CEO" if item["character_id"] == ceo_id else None)
               for item in resp]
    members.sort(key=lambda m: (_weight(m.roles), m.name))
    return members

def home():
    """Render and return the main members page."""
    return render_template("members/members.mako", members=get_members())

def navitem():
    """Render and return the navigation item for this module."""
    return render_template("members/navitem.mako").decode("utf8")

@blueprint.rroute("/members")
def members():
    """Render and return the main members page."""
    return home()
