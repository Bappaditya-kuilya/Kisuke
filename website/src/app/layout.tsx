import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { JsonLd } from "@/components/ui/json-ld";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Kisuke — Local-First Context Reconstruction",
    template: "%s — Kisuke",
  },
  description:
    "Reconstruct context from your code, commits, documents, and conversations. Everything stays local. AI is optional.",
  keywords: [
    "context reconstruction",
    "local-first",
    "code context",
    "developer tools",
    "resume engine",
    "knowledge graph",
  ],
  authors: [{ name: "Kisuke" }],
  openGraph: {
    title: "Kisuke — Local-First Context Reconstruction",
    description:
      "Reconstruct context from your code, commits, documents, and conversations. Everything stays local. AI is optional.",
    url: "https://kisuke.vercel.app",
    siteName: "Kisuke",
    type: "website",
    locale: "en_US",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "Kisuke — Local-First Context Reconstruction",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Kisuke — Local-First Context Reconstruction",
    description:
      "Reconstruct context from your code, commits, documents, and conversations. Everything stays local. AI is optional.",
    images: ["/og.svg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: "https://kisuke.vercel.app",
  },
  metadataBase: new URL("https://kisuke.vercel.app"),
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#0a0a0b",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-canvas text-text-primary">
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "Organization",
            name: "Kisuke",
            url: "https://kisuke.vercel.app",
            logo: "https://kisuke.vercel.app/og.svg",
            sameAs: ["https://github.com/kisuke/kisuke"],
          }}
        />
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "Kisuke",
            url: "https://kisuke.vercel.app",
            description:
              "Local-first context reconstruction. Reconstruct context from your code, commits, documents, and conversations.",
            potentialAction: {
              "@type": "SearchAction",
              target: "https://kisuke.vercel.app/docs?q={search_term_string}",
              "query-input": "required name=search_term_string",
            },
          }}
        />
        {children}
      </body>
    </html>
  );
}
