import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
}

function Badge({ children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-3 py-1 text-xs font-medium uppercase tracking-widest text-accent bg-accent-muted rounded-full",
        className
      )}
    >
      {children}
    </span>
  );
}

export { Badge };
