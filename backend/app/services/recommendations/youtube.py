import logging
import re
from collections import Counter
from typing import Dict, List, Tuple

import httpx
from sqlalchemy.orm import Session

from app.models.recommendation import Content

logger = logging.getLogger(__name__)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

# topic → skills gained
TOPIC_SKILLS: Dict[str, List[str]] = {
    "arrays":              ["array manipulation", "problem solving", "DSA"],
    "linked lists":        ["pointer logic", "DSA", "memory management"],
    "trees":               ["tree traversal", "recursion", "DSA"],
    "graphs":              ["graph traversal", "BFS", "DFS", "shortest path"],
    "dynamic programming": ["memoization", "tabulation", "optimization"],
    "recursion":           ["recursive thinking", "base cases", "call stack"],
    "sorting":             ["comparison sorts", "divide and conquer", "DSA"],
    "hashing":             ["hash maps", "collision handling", "O(1) lookup"],
    "stacks queues":       ["LIFO/FIFO", "monotonic stack", "BFS"],
    "backtracking":        ["state space search", "pruning", "combinatorics"],
    "bit manipulation":    ["bitwise ops", "XOR tricks", "space optimization"],
    "greedy":              ["greedy choice", "interval scheduling", "optimization"],
    "math":                ["number theory", "modular arithmetic", "combinatorics"],
    "strings":             ["string matching", "sliding window", "pattern search"],
    "two pointers":        ["two pointer technique", "in-place algorithms"],
    "sliding window":      ["window management", "subarray problems"],
    "oop":                 ["classes", "inheritance", "polymorphism", "encapsulation"],
    "design patterns":     ["SOLID principles", "software architecture", "reusability"],
    "databases":           ["SQL", "normalization", "indexing", "query optimization"],
    "web development":     ["HTML", "CSS", "JavaScript", "REST APIs"],
    "machine learning":    ["supervised learning", "model training", "scikit-learn"],
    "system design":       ["scalability", "microservices", "caching", "load balancing"],
}

_DIFF_MAP = {
    "easy": "beginner", "beginner": "beginner",
    "medium": "intermediate", "intermediate": "intermediate",
    "hard": "advanced", "advanced": "advanced",
}
_TYPE_ROTATION = ["video", "tutorial", "article", "exercise", "project"]


class YouTubeSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        if not self.api_key:
            return []
        try:
            r = httpx.get(
                f"{YOUTUBE_API_URL}/search",
                params={"part": "snippet", "q": query + " tutorial",
                        "type": "video", "maxResults": max_results,
                        "relevanceLanguage": "en", "videoDuration": "medium",
                        "key": self.api_key},
                timeout=6.0,
            )
            r.raise_for_status()
            items = r.json().get("items", [])
            if not items:
                return []

            ids = [i["id"]["videoId"] for i in items]
            sr = httpx.get(
                f"{YOUTUBE_API_URL}/videos",
                params={"part": "statistics,contentDetails,snippet",
                        "id": ",".join(ids), "key": self.api_key},
                timeout=6.0,
            )
            sr.raise_for_status()
            stat_map = {v["id"]: v for v in sr.json().get("items", [])}

            videos = []
            for item in items:
                vid = item["id"]["videoId"]
                s   = stat_map.get(vid, {})
                st  = s.get("statistics", {})
                sn  = s.get("snippet", item.get("snippet", {}))
                views = int(st.get("viewCount", 0))
                likes = int(st.get("likeCount", 0))
                dur   = self._parse_duration(s.get("contentDetails", {}).get("duration", "PT0M"))
                q     = round(min(views/1_000_000, 1)*0.5 + min(likes/50_000, 1)*0.3 + 0.2, 4)
                videos.append({
                    "id": vid, "title": sn.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumbnail": sn.get("thumbnails", {}).get("medium", {}).get("url"),
                    "channel": sn.get("channelTitle", ""),
                    "views": views, "likes": likes,
                    "duration_mins": dur, "quality_score": q,
                })
            videos.sort(key=lambda v: v["quality_score"], reverse=True)
            return videos
        except Exception:
            # An empty list here is indistinguishable from "no results", and the rows
            # it leaves behind keep url=None forever. An operator reading quota
            # exhaustion or a schema change out of this needs the query and the cause.
            logger.warning("YouTube search failed for %r", query, exc_info=True)
            return []

    def _parse_duration(self, iso: str) -> float:
        h = re.search(r'(\d+)H', iso)
        m = re.search(r'(\d+)M', iso)
        s = re.search(r'(\d+)S', iso)
        return round(
            (int(h.group(1)) * 60 if h else 0) +
            (int(m.group(1)) if m else 0) +
            (int(s.group(1)) / 60 if s else 0), 1
        )


def _generate_content_for_profile(
    db: Session, yt: YouTubeSearchTool, user_ctx: Dict
) -> Tuple[int, int]:
    """Creates Content rows from the user's profile topics and languages.

    Two-phase: rows are inserted first so the pipeline is not blocked on YouTube,
    then the URLs are backfilled best-effort.

    Returns (created, linked). They differ whenever the backfill failed, and the two
    numbers are reported separately: a row with no URL is not a video the student can
    watch, so counting it as one would be the step log lying about the outcome.
    """
    topics    = user_ctx["interested_topics"] or []
    languages = user_ctx["preferred_languages"] or ["python"]
    skill     = user_ctx["skill_level"]
    diff_pref = user_ctx["difficulty_pref"]

    target_diff = _DIFF_MAP.get(diff_pref, _DIFF_MAP.get(skill, "intermediate"))
    diff_ladder = {
        "beginner":     ["beginner", "intermediate"],
        "intermediate": ["beginner", "intermediate", "advanced"],
        "advanced":     ["intermediate", "advanced"],
    }
    difficulties = diff_ladder.get(target_diff, ["intermediate"])

    # Load existing content in-memory to avoid JSON LIKE queries
    existing_rows = db.query(
        Content.title, Content.language, Content.difficulty, Content.topics
    ).filter(Content.is_active.is_(True)).all()

    combo_counts: Counter = Counter()
    existing_titles: set  = set()
    for row in existing_rows:
        existing_titles.add(row.title)
        row_lang = (row.language or "").lower()
        row_diff = (row.difficulty.value if hasattr(row.difficulty, "value") else str(row.difficulty)).lower()
        for t in (row.topics or []):
            combo_counts[(t.lower(), row_lang, row_diff)] += 1

    created   = 0
    new_items = []

    # Phase 1: insert rows immediately (no YouTube — keeps it fast)
    for topic_raw in topics:
        topic         = topic_raw.lower().replace("_", " ")
        skills_gained = TOPIC_SKILLS.get(topic_raw.lower(), [topic, "problem solving"])

        for lang in languages[:3]:
            lang_lower = lang.lower()
            for difficulty in difficulties:
                if combo_counts.get((topic, lang_lower, difficulty.lower()), 0) >= 2:
                    continue
                title = f"{topic.title()} — {lang.title()} ({difficulty.title()})"[:500]
                if title in existing_titles:
                    continue
                content_type = _TYPE_ROTATION[created % len(_TYPE_ROTATION)]
                c = Content(
                    title=title,
                    description=f"Learn {topic} in {lang} at {difficulty} level.",
                    content_type=content_type, difficulty=difficulty,
                    language=lang.title(), topics=[topic],
                    skills_gained=skills_gained, source="YouTube",
                    avg_rating=4.5, duration_mins=30,
                    url=None, thumbnail_url=None, author=None, is_active=True,
                )
                db.add(c)
                new_items.append((c, topic, lang, difficulty))
                existing_titles.add(title)
                combo_counts[(topic, lang_lower, difficulty.lower())] += 1
                created += 1

    if created > 0:
        db.commit()

    # Phase 2: backfill YouTube URLs (best-effort, non-blocking)
    updated = 0
    if yt.api_key and new_items:
        for content_obj, topic, lang, difficulty in new_items:
            query = f"{topic} {lang} {difficulty} tutorial"
            try:
                videos = yt.search(query, max_results=2)
                if videos:
                    best = videos[0]
                    content_obj.url           = best["url"]
                    content_obj.thumbnail_url = best["thumbnail"]
                    content_obj.author        = best["channel"]
                    if best["title"]:
                        content_obj.title = best["title"][:500]
                    if best["duration_mins"]:
                        content_obj.duration_mins = best["duration_mins"]
                    updated += 1
            except Exception:
                logger.warning("YouTube backfill failed for content %s (%r)",
                               content_obj.id, query, exc_info=True)
        if updated > 0:
            db.commit()
        if updated < len(new_items):
            logger.warning(
                "YouTube backfill linked %d of %d new items; the rest have no url",
                updated, len(new_items),
            )
    elif new_items:
        logger.warning("No YouTube API key configured; %d new items have no url",
                       len(new_items))

    return created, updated
