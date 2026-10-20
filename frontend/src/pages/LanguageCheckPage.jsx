import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { ArrowRight, Loader2, Sparkles } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { recheckAPI, getErrorMessage } from '../utils/api'
import { StepTitle } from '../components/onboarding/StepControls'
import BandSummary from '../components/onboarding/BandSummary'
import DiagnosticStep from './onboarding/steps/DiagnosticStep'

const LABELS = { c: 'C', cpp: 'C++', python: 'Python' }

export default function LanguageCheckPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const language = LABELS[user?.preferred_language] || 'your new language'
  const [result, setResult] = useState(null)
  const [finishing, setFinishing] = useState(false)
  const [finishError, setFinishError] = useState(null)

  const finish = async () => {
    setFinishing(true)
    setFinishError(null)
    try {
      const { data } = await recheckAPI.finish()
      setResult(data)
    } catch (err) {
      setFinishError(getErrorMessage(err, 'Could not save your check.'))
    } finally {
      setFinishing(false)
    }
  }

  // No open check (already finished, or never switched): Practice is free to open.
  const onConflict = () => {
    toast('No language check is waiting for you.')
    navigate('/practice', { replace: true })
  }

  const intro = (
    <>
      <StepTitle title={`A short check in ${language}`}
        subtitle="Up to 9 code questions, about 4 minutes. It starts easy and adapts to your answers." />
      <ul className="space-y-2 text-sm text-white/60 mb-8 list-disc pl-5">
        <li>Your progress in each language is kept separately, so we need to see where you stand in {language}.</li>
        <li>How well you explain ideas carries over, so there are no written answers this time.</li>
        <li>Not sure? Press "I don't know" — it simply counts as not known yet.</li>
      </ul>
    </>
  )

  let body
  if (result) {
    body = (
      <div>
        <StepTitle title={`You're set up in ${language}`} subtitle={result.title} />
        <div className="mb-8"><BandSummary card={{ bands: result.bands }} /></div>
        <button type="button" onClick={() => navigate('/practice', { replace: true })}
          className="btn-primary !w-auto flex items-center gap-2">
          Go to Practice <ArrowRight size={16} />
        </button>
      </div>
    )
  } else if (finishing || finishError) {
    body = finishError ? (
      <div className="text-center py-6">
        <p className="text-sm text-red-300 mb-4">{finishError}</p>
        <button type="button" onClick={finish} className="btn-secondary !w-auto">Try again</button>
      </div>
    ) : (
      <div className="flex justify-center py-16">
        <Loader2 size={24} className="animate-spin text-brand-400" aria-label="Saving your check" />
      </div>
    )
  } else {
    body = <DiagnosticStep api={recheckAPI} intro={intro} written={false} onSaved={finish} onConflict={onConflict} />
  }

  return (
    <div className="min-h-screen px-4 sm:px-6 py-10">
      <div className={`${result ? 'max-w-2xl' : 'max-w-5xl'} mx-auto`}>
        <div className="flex items-center justify-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="font-display font-bold text-xl text-white">ai<span className="text-brand-400">TA</span></span>
        </div>
        <div className="glass-card p-6 sm:p-8 animate-fade-in">{body}</div>
      </div>
    </div>
  )
}
