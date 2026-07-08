import { cn } from "@/lib/utils";

interface TerminalProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
}

function Terminal({ children, className, title }: TerminalProps) {
  return (
    <div
      className={cn(
        "bg-surface-inset border border-border-subtle rounded-lg overflow-hidden",
        className
      )}
    >
      <div className="flex items-center gap-2 px-4 h-8 border-b border-border-subtle">
        <div className="flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-text-disabled/40" />
          <div className="w-2.5 h-2.5 rounded-full bg-text-disabled/40" />
          <div className="w-2.5 h-2.5 rounded-full bg-text-disabled/40" />
        </div>
        {title && (
          <span className="text-xs text-text-tertiary font-mono ml-2">
            {title}
          </span>
        )}
      </div>
      <div className="p-4 overflow-x-auto">
        <pre className="font-mono text-sm text-text-secondary leading-relaxed">
          <code>{children}</code>
        </pre>
      </div>
    </div>
  );
}

export { Terminal };
