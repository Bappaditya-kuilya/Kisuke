import { Navigation } from "@/components/navigation";
import { Hero } from "@/components/sections/hero";
import { Features } from "@/components/sections/features";
import { Architecture } from "@/components/sections/architecture";
import { CliDemo } from "@/components/sections/cli-demo";
import { GithubCta } from "@/components/sections/github-cta";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <>
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
