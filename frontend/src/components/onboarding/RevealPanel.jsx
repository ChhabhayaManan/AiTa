import { useEffect, useRef } from 'react'
import { ArrowRight, Check, CheckCircle2, Clock, MinusCircle, PauseCircle, X, XCircle } from 'lucide-react'
import { topicLabel } from '../learning/labels'

const EXPECTED_LABEL = {
  predict_output: 'The program prints',
  find_bug: 'A fixed version',
  fill_blank: 'The blank is',
  write_code: 'A reference solution',
}

const VERDICTS = {
  skipped: { Icon: PauseCircle,  text: "Couldn't run this one, moving on", color: 'text-white/70' },
  correct: { Icon: CheckCircle2, text: 'Correct',      color: 'text-emerald-300' },
  partial: { Icon: MinusCircle,  text: 'Partly right', color: 'text-sky-300' },
  wrong:   { Icon: XCircle,      text: 'Not quite',    color: 'text-amber-300' },
}

function verdictOf(score, correct) {
  if (score == null) return correct == null ? 'skipped' : correct ? 'correct' : 'wrong'
  if (score >= 1) return 'correct'
  return score > 0 ? 'partial' : 'wrong'
}

function Verdict({ score, correct }) {
  const { Icon, text, color } = VERDICTS[verdictOf(score, correct)]
  return <p className={`flex items-center gap-2 font-display font-bold ${color}`}><Icon size={20} /> {text}</p>
}

function Pre({ children }) {
  return <pre className="p-3 rounded-xl bg-black/40 border border-white/10 text-green-300 text-sm font-mono overflow-x-auto whitespace-pre">{children}</pre>
}

function CodeReveal({ reveal }) {
  if (reveal.score == null && reveal.correct == null) {
    return (
      <>
        <Verdict score={null} correct={null} />
        <p className="text-sm text-white/50 mt-2">The code runner is busy right now, so this question isn't counted.</p>
      </>
    )
  }
  const bugLineInWhy = reveal.why?.includes(`line ${reveal.bug_line}`)
  return (
    <>
      <Verdict score={reveal.score} correct={reveal.correct} />
      {reveal.why && <p className="text-sm text-white/70 mt-2 leading-relaxed">{reveal.why}</p>}
      {reveal.kind === 'find_bug' && reveal.bug_line != null && !bugLineInWhy && (
        <p className="text-sm text-white/60 mt-3">The bug is on <span className="font-mono text-amber-300">line {reveal.bug_line}</span>.</p>
      )}
      {reveal.kind === 'write_code' && reveal.total > 0 && (
        <p className="text-sm text-white/60 mt-3 font-mono">{reveal.passed} / {reveal.total} tests passed</p>
      )}
      {reveal.expected != null && reveal.expected !== '' && (
        <div className="mt-4">
          <p className="label">{EXPECTED_LABEL[reveal.kind] || 'Expected'}</p>
          <Pre>{reveal.expected}</Pre>
        </div>
      )}
    </>
  )
}

function TheoryItem({ entry }) {
  const r = entry.reveal || {}
  return (
    <li className="rounded-xl border border-white/[0.08] bg-surface-700/20 p-4">
      <p className="text-[11px] font-mono text-white/35 mb-1">{topicLabel(entry.topic)}</p>
      {entry.question && <p className="text-sm text-white/80 mb-3">{entry.question}</p>}
      {entry.score == null && r.correct == null
        ? <p className="text-sm text-white/60">This answer couldn't be reviewed, so it isn't counted.</p>
        : <Verdict score={entry.score} correct={r.correct ?? false} />}
      {entry.feedback && <p className="text-sm text-white/65 mt-2">{entry.feedback}</p>}
      {Array.isArray(r.rubric) && (
        <ul className="mt-3 space-y-1.5" aria-label="Key points">
          {r.rubric.map((point, i) => {
            const hit = !!r.points_present?.[i]
            return (
              <li key={i} className="flex items-start gap-2 text-sm">
                {hit ? <Check size={15} className="mt-0.5 shrink-0 text-emerald-400" aria-label="Covered" />
                  : <X size={15} className="mt-0.5 shrink-0 text-white/30" aria-label="Missing" />}
                <span className={hit ? 'text-white/80' : 'text-white/45'}>{point}</span>
              </li>
            )
          })}
        </ul>
      )}
      {r.model_answer && (
        <div className="mt-3">
          <p className="label">A model answer</p>
          <p className="text-sm text-white/70 leading-relaxed">{r.model_answer}</p>
        </div>
      )}
    </li>
  )
}

function TheoryReveal({ reveal }) {
  const items = reveal.items || []
  if (!items.length) {
    return (
      <p className="flex items-start gap-2 text-sm text-white/70">
        <Clock size={18} className="shrink-0 text-brand-300" />
        Your answers are saved and will be reviewed shortly.
      </p>
    )
  }
  return (
    <>
      <p className="font-display font-bold text-white mb-3">Your written answers</p>
      <ul className="space-y-3">
        {items.map(entry => <TheoryItem key={entry.item_id} entry={entry} />)}
      </ul>
      {reveal.expectedCount > items.length && (
        <p className="text-xs text-white/45 mt-3">The rest are saved and will be reviewed shortly.</p>
      )}
    </>
  )
}

export default function RevealPanel({ reveal, onContinue }) {
  const continueRef = useRef(null)
  useEffect(() => { continueRef.current?.focus() }, [reveal])

  return (
    <div className="motion-safe:animate-fade-in" aria-live="polite">
      <div className="rounded-xl border border-white/[0.08] bg-surface-900/40 p-5">
        {reveal.kind === 'theory' ? <TheoryReveal reveal={reveal} /> : <CodeReveal reveal={reveal} />}
      </div>
      <div className="flex justify-end mt-5">
        <button ref={continueRef} type="button" onClick={onContinue} className="btn-primary !w-auto flex items-center gap-2">
          Continue <ArrowRight size={16} />
        </button>
      </div>
    </div>
  )
}
