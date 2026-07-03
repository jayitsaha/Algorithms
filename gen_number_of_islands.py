"""
gen_number_of_islands.py — Rebuild the Notion page for Number of Islands (LC #200)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8181-8a04-c16a369c4710"

# ─── 1. Set properties ───────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=200,
    pattern="Graph",
    subpatterns=["DFS Mark Visited"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Scan grid; each unvisited '1' is a new island — sink the entire connected component via DFS before continuing.",
    icon="🟡"
)
print("  Properties OK")

# ─── 2. Wipe existing body ───────────────────────────────────────────────────
print("Wiping existing body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

# ─── 3. Build new body ───────────────────────────────────────────────────────
print("Building content blocks...")

DFS_CODE = """\
def numIslands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] == '0': return
        grid[r][c] = '0'          # sink this cell
        dfs(r+1, c); dfs(r-1, c)
        dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count"""

BFS_CODE = """\
from collections import deque

def numIslands(grid):
    if not grid: return 0
    rows, cols, count = len(grid), len(grid[0]), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                grid[r][c] = '0'      # sink before enqueue
                q = deque([(r, c)])
                while q:
                    row, col = q.popleft()
                    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr, nc = row+dr, col+dc
                        if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]=='1':
                            grid[nr][nc] = '0'
                            q.append((nr, nc))
    return count"""

UNION_FIND_CODE = """\
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        self.count -= 1

def numIslands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                uf.count += 1
                for dr, dc in [(1,0),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]=='1':
                        uf.union(r*cols+c, nr*cols+nc)
    return uf.count"""

blocks = []

# ── Problem statement ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an ", ("m × n", {"bold": True}),
        " grid of characters where each cell is either ",
        ("'1'", {"code": True}), " (land) or ",
        ("'0'", {"code": True}),
        " (water), return the number of islands.\n\n"
        "An island is surrounded by water and is formed by connecting adjacent land cells "
        "horizontally or vertically. You may assume all four edges of the grid are all "
        "surrounded by water."
    ])),
    N.divider(),
]

# ── Solution 1: DFS ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — DFS Sink the Island (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think of the grid as a graph: each '1' cell is a node, and two '1' cells share "
            "an edge if they are horizontally or vertically adjacent. Counting islands = "
            "counting connected components in this graph."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive brute-force: for each '1' cell, do a fresh scan to count how many cells "
            "belong to its island, then avoid re-counting them. But tracking which cells "
            "belong to which island without revisiting is complicated and leads to O((m·n)²) "
            "time — far too slow for large grids."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Once we identify a land cell as part of an island, we want to instantly eliminate "
            "its entire connected island from future consideration. DFS does this in one sweep: "
            "visit every connected '1' and set it to '0'. After DFS completes, the entire island "
            "has been 'sunk' into the water — the outer scanner will never see it again."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Scan every cell.\n"
            "2. When grid[r][c] == '1': increment count (new island found).\n"
            "3. Call dfs(r, c) which sets grid[r][c] = '0' then recurses in 4 directions.\n"
            "4. DFS base cases: out-of-bounds OR cell is '0' → return.\n"
            "5. Continue outer scan — all sunk cells look like water; they're skipped."
        ),
        N.callout(
            "Analogy: Imagine flooding each island with water the moment you spot it from a helicopter. "
            "Once flooded, it disappears from view — you only count islands that are still dry.",
            "🌊", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(DFS_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not grid: return 0", {"code": True}),
                   " — Guard for empty input; an empty grid has 0 islands."])),
    N.para(N.rich([("rows, cols = len(grid), len(grid[0])", {"code": True}),
                   " — Cache dimensions to avoid repeated len() calls."])),
    N.para(N.rich([("count = 0", {"code": True}),
                   " — Island counter; increments once per connected component discovered."])),
    N.para(N.rich([("def dfs(r, c):", {"code": True}),
                   " — Inner helper that sinks an entire island starting at (r, c)."])),
    N.para(N.rich([("if r < 0 or r >= rows or c < 0 or c >= cols: return", {"code": True}),
                   " — Bounds check FIRST. Prevents IndexError. Must precede grid access."])),
    N.para(N.rich([("if grid[r][c] == '0': return", {"code": True}),
                   " — Water or already-sunk cell: nothing to do, stop recursion here."])),
    N.para(N.rich([("grid[r][c] = '0'", {"code": True}),
                   " — SINK the current cell BEFORE recursing — marks it visited in O(1), prevents re-entry."])),
    N.para(N.rich([("dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)", {"code": True}),
                   " — Explore all 4 neighbours. No diagonal — problem says horizontal/vertical only."])),
    N.para(N.rich([("if grid[r][c] == '1': count += 1; dfs(r, c)", {"code": True}),
                   " — Outer loop: when fresh land is found, count it and sink the whole island."])),
    N.para(N.rich([("return count", {"code": True}),
                   " — Total distinct connected components (islands)."])),
    N.divider(),
]

# ── Solution 2: BFS ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative BFS (Production-Safe, No Stack Overflow)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same connected-component problem, but we need to handle large grids where "
            "recursive DFS would exceed Python's default call stack depth of ~1000 frames."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "For a 300×300 all-land grid, recursive DFS would attempt 90,000 nested calls. "
            "Python raises RecursionError. Setting sys.setrecursionlimit is a hack. "
            "Better: use an explicit queue (BFS) to manage the frontier iteratively."
        ),
        N.h4("The Key Observation"),
        N.para(
            "BFS and DFS both explore every cell exactly once. BFS uses a deque instead of the "
            "call stack. The key detail: sink the cell ('0') BEFORE enqueuing it, not when "
            "dequeuing it. If you sink on dequeue, the same cell could be enqueued multiple "
            "times (by different neighbours), causing redundant work."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Same outer scan. When '1' is found: count++, set to '0', enqueue. "
            "While queue non-empty: dequeue (row, col), check 4 neighbours. "
            "For each valid '1' neighbour: set to '0' and enqueue."
        ),
        N.callout(
            "Interview tip: prefer BFS when the problem involves large grids or when the interviewer "
            "asks about production robustness. It eliminates recursion depth concerns entirely.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(BFS_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("grid[r][c] = '0'", {"code": True}),
                   " before enqueue — sink immediately to prevent duplicate enqueues from multiple neighbours."])),
    N.para(N.rich([("q = deque([(r, c)])", {"code": True}),
                   " — Start BFS from the discovered island cell."])),
    N.para(N.rich([("for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:", {"code": True}),
                   " — Iterate over all 4 cardinal directions."])),
    N.para(N.rich([("if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]=='1':", {"code": True}),
                   " — Combined bounds + land check in one condition."])),
    N.divider(),
]

# ── Solution 3: Union-Find ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Union-Find (Best for Dynamic Grids)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "What if islands are added one cell at a time and we need the count after each addition? "
            "DFS/BFS would need to re-scan the whole grid each time — too slow. "
            "Union-Find maintains connected components incrementally in near-O(1) per operation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Each land cell starts as its own component (its own island). When we add a new land cell, "
            "we union it with each adjacent land cell. The component count decreases by 1 for each "
            "merge. Union-Find with path compression and union-by-rank gives O(α) per operation "
            "where α is the inverse Ackermann function — effectively constant."
        ),
        N.h4("When to Recognize"),
        N.para(
            "Use Union-Find when: (a) the grid is updated dynamically and you need live counts, "
            "(b) you need to query 'are two cells on the same island?' in O(1), "
            "(c) the problem is LeetCode #305 (add land one cell at a time)."
        ),
        N.callout(
            "Algorithm: Union-Find (Disjoint Set Union). Each cell maps to a flat array index "
            "via index = r * cols + c. Only union with right and down neighbours (to avoid double-counting). "
            "The count field in UnionFind tracks the number of distinct components.",
            "🔬", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(UNION_FIND_CODE),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS (grid mutation)", "O(m·n)", "O(m·n)", "Interview pick; elegant and minimal"],
        ["BFS iterative", "O(m·n)", "O(m·n)", "Production-safe; no stack overflow"],
        ["Union-Find", "O(m·n·α)", "O(m·n)", "Best for dynamic grids (#305)"],
    ]),
    N.divider(),
]

# ── Pattern classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS Mark Visited; Union-Find (for dynamic variant)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count groups / clusters / components' in a 2D grid\n"
        "• 'Cells connected horizontally and vertically' → graph with 4-directional edges\n"
        "• 'Flood fill / spread from origin cells' → multi-source BFS\n"
        "• 'Distinct regions satisfying a property' → DFS + visited marking\n"
        "• 'Dynamic updates to connected structure' → Union-Find",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS Mark Visited / connected-component technique:"),
    N.bullet(N.rich([("Max Area of Island", {"bold": True}),
                     " (Medium) — Same DFS sink; track component size, return max (#695)"])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}),
                     " (Medium) — DFS from borders to protect edge-connected 'O's; flip the rest (#130)"])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}),
                     " (Medium) — DFS from both ocean borders; find cells reachable from both (#417)"])),
    N.bullet(N.rich([("Number of Closed Islands", {"bold": True}),
                     " (Medium) — Pre-sink border-connected islands via DFS, then count interior (#1254)"])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}),
                     " (Medium) — Multi-source BFS from all rotten cells; count time steps (#994)"])),
    N.bullet(N.rich([("Flood Fill", {"bold": True}),
                     " (Easy) — Classic paint-bucket DFS on a grid; foundational pattern (#733)"])),
    N.bullet(N.rich([("Number of Islands II", {"bold": True}),
                     " (Hard) — Islands added dynamically; Union-Find with online count (#305)"])),
    N.bullet(N.rich([("Word Search", {"bold": True}),
                     " (Medium) — DFS on grid with backtracking for path matching (#79)"])),
    N.para("These problems share the core technique: launch DFS/BFS from each undiscovered '1' cell and mark the entire connected component as visited before continuing the outer scan."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, DFS Mark Visited sub-pattern", "📚", "gray_background"),
]

# ── Embed section ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_islands")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
