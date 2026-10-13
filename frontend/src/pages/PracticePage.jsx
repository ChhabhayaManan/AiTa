import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  ArrowLeft, ArrowRight, Bug, CheckCircle2, Code2, HelpCircle, Lightbulb,
  ListChecks, Loader2, Play, Send, Target, XCircle,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { assessmentAPI, codeEvalAPI, feedbackAPI, getErrorMessage } from '../utils/api'
import { LANGUAGES, TEMPLATES } from '../components/code_eval/CodeEditor'
import { useAuth } from '../hooks/useAuth'
import MasteryPanel from '../components/learning/MasteryPanel'
import RichText from '../components/learning/RichText'
import { ITEM_TYPE_LABELS, misconceptionLabel, topicLabel } from '../components/learning/labels'

const TYPE_ICON = { diagnostic: ListChecks, mcq: HelpCircle, coding: Code2, debug: Bug }
const DIFF_STYLE = {
  easy: 'bg-green-500/15 text-green-400',
  medium: 'bg-yellow-500/15 text-yellow-400',
  hard: 'bg-red-500/15 text-red-400',
}

function Button({ children, onClick, disabled, variant = 'primary', icon: Icon, busy }) {
  const styles = {
    primary: 'bg-brand-600 hover:bg-brand-500 text-white',
    ghost: 'bg-surface-700 hover:bg-surface-600 text-white/80 border border-white/10',
    amber: 'bg-yellow-500/15 hover:bg-yellow-500/25 text-yellow-300 border border-yellow-500/30',
  }
  return (
    <button onClick={onClick} disabled={disabled || busy}
      className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-display font-600 transition-colors disabled:opacity-40 ${styles[variant]}`}>
      {busy ? <Loader2 size={15} className="animate-spin" /> : Icon && <Icon size={15} />}
      {children}
    </button>
  )
}

function CaseBlock({ input, expected, actual }) {
  const row = (label, value, color) => (
    <div className="flex gap-3 items-start">
      <span className="w-16 shrink-0 text-xs font-mono text-white/30 pt-1">{label}</span>
      <code className={`flex-1 px-2 py-1 rounded bg-black/40 border border-white/10 font-mono text-xs whitespace-pre-wrap ${color}`}>{value}</code>
    </div>
  )
  return (
    <div className="space-y-1.5 mt-3">
      {row('Input', input, 'text-sky-300')}
      {row('Expected', expected, 'text-green-300')}
      {row('Got', actual || '(nothing)', 'text-red-300')}
    </div>
  )
}

function Editor({ value, onChange }) {
  return (
    <textarea value={value} onChange={e => onChange(e.target.value)} spellCheck={false}
      className="w-full h-72 p-4 rounded-xl bg-black/40 border border-white/10 text-sky-100 font-mono text-sm leading-relaxed focus:outline-none focus:border-brand-500/50 resize-y" />
  )
}

function MasteryDelta({ after }) {
  if (after == null) return null
  return <span className="text-xs font-mono text-white/40">topic mastery now {Math.round(after * 100)}%</span>
}

// ── Multiple choice / diagnostic ─────────────────────────────────────────────
function McqView({ item, onGraded }) {
  const [chosen, setChosen] = useState(null)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)

  const submit = async () => {
    setBusy(true)
    try {
      const { data } = await assessmentAPI.answerMcq(item.id, chosen)
      setResult(data)
      onGraded()
    } catch (err) {
      toast.error(getErrorMessage(err, 'Could not submit the answer.'))
    } finally {
      setBusy(false)
    }
  }

  const optionStyle = i => {
    if (!result) return chosen === i ? 'border-brand-500/60 bg-brand-600/10' : 'border-white/10 hover:border-white/20'
    if (i === result.answer_index) return 'border-green-500/60 bg-green-500/10'
    if (i === result.chosen_index) return 'border-red-500/60 bg-red-500/10'
    return 'border-white/5 opacity-50'
  }

  return (
    <div>
      <RichText text={item.stem} className="text-white/85 text-[15px] mb-5" />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-5">
        {item.options.map((opt, i) => (
          <button key={i} disabled={!!result} onClick={() => setChosen(i)}
            className={`text-left px-4 py-3 rounded-xl border transition-colors ${optionStyle(i)}`}>
            <span className="text-white/30 font-mono text-xs mr-2">{String.fromCharCode(65 + i)}</span>
            <code className="font-mono text-sm text-white/85 whitespace-pre-wrap">{opt}</code>
          </button>
        ))}
      </div>
      {!result ? (
        <Button onClick={submit} disabled={chosen === null} busy={busy} icon={Send}>Check answer</Button>
      ) : (
        <div className={`p-4 rounded-xl border ${result.correct ? 'border-green-500/30 bg-green-500/5' : 'border-red-500/30 bg-red-500/5'}`}>
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <span className={`flex items-center gap-2 font-display font-600 ${result.correct ? 'text-green-400' : 'text-red-400'}`}>
              {result.correct ? <CheckCircle2 size={17} /> : <XCircle size={17} />}
              {result.correct ? 'Correct' : 'Not quite'}
            </span>
            <MasteryDelta after={result.mastery_after} />
          </div>
          {result.misconception && (
            <p className="text-sm text-yellow-300/90 mt-2">
              That answer is what you get from: <span className="font-600">{misconceptionLabel(result.misconception)}</span>
            </p>
          )}
          {result.explanation && <p className="text-sm text-white/60 mt-2">{result.explanation}</p>}
        </div>
      )}
    </div>
  )
}

// ── Debug challenge ──────────────────────────────────────────────────────────
function DebugView({ item, onGraded }) {
  const [code, setCode] = useState(item.buggy_code)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)

  const submit = async () => {
    setBusy(true)
    try {
      const { data } = await assessmentAPI.submitDebug(item.id, code)
      setResult(data)
      onGraded()
    } catch (err) {
      toast.error(getErrorMessage(err, 'Could not run your fix.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <RichText text={item.statement} className="text-white/70 text-sm mb-4" />
      <p className="text-yellow-300/80 text-sm mb-3">
        This {item.language === 'cpp' ? 'C++' : 'Python'} program has one planted bug. Find it and fix it.
      </p>
      <Editor value={code} onChange={setCode} />
      <div className="flex items-center gap-3 mt-4">
        <Button onClick={submit} busy={busy} icon={Send} disabled={result?.fixed}>Submit fix</Button>
        <Button variant="ghost" onClick={() => setCode(item.buggy_code)} disabled={busy}>Reset code</Button>
      </div>
      {result && (
        <div className={`mt-4 p-4 rounded-xl border ${result.fixed ? 'border-green-500/30 bg-green-500/5' : 'border-red-500/30 bg-red-500/5'}`}>
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <span className={`font-display font-600 ${result.fixed ? 'text-green-400' : 'text-red-400'}`}>
              {result.verdict} · {result.tests_passed}/{result.tests_total} tests
            </span>
            <MasteryDelta after={result.mastery_after} />
          </div>
          {!result.fixed && result.failing_input != null && (
            <CaseBlock input={result.failing_input} expected={result.failing_expected} actual={result.failing_actual} />
          )}
        </div>
      )}
    </div>
  )
}

// ── Coding problem ───────────────────────────────────────────────────────────
function HintLadder({ hints }) {
  const top = hints.length ? hints[hints.length - 1].level : 0
  return (
    <div className="mt-4 p-4 rounded-xl border border-yellow-500/25 bg-yellow-500/5">
      <div className="flex items-center justify-between mb-3">
        <span className="flex items-center gap-2 text-yellow-300 font-display font-600 text-sm">
          <Lightbulb size={15} /> Hints
        </span>
        <span className="flex items-center gap-1.5">
          {[1, 2, 3, 4].map(l => (
            <span key={l} title={['', 'Failing case', 'Concept', 'Steps', 'Line pointer'][l]}
              className={`w-6 h-1.5 rounded-full ${l <= top ? 'bg-yellow-400' : 'bg-white/10'}`} />
          ))}
          <span className="text-xs font-mono text-white/40 ml-1">L{top}/4</span>
        </span>
      </div>
      <div className="space-y-3">
        {hints.map((h, i) => (
          <div key={i}>
            <span className="text-xs font-mono text-yellow-400/70">
              L{h.level} · {['', 'failing case', 'concept', 'steps in words', 'line pointer'][h.level]}
            </span>
            <p className="text-sm text-white/75 whitespace-pre-wrap mt-0.5">{h.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function CodingView({ item, onGraded }) {
  const { user } = useAuth()
  const defaultLanguage = user?.preferred_language || 'c'
  const [language, setLanguage] = useState(defaultLanguage)
  const [code, setCode] = useState(TEMPLATES[defaultLanguage])
  const [runResult, setRunResult] = useState(null)
  const [report, setReport] = useState(null)
  const [hints, setHints] = useState([])
  const [busy, setBusy] = useState(null)

  const changeLanguage = lang => {
    if (Object.values(TEMPLATES).includes(code) || !code.trim()) setCode(TEMPLATES[lang])
    setLanguage(lang)
  }

  const run = async () => {
    setBusy('run')
    try {
      const { data } = await codeEvalAPI.run({ problem_id: item.id, language, code })
      setRunResult(data)
    } catch (err) {
      toast.error(getErrorMessage(err, 'Run failed.'))
    } finally {
      setBusy(null)
    }
  }

  const submit = async () => {
    setBusy('submit')
    try {
      const { data } = await codeEvalAPI.submitAndEvaluate({
        language, code, title: item.title, problem_id: item.id,
      })
      setReport(data)
      setHints(data.hint ? [data.hint] : [])
      onGraded()
    } catch (err) {
      toast.error(getErrorMessage(err, 'Evaluation failed.'))
    } finally {
      setBusy(null)
    }
  }

  const moreHelp = async () => {
    setBusy('hint')
    try {
      const { data } = await feedbackAPI.hint(item.id)
      setHints(prev => [...prev, data])
      onGraded()
    } catch (err) {
      toast.error(getErrorMessage(err, 'No hint available.'))
    } finally {
      setBusy(null)
    }
  }

  const passed = report && report.tests_total > 0 && report.tests_passed === report.tests_total
  const topLevel = hints.length ? hints[hints.length - 1].level : 0

  return (
    <div>
      <RichText text={item.statement} className="text-white/75 text-sm mb-4" />
      {item.sample_input != null && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
          <div>
            <p className="text-xs font-mono text-white/30 mb-1">Example input</p>
            <pre className="p-3 rounded-xl bg-black/40 border border-white/10 text-sky-300 text-xs font-mono whitespace-pre-wrap">{item.sample_input}</pre>
          </div>
          <div>
            <p className="text-xs font-mono text-white/30 mb-1">Example output</p>
            <pre className="p-3 rounded-xl bg-black/40 border border-white/10 text-green-300 text-xs font-mono whitespace-pre-wrap">{item.sample_output}</pre>
          </div>
        </div>
      )}
      <div className="flex items-center gap-2 mb-3">
        {LANGUAGES.map(l => (
          <button key={l.value} onClick={() => changeLanguage(l.value)}
            className={`px-3 py-1.5 rounded-lg text-xs font-display font-600 border ${language === l.value ? 'border-brand-500/60 bg-brand-600/15 text-brand-300' : 'border-white/10 text-white/40'}`}>
            {l.label}
          </button>
        ))}
      </div>
      <Editor value={code} onChange={setCode} />
      <div className="flex flex-wrap items-center gap-3 mt-4">
        <Button variant="ghost" icon={Play} onClick={run} busy={busy === 'run'} disabled={!!busy}>Run example</Button>
        <Button icon={Send} onClick={submit} busy={busy === 'submit'} disabled={!!busy || passed}>Submit</Button>
        {report && !passed && topLevel < 4 && (
          <Button variant="amber" icon={Lightbulb} onClick={moreHelp} busy={busy === 'hint'} disabled={!!busy}>
            {topLevel === 0 ? 'Get a hint' : 'Stronger hint'}
          </Button>
        )}
      </div>

      {runResult && !report && (
        <div className="mt-4 p-4 rounded-xl border border-white/10 bg-white/[0.02]">
          <span className={`font-display font-600 text-sm ${runResult.passed === runResult.total ? 'text-green-400' : 'text-red-400'}`}>
            Example: {runResult.verdict}
          </span>
          {runResult.cases.filter(c => !c.passed).map((c, i) => (
            <CaseBlock key={i} input={c.input} expected={c.expected} actual={c.actual} />
          ))}
          {(runResult.compile_output || runResult.stderr) && (
            <pre className="mt-3 text-xs text-red-300 font-mono whitespace-pre-wrap">{runResult.compile_output || runResult.stderr}</pre>
          )}
        </div>
      )}

      {report && (
        <div className={`mt-4 p-4 rounded-xl border ${passed ? 'border-green-500/30 bg-green-500/5' : 'border-red-500/30 bg-red-500/5'}`}>
          <span className={`font-display font-600 ${passed ? 'text-green-400' : 'text-red-400'}`}>
            {report.verdict} · {report.tests_passed}/{report.tests_total} tests passed
          </span>
          {report.first_failing_case && (
            <CaseBlock input={report.first_failing_case.stdin}
              expected={report.first_failing_case.expected_stdout}
              actual={report.first_failing_case.actual_stdout} />
          )}
          {report.summary && <p className="text-sm text-white/60 mt-3">{report.summary}</p>}
          {report.misconceptions?.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3">
              {report.misconceptions.map(m => (
                <span key={m} className="text-xs px-2 py-1 rounded-full bg-yellow-500/15 text-yellow-300">{misconceptionLabel(m)}</span>
              ))}
            </div>
          )}
        </div>
      )}

      {hints.length > 0 && !passed && <HintLadder hints={hints} />}
    </div>
  )
}

// ── Page ─────────────────────────────────────────────────────────────────────
export default function PracticePage() {
  const navigate = useNavigate()
  const [next, setNext] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [graded, setGraded] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    setGraded(false)
    try {
      const { data } = await assessmentAPI.next()
      setNext(data)
    } catch (err) {
      setError(getErrorMessage(err, 'Could not load the next item.'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const onGraded = () => {
    setGraded(true)
    setRefreshKey(k => k + 1)
  }

  const Icon = next ? TYPE_ICON[next.item_type] || Target : Target
  const View = next && { diagnostic: McqView, mcq: McqView, debug: DebugView, coding: CodingView }[next.item_type]

  return (
    <div className="min-h-screen bg-surface-950">
      <nav className="border-b border-white/[0.06] bg-surface-900/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center gap-4">
          <button onClick={() => navigate('/dashboard')} className="p-2 rounded-xl text-white/40 hover:text-white/80 hover:bg-surface-700/60">
            <ArrowLeft size={17} />
          </button>
          <span className="font-display font-800 text-lg text-white">Practice</span>
          <span className="text-white/30 text-xs font-mono">Assessment Agent · adapts to your measured mastery</span>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-8 space-y-8">
        {loading && <div className="glass-card h-64 flex items-center justify-center"><Loader2 className="animate-spin text-white/30" /></div>}

        {error && !loading && (
          <div className="glass-card p-8 text-center">
            <p className="text-white/60 mb-4">{error}</p>
            <Button onClick={load} icon={ArrowRight}>Try again</Button>
          </div>
        )}

        {next && !loading && (
          <div className="glass-card p-6 sm:p-8">
            <div className="flex flex-wrap items-center gap-2 mb-3">
              <span className="flex items-center gap-1.5 text-xs font-mono px-2.5 py-1 rounded-full bg-brand-600/15 text-brand-300">
                <Icon size={12} /> {ITEM_TYPE_LABELS[next.item_type]}
              </span>
              <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-surface-700 text-white/60">{topicLabel(next.topic)}</span>
              <span className={`text-xs font-mono px-2.5 py-1 rounded-full ${DIFF_STYLE[next.difficulty] || 'bg-surface-700 text-white/60'}`}>{next.difficulty}</span>
            </div>
            <div className="flex items-start gap-2 mb-6 p-3 rounded-xl bg-white/[0.02] border border-white/[0.06]">
              <Target size={14} className="text-teal-400 mt-0.5 shrink-0" />
              <p className="text-sm text-white/55"><span className="text-white/35">Why this: </span>{next.reason}</p>
            </div>

            <View key={`${next.item_type}-${next.item.id}`} item={next.item} onGraded={onGraded} />

            {graded && (
              <div className="flex justify-end mt-6 pt-5 border-t border-white/[0.06]">
                <Button onClick={load} icon={ArrowRight}>Next item</Button>
              </div>
            )}
          </div>
        )}

        <MasteryPanel refreshKey={refreshKey} />
      </div>
    </div>
  )
}
