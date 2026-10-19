import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { onboardingAPI, getErrorMessage } from '../../utils/api'
import ProgressHeader from '../../components/onboarding/ProgressHeader'
import { STEPS } from '../../components/onboarding/options'
import WelcomeStep from './steps/WelcomeStep'
import LanguageStep from './steps/LanguageStep'
import AboutStep from './steps/AboutStep'
import LearningStep from './steps/LearningStep'
import DiagnosticStep from './steps/DiagnosticStep'
import ProfileCardStep from './steps/ProfileCardStep'

const ORDER = [...STEPS.map(s => s.key), 'done']
const VIEWS = {
  welcome: WelcomeStep,
  language: LanguageStep,
  about: AboutStep,
  learning: LearningStep,
  diagnostic: DiagnosticStep,
  card: ProfileCardStep,
}
const CAN_GO_BACK = ['language', 'about', 'learning']

function initialFor(step, state) {
  if (step === 'diagnostic') return state.diagnostic
  if (step === 'card') return state.card
  return state.answers?.[step] ?? null
}

export default function OnboardingFlow() {
  const navigate = useNavigate()
  const { updateUser } = useAuth()
  const [state, setState] = useState(null)
  const [view, setView] = useState(null)
  const [error, setError] = useState(null)

  const load = useCallback(() => {
    setError(null)
    onboardingAPI.state()
      .then(({ data }) => setState(data))
      .catch(err => setError(getErrorMessage(err, 'Could not load your onboarding.')))
  }, [])

  useEffect(load, [load])

  const step = view || state?.current_step

  useEffect(() => {
    if (step !== 'done') return
    updateUser({ onboarding_done: true })
    navigate('/practice', { replace: true })
  }, [step, updateUser, navigate])

  useEffect(() => { window.scrollTo(0, 0) }, [step])

  // After going Back and re-saving, walk forward one step rather than jump to the server's step.
  const handleSaved = (newState) => {
    setState(s => ({ ...s, ...newState }))
    const next = ORDER[ORDER.indexOf(step) + 1]
    setView(ORDER.indexOf(next) < ORDER.indexOf(newState.current_step) ? next : null)
  }

  const handleProgress = (diagnostic) => setState(s => ({ ...s, diagnostic }))

  const handleBack = () => setView(ORDER[ORDER.indexOf(step) - 1])

  // Another tab moved the server on (e.g. started the check), so drop the local Back view.
  const handleConflict = () => {
    setView(null)
    load()
  }

  const View = VIEWS[step]
  const diag = step === 'diagnostic' ? state?.diagnostic : null
  const question = diag && !diag.done && diag.item ? diag.order : null

  return (
    <div className="min-h-screen px-4 sm:px-6 py-10">
      <div className={`${step === 'diagnostic' ? 'max-w-5xl' : 'max-w-2xl'} mx-auto`}>
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="font-display font-bold text-xl text-white">ai<span className="text-brand-400">TA</span></span>
        </div>

        {error ? (
          <div className="glass-card p-6 text-center">
            <p className="text-sm text-red-300 mb-4">{error}</p>
            <button type="button" onClick={load} className="btn-secondary !w-auto">Try again</button>
          </div>
        ) : !View ? (
          <div className="flex justify-center py-20">
            <div className="w-6 h-6 border-2 border-white/20 border-t-brand-400 rounded-full animate-spin" />
          </div>
        ) : (
          <>
            <ProgressHeader step={step} question={question} remaining={diag?.remaining} />
            <div className="glass-card p-6 sm:p-8 animate-fade-in">
              <View
                key={step}
                initial={initialFor(step, state)}
                onSaved={handleSaved}
                onConflict={handleConflict}
                onProgress={handleProgress}
                onBack={CAN_GO_BACK.includes(step) ? handleBack : undefined}
              />
            </div>
          </>
        )}
      </div>
    </div>
  )
}
