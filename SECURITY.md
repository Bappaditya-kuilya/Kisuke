# Security Policy

---

# Reporting Vulnerabilities

If you discover a security vulnerability in Kisuke, please report it responsibly.

Do not open a public GitHub issue for security vulnerabilities.

Instead, please email the maintainers directly.

---

# Scope

Kisuke is a local-first context reconstruction tool.

Security considerations:

- Kisuke operates on local files only
- No data is transmitted externally by default
- AI integrations are optional and require explicit configuration
- API keys are read from environment variables only

---

# Secrets

Kisuke never:

- Commits secrets to version control
- Stores API keys in configuration files
- Transmits secrets over the network without explicit user action
- Logs secrets or API keys

---

# AI Security

When using AI providers:

- API keys are stored in environment variables only
- Context is sent to providers only when explicitly requested
- No data is uploaded automatically
- Users control what context is shared

---

# File System Security

Kisuke operates with the permissions of the user running it.

No privilege escalation.

No hidden file operations.

All file operations are visible and predictable.

---

# Dependencies

Kisuke minimizes external dependencies.

All dependencies are:

- Actively maintained
- Well-established
- Permissively licensed

---

# Version Support

Security updates are provided for:

- Current major version
- Previous major version (for 12 months)

---

# Acknowledgments

We appreciate responsible disclosure of security vulnerabilities.
