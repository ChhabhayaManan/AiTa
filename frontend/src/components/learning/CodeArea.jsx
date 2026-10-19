export default function CodeArea({ value, onChange, disabled, maxLength, height = 'h-72', label }) {
  return (
    <textarea value={value} onChange={e => onChange(e.target.value)} spellCheck={false}
      disabled={disabled} maxLength={maxLength} aria-label={label}
      className={`w-full ${height} p-4 rounded-xl bg-black/40 border border-white/10 text-sky-100 font-mono text-sm leading-relaxed focus:outline-none focus:border-brand-500/50 resize-y disabled:opacity-60`} />
  )
}
