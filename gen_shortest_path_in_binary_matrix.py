"""
Notion page generator for: Shortest Path in Binary Matrix (#1091)
Runs against the existing page: 39193418-809c-81b1-87e1-dff1cbf49db2
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81b1-87e1-dff1cbf49db2"

# ─── 1) Properties ───────────────────────────────────────────────────────────
N.set_properties(PAGE_ID,
    difficulty="Medium", number=1091,
    pattern="Graph Algorithms",
    subpatterns=["BFS 8 Directions"],
    tc="O(n²)", sc="O(n²)",
    key_insight="BFS with 8-directional expansion; first time goal is reached is the shortest path. Flip 0→1 as visited marker.",
    icon="🟡")
print("Properties set ✓")

# ─── 2) Wipe old content ─────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks ✓")

# ─── 3) Build body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("n×n", {"bold": True}),
        (" binary matrix ", {}),
        ("grid", {"code": True}),
        (", return the length of the shortest clear path from the top-left cell ", {}),
        ("(0, 0)", {"code": True}),
        (" to the bottom-right cell ", {}),
        ("(n-1, n-1)", {"code": True}),
        (". A clear path moves through cells with value ", {}),
        ("0", {"code": True}),
        (" in ", {}),
        ("8 directions", {"bold": True}),
        (" (horizontal, vertical, and diagonal). The path length is the number of visited cells (including start and end). Return ", {}),
        ("-1", {"code": True}),
        (" if no such path exists.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: BFS (Optimal) ──
sol1_code = """\
from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    # Guard: if start or end is blocked, impossible
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    # Edge case: 1x1 grid
    if n == 1:
        return 1
    # 8-directional deltas (all neighbors including diagonals)
    DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    # BFS: (row, col, distance)
    queue = deque([(0, 0, 1)])
    grid[0][0] = 1  # Mark start visited (flip 0 → 1)
    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                if nr == n-1 and nc == n-1:
                    return dist + 1   # Goal reached — shortest path
                grid[nr][nc] = 1      # Mark visited at enqueue time
                queue.append((nr, nc, dist + 1))
    return -1  # Queue exhausted, no path found
"""

blocks += [
    N.h2("Solution 1 — BFS with 8 Directions (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the fewest steps to get from top-left to bottom-right, moving only through 0-cells, with 8 possible move directions. This is exactly a shortest path problem on an unweighted graph — each cell is a node, each valid adjacent cell is an edge of cost 1."),
        N.h4("What Doesn't Work"),
        N.para("DFS explores deeply before broadly. It might find a long winding path before it ever tries the short diagonal route. To use DFS for shortest path, we would need to explore all paths and take the minimum — that is O(8^(n²)), completely infeasible. We need an approach that inherently prefers shorter paths."),
        N.h4("The Key Observation"),
        N.para("BFS processes cells in order of distance from the source. All cells at distance 1 are processed before any at distance 2, and so on. This means the first time BFS reaches the goal, it has taken the minimum possible number of steps — no shorter route could have been missed."),
        N.h4("Building the Solution"),
        N.para("Start BFS at (0,0) with dist=1. For each dequeued cell, try all 8 neighbors. Mark cells visited when enqueuing (not dequeuing) to prevent duplicate queue entries. If any valid neighbor is the goal, return dist+1 immediately. If the queue empties, return -1."),
        N.callout("Analogy: BFS is like flooding water into the grid from the start. Water spreads in all 8 directions simultaneously, at equal speed. The first moment water reaches the goal is the soonest possible — that's the shortest path length.", "💧", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), (" — deque provides O(1) popleft. Python's list.pop(0) is O(n) and would make BFS O(n³) overall.", {})])),
    N.para(N.rich([("if grid[0][0]==1 or grid[n-1][n-1]==1", {"code": True}), (" — Guard clause: if start or end is blocked, no path is possible. Return -1 immediately without running BFS.", {})])),
    N.para(N.rich([("if n == 1: return 1", {"code": True}), (" — Special case: a 1×1 grid where start equals the goal. The path length is 1 (just the start cell itself).", {})])),
    N.para(N.rich([("DIRS = [(...)...]", {"code": True}), (" — All 8 direction deltas: the 8 combinations of dr,dc ∈ {-1,0,1} excluding (0,0). Covers N, NE, E, SE, S, SW, W, NW.", {})])),
    N.para(N.rich([("queue = deque([(0, 0, 1)])", {"code": True}), (" — Initialize BFS with the start cell at distance 1 (we've visited 1 cell so far — the start itself).", {})])),
    N.para(N.rich([("grid[0][0] = 1", {"code": True}), (" — Mark start as visited by flipping 0→1. Reusing the grid as a visited array saves O(n²) extra space.", {})])),
    N.para(N.rich([("r, c, dist = queue.popleft()", {"code": True}), (" — FIFO dequeue: always process the closest cell first. This enforces the distance-ordering invariant of BFS.", {})])),
    N.para(N.rich([("if 0<=nr<n and 0<=nc<n and grid[nr][nc]==0", {"code": True}), (" — Validity check: in bounds AND unblocked/unvisited. Since we flip 0→1 on visit, this single condition filters both obstacles and visited cells.", {})])),
    N.para(N.rich([("if nr==n-1 and nc==n-1: return dist+1", {"code": True}), (" — Goal detected when enqueuing the neighbor. Return dist+1 because we are taking one more step to reach this neighbor.", {})])),
    N.para(N.rich([("grid[nr][nc] = 1; queue.append(...)", {"code": True}), (" — Mark visited (at enqueue time) and add to queue with incremented distance. Marking at enqueue prevents the same cell appearing in the queue multiple times.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — Queue exhausted without reaching (n-1,n-1). No clear path exists.", {})])),
    N.divider(),
]

# ── Solution 2: Alternative BFS (goal check at dequeue) ──
sol2_code = """\
from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    queue = deque([(0, 0, 1)])
    grid[0][0] = 1
    while queue:
        r, c, dist = queue.popleft()
        if r == n-1 and c == n-1:
            return dist          # ← goal check at dequeue
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    queue.append((nr, nc, dist + 1))
    return -1
"""

blocks += [
    N.h2("Solution 2 — BFS (Goal Check at Dequeue Variant)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same BFS approach. The only difference is when we check for the goal: instead of checking when we discover (enqueue) the goal's cell, we check when we pop it from the queue."),
        N.h4("What Doesn't Work"),
        N.para("The 'check at dequeue' approach still works correctly — BFS ordering ensures the first dequeue of the goal is at minimum distance. The downside is that the goal cell is added to the queue before we realize it is the answer, which adds one extra queue operation."),
        N.h4("The Key Observation"),
        N.para("Both approaches (check at enqueue vs. check at dequeue) produce the same answer. The enqueue-check variant is marginally more efficient because it avoids enqueueing the goal. The dequeue-check variant is arguably more readable. Use whichever you find clearer in an interview."),
        N.h4("Building the Solution"),
        N.para("Initialize with dist=1 (including start). Check for goal when dequeuing: if r==n-1 and c==n-1, return dist. Uses nested loops for the 8 directions — equivalent to the flat DIRS list but written differently."),
        N.callout("Note: This variant requires handling the 1×1 case implicitly — when dist=1 is dequeued at (0,0) and (0,0) is also (n-1,n-1), it returns 1 correctly.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if r == n-1 and c == n-1: return dist", {"code": True}), (" — Goal check happens at dequeue time. Since BFS processes cells in order of distance, the first time this check triggers is at the minimum distance.", {})])),
    N.para(N.rich([("for dr in (-1,0,1): for dc in (-1,0,1):", {"code": True}), (" — Generates all 9 combinations; the skip condition eliminates (0,0). Produces the same 8 directions as the flat DIRS list in Solution 1.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS (enqueue check)", "O(n²)", "O(n²)", "Optimal; goal found one step early"],
        ["BFS (dequeue check)", "O(n²)", "O(n²)", "Equivalent; goal cell enters queue once"],
        ["DFS all paths", "O(8^(n²))", "O(n²)", "Exponential — cannot use for shortest path"],
        ["A* search", "O(n² log n)", "O(n²)", "Faster in practice; same worst case; overkill here"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Algorithms", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS 8 Directions", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("'Shortest path' + 'grid' + 'equal cost moves' → BFS. '8 directions' or 'includes diagonals' → extend direction vectors from 4 to 8. 'Binary matrix (0 open, 1 blocked)' → BFS with grid[nr][nc]==0 condition. Multi-source variant: enqueue all source cells simultaneously at dist=0.", {})]),
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS on Grid technique (Guide Section 17.2):"),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), (" (Medium) — Multi-source BFS from all 0s simultaneously; fills each cell with distance to nearest 0. LC #542", {})])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), (" (Medium) — Multi-source BFS from all rotten oranges; simulates 4-directional spread. LC #994", {})])),
    N.bullet(N.rich([("Walls and Gates", {"bold": True}), (" (Medium) — Multi-source BFS from all gates; fills empty rooms with min distance to a gate. LC #286", {})])),
    N.bullet(N.rich([("Minimum Knight Moves", {"bold": True}), (" (Medium) — BFS with 8 L-shaped direction vectors; same template, different DIRS. LC #1197", {})])),
    N.bullet(N.rich([("Snakes and Ladders", {"bold": True}), (" (Medium) — BFS shortest path on a board with teleporters; linearize board then BFS. LC #909", {})])),
    N.bullet(N.rich([("Shortest Path with Obstacles Elimination", {"bold": True}), (" (Hard) — BFS with 3D state (r, c, k) where k = wall-breaks remaining. LC #1293", {})])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), (" (Medium) — BFS on state space; same BFS template applied to string states. LC #752", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — DFS/BFS to mark and count connected components on a 0/1 grid. LC #200", {})])),
    N.para("These problems share the same BFS-on-grid core: model cells as graph nodes, use a deque for O(1) enqueue/dequeue, mark visited inline to prevent revisiting."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.2 — BFS 8 Directions", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("shortest_path_in_binary_matrix")),
    N.para(N.rich([("Step through the BFS algorithm visually — watch the frontier wave expand level-by-level until the goal is reached. Use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ─── 4) Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks ✓")
print(f"NOTION OK {PAGE_ID}")
