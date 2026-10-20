export default function LogoMark({ className = 'h-8 w-8' }) {
  return (
    <svg viewBox="0 0 32 32" className={`shrink-0 ${className}`} aria-hidden="true">
      <rect x="0.75" y="0.75" width="30.5" height="30.5" rx="9.25" fill="#1b1b1f" stroke="#36363d" strokeWidth="1.5" />
      <path d="M9.5 10.5 15 16l-5.5 5.5" fill="none" stroke="#f5f5f7" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
      <rect x="17.25" y="19.75" width="6.5" height="2.75" rx="1.375" fill="#8fe3a0" className="motion-safe:animate-blink" />
      <path d="M23.5 7.25v4.5M21.25 9.5h4.5" stroke="#f6d66f" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  )
}

export function Wordmark({ className = '' }) {
  return (
    <span className={`text-lg font-semibold tracking-tight text-ink ${className}`}>
      ai<span className="text-pop-mint">TA</span>
    </span>
  )
}
