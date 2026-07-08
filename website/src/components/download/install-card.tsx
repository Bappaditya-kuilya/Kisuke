import { CopyCommand } from "./copy-command";

interface InstallCardProps {
  method: string;
  command: string;
  description: string;
  recommended?: boolean;
}

function InstallCard({
  method,
  command,
  description,
  recommended,
}: InstallCardProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-5">
      <div className="flex items-center gap-2 mb-3">
        <h3 className="text-sm font-medium text-text-primary">{method}</h3>
        {recommended && (
          <span className="px-2 py-0.5 text-xs font-medium bg-accent/10 text-accent rounded-full">
            Recommended
          </span>
        )}
      </div>
      <p className="text-xs text-text-secondary mb-3 leading-relaxed">
        {description}
      </p>
      <CopyCommand command={command} />
    </div>
  );
}

export { InstallCard };
