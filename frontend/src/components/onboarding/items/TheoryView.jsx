import { useState } from 'react'
import RichText from '../../learning/RichText'
import { ItemActions } from './shared'

const THEORY_CAP = 2000

export default function TheoryView({ item, onSubmit, disabled }) {
  const [text, setText] = useState('')

  return (
    <div>
      <RichText text={item.body.question} className="text-white/85 text-[15px] mb-4" />
      <label htmlFor="theory-answer" className="label">Your answer, in 1–3 sentences</label>
      <textarea id="theory-answer" value={text} onChange={e => setText(e.target.value)}
        rows={5} maxLength={THEORY_CAP} disabled={disabled}
        aria-describedby="theory-count" className="input-field resize-y" />
      <p id="theory-count" className={`mt-1.5 text-right text-xs font-mono ${text.length >= THEORY_CAP ? 'text-amber-300' : 'text-white/30'}`}>
        {text.length} / {THEORY_CAP}
      </p>
      <ItemActions canSubmit={!!text.trim()} disabled={disabled} label="Save answer" busyLabel="Saving..."
        onSubmit={() => onSubmit({ text })} onSkip={() => onSubmit({ text: '' })} />
    </div>
  )
}
