import Link from "next/link";

const footerLinks = {
  Product: [
    { label: "Features", href: "#features" },
    { label: "Architecture", href: "#architecture" },
    { label: "CLI", href: "#cli" },
    { label: "Changelog", href: "/changelog" },
  ],
  Docs: [
    { label: "Getting Started", href: "/docs/getting-started" },
    { label: "Domain Model", href: "/docs/domain-model" },
    { label: "Resume Engine", href: "/docs/resume" },
    { label: "Search", href: "/docs/search" },
    { label: "Integrations", href: "/docs/integrations" },
    { label: "AI", href: "/docs/ai" },
  ],
  Community: [
    {
      label: "GitHub",
      href: "https://github.com/kisuke/kisuke",
      external: true,
    },
    { label: "Contributing", href: "/CONTRIBUTING" },
    { label: "Code of Conduct", href: "/CODE_OF_CONDUCT" },
  ],
  Legal: [
    { label: "License (MIT)", href: "/LICENSE" },
    { label: "Security", href: "/security" },
  ],
};

function Footer() {
  return (
    <footer className="border-t border-border-subtle">
      <div className="mx-auto max-w-[1200px] py-16 px-6 md:px-8">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          <div className="col-span-2 md:col-span-1">
            <Link
              href="/"
              className="text-text-primary font-medium text-base tracking-tight"
            >
              Kisuke
            </Link>
            <p className="mt-3 text-sm text-text-tertiary leading-relaxed max-w-[200px]">
              Local-first context reconstruction.
            </p>
          </div>

          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h3 className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-3">
                {category}
              </h3>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    {link.href.startsWith("http") ? (
                      <a
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-text-secondary hover:text-text-primary transition-colors duration-100"
                      >
                        {link.label}
                      </a>
                    ) : (
                      <Link
                        href={link.href}
                        className="text-sm text-text-secondary hover:text-text-primary transition-colors duration-100"
                      >
                        {link.label}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="pt-8 border-t border-border-subtle flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-xs text-text-tertiary">
            MIT License. Built with care.
          </p>
          <p className="text-xs text-text-tertiary">
            &copy; {new Date().getFullYear()} Kisuke
          </p>
        </div>
      </div>
    </footer>
  );
}

export { Footer };
