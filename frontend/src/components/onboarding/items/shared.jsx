import { Loader2, Send } from 'lucide-react'
import { LANGUAGES } from '../options'

export const CODE_CAP = 4000

export function CodeFrame({ language, children }) {
  const label = LANGUAGES.find(l => l.value === language)?.label || language
  return (
    <div className="rounded-xl bg-black/40 border border-white/10 overflow-hidden">
      <div className="px-4 py-1.5 border-b border-white/[0.06] text-[10px] font-mono uppercase tracking-widest text-white/30">{label}</div>
      {children}
    </div>
  )
}

export function CodeBlock({ language, children }) {
  return (
    <CodeFrame language={language}>
      <pre className="p-4 text-sky-300 text-sm font-mono leading-relaxed overflow-x-auto whitespace-pre">{children}</pre>
    </CodeFrame>
  )
}

export function ItemActions({ canSubmit, disabled, onSubmit, onSkip, label = 'Submit', busyLabel = 'Checking...' }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 mt-5">
      <button type="button" onClick={onSkip} disabled={disabled}
        className="text-sm text-white/40 hover:text-white/70 transition-colors disabled:opacity-50">
        I don't know
      </button>
      <button type="button" onClick={onSubmit} disabled={!canSubmit || disabled}
        className="btn-primary !w-auto flex items-center gap-2">
        {disabled ? <Loader2 size={16} className="animate-spin" /> : <Send size={15} />}
        {disabled ? busyLabel : label}
      </button>
    </div>
  )
}
