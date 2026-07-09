"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GithubIcon } from "@/components/ui/github-icon";

const navLinks = [
  { label: "Features", href: "#features" },
  { label: "Architecture", href: "#architecture" },
  { label: "CLI", href: "#cli" },
];

function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 0);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-200 ${
        isScrolled
          ? "bg-canvas/80 backdrop-blur-md border-b border-border-subtle"
          : "bg-transparent"
      }`}
    >
    <nav aria-label="Main navigation">
      <div className="mx-auto max-w-[1200px] flex items-center justify-between h-14 px-6 md:px-8">
        <Link
          href="/"
          className="text-text-primary font-medium text-base tracking-tight"
        >
          Kisuke
        </Link>

        <div className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="px-3 py-1.5 text-sm text-text-secondary hover:text-text-primary transition-colors duration-100 rounded-md hover:bg-surface-raised"
            >
              {link.label}
            </a>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-3">
          <a
            href="https://github.com/kisuke/kisuke"
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-secondary hover:text-text-primary transition-colors duration-100"
            aria-label="GitHub"
          >
            <GithubIcon className="w-5 h-5" />
          </a>
          <Button variant="primary" size="sm">
            <a
              href="https://github.com/kisuke/kisuke"
              target="_blank"
              rel="noopener noreferrer"
            >
              Star on GitHub
            </a>
          </Button>
        </div>

        <button
          className="md:hidden text-text-secondary hover:text-text-primary p-1"
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Close menu" : "Open menu"}
        >
          {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {isOpen && (
        <div className="md:hidden bg-canvas border-b border-border-subtle">
          <div className="px-6 py-4 flex flex-col gap-2">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="py-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </a>
            ))}
            <div className="pt-2 border-t border-border-subtle flex flex-col gap-2">
              <a
                href="https://github.com/kisuke/kisuke"
                target="_blank"
                rel="noopener noreferrer"
                className="py-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
              >
                GitHub
              </a>
              <Button variant="primary" size="sm">
                <a
                  href="https://github.com/kisuke/kisuke"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Star on GitHub
                </a>
              </Button>
            </div>
          </div>
        </div>
      )}
    </nav>
    </header>
  );
}

export { Navigation };
