import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Reveal } from "@/components/ui/reveal";
import { ArrowRight, Star } from "lucide-react";

function Hero() {
  return (
    <section className="relative pt-32 pb-20 px-6 md:px-8 lg:px-0">
      <div className="mx-auto max-w-[1200px] text-center">
        <Reveal>
          <Badge>Local-first context reconstruction</Badge>
        </Reveal>

        <Reveal delay={100}>
          <h1 className="mt-6 text-4xl sm:text-5xl md:text-6xl font-medium tracking-tight text-text-primary leading-[1.1]">
            Your second brain,
            <br />
            on your machine.
          </h1>
        </Reveal>

        <Reveal delay={200}>
          <p className="mt-6 text-lg text-text-secondary max-w-[600px] mx-auto leading-relaxed">
            Kisuke reconstructs context from your code, commits, documents, and
            conversations. Everything stays local. AI is optional.
          </p>
        </Reveal>

        <Reveal delay={300}>
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Button size="lg">
              <a
                href="https://github.com/kisuke/kisuke"
                target="_blank"
                rel="noopener noreferrer"
              >
                Get Started
              </a>
              <ArrowRight className="w-4 h-4 ml-0.5" />
            </Button>
            <Button variant="secondary" size="lg">
              <a
                href="https://github.com/kisuke/kisuke"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Star className="w-4 h-4 mr-1" />
                Star on GitHub
              </a>
            </Button>
          </div>
        </Reveal>

        <Reveal delay={400}>
          <div className="mt-16 mx-auto max-w-[720px]">
            <div className="relative rounded-lg border border-border-subtle bg-surface-inset p-1 shadow-lg">
              <div className="absolute inset-0 bg-gradient-to-b from-accent/5 to-transparent rounded-lg" />
              <pre className="relative font-mono text-sm text-text-secondary overflow-x-auto p-4 leading-relaxed">
                <code>
                  <span className="text-text-tertiary">$</span>{" "}
                  <span className="text-text-primary">kisuke resume</span>{" "}
                  <span className="text-text-tertiary">--focus</span>{" "}
                  <span className="text-text-tertiary">
                    feat/search-api
                  </span>{"\n"}
                  <span className="text-text-tertiary">&gt;</span>{" "}
                  <span className="text-code-comment">
                    Reconstructing context...
                  </span>{"\n"}
                  <span className="text-text-tertiary">&gt;</span>{" "}
                  <span className="text-code-keyword">Found</span>{" "}
                  <span className="text-text-primary">14 files</span>{" "}
                  <span className="text-code-comment">changed</span>{"\n"}
                  <span className="text-text-tertiary">&gt;</span>{" "}
                  <span className="text-code-keyword">Indexed</span>{" "}
                  <span className="text-text-primary">3 commits</span>{"\n"}
                  <span className="text-text-tertiary">&gt;</span>{" "}
                  <span className="text-code-string">Context ready</span>
                </code>
              </pre>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

export { Hero };
