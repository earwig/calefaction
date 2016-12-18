# -*- coding: utf-8  -*-

from flask import g, session, url_for
from itsdangerous import URLSafeSerializer

__all__ = ["AuthManager"]

_SCOPES = ["publicData", "characterAssetsRead"]  # ...

class AuthManager:

    def __init__(self, config, eve):
        self._config = config
        self._eve = eve

    def _new_session_id(self):
        with g.db as conn:
            cur = conn.execute("INSERT INTO session DEFAULT VALUES")
            return cur.lastrowid

    def get_session_id(self):
        if "id" not in session:
            session["id"] = self._new_session_id()
        return session["id"]

    def get_state_hash(self):
        key = self._config.get("auth.session_key")
        serializer = URLSafeSerializer(key)
        return serializer.dumps(self.get_session_id())

    def make_login_link(self):
        cid = self._config.get("auth.client_id")
        target = url_for("login", _external=True, _scheme=self._config.scheme)
        scopes = _SCOPES
        state = self.get_state_hash()
        return self._eve.sso.get_authorize_url(cid, target, scopes, state)
