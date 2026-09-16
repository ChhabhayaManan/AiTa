import { useState, useCallback } from 'react'
import { recommendationAPI, getErrorMessage } from '../utils/api'
import toast from 'react-hot-toast'

export function useRecommendations() {
  const [recommendations, setRecommendations] = useState([])
  const [agentLog,        setAgentLog]        = useState(null)
  const [thoughtSteps,    setThoughtSteps]    = useState([])
  const [loading,         setLoading]         = useState(false)
  const [generating,      setGenerating]      = useState(false)

  // ─── Fetch stored recommendations ──────────────────────────────────────────
  const fetchRecommendations = useCallback(async () => {
    setLoading(true)
    try {
      const { data } = await recommendationAPI.getAll()
      setRecommendations(data)
    } catch (err) {
      if (err.response?.status !== 404) {
        // silent on 404 (no recommendations yet)
        toast.error('Failed to load recommendations.')
      }
    } finally {
      setLoading(false)
    }
  }, [])

  // ─── Fetch agent run log ────────────────────────────────────────────────────
  const fetchAgentLog = useCallback(async () => {
    try {
      const { data } = await recommendationAPI.getAgentLog()
      setAgentLog(data)
      setThoughtSteps(data.step_log || [])
    } catch {
      // No log yet — that's fine on first load
    }
  }, [])

  // ─── Run the AI Agent ───────────────────────────────────────────────────────
  // Auto-seed is now handled by the backend agent itself.
  // The frontend just shows animated progress steps while waiting.
  const runAgent = useCallback(async () => {
    setGenerating(true)
    setThoughtSteps([])
    setRecommendations([])

    // Placeholders shown until the real step_log arrives. They mirror the stages
    // ContentRecommendationAgent.run() actually logs, so the two do not contradict
    // each other when the response swaps them out.
    const progressSteps = [
      '🔍 Step 1: Reading your learning profile, history & error patterns...',
      '🎯 Step 2: Generating content for your topics & languages...',
      '🗺️  Step 3: Analysing knowledge gaps and learning path...',
      '🤝 Step 4a: Collaborative Filtering — finding similar learners...',
      '📚 Step 4b: Content-Based Filtering — matching your profile...',
      '⚙️  Step 5: Merging CF + CBF + RL exploration bonus...',
      '🤖 Step 6: AI re-ranking with full profile context...',
      '💾 Step 7: Saving your personalised recommendations...',
    ]

    let stepIdx = 0
    const interval = setInterval(() => {
      if (stepIdx < progressSteps.length) {
        setThoughtSteps(prev => [...prev, progressSteps[stepIdx]])
        stepIdx++
      }
    }, 900)

    try {
      const { data } = await recommendationAPI.generate()
      clearInterval(interval)

      // Replace animated steps with real backend thought log
      setThoughtSteps(data.agent_thought_steps || progressSteps)

      // Fetch final recommendations (now with real YouTube URLs)
      const { data: recs } = await recommendationAPI.getAll()
      setRecommendations(recs)

      await fetchAgentLog()
      toast.success(`✅ ${data.total} personalised recommendations ready!`)
    } catch (err) {
      clearInterval(interval)
      setThoughtSteps(prev => [
        ...prev,
        `❌ Error: ${getErrorMessage(err, 'Agent run failed.')}`
      ])
      // An unreachable model is not what lands here — the agent degrades to a
      // score-ordered ranking and still returns. This is the run itself failing.
      toast.error(getErrorMessage(err, 'Agent run failed. Please try again.'))
    } finally {
      setGenerating(false)
    }
  }, [fetchAgentLog])

  // ─── Log interaction ────────────────────────────────────────────────────────
  const logInteraction = useCallback(async (contentId, interaction, extra = {}) => {
    try {
      await recommendationAPI.logInteraction({ content_id: contentId, interaction, ...extra })
    } catch {
      // silent — interaction logging should never block UI
    }
  }, [])

  // ─── Dismiss ────────────────────────────────────────────────────────────────
  const dismiss = useCallback(async (recId) => {
    try {
      await recommendationAPI.dismiss(recId)
      setRecommendations(prev => prev.filter(r => r.id !== recId))
      toast.success('Recommendation dismissed.')
    } catch {
      toast.error('Failed to dismiss.')
    }
  }, [])

  return {
    recommendations, agentLog, thoughtSteps,
    loading, generating,
    fetchRecommendations, fetchAgentLog, runAgent,
    logInteraction, dismiss,
  }
}