# -*- coding: utf-8  -*-

from datetime import datetime

__all__ = ["Clock"]

YEAR_DELTA = 1898

class Clock:

    def now(self):
        dt = datetime.utcnow()
        return str(dt.year - YEAR_DELTA) + dt.strftime("-%m-%d %H:%M")
