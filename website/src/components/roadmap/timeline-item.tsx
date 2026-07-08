import { cn } from "@/lib/utils";

interface TimelineItemProps {
  title: string;
  description: string;
  version?: string;
  status: "completed" | "current" | "upcoming";
  isLast?: boolean;
}

function TimelineItem({
  title,
  description,
  version,
  status,
  isLast = false,
}: TimelineItemProps) {
  return (
    <div className="flex gap-4">
      {/* Vertical line + dot */}
      <div className="flex flex-col items-center">
        <div
          className={cn(
            "w-3 h-3 rounded-full shrink-0 mt-1.5",
            status === "completed" && "bg-success",
            status === "current" && "bg-accent shadow-glow",
            status === "upcoming" && "bg-text-disabled"
          )}
        />
        {!isLast && (
          <div
            className={cn(
              "w-px flex-1 min-h-[24px]",
              status === "completed" ? "bg-success/30" : "bg-border-subtle"
            )}
          />
        )}
      </div>

      {/* Content */}
      <div className="pb-6">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="text-sm font-medium text-text-primary">{title}</h3>
          {version && (
            <span className="text-xs font-mono text-text-tertiary">
              {version}
            </span>
          )}
          {status === "completed" && (
            <span className="px-1.5 py-0.5 text-xs font-medium bg-success/10 text-success rounded">
              Done
            </span>
          )}
          {status === "current" && (
            <span className="px-1.5 py-0.5 text-xs font-medium bg-accent/10 text-accent rounded">
              Current
            </span>
          )}
        </div>
        <p className="text-xs text-text-secondary leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
}

export { TimelineItem };
