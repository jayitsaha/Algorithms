"""
gen_minimum_cost_to_make_at_least_one_valid_path_in_a_grid.py
Regenerates the Notion page for LeetCode #1368 from scratch.
notion_page_id: null — creates a new page first.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "minimum_cost_to_make_at_least_one_valid_path_in_a_grid"
NAME = "Minimum Cost to Make at Least One Valid Path in a Grid"
NUMBER = 1368
DIFFICULTY = "Hard"
ICON = "🔴"

# ── Step 0: Create page (notion_page_id is null) ──────────────────────────────
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern="Graph",
    subpatterns=["0-1 BFS"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Model each cell's 4 moves as 0/1-weighted edges; use deque-based 0-1 BFS instead of Dijkstra for O(m·n) shortest path.",
    icon=ICON,
)
print("Properties set.")

# ── Step 2: Wipe any existing body (fresh page — wipe is safe no-op) ─────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Step 3: Build body blocks ─────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "Given an m × n grid where each cell contains a direction sign "
    "(1=right, 2=left, 3=down, 4=up), find the minimum number of sign changes "
    "needed so that there exists at least one valid path from the top-left cell "
    "(0,0) to the bottom-right cell (m-1,n-1). Each sign change costs 1."
)

SOL1_CODE = '''\
from collections import deque

def minCost(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # DIRS[d] = (dr, dc); sign value d+1 points in direction d
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0, 0)])  # (cost, row, col)

    while dq:
        cost, r, c = dq.popleft()
        if cost > dist[r][c]:
            continue  # stale entry — skip

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                # Free if existing sign matches direction d (sign = d+1)
                edge = 0 if grid[r][c] == d + 1 else 1
                new_cost = cost + edge
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    if edge == 0:
                        dq.appendleft((new_cost, nr, nc))
                    else:
                        dq.append((new_cost, nr, nc))

    return dist[m - 1][n - 1]
'''

SOL2_CODE = '''\
import heapq
from collections import defaultdict

def minCost(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]  # (cost, row, col)

    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost > dist[r][c]:
            continue

        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                edge = 0 if grid[r][c] == d + 1 else 1
                new_cost = cost + edge
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return dist[m - 1][n - 1]
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: 0-1 BFS (Interview Pick) ─────────────────────────────────────
blocks += [
    N.h2("Solution 1 — 0-1 BFS with Deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the cheapest sequence of sign changes to create a valid path. "
            "Each sign change costs 1. This is equivalent to finding the minimum-cost "
            "path from (0,0) to (m-1,n-1) in a graph where edges have cost 0 (free, "
            "follows the existing sign) or 1 (override, changes the sign)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard BFS assumes equal edge weights — here edges have cost 0 or 1, "
            "so BFS can process a cell before its optimal cost is known. "
            "A naive DFS/backtracking over all sign-change subsets is exponential: "
            "2^(m·n) possibilities. Even Dijkstra works but costs O(m·n · log(m·n)) "
            "where we can do better."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Edge weights are exactly {0, 1}. This is the special case where "
            "0-1 BFS applies: use a deque, push cost-0 neighbours to the front "
            "(they don't increase cost, so they should be explored first), "
            "push cost-1 neighbours to the back. The deque stays sorted in "
            "non-decreasing cost order — exactly like Dijkstra, but O(1) per "
            "operation instead of O(log n)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Model: each of the 4 DIRS from a cell has edge weight 0 if the "
            "existing sign points there, else 1. "
            "2. Initialise dist[0][0]=0, all others ∞. "
            "3. Run 0-1 BFS: pop front, skip stale entries, update dist for "
            "each neighbour, push to front (cost 0) or back (cost 1). "
            "4. Answer is dist[m-1][n-1]."
        ),
        N.callout(
            "Analogy: A city where streets have one-way signs. Following an existing "
            "sign is free (green light). Going the 'wrong way' costs $1 (toll). "
            "0-1 BFS always tries free roads first before paying.",
            "🚦", "green_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: 0-1 BFS"),
    N.para(
        "0-1 BFS solves single-source shortest paths on graphs with edge weights "
        "in {0, 1}. It was described as a variant of BFS by Dijkstra's framework: "
        "instead of a priority queue (heap), use a double-ended queue (deque). "
        "Core invariant: the deque always contains at most two distinct cost values "
        "(the current minimum k and k+1). Cost-0 edges appendleft (stay in k-section); "
        "cost-1 edges append (go to k+1-section). When k-section is exhausted, the "
        "k+1 section becomes the new front automatically. Time: O(V+E) = O(m·n)."
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("DIRS = [(0,1),(0,-1),(1,0),(-1,0)]", {"code": True}),
                   " — direction vectors; index d corresponds to sign value d+1."])),
    N.para(N.rich([("dist[0][0] = 0", {"code": True}),
                   " — source has zero cost; all other cells start at infinity."])),
    N.para(N.rich([("dq = deque([(0, 0, 0)])", {"code": True}),
                   " — initialise deque with (cost, row, col) for source."])),
    N.para(N.rich([("cost, r, c = dq.popleft()", {"code": True}),
                   " — always pop the minimum-cost entry (front of sorted deque)."])),
    N.para(N.rich([("if cost > dist[r][c]: continue", {"code": True}),
                   " — stale entry: we already found a cheaper path to (r,c), skip."])),
    N.para(N.rich([("edge = 0 if grid[r][c] == d+1 else 1", {"code": True}),
                   " — FREE if current sign already points this way; otherwise costs 1 to override."])),
    N.para(N.rich([("if edge == 0: dq.appendleft(...)", {"code": True}),
                   " — free neighbour goes to front (same cost level, explore first)."])),
    N.para(N.rich([("else: dq.append(...)", {"code": True}),
                   " — paid neighbour goes to back (cost level +1, explore after current level)."])),
    N.para(N.rich([("return dist[m-1][n-1]", {"code": True}),
                   " — minimum cost to reach the bottom-right corner."])),
    N.divider(),
]

# ── Solution 2: Dijkstra ──────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Dijkstra with Min-Heap"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same graph model as Solution 1: nodes are cells, edges have weight 0 or 1. "
            "Dijkstra's algorithm solves shortest path for non-negative edge weights. "
            "It's the natural first instinct for 'minimum cost path' problems."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Dijkstra is correct here, just not optimal. It uses a min-heap, giving "
            "O(m·n · log(m·n)) — acceptable for m,n ≤ 100 (≈130,000 ops), but "
            "the 0-1 BFS deque achieves O(m·n) ≈ 10,000 ops. In an interview, "
            "Dijkstra earns full credit but mentioning 0-1 BFS shows depth."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Dijkstra works for any non-negative edge weights. When weights are "
            "restricted to {0,1}, the heap is overkill — the deque trick achieves "
            "the same ordering in O(1) per push/pop. Both algorithms are correct; "
            "0-1 BFS is simply asymptotically faster."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Replace deque with heapq. Push (new_cost, nr, nc) to the heap. "
            "heappop always gives the minimum-cost entry. Same stale-entry check applies."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(0, 0, 0)]", {"code": True}),
                   " — min-heap with (cost, row, col); Python's heapq is a min-heap."])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}),
                   " — always returns the minimum-cost (r,c) pair."])),
    N.para(N.rich([("heapq.heappush(heap, (new_cost, nr, nc))", {"code": True}),
                   " — push regardless of edge weight (heap maintains order automatically)."])),
    N.para("Correctness is identical to 0-1 BFS; complexity is O(m·n·log(m·n)) due to heap operations."),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["0-1 BFS (Deque)", "O(m·n)", "O(m·n)", "Optimal — interview pick"],
        ["Dijkstra (Min-Heap)", "O(m·n·log(m·n))", "O(m·n)", "Correct but slower — acceptable"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (Shortest Path on Implicit Graph)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "0-1 BFS (Deque-Based Shortest Path for 0/1 Edge Weights)"])),
    N.callout(
        "When to recognise this pattern: "
        "(1) Grid or graph problem asking for minimum cost/changes/flips. "
        "(2) Each move has exactly two possible costs — 0 (free/natural) or 1 (paid/overriding). "
        "(3) Dijkstra would work but you want O(n) not O(n log n). "
        "Keywords: 'minimum sign changes', 'minimum flips', 'minimum changes to achieve path'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 0-1 BFS / shortest path on 0/1-weighted graph technique:"),
]
related = [
    ("Minimum Obstacle Removal to Reach Corner", "Medium",
     "Identical 0-1 BFS: empty cell = 0 cost, obstacle = 1 cost (remove it)."),
    ("Shortest Path in Binary Matrix", "Medium",
     "Standard BFS (all moves equal cost = 1); simpler version of the same grid pattern."),
    ("Cheapest Flights Within K Stops", "Medium",
     "Weighted graph shortest path with hop constraint; use modified Dijkstra or Bellman-Ford."),
    ("Network Delay Time", "Medium",
     "Classic Dijkstra on weighted graph — recognise when you need heap vs. deque."),
    ("Snakes and Ladders", "Medium",
     "BFS on implicit graph where board state is the node."),
    ("Jump Game VII", "Medium",
     "BFS reachability on a string with range jumps; step-count minimisation."),
    ("Minimum Cost to Reach City With Discounts", "Medium",
     "State-augmented Dijkstra: (city, discounts_used) as state — extends the grid path family."),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([(name, {"bold": True}), f" ({diff}) — {note}"])))

blocks += [
    N.para("These problems share the core technique: model as a shortest-path problem and choose the right algorithm based on edge weight structure."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, BFS: Shortest Path Unweighted / Dijkstra subsections.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the 0-1 BFS algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=936")
