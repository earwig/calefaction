calefaction
===========

__calefaction__ is a corporation manager and dashboard for the video game
[EVE Online](https://www.eveonline.com/).

Guide
-----

### Install

    git clone git@github.com:earwig/calefaction.git
    cd calefaction
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

### Setup

    cp config/config.yml.sample config/config.yml
    vim config/config.yml  # follow instructions
    cat data/schema.sql | sqlite3 data/db.sqlite3
    ...

### Test

    ./app.py
    # go to http://localhost:8080

### Deploy

    uwsgi --ini uwsgi.ini
    # proxy to 127.0.0.1:9001
