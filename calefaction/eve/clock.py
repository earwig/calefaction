# -*- coding: utf-8  -*-

from datetime import datetime

__all__ = ["Clock"]

_YEAR_DELTA = 1898

class Clock:
    """EVE API module for the in-game clock."""

    def now(self):
        """Return the current date and time in the YC calendar as a string."""
        dt = datetime.utcnow()
        return str(dt.year - _YEAR_DELTA) + dt.strftime("-%m-%d %H:%M")
