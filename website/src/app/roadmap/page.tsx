import type { Metadata } from "next";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { Reveal } from "@/components/ui/reveal";
import { Breadcrumbs } from "@/components/docs/breadcrumbs";
import { TimelineItem } from "@/components/roadmap/timeline-item";
import { VersionCard } from "@/components/roadmap/version-card";
import { PrincipleCard } from "@/components/roadmap/principle-card";
import { StatusStat } from "@/components/roadmap/status-stat";
import { ContributionFlow } from "@/components/roadmap/contribution-flow";
import { GithubIcon } from "@/components/ui/github-icon";

export const metadata: Metadata = {
  title: "Roadmap",
  description:
    "Kisuke development roadmap. From foundation to v1.0 — local-first context reconstruction for every developer.",
  openGraph: {
    title: "Roadmap — Kisuke",
    description:
      "Kisuke development roadmap. From foundation to v1.0 — local-first context reconstruction for every developer.",
    url: "https://kisuke.dev/roadmap",
    type: "website",
  },
};

const completedMilestones = [
  {
    title: "M0 — Repository Bootstrap",
    description:
      "Project structure, build system, test framework, documentation foundation, ADR system.",
    version: "v0.0.1",
    status: "completed" as const,
  },
  {
    title: "M1 — Domain Core",
    description:
      "11 entity types: Mission, Project, Task, Knowledge, Cookbook, Decision, Meeting, Person, Resource, Review, Attachment. Ownership graph, lifecycle states.",
    status: "completed" as const,
  },
  {
    title: "M2 — Markdown Storage",
    description:
      "One entity = one file. Frontmatter for metadata, body for content. Relationships stored by ID. FileRepository implementation.",
    status: "completed" as const,
  },
  {
    title: "M3 — Parser & Validation",
    description:
      "Schema validation, reference integrity checks, ownership verification, recovery suggestions. Full validation pipeline.",
    status: "completed" as const,
  },
  {
    title: "M4 — Search Engine",
    description:
      "Tantivy-powered full-text search. Filters, grouping, ranking. Warm search <500ms. Incremental indexing.",
    status: "completed" as const,
  },
  {
    title: "M5 — Resume Engine",
    description:
      "Deterministic context reconstruction. Fixed ordering. 8.8ms warm cache. ResumeService with search integration.",
    status: "completed" as const,
  },
  {
    title: "M6 — CLI",
    description:
      "20+ commands. JSON output, shell completion, health checks. Entry point: kisuke.cli.main. Performance: <200ms startup.",
    status: "completed" as const,
  },
  {
    title: "M7 — Review System",
    description:
      "Morning, weekly, monthly, quarterly reviews. Blockers and next actions. Review engine with Markdown output.",
    status: "completed" as const,
  },
  {
    title: "M8 — Integrations",
    description:
      "Git, GitHub, Obsidian, VS Code adapters. Filesystem watcher. Sync service with incremental indexing. 309 tests passing.",
    status: "completed" as const,
  },
  {
    title: "M9 — AI Abstraction",
    description:
      "Provider-independent interface. OpenAI, Anthropic, Gemini, Ollama support. AI owns nothing. Summarize, explain, classify, search.",
    status: "completed" as const,
  },
  {
    title: "M10 — Plugin System",
    description:
      "Interfaces, registry, loader. Plugins read, create derived artifacts, request changes. Never mutate core.",
    status: "completed" as const,
  },
  {
    title: "M11 — Polish & Release",
    description:
      "Documentation coverage, performance verification, security audit, v0.1.0 release.",
    status: "completed" as const,
  },
];

const futureMilestones = [
  {
    title: "v0.2 — Workflow Improvements",
    description:
      "Enhanced review templates, batch operations, improved search filters, workflow automation hooks.",
    status: "upcoming" as const,
  },
  {
    title: "v0.3 — Plugin Ecosystem",
    description:
      "Plugin marketplace, community plugins, extended AI providers, calendar integration improvements.",
    status: "upcoming" as const,
  },
  {
    title: "v1.0 — Stable Release",
    description:
      "Production-ready stability, full documentation, migration guides, long-term support.",
    status: "upcoming" as const,
  },
];

const versionCards = [
  {
    version: "v0.1",
    title: "Foundation",
    description:
      "Complete domain model, Markdown storage, search engine, resume engine, CLI, integrations, AI abstraction, plugin system. 309 tests. Zero runtime dependencies.",
    status: "released" as const,
  },
  {
    version: "v0.2",
    title: "Workflow Improvements",
    description:
      "Enhanced review templates, batch operations, improved search filters, workflow automation hooks.",
    status: "planned" as const,
  },
  {
    version: "v0.3",
    title: "Plugin Ecosystem",
    description:
      "Plugin marketplace, community plugins, extended AI providers, calendar integration improvements.",
    status: "planned" as const,
  },
  {
    version: "v1.0",
    title: "Stable Production Release",
    description:
      "Production-ready stability, full documentation, migration guides, long-term support commitment.",
    status: "future" as const,
  },
];

const principles = [
  {
    title: "Markdown First",
    description:
      "Markdown is the source of truth. One entity = one file. Human-readable, version-controlled, long-term durable.",
  },
  {
    title: "Offline First",
    description:
      "No cloud, no API calls, no telemetry. Everything runs on your machine. Works without internet.",
  },
  {
    title: "AI Optional",
    description:
      "AI may summarize, explain, classify, search. AI owns nothing. Core functions without any AI provider.",
  },
  {
    title: "Open Source",
    description:
      "MIT licensed. Community-driven. Transparent development. Contributions welcome.",
  },
  {
    title: "Deterministic",
    description:
      "Same input = same output. Resume is byte-for-byte deterministic. Search results are stable.",
  },
  {
    title: "Developer First",
    description:
      "Built for developers, by developers. CLI-first. JSON output. Shell completion. Scriptable.",
  },
];

export default function RoadmapPage() {
  return (
    <>
      <Navigation />
      <main className="pt-14">
        {/* Hero */}
        <Section className="pt-12 pb-12">
          <Breadcrumbs items={[{ label: "Roadmap" }]} />

          <Reveal>
            <Badge>Roadmap</Badge>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-3xl sm:text-4xl md:text-5xl font-medium tracking-tight text-text-primary leading-[1.1]">
              Roadmap.
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-4 text-lg text-text-secondary max-w-[600px] leading-relaxed">
              From foundation to v1.0. Local-first context reconstruction for
              every developer.
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-6 flex flex-wrap items-center gap-3 text-sm">
              <span className="font-mono text-text-tertiary">v0.1.0</span>
              <span className="px-2 py-0.5 text-xs font-medium bg-success/10 text-success rounded-full">
                Released
              </span>
              <span className="text-text-disabled">|</span>
              <a
                href="https://github.com/kisuke/kisuke"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-text-secondary hover:text-text-primary transition-colors duration-100"
              >
                <GithubIcon className="w-4 h-4" />
                GitHub
              </a>
            </div>
          </Reveal>
        </Section>

        {/* Current Status */}
        <Section id="status" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Current Status
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              v0.1.0 released.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              <StatusStat label="Version" value="v0.1.0" />
              <StatusStat label="Tests" value="309" />
              <StatusStat label="Coverage" value="95%+" />
              <StatusStat label="Runtime Deps" value="0" />
              <StatusStat label="License" value="MIT" />
            </div>
          </Reveal>
        </Section>

        {/* Timeline */}
        <Section id="timeline" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Development Timeline
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              12 milestones. All completed.
            </h2>
          </Reveal>

          <div className="max-w-[720px]">
            {completedMilestones.map((ms, i) => (
              <Reveal key={ms.title} delay={i * 40}>
                <TimelineItem
                  title={ms.title}
                  description={ms.description}
                  version={ms.version}
                  status={ms.status}
                  isLast={i === completedMilestones.length - 1}
                />
              </Reveal>
            ))}
          </div>

          <Reveal delay={500}>
            <div className="mt-4">
              <h3 className="text-sm font-medium text-text-primary mb-4">
                Up Next
              </h3>
              <div className="max-w-[720px]">
                {futureMilestones.map((ms, i) => (
                  <TimelineItem
                    key={ms.title}
                    title={ms.title}
                    description={ms.description}
                    status={ms.status}
                    isLast={i === futureMilestones.length - 1}
                  />
                ))}
              </div>
            </div>
          </Reveal>
        </Section>

        {/* Version Roadmap */}
        <Section id="versions" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Version Roadmap
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              What&apos;s next.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {versionCards.map((card) => (
                <VersionCard
                  key={card.version}
                  version={card.version}
                  title={card.title}
                  description={card.description}
                  status={card.status}
                />
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Principles */}
        <Section id="principles" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Principles
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              What guides us.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {principles.map((p) => (
                <PrincipleCard
                  key={p.title}
                  title={p.title}
                  description={p.description}
                />
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Long-Term Vision */}
        <Section id="vision" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Long-Term Vision
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              A developer knowledge system.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="bg-surface border border-border-subtle rounded-lg p-6 md:p-8 max-w-[800px]">
              <div className="space-y-4 text-sm text-text-secondary leading-relaxed">
                <p>
                  Context is rarely lost; knowledge is. Every interruption forces
                  manual context reconstruction. Developers lose hours each week
                  re-discovering what they already knew.
                </p>
                <p>
                  Kisuke exists to change that. Not a note-taking app. Not a
                  search engine. A context reconstruction system that returns
                  exactly what you need to continue meaningful work.
                </p>
                <p>
                  The vision: a local-first knowledge operating system that
                  understands your projects, your decisions, your workflow.
                  Everything in Markdown. Everything on your machine. AI
                  optional. Offline first.
                </p>
                <p>
                  v0.1.0 is the foundation. v1.0 is the promise delivered. The
                  journey continues.
                </p>
              </div>
            </div>
          </Reveal>
        </Section>

        {/* GitHub Contribution */}
        <Section id="contribute" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Contribute
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              How to contribute.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <ContributionFlow />
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-[800px]">
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Development Setup
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Clone, install with{" "}
                  <code className="font-mono text-accent">uv sync</code>, run
                  tests with{" "}
                  <code className="font-mono text-accent">uv run pytest</code>.
                  Ruff for linting, MyPy for types.
                </p>
              </div>
              <div className="bg-surface border border-border-subtle rounded-lg p-5">
                <h3 className="text-sm font-medium text-text-primary mb-2">
                  Architecture Changes
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Require RFC before PR. Constitution &gt; ADRs &gt; Architecture
                  &gt; Engineering &gt; Execution &gt; Source Code.
                </p>
              </div>
            </div>
          </Reveal>
        </Section>
      </main>
      <Footer />
    </>
  );
}
