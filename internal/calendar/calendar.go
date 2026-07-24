package calendar

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"os"
	"strings"
	"time"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/calendar/v3"
	"google.golang.org/api/option"

	"kisuke-mcp/internal/store"
)

type Calendar struct {
	service *calendar.Service
	store   store.Store
}

func NewCalendar(credsPath string, st store.Store) (*Calendar, error) {
	ctx := context.Background()

	b, err := os.ReadFile(credsPath)
	if err != nil {
		return nil, fmt.Errorf("read credentials: %w", err)
	}

	config, err := google.ConfigFromJSON(b, calendar.CalendarReadonlyScope)
	if err != nil {
		return nil, fmt.Errorf("parse config: %w", err)
	}

	client := getClient(ctx, config)

	srv, err := calendar.NewService(ctx, option.WithHTTPClient(client))
	if err != nil {
		return nil, fmt.Errorf("create calendar service: %w", err)
	}

	return &Calendar{service: srv, store: st}, nil
}

func getClient(ctx context.Context, config *oauth2.Config) *http.Client {
	tokFile := "token.json"
	tok, err := tokenFromFile(tokFile)
	if err != nil {
		tok = getTokenFromWeb(config)
		saveToken(tokFile, tok)
	}
	return config.Client(ctx, tok)
}

func tokenFromFile(file string) (*oauth2.Token, error) {
	f, err := os.Open(file)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	tok := &oauth2.Token{}
	err = json.NewDecoder(f).Decode(tok)
	return tok, err
}

func getTokenFromWeb(config *oauth2.Config) *oauth2.Token {
	authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
	fmt.Printf("Go to the following link in your browser then type the authorization code: \n%v\n", authURL)

	var authCode string
	if _, err := fmt.Scan(&authCode); err != nil {
		log.Fatalf("Unable to read authorization code: %v", err)
	}

	tok, err := config.Exchange(context.TODO(), authCode)
	if err != nil {
		log.Fatalf("Unable to retrieve token from web: %v", err)
	}
	return tok
}

func saveToken(path string, token *oauth2.Token) {
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0600)
	if err != nil {
		log.Fatalf("Unable to cache oauth token: %v", err)
	}
	defer f.Close()
	json.NewEncoder(f).Encode(token)
}

func (c *Calendar) SyncEvents(ctx context.Context, hours int) ([]store.CalendarEvent, error) {
	now := time.Now()
	end := now.Add(time.Duration(hours) * time.Hour)

	events, err := c.service.Events.List("primary").
		TimeMin(now.Format(time.RFC3339)).
		TimeMax(end.Format(time.RFC3339)).
		SingleEvents(true).
		OrderBy("startTime").
		Do()
	if err != nil {
		return nil, fmt.Errorf("list events: %w", err)
	}

	var result []store.CalendarEvent
	for _, item := range events.Items {
		start := item.Start.DateTime
		if start == "" {
			start = item.Start.Date
		}
		end := item.End.DateTime
		if end == "" {
			end = item.End.Date
		}

		startTime, _ := time.Parse(time.RFC3339, start)
		endTime, _ := time.Parse(time.RFC3339, end)

		e := store.CalendarEvent{
			ID:          item.Id,
			Summary:     item.Summary,
			Description: item.Description,
			StartTime:   startTime,
			EndTime:     endTime,
			CalendarID:  item.ICalUID,
		}

		if item.Description != "" {
			e.ProjectTag = extractProjectTag(item.Description)
		}

		result = append(result, e)
	}

	if err := c.store.SyncCalendarEvents(result); err != nil {
		slog.Error("Failed to sync calendar events to store", "error", err)
	}

	return result, nil
}

func extractProjectTag(desc string) string {
	lines := strings.Split(desc, "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(strings.ToLower(line), "project:") {
			return strings.TrimSpace(strings.TrimPrefix(strings.ToLower(line), "project:"))
		}
	}
	return ""
}

func (c *Calendar) GetUpcomingEvents(hours int, projectTag string) ([]store.CalendarEvent, error) {
	return c.store.GetUpcomingEvents(hours, projectTag)
}