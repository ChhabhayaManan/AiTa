import { useState } from 'react'
import toast from 'react-hot-toast'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { onboardingAPI, getErrorMessage } from '../../utils/api'

export function useSaveStep(step, onSaved, onConflict) {
  const [saving, setSaving] = useState(false)
  const save = async (data) => {
    setSaving(true)
    try {
      const { data: state } = await onboardingAPI.saveStep(step, data)
      onSaved(state)
    } catch (err) {
      toast.error(getErrorMessage(err, 'Could not save this step. Please try again.'))
      if (err?.response?.status === 409) onConflict?.()
    } finally {
      setSaving(false)
    }
  }
  return { saving, save }
}

export function StepTitle({ title, subtitle }) {
  return (
    <div className="mb-6">
      <h2 className="font-display font-bold text-xl text-white">{title}</h2>
      {subtitle && <p className="text-sm text-white/45 mt-1 leading-relaxed">{subtitle}</p>}
    </div>
  )
}

export function ChoiceGroup({ label, options, value, onChange, columns = 2, clearable = false }) {
  const cols = { 2: 'grid-cols-2', 3: 'grid-cols-2 sm:grid-cols-3', 4: 'grid-cols-2 sm:grid-cols-4', 5: 'grid-cols-2 sm:grid-cols-5', 6: 'grid-cols-3 sm:grid-cols-6' }
  return (
    <div role="radiogroup" aria-label={label}>
      <span className="label">{label}</span>
      <div className={`grid gap-2 ${cols[columns] || cols[2]}`}>
        {options.map(o => {
          const selected = value === o.value
          return (
            <button key={o.value} type="button" role="radio" aria-checked={selected}
              onClick={() => onChange(selected && clearable ? null : o.value)}
              className={`py-2.5 px-3 rounded-xl border text-sm font-display font-semibold transition-all ${selected ? 'border-brand-500/60 bg-brand-600/10 text-brand-300' : 'border-white/10 bg-surface-700/30 text-white/50 hover:border-white/20'}`}>
              {o.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export function StepNav({ onBack, onNext, canNext = true, saving, nextLabel = 'Next' }) {
  return (
    <div className="flex items-center justify-between gap-3 mt-8">
      {onBack ? (
        <button type="button" onClick={onBack} disabled={saving}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-white/10 text-sm text-white/50 hover:text-white/80 hover:border-white/20 transition-all disabled:opacity-50">
          <ChevronLeft size={16} /> Back
        </button>
      ) : <span />}
      <button type="button" onClick={onNext} disabled={!canNext || saving}
        className="btn-primary !w-auto flex items-center gap-1.5">
        {saving ? 'Saving...' : nextLabel} {!saving && <ChevronRight size={16} />}
      </button>
    </div>
  )
}
