package context

import (
	"context"
	"testing"

	"kisuke-mcp/internal/store"
)

func TestEngine_GetInjectedContext(t *testing.T) {
	s, err := store.NewStore(":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()

	if err := s.SetDefaultProfile(); err != nil {
		t.Fatal(err)
	}

	// Add some vault notes
	if err := s.IndexVaultNote("docker.md", "Docker Learning", "Learn Docker and containerization"); err != nil {
		t.Fatal(err)
	}
	if err := s.IndexVaultNote("postgres.md", "PostgreSQL Learning", "Learn PostgreSQL and advanced SQL"); err != nil {
		t.Fatal(err)
	}

	// Add skill
	if err := s.UpdateSkillProgress("docker", 2, true); err != nil {
		t.Fatal(err)
	}

	engine := NewEngine(s, "", "", "")

	ctx, err := engine.GetInjectedContext(context.Background(), "test-session")
	if err != nil {
		t.Fatal(err)
	}

	if ctx.SessionID != "test-session" {
		t.Errorf("expected session_id test-session, got %s", ctx.SessionID)
	}

	if len(ctx.SkillProgress) != 1 {
		t.Errorf("expected 1 skill, got %d", len(ctx.SkillProgress))
	}

	if ctx.TokenEstimate == 0 {
		t.Errorf("token estimate should not be zero")
	}
}

func TestEngine_GetForgottenNotesBySkills(t *testing.T) {
	s, err := store.NewStore(":memory:")
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()

	if err := s.SetDefaultProfile(); err != nil {
		t.Fatal(err)
	}

	// Override learning_focus to simpler terms for FTS5 matching
	if err := s.SetProfile("learning_focus", "Docker PostgreSQL"); err != nil {
		t.Fatal(err)
	}

	// Add skill-focused notes with FTS index AND vault_links
	if err := s.IndexVaultNote("docker.md", "Docker", "Docker containerization and multi-stage builds"); err != nil {
		t.Fatal(err)
	}
	if err := s.CreateVaultLink("docker.md", "Docker", "project", "proj_docker", "documents", 0.9); err != nil {
		t.Fatal(err)
	}
	if err := s.IndexVaultNote("postgres.md", "PostgreSQL", "PostgreSQL advanced indexing and JSONB"); err != nil {
		t.Fatal(err)
	}
	if err := s.CreateVaultLink("postgres.md", "PostgreSQL", "project", "proj_postgres", "documents", 0.9); err != nil {
		t.Fatal(err)
	}

	engine := NewEngine(s, "", "", "")

	ctx, err := engine.GetInjectedContext(context.Background(), "test-session")
	if err != nil {
		t.Fatal(err)
	}

	// Should find notes related to learning_focus skills
	if len(ctx.ForgottenNotes) == 0 {
		t.Errorf("expected at least 1 forgotten note based on learning_focus")
	}
	for _, note := range ctx.ForgottenNotes {
		if note.Confidence <= 0 || note.Confidence > 1 {
			t.Errorf("confidence out of range: %f", note.Confidence)
		}
	}
}