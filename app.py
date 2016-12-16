#! /usr/bin/env python3
# -*- coding: utf-8  -*-

from pathlib import Path

from flask import Flask, g
from flask_mako import MakoTemplates, render_template

import calefaction
from calefaction.config import Config
from calefaction.eve import EVE
from calefaction.util import catch_errors, set_up_hash_versioning

basepath = Path(__file__).resolve().parent
app = Flask(__name__)
config = Config(basepath / "config")
eve = EVE()

MakoTemplates(app)
set_up_hash_versioning(app)

@app.before_request
def prepare_request():
    g.config = config
    g.eve = eve
    g.version = calefaction.__version__

@app.route("/")
@catch_errors(app)
def index():
    return render_template("landing.mako")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
