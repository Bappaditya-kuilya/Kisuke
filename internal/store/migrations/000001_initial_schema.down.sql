-- 000001_initial_schema.down.sql
-- Rollback initial schema

DROP INDEX IF EXISTS idx_vault_links_entity;
DROP INDEX IF NOT EXISTS idx_vault_links_note;
DROP TABLE IF EXISTS vault_links;

DROP TABLE IF EXISTS notes_fts;
DROP TABLE IF EXISTS notes_fts_content;
DROP TABLE IF EXISTS notes_fts_data;
DROP TABLE IF EXISTS notes_fts_idx;
DROP TABLE IF EXISTS notes_fts_docsize;
DROP TABLE IF EXISTS notes_fts_config;

DROP TABLE IF EXISTS developer_profile;
DROP TABLE IF EXISTS context_history;
DROP TABLE IF EXISTS skill_progress;
DROP TABLE IF EXISTS mcp_connections;
DROP TABLE IF EXISTS calendar_events;