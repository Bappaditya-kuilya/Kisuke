function ArchitectureDiagram() {
  return (
    <svg
      viewBox="0 0 800 520"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-auto"
      role="img"
      aria-label="Kisuke architecture diagram showing layered dependencies"
    >
      {/* Background */}
      <rect width="800" height="520" fill="#08080a" rx="8" />

      {/* Title */}
      <text x="400" y="32" textAnchor="middle" fill="#a0a0a8" fontSize="12" fontFamily="system-ui">
        Layered Architecture — Dependencies point inward
      </text>

      {/* User */}
      <rect x="355" y="52" width="90" height="36" rx="6" fill="#18181b" stroke="#1f1f23" strokeWidth="1" />
      <text x="400" y="74" textAnchor="middle" fill="#ececef" fontSize="13" fontFamily="system-ui" fontWeight="500">
        User
      </text>

      {/* Arrow: User -> CLI */}
      <line x1="400" y1="88" x2="400" y2="108" stroke="#45454d" strokeWidth="1" />
      <polygon points="400,108 396,100 404,100" fill="#45454d" />

      {/* CLI / Presentation Layer */}
      <rect x="280" y="108" width="240" height="56" rx="8" fill="#111113" stroke="#6366f1" strokeWidth="1" strokeOpacity="0.3" />
      <text x="400" y="132" textAnchor="middle" fill="#6366f1" fontSize="10" fontFamily="monospace" fontWeight="500">
        PRESENTATION
      </text>
      <text x="400" y="150" textAnchor="middle" fill="#ececef" fontSize="13" fontFamily="system-ui" fontWeight="500">
        CLI
      </text>

      {/* Arrow: CLI -> Application */}
      <line x1="400" y1="164" x2="400" y2="184" stroke="#45454d" strokeWidth="1" />
      <polygon points="400,184 396,176 404,176" fill="#45454d" />

      {/* Application Layer */}
      <rect x="240" y="184" width="320" height="56" rx="8" fill="#111113" stroke="#86efac" strokeWidth="1" strokeOpacity="0.3" />
      <text x="400" y="208" textAnchor="middle" fill="#86efac" fontSize="10" fontFamily="monospace" fontWeight="500">
        APPLICATION
      </text>
      <text x="400" y="226" textAnchor="middle" fill="#ececef" fontSize="13" fontFamily="system-ui" fontWeight="500">
        Use Cases, Commands, Orchestration
      </text>

      {/* Arrow: Application -> Domain */}
      <line x1="400" y1="240" x2="400" y2="260" stroke="#45454d" strokeWidth="1" />
      <polygon points="400,260 396,252 404,252" fill="#45454d" />

      {/* Domain Layer */}
      <rect x="200" y="260" width="400" height="72" rx="8" fill="#111113" stroke="#c084fc" strokeWidth="1" strokeOpacity="0.3" />
      <text x="400" y="284" textAnchor="middle" fill="#c084fc" fontSize="10" fontFamily="monospace" fontWeight="500">
        DOMAIN (CORE)
      </text>
      <text x="400" y="304" textAnchor="middle" fill="#ececef" fontSize="13" fontFamily="system-ui" fontWeight="500">
        Entities, Business Rules, Ownership
      </text>
      <text x="400" y="322" textAnchor="middle" fill="#a0a0a8" fontSize="11" fontFamily="system-ui">
        No external dependencies
      </text>

      {/* Arrow: Domain -> Infrastructure (left) */}
      <line x1="320" y1="332" x2="200" y2="380" stroke="#45454d" strokeWidth="1" />
      <polygon points="200,380 208,372 210,380" fill="#45454d" />

      {/* Arrow: Domain -> Integrations (right) */}
      <line x1="480" y1="332" x2="600" y2="380" stroke="#45454d" strokeWidth="1" />
      <polygon points="600,380 592,372 590,380" fill="#45454d" />

      {/* Infrastructure Layer */}
      <rect x="60" y="380" width="280" height="80" rx="8" fill="#111113" stroke="#93c5fd" strokeWidth="1" strokeOpacity="0.3" />
      <text x="200" y="404" textAnchor="middle" fill="#93c5fd" fontSize="10" fontFamily="monospace" fontWeight="500">
        INFRASTRUCTURE
      </text>
      <text x="200" y="424" textAnchor="middle" fill="#ececef" fontSize="12" fontFamily="system-ui" fontWeight="500">
        Markdown, SQLite, Filesystem
      </text>
      <text x="200" y="442" textAnchor="middle" fill="#a0a0a8" fontSize="11" fontFamily="system-ui">
        Storage, Index, Cache
      </text>
      <text x="200" y="454" textAnchor="middle" fill="#6b6b73" fontSize="10" fontFamily="system-ui">
        Implements Domain interfaces
      </text>

      {/* Integrations Layer */}
      <rect x="460" y="380" width="280" height="80" rx="8" fill="#111113" stroke="#fbbf24" strokeWidth="1" strokeOpacity="0.3" />
      <text x="600" y="404" textAnchor="middle" fill="#fbbf24" fontSize="10" fontFamily="monospace" fontWeight="500">
        INTEGRATIONS
      </text>
      <text x="600" y="424" textAnchor="middle" fill="#ececef" fontSize="12" fontFamily="system-ui" fontWeight="500">
        Git, GitHub, Obsidian, VS Code
      </text>
      <text x="600" y="442" textAnchor="middle" fill="#a0a0a8" fontSize="11" fontFamily="system-ui">
        Calendar, AI Providers
      </text>
      <text x="600" y="454" textAnchor="middle" fill="#6b6b73" fontSize="10" fontFamily="system-ui">
        Optional. Never accessed by Domain.
      </text>

      {/* Plugins box */}
      <rect x="620" y="260" width="140" height="56" rx="8" fill="#111113" stroke="#f9a8d4" strokeWidth="1" strokeOpacity="0.3" />
      <text x="690" y="284" textAnchor="middle" fill="#f9a8d4" fontSize="10" fontFamily="monospace" fontWeight="500">
        PLUGINS
      </text>
      <text x="690" y="302" textAnchor="middle" fill="#ececef" fontSize="11" fontFamily="system-ui">
        Read, Derive, Request
      </text>

      {/* Dashed line from Plugins to Domain */}
      <line x1="620" y1="288" x2="600" y2="288" stroke="#45454d" strokeWidth="1" strokeDasharray="4 4" />

      {/* Legend */}
      <rect x="60" y="480" width="680" height="28" rx="4" fill="#111113" />
      <circle cx="80" cy="494" r="4" fill="#6366f1" />
      <text x="90" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Presentation</text>
      <circle cx="170" cy="494" r="4" fill="#86efac" />
      <text x="180" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Application</text>
      <circle cx="270" cy="494" r="4" fill="#c084fc" />
      <text x="280" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Domain</text>
      <circle cx="350" cy="494" r="4" fill="#93c5fd" />
      <text x="360" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Infrastructure</text>
      <circle cx="460" cy="494" r="4" fill="#fbbf24" />
      <text x="470" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Integrations</text>
      <circle cx="560" cy="494" r="4" fill="#f9a8d4" />
      <text x="570" y="498" fill="#a0a0a8" fontSize="10" fontFamily="system-ui">Plugins</text>
    </svg>
  );
}

export { ArchitectureDiagram };
