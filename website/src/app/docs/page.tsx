import type { Metadata } from "next";
import Link from "next/link";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { Reveal } from "@/components/ui/reveal";
import { Breadcrumbs } from "@/components/docs/breadcrumbs";
import { DocCard } from "@/components/docs/doc-card";
import { QuickStartStep } from "@/components/docs/quick-start-step";
import { CliCheatSheet } from "@/components/docs/cli-cheat-sheet";
import { JsonLd } from "@/components/ui/json-ld";
import {
  BookOpen,
  Download,
  Layers,
  Terminal,
  Search,
  RotateCcw,
  Bot,
  Puzzle,
  Boxes,
  Code,
  HelpCircle,
  Zap,
  ArrowRight,
  Command,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "Learn how to use Kisuke for local-first context reconstruction. Guides, references, and CLI documentation.",
  openGraph: {
    title: "Documentation — Kisuke",
    description:
      "Learn how to use Kisuke for local-first context reconstruction. Guides, references, and CLI documentation.",
    url: "https://kisuke.vercel.app/docs",
    siteName: "Kisuke",
    type: "website",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "Documentation — Kisuke",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Documentation — Kisuke",
    description:
      "Learn how to use Kisuke for local-first context reconstruction. Guides, references, and CLI documentation.",
    images: ["/og.svg"],
  },
  alternates: {
    canonical: "https://kisuke.vercel.app/docs",
  },
};

const categories = [
  {
    icon: BookOpen,
    title: "Getting Started",
    description:
      "Quick overview of what Kisuke is, how it works, and how to get running in under 2 minutes.",
    href: "#quick-start",
    category: "foundation",
  },
  {
    icon: Download,
    title: "Installation",
    description:
      "Install Kisuke via pip, verify your setup, and configure your first repository.",
    href: "#quick-start",
    category: "setup",
  },
  {
    icon: Layers,
    title: "Core Concepts",
    description:
      "Missions, projects, tasks, knowledge, decisions, and the ownership graph.",
    href: "#categories",
    category: "domain",
  },
  {
    icon: Terminal,
    title: "CLI Reference",
    description:
      "Every command, flag, and option. With examples and exit codes.",
    href: "#cli-cheat-sheet",
    category: "reference",
  },
  {
    icon: Search,
    title: "Search Engine",
    description:
      "Full-text search, filters, ranking, and scope control over your entire graph.",
    href: "#categories",
    category: "engine",
  },
  {
    icon: RotateCcw,
    title: "Resume Engine",
    description:
      "Context reconstruction from commits, files, and conversations. Focus on branches or time windows.",
    href: "#categories",
    category: "engine",
  },
  {
    icon: Bot,
    title: "AI Abstraction",
    description:
      "Optional provider-independent AI for summarization, classification, and search.",
    href: "#categories",
    category: "integration",
  },
  {
    icon: Puzzle,
    title: "Integrations",
    description:
      "Git, GitHub, Obsidian, VS Code, and Google Calendar adapters.",
    href: "#categories",
    category: "integration",
  },
  {
    icon: Boxes,
    title: "Architecture",
    description:
      "Clean Architecture, DDD, layered design, and dependency rules.",
    href: "#categories",
    category: "engineering",
  },
  {
    icon: Code,
    title: "API",
    description:
      "Python API for programmatic access to Kisuke's domain, search, and resume engines.",
    href: "#categories",
    category: "reference",
  },
  {
    icon: HelpCircle,
    title: "FAQ",
    description:
      "Common questions about local-first operation, data ownership, and AI usage.",
    href: "#categories",
    category: "support",
  },
];

const documentationCards = [
  {
    title: "Vision & Philosophy",
    description:
      "Why Kisuke exists, what it solves, and the principles it follows.",
    href: "/docs/vision",
    category: "foundation",
    readTime: "3 min",
    difficulty: "beginner" as const,
  },
  {
    title: "Domain Model",
    description:
      "Entities, value objects, aggregates, and the ownership graph.",
    href: "/docs/domain-model",
    category: "domain",
    readTime: "8 min",
    difficulty: "intermediate" as const,
  },
  {
    title: "Markdown Storage",
    description:
      "One entity = one file. Relationships by ID. Derived index rebuilt, never authored.",
    href: "/docs/storage",
    category: "engine",
    readTime: "5 min",
    difficulty: "beginner" as const,
  },
  {
    title: "Search Engine",
    description:
      "Tantivy-powered full-text search with filters, grouping, and ranking.",
    href: "/docs/search",
    category: "engine",
    readTime: "6 min",
    difficulty: "intermediate" as const,
  },
  {
    title: "Resume Engine",
    description:
      "Deterministic context reconstruction. Fixed ordering. Sub-30ms warm cache.",
    href: "/docs/resume",
    category: "engine",
    readTime: "7 min",
    difficulty: "intermediate" as const,
  },
  {
    title: "CLI Specification",
    description:
      "Command tree, global flags, exit codes, and JSON output mode.",
    href: "/docs/cli",
    category: "reference",
    readTime: "10 min",
    difficulty: "beginner" as const,
  },
  {
    title: "AI Abstraction Layer",
    description:
      "Provider-independent interface. Summarize, explain, classify, search.",
    href: "/docs/ai",
    category: "integration",
    readTime: "5 min",
    difficulty: "intermediate" as const,
  },
  {
    title: "Integrations",
    description:
      "Git, GitHub, Obsidian, VS Code, and Calendar adapters. All optional.",
    href: "/docs/integrations",
    category: "integration",
    readTime: "4 min",
    difficulty: "beginner" as const,
  },
  {
    title: "Engineering Architecture",
    description:
      "Clean Architecture layers, dependency rules, and module boundaries.",
    href: "/docs/architecture",
    category: "engineering",
    readTime: "9 min",
    difficulty: "advanced" as const,
  },
  {
    title: "Review System",
    description:
      "Morning, weekly, monthly, and quarterly reviews. Blockers and next actions.",
    href: "/docs/reviews",
    category: "engine",
    readTime: "4 min",
    difficulty: "beginner" as const,
  },
  {
    title: "Plugin System",
    description:
      "Interfaces, registry, loader. Read, derive, request. Never mutate core.",
    href: "/docs/plugins",
    category: "integration",
    readTime: "5 min",
    difficulty: "advanced" as const,
  },
  {
    title: "Security",
    description:
      "Local-first guarantees, data ownership, and optional AI provider trust.",
    href: "/docs/security",
    category: "support",
    readTime: "3 min",
    difficulty: "beginner" as const,
  },
];

export default function DocsPage() {
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
              name: "Documentation",
              item: "https://kisuke.vercel.app/docs",
            },
          ],
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          name: "Documentation — Kisuke",
          description:
            "Learn how to use Kisuke for local-first context reconstruction. Guides, references, and CLI documentation.",
          url: "https://kisuke.vercel.app/docs",
          isPartOf: {
            "@type": "WebSite",
            name: "Kisuke",
            url: "https://kisuke.vercel.app",
          },
        }}
      />
      <Navigation />
      <main className="pt-14">
        <Section className="pt-12 pb-12">
          <Breadcrumbs items={[{ label: "Documentation" }]} />

          <Reveal>
            <Badge>Documentation</Badge>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-3xl sm:text-4xl md:text-5xl font-medium tracking-tight text-text-primary leading-[1.1]">
              Learn Kisuke.
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-4 text-lg text-text-secondary max-w-[600px] leading-relaxed">
              Everything you need to get started, understand the architecture,
              and master the CLI.
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 flex flex-col sm:flex-row items-start gap-3">
              <Link
                href="#quick-start"
                className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-accent text-white rounded-full hover:bg-accent-hover transition-colors duration-100"
              >
                <Zap className="w-4 h-4" />
                Quick Start
              </Link>
              <div className="flex items-center gap-2 px-4 py-2 text-sm text-text-tertiary bg-surface border border-border-subtle rounded-full">
                <Command className="w-4 h-4" />
                <span className="font-mono text-xs">
                  Press{" "}
                  <kbd className="px-1.5 py-0.5 bg-surface-raised border border-border-subtle rounded text-text-secondary">
                    /
                  </kbd>{" "}
                  to search
                </span>
              </div>
            </div>
          </Reveal>
        </Section>

        <Section id="categories" className="pt-0 pb-16">
          <Reveal>
            <h2 className="text-2xl font-medium tracking-tight text-text-primary mb-8">
              Documentation Categories
            </h2>
          </Reveal>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {categories.map((cat, i) => (
              <Reveal key={cat.title} delay={i * 50}>
                <DocCard
                  icon={cat.icon}
                  title={cat.title}
                  description={cat.description}
                  href={cat.href}
                  category={cat.category}
                />
              </Reveal>
            ))}
          </div>
        </Section>

        <Section id="quick-start" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Quick Start
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Up and running in 60 seconds.
            </h2>
          </Reveal>

          <div className="max-w-[720px] space-y-8">
            <Reveal delay={200}>
              <QuickStartStep
                step={1}
                title="Install Kisuke"
                command="pip install kisuke"
                description="Requires Python 3.12+. Zero runtime dependencies."
              />
            </Reveal>
            <Reveal delay={250}>
              <QuickStartStep
                step={2}
                title="Initialize your repository"
                command="kisuke init"
                description="Creates the .kisuke directory structure and configures your workspace."
              />
            </Reveal>
            <Reveal delay={300}>
              <QuickStartStep
                step={3}
                title="Create a mission"
                command='kisuke mission create "Product Launch"'
                description="A mission is the top-level container. It owns projects, reviews, and context."
              />
            </Reveal>
            <Reveal delay={350}>
              <QuickStartStep
                step={4}
                title="Add a project and tasks"
                command='kisuke project create "Landing Page" && kisuke task add "Design hero section"'
                description="Projects live under missions. Tasks, knowledge, and decisions live under projects."
              />
            </Reveal>
            <Reveal delay={400}>
              <QuickStartStep
                step={5}
                title="Resume your context"
                command="kisuke resume"
                description="Reconstructs the full working context. Mission, project, tasks, decisions, and next action."
              />
            </Reveal>
            <Reveal delay={450}>
              <QuickStartStep
                step={6}
                title="Search across everything"
                command='kisuke search "hero section"'
                description="Full-text search over all entities. Results in under 500ms on warm index."
              />
            </Reveal>
          </div>

          <Reveal delay={500}>
            <div className="mt-10">
              <Link
                href="#quick-start"
                className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent-hover transition-colors duration-100"
              >
                Read the full getting started guide
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </Reveal>
        </Section>

        <Section id="docs-grid" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              All Documentation
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Browse by topic.
            </h2>
          </Reveal>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {documentationCards.map((card, i) => (
              <Reveal key={card.title} delay={i * 50}>
                <DocCard
                  icon={BookOpen}
                  title={card.title}
                  description={card.description}
                  href={card.href}
                  category={card.category}
                  readTime={card.readTime}
                  difficulty={card.difficulty}
                />
              </Reveal>
            ))}
          </div>
        </Section>

        <Section id="cli-cheat-sheet" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Reference
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              CLI Cheat Sheet.
            </h2>
          </Reveal>

          <CliCheatSheet />

          <Reveal delay={200}>
            <div className="mt-8">
              <Link
                href="#cli-cheat-sheet"
                className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent-hover transition-colors duration-100"
              >
                Full CLI reference
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </Reveal>
        </Section>
      </main>
      <Footer />
    </>
  );
}
