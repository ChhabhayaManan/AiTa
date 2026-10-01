import time
from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.agents.code_eval.nodes.analyse import analyse
from app.agents.code_eval.nodes.emit_event import emit_event
from app.agents.code_eval.nodes.ensure_tests import ensure_tests
from app.agents.code_eval.nodes.execute_student import execute_student
from app.agents.code_eval.nodes.explain import explain
from app.agents.code_eval.nodes.hint_l1 import hint_l1, log_l1
from app.agents.code_eval.nodes.persist import persist
from app.agents.code_eval.nodes.route_mode import route_mode
from app.agents.code_eval.nodes.score import score
from app.agents.code_eval.schemas import EvalReport
from app.agents.code_eval.state import EvalState


def _after_execute(state: EvalState) -> str:
    return "score" if state.halted else "explain"


@lru_cache(maxsize=1)
def build_eval_graph():
    graph = StateGraph(EvalState)
    graph.add_node("route_mode", route_mode)
    graph.add_node("analyse", analyse)
    graph.add_node("ensure_tests", ensure_tests)
    graph.add_node("execute_student", execute_student)
    graph.add_node("explain", explain)
    graph.add_node("score", score)

    graph.add_edge(START, "route_mode")
    graph.add_edge("route_mode", "analyse")
    graph.add_edge("analyse", "ensure_tests")
    graph.add_edge("ensure_tests", "execute_student")
    graph.add_conditional_edges(
        "execute_student", _after_execute, {"explain": "explain", "score": "score"}
    )
    graph.add_node("hint_l1", hint_l1)
    graph.add_edge("explain", "score")
    graph.add_edge("score", "hint_l1")
    graph.add_edge("hint_l1", END)
    return graph.compile()


def evaluate_submission(db, submission_id: int, user_id: int, *, provider=None,
                        generator=None, explain_runnable=None) -> EvalReport:
    started_ms = int(time.time() * 1000)
    state = EvalState(
        db=db, submission_id=submission_id, user_id=user_id, provider=provider,
        generator=generator, explain_runnable=explain_runnable,
    )
    result = build_eval_graph().invoke(state)
    final = result if isinstance(result, EvalState) else EvalState(**result)
    persist(final, started_ms=started_ms)
    emit_event(final)
    log_l1(final)
    return final.report
