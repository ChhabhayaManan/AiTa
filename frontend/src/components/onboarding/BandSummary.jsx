import { TIERS } from './options'
import { topicLabel } from '../learning/labels'

const GROUPS = [
  { band: 'strong',      label: 'Strengths',       chip: 'border-emerald-500/50 bg-emerald-500/15 text-emerald-300' },
  { band: 'needs_work',  label: 'Next focus',      chip: 'border-amber-500/50 bg-amber-500/10 text-amber-300' },
  { band: 'ok',          label: 'Doing fine',      chip: 'border-sky-500/40 bg-sky-500/10 text-sky-300' },
  { band: 'not_checked', label: 'Not checked yet', chip: 'border-white/10 bg-surface-700/30 text-white/45' },
]

const ORDER = TIERS.flat()
const rank = t => (ORDER.includes(t) ? ORDER.indexOf(t) : ORDER.length)

export const conceptLine = (card) => {
  if (card.theory_pending) return 'Theory answers being reviewed'
  if (card.concept_level === 'unknown') return 'How well you explain ideas: not checked yet'
  return `How well you explain ideas: ${card.concept_level}`
}

export default function BandSummary({ card, headingLevel = 3 }) {
  const Heading = `h${headingLevel}`
  const inferred = new Set(card.inferred || [])
  const topics = Object.keys(card.bands || {}).sort((a, b) => rank(a) - rank(b))

  return (
    <div className="space-y-4">
      {GROUPS.map(({ band, label, chip }) => {
        const list = topics.filter(t => card.bands[t] === band)
        if (!list.length) return null
        return (
          <section key={band}>
            <Heading className="label !mb-2">{label}</Heading>
            <ul className="flex flex-wrap gap-1.5">
              {list.map(t => (
                <li key={t}
                  className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border-2 text-xs font-display font-semibold ${chip} ${inferred.has(t) ? 'border-dotted' : ''}`}>
                  {topicLabel(t)}
                  {inferred.has(t) && <span className="font-normal opacity-75">· inferred</span>}
                </li>
              ))}
            </ul>
          </section>
        )
      })}
      {inferred.size > 0 && (
        <p className="text-xs text-white/40">Inferred topics weren't asked directly; they're estimated from your other answers.</p>
      )}
    </div>
  )
}
