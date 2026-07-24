-- Add migration tracking table
-- Version: 2
-- Description: Add migration tracking table for version management

CREATE TABLE IF NOT EXISTS migrations (
    version INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO migrations (version, description) VALUES (1, 'Initial schema');