"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { ChevronDown } from "lucide-react";

interface FaqItemProps {
  question: string;
  answer: string;
}

function FaqItem({ question, answer }: FaqItemProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="bg-surface border border-border-subtle rounded-lg overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-4 p-5 text-left hover:bg-surface-raised transition-colors duration-100"
        aria-expanded={isOpen}
      >
        <span className="text-sm font-medium text-text-primary">{question}</span>
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
            {answer}
          </p>
        </div>
      )}
    </div>
  );
}

export { FaqItem };
