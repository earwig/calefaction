# -*- coding: utf-8  -*-

from urllib.parse import urlencode

import requests

from ..exceptions import EVEAPIError

__all__ = ["EVESwaggerInterface"]

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

    def get(self):
        """Do an HTTP GET request for the built query."""
        return self._esi.get(self._path, self._token)

    def post(self, **kwargs):
        """Do an HTTP POST request for the built query."""
        return self._esi.post(self._path, self._token, data=kwargs)

    def put(self, **kwargs):
        """Do an HTTP PUT request for the built query."""
        return self._esi.put(self._path, self._token, data=kwargs)

    def delete(self):
        """Do an HTTP DELETE request for the built query."""
        return self._esi.delete(self._path, self._token)


class EVESwaggerInterface:
    """EVE API module for the EVE Swagger Interface (ESI).

    There are two equivalent ways to use this interface:

    data = esi.get("/v3/characters/{char_id}/".format(char_id=char_id), token)
    data = esi(token).v3.characters(char_id).get()

    For more complex requests:

    data = esi.post("/v1/universe/names/", token, {"ids": [entity_id]})
    data = esi(token).v1.universe.names.post(ids=[entity_id]})
    """

    def __init__(self, session):
        self._session = session
        self._base_url = "https://esi.tech.ccp.is"
        self._data_source = "tranquility"

    def __call__(self, token):
        return _ESIQueryBuilder(self, token)

    def _do(self, query, data, token, method):
        """Execute a query using a token with the given session method.

        Return the JSON result, if any. Raise EVEAPIError for any errors.
        """
        ...  # cache requests

        params = {"datasource": self._data_source}
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token
        }
        url = self._base_url + query + "?" + urlencode(params)

        try:
            resp = method(url, json=data or None, timeout=10, headers=headers)
            resp.raise_for_status()
            return resp.json() if resp.content else None
        except (requests.RequestException, ValueError) as exc:
            raise EVEAPIError(str(exc))

    def get(self, query, token):
        """Do an HTTP GET request for a query using a token."""
        return self._do(query, None, token, self._session.get)

    def post(self, query, token, data=None):
        """Do an HTTP POST request for a query using a token."""
        return self._do(query, data, token, self._session.post)

    def put(self, query, token, data=None):
        """Do an HTTP PUT request for a query using a token."""
        return self._do(query, data, token, self._session.put)

    def delete(self, query, token):
        """Do an HTTP DELETE request for a query using a token."""
        return self._do(query, None, token, self._session.delete)
