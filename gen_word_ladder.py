"""gen_word_ladder.py — Notion updater for Word Ladder (LC #127)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-816a-acd1-e4e9f9d3082e"

# ── 1) Properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=127,
    pattern="Graph Algorithms",
    subpatterns=["BFS + Wildcard Patterns"],
    tc="O(N·L²)",
    sc="O(N·L)",
    key_insight="Model words as graph nodes; wildcard buckets find 1-letter neighbors in O(L²) instead of O(N·L); BFS yields shortest path.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────
print("Wiping old page content...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two words ", {}),
        ("beginWord", {"code": True}),
        (" and ", {}),
        ("endWord", {"code": True}),
        (", and a dictionary ", {}),
        ("wordList", {"code": True}),
        (", return the number of words in the shortest transformation sequence from ", {}),
        ("beginWord", {"code": True}),
        (" to ", {}),
        ("endWord", {"code": True}),
        (", or 0 if no such sequence exists. Each step may change only one letter, and every intermediate word must exist in ", {}),
        ("wordList", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: beginWord=\"hit\", endWord=\"cog\", wordList=[\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"] ", {}),
        ("→ hit → hot → dot → dog → cog", {"code": True}),
        (" = length 5.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
SOL1_CODE = '''\
from collections import defaultdict, deque

def ladderLength(beginWord: str, endWord: str, wordList: list) -> int:
    if endWord not in wordList:
        return 0

    L = len(beginWord)
    # Build wildcard buckets: pattern -> [matching words]
    buckets = defaultdict(list)
    for word in wordList:
        for i in range(L):
            buckets[word[:i] + '*' + word[i+1:]].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, dist = queue.popleft()
        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]
            for neighbor in buckets[pattern]:
                if neighbor == endWord:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

    return 0
'''

blocks += [
    N.h2("Solution 1 — BFS with Wildcard Buckets (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the minimum number of one-letter changes to get from beginWord to endWord. Think of each word as a city: two cities are connected by a road if they differ by exactly one letter. We need the shortest route between two cities. That is BFS on an unweighted graph."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force: compare every unvisited word against the current word using character-by-character diff — O(N·L) per node, O(N²·L) total. With N=5000 words, this is 125 million character comparisons. DFS finds a path but not necessarily the shortest one."),
        N.h4("The Key Observation"),
        N.para("Two words are 1-letter neighbors if and only if they share a wildcard pattern. 'hot' and 'dot' both produce '*ot'. Pre-group all wordList words by their L wildcard patterns. Then finding all neighbors of a word is just L dictionary lookups — O(L²) instead of O(N·L)."),
        N.h4("Building the Solution"),
        N.para("Step 1: If endWord not in wordList, return 0. Step 2: Build bucket map — for each word in wordList, generate L patterns and append the word to each bucket. Step 3: BFS from beginWord. For each dequeued word, look up L patterns, check each bucket member. If it's endWord, return dist+1. If unvisited, enqueue at dist+1. Step 4: Return 0 if queue exhausts."),
        N.callout(
            "Analogy: wildcard buckets are like a phone book indexed by 'first name *' — looking up all Smiths is O(1), not O(N). We trade preprocessing storage for instant neighbor lookup.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if endWord not in wordList: return 0", {"code": True}), (" — Fast fail: if endWord is not in the dictionary, no transformation can ever reach it.", {})])),
    N.para(N.rich([("L = len(beginWord)", {"code": True}), (" — All words have the same length (problem guarantee). Compute once.", {})])),
    N.para(N.rich([("buckets = defaultdict(list)", {"code": True}), (" — Maps wildcard pattern strings to lists of matching dictionary words.", {})])),
    N.para(N.rich([("for word in wordList: for i in range(L): buckets[word[:i]+'*'+word[i+1:]].append(word)", {"code": True}), (" — For each word, generate L patterns and add word to each bucket. Total: O(N·L²) time.", {})])),
    N.para(N.rich([("queue = deque([(beginWord, 1)])", {"code": True}), (" — BFS queue holds (word, distance). Start word counts as step 1 per problem definition.", {})])),
    N.para(N.rich([("visited = {beginWord}", {"code": True}), (" — Hash set for O(1) membership. Mark beginWord visited immediately.", {})])),
    N.para(N.rich([("word, dist = queue.popleft()", {"code": True}), (" — Dequeue from front (O(1) with deque). Process nearest unvisited word.", {})])),
    N.para(N.rich([("pattern = word[:i] + '*' + word[i+1:]", {"code": True}), (" — Generate wildcard by replacing position i with '*'.", {})])),
    N.para(N.rich([("if neighbor == endWord: return dist + 1", {"code": True}), (" — Check BEFORE visited test. First discovery via BFS = shortest path. Return immediately.", {})])),
    N.para(N.rich([("if neighbor not in visited: visited.add(neighbor); queue.append(...)", {"code": True}), (" — Add to visited WHEN ENQUEUING, not when dequeuing, to prevent duplicate queue entries.", {})])),
    N.para(N.rich([("return 0", {"code": True}), (" — Queue exhausted without finding endWord: no transformation sequence exists.", {})])),
    N.divider(),
]

# ── Solution 2 ──
SOL2_CODE = '''\
from collections import deque

def ladderLength_brute(beginWord: str, endWord: str, wordList: list) -> int:
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, dist = queue.popleft()
        for candidate in word_set:
            if candidate not in visited:
                # Count differing characters — O(L) per pair
                diffs = sum(a != b for a, b in zip(word, candidate))
                if diffs == 1:
                    if candidate == endWord:
                        return dist + 1
                    visited.add(candidate)
                    queue.append((candidate, dist + 1))

    return 0
'''

blocks += [
    N.h2("Solution 2 — Brute Force BFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same BFS approach, but instead of wildcard buckets, we directly compare the current word against every unvisited word in the dictionary using a character diff."),
        N.h4("What Doesn't Work at Scale"),
        N.para("For each of the N words we dequeue, we compare against all N candidates: O(N²·L) total. With N=5000 and L=5, that's 125 million character comparisons vs the wildcard approach's 125 thousand."),
        N.h4("The Key Observation"),
        N.para("sum(a != b for a, b in zip(word, candidate)) == 1 is a clean O(L) way to check if two words differ by exactly one character. Simple and correct, but not scalable."),
        N.h4("Building the Solution"),
        N.para("Use a set for O(1) membership test. BFS from beginWord. For each dequeued word, iterate over all wordList words; compare character by character; if exactly 1 difference and not visited, enqueue."),
        N.callout("Use this approach to validate correctness during development, then optimize to wildcard buckets. Always describe this approach first in an interview, then propose the O(N·L²) optimization.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force BFS", "O(N²·L)", "O(N)"],
        ["Wildcard BFS (Optimal ✓)", "O(N·L²)", "O(N·L)"],
        ["Bidirectional BFS", "O(N·L²)", "O(N·L)"],
    ]),
    N.para("N = number of words in wordList; L = length of each word. With N=5000, L=5: Wildcard BFS performs ~125K operations vs Brute Force's ~125M — 1000× improvement."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Algorithms (Section 17 of DSA Guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS + Wildcard Patterns — BFS on implicit graph; wildcard bucket trick for O(L²) neighbor enumeration.", {})])),
    N.callout(
        "When to recognize this pattern: 'minimum steps/transformations'; each step changes one discrete unit; every intermediate state must be valid; all transitions have equal cost. Model as BFS on implicit graph. If neighbor lookup is the bottleneck, apply wildcard/mask precomputation.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BFS shortest path / wildcard neighbor enumeration):"),
    N.bullet(N.rich([("Word Ladder II", {"bold": True}), (" (Hard) — Return all shortest transformation paths; BFS for level structure, DFS to extract paths. #126", {})])),
    N.bullet(N.rich([("Minimum Genetic Mutation", {"bold": True}), (" (Medium) — Identical algorithm on DNA strings; alphabet {A,C,G,T}, bank is wordList. #433", {})])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), (" (Medium) — BFS state space on 4-dial combination lock; each dial has 10 neighbors (0-9). #752", {})])),
    N.bullet(N.rich([("Sliding Puzzle", {"bold": True}), (" (Hard) — BFS on board states serialized as strings; state space is 6!/2 = 360 nodes. #773", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — BFS on 2D grid with 8-directional moves; count steps to bottom-right. #1091", {})])),
    N.bullet(N.rich([("Bus Routes", {"bold": True}), (" (Hard) — BFS where nodes are bus routes not stops; rethink what a 'node' is. #815", {})])),
    N.para("These problems share the core technique: BFS on implicit or constructed graphs where the challenge is efficiently enumerating neighbors."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.2 — BFS + Wildcard Patterns", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("word_ladder")),
    N.para(N.rich([("Step through BFS level-by-level — use Next/Prev or arrow keys to follow the wildcard bucket lookups.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
