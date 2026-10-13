import { useState } from 'react'
import { Check, Copy } from 'lucide-react'
import toast from 'react-hot-toast'

const LANGUAGE_LABELS = {
  c: 'C', h: 'C',
  cpp: 'C++', 'c++': 'C++', cc: 'C++', cxx: 'C++', hpp: 'C++',
  python: 'Python', py: 'Python', python3: 'Python',
  sh: 'Shell', bash: 'Shell', shell: 'Shell', console: 'Shell',
  text: 'Text', txt: 'Text', plaintext: 'Text',
  json: 'JSON', java: 'Java', js: 'JavaScript', javascript: 'JavaScript',
}

const LANGUAGE_DOTS = {
  C: 'bg-sky-400',
  'C++': 'bg-indigo-400',
  Python: 'bg-yellow-400',
}

function languageLabel(language) {
  const key = (language || '').toLowerCase()
  return LANGUAGE_LABELS[key] || (key ? key.toUpperCase() : 'Code')
}

export default function CodeBlock({ code, language }) {
  const [copied, setCopied] = useState(false)
  const label = languageLabel(language)

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 1600)
    } catch {
      toast.error('Could not copy the code')
    }
  }

  return (
    <div className="my-3 overflow-hidden rounded-xl border border-indigo-400/20 bg-[#0e1224] shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
      <div className="flex items-center justify-between gap-2 border-b border-indigo-400/15 bg-indigo-500/[0.07] px-3 py-1.5">
        <span className="flex items-center gap-1.5 font-mono text-[11px] font-semibold tracking-wide text-indigo-100/80">
          <span className={`h-2 w-2 rounded-full ${LANGUAGE_DOTS[label] || 'bg-white/40'}`} />
          {label}
        </span>
        <button
          type="button"
          onClick={copy}
          className="flex items-center gap-1 rounded-md px-1.5 py-0.5 font-mono text-[11px] text-white/45 transition-colors hover:bg-white/[0.06] hover:text-white/85"
          aria-label="Copy code"
        >
          {copied ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <pre className="overflow-x-auto px-4 py-3 font-mono text-[12.5px] leading-relaxed text-slate-200">
        <code>{code}</code>
      </pre>
    </div>
  )
}
