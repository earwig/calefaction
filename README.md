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

    cp config.yml.sample config.yml
    vim config.yml
    ...

### Test

    ./app.py
    # go to http://localhost:8080

### Deploy

    ...
