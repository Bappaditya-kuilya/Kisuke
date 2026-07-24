package mcp

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"

	"personal-context-mcp/internal/store"
)

type Server struct {
	mcpServer *server.MCPServer
	store     store.Store
	vaultPath string
}

func NewServer(store store.Store, vaultPath string) *Server {
	s := &Server{
		store:     store,
		vaultPath: vaultPath,
	}

	s.mcpServer = server.NewMCPServer(
		"personal-context",
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
	s.mcpServer.AddTool(mcp.NewTool("search_notes",
		mcp.WithDescription("Search personal notes/knowledge base for relevant content"),
		mcp.WithString("query", mcp.Required(), mcp.Description("Search query")),
		mcp.WithNumber("limit", mcp.Description("Max results (default 10)")),
	), s.handleSearchNotes)

	s.mcpServer.AddTool(mcp.NewTool("link_note",
		mcp.WithDescription("Create a link between a note and a project/entity"),
		mcp.WithString("note_path", mcp.Required(), mcp.Description("Path to note (relative to vault)")),
		mcp.WithString("note_title", mcp.Description("Note title (auto-read if empty)")),
		mcp.WithString("project", mcp.Required(), mcp.Description("Project/entity name")),
		mcp.WithString("type", mcp.Description("Link type: reference, implements, documents, decision (default: reference)")),
		mcp.WithNumber("confidence", mcp.Description("Confidence 0-1 (default 0.8)")),
	), s.handleLinkNote)

	s.mcpServer.AddTool(mcp.NewTool("unlink_note",
		mcp.WithDescription("Remove a link between a note and project"),
		mcp.WithString("note_path", mcp.Required(), mcp.Description("Path to note")),
		mcp.WithString("project", mcp.Required(), mcp.Description("Project name")),
	), s.handleUnlinkNote)

	s.mcpServer.AddTool(mcp.NewTool("index_vault",
		mcp.WithDescription("Scan and index all markdown files in the notes vault"),
		mcp.WithNumber("limit", mcp.Description("Max files to process (default 1000)")),
	), s.handleIndexVault)

	s.mcpServer.AddTool(mcp.NewTool("get_context",
		mcp.WithDescription("Get injected context for current session - project focus, relevant notes, profile"),
		mcp.WithString("session_id", mcp.Required(), mcp.Description("Unique session identifier")),
		mcp.WithString("project", mcp.Description("Project name to focus on")),
	), s.handleGetContext)

	s.mcpServer.AddTool(mcp.NewTool("get_profile",
		mcp.WithDescription("Get your developer profile (goals, preferences, build style)"),
	), s.handleGetProfile)

	s.mcpServer.AddTool(mcp.NewTool("update_profile",
		mcp.WithDescription("Update your developer profile"),
		mcp.WithString("key", mcp.Required(), mcp.Description("Profile key")),
		mcp.WithString("value", mcp.Required(), mcp.Description("Profile value")),
	), s.handleUpdateProfile)

	s.mcpServer.AddTool(mcp.NewTool("add_mcp",
		mcp.WithDescription("Register an external MCP server for seamless integration"),
		mcp.WithString("name", mcp.Required(), mcp.Description("Connection name")),
		mcp.WithString("command", mcp.Required(), mcp.Description("Command to run (e.g., npx, python, docker)")),
		mcp.WithString("args", mcp.Description("JSON array of arguments")),
		mcp.WithString("env", mcp.Description("JSON object of environment variables")),
	), s.handleAddMCP)

	s.mcpServer.AddTool(mcp.NewTool("list_mcps",
		mcp.WithDescription("List registered MCP servers"),
	), s.handleListMCPs)
}

func (s *Server) registerResources() {
	s.mcpServer.AddResource(mcp.NewResource(
		"context://session/{session_id}",
		"Injected context for session",
		mcp.WithMIMEType("application/json"),
	), s.handleContextResource)

	s.mcpServer.AddResource(mcp.NewResource(
		"vault://search/{query}",
		"Search vault notes",
		mcp.WithMIMEType("application/json"),
	), s.handleVaultSearchResource)

	s.mcpServer.AddResource(mcp.NewResource(
		"context://profile",
		"Developer profile",
		mcp.WithMIMEType("application/json"),
	), s.handleProfileResource)
}

func (s *Server) registerPrompts() {
	s.mcpServer.AddPrompt(mcp.NewPrompt("morning_brief",
		mcp.WithPromptDescription("Generate morning briefing with context, relevant notes, and schedule"),
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
		if f, ok := v.(float64); ok {
			return strconv.FormatFloat(f, 'f', -1, 64)
		}
	}
	return ""
}

func getArgStr(args map[string]string, key string) string {
	if v, ok := args[key]; ok {
		return v
	}
	return ""
}

func toAnyArgs(args map[string]string) map[string]any {
	result := make(map[string]any, len(args))
	for k, v := range args {
		result[k] = v
	}
	return result
}

func (s *Server) handleSearchNotes(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	query := getArg(args, "query")
	if query == "" {
		return mcp.NewToolResultError("query is required"), nil
	}
	limitStr := getArg(args, "limit")
	limit := 10
	if limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}
	if limit == 0 {
		limit = 10
	}

	links, err := s.store.SearchVaultNotes(query, limit)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("search failed: %v", err)), nil
	}

	var results []map[string]any
	for _, l := range links {
		content, title := s.readVaultNote(l.VaultNotePath)
		results = append(results, map[string]any{
			"path":        l.VaultNotePath,
			"title":       title,
			"snippet":     extractSnippet(content, query, 200),
			"confidence":  l.Confidence,
			"project":     l.EntityType,
			"entity_id":   l.EntityID,
		})
	}

	data, _ := json.MarshalIndent(results, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) readVaultNote(path string) (content, title string) {
	if s.vaultPath == "" {
		return "", ""
	}

	fullPath := filepath.Join(s.vaultPath, path)
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

func (s *Server) handleLinkNote(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	notePath := getArg(args, "note_path")
	noteTitle := getArg(args, "note_title")
	project := getArg(args, "project")
	linkType := getArg(args, "type")
	if linkType == "" {
		linkType = "reference"
	}
	confidence := 0.8
	if c := getArg(args, "confidence"); c != "" {
		fmt.Sscanf(c, "%f", &confidence)
	}

	if notePath == "" || project == "" {
		return mcp.NewToolResultError("note_path and project are required"), nil
	}

	if noteTitle == "" {
		_, noteTitle = s.readVaultNote(notePath)
	}

	if err := s.store.CreateVaultLink(notePath, noteTitle, project, project, linkType, confidence); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to link: %v", err)), nil
	}

	return mcp.NewToolResultText(fmt.Sprintf("Linked %s to %s", notePath, project)), nil
}

func (s *Server) handleUnlinkNote(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	notePath := getArg(args, "note_path")
	project := getArg(args, "project")

	if notePath == "" || project == "" {
		return mcp.NewToolResultError("note_path and project are required"), nil
	}

	if err := s.store.DeleteVaultLink(notePath, project, project); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to unlink: %v", err)), nil
	}

	return mcp.NewToolResultText("Unlinked"), nil
}

func (s *Server) handleGetContext(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	sessionID := getArg(args, "session_id")
	project := getArg(args, "project")
	if sessionID == "" {
		return mcp.NewToolResultError("session_id is required"), nil
	}

	ic, err := s.getContextForSession(sessionID, project)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("failed to get context: %v", err)), nil
	}

	data, _ := json.MarshalIndent(ic, "", "  ")
	return mcp.NewToolResultText(string(data)), nil
}

func (s *Server) getContextForSession(sessionID, project string) (map[string]any, error) {
	profile, _ := s.store.GetAllProfile()
	skills, _ := s.store.GetSkillProgress()

	var links []map[string]any
	if project != "" {
		dbLinks, _ := s.store.GetVaultLinksByEntity(project, project)
		for _, l := range dbLinks {
			content, title := s.readVaultNote(l.VaultNotePath)
			links = append(links, map[string]any{
				"path":       l.VaultNotePath,
				"title":      title,
				"snippet":    extractSnippet(content, project, 200),
				"confidence": l.Confidence,
			})
		}
	}

	return map[string]any{
		"session_id":    sessionID,
		"project":       project,
		"profile":       profile,
		"skills":        skills,
		"relevant_notes": links,
		"token_estimate": 1000 + len(links)*200,
	}, nil
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

func (s *Server) handleIndexVault(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	args := req.Params.Arguments
	limitStr := getArg(args, "limit")
	limit := 1000
	if limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}

	indexed := 0
	err := filepath.Walk(s.vaultPath, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || !strings.HasSuffix(strings.ToLower(info.Name()), ".md") {
			return nil
		}
		if indexed >= limit {
			return filepath.SkipDir
		}
		relPath, _ := filepath.Rel(s.vaultPath, path)
		content, title := s.readVaultNote(relPath)
		if content == "" {
			return nil
		}
		s.store.IndexVaultNote(relPath, title, content)
		indexed++
		return nil
	})

	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("index failed: %v", err)), nil
	}
	return mcp.NewToolResultText(fmt.Sprintf("Indexed %d markdown files from vault", indexed)), nil
}

func (s *Server) handleContextResource(ctx context.Context, req mcp.ReadResourceRequest) ([]mcp.ResourceContents, error) {
	args := req.Params.Arguments
	sessionID := getArg(args, "session_id")
	if sessionID == "" {
		return nil, fmt.Errorf("session_id required")
	}
	ic, err := s.getContextForSession(sessionID, "")
	if err != nil {
		return nil, err
	}
	data, _ := json.MarshalIndent(ic, "", "  ")
	return []mcp.ResourceContents{
		mcp.TextResourceContents{
			URI:      fmt.Sprintf("context://session/%s", sessionID),
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
			"path":       l.VaultNotePath,
			"title":      title,
			"snippet":    extractSnippet(content, query, 200),
			"confidence": l.Confidence,
		})
	}
	data, _ := json.MarshalIndent(results, "", "  ")
	return []mcp.ResourceContents{
		mcp.TextResourceContents{
			URI:      fmt.Sprintf("vault://search/%s", query),
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
			URI:      "context://profile",
			MIMEType: "application/json",
			Text:     string(data),
		},
	}, nil
}

func (s *Server) handleMorningBriefPrompt(ctx context.Context, req mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
	args := req.Params.Arguments
	sessionID := getArgStr(args, "session_id")
	if sessionID == "" {
		return nil, fmt.Errorf("session_id required")
	}
	ic, err := s.getContextForSession(sessionID, "")
	if err != nil {
		return nil, err
	}

	var brief strings.Builder
	brief.WriteString("# Morning Briefing\n\n")

	if ic["project"] != "" {
		brief.WriteString(fmt.Sprintf("## 🎯 Current Project: %s\n\n", ic["project"]))
	}

	if links, ok := ic["relevant_notes"].([]map[string]any); ok && len(links) > 0 {
		brief.WriteString("## 📝 Relevant Notes\n")
		for _, fn := range links {
			conf := 0.0
			if c, ok := fn["confidence"].(float64); ok {
				conf = c
			}
			brief.WriteString(fmt.Sprintf("- **%s** (%.0f%%)\n  %s\n\n", fn["title"], conf*100, fn["snippet"]))
		}
	}

	if skills, ok := ic["skills"].([]any); ok && len(skills) > 0 {
		brief.WriteString("## 📈 Skill Progress\n")
		for _, sp := range skills {
			if m, ok := sp.(map[string]any); ok {
				brief.WriteString(fmt.Sprintf("- %s: Level %v/%v\n", m["Name"], m["CurrentLevel"], m["TargetLevel"]))
			}
		}
	}

	brief.WriteString("---\n*Have a productive day!*")

	return mcp.NewGetPromptResult(
		"Morning briefing with project context and relevant notes",
		[]mcp.PromptMessage{{Role: "user", Content: mcp.TextContent{Type: "text", Text: brief.String()}}},
	), nil
}

func (s *Server) handleProjectContextPrompt(ctx context.Context, req mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
	args := req.Params.Arguments
	sessionID := getArgStr(args, "session_id")
	focus := getArgStr(args, "focus")
	if sessionID == "" {
		return nil, fmt.Errorf("session_id required")
	}
	ic, err := s.getContextForSession(sessionID, "")
	if err != nil {
		return nil, err
	}

	var context strings.Builder
	context.WriteString("# Project Context\n\n")
	if ic["project"] != "" {
		context.WriteString(fmt.Sprintf("## Project: %s\n\n", ic["project"]))
	}
	if focus != "" {
		context.WriteString(fmt.Sprintf("## Current Focus: %s\n\n", focus))
	}
	if links, ok := ic["relevant_notes"].([]map[string]any); ok {
		for _, fn := range links {
			context.WriteString(fmt.Sprintf("- **%s**: %s\n", fn["title"], fn["snippet"]))
		}
	}
	context.WriteString(fmt.Sprintf("\n*Token estimate: ~%d tokens*", ic["token_estimate"]))

	return mcp.NewGetPromptResult(
		"Project context for coding session",
		[]mcp.PromptMessage{{Role: "user", Content: mcp.TextContent{Type: "text", Text: context.String()}}},
	), nil
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