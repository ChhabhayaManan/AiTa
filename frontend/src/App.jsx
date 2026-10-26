import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './hooks/useAuth'
import ProtectedRoute from './components/auth/ProtectedRoute'
import ErrorBoundary from './components/ui/ErrorBoundary'
import Backdrop from './components/ui/Backdrop'
import LogoMark from './components/ui/LogoMark'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'

const OnboardingPage     = lazy(() => import('./pages/OnboardingPage'))
const ProfilePage        = lazy(() => import('./pages/ProfilePage'))
const CodeEvalPage       = lazy(() => import('./pages/CodeEvalPage'))
const FeedbackPage       = lazy(() => import('./pages/FeedbackPage'))
const CodeHelpPage       = lazy(() => import('./pages/CodeHelpPage'))
const PracticePage       = lazy(() => import('./pages/PracticePage'))
const LanguageCheckPage  = lazy(() => import('./pages/LanguageCheckPage'))
const SessionSummaryPage = lazy(() => import('./pages/SessionSummaryPage'))

function PageLoading({ label = 'Loading' }) {
  return (
    <div className="flex min-h-[100dvh] flex-col items-center justify-center gap-4" role="status">
      <LogoMark className="h-11 w-11 motion-safe:animate-pulse" />
      <p className="text-sm text-ink-subtle">{label}…</p>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Backdrop />
        <Toaster
          position="top-center"
          toastOptions={{
            style: {
              background: '#1b1b1f',
              color: '#f5f5f7',
              border: '1px solid #36363d',
              fontFamily: '"Geist", system-ui, sans-serif',
              fontSize: '14px',
              borderRadius: '9999px',
              padding: '8px 14px',
            },
            success: { iconTheme: { primary: '#8fe3a0', secondary: '#0a0a0c' } },
            error:   { iconTheme: { primary: '#f58a7a', secondary: '#0a0a0c' } },
          }}
        />
        <ErrorBoundary>
        <Suspense fallback={<PageLoading />}>
        <Routes>
          <Route path="/"                element={<Navigate to="/dashboard" replace />} />
          <Route path="/login"           element={<LoginPage />} />
          <Route path="/register"        element={<RegisterPage />} />
          <Route path="/onboarding"      element={<ProtectedRoute><OnboardingPage /></ProtectedRoute>} />
          <Route path="/dashboard"       element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/profile"         element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="/code-eval"       element={<ProtectedRoute><CodeEvalPage /></ProtectedRoute>} />
          <Route path="/feedback"        element={<ProtectedRoute><FeedbackPage /></ProtectedRoute>} />
          <Route path="/code-help"       element={<ProtectedRoute><CodeHelpPage /></ProtectedRoute>} />
          <Route path="/practice"        element={<ProtectedRoute><PracticePage /></ProtectedRoute>} />
          <Route path="/practice/session/:id" element={<ProtectedRoute><SessionSummaryPage /></ProtectedRoute>} />
          <Route path="/language-check"  element={<ProtectedRoute><LanguageCheckPage /></ProtectedRoute>} />
          <Route path="*"                element={<Navigate to="/dashboard" replace />} />
        </Routes>
        </Suspense>
        </ErrorBoundary>
      </AuthProvider>
    </BrowserRouter>
  )
}
