-- Schema for Calefaction's Campaign module's internal database

DROP TABLE IF EXISTS last_updated;

CREATE TABLE last_updated (
    lu_campaign TEXT,
    lu_operation TEXT,
    lu_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lu_key INTEGER DEFAULT NULL,
    UNIQUE (lu_campaign, lu_operation)
);

DROP TABLE IF EXISTS overview;

CREATE TABLE overview (
    ov_campaign TEXT,
    ov_operation TEXT,
    ov_primary INTEGER DEFAULT 0,
    ov_secondary REAL DEFAULT NULL,
    UNIQUE (ov_campaign, ov_operation)
);

DROP TABLE IF EXISTS kill;

CREATE TABLE kill (
    kill_id INTEGER PRIMARY KEY,
    kill_date TIMESTAMP,
    kill_system INTEGER,
    kill_victim_shipid INTEGER,
    kill_victim_charid INTEGER,
    kill_victim_charname TEXT,
    kill_victim_corpid INTEGER,
    kill_victim_corpname TEXT,
    kill_victim_allianceid INTEGER,
    kill_victim_alliancename TEXT,
    kill_victim_factionid INTEGER,
    kill_victim_factionname TEXT,
    kill_value REAL
);

DROP TABLE IF EXISTS oper_kill;

CREATE TABLE oper_kill (
    ok_campaign TEXT,
    ok_operation TEXT,
    ok_killid INTEGER,
    UNIQUE (ok_campaign, ok_operation, ok_killid),
    FOREIGN KEY (ok_killid) REFERENCES kill (kill_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX ok_campaign_operation ON oper_kill (ok_campaign, ok_operation);
CREATE INDEX ok_campaign_killid    ON oper_kill (ok_campaign, ok_killid);

DROP TABLE IF EXISTS oper_item;

CREATE TABLE oper_item (
    oi_campaign TEXT,
    oi_operation TEXT,
    oi_character INTEGER,
    oi_type INTEGER,
    oi_count INTEGER,
    oi_value REAL,
    UNIQUE (oi_campaign, oi_operation, oi_character, oi_type)
);

CREATE INDEX oi_campaign_operation ON oper_item (oi_campaign, oi_operation);
