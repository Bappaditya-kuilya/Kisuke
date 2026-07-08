interface VerificationStatProps {
  label: string;
  value: string;
  icon: string;
}

function VerificationStat({ label, value, icon }: VerificationStatProps) {
  return (
    <div className="flex items-center gap-3 bg-surface border border-border-subtle rounded-lg px-5 py-3.5">
      <span className="text-lg">{icon}</span>
      <div>
        <div className="text-sm font-medium text-text-primary">{value}</div>
        <div className="text-xs text-text-tertiary">{label}</div>
      </div>
    </div>
  );
}

export { VerificationStat };
