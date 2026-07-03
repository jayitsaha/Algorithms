"""
Notion page rebuild for Pacific Atlantic Water Flow (#417)
Run: python3 gen_pacific_atlantic_water_flow.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8150-9f29-cf3be26b1058"
SLUG    = "pacific_atlantic_water_flow"

print(f"Updating Notion page {PAGE_ID}...")

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 417,
    pattern     = "Graph",
    subpatterns = ["DFS from Both Oceans"],
    tc          = "O(m·n)",
    sc          = "O(m·n)",
    key_insight = "Reverse the flow: DFS uphill from ocean borders; intersect two visited sets.",
    icon        = "🟡",
)
print("Properties set ✓")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks ✓")

# ── 3) Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"code": True}),
        (" integer matrix ", {}),
        ("heights", {"code": True}),
        (" representing the height of each cell, return a list of all coordinates ", {}),
        ("[r, c]", {"code": True}),
        (" such that rain water can flow from ", {}),
        ("[r, c]", {"code": True}),
        (" to both the Pacific Ocean (touching top row and left column) and the Atlantic Ocean (touching bottom row and right column). "
         "Water can flow to a neighbor (up/down/left/right) if the neighbor's height is ≤ the current cell's height.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Reverse DFS (Interview Pick) ──
SOL1_CODE = """\
def pacificAtlantic(heights):
    if not heights or not heights[0]:
        return []
    m, n = len(heights), len(heights[0])

    def dfs(r, c, visited):
        visited.add((r, c))
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < m
                and 0 <= nc < n
                and (nr, nc) not in visited
                and heights[nr][nc] >= heights[r][c]):  # UPHILL
                dfs(nr, nc, visited)

    pacific  = set()
    atlantic = set()

    for c in range(n):
        dfs(0, c, pacific)      # top row → Pacific
        dfs(m-1, c, atlantic)   # bottom row → Atlantic
    for r in range(m):
        dfs(r, 0, pacific)      # left col → Pacific
        dfs(r, n-1, atlantic)   # right col → Atlantic

    return [[r, c] for r, c in pacific & atlantic]
"""

blocks += [
    N.h2("Solution 1 — Reverse DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need every cell from which rain can flow downhill to BOTH the Pacific (top/left) and Atlantic (bottom/right). "
               "Simulating forward flow from each cell would be O(m²n²) — too slow."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each of the m·n cells, run a full DFS toward ocean edges. "
               "Each DFS is O(m·n), so total is O(m²n²). On a 200×200 grid that's 1.6 billion operations — TLE."),
        N.h4("The Key Observation"),
        N.para("Reverse the flow direction. \"Water at cell X can reach the ocean\" is equivalent to "
               "\"the ocean can reach X going uphill.\" So: start DFS from all ocean-border cells and flood uphill "
               "(visit neighbors with height ≥ current). Each cell is visited at most once per ocean."),
        N.h4("Building the Solution"),
        N.para("1. Initialize two visited sets: pacific and atlantic.\n"
               "2. Seed pacific with all top-row and left-column cells; run uphill DFS.\n"
               "3. Seed atlantic with all bottom-row and right-column cells; run uphill DFS.\n"
               "4. Return cells in both sets (intersection)."),
        N.callout(
            "Analogy: Imagine the ocean is a dye that seeps uphill into the landscape. "
            "Wherever both dyes (blue=Pacific, green=Atlantic) overlap is a dual-draining cell.",
            "🌊", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not heights or not heights[0]:", {"code": True}),
                   (" — Guard: return [] for empty grid or empty rows.", {})])),
    N.para(N.rich([("m, n = len(heights), len(heights[0])", {"code": True}),
                   (" — Capture grid dimensions.", {})])),
    N.para(N.rich([("def dfs(r, c, visited):", {"code": True}),
                   (" — Inner helper that flood-fills uphill from a given cell into the visited set.", {})])),
    N.para(N.rich([("visited.add((r, c))", {"code": True}),
                   (" — Mark current cell as reachable from this ocean.", {})])),
    N.para(N.rich([("for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:", {"code": True}),
                   (" — Explore all 4 neighbors (right, left, down, up).", {})])),
    N.para(N.rich([("heights[nr][nc] >= heights[r][c]", {"code": True}),
                   (" — CRITICAL: visit neighbor only if it is at least as high (uphill or flat). "
                    "This is the reverse of forward flow (downhill). Writing <= here is the classic bug.", {})])),
    N.para(N.rich([("dfs(0, c, pacific) / dfs(m-1, c, atlantic)", {"code": True}),
                   (" — Seed top row into pacific, bottom row into atlantic. Then same for columns.", {})])),
    N.para(N.rich([("return [[r,c] for r,c in pacific & atlantic]", {"code": True}),
                   (" — Python set intersection returns cells in BOTH sets. "
                    "These are all cells that can drain to both oceans.", {})])),
    N.divider(),
]

# ── Solution 2 — BFS with deque ──
SOL2_CODE = """\
from collections import deque

def pacificAtlantic(heights):
    m, n = len(heights), len(heights[0])

    def bfs(seeds):
        q = deque(seeds)
        vis = set(seeds)          # mark before processing
        while q:
            r, c = q.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n
                        and (nr, nc) not in vis
                        and heights[nr][nc] >= heights[r][c]):
                    vis.add((nr, nc))   # mark BEFORE enqueuing
                    q.append((nr, nc))
        return vis

    pac_seeds = [(0, c) for c in range(n)] + [(r, 0) for r in range(m)]
    atl_seeds = [(m-1, c) for c in range(n)] + [(r, n-1) for r in range(m)]

    pac = bfs(pac_seeds)
    atl = bfs(atl_seeds)
    return [[r, c] for r, c in pac & atl]
"""

blocks += [
    N.h2("Solution 2 — Reverse BFS (Preferred in Python — No Recursion Limit)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same reverse-flow insight as Solution 1, but using a FIFO queue instead of a recursion stack."),
        N.h4("What Doesn't Work"),
        N.para("Recursive DFS on Python can hit the default call-stack limit of ~1000 on large grids (200×200 = 40,000 cells). "
               "BFS is iterative and avoids this entirely."),
        N.h4("The Key Observation"),
        N.para("BFS processes cells level by level from the ocean inward. "
               "The key BFS invariant: mark cells in vis BEFORE enqueuing, not after dequeuing. "
               "This prevents enqueuing the same cell multiple times."),
        N.h4("Building the Solution"),
        N.para("Collect all border cells as seeds into a deque. "
               "Process cell by cell: for each, enqueue unvisited uphill neighbors. "
               "Return the visited set. Intersect two runs."),
        N.callout("Mark visited BEFORE enqueue (BFS idiom). Marking after dequeue allows duplicates in the queue, "
                  "which wastes work but is still correct — marking before is the clean version.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque(seeds)", {"code": True}), (" — Start the queue with all border cells already populated.", {})])),
    N.para(N.rich([("vis = set(seeds)", {"code": True}), (" — Pre-mark all seeds so they won't be re-enqueued.", {})])),
    N.para(N.rich([("vis.add((nr, nc))", {"code": True}), (" — Mark BEFORE appending to queue (BFS correctness invariant).", {})])),
    N.para(N.rich([("pac_seeds = [...] + [...]", {"code": True}), (" — Collect all top-row and left-column cells as Pacific seeds in one list.", {})])),
    N.para(N.rich([("pac & atl", {"code": True}), (" — Python set intersection. O(min(|pac|, |atl|)) time.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (DFS per cell)", "O(m²n²)", "O(m·n)", "TLE on large grids"],
        ["Reverse DFS (Solution 1)", "O(m·n)", "O(m·n)", "Optimal; may hit recursion limit"],
        ["Reverse BFS (Solution 2)", "O(m·n)", "O(m·n)", "Optimal; safe for Python"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS from Both Oceans (Multi-Source Reverse BFS/DFS, Intersection of Reachable Sets)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Which cells can reach X AND Y?' → run two traversals, intersect\n"
        "• 'Mark all cells reachable from a border' → seed entire border, flood inward\n"
        "• Flow problem where forward is expensive → try reversing the direction\n"
        "• Result = intersection or union of two reachability sets",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (multi-source BFS/DFS, border seeding, or reachability intersection):"),
]
related = [
    ("Number of Islands", "Medium", "DFS/BFS flood-fill to count connected components in grid (#200)"),
    ("Surrounded Regions", "Medium", "DFS from border 'O' cells; interior 'O's not reachable = captured (#130)"),
    ("Walls and Gates", "Medium", "Multi-source BFS from all gates simultaneously to fill distances (#286)"),
    ("Rotting Oranges", "Medium", "Multi-source BFS from all rotten oranges; find min time to infect all (#994)"),
    ("Shortest Path in Binary Matrix", "Medium", "BFS from top-left on 0-valued cells (#1091)"),
    ("Max Area of Island", "Medium", "DFS flood-fill tracking connected component size (#695)"),
    ("Word Ladder II", "Hard", "Bidirectional BFS from both start and end words; intersection = meeting point (#126)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (f" — {note}", {}),
    ])))
blocks += [
    N.para("These problems share the core technique: flood-fill from a known boundary, intersect reachable sets."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section\n"
              "Sub-Pattern: DFS from Both Oceans (multi-source reverse BFS/DFS)", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks ✓")
print(f"NOTION OK {PAGE_ID}")
