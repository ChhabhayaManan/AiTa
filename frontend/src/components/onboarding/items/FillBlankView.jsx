import { useState } from 'react'
import { CodeBlock, ItemActions } from './shared'

const BLANK_CAP = 300

export default function FillBlankView({ item, onSubmit, disabled }) {
  const [text, setText] = useState('')
  const { code_with_blank: code, blank_marker: marker = '____' } = item.body
  const parts = code.split(marker)
  const canSubmit = !!text.trim() && !disabled

  return (
    <div>
      <CodeBlock language={item.language}>
        {parts.map((part, i) => (
          <span key={i}>
            {part}
            {i < parts.length - 1 && (
              <mark className="px-1 rounded bg-amber-400/20 text-amber-200 ring-1 ring-amber-400/50">{marker}</mark>
            )}
          </span>
        ))}
      </CodeBlock>
      <label htmlFor="fill-blank" className="label mt-5">What goes in the blank?</label>
      <input id="fill-blank" type="text" value={text} onChange={e => setText(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter' && canSubmit) onSubmit({ text }) }}
        maxLength={BLANK_CAP} spellCheck={false} autoComplete="off" disabled={disabled}
        placeholder="The missing code" className="input-field font-mono" />
      <ItemActions canSubmit={!!text.trim()} disabled={disabled}
        onSubmit={() => onSubmit({ text })} onSkip={() => onSubmit({ text: '' })} />
    </div>
  )
}
