/**
 * A picked bank problem, shown the way a judge shows one: the statement, the
 * constraints, and a worked sample so the student can see the exact stdin they
 * will receive and the stdout they must print.
 */
export default function ProblemStatement({ problem }) {
  if (!problem) return null

  return (
    <div className="space-y-2.5">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-sm font-display font-600 text-white/80">{problem.title}</span>
        {problem.topic && (
          <span className="px-1.5 py-0.5 bg-white/[0.04] border border-white/[0.06] rounded text-white/40 text-[10px] font-mono">
            {problem.topic}
          </span>
        )}
        <span className="px-1.5 py-0.5 bg-white/[0.04] border border-white/[0.06] rounded text-white/40 text-[10px] font-mono">
          {problem.test_count} test cases
        </span>
      </div>

      <p className="text-xs text-white/60 font-body leading-relaxed whitespace-pre-wrap">
        {problem.statement}
      </p>

      {problem.constraints && (
        <p className="text-[11px] text-white/35 font-mono leading-relaxed">
          Constraints: {problem.constraints}
        </p>
      )}

      {problem.sample_input && (
        <div className="grid grid-cols-2 gap-2">
          <div>
            <p className="text-white/30 text-[10px] font-mono mb-1 uppercase tracking-wide">Sample input</p>
            <pre className="bg-surface-900/60 border border-white/[0.06] rounded-lg px-2.5 py-2 text-[11px] font-mono text-white/70 overflow-x-auto whitespace-pre">
{problem.sample_input}
            </pre>
          </div>
          <div>
            <p className="text-white/30 text-[10px] font-mono mb-1 uppercase tracking-wide">Sample output</p>
            <pre className="bg-surface-900/60 border border-white/[0.06] rounded-lg px-2.5 py-2 text-[11px] font-mono text-white/70 overflow-x-auto whitespace-pre">
{problem.sample_output}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
