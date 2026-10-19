import { useState } from 'react'
import { Check } from 'lucide-react'
import { LANGUAGES } from '../../../components/onboarding/options'
import { StepTitle, StepNav, useSaveStep } from '../../../components/onboarding/StepControls'

export default function LanguageStep({ initial, onSaved, onBack, onConflict }) {
  const [language, setLanguage] = useState(initial || null)
  const { saving, save } = useSaveStep('language', onSaved, onConflict)

  return (
    <div>
      <StepTitle
        title="Pick your language"
        subtitle="The check and your practice problems will use it. You can change the default later on your profile."
      />

      <div role="radiogroup" aria-label="Programming language" className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {LANGUAGES.map(l => {
          const selected = language === l.value
          return (
            <button key={l.value} type="button" role="radio" aria-checked={selected}
              onClick={() => setLanguage(l.value)}
              className={`relative text-left p-5 rounded-2xl border transition-all ${selected ? 'border-brand-500/60 bg-brand-600/10' : 'border-white/10 bg-surface-700/30 hover:border-white/20'}`}>
              <span className={`block font-mono font-bold text-3xl mb-3 ${selected ? 'text-brand-300' : 'text-white/70'}`}>
                {l.label}
              </span>
              <span className="block text-xs text-white/45 leading-relaxed">{l.blurb}</span>
              {selected && (
                <span className="absolute top-3 right-3 w-5 h-5 rounded-full bg-brand-500 flex items-center justify-center">
                  <Check size={12} className="text-white" />
                </span>
              )}
            </button>
          )
        })}
      </div>

      <StepNav onBack={onBack} onNext={() => save({ language })} canNext={!!language} saving={saving} />
    </div>
  )
}
