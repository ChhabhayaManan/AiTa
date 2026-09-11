from app.agents.code_eval.state import EvalState
from app.agents.code_eval.static_metrics import find_issues, measure


def analyse(state: EvalState) -> EvalState:
    metrics = measure(state.code, state.language)
    state.metrics = metrics
    state.issues = find_issues(state.code, state.language, metrics)
    state.log(
        f"Static analysis: {metrics.lines_of_code} LOC, "
        f"CCN {metrics.cyclomatic_complexity}, {len(state.issues)} issues."
    )
    return state
