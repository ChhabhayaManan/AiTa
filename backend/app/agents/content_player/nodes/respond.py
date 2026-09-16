import logging

from app.agents.content_player.prompts import (
    BUMP_NOTE,
    IMPROVISED_BLOCK,
    LEETCODE_PROMPTS,
    PROBLEM_BLOCK,
    SOLVED_CONTEXT,
    SOLVED_NOTE,
    _get_system_prompt,
)
from app.agents.content_player.schemas import TutorReply
from app.agents.content_player.state import ChatState
from app.core.exceptions import LLMUnavailable
from app.core.llm import get_chat_model, invoke_with_retry, structured

logger = logging.getLogger(__name__)

# The window of the conversation the model is given, as it has always been.
MAX_HISTORY_MESSAGES = 10

TEMPERATURE = 0.7


def _system(state: ChatState) -> str:
    prompt = _get_system_prompt(
        mode=state.mode,
        topic=state.effective_topic,
        language=state.language,
        skill_level=state.skill_level,
        interested_topics=state.interested_topics,
        difficulty=state.new_difficulty,
    )

    if state.solved_questions:
        prompt += SOLVED_CONTEXT.format(count=len(state.solved_questions))

    if state.problem_statement:
        prompt += PROBLEM_BLOCK.format(language=state.language,
                                       statement=state.problem_statement)
    elif state.problem_origin == "improvised":
        format_block = LEETCODE_PROMPTS.get(state.new_difficulty,
                                            LEETCODE_PROMPTS["medium"])
        prompt += IMPROVISED_BLOCK.format(
            topic=state.effective_topic,
            format_block=format_block.format(topic=state.effective_topic),
        )

    if state.question_solved:
        bump = (BUMP_NOTE.format(difficulty=state.new_difficulty)
                if state.difficulty_increased else "")
        prompt += SOLVED_NOTE.format(accuracy=state.accuracy or 0.0,
                                     bump_note=bump, topic=state.effective_topic)
    return prompt


def _human(state: ChatState) -> str:
    message = state.message
    if state.comfort_signal != "comfortable":
        message = f"[User comfort signal: {state.comfort_signal}]\n{message}"
    if state.code_snippet:
        message += f"\n\n```{state.language}\n{state.code_snippet}\n```"
    return message


def _payload(state: ChatState) -> list[tuple[str, str]]:
    payload = [("system", _system(state))]
    for turn in state.history[-MAX_HISTORY_MESSAGES:]:
        payload.append((turn["role"], turn["content"]))
    payload.append(("human", _human(state)))
    return payload


def respond(state: ChatState) -> ChatState:
    try:
        runnable = (state.respond_runnable
                    or structured(get_chat_model(temperature=TEMPERATURE), TutorReply))
        reply, usage = invoke_with_retry(runnable, _payload(state))
    except LLMUnavailable as exc:
        logger.warning("Tutor reply unavailable for session %s: %s",
                       state.session_id, exc.detail)
        state.llm_failed = True
        return state

    if reply is None:
        # Structured output that failed to parse is the same situation as no call at
        # all. This agent has nothing of its own to say, so inventing a tutor reply
        # here would be the silent fallback the migration exists to remove.
        logger.warning("Tutor reply did not parse for session %s", state.session_id)
        state.llm_failed = True
        return state

    state.reply = reply.reply
    state.concepts = reply.concepts or [state.effective_topic]
    state.mastery = reply.mastery
    state.weak = reply.weak
    state.suggestions = reply.suggestions
    state.tokens_used = usage.tokens
    state.latency_ms = usage.latency_ms
    state.model_used = usage.model
    return state
