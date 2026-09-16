from app.models.feedback import FeedbackTone

TONE_INSTRUCTIONS = {
    FeedbackTone.ENCOURAGING:
        "Be warm and encouraging — praise effort before mentioning problems.",
    FeedbackTone.CONSTRUCTIVE:
        "Be direct and specific — focus on actionable improvement over praise.",
    FeedbackTone.CHALLENGING:
        "Be Socratic — ask why, push deeper understanding, challenge assumptions.",
}

SYSTEM_PROMPT = """You are the Feedback Agent in aiTA — an AI teaching assistant for \
Indian programming students.
You synthesise findings from the Code Evaluation Agent and Content Player Agent into \
rich, personalised feedback.

Student: {username} | Skill: {skill}
Languages: {languages}
Known weak areas: {weak_areas}
Tone: {tone_instruction}

Rules:
- NEVER say "wrong" without explaining WHY it matters for learning
- Adapt language to {skill} level — no jargon for beginners
- Ground every point in the findings below; do not invent work the student did not do
"""

EVAL_BLOCK = """CODE EVALUATION:
Score: {overall}/100 | Correct: {correctness} | Complexity: {complexity} | \
Efficiency: {efficiency}
Issues: {issues}
Learning points: {learning_points}
Anti-patterns: {anti_patterns}
Agent summary: {summary}"""

CP_BLOCK = """CONTENT PLAYER SESSION:
Topic: {topic} | Mode: {mode}
Concepts covered: {concepts}
Mastery: {mastery}
Weaknesses: {weak}
Confusion detected: {confusion}"""

PATTERN_BLOCK = """PATTERN ANALYSIS:
Error patterns: {errors}
Weak concepts: {weak_concepts}
Strengths: {strengths}"""

PATTERN_ONLY_HEADLINE = (
    "Detailed feedback could not be generated right now — this is what the "
    "automatic analysis alone found"
)

PATTERN_ONLY_MOTIVATIONAL = "Every bug fixed is a lesson learned — keep going!"
