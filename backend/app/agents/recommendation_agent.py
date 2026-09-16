"""
Content Recommendation Agent
==============================
Implements the full recommendation pipeline described in the aiTA paper:

  1. User Profile Extraction
     - Skill level, preferred languages, interested topics (from registration)
     - Learning history: lessons done, time spent per topic, error patterns
     - Problem-solving approach signals from code evaluations
     - Accuracy rate and improvement trajectory

  2. Content-Based Filtering (CBF)
     - Matches content to profile topics, languages, difficulty preference
     - Boosts content covering weak areas and error patterns
     - Penalises content on already-mastered strong areas

  3. Collaborative Filtering (CF)
     - Cosine similarity between user interaction vectors
     - Co-completion chains: users who finished X also finished Y
     - Weighted by recency and interaction quality

  4. Reinforcement Learning (RL) Exploration Bonus
     - Rewards under-explored content types and topics
     - Prevents the agent from always recommending the same format

  5. Learning Path Sequencing
     - Prerequisite-aware ordering (arrays → linked lists → trees)
     - Difficulty progression: foundation → target → stretch
     - Gap detection: topics with low accuracy get prioritised

  6. LLM Re-ranking
     - Final re-rank with full profile context
     - Personalised explanations referencing actual user data
     - Fallback to score-based ranking if LLM unavailable

The stages themselves live in app/services/recommendations/; this module is the
orchestrator that runs them in order and records what happened.
"""

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.recommendation import AgentRunLog, Content, Recommendation
from app.services.recommendations.candidates import (
    _analyse_learning_path,
    _extract_user_context,
)
from app.services.recommendations.collaborative import _collaborative_filtering
from app.services.recommendations.content_based import (
    _content_based_filtering,
    _expand_related_topics,
)
from app.services.recommendations.ranking import _merge_and_rank, rank_with_llm
from app.services.recommendations.weights import CANDIDATE_K, TOP_N
from app.services.recommendations.youtube import (
    YouTubeSearchTool,
    _generate_content_for_profile,
)


class ContentRecommendationAgent:

    def __init__(self, db: Session):
        self.db = db
        self.yt = YouTubeSearchTool(getattr(settings, "YOUTUBE_API_KEY", ""))

    # ── PUBLIC ENTRY POINT ────────────────────────────────────────────────────

    def run(self, user_id: int, *, rank_runnable=None) -> Dict[str, Any]:
        batch_id = str(uuid.uuid4())
        start_ms = int(time.time() * 1000)
        step_log: List[str] = []

        run_log = AgentRunLog(user_id=user_id, batch_id=batch_id, status="running", step_log=[])
        self.db.add(run_log)
        self.db.commit()

        try:
            # ── Step 1: Extract full user profile ────────────────────────
            step_log.append("🔍 Step 1: Reading your learning profile, history & error patterns...")
            user_ctx = _extract_user_context(self.db, user_id)

            if not user_ctx["interested_topics"]:
                # Last resort: derive topics from learning_goals and interests
                fallback_topics = (user_ctx.get("learning_goals") or []) + (user_ctx.get("interests") or [])
                if fallback_topics:
                    user_ctx["interested_topics"] = fallback_topics
                    step_log.append(f"   ℹ️  No explicit topics set — using goals/interests as topics: {fallback_topics[:4]}")
                else:
                    step_log.append("⚠️  Profile has no topics, interests, or goals — add them in your profile for better recommendations.")
                    # Continue anyway with general content rather than bailing out

            step_log.append(
                f"   ✅ {user_ctx['username']} | {user_ctx['skill_level']} | "
                f"Topics: {user_ctx['interested_topics']} | "
                f"Languages: {user_ctx['preferred_languages']} | "
                f"Weak areas: {user_ctx['weak_areas'] or 'none yet'} | "
                f"Error patterns: {user_ctx['error_patterns'][:2] or 'none yet'} | "
                f"Accuracy: {user_ctx['accuracy_rate']:.0%} | "
                f"Excluded (done/dismissed): {len(user_ctx['excluded_ids'])}"
            )

            # ── Step 2: Generate profile-driven content catalog ───────────
            step_log.append("🎯 Step 2: Generating content for your topics & languages...")
            new_items, linked = _generate_content_for_profile(self.db, self.yt, user_ctx)
            total = self.db.query(Content).filter(Content.is_active == True).count()
            step_log.append(
                f"   ✅ {new_items} new items created, {linked} with a real video link. "
                f"Catalog: {total} total."
            )
            if linked < new_items:
                step_log.append(
                    f"   ⚠️  {new_items - linked} could not be matched to a YouTube "
                    "video and have no link to open."
                )

            # ── Step 3: Detect knowledge gaps & learning path ─────────────
            step_log.append("🗺️  Step 3: Analysing knowledge gaps and learning path...")
            gap_topics, next_topics = _analyse_learning_path(user_ctx)
            step_log.append(
                f"   ✅ Gaps detected: {gap_topics or 'none'} | "
                f"Suggested next: {next_topics or 'continuing current topics'}"
            )

            # ── Step 4a: Collaborative Filtering ─────────────────────────
            step_log.append("🤝 Step 4a: Collaborative Filtering — finding similar learners...")
            cf_scores = _collaborative_filtering(self.db, user_id, user_ctx)
            step_log.append(
                f"   ✅ CF found {len(cf_scores)} candidates from similar learner paths."
            )
            run_log.cf_candidates = len(cf_scores)

            # ── Step 4b: Content-Based Filtering ─────────────────────────
            step_log.append("📚 Step 4b: Content-Based Filtering — matching your profile...")
            cbf_scores = _content_based_filtering(self.db, user_ctx, gap_topics)
            step_log.append(
                f"   ✅ CBF scored {len(cbf_scores)} items "
                f"(prioritising: {(gap_topics + user_ctx['interested_topics'])[:3]})."
            )
            run_log.cbf_candidates = len(cbf_scores)

            # ── Step 4c: Related-topic expansion if needed ────────────────
            raw_count = len(set(cf_scores) | set(cbf_scores))
            expansion_scores: Dict[int, float] = {}
            if raw_count < TOP_N:
                step_log.append(f"🔗 Step 4c: Only {raw_count} fresh items — expanding to adjacent topics...")
                expansion_scores = _expand_related_topics(self.db, user_ctx, next_topics)
                step_log.append(f"   ✅ Expansion added {len(expansion_scores)} adjacent-topic items.")
            else:
                step_log.append(f"   ℹ️  {raw_count} fresh candidates — no expansion needed.")

            # ── Step 5: Merge + RL exploration bonus ─────────────────────
            step_log.append("⚙️  Step 5: Merging CF + CBF + RL exploration bonus...")
            merged     = _merge_and_rank(self.db, cf_scores, cbf_scores, user_ctx, expansion_scores)
            candidates = merged[:CANDIDATE_K]
            step_log.append(
                f"   ✅ {len(candidates)} diverse candidates after RL diversity enforcement."
            )

            # ── Step 6: LLM re-ranking ────────────────────────────────────
            step_log.append("🤖 Step 6: AI re-ranking with full profile context...")
            llm_result   = rank_with_llm(self.db, user_ctx, candidates, gap_topics,
                                         next_topics, runnable=rank_runnable)
            ranked_ids   = llm_result["ranked_ids"]
            explanations = llm_result["explanations"]
            descriptions = llm_result.get("descriptions", {})
            difficulties = llm_result.get("difficulties", {})
            tokens_used  = llm_result["tokens_used"]
            step_log.append(
                f"   ✅ Ranked {len(ranked_ids)} items "
                f"({tokens_used} tokens, model: {llm_result.get('model_used','fallback')})."
            )
            step_log.append("🧠 Strategy: " + llm_result.get("summary", ""))

            # ── Step 7: Persist ───────────────────────────────────────────
            step_log.append("💾 Step 7: Saving your personalised recommendations...")
            self.db.query(Recommendation).filter(
                Recommendation.user_id == user_id,
                Recommendation.is_clicked == False,
                Recommendation.is_dismissed == False,
            ).delete()

            saved_recs = []
            for rank, cid in enumerate(ranked_ids[:TOP_N], start=1):
                candidate = next((c for c in candidates if c["content_id"] == cid), None)
                if not candidate:
                    continue
                # Pack LLM-generated fields into agent_reasoning as JSON
                reasoning_payload = json.dumps({
                    "description":  descriptions.get(str(cid), ""),
                    "difficulty":   difficulties.get(str(cid), ""),
                    "why_relevant": explanations.get(str(cid), ""),
                })
                self.db.add(Recommendation(
                    user_id=user_id, content_id=cid,
                    score=candidate["blended_score"],
                    cf_score=candidate["cf_score"],
                    cbf_score=candidate["cbf_score"],
                    rl_bonus=candidate["rl_bonus"],
                    agent_reasoning=reasoning_payload,
                    rank=rank, batch_id=batch_id,
                ))
                saved_recs.append(cid)

            duration = int(time.time() * 1000) - start_ms
            run_log.status = "done"; run_log.step_log = step_log
            run_log.final_count = len(saved_recs)
            run_log.llm_tokens_used = tokens_used
            run_log.duration_ms = duration
            self.db.commit()
            step_log.append(f"✅ Done! {len(saved_recs)} personalised recommendations in {duration}ms.")

            return {
                "batch_id": batch_id, "user_id": user_id, "total": len(saved_recs),
                "agent_thought_steps": step_log, "generated_at": datetime.now(timezone.utc),
            }

        except Exception as exc:
            try: self.db.rollback()
            except Exception: pass
            try:
                run_log.status = "failed"
                run_log.error_message = str(exc)
                run_log.step_log = step_log + [f"❌ Error: {exc}"]
                self.db.commit()
            except Exception: pass
            raise
