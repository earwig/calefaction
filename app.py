#! /usr/bin/env python3
# -*- coding: utf-8  -*-

from pathlib import Path

from flask import Flask, g, redirect, request, url_for
from flask_mako import MakoTemplates, render_template

import calefaction
from calefaction.auth import AuthManager
from calefaction.config import Config
from calefaction.database import Database
from calefaction.eve import EVE
from calefaction.exceptions import AccessDeniedError, EVEAPIError
from calefaction.util import catch_errors, set_up_asset_versioning

app = Flask(__name__)

basepath = Path(__file__).resolve().parent
config = Config(basepath / "config")
Database.path = str(basepath / "data" / "db.sqlite3")
eve = EVE(config)
auth = AuthManager(config, eve)

MakoTemplates(app)
set_up_asset_versioning(app)
config.install(app)

@app.before_request
def prepare_request():
    g.auth = auth
    g.config = config
    g.eve = eve
    g.version = calefaction.__version__

app.before_request(Database.pre_hook)
app.teardown_appcontext(Database.post_hook)

@app.route("/")
@catch_errors(app)
def index():
    ...  # handle flashed error messages in _base.mako
    if auth.is_authenticated():  # ... need to check for exceptions
        return render_template("home.mako")
    return render_template("landing.mako")

@app.route("/login", methods=["GET", "POST"])
@catch_errors(app)
def login():
    code = request.args.get("code")
    state = request.args.get("state")
    try:
        auth.handle_login(code, state)
    except EVEAPIError:
        ...  # flash error message
    except AccessDeniedError:
        ...  # flash error message
    if getattr(g, "_session_expired"):
        ...  # flash error message
    return redirect(url_for("index"), 303)

# @app.route("/logout") ...

# @auth.route_restricted ...
# check for same exceptions as login() and use same flashes

if __name__ == "__main__":
    app.run(debug=True, port=8080)
