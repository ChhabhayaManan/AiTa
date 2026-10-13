import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import {
  AlertCircle, ArrowUp, BarChart3, BookOpen, Code2, Lightbulb,
  Loader2, Paperclip, Play, Plus, Sparkles, X,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../../hooks/useAuth'
import useChatStream from '../../hooks/useChatStream'
import ChatMessage from './ChatMessage'
import ThreadPicker from './ThreadPicker'
import { problemPrefix } from './problemContext'

const MAX_CHARS = 8000
const CONTEXT_CHARS = 3000

const LANGUAGES = [
  { value: 'c',      label: 'C'   },
  { value: 'cpp',    label: 'C++' },
  { value: 'python', label: 'Py'  },
]

const HOME_EXAMPLES = [
  { icon: BookOpen,  tone: 'text-sky-300',     text: 'What is a pointer in C?', send: true },
  { icon: BarChart3, tone: 'text-violet-300',  text: 'How many problems have I solved, and what is my accuracy?', send: true },
  { icon: Play,      tone: 'text-emerald-300', label: 'Check my code for this problem…', text: 'Check my code for this problem.\n\nProblem:\n\nMy code:\n' },
  { icon: Lightbulb, tone: 'text-amber-300',   text: "I'm stuck on my last problem — give me a hint.", send: true },
]

const PROBLEM_EXAMPLES = [
  { icon: BookOpen,  tone: 'text-sky-300',     text: 'Explain what this problem is asking, in simple words.', send: true },
  { icon: Lightbulb, tone: 'text-amber-300',   text: "I'm stuck — give me a hint to get started.", send: true },
  { icon: Play,      tone: 'text-emerald-300', label: 'Check my code — why does it fail?', text: 'Check my code — why does it fail?', withCode: true },
  { icon: BookOpen,  tone: 'text-violet-300',  text: 'Which concept does this problem test? Point me to the book section.', send: true },
]

function EmptyState({ name, hasProblem, onPick }) {
  const examples = hasProblem ? PROBLEM_EXAMPLES : HOME_EXAMPLES
  return (
    <div className="flex min-h-full flex-col items-center justify-center px-1 py-4 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl border border-brand-500/25 bg-brand-600/15">
        <Sparkles size={20} className="text-brand-300" />
      </div>
      <h3 className="font-display text-lg font-bold text-white">
        Hi{name ? ` ${name}` : ''}, what are we working on?
      </h3>
      <p className="mt-1.5 max-w-sm text-sm leading-relaxed text-white/45">
        {hasProblem
          ? "I can see the problem you're on. Ask about it, get a hint, or have me run your code against the tests."
          : 'I explain concepts from your course books, run your code against real tests, give hints, and know your progress.'}
      </p>
      <div className="mt-5 grid w-full max-w-md grid-cols-1 gap-2 sm:grid-cols-2">
        {examples.map(example => {
          const Icon = example.icon
          return (
            <button
              key={example.label || example.text}
              type="button"
              onClick={() => onPick(example)}
              className="flex items-start gap-2.5 rounded-xl border border-white/[0.08] bg-white/[0.025] px-3 py-2.5 text-left text-[13px] leading-snug text-white/70 transition-all hover:-translate-y-0.5 hover:border-brand-500/30 hover:bg-white/[0.05] hover:text-white"
            >
              <Icon size={14} className={`mt-0.5 shrink-0 ${example.tone}`} />
              <span>{example.label || example.text}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default function ChatPanel({ initialPrompt = '', problemContext = '', defaultLanguage, getCode, className = '' }) {
  const { user } = useAuth()
  const chat = useChatStream({ startFresh: Boolean(initialPrompt || problemContext) })
  const [draft, setDraft] = useState(initialPrompt)
  const [language, setLanguage] = useState(defaultLanguage || user?.preferred_language || 'c')
  const listRef = useRef(null)
  const inputRef = useRef(null)
  const stickRef = useRef(true)
  const wasStreaming = useRef(false)
  const [announcement, setAnnouncement] = useState('')

  useEffect(() => {
    const last = chat.messages[chat.messages.length - 1]
    if (wasStreaming.current && !chat.streaming && last?.role === 'assistant' && !last.live) {
      setAnnouncement(`aiTA replied: ${(last.content || '').slice(0, 200)}`)
    }
    wasStreaming.current = chat.streaming
  }, [chat.streaming, chat.messages])

  useEffect(() => {
    if (defaultLanguage) setLanguage(defaultLanguage)
  }, [defaultLanguage])

  useEffect(() => {
    const el = inputRef.current
    if (!initialPrompt || !el) return
    el.focus()
    el.setSelectionRange(el.value.length, el.value.length)
  }, [initialPrompt])

  useLayoutEffect(() => {
    const el = inputRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`
  }, [draft])

  useEffect(() => {
    const el = listRef.current
    if (el && stickRef.current) el.scrollTop = el.scrollHeight
  }, [chat.messages, chat.loading])

  const onScroll = () => {
    const el = listRef.current
    stickRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80
  }

  const fresh = chat.messages.length === 0
  const prefix = fresh ? problemPrefix(problemContext.slice(0, CONTEXT_CHARS)) : ''
  const limit = MAX_CHARS - prefix.length
  const count = draft.trim().length
  const over = count > limit
  const blocked = chat.streaming || chat.loading
  const canSend = count > 0 && !over && !blocked

  const focusEnd = () => {
    const el = inputRef.current
    if (!el) return
    el.focus()
    requestAnimationFrame(() => el.setSelectionRange(el.value.length, el.value.length))
  }

  const submit = async (text = draft) => {
    const body = text.trim()
    if (!body || body.length > limit || blocked) return
    setDraft('')
    stickRef.current = true
    const result = await chat.send(prefix + body, language)
    if (result?.restore) setDraft(current => current || body)
  }

  const insertCode = (lead) => {
    const { code, language: codeLanguage } = getCode?.() || {}
    if (!code?.trim()) {
      toast('Write some code in the editor first', { icon: '✏️' })
      return
    }
    const block = '```' + (codeLanguage || '') + '\n' + code.trim() + '\n```'
    setDraft(current => [lead || current.trim(), block].filter(Boolean).join('\n\n'))
    focusEnd()
  }

  const pickExample = (example) => {
    if (example.withCode && getCode) return insertCode(example.text)
    if (example.send) return submit(example.text)
    setDraft(example.text)
    focusEnd()
  }

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault()
      submit()
    }
  }

  const openThread = (id) => {
    stickRef.current = true
    chat.openThread(id)
  }

  const startNew = () => {
    stickRef.current = true
    chat.newChat()
    inputRef.current?.focus()
  }

  const lastIndex = chat.messages.length - 1
  const retryFor = (index) => {
    if (index !== lastIndex || blocked) return undefined
    const previous = chat.messages.slice(0, index).reverse().find(m => m.role === 'user')
    if (!previous) return undefined
    return () => {
      stickRef.current = true
      chat.send(previous.content, language)
    }
  }

  const firstName = user?.full_name?.split(' ')[0] || user?.username

  return (
    <section className={`glass-card flex min-h-0 flex-col overflow-hidden ${className}`} aria-label="Chat with aiTA">
      <div className="sr-only" aria-live="polite">{announcement}</div>
      <header className="relative flex shrink-0 items-center gap-3 border-b border-white/[0.06] px-4 py-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-900/40">
          <Sparkles size={16} className="text-white" />
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <h2 className="font-display text-[15px] font-bold leading-tight text-white">Ask aiTA</h2>
            {chat.streaming && (
              <span className="flex items-center gap-1 font-mono text-[10px] text-brand-300">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-brand-400" /> answering
              </span>
            )}
          </div>
          <ThreadPicker threads={chat.threads} currentId={chat.threadId} onSelect={openThread} />
        </div>
        <button
          type="button"
          onClick={startNew}
          disabled={fresh && !chat.threadId}
          className="flex shrink-0 items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-xs font-medium text-white/70 transition-colors hover:bg-white/[0.07] hover:text-white disabled:cursor-default disabled:opacity-40 disabled:hover:bg-white/[0.03]"
          title="Start a new chat"
        >
          <Plus size={13} /> New chat
        </button>
      </header>

      <div ref={listRef} onScroll={onScroll} className="min-h-0 flex-1 overflow-y-auto px-4 py-5">
        {chat.loading ? (
          <div className="flex h-full items-center justify-center gap-2 text-sm text-white/35">
            <Loader2 size={16} className="animate-spin" /> Loading chat…
          </div>
        ) : fresh ? (
          <EmptyState name={firstName} hasProblem={Boolean(problemContext)} onPick={pickExample} />
        ) : (
          <div className="space-y-5">
            {chat.messages.map((message, i) => (
              <ChatMessage
                key={message.id}
                message={message}
                onThumbs={chat.setThumbs}
                onRetry={retryFor(i)}
              />
            ))}
          </div>
        )}
      </div>

      <div className="shrink-0 border-t border-white/[0.06] p-3">
        {chat.error && (
          <div className="mb-2.5 flex items-start gap-2 rounded-xl border border-amber-400/20 bg-amber-500/[0.08] px-3 py-2 text-xs leading-relaxed text-amber-100/90" role="status">
            <AlertCircle size={14} className="mt-px shrink-0 text-amber-300" />
            <span className="flex-1">{chat.error}</span>
            <button type="button" onClick={chat.clearError} className="text-amber-200/60 hover:text-amber-100" aria-label="Dismiss">
              <X size={13} />
            </button>
          </div>
        )}
        <div className="rounded-2xl border border-white/10 bg-surface-700/50 transition-all focus-within:border-brand-500/50 focus-within:ring-2 focus-within:ring-brand-500/15">
          {prefix && (
            <div className="flex items-center gap-1.5 px-3.5 pt-2.5 text-[11px] text-teal-300/80">
              <Paperclip size={11} /> The current problem is attached to your first message
            </div>
          )}
          <textarea
            ref={inputRef}
            rows={1}
            value={draft}
            onChange={e => setDraft(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder={chat.streaming ? 'aiTA is answering…' : 'Ask about a concept, your code, or your progress…'}
            aria-label="Message aiTA"
            className="block max-h-[200px] w-full resize-none bg-transparent px-3.5 pb-1 pt-3 text-sm leading-relaxed text-white placeholder-white/30 focus:outline-none"
          />
          <div className="flex items-center gap-2 px-2.5 pb-2.5 pt-1">
            <div className="flex items-center rounded-lg border border-white/10 bg-black/20 p-0.5" role="group" aria-label="Language for code examples">
              {LANGUAGES.map(l => (
                <button
                  key={l.value}
                  type="button"
                  aria-pressed={language === l.value}
                  onClick={() => setLanguage(l.value)}
                  title={`Code examples in ${l.value === 'cpp' ? 'C++' : l.value === 'python' ? 'Python' : 'C'}`}
                  className={`rounded-md px-2 py-0.5 font-mono text-[11px] transition-colors ${language === l.value ? 'bg-brand-600 text-white shadow' : 'text-white/45 hover:text-white/80'}`}
                >
                  {l.label}
                </button>
              ))}
            </div>
            {getCode && (
              <button
                type="button"
                onClick={() => insertCode()}
                className="flex items-center gap-1 rounded-lg px-2 py-1 text-[11px] text-white/45 transition-colors hover:bg-white/[0.05] hover:text-white/80"
                title="Paste the code from the editor into your message"
              >
                <Code2 size={12} /> Insert my code
              </button>
            )}
            <span className={`ml-auto font-mono text-[10px] ${over ? 'text-rose-400' : count > limit * 0.9 ? 'text-amber-300' : 'text-white/25'}`}>
              {count.toLocaleString()}/{limit.toLocaleString()}
            </span>
            <button
              type="button"
              onClick={() => submit()}
              disabled={!canSend}
              aria-label="Send message"
              className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-brand-600 text-white shadow-lg shadow-brand-900/40 transition-all hover:bg-brand-500 active:scale-95 disabled:cursor-not-allowed disabled:bg-surface-600 disabled:text-white/30 disabled:shadow-none"
            >
              {chat.streaming ? <Loader2 size={15} className="animate-spin" /> : <ArrowUp size={16} />}
            </button>
          </div>
        </div>
        <p className="mt-1.5 hidden px-1 text-[10px] text-white/25 sm:block">
          Enter to send · Shift+Enter for a new line
        </p>
      </div>
    </section>
  )
}
