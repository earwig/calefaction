# -*- coding: utf-8  -*-

from datetime import datetime
import sqlite3

from flask import g
from werkzeug.local import LocalProxy

__all__ = ["CampaignDB"]

class CampaignDB:
    """Database manager for internal storage for the Campaigns module."""
    path = None

    def __init__(self):
        if self.path is None:
            raise RuntimeError("CampaignDB.path not set")
        self._conn = sqlite3.connect(self.path)

    @classmethod
    def _get(cls):
        """Return the current database, or allocate a new one if necessary."""
        if not hasattr(g, "_campaign_db"):
            g._campaign_db = cls()
        return g._campaign_db

    @classmethod
    def pre_hook(cls):
        """Hook to be called before a request context.

        Sets up the g.campaign_db proxy.
        """
        g.campaign_db = LocalProxy(cls._get)

    @classmethod
    def post_hook(cls, exc):
        """Hook to be called when tearing down an application context.

        Closes the database if necessary.
        """
        if hasattr(g, "_campaign_db"):
            g._campaign_db.close()

    def close(self):
        """Close the database connection."""
        return self._conn.close()

    def check_operation(self, campaign, operation):
        """Return the last updated timestamp for the given operation.

        Return None if the given operation was never updated.
        """
        query = """SELECT lu_date FROM last_updated
            WHERE lu_campaign = ? AND lu_operation = ?"""
        res = self._conn.execute(query, (campaign, operation)).fetchall()
        if not res:
            return None
        return datetime.strptime(res[0][0], "%Y-%m-%d %H:%M:%S")

    def add_operation(self, campaign, operation):
        """Insert a new operation into the database as just updated."""
        with self._conn as conn:
            conn.execute("""INSERT INTO last_updated
                (lu_campaign, lu_operation) VALUES (?, ?)""", (
                    campaign, operation))

    def touch_operation(self, campaign, operation):
        """Mark the given operation as just updated."""
        with self._conn as conn:
            conn.execute("""UPDATE last_updated SET lu_date = CURRENT_TIMESTAMP
                WHERE lu_campaign = ? AND lu_operation = ?""", (
                    campaign, operation))

    def set_overview(self, campaign, operation, primary, secondary=None):
        """Set overview information for this operation."""
        with self._conn as conn:
            conn.execute("""INSERT OR REPLACE INTO overview
                (ov_campaign, ov_operation, ov_primary, ov_secondary)
                VALUES (?, ?, ?, ?)""", (
                    campaign, operation, primary, secondary))

    def get_overview(self, campaign, operation):
        """Return a 2-tuple of overview information for this operation."""
        query = """SELECT ov_primary, ov_secondary FROM overview
            WHERE ov_campaign = ? AND ov_operation = ?"""
        res = self._conn.execute(query, (campaign, operation)).fetchall()
        return res[0] if res else (0, None)
