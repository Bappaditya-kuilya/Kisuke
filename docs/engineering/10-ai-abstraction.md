# AI Abstraction

> Source: MASTER_SPECIFICATION.md §11

---

# Purpose

This document defines how AI capabilities integrate with Kisuke.

AI is an enhancement.

AI is never a dependency.

---

# Principles

- AI is optional.
- Provider-independent.
- Stateless.
- Replaceable.
- No vendor lock-in.
- No business logic inside providers.

---

# Responsibilities

AI may:

- Summarize
- Explain
- Classify
- Extract
- Rank
- Generate search keywords
- Reconstruct context
- Answer questions about existing data

AI may not:

- Own data
- Modify Markdown automatically
- Change ownership
- Execute actions without approval
- Become the source of truth

---

# Architecture

```text
Core
   │
   ▼
AI Service
   │
   ▼
Provider Interface
   │
   ├── OpenAI
   ├── Anthropic
   ├── Gemini
   ├── Ollama
   ├── OpenRouter
   └── OpenAI-Compatible
```

The Core never communicates directly with a provider.

---

# Provider Interface

Every provider implements the same contract.

Required operations:

- Chat
- Embeddings
- Reranking (optional)
- Model Listing
- Health Check

---

# Configuration

Configuration is external.

Supported:

- Environment variables
- Configuration file

Never hardcode:

- API keys
- Endpoints
- Models

---

# Model Selection

Users choose:

- Provider
- Model
- Temperature
- Token limits

Changing providers must require configuration only.

No code changes.

---

# Prompt Rules

Prompts are:

- Version controlled
- Reusable
- Independent of providers

Never embed prompts inside application logic.

---

# Context Rules

AI receives only the minimum context required.

Priority:

1. Current Project
2. Current Task
3. Related Decisions
4. Relevant Knowledge
5. Resources

Entire repositories are never sent by default.

---

# Privacy

Default behavior:

Local.

Cloud providers require explicit configuration.

No data is uploaded automatically.

---

# Failure Handling

If AI fails:

- Continue normally.
- Show meaningful error.
- Never block core workflows.
- Never lose user data.

---

# Performance

AI requests must:

- Support timeout.
- Support cancellation.
- Support retries.
- Return structured responses.

---

# Provider Requirements

Every provider must support:

- Authentication
- Streaming (optional)
- Timeouts
- Error handling
- Structured responses

---

# Future Providers

Adding a provider must require:

- New adapter only.

Core must remain unchanged.

---

# Acceptance Criteria

- Core works without AI.
- Providers are interchangeable.
- No provider-specific logic exists in Core.
- AI never owns data.
- AI failures never break Kisuke.