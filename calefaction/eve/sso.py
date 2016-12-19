# -*- coding: utf-8  -*-

from urllib.parse import urlencode

import requests

from ..exceptions import EVEAPIError

__all__ = ["SSOManager"]

class SSOManager:
    """EVE API module for Single Sign-On (SSO)."""

    def __init__(self, session):
        self._session = session

    def get_authorize_url(self, client_id, redirect_uri, scopes=None,
                          state=None):
        """Return a URL that the end user can use to start a login."""
        baseurl = "https://login.eveonline.com/oauth/authorize?"
        params = {
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "client_id": client_id
        }
        if scopes:
            params["scope"] = " ".join(scopes)
        if state is not None:
            params["state"] = state
        return baseurl + urlencode(params)

    def get_access_token(self, client_id, client_secret, code, refresh=False):
        """Given an auth code or refresh token, return an access token.

        If refresh is True, code should be a refresh token. Otherwise, it
        should be an authorization code.

        Does a step of OAuth2 and returns a 3-tuple of (access_token,
        token_expiry, refresh_token) if successful. Returns None if one of the
        arguments is not valid. Raises EVEAPIError if the API did not respond
        in a sensible way or looks to be down.
        """
        url = "https://login.eveonline.com/oauth/token"
        params = {"code": code}
        if refresh:
            params["grant_type"] = "refresh_token"
        else:
            params["grant_type"] = "authorization_code"

        try:
            resp = self._session.post(url, data=params, timeout=10,
                                      auth=(client_id, client_secret))
            json = resp.json()
        except (requests.RequestException, ValueError):
            raise EVEAPIError()

        if not resp.ok or "error" in json:
            return None

        if json.get("token_type") != "Bearer":
            raise EVEAPIError()

        token = json.get("access_token")
        expiry = json.get("expires_in")
        refresh = json.get("refresh_token")

        if not token or not expiry or not refresh:
            raise EVEAPIError()

        return token, expiry, refresh

    def get_character_info(self, token):
        """Given an access token, return character info.

        If successful, returns a 2-tuple of (character_id, character_name).
        Returns None if the token isn't valid. Raises EVEAPIError if the API
        did not respond in a sensible way or looks to be down.
        """
        url = "https://login.eveonline.com/oauth/verify"
        headers = {"Authorization": "Bearer " + token}
        try:
            resp = self._session.get(url, timeout=10, headers=headers)
            json = resp.json()
        except (requests.RequestException, ValueError):
            raise EVEAPIError()

        if not resp.ok or "error" in json:
            return None

        char_id = json.get("CharacterID")
        char_name = json.get("CharacterName")

        if not char_id or not char_name:
            raise EVEAPIError()

        return char_id, char_name
