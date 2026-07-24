package mcp

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log/slog"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	_ "github.com/mattn/go-sqlite3"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"

	ctxpkg "kisuke-mcp/internal/context"
	"kisuke-mcp/internal/store"
)

type Server struct {
	mcpServer   *server.MCPServer
	ctxEngine   *ctxpkg.Engine
	store       store.Store
	kisukeIndex string
}

func NewServer(ctxEngine *ctxpkg.Engine, store store.Store, kisukeIndex string) *Server {
	s := &Server{
		ctxEngine:   ctxEngine,
		store:       store,
		kisukeIndex: kisukeIndex,
	}

	s.mcpServer = server.NewMCPServer(
		"kisuke-mcp",
		"1.0.0",
		server.WithToolCapabilities(true),
		server.WithResourceCapabilities(true, true),
	)

	s.registerTools()
	s.registerResources()
	s.registerPrompts()

	return s
}

func (s *Server) registerTools() {
	s.mcpServer.AddTool(mcp.NewTool("get_context",
		mcp.WithDescription("Get injected context for current session - project focus, forgotten notes, today's events, profile, skill progress"),
		mcp.WithString("session_id", mcp.Required(), mcp.Description("Unique session identifier")),
	), s.handleGetContext)

	s.mcpServer.AddTool(mcp.NewTool("search_vault",
		mcp.WithDescription("Search your Obsidian vault for notes relevant to a query"),
		mcp.WithString("query", mcp.Required(), mcp.Description("Search query")),
		mcp.WithNumber("limit", mcp.Description("Max results (default 10)")),
	), s.handleSearchVault)

	s.mcpServer.AddTool(mcp.NewTool("link_note",
		mcp.WithDescription("Create a link between a vault note and a Kisuke entity"),
		mcp.WithString("note_path", mcp.Required(), mcp.Description("Path to note in vault (relative)")),
		mcp.WithString("note_title", mcp.Description("Note title (auto-read if empty)")),
		mcp.WithString("entity_type", mcp.Required(), mcp.Description("Kisuke entity type: project, mission, context, task, decision, pattern")),
		mcp.WithString("entity_id", mcp.Required(), mcp.Description("Kisuke entity ID")),
		mcp.WithString("link_type", mcp.Description("Type of link: reference, implements, documents, decision, pattern")),
		mcp.WithNumber("confidence", mcp.Description("Confidence 0-1 (default 0.8)")),
	), s.handleLinkNote)

	s.mcpServer.AddTool(mcp.NewTool("unlink_note",
		mcp.WithDescription("Remove a link between a vault note and Kisuke entity"),
		mcp.WithString("note_path", mcp.Required(), mcp.Description("Path to note in vault")),
		mcp.WithString("entity_type", mcp.Required(), mcp.Description("Kisuke entity type")),
		mcp.WithString("entity_id", mcp.Required(), mcp.Description("Kisuke entity ID")),
	), s.handleUnlinkNote)

	s.mcpServer.AddTool(mcp.NewTool("index_vault",
		mcp.WithDescription("Scan and index all markdown files in the Obsidian vault for search"),
		mcp.WithNumber("limit", mcp.Description("Max files to process (default 1000)")),
	), s.handleIndexVault)

	s.mcpServer.AddTool(mcp.NewTool("get_forgotten",
		mcp.WithDescription("Get forgotten notes relevant to current project/mission context"),
		mcp.WithString("project_name", mcp.Description("Project name to find relevant notes for")),
		mcp.WithNumber("limit", mcp.Description("Max results (default 5)")),
	), s.handleGetForgotten)

	s.mcpServer.AddTool(mcp.NewTool("get_profile",
		mcp.WithDescription("Get your developer profile (goals, preferences, build style)"),
	), s.handleGetProfile)

	s.mcpServer.AddTool(mcp.NewTool("update_profile",
		mcp.WithDescription("Update your developer profile"),
		mcp.WithString("key", mcp.Required(), mcp.Description("Profile key")),
		mcp.WithString("value", mcp.Required(), mcp.Description("Profile value")),
	), s.handleUpdateProfile)

	s.mcpServer.AddTool(mcp.NewTool("get_skills",
		mcp.WithDescription("Get your skill progress tracking"),
	), s.handleGetSkills)

	s.mcpServer.AddTool(mcp.NewTool("practice_skill",
		mcp.WithDescription("Log a skill practice session"),
		mcp.WithString("skill", mcp.Required(), mcp.Description("Skill name")),
		mcp.WithNumber("level", mcp.Description("Current level achieved")),
	), s.handlePracticeSkill)

	s.mcpServer.AddTool(mcp.NewTool("add_mcp",
		mcp.WithDescription("Register an MCP server for seamless integration"),
		mcp.WithString("name", mcp.Required(), mcp.Description("Connection name")),
		mcp.WithString("command", mcp.Required(), mcp.Description("Command to run (e.g., npx, python, docker)")),
		mcp.WithString("args", mcp.Description("JSON array of arguments")),
		mcp.WithString("env", mcp.Description("JSON object of environment variables")),
	), s.handleAddMCP)

	s.mcpServer.AddTool(mcp.NewTool("list_mcps",
		mcp.WithDescription("List registered MCP servers"),
	), s.handleListMCPs)

	s.mcpServer.AddTool(mcp.NewTool("get_upcoming",
		mcp.WithDescription("Get upcoming calendar events"),
		mcp.WithNumber("hours", mcp.Description("Hours ahead (default 24)")),
		mcp.WithString("project_tag", mcp.Description("Filter by project tag")),
	), s.handleGetUpcoming)
}

func (s *Server) registerResources() {
	s.mcpServer.AddResource(mcp.NewResource(
		"kisuke://context/{session_id}",
		"Injected context for session",
		mcp.WithMIMEType("application/json"),
	), s.handleContextResource)

	s.mcpServer.AddResource(mcp.NewResource(
		"kisuke://vault/search/{query}",
		"Search vault notes",
		mcp.WithMIMEType("application/json"),
	), s.handleVaultSearchResource)

	s.mcpServer.AddResource(mcp.NewResource(
		"kisuke://profile",
		"Developer profile",
		mcp.WithMIMEType("application/json"),
	), s.handleProfileResource)
}

func (s *Server) registerPrompts() {
	s.mcpServer.AddPrompt(mcp.NewPrompt("morning_brief",
		mcp.WithPromptDescription("Generate morning briefing with context, forgotten notes, and today's schedule"),
		mcp.WithArgument("session_id", mcp.ArgumentDescription("Session ID"), mcp.RequiredArgument()),
	), s.handleMorningBriefPrompt)

	s.mcpServer.AddPrompt(mcp.NewPrompt("project_context",
		mcp.WithPromptDescription("Get full project context for a coding session"),
		mcp.WithArgument("session_id", mcp.ArgumentDescription("Session ID"), mcp.RequiredArgument()),
		mcp.WithArgument("focus", mcp.ArgumentDescription("What you're working on right now")),
	), s.handleProjectContextPrompt)
}

func getArg(args map[string]any, key string) string {
	if v, ok := args[key]; ok {
		if s, ok := v.(string); ok {
			return s
		}
	}
	return ""
}

func getArgFloat(args map[string]any, key string, def float64) float64 {
	if v, ok := args[key]; ok {
		switch val := v.(type) {
		case float64:
			return val
		case string:
			if f, err := strconv.ParseFloat(val, 64); err == nil {
				return f
			}
		}
	}
	return def
}

func (s *Server) handleGetContext(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	sessionID := getArg(req.Params.Arguments, "session_id")
	if sessionID == "" {
		return mcp.NewToolResultError("session_id is required"), nil
	}

	ic, err := s.ctxEngine.GetInjectedContext(ctx, sessionID)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to get context: %v", err)), nil
	}

	data, _ := json.MarshalIndent(ic, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handleSearchVault(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	query := getArg(args, "query")
	if query == "" {
		return mcp.NewToolResultError("query is required"), nil
	}
	limit := int(getArgFloat(args, "limit", 10))

	// First try to search via vault_links (explicit links)
	links, err := s.store.SearchVaultNotes(query, limit)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("search failed: %v", err)), nil
	}

	// If no results, also search the FTS index directly for unlinked notes
	if len(links) == 0 {
		directResults, err := s.store.SearchVaultNotesDirect(query, limit)
		if err != nil {
			return mcp.NewToolResultError(fmt.Sprintf("direct search failed: %v", err)), nil
		}
		links = directResults
	}

	var results []map[string]any
	for _, l := range links {
		content, title := s.readVaultNote(l.VaultNotePath)
		results = append(results, map[string]any{
			"path":        l.VaultNotePath,
			"title":       title,
			"snippet":     extractSnippet(content, query, 200),
			"confidence":  l.Confidence,
			"entity_type": l.KisukeEntityType,
			"entity_id":   l.KisukeEntityID,
		})
	}

	data, _ := json.MarshalIndent(results, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) readVaultNote(path string) (content, title string) {
	vaultPath := os.Getenv("VAULT_PATH")
	if vaultPath == "" {
		vaultPath = "/mnt/d/Obsidian Vault/AI Research"
	}

	fullPath := filepath.Join(vaultPath, path)
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

// computeConfidence calculates semantic similarity between note content and Kisuke entity
func (s *Server) computeConfidence(notePath, entityType, entityID string) float64 {
	noteContent, _ := s.readVaultNote(notePath)
	if noteContent == "" {
		return 0.5 // default if can't read note
	}

	// Try to fetch entity content from Kisuke index
	var entityContent string
	if s.kisukeIndex != "" {
		db, err := sql.Open("sqlite3", s.kisukeIndex)
		if err == nil {
			defer db.Close()
			var body string
			err := db.QueryRow(`
				SELECT body FROM entities WHERE id = ? AND type = ?
			`, entityID, entityType).Scan(&body)
			if err == nil && body != "" {
				entityContent = body
			}
		}
	}

	if entityContent == "" {
		// Fallback: use entity ID as content for basic matching
		entityContent = entityID
	}

	// Compute Jaccard similarity on word sets
	noteWords := tokenize(noteContent)
	entityWords := tokenize(entityContent)

	noteSet := make(map[string]bool)
	for _, w := range noteWords {
		noteSet[w] = true
	}

	entitySet := make(map[string]bool)
	for _, w := range entityWords {
		entitySet[w] = true
	}

	intersection := 0
	union := 0
	for w := range noteSet {
		union++
		if entitySet[w] {
			intersection++
		}
	}
	for w := range entitySet {
		if !noteSet[w] {
			union++
		}
	}

	if union == 0 {
		return 0.5
	}

	similarity := float64(intersection) / float64(union)
	// Boost confidence for explicit links
	return math.Min(0.95, 0.5+similarity*0.5)
}

// tokenize splits text into lowercase words
func tokenize(text string) []string {
	reg := regexp.MustCompile(`[a-zA-Z]+`)
	words := reg.FindAllString(strings.ToLower(text), -1)
	return words
}

func (s *Server) handleLinkNote(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	notePath := getArg(args, "note_path")
	noteTitle := getArg(args, "note_title")
	entityType := getArg(args, "entity_type")
	entityID := getArg(args, "entity_id")
	linkType := getArg(args, "link_type")
	if linkType == "" {
		linkType = "reference"
	}
	confidence := getArgFloat(args, "confidence", 0.8)

	if notePath == "" || entityType == "" || entityID == "" {
		return mcp.NewToolResultError("note_path, entity_type, entity_id are required"), nil
	}

	if noteTitle == "" {
		_, noteTitle = s.readVaultNote(notePath)
	}

	if err := s.store.CreateVaultLink(notePath, noteTitle, entityType, entityID, linkType, confidence); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to link: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Linked %s to %s:%s", notePath, entityType, entityID)), nil
}

func (s *Server) handleUnlinkNote(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	notePath := getArg(args, "note_path")
	entityType := getArg(args, "entity_type")
	entityID := getArg(args, "entity_id")

	if notePath == "" || entityType == "" || entityID == "" {
		return mcp.NewToolResultError("note_path, entity_type, entity_id are required"), nil
	}

	if err := s.store.DeleteVaultLink(notePath, entityType, entityID); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to unlink: %v", err)), nil
	}

	return mcp.NewToolResultText("Unlinked"), nil
}

func (s *Server) handleGetForgotten(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	projectName := getArg(args, "project_name")
	limit := int(getArgFloat(args, "limit", 5))

	links, err := s.store.SearchVaultNotes(projectName, limit)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("search failed: %v", err)), nil
	}

	var results []map[string]any
	for _, l := range links {
		content, title := s.readVaultNote(l.VaultNotePath)
		results = append(results, map[string]any{
			"path":        l.VaultNotePath,
			"title":       title,
			"snippet":     extractSnippet(content, projectName, 200),
			"confidence":  l.Confidence,
			"reason":      fmt.Sprintf("Semantically related to %s", projectName),
			"entity_type": "inferred",
		})
	}

	data, _ := json.MarshalIndent(results, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handleGetProfile(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	profile, err := s.store.GetAllProfile()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to get profile: %v", err)), nil
	}

	data, _ := json.MarshalIndent(profile, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handleUpdateProfile(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	key := getArg(args, "key")
	value := getArg(args, "value")

	if key == "" {
		return mcp.NewToolResultError("key is required"), nil
	}

	if err := s.store.SetProfile(key, value); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to update: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Updated %s", key)), nil
}

func (s *Server) handleGetSkills(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	skills, err := s.store.GetSkillProgress()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to get skills: %v", err)), nil
	}

	data, _ := json.MarshalIndent(skills, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handlePracticeSkill(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	skill := getArg(args, "skill")
	level := int(getArgFloat(args, "level", 1))

	if skill == "" {
		return mcp.NewToolResultError("skill is required"), nil
	}

	if err := s.store.UpdateSkillProgress(skill, level, true); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to log practice: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Logged practice for %s (level %d)", skill, level)), nil
}

func (s *Server) handleAddMCP(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	name := getArg(args, "name")
	command := getArg(args, "command")
	argsStr := getArg(args, "args")
	if argsStr == "" {
		argsStr = "[]"
	}
	env := getArg(args, "env")
	if env == "" {
		env = "{}"
	}

	if name == "" || command == "" {
		return mcp.NewToolResultError("name and command are required"), nil
	}

	if err := s.store.AddMCPConnection(store.MCPConnection{
		Name:    name,
		Command: command,
		Args:    argsStr,
		Env:     env,
		Enabled: true,
	}); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to add: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Added MCP connection: %s", name)), nil
}

func (s *Server) handleListMCPs(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	conns, err := s.store.GetMCPConnections()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to list: %v", err)), nil
	}

	data, _ := json.MarshalIndent(conns, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handleGetUpcoming(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	hours := int(getArgFloat(args, "hours", 24))
	projectTag := getArg(args, "project_tag")

	events, err := s.store.GetUpcomingEvents(hours, projectTag)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to get events: %v", err)), nil
	}

	data, _ := json.MarshalIndent(events, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) handleContextResource(ctx context.Context, req mcp.ReadResourceRequest) ([]mcp.ResourceContents, error) {
	args := req.Params.Arguments
	sessionID := getArg(args, "session_id")
	if sessionID == "" {
		return nil, fmt.Errorf("session_id required")
	}

	ic, err := s.ctxEngine.GetInjectedContext(ctx, sessionID)
	if err != nil {
		return nil, err
	}

	data, _ := json.MarshalIndent(ic, "", "  ")
	return []mcp.ResourceContents{
		mcp.TextResourceContents{
			URI:      fmt.Sprintf("kisuke://context/%s", sessionID),
			MIMEType: "application/json",
			Text:     string(data),
		},
	}, nil
}

func (s *Server) handleVaultSearchResource(ctx context.Context, req mcp.ReadResourceRequest) ([]mcp.ResourceContents, error) {
	args := req.Params.Arguments
	query := getArg(args, "query")
	if query == "" {
		return nil, fmt.Errorf("query required")
	}

	links, err := s.store.SearchVaultNotes(query, 10)
	if err != nil {
		return nil, err
	}

	var results []map[string]any
	for _, l := range links {
		content, title := s.readVaultNote(l.VaultNotePath)
		results = append(results, map[string]any{
			"path":        l.VaultNotePath,
			"title":       title,
			"snippet":     extractSnippet(content, query, 200),
			"confidence":  l.Confidence,
			"entity_type": l.KisukeEntityType,
			"entity_id":   l.KisukeEntityID,
		})
	}

	data, _ := json.MarshalIndent(results, "", "  ")
	return []mcp.ResourceContents{
		mcp.TextResourceContents{
			URI:      fmt.Sprintf("kisuke://vault/search/%s", query),
			MIMEType: "application/json",
			Text:     string(data),
		},
	}, nil
}

func (s *Server) handleProfileResource(ctx context.Context, req mcp.ReadResourceRequest) ([]mcp.ResourceContents, error) {
	profile, err := s.store.GetAllProfile()
	if err != nil {
		return nil, err
	}

	data, _ := json.MarshalIndent(profile, "", "  ")
	return []mcp.ResourceContents{
		mcp.TextResourceContents{
			URI:      "kisuke://profile",
			MIMEType: "application/json",
			Text:     string(data),
		},
	}, nil
}

func (s *Server) handleMorningBriefPrompt(ctx context.Context, req mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
	args := make(map[string]any)
	for k, v := range req.Params.Arguments {
		args[k] = v
	}
	sessionID := getArg(args, "session_id")
	if sessionID == "" {
		return nil, fmt.Errorf("session_id required")
	}

	ic, err := s.ctxEngine.GetInjectedContext(ctx, sessionID)
	if err != nil {
		return nil, err
	}

	var brief strings.Builder
	brief.WriteString("# Good morning! Here's your briefing\n\n")

	if ic.ProjectFocus != nil {
		brief.WriteString(fmt.Sprintf("## 🎯 Current Focus: %s\n", ic.ProjectFocus.ProjectName))
		if ic.ProjectFocus.Mission != "" {
			brief.WriteString(fmt.Sprintf("**Mission**: %s\n", ic.ProjectFocus.Mission))
		}
		brief.WriteString("\n")
	}

	if len(ic.TodayEvents) > 0 {
		brief.WriteString("## 📅 Today's Schedule\n")
		for _, ev := range ic.TodayEvents {
			brief.WriteString(fmt.Sprintf("- **%s** %s–%s", ev.Summary, ev.StartTime.Format("15:04"), ev.EndTime.Format("15:04")))
			if ev.ProjectTag != "" {
				brief.WriteString(fmt.Sprintf(" [%s]", ev.ProjectTag))
			}
			brief.WriteString("\n")
		}
		brief.WriteString("\n")
	}

	if len(ic.ForgottenNotes) > 0 {
		brief.WriteString("## 💭 Forgotten Notes (you wrote these, remember?)\n")
		for _, fn := range ic.ForgottenNotes {
			brief.WriteString(fmt.Sprintf("- **%s** (%.0f%% confidence)\n  %s\n  *%s*\n\n", fn.Title, fn.Confidence*100, fn.Snippet, fn.Reason))
		}
	}

	if len(ic.SkillProgress) > 0 {
		brief.WriteString("## 📈 Skill Progress\n")
		for _, sp := range ic.SkillProgress {
			brief.WriteString(fmt.Sprintf("- %s: Level %d/%d (streak: %d days)\n", sp.Name, sp.CurrentLevel, sp.TargetLevel, sp.StreakDays))
		}
		brief.WriteString("\n")
	}

	brief.WriteString("---\n*Have a productive day! Remember: you're building the AI Engineer you want to become.*")

	return mcp.NewGetPromptResult(
		"Morning briefing with project context, forgotten notes, schedule, and skill progress",
		[]mcp.PromptMessage{
			{Role: "user", Content: mcp.TextContent{Type: "text", Text: brief.String()}},
		},
	), nil
}

func (s *Server) handleProjectContextPrompt(ctx context.Context, req mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
	args := make(map[string]any)
	for k, v := range req.Params.Arguments {
		args[k] = v
	}
	sessionID := getArg(args, "session_id")
	focus := getArg(args, "focus")

	ic, err := s.ctxEngine.GetInjectedContext(ctx, sessionID)
	if err != nil {
		return nil, err
	}

	var context strings.Builder
	context.WriteString("# Project Context Injection\n\n")

	if ic.ProjectFocus != nil {
		context.WriteString(fmt.Sprintf("## Project: %s\n", ic.ProjectFocus.ProjectName))
		if ic.ProjectFocus.Mission != "" {
			context.WriteString(fmt.Sprintf("**Mission**: %s\n", ic.ProjectFocus.Mission))
		}
	}

	if focus != "" {
		context.WriteString(fmt.Sprintf("\n## Current Focus: %s\n", focus))
	}

	if len(ic.ForgottenNotes) > 0 {
		context.WriteString("\n## Relevant Notes You Forgot\n")
		for _, fn := range ic.ForgottenNotes {
			context.WriteString(fmt.Sprintf("- **%s**: %s\n", fn.Title, fn.Snippet))
		}
	}

	if len(ic.RelevantPatterns) > 0 {
		context.WriteString("\n## Relevant Code Patterns\n")
		for _, p := range ic.RelevantPatterns {
			context.WriteString(fmt.Sprintf("- **%s**: %s\n", p.Name, p.Description))
		}
	}

	context.WriteString(fmt.Sprintf("\n*Token estimate: ~%d tokens*", ic.TokenEstimate))

	return mcp.NewGetPromptResult(
		"Project context for coding session",
		[]mcp.PromptMessage{
			{Role: "user", Content: mcp.TextContent{Type: "text", Text: context.String()}},
		},
	), nil
}

func (s *Server) handleIndexVault(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	limit := int(getArgFloat(args, "limit", 1000))

	vaultPath := os.Getenv("VAULT_PATH")
	if vaultPath == "" {
		vaultPath = "/mnt/d/Obsidian Vault/AI Research"
	}

	indexed := 0
	err := filepath.Walk(vaultPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}
		if info.IsDir() {
			return nil
		}
		if !strings.HasSuffix(strings.ToLower(info.Name()), ".md") {
			return nil
		}
		if indexed >= limit {
			return filepath.SkipDir
		}

		relPath, err := filepath.Rel(vaultPath, path)
		if err != nil {
			return nil
		}

		content, title := s.readVaultNote(relPath)
		if content == "" {
			return nil
		}

		if err := s.store.IndexVaultNote(relPath, title, content); err != nil {
			slog.Error("Failed to index", "path", relPath, "error", err)
			return nil
		}
		indexed++
		return nil
	})

	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("index failed: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Indexed %d markdown files from vault", indexed)), nil
}

func (s *Server) Serve() error {
	return server.ServeStdio(s.mcpServer)
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