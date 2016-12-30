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
    mkdir logs
    sudo chmod 0600 config/config.yml data/db.sqlite3
    sudo chown www-data:www-data config/config.yml data data/db.sqlite3 logs
    ...  # TODO: convert these into scripts, add SDE instructions, add module instructions

### Test

    export FLASK_APP=`pwd`/app.py
    export FLASK_DEBUG=1
    flask run
    # go to http://localhost:5000

### Deploy

    uwsgi --ini config/uwsgi.ini
    # proxy to http://127.0.0.1:9001
