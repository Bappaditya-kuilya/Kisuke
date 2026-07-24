package store

import (
	"database/sql"
	"time"
)

type Store interface {
	InitSchema() error
	SetDefaultProfile() error
	Close() error
	DB() *sql.DB

	// Vault links
	SearchVaultNotes(query string, limit int) ([]VaultLink, error)
	SearchVaultNotesDirect(query string, limit int) ([]VaultLink, error)
	GetVaultLinksByEntity(entityType, entityID string) ([]VaultLink, error)
	GetVaultLinksByNote(notePath string) ([]VaultLink, error)
	CreateVaultLink(notePath, noteTitle, entityType, entityID, linkType string, confidence float64) error
	DeleteVaultLink(notePath, entityType, entityID string) error
	IndexVaultNote(path, title, content string) error
	RemoveVaultNoteIndex(path string) error

	// Profile
	GetAllProfile() (map[string]string, error)
	GetProfile(key string) (string, error)
	SetProfile(key, value string) error
	DeleteProfile(key string) error

	// Skill progress
	GetSkillProgress() ([]SkillProgress, error)
	UpdateSkillProgress(skill string, level int, practiced bool) error

	// MCP connections
	AddMCPConnection(conn MCPConnection) error
	GetMCPConnections() ([]MCPConnection, error)
	DeleteMCPConnection(name string) error

	// Calendar
	GetUpcomingEvents(hours int, projectTag string) ([]CalendarEvent, error)
	SyncCalendarEvents(events []CalendarEvent) error

	// Context history
	LogContextInjection(sessionID, context string) error
	RateContextHistory(id int64, rating int, feedback string) error
	GetContextHistory(sessionID string) ([]ContextHistoryEntry, error)
	GetAllVaultLinks() ([]VaultLink, error)

	// Stats
	GetStats() (map[string]int64, error)
	Vacuum() error
}

type VaultLink struct {
	ID               int64
	VaultNotePath    string
	VaultNoteTitle   string
	KisukeEntityType string
	KisukeEntityID   string
	LinkType         string
	Confidence       float64
	CreatedAt        string
	UpdatedAt        string
}

type SkillProgress struct {
	Name          string
	CurrentLevel  int
	TargetLevel   int
	LastPracticed sql.NullTime
	StreakDays    int
	TotalSessions int
	UpdatedAt     string
}

type MCPConnection struct {
	Name    string
	Command string
	Args    string
	Env     string
	Enabled bool
}

type CalendarEvent struct {
	ID          string
	Summary     string
	Description string
	StartTime   time.Time
	EndTime     time.Time
	CalendarID  string
	ProjectTag  string
	SyncedAt    time.Time
}

type ContextHistoryEntry struct {
	ID              int64
	SessionID       string
	InjectedContext string
	UserRating      sql.NullInt64
	UserFeedback    sql.NullString
	CreatedAt       time.Time
}