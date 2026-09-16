from typing import Dict, Optional


def analyse_patterns(eval_ctx: Optional[Dict], cp_ctx: Optional[Dict]) -> Dict:
    errors, weak_concepts, strengths = [], [], []

    if eval_ctx:
        for issue in eval_ctx["issues"][:10]:
            if issue.get("severity") in ("error", "critical"):
                errors.append(f"[{issue.get('category', '?')}] {issue.get('message', '')}")
        for dim, score in [("correctness", eval_ctx["correctness"]),
                           ("complexity", eval_ctx["complexity"]),
                           ("efficiency", eval_ctx["efficiency"]),
                           ("style", eval_ctx["style"])]:
            if score is not None and score < 60:
                weak_concepts.append(dim)
        strengths.extend(eval_ctx.get("best_practices", [])[:3])

    if cp_ctx:
        weak_concepts.extend(cp_ctx.get("weak", []))
        strengths.extend(cp_ctx.get("mastery", []))
        if cp_ctx.get("confusion"):
            errors.append(f"Confusion on topic: '{cp_ctx.get('topic', '')}'")

    return {
        "errors": list(dict.fromkeys(errors))[:8],
        "weak_concepts": list(dict.fromkeys(weak_concepts))[:6],
        "strengths": list(dict.fromkeys(strengths))[:5],
    }
