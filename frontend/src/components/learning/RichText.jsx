// Question stems and statements mix prose with ```fenced``` code and `inline` code.
// Rendered as plain elements: no HTML from the model is ever injected.
export default function RichText({ text, className = '' }) {
  const parts = (text || '').split(/```[^\n]*\n([\s\S]*?)```/g)
  return (
    <div className={className}>
      {parts.map((part, i) =>
        i % 2 === 1 ? (
          <pre key={i} className="my-3 p-4 rounded-xl bg-black/40 border border-white/10 text-sky-300 text-sm font-mono overflow-x-auto whitespace-pre">
            {part}
          </pre>
        ) : (
          <p key={i} className="whitespace-pre-wrap leading-relaxed">
            {part.split(/(`[^`\n]+`)/g).map((chunk, j) =>
              chunk.startsWith('`') && chunk.endsWith('`') && chunk.length > 2
                ? <code key={j} className="px-1.5 py-0.5 rounded bg-black/40 text-sky-300 font-mono text-[0.9em]">{chunk.slice(1, -1)}</code>
                : chunk
            )}
          </p>
        )
      )}
    </div>
  )
}
