package store

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

type sqliteStore struct {
	db *sql.DB
}

func NewStore(dbPath string) (Store, error) {
	// Skip filesystem operations for in-memory databases
	isMemory := dbPath == ":memory:"

	if !isMemory {
		// Ensure parent directory has restrictive permissions
		dbDir := filepath.Dir(dbPath)
		if err := os.MkdirAll(dbDir, 0o700); err != nil {
			return nil, fmt.Errorf("create db directory: %w", err)
		}

		// Set restrictive permissions on database file if it exists
		if _, err := os.Stat(dbPath); err == nil {
			if err := os.Chmod(dbPath, 0o600); err != nil {
				return nil, fmt.Errorf("chmod db file: %w", err)
			}
		}
	}

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("open db: %w", err)
	}

	db.SetMaxOpenConns(1)

	s := &sqliteStore{db: db}
	if err := s.initSchema(); err != nil {
		db.Close()
		return nil, fmt.Errorf("init schema: %w", err)
	}

	// Ensure database file has restrictive permissions after creation
	if !isMemory {
		if err := os.Chmod(dbPath, 0o600); err != nil {
			return nil, fmt.Errorf("chmod db file: %w", err)
		}
	}

	return s, nil
}

func (s *sqliteStore) initSchema() error {
	// Create migrations table first
	if _, err := s.db.Exec(`
		CREATE TABLE IF NOT EXISTS migrations (
			version INTEGER PRIMARY KEY,
			description TEXT NOT NULL,
			applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
		);
	`); err != nil {
		return fmt.Errorf("create migrations table: %w", err)
	}

	// For in-memory databases, we can't use file-based migrations
	// Just run the initial schema directly
	// TODO: Use proper migration library for file-based databases
	schema := `
	CREATE TABLE IF NOT EXISTS vault_links (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		vault_note_path TEXT NOT NULL,
		vault_note_title TEXT NOT NULL,
		kisuke_entity_type TEXT NOT NULL,
		kisuke_entity_id TEXT NOT NULL,
		link_type TEXT DEFAULT 'reference',
		confidence REAL DEFAULT 0.8,
		created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
		UNIQUE(vault_note_path, kisuke_entity_type, kisuke_entity_id)
	);

	CREATE INDEX IF NOT EXISTS idx_vault_links_entity ON vault_links(kisuke_entity_type, kisuke_entity_id);
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
	`

	if _, err := s.db.Exec(schema); err != nil {
		return fmt.Errorf("exec schema: %w", err)
	}

	return nil
}

func (s *sqliteStore) Migrate() error {
	return s.initSchema()
}

func (s *sqliteStore) InitSchema() error {
	return s.initSchema()
}

func (s *sqliteStore) SetDefaultProfile() error {
	defaults := map[string]string{
		"name":            "Bappaditya Kuilya",
		"role":            "AI Engineer (aspiring)",
		"goal":            "Become elite engineer, master Docker, PostgreSQL, DSA, build resume projects",
		"build_style":     "Clean architecture, test-driven, well-documented, minimal deps",
		"preferred_stack": "Go, Python, SQLite, Docker, PostgreSQL",
		"learning_focus":  "Docker, PostgreSQL, DSA, System Design, AI/ML",
		"vault_path":      "/mnt/d/Obsidian Vault/AI Research",
		"kisuke_db":       "",
	}

	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	stmt, err := tx.Prepare(`
		INSERT INTO developer_profile (key, value) VALUES (?, ?)
		ON CONFLICT(key) DO NOTHING
	`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for k, v := range defaults {
		if _, err := stmt.Exec(k, v); err != nil {
			return err
		}
	}

	return tx.Commit()
}

func (s *sqliteStore) LogContextInjection(sessionID, context string) error {
	_, err := s.db.Exec(`
		INSERT INTO context_history (session_id, injected_context)
		VALUES (?, ?)
	`, sessionID, context)
	return err
}

func (s *sqliteStore) Close() error {
	return s.db.Close()
}

func (s *sqliteStore) DB() *sql.DB {
	return s.db
}

func (s *sqliteStore) SearchVaultNotes(query string, limit int) ([]VaultLink, error) {
	if limit <= 0 {
		limit = 10
	}

	rows, err := s.db.Query(`
		SELECT vl.id, vl.vault_note_path, vl.vault_note_title, vl.kisuke_entity_type, vl.kisuke_entity_id,
		       vl.link_type, vl.confidence, vl.created_at, vl.updated_at
		FROM vault_links vl
		WHERE vl.vault_note_path IN (
			SELECT path FROM notes_fts WHERE notes_fts MATCH ? ORDER BY rank LIMIT ?
		)
		ORDER BY vl.confidence DESC
	`, query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var links []VaultLink
	for rows.Next() {
		var l VaultLink
		if err := rows.Scan(&l.ID, &l.VaultNotePath, &l.VaultNoteTitle, &l.KisukeEntityType, &l.KisukeEntityID,
			&l.LinkType, &l.Confidence, &l.CreatedAt, &l.UpdatedAt); err != nil {
			return nil, err
		}
		links = append(links, l)
	}
	return links, nil
}

func (s *sqliteStore) SearchVaultNotesDirect(query string, limit int) ([]VaultLink, error) {
	if limit <= 0 {
		limit = 10
	}

	rows, err := s.db.Query(`
		SELECT path, title, content, rank
		FROM notes_fts
		WHERE notes_fts MATCH ?
		ORDER BY rank
		LIMIT ?
	`, query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var links []VaultLink
	for rows.Next() {
		var path, title, content string
		var rank float64
		if err := rows.Scan(&path, &title, &content, &rank); err != nil {
			return nil, err
		}
		links = append(links, VaultLink{
			VaultNotePath:    path,
			VaultNoteTitle:   title,
			KisukeEntityType: "inferred",
			KisukeEntityID:   "",
			LinkType:         "inferred",
			Confidence:       0.4,
			CreatedAt:        "",
			UpdatedAt:        "",
		})
	}
	return links, nil
}

func (s *sqliteStore) GetUpcomingEvents(hours int, projectTag string) ([]CalendarEvent, error) {
	query := `
		SELECT id, summary, description, start_time, end_time, calendar_id, project_tag, synced_at
		FROM calendar_events
		WHERE start_time > datetime('now') AND start_time < datetime('now', ?)
	`
	args := []any{fmt.Sprintf("+%d hours", hours)}

	if projectTag != "" {
		query += ` AND project_tag = ?`
		args = append(args, projectTag)
	}

	query += ` ORDER BY start_time LIMIT 50`

	rows, err := s.db.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []CalendarEvent
	for rows.Next() {
		var e CalendarEvent
		if err := rows.Scan(&e.ID, &e.Summary, &e.Description, &e.StartTime, &e.EndTime, &e.CalendarID, &e.ProjectTag, &e.SyncedAt); err != nil {
			return nil, err
		}
		events = append(events, e)
	}
	return events, nil
}

func (s *sqliteStore) SyncCalendarEvents(events []CalendarEvent) error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	stmt, err := tx.Prepare(`
		INSERT INTO calendar_events (id, summary, description, start_time, end_time, calendar_id, project_tag, synced_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(id) DO UPDATE SET
			summary = excluded.summary,
			description = excluded.description,
			start_time = excluded.start_time,
			end_time = excluded.end_time,
			calendar_id = excluded.calendar_id,
			project_tag = excluded.project_tag,
			synced_at = CURRENT_TIMESTAMP
	`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for _, e := range events {
		_, err := stmt.Exec(e.ID, e.Summary, e.Description, e.StartTime.Format(time.RFC3339), e.EndTime.Format(time.RFC3339), e.CalendarID, e.ProjectTag, time.Now().Format(time.RFC3339))
		if err != nil {
			return err
		}
	}

	return tx.Commit()
}

func (s *sqliteStore) GetVaultLinksByEntity(entityType, entityID string) ([]VaultLink, error) {
	rows, err := s.db.Query(`
		SELECT id, vault_note_path, vault_note_title, kisuke_entity_type, kisuke_entity_id, link_type, confidence, created_at, updated_at
		FROM vault_links
		WHERE kisuke_entity_type = ? AND kisuke_entity_id = ?
		ORDER BY confidence DESC
	`, entityType, entityID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var links []VaultLink
	for rows.Next() {
		var l VaultLink
		if err := rows.Scan(&l.ID, &l.VaultNotePath, &l.VaultNoteTitle, &l.KisukeEntityType, &l.KisukeEntityID,
			&l.LinkType, &l.Confidence, &l.CreatedAt, &l.UpdatedAt); err != nil {
			return nil, err
		}
		links = append(links, l)
	}
	return links, nil
}

func (s *sqliteStore) GetVaultLinksByNote(notePath string) ([]VaultLink, error) {
	rows, err := s.db.Query(`
		SELECT id, vault_note_path, vault_note_title, kisuke_entity_type, kisuke_entity_id, link_type, confidence, created_at, updated_at
		FROM vault_links
		WHERE vault_note_path = ?
		ORDER BY confidence DESC
	`, notePath)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var links []VaultLink
	for rows.Next() {
		var l VaultLink
		if err := rows.Scan(&l.ID, &l.VaultNotePath, &l.VaultNoteTitle, &l.KisukeEntityType, &l.KisukeEntityID,
			&l.LinkType, &l.Confidence, &l.CreatedAt, &l.UpdatedAt); err != nil {
			return nil, err
		}
		links = append(links, l)
	}
	return links, nil
}

func (s *sqliteStore) CreateVaultLink(notePath, noteTitle, entityType, entityID, linkType string, confidence float64) error {
	_, err := s.db.Exec(`
		INSERT INTO vault_links (vault_note_path, vault_note_title, kisuke_entity_type, kisuke_entity_id, link_type, confidence)
		VALUES (?, ?, ?, ?, ?, ?)
		ON CONFLICT(vault_note_path, kisuke_entity_type, kisuke_entity_id) DO UPDATE SET
			confidence = excluded.confidence,
			link_type = excluded.link_type,
			updated_at = CURRENT_TIMESTAMP
	`, notePath, noteTitle, entityType, entityID, linkType, confidence)
	return err
}

func (s *sqliteStore) DeleteVaultLink(notePath, entityType, entityID string) error {
	_, err := s.db.Exec(`
		DELETE FROM vault_links
		WHERE vault_note_path = ? AND kisuke_entity_type = ? AND kisuke_entity_id = ?
	`, notePath, entityType, entityID)
	return err
}

func (s *sqliteStore) IndexVaultNote(path, title, content string) error {
	_, err := s.db.Exec(`DELETE FROM notes_fts WHERE path = ?`, path)
	if err != nil {
		return err
	}
	_, err = s.db.Exec(`
		INSERT INTO notes_fts (path, title, content) VALUES (?, ?, ?)
	`, path, title, content)
	return err
}

func (s *sqliteStore) RemoveVaultNoteIndex(path string) error {
	_, err := s.db.Exec(`DELETE FROM notes_fts WHERE path = ?`, path)
	return err
}

func (s *sqliteStore) GetAllProfile() (map[string]string, error) {
	rows, err := s.db.Query(`SELECT key, value FROM developer_profile`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	profile := make(map[string]string)
	for rows.Next() {
		var key, value string
		if err := rows.Scan(&key, &value); err != nil {
			return nil, err
		}
		profile[key] = value
	}
	return profile, nil
}

func (s *sqliteStore) GetProfile(key string) (string, error) {
	var value string
	err := s.db.QueryRow(`SELECT value FROM developer_profile WHERE key = ?`, key).Scan(&value)
	if err == sql.ErrNoRows {
		return "", nil
	}
	return value, err
}

func (s *sqliteStore) SetProfile(key, value string) error {
	_, err := s.db.Exec(`
		INSERT INTO developer_profile (key, value) VALUES (?, ?)
		ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
	`, key, value)
	return err
}

func (s *sqliteStore) DeleteProfile(key string) error {
	_, err := s.db.Exec(`DELETE FROM developer_profile WHERE key = ?`, key)
	return err
}

func (s *sqliteStore) GetSkillProgress() ([]SkillProgress, error) {
	rows, err := s.db.Query(`
		SELECT skill_name, current_level, target_level, last_practiced, streak_days, total_sessions, updated_at
		FROM skill_progress
		ORDER BY skill_name
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var skills []SkillProgress
	for rows.Next() {
		var sp SkillProgress
		if err := rows.Scan(&sp.Name, &sp.CurrentLevel, &sp.TargetLevel, &sp.LastPracticed, &sp.StreakDays, &sp.TotalSessions, &sp.UpdatedAt); err != nil {
			return nil, err
		}
		skills = append(skills, sp)
	}
	return skills, nil
}

func (s *sqliteStore) UpdateSkillProgress(skill string, level int, practiced bool) error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var currentLevel, streak, total int
	var lastPracticed sql.NullTime

	err = tx.QueryRow(`
		SELECT current_level, streak_days, total_sessions, last_practiced
		FROM skill_progress WHERE skill_name = ?
	`, skill).Scan(&currentLevel, &streak, &total, &lastPracticed)

	if err == sql.ErrNoRows {
		_, err = tx.Exec(`
			INSERT INTO skill_progress (skill_name, current_level, last_practiced, streak_days, total_sessions)
			VALUES (?, ?, ?, 1, 1)
		`, skill, level, time.Now())
		if err != nil {
			return err
		}
		return tx.Commit()
	}
	if err != nil {
		return err
	}

	newLevel := currentLevel
	if level > currentLevel {
		newLevel = level
	}

	newStreak := streak
	if practiced {
		if lastPracticed.Valid && time.Since(lastPracticed.Time) <= 48*time.Hour {
			newStreak = streak + 1
		} else if !lastPracticed.Valid || time.Since(lastPracticed.Time) > 48*time.Hour {
			newStreak = 1
		}
	}

	_, err = tx.Exec(`
		UPDATE skill_progress SET current_level = ?, last_practiced = ?, streak_days = ?, total_sessions = total_sessions + 1
		WHERE skill_name = ?
	`, newLevel, time.Now(), newStreak, skill)
	if err != nil {
		return err
	}

	return tx.Commit()
}

func (s *sqliteStore) AddMCPConnection(conn MCPConnection) error {
	_, err := s.db.Exec(`
		INSERT INTO mcp_connections (name, command, args, env, enabled)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(name) DO UPDATE SET command = excluded.command, args = excluded.args, env = excluded.env, enabled = excluded.enabled
	`, conn.Name, conn.Command, conn.Args, conn.Env, conn.Enabled)
	return err
}

func (s *sqliteStore) GetMCPConnections() ([]MCPConnection, error) {
	rows, err := s.db.Query(`SELECT name, command, args, env, enabled FROM mcp_connections WHERE enabled = 1 ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var conns []MCPConnection
	for rows.Next() {
		var c MCPConnection
		if err := rows.Scan(&c.Name, &c.Command, &c.Args, &c.Env, &c.Enabled); err != nil {
			return nil, err
		}
		conns = append(conns, c)
	}
	return conns, nil
}

func (s *sqliteStore) DeleteMCPConnection(name string) error {
	_, err := s.db.Exec(`DELETE FROM mcp_connections WHERE name = ?`, name)
	return err
}

func (s *sqliteStore) RateContextHistory(id int64, rating int, feedback string) error {
	_, err := s.db.Exec(`
		UPDATE context_history SET user_rating = ?, user_feedback = ? WHERE id = ?
	`, rating, feedback, id)
	return err
}

func (s *sqliteStore) GetContextHistory(sessionID string) ([]ContextHistoryEntry, error) {
	rows, err := s.db.Query(`
		SELECT id, session_id, injected_context, user_rating, user_feedback, created_at
		FROM context_history
		WHERE session_id = ?
		ORDER BY created_at DESC
		LIMIT 20
	`, sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var entries []ContextHistoryEntry
	for rows.Next() {
		var e ContextHistoryEntry
		if err := rows.Scan(&e.ID, &e.SessionID, &e.InjectedContext, &e.UserRating, &e.UserFeedback, &e.CreatedAt); err != nil {
			return nil, err
		}
		entries = append(entries, e)
	}
	return entries, nil
}

func (s *sqliteStore) GetStats() (map[string]int64, error) {
	stats := make(map[string]int64)
	tables := []string{"vault_links", "developer_profile", "context_history", "skill_progress", "mcp_connections", "calendar_events", "notes_fts"}
	for _, table := range tables {
		var count int64
		err := s.db.QueryRow(fmt.Sprintf("SELECT COUNT(*) FROM %s", table)).Scan(&count)
		if err != nil {
			continue
		}
		stats[table] = count
	}
	return stats, nil
}

func (s *sqliteStore) Vacuum() error {
	_, err := s.db.Exec(`VACUUM`)
	return err
}

func (s *sqliteStore) GetAllVaultLinks() ([]VaultLink, error) {
	rows, err := s.db.Query(`
		SELECT id, vault_note_path, vault_note_title, kisuke_entity_type, kisuke_entity_id, link_type, confidence, created_at, updated_at
		FROM vault_links
		ORDER BY confidence DESC, updated_at DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var links []VaultLink
	for rows.Next() {
		var l VaultLink
		if err := rows.Scan(&l.ID, &l.VaultNotePath, &l.VaultNoteTitle, &l.KisukeEntityType, &l.KisukeEntityID, &l.LinkType, &l.Confidence, &l.CreatedAt, &l.UpdatedAt); err != nil {
			return nil, err
		}
		links = append(links, l)
	}
	return links, nil
}