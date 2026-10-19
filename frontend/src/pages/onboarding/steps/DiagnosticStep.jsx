import { useEffect, useRef, useState } from 'react'
import toast from 'react-hot-toast'
import { Loader2, Play } from 'lucide-react'
import { onboardingAPI, getErrorMessage } from '../../../utils/api'
import { StepTitle } from '../../../components/onboarding/StepControls'
import { topicLabel } from '../../../components/learning/labels'
import TopicMap from '../../../components/onboarding/TopicMap'
import RevealPanel from '../../../components/onboarding/RevealPanel'
import PredictOutputView from '../../../components/onboarding/items/PredictOutputView'
import FindBugView from '../../../components/onboarding/items/FindBugView'
import FillBlankView from '../../../components/onboarding/items/FillBlankView'
import WriteCodeView from '../../../components/onboarding/items/WriteCodeView'
import TheoryView from '../../../components/onboarding/items/TheoryView'

const VIEWS = {
  predict_output: PredictOutputView,
  find_bug: FindBugView,
  fill_blank: FillBlankView,
  write_code: WriteCodeView,
  theory: TheoryView,
}

const KIND_LABEL = {
  predict_output: 'Predict the output',
  find_bug: 'Find the bug',
  fill_blank: 'Fill the blank',
  write_code: 'Write the code',
  theory: 'Explain in words',
}

const MS_CAP = 3_600_000
const THEORY_COUNT = 3

export default function DiagnosticStep({ initial, onSaved, onConflict, onProgress, api = onboardingAPI, intro }) {
  const [started, setStarted] = useState(!!initial)
  const [diag, setDiag] = useState(null)
  const [map, setMap] = useState(initial?.topic_map || {})
  const [reveal, setReveal] = useState(null)
  const [busy, setBusy] = useState(false)
  const [loadError, setLoadError] = useState(null)
  const inFlight = useRef(false)
  const shownAt = useRef(0)
  const upcoming = useRef(null)
  const moveFocus = useRef(false)
  const headingRef = useRef(null)

  useEffect(() => {
    if (!moveFocus.current || reveal || !diag) return
    moveFocus.current = false
    window.scrollTo(0, 0)
    headingRef.current?.focus({ preventScroll: true })
  }, [diag, reveal])

  const show = (d) => {
    setMap(d.topic_map)
    onProgress?.(d)
    if (d.done || !d.item) {
      onSaved({ current_step: 'card', diagnostic: d, card: null })
      return
    }
    shownAt.current = Date.now()
    setDiag(d)
  }

  const run = async (task) => {
    if (inFlight.current) return
    inFlight.current = true
    setBusy(true)
    try {
      await task()
    } finally {
      inFlight.current = false
      setBusy(false)
    }
  }

  const fetchNext = async () => {
    setLoadError(null)
    try {
      const { data } = await api.next()
      show(data)
    } catch (err) {
      if (err?.response?.status === 409) {
        toast.error(getErrorMessage(err, 'Finish the earlier steps first.'))
        onConflict?.()
        return
      }
      setLoadError(getErrorMessage(err, 'Could not load the next question.'))
    }
  }

  useEffect(() => {
    if (started) run(fetchNext)
  }, [started])

  const submit = (answer) => run(async () => {
    const item = diag.item
    const ms = Math.min(MS_CAP, Math.max(0, Date.now() - shownAt.current))
    try {
      const { data } = await api.answer(item.id, answer, ms)
      if (data.saved_only) {
        toast.success('Saved — reviewed at the end of this block')
        moveFocus.current = true
        show(data.next)
      } else if (item.kind === 'theory') {
        upcoming.current = data.next
        setReveal({ kind: 'theory', items: data.theory_reveals, expectedCount: THEORY_COUNT })
      } else if (data.reveal) {
        upcoming.current = data.next
        setReveal({ kind: item.kind, ...data.reveal, score: data.score })
      } else {
        moveFocus.current = true
        show(data.next)
      }
    } catch (err) {
      const status = err?.response?.status
      if (status === 409) {
        toast.error('That question is out of date. Loading the current one.')
        await fetchNext()
      } else {
        toast.error(getErrorMessage(err, 'Could not submit your answer. Please try again.'))
      }
    }
  })

  const handleContinue = () => {
    setReveal(null)
    moveFocus.current = true
    show(upcoming.current)
  }

  if (!started) {
    return (
      <div>
        {intro || (
          <>
            <StepTitle title="A short check"
              subtitle="Up to 12 questions in your language, about 5 minutes. It starts easy and adapts to your answers." />
            <ul className="space-y-2 text-sm text-white/60 mb-8 list-disc pl-5">
              <li>Code questions: predict the output, find a bug, fill a blank.</li>
              <li>After each one you'll see the right answer and why.</li>
              <li>The last few are short written answers, reviewed together at the end.</li>
              <li>Not sure? Press "I don't know" — it simply counts as not known yet.</li>
            </ul>
          </>
        )}
        <button type="button" onClick={() => setStarted(true)} className="btn-primary !w-auto flex items-center gap-2">
          <Play size={16} /> Start the check
        </button>
      </div>
    )
  }

  if (loadError) {
    return (
      <div className="text-center py-6">
        <p className="text-sm text-red-300 mb-4">{loadError}</p>
        <button type="button" onClick={() => run(fetchNext)} disabled={busy} className="btn-secondary !w-auto">Try again</button>
      </div>
    )
  }

  if (!diag) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 size={24} className="animate-spin text-brand-400" aria-label="Loading the question" />
      </div>
    )
  }

  const { item } = diag
  const View = VIEWS[item.kind]

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      <aside className="lg:order-2 lg:w-72 shrink-0">
        <TopicMap states={map} />
      </aside>

      <div className="flex-1 min-w-0 lg:order-1">
        {reveal ? (
          <RevealPanel reveal={reveal} onContinue={handleContinue} />
        ) : (
          <div key={item.id} className="motion-safe:animate-fade-in">
            <div className="flex flex-wrap items-center gap-2 mb-4">
              <h2 ref={headingRef} tabIndex={-1} className="font-display font-bold text-lg text-white mr-1 focus:outline-none">
                {KIND_LABEL[item.kind] || 'Question'}
              </h2>
              {diag.phase === 'warmup' && (
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300">warm-up</span>
              )}
              <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-surface-700 text-white/60">{topicLabel(item.topic)}</span>
            </div>
            {item.kind === 'theory' && (
              <p className="text-xs text-white/45 mb-4">
                Written answers are saved one by one and reviewed together after the last one.
              </p>
            )}
            {View ? (
              <View item={item} onSubmit={submit} disabled={busy} />
            ) : (
              <div>
                <p className="text-sm text-white/60 mb-4">This question can't be shown here.</p>
                <button type="button" onClick={() => run(fetchNext)} disabled={busy} className="btn-secondary !w-auto">Continue</button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
