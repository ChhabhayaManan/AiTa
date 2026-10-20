import { TIERS } from './options'
import { topicLabel } from '../learning/labels'

const STATES = {
  asking:     { label: 'Asking now',  chip: 'border-brand-400/80 bg-brand-600/20 text-brand-200 motion-safe:animate-pulse' },
  strong:     { label: 'Strong',      chip: 'border-emerald-500/50 bg-emerald-500/15 text-emerald-300' },
  ok:         { label: 'Passed',      chip: 'border-sky-500/40 bg-sky-500/10 text-sky-300' },
  needs_work: { label: 'Needs work',  chip: 'border-amber-500/50 bg-amber-500/10 text-amber-300' },
  inferred:   { label: 'Inferred',    chip: 'border-dotted border-sky-400/60 bg-transparent text-sky-300/80' },
  skipped:    { label: 'Skipped',     chip: 'border-white/15 bg-transparent text-white/35 italic' },
  unknown:    { label: 'Not checked', chip: 'border-white/10 bg-surface-700/30 text-white/40' },
}

const CHIP = 'inline-flex items-center px-2.5 py-1 rounded-lg border-2 text-[11px] font-display font-semibold leading-tight'

export default function TopicMap({ states = {}, note }) {
  return (
    <section aria-label="Topic map" className="rounded-xl border border-white/[0.06] bg-surface-900/40 p-4">
      <h3 className={`label ${note ? '!mb-1' : '!mb-3'}`}>Topic map</h3>
      {note && <p className="text-[11px] text-white/40 mb-3">{note}</p>}
      <ol className="space-y-2">
        {TIERS.map((tier, i) => (
          <li key={i} className="flex items-start gap-2">
            <span className="w-6 shrink-0 pt-1 text-[10px] font-mono text-white/30">T{i + 1}</span>
            <ul className="flex flex-wrap gap-1.5">
              {tier.map(topic => {
                const s = STATES[states[topic]] || STATES.unknown
                return (
                  <li key={topic} className={`${CHIP} ${s.chip}`} title={s.label}>
                    {topicLabel(topic)}<span className="sr-only">: {s.label}</span>
                  </li>
                )
              })}
            </ul>
          </li>
        ))}
      </ol>
      <ul aria-hidden="true" className="mt-4 pt-3 border-t border-white/[0.06] flex flex-wrap gap-x-3 gap-y-1.5">
        {Object.entries(STATES).map(([key, s]) => (
          <li key={key} className="flex items-center gap-1.5 text-[10px] text-white/45">
            <span className={`w-3 h-3 rounded border-2 ${s.chip}`} />
            {s.label}
          </li>
        ))}
      </ul>
    </section>
  )
}
