# -*- coding: utf-8  -*-

import importlib
import sys
from types import ModuleType

from flask import Blueprint

from . import baseLogger

__all__ = ["Module"]

class Module:
    """Handles common operations for Calefaction's modular components."""

    def __init__(self, config, name):
        self._config = config
        self._name = name
        self._logger = baseLogger.getChild("module").getChild(name)

        self._module = None
        self._blueprint = None

    def __getattr__(self, attr):
        return getattr(self._module, attr)

    def _import(self, app):
        """Set up the environment for the module, then import it."""
        base = "calefaction.modules"
        fullname = base + "." + self._name
        self._blueprint = bp = Blueprint(self._name, fullname)
        bp.rroute = lambda *a, **kw: (lambda f: bp.route(*a, **kw)(
            app.catch_exceptions(app.route_restricted(f))))

        provided = ModuleType(base + "._provided")
        provided.__package__ = base
        provided.app = app
        provided.blueprint = bp
        provided.config = self._config.load_module_config(self._name)
        provided.logger = self._logger
        sys.modules[provided.__name__] = provided

        self._module = importlib.import_module(fullname)
        del sys.modules[provided.__name__]

    def install(self, app):
        """Load this module and register it with the application."""
        self._import(app)
        app.register_blueprint(self._blueprint)

    def navitem(self):
        """Return a navigation bar HTML snippet for this module, or None."""
        if hasattr(self._module, "navitem"):
            return self._module.navitem()

    def scopes(self):
        """Return a set of SSO scopes required by this module."""
        if hasattr(self._module, "SCOPES"):
            return set(self._module.SCOPES)
        return set()
