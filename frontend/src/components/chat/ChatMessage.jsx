import { useCallback, useMemo, useRef, useState } from 'react'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  AlertCircle, ChevronDown, Clock, FileText, HeartHandshake,
  RotateCcw, ShieldAlert, Sparkles, ThumbsDown, ThumbsUp,
} from 'lucide-react'
import CodeBlock from './CodeBlock'
import ToolChips from './ToolChips'
import Citations from './Citations'
import { splitProblem } from './problemContext'

const MODERATED = {
  abuse: 'abusive language',
  slur: 'a slur',
  sexual: 'sexual content',
  self_harm: 'self-harm',
}

const NOTICES = {
  busy:  { icon: Clock,       tone: 'text-amber-300/80' },
  error: { icon: AlertCircle, tone: 'text-rose-300/80' },
}

const LIVE_LABELS = {
  thinking: 'Thinking',
  waiting: 'aiTA is still working on your last message',
  reconnecting: 'Connection dropped — fetching the saved reply',
}

const NO_CITATIONS = []

// The lookbehind keeps indexing like arr[1] or grid[0][2] in prose from becoming a ref.
const REF = /(?<![\w\])])\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\]/

const citationLabel = (c) => (c ? [c.title, c.chapter, c.section].filter(Boolean).join(' › ') : '')

function refNode(n) {
  return { type: 'element', tagName: 'sup', properties: { dataCite: n }, children: [{ type: 'text', value: String(n) }] }
}

// Turns "[2]" or "[1, 3]" in the answer text into clickable refs, leaving code alone.
function linkRefs(node, count) {
  if (!node.children || ['code', 'pre', 'a'].includes(node.tagName)) return
  const next = []
  for (const child of node.children) {
    if (child.type !== 'text') {
      linkRefs(child, count)
      next.push(child)
      continue
    }
    const parts = child.value.split(REF)
    if (parts.length === 1) {
      next.push(child)
      continue
    }
    parts.forEach((part, i) => {
      if (i % 2 === 0) {
        if (part) next.push({ type: 'text', value: part })
        return
      }
      const refs = part.split(',').map(s => Number(s.trim()))
      if (refs.every(n => n >= 1 && n <= count)) refs.forEach(n => next.push(refNode(n)))
      else next.push({ type: 'text', value: `[${part}]` })
    })
  }
  node.children = next
}

function rehypeCiteRefs({ count }) {
  return (tree) => {
    if (count) linkRefs(tree, count)
  }
}

function hastText(node) {
  if (!node) return ''
  if (node.type === 'text') return node.value
  return (node.children || []).map(hastText).join('')
}

function FencedCode({ node }) {
  const code = node?.children?.find(c => c.tagName === 'code')
  const classes = (code?.properties?.className || []).map(String)
  const language = classes.find(c => c.startsWith('language-'))?.slice('language-'.length) || ''
  return <CodeBlock code={hastText(code || node).replace(/\n$/, '')} language={language} />
}

function AnswerMarkdown({ content, citations, onCite }) {
  const count = citations?.length || 0
  const rehypePlugins = useMemo(() => [[rehypeCiteRefs, { count }]], [count])
  const components = useMemo(() => ({
    pre: ({ node }) => <FencedCode node={node} />,
    code: ({ children }) => (
      <code className="rounded-md border border-white/10 bg-white/[0.07] px-1.5 py-0.5 font-mono text-[0.85em] text-amber-200/90">{children}</code>
    ),
    sup: ({ node, children }) => {
      const n = Number(node?.properties?.dataCite)
      if (!n) return <sup>{children}</sup>
      return (
        <button
          type="button"
          onClick={() => onCite(n)}
          title={citationLabel(citations[n - 1])}
          aria-label={`Source ${n}: ${citationLabel(citations[n - 1])}`}
          className="mx-0.5 inline-flex h-[1.05rem] min-w-[1.05rem] -translate-y-[2px] items-center justify-center rounded bg-brand-500/15 px-1 align-middle font-mono text-[10px] font-bold text-brand-300 transition-colors hover:bg-brand-500/30 hover:text-white"
        >
          {n}
        </button>
      )
    },
    a: ({ href, children }) => (
      <a href={href} target="_blank" rel="noopener noreferrer" className="text-brand-300 underline decoration-brand-400/40 underline-offset-2 hover:text-brand-200">{children}</a>
    ),
    p: ({ children }) => <p className="my-2 first:mt-0 last:mb-0">{children}</p>,
    ul: ({ children }) => <ul className="my-2 list-disc space-y-1 pl-5 marker:text-brand-400/70">{children}</ul>,
    ol: ({ children }) => <ol className="my-2 list-decimal space-y-1 pl-5 marker:text-white/40">{children}</ol>,
    li: ({ children }) => <li className="pl-0.5">{children}</li>,
    h1: ({ children }) => <h3 className="mb-2 mt-4 font-display text-base font-bold text-white first:mt-0">{children}</h3>,
    h2: ({ children }) => <h3 className="mb-2 mt-4 font-display text-[15px] font-bold text-white first:mt-0">{children}</h3>,
    h3: ({ children }) => <h4 className="mb-1.5 mt-3 font-display text-sm font-semibold text-white first:mt-0">{children}</h4>,
    h4: ({ children }) => <h4 className="mb-1 mt-3 text-sm font-semibold text-white/90 first:mt-0">{children}</h4>,
    strong: ({ children }) => <strong className="font-semibold text-white">{children}</strong>,
    blockquote: ({ children }) => <blockquote className="my-2 border-l-2 border-brand-500/40 pl-3 text-white/60">{children}</blockquote>,
    hr: () => <hr className="my-4 border-white/10" />,
    table: ({ children }) => (
      <div className="my-3 overflow-x-auto rounded-lg border border-white/10">
        <table className="w-full border-collapse text-xs">{children}</table>
      </div>
    ),
    th: ({ children }) => <th className="border-b border-white/10 bg-white/[0.04] px-2.5 py-1.5 text-left font-semibold text-white/85">{children}</th>,
    td: ({ children }) => <td className="border-t border-white/[0.06] px-2.5 py-1.5 align-top">{children}</td>,
  }), [citations, onCite])

  return (
    <div className="break-words text-sm leading-relaxed text-white/80">
      <Markdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={rehypePlugins}
        components={components}
        disallowedElements={['img']}
        unwrapDisallowed
      >
        {content}
      </Markdown>
    </div>
  )
}

function UserText({ text }) {
  const parts = text.split(/```([^\n`]*)\n([\s\S]*?)```/)
  const out = []
  for (let i = 0; i < parts.length; i += 3) {
    const prose = parts[i].replace(/^\n+|\n+$/g, '')
    if (prose) out.push(<p key={i} className="whitespace-pre-wrap break-words">{prose}</p>)
    if (i + 2 < parts.length) {
      out.push(
        <pre key={`code-${i}`} className="my-2 overflow-x-auto rounded-lg border border-white/[0.06] bg-[#0d1117] px-3 py-2 font-mono text-xs leading-6 text-green-200/80">
          {parts[i + 2]}
        </pre>
      )
    }
  }
  return out
}

function ProblemContext({ text }) {
  const [open, setOpen] = useState(false)
  const title = text.split('\n')[0].replace(/\s*\(problem_id \d+\)$/, '')
  return (
    <div className="mb-2 overflow-hidden rounded-lg border border-teal-400/20 bg-teal-500/[0.07]">
      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
        className="flex w-full items-center gap-1.5 px-2.5 py-1.5 text-left text-[11px] text-teal-200/90"
      >
        <FileText size={12} className="shrink-0" />
        <span className="truncate">Problem attached · {title}</span>
        <ChevronDown size={12} className={`ml-auto shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="max-h-48 overflow-y-auto whitespace-pre-wrap border-t border-teal-400/15 px-2.5 py-2 text-[11px] leading-relaxed text-white/60">
          {text}
        </div>
      )}
    </div>
  )
}

function Avatar() {
  return (
    <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 shadow-md shadow-brand-900/40">
      <Sparkles size={13} className="text-white" />
    </div>
  )
}

function Typing({ status }) {
  return (
    <div className="flex items-center gap-2 py-1 text-xs text-white/40">
      <span className="flex gap-1">
        {[0, 150, 300].map(delay => (
          <span key={delay} className="h-1.5 w-1.5 animate-bounce rounded-full bg-brand-400/70" style={{ animationDelay: `${delay}ms` }} />
        ))}
      </span>
      {LIVE_LABELS[status] || LIVE_LABELS.thinking}…
    </div>
  )
}

function ThumbButton({ active, onClick, label, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      aria-pressed={active}
      title={label}
      className={`rounded-md p-1.5 transition-colors ${active ? 'bg-brand-500/15 text-brand-300' : 'text-white/25 hover:bg-white/[0.05] hover:text-white/70'}`}
    >
      {children}
    </button>
  )
}

export default function ChatMessage({ message, onThumbs, onRetry }) {
  const [activeCite, setActiveCite] = useState(null)
  const timer = useRef(null)

  const onCite = useCallback((n) => {
    setActiveCite(n)
    document.getElementById(`cite-${message.id}-${n}`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
    clearTimeout(timer.current)
    timer.current = setTimeout(() => setActiveCite(null), 2200)
  }, [message.id])

  if (message.role === 'user') {
    const { problem, question } = splitProblem(message.content || '')
    return (
      <div className="flex justify-end animate-fade-in">
        <div className="max-w-[85%] rounded-2xl rounded-br-md border border-brand-500/25 bg-brand-600/20 px-4 py-2.5 text-sm leading-relaxed text-white/90">
          {problem && <ProblemContext text={problem} />}
          <UserText text={question} />
        </div>
      </div>
    )
  }

  if (message.live) {
    return (
      <div className="flex gap-3">
        <Avatar />
        <div className="min-w-0 flex-1 pt-0.5">
          <ToolChips traces={message.tools} />
          {message.content
            ? <AnswerMarkdown content={message.content} citations={NO_CITATIONS} onCite={onCite} />
            : <Typing status={message.status} />}
        </div>
      </div>
    )
  }

  const notice = NOTICES[message.moderation_flag]
  const moderated = MODERATED[message.moderation_flag]

  if (notice) {
    const Icon = notice.icon
    return (
      <div className="flex gap-3 animate-fade-in">
        <Avatar />
        <div className="min-w-0 flex-1 pt-0.5">
          <ToolChips traces={message.tool_calls} />
          <div className="flex items-start gap-2.5 rounded-xl border border-dashed border-white/[0.12] bg-white/[0.025] px-3.5 py-2.5 text-sm text-white/60">
            <Icon size={15} className={`mt-0.5 shrink-0 ${notice.tone}`} />
            <div className="min-w-0">
              <p>{message.content}</p>
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className="mt-1.5 inline-flex items-center gap-1 text-xs font-medium text-brand-300 transition-colors hover:text-brand-200"
                >
                  <RotateCcw size={12} /> Try again
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="group flex gap-3 animate-fade-in">
      <Avatar />
      <div className="min-w-0 flex-1 pt-0.5">
        <ToolChips traces={message.tool_calls} />
        {moderated && (
          message.moderation_flag === 'self_harm' ? (
            <div className="mb-2 inline-flex items-center gap-1.5 rounded-full border border-rose-400/25 bg-rose-500/10 px-2.5 py-0.5 text-[11px] text-rose-200/90">
              <HeartHandshake size={11} /> Support message
            </div>
          ) : (
            <div
              className="mb-2 inline-flex items-center gap-1.5 rounded-full border border-amber-400/25 bg-amber-500/10 px-2.5 py-0.5 text-[11px] text-amber-200/90"
              title={`The safety filter flagged ${moderated} in this exchange`}
            >
              <ShieldAlert size={11} /> Safety reply
            </div>
          )
        )}
        <AnswerMarkdown content={message.content || ''} citations={message.citations || NO_CITATIONS} onCite={onCite} />
        <Citations citations={message.citations} messageId={message.id} active={activeCite} />
        {typeof message.id === 'number' && onThumbs && (
          <div className="mt-1.5 flex items-center gap-0.5 opacity-60 transition-opacity group-hover:opacity-100">
            <ThumbButton
              label="Helpful"
              active={message.thumbs === 'up'}
              onClick={() => onThumbs(message, message.thumbs === 'up' ? null : 'up')}
            >
              <ThumbsUp size={13} />
            </ThumbButton>
            <ThumbButton
              label="Not helpful"
              active={message.thumbs === 'down'}
              onClick={() => onThumbs(message, message.thumbs === 'down' ? null : 'down')}
            >
              <ThumbsDown size={13} />
            </ThumbButton>
          </div>
        )}
      </div>
    </div>
  )
}
