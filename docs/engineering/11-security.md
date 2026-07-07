# Security

> Source: MASTER_SPECIFICATION.md §12

---

# Purpose

This document defines the security principles of Kisuke.

Security must protect user data without reducing usability.

---

# Principles

- Local-first
- Least privilege
- Secure by default
- Explicit user consent
- Privacy first
- Zero hidden telemetry

---

# Security Goals

- Protect user data
- Prevent unauthorized modification
- Protect secrets
- Preserve data integrity
- Maintain user privacy

---

# Threat Model

Kisuke protects against:

- Accidental data loss
- Malicious plugins
- Secret leakage
- Corrupted indexes
- Unauthorized AI requests

Kisuke does not attempt to defend against:

- Full device compromise
- Physical theft
- Operating system compromise

---

# Authentication

Core Kisuke requires no authentication.

External services authenticate independently.

Examples:

- GitHub
- Google Calendar
- AI Providers

---

# Authorization

Every action is performed as the current user.

Kisuke never escalates privileges.

---

# Secrets

Secrets include:

- API Keys
- OAuth Tokens
- Access Tokens

Secrets must:

- Never be committed
- Never appear in logs
- Never appear in Markdown
- Never be indexed

Store secrets only in:

- Environment variables
- OS keychain (future)

---

# Data Ownership

Markdown owns data.

SQLite owns indexes.

AI owns nothing.

Git owns history.

---

# Encryption

At Rest

Delegated to the operating system.

In Transit

HTTPS only.

---

# Plugin Security

Plugins:

May

- Read public APIs
- Read approved files

May not

- Modify Core
- Access secrets directly
- Execute privileged operations
- Bypass validation

---

# AI Security

AI requests must:

- Use explicit provider configuration
- Send minimum required context
- Never include secrets
- Never automatically modify Markdown

---

# Logging

Logs may contain:

- Errors
- Timing
- Diagnostics

Logs must never contain:

- API Keys
- Tokens
- Passwords
- Private content

---

# File Integrity

Every write operation must be:

- Atomic
- Validated
- Recoverable

Never partially overwrite Markdown.

---

# Backup Strategy

Primary

Git

Secondary

User-managed backups

Cloud backup is optional.

---

# Validation

Before writing:

- Validate schema
- Validate references
- Validate ownership

Reject invalid writes.

---

# Failure Recovery

If corruption is detected:

- Stop write
- Preserve originals
- Report error
- Allow recovery

---

# Privacy

Kisuke collects:

Nothing.

No telemetry.

No analytics.

No usage tracking.

No crash reporting without explicit opt-in.

---

# Security Checklist

Every feature must satisfy:

- No secret leakage
- No hidden network calls
- No privilege escalation
- No ownership violations
- No Markdown corruption
- No automatic cloud upload

---

# Acceptance Criteria

Security is complete when:

- Secrets remain protected.
- Markdown integrity is preserved.
- AI cannot own data.
- Plugins cannot bypass validation.
- Core remains fully offline.