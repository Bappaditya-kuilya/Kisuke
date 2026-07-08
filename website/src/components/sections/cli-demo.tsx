"use client";

import { useState } from "react";
import { Section } from "@/components/ui/section";
import { Terminal } from "@/components/ui/terminal";
import { Reveal } from "@/components/ui/reveal";

type CommandId = "resume" | "search" | "graph" | "review";

interface CommandEntry {
  id: CommandId;
  label: string;
  command: string;
  output: string;
}

const commands: CommandEntry[] = [
  {
    id: "resume",
    label: "Resume",
    command: "kisuke resume --focus feat/search-api",
    output: `Reconstructing context for feat/search-api...

Files changed:     14
Commits analyzed:  3
Branch:            feat/search-api
Time window:       2025-12-01 → 2025-12-15

Key entities:
  • SearchEngine (search/engine.py)
  • QueryParser (search/parser.py)
  • RankingModel (search/ranking.py)

Context ready. Use --format json for structured output.`,
  },
  {
    id: "search",
    label: "Search",
    command: "kisuke search 'authentication middleware' --limit 5",
    output: `Found 5 results (12ms):

  1. src/auth/middleware.py    [score: 0.94]
     JWT validation, token refresh, role-based access

  2. src/api/decorators.py     [score: 0.87]
     @require_auth decorator, permission checks

  3. src/config/settings.py    [score: 0.82]
     AUTH_SECRET_KEY, TOKEN_EXPIRY, ALLOWED_ROLES

  4. tests/test_auth.py        [score: 0.79]
     Integration tests for auth flow

  5. docs/authentication.md    [score: 0.71]
     Authentication architecture overview`,
  },
  {
    id: "graph",
    label: "Graph",
    command: "kisuke graph --focus src/auth/ --depth 2",
    output: `Ownership graph for src/auth/ (depth: 2):

  src/auth/middleware.py
    → owns: JWT validation, token refresh
    → depends: src/config/settings.py
    → depends: src/auth/tokens.py

  src/auth/tokens.py
    → owns: token generation, signing
    → depends: src/config/settings.py

  src/auth/roles.py
    → owns: role definitions, permissions
    → depends: nothing (leaf)

Ownership: 1 entity, 3 files, 5 dependencies`,
  },
  {
    id: "review",
    label: "Review",
    command: "kisuke review --since 7d",
    output: `Weekly review — last 7 days:

  Commits: 12
  Files:   23
  Lines:   +847 / -203

  Focus areas:
  • auth (8 commits) — major refactor
  • api (3 commits) — new endpoints
  • docs (1 commit) — updated README

  Suggested review:
  1. src/auth/middleware.py — large changes, 3 open questions
  2. src/api/routes.py — new patterns, verify consistency`,
  },
];

function CliDemo() {
  const [active, setActive] = useState<CommandId>("resume");
  const entry = commands.find((c) => c.id === active)!;

  return (
    <Section id="cli">
      <Reveal>
        <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
          CLI experience
        </p>
      </Reveal>
      <Reveal delay={100}>
        <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-text-primary mb-12">
          Fast. Focused. Familiar.
        </h2>
      </Reveal>

      <Reveal delay={200}>
        <div className="flex flex-wrap gap-2 mb-6">
          {commands.map((cmd) => (
            <button
              key={cmd.id}
              onClick={() => setActive(cmd.id)}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors duration-100 ${
                active === cmd.id
                  ? "bg-surface-raised text-text-primary"
                  : "text-text-secondary hover:text-text-primary hover:bg-surface-raised"
              }`}
            >
              {cmd.label}
            </button>
          ))}
        </div>
      </Reveal>

      <Reveal delay={300}>
        <Terminal title={`kisuke ${active}`}>
          <span className="text-text-tertiary">$</span>{" "}
          <span className="text-text-primary">{entry.command}</span>
          {"\n\n"}
          <span className="text-code-comment">{entry.output}</span>
        </Terminal>
      </Reveal>
    </Section>
  );
}

export { CliDemo };
