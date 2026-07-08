import { Terminal } from "@/components/ui/terminal";

interface QuickStartStepProps {
  step: number;
  title: string;
  command: string;
  description?: string;
}

function QuickStartStep({
  step,
  title,
  command,
  description,
}: QuickStartStepProps) {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-3">
        <span className="flex items-center justify-center w-7 h-7 rounded-full bg-accent-muted text-accent text-xs font-mono font-medium">
          {step}
        </span>
        <h3 className="text-base font-medium text-text-primary">{title}</h3>
      </div>
      <Terminal className="text-sm">
        <span className="text-text-tertiary">$</span>{" "}
        <span className="text-text-primary">{command}</span>
      </Terminal>
      {description && (
        <p className="text-sm text-text-secondary leading-relaxed">
          {description}
        </p>
      )}
    </div>
  );
}

export { QuickStartStep };
