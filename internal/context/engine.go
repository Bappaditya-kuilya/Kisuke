package context

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log/slog"
	"os"
	"path/filepath"
	"strings"
	"time"

	"kisuke-mcp/internal/kisuke"
	"kisuke-mcp/internal/store"
)

type Engine struct {
	store        store.Store
	vaultPath    string
	kisukeRepo   string
	kisukeIndex  string
	resumeEngine *kisuke.ResumeEngine
}

func NewEngine(st store.Store, vaultPath, kisukeRepo, kisukeIndex string) *Engine {
	e := &Engine{
		store:       st,
		vaultPath:   vaultPath,
		kisukeRepo:  kisukeRepo,
		kisukeIndex: kisukeIndex,
	}
	if kisukeRepo != "" {
		e.resumeEngine = kisuke.NewResumeEngine(kisukeRepo, kisukeIndex)
	}
	return e
}

func (e *Engine) GetInjectedContext(ctx context.Context, sessionID string) (*InjectedContext, error) {
	ic := &InjectedContext{
		SessionID:   sessionID,
		GeneratedAt: time.Now(),
	}

	pf, err := e.getProjectFocus(ctx)
	if err != nil {
		slog.Error("get project focus", "error", err)
	} else {
		ic.ProjectFocus = pf
	}

	events, err := e.store.GetUpcomingEvents(24, "")
	if err != nil {
		slog.Error("get events", "error", err)
	} else {
		for _, ev := range events {
			ic.TodayEvents = append(ic.TodayEvents, CalendarEvent{
				ID:         ev.ID,
				Summary:    ev.Summary,
				StartTime:  ev.StartTime,
				EndTime:    ev.EndTime,
				ProjectTag: ev.ProjectTag,
			})
		}
	}

profile, err := e.store.GetAllProfile()
	if err != nil {
		slog.Error("get profile failed", "error", err)
	} else {
		ic.Profile = profile
	}

skills, err := e.store.GetSkillProgress()
	if err != nil {
		slog.Error("get skills failed", "error", err)
	} else {
		for _, sp := range skills {
			var lastPracticedStr string
			if sp.LastPracticed.Valid {
				lastPracticedStr = sp.LastPracticed.Time.Format(time.RFC3339)
			}
			ic.SkillProgress = append(ic.SkillProgress, SkillStatus{
				Name:          sp.Name,
				CurrentLevel:  sp.CurrentLevel,
				TargetLevel:   sp.TargetLevel,
				StreakDays:    sp.StreakDays,
				LastPracticed: lastPracticedStr,
			})
		}
	}

	// Get forgotten notes - try project focus first, then fallback to skills/profile
	if pf != nil {
		notes, err := e.getForgottenNotes(ctx, pf.ProjectName, 5)
		if err != nil {
			slog.Error("get forgotten notes", "error", err)
		} else {
			ic.ForgottenNotes = notes
		}
	} else {
		// No project focus - find notes relevant to user's skills and learning focus
		notes, err := e.getForgottenNotesBySkills(ctx, 5)
		if err != nil {
			slog.Error("get forgotten notes by skills", "error", err)
		} else {
			ic.ForgottenNotes = notes
		}
	}

	ic.TokenEstimate = e.estimateTokens(ic)

	if err := e.store.LogContextInjection(sessionID, ic.toJSON()); err != nil {
		slog.Error("log context injection", "error", err)
	}

	return ic, nil
}

func (e *Engine) getProjectFocus(ctx context.Context) (*ProjectContext, error) {
	// Use real resume engine if available
	if e.resumeEngine != nil {
		pc, err := e.resumeEngine.GetCurrentContext(ctx)
		if err == nil && pc != nil {
			// Convert kisuke.ProjectContext to context.ProjectContext
			return &ProjectContext{
				ProjectID:   pc.ProjectID,
				ProjectName: pc.ProjectName,
				Mission:     pc.Mission,
			}, nil
		}
		slog.Error("resume engine failed, falling back", "error", err)
	}

	// Fallback: try resume state file (.kisuke/resume_state.json)
	if e.kisukeRepo != "" {
		resumeState := filepath.Join(e.kisukeRepo, ".kisuke", "resume_state.json")
		if data, err := os.ReadFile(resumeState); err == nil {
			var rs ResumeState
			if json.Unmarshal(data, &rs) == nil {
				if rs.FocusProjectID != "" {
					project, err := e.getProjectByID(rs.FocusProjectID)
					if err == nil && project != nil {
						mission := ""
						if rs.FocusMissionID != "" {
							if m, err := e.getMissionByID(rs.FocusMissionID); err == nil && m != nil {
								mission = m.Title
							}
						}
						return &ProjectContext{
							ProjectID:   project.ID,
							ProjectName: project.Title,
							Mission:     mission,
						}, nil
					}
				}
			}
		}
	}

	// Fallback: use Kisuke's search index to find active projects
	if e.kisukeIndex != "" {
		db, err := sql.Open("sqlite3", e.kisukeIndex)
		if err != nil {
			return nil, err
		}
		defer db.Close()

		row := db.QueryRow(`
			SELECT id, title FROM entities 
			WHERE type = 'project' AND status = 'ACTIVE' 
			ORDER BY updated_at DESC LIMIT 1
		`)
		var id, title string
		if err := row.Scan(&id, &title); err == nil {
			return &ProjectContext{
				ProjectID:   id,
				ProjectName: title,
			}, nil
		}
	}

	return nil, nil
}

type ResumeState struct {
	FocusProjectID string `json:"focus_project_id"`
	FocusMissionID string `json:"focus_mission_id"`
}

type KisukeEntity struct {
	ID      string
	Type    string
	Title   string
	Owner   string
	Status  string
	Tags    string
	Body    string
}

func (e *Engine) getProjectByID(id string) (*KisukeEntity, error) {
	if e.kisukeIndex == "" {
		return nil, fmt.Errorf("no kisuke index")
	}

	db, err := sql.Open("sqlite3", e.kisukeIndex)
	if err != nil {
		return nil, err
	}
	defer db.Close()

	row := db.QueryRow(`
		SELECT id, type, title, owner, status, tags, body
		FROM entities WHERE id = ? AND type = 'project'
	`, id)
	var ent KisukeEntity
	if err := row.Scan(&ent.ID, &ent.Type, &ent.Title, &ent.Owner, &ent.Status, &ent.Tags, &ent.Body); err != nil {
		return nil, err
	}
	return &ent, nil
}

func (e *Engine) getMissionByID(id string) (*KisukeEntity, error) {
	if e.kisukeIndex == "" {
		return nil, fmt.Errorf("no kisuke index")
	}

	db, err := sql.Open("sqlite3", e.kisukeIndex)
	if err != nil {
		return nil, err
	}
	defer db.Close()

	row := db.QueryRow(`
		SELECT id, type, title, owner, status, tags, body
		FROM entities WHERE id = ? AND type = 'mission'
	`, id)
	var ent KisukeEntity
	if err := row.Scan(&ent.ID, &ent.Type, &ent.Title, &ent.Owner, &ent.Status, &ent.Tags, &ent.Body); err != nil {
		return nil, err
	}
	return &ent, nil
}

func (e *Engine) getForgottenNotes(ctx context.Context, projectName string, limit int) ([]ForgottenNote, error) {
	if projectName == "" {
		return nil, nil
	}

	// First try explicit vault_links
	links, err := e.store.SearchVaultNotes(projectName, limit)
	if err != nil {
		return nil, err
	}

	var notes []ForgottenNote
	for _, l := range links {
		content, title := e.readVaultNote(l.VaultNotePath)
		notes = append(notes, ForgottenNote{
			Path:       l.VaultNotePath,
			Title:      title,
			Snippet:    extractSnippet(content, projectName, 200),
			Confidence: l.Confidence,
			Reason:     fmt.Sprintf("Semantically related to %s", projectName),
			EntityType: l.KisukeEntityType,
			EntityID:   l.KisukeEntityID,
		})
	}

	// Then augment with inferred notes from Kisuke search index
	if e.kisukeIndex != "" && len(notes) < limit {
		inferred, err := e.inferFromKisukeIndex(projectName, limit-len(notes))
		if err == nil {
			notes = append(notes, inferred...)
		}
	}

	return notes, nil
}

func (e *Engine) inferFromKisukeIndex(projectName string, limit int) ([]ForgottenNote, error) {
	if e.kisukeIndex == "" {
		return nil, nil
	}

	db, err := sql.Open("sqlite3", e.kisukeIndex)
	if err != nil {
		return nil, err
	}
	defer db.Close()

	rows, err := db.Query(`
		SELECT id, type, title, body FROM entities 
		WHERE type IN ('knowledge', 'decision', 'task', 'meeting') 
		AND (title LIKE ? OR body LIKE ?)
		ORDER BY updated_at DESC LIMIT ?
	`, "%"+projectName+"%", "%"+projectName+"%", limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var notes []ForgottenNote
	for rows.Next() {
		var id, typ, title, body string
		if err := rows.Scan(&id, &typ, &title, &body); err != nil {
			continue
		}
		snippet := extractSnippet(body, projectName, 200)
		notes = append(notes, ForgottenNote{
			Path:       typ + "/" + id + ".md",
			Title:      title,
			Snippet:    snippet,
			Confidence: 0.4,
			Reason:     fmt.Sprintf("Found in Kisuke %s: %s", typ, projectName),
			EntityType: "inferred",
			EntityID:   id,
		})
	}
	return notes, nil
}

func (e *Engine) getForgottenNotesBySkills(ctx context.Context, limit int) ([]ForgottenNote, error) {
	var notes []ForgottenNote

	// Get user's learning focus from profile
	learningFocus := ""
	if profile, err := e.store.GetAllProfile(); err == nil {
		if f, ok := profile["learning_focus"]; ok {
			learningFocus = f
		}
	}

	// Search for notes related to learning focus - split into terms and search each
	if learningFocus != "" {
		// Split learning focus by commas and spaces to get individual terms
		terms := splitLearningFocus(learningFocus)
		seen := make(map[string]bool)
		
		for _, term := range terms {
			if term == "" {
				continue
			}
			links, err := e.store.SearchVaultNotes(term, limit)
			if err != nil {
				continue
			}
			for _, l := range links {
				if seen[l.VaultNotePath] {
					continue
				}
				seen[l.VaultNotePath] = true
				content, title := e.readVaultNote(l.VaultNotePath)
				notes = append(notes, ForgottenNote{
					Path:       l.VaultNotePath,
					Title:      title,
					Snippet:    extractSnippet(content, term, 200),
					Confidence: 0.5,
					Reason:     fmt.Sprintf("Related to your learning focus: %s", term),
					EntityType: "inferred",
					EntityID:   "",
				})
				if len(notes) >= limit {
					break
				}
			}
			if len(notes) >= limit {
				break
			}
		}
	}

	// If still no notes, search for explicit vault_links (any linked notes)
	if len(notes) == 0 {
		links, err := e.store.SearchVaultNotes("project", limit)
		if err == nil {
			for _, l := range links {
				content, title := e.readVaultNote(l.VaultNotePath)
				notes = append(notes, ForgottenNote{
					Path:       l.VaultNotePath,
					Title:      title,
					Snippet:    extractSnippet(content, l.VaultNotePath, 200),
					Confidence: l.Confidence,
					Reason:     fmt.Sprintf("Linked to %s:%s", l.KisukeEntityType, l.KisukeEntityID),
					EntityType: l.KisukeEntityType,
					EntityID:   l.KisukeEntityID,
				})
			}
		}
	}

	if len(notes) > limit {
		notes = notes[:limit]
	}

	return notes, nil
}

func splitLearningFocus(focus string) []string {
	// Replace commas with spaces, then split by whitespace
	focus = strings.ReplaceAll(focus, ",", " ")
	var terms []string
	for _, term := range strings.Fields(focus) {
		if len(term) > 2 { // Skip very short terms
			terms = append(terms, term)
		}
	}
	return terms
}

func (e *Engine) readVaultNote(path string) (content, title string) {
	if e.vaultPath == "" {
		e.vaultPath = os.Getenv("VAULT_PATH")
		if e.vaultPath == "" {
			return "", ""
		}
	}

	fullPath := filepath.Join(e.vaultPath, path)
	if !strings.HasSuffix(fullPath, ".md") {
		fullPath += ".md"
	}

	data, err := os.ReadFile(fullPath)
	if err != nil {
		return "", ""
	}

	content = string(data)
	lines := strings.Split(content, "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "# ") {
			title = strings.TrimSpace(line[2:])
			break
		}
	}
	if title == "" {
		title = filepath.Base(path)
		title = strings.TrimSuffix(title, ".md")
	}
	return content, title
}

func (e *Engine) estimateTokens(ic *InjectedContext) int {
	tokens := 0

	if ic.ProjectFocus != nil {
		tokens += len(ic.ProjectFocus.ProjectName) / 4
		tokens += len(ic.ProjectFocus.Mission) / 4
	}

	for _, ev := range ic.TodayEvents {
		tokens += len(ev.Summary) / 4
		tokens += 20
	}

	for _, fn := range ic.ForgottenNotes {
		tokens += len(fn.Title) / 4
		tokens += len(fn.Snippet) / 4
		tokens += 10
	}

	for k, v := range ic.Profile {
		tokens += (len(k) + len(v)) / 4
	}

	for _, sp := range ic.SkillProgress {
		tokens += len(sp.Name) / 4
		tokens += 10
	}

	return tokens
}

func (ic *InjectedContext) toJSON() string {
	data, _ := json.Marshal(ic)
	return string(data)
}

func extractSnippet(content, keyword string, maxLen int) string {
	idx := strings.Index(strings.ToLower(content), strings.ToLower(keyword))
	if idx == -1 {
		if len(content) > maxLen {
			return content[:maxLen] + "..."
		}
		return content
	}
	start := idx - maxLen/2
	if start < 0 {
		start = 0
	}
	end := start + maxLen
	if end > len(content) {
		end = len(content)
	}
	snippet := content[start:end]
	if start > 0 {
		snippet = "..." + snippet
	}
	if end < len(content) {
		snippet = snippet + "..."
	}
	return snippet
}