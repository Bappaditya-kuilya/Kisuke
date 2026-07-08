import { Section } from "@/components/ui/section";
import { Button } from "@/components/ui/button";
import { Reveal } from "@/components/ui/reveal";
import { ArrowRight, Star } from "lucide-react";

function GithubCta() {
  return (
    <Section>
      <Reveal>
        <div className="relative rounded-lg border border-border-subtle bg-surface p-8 md:p-12 text-center overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-accent/5 to-transparent" />
          <div className="relative">
            <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-text-primary mb-4">
              Open source.
              <br />
              Local first.
            </h2>
            <p className="text-lg text-text-secondary max-w-[500px] mx-auto mb-8">
              Kisuke is MIT licensed. Your data stays on your machine. AI is
              optional. You own everything.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Button size="lg">
                <a
                  href="https://github.com/kisuke/kisuke"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Star on GitHub
                </a>
                <Star className="w-4 h-4 ml-0.5" />
              </Button>
              <Button variant="secondary" size="lg">
                <a href="/docs">Read the Docs</a>
                <ArrowRight className="w-4 h-4 ml-0.5" />
              </Button>
            </div>
          </div>
        </div>
      </Reveal>
    </Section>
  );
}

export { GithubCta };
