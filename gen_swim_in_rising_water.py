"""
Notion in-place update for: Swim in Rising Water (LC #778)
Run from the Algorithms directory where notion_lib.py lives.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813d-93ef-e71e22021156"
SLUG = "swim_in_rising_water"

# ── 1. Properties ─────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=778,
    pattern="Graph",
    subpatterns=["Binary Search + BFS or Dijkstra's"],
    tc="O(n² log n)",
    sc="O(n²)",
    key_insight="Min-bottleneck path: minimize max-elevation on any route; use Dijkstra's with max(cost, neighbor_elev) as the cost function.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("n × n", {"bold": True}),
        (" integer grid where each value is unique and represents the elevation of that cell. "
         "At time ", {}),
        ("t", {"code": True}),
        (", you can move to any adjacent cell (up/down/left/right) whose elevation is ≤ ", {}),
        ("t", {"code": True}),
        (". You start at ", {}),
        ("grid[0][0]", {"code": True}),
        (" and want to reach ", {}),
        ("grid[n-1][n-1]", {"code": True}),
        (". Return the minimum time ", {}),
        ("t", {"code": True}),
        (" so that it is possible to swim from the top-left to the bottom-right.", {})
    ])),
    N.divider()
]

# ── Solution 1: Dijkstra's (Interview Pick) ───────────────────────────────────
blocks += [
    N.h2("Solution 1 — Dijkstra's Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the minimum time t such that a path from (0,0) to (n-1,n-1) exists using "
            "only cells with elevation ≤ t. The time for any path equals the maximum elevation "
            "on that path. So we want: minimize the maximum cell elevation across all possible "
            "paths. This is the bottleneck shortest path problem."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Plain BFS finds the shortest path by hop count. But fewer hops does NOT mean lower "
            "maximum elevation. A 2-hop shortcut might cross a mountain, while a 10-hop route "
            "stays in the valley. We cannot optimize both simultaneously — we must prioritize "
            "the cell that gives us the global minimum bottleneck next, not the nearest cell by steps."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This is a graph shortest-path problem where edge cost = max(current_cost, neighbor_elevation) "
            "instead of a sum. The cost function is monotone (it never decreases as we extend a path), "
            "which is the crucial property that makes Dijkstra's algorithm correct. So we use a min-heap "
            "ordered by this max-cost, and standard Dijkstra's analysis applies."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Push (grid[0][0], 0, 0) onto the min-heap — the start cell's elevation is its own bottleneck.\n"
            "2. Pop the cell with the globally smallest bottleneck cost.\n"
            "3. If it's the destination, return cost (Dijkstra's invariant: first pop = optimal).\n"
            "4. For each unvisited neighbor, compute new_cost = max(cost, neighbor_elevation) and push it.\n"
            "5. Mark popped cells as visited to avoid reprocessing."
        ),
        N.callout(
            "Analogy: Imagine hiking to a destination. The 'cost' of a route is its highest peak. "
            "Dijkstra's finds the route that minimizes that highest peak by always exploring the "
            "cheapest frontier (lowest peak seen so far) before higher ones.",
            "🏔️", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "def swimInWater(grid: list[list[int]]) -> int:\n"
        "    n = len(grid)\n"
        "    visited = set()\n"
        "    heap = [(grid[0][0], 0, 0)]  # (max_elev_so_far, row, col)\n"
        "\n"
        "    while heap:\n"
        "        cost, r, c = heapq.heappop(heap)\n"
        "        if (r, c) in visited:\n"
        "            continue\n"
        "        visited.add((r, c))\n"
        "\n"
        "        if r == n - 1 and c == n - 1:\n"
        "            return cost  # Dijkstra's invariant: first pop = optimal\n"
        "\n"
        "        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:\n"
        "                new_cost = max(cost, grid[nr][nc])  # bottleneck update\n"
        "                heapq.heappush(heap, (new_cost, nr, nc))"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(grid[0][0], 0, 0)]", {"code": True}), (" — Initialize min-heap with the start cell. Tuple: (bottleneck_cost, row, col). The start's elevation is its own bottleneck since there's no prior path.", {})])),
    N.para(N.rich([("visited = set()", {"code": True}), (" — Once a cell is popped, its cost is final (Dijkstra's invariant). The visited set prevents stale heap entries from being reprocessed.", {})])),
    N.para(N.rich([("cost, r, c = heapq.heappop(heap)", {"code": True}), (" — Pop the cell with the globally smallest bottleneck cost. By the min-heap property, this is guaranteed to be optimal.", {})])),
    N.para(N.rich([("if (r, c) in visited: continue", {"code": True}), (" — A cell can be pushed multiple times (with different costs) as better paths are found. Skip if already settled.", {})])),
    N.para(N.rich([("if r == n-1 and c == n-1: return cost", {"code": True}), (" — First time we pop the destination, the cost is guaranteed optimal — return immediately.", {})])),
    N.para(N.rich([("new_cost = max(cost, grid[nr][nc])", {"code": True}), (" — The bottleneck of extending to a neighbor = max of current path's bottleneck and the neighbor's own elevation. This is the core modification from textbook Dijkstra's (which would use cost + weight).", {})])),
    N.divider()
]

# ── Solution 2: Binary Search + BFS ──────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Binary Search + BFS (Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of finding the optimal path directly, ask: 'For a given time t, is it possible "
            "to reach the destination?' This is a yes/no (feasibility) question — and the answer "
            "transitions exactly once from No to Yes as t increases. Perfect for binary search."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Trying every value of t from 0 to n²-1 linearly would be O(n² × n²) = O(n⁴). "
            "Since the feasibility is monotone (once reachable, always reachable for larger t), "
            "we can binary search on t to reduce the outer loop to O(log n²) = O(log n)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The feasibility function is monotone: if we can reach the destination at time t, "
            "we can also reach it at any time t' > t. This monotonicity is what makes binary "
            "search applicable. We binary search on t in [0, n²-1], and for each candidate, "
            "run a standard BFS using only cells with elevation ≤ t."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Binary search lo=0, hi=n²-1. At each midpoint t:\n"
            "  - BFS from (0,0) using only cells with elevation ≤ t\n"
            "  - If (n-1,n-1) is reachable: hi = t (try smaller)\n"
            "  - If not reachable: lo = t+1 (need larger t)\n"
            "When lo == hi, that is the answer."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def swimInWater(grid: list[list[int]]) -> int:\n"
        "    n = len(grid)\n"
        "\n"
        "    def can_reach(t: int) -> bool:\n"
        "        if grid[0][0] > t:\n"
        "            return False\n"
        "        queue = deque([(0, 0)])\n"
        "        seen = {(0, 0)}\n"
        "        while queue:\n"
        "            r, c = queue.popleft()\n"
        "            if r == n - 1 and c == n - 1:\n"
        "                return True\n"
        "            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "                nr, nc = r + dr, c + dc\n"
        "                if (0 <= nr < n and 0 <= nc < n\n"
        "                        and (nr, nc) not in seen\n"
        "                        and grid[nr][nc] <= t):\n"
        "                    seen.add((nr, nc))\n"
        "                    queue.append((nr, nc))\n"
        "        return False\n"
        "\n"
        "    lo, hi = 0, n * n - 1\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if can_reach(mid):\n"
        "            hi = mid        # feasible — try smaller\n"
        "        else:\n"
        "            lo = mid + 1    # infeasible — need larger t\n"
        "    return lo"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def can_reach(t)", {"code": True}), (" — Feasibility check: BFS restricted to cells with elevation ≤ t. Returns True if destination is reachable at time t.", {})])),
    N.para(N.rich([("lo, hi = 0, n*n - 1", {"code": True}), (" — The search space: minimum possible answer is 0 (all cells instantly accessible), maximum is n²-1 (largest elevation in the grid).", {})])),
    N.para(N.rich([("if can_reach(mid): hi = mid", {"code": True}), (" — If feasible at mid, the answer could be mid or smaller (try left half).", {})])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — If infeasible, the answer must be strictly greater than mid (try right half).", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — When lo == hi, both bounds have converged to the minimum feasible t.", {})])),
    N.divider()
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (all paths)", "Exponential", "Exponential", "Not feasible"],
        ["Dijkstra's Min-Heap ✓", "O(n² log n)", "O(n²)", "Single pass; heap has ≤ n² entries, each log n pop/push"],
        ["Binary Search + BFS", "O(n² log n)", "O(n²)", "O(log n²) BFS runs of O(n²) each"],
        ["Union-Find (sort + union)", "O(n² log n)", "O(n²)", "Sort all cells once; union until start connects to end"],
    ]),
    N.divider()
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search + BFS or Dijkstra's", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Minimum time/threshold such that a path from A to B exists'\n"
        "• 'Minimize the maximum value along any path in a grid'\n"
        "• Grid navigation where the constraint can be binary-searched\n"
        "• Cost function is max() of values, not sum — signals bottleneck path",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra's bottleneck or Binary Search + BFS):"),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), (" (Medium) — Minimize max |elevation difference| between adjacent cells; same Dijkstra's pattern with different cost formula (#1631)", {})])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium) — Classic Dijkstra's: minimum time for signal to reach all nodes; weighted graph, cost = sum (#743)", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Modified Dijkstra's with an additional hop-count constraint; state = (cost, node, stops_remaining) (#787)", {})])),
    N.bullet(N.rich([("Find the Safest Path in a Grid", {"bold": True}), (" (Medium) — Maximize the minimum safety factor on any path; binary search on safety + BFS (#2812)", {})])),
    N.bullet(N.rich([("Minimum Cost to Make at Least One Valid Path", {"bold": True}), (" (Hard) — 0-1 BFS on directed grid; edges have cost 0 (follow sign) or 1 (change sign) (#1368)", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — Binary search on the answer value in a 2D sorted matrix (#378)", {})])),
    N.para("These problems all share the bottleneck path or binary-search-on-answer technique."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section → Dijkstra / Weighted Shortest Path. Sub-Pattern: Binary Search + BFS or Dijkstra's", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through Dijkstra's algorithm visually on a 4×4 grid — use Next/Prev or arrow keys to see each cell being popped, settled, and neighbors being pushed with their bottleneck costs.",
         {"italic": True, "color": "gray"})
    ]))
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
