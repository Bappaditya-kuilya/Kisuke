import { Navigation } from "@/components/navigation";
import { Hero } from "@/components/sections/hero";
import { Features } from "@/components/sections/features";
import { Architecture } from "@/components/sections/architecture";
import { CliDemo } from "@/components/sections/cli-demo";
import { GithubCta } from "@/components/sections/github-cta";
import { Footer } from "@/components/footer";
import { JsonLd } from "@/components/ui/json-ld";

export default function Home() {
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "SoftwareApplication",
          name: "Kisuke",
          applicationCategory: "DeveloperApplication",
          operatingSystem: "Linux, macOS, Windows",
          description:
            "Local-first context reconstruction engine. Reconstruct context from your code, commits, documents, and conversations.",
          url: "https://kisuke.vercel.app",
          softwareVersion: "0.1.0",
          license: "https://opensource.org/licenses/MIT",
          offers: {
            "@type": "Offer",
            price: "0",
            priceCurrency: "USD",
          },
        }}
      />
      <Navigation />
      <main>
        <Hero />
        <Features />
        <Architecture />
        <CliDemo />
        <GithubCta />
      </main>
      <Footer />
    </>
  );
}
