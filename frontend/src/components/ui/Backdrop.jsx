import { memo } from 'react'

const W = 1600
const H = 1000
const ACCENTS = { 4: '#8fe3a0', 9: '#7de3e8', 14: '#f27aa2' }

function contour(i) {
  const base = 40 + i * 52
  const amp = 26 + (i % 5) * 9
  const phase = i * 0.55
  const pts = []
  for (let x = -40; x <= W + 40; x += 40) {
    const y = base
      + Math.sin(x / 210 + phase) * amp
      + Math.sin(x / 97 + phase * 1.7) * (amp * 0.28)
    pts.push(`${x},${y.toFixed(1)}`)
  }
  return `M${pts.join(' L')}`
}

const LINES = Array.from({ length: 19 }, (_, i) => ({ d: contour(i), color: ACCENTS[i] }))

function Backdrop() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden" aria-hidden="true">
      <svg className="absolute inset-0 h-full w-full" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid slice">
        <defs>
          <pattern id="bd-dots" width="24" height="24" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1" fill="#ffffff" fillOpacity="0.1" />
          </pattern>
          <linearGradient id="bd-fade" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#fff" stopOpacity="1" />
            <stop offset="1" stopColor="#fff" stopOpacity="0.25" />
          </linearGradient>
          <mask id="bd-mask">
            <rect width={W} height={H} fill="url(#bd-fade)" />
          </mask>
          <filter id="bd-grain">
            <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" />
            <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.5 0" />
          </filter>
        </defs>
        <g mask="url(#bd-mask)">
          <rect width={W} height={H} fill="url(#bd-dots)" />
          {LINES.map((l, i) => (
            <path
              key={i}
              d={l.d}
              fill="none"
              stroke={l.color || '#ffffff'}
              strokeOpacity={l.color ? 0.3 : 0.11}
              strokeWidth={l.color ? 1.4 : 1}
            />
          ))}
        </g>
        <rect width={W} height={H} filter="url(#bd-grain)" opacity="0.05" />
      </svg>
      <div className="absolute inset-0 bg-canvas/40" />
    </div>
  )
}

export default memo(Backdrop)
