# -*- coding: utf-8  -*-

from .clock import Clock
from .image import ImageServer

__all__ = ["EVE"]

class EVE:

    def __init__(self):
        self._clock = Clock()
        self._image = ImageServer()

    @property
    def clock(self):
        return self._clock

    @property
    def image(self):
        return self._image
