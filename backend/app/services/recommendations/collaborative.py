import math
from collections import defaultdict
from typing import Dict

from sqlalchemy.orm import Session

from app.models.recommendation import UserContentInteraction


def _collaborative_filtering(db: Session, user_id: int, user_ctx: Dict) -> Dict[int, float]:
    """
    Two-part CF:
    1. Cosine similarity between user interaction vectors (standard CF)
    2. Co-completion chains: users who completed X also completed Y
       → recommend Y to users who completed X (like JS → React)
    """
    all_interactions = db.query(UserContentInteraction).filter(
        UserContentInteraction.implicit_score > 0
    ).all()
    if not all_interactions:
        return {}

    # Build user vectors: user_id → {content_id: score}
    user_vectors: Dict[int, Dict[int, float]] = defaultdict(dict)
    for inter in all_interactions:
        score = inter.implicit_score or 0.0
        if inter.rating:
            score = max(score, inter.rating / 5.0)
        # Recency boost: more recent interactions count more
        user_vectors[inter.user_id][inter.content_id] = score

    excluded = user_ctx["excluded_ids"] | user_ctx["seen_content_ids"]

    # Part 1: Standard cosine similarity CF
    cf_scores: Dict[int, float] = defaultdict(float)
    sim_sum:   Dict[int, float] = defaultdict(float)

    if user_id in user_vectors:
        target_vec = user_vectors[user_id]

        def cosine_sim(a: Dict, b: Dict) -> float:
            common = set(a) & set(b)
            if not common:
                return 0.0
            dot    = sum(a[k] * b[k] for k in common)
            norm_a = math.sqrt(sum(v**2 for v in a.values()))
            norm_b = math.sqrt(sum(v**2 for v in b.values()))
            return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

        similarities = sorted(
            [(uid, cosine_sim(target_vec, vec))
             for uid, vec in user_vectors.items() if uid != user_id],
            key=lambda x: x[1], reverse=True
        )[:20]

        for neighbor_id, sim in similarities:
            if sim <= 0.05:
                continue
            for cid, score in user_vectors[neighbor_id].items():
                if cid not in excluded:
                    cf_scores[cid] += sim * score
                    sim_sum[cid]   += sim

    standard_cf = {
        cid: (cf_scores[cid] / sim_sum[cid]) if sim_sum[cid] > 0 else 0.0
        for cid in cf_scores
    }

    # Part 2: Co-completion chains
    # Find content the user completed, then find what other users completed next
    completed_ids = user_ctx["completed_ids"]
    co_completion: Dict[int, float] = defaultdict(float)

    if completed_ids:
        # Users who also completed the same content
        similar_users = set()
        for inter in all_interactions:
            if inter.content_id in completed_ids and inter.user_id != user_id:
                if inter.is_completed or inter.completion_pct >= 80:
                    similar_users.add(inter.user_id)

        # What did those users complete AFTER?
        for inter in all_interactions:
            if (inter.user_id in similar_users and
                    inter.content_id not in excluded and
                    (inter.is_completed or inter.completion_pct >= 80)):
                # Weight by how many similar users completed it
                co_completion[inter.content_id] += 1.0

        # Normalise co-completion scores to 0-1
        max_co = max(co_completion.values(), default=1) or 1
        co_completion = {cid: v / max_co for cid, v in co_completion.items()}

    # Merge: standard CF + co-completion boost
    all_cids = set(standard_cf) | set(co_completion)
    merged_cf = {}
    for cid in all_cids:
        merged_cf[cid] = round(
            standard_cf.get(cid, 0.0) * 0.7 + co_completion.get(cid, 0.0) * 0.3, 4
        )

    return merged_cf
