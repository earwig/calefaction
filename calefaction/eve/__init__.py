# -*- coding: utf-8  -*-

import platform

import requests

from .clock import Clock
from .esi import EVESwaggerInterface
from .image import ImageServer
from .sso import SSOManager
from .. import __release__

__all__ = ["EVE"]

class EVE:
    """Interface to EVE's various APIs."""

    def __init__(self, config):
        session = requests.Session()
        agent = self._get_user_agent(config.get("site.contact"))
        session.headers["User-Agent"] = agent

        self._clock = Clock()
        self._esi = EVESwaggerInterface(session)
        self._image = ImageServer()
        self._sso = SSOManager(session)

    @staticmethod
    def _get_user_agent(contact):
        """Return the user agent when accessing APIs."""
        template = ("Calefaction/{} ({}; Python/{}; {}; "
                    "https://github.com/earwig/calefaction)")
        return template.format(
            __release__, requests.utils.default_user_agent(),
            platform.python_version(), contact)

    @property
    def clock(self):
        """The Clock API module."""
        return self._clock

    @property
    def esi(self):
        """The EVE Swagger Interface API module."""
        return self._esi

    @property
    def image(self):
        """The ImageServer API module."""
        return self._image

    @property
    def sso(self):
        """The Single Sign-On API module."""
        return self._sso
