import { useState } from 'react'
import { CODE_CAP, CodeBlock, ItemActions } from './shared'

export default function PredictOutputView({ item, onSubmit, disabled }) {
  const [text, setText] = useState('')

  return (
    <div>
      <CodeBlock language={item.language}>{item.body.code}</CodeBlock>
      <label htmlFor="predict-output" className="label mt-5">What does this print?</label>
      <textarea id="predict-output" value={text} onChange={e => setText(e.target.value)}
        rows={4} maxLength={CODE_CAP} spellCheck={false} disabled={disabled}
        placeholder="Type the exact output"
        className="input-field font-mono resize-y" />
      <ItemActions canSubmit={!!text.trim()} disabled={disabled}
        onSubmit={() => onSubmit({ text })} onSkip={() => onSubmit({ text: '' })} />
    </div>
  )
}
