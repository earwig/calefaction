#! /usr/bin/env python3
# -*- coding: utf-8  -*-

from flask import Flask, g
from flask_mako import MakoTemplates, render_template

from calefaction.util import catch_errors, set_up_hash_versioning

app = Flask(__name__)

MakoTemplates(app)
set_up_hash_versioning(app)

@app.before_request
def prepare_request():
    g.something = None  # ...

@app.route("/")
@catch_errors(app)
def index():
    return render_template("landing.mako")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
