"""
gen_walls_and_gates.py
Regenerate the Notion page for Walls and Gates (LeetCode #286) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8184-a151-e2dda32046e8"
SLUG = "walls_and_gates"

# ─── 1) Set page properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=286,
    pattern="Graph",
    subpatterns=["Multi-source BFS from Gates"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Multi-source BFS from all gates simultaneously; first-visit = minimum distance; cell value == INF serves as visited guard.",
    icon="🟡",
)
print("Properties set ✓")

# ─── 2) Wipe existing body ───
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks ✓")

# ─── 3) Build body blocks ───
blocks = []

# ──── Problem section ────
blocks += [
    N.h2("Problem"),
    N.para(
        "You are given an m×n grid of integers with three special values: "
        "-1 (Wall — impassable), 0 (Gate — destination), and INF=2^31-1 (Empty Room). "
        "Fill each empty room in-place with the minimum number of steps needed to reach "
        "any gate, moving only up/down/left/right. If no gate is reachable, leave the room as INF. "
        "Walls and gates remain unchanged."
    ),
    N.divider(),
]

# ──── Solution 1 — Multi-Source BFS (Interview Pick) ────
blocks += [
    N.h2("Solution 1 — Multi-Source BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "For every empty room, we want the shortest BFS distance to any gate in an unweighted grid. "
            "The naive approach: run an independent BFS from each room to find its nearest gate. "
            "That is O(m·n) BFS calls, each costing O(m·n) → O((m·n)²) total. "
            "For a 1000×1000 grid, that is 10^12 operations — completely infeasible."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "DFS does not find shortest paths. "
            "Dijkstra is correct but overkill — all edges have weight 1, so BFS is optimal. "
            "Running BFS from each room separately is correct but quadratic."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Distance is symmetric: dist(room, gate) = dist(gate, room). "
            "What if we reverse the search direction? Instead of each room asking 'where is my nearest gate?', "
            "let all gates simultaneously broadcast outward. Because BFS explores in non-decreasing distance order, "
            "the first time any room is reached is necessarily from the nearest gate. "
            "This is called multi-source BFS — seed the queue with all sources at distance 0 and run a single BFS pass."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Scan the entire grid. Enqueue every cell where rooms[r][c]==0. "
            "Step 2: Standard BFS loop. Dequeue (r,c). Explore all 4 neighbours. "
            "Step 3: For each neighbour (nr,nc): if in-bounds AND rooms[nr][nc]==INF, "
            "set rooms[nr][nc]=rooms[r][c]+1 and enqueue (nr,nc). "
            "The INF check doubles as a visited guard — walls are -1, gates are 0, settled rooms are positive — "
            "none of them are INF, so they are automatically skipped."
        ),
        N.callout(
            "Analogy: Imagine dropping stones into a pond simultaneously from every gate. "
            "The ripples spread outward at the same speed. The ripple that first reaches any point "
            "on the pond comes from the nearest stone-drop location. Multi-source BFS is exactly this.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
"""from collections import deque

def wallsAndGates(rooms) -> None:
    \"\"\"Modifies rooms in-place, returns None.\"\"\"
    if not rooms or not rooms[0]:
        return
    m, n = len(rooms), len(rooms[0])
    INF = 2**31 - 1
    queue = deque()

    # Phase 1: Seed queue with every gate at distance 0
    for r in range(m):
        for c in range(n):
            if rooms[r][c] == 0:
                queue.append((r, c))

    # Phase 2: Multi-source BFS expansion
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n
                    and rooms[nr][nc] == INF):
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — deque provides O(1) popleft. Using list.pop(0) is O(n) and would make BFS O(n²)."])),
    N.para(N.rich([("if not rooms or not rooms[0]:", {"code": True}), " — Guard against empty grid input to avoid IndexError."])),
    N.para(N.rich([("INF = 2**31 - 1", {"code": True}), " — The sentinel value that marks empty rooms in the problem. Must match the constraint exactly."])),
    N.para(N.rich([("Phase 1 double loop:", {"bold": True}), " Scans every cell in O(m·n). Every gate cell is enqueued. These become our BFS starting frontier at distance 0."])),
    N.para(N.rich([("dirs = [(0,1),(0,-1),(1,0),(-1,0)]", {"code": True}), " — The four cardinal directions (right, left, down, up). Diagonal movement is not permitted."])),
    N.para(N.rich([("r, c = queue.popleft()", {"code": True}), " — When we dequeue a cell, rooms[r][c] is already its final minimum distance. BFS guarantees this."])),
    N.para(N.rich([("rooms[nr][nc] == INF", {"code": True}), " — This is the visited check. Walls are -1 (≠INF), gates are 0 (≠INF), settled rooms are positive (≠INF). Only unvisited empty rooms match."])),
    N.para(N.rich([("rooms[nr][nc] = rooms[r][c] + 1", {"code": True}), " — Write the distance: one step further than the current cell's distance from its nearest gate."])),
    N.callout(
        "No separate visited set needed — the room value itself tracks visited status. "
        "This saves O(m·n) extra space (though overall space is still O(m·n) for the queue).",
        "💡", "green_background"
    ),
    N.divider(),
]

# ──── Solution 2 — Brute Force (for comparison only) ────
blocks += [
    N.h2("Solution 2 — Brute Force: BFS from Each Room (DO NOT USE)"),
    N.toggle_h3("💡 Intuition: Why This Fails", [
        N.h4("Reframe the Problem"),
        N.para("Treat each empty room as a BFS source. Run a separate BFS outward until we hit a gate. Record that distance."),
        N.h4("What Doesn't Work"),
        N.para(
            "For each of O(m·n) rooms we run a BFS of cost O(m·n). "
            "Total: O((m·n)²). For a 300×300 grid: ~8 billion operations. "
            "This correctly computes all distances but is impractical for large inputs."
        ),
        N.h4("The Key Observation"),
        N.para("The multi-source BFS approach solves this 1000× faster by reversing the direction of search."),
    ]),
    N.h3("Code"),
    N.code(
"""from collections import deque

def wallsAndGates_brute(rooms) -> None:
    if not rooms: return
    m, n = len(rooms), len(rooms[0])
    INF = 2**31 - 1
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    for r in range(m):
        for c in range(n):
            if rooms[r][c] != INF:
                continue  # only process empty rooms
            # BFS from this room to find nearest gate
            queue = deque([(r, c, 0)])
            visited = {(r, c)}
            found = False
            while queue and not found:
                cr, cc, dist = queue.popleft()
                for dr, dc in dirs:
                    nr, nc = cr+dr, cc+dc
                    if (0 <= nr < m and 0 <= nc < n
                            and (nr, nc) not in visited
                            and rooms[nr][nc] != -1):
                        if rooms[nr][nc] == 0:
                            rooms[r][c] = dist + 1
                            found = True
                            break
                        visited.add((nr, nc))
                        queue.append((nr, nc, dist+1))"""
    ),
    N.divider(),
]

# ──── Complexity table ────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Multi-Source BFS (optimal)", "O(m·n)", "O(m·n)"],
        ["Brute Force BFS per room", "O((m·n)²)", "O(m·n)"],
    ]),
    N.divider(),
]

# ──── Pattern Classification ────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (BFS on Implicit Grid Graph)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Multi-source BFS from Gates — multiple sources enqueued simultaneously at distance 0; BFS wave radiates outward filling each room with minimum gate distance."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Grid/graph problem asking for 'distance to nearest X'\n"
        "• Multiple valid source nodes, all equally close at distance 0\n"
        "• Keywords: 'nearest gate', 'closest 0', 'minimum steps to any X'\n"
        "• Reversing the search direction (from targets to sources) transforms O((mn)²) → O(mn)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ──── Related Problems ────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Multi-Source BFS technique:"),
    N.bullet(N.rich([("01 Matrix (LeetCode 542)", {"bold": True}), " (Medium) — Multi-source BFS from all 0-cells to fill 1-cells with distance to nearest 0. Exact same pattern."])),
    N.bullet(N.rich([("Rotting Oranges (LeetCode 994)", {"bold": True}), " (Medium) — Multi-source BFS from all rotten oranges; count BFS levels (= minutes elapsed)."])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow (LeetCode 417)", {"bold": True}), " (Medium) — BFS/DFS from two border sources (Pacific and Atlantic); intersect reachable sets."])),
    N.bullet(N.rich([("Nearest Exit from Entrance in Maze (LeetCode 1926)", {"bold": True}), " (Medium) — Single-source BFS from entrance; first border cell reached = nearest exit."])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix (LeetCode 1091)", {"bold": True}), " (Medium) — Single-source BFS through 0-valued cells from top-left to bottom-right."])),
    N.bullet(N.rich([("As Far from Land as Possible (LeetCode 1162)", {"bold": True}), " (Medium) — Multi-source BFS from all land cells; maximize distance in water cells."])),
    N.bullet(N.rich([("Surrounded Regions (LeetCode 130)", {"bold": True}), " (Medium) — BFS from borders to mark safe 'O' cells; same 'reverse search direction' insight."])),
    N.para("These problems share the core technique: seeding BFS with multiple sources simultaneously to compute minimum distances in O(V+E) instead of O(sources × (V+E))."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, BFS: Shortest Path Unweighted sub-pattern.", "📚", "gray_background"),
]

# ──── Embed section ────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the multi-source BFS on the canonical 4×4 grid — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4) Append all blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"Blocks appended: {len(blocks)} ✓")
print(f"NOTION OK {PAGE_ID}")
