# -*- coding: utf-8  -*-

import yaml

__all__ = ["Config"]

class Config:
    """Stores application-wide configuration info."""

    def __init__(self, confdir):
        self._filename = confdir / "config.yml"
        self._data = None
        self._load()

    def _load(self):
        """Load config from the config file."""
        with self._filename.open("rb") as fp:
            self._data = yaml.load(fp)

    def get(self, key="", default=None):
        """Acts like a dict lookup in the config file.

        Dots can be used to separate keys. For example,
        config["foo.bar"] == config["foo"]["bar"].
        """
        obj = self._data
        for item in key.split("."):
            if item not in obj:
                return default
            obj = obj[item]
        return obj

    @property
    def scheme(self):
        """Return the site's configured scheme, either "http" or "https"."""
        return "https" if self.get("site.https") else "http"

    def install(self, app):
        """Install relevant config parameters into the application."""
        app.config["SERVER_NAME"] = self.get("site.canonical")
        app.config["PREFERRED_URL_SCHEME"] = self.scheme
        app.secret_key = self.get("auth.session_key")
