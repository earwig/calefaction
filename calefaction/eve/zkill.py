# -*- coding: utf-8  -*-

import time

import requests

from ..exceptions import ZKillboardError

__all__ = ["ZKillboard"]

class ZKillboard:
    """EVE API module for zKillboard."""
    _MAX_RATE = 0.5

    def __init__(self, session, logger):
        self._session = session
        self._logger = logger
        self._debug = logger.debug

        self._base_url = "https://zkillboard.com/api"
        self._last_query = 0

    def query(self, *args):
        """Make an API query using the given arguments."""
        query = "/" + "".join(str(arg) + "/" for arg in args)
        url = self._base_url + query
        delta = self._MAX_RATE - (time.time() - self._last_query)
        if delta > 0:
            self._debug("[GET] [wait %.2fs] %s", delta, query)
            time.sleep(delta)
        else:
            self._debug("[GET] %s", query)

        try:
            resp = self._session.get(url, timeout=10)
            resp.raise_for_status()
            result = resp.json() if resp.content else None
        except (requests.RequestException, ValueError):
            self._logger.exception("zKillboard API query failed")
            raise ZKillboardError()

        self._last_query = time.time()
        return result

    def iter_killmails(self, *args):
        """Return an iterator over killmails using the given API arguments.

        Automagically follows pagination as far as possible. (Be careful.)
        """
        page = 1
        while True:
            if page > 1:
                result = self.query(*args, "page", page)
            else:
                result = self.query(*args)

            if result:
                yield from result
                page += 1
            else:
                break
