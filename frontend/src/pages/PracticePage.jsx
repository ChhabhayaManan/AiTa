import { useCallback, useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, Bug, ChevronDown, Code2, Flag, HelpCircle, ListChecks, RefreshCw, Target } from 'lucide-react'
import toast from 'react-hot-toast'
import { assessmentAPI, getErrorMessage, practiceSessionAPI, profileAPI } from '../utils/api'
import { BAND_STYLE, ITEM_TYPE_LABELS, topicLabel } from '../components/learning/labels'
import AppShell from '../components/ui/AppShell'
import Button from '../components/ui/Button'
import Chip from '../components/ui/Chip'
import Skeleton from '../components/ui/Skeleton'
import BusyNote from '../components/ui/BusyNote'
import LevelBar from '../components/ui/LevelBar'
import TopicLevelsTile from '../components/dashboard/TopicLevelsTile'
import McqView from '../components/practice/McqView'
import DebugView from '../components/practice/DebugView'
import CodingView from '../components/practice/CodingView'

const TYPE = {
  diagnostic: { icon: ListChecks, tone: 'aqua' },
  mcq: { icon: HelpCircle, tone: 'aqua' },
  coding: { icon: Code2, tone: 'mint' },
  debug: { icon: Bug, tone: 'pink' },
}
const DIFF_TONE = { easy: 'mint', medium: 'sun', hard: 'coral' }
const VIEWS = { diagnostic: McqView, mcq: McqView, debug: DebugView, coding: CodingView }

const LOADING_STEPS = [
  { after: 0, text: 'Picking your next question…' },
  { after: 6, text: 'Writing a fresh problem for you…' },
  { after: 30, text: 'Still writing. New problems can take up to a minute…' },
]

function ItemHeader({ next, topic }) {
  const type = TYPE[next.item_type] || { icon: Target, tone: 'neutral' }
  const band = topic && topic.evidence_count > 0 ? topic.band : 'unseen'
  return (
    <section className="tile flex flex-col gap-4 p-5 sm:p-6 md:flex-row md:items-center md:justify-between">
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <Chip tone={type.tone} icon={type.icon}>{ITEM_TYPE_LABELS[next.item_type] || next.item_type}</Chip>
          <Chip>{topicLabel(next.topic)}</Chip>
          {next.difficulty && <Chip tone={DIFF_TONE[next.difficulty] || 'neutral'}>{next.difficulty}</Chip>}
        </div>
        {next.reason && (
          <p className="mt-3 max-w-[75ch] text-sm leading-relaxed text-ink-muted">
            <span className="font-medium text-ink">Why this: </span>{next.reason}
          </p>
        )}
      </div>
      {topic && (
        <div className="w-full shrink-0 rounded-2xl border border-line bg-tile-2 px-4 py-3 md:w-56">
          <div className="flex items-baseline justify-between gap-2 text-xs">
            <span className="text-ink-subtle">Topic level</span>
            <span className={BAND_STYLE[band].text}>
              {BAND_STYLE[band].label}
              {topic.evidence_count > 0 && <span className="ml-1.5 font-mono text-ink">{Math.round(topic.mastery * 100)}%</span>}
            </span>
          </div>
          <LevelBar value={topic.evidence_count > 0 ? topic.mastery : 0} band={band} className="mt-2" />
        </div>
      )}
    </section>
  )
}

function LoadingState() {
  return (
    <div className="flex flex-col gap-4" aria-busy="true">
      <div className="tile space-y-3 p-6">
        <div className="flex gap-2">
          <Skeleton className="h-6 w-32 rounded-full" />
          <Skeleton className="h-6 w-24 rounded-full" />
          <Skeleton className="h-6 w-16 rounded-full" />
        </div>
        <Skeleton className="h-4 w-3/5" />
      </div>
      <BusyNote active steps={LOADING_STEPS} />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[5fr_7fr]">
        <div className="tile space-y-3 p-6">
          {[90, 75, 82, 40].map(w => <Skeleton key={w} className="h-3.5" style={{ width: `${w}%` }} />)}
        </div>
        <div className="tile h-[380px] p-6"><Skeleton className="h-full w-full rounded-2xl" /></div>
      </div>
    </div>
  )
}

function AllLevels({ topics, current }) {
  const [open, setOpen] = useState(false)
  if (!topics) return null
  return (
    <section className="flex flex-col gap-3">
      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
        className="flex h-11 items-center gap-2 self-start rounded-full border border-line-strong px-4 text-sm font-medium text-ink-muted hover:bg-white/[0.04] hover:text-ink"
      >
        {open ? 'Hide' : 'Show'} all topic levels
        <ChevronDown size={15} className={`transition-transform duration-300 ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="motion-safe:animate-rise">
          <TopicLevelsTile topics={topics} highlight={current} />
        </div>
      )}
    </section>
  )
}

export default function PracticePage() {
  const navigate = useNavigate()
  const [next, setNext] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [graded, setGraded] = useState(false)
  const [topics, setTopics] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)
  const [session, setSession] = useState(null)
  const [finishing, setFinishing] = useState(false)
  const nextRef = useRef(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    setGraded(false)
    window.scrollTo({ top: 0 })
    try {
      const { data } = await assessmentAPI.next()
      setNext(data)
      practiceSessionAPI.current().then(({ data }) => setSession(data)).catch(() => {})
    } catch (err) {
      if (err?.response?.status === 428) {
        navigate('/language-check', { replace: true })
        return
      }
      setError(getErrorMessage(err, "Couldn't load your next question."))
    } finally {
      setLoading(false)
    }
  }, [navigate])

  useEffect(() => { load() }, [load])

  useEffect(() => {
    profileAPI.getMastery().then(({ data }) => setTopics(data.topics)).catch(() => {})
    practiceSessionAPI.current().then(({ data }) => setSession(data)).catch(() => {})
  }, [refreshKey])

  const finish = async () => {
    setFinishing(true)
    try {
      await practiceSessionAPI.finish(session.id)
      navigate(`/practice/session/${session.id}`)
    } catch (err) {
      toast.error(getErrorMessage(err, "Couldn't finish the session. Try again in a moment."))
      setFinishing(false)
      setRefreshKey(k => k + 1)
    }
  }

  const onGraded = () => {
    setGraded(true)
    setRefreshKey(k => k + 1)
  }

  useEffect(() => {
    if (graded) nextRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  }, [graded])

  const View = next && VIEWS[next.item_type]
  const topic = next && topics?.find(t => t.topic === next.topic)

  return (
    <AppShell title="Practice">
      <div className="mx-auto flex max-w-[1320px] flex-col gap-5">
        <header className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="eyebrow">Practice</p>
            <h1 className="mt-2 text-2xl font-semibold tracking-tight text-ink md:text-[32px]">One question at a time</h1>
          </div>
          <div className="flex flex-col items-start gap-3 sm:items-end">
            <p className="max-w-[46ch] text-sm text-ink-subtle">Each answer is graded, moves your topic level, and picks what comes next.</p>
            {session?.id && (
              <div className="flex flex-wrap items-center gap-3">
                <span className="font-mono text-xs text-ink-muted">{session.graded_count} answered this session</span>
                <Button size="sm" variant="secondary" icon={Flag} busy={finishing} onClick={finish}>Finish session</Button>
              </div>
            )}
          </div>
        </header>

        {loading && <LoadingState />}

        {error && !loading && (
          <section className="tile flex flex-col items-start gap-4 p-6">
            <p className="text-sm text-ink-muted">{error} Check your connection, then try again.</p>
            <Button icon={RefreshCw} onClick={load}>Try again</Button>
          </section>
        )}

        {next && !loading && View && (
          <div className={`flex w-full flex-col gap-5 ${next.item_type === 'mcq' || next.item_type === 'diagnostic' ? 'mx-auto max-w-3xl' : ''}`}>
            <ItemHeader next={next} topic={topic} />
            <div className="motion-safe:animate-rise">
              <View key={`${next.item_type}-${next.item.id}`} item={next.item} onGraded={onGraded} />
            </div>
            {graded && (
              <div ref={nextRef} className="flex flex-col items-start justify-between gap-3 rounded-tile border border-line-strong bg-tile-2 p-5 motion-safe:animate-rise sm:flex-row sm:items-center">
                <p className="text-sm text-ink-muted">Graded. Your topic level is updated.</p>
                <Button size="lg" iconRight={ArrowRight} onClick={load}>Next question</Button>
              </div>
            )}
          </div>
        )}

        {!loading && <AllLevels topics={topics} current={next?.topic} />}
      </div>
    </AppShell>
  )
}
