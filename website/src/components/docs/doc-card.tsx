import Link from "next/link";
import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";

interface DocCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  href: string;
  category?: string;
  readTime?: string;
  difficulty?: "beginner" | "intermediate" | "advanced";
}

function DocCard({
  icon: Icon,
  title,
  description,
  href,
  category,
  readTime,
  difficulty,
}: DocCardProps) {
  return (
    <Link href={href} className="group block">
      <div
        className={cn(
          "bg-surface border border-border-subtle rounded-lg p-6 h-full",
          "transition-all duration-100",
          "hover:bg-surface-raised hover:border-border-default hover:shadow-sm"
        )}
      >
        <div className="flex items-start justify-between gap-4 mb-3">
          <Icon className="w-5 h-5 text-accent shrink-0 mt-0.5" />
          <div className="flex items-center gap-2 text-xs text-text-tertiary">
            {difficulty && (
              <span
                className={cn("capitalize", {
                  "text-code-string": difficulty === "beginner",
                  "text-code-type": difficulty === "intermediate",
                  "text-code-keyword": difficulty === "advanced",
                })}
              >
                {difficulty}
              </span>
            )}
            {readTime && <span>{readTime}</span>}
          </div>
        </div>
        <h3 className="text-base font-medium text-text-primary mb-1.5 group-hover:text-accent transition-colors duration-100">
          {title}
        </h3>
        <p className="text-sm text-text-secondary leading-relaxed mb-3">
          {description}
        </p>
        {category && (
          <span className="inline-block text-xs text-text-tertiary font-mono">
            {category}
          </span>
        )}
      </div>
    </Link>
  );
}

export { DocCard };
export type { DocCardProps };
