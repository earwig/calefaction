# -*- coding: utf-8  -*-

from datetime import datetime, timedelta

from flask import g, session, url_for
from itsdangerous import BadSignature, URLSafeSerializer

from . import baseLogger
from .exceptions import AccessDeniedError

__all__ = ["AuthManager"]

_SCOPES = ["publicData", "characterAssetsRead"]  # ...

class AuthManager:
    """Authentication manager. Handles user access and management."""
    EXPIRY_THRESHOLD = 30

    def __init__(self, config, eve):
        self._config = config
        self._eve = eve

        self._logger = baseLogger.getChild("auth")
        self._debug = self._logger.debug

    def _get_session_id(self):
        """Return the current session ID, allocating a new one if necessary."""
        if "id" not in session:
            session["id"] = g.db.new_session()
            self._debug("Allocated session id=%d", session["id"])
            g._session_checked = True
            g._session_expired = False
        return session["id"]

    def _invalidate_session(self):
        """Mark the current session as invalid.

        Remove it from the database and from the user's cookies.
        """
        if "id" in session:
            sid = session["id"]
            g.db.drop_session(sid)
            self._debug("Dropped session id=%d", sid)
            del session["id"]

    def _check_session(self):
        """Return whether the user has a valid, non-expired session.

        This checks for the session existing in the database, but does not
        check that the user is logged in or has any particular access roles.
        """
        if "id" not in session:
            return False

        if hasattr(g, "_session_checked"):
            return g._session_checked

        g._session_checked = check = g.db.has_session(session["id"])
        if not check:
            g._session_expired = True
            self._debug("Session expired id=%d", session["id"])
            self._invalidate_session()
        return check

    def _get_state_hash(self):
        """Return a hash of the user's session ID suitable for OAuth2 state.

        Allocates a new session ID if necessary.
        """
        key = self._config.get("auth.session_key")
        serializer = URLSafeSerializer(key)
        return serializer.dumps(self._get_session_id())

    def _verify_state_hash(self, state):
        """Confirm that a state hash is correct for the user's session.

        Assumes we've already checked the session ID. If the state is invalid,
        the session will be invalidated.
        """
        key = self._config.get("auth.session_key")
        serializer = URLSafeSerializer(key)
        try:
            value = serializer.loads(state)
        except BadSignature:
            self._debug("Bad signature for session id=%d", session["id"])
            self._invalidate_session()
            return False

        if value != session["id"]:
            self._debug("Got session id=%d, expected id=%d", value,
                        session["id"])
            self._invalidate_session()
            return False
        return True

    def _fetch_new_token(self, code, refresh=False):
        """Given an auth code or refresh token, get a new token and other data.

        If refresh is True, code should be a refresh token, otherwise an auth
        code. If successful, we'll return a 5-tuple of (access_token,
        token_expiry, refresh_token, char_id, char_name). If the token was
        invalid, we'll return None. We may also raise EVEAPIError if there was
        an internal API error.
        """
        cid = self._config.get("auth.client_id")
        secret = self._config.get("auth.client_secret")
        result = self._eve.sso.get_access_token(cid, secret, code, refresh)
        if not result:
            return None

        token, expiry, refresh = result
        expires = datetime.utcnow() + timedelta(seconds=expiry)

        result = self._eve.sso.get_character_info(token)
        if not result:
            return None

        char_id, char_name = result
        return token, expires, refresh, char_id, char_name

    def _get_token(self, cid):
        """Return a valid access token for the given character, or None.

        If the database doesn't have an auth entry for this character, return
        None. If the database's token is expired but the refresh token is
        valid, then refresh it, update the database, and return the new token.
        If the token has become invalid and couldn't be refreshed, drop the
        auth information from the database and return None.
        """
        result = g.db.get_auth(cid)
        if not result:
            self._debug("No auth info in database for char id=%d", cid)
            return None

        token, expires, refresh = result
        seconds_til_expiry = (expires - datetime.utcnow()).total_seconds()
        if seconds_til_expiry >= self.EXPIRY_THRESHOLD:
            self._debug("Using cached access token for char id=%d", cid)
            return token

        result = self._fetch_new_token(refresh, refresh=True)
        if not result:
            self._debug("Couldn't refresh token for char id=%d", cid)
            g.db.drop_auth(cid)
            return None

        token, expires, refresh, char_id, char_name = result
        if char_id != cid:
            self._debug("Refreshed token has incorrect char id=%d for "
                        "char id=%d", char_id, cid)
            g.db.drop_auth(cid)
            return None

        self._debug("Using fresh access token for char id=%d", cid)
        g.db.put_character(cid, char_name)
        g.db.update_auth(cid, token, expires, refresh)
        return token

    def _check_access(self, token, char_id):
        """"Check whether the given character is allowed to access this site.

        If allowed, do nothing. If not, raise AccessDeniedError.
        """
        resp = self._eve.esi(token).v3.characters(char_id).get()
        if resp.get("corporation_id") != self._config.get("corp.id"):
            self._debug("Access denied per corp membership for char id=%d "
                        "session id=%d", char_id, session["id"])
            g.db.drop_auth(char_id)
            self._invalidate_session()
            raise AccessDeniedError()

    def get_character_id(self):
        """Return the character ID associated with the current session.

        Returns None if the session is invalid or is not associated with a
        character.
        """
        if not self._check_session():
            return None

        if not hasattr(g, "_character_id"):
            g._character_id = g.db.read_session(session["id"])
        return g._character_id

    def get_character_prop(self, prop):
        """Look up a property for the current session's character.

        Returns None if the session is invalid, is not associated with a
        character, or the property has no non-default value.
        """
        cid = self.get_character_id()
        if not cid:
            return None

        if not hasattr(g, "_character_props"):
            g._character_props = g.db.read_character(cid)
        return g._character_props.get(prop)

    def is_authenticated(self):
        """Return whether the user has permission to access this site.

        We confirm that they have a valid, non-expired session that is
        associated with a character that is permitted to be here.

        EVEAPIError or AccessDeniedError may be raised.
        """
        if "id" in session:
            self._debug("Checking auth for session id=%d", session["id"])

        cid = self.get_character_id()
        if not cid:
            return False

        token = self._get_token(cid)
        if not token:
            self._debug("No valid token for char id=%d session id=%d", cid,
                        session["id"])
            self._invalidate_session()
            return False

        self._check_access(token, cid)

        self._debug("Access granted for char id=%d session id=%d", cid,
                    session["id"])
        g.db.touch_session(session["id"])
        return True

    def make_login_link(self):
        """Return a complete EVE SSO link that the user can use to log in."""
        cid = self._config.get("auth.client_id")
        target = url_for("login", _external=True, _scheme=self._config.scheme)
        scopes = _SCOPES
        state = self._get_state_hash()
        return self._eve.sso.get_authorize_url(cid, target, scopes, state)

    def handle_login(self, code, state):
        """Given an OAuth2 code and state, try to authenticate the user.

        If the user has a legitimate session and the state is valid, we'll
        check the code with EVE SSO to fetch an authentication token. If the
        token corresponds to a character that is allowed to access the site,
        we'll update their session to indicate so.

        Return whether authentication was successful. EVEAPIError or
        AccessDeniedError may be raised.
        """
        if not code or not state:
            return False

        if "id" in session:
            self._debug("Logging in session id=%d", session["id"])
        if not self._check_session():
            return False
        if not self._verify_state_hash(state):
            return False

        sid = session["id"]
        result = self._fetch_new_token(code)
        if not result:
            self._debug("Couldn't fetch token for session id=%d", sid)
            self._invalidate_session()
            return False

        token, expires, refresh, char_id, char_name = result
        self._check_access(token, char_id)

        self._debug("Logged in char id=%d session id=%d", char_id, sid)
        g.db.put_character(char_id, char_name)
        g.db.set_auth(char_id, token, expires, refresh)
        g.db.attach_session(sid, char_id)
        g.db.touch_session(sid)
        return True

    def handle_logout(self):
        """Log out the user if they are logged in.

        Invalidates their session and clears the session cookie.
        """
        if "id" in session:
            self._debug("Logging out session id=%d", session["id"])

        self._invalidate_session()
        session.clear()
