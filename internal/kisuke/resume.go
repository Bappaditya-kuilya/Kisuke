package kisuke

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"kisuke-mcp/internal/store"
)

// ProjectContext mirrors the context package type for the resume engine
type ProjectContext struct {
	ProjectID   string
	ProjectName string
	Mission     string
}

// ResumeEngine provides access to Kisuke's resume state
type ResumeEngine struct {
	repoPath string
	indexDB  string
}

func NewResumeEngine(repoPath, indexDB string) *ResumeEngine {
	return &ResumeEngine{
		repoPath: repoPath,
		indexDB:  indexDB,
	}
}

func (e *ResumeEngine) GetCurrentContext(ctx context.Context) (*ProjectContext, error) {
	// Try to read resume state from repo
	statePath := filepath.Join(e.repoPath, ".kisuke", "resume_state.json")
	if _, err := os.Stat(statePath); err == nil {
		if pc, err := e.readResumeState(statePath); err == nil {
			return pc, nil
		}
	}

	// Fallback: query index DB for active project
	if e.indexDB != "" {
		if pc, err := e.getActiveProjectFromIndex(ctx); err == nil && pc != nil {
			return pc, nil
		}
	}

	return nil, fmt.Errorf("no active project found")
}

func (e *ResumeEngine) readResumeState(path string) (*ProjectContext, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var rs ResumeState
	if err := json.Unmarshal(data, &rs); err != nil {
		return nil, err
	}

	if rs.FocusProjectID == "" {
		return nil, fmt.Errorf("no focus project")
	}

	// Get project details from index
	if e.indexDB == "" {
		return nil, fmt.Errorf("no index DB")
	}

	db, err := sql.Open("sqlite3", e.indexDB)
	if err != nil {
		return nil, err
	}
	defer db.Close()

	var title, mission string
	queryErr := db.QueryRow(`
		SELECT e.title, m.title 
		FROM entities e
		LEFT JOIN entities m ON e.owner = m.id AND m.type = 'mission'
		WHERE e.id = ? AND e.type = 'project'
	`, rs.FocusProjectID).Scan(&title, &mission)
	if queryErr != nil {
		return nil, queryErr
	}

	return &ProjectContext{
		ProjectID:   rs.FocusProjectID,
		ProjectName: title,
		Mission:     mission,
	}, nil
}

func (e *ResumeEngine) getActiveProjectFromIndex(ctx context.Context) (*ProjectContext, error) {
	db, err := sql.Open("sqlite3", e.indexDB)
	if err != nil {
		return nil, err
	}
	defer db.Close()

	var id, title, mission string
	queryErr := db.QueryRow(`
		SELECT e.id, e.title, m.title
		FROM entities e
		LEFT JOIN entities m ON e.owner = m.id AND m.type = 'mission'
		WHERE e.type = 'project' AND e.status = 'ACTIVE'
		ORDER BY e.updated_at DESC LIMIT 1
	`).Scan(&id, &title, &mission)
	if queryErr != nil {
		return nil, queryErr
	}

	return &ProjectContext{
		ProjectID:   id,
		ProjectName: title,
		Mission:     mission,
	}, nil
}

// ResumeState mirrors the JSON structure in .kisuke/resume_state.json
type ResumeState struct {
	FocusProjectID string `json:"focus_project_id"`
	FocusMissionID string `json:"focus_mission_id"`
	FocusProjectName string `json:"focus_project_name"`
}

// Context helpers for finding relevant notes
func (e *ResumeEngine) GetProjectNotes(ctx context.Context, projectID string) ([]store.CalendarEvent, error) {
	// This would query the Kisuke search index for notes linked to this project
	// For now return empty - the context engine will search via FTS5
	return nil, nil
}

func (e *ResumeEngine) GetMissionNotes(ctx context.Context, missionID string) ([]store.CalendarEvent, error) {
	return nil, nil
}