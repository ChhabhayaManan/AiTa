import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { ArrowRight, AtSign, Eye, EyeOff, Lock, Mail, User } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { getErrorMessage } from '../utils/api'
import AuthLayout from '../components/auth/AuthLayout'
import Button from '../components/ui/Button'
import { TextField } from '../components/ui/Field'

function validate(form) {
  const e = {}
  if (!/^[a-zA-Z0-9_]{3,50}$/.test(form.username)) e.username = '3 to 50 characters: letters, digits or underscore'
  if (!/\S+@\S+\.\S+/.test(form.email)) e.email = 'Enter a valid email'
  if (form.password.length < 8 || !/[A-Z]/.test(form.password) || !/\d/.test(form.password)) {
    e.password = 'Use at least 8 characters, with 1 uppercase letter and 1 digit'
  }
  if (form.confirmPassword !== form.password) e.confirmPassword = "The passwords don't match"
  return e
}

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register } = useAuth()
  const [form, setForm] = useState({ full_name: '', username: '', email: '', password: '', confirmPassword: '' })
  const [errors, setErrors] = useState({})
  const [general, setGeneral] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const set = field => e => {
    setForm(f => ({ ...f, [field]: e.target.value }))
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: undefined }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setGeneral('')
    const found = validate(form)
    setErrors(found)
    if (Object.keys(found).length) return
    setLoading(true)
    try {
      await register({
        username: form.username,
        email: form.email,
        password: form.password,
        full_name: form.full_name.trim() || undefined,
      })
      navigate('/login', { replace: true, state: { registered: true, email: form.email } })
    } catch (err) {
      setGeneral(getErrorMessage(err, "Couldn't create your account."))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Takes a minute. After you log in, a short setup gets your first questions at the right level."
      footer={<>Already have an account? <Link to="/login" className="font-medium text-ink underline decoration-ink-faint underline-offset-4 hover:decoration-ink">Log in</Link></>}
    >
      {general && (
        <div className="mb-5 rounded-2xl border border-pop-coral/25 bg-pop-coral/[0.07] px-4 py-3 text-sm text-pop-coral" role="alert">{general}</div>
      )}
      <form onSubmit={handleSubmit} className="space-y-5" noValidate>
        <TextField label="Full name" optional icon={User} value={form.full_name} onChange={set('full_name')}
          placeholder="Riya Deshpande" autoComplete="name" maxLength={255} />
        <TextField label="Username" icon={AtSign} value={form.username} onChange={set('username')}
          placeholder="riya_codes" autoComplete="username" helper="Letters, digits or underscore" error={errors.username} />
        <TextField label="Email" type="email" icon={Mail} value={form.email} onChange={set('email')}
          placeholder="you@college.edu" autoComplete="email" error={errors.email} />
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <TextField
            label="Password"
            type={showPassword ? 'text' : 'password'}
            icon={Lock}
            value={form.password}
            onChange={set('password')}
            autoComplete="new-password"
            helper="Min 8 chars, 1 uppercase, 1 digit"
            error={errors.password}
            trailing={
              <button
                type="button"
                onClick={() => setShowPassword(v => !v)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                className="flex h-9 w-9 items-center justify-center rounded-full text-ink-subtle hover:bg-white/[0.06] hover:text-ink"
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            }
          />
          <TextField label="Confirm password" type={showPassword ? 'text' : 'password'} icon={Lock}
            value={form.confirmPassword} onChange={set('confirmPassword')} autoComplete="new-password" error={errors.confirmPassword} />
        </div>
        <Button type="submit" size="lg" iconRight={ArrowRight} busy={loading} className="w-full">
          {loading ? 'Creating account…' : 'Create account'}
        </Button>
      </form>
    </AuthLayout>
  )
}
