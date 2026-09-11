import { useEffect, useState } from 'react'
import { BookOpen, Check, X, Search } from 'lucide-react'
import { codeEvalAPI } from '../../utils/api'

const DIFF_STYLES = {
  easy:   'text-emerald-400 bg-emerald-600/15 border-emerald-500/20',
  medium: 'text-amber-400 bg-amber-600/15 border-amber-500/20',
  hard:   'text-rose-400 bg-rose-600/15 border-rose-500/20',
}

export default function ProblemBank({ selected, onPick, onClear }) {
  const [problems, setProblems] = useState([])
  const [loading,  setLoading]  = useState(true)
  const [query,    setQuery]    = useState('')
  const [open,     setOpen]     = useState(true)

  useEffect(() => {
    codeEvalAPI.getProblems()
      .then(({ data }) => setProblems(data))
      .catch(() => setProblems([]))
      .finally(() => setLoading(false))
  }, [])

  const term = query.trim().toLowerCase()
  const shown = term
    ? problems.filter(p =>
        p.title.toLowerCase().includes(term) ||
        (p.topic || '').toLowerCase().includes(term))
    : problems

  return (
    <div className="shrink-0 border-b border-white/[0.06] bg-surface-800/50">
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center gap-2 px-4 py-2.5 text-left hover:bg-surface-700/30 transition-colors"
      >
        <div className="w-5 h-5 rounded-md bg-orange-600/20 border border-orange-500/30 flex items-center justify-center shrink-0">
          <BookOpen className="w-3 h-3 text-orange-400" />
        </div>
        <span className="text-xs font-display font-600 text-white/60">Problem Bank</span>
        <span className="ml-1 px-1.5 py-0.5 bg-white/[0.04] border border-white/[0.06] rounded text-white/40 text-xs font-mono">
          {loading ? '…' : problems.length}
        </span>
        {selected && (
          <span className="ml-1 px-1.5 py-0.5 bg-orange-600/15 border border-orange-500/20 rounded text-orange-400 text-xs font-mono truncate max-w-[180px]">
            {selected.title}
          </span>
        )}
        <span className="ml-auto text-white/20 text-xs font-mono">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="px-4 pb-3 animate-slide-up">
          <div className="flex items-center gap-2 mb-2">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3 h-3 text-white/20" />
              <input
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Filter by name or topic…"
                className="w-full bg-surface-700/40 border border-white/[0.06] rounded-lg pl-7 pr-3 py-1.5 text-xs text-white/70 placeholder-white/20 font-body focus:outline-none focus:border-orange-500/30 transition-colors"
              />
            </div>
            {selected && (
              <button
                onClick={onClear}
                className="flex items-center gap-1 px-2 py-1.5 rounded-lg border border-white/[0.06] text-white/40 hover:text-white/70 hover:border-white/20 text-xs font-mono transition-colors"
              >
                <X className="w-3 h-3" /> clear
              </button>
            )}
          </div>

          {loading ? (
            <p className="text-white/20 text-xs font-mono py-3">Loading problems…</p>
          ) : shown.length === 0 ? (
            <p className="text-white/20 text-xs font-mono py-3">No problems match.</p>
          ) : (
            <div className="max-h-40 overflow-y-auto grid grid-cols-2 gap-1.5 pr-1">
              {shown.map(p => {
                const active = selected?.id === p.id
                return (
                  <button
                    key={p.id}
                    onClick={() => onPick(p)}
                    className={`flex items-center gap-2 px-2.5 py-2 rounded-lg border text-left transition-colors ${
                      active
                        ? 'bg-orange-600/15 border-orange-500/30'
                        : 'bg-surface-700/30 border-white/[0.06] hover:border-white/20'
                    }`}
                  >
                    {active && <Check className="w-3 h-3 text-orange-400 shrink-0" />}
                    <span className="text-xs text-white/70 font-body truncate flex-1">{p.title}</span>
                    {p.difficulty && (
                      <span className={`px-1.5 py-0.5 rounded border text-[10px] font-mono shrink-0 ${
                        DIFF_STYLES[p.difficulty] || 'text-white/40 bg-white/[0.04] border-white/[0.06]'
                      }`}>
                        {p.difficulty}
                      </span>
                    )}
                    <span className="text-[10px] font-mono text-white/25 shrink-0">{p.test_count}t</span>
                  </button>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
