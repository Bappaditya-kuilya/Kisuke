import { Check } from "lucide-react";

interface FeatureCheckProps {
  label: string;
}

function FeatureCheck({ label }: FeatureCheckProps) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex items-center justify-center w-5 h-5 rounded-full bg-success/10 shrink-0">
        <Check className="w-3 h-3 text-success" />
      </div>
      <span className="text-sm text-text-secondary">{label}</span>
    </div>
  );
}

export { FeatureCheck };
