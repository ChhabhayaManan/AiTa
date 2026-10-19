import { useState } from 'react'
import RichText from '../../learning/RichText'
import CodeArea from '../../learning/CodeArea'
import { CODE_CAP, CodeFrame, ItemActions } from './shared'

export default function FindBugView({ item, onSubmit, disabled }) {
  const code = item.body.code
  const lines = code.replace(/\n$/, '').split('\n')
  const [line, setLine] = useState(null)
  const [fix, setFix] = useState(code)

  const submit = () => onSubmit({ line, fix_code: fix === code ? '' : fix })

  return (
    <div>
      {item.body.statement && (
        <RichText text={item.body.statement} className="text-white/85 text-[15px] mb-4" />
      )}
      <p className="label">Click the line with the bug</p>
      <CodeFrame language={item.language}>
        <div className="py-2 overflow-x-auto">
          {lines.map((text, i) => {
            const n = i + 1
            const selected = line === n
            return (
              <button key={n} type="button" aria-pressed={selected}
                aria-label={`Line ${n}: ${text.trim() || 'blank'}`}
                onClick={() => setLine(n)} disabled={disabled}
                className={`w-full min-w-max flex text-left font-mono text-sm leading-6 border-l-2 transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-brand-400/70
                  ${selected ? 'border-amber-400 bg-amber-400/10 text-amber-100' : 'border-transparent text-sky-300 hover:bg-white/[0.04]'}`}>
                <span className={`w-10 shrink-0 pr-3 text-right select-none ${selected ? 'text-amber-300' : 'text-white/25'}`}>{n}</span>
                <span className="pr-4 whitespace-pre">{text || ' '}</span>
              </button>
            )
          })}
        </div>
      </CodeFrame>

      {line && (
        <div className="mt-5 motion-safe:animate-fade-in">
          <p className="label">Fix it (optional)</p>
          <p className="text-xs text-white/40 mb-2">Edit the code below. The line alone earns half the credit.</p>
          <CodeArea value={fix} onChange={setFix} disabled={disabled} maxLength={CODE_CAP}
            height="h-64" label="Fixed code" />
        </div>
      )}

      <ItemActions canSubmit={line !== null} disabled={disabled}
        onSubmit={submit} onSkip={() => onSubmit({})} />
    </div>
  )
}
