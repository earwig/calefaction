-- Schema for Calefaction's internal database

DROP TABLE IF EXISTS session;

CREATE TABLE session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_character INTEGER DEFAULT NULL,
    session_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_touched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS character;

CREATE TABLE character (
    character_id INTEGER PRIMARY KEY,
    character_name TEXT,
    character_style TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS auth;

CREATE TABLE auth (
    auth_character INTEGER PRIMARY KEY,
    auth_token BLOB,
    auth_refresh BLOB,
    auth_token_expiry TIMESTAMP
);
