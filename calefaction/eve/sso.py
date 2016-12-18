# -*- coding: utf-8  -*-

from urllib.parse import urlencode

__all__ = ["SSOManager"]

class SSOManager:

    def get_authorize_url(self, client_id, redirect_uri, scopes=None,
                          state=None):
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
