import { Section } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Reveal } from "@/components/ui/reveal";
import {
  GitBranch,
  Search,
  FileText,
  Bot,
  Shield,
  Layers,
} from "lucide-react";

const features = [
  {
    icon: GitBranch,
    title: "Domain-Driven Design",
    description:
      "Entities, value objects, and aggregates model your workflow. Every object has one owner. Relationships never imply ownership.",
  },
  {
    icon: Search,
    title: "Local Search Engine",
    description:
      "Full-text search, filters, and ranking over your entire graph. No cloud. No API calls. Results in under 500ms.",
  },
  {
    icon: FileText,
    title: "Resume Engine",
    description:
      "Reconstruct context from commits, files, and conversations. Focus on a branch, feature, or time window.",
  },
  {
    icon: Bot,
    title: "AI Abstraction Layer",
    description:
      "Optional. Provider-independent. Summarize, explain, classify, and search with any backend. AI owns nothing.",
  },
  {
    icon: Shield,
    title: "Production Ready",
    description:
      "Typed errors, graceful degradation, health checks, metrics. 309 tests. Lighthouse 95+. Zero runtime crashes.",
  },
  {
    icon: Layers,
    title: "Plugin Architecture",
    description:
      "Adapters for GitHub, Obsidian, VS Code. Plugins can read, create derived artifacts, and request changes. Core stays clean.",
  },
];

function Features() {
  return (
    <Section id="features">
      <Reveal>
        <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
          What Kisuke does
        </p>
      </Reveal>
      <Reveal delay={100}>
        <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-text-primary mb-12">
          Everything you need,
          <br />
          nothing you don&apos;t.
        </h2>
      </Reveal>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((feature, i) => (
          <Reveal key={feature.title} delay={i * 80}>
            <Card hover className="h-full">
              <feature.icon className="w-5 h-5 text-accent mb-4" />
              <h3 className="text-base font-medium text-text-primary mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-text-secondary leading-relaxed">
                {feature.description}
              </p>
            </Card>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}

export { Features };
