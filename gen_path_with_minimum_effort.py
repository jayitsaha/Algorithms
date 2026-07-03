"""gen_path_with_minimum_effort.py — Notion update for LeetCode #1631."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8128-9d8c-e3a15358d9f5"
SLUG = "path_with_minimum_effort"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1631,
    pattern="Graph",
    subpatterns=["Dijkstra's on Max Edge"],
    tc="O(m·n·log(m·n))",
    sc="O(m·n)",
    key_insight="Redefine Dijkstra's relaxation: new_effort = max(curr_effort, |height_diff|) instead of sum. The max operation is monotone, so Dijkstra's correctness guarantee holds.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# 3) Rebuild body
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are a hiker preparing to travel through a 2D grid of ", {}),
        ("heights", {"code": True}),
        (" of size m×n. The effort of a route is defined as the maximum absolute difference in heights between two consecutive cells of the route. Return the minimum effort required to travel from the top-left to the bottom-right cell.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Modified Dijkstra ──
blocks += [
    N.h2("Solution 1 — Modified Dijkstra on Max Edge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to minimise the maximum single step on any path from (0,0) to (m-1,n-1). This is a minimax problem on a grid graph. Think of it as: for each cell, what is the best (lowest) 'worst step' I can guarantee if I travel there?"),
        N.h4("What Doesn't Work"),
        N.para("BFS (unweighted) treats all edges as equal — wrong. Standard Dijkstra minimises the sum of edge weights — also wrong. We need to track the maximum single edge, not the total cost."),
        N.h4("The Key Observation"),
        N.para("Define dist[r][c] = minimum possible maximum edge weight on any path from (0,0) to (r,c). The relaxation changes from dist[u] + w(u,v) to max(dist[u], w(u,v)). Everything else in Dijkstra stays the same. This works because max is monotone: extending a path never decreases its maximum step, which is the same property Dijkstra needs."),
        N.h4("Building the Solution"),
        N.para("1. Initialize dist[0][0]=0, all others=infinity. 2. Min-heap on effort. 3. Pop minimum. 4. If goal: return. 5. If stale: skip. 6. For each neighbour: compute max(eff, |h_diff|). 7. If improved: update and push. The key substitution is max() for + in the relaxation step."),
        N.callout("Analogy: Think of hiking. You want the path where the steepest single climb is minimised — not the path with the least total climbing. You would prefer 10 gentle slopes over one cliff, even if the total ascent is the same.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Modified Dijkstra"),
    N.para(N.rich([
        ("Dijkstra's Algorithm", {"bold": True}),
        (" (Edsger W. Dijkstra, 1956) finds shortest paths from a source in a weighted graph. Its correctness relies on one property: the cost function must be ", {}),
        ("monotone", {"bold": True}),
        (" — extending a path never decreases its cost. For standard Dijkstra: sum is monotone (non-negative weights). For this problem: max is monotone (max(a,b) ≥ a always). We substitute max for sum in the relaxation step, and the entire correctness proof transfers.", {}),
    ])),
    N.code(
        "# Modified Dijkstra template\n"
        "# dist[v] = min over all paths of MAX edge weight\n"
        "# Relax: new_eff = max(dist[u], w(u,v))\n"
        "# if new_eff < dist[v]: update and push\n"
        "#\n"
        "# Invariant: when v is popped from heap,\n"
        "# dist[v] is optimal and final (never improved again)\n"
        "# Reason: heap is ordered by effort; max is monotone;\n"
        "# no future path can produce a lower max effort to v.",
        "python"
    ),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("When a cell is popped from the heap, its dist value is the true minimum possible maximum edge weight. No future exploration can improve it — the heap only contains entries with effort ≥ current, and max is monotone.", {}),
    ])),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "def minimumEffortPath(heights):\n"
        "    m, n = len(heights), len(heights[0])\n"
        "    dist = [[float('inf')] * n for _ in range(m)]\n"
        "    dist[0][0] = 0\n"
        "    heap = [(0, 0, 0)]  # (effort, row, col)\n"
        "    dirs = [(0,1),(0,-1),(1,0),(-1,0)]\n"
        "    while heap:\n"
        "        eff, r, c = heapq.heappop(heap)\n"
        "        if r == m-1 and c == n-1:\n"
        "            return eff\n"
        "        if eff > dist[r][c]:\n"
        "            continue\n"
        "        for dr, dc in dirs:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < m and 0 <= nc < n:\n"
        "                edge = abs(heights[r][c] - heights[nr][nc])\n"
        "                new_eff = max(eff, edge)  # KEY: max not sum\n"
        "                if new_eff < dist[nr][nc]:\n"
        "                    dist[nr][nc] = new_eff\n"
        "                    heapq.heappush(heap, (new_eff, nr, nc))\n"
        "    return dist[m-1][n-1]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dist = [[inf]*n ...]", {"code": True}), (" — Initialize all cells unreachable (infinity effort). Base case: dist[0][0]=0, the start needs zero effort.", {})])),
    N.para(N.rich([("heap = [(0, 0, 0)]", {"code": True}), (" — Min-heap seeded with (effort=0, row=0, col=0). Python's heapq is a min-heap by default, so smallest effort is always popped first.", {})])),
    N.para(N.rich([("eff, r, c = heapq.heappop(heap)", {"code": True}), (" — Pop the cell with the smallest known effort. By the invariant, when this cell is the goal, eff is the optimal answer.", {})])),
    N.para(N.rich([("if r == m-1 and c == n-1: return eff", {"code": True}), (" — Early exit: Dijkstra guarantees the first time we pop the goal, we have the optimal effort. No need to continue.", {})])),
    N.para(N.rich([("if eff > dist[r][c]: continue", {"code": True}), (" — Stale entry check. The heap can contain multiple (now-outdated) entries for the same cell. If the popped effort is worse than the current best, skip it.", {})])),
    N.para(N.rich([("edge = abs(heights[r][c] - heights[nr][nc])", {"code": True}), (" — Cost of moving from current cell to neighbour: absolute height difference.", {})])),
    N.para(N.rich([("new_eff = max(eff, edge)", {"code": True}), (" — THE KEY LINE. We take the maximum of the current path effort and this edge. This is the bottleneck along the path through this route.", {})])),
    N.para(N.rich([("if new_eff < dist[nr][nc]:", {"code": True}), (" — Relaxation condition: only update if we found a strictly better (lower) effort to reach the neighbour.", {})])),
    N.divider(),
]

# ── Solution 2: Binary Search + BFS ──
blocks += [
    N.h2("Solution 2 — Binary Search on Answer + BFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of finding the optimal effort directly, ask a simpler question: 'Given a maximum allowed effort E, can I reach the goal using only edges with |height_diff| ≤ E?' If we can answer this efficiently, binary search on E gives the answer."),
        N.h4("What Doesn't Work"),
        N.para("Checking all possible values of E naively is too slow (up to 10^6 values). We need to reduce the search space."),
        N.h4("The Key Observation"),
        N.para("The answer (effort) is monotone: if we can reach the goal with effort E, we can also reach it with any effort E' > E. This monotonicity means binary search applies. Search space: [0, max_height]. For each candidate E, run BFS/DFS using only edges with |diff| ≤ E."),
        N.h4("Building the Solution"),
        N.para("Binary search lo=0, hi=max_height. At each mid, run BFS allowing only edges ≤ mid. If reachable, try smaller (hi=mid); else try larger (lo=mid+1). lo converges to the minimum effort."),
        N.callout("When to use BS+BFS: Easier to derive under pressure than Modified Dijkstra. O(m*n*log H) is slightly worse but usually acceptable. Recognise 'minimise the maximum threshold' = binary search.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def minimumEffortPath(heights):\n"
        "    m, n = len(heights), len(heights[0])\n"
        "\n"
        "    def canReach(limit):\n"
        "        \"\"\"BFS: can we reach (m-1,n-1) using only edges with |diff| <= limit?\"\"\"\n"
        "        visited = [[False] * n for _ in range(m)]\n"
        "        q = deque([(0, 0)])\n"
        "        visited[0][0] = True\n"
        "        while q:\n"
        "            r, c = q.popleft()\n"
        "            if r == m-1 and c == n-1:\n"
        "                return True\n"
        "            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "                nr, nc = r+dr, c+dc\n"
        "                if (0 <= nr < m and 0 <= nc < n\n"
        "                        and not visited[nr][nc]\n"
        "                        and abs(heights[r][c] - heights[nr][nc]) <= limit):\n"
        "                    visited[nr][nc] = True\n"
        "                    q.append((nr, nc))\n"
        "        return False\n"
        "\n"
        "    lo, hi = 0, max(max(row) for row in heights)\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if canReach(mid):\n"
        "            hi = mid      # Can reach with this limit? Try smaller.\n"
        "        else:\n"
        "            lo = mid + 1  # Cannot reach? Need at least mid+1.\n"
        "    return lo",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("canReach(limit)", {"code": True}), (" — Inner function: standard BFS, but only traverses edges where the absolute height difference is ≤ limit. Returns True if the goal is reachable under this constraint.", {})])),
    N.para(N.rich([("lo, hi = 0, max(max(row) for row in heights)", {"code": True}), (" — Search space: 0 (all heights equal, trivial path) to max height (any single step is allowed). The answer lies in [lo, hi].", {})])),
    N.para(N.rich([("if canReach(mid): hi = mid", {"code": True}), (" — If we can navigate with effort ≤ mid, the true minimum effort is ≤ mid. Narrow upper bound.", {})])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — Cannot reach with effort ≤ mid, so we need strictly more. Raise lower bound.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — When lo==hi, we've found the minimum effort. lo is the smallest value for which canReach returns True.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Modified Dijkstra (Interview Pick)", "O(m·n·log(m·n))", "O(m·n)"],
        ["Binary Search + BFS", "O(m·n·log H) where H = max height", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Dijkstra's Algorithm)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dijkstra's on Max Edge — modified from standard Dijkstra by substituting max for sum in the relaxation step to handle minimax path objectives.", {})])),
    N.callout(
        "When to recognise this pattern:\n"
        "• Problem asks for 'minimum of the maximum' or 'minimize the bottleneck' along a path\n"
        "• Grid or graph traversal where the path cost is the worst single edge, not the total\n"
        "• Edge weights are non-negative (required for Dijkstra correctness)\n"
        "• Keywords: 'effort', 'maximum difference', 'safest path', 'threshold'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra / Modified Dijkstra / Minimax Path):"),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium) — Classic Dijkstra with sum weights; great warm-up before this problem (#743)", {})])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), (" (Hard) — Same minimax structure on a grid, but node-based cost (#778)", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Modified Dijkstra/Bellman-Ford with a K-stop budget constraint (#787)", {})])),
    N.bullet(N.rich([("Find the Safest Path in a Grid", {"bold": True}), (" (Medium) — Maximize the minimum safety factor — dual of this problem (#2812)", {})])),
    N.bullet(N.rich([("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}), (" (Hard) — 0-1 BFS / Dijkstra on directed grid (#1368)", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Matrix", {"bold": True}), (" (Medium) — Binary search on answer + matrix traversal; same BS structure as Solution 2 (#378)", {})])),
    N.para("These problems share the core technique: treat grid edges as a weighted graph and apply Dijkstra (or binary search + BFS) with a modified cost function."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Graph Algorithms → Dijkstra.\nSub-Pattern: Dijkstra's on Max Edge. Source: Analysis (not explicitly listed in guide as this specific sub-pattern name).", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# 4) Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
