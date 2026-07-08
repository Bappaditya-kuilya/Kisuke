interface RequirementCardProps {
  label: string;
  value: string;
  icon: string;
}

function RequirementCard({ label, value, icon }: RequirementCardProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-5 text-center">
      <div className="text-2xl mb-2">{icon}</div>
      <div className="text-sm font-medium text-text-primary mb-1">{label}</div>
      <div className="text-xs text-text-secondary">{value}</div>
    </div>
  );
}

export { RequirementCard };
