interface StatusStatProps {
  label: string;
  value: string;
}

function StatusStat({ label, value }: StatusStatProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-5 text-center">
      <div className="text-2xl font-medium tracking-tight text-text-primary mb-1">
        {value}
      </div>
      <div className="text-xs text-text-tertiary">{label}</div>
    </div>
  );
}

export { StatusStat };
