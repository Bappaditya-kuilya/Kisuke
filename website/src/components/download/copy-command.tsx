"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface CopyCommandProps {
  command: string;
  className?: string;
}

function CopyCommand({ command, className }: CopyCommandProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div
      className={`flex items-center gap-2 bg-surface-inset border border-border-subtle rounded-lg px-4 py-2.5 ${
        className ?? ""
      }`}
    >
      <code className="font-mono text-sm text-text-primary flex-1 overflow-x-auto">
        {command}
      </code>
      <button
        onClick={handleCopy}
        className="shrink-0 p-1 text-text-disabled hover:text-text-secondary transition-colors duration-100"
        aria-label={`Copy ${command}`}
      >
        {copied ? (
          <Check className="w-3.5 h-3.5 text-success" />
        ) : (
          <Copy className="w-3.5 h-3.5" />
        )}
      </button>
    </div>
  );
}

export { CopyCommand };
