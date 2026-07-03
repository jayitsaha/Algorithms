"""
gen_number_of_enclaves.py
Notion in-place update for LeetCode #1020 — Number of Enclaves
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-b38b-e003351a80df"

# ── Step 1: Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1020,
    pattern="Graph",
    subpatterns=["DFS Mark Border Connected"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="DFS from border land cells to mark all escapable land; count remaining 1s as enclaves.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing body ──
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── Step 3: Build body blocks ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an m×n binary matrix ", {}),
        ("grid", {"code": True}),
        (", where ", {}),
        ("0", {"code": True}),
        (" represents sea and ", {}),
        ("1", {"code": True}),
        (" represents land. A move consists of walking from one land cell to another "
         "adjacent (4-directional) land cell or walking off the boundary of the grid. "
         "Return the number of land cells in ", {}),
        ("grid", {"code": True}),
        (" for which we cannot walk off the boundary of the grid in any number of moves.", {})
    ])),
    N.divider(),
]

# ── Solution 1: DFS Mark Border-Connected (Interview Pick) ──
solution1_code = '''\
def numEnclaves(grid):
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != 1:
            return
        grid[r][c] = 2  # mark: border-connected, cannot be enclave
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            dfs(r+dr, c+dc)

    # Phase 1: Seed from all 4 borders
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    # Phase 2: Count remaining land = enclaves
    return sum(grid[r][c] == 1
               for r in range(rows)
               for c in range(cols))
'''

blocks += [
    N.h2("Solution 1 — DFS Mark Border-Connected (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'which land cells are enclosed?', ask 'which land cells can escape to the border?' Any land NOT in the escapable set is an enclave. This inversion lets us run a single efficient sweep instead of checking each cell individually."),
        N.h4("What Doesn't Work"),
        N.para("Naive: DFS from every land cell, check if it reaches the border. "
               "That's O(m·n) cells × O(m·n) DFS per cell = O(m²·n²) total. "
               "On a 300×300 grid, that's 8.1 billion operations — too slow."),
        N.h4("The Key Observation"),
        N.para("Graph reachability is transitive. If cell A connects via land to cell B, "
               "and B is on the border, then A can escape. We can propagate this 'escape' "
               "label outward from borders. The border-connected set is exactly all cells "
               "reachable from any border land cell through land."),
        N.h4("Building the Solution"),
        N.para("1. Walk all 4 edges. Any land cell on the border is a DFS seed. "
               "2. DFS from each seed, marking reachable land as 2 (border-connected). "
               "Value 2 acts as the 'visited' flag so each cell is processed at most once. "
               "3. Scan the grid: count cells still equal to 1 — those are the enclaves."),
        N.callout("Analogy: Think of the grid as a walled garden. The border is the wall. "
                  "Pour water in from the wall — wherever it flows through land = escapable. "
                  "Dry land patches that the flood never reached = enclaves.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("rows, cols = len(grid), len(grid[0])", {"code": True}),
                   ("  — Grid dimensions, used for bounds checking in DFS.", {})])),
    N.para(N.rich([("def dfs(r, c)", {"code": True}),
                   ("  — Recursive helper. Marks all land reachable from (r,c) as border-connected.", {})])),
    N.para(N.rich([("if r<0 or r>=rows or c<0 or c>=cols: return", {"code": True}),
                   ("  — Bounds guard: return if we've walked off the grid.", {})])),
    N.para(N.rich([("if grid[r][c] != 1: return", {"code": True}),
                   ("  — Skip water (0) and already-marked cells (2). This prevents revisiting.", {})])),
    N.para(N.rich([("grid[r][c] = 2", {"code": True}),
                   ("  — Mark this cell as border-connected. It will never be counted as an enclave.", {})])),
    N.para(N.rich([("for dr,dc in [...]: dfs(r+dr, c+dc)", {"code": True}),
                   ("  — Explore all 4 neighbors, propagating the 'connected to border' label.", {})])),
    N.para(N.rich([("for r in range(rows): dfs(r,0); dfs(r,cols-1)", {"code": True}),
                   ("  — Seed DFS from left column (c=0) and right column (c=cols-1).", {})])),
    N.para(N.rich([("for c in range(cols): dfs(0,c); dfs(rows-1,c)", {"code": True}),
                   ("  — Seed DFS from top row (r=0) and bottom row (r=rows-1).", {})])),
    N.para(N.rich([("return sum(grid[r][c]==1 ...)", {"code": True}),
                   ("  — Count all cells still land (value 1, never marked). These are the enclaves.", {})])),
    N.divider(),
]

# ── Solution 2: BFS Iterative ──
solution2_code = '''\
from collections import deque

def numEnclaves_bfs(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()

    # Seed all border land at once, mark immediately
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r][c] == 1:
                grid[r][c] = 2
                q.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            if grid[r][c] == 1:
                grid[r][c] = 2
                q.append((r, c))

    # BFS: expand frontier
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                q.append((nr, nc))

    return sum(grid[r][c] == 1 for r in range(rows) for c in range(cols))
'''

blocks += [
    N.h2("Solution 2 — BFS Iterative (No Recursion Limit)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same inversion as DFS: find border-connected land first, count the rest. "
               "BFS uses an explicit queue instead of the call stack."),
        N.h4("What Doesn't Work"),
        N.para("DFS with deep recursion can hit Python's default recursion limit (~1000) "
               "on large grids. A 300×300 all-land grid would stack-overflow. BFS with a "
               "deque is iterative and has no such limit."),
        N.h4("The Key Observation"),
        N.para("BFS and DFS both explore the same connected components — they just differ "
               "in traversal order. For this problem the order doesn't matter, so BFS is "
               "a drop-in replacement with better stack safety."),
        N.h4("Building the Solution"),
        N.para("Seed the deque with ALL border land cells at once (mark them 2 before "
               "enqueuing to avoid double-adds). Then run standard BFS: pop a cell, check "
               "4 neighbors, enqueue any land neighbor after marking it 2. When queue is "
               "empty, all border-connected land is marked. Count remaining 1s."),
    ]),
    N.h3("Code"),
    N.code(solution2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque()", {"code": True}),
                   ("  — BFS frontier queue. deque gives O(1) popleft.", {})])),
    N.para(N.rich([("grid[r][c] = 2; q.append((r,c))", {"code": True}),
                   ("  — Mark before enqueuing! Prevents the same cell being added multiple times.", {})])),
    N.para(N.rich([("while q: r,c = q.popleft()", {"code": True}),
                   ("  — Process one cell at a time from the front of the queue.", {})])),
    N.para(N.rich([("if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1", {"code": True}),
                   ("  — In-bounds AND land AND not-yet-marked. All 3 must hold.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS (recursive)", "O(m·n)", "O(m·n) call stack"],
        ["BFS (iterative)", "O(m·n)", "O(m·n) queue"],
    ]),
    N.callout(
        "Every cell is visited at most once across all DFS/BFS calls (the mark-before-recurse "
        "guard ensures this). Total work is proportional to grid size, not number of islands.",
        "⏱️", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Grid DFS/BFS)", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("DFS Mark Border Connected — flood-fill from boundary outward, eliminate border-reachable cells, count remainder.", {})])),
    N.callout(
        "When to recognize this pattern: "
        "Binary grid + 4-directional movement + 'cannot reach the boundary' or 'enclosed by water' phrasing. "
        "Whenever you need to exclude border-adjacent regions from a count, use border-seeded DFS/BFS.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS-from-border / flood-from-exterior technique:"),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}), (" (Medium) — Mark border-connected O's, flip enclosed O's to X. Closest structural sibling.", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Core DFS island flood-fill; foundational to this sub-pattern.", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}), (" (Medium) — Multi-source DFS from 2 borders, find intersection; same seeding idea.", {})])),
    N.bullet(N.rich([("Flood Fill", {"bold": True}), (" (Easy) — Simplest DFS grid flood-fill; the core mechanic used here.", {})])),
    N.bullet(N.rich([("Walls and Gates", {"bold": True}), (" (Medium) — Multi-source BFS from all gates outward; exact structural analogy.", {})])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), (" (Medium) — Multi-source BFS from all rotten cells; same seeding and sweep.", {})])),
    N.bullet(N.rich([("Number of Closed Islands", {"bold": True}), (" (Medium) — Count fully enclosed 0-islands; direct variant of this problem.", {})])),
    N.para("These problems all share the 'DFS/BFS from boundary inward' technique: "
           "seed from the exterior, mark what's border-connected, operate on the remainder."),
    N.callout("Sub-Pattern Source: Analysis (DFS Mark Border Connected). "
              "Related to Graph section of DSA_Patterns_and_SubPatterns_Guide.md "
              "under DFS/BFS flood-fill variants.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_enclaves")),
    N.para(N.rich([("Step through the border-seeded DFS algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
