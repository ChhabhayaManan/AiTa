from app.agents.content_player.state import ChatState
from app.services.content_player.signals import (
    DIFFICULTY_LEVELS,
    MIN_TOPIC_SWITCH_LENGTH,
    SOLVE_STREAK_FOR_BUMP,
    SOLVED_ACCURACY,
    _adjust_difficulty,
    _detect_comfort_signal,
    _detect_topic_from_message,
    _extract_accuracy_from_message,
    _get_difficulty_index,
    _has_code_submission,
)


def detect_signals(state: ChatState) -> ChatState:
    accuracy = _extract_accuracy_from_message(state.message)
    submitted = _has_code_submission(state.message, state.code_snippet)

    difficulty = state.difficulty
    consecutive = state.consecutive_easy_solves

    if submitted and accuracy is not None and accuracy >= SOLVED_ACCURACY:
        state.question_solved = True
        consecutive += 1

        if consecutive >= SOLVE_STREAK_FOR_BUMP:
            idx = _get_difficulty_index(difficulty)
            if idx < len(DIFFICULTY_LEVELS) - 1:
                difficulty = DIFFICULTY_LEVELS[idx + 1]
                state.difficulty_increased = True
                consecutive = 0  # reset streak after bump
    elif submitted:
        # Wrong or incomplete submission — reset streak.
        consecutive = 0

    state.accuracy = accuracy
    state.new_consecutive = consecutive
    state.comfort_signal = _detect_comfort_signal(state.message)

    # A bump earned by solving is not then re-adjusted by tone in the same turn.
    state.new_difficulty = (difficulty if state.difficulty_increased
                            else _adjust_difficulty(difficulty, state.comfort_signal))

    detected = _detect_topic_from_message(state.message)
    state.effective_topic = state.topic
    if (detected and detected != state.topic
            and len(state.message) > MIN_TOPIC_SWITCH_LENGTH):
        state.topic_changed = True
        state.effective_topic = detected

    return state
