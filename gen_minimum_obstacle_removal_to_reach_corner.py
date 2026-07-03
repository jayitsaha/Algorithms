"""
gen_minimum_obstacle_removal_to_reach_corner.py
Regenerates the Notion page for LeetCode #2290 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8156-b833-e6e2dfeb617e"
SLUG = "minimum_obstacle_removal_to_reach_corner"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2290,
    pattern="Graph",
    subpatterns=["0-1 BFS"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Model as weighted grid: empty=0 cost, obstacle=1 cost. Use 0-1 BFS (deque): 0-cost neighbors go to front, 1-cost to back — O(m·n) vs Dijkstra's O(m·n·log(m·n)).",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old page body...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m × n", {"bold": True}),
        (" integer matrix ", {}),
        ("grid", {"code": True}),
        (" where each cell is either ", {}),
        ("0", {"code": True}),
        (" (empty) or ", {}),
        ("1", {"code": True}),
        (" (obstacle). You can move up, down, left, or right from and to an empty cell in ", {}),
        ("one step", {"italic": True}),
        (". Return the ", {}),
        ("minimum number of obstacles", {"bold": True}),
        (" to remove so you can travel from the top-left corner ", {}),
        ("(0, 0)", {"code": True}),
        (" to the bottom-right corner ", {}),
        ("(m-1, n-1)", {"code": True}),
        (". (Constraints guarantee ", {}),
        ("grid[0][0] == grid[m-1][n-1] == 0", {"code": True}),
        (").", {}),
    ])),
    N.divider(),
]

# Solution 1 — 0-1 BFS (Interview Pick)
SOLUTION_1_CODE = '''from collections import deque

def minimumObstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # dist[r][c] = minimum obstacles removed to reach (r, c)
    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0, 0)])  # (cost, row, col)

    while dq:
        d, r, c = dq.popleft()
        if d > dist[r][c]:   # stale entry — skip
            continue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]   # 0 if free, 1 if obstacle
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    if grid[nr][nc] == 0:
                        dq.appendleft((nd, nr, nc))  # free: same cost level
                    else:
                        dq.append((nd, nr, nc))       # obstacle: +1 cost level
    return dist[m - 1][n - 1]'''

blocks += [
    N.h2("Solution 1 — 0-1 BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're navigating a grid from top-left to bottom-right. Moving through a cell costs 0 if it's empty and 1 if it's an obstacle (you remove it). We want the minimum total cost — i.e., the minimum number of obstacles removed on any valid path."),
        N.h4("What Doesn't Work"),
        N.para("DFS or regular BFS cannot find the optimal path here. DFS explores arbitrarily and finds A path, not the cheapest one. Regular BFS finds the path with the fewest steps, not the lowest cost — it treats all moves equally, ignoring that obstacle cells cost 1."),
        N.h4("The Key Observation"),
        N.para("This is a shortest-path problem on a weighted graph, where edge weights are exactly 0 (empty cell) or 1 (obstacle cell). For binary weights, 0-1 BFS is the perfect tool: it maintains a deque where the front always holds the cheapest nodes, enabling O(m·n) processing — the same guarantee as Dijkstra but without the log factor."),
        N.h4("Building the Solution"),
        N.para("Use a double-ended queue (deque). When a neighbor is a free cell (cost 0), push to the FRONT — it's at the same cost level as the current node. When a neighbor is an obstacle (cost 1), push to the BACK — it costs one more. The deque stays sorted: front entries always have cost ≤ back entries, processing cheapest-first automatically."),
        N.callout(
            "Analogy: Think of the deque like a hospital waiting room with two tiers. "
            "Patients with the same severity (cost 0) go to the front. "
            "Patients one level sicker (cost 1) go to the back. "
            "We always treat the least-sick patient first — Dijkstra's greedy property, free of charge.",
            "🧠", "blue_background"
        ),
    ]),
]

# Algorithm Deep-Dive
blocks += [
    N.h3("🔬 Algorithm Deep-Dive: 0-1 BFS"),
    N.para("0-1 BFS is a specialization of Dijkstra's algorithm for graphs where all edge weights are either 0 or 1. It was formalized from the observation that a sorted priority queue is overkill when only two distinct cost levels exist."),
    N.code(
        "# 0-1 BFS Template\nfrom collections import deque\n\n"
        "def zero_one_bfs(graph, source):\n"
        "    dist = {node: float('inf') for node in graph}\n"
        "    dist[source] = 0\n"
        "    dq = deque([(0, source)])\n"
        "    while dq:\n"
        "        d, u = dq.popleft()\n"
        "        if d > dist[u]: continue  # stale\n"
        "        for v, w in graph[u]:     # w is 0 or 1\n"
        "            nd = d + w\n"
        "            if nd < dist[v]:\n"
        "                dist[v] = nd\n"
        "                if w == 0: dq.appendleft((nd, v))\n"
        "                else: dq.append((nd, v))\n"
        "    return dist"
    ),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("At any moment, the deque contains nodes with cost only at ", {}),
        ("current_min", {"code": True}),
        (" or ", {}),
        ("current_min + 1", {"code": True}),
        (". Pushing 0-cost to front maintains the minimum at front. Pushing 1-cost to back ensures they are processed exactly one step later. This is equivalent to Dijkstra's priority queue for binary weights, but with O(1) push/pop instead of O(log n).", {}),
    ])),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(grid), len(grid[0])", {"code": True}), (" — Capture grid dimensions.", {})])),
    N.para(N.rich([("dist = [[inf]*n ...]", {"code": True}), (" — Distance matrix: ", {}), ("dist[r][c]", {"code": True}), (" = minimum obstacles to reach cell (r, c). Initialized to infinity.", {})])),
    N.para(N.rich([("dist[0][0] = 0", {"code": True}), (" — Source has zero cost to reach (we start here).", {})])),
    N.para(N.rich([("dq = deque([(0, 0, 0)])", {"code": True}), (" — Seed the deque with the source: (cost=0, row=0, col=0).", {})])),
    N.para(N.rich([("d, r, c = dq.popleft()", {"code": True}), (" — Pop from front. This always gives the current minimum-cost entry due to the deque invariant.", {})])),
    N.para(N.rich([("if d > dist[r][c]: continue", {"code": True}), (" — Stale entry check. If we already found a cheaper path to (r,c), skip this outdated entry.", {})])),
    N.para(N.rich([("nd = d + grid[nr][nc]", {"code": True}), (" — New cost to reach neighbor: current cost plus 0 (free) or 1 (obstacle).", {})])),
    N.para(N.rich([("if nd < dist[nr][nc]:", {"code": True}), (" — Only process if we found a cheaper path. This prevents duplicate processing.", {})])),
    N.para(N.rich([("dq.appendleft(...)", {"code": True}), (" — Free cell: same cost as current. Place at front to maintain ordering.", {})])),
    N.para(N.rich([("dq.append(...)", {"code": True}), (" — Obstacle: costs one more. Place at back to process after current-level nodes.", {})])),
    N.para(N.rich([("return dist[m-1][n-1]", {"code": True}), (" — The minimum obstacles removed to reach the bottom-right corner.", {})])),
    N.divider(),
]

# Solution 2 — Dijkstra
SOLUTION_2_CODE = '''import heapq

def minimumObstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dist = [[float('inf')] * n for _ in range(m)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]   # (cost, row, col)

    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[r][c]:
            continue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return dist[m - 1][n - 1]'''

blocks += [
    N.h2("Solution 2 — Dijkstra (Min-Heap)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same as Solution 1 — shortest path with binary edge weights. Dijkstra is the classic general algorithm for shortest paths in non-negatively weighted graphs."),
        N.h4("What Doesn't Work"),
        N.para("Bellman-Ford would work but is O(V·E) — far too slow for a grid. Plain BFS fails because it ignores edge weights."),
        N.h4("The Key Observation"),
        N.para("Dijkstra always processes the node with the smallest known distance next. With a min-heap, this is O(log n) per operation, giving total time O(m·n·log(m·n)). Correct and straightforward to implement, but slower than 0-1 BFS for this specific problem."),
        N.h4("Building the Solution"),
        N.para("Replace the deque with a min-heap (priority queue). Use heapq.heappush and heapq.heappop. The rest of the algorithm is identical — same stale-entry check, same distance update logic. The only difference is O(log n) per heap operation vs O(1) for the deque."),
        N.callout(
            "When to use Dijkstra instead of 0-1 BFS: "
            "If obstacle costs were variable (e.g., 0, 1, 2, or 3), you'd need Dijkstra. "
            "0-1 BFS only works when costs are binary (exactly 0 or 1).",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time Complexity", "Space Complexity"],
        ["0-1 BFS (Deque)", "O(m·n)", "O(m·n)"],
        ["Dijkstra (Min-Heap)", "O(m·n·log(m·n))", "O(m·n)"],
        ["Brute-Force DFS All Paths", "Exponential", "O(m·n) stack"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Shortest Path on Grid)", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("0-1 BFS — from DSA Guide Section 17.2 (BFS Shortest Path)", {})])),
    N.callout(
        "When to recognize 0-1 BFS:\n"
        "• Grid or graph with edge weights of EXACTLY 0 or 1\n"
        "• Problem asks for minimum cost/removals/flips to reach a target\n"
        "• Keywords: 'minimum removals', 'minimum flips to reach', 'binary cost grid'\n"
        "• You want O(m·n) — can't afford the log factor of Dijkstra\n"
        "• Contrast with BFS (all weights equal) and Dijkstra (arbitrary weights)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 0-1 BFS or related shortest-path technique:"),
    N.bullet(N.rich([
        ("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}),
        (" (Hard) — 0-1 BFS: follow arrow = 0 cost, change direction = 1 cost", {})
    ])),
    N.bullet(N.rich([
        ("Shortest Path in Binary Matrix", {"bold": True}),
        (" (Medium) — Standard BFS (all weights 1, 8-directional)", {})
    ])),
    N.bullet(N.rich([
        ("Shortest Path in a Grid with Obstacles Elimination", {"bold": True}),
        (" (Hard) — BFS with state (x, y, remaining_k_eliminations)", {})
    ])),
    N.bullet(N.rich([
        ("Network Delay Time", {"bold": True}),
        (" (Medium) — Dijkstra with arbitrary positive weights; good comparison", {})
    ])),
    N.bullet(N.rich([
        ("Walls and Gates", {"bold": True}),
        (" (Medium) — Multi-source BFS from gates; conceptual predecessor", {})
    ])),
    N.bullet(N.rich([
        ("Minimum Cost Path with Edge Reversals", {"bold": True}),
        (" (Medium) — 0-1 BFS: follow edge = 0, reverse edge = 1", {})
    ])),
    N.bullet(N.rich([
        ("01 Matrix", {"bold": True}),
        (" (Medium) — Multi-source BFS from 0-cells outward to find nearest 0", {})
    ])),
    N.para("These problems share the binary-weighted or BFS shortest-path pattern. The deque/0-1 BFS insight transfers directly to any problem with edge weights 0 and 1."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.2 — BFS Shortest Path", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the 0-1 BFS algorithm visually — grid state, deque contents, and dist matrix update at each step. Use Next/Prev or ← → arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
