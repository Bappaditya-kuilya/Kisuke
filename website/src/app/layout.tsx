import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "context-mcp — Minimal MCP Server for Personal Context",
  description: "Minimal MCP server that connects your notes, profile, and tools to any AI assistant. No vendor lock-in. Works with opencode, Claude Code, Codex.",
  keywords: ["MCP", "context", "notes", "developer tools", "AI assistant", "personal knowledge"],
  authors: [{ name: "context-mcp" }],
  creator: "context-mcp",
  publisher: "context-mcp",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://context-mcp.vercel.app",
    title: "context-mcp — Minimal MCP Server for Personal Context",
    description: "Minimal MCP server that connects your notes, profile, and tools to any AI assistant.",
    siteName: "context-mcp",
    images: [
      {
        url: "/og.svg",
        width: 1200,
        height: 630,
        alt: "context-mcp — Minimal MCP Server for Personal Context",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "context-mcp — Minimal MCP Server for Personal Context",
    description: "Minimal MCP server that connects your notes, profile, and tools to any AI assistant.",
    images: ["/og.svg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}>
      <head>
        <link rel="icon" href="/favicon.ico" sizes="256x256" type="image/x-icon" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className="min-h-full flex flex-col bg-canvas text-text-primary">{children}</body>
    </html>
  );
}