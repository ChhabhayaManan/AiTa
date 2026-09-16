from app.agents.feedback.state import FeedbackState
from app.services.feedback.patterns import analyse_patterns as _analyse


def analyse_patterns(state: FeedbackState) -> FeedbackState:
    state.log("Analysing error patterns and concept gaps.")
    state.patterns = _analyse(state.eval_ctx, state.cp_ctx)
    state.log(f"{len(state.patterns['errors'])} errors, "
              f"{len(state.patterns['weak_concepts'])} weak concepts found.")
    return state
