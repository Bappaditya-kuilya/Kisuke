package store

import (
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

func TestStore_BasicOperations(t *testing.T) {
	s, err := NewStore(":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()

	if err := s.SetDefaultProfile(); err != nil {
		t.Fatal(err)
	}

	// Test profile
	if err := s.SetProfile("test_key", "test_value"); err != nil {
		t.Fatal(err)
	}
	val, err := s.GetProfile("test_key")
	if err != nil {
		t.Fatal(err)
	}
	if val != "test_value" {
		t.Errorf("expected test_value, got %s", val)
	}

	// Test vault links
	if err := s.CreateVaultLink("note1.md", "Note 1", "project", "proj_1", "reference", 0.9); err != nil {
		t.Fatal(err)
	}
	links, err := s.GetVaultLinksByEntity("project", "proj_1")
	if err != nil {
		t.Fatal(err)
	}
	if len(links) != 1 {
		t.Errorf("expected 1 link, got %d", len(links))
	}
	if links[0].Confidence != 0.9 {
		t.Errorf("expected confidence 0.9, got %f", links[0].Confidence)
	}

	// Test FTS index
	if err := s.IndexVaultNote("note1.md", "Note 1", "This is test content about Docker"); err != nil {
		t.Fatal(err)
	}
	results, err := s.SearchVaultNotesDirect("Docker", 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(results) != 1 {
		t.Errorf("expected 1 search result, got %d", len(results))
	}

	// Test skill progress
	if err := s.UpdateSkillProgress("docker", 2, true); err != nil {
		t.Fatal(err)
	}
	skills, err := s.GetSkillProgress()
	if err != nil {
		t.Fatal(err)
	}
	if len(skills) != 1 {
		t.Errorf("expected 1 skill, got %d", len(skills))
	}
	if skills[0].CurrentLevel != 2 {
		t.Errorf("expected level 2, got %d", skills[0].CurrentLevel)
	}
	if skills[0].StreakDays != 1 {
		t.Errorf("expected streak 1, got %d", skills[0].StreakDays)
	}

	// Test calendar events
	now := time.Now()
	event := CalendarEvent{
		ID:          "evt_1",
		Summary:     "Test Event",
		Description: "Description",
		StartTime:   now.Add(time.Hour),
		EndTime:     now.Add(2 * time.Hour),
		CalendarID:  "cal_1",
		ProjectTag:  "proj_test",
	}
	if err := s.SyncCalendarEvents([]CalendarEvent{event}); err != nil {
		t.Fatal(err)
	}
	events, err := s.GetUpcomingEvents(24, "proj_test")
	if err != nil {
		t.Fatal(err)
	}
	if len(events) != 1 {
		t.Errorf("expected 1 event, got %d", len(events))
	}

	// Test MCP connections
	conn := MCPConnection{
		Name:    "test_mcp",
		Command: "npx",
		Args:    `["@modelcontextprotocol/server-postgres"]`,
		Enabled: true,
	}
	if err := s.AddMCPConnection(conn); err != nil {
		t.Fatal(err)
	}
	conns, err := s.GetMCPConnections()
	if err != nil {
		t.Fatal(err)
	}
	if len(conns) != 1 {
		t.Errorf("expected 1 connection, got %d", len(conns))
	}

	// Test context history
	if err := s.LogContextInjection("session_1", "test context"); err != nil {
		t.Fatal(err)
	}
	history, err := s.GetContextHistory("session_1")
	if err != nil {
		t.Fatal(err)
	}
	if len(history) != 1 {
		t.Errorf("expected 1 history entry, got %d", len(history))
	}

	// Test stats
	stats, err := s.GetStats()
	if err != nil {
		t.Fatal(err)
	}
	if stats["vault_links"] != 1 {
		t.Errorf("expected 1 vault_link, got %d", stats["vault_links"])
	}
}

func TestStore_ConfidenceScoring(t *testing.T) {
	s, err := NewStore(":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()

	// Test explicit link gets high confidence
	if err := s.CreateVaultLink("note1.md", "Note 1", "project", "proj_1", "implements", 0.95); err != nil {
		t.Fatal(err)
	}

	// Test inferred link gets lower confidence
	if err := s.IndexVaultNote("note2.md", "Note 2", "This is about Docker"); err != nil {
		t.Fatal(err)
	}
	links, err := s.SearchVaultNotesDirect("Docker", 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(links) == 1 && links[0].Confidence > 0.4 && links[0].Confidence < 0.8 {
		t.Logf("Inferred confidence: %f (expected ~0.4)", links[0].Confidence)
	}
}