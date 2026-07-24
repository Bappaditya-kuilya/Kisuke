-- Rollback initial schema
DROP INDEX IF EXISTS idx_vault_links_entity;
DROP INDEX IF EXISTS idx_vault_links_note;
DROP TABLE IF EXISTS vault_links;

DROP TABLE IF EXISTS notes_fts;

DROP TABLE IF EXISTS developer_profile;

DROP INDEX IF EXISTS idx_context_history_session;
DROP TABLE IF EXISTS context_history;

DROP TABLE IF EXISTS skill_progress;

DROP TABLE IF EXISTS mcp_connections;

DROP INDEX IF EXISTS idx_calendar_events_time;
DROP INDEX IF EXISTS idx_calendar_events_tag;
DROP TABLE IF EXISTS calendar_events;