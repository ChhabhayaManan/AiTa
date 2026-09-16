"""Tuning constants and the topic tables the recommendation stages share.

Kept in its own module so the stages can import them without importing each other
or the agent that orchestrates them.
"""

from typing import Dict, List

CF_WEIGHT   = 0.35   # collaborative filtering
CBF_WEIGHT  = 0.45   # content-based filtering (profile-driven)
RL_WEIGHT   = 0.20   # exploration bonus
TOP_N       = 10
CANDIDATE_K = 40

# topic → [prerequisites that should come first]
PREREQUISITES: Dict[str, List[str]] = {
    "linked lists":        ["arrays"],
    "trees":               ["linked lists", "recursion"],
    "graphs":              ["trees", "recursion"],
    "dynamic programming": ["recursion", "arrays"],
    "backtracking":        ["recursion"],
    "binary search":       ["arrays", "sorting"],
    "sliding window":      ["arrays", "two pointers"],
    "two pointers":        ["arrays"],
    "hashing":             ["arrays"],
    "stacks queues":       ["arrays"],
    "greedy":              ["sorting", "arrays"],
    "bit manipulation":    ["math"],
    "design patterns":     ["oop"],
    "system design":       ["databases", "oop"],
    "machine learning":    ["math", "python"],
    "react":               ["javascript", "web development"],
    "django":              ["python", "databases"],
    "spring":              ["java", "oop"],
}

# topic → adjacent topics to suggest when this topic is exhausted
TOPIC_ADJACENCY: Dict[str, List[str]] = {
    "arrays":              ["linked lists", "sorting", "binary search", "two pointers"],
    "linked lists":        ["arrays", "stacks queues", "trees"],
    "trees":               ["graphs", "dynamic programming", "recursion"],
    "graphs":              ["trees", "dynamic programming", "backtracking"],
    "dynamic programming": ["recursion", "greedy", "trees"],
    "recursion":           ["dynamic programming", "backtracking", "trees"],
    "sorting":             ["arrays", "binary search", "greedy"],
    "binary search":       ["arrays", "sorting", "two pointers"],
    "hashing":             ["arrays", "strings", "two pointers"],
    "stacks queues":       ["arrays", "linked lists", "trees"],
    "backtracking":        ["recursion", "dynamic programming", "graphs"],
    "greedy":              ["dynamic programming", "sorting", "arrays"],
    "bit manipulation":    ["math", "arrays", "dynamic programming"],
    "math":                ["bit manipulation", "dynamic programming", "greedy"],
    "strings":             ["arrays", "hashing", "dynamic programming"],
    "two pointers":        ["arrays", "binary search", "sliding window"],
    "sliding window":      ["arrays", "two pointers", "strings"],
    "oop":                 ["design patterns", "recursion"],
    "design patterns":     ["oop", "system design"],
    "python":              ["algorithms", "data structures"],
    "javascript":          ["web development", "react"],
    "java":                ["oop", "spring"],
}
