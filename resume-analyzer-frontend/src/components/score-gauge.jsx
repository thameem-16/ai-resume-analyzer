import { useEffect, useState } from "react"

function scoreLabel(score) {
  if (score >= 80) return "Strong match"
  if (score >= 60) return "Good match"
  if (score >= 40) return "Partial match"
  return "Weak match"
}

export function ScoreGauge({ score }) {
  const clamped = Math.max(0, Math.min(100, Math.round(score)))
  const [animated, setAnimated] = useState(0)

  useEffect(() => {
    const raf = requestAnimationFrame(() => setAnimated(clamped))
    return () => cancelAnimationFrame(raf)
  }, [clamped])

  const size = 220
  const stroke = 16
  const radius = (size - stroke) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (animated / 100) * circumference

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="-rotate-90"
        role="img"
        aria-label={`Match score ${clamped} out of 100`}
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--secondary)"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--primary)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1.1s cubic-bezier(0.22, 1, 0.36, 1)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display text-5xl font-bold tabular-nums text-foreground">{clamped}</span>
        <span className="text-sm font-medium text-muted-foreground">out of 100</span>
        <span className="mt-1 text-sm font-semibold text-primary">{scoreLabel(clamped)}</span>
      </div>
    </div>
  )
}
