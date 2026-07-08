interface LayerCardProps {
  name: string;
  responsibility: string;
  dependsOn: string;
  usedBy: string;
  modules: string[];
  color: string;
}

function LayerCard({
  name,
  responsibility,
  dependsOn,
  usedBy,
  modules,
  color,
}: LayerCardProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <div
          className="w-2.5 h-2.5 rounded-full"
          style={{ backgroundColor: color }}
        />
        <h3 className="text-base font-medium text-text-primary">{name}</h3>
      </div>

      <div className="space-y-3 text-sm">
        <div>
          <span className="text-text-tertiary text-xs uppercase tracking-wider">
            Responsibility
          </span>
          <p className="text-text-secondary mt-1 leading-relaxed">
            {responsibility}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row sm:gap-6">
          <div>
            <span className="text-text-tertiary text-xs uppercase tracking-wider">
              Depends on
            </span>
            <p className="text-text-secondary mt-1">{dependsOn}</p>
          </div>
          <div>
            <span className="text-text-tertiary text-xs uppercase tracking-wider">
              Used by
            </span>
            <p className="text-text-secondary mt-1">{usedBy}</p>
          </div>
        </div>

        <div>
          <span className="text-text-tertiary text-xs uppercase tracking-wider">
            Key modules
          </span>
          <div className="flex flex-wrap gap-1.5 mt-2">
            {modules.map((mod) => (
              <span
                key={mod}
                className="inline-block px-2 py-0.5 text-xs font-mono text-text-secondary bg-surface-inset border border-border-subtle rounded"
              >
                {mod}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export { LayerCard };
