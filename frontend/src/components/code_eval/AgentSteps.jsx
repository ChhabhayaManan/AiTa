import { CheckCircle2, Loader2, XCircle } from 'lucide-react'

// The backend runs the whole graph in one synchronous call, so there is no live
// progress to stream. These are the real stages, shown as pending — never ticked
// off, because we genuinely do not know which one is running.
const STAGES = [
  'Finding the problem',
  'Checking the code',
  'Getting test cases',
  'Running it in the sandbox',
  'Writing the feedback',
  'Working out the score',
]

export default function AgentSteps({ steps = [], evaluating }) {
  if (steps.length === 0 && !evaluating) return null

  const realSteps = steps.map(step =>
    typeof step === 'string' ? step
      : step && typeof step === 'object' ? (step.msg || step.message || JSON.stringify(step))
      : String(step ?? ''))

  return (
    <div className="glass-card border-brand-500/15 overflow-hidden animate-fade-in">
      <div className="flex items-center gap-3 px-5 py-3 border-b border-white/[0.06]">
        {evaluating
          ? <Loader2 size={14} className="text-brand-400 animate-spin" />
          : <CheckCircle2 size={14} className="text-green-400" />}
        <p className="font-display font-600 text-sm text-white">
          {evaluating ? 'Agent running…' : 'Agent thought log'}
        </p>
        {evaluating && (
          <span className="ml-auto text-white/25 text-xs font-mono">
            compiling and running your code
          </span>
        )}
      </div>

      <div className="px-5 py-4 space-y-2.5 max-h-52 overflow-y-auto">
        {evaluating
          ? STAGES.map((stage, i) => (
              <div key={i} className="flex items-start gap-2.5">
                <div className="shrink-0 mt-0.5 w-3 h-3 rounded-full border border-white/15" />
                <p className="text-xs font-mono leading-relaxed text-white/30">{stage}</p>
              </div>
            ))
          : realSteps.map((str, i) => {
              const isError = str.startsWith('❌') || /fail|unavailable|cannot/i.test(str)
              return (
                <div key={i} className="flex items-start gap-2.5 animate-slide-up"
                  style={{ animationDelay: `${i * 50}ms`, animationFillMode: 'both' }}>
                  <div className="shrink-0 mt-0.5">
                    {isError
                      ? <XCircle size={13} className="text-red-400" />
                      : <CheckCircle2 size={13} className="text-green-400" />}
                  </div>
                  <p className={`text-xs font-mono leading-relaxed ${
                    isError ? 'text-red-300' : 'text-white/50'
                  }`}>{str}</p>
                </div>
              )
            })}
      </div>
    </div>
  )
}
