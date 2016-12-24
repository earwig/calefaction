# -*- coding: utf-8  -*-

import yaml

from .module import Module

__all__ = ["Config"]

class _ModuleIndex(list):
    """List class that supports attribute access to its elements by key."""

    def __init__(self):
        super().__init__()
        self._index = {}

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except TypeError:
            return super().__getitem__(self._index[key])

    def __getattr__(self, attr):
        return self[self._index[attr]]

    def append(self, key, value):
        self._index[key] = len(self)
        super().append(value)


class Config:
    """Stores application-wide configuration info."""

    def __init__(self, confdir):
        self._dir = confdir
        self._filename = confdir / "config.yml"
        self._data = None
        self._modules = _ModuleIndex()
        self._load()

    def _load(self):
        """Load config from the config file."""
        with self._filename.open("rb") as fp:
            self._data = yaml.load(fp)

        self._modules = _ModuleIndex()
        for name in self.get("modules.enabled", []):
            self._modules.append(name, Module(self, name))

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
    def modules(self):
        """Return a list-like object (a _ModuleIndex) of loaded modules."""
        return self._modules

    @property
    def scheme(self):
        """Return the site's configured scheme, either "http" or "https"."""
        return "https" if self.get("site.https") else "http"

    def install(self, app):
        """Install relevant config into the application, including modules."""
        app.config["SERVER_NAME"] = self.get("site.canonical")
        app.config["PREFERRED_URL_SCHEME"] = self.scheme
        app.secret_key = self.get("auth.session_key")

        for module in self.modules:
            module.install(app)

    def load_module_config(self, name):
        """Load and return a module config file.

        Returns a YAML parse of {confdir}/modules/{name}.yml, or None.
        """
        filename = self._dir / "modules" / (name + ".yml")
        try:
            with filename.open("rb") as fp:
                return yaml.load(fp)
        except FileNotFoundError:
            return None
