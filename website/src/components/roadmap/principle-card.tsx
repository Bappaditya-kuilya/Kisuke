interface PrincipleCardProps {
  title: string;
  description: string;
}

function PrincipleCard({ title, description }: PrincipleCardProps) {
  return (
    <div className="bg-surface border border-border-subtle rounded-lg p-5">
      <h3 className="text-sm font-medium text-text-primary mb-2">{title}</h3>
      <p className="text-xs text-text-secondary leading-relaxed">
        {description}
      </p>
    </div>
  );
}

export { PrincipleCard };
