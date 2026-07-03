"""
gen_open_the_lock.py — Notion update for LeetCode #752 Open the Lock
Run: python3 gen_open_the_lock.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e9-b7bc-c62b7df5bbaa"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=752,
    pattern="Graph",
    subpatterns=["BFS State Space"],
    tc="O(10^4 + D)",
    sc="O(10^4 + D)",
    key_insight="Model each 4-digit combination as a graph node; BFS from 0000 finds minimum turns while deadends are pre-poisoned into visited.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "You have a lock with four circular wheels, each displaying digits 0–9. The lock starts at ",
        ("\"0000\"", {"code": True}),
        ". You want to reach the ",
        ("target", {"code": True}),
        " combination using the minimum number of turns. One turn = rotate one wheel by one digit up or down (wrapping: 9→0 and 0→9). Some combinations are ",
        ("deadends", {"code": True}),
        " — if the lock ever shows a deadend it locks permanently. Return the minimum turns to reach target, or -1 if impossible."
    ])),
    N.divider(),
]

# ── Solution 1: BFS ──
SOLUTION_1_CODE = '''from collections import deque

def openLock(deadends: list, target: str) -> int:
    dead = set(deadends)            # O(1) lookup
    if "0000" in dead: return -1   # can't start
    if target == "0000": return 0  # already there
    queue = deque([("0000", 0)])
    visited = dead | {"0000"}      # pre-poison deadends
    while queue:
        state, steps = queue.popleft()
        for i in range(4):         # each of 4 wheels
            d = int(state[i])
            for delta in [1, -1]:  # up or down
                new_d = (d + delta) % 10
                nb = state[:i] + str(new_d) + state[i+1:]
                if nb == target:
                    return steps + 1   # BFS = minimum guaranteed
                if nb not in visited:
                    visited.add(nb)    # mark at enqueue, not dequeue
                    queue.append((nb, steps + 1))
    return -1  # no path found'''

blocks += [
    N.h2("Solution 1 — BFS on State Space (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are navigating from one configuration to another on a graph. Each of the 10,000 possible 4-digit combinations is a node. Two nodes are adjacent if they differ by one wheel turn. Deadends are nodes we cannot visit. We want the shortest path from '0000' to target."),
        N.h4("What Doesn't Work"),
        N.para("DFS explores paths greedily without any guarantee of finding the shortest one. It might find a 50-turn path before discovering a 6-turn path, giving a wrong answer. We need an approach that finds the shortest path, not just any path."),
        N.h4("The Key Observation"),
        N.para("BFS processes all states reachable in k turns before any state reachable in k+1 turns. This means the FIRST time BFS reaches the target, it is via the shortest possible path. Since all edges cost exactly 1 (each turn is one step), BFS is the perfect tool."),
        N.h4("Building the Solution"),
        N.para("1. Model as graph: nodes = 4-digit strings, edges = single-wheel turns. 2. Deadends become unreachable nodes — add them to visited before BFS starts (pre-poisoning). 3. Generate 8 neighbors per state (4 wheels × 2 directions) using (digit ± 1) % 10 for wrapping. 4. When any neighbor equals target, return steps + 1 immediately."),
        N.callout(
            "Analogy: Think of a maze. BFS explores outward in rings from the start. The first ring is everything 1 step away, second ring is 2 steps away. The moment target appears in any ring, that ring number is the answer. Deadends are walls you can never pass through.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dead = set(deadends)", {"code": True}), " — Convert list to set for O(1) membership checks. Crucial: list lookup would be O(D) per neighbor check."])),
    N.para(N.rich([("if \"0000\" in dead: return -1", {"code": True}), " — Edge case: if the starting position is itself a deadend, we can't even begin. Return -1 immediately."])),
    N.para(N.rich([("if target == \"0000\": return 0", {"code": True}), " — Edge case: already at target, zero turns needed."])),
    N.para(N.rich([("queue = deque([(\"0000\", 0)])", {"code": True}), " — BFS queue stores (state_string, turns_taken_so_far). Using deque gives O(1) popleft."])),
    N.para(N.rich([("visited = dead | {\"0000\"}", {"code": True}), " — Pre-poison: union of deadends and start. Now BFS naturally skips deadends — no separate check needed in the loop."])),
    N.para(N.rich([("state, steps = queue.popleft()", {"code": True}), " — Dequeue oldest entry (fewest turns). BFS FIFO property guarantees we process shorter paths first."])),
    N.para(N.rich([("for i in range(4):", {"code": True}), " — Iterate over each of the 4 wheel positions."])),
    N.para(N.rich([("for delta in [1, -1]:", {"code": True}), " — Try turning up (+1) and turning down (-1)."])),
    N.para(N.rich([("new_d = (d + delta) % 10", {"code": True}), " — Modular arithmetic handles wrapping: 9+1→0 and 0-1→9 (Python modulo is always non-negative)."])),
    N.para(N.rich([("nb = state[:i] + str(new_d) + state[i+1:]", {"code": True}), " — String slicing to build the neighbor: keep prefix, replace digit i, keep suffix."])),
    N.para(N.rich([("if nb == target: return steps + 1", {"code": True}), " — BFS guarantees: first time we reach target = minimum steps. Return immediately."])),
    N.para(N.rich([("if nb not in visited:", {"code": True}), " — This single check handles BOTH deadend avoidance AND cycle prevention, because deadends were pre-added to visited."])),
    N.para(N.rich([("visited.add(nb)", {"code": True}), " — Mark visited at ENQUEUE time. If we waited for dequeue, the same state could be added to queue multiple times."])),
    N.para(N.rich([("queue.append((nb, steps + 1))", {"code": True}), " — Enqueue with incremented step count. This neighbor will be processed in the next BFS wave."])),
    N.para(N.rich([("return -1", {"code": True}), " — Queue exhausted without finding target = no valid path exists through the deadend minefield."])),
    N.divider(),
]

# ── Solution 2: Bidirectional BFS ──
SOLUTION_2_CODE = '''def openLock_bidir(deadends: list, target: str) -> int:
    dead = set(deadends)
    if "0000" in dead or target in dead: return -1
    if target == "0000": return 0
    front, back = {"0000"}, {target}  # two expanding frontiers
    visited = dead | {"0000"}
    steps = 0
    while front:
        # Always expand the smaller frontier for efficiency
        if len(front) > len(back):
            front, back = back, front
        nxt = set()
        for state in front:
            for i in range(4):
                d = int(state[i])
                for delta in [1, -1]:
                    nb = state[:i] + str((d + delta) % 10) + state[i+1:]
                    if nb in back:
                        return steps + 1  # frontiers met!
                    if nb not in visited:
                        visited.add(nb)
                        nxt.add(nb)
        front = nxt
        steps += 1
    return -1'''

blocks += [
    N.h2("Solution 2 — Bidirectional BFS (Advanced Optimization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Standard BFS expands outward from one end. Bidirectional BFS simultaneously expands from both the start ('0000') and the target, meeting somewhere in the middle."),
        N.h4("What Doesn't Work"),
        N.para("Standard BFS explores O(b^d) nodes where b=8 neighbors per node and d=answer. For a target requiring 6 turns, that's 8^6 ≈ 262,144 nodes. But the real state space caps at 10,000, so in practice standard BFS is already fine."),
        N.h4("The Key Observation"),
        N.para("If you expand from both ends simultaneously, each frontier only needs to grow to roughly O(b^(d/2)) before they meet. Two frontiers of size b^3 = 512 each vs one frontier of b^6 = 262,144. This is the bidirectional BFS advantage."),
        N.h4("Building the Solution"),
        N.para("Maintain two sets: front (expanding from start) and back (expanding from target). Each iteration, expand the smaller frontier. When any newly generated neighbor appears in the OTHER frontier, the frontiers have met — return steps + 1."),
        N.callout("Always expand the smaller frontier: if len(front) > len(back), swap them. This is the key optimization that balances the two sides and minimizes total work.", "⚡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("front, back = {\"0000\"}, {target}", {"code": True}), " — Two frontier sets. front expands from start, back represents the target side. Initially, start has one state and so does target."])),
    N.para(N.rich([("if len(front) > len(back): front, back = back, front", {"code": True}), " — Always expand the smaller set. This balances both sides and gives the O(b^(d/2)) advantage."])),
    N.para(N.rich([("if nb in back: return steps + 1", {"code": True}), " — The frontiers met! Any neighbor that exists in the opposite frontier completes the path. Return current steps + 1."])),
    N.para(N.rich([("front = nxt; steps += 1", {"code": True}), " — Replace front with its expansion. Increment step count for the next iteration."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Standard BFS", "O(10^4 + D)", "O(10^4 + D)"],
        ["Bidirectional BFS", "O(10^2 × 8) in practice", "O(10^2)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS State Space — shortest path where nodes are encoded states and edges are state transitions"])),
    N.callout(
        "When to recognize this pattern: 'minimum steps/turns/moves', 'starting state', 'target state', 'forbidden/blocked states', 'all transitions cost 1'. The state (here: 4-char string) becomes a graph node; BFS finds the shortest path.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS State Space technique:"),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), " (Hard) — BFS where state = word, transition = change one letter; word bank restricts valid states (#127)"])),
    N.bullet(N.rich([("Minimum Genetic Mutation", {"bold": True}), " (Medium) — BFS on gene strings; only mutations in the gene bank are valid transitions (#433)"])),
    N.bullet(N.rich([("Snakes and Ladders", {"bold": True}), " (Medium) — BFS on board positions; snakes/ladders create teleport edges (#909)"])),
    N.bullet(N.rich([("Sliding Puzzle", {"bold": True}), " (Hard) — BFS on all permutations of a 2×3 board; swap = transition (#773)"])),
    N.bullet(N.rich([("Minimum Knight Moves", {"bold": True}), " (Medium) — BFS on 2D grid coordinates; 8 knight moves = 8 edges per node (#1197)"])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}), " (Hard) — BFS on array indices; same-value positions create long-range edges (#1345)"])),
    N.para("These problems share the core technique: encode state as a hashable object, use BFS to find shortest path, use visited set to avoid cycles and deadends."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Graph) → BFS State Space", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("open_the_lock")),
    N.para(N.rich([("Step through the BFS algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append everything ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} blocks to {PAGE_ID}")
