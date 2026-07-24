export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-800">
        <nav className="mx-auto max-w-7xl flex items-center justify-between h-16 px-6 md:px-8">
          <a href="/" className="text-gray-900 dark:text-gray-100 font-semibold text-lg tracking-tight">
            context-mcp
          </a>
          <div className="hidden md:flex items-center gap-1">
            <a href="#features" className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-100 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              Features
            </a>
            <a href="#architecture" className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-100 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              Architecture
            </a>
            <a href="#cli" className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-100 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
              CLI
            </a>
          </div>
          <div className="hidden md:flex items-center gap-3">
            <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors duration-100" aria-label="GitHub">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-git-branch w-5 h-5" aria-hidden="true"><path d="M15 6a9 9 0 0 0-9 9V3"></path><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle></svg>
            </a>
            <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center font-medium transition-all duration-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:pointer-events-none disabled:opacity-40 bg-gray-900 dark:bg-white text-white dark:text-gray-950 hover:bg-gray-700 dark:hover:bg-gray-300 shadow-glow hover:shadow-lg rounded-full h-9 px-4 text-sm gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-star w-4 h-4 mr-1" aria-hidden="true"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
              Star on GitHub
            </a>
          </div>
        </nav>
      </header>

      <main>
        <section className="relative pt-32 pb-20 px-6 md:px-8 lg:px-0">
          <div className="mx-auto max-w-7xl text-center">
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 0ms, transform 300ms ease-out 0ms'}} className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium uppercase tracking-widest text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30 rounded-full">
              Minimal MCP context server
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 100ms, transform 300ms ease-out 100ms'}} className="mt-6">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-medium tracking-tight text-gray-900 dark:text-gray-50 leading-[1.1]">
                Minimal MCP server<br/>
                for personal context.
              </h1>
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 200ms, transform 300ms ease-out 200ms'}} className="mt-6 text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
              Connect your notes, profile, and tools to any AI assistant via MCP. No vendor lock-in. Works with opencode, Claude Code, Codex.
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 300ms, transform 300ms ease-out 300ms'}} className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
              <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center font-medium transition-all duration-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:pointer-events-none disabled:opacity-40 bg-gray-900 dark:bg-white text-white dark:text-gray-950 hover:bg-gray-700 dark:hover:bg-gray-300 shadow-glow hover:shadow-lg rounded-full h-12 px-7 text-base gap-2.5">
                Get Started
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-4 h-4 ml-0.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
              </a>
              <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center font-medium transition-all duration-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:pointer-events-none disabled:opacity-40 bg-transparent text-gray-900 dark:text-gray-50 border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full h-12 px-7 text-base gap-2.5">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-star w-4 h-4 mr-1" aria-hidden="true"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
                Star on GitHub
              </a>
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 400ms, transform 300ms ease-out 400ms'}} className="mt-16 mx-auto max-w-[720px]">
              <div className="relative rounded-lg border border-gray-200 dark:border-gray-800 bg-gray-100 dark:bg-gray-900 p-1 shadow-lg">
                <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/5 to-transparent rounded-lg"></div>
                <pre className="relative font-mono text-sm text-gray-600 dark:text-gray-400 overflow-x-auto p-4 leading-relaxed">
                  <code>{`$ context-mcp init --vault /path/to/notes
$ context-mcp
# Or HTTP for other clients
$ context-mcp -http :8080`}</code>
                </pre>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="py-24 px-6 md:px-8 lg:px-0">
          <div className="mx-auto max-w-7xl">
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 0ms, transform 300ms ease-out 0ms'}} className="text-center mb-12">
              <p className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3">What context-mcp does</p>
              <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-gray-900 dark:text-gray-50 mb-12">Everything you need,<br/>nothing you don&apos;t.</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-git-branch w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="M15 6a9 9 0 0 0-9 9V3"></path><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle></svg>
                  ),
                  title: "Search Your Notes",
                  desc: "FTS5 full-text search over your markdown vault. No cloud. No API calls. Results in under 500ms."
                },
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-search w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
                  ),
                  title: "Link Notes to Projects",
                  desc: "Create bidirectional links between notes and projects. Confidence scoring helps you trust the connection."
                },
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-file-text w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg>
                  ),
                  title: "Session Context Injection",
                  desc: "Auto-injects project focus, relevant notes, profile, and skill progress into every AI session."
                },
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-bot w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="M12 8V4H8"></path><rect width="16" height="12" x="4" y="8" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path></svg>
                  ),
                  title: "MCP Host Registry",
                  desc: "Register any MCP server once. Call through context-mcp from any session seamlessly."
                },
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-shield w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>
                  ),
                  title: "Production Ready",
                  desc: "Typed errors, graceful degradation, health checks. ~10MB binary, ~30MB RAM baseline."
                },
                {
                  icon: (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-layers w-5 h-5 text-emerald-600 dark:text-emerald-400 mb-4" aria-hidden="true"><path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"></path><path d="M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12"></path><path d="M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17"></path></svg>
                  ),
                  title: "Skill Progress Tracking",
                  desc: "Built-in streak counting, level progression, and learning goals. Integrated into morning brief."
                }
              ].map((feature, i) => (
                <div key={feature.title} style={{opacity:0,transform:'translateY(8px)',transition:`opacity 300ms ease-out ${80*i}ms, transform 300ms ease-out ${80*i}ms`}} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6 transition-all duration-100 hover:bg-gray-50 dark:hover:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-700 hover:shadow-sm h-full">
                  {feature.icon}
                  <h3 className="text-base font-medium text-gray-900 dark:text-gray-100 mb-2">{feature.title}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="architecture" className="py-24 px-6 md:px-8 lg:px-0">
          <div className="mx-auto max-w-7xl">
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 0ms, transform 300ms ease-out 0ms'}} className="text-center mb-12">
              <p className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3">How it&apos;s built</p>
              <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-gray-900 dark:text-gray-50">Eight layers.<br/>Zero coupling.</h2>
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 200ms, transform 300ms ease-out 200ms'}} className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6 md:p-8 bg-gray-50 dark:bg-gray-950 border-gray-200 dark:border-gray-800 p-6 md:p-8">
              <div className="space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">CLI Layer</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">Typer</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Command interface, argument parsing, output formatting</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Adapters</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">Plugins</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">GitHub, Obsidian, VS Code, MCP — provider-specific implementations</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">AI Abstraction</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">Optional</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Summarize, explain, classify, search — provider-independent</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Search</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">FTS5</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Full-text indexing, filters, grouping, ranking via SQLite</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Resume Engine</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">Pure Go</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Context reconstruction from git history, files, and metadata</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Graph</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">SQLite</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Ownership graph, dependency tracking, relationship analysis</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2 border-b border-gray-200 dark:border-gray-800 last:border-b-0">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Metadata Store</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">SQLite</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Lightweight storage, entity tracking, relationship mapping</span>
                </div>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 py-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-3 h-3 text-gray-400 hidden sm:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  <div className="flex items-center gap-3 min-w-[200px]">
                    <span className="font-mono text-sm font-medium text-gray-900 dark:text-gray-100">Domain Model</span>
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono w-20">Pure Go</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Entities, value objects, aggregates — the source of truth</span>
                </div>
              </div>
              <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-800">
                <p className="text-xs text-gray-500 dark:text-gray-400">Core is provider-independent. AI is optional. Plugins read, create derived artifacts, and request changes. They never mutate core directly.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="cli" className="py-24 px-6 md:px-8 lg:px-0">
          <div className="mx-auto max-w-7xl">
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 0ms, transform 300ms ease-out 0ms'}} className="text-center mb-12">
              <p className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3">CLI experience</p>
              <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-gray-900 dark:text-gray-50 mb-12">Fast. Focused. Familiar.</h2>
            </div>
            <div style={{opacity:0,transform:'translateY(8px)',transition:'opacity 300ms ease-out 200ms, transform 300ms ease-out 200ms'}} className="bg-gray-950 dark:bg-gray-950 rounded-lg overflow-hidden border border-gray-800">
              <div className="flex items-center gap-2 px-4 h-8 border-b border-gray-800">
                <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-gray-600/40"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-gray-600/40"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-gray-600/40"></div>
                </div>
                <span className="text-xs text-gray-500 font-mono ml-2">context-mcp init</span>
              </div>
              <div className="p-4 overflow-x-auto">
                <pre className="font-mono text-sm text-gray-300 leading-relaxed"><code>{`$ context-mcp init
Obsidian vault path []: /home/user/notes
Google Calendar credentials JSON path (optional): 
Kisuke database path (optional): 

✓ Database initialized
✓ Schema created
✓ Default profile set

To run the server:
  context-mcp

Environment variables:
  VAULT_PATH=/home/user/notes
  GOOGLE_CREDENTIALS=
  KISUKE_DB=
  CONTEXT_MCP_DB=context-mcp.db`}</code></pre>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24 px-6 md:px-8 lg:px-0">
          <div className="mx-auto max-w-7xl text-center">
            <p className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-gray-400 mb-3">Open source. Local first.</p>
            <h2 className="text-3xl sm:text-4xl font-medium tracking-tight text-gray-900 dark:text-zinc-50 mb-6">MIT License. Your data stays on your machine. AI is optional. You own everything.</h2>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center font-medium transition-all duration-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:pointer-events-none disabled:opacity-40 bg-gray-900 dark:bg-white text-white dark:text-gray-950 hover:bg-gray-700 dark:hover:bg-zinc-300 shadow-glow hover:shadow-lg rounded-full h-12 px-7 text-base gap-2.5">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right w-4 h-4 ml-0.5" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                View on GitHub
              </a>
              <a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center font-medium transition-all duration-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:pointer-events-none disabled:opacity-40 bg-transparent text-gray-900 dark:text-zinc-50 border border-gray-300 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-full h-12 px-7 text-base gap-2.5">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-star w-4 h-4 mr-1" aria-hidden="true"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
                Star on GitHub
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-50 dark:bg-zinc-950 border-t border-gray-200 dark:border-zinc-800">
        <div className="mx-auto max-w-7xl px-6 md:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <a href="/" className="text-gray-900 dark:text-zinc-100 font-medium text-base tracking-tight">context-mcp</a>
              <p className="mt-4 text-sm text-gray-600 dark:text-zinc-400">Minimal MCP context server.</p>
            </div>
            <nav>
              <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-zinc-400 mb-3">Product</h4>
              <ul className="space-y-2">
                <li><a href="#features" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Features</a></li>
                <li><a href="#architecture" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Architecture</a></li>
                <li><a href="#cli" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">CLI</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/CHANGELOG.md" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Changelog</a></li>
              </ul>
            </nav>
            <nav>
              <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-zinc-400 mb-3">Docs</h4>
              <ul className="space-y-2">
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Getting Started</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/README.md#database-schema" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Database Schema</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/README.md#mcp-tools-exposed" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">MCP Tools</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/README.md#mcp-prompts" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">MCP Prompts</a></li>
              </ul>
            </nav>
            <nav>
              <h4 className="text-xs font-medium uppercase tracking-widest text-gray-500 dark:text-zinc-400 mb-3">Community</h4>
              <ul className="space-y-2">
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors flex items-center gap-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4" aria-hidden="true"><path d="M15 6a9 9 0 0 0-9 9V3"></path><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle></svg> GitHub</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Contributing</a></li>
                <li><a href="https://github.com/Bappaditya-kuilya/kisuke-mcp/blob/main/CODE_OF_CONDUCT.md" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-600 dark:text-zinc-400 hover:text-gray-900 dark:hover:text-zinc-100 transition-colors">Code of Conduct</a></li>
              </ul>
            </nav>
          </div>
          <div className="mt-12 pt-8 border-t border-gray-200 dark:border-zinc-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-gray-500 dark:text-zinc-400">MIT License. Built with care.</p>
            <p className="text-xs text-gray-500 dark:text-zinc-400">© 2026 context-mcp</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
