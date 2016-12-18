#! /usr/bin/env python3
# -*- coding: utf-8  -*-

from pathlib import Path

from flask import Flask, g
from flask_mako import MakoTemplates, render_template
from werkzeug.local import LocalProxy

import calefaction
from calefaction.auth import AuthManager
from calefaction.config import Config
from calefaction.database import Database
from calefaction.eve import EVE
from calefaction.util import catch_errors, set_up_hash_versioning

app = Flask(__name__)

basepath = Path(__file__).resolve().parent
config = Config(basepath / "config")
Database.path = str(basepath / "data" / "db.sqlite3")
eve = EVE()
auth = AuthManager(config, eve)

MakoTemplates(app)
set_up_hash_versioning(app)
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
    return render_template("landing.mako")

@app.route("/login")
@catch_errors(app)
def login():
    return "login"  # ...

if __name__ == "__main__":
    app.run(debug=True, port=8080)
