import { useState } from 'react'
import { LearningFields, learningForm, learningComplete } from '../../../components/onboarding/BackgroundFields'
import { StepTitle, StepNav, useSaveStep } from '../../../components/onboarding/StepControls'

export default function LearningStep({ initial, onSaved, onBack, onConflict }) {
  const [form, setForm] = useState(() => learningForm(initial))
  const { saving, save } = useSaveStep('learning', onSaved, onConflict)

  return (
    <div>
      <StepTitle title="How you learn" subtitle="aiTA's hints, feedback and chat will follow these." />
      <LearningFields form={form} onChange={setForm} />
      <StepNav onBack={onBack} onNext={() => save(form)} saving={saving} canNext={learningComplete(form)}
        nextLabel="Continue to the check" />
    </div>
  )
}
