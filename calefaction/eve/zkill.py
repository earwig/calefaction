# -*- coding: utf-8  -*-

import time

from flask import g
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

    def _extend_killmail(self, kill):
        """Extend a killmail object to match the old ZKill format.

        Requires ESI API calls to fill in entity names. If we can't do them,
        we'll just set the names to be empty.
        """
        esi = g.eve.esi
        victim = kill["victim"]

        if "character_id" in victim:
            char_info = esi().v4.characters(victim["character_id"]).get()
            victim["character_name"] = char_info["name"]
        else:
            victim["character_id"] = 0
            victim["character_name"] = ""

        if "corporation_id" in victim:
            corp_info = esi().v3.corporations(victim["corporation_id"]).get()
            victim["corporation_name"] = corp_info["corporation_name"]
        else:
            victim["corporation_id"] = 0
            victim["corporation_name"] = ""

        if "alliance_id" in victim:
            alliance_info = esi().v2.alliances(victim["alliance_id"]).get()
            victim["alliance_name"] = alliance_info["alliance_name"]
        else:
            victim["alliance_id"] = 0
            victim["alliance_name"] = ""

        if "faction_id" in victim:
            factions = esi().v1.universe.factions.get()
            matches = [fac["name"] for fac in factions
                       if fac["faction_id"] == victim["faction_id"]]
            victim["faction_name"] = matches[0] if matches else ""
        else:
            victim["faction_id"] = 0
            victim["faction_name"] = ""

        return kill

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
            try:
                resp = self._session.get(url, timeout=10)
            except requests.ConnectionError:
                self._logger.warn("zKillboard API query failed, retrying once")
                time.sleep(self._MAX_RATE)
                resp = self._session.get(url, timeout=10)
            resp.raise_for_status()
            result = resp.json() if resp.content else None
        except (requests.RequestException, ValueError):
            self._logger.exception("zKillboard API query failed")
            raise ZKillboardError()

        self._last_query = time.time()
        return result

    def iter_killmails(self, *args, extended=False):
        """Return an iterator over killmails using the given API arguments.

        Automagically follows pagination as far as possible. (Be careful.)

        If extended is True, we will provide extra information for each kill
        (names of entities instead of just IDs), which requires ESI API calls.
        This matches the original API format of ZKill before it was, er,
        "simplified".
        """
        page = 1
        while True:
            if page > 1:
                result = self.query(*args, "page", page)
            else:
                result = self.query(*args)

            if result:
                if extended:
                    for kill in result:
                        yield self._extend_killmail(kill)
                else:
                    yield from result
                page += 1
            else:
                break
