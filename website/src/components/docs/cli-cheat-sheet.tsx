"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface CommandEntry {
  command: string;
  description: string;
}

interface CommandGroup {
  label: string;
  commands: CommandEntry[];
}

const commandGroups: CommandGroup[] = [
  {
    label: "Getting Started",
    commands: [
      { command: "kisuke init", description: "Initialize a Kisuke repository" },
      {
        command: "kisuke doctor",
        description: "Run health checks on your repository",
      },
      {
        command: "kisuke status",
        description: "Show repository status and entity counts",
      },
    ],
  },
  {
    label: "Context",
    commands: [
      {
        command: "kisuke resume",
        description: "Reconstruct working context for the current mission",
      },
      {
        command: "kisuke resume --project <name>",
        description: "Resume context for a specific project",
      },
      {
        command: "kisuke resume --last",
        description: "Resume the most recent context",
      },
    ],
  },
  {
    label: "Entities",
    commands: [
      {
        command: "kisuke mission create <name>",
        description: "Create a new mission",
      },
      {
        command: "kisuke project create <name>",
        description: "Create a new project under the active mission",
      },
      {
        command: "kisuke task add <title>",
        description: "Add a task to the current project",
      },
      {
        command: "kisuke decision add <title>",
        description: "Record an architectural or design decision",
      },
      {
        command: "kisuke knowledge add <title>",
        description: "Add a knowledge entry",
      },
    ],
  },
  {
    label: "Search & Review",
    commands: [
      {
        command: "kisuke search <query>",
        description: "Search across all entities",
      },
      {
        command: "kisuke review weekly",
        description: "Generate a weekly review",
      },
      {
        command: "kisuke sync",
        description: "Sync the search index",
      },
    ],
  },
  {
    label: "Management",
    commands: [
      {
        command: "kisuke config get <key>",
        description: "Read a configuration value",
      },
      {
        command: "kisuke config set <key> <value>",
        description: "Set a configuration value",
      },
      {
        command: "kisuke plugin list",
        description: "List installed plugins",
      },
      {
        command: "kisuke index build",
        description: "Rebuild the search index",
      },
    ],
  },
];

function CliCheatSheet() {
  const [copiedIdx, setCopiedIdx] = useState<string | null>(null);

  const handleCopy = async (command: string, groupIdx: number, cmdIdx: number) => {
    await navigator.clipboard.writeText(command);
    setCopiedIdx(`${groupIdx}-${cmdIdx}`);
    setTimeout(() => setCopiedIdx(null), 1500);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {commandGroups.map((group, groupIdx) => (
        <div key={group.label}>
          <h3 className="text-sm font-medium text-text-primary mb-3 font-mono">
            {group.label}
          </h3>
          <div className="space-y-2">
            {group.commands.map((cmd, cmdIdx) => (
              <div
                key={cmd.command}
                className="group flex items-center gap-2 bg-surface-inset border border-border-subtle rounded-lg px-4 py-2.5"
              >
                <code className="font-mono text-sm text-text-primary flex-1 overflow-x-auto">
                  {cmd.command}
                </code>
                <span className="text-xs text-text-tertiary hidden sm:block shrink-0 max-w-[200px] truncate">
                  {cmd.description}
                </span>
                <button
                  onClick={() => handleCopy(cmd.command, groupIdx, cmdIdx)}
                  className="shrink-0 p-1 text-text-disabled hover:text-text-secondary transition-colors duration-100"
                  aria-label={`Copy ${cmd.command}`}
                >
                  {copiedIdx === `${groupIdx}-${cmdIdx}` ? (
                    <Check className="w-3.5 h-3.5 text-success" />
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export { CliCheatSheet };
