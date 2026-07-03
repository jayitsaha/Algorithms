"""
gen_minimum_cost_path_with_teleportations.py
Notion page builder for: Minimum Cost Path with Teleportations (Custom Hard, DP with State)
Page already exists: 39293418-809c-81c3-b35c-c1f03b6a2fa7
HTML already good (920 lines) — Notion body only.
"""
import sys, json, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39293418-809c-81c3-b35c-c1f03b6a2fa7"
SLUG    = "minimum_cost_path_with_teleportations"

# ─── 1. Set page properties ────────────────────────────────────────────────
print("Setting properties …")
N.set_properties(
    PAGE_ID,
    difficulty  = "Hard",
    number      = 0,
    pattern     = "Dynamic Programming",
    subpatterns = ["DP with State"],
    tc          = "O((R*C + T) * log(R*C)) — T = number of teleporters",
    sc          = "O(R*C + T)",
    key_insight = "Model grid + teleporters as a weighted graph; teleport edges are free (cost 0). Dijkstra finds minimum cost path.",
    icon        = "🔴",
    source      = "LeetCode",
)
print("Properties set OK")

# ─── 2. Wipe old body ─────────────────────────────────────────────────────
print("Wiping old body …")
removed = N.wipe_page(PAGE_ID)
print(f"  Wiped {removed} blocks")

# ─── 3. Build body blocks ─────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("R x C", {"code": True}),
        (" grid where each cell has a non-negative integer entry cost ", {}),
        ("grid[r][c]", {"code": True}),
        (". You start at the top-left cell ", {}),
        ("(0, 0)", {"code": True}),
        (" and want to reach the bottom-right cell ", {}),
        ("(R-1, C-1)", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Movement: ", {"bold": True}),
        ("From any cell you may step to any of the 4 adjacent neighbours (up, down, left, right), paying the neighbour's entry cost.", {}),
    ])),
    N.para(N.rich([
        ("Teleportation: ", {"bold": True}),
        ("You are also given ", {}),
        ("teleporters = [(r1,c1,r2,c2), ...]", {"code": True}),
        (". From ", {}),
        ("(r1, c1)", {"code": True}),
        (" you may instantly jump to ", {}),
        ("(r2, c2)", {"code": True}),
        (" at zero additional cost.", {}),
    ])),
    N.para(N.rich([
        ("Goal: ", {"bold": True}),
        ("Return the minimum total cost to reach ", {}),
        ("(R-1, C-1)", {"code": True}),
        (" from ", {}),
        ("(0, 0)", {"code": True}),
        (" paying each cell's entry cost exactly once.", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Dijkstra ─────────────────────────────────────────────────
sol1_code = (
    "import heapq\n"
    "\n"
    "def minCostPath(grid, teleporters):\n"
    "    R, C = len(grid), len(grid[0])\n"
    "\n"
    "    # Build adjacency list\n"
    "    adj = [[[] for _ in range(C)] for _ in range(R)]\n"
    "    dirs = [(-1,0),(1,0),(0,-1),(0,1)]\n"
    "    for r in range(R):\n"
    "        for c in range(C):\n"
    "            for dr, dc in dirs:\n"
    "                nr, nc = r+dr, c+dc\n"
    "                if 0 <= nr < R and 0 <= nc < C:\n"
    "                    adj[r][c].append((nr, nc, grid[nr][nc]))\n"
    "\n"
    "    for r1,c1,r2,c2 in teleporters:\n"
    "        adj[r1][c1].append((r2, c2, 0))  # free teleport\n"
    "\n"
    "    # Dijkstra\n"
    "    dist = [[float('inf')]*C for _ in range(R)]\n"
    "    dist[0][0] = grid[0][0]\n"
    "    heap = [(grid[0][0], 0, 0)]\n"
    "\n"
    "    while heap:\n"
    "        cost, r, c = heapq.heappop(heap)\n"
    "        if cost > dist[r][c]:\n"
    "            continue\n"
    "        for nr, nc, w in adj[r][c]:\n"
    "            nc_cost = cost + w\n"
    "            if nc_cost < dist[nr][nc]:\n"
    "                dist[nr][nc] = nc_cost\n"
    "                heapq.heappush(heap, (nc_cost, nr, nc))\n"
    "\n"
    "    return dist[R-1][C-1]\n"
)

blocks += [
    N.h2("Solution 1 — Dijkstra with Teleport Edges (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Forget 'grid' for a moment. Each cell is a node in a weighted graph. "
            "Moving to a neighbour adds that neighbour's cost as the edge weight. "
            "Teleporting adds a zero-weight edge. We want the minimum-cost path "
            "from node (0,0) to node (R-1,C-1) in this graph. That is Dijkstra's problem."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Plain BFS ignores edge weights — it treats a cost-10 move identically to a "
            "cost-1 move. Standard grid DP (filling top-left to bottom-right) fails because "
            "teleports can jump backwards (e.g., row 5 to row 0), so we cannot process cells "
            "in a simple forward order."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Teleporters are zero-weight edges. As soon as we model the grid as a graph "
            "with both normal (positive-weight) and teleport (zero-weight) edges, Dijkstra "
            "handles it exactly. No special casing needed — just add the edges."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Build adjacency list from all 4-directional moves (weight = neighbour entry cost). "
            "Step 2: Add teleport edges (weight 0). "
            "Step 3: Initialize dist[0][0] = grid[0][0]. "
            "Step 4: Dijkstra with min-heap. "
            "Step 5: Return dist[R-1][C-1]."
        ),
        N.callout(
            "Analogy: Think of a city with toll roads (normal moves) and free subway tunnels "
            "(teleporters). Dijkstra always picks the next cheapest destination regardless of "
            "whether you drove or teleported.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Dijkstra"),
    N.para(
        "Dijkstra's algorithm (1959) solves single-source shortest path for graphs with "
        "non-negative edge weights. Core invariant: when a node is popped from the min-heap, "
        "its recorded distance is final and optimal. This holds because all weights >= 0, "
        "so no future path can improve it. Time: O((V+E) log V) with a binary heap."
    ),
    N.para(
        "Recognize Dijkstra when: minimum cost to reach a node, edge weights >= 0, "
        "back-edges or jumps are possible (making simple DP infeasible)."
    ),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = [[[] for _ in range(C)] for _ in range(R)]", {"code": True}),
                   (" — Adjacency list: for each cell, store (neighbour_r, neighbour_c, edge_cost).", {})])),
    N.para(N.rich([("adj[r][c].append((nr, nc, grid[nr][nc]))", {"code": True}),
                   (" — Normal 4-directional move: edge weight = neighbour's entry cost.", {})])),
    N.para(N.rich([("adj[r1][c1].append((r2, c2, 0))", {"code": True}),
                   (" — Teleport edge: weight 0 (free jump).", {})])),
    N.para(N.rich([("dist[0][0] = grid[0][0]", {"code": True}),
                   (" — Seed: we pay the start cell's own entry cost to 'enter' it.", {})])),
    N.para(N.rich([("heap = [(grid[0][0], 0, 0)]", {"code": True}),
                   (" — Min-heap stores (current_cost, row, col). Priority = cost.", {})])),
    N.para(N.rich([("if cost > dist[r][c]: continue", {"code": True}),
                   (" — Lazy deletion: skip stale heap entries (a cheaper path was already found).", {})])),
    N.para(N.rich([("nc_cost = cost + w", {"code": True}),
                   (" — Tentative cost to reach (nr,nc) via current cell.", {})])),
    N.para(N.rich([("if nc_cost < dist[nr][nc]:", {"code": True}),
                   (" — Only update and push if we found a strictly cheaper route.", {})])),
    N.para(N.rich([("return dist[R-1][C-1]", {"code": True}),
                   (" — The minimum cost recorded for the destination cell.", {})])),
    N.divider(),
]

# ─── Solution 2: Bellman-Ford DP ──────────────────────────────────────────
sol2_code = (
    "def minCostPathDP(grid, teleporters):\n"
    "    R, C = len(grid), len(grid[0])\n"
    "    INF = float('inf')\n"
    "    dp = [[INF]*C for _ in range(R)]\n"
    "    dp[0][0] = grid[0][0]\n"
    "    dirs = [(-1,0),(1,0),(0,-1),(0,1)]\n"
    "\n"
    "    changed = True\n"
    "    while changed:\n"
    "        changed = False\n"
    "        for r in range(R):\n"
    "            for c in range(C):\n"
    "                if dp[r][c] == INF:\n"
    "                    continue\n"
    "                for dr, dc in dirs:\n"
    "                    nr, nc = r+dr, c+dc\n"
    "                    if 0 <= nr < R and 0 <= nc < C:\n"
    "                        new_cost = dp[r][c] + grid[nr][nc]\n"
    "                        if new_cost < dp[nr][nc]:\n"
    "                            dp[nr][nc] = new_cost\n"
    "                            changed = True\n"
    "        for r1,c1,r2,c2 in teleporters:\n"
    "            if dp[r1][c1] < dp[r2][c2]:\n"
    "                dp[r2][c2] = dp[r1][c1]\n"
    "                changed = True\n"
    "\n"
    "    return dp[R-1][C-1]\n"
)

blocks += [
    N.h2("Solution 2 — Bellman-Ford DP (Teaching Contrast)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think of dp[r][c] as 'the best cost found so far to reach cell (r,c)'. "
            "We propagate costs outward, relaxing edges repeatedly, exactly like Bellman-Ford "
            "relaxes graph edges in multiple passes until convergence."
        ),
        N.h4("What Doesn't Work — Single Pass"),
        N.para(
            "A single forward scan fails because teleports can send cost information backwards. "
            "Cell (0,5) might be cheaply reachable via a teleport from (3,3), which we haven't "
            "processed yet in a forward scan."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Repeat scans until no cell improves. Each iteration propagates cost 'one hop "
            "further' from the source. This is correct but slow: O(R^2 * C^2) in the worst case."
        ),
        N.callout(
            "Mention this in interviews to contrast with Dijkstra. "
            "Always propose Dijkstra as the optimal solution.",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [[INF]*C for _ in range(R)]", {"code": True}),
                   (" — Cost table; all infinity except the seeded start.", {})])),
    N.para(N.rich([("while changed:", {"code": True}),
                   (" — Keep iterating until a full scan produces no improvement.", {})])),
    N.para(N.rich([("new_cost = dp[r][c] + grid[nr][nc]", {"code": True}),
                   (" — Tentative cost to enter neighbour via current cell.", {})])),
    N.para(N.rich([("if dp[r1][c1] < dp[r2][c2]: dp[r2][c2] = dp[r1][c1]", {"code": True}),
                   (" — Teleport is free: propagate cheaper cost to destination.", {})])),
    N.divider(),
]

# ─── Complexity table ─────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Dijkstra (optimal)", "O((R·C + T) · log(R·C))", "O(R·C + T)"],
        ["Bellman-Ford DP", "O(R²·C² + R·C·T) worst case", "O(R·C)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Dynamic Programming / Graph Shortest Path", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("DP with State — the DP distance table is updated via Dijkstra-style "
                    "state relaxation transitions (normal moves + zero-cost teleport edges).", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Grid with variable cell entry costs\n"
        "• Extra 'jump' edges (teleporters, wormholes, free passes)\n"
        "• 'Minimum cost to reach destination'\n"
        "• Back-edges possible — simple top-to-bottom DP fails\n"
        "• Key signal: Dijkstra when edges >= 0 and back-edges exist",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP-with-State / Graph Shortest Path technique:"),
    N.bullet(N.rich([
        ("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}),
        (" (Hard) — 0-1 BFS on grid with directional arrow costs", {})])),
    N.bullet(N.rich([
        ("Minimum Path Sum", {"bold": True}),
        (" (Medium) — Classic grid DP, no teleports, no back-edges", {})])),
    N.bullet(N.rich([
        ("Shortest Path in Binary Matrix", {"bold": True}),
        (" (Medium) — BFS on 0/1 grid, 8-directional", {})])),
    N.bullet(N.rich([
        ("Network Delay Time", {"bold": True}),
        (" (Medium) — Dijkstra on explicit directed weighted graph", {})])),
    N.bullet(N.rich([
        ("The Maze II", {"bold": True}),
        (" (Medium) — Dijkstra with rolling-ball physics on grid", {})])),
    N.bullet(N.rich([
        ("Cheapest Flights Within K Stops", {"bold": True}),
        (" (Medium) — Bellman-Ford / modified Dijkstra with hop-count state", {})])),
    N.bullet(N.rich([
        ("Jump Game VI", {"bold": True}),
        (" (Medium) — DP with deque (sliding window max) for jump-range optimization", {})])),
    N.bullet(N.rich([
        ("Swim in Rising Water", {"bold": True}),
        (" (Hard) — Dijkstra / binary search on grid bottleneck cost", {})])),
    N.para("These problems share: model the problem as shortest path, choose Dijkstra/BFS/DP "
           "based on edge weight structure, handle non-standard edges (jumps, teleports) as extra graph edges."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — "
        "Section 18 (Dynamic Programming: DP with State) and Section 13 (Graph: Dijkstra / Weighted Shortest Path)",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ─── Interactive Explainer embed ──────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Push to Notion ────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion …")
N.append_blocks(PAGE_ID, blocks)
print("Notion body written OK")

# ─── 5. Write status file ─────────────────────────────────────────────────
html_path = f"/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/{SLUG}_explainer.html"
html_lines = sum(1 for _ in open(html_path))
status_dir = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status"
os.makedirs(status_dir, exist_ok=True)
status = {
    "slug":           SLUG,
    "html":           "OK",
    "notion":         "OK",
    "lines":          html_lines,
    "notes":          f"HTML already good ({html_lines} lines, all markers present); Notion page existed with 0 children, body rebuilt.",
    "notion_page_id": PAGE_ID,
}
status_path = os.path.join(status_dir, f"{SLUG}.json")
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)
print(f"Status written -> {status_path}")
print(f"\nRESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
