interface PerformanceStatProps {
  label: string;
  value: string;
  unit?: string;
  description?: string;
  color?: string;
}

function PerformanceStat({
  label,
  value,
  unit,
  description,
  color = "#6366f1",
}: PerformanceStatProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-6 text-center">
      <div className="text-3xl sm:text-4xl font-medium tracking-tight mb-1" style={{ color }}>
        {value}
        {unit && (
          <span className="text-lg text-text-tertiary ml-1">{unit}</span>
        )}
      </div>
      <div className="text-sm font-medium text-text-primary mb-1">{label}</div>
      {description && (
        <div className="text-xs text-text-tertiary">{description}</div>
      )}
    </div>
  );
}

export { PerformanceStat };
