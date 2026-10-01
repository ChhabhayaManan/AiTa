import { useEffect, useState } from 'react'
import { Lock, Activity, AlertTriangle, History } from 'lucide-react'
import { profileAPI } from '../../utils/api'
import {
  BAND_STYLE, EVENT_KIND_LABELS, misconceptionLabel, topicLabel,
} from './labels'

function MasteryBar({ topic }) {
  const style = BAND_STYLE[topic.band] || BAND_STYLE.unseen
  const pct = Math.round(topic.mastery * 100)
  return (
    <div className={topic.unlocked ? '' : 'opacity-50'}>
      <div className="flex items-center justify-between mb-1">
        <span className="flex items-center gap-1.5 text-sm text-white/80 font-body">
          {!topic.unlocked && <Lock size={11} className="text-white/30" />}
          {topic.label}
        </span>
        <span className={`text-xs font-mono ${style.text}`}>
          {topic.evidence_count === 0 ? 'not yet practised' : `${pct}% · ${topic.evidence_count} graded`}
        </span>
      </div>
      <div className="h-2 bg-surface-600 rounded-full overflow-hidden">
        <div className={`h-full ${style.bar} rounded-full transition-all duration-700`}
             style={{ width: `${topic.evidence_count === 0 ? 0 : pct}%` }} />
      </div>
    </div>
  )
}

export default function MasteryPanel({ refreshKey = 0 }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    profileAPI.getMastery()
      .then(({ data }) => { setData(data); setError(false) })
      .catch(() => setError(true))
  }, [refreshKey])

  if (error) {
    return <div className="glass-card p-6 text-white/40 text-sm">Mastery could not be loaded.</div>
  }
  if (!data) return <div className="glass-card h-72 animate-pulse" />

  const practised = data.topics.filter(t => t.evidence_count > 0).length

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="glass-card p-6 lg:col-span-2">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <Activity size={15} className="text-brand-400" />
            <p className="text-white/40 text-xs font-mono uppercase tracking-wider">Topic mastery (measured)</p>
          </div>
          <span className="text-white/30 text-xs font-mono">{practised}/12 topics practised</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
          {data.topics.map(t => <MasteryBar key={t.topic} topic={t} />)}
        </div>
        <div className="flex flex-wrap gap-4 mt-5 pt-4 border-t border-white/[0.06]">
          {['weak', 'developing', 'mastered'].map(b => (
            <span key={b} className="flex items-center gap-1.5 text-xs text-white/40">
              <span className={`w-2.5 h-2.5 rounded-full ${BAND_STYLE[b].bar}`} /> {BAND_STYLE[b].label}
            </span>
          ))}
          <span className="flex items-center gap-1.5 text-xs text-white/40">
            <Lock size={11} /> Locked until its prerequisites reach 40%
          </span>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="glass-card p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle size={15} className="text-yellow-400" />
            <p className="text-white/40 text-xs font-mono uppercase tracking-wider">Recurring mistakes</p>
          </div>
          {data.top_misconceptions.length === 0 ? (
            <p className="text-white/30 text-sm">None recorded yet.</p>
          ) : (
            <div className="space-y-2">
              {data.top_misconceptions.slice(0, 5).map(m => (
                <div key={m.tag} className="flex items-center justify-between">
                  <span className="text-sm text-white/70">{misconceptionLabel(m.tag)}</span>
                  <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-yellow-500/15 text-yellow-400">×{m.count}</span>
                </div>
              ))}
            </div>
          )}
          <p className="text-white/25 text-xs mt-4">
            Hint reliance: <span className="text-white/50 font-mono">{data.hint_reliance.toFixed(1)}</span> average hint level over the last 10 coding attempts
          </p>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center gap-2 mb-4">
            <History size={15} className="text-teal-400" />
            <p className="text-white/40 text-xs font-mono uppercase tracking-wider">Recent evidence</p>
          </div>
          {data.recent_events.length === 0 ? (
            <p className="text-white/30 text-sm">Nothing graded yet.</p>
          ) : (
            <div className="space-y-2.5">
              {data.recent_events.slice(0, 6).map(e => (
                <div key={e.id} className="text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-white/70">{EVENT_KIND_LABELS[e.kind] || e.kind} · {topicLabel(e.topic)}</span>
                    <span className="font-mono text-white/50">{Math.round(e.score * 100)}%</span>
                  </div>
                  {e.mastery_before != null && (
                    <div className="font-mono text-white/30 mt-0.5">
                      mastery {e.mastery_before.toFixed(2)} → {e.mastery_after.toFixed(2)}
                      {e.hint_level_used > 0 && ` · hint L${e.hint_level_used}`}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
