from functools import lru_cache
from typing import Optional

from langgraph.graph import END, START, StateGraph

from app.agents.content_player.nodes.detect_signals import detect_signals
from app.agents.content_player.nodes.load_session import load_session
from app.agents.content_player.nodes.persist import persist
from app.agents.content_player.nodes.respond import respond
from app.agents.content_player.nodes.select_problem import select_problem
from app.agents.content_player.schemas import ChatTurn
from app.agents.content_player.state import ChatState
from app.core.exceptions import LLMUnavailable

TUTOR_UNAVAILABLE = ("The tutor could not answer right now. Your message was saved — "
                     "please try again in a moment.")


@lru_cache(maxsize=1)
def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("load_session", load_session)
    graph.add_node("detect_signals", detect_signals)
    graph.add_node("select_problem", select_problem)
    graph.add_node("respond", respond)
    graph.add_node("persist", persist)

    graph.add_edge(START, "load_session")
    graph.add_edge("load_session", "detect_signals")
    graph.add_edge("detect_signals", "select_problem")
    graph.add_edge("select_problem", "respond")
    graph.add_edge("respond", "persist")
    graph.add_edge("persist", END)
    return graph.compile()


def run_chat_turn(db, session_id: int, user_id: int, message: str,
                  code_snippet: Optional[str] = None, *,
                  respond_runnable=None) -> ChatTurn:
    """One chat turn, start to finish.

    Synchronous on purpose: the graph blocks on the model, so a caller must run it
    off the event loop rather than stalling every other request on it.
    """
    state = ChatState(
        db=db, session_id=session_id, user_id=user_id, message=message,
        code_snippet=code_snippet, respond_runnable=respond_runnable,
    )
    result = build_chat_graph().invoke(state)
    final = result if isinstance(result, ChatState) else ChatState(**result)

    if final.llm_failed:
        # `persist` has already saved the student's message. There is nothing to
        # return, and this agent has no non-model content to return in its place.
        raise LLMUnavailable(TUTOR_UNAVAILABLE)

    return final.turn
