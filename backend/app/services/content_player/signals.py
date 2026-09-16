"""What the student's own message says about them.

Everything here reads the message and nothing else: no database, no model call. The
thresholds are the ones the agent has always used, kept exactly.
"""

import re
from typing import Optional

DIFFICULTY_LEVELS = ["easy", "medium", "hard", "expert"]

# An accuracy at or above this counts as a solve, and this many consecutive solves
# earns a harder problem.
SOLVED_ACCURACY = 70.0
SOLVE_STREAK_FOR_BUMP = 3

# A topic has to be mentioned in a message long enough to be about that topic, not
# one that happens to contain the word.
MIN_TOPIC_SWITCH_LENGTH = 50

_CODE_MARKERS = re.compile(r'def |class |#include|public static|function |=>|{|}')


def _get_difficulty_index(level: str) -> int:
    try:
        return DIFFICULTY_LEVELS.index(level.lower())
    except ValueError:
        return 1  # default medium


def _adjust_difficulty(current_level: str, comfort_signal: str) -> str:
    """
    Adjust difficulty based on user comfort.
    comfort_signal: 'too_easy' | 'comfortable' | 'struggling' | 'too_hard'
    """
    idx = _get_difficulty_index(current_level)
    if comfort_signal in ("too_easy",):
        idx = min(idx + 1, len(DIFFICULTY_LEVELS) - 1)
    elif comfort_signal in ("struggling", "too_hard"):
        idx = max(idx - 1, 0)
    return DIFFICULTY_LEVELS[idx]


TOPIC_KEYWORDS = {
    "arrays": ["array", "list", "subarray", "sliding window", "two pointer"],
    "linked_lists": ["linked list", "node", "pointer", "head", "tail", "next"],
    "trees": ["tree", "bst", "binary", "traversal", "root", "leaf", "graph", "dfs", "bfs"],
    "dynamic_programming": ["dp", "dynamic programming", "memoization", "tabulation", "subproblem"],
    "sorting": ["sort", "merge sort", "quick sort", "bubble", "insertion", "binary search"],
    "recursion": ["recursion", "recursive", "base case", "call stack", "fibonacci"],
    "hashing": ["hash", "dictionary", "map", "set", "collision", "hashmap"],
    "stacks_queues": ["stack", "queue", "deque", "lifo", "fifo", "push", "pop"],
    "backtracking": ["backtrack", "permutation", "combination", "n-queens", "sudoku"],
    "bit_manipulation": ["bit", "bitwise", "xor", "and", "or", "shift", "mask"],
    "greedy": ["greedy", "optimal", "local optimum", "activity selection"],
    "math": ["prime", "gcd", "lcm", "modulo", "factorial", "fibonacci"],
}


def _detect_topic_from_message(message: str) -> Optional[str]:
    """Detect if user message is strongly about a different topic."""
    msg_lower = message.lower()
    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in msg_lower)
        if score >= 2:  # Need at least 2 keyword matches to avoid false positives
            topic_scores[topic] = score
    if topic_scores:
        return max(topic_scores, key=topic_scores.get)
    return None


def _detect_comfort_signal(message: str) -> str:
    """Detect how comfortable the user is from their message."""
    msg_lower = message.lower()

    struggling_signals = [
        "don't understand", "confused", "lost", "what?", "huh", "i don't get",
        "this is hard", "too difficult", "not making sense", "can you explain again",
        "still confused", "not sure", "help me", "stuck"
    ]
    easy_signals = [
        "too easy", "already know", "boring", "trivial", "simple", "obviously",
        "that's basic", "i know this", "harder please", "next level", "more challenging"
    ]

    if any(s in msg_lower for s in struggling_signals):
        return "struggling"
    if any(s in msg_lower for s in easy_signals):
        return "too_easy"
    return "comfortable"


def _extract_accuracy_from_message(message: str) -> Optional[float]:
    """
    Extract accuracy percentage from a message like:
    'accuracy: 85%', 'score: 90', 'passed 9/10 test cases', etc.
    Returns float 0-100 or None if not found.
    """
    msg_lower = message.lower()

    # Pattern: "accuracy: 85%" or "score: 90%"
    m = re.search(r'(?:accuracy|score)[:\s]+(\d+(?:\.\d+)?)\s*%?', msg_lower)
    if m:
        return float(m.group(1))

    # Pattern: "passed 9/10" or "9 out of 10"
    m = re.search(r'(\d+)\s*(?:/|out of)\s*(\d+)', msg_lower)
    if m:
        passed, total = int(m.group(1)), int(m.group(2))
        if total > 0:
            return (passed / total) * 100

    # Pattern: "85%" standalone
    m = re.search(r'\b(\d{2,3})\s*%', msg_lower)
    if m:
        val = float(m.group(1))
        if 0 <= val <= 100:
            return val

    return None


def _has_code_submission(message: str, code_snippet: Optional[str] = None) -> bool:
    """A turn only counts as a submission when there is code in it — an accuracy
    number on its own is a student talking about a score, not handing one in."""
    return bool(code_snippet) or bool(_CODE_MARKERS.search(message))
