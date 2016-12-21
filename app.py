#! /usr/bin/env python3
# -*- coding: utf-8  -*-

from pathlib import Path

from flask import Flask, abort, flash, g, redirect, request, url_for
from flask_mako import MakoTemplates, render_template

import calefaction
from calefaction.auth import AuthManager
from calefaction.config import Config
from calefaction.database import Database
from calefaction.eve import EVE
from calefaction.messages import Messages
from calefaction.util import (
    try_func, make_error_catcher, make_route_restricter,
    set_up_asset_versioning)

app = Flask(__name__)

basepath = Path(__file__).resolve().parent
config = Config(basepath / "config")
Database.path = str(basepath / "data" / "db.sqlite3")
eve = EVE(config)
auth = AuthManager(config, eve)

catch_exceptions = make_error_catcher(app, "error.mako")
route_restricted = make_route_restricter(
    auth, lambda: redirect(url_for("index"), 303))

MakoTemplates(app)
set_up_asset_versioning(app)
config.install(app)
calefaction.enable_logging()

@app.before_request
def prepare_request():
    g.auth = auth
    g.config = config
    g.eve = eve
    g.version = calefaction.__version__

app.before_request(Database.pre_hook)
app.teardown_appcontext(Database.post_hook)

@app.route("/")
@catch_exceptions
def index():
    success, _ = try_func(auth.is_authenticated)
    if success:
        return render_template("home.mako")
    return render_template("landing.mako")

@app.route("/login", methods=["GET", "POST"])
@catch_exceptions
def login():
    code = request.args.get("code")
    state = request.args.get("state")

    success, caught = try_func(lambda: auth.handle_login(code, state))
    if success:
        flash(Messages.LOGGED_IN, "success")
    elif not caught:
        flash(Messages.LOGIN_FAILED, "error")
    return redirect(url_for("index"), 303)

@app.route("/logout", methods=["GET", "POST"])
@catch_exceptions
def logout():
    if request.method == "GET":
        return render_template("logout.mako")

    auth.handle_logout()
    flash(Messages.LOGGED_OUT, "success")
    return redirect(url_for("index"), 303)

@app.route("/settings/style/<style>", methods=["POST"])
@catch_exceptions
@route_restricted
def set_style(style):
    if not auth.set_character_style(style):
        abort(404)
    return "", 204

@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.mako"), 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)
