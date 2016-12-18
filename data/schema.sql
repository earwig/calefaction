-- Schema for Calefaction's internal database

DROP TABLE IF EXISTS session;

CREATE TABLE session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_character INTEGER DEFAULT 0,
    session_touched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS character;

CREATE TABLE character (
    character_id INTEGER PRIMARY KEY,
    character_name TEXT,
    character_token BLOB,
    character_refresh BLOB,
    character_token_expiry TIMESTAMP,
    character_last_verify TIMESTAMP,
    character_style TEXT
);
