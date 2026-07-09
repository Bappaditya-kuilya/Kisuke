import type { Metadata } from "next";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Section } from "@/components/ui/section";
import { Badge } from "@/components/ui/badge";
import { Terminal } from "@/components/ui/terminal";
import { Reveal } from "@/components/ui/reveal";
import { Breadcrumbs } from "@/components/docs/breadcrumbs";
import { InstallCard } from "@/components/download/install-card";
import { RequirementCard } from "@/components/download/requirement-card";
import { FeatureCheck } from "@/components/download/feature-check";
import { FaqItem } from "@/components/download/faq-item";
import { VerificationStat } from "@/components/download/verification-stat";
import { GithubIcon } from "@/components/ui/github-icon";
import { JsonLd } from "@/components/ui/json-ld";

export const metadata: Metadata = {
  title: "Download",
  description:
    "Install Kisuke — local-first context reconstruction engine. Zero runtime dependencies. MIT licensed.",
  openGraph: {
    title: "Download — Kisuke",
    description:
      "Install Kisuke — local-first context reconstruction engine. Zero runtime dependencies. MIT licensed.",
    url: "https://kisuke.vercel.app/download",
    siteName: "Kisuke",
    type: "website",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "Download — Kisuke",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Download — Kisuke",
    description:
      "Install Kisuke — local-first context reconstruction engine. Zero runtime dependencies. MIT licensed.",
    images: ["/og.svg"],
  },
  alternates: {
    canonical: "https://kisuke.vercel.app/download",
  },
};

const installMethods = [
  {
    method: "uv",
    command: "uv tool install kisuke",
    description:
      "Fastest. uv is the modern Python package manager. Installs in isolation.",
    recommended: true,
  },
  {
    method: "pip",
    command: "pip install kisuke",
    description:
      "Standard Python installer. Requires pip and Python 3.12+.",
  },
  {
    method: "pipx",
    command: "pipx install kisuke",
    description:
      "Isolated install for CLI tools. Similar to uv but uses pip under the hood.",
  },
  {
    method: "From source",
    command: "git clone https://github.com/kisuke/kisuke && cd kisuke && pip install -e .",
    description:
      "Clone the repo and install in editable mode. Good for contributors.",
  },
];

const requirementCards = [
  { label: "Python", value: "3.12+", icon: "\u{1F40D}" },
  { label: "OS", value: "macOS, Linux, Windows", icon: "\u{1F5A5}\uFE0F" },
  { label: "RAM", value: "50 MB minimum", icon: "\uD83D\uDCCA" },
  {
    label: "Disk",
    value: "< 10 MB installed",
    icon: "\uD83D\uDCBE",
  },
  {
    label: "Terminal",
    value: "Any (bash, zsh, fish, powershell)",
    icon: "\u2328\uFE0F",
  },
];

const features = [
  "Markdown-native",
  "Full-text Search",
  "Resume Engine",
  "CLI",
  "AI Optional",
  "Offline First",
  "Zero Runtime Dependencies",
  "MIT Licensed",
];

const verificationStats = [
  { label: "Tests passing", value: "309", icon: "\u2705" },
  { label: "Coverage", value: "95%+", icon: "\uD83D\uDCCA" },
  { label: "Ruff", value: "Clean", icon: "\u2713" },
  { label: "MyPy", value: "Strict", icon: "\u2713" },
  { label: "Type Safe", value: "Yes", icon: "\u2713" },
];

const faqItems = [
  {
    question: "What Python version do I need?",
    answer:
      "Kisuke requires Python 3.12 or later. We recommend using the latest stable release (3.13+) for best performance.",
  },
  {
    question: "Does Kisuke work offline?",
    answer:
      "Yes. Kisuke is fully offline. All data stays on your machine. No cloud, no API calls, no telemetry.",
  },
  {
    question: "Does Kisuke have any runtime dependencies?",
    answer:
      "No. Kisuke has zero runtime dependencies. The only dependencies are the Python standard library. Dev dependencies (pytest, ruff, mypy) are optional and not required to run.",
  },
  {
    question: "Can I use Kisuke with AI?",
    answer:
      "Yes, but AI is optional. Kisuke includes a provider-independent AI abstraction layer supporting OpenAI, Anthropic, Gemini, Ollama, and OpenAI-compatible providers. Core functionality works without AI.",
  },
  {
    question: "How do I upgrade Kisuke?",
    answer:
      "Run the same install command with the upgrade flag: uv tool upgrade kisuke, pip install --upgrade kisuke, or pipx upgrade kisuke.",
  },
  {
    question: "Is Kisuke production-ready?",
    answer:
      "Kisuke is in Beta (v0.1.0). The architecture is frozen, 309 tests pass, and performance targets are met. It is suitable for individual use. Team collaboration is planned for a future release.",
  },
];

export default function DownloadPage() {
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
              name: "Download",
              item: "https://kisuke.vercel.app/download",
            },
          ],
        }}
      />
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          name: "Download — Kisuke",
          description:
            "Install Kisuke — local-first context reconstruction engine. Zero runtime dependencies. MIT licensed.",
          url: "https://kisuke.vercel.app/download",
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
          <Breadcrumbs items={[{ label: "Download" }]} />

          <Reveal>
            <Badge>Download</Badge>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 text-3xl sm:text-4xl md:text-5xl font-medium tracking-tight text-text-primary leading-[1.1]">
              Download Kisuke.
            </h1>
          </Reveal>

          <Reveal delay={200}>
            <p className="mt-4 text-lg text-text-secondary max-w-[600px] leading-relaxed">
              Local-first context reconstruction. Zero runtime dependencies. MIT
              licensed.
            </p>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-6 flex flex-wrap items-center gap-3 text-sm">
              <span className="font-mono text-text-tertiary">v0.1.0</span>
              <span className="px-2 py-0.5 text-xs font-medium bg-accent/10 text-accent rounded-full">
                MIT License
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
              <span className="text-text-disabled">|</span>
              <span className="text-text-tertiary">Released Dec 2025</span>
            </div>
          </Reveal>
        </Section>

        {/* Install Methods */}
        <Section id="install" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Install Methods
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              One command.
            </h2>
          </Reveal>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {installMethods.map((method, i) => (
              <Reveal key={method.method} delay={i * 60}>
                <InstallCard
                  method={method.method}
                  command={method.command}
                  description={method.description}
                  recommended={method.recommended}
                />
              </Reveal>
            ))}
          </div>
        </Section>

        {/* Requirements */}
        <Section id="requirements" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Requirements
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Minimal footprint.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              {requirementCards.map((req) => (
                <RequirementCard
                  key={req.label}
                  label={req.label}
                  value={req.value}
                  icon={req.icon}
                />
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Quick Start */}
        <Section id="quick-start" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Quick Start
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Up and running in 30 seconds.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <Terminal title="terminal">
              <span className="text-text-tertiary">$</span>{" "}
              <span className="text-text-primary">uv tool install kisuke</span>
              {"\n"}
              <span className="text-code-comment">
                Resolved 0 packages in 12ms
              </span>
              {"\n"}
              <span className="text-code-string">
                Installed 1 package in 45ms
              </span>
              {"\n"}
              <span className="text-code-string">
                {" "}
                + kisuke
              </span>
              {"\n\n"}
              <span className="text-text-tertiary">$</span>{" "}
              <span className="text-text-primary">kisuke init</span>
              {"\n"}
              <span className="text-code-comment">
                Initialized Kisuke repository at ./kisuke-data
              </span>
              {"\n\n"}
              <span className="text-text-tertiary">$</span>{" "}
              <span className="text-text-primary">
                kisuke mission create &quot;My Project&quot;
              </span>
              {"\n"}
              <span className="text-code-string">
                Created mission: 3f8a2c1d-...
              </span>
              {"\n\n"}
              <span className="text-text-tertiary">$</span>{" "}
              <span className="text-text-primary">kisuke resume</span>
              {"\n"}
              <span className="text-code-comment">
                Reconstructing context...
              </span>
              {"\n"}
              <span className="text-code-keyword">Mission:</span>{" "}
              <span className="text-text-primary">My Project</span>
              {"\n"}
              <span className="text-code-keyword">Status:</span>{" "}
              <span className="text-text-primary">No active projects</span>
              {"\n"}
              <span className="text-code-keyword">Next Action:</span>{" "}
              <span className="text-text-primary">
                Create a project with kisuke project create
              </span>
            </Terminal>
          </Reveal>
        </Section>

        {/* Feature Checklist */}
        <Section id="features" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              What&apos;s Included
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Everything you need.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {features.map((feature) => (
                <FeatureCheck key={feature} label={feature} />
              ))}
            </div>
          </Reveal>
        </Section>

        {/* Release Notes */}
        <Section id="releases" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Release Notes
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Latest release.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="bg-surface border border-border-subtle rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <h3 className="text-lg font-medium text-text-primary">
                  v0.1.0
                </h3>
                <span className="px-2 py-0.5 text-xs font-medium bg-success/10 text-success rounded-full">
                  Latest
                </span>
                <span className="text-sm text-text-tertiary">Dec 2025</span>
              </div>
              <div className="space-y-3 text-sm text-text-secondary">
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">Domain Core</strong>{" "}
                    — 11 entity types with ownership, lifecycle, and relationship
                    management
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">
                      Markdown Storage
                    </strong>{" "}
                    — One entity = one file. Relationships by ID. Derived index
                    rebuildable.
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">Search Engine</strong>{" "}
                    — Tantivy-powered full-text search with filters and ranking
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">Resume Engine</strong>{" "}
                    — Deterministic context reconstruction in under 30ms
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">CLI</strong> — 20+
                    commands with JSON output, shell completion, and health
                    checks
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">Review System</strong>{" "}
                    — Morning, weekly, monthly, and quarterly reviews
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">AI Abstraction</strong>{" "}
                    — Provider-independent interface (OpenAI, Anthropic, Gemini,
                    Ollama)
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-code-string mt-0.5">+</span>
                  <span>
                    <strong className="text-text-primary">Integrations</strong>{" "}
                    — Git, GitHub, Obsidian, VS Code adapters
                  </span>
                </div>
              </div>
            </div>
          </Reveal>
        </Section>

        {/* Verification */}
        <Section id="verification" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              Verification
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Production quality.
            </h2>
          </Reveal>

          <Reveal delay={200}>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              {verificationStats.map((stat) => (
                <VerificationStat
                  key={stat.label}
                  label={stat.label}
                  value={stat.value}
                  icon={stat.icon}
                />
              ))}
            </div>
          </Reveal>
        </Section>

        {/* FAQ */}
        <Section id="faq" className="pt-0 pb-16">
          <Reveal>
            <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
              FAQ
            </p>
          </Reveal>
          <Reveal delay={100}>
            <h2 className="text-2xl sm:text-3xl font-medium tracking-tight text-text-primary mb-8">
              Common questions.
            </h2>
          </Reveal>

          <div className="space-y-3">
            {faqItems.map((item, i) => (
              <Reveal key={item.question} delay={i * 50}>
                <FaqItem
                  question={item.question}
                  answer={item.answer}
                />
              </Reveal>
            ))}
          </div>
        </Section>
      </main>
      <Footer />
    </>
  );
}
