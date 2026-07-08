function DataFlowDiagram() {
  const steps = [
    { label: "Markdown", sub: "Source of truth", color: "#c084fc" },
    { label: "Storage", sub: "One entity = one file", color: "#93c5fd" },
    { label: "Validation", sub: "Schema + references", color: "#86efac" },
    { label: "Search Index", sub: "Tantivy", color: "#fbbf24" },
    { label: "Resume Engine", sub: "Context reconstruction", color: "#f9a8d4" },
    { label: "AI", sub: "Optional", color: "#6366f1" },
    { label: "CLI", sub: "Output", color: "#ececef" },
  ];

  return (
    <svg
      viewBox="0 0 800 180"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-auto"
      role="img"
      aria-label="Data flow diagram showing how data moves through Kisuke"
    >
      <rect width="800" height="180" fill="#08080a" rx="8" />

      {steps.map((step, i) => {
        const x = 40 + i * 112;
        return (
          <g key={step.label}>
            {/* Box */}
            <rect
              x={x}
              y="50"
              width="96"
              height="64"
              rx="8"
              fill="#111113"
              stroke={step.color}
              strokeWidth="1"
              strokeOpacity="0.4"
            />
            {/* Label */}
            <text
              x={x + 48}
              y="76"
              textAnchor="middle"
              fill="#ececef"
              fontSize="12"
              fontFamily="system-ui"
              fontWeight="500"
            >
              {step.label}
            </text>
            {/* Sub label */}
            <text
              x={x + 48}
              y="94"
              textAnchor="middle"
              fill="#6b6b73"
              fontSize="10"
              fontFamily="system-ui"
            >
              {step.sub}
            </text>

            {/* Arrow */}
            {i < steps.length - 1 && (
              <>
                <line
                  x1={x + 96}
                  y1="82"
                  x2={x + 112}
                  y2="82"
                  stroke="#45454d"
                  strokeWidth="1"
                />
                <polygon
                  points={`${x + 112},82 ${x + 106},78 ${x + 106},86`}
                  fill="#45454d"
                />
              </>
            )}
          </g>
        );
      })}

      {/* Optional badge on AI */}
      <rect x="660" y="120" width="52" height="18" rx="9" fill="#6366f1" fillOpacity="0.15" />
      <text x="686" y="132" textAnchor="middle" fill="#6366f1" fontSize="9" fontFamily="system-ui" fontWeight="500">
        OPTIONAL
      </text>

      {/* Legend */}
      <text x="40" y="160" fill="#6b6b73" fontSize="10" fontFamily="system-ui">
        Data flows left to right. AI is optional. Markdown is the single source of truth.
      </text>
    </svg>
  );
}

export { DataFlowDiagram };
