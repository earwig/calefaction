-- Schema for Calefaction's internal database

DROP TABLE IF EXISTS character;

CREATE TABLE character (
    character_id INTEGER PRIMARY KEY,
    character_name TEXT,
    character_style TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS session;

CREATE TABLE session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_character INTEGER DEFAULT NULL,
    session_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_touched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_character) REFERENCES character (character_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

DROP TABLE IF EXISTS auth;

CREATE TABLE auth (
    auth_character INTEGER PRIMARY KEY,
    auth_token BLOB,
    auth_refresh BLOB,
    auth_token_expiry TIMESTAMP,
    FOREIGN KEY (auth_character) REFERENCES character (character_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS character_prop;

CREATE TABLE character_prop (
    cprop_character INTEGER,
    cprop_module TEXT,
    cprop_key TEXT,
    cprop_value TEXT,
    UNIQUE (cprop_character, cprop_module, cprop_key),
    FOREIGN KEY (cprop_character) REFERENCES character (character_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
