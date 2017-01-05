# -*- coding: utf-8  -*-

from datetime import datetime
import random
import sqlite3

from flask import current_app, g
from werkzeug.local import LocalProxy

__all__ = ["Database"]

class Database:
    """Database manager for low-level authentication actions."""
    MAX_SESSION_STALENESS = 7 * 24 * 60 * 60  # 7 days
    MAX_SESSION_AGE = 30 * 24 * 60 * 60  # 30 days
    SESSION_GRACE = 60 * 60  # 1 hour
    path = None

    def __init__(self):
        if self.path is None:
            raise RuntimeError("Database.path not set")
        self._conn = sqlite3.connect(self.path)

    def __enter__(self):
        return self._conn.__enter__()

    def __exit__(self, exc_type, exc_value, trace):
        return self._conn.__exit__(exc_type, exc_value, trace)

    @classmethod
    def _get(cls):
        """Return the current database, or allocate a new one if necessary."""
        if not hasattr(g, "_db"):
            g._db = cls()
        return g._db

    @classmethod
    def pre_hook(cls):
        """Hook to be called before a request context.

        Sets up the g.db proxy.
        """
        g.db = LocalProxy(cls._get)

    @classmethod
    def post_hook(cls, exc):
        """Hook to be called when tearing down an application context.

        Closes the database if necessary.
        """
        if hasattr(g, "_db"):
            g._db.close()

    def close(self):
        """Close the database connection."""
        return self._conn.close()

    def _clear_old_sessions(self):
        """Remove old sessions from the database.

        Sessions can expire if they are not touched (accessed) in a certain
        period of time, or if their absolute age exceeds some number. We don't
        actually remove them until a bit after this time.
        """
        if current_app.debug:
            return  # Sessions don't expire in debug mode

        query = """DELETE FROM session WHERE
            strftime("%s", "now") - strftime("%s", session_created) >= {} OR
            strftime("%s", "now") - strftime("%s", session_touched) >= {}"""
        create_thresh = self.MAX_SESSION_AGE + self.SESSION_GRACE
        touch_thresh = self.MAX_SESSION_STALENESS + self.SESSION_GRACE

        with self._conn as conn:
            conn.execute(query.format(create_thresh, touch_thresh))

    def _build_expiry_check(self):
        """Build and return a snippet of SQL to check for valid sessions.

        The SQL should be inserted in a WHERE clause. If debug mode is active,
        we just return an empty string.
        """
        if current_app.debug:
            return ""

        check = """ AND
            strftime("%s", "now") -
                strftime("%s", session_created) < {} AND
            strftime("%s", "now") -
                strftime("%s", session_touched) < {}"""
        return check.format(self.MAX_SESSION_AGE, self.MAX_SESSION_STALENESS)

    def new_session(self):
        """Allocate a new session in the database.

        Return its ID as an integer and creation timestamp as a naive UTC
        datetime.
        """
        created = datetime.utcnow().replace(microsecond=0)
        query = "INSERT INTO session (session_created) VALUES (?)"
        with self._conn as conn:
            cur = conn.execute(query, (created,))
            return cur.lastrowid, created

    def has_session(self, sid):
        """Return the creation timestamp for the given session ID, or None.

        Will only return a timestamp for non-expired sessions. This function
        randomly does database maintenance; very old expired sessions may be
        cleared.
        """
        if random.random() <= 0.2:
            self._clear_old_sessions()

        query = """SELECT session_created FROM session
            WHERE session_id = ?""" + self._build_expiry_check()
        res = self._conn.execute(query, (sid,)).fetchall()
        if not res:
            return None
        return datetime.strptime(res[0][0], "%Y-%m-%d %H:%M:%S")

    def read_session(self, sid):
        """Return the character associated with the given session, or None."""
        query = """SELECT session_character FROM session
            WHERE session_id = ?""" + self._build_expiry_check()
        res = self._conn.execute(query, (sid,)).fetchall()
        return res[0][0] if res else None

    def touch_session(self, sid):
        """Update the given session's last access timestamp."""
        query = """UPDATE session
            SET session_touched = CURRENT_TIMESTAMP
            WHERE session_id = ?"""

        with self._conn as conn:
            conn.execute(query, (sid,))

    def attach_session(self, sid, cid):
        """Attach the given session to a character. Does not touch it."""
        query = """UPDATE session
            SET session_character = ?
            WHERE session_id = ?"""

        with self._conn as conn:
            conn.execute(query, (cid, sid))

    def drop_session(self, sid):
        """Remove the given session from the database."""
        with self._conn as conn:
            conn.execute("DELETE FROM session WHERE session_id = ?", (sid,))

    def put_character(self, cid, name):
        """Put a character into the database if they don't already exist."""
        with self._conn as conn:
            cur = conn.execute("BEGIN TRANSACTION")
            cur.execute(
                """UPDATE character SET character_name = ?
                    WHERE character_id = ?""", (name, cid))
            if cur.rowcount == 0:
                cur.execute(
                    """INSERT INTO character (character_id, character_name)
                        VALUES (?, ?)""", (cid, name))

    def read_character(self, cid):
        """Return a dictionary of properties for the given character."""
        query = """SELECT character_name, character_style
            FROM character WHERE character_id = ?"""
        res = self._conn.execute(query, (cid,)).fetchall()
        return {"name": res[0][0], "style": res[0][1]} if res else {}

    def update_character(self, cid, prop, value):
        """Update a property for the given character."""
        props = {"name": "character_name", "style": "character_style"}
        field = props[prop]
        with self._conn as conn:
            conn.execute("""UPDATE character SET {} = ?
                WHERE character_id = ?""".format(field), (value, cid))

    def set_auth(self, cid, token, expires, refresh):
        """Set the authentication info for the given character."""
        with self._conn as conn:
            conn.execute("""INSERT OR REPLACE INTO auth
                (auth_character, auth_token, auth_token_expiry, auth_refresh)
                VALUES (?, ?, ?, ?)""", (cid, token, expires, refresh))

    def update_auth(self, cid, token, expires, refresh):
        """Update the authentication info for the given character.

        Functionally equivalent to set_auth provided that the character has an
        existing auth entry, but is more efficient.
        """
        with self._conn as conn:
            conn.execute("""UPDATE auth
                SET auth_token = ?, auth_token_expiry = ?, auth_refresh = ?
                WHERE auth_character = ?""", (token, expires, refresh, cid))

    def get_auth(self, cid):
        """Return authentication info for the given character.

        Return a 3-tuple of (access_token, token_expiry, refresh_token), or
        None if there is no auth info.
        """
        query = """SELECT auth_token, auth_token_expiry, auth_refresh
            FROM auth WHERE auth_character = ?"""
        res = self._conn.execute(query, (cid,)).fetchall()
        if not res:
            return None

        token, expiry, refresh = res[0]
        expires = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
        return token, expires, refresh

    def drop_auth(self, cid):
        """Drop any authentication info for the given character."""
        with self._conn as conn:
            conn.execute("DELETE FROM auth WHERE auth_character = ?", (cid,))

    def get_authed_characters(self):
        """Return a list of characters with authentication info.

        Each list item is a 4-tuple of (character_id, access_token,
        token_expiry, refresh_token).
        """
        query = """SELECT auth_character, auth_token, auth_token_expiry,
            auth_refresh FROM auth"""
        res = self._conn.execute(query).fetchall()
        dtparse = lambda dt: datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return [(cid, token, dtparse(expiry), refresh)
                for (cid, token, expiry, refresh) in res]

    def set_character_modprop(self, cid, module, prop, value):
        """Add or update a character module property."""
        with self._conn as conn:
            conn.execute("""INSERT OR REPLACE INTO character_prop
                (cprop_character, cprop_module, cprop_key, cprop_value)
                VALUES (?, ?, ?, ?)""", (cid, module, prop, value))

    def get_character_modprop(self, cid, module, prop):
        """Return the value of a character module property, or None."""
        query = """SELECT cprop_value FROM character_prop
            WHERE cprop_character = ? AND cprop_module = ? AND cprop_key = ?"""
        res = self._conn.execute(query, (cid, module, prop)).fetchall()
        return res[0][0] if res else None
