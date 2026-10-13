import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './hooks/useAuth'
import { ThemeProvider } from './hooks/useTheme'
import ProtectedRoute from './components/auth/ProtectedRoute'
import ErrorBoundary from './components/ui/ErrorBoundary'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'

const OnboardingPage     = lazy(() => import('./pages/OnboardingPage'))
const ProfilePage        = lazy(() => import('./pages/ProfilePage'))
const RecommendationPage = lazy(() => import('./pages/RecommendationPage'))
const CodeEvalPage       = lazy(() => import('./pages/CodeEvalPage'))
const FeedbackPage       = lazy(() => import('./pages/FeedbackPage'))
const CodeHelpPage       = lazy(() => import('./pages/CodeHelpPage'))
const PracticePage       = lazy(() => import('./pages/PracticePage'))

function PageLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-6 h-6 border-2 border-white/20 border-t-brand-400 rounded-full animate-spin" />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: '#1a2236',
                color: '#fff',
                border: '1px solid rgba(255,255,255,0.08)',
                fontFamily: '"DM Sans", sans-serif',
                fontSize: '14px',
                borderRadius: '12px',
              },
              success: { iconTheme: { primary: '#2e9aff', secondary: '#fff' } },
              error:   { iconTheme: { primary: '#f87171', secondary: '#fff' } },
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
            <Route path="/recommendations" element={<ProtectedRoute><RecommendationPage /></ProtectedRoute>} />
            <Route path="/code-eval"       element={<ProtectedRoute><CodeEvalPage /></ProtectedRoute>} />
            <Route path="/feedback"        element={<ProtectedRoute><FeedbackPage /></ProtectedRoute>} />
            <Route path="/code-help"       element={<ProtectedRoute><CodeHelpPage /></ProtectedRoute>} />
            <Route path="/practice"        element={<ProtectedRoute><PracticePage /></ProtectedRoute>} />
            <Route path="*"               element={<Navigate to="/dashboard" replace />} />
          </Routes>
          </Suspense>
          </ErrorBoundary>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  )
}