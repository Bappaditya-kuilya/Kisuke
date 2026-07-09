import type { Metadata } from "next";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { Terminal } from "@/components/ui/terminal";
import { Reveal } from "@/components/ui/reveal";
import { Breadcrumbs } from "@/components/docs/breadcrumbs";
import { ArchitectureDiagram } from "@/components/architecture/architecture-diagram";
import { DataFlowDiagram } from "@/components/architecture/data-flow-diagram";
import { LayerCard } from "@/components/architecture/layer-card";
import { AdrCard } from "@/components/architecture/adr-card";
import { PerformanceStat } from "@/components/architecture/performance-stat";
import { GithubIcon } from "@/components/ui/github-icon";
import { JsonLd } from "@/components/ui/json-ld";

export const metadata: Metadata = {
  title: "Architecture",
  description:
    "Clean Architecture, DDD, and local-first design. See how Kisuke is built — eight layers, zero coupling, Markdown as source of truth.",
  openGraph: {
    title: "Architecture — Kisuke",
    description:
      "Clean Architecture, DDD, and local-first design. See how Kisuke is built — eight layers, zero coupling, Markdown as source of truth.",
    url: "https://kisuke.vercel.app/architecture",
    siteName: "Kisuke",
    type: "website",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "Architecture — Kisuke",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Architecture — Kisuke",
    description:
      "Clean Architecture, DDD, and local-first design. See how Kisuke is built — eight layers, zero coupling, Markdown as source of truth.",
    images: ["/og.svg"],
  },
  alternates: {
    canonical: "https://kisuke.vercel.app/architecture",
  },
};

const layers = [
  {
    name: "CLI (Presentation)",
    responsibility:
      "Command parsing, argument validation, output formatting. The only entry point for users. Never contains business logic.",
    dependsOn: "Application",
    usedBy: "User",
    modules: ["main.py", "commands.py", "format.py", "errors.py", "completion.py"],
    color: "#6366f1",
  },
  {
    name: "Application",
    responsibility:
      "Use cases, command orchestration, validation coordination. Translates CLI input into domain operations.",
    dependsOn: "Domain",
    usedBy: "CLI",
    modules: ["resume_app.py", "search_app.py", "tasks.py", "reviews.py", "doctor.py", "config_app.py"],
    color: "#86efac",
  },
  {
    name: "Domain (Core)",
    responsibility:
      "Entities, business rules, ownership graph, lifecycle states, context reconstruction logic. The source of truth. No external dependencies.",
    dependsOn: "Nothing",
    usedBy: "Application, Infrastructure",
    modules: ["entities/", "validation/", "ownership/", "lifecycle/", "relationships/", "ids/", "timestamps/"],
    color: "#c084fc",
  },
  {
    name: "Infrastructure",
    responsibility:
      "Markdown storage, SQLite indexing, filesystem operations, cache management. Implements Domain interfaces.",
    dependsOn: "Domain",
    usedBy: "Application",
    modules: ["storage/", "search/", "resume/", "validation/"],
    color: "#93c5fd",
  },
  {
    name: "Integrations",
    responsibility:
      "External system adapters. Git, GitHub, Obsidian, VS Code, Calendar. All optional. Never accessed by Domain.",
    dependsOn: "Domain interfaces",
    usedBy: "Application (optional)",
    modules: ["git.py", "sync.py", "watcher.py", "config.py", "export.py"],
    color: "#fbbf24",
  },
  {
    name: "AI",
    responsibility:
      "Provider-independent AI abstraction. Summarize, explain, classify, search. AI owns nothing.",
    dependsOn: "Domain interfaces",
    usedBy: "Application (optional)",
    modules: ["service.py", "interfaces.py", "providers/", "prompts.py", "config.py"],
    color: "#6366f1",
  },
];

const adrCards = [
  {
    id: "ADR-001",
    title: "Architecture Principles",
    status: "Accepted" as const,
    summary:
      "Adopts Clean Architecture, DDD, Local-first, Markdown-first, Offline-first, Git-native, Provider-independent AI, Documentation-first, Single ownership, Reference over duplication, Resume before search, Integrate before rebuilding.",
    details:
      "The Domain layer is independent of UI, Database, AI, and External services. CLI is the reference implementation. Dependencies always point inward. Architecture is frozen once accepted.",
  },
  {
    id: "ADR-002",
    title: "Markdown as Canonical Data Store",
    status: "Accepted" as const,
    summary:
      "Markdown is canonical. Everything else — SQLite, Search Index, Cache, Embeddings, AI Outputs — is derived and rebuildable.",
    details:
      "Rejected SQLite (not human-readable), JSON (poor long-term editing). Markdown provides readability, editability, version control compatibility, and long-term durability. One entity = one file. Relationships stored by ID only.",
  },
  {
    id: "ADR-003",
    title: "Provider Independent AI",
    status: "Accepted" as const,
    summary:
      "All AI goes through a Provider Interface. Supported: OpenAI, Anthropic, Gemini, Ollama, OpenRouter, any OpenAI-compatible. Core never knows which provider.",
    details:
      "No vendor lock-in. Adding a provider requires only a new adapter; Core remains unchanged. AI may summarize, explain, classify, extract, rank. AI may not own data, modify Markdown, or change ownership.",
  },
  {
    id: "ADR-004",
    title: "Plugin Architecture",
    status: "Accepted" as const,
    summary:
      "Optional functionality delivered as plugins. Core exposes stable interfaces. Plugins interact only through public APIs. Never modify Core directly.",
    details:
      "Plugins may: read, create derived artifacts, request changes. Plugins may not: mutate core directly, modify ownership, bypass validation. Plugin system includes interfaces, registry, and loader.",
  },
  {
    id: "ADR-005",
    title: "Resume Before Search",
    status: "Accepted" as const,
    summary:
      "Resume is the primary workflow. Search exists only to support resume. Every major feature must improve context reconstruction before search.",
    details:
      "Kisuke does not return notes. Kisuke returns working context. Resume reconstructs the exact context required to continue meaningful work. Search is a fallback when resume cannot determine the focus.",
  },
];

const repositoryTree = `kisuke/
├── src/kisuke/
│   ├── domain/           # Entities, rules, ownership
│   ├── application/      # Use cases, orchestration
│   ├── infrastructure/
│   │   ├── storage/      # Markdown read/write
│   │   ├── search/       # Tantivy index
│   │   ├── resume/       # Context reconstruction
│   │   └── validation/   # Schema + reference checks
│   ├── integrations/     # Git, GitHub, Obsidian, VS Code
│   ├── ai/               # Provider abstraction
│   ├── plugins/          # Interfaces, registry
│   ├── cli/              # Command interface
│   └── shared/           # Logging, config
├── tests/
│   ├── unit/             # Domain + Application
│   ├── integration/      # Infrastructure
│   └── e2e/              # CLI end-to-end
├── architecture/         # Design documents
├── docs/                 # Foundation + engineering
└── pyproject.toml        # Zero runtime dependencies`;

export default function ArchitecturePage() {
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "BreadcrumbList",
          itemListElement: [
            {
              "@type": "ListItem",
              position: 1,
              name: "Home",
              item: "https://kisuke.vercel.app",
            },
            {
              "@type": "ListItem",
              position: 2,
              name: "Architecture",
              item: "https://kisuke.vercel.app/architecture",
            },
          ],
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          name: "Architecture — Kisuke",
          description:
            "Clean Architecture, DDD, and local-first design. See how Kisuke is built — eight layers, zero coupling, Markdown as source of truth.",
          url: "https://kisuke.vercel.app/architecture",
          isPartOf: {
            "@type": "WebSite",
            name: "Kisuke",
            url: "https://kisuke.vercel.app",
          },
        }}
      />
      <Navigation />
      <main className="pt-14">
        {/* Hero */}
        <Section className="pt-12 pb-12">
          <Breadcrumbs items={[{ label: "Architecture" }]} />

          <Reveal>
            <Badge>Architecture</Badge>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-3xl sm:text-4xl md:text-5xl font-medium tracking-tight text-text-primary leading-[1.1]">
              Eight layers.
              <br />
              Zero coupling.
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-4 text-lg text-text-secondary max-w-[600px] leading-relaxed">
              Clean Architecture, DDD, and local-first design. Markdown is the
              source of truth. AI is optional. Core depends on nothing.
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-6 flex items-center gap-4 text-sm text-text-tertiary">
              <span className="font-mono">v0.1.0</span>
              <span className="text-text-disabled">|</span>
              <a
                href="https://github.com/kisuke/kisuke"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 hover:text-text-primary transition-colors duration-100"
              >
                <GithubIcon className="w-4 h-4" />
                View on GitHub
              </a>
            </div>
          </Reveal>
        </Section>

        {/* System Overview */}
        <Section id="overview" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              System Overview
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              High-level architecture.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <ArchitectureDiagram />
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Dependencies point inward
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Presentation depends on Application. Application depends on
                  Domain. Infrastructure implements Domain interfaces. Domain
                  depends on nothing.
                </p>
              </div>
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Markdown is source of truth
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  SQLite, search index, cache, and embeddings are derived.
                  Everything rebuildable from Markdown files alone.
                </p>
              </div>
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  AI is optional
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Core functions without any integration. AI, Git, Obsidian —
                  all optional. Failure = continue core functionality.
                </p>
              </div>
            </div>
          </Reveal>
        </Section>

        {/* Layer Breakdown */}
        <Section id="layers" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Layer Breakdown
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Every layer has one job.
            </h2>
          </Reveal>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {layers.map((layer, i) => (
              <Reveal key={layer.name} delay={i * 60}>
                <LayerCard
                  name={layer.name}
                  responsibility={layer.responsibility}
                  dependsOn={layer.dependsOn}
                  usedBy={layer.usedBy}
                  modules={layer.modules}
                  color={layer.color}
                />
              </Reveal>
            ))}
          </div>
        </Section>

        {/* Data Flow */}
        <Section id="data-flow" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Data Flow
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              From Markdown to output.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <DataFlowDiagram />
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Capture flow
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  User runs <code className="font-mono text-accent">kisuke &lt;entity&gt; add</code>.
                  CLI validates, writes one Markdown file. Relationships stored
                  by ID. Index rebuilt, never authored.
                </p>
              </div>
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Resume flow
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  User runs <code className="font-mono text-accent">kisuke resume</code>.
                  Engine loads Mission, Project, traverses relationships,
                  computes Next Action, returns ordered Context Stack.
                </p>
              </div>
            </div>
          </Reveal>
        </Section>

        {/* Repository Structure */}
        <Section id="repository" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Repository Structure
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Real project layout.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <Terminal title="tree -L 2">
              {repositoryTree}
            </Terminal>
          </Reveal>
        </Section>

        {/* Design Decisions */}
        <Section id="decisions" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Design Decisions
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Architecture Decision Records.
            </h2>
          </Reveal>

          <div className="space-y-3">
            {adrCards.map((adr, i) => (
              <Reveal key={adr.id} delay={i * 60}>
                <AdrCard
                  id={adr.id}
                  title={adr.title}
                  status={adr.status}
                  summary={adr.summary}
                  details={adr.details}
                />
              </Reveal>
            ))}
          </div>
        </Section>

        {/* Performance */}
        <Section id="performance" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Performance
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Measured. Verified.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              <PerformanceStat
                label="Resume latency"
                value="8.8"
                unit="ms"
                description="150 entities, warm cache"
                color="#86efac"
              />
              <PerformanceStat
                label="Search latency"
                value="<500"
                unit="ms"
                description="Warm index target"
                color="#93c5fd"
              />
              <PerformanceStat
                label="Tests passing"
                value="309"
                description="Unit + integration + E2E"
                color="#c084fc"
              />
              <PerformanceStat
                label="Runtime deps"
                value="0"
                description="Zero dependencies"
                color="#fbbf24"
              />
              <PerformanceStat
                label="CLI startup"
                value="<200"
                unit="ms"
                description="Cold start target"
                color="#6366f1"
              />
            </div>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 bg-surface border border-border-subtle rounded-lg p-6">
              <h3 className="text-sm font-medium text-text-primary mb-4">
                Benchmark Results
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border-subtle">
                      <th className="text-left py-2 text-text-tertiary font-medium text-xs uppercase tracking-wider">
                        Repository Size
                      </th>
                      <th className="text-left py-2 text-text-tertiary font-medium text-xs uppercase tracking-wider">
                        Warm Resume
                      </th>
                      <th className="text-left py-2 text-text-tertiary font-medium text-xs uppercase tracking-wider">
                        Repeated Resume
                      </th>
                    </tr>
                  </thead>
                  <tbody className="font-mono text-xs">
                    <tr className="border-b border-border-subtle">
                      <td className="py-2.5 text-text-secondary">150 entities</td>
                      <td className="py-2.5 text-code-string">8.8 ms</td>
                      <td className="py-2.5 text-text-secondary">9.5 ms</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 text-text-secondary">500 entities</td>
                      <td className="py-2.5 text-code-string">30.4 ms</td>
                      <td className="py-2.5 text-text-secondary">31.3 ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p className="mt-3 text-xs text-text-tertiary">
                All targets met. Warm cache resume &lt; 2s (actual: 8.8–30.4 ms).
                Linear scaling. Deterministic output verified.
              </p>
            </div>
          </Reveal>
        </Section>
      </main>
      <Footer />
    </>
  );
}
