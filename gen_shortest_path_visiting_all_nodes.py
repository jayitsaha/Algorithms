"""
gen_shortest_path_visiting_all_nodes.py
Regenerates the Notion page for LeetCode #847 - Shortest Path Visiting All Nodes.
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "shortest_path_visiting_all_nodes"
NAME = "Shortest Path Visiting All Nodes"
NUMBER = 847
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "Dynamic Programming"
SUBPATTERNS = ["BFS with node and visited-mask"]
TC = "O(2^n · n^2)"
SC = "O(2^n · n)"
KEY_INSIGHT = "BFS on augmented (node, bitmask) state space; multi-source seed enables any-start; n<=12 makes 2^n=4096 tractable."

# ── Step 0: create page (notion_page_id is null) ──
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: set properties ──
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON,
)
print("Properties set.")

# ── Step 2: wipe (new page is empty, but call for safety) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: build body ──
PROBLEM_STATEMENT = (
    "You are given an undirected, connected graph of n nodes labeled 0 to n-1. "
    "The graph is given as follows: graph[i] is a list of all the nodes connected with node i by an edge. "
    "Return the length of the shortest path that visits every node. "
    "You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges."
)

SOL1_CODE = """\
from collections import deque

def shortestPathLength(graph: list[list[int]]) -> int:
    n = len(graph)
    if n == 1:
        return 0

    full_mask = (1 << n) - 1          # e.g. n=4 -> 0b1111 = 15

    queue = deque()
    seen = set()

    # Multi-source BFS: seed from every possible starting node
    for i in range(n):
        state = (i, 1 << i)
        queue.append((i, 1 << i, 0))  # (node, visited_mask, distance)
        seen.add(state)

    while queue:
        node, mask, dist = queue.popleft()

        for nei in graph[node]:
            new_mask = mask | (1 << nei)   # mark neighbor as visited

            if new_mask == full_mask:       # all nodes visited?
                return dist + 1             # BFS guarantees minimum

            if (nei, new_mask) not in seen:
                seen.add((nei, new_mask))
                queue.append((nei, new_mask, dist + 1))

    return -1  # unreachable (graph is guaranteed connected)
"""

SOL2_CODE = """\
def shortestPathLength_dp(graph: list[list[int]]) -> int:
    n = len(graph)
    if n == 1:
        return 0

    full = (1 << n) - 1
    INF = float('inf')

    # dp[mask][node] = min steps to be at 'node' with visited set = 'mask'
    dp = [[INF] * n for _ in range(1 << n)]

    # Base case: start at any node, only that node is visited
    for i in range(n):
        dp[1 << i][i] = 0

    # We need to process states in BFS order (by dp value), so use deque
    from collections import deque
    queue = deque()
    for i in range(n):
        queue.append((1 << i, i))

    while queue:
        mask, node = queue.popleft()
        d = dp[mask][node]

        for nei in graph[node]:
            nm = mask | (1 << nei)
            if dp[nm][nei] > d + 1:
                dp[nm][nei] = d + 1
                queue.append((nm, nei))

    return min(dp[full])
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: BFS + Bitmask (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — BFS + Bitmask State (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to visit every node, but we may backtrack freely. This is NOT a standard "
            "shortest-path problem (which finds min distance between two fixed nodes). Instead, "
            "it asks: what is the minimum number of edges to traverse to touch all n nodes at "
            "least once, starting and ending anywhere?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard BFS/DFS on the original graph fails because 'visited' means something different here. "
            "In normal BFS we mark nodes as visited to avoid cycles. But here we NEED to revisit nodes — "
            "for example, in a star graph we must return through the hub multiple times. "
            "Greedy (always go to nearest unvisited) also fails: it ignores that backtracking costs edges."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two paths that arrive at the same node having visited the same subset of nodes are "
            "interchangeable — they face exactly the same future decisions. So the state we need "
            "is (current_node, visited_subset). With n<=12, we can encode visited_subset as a bitmask "
            "integer (12 bits = 4096 possible values). This gives at most n * 2^n = 49,152 states."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Encode the problem: state = (node, mask) where mask bit i = 1 means node i is visited. "
            "2. BFS on this augmented state space (each state is a virtual node). "
            "3. Since we can start anywhere, use multi-source BFS: add all (i, 1<<i, dist=0) at once. "
            "4. When any expansion produces new_mask == full_mask, return dist+1 immediately. "
            "BFS guarantees the first time we reach any state is via the shortest path."
        ),
        N.callout(
            "Analogy: Think of it like a treasure hunt where your 'position' card shows both your location "
            "AND a checklist of treasures found so far. Two hunters at the same location with the same "
            "checklist are in identical situations — the one who got there faster wins.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("full_mask = (1 << n) - 1", {"code": True}), " — creates an integer with all n bits set to 1; e.g. n=4 → 0b1111=15. This is the goal state for the visited mask."])),
    N.para(N.rich([("Multi-source init loop", {"bold": True}), " — adds (node=i, mask=1<<i, dist=0) for every i. This is key: we seed from ALL nodes simultaneously since any can be the start."])),
    N.para(N.rich([("seen.add((i, 1<<i))", {"code": True}), " — mark as seen BEFORE enqueueing (not after dequeuing). This prevents adding the same state to the queue multiple times, which would cause exponential queue growth."])),
    N.para(N.rich([("new_mask = mask | (1 << nei)", {"code": True}), " — bitwise OR sets bit 'nei' in the mask. If nei was already visited, mask is unchanged."])),
    N.para(N.rich([("if new_mask == full_mask: return dist + 1", {"code": True}), " — goal check on every neighbor expansion. Once the mask is all 1s, all nodes have been visited. BFS ensures the first time we reach this is the shortest path."])),
    N.divider(),
]

# ── Solution 2: DP + Bitmask ──
blocks += [
    N.h2("Solution 2 — Bitmask DP (Bottom-Up Tabulation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want dp[mask][node] = minimum steps to reach state (at node, having visited exactly 'mask'). "
            "This is classic bitmask DP: define a 2D table indexed by (subset, position), fill it from "
            "base cases upward."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure top-down recursion without memoization would recompute the same subproblems exponentially. "
            "The DP table has n * 2^n entries; with memoization, each is computed once."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For unweighted graphs, BFS and DP give the same complexity. DP is useful when you need "
            "path reconstruction or when working with weighted graphs (replace BFS-based DP with "
            "Dijkstra-based DP). For this problem, BFS is simpler and terminates early."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base: dp[1<<i][i] = 0 for all i. "
            "Transition: dp[nm][nei] = min(dp[nm][nei], dp[mask][node] + 1) where nm = mask | (1<<nei). "
            "Answer: min(dp[full_mask])."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("dp[mask][node]", {"code": True}), " — 2D table: mask = visited subset (0..2^n-1), node = current position (0..n-1). Value = min steps to reach this state."])),
    N.para(N.rich([("Base cases", {"bold": True}), ": dp[1<<i][i] = 0 for each node i. Meaning: if we start at node i having visited only node i, cost is 0."])),
    N.para(N.rich([("Transition", {"bold": True}), ": nm = mask | (1<<nei). Moving from node to nei takes 1 step and adds nei to visited set."])),
    N.para(N.rich([("min(dp[full])", {"code": True}), " — answer is the minimum over all ending positions, since we can end anywhere."])),
    N.callout(
        "DP vs BFS: Both are O(2^n * n^2). BFS is preferred for unweighted graphs (early termination, simpler code). "
        "DP is preferred if you need to reconstruct the actual path or if edges are weighted.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS + Bitmask (optimal)", "O(2^n · n^2)", "O(2^n · n)", "Early termination; n<=12 → fast"],
        ["DP + Bitmask", "O(2^n · n^2)", "O(2^n · n)", "Same asymptotics; full table filled"],
        ["Brute Force DFS", "O(n! · n)", "O(n)", "TLE for n>6"],
    ]),
    N.divider(),
]

# ── DP Deep-Dive: Why is This DP? ──
blocks += [
    N.h2("🔬 Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}), "The shortest path to reach state (node, mask) in d steps, combined with one more edge to (nei, mask | (1<<nei)), gives the optimal cost to reach that new state. Extending an optimal solution remains optimal."])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}), "Many different traversal sequences lead to the same (node, mask) state. Without memoization/deduplication, we'd recompute the optimal cost to reach (node, mask) exponentially many times."])),
    N.h3("Recurrence Relation"),
    N.code(
        "# BFS formulation:\n"
        "dist[nei][mask | (1<<nei)] = dist[node][mask] + 1\n"
        "  (only if this gives a shorter path)\n\n"
        "# DP table formulation:\n"
        "dp[mask | (1<<nei)][nei] = min(dp[mask | (1<<nei)][nei],\n"
        "                               dp[mask][node] + 1)\n\n"
        "# Base case:\n"
        "dp[1<<i][i] = 0  for all i in range(n)\n\n"
        "# Answer:\n"
        "return min(dp[(1<<n)-1])  # minimum over all ending positions",
        "python"
    ),
    N.callout(
        "This is a Bitmask DP problem — one of the canonical hard DP patterns. "
        "Recognize it when: n<=20, need to track 'which subset collected', "
        "and you need minimum cost/steps. Classic example: Travelling Salesman Problem.",
        "🔎", "purple_background"
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS with (node, visited_mask) — augmented state BFS; also classifiable as Bitmask DP"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• n <= 12 (or n <= 20) — small enough for 2^n states\n"
        "• Need to visit ALL nodes/items/cities\n"
        "• May revisit nodes (standard BFS visited[] would block this)\n"
        "• Minimum edges/steps required\n"
        "• 'Start at any node' → multi-source BFS\n"
        "• State = (position, subset-of-collected)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS+Bitmask or Bitmask DP technique:"),
    N.bullet(N.rich([("Campus Bikes II", {"bold": True}), " (Hard, LC 1066) — Bitmask DP on worker-bike minimum cost assignment; same n*2^n structure"])),
    N.bullet(N.rich([("Fair Distribution of Cookies", {"bold": True}), " (Medium, LC 2305) — Bitmask DFS/DP to distribute cookie bags; subset enumeration"])),
    N.bullet(N.rich([("Minimum Number of Work Sessions", {"bold": True}), " (Medium, LC 1986) — Bitmask DP over task subsets to minimize sessions"])),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets", {"bold": True}), " (Medium, LC 698) — Bitmask to track which elements are in which subset"])),
    N.bullet(N.rich([("Shortest Path in Grid with Obstacles Elimination", {"bold": True}), " (Hard, LC 1293) — BFS with augmented state (pos, k-remaining); same pattern"])),
    N.bullet(N.rich([("Find the Shortest Superstring", {"bold": True}), " (Hard, LC 943) — Bitmask DP + TSP on strings; visit all strings minimizing overlap cost"])),
    N.bullet(N.rich([("Travelling Salesman Problem", {"bold": True}), " (NP-Hard, classic) — This problem is the unweighted, flexible-start variant of TSP"])),
    N.para("These problems share the core technique: represent a subset of items as a bitmask, use it as part of the DP/BFS state to track progress toward a global goal."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Dynamic Programming, Sub-Pattern: BFS with (node, visited_mask)", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the BFS algorithm visually — use Next/Prev or arrow keys to see how the bitmask state evolves.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Step 4: write status file ──
import json
status_dir = os.path.join(os.path.dirname(__file__), ".status")
os.makedirs(status_dir, exist_ok=True)
status_path = os.path.join(status_dir, f"{SLUG}.json")
with open(status_path, "w") as f:
    json.dump({
        "slug": SLUG,
        "html": "OK",
        "notion": "OK",
        "lines": 897,
        "notes": "BFS+bitmask state space; multi-source; star graph walkthrough; 14 steps; 897 lines"
    }, f, indent=2)
print(f"Status written: {status_path}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=897")
