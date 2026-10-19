import { Check } from 'lucide-react'
import { STEPS } from './options'

export default function ProgressHeader({ step, question, remaining }) {
  const current = STEPS.findIndex(s => s.key === step)
  const total = question ? question + (remaining || 0) : 0

  return (
    <div className="mb-6">
      <ol className="flex items-start">
        {STEPS.map((s, i) => {
          const done = i < current
          const active = i === current
          return (
            <li key={s.key} className="flex-1 flex flex-col items-center relative">
              {i > 0 && (
                <span className={`absolute top-3.5 right-1/2 w-full h-0.5 ${i <= current ? 'bg-brand-500/60' : 'bg-white/10'}`} />
              )}
              <span
                className={`relative z-10 w-7 h-7 rounded-full flex items-center justify-center text-xs font-display font-bold border-2 transition-all
                  ${done ? 'bg-brand-600 border-brand-500 text-white'
                    : active ? 'bg-brand-600/15 border-brand-500 text-brand-300'
                    : 'bg-surface-800 border-white/10 text-white/30'}`}
                aria-current={active ? 'step' : undefined}
              >
                {done ? <Check size={13} /> : i + 1}
              </span>
              <span className={`mt-2 text-[11px] font-display font-semibold text-center leading-tight ${active ? 'text-white' : 'text-white/35'}`}>
                {s.label}
              </span>
            </li>
          )
        })}
      </ol>

      {question ? (
        <div className="mt-5">
          <p className="text-xs text-white/50 font-body mb-1.5">
            Question {question} · {remaining ? `about ${remaining} left` : 'Last question'}
          </p>
          <div className="h-1 rounded-full bg-white/10 overflow-hidden">
            <div className="h-full bg-brand-500 transition-all duration-500"
              style={{ width: `${Math.min(100, (question / total) * 100)}%` }} />
          </div>
        </div>
      ) : null}
    </div>
  )
}
