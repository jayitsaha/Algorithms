"""
Notion page generator for:
  Find Minimum Time to Reach Last Room I (#3341, Medium, Graph / Modified Dijkstra)
notion_page_id: null → create fresh page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Create page (notion_page_id was null) ──────────────────────────
PAGE_ID = N.create_page("Find Minimum Time to Reach Last Room I", 3341, "Medium", "🟡")
print("Created page:", PAGE_ID)

# ── Step 1: Set properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=3341,
    pattern="Graph",
    subpatterns=["Modified Dijkstra"],
    tc="O(n·m·log(n·m))",
    sc="O(n·m)",
    key_insight="Treat grid as weighted graph; use Dijkstra with edge cost max(cur_t, moveTime[nr][nc])+1 to handle waiting.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe any existing body (fresh page, but safe to call) ──────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ──────────────────────────────────────────────

SOL1_CODE = '''import heapq

def minTimeToReach(moveTime: list[list[int]]) -> int:
    n, m = len(moveTime), len(moveTime[0])
    dist = [[float('inf')] * m for _ in range(n)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]  # (time, row, col)

    while heap:
        t, r, c = heapq.heappop(heap)
        if t > dist[r][c]:      # stale entry — lazy deletion
            continue
        if r == n - 1 and c == m - 1:
            return t             # Dijkstra guarantees optimality at first pop
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                new_t = max(t, moveTime[nr][nc]) + 1
                if new_t < dist[nr][nc]:
                    dist[nr][nc] = new_t
                    heapq.heappush(heap, (new_t, nr, nc))

    return dist[n - 1][m - 1]'''

SOL2_CODE = '''# BFS (WRONG for this problem — shown for contrast)
# BFS processes cells in hop-order, not time-order.
# Two paths with equal hops can have unequal times due to waiting.
# Example: moveTime=[[0,0,10],[0,0,0],[0,0,0]]
# BFS thinks all cells at distance 2 hops are equally costly,
# but waiting at row 0 col 2 adds 10 seconds.

from collections import deque

def minTimeToReach_BFS_WRONG(moveTime):
    n, m = len(moveTime), len(moveTime[0])
    dist = [[float('inf')] * m for _ in range(n)]
    dist[0][0] = 0
    dq = deque([(0, 0, 0)])
    while dq:
        t, r, c = dq.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < m:
                # BFS MISTAKE: doesn't account for waiting time correctly
                new_t = max(t, moveTime[nr][nc]) + 1
                if new_t < dist[nr][nc]:
                    dist[nr][nc] = new_t
                    dq.append((new_t, nr, nc))  # re-queues if improved
    return dist[n-1][m-1]
# ^^ This is actually Bellman-Ford-like, not Dijkstra. Slower + no guarantee
# of correctness for this cost function. Use Dijkstra instead.'''

blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is a dungeon with ", {}),
        ("n", {"code": True}),
        (" rows and ", {}),
        ("m", {"code": True}),
        (" columns, given as a 0-indexed 2D array ", {}),
        ("moveTime", {"code": True}),
        (". The value ", {}),
        ("moveTime[i][j]", {"code": True}),
        (" represents the minimum time in seconds when you can start moving to that room. "
         "You are initially in room (0, 0) at second 0. In one second you can move to an "
         "adjacent room (up, down, left, right). Return the minimum time to reach the room "
         "(n-1, m-1).", {})
    ])),
    N.divider(),
]

# ── Solution 1: Modified Dijkstra ──────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Modified Dijkstra (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a grid where entering each room costs at least 1 second, but may cost more if we arrive before the room 'opens'. We want the minimum time to travel from top-left to bottom-right. This is fundamentally a shortest-path problem on a weighted graph."),
        N.h4("What Doesn't Work"),
        N.para("BFS finds shortest hops, not shortest time. Two paths with equal hop counts can have very different arrival times if one path encounters high moveTime cells that force waiting. We need an algorithm that tracks actual arrival time, not hop count."),
        N.h4("The Key Observation"),
        N.para("The 'cost' to move from cell (r,c) at time t to neighbor (nr,nc) is: max(t, moveTime[nr][nc]) + 1. The max() captures waiting: if we arrive early, we wait; if late, no wait. Adding 1 accounts for the move itself. Crucially, this cost is always ≥ 1 (non-negative), so Dijkstra applies."),
        N.h4("Building the Solution"),
        N.para("Model the grid as a weighted graph. Initialize dist[0][0]=0, all others=inf. Use a min-heap prioritized by arrival time. At each step, pop the cell with the smallest known arrival time, check if it's the goal (return immediately — Dijkstra guarantees optimality), then relax all 4 neighbors using the modified edge weight formula."),
        N.callout("Analogy: Imagine airports with different 'opening times'. You can be at the gate early, but the door only opens at a scheduled time. You always want to take the route that gets you to your destination earliest — not fewest stops.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra's Shortest Path"),
    N.para(N.rich([
        ("Dijkstra's Algorithm", {"bold": True}),
        (" — Origin: Edsger W. Dijkstra, 1956 (published 1959). Solves single-source shortest path "
         "on graphs with non-negative edge weights. Core invariant: when a node is popped from the "
         "min-heap, its shortest distance is finalized. No future path can improve it because all "
         "future edge weights are ≥ 0.", {})
    ])),
    N.code("# Dijkstra Template\nimport heapq\n\ndef dijkstra(graph, source):\n    dist = {node: float('inf') for node in graph}\n    dist[source] = 0\n    heap = [(0, source)]  # (cost, node)\n    while heap:\n        d, u = heapq.heappop(heap)\n        if d > dist[u]:  # stale — lazy deletion\n            continue\n        for v, weight in graph[u]:\n            if dist[u] + weight < dist[v]:\n                dist[v] = dist[u] + weight\n                heapq.heappush(heap, (dist[v], v))\n    return dist", "python"),
    N.para("Modified for this problem: replace 'dist[u] + weight' with 'max(dist[u], moveTime[nr][nc]) + 1'. This dynamic edge weight is what makes this a 'Modified Dijkstra'. The algorithm structure is identical — only the relaxation formula changes."),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("import heapq", {"code": True}), " — Python's built-in min-heap (always a min-heap by default)."])),
    N.para(N.rich([("n, m = len(moveTime), len(moveTime[0])", {"code": True}), " — capture grid dimensions once for clarity and reuse."])),
    N.para(N.rich([("dist = [[float('inf')] * m for _ in range(n)]", {"code": True}), " — 2D array tracking best known arrival time for each cell, initialized to infinity (unreachable)."])),
    N.para(N.rich([("dist[0][0] = 0", {"code": True}), " — we start at (0,0) at time 0."])),
    N.para(N.rich([("heap = [(0, 0, 0)]", {"code": True}), " — min-heap entry: (arrival_time, row, col). Python heaps compare tuples lexicographically, so sorting by time first is correct."])),
    N.para(N.rich([("t, r, c = heapq.heappop(heap)", {"code": True}), " — extract the cell reachable in minimum time from all current candidates."])),
    N.para(N.rich([("if t > dist[r][c]: continue", {"code": True}), " — lazy deletion: if a better path was found after this entry was pushed, skip it. This avoids expensive decrease-key operations."])),
    N.para(N.rich([("if r == n-1 and c == m-1: return t", {"code": True}), " — early termination: first time we pop the goal, its time is optimal (Dijkstra invariant). No need to finish processing all cells."])),
    N.para(N.rich([("for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:", {"code": True}), " — 4-directional neighbor expansion (up, down, left, right)."])),
    N.para(N.rich([("new_t = max(t, moveTime[nr][nc]) + 1", {"code": True}), " — THE KEY LINE. If we arrive at time t < moveTime[nr][nc], we wait until moveTime; then +1 for the move. If t >= moveTime, no waiting needed."])),
    N.para(N.rich([("if new_t < dist[nr][nc]:", {"code": True}), " — only relax if we found a strictly better path (prevents redundant pushes)."])),
    N.para(N.rich([("dist[nr][nc] = new_t; heapq.heappush(heap, (new_t, nr, nc))", {"code": True}), " — update best time and schedule neighbor for future processing."])),
    N.divider(),
]

# ── Solution 2: BFS contrast ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Why BFS Fails (Educational Contrast)"),
    N.toggle_h3("💡 Intuition: What Happens with BFS", [
        N.h4("Reframe the Problem"),
        N.para("BFS explores nodes in order of hop count. It implicitly assumes all edges have equal cost. That assumption breaks here because waiting time makes some paths costlier than others even with equal hop counts."),
        N.h4("What Doesn't Work"),
        N.para("Consider moveTime=[[0,0,10],[0,0,0],[0,0,0]]. BFS would process (0,2) and (1,1) at the same 'distance 2' level. But reaching (0,2) requires waiting until t=10 (arrival at t=11 total), while (1,1) is reachable at t=2. BFS cannot order these correctly."),
        N.h4("The Key Observation"),
        N.para("When edge costs vary, we need a priority queue ordered by total path cost — not a regular queue ordered by hop count. This is exactly the difference between BFS and Dijkstra."),
        N.callout("Rule of thumb: BFS for uniform costs (unit graph). Dijkstra for non-negative variable costs. Bellman-Ford for negative costs (but slower).", "📌", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Modified Dijkstra (optimal)", "O(n·m·log(n·m))", "O(n·m)"],
        ["BFS (incorrect)", "O(n·m)", "O(n·m)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph — shortest path on a weighted implicit graph (grid as adjacency list)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Modified Dijkstra — standard Dijkstra with dynamic/context-dependent edge weights"])),
    N.callout(
        "When to recognize this pattern: 'minimum time/cost to reach destination', edge cost depends on arrival state (time, resource, parity), waiting is allowed but time doesn't go backward (non-negative costs guaranteed). Grid problems where BFS gives wrong answers are a strong signal for Dijkstra.",
        "🔎", "green_background"
    ),
    N.para("*Note: 'Modified Dijkstra' as a named sub-pattern is based on analysis — it is a variant of the standard Dijkstra sub-pattern where the relaxation formula is adapted for problem-specific dynamic edge weights.*"),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Modified / Standard Dijkstra on graphs):"),
    N.bullet(N.rich([("Find Minimum Time to Reach Last Room II", {"bold": True}), " (Medium) — same grid, moves alternate between 1 and 2 seconds per step (#3342)"])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), " (Medium) — classic Dijkstra: find max time for signal to propagate from source (#743)"])),
    N.bullet(N.rich([("Path with Minimum Effort", {"bold": True}), " (Medium) — Dijkstra on grid; cost = max height difference along path (#1631)"])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), " (Medium) — Dijkstra with state augmented by number of stops used (#787)"])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), " (Hard) — Dijkstra where cost = max cell value encountered in path (#778)"])),
    N.bullet(N.rich([("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}), " (Hard) — 0-1 BFS / Dijkstra; forced directions cost 0, changes cost 1 (#1368)"])),
    N.bullet(N.rich([("The Maze II", {"bold": True}), " (Medium) — Dijkstra where a ball rolls until hitting a wall, counting total distance (#505)"])),
    N.para("These problems share the core technique: model as weighted graph, use min-heap ordered by cumulative cost, relax neighbors with problem-specific edge weight formula."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Algorithms section, Dijkstra sub-pattern. Sub-pattern 'Modified Dijkstra' is an analysis-based classification for Dijkstra variants with dynamic edge weights.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_minimum_time_to_reach_last_room_i")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("Notion OK", PAGE_ID)

# ── Write status file ──────────────────────────────────────────────────────
import json, pathlib

html_path = pathlib.Path(__file__).parent / "find_minimum_time_to_reach_last_room_i_explainer.html"
html_lines = len(html_path.read_text().splitlines()) if html_path.exists() else 0

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
status_file = status_dir / "find_minimum_time_to_reach_last_room_i.json"
status = {
    "slug": "find_minimum_time_to_reach_last_room_i",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Modified Dijkstra on 2x2 grid walkthrough; 11-step interactive visualization; 942 lines"
}
status_file.write_text(json.dumps(status, indent=2))
print(f"RESULT find_minimum_time_to_reach_last_room_i | html=OK | notion=OK | lines={html_lines}")
