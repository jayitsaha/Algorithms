"""gen_unique_paths_iii.py — Notion update for Unique Paths III (LC #980)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c1-8d82-f8a2454903a2"
SLUG = "unique_paths_iii"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=980,
    pattern="Backtracking",
    subpatterns=["Visit All Empty Cells"],
    tc="O(4^(m·n))",
    sc="O(m·n)",
    key_insight="DFS backtracking: mark cells visited in-place with -1, restore on backtrack; count paths reaching End when remaining==1.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ──
SOLUTION_1 = """\
def uniquePathsIII(grid):
    m, n = len(grid), len(grid[0])
    sr = sc = remaining = 0

    # Pre-scan: count walkable cells, find Start
    for r in range(m):
        for c in range(n):
            if grid[r][c] != -1:
                remaining += 1
            if grid[r][c] == 1:
                sr, sc = r, c

    def dfs(r, c, remaining):
        if grid[r][c] == 2:
            return 1 if remaining == 1 else 0

        original = grid[r][c]
        grid[r][c] = -1   # mark visited
        paths = 0

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
                paths += dfs(nr, nc, remaining - 1)

        grid[r][c] = original   # backtrack
        return paths

    return dfs(sr, sc, remaining - 1)
"""

SOLUTION_2 = """\
def uniquePathsIII(grid):
    \"\"\"Bitmask DP alternative (for reference — same exponential complexity).\"\"\"
    m, n = len(grid), len(grid[0])
    sr = sc = 0
    end_r = end_c = 0
    all_cells = 0

    for r in range(m):
        for c in range(n):
            if grid[r][c] != -1:
                all_cells |= (1 << (r * n + c))
            if grid[r][c] == 1:
                sr, sc = r, c
            if grid[r][c] == 2:
                end_r, end_c = r, c

    from functools import lru_cache

    @lru_cache(None)
    def dp(r, c, visited):
        if r == end_r and c == end_c:
            return 1 if visited == all_cells else 0
        total = 0
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            bit = 1 << (nr * n + nc)
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
                if not (visited & bit):
                    total += dp(nr, nc, visited | bit)
        return total

    start_bit = 1 << (sr * n + sc)
    return dp(sr, sc, start_bit)
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m × n", {"bold": True}),
        (" integer grid where each cell is one of: ", {}),
        ("1", {"code": True}),
        (" = Start, ", {}),
        ("0", {"code": True}),
        (" = Empty, ", {}),
        ("-1", {"code": True}),
        (" = Obstacle, ", {}),
        ("2", {"code": True}),
        (" = End.", {}),
        (" Return the number of 4-directional walks from Start to End that walk over every non-obstacle square exactly once.", {})
    ])),
    N.divider()
]

# Solution 1 — DFS Backtracking
blocks += [
    N.h2("Solution 1 — DFS Backtracking with Coverage Count (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count Hamiltonian paths from Start to End on a grid. A Hamiltonian path visits every node exactly once — here, 'nodes' are the non-obstacle cells. This reframe immediately rules out simple DP (no subproblem reuse without exponential state)."),
        N.h4("What Doesn't Work"),
        N.para("Standard DP (as in Unique Paths / Unique Paths II) cannot work here because the answer for 'paths from cell X to End' depends on which cells are already visited — a different set for every different route. BFS similarly cannot count all complete paths without tracking full path history."),
        N.h4("The Key Observation"),
        N.para("Try every possible path (backtracking) and count only those that reach End after visiting all cells. The grid is small (m·n ≤ 20 by constraints), so exponential time is acceptable."),
        N.h4("Building the Solution"),
        N.para("1) Pre-scan: count walkable cells → remaining. 2) DFS from Start, marking visited by overwriting with -1 (obstacle sentinel). 3) Recurse in 4 directions, decrementing remaining each step. 4) At End: valid iff remaining == 1. 5) After each recursion: restore original value (backtrack)."),
        N.callout("Analogy: Floor painter who must paint every tile before leaving through the exit. If stuck in a corner, step back and try another route. Count every complete route.", "🎨", "blue_background")
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(grid), len(grid[0])", {"code": True}), (" — grid dimensions for bounds checking.", {})])),
    N.para(N.rich([("sr = sc = remaining = 0", {"code": True}), (" — initialise start position and walkable-cell counter.", {})])),
    N.para(N.rich([("if grid[r][c] != -1: remaining += 1", {"code": True}), (" — count every non-obstacle cell: Start, empty cells, and End all count.", {})])),
    N.para(N.rich([("if grid[r][c] == 1: sr, sc = r, c", {"code": True}), (" — remember where Start is.", {})])),
    N.para(N.rich([("if grid[r][c] == 2: return 1 if remaining == 1 else 0", {"code": True}), (" — base case: we're at End. remaining==1 means End was the last cell (its own slot in the initial count). Otherwise this path didn't cover everything.", {})])),
    N.para(N.rich([("original = grid[r][c]; grid[r][c] = -1", {"code": True}), (" — save value then overwrite with obstacle sentinel to mark as visited. No extra visited set needed.", {})])),
    N.para(N.rich([("for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:", {"code": True}), (" — try all four cardinal directions.", {})])),
    N.para(N.rich([("if 0<=nr<m and 0<=nc<n and grid[nr][nc] != -1:", {"code": True}), (" — bounds check plus skip visited (-1) and obstacle (-1) cells.", {})])),
    N.para(N.rich([("paths += dfs(nr, nc, remaining - 1)", {"code": True}), (" — recurse with one fewer cell remaining to visit.", {})])),
    N.para(N.rich([("grid[r][c] = original", {"code": True}), (" — BACKTRACK: restore cell to its original value so other paths can visit it.", {})])),
    N.para(N.rich([("return dfs(sr, sc, remaining - 1)", {"code": True}), (" — launch DFS from Start, subtracting 1 from remaining because Start is already 'visited' when we begin.", {})])),
    N.divider()
]

# Solution 2 — Bitmask DP
blocks += [
    N.h2("Solution 2 — Bitmask DP (Top-Down Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("State = (current position, set of visited cells). The visited set fits in a bitmask (up to 20 bits for m·n ≤ 20). This enables memoization: same (position, visited) state encountered from different paths gives the same subproblem result."),
        N.h4("What Doesn't Work"),
        N.para("The backtracking solution re-explores identical sub-states via different routes. Memoization theoretically avoids this — but the state space is O(m·n·2^(m·n)), so in practice it doesn't save much for this problem size."),
        N.h4("The Key Observation"),
        N.para("Two DFS calls with the same (r, c, visited_bitmask) are identical subproblems. By caching them, we can avoid recomputation at the cost of more memory."),
        N.h4("Building the Solution"),
        N.para("Represent each cell as bit (r*n + c) in an integer. Start with start_bit set. Recurse: if at End and visited == all_cells, return 1. Try neighbors not yet set in visited."),
        N.callout("Trade-off: Bitmask DP uses O(m·n·2^(m·n)) memory — much worse than backtracking's O(m·n) stack. For this problem, DFS backtracking is the preferred interview solution.", "⚖️", "yellow_background")
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("all_cells", {"code": True}), (" — bitmask where bit (r*n+c) is set for every non-obstacle cell.", {})])),
    N.para(N.rich([("dp(r, c, visited)", {"code": True}), (" — memoized function: from position (r,c) with visited bitmask, how many complete paths reach End?", {})])),
    N.para(N.rich([("if visited == all_cells:", {"code": True}), (" — all non-obstacle cells are set in the bitmask — a complete Hamiltonian path.", {})])),
    N.para(N.rich([("if not (visited & bit):", {"code": True}), (" — only move to cells not yet visited (bit not set).", {})])),
    N.para(N.rich([("dp(nr, nc, visited | bit)", {"code": True}), (" — recurse with the new cell added to visited bitmask.", {})])),
    N.divider()
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS Backtracking (recommended)", "O(4^(m·n))", "O(m·n)"],
        ["Bitmask DP", "O(m·n·2^(m·n))", "O(m·n·2^(m·n))"]
    ]),
    N.divider()
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Visit All Empty Cells (Hamiltonian Path on Grid)", {})])),
    N.callout(
        "When to recognize this pattern: 'count paths visiting every cell exactly once', grid traversal with coverage requirement, small grid (m·n ≤ 20), no polynomial shortcut visible → backtracking.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related problems
blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same or closely related technique:")]
related = [
    ("Unique Paths", "Medium", "Count paths top-left to bottom-right — DP, no coverage requirement"),
    ("Unique Paths II", "Medium", "DP with obstacles, no Hamiltonian requirement"),
    ("Word Search", "Medium", "DFS backtracking on grid, mark visited in-place; no 'cover all' needed"),
    ("Robot Room Cleaner", "Hard", "Backtracking to cover all reachable cells without full grid view"),
    ("Path with Maximum Gold", "Medium", "DFS + in-place marking, maximize collected value"),
    ("N-Queens", "Hard", "Constraint satisfaction + backtracking, column/diagonal state tracking"),
    ("Sudoku Solver", "Hard", "Constraint propagation + backtracking on a structured grid"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))

blocks += [
    N.para("These problems share the core DFS backtracking technique: explore all possibilities, undo choices on failure."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 10 — BACKTRACKING, Sub-Pattern: Visit All Empty Cells", "📚", "gray_background")
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
