import { Section } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Reveal } from "@/components/ui/reveal";
import { ArrowRight } from "lucide-react";

const layers = [
  {
    name: "CLI Layer",
    tech: "Typer",
    color: "text-code-keyword",
    description: "Command interface, argument parsing, output formatting",
  },
  {
    name: "Adapters",
    tech: "Plugins",
    color: "text-code-string",
    description: "GitHub, Obsidian, VS Code, MCP — provider-specific implementations",
  },
  {
    name: "AI Abstraction",
    tech: "Optional",
    color: "text-code-type",
    description: "Summarize, explain, classify, search — provider-independent",
  },
  {
    name: "Search",
    tech: "Tantivy",
    color: "text-code-function",
    description: "Full-text indexing, filters, grouping, ranking",
  },
  {
    name: "Resume Engine",
    tech: "Pure Python",
    color: "text-code-number",
    description: "Context reconstruction from git history, files, and metadata",
  },
  {
    name: "Graph",
    tech: "NetworkX",
    color: "text-code-keyword",
    description: "Ownership graph, dependency tracking, relationship analysis",
  },
  {
    name: "Metadata Store",
    tech: "SQLite",
    color: "text-code-string",
    description: "Lightweight storage, entity tracking, relationship mapping",
  },
  {
    name: "Domain Model",
    tech: "Pure Python",
    color: "text-code-type",
    description: "Entities, value objects, aggregates — the source of truth",
  },
];

function Architecture() {
  return (
    <Section id="architecture">
      <Reveal>
        <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
          How it&apos;s built
        </p>
      </Reveal>
      <Reveal delay={100}>
        <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-text-primary mb-12">
          Eight layers.
          <br />
          Zero coupling.
        </h2>
      </Reveal>

      <Reveal delay={200}>
        <Card className="bg-surface-inset border-border-subtle p-6 md:p-8">
          <div className="space-y-3">
            {layers.map((layer, i) => (
              <div
                key={layer.name}
                className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-border-subtle last:border-b-0"
              >
                <div className="flex items-center gap-3 min-w-[200px]">
                  {i > 0 && (
                    <ArrowRight className="w-3 h-3 text-text-disabled hidden sm:block" />
                  )}
                  <span
                    className={`font-mono text-sm font-medium ${layer.color}`}
                  >
                    {layer.name}
                  </span>
                </div>
                <span className="text-xs text-text-tertiary font-mono w-20">
                  {layer.tech}
                </span>
                <span className="text-sm text-text-secondary">
                  {layer.description}
                </span>
              </div>
            ))}
          </div>
          <div className="mt-6 pt-4 border-t border-border-subtle">
            <p className="text-xs text-text-tertiary">
              Core is provider-independent. AI is optional. Plugins read, create
              derived artifacts, and request changes. They never mutate core
              directly.
            </p>
          </div>
        </Card>
      </Reveal>
    </Section>
  );
}

export { Architecture };
