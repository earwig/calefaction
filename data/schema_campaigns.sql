-- Schema for Calefaction's Campaign module's internal database

DROP TABLE IF EXISTS last_updated;

CREATE TABLE last_updated (
    lu_campaign TEXT,
    lu_operation TEXT,
    lu_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (lu_campaign, lu_operation)
);

DROP TABLE IF EXISTS overview;

CREATE TABLE overview (
    ov_campaign TEXT,
    ov_operation TEXT,
    ov_primary INTEGER DEFAULT 0,
    ov_secondary INTEGER DEFAULT NULL,
    UNIQUE (ov_campaign, ov_operation)
);
