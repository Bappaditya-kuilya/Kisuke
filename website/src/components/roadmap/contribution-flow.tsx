function ContributionFlow() {
  const steps = [
    { label: "Issue", color: "#c084fc" },
    { label: "Discussion", color: "#93c5fd" },
    { label: "PR", color: "#86efac" },
    { label: "Review", color: "#fbbf24" },
    { label: "Merge", color: "#22c55e" },
  ];

  return (
    <svg
      viewBox="0 0 700 120"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-auto"
      role="img"
      aria-label="Contribution flow: Issue, Discussion, PR, Review, Merge"
    >
      <rect width="700" height="120" fill="#08080a" rx="8" />

      {steps.map((step, i) => {
        const x = 40 + i * 136;
        return (
          <g key={step.label}>
            <rect
              x={x}
              y="35"
              width="104"
              height="50"
              rx="8"
              fill="#111113"
              stroke={step.color}
              strokeWidth="1"
              strokeOpacity="0.4"
            />
            <text
              x={x + 52}
              y="65"
              textAnchor="middle"
              fill="#ececef"
              fontSize="13"
              fontFamily="system-ui"
              fontWeight="500"
            >
              {step.label}
            </text>

            {i < steps.length - 1 && (
              <>
                <line
                  x1={x + 104}
                  y1="60"
                  x2={x + 136}
                  y2="60"
                  stroke="#45454d"
                  strokeWidth="1"
                />
                <polygon
                  points={`${x + 136},60 ${x + 130},56 ${x + 130},64`}
                  fill="#45454d"
                />
              </>
            )}
          </g>
        );
      })}

      <text x="350" y="110" textAnchor="middle" fill="#6b6b73" fontSize="10" fontFamily="system-ui">
        Architecture changes require RFC before PR
      </text>
    </svg>
  );
}

export { ContributionFlow };
