import time
from functools import lru_cache
from typing import Optional

from langgraph.graph import END, START, StateGraph

from app.agents.feedback.nodes.analyse_patterns import analyse_patterns
from app.agents.feedback.nodes.gather_context import gather_context
from app.agents.feedback.nodes.persist import persist
from app.agents.feedback.nodes.synthesise import synthesise
from app.agents.feedback.state import FeedbackState
from app.models.feedback import FeedbackReport, FeedbackTone


@lru_cache(maxsize=1)
def build_feedback_graph():
    graph = StateGraph(FeedbackState)
    graph.add_node("gather_context", gather_context)
    graph.add_node("analyse_patterns", analyse_patterns)
    graph.add_node("synthesise", synthesise)
    graph.add_node("persist", persist)

    graph.add_edge(START, "gather_context")
    graph.add_edge("gather_context", "analyse_patterns")
    graph.add_edge("analyse_patterns", "synthesise")
    graph.add_edge("synthesise", "persist")
    graph.add_edge("persist", END)
    return graph.compile()


def generate_feedback(db, user_id: int, evaluation_id: Optional[int],
                      cp_session_id: Optional[int], tone: FeedbackTone,
                      *, synthesise_runnable=None) -> FeedbackReport:
    state = FeedbackState(
        db=db, user_id=user_id, evaluation_id=evaluation_id,
        cp_session_id=cp_session_id, tone=tone,
        synthesise_runnable=synthesise_runnable,
        started_ms=int(time.time() * 1000),
    )
    result = build_feedback_graph().invoke(state)
    final = result if isinstance(result, FeedbackState) else FeedbackState(**result)
    return final.report
