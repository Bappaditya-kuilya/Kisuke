import type { Metadata } from "next";
import Link from "next/link";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { Reveal } from "@/components/ui/reveal";
import { Breadcrumbs } from "@/components/docs/breadcrumbs";
import { GithubIcon } from "@/components/ui/github-icon";
import { JsonLd } from "@/components/ui/json-ld";

export const metadata: Metadata = {
  title: "About",
  description:
    "About Kisuke — local-first context reconstruction. Why it exists, how it works, and what guides it.",
  openGraph: {
    title: "About — Kisuke",
    description:
      "About Kisuke — local-first context reconstruction. Why it exists, how it works, and what guides it.",
    url: "https://kisuke.vercel.app/about",
    siteName: "Kisuke",
    type: "website",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "About — Kisuke",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "About — Kisuke",
    description:
      "About Kisuke — local-first context reconstruction. Why it exists, how it works, and what guides it.",
    images: ["/og.svg"],
  },
  alternates: {
    canonical: "https://kisuke.vercel.app/about",
  },
};

const philosophies = [
  {
    title: "Markdown First",
    description:
      "Markdown is the source of truth. One entity equals one file. Human-readable, version-controlled, long-term durable. No proprietary formats.",
  },
  {
    title: "Offline First",
    description:
      "No cloud, no API calls, no telemetry. Everything runs on your machine. Works without internet. Your data never leaves your device.",
  },
  {
    title: "AI Optional",
    description:
      "AI may summarize, explain, classify, search. AI owns nothing. Core functions without any AI provider. You choose whether to use AI.",
  },
  {
    title: "Deterministic",
    description:
      "Same input equals same output. Resume is byte-for-byte deterministic. Search results are stable. No randomness, no surprises.",
  },
  {
    title: "Open Source",
    description:
      "MIT licensed. Community-driven. Transparent development. Every decision documented. Contributions welcome.",
  },
  {
    title: "Developer First",
    description:
      "Built for developers, by developers. CLI-first. JSON output. Shell completion. Scriptable. Fast.",
  },
];

const problems = [
  {
    title: "Losing context",
    description:
      "Every interruption forces manual context reconstruction. Developers lose hours each week re-discovering what they already knew.",
  },
  {
    title: "Fragmented notes",
    description:
      "Notes scattered across apps, files, chats, and browser tabs. No single source of truth. No relationships between ideas.",
  },
  {
    title: "Weak search",
    description:
      "Keyword search returns noise. No understanding of project structure, ownership, or relationships. Results lack context.",
  },
  {
    title: "AI without memory",
    description:
      "AI assistants start fresh every conversation. No project context. No decision history. No understanding of your workflow.",
  },
];

const techStack = [
  {
    name: "Python",
    description: "Core language. 3.12+. Type-safe with MyPy strict.",
  },
  {
    name: "SQLite",
    description: "Search index. Tantivy-powered full-text search.",
  },
  {
    name: "Markdown",
    description: "Source of truth. One entity per file. YAML frontmatter.",
  },
  {
    name: "Next.js",
    description: "Marketing website. App Router. Static generation.",
  },
  {
    name: "Tailwind CSS",
    description: "Design system. Dark mode. Responsive. Utility-first.",
  },
  {
    name: "Framer Motion",
    description: "Scroll reveals. Reduced motion respected.",
  },
];

export default function AboutPage() {
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
              name: "About",
              item: "https://kisuke.vercel.app/about",
            },
          ],
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          name: "About — Kisuke",
          description:
            "About Kisuke — local-first context reconstruction. Why it exists, how it works, and what guides it.",
          url: "https://kisuke.vercel.app/about",
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
          <Breadcrumbs items={[{ label: "About" }]} />

          <Reveal>
            <Badge>About</Badge>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-3xl sm:text-4xl md:text-5xl font-medium tracking-tight text-text-primary leading-[1.1]">
              About Kisuke.
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-4 text-lg text-text-secondary max-w-[600px] leading-relaxed">
              Local-first context reconstruction. Kisuke does not return notes.
              Kisuke returns working context.
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-6 flex flex-wrap items-center gap-3 text-sm">
              <span className="font-mono text-text-tertiary">v0.1.0</span>
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

        {/* Philosophy */}
        <Section id="philosophy" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Philosophy
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              What guides us.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {philosophies.map((p) => (
                <div
                  key={p.title}
                  className="bg-surface border border-border-subtle rounded-lg p-5"
                >
                  <h3 className="text-sm font-medium text-text-primary mb-2">
                    {p.title}
                  </h3>
                  <p className="text-xs text-text-secondary leading-relaxed">
                    {p.description}
                  </p>
                </div>
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Why Kisuke Exists */}
        <Section id="why" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Why Kisuke Exists
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-4">
              The problem.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
              {problems.map((p) => (
                <div
                  key={p.title}
                  className="bg-surface border border-border-subtle rounded-lg p-5"
                >
                  <h3 className="text-sm font-medium text-text-primary mb-2">
                    {p.title}
                  </h3>
                  <p className="text-xs text-text-secondary leading-relaxed">
                    {p.description}
                  </p>
                </div>
              ))}
            </div>
          </Reveal>

          <Reveal delay={300}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-4">
              The solution.
            </h2>
          </Reveal>

          <Reveal delay={400}>
            <div className="bg-surface border border-border-subtle rounded-lg p-6 md:p-8 max-w-[800px]">
              <div className="space-y-4 text-sm text-text-secondary leading-relaxed">
                <p>
                  Context is rarely lost; knowledge is. Every interruption forces
                  manual context reconstruction. Kisuke exists to change that.
                </p>
                <p>
                  Not a note-taking app. Not a search engine. A context
                  reconstruction system that returns exactly what you need to
                  continue meaningful work.
                </p>
                <p>
                  Kisuke reconstructs the exact context required to continue
                  meaningful work. From your code, commits, documents, and
                  conversations. Everything stays local. AI is optional.
                </p>
              </div>
            </div>
          </Reveal>
        </Section>

        {/* Core Architecture */}
        <Section id="architecture" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Core Architecture
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              How it works.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="max-w-[720px]">
              <svg
                viewBox="0 0 700 200"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="w-full h-auto"
                role="img"
                aria-label="Core architecture: Markdown to Validation to Search to Resume to CLI"
              >
                <rect width="700" height="200" fill="#08080a" rx="8" />

                {[
                  { label: "Markdown", color: "#c084fc" },
                  { label: "Validation", color: "#86efac" },
                  { label: "Search", color: "#fbbf24" },
                  { label: "Resume", color: "#f9a8d4" },
                  { label: "CLI", color: "#ececef" },
                ].map((step, i) => {
                  const x = 50 + i * 130;
                  return (
                    <g key={step.label}>
                      <rect
                        x={x}
                        y="65"
                        width="104"
                        height="50"
                        rx="8"
                        fill="#111113"
                        stroke={step.color}
                        strokeWidth="1"
                        strokeOpacity="0.4"
                      />
                      <text
                        x={x + 52}
                        y="95"
                        textAnchor="middle"
                        fill="#ececef"
                        fontSize="13"
                        fontFamily="system-ui"
                        fontWeight="500"
                      >
                        {step.label}
                      </text>
                      {i < 4 && (
                        <>
                          <line
                            x1={x + 104}
                            y1="90"
                            x2={x + 130}
                            y2="90"
                            stroke="#45454d"
                            strokeWidth="1"
                          />
                          <polygon
                            points={`${x + 130},90 ${x + 124},86 ${x + 124},94`}
                            fill="#45454d"
                          />
                        </>
                      )}
                    </g>
                  );
                })}

                <text
                  x="350"
                  y="150"
                  textAnchor="middle"
                  fill="#6b6b73"
                  fontSize="11"
                  fontFamily="system-ui"
                >
                  Markdown is source of truth. AI is optional.
                </text>

                <rect
                  x="280"
                  y="160"
                  width="52"
                  height="18"
                  rx="9"
                  fill="#6366f1"
                  fillOpacity="0.15"
                />
                <text
                  x="306"
                  y="172"
                  textAnchor="middle"
                  fill="#6366f1"
                  fontSize="9"
                  fontFamily="system-ui"
                  fontWeight="500"
                >
                  OPTIONAL
                </text>
              </svg>
            </div>
          </Reveal>

          <Reveal delay={300}>
            <Link
              href="/architecture"
              className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent-hover transition-colors duration-100 mt-6"
            >
              Read the full architecture documentation
            </Link>
          </Reveal>
        </Section>

        {/* Project Statistics */}
        <Section id="stats" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Project Statistics
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Measured. Verified.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
              {[
                { label: "Version", value: "v0.1.0" },
                { label: "Tests", value: "309" },
                { label: "Coverage", value: "95%+" },
                { label: "Runtime Deps", value: "0" },
                { label: "License", value: "MIT" },
                { label: "Python", value: "3.12+" },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="bg-surface border border-border-subtle rounded-lg p-5 text-center"
                >
                  <div className="text-2xl font-medium tracking-tight text-text-primary mb-1">
                    {stat.value}
                  </div>
                  <div className="text-xs text-text-tertiary">{stat.label}</div>
                </div>
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Tech Stack */}
        <Section id="tech" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Tech Stack
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Built with.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {techStack.map((tech) => (
                <div
                  key={tech.name}
                  className="bg-surface border border-border-subtle rounded-lg p-5"
                >
                  <h3 className="text-sm font-medium text-text-primary mb-1">
                    {tech.name}
                  </h3>
                  <p className="text-xs text-text-secondary leading-relaxed">
                    {tech.description}
                  </p>
                </div>
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Open Source */}
        <Section id="open-source" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Open Source
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Community-driven.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="bg-surface border border-border-subtle rounded-lg p-6 md:p-8 max-w-[800px]">
              <div className="space-y-4 text-sm text-text-secondary leading-relaxed">
                <p>
                  Kisuke is MIT licensed. Free to use, modify, and distribute.
                  No restrictions. No vendor lock-in.
                </p>
                <p>
                  Found a bug?{" "}
                  <a
                    href="https://github.com/kisuke/kisuke/issues"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-accent hover:text-accent-hover transition-colors duration-100"
                  >
                    Open an issue
                  </a>
                  . Have an idea?{" "}
                  <a
                    href="https://github.com/kisuke/kisuke/discussions"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-accent hover:text-accent-hover transition-colors duration-100"
                  >
                    Start a discussion
                  </a>
                  . Want to contribute?{" "}
                  <a
                    href="https://github.com/kisuke/kisuke/pulls"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-accent hover:text-accent-hover transition-colors duration-100"
                  >
                    Open a pull request
                  </a>
                  .
                </p>
                <p>
                  Every decision is documented. Every change is reviewed.
                  Architecture changes require RFC before PR. The{" "}
                  <Link
                    href="/architecture"
                    className="text-accent hover:text-accent-hover transition-colors duration-100"
                  >
                    Constitution
                  </Link>{" "}
                  governs all.
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
