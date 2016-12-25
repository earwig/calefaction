# -*- coding: utf-8  -*-

from datetime import datetime
import random
from threading import Lock

import requests

from ..exceptions import EVEAPIError

__all__ = ["EVESwaggerInterface"]

class _ESICache:
    """Caches ESI API responses according to their headers.

    This interface is thread-safe.
    """
    EXPIRATION_RATE = 0.2

    def __init__(self):
        self._public = {}
        self._private = {}
        self._lock = Lock()

    @staticmethod
    def _get_cache_policy(resp):
        """Calculate the expiry and availability of the given response."""
        if "Cache-Control" not in resp.headers:
            return None

        directives = resp.headers["Cache-Control"].lower().split(";")
        directives = [d.strip() for d in directives]

        if "public" in directives:
            public = True
        elif "private" in directives:
            public = False
        else:
            return None

        expires = resp.headers.get("Expires")
        if not expires:
            return None

        try:
            expiry = datetime.strptime(expires, "%a, %d %b %Y %H:%M:%S GMT")
        except ValueError:
            return None

        return public, expiry

    @staticmethod
    def freeze_dict(d):
        """Return a hashable string key for the given dictionary."""
        if not d:
            return "{}"
        items = sorted((repr(str(k)), repr(str(v))) for k, v in d.items())
        return "{" + ",".join(":".join(p) for p in items) + "}"

    def _expire(self):
        """Remove old entries from the cache. Assumes lock is acquired."""
        now = datetime.utcnow()
        for index in (self._private, self._public):
            condemned = []
            for key, (expiry, _) in index.items():
                if expiry < now:
                    condemned.append(key)
            for key in condemned:
                del index[key]

    def fetch(self, key, token):
        """Try to look up a key in the cache. Return None if not found.

        The key should be a string. The token is used if a route is cached
        privately.

        This will periodically clear the cache of expired entries.
        """
        with self._lock:
            if random.random() < self.EXPIRATION_RATE:
                self._expire()

            if (key, token) in self._private:
                expiry, value = self._private[key, token]
                if expiry > datetime.utcnow():
                    return value

            if key in self._public:
                expiry, value = self._public[key]
                if expiry > datetime.utcnow():
                    return value

            return None

    def insert(self, key, token, value, response):
        """Store a key-value pair using the response as cache control."""
        policy = self._get_cache_policy(response)
        if not policy:
            return

        public, expiry = policy
        if expiry > datetime.utcnow():
            with self._lock:
                if public:
                    self._public[key] = (expiry, value)
                else:
                    self._private[key, token] = (expiry, value)


class _ESIQueryBuilder:
    """Stores an ESI query that is being built by the client."""

    def __init__(self, esi, token):
        self._esi = esi
        self._token = token
        self._path = "/"

    def __getattr__(self, item):
        self._path += str(item) + "/"
        return self

    def __call__(self, item):
        self._path += str(item) + "/"
        return self

    def get(self, **kwargs):
        """Do an HTTP GET request for the built query."""
        return self._esi.get(self._path, self._token, params=kwargs)

    def post(self, **kwargs):
        """Do an HTTP POST request for the built query."""
        return self._esi.post(self._path, self._token, data=kwargs)

    def put(self, **kwargs):
        """Do an HTTP PUT request for the built query."""
        return self._esi.put(self._path, self._token, data=kwargs)

    def delete(self, **kwargs):
        """Do an HTTP DELETE request for the built query."""
        return self._esi.delete(self._path, self._token, params=kwargs)


class EVESwaggerInterface:
    """EVE API module for the EVE Swagger Interface (ESI).

    There are two equivalent ways to use this interface:

    data = esi.get("/v3/characters/{char_id}/".format(char_id=char_id), token)
    data = esi(token).v3.characters(char_id).get()

    For more complex requests:

    data = esi.post("/v1/universe/names/", token, data={"ids": [entity_id]})
    data = esi(token).v1.universe.names.post(ids=[entity_id]})
    """

    def __init__(self, session, logger):
        self._session = session
        self._logger = logger
        self._debug = logger.debug

        self._base_url = "https://esi.tech.ccp.is"
        self._data_source = "tranquility"
        self._cache = _ESICache()

    def __call__(self, token):
        return _ESIQueryBuilder(self, token)

    def _do(self, method, query, params, data, token, can_cache=False):
        """Execute a query using a token with the given session method.

        Return the JSON result, if any. Raise EVEAPIError for any errors.
        """
        if can_cache:
            pkey = self._cache.freeze_dict(params)
            key = "|".join((method.__name__, self._data_source, query, pkey))
            cached = self._cache.fetch(key, token)
        else:
            cached = None

        self._debug("[%s] [%s] %s", method.__name__.upper(),
                    "fresh" if cached is None else "cache", query)
        if cached is not None:
            return cached

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token
        }
        params = params.copy() if params else {}
        params["datasource"] = self._data_source
        url = self._base_url + query

        try:
            resp = method(url, params=params, json=data or None,
                          headers=headers, timeout=10)
            resp.raise_for_status()
            result = resp.json() if resp.content else None
        except (requests.RequestException, ValueError):
            self._logger.exception("ESI request failed")
            raise EVEAPIError()

        if can_cache and result is not None:
            self._cache.insert(key, token, result, resp)
        return result

    def get(self, query, token, params=None):
        """Do an HTTP GET request for a query using a token."""
        meth = self._session.get
        return self._do(meth, query, params, None, token, True)

    def post(self, query, token, params=None, data=None):
        """Do an HTTP POST request for a query using a token."""
        meth = self._session.post
        return self._do(meth, query, params, data, token)

    def put(self, query, token, params=None, data=None):
        """Do an HTTP PUT request for a query using a token."""
        meth = self._session.put
        return self._do(meth, query, params, data, token)

    def delete(self, query, token, params=None):
        """Do an HTTP DELETE request for a query using a token."""
        meth = self._session.delete
        return self._do(meth, query, params, None, token)
