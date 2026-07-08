"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { ChevronDown } from "lucide-react";

interface AdrCardProps {
  id: string;
  title: string;
  status: "Accepted" | "Proposed" | "Superseded";
  summary: string;
  details: string;
}

function AdrCard({ id, title, status, summary, details }: AdrCardProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="bg-surface border border-border-subtle rounded-lg overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-4 p-5 text-left hover:bg-surface-raised transition-colors duration-100"
        aria-expanded={isOpen}
      >
        <div className="flex items-center gap-3 min-w-0">
          <span className="text-xs font-mono text-text-tertiary shrink-0">
            {id}
          </span>
          <span className="text-sm font-medium text-text-primary truncate">
            {title}
          </span>
          <span
            className={cn(
              "shrink-0 px-2 py-0.5 text-xs font-medium rounded-full",
              status === "Accepted" && "bg-success/10 text-success",
              status === "Proposed" && "bg-warning/10 text-warning",
              status === "Superseded" && "bg-text-tertiary/10 text-text-tertiary"
            )}
          >
            {status}
          </span>
        </div>
        <ChevronDown
          className={cn(
            "w-4 h-4 text-text-tertiary shrink-0 transition-transform duration-100",
            isOpen && "rotate-180"
          )}
        />
      </button>

      {isOpen && (
        <div className="px-5 pb-5 border-t border-border-subtle">
          <p className="text-sm text-text-secondary mt-4 leading-relaxed">
            {summary}
          </p>
          <p className="text-sm text-text-tertiary mt-3 leading-relaxed">
            {details}
          </p>
        </div>
      )}
    </div>
  );
}

export { AdrCard };
