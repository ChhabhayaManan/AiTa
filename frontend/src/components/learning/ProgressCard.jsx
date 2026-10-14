import { useState } from 'react'
import { Award, ArrowDown, ArrowUp, Eye, Minus, TrendingUp } from 'lucide-react'
import { BAND_STYLE } from './labels'

function TopicStep({ topic }) {
  const style = BAND_STYLE[topic.band] || BAND_STYLE.unseen
  const target = topic.next_band === 'developing' ? 0.4 : 0.75
  const pct = topic.next_band ? Math.min(100, Math.round((topic.mastery / target) * 100)) : 100
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm text-white/80 font-body">{topic.label}</span>
        <span className={`text-xs font-mono ${style.text}`}>
          {topic.next_band ? `${topic.gap_to_next.toFixed(2)} to ${topic.next_band}` : BAND_STYLE.mastered.label}
        </span>
      </div>
      <div className="h-2 bg-surface-600 rounded-full overflow-hidden">
        <div className={`h-full ${style.bar} rounded-full transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function Delta({ label, now, before }) {
  const Icon = now > before ? ArrowUp : now < before ? ArrowDown : Minus
  const color = now > before ? 'text-teal-400' : now < before ? 'text-white/40' : 'text-white/30'
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-white/50">{label}</span>
      <span className="flex items-center gap-2 font-mono">
        <span className="text-white">{now}</span>
        <Icon size={12} className={color} />
        <span className="text-white/30 text-xs">vs {before}</span>
      </span>
    </div>
  )
}

export default function ProgressCard({ data }) {
  const [revealed, setRevealed] = useState(false)
  if (!data || data.mode === 'off') return null

  if (data.mode === 'silent' && !revealed) {
    return (
      <div className="glass-card p-6 mb-6 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <TrendingUp size={18} className="text-brand-400" />
          <p className="text-white/60 text-sm">Your progress recap is ready.</p>
        </div>
        <button onClick={() => setRevealed(true)}
          className="inline-flex items-center gap-2 px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-sm font-display font-600 rounded-xl transition-colors">
          <Eye size={14} /> Reveal my progress
        </button>
      </div>
    )
  }

  const { last_7: now, prev_7: before } = data.self_board
  const practised = data.topics.filter(t => t.band !== 'unseen')

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
      <div className="glass-card p-6 lg:col-span-2">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <TrendingUp size={15} className="text-brand-400" />
            <p className="text-white/40 text-xs font-mono uppercase tracking-wider">Your progress</p>
          </div>
          <span className="text-white/30 text-xs font-mono">{data.points} pts · level {data.level}</span>
        </div>
        {practised.length === 0 ? (
          <p className="text-white/30 text-sm">Solve a few items and your topic levels appear here.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
            {practised.map(t => <TopicStep key={t.topic} topic={t} />)}
          </div>
        )}
      </div>

      <div className="flex flex-col gap-4">
        <div className="glass-card p-6">
          <p className="text-white/40 text-xs font-mono uppercase tracking-wider mb-4">You vs last week</p>
          <div className="flex flex-col gap-2">
            <Delta label="Points" now={now.points} before={before.points} />
            <Delta label="Items solved" now={now.solved} before={before.solved} />
            <Delta label="Topics levelled up" now={now.level_ups} before={before.level_ups} />
          </div>
        </div>
        <div className="glass-card p-6">
          <div className="flex items-center gap-2 mb-4">
            <Award size={15} className="text-yellow-400" />
            <p className="text-white/40 text-xs font-mono uppercase tracking-wider">Badges</p>
          </div>
          {data.badges.length === 0 ? (
            <p className="text-white/30 text-sm">None yet. They show up when you earn them.</p>
          ) : (
            <ul className="flex flex-col gap-3">
              {data.badges.map(b => (
                <li key={b.code}>
                  <div className="text-sm text-white font-display font-600">{b.title}</div>
                  <div className="text-xs text-white/50">{b.message}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
