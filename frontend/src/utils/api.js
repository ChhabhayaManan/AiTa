import axios from 'axios'

// ─── Helper: safely extract a string from any API error ──────────────────────
export function getErrorMessage(err, fallback = 'Something went wrong.') {
  const detail = err?.response?.data?.detail
  if (!detail) return err?.message || fallback
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map(e => (typeof e === 'object' ? (e.msg || JSON.stringify(e)) : String(e))).join(', ')
  }
  if (typeof detail === 'object') return detail.msg || JSON.stringify(detail)
  return String(detail)
}

export const API_BASE = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,   // 60s — gives Render free tier time to wake up
})

// An evaluation compiles code, runs it in the sandbox and calls an LLM, which
// routinely passes 60s. Aborting the request does not stop the backend, so the
// work completes while the UI reports "Network Error" and resets itself.
const EVAL_TIMEOUT = 300000

// Must go through API_BASE. A relative path posts to the frontend's own
// origin, which 404s, so every refresh failed and logged the user out.
export async function refreshAccessToken() {
  const { data } = await axios.post(`${API_BASE}/auth/refresh`, {
    refresh_token: localStorage.getItem('refresh_token'),
  })
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('refresh_token', data.refresh_token)
  return data.access_token
}

function sendToLogin() {
  localStorage.clear()
  window.location.href = '/login'
}

// ─── Request Interceptor: attach token ───────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// ─── Response Interceptor: auto-refresh on 401 ───────────────────────────────
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      if (localStorage.getItem('refresh_token')) {
        try {
          const token = await refreshAccessToken()
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        } catch {
          sendToLogin()
        }
      }
    }
    return Promise.reject(error)
  }
)

// ─── Auth API ─────────────────────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  verifyOtp: (data) => api.post('/auth/verify-otp', data),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (data) => api.post('/auth/reset-password', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
  // Both 404 unless the backend has DEBUG on and DEV_LOGIN_EMAIL set.
  devLoginAvailable: () => api.get('/auth/dev-login'),
  devLogin: () => api.post('/auth/dev-login'),
}

// ─── User Profile API ─────────────────────────────────────────────────────────
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.patch('/users/profile', data),
  changePassword: (data) => api.post('/users/change-password', data),
  updateConsent: (consent) => api.patch(`/users/consent?consent=${consent}`),
  getPeerComparison: () => api.get('/users/peer-comparison'),
}

export const recommendationAPI = {
  // Trigger the AI agent — long timeout since it fetches YouTube + calls the LLM
  generate: () => api.post('/recommendations/generate', {}, { timeout: 120000 }),
  // Get current stored recommendations
  getAll: () => api.get('/recommendations/'),
  // Get last agent run log with thought steps
  getAgentLog: () => api.get('/recommendations/agent-log'),
  // Log an interaction (view, complete, like, etc.)
  logInteraction: (data) => api.post('/recommendations/interact', data),
  // Dismiss a recommendation
  dismiss: (recId) => api.patch(`/recommendations/${recId}/dismiss`),
  // Browse content catalog
  listContent: (skip = 0, limit = 50) => api.get(`/recommendations/content?skip=${skip}&limit=${limit}`),
  // Seed starter content (call once)
  seedContent: () => api.post('/recommendations/content/seed'),
}

export const problemsAPI = {
  generate: (data) => api.post('/problems/generate', data),
};

// ─── Code Evaluation Agent API ────────────────────────────────────────────────
export const codeEvalAPI = {
  // Submit code (no eval yet)
  submit:           (data) => api.post('/code-eval/submit', data),
  // Evaluate an existing submission
  evaluate:         (id)   => api.post(`/code-eval/submit/${id}/evaluate`, null, { timeout: EVAL_TIMEOUT }),
  // Submit + evaluate in one call  ← main action
  submitAndEvaluate:(data) => api.post('/code-eval/evaluate', data, { timeout: EVAL_TIMEOUT }),
  // Run against the shown example only — not scored, not saved
  run:              (data) => api.post('/code-eval/run', data),
  // History
  getSubmissions:   ()     => api.get('/code-eval/submissions'),
  getSubmission:    (id)   => api.get(`/code-eval/submissions/${id}`),
  deleteSubmission: (id)   => api.delete(`/code-eval/submissions/${id}`),
  // Stats & progress
  getStats:         ()     => api.get('/code-eval/stats'),
  // Problem bank
  getProblems:      ()     => api.get('/code-eval/problems'),
  getProblem:       (id)   => api.get(`/code-eval/problems/${id}`),
}

export const feedbackAPI = {
  autoGenerate: ()       => api.post('/feedback/auto-generate'),
  generate:    (data)    => api.post('/feedback/generate', data),
  getAll:      ()        => api.get('/feedback/'),
  unreadCount: ()        => api.get('/feedback/unread-count'),
  getReport:   (id)      => api.get(`/feedback/${id}`),
  markRead:    (id)      => api.patch(`/feedback/${id}/read`),
  // Next rung of the hint ladder for a problem the student is failing
  hint:        (problemId) => api.post('/feedback/hint', { problem_id: problemId }, { timeout: EVAL_TIMEOUT }),
}

export const profileAPI = {
  getMastery: () => api.get('/profile/mastery'),
}

const signedOut = (res) => res.status === 401

// The reply is a Server-Sent Events stream over POST, which axios cannot read
// incrementally, so this one call uses fetch with the same token handling.
async function postStream(path, body, signal) {
  const send = () => {
    const token = localStorage.getItem('access_token')
    return fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
      signal,
    })
  }
  let res = await send()
  if (!signedOut(res)) return res
  if (!localStorage.getItem('refresh_token')) {
    sendToLogin()
    return res
  }
  try {
    await refreshAccessToken()
  } catch {
    sendToLogin()
    return res
  }
  res = await send()
  if (signedOut(res)) sendToLogin()
  return res
}

export const chatAPI = {
  listThreads:  ()                       => api.get('/chat/threads'),
  getThread:    (id)                     => api.get(`/chat/threads/${id}`),
  createThread: (mode)                   => api.post('/chat/threads', mode ? { mode } : {}),
  thumbs:       (messageId, value)       => api.patch(`/chat/messages/${messageId}/thumbs`, { value }),
  send:         (threadId, body, signal) => postStream(`/chat/threads/${threadId}/messages`, body, signal),
}

export const assessmentAPI = {
  // May generate a coding problem when the bank has none left, which calls the LLM
  next:        ()               => api.get('/assessment/next', { timeout: EVAL_TIMEOUT }),
  answerMcq:   (id, chosenIndex) => api.post(`/assessment/mcq/${id}/answer`, { chosen_index: chosenIndex }),
  submitDebug: (id, code)       => api.post(`/assessment/debug/${id}/submit`, { code }, { timeout: EVAL_TIMEOUT }),
}

export const gamificationAPI = {
  me: () => api.get('/gamification/me'),
}

export const onboardingAPI = {
  state:       ()                          => api.get('/onboarding/state'),
  saveStep:    (step, data)                => api.put(`/onboarding/steps/${step}`, data),
  next:        ()                          => api.post('/onboarding/diagnostic/next'),
  // Code answers run in the sandbox and theory answers may call the LLM
  answer:      (itemId, answer, msTaken)   => api.post('/onboarding/diagnostic/answer',
    { item_id: itemId, answer, ms_taken: msTaken }, { timeout: EVAL_TIMEOUT }),
  finish:      ()                          => api.post('/onboarding/finish', null, { timeout: EVAL_TIMEOUT }),
  editProfile: (data)                      => api.patch('/onboarding/profile', data),
}

export default api