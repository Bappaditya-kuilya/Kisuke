package context

import (
	"database/sql"
	"time"
)

type ProjectContext struct {
	ProjectID   string `json:"project_id"`
	ProjectName string `json:"project_name"`
	Mission     string `json:"mission,omitempty"`
}

type ForgottenNote struct {
	Path       string  `json:"path"`
	Title      string  `json:"title"`
	Snippet    string  `json:"snippet"`
	Confidence float64 `json:"confidence"`
	Reason     string  `json:"reason"`
	EntityType string  `json:"entity_type"`
	EntityID   string  `json:"entity_id"`
}

type CalendarEvent struct {
	ID         string    `json:"id"`
	Summary    string    `json:"summary"`
	StartTime  time.Time `json:"start_time"`
	EndTime    time.Time `json:"end_time"`
	ProjectTag string    `json:"project_tag,omitempty"`
}

type SkillStatus struct {
	Name         string `json:"name"`
	CurrentLevel int    `json:"current_level"`
	TargetLevel  int    `json:"target_level"`
	StreakDays   int    `json:"streak_days"`
	LastPracticed string `json:"last_practiced,omitempty"`
}

type CodePattern struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Relevance   string `json:"relevance"`
}

type InjectedContext struct {
	SessionID        string           `json:"session_id"`
	ProjectFocus     *ProjectContext  `json:"project_focus,omitempty"`
	ForgottenNotes   []ForgottenNote  `json:"forgotten_notes"`
	TodayEvents      []CalendarEvent  `json:"today_events"`
	Profile          map[string]string `json:"profile"`
	SkillProgress    []SkillStatus    `json:"skill_progress"`
	RelevantPatterns []CodePattern    `json:"relevant_patterns,omitempty"`
	TokenEstimate    int              `json:"token_estimate"`
	GeneratedAt      time.Time        `json:"generated_at"`
}

type VaultLink struct {
	ID                int64
	VaultNotePath     string
	VaultNoteTitle    string
	KisukeEntityType  string
	KisukeEntityID    string
	LinkType          string
	Confidence        float64
	CreatedAt         time.Time
	UpdatedAt         time.Time
}

type SkillProgress struct {
	Name          string
	CurrentLevel  int
	TargetLevel   int
	LastPracticed sql.NullTime
	StreakDays    int
	TotalSessions int
	UpdatedAt     time.Time
}

type MCPConnection struct {
	Name    string
	Command string
	Args    string
	Env     string
	Enabled bool
}

type ContextHistoryEntry struct {
	ID              int64
	SessionID       string
	InjectedContext string
	UserRating      sql.NullInt64
	UserFeedback    sql.NullString
	CreatedAt       time.Time
}

type CalendarEventStore struct {
	ID          string
	Summary     string
	Description string
	StartTime   time.Time
	EndTime     time.Time
	CalendarID  string
	ProjectTag  string
	SyncedAt    time.Time
}