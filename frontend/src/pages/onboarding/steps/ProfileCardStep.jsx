import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { Award, Compass, Lightbulb, Pencil, Rocket, Save } from 'lucide-react'
import { useAuth } from '../../../hooks/useAuth'
import { onboardingAPI, getErrorMessage } from '../../../utils/api'
import { topicLabel } from '../../../components/learning/labels'
import BandSummary, { conceptLine } from '../../../components/onboarding/BandSummary'
import {
  AboutFields, LearningFields, aboutForm, aboutPayload, aboutComplete, learningForm, learningComplete,
} from '../../../components/onboarding/BackgroundFields'

function BackgroundEditor({ card, onSaved }) {
  const { user } = useAuth()
  const [editing, setEditing] = useState(false)
  const [about, setAbout] = useState(() => aboutForm(card.preferences?.about, user))
  const [learning, setLearning] = useState(() => learningForm(card.preferences?.learning))
  const [saving, setSaving] = useState(false)

  const cancel = () => {
    setAbout(aboutForm(card.preferences?.about, user))
    setLearning(learningForm(card.preferences?.learning))
    setEditing(false)
  }

  const save = async () => {
    setSaving(true)
    try {
      const { data } = await onboardingAPI.editProfile({ about: aboutPayload(about), learning })
      onSaved(data)
      setEditing(false)
      toast.success('Background saved.')
    } catch (err) {
      toast.error(getErrorMessage(err, 'Could not save your background.'))
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="rounded-xl border border-white/[0.06] bg-surface-900/40 p-4">
      <div className="flex items-center justify-between gap-3">
        <h3 className="font-display font-semibold text-sm text-white">Your background</h3>
        {!editing && (
          <button type="button" onClick={() => setEditing(true)}
            className="flex items-center gap-1.5 text-xs text-brand-300 hover:text-brand-200">
            <Pencil size={13} /> Edit
          </button>
        )}
      </div>
      {editing ? (
        <div className="mt-4 space-y-6">
          <AboutFields form={about} onChange={setAbout} />
          <LearningFields form={learning} onChange={setLearning} />
          <div className="flex justify-end gap-2">
            <button type="button" onClick={cancel} disabled={saving}
              className="px-4 py-2.5 rounded-xl border border-white/10 text-sm text-white/50 hover:text-white/80 hover:border-white/20 transition-all disabled:opacity-50">
              Cancel
            </button>
            <button type="button" onClick={save}
              disabled={saving || !aboutComplete(about) || !learningComplete(learning)}
              className="btn-primary !w-auto flex items-center gap-1.5">
              <Save size={15} /> {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      ) : (
        <p className="text-xs text-white/40 mt-1">Your answers from the earlier steps. You can change them here or later on your Profile page.</p>
      )}
    </section>
  )
}

export default function ProfileCardStep({ initial, onConflict }) {
  const navigate = useNavigate()
  const { updateUser, refreshUser } = useAuth()
  const [card, setCard] = useState(initial)
  const [error, setError] = useState(null)
  const [attempt, setAttempt] = useState(0)
  const [starting, setStarting] = useState(false)
  const finishing = useRef(null)

  useEffect(() => {
    let cancelled = false
    setError(null)
    if (!finishing.current) finishing.current = onboardingAPI.finish()
    finishing.current
      .then(({ data }) => { if (!cancelled) setCard(data) })
      .catch(err => {
        finishing.current = null
        if (cancelled) return
        if (err?.response?.status === 409) {
          toast.error(getErrorMessage(err, 'Finish the starting check first.'))
          onConflict?.()
          return
        }
        setError(getErrorMessage(err, 'Could not build your profile.'))
      })
    return () => { cancelled = true }
  }, [attempt])

  const handleSaved = (data) => {
    setCard(data)
    refreshUser().catch(() => {})
  }

  const start = async () => {
    setStarting(true)
    try {
      await refreshUser()
    } catch { /* ignore */ }
    updateUser({ onboarding_done: true })
    navigate('/practice')
  }

  if (!card) {
    return error ? (
      <div className="text-center py-6" role="alert">
        <p className="text-sm text-red-300 mb-4">{error}</p>
        <button type="button" onClick={() => setAttempt(a => a + 1)} className="btn-secondary !w-auto">Try again</button>
      </div>
    ) : (
      <div className="flex flex-col items-center gap-3 py-10" role="status">
        <div className="w-6 h-6 border-2 border-white/20 border-t-brand-400 rounded-full animate-spin" />
        <p className="text-sm text-white/50">Building your profile...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <p className="text-xs font-mono uppercase tracking-wider text-white/40">Your starting title</p>
        <h2 className="font-display font-bold text-3xl text-white mt-1 flex items-center justify-center gap-2">
          <Award size={26} className="text-brand-400" aria-hidden="true" /> {card.title}
        </h2>
      </div>

      <BandSummary card={card} />

      <p className="flex items-center gap-2 text-sm text-white/70">
        <Lightbulb size={16} className="text-brand-400 shrink-0" aria-hidden="true" /> {conceptLine(card)}
      </p>

      <section className="rounded-xl border border-brand-500/20 bg-brand-600/10 p-4">
        <h3 className="flex items-center gap-2 font-display font-semibold text-sm text-white">
          <Compass size={16} className="text-brand-400" aria-hidden="true" />
          Start with {topicLabel(card.start_topic)}
        </h3>
        {card.start_reason && <p className="text-sm text-white/60 mt-1">{card.start_reason}</p>}
      </section>

      <BackgroundEditor card={card} onSaved={handleSaved} />

      <div className="flex justify-end">
        <button type="button" onClick={start} disabled={starting} className="btn-primary !w-auto flex items-center gap-1.5">
          <Rocket size={16} /> Start learning
        </button>
      </div>
    </div>
  )
}
