"""Ranking tests. Offline: no network and no live DB — the sqlite `session` fixture
supplies the catalog and a fake runnable supplies the ranking."""

import pytest
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.models.recommendation import Content, ContentType, DifficultyLevel
from app.services.recommendations.ranking import _merge_and_rank, rank_with_llm
from app.services.recommendations.schemas import RankedItem, RankedRecommendations
from app.services.recommendations.weights import TOP_N


def add_content(session, *, title, content_type, topics, language="Python",
                difficulty=DifficultyLevel.BEGINNER, url=None):
    c = Content(title=title, description=f"About {title}.", content_type=content_type,
                difficulty=difficulty, language=language, topics=topics,
                skills_gained=["problem solving"], duration_mins=30, url=url,
                avg_rating=4.5, is_active=True)
    session.add(c)
    session.commit()
    return c


def ctx(**overrides):
    base = {
        "seen_content_ids":    set(),
        "preferred_languages": ["python"],
        "skill_level":         "beginner",
        "interested_topics":   ["trees"],
        "learning_goals":      ["build a parser"],
        "weak_areas":          ["recursion"],
        "error_patterns":      ["off-by-one"],
        "accuracy_rate":       0.42,
        "time_per_topic":      {"arrays": 90.0, "trees": 15.0},
    }
    base.update(overrides)
    return base


def candidate(content_id, blended, **overrides):
    c = {"content_id": content_id, "blended_score": blended, "cf_score": 0.1,
         "cbf_score": 0.2, "rl_bonus": 0.2, "content_type": "video",
         "topics": ["trees"], "is_expansion": False}
    c.update(overrides)
    return c


class FakeRankRunnable:
    def __init__(self, parsed=None, error=None):
        self.parsed = parsed
        self.error = error
        self.payloads = []

    def invoke(self, payload):
        self.payloads.append(payload)
        if self.error:
            raise self.error
        return {"parsed": self.parsed, "raw": None}


# ── _merge_and_rank ──────────────────────────────────────────────────────────

@pytest.fixture
def five_items(session):
    add_content(session, title="Arrays", content_type=ContentType.VIDEO, topics=["arrays"])
    add_content(session, title="Trees", content_type=ContentType.ARTICLE, topics=["trees"],
                language="Java")
    add_content(session, title="Graphs", content_type=ContentType.TUTORIAL, topics=["graphs"])
    add_content(session, title="Sorting", content_type=ContentType.EXERCISE, topics=["sorting"])
    add_content(session, title="Hashing", content_type=ContentType.PROJECT, topics=["hashing"])
    return session


def test_merge_and_rank_ordering_is_pinned(five_items):
    ranked = _merge_and_rank(
        five_items,
        {1: 0.8, 2: 0.4, 4: 0.2, 5: 0.6},
        {1: 0.2, 2: 0.9, 4: 0.7, 5: 0.1},
        ctx(),
        {3: 0.8},
    )

    assert [c["content_id"] for c in ranked] == [2, 4, 1, 3, 5]
    assert [c["blended_score"] for c in ranked] == [0.745, 0.635, 0.62, 0.61, 0.505]


def test_merge_and_rank_reports_the_component_scores(five_items):
    ranked = _merge_and_rank(five_items, {1: 0.8}, {1: 0.2}, ctx(), {3: 0.8})
    by_id = {c["content_id"]: c for c in ranked}

    assert by_id[1]["cf_score"] == 0.8
    assert by_id[1]["cbf_score"] == 0.2
    # Nothing seen yet, so every type is equally unexplored and gets the full bonus.
    assert by_id[1]["rl_bonus"] == 0.2
    assert by_id[1]["is_expansion"] is False
    # Scored only by the expansion pass, and labelled so the prompt can rank it lower.
    assert by_id[3]["cbf_score"] == 0.8
    assert by_id[3]["is_expansion"] is True


def test_merge_and_rank_caps_each_content_type_at_three(session):
    for i in range(4):
        add_content(session, title=f"Video {i}", content_type=ContentType.VIDEO,
                    topics=[f"topic{i}"])
    add_content(session, title="Article", content_type=ContentType.ARTICLE,
                topics=["topic9"])

    ranked = _merge_and_rank(
        session, {}, {1: 0.9, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.5},
        ctx(preferred_languages=[]),
    )

    # The fourth video scores above the article but is held back by the type cap,
    # then re-appended behind it rather than dropped.
    assert [c["content_id"] for c in ranked] == [1, 2, 3, 5, 4]


# ── rank_with_llm ────────────────────────────────────────────────────────────

@pytest.fixture
def two_items(session):
    add_content(session, title="Trees 101", content_type=ContentType.VIDEO,
                topics=["trees"], url="https://example.com/1")
    add_content(session, title="Recursion drills", content_type=ContentType.EXERCISE,
                topics=["recursion"])
    return session


def test_rank_with_llm_returns_the_models_order_and_explanations(two_items):
    runnable = FakeRankRunnable(RankedRecommendations(
        summary="Shore up recursion before trees.",
        ranked=[
            RankedItem(id=2, title="Recursion drills", description="Ten drills.",
                       difficulty="beginner", why_relevant="Recursion is your weak area."),
            RankedItem(id=1, title="Trees 101", description="Traversals from scratch.",
                       difficulty="beginner", why_relevant="Trees is your stated topic."),
        ],
    ))

    result = rank_with_llm(
        two_items, ctx(), [candidate(1, 0.7), candidate(2, 0.6)],
        ["recursion"], ["arrays"], runnable=runnable,
    )

    assert result["ranked_ids"] == [2, 1]
    assert result["explanations"]["2"] == "Ten drills. Recursion is your weak area."
    assert result["descriptions"]["1"] == "Traversals from scratch."
    assert result["difficulties"]["1"] == "beginner"
    assert result["summary"] == "Shore up recursion before trees."
    assert result["tokens_used"] == 0
    assert result["model_used"] == settings.NVIDIA_MODEL


def test_rank_with_llm_prompt_keeps_the_profile_and_drops_the_json_instructions(two_items):
    runnable = FakeRankRunnable(RankedRecommendations(summary="s", ranked=[]))
    rank_with_llm(two_items, ctx(), [candidate(1, 0.7)], ["recursion"], ["arrays"],
                  runnable=runnable)

    system = dict(runnable.payloads[0])["system"]
    assert "beginner" in system
    assert "recursion" in system
    assert "off-by-one" in system
    assert "42%" in system
    assert "arrays: 90min" in system
    assert "JSON" not in system


def test_rank_with_llm_falls_back_to_score_order_when_the_model_is_unreachable(session):
    for i in range(1, 13):
        add_content(session, title=f"Item {i}", content_type=ContentType.VIDEO,
                    topics=["trees"])
    candidates = [candidate(i, round(1.0 - i / 100, 4)) for i in range(1, 13)]
    runnable = FakeRankRunnable(error=RuntimeError("provider refused"))

    result = rank_with_llm(session, ctx(), candidates, [], [], runnable=runnable)

    assert result["ranked_ids"] == list(range(1, TOP_N + 1))
    assert result["tokens_used"] == 0
    assert result["model_used"] == "fallback"
    assert result["explanations"] == {str(i): "" for i in range(1, TOP_N + 1)}
    summary = result["summary"].lower()
    assert "score" in summary and "explanation" in summary
    assert "provider refused" in summary


def test_rank_with_llm_falls_back_when_the_model_cannot_even_be_built(two_items, monkeypatch):
    """No runnable injected, so ranking builds its own model — and with no key it
    must degrade like any other failed call rather than escape as a 500."""
    # Real construction is the subject here, so this opts out of the suite-wide guard
    # in tests/conftest.py. Safe: the emptied key is what makes the client refuse to
    # be built, so nothing can reach a provider.
    monkeypatch.setattr("app.core.llm.ChatOpenAI", ChatOpenAI)
    monkeypatch.setattr(settings, "NVIDIA_API_KEY", "")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = rank_with_llm(two_items, ctx(), [candidate(1, 0.7)], [], [])

    assert result["ranked_ids"] == [1]
    assert result["model_used"] == "fallback"
    assert result["tokens_used"] == 0


def test_rank_with_llm_falls_back_when_nothing_could_be_parsed(two_items):
    result = rank_with_llm(two_items, ctx(), [candidate(1, 0.7)], [], [],
                           runnable=FakeRankRunnable(parsed=None))

    assert result["ranked_ids"] == [1]
    assert result["model_used"] == "fallback"
