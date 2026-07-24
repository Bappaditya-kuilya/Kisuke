-- 000001_initial_schema.up.sql
-- Initial schema for context-mcp

CREATE TABLE IF NOT EXISTS vault_links (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	vault_note_path TEXT NOT NULL,
	vault_note_title TEXT NOT NULL,
	entity_type TEXT NOT NULL,
	entity_id TEXT NOT NULL,
	link_type TEXT DEFAULT 'reference',
	confidence REAL DEFAULT 0.8,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	UNIQUE(vault_note_path, entity_type, entity_id)
);

CREATE INDEX IF NOT EXISTS idx_vault_links_entity ON vault_links(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_vault_links_note ON vault_links(vault_note_path);

CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
	path UNINDEXED,
	title,
	content,
	tokenize='porter'
);

CREATE TABLE IF NOT EXISTS developer_profile (
	key TEXT PRIMARY KEY,
	value TEXT NOT NULL,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS context_history (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	session_id TEXT NOT NULL,
	injected_context TEXT NOT NULL,
	user_rating INTEGER,
	user_feedback TEXT,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_context_history_session ON context_history(session_id);

CREATE TABLE IF NOT EXISTS skill_progress (
	skill_name TEXT PRIMARY KEY,
	current_level INTEGER DEFAULT 0,
	target_level INTEGER DEFAULT 5,
	last_practiced DATETIME,
	streak_days INTEGER DEFAULT 0,
	total_sessions INTEGER DEFAULT 0,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mcp_connections (
	name TEXT PRIMARY KEY,
	command TEXT NOT NULL,
	args TEXT DEFAULT '[]',
	env TEXT DEFAULT '{}',
	enabled BOOLEAN DEFAULT 1,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS calendar_events (
	id TEXT PRIMARY KEY,
	summary TEXT NOT NULL,
	description TEXT,
	start_time DATETIME NOT NULL,
	end_time DATETIME NOT NULL,
	calendar_id TEXT NOT NULL,
	project_tag TEXT,
	synced_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calendar_events_time ON calendar_events(start_time);
CREATE INDEX IF NOT EXISTS idx_calendar_events_tag ON calendar_events(project_tag);