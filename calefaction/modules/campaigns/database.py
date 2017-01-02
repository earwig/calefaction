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
        """Return the last updated timestamp and key for the given operation.

        Return (None, None) if the given operation was never updated.
        """
        query = """SELECT lu_date, lu_key FROM last_updated
            WHERE lu_campaign = ? AND lu_operation = ?"""
        res = self._conn.execute(query, (campaign, operation)).fetchall()
        if not res:
            return None, None
        return datetime.strptime(res[0][0], "%Y-%m-%d %H:%M:%S"), res[0][1]

    def touch_operation(self, campaign, operation, key=None):
        """Mark the given operation as just updated, or add it."""
        with self._conn as conn:
            cur = conn.execute("BEGIN TRANSACTION")
            cur.execute("""UPDATE last_updated
                SET lu_date = CURRENT_TIMESTAMP, lu_key = ?
                WHERE lu_campaign = ? AND lu_operation = ?""", (
                    key, campaign, operation))
            if cur.rowcount == 0:
                cur.execute("""INSERT INTO last_updated
                    (lu_campaign, lu_operation, lu_key) VALUES (?, ?, ?)""", (
                        campaign, operation, key))

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
        return tuple(res[0]) if res else (0, None)

    def has_kill(self, kill_id):
        """Return whether the database has a killmail with the given ID."""
        query = "SELECT 1 FROM kill WHERE kill_id = ?"
        res = self._conn.execute(query, (kill_id,)).fetchall()
        return bool(res)

    def add_kill(self, kill):
        """Insert a killmail into the database."""
        try:
            datetime.strptime(kill["killTime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise RuntimeError("Invalid kill_date=%s for kill_id=%d" % (
                kill["killTime"], kill["killID"]))

        query = """INSERT OR REPLACE INTO kill (
                kill_id, kill_date, kill_system, kill_victim_shipid,
                kill_victim_charid, kill_victim_charname, kill_victim_corpid,
                kill_victim_corpname, kill_victim_allianceid,
                kill_victim_alliancename, kill_victim_factionid,
                kill_victim_factionname, kill_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        victim = kill["victim"]
        args = (
            int(kill["killID"]), kill["killTime"], int(kill["solarSystemID"]),
            int(victim["shipTypeID"]), int(victim["characterID"]),
            victim["characterName"], int(victim["corporationID"]),
            victim["corporationName"], int(victim["allianceID"]),
            victim["allianceName"], int(victim["factionID"]),
            victim["factionName"], float(kill["zkb"]["totalValue"]))
        with self._conn as conn:
            conn.execute(query, args)

    def get_kill_associations(self, campaign, kill_id):
        """Return a list of operations associated with a campaign and kill."""
        query = """SELECT ok_operation FROM oper_kill
            WHERE ok_campaign = ? AND ok_killid = ?"""
        res = self._conn.execute(query, (campaign, kill_id)).fetchall()
        return [row[0] for row in res]

    def associate_kill(self, campaign, kill_id, operations):
        """Associate a killmail with a set of campaign/operations."""
        query = """INSERT OR IGNORE INTO oper_kill
            (ok_campaign, ok_operation, ok_killid) VALUES (?, ?, ?)"""
        arglist = [(campaign, op, kill_id) for op in operations]
        with self._conn as conn:
            conn.executemany(query, arglist)

    def count_kills(self, campaign, operation):
        """Return the number of matching kills and the total kill value."""
        query = """SELECT COUNT(*), TOTAL(kill_value)
            FROM oper_kill
            JOIN kill ON ok_killid = kill_id
            WHERE ok_campaign = ? AND ok_operation = ?"""
        res = self._conn.execute(query, (campaign, operation)).fetchall()
        return tuple(res[0])

    def get_associated_kills(self, campaign, operation, sort="new", limit=-1,
                             offset=0):
        """Return a list of kills associated with a campaign/operation.

        Kills are returned as dictionaries, up to a limit. Use -1 for no limit.
        The sort should be "new" for most recent first, "old" for most recent
        last, or "value" for most valuable first.
        """
        sortkeys = {
            "new": "ok_killid DESC",
            "old": "ok_killid ASC",
            "value": "kill_value DESC, ok_killid DESC"
        }
        if sort in sortkeys:
            sortkey = sortkeys[sort]
        else:
            raise ValueError(sort)
        if not isinstance(limit, int):
            raise ValueError(limit)
        if not isinstance(offset, int):
            raise ValueError(offset)

        query = """SELECT kill_id, kill_date, kill_system, kill_victim_shipid,
                kill_victim_charid, kill_victim_charname, kill_victim_corpid,
                kill_victim_corpname, kill_victim_allianceid,
                kill_victim_alliancename, kill_victim_factionid,
                kill_victim_factionname, kill_value
            FROM oper_kill
            JOIN kill ON ok_killid = kill_id
            WHERE ok_campaign = ? AND ok_operation = ?
            ORDER BY {} LIMIT {} OFFSET {}"""
        qform = query.format(sortkey, limit, offset)
        res = self._conn.execute(qform, (campaign, operation)).fetchall()

        return [{
            "id": row[0],
            "date": datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"),
            "system": row[2],
            "victim": {
                "ship_id": row[3],
                "char_id": row[4],
                "char_name": row[5],
                "corp_id": row[6],
                "corp_name": row[7],
                "alliance_id": row[8],
                "alliance_name": row[9],
                "faction_id": row[10],
                "faction_name": row[11]
            },
            "value": row[12]
        } for row in res]

    def update_items(self, campaign, data):
        """Update all item details in the database for the given campaign.

        The data should be a multi-layered dictionary. It maps operation names
        to a dict that maps character IDs to a dict that maps type IDs to
        tuples of integer counts and float values.
        """
        with self._conn as conn:
            cur = conn.execute("BEGIN TRANSACTION")
            query = "DELETE FROM oper_item WHERE oi_campaign = ?"
            cur.execute(query, (campaign,))

            query = """INSERT INTO oper_item (
                    oi_campaign, oi_operation, oi_character, oi_type, oi_count,
                    oi_value)
                VALUES (?, ?, ?, ?, ?, ?)"""
            cur.executemany(query, [
                (campaign, operation, int(char_id), int(type_id), int(count),
                 float(value))
                for operation, chars in data.items()
                for char_id, types in chars.items()
                for type_id, (count, value) in types.items()])

    def get_associated_items(self, campaign, operation, sort="value", limit=-1,
                             offset=0):
        """Return a list of items associated with a campaign/operation.

        Items are returned as 2-tuples of (item_type, item_count), up to a
        limit. Use -1 for no limit. The sort should be "value" for most
        valuable first (individual item value * quantity), "quantity" for
        greatest quantity first, "price" for most valuable items first.
        """
        sortkeys = {
            "value": "total_value DESC",
            "quantity": "total_count DESC",
            "price": "(total_value / total_count) DESC"
        }
        if sort in sortkeys:
            sortkey = sortkeys[sort]
        else:
            raise ValueError(sort)
        if not isinstance(limit, int):
            raise ValueError(limit)
        if not isinstance(offset, int):
            raise ValueError(offset)

        query = """SELECT oi_type, SUM(oi_count) AS total_count,
                TOTAL(oi_value) as total_value
            FROM oper_item
            WHERE oi_campaign = ? AND oi_operation = ?
            GROUP BY oi_type ORDER BY {} LIMIT {} OFFSET {}"""
        qform = query.format(sortkey, limit, offset)
        res = self._conn.execute(qform, (campaign, operation)).fetchall()
        return [(type_id, count or 0, value) for type_id, count, value in res]
