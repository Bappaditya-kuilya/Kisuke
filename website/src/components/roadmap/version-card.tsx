interface VersionCardProps {
  version: string;
  title: string;
  description: string;
  status: "released" | "planned" | "future";
}

function VersionCard({
  version,
  title,
  description,
  status,
}: VersionCardProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-6">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg font-medium text-text-primary font-mono">
          {version}
        </span>
        {status === "released" && (
          <span className="px-1.5 py-0.5 text-xs font-medium bg-success/10 text-success rounded">
            Released
          </span>
        )}
        {status === "planned" && (
          <span className="px-1.5 py-0.5 text-xs font-medium bg-accent/10 text-accent rounded">
            Planned
          </span>
        )}
        {status === "future" && (
          <span className="px-1.5 py-0.5 text-xs font-medium bg-text-tertiary/10 text-text-tertiary rounded">
            Future
          </span>
        )}
      </div>
      <h3 className="text-base font-medium text-text-primary mb-2">{title}</h3>
      <p className="text-sm text-text-secondary leading-relaxed">
        {description}
      </p>
    </div>
  );
}

export { VersionCard };
