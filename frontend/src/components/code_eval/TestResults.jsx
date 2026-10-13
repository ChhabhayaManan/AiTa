import { CheckCircle2, XCircle, AlertTriangle, FlaskConical, Clock } from 'lucide-react'

const UNVERIFIED_REASON = {
  no_problem_statement:      'You did not give a problem statement, so there was nothing to test against.',
  language_not_executable:   'Only C, C++ and Python can be run right now. Other languages get a code review instead.',
  executor_unavailable:      'The sandbox that runs your code was unreachable, so nothing could be executed.',
  reference_unvalidated:     'A reference solution could not be produced for this problem, so the tests could not be trusted.',
  insufficient_agreed_tests: 'Too few test cases could be verified for this problem to grade it honestly.',
  test_generation_failed:    'Test cases could not be generated right now. Try again in a few minutes.',
}

const CASE_STATUS_LABEL = {
  ok:              'passed',
  wrong_answer:    'wrong output',
  runtime_error:   'crashed',
  timeout:         'too slow',
  memory_exceeded: 'used too much memory',
  compile_error:   'did not compile',
  internal_error:  'could not be run',
}

function ratioColor(passed, total) {
  if (!total) return '#71717a'
  const pct = (passed / total) * 100
  if (pct === 100) return '#22c55e'
  if (pct >= 60) return '#f59e0b'
  return '#ef4444'
}

function CaseStrip({ cases }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {cases.map(c => (
        <div
          key={c.ordinal}
          title={`Case ${c.ordinal} (${c.kind}) — ${CASE_STATUS_LABEL[c.status] || c.status} · ${c.time_ms}ms`}
          className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-mono font-600 transition-transform hover:scale-110 cursor-default ${
            c.passed
              ? 'bg-green-500/15 text-green-400 border border-green-500/25'
              : 'bg-red-500/15 text-red-400 border border-red-500/25'
          }`}
        >
          {c.ordinal}
        </div>
      ))}
    </div>
  )
}

function FailingCase({ failing }) {
  const rows = [
    ['input',     failing.stdin],
    ['expected',  failing.expected_stdout],
    ['your code', failing.actual_stdout],
  ]

  return (
    <div className="glass-card overflow-hidden">
      <div className="px-4 py-3 border-b border-white/[0.06] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <XCircle size={14} className="text-red-400" />
          <span className="font-display font-600 text-sm text-white">First failing case</span>
        </div>
        <span className="text-white/30 text-xs font-mono px-2 py-0.5 rounded-md bg-surface-600/60">
          {failing.kind}
        </span>
      </div>

      <div className="p-4 space-y-3">
        {rows.map(([label, value]) => (
          <div key={label} className="grid grid-cols-[88px_1fr] gap-3 items-start">
            <span className="text-white/30 text-xs font-display font-600 pt-1.5">{label}</span>
            <pre className="bg-[#0d1117] border border-white/[0.06] rounded-lg px-3 py-1.5 overflow-x-auto text-xs font-mono text-white/75 whitespace-pre-wrap break-words">
              {value === '' ? <span className="text-white/20">(empty)</span> : value}
            </pre>
          </div>
        ))}

        {failing.rationale && (
          <div className="grid grid-cols-[88px_1fr] gap-3 items-start pt-1">
            <span className="text-white/30 text-xs font-display font-600">checks</span>
            <p className="text-white/50 text-xs leading-relaxed">{failing.rationale}</p>
          </div>
        )}

        {failing.stderr && (
          <div className="grid grid-cols-[88px_1fr] gap-3 items-start">
            <span className="text-white/30 text-xs font-display font-600 pt-1.5">error</span>
            <pre className="bg-[#0d1117] border border-red-500/15 rounded-lg px-3 py-1.5 overflow-x-auto text-xs font-mono text-red-300/70 whitespace-pre-wrap break-words max-h-40">
              {failing.stderr}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default function TestResults({ result }) {
  if (!result) return null

  const {
    compiled, compile_output, verification_status, unverified_reason,
    tests_passed = 0, tests_total = 0, cases = [], first_failing_case, metrics,
    verdict, extra_output, missing_output,
  } = result

  // Compilation failed: no score, no hint — just the compiler's own words.
  if (compiled === false) {
    return (
      <div className="glass-card overflow-hidden animate-fade-in">
        <div className="px-4 py-3 border-b border-white/[0.06] flex items-center gap-2">
          <AlertTriangle size={14} className="text-orange-400" />
          <span className="font-display font-600 text-sm text-white">Your code did not compile</span>
        </div>
        <div className="p-4 space-y-3">
          <p className="text-white/40 text-xs leading-relaxed">
            Nothing was run, so there is no score. Fix the error below and submit again.
          </p>
          <pre className="bg-[#0d1117] border border-orange-500/15 rounded-xl px-4 py-3 overflow-x-auto text-xs font-mono text-orange-300/80 whitespace-pre-wrap">
            {compile_output || 'The compiler gave no output.'}
          </pre>
        </div>
      </div>
    )
  }

  // Nothing was verified: say why, and say what to do about it.
  if (verification_status !== 'verified') {
    return (
      <div className="glass-card p-5 animate-fade-in">
        <div className="flex items-center gap-2 mb-3">
          <FlaskConical size={14} className="text-white/30" />
          <span className="font-display font-600 text-sm text-white">No tests were run</span>
        </div>
        <p className="text-white/50 text-sm leading-relaxed mb-3">
          {UNVERIFIED_REASON[unverified_reason] ||
            'Your code could not be verified against test cases this time.'}
        </p>
        {unverified_reason === 'no_problem_statement' && (
          <p className="text-white/30 text-xs leading-relaxed">
            Add a problem statement above and your code will be executed against
            generated test cases, including the edge cases people usually miss.
          </p>
        )}
      </div>
    )
  }

  const color = ratioColor(tests_passed, tests_total)
  const allPassed = tests_passed === tests_total && tests_total > 0

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            {allPassed
              ? <CheckCircle2 size={15} className="text-green-400" />
              : <XCircle size={15} className="text-red-400" />}
            <span className="font-display font-600 text-sm" style={{ color }}>
              {verdict || 'Test results'}
            </span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="font-display font-800 text-2xl" style={{ color }}>
              {tests_passed}
            </span>
            <span className="text-white/30 text-sm font-mono">/ {tests_total} passed</span>
          </div>
        </div>

        <CaseStrip cases={cases} />

        {verdict === 'No output' ? (
          <div className="mt-4 px-3 py-2 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <p className="text-orange-300/80 text-xs leading-relaxed">
              Your program compiled and ran, but printed nothing at all — so every case
              is counted wrong. This is usually a loop that never runs. The first line of
              input is the number of test cases: make sure you read it before looping.
            </p>
          </div>
        ) : (missing_output || extra_output) && (
          <div className="mt-4 px-3 py-2 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <p className="text-orange-300/80 text-xs leading-relaxed">
              Your program printed {missing_output ? 'fewer' : 'more'} lines than expected.
              Every test after the first mismatch shifts out of place and is counted wrong —
              check how many lines you print per test case before hunting a logic bug.
            </p>
          </div>
        )}

        <div className="flex items-center gap-4 mt-4 pt-3 border-t border-white/[0.06]">
          <p className="text-white/25 text-xs">
            One run over all {tests_total} cases. Counted, not estimated.
          </p>
          {metrics?.slowest_case_ms != null && (
            <span className="ml-auto flex items-center gap-1 text-white/25 text-xs font-mono shrink-0">
              <Clock size={11} /> slowest {metrics.slowest_case_ms}ms
            </span>
          )}
        </div>
      </div>

      {first_failing_case
        ? <FailingCase failing={first_failing_case} />
        : (
          <div className="glass-card p-5 flex items-center gap-3">
            <CheckCircle2 size={16} className="text-green-400 shrink-0" />
            <p className="text-white/60 text-sm">
              Every test case passed, including the edge cases. Nice work.
            </p>
          </div>
        )}
    </div>
  )
}
