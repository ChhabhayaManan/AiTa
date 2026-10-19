import { Code2, User, BookOpen, ListChecks } from 'lucide-react'
import { StepTitle, StepNav, useSaveStep } from '../../../components/onboarding/StepControls'

const COLLECTED = [
  { icon: Code2,      text: 'The programming language you want to practise in' },
  { icon: User,       text: 'Your background: year, program, institution, coding experience and goal' },
  { icon: BookOpen,   text: 'How you like to learn: explanation style, examples, chat language and study time' },
  { icon: ListChecks, text: 'Your answers to a short check of up to 12 questions' },
]

export default function WelcomeStep({ onSaved, onConflict }) {
  const { saving, save } = useSaveStep('welcome', onSaved, onConflict)

  return (
    <div>
      <StepTitle
        title="Welcome to aiTA"
        subtitle="Before you start, we'll spend under 10 minutes getting to know you."
      />

      <span className="label">What we collect</span>
      <ul className="space-y-2.5 mb-6">
        {COLLECTED.map(({ icon: Icon, text }) => (
          <li key={text} className="flex items-start gap-3 text-sm text-white/70">
            <span className="w-7 h-7 rounded-lg bg-brand-600/15 flex items-center justify-center flex-shrink-0">
              <Icon size={14} className="text-brand-400" />
            </span>
            <span className="pt-1">{text}</span>
          </li>
        ))}
      </ul>

      <span className="label">Why</span>
      <p className="text-sm text-white/60 leading-relaxed mb-4">
        aiTA uses this to personalise your practice problems, hints and chat, so you start at the
        right level instead of from scratch.
      </p>
      <p className="text-sm text-white/60 leading-relaxed">
        You can view everything we saved and correct it later on your profile page.
      </p>

      <StepNav onNext={() => save({})} saving={saving} nextLabel="Get started" />
    </div>
  )
}
