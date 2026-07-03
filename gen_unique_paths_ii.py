"""
gen_unique_paths_ii.py — Notion in-place update for Unique Paths II (LeetCode #63)
Run from Algorithms/ directory: python3 gen_unique_paths_ii.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81bc-8078-fe28f9b3b871"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=63,
    pattern="Dynamic Programming",
    subpatterns=["Grid DP with Obstacles"],
    tc="O(m·n)",
    sc="O(n)",
    key_insight="dp[r][c] = sum of paths from above + from left; obstacles zero out that cell and propagate.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ──
TABULATION_CODE = """\
def uniquePathsWithObstacles(obstacleGrid):
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1:
        return 0
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = 1
    for c in range(1, n):
        dp[0][c] = 0 if obstacleGrid[0][c] else dp[0][c-1]
    for r in range(1, m):
        dp[r][0] = 0 if obstacleGrid[r][0] else dp[r-1][0]
    for r in range(1, m):
        for c in range(1, n):
            if obstacleGrid[r][c] == 1:
                dp[r][c] = 0
            else:
                dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[m-1][n-1]"""

MEMO_CODE = """\
from functools import lru_cache

def uniquePathsWithObstacles(obstacleGrid):
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    @lru_cache(maxsize=None)
    def dp(r, c):
        if r < 0 or c < 0:          return 0
        if obstacleGrid[r][c] == 1: return 0
        if r == 0 and c == 0:       return 1
        return dp(r-1, c) + dp(r, c-1)
    return dp(m-1, n-1)"""

SPACE_OPT_CODE = """\
def uniquePathsWithObstacles(obstacleGrid):
    n = len(obstacleGrid[0])
    dp = [0] * n
    dp[0] = 1 if not obstacleGrid[0][0] else 0
    for row in obstacleGrid:
        for c in range(n):
            if row[c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c-1]
    return dp[-1]"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m x n", {"code": True}),
        (" integer array grid called ", {}),
        ("obstacleGrid", {"code": True}),
        (". A robot is initially located at the top-left corner (", {}),
        ("grid[0][0]", {"code": True}),
        ("). The robot tries to move to the bottom-right corner (", {}),
        ("grid[m-1][n-1]", {"code": True}),
        ("). The robot can only move either down or right at any point in time. An obstacle and space are marked as ", {}),
        ("1", {"code": True}),
        (" and ", {}),
        ("0", {"code": True}),
        (" respectively. Paths that include any obstacle are invalid. Return the number of possible unique paths that the robot can take to reach the bottom-right corner.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Tabulation ──
blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count distinct paths in a grid where movement is restricted to right or down only, and certain cells are blocked. 'Count distinct paths with restrictions' is a classic DP signal."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force DFS tries every path: O(2^(m+n)) — exponential and totally impractical for large grids. Greedy (always go right first) finds one path but misses all others."),
        N.h4("The Key Observation"),
        N.para("Because you can only arrive at (r,c) from (r-1,c) or (r,c-1), the count at any cell is exactly the sum of counts at its two possible predecessors. Obstacles simply force their cell's count to 0, and that 0 propagates forward through the summation automatically."),
        N.h4("Building the Solution"),
        N.para("Define dp[r][c] = paths from (0,0) to (r,c). Base case: dp[0][0] = 1. Fill first row (each cell = left neighbor) and first column (each cell = cell above). Fill interior row by row: dp[r][c] = dp[r-1][c] + dp[r][c-1] (or 0 if obstacle). Fill order ensures dependencies always come before the cell needing them."),
        N.callout("Analogy: Think of water flowing from a source at (0,0). At each cell, inflow = flow from above + flow from left. An obstacle is a dam — blocks all flow through that cell.", "🌊", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The total paths to (r,c) = paths to (r-1,c) + paths to (r,c-1). Every path to (r,c) passes through exactly one of those two cells as its final step — no double counting, no missing cases.")
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursion recomputes dp(2,2) from dp(1,2) and dp(2,1), each of which re-expands dp(0,2), dp(1,1), etc. — exponential redundancy. The table caches every cell, giving O(m·n) total work.")
    ])),
    N.code("# Recurrence\ndp[r][c] = 0                         if obstacleGrid[r][c] == 1\ndp[r][c] = dp[r-1][c] + dp[r][c-1]  otherwise\ndp[0][0] = 1                         (base case)", "python"),
    N.h3("Code"),
    N.code(TABULATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = ...", {"code": True}), (" — Extract grid dimensions.")])),
    N.para(N.rich([("if obstacleGrid[0][0] == 1", {"code": True}), (" — Guard clause: if the start is blocked, no paths exist at all.")])),
    N.para(N.rich([("dp = [[0]*n for _ in range(m)]", {"code": True}), (" — Initialize a 2D table of zeros, same shape as the grid.")])),
    N.para(N.rich([("dp[0][0] = 1", {"code": True}), (" — Base case: exactly 1 way to stand at the start.")])),
    N.para(N.rich([("for c in range(1, n): dp[0][c] = ...", {"code": True}), (" — Fill the top row. Can only come from the left. Obstacle → 0; otherwise inherit left neighbor's value.")])),
    N.para(N.rich([("for r in range(1, m): dp[r][0] = ...", {"code": True}), (" — Fill the left column. Can only come from above. Same cascade rule.")])),
    N.para(N.rich([("dp[r][c] = 0", {"code": True}), (" if obstacle — Obstacle zeroes out this cell; downstream cells will sum 0 from this direction.")])),
    N.para(N.rich([("dp[r][c] = dp[r-1][c] + dp[r][c-1]", {"code": True}), (" — Core recurrence: paths from above + paths from left.")])),
    N.para(N.rich([("return dp[m-1][n-1]", {"code": True}), (" — The bottom-right cell holds the final answer.")])),
    N.callout("⚠️ Zero propagation: once any cell in the first row/column is 0 (obstacle), all cells beyond it in that edge are also 0 — they inherit 0 through the chain automatically.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Ask: 'How many paths reach (m-1, n-1)?' Recursively: paths(r,c) = paths(r-1,c) + paths(r,c-1). This is a direct transcription of the recurrence into code."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion (no cache) recomputes paths(r,c) exponentially many times — the same subproblems appear over and over in the recursion tree."),
        N.h4("The Key Observation"),
        N.para("@lru_cache memoizes each (r,c) call. The first time we ask for paths(r,c), we compute it; every subsequent call retrieves the cached answer in O(1). Total unique calls: m*n."),
        N.h4("Building the Solution"),
        N.para("Base cases: out of bounds → 0, obstacle → 0, (0,0) → 1. Recursive case: return dp(r-1,c) + dp(r,c-1). Call dp(m-1, n-1) to start. The recursion naturally explores only needed subproblems."),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Python's built-in memoization decorator. Caches (r,c) → result automatically.")])),
    N.para(N.rich([("if r < 0 or c < 0: return 0", {"code": True}), (" — Boundary guard: stepping off the grid contributes 0 paths.")])),
    N.para(N.rich([("if obstacleGrid[r][c] == 1: return 0", {"code": True}), (" — Obstacle cell: no valid path passes through here.")])),
    N.para(N.rich([("if r == 0 and c == 0: return 1", {"code": True}), (" — Base case: we are at the start, 1 way.")])),
    N.para(N.rich([("return dp(r-1, c) + dp(r, c-1)", {"code": True}), (" — Sum paths from above (move up one row) and from left (move left one column).")])),
    N.divider(),
]

# ── Solution 3: Space Optimized ──
blocks += [
    N.h2("Solution 3 — Space-Optimized Tabulation (O(n) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We only ever look at the previous row and the current row. Can we eliminate the previous row from memory once we've moved past it?"),
        N.h4("The Key Observation"),
        N.para("Yes: maintain a single 1D array dp[]. Before we update dp[c] for row r, dp[c] still holds the value from row r-1 (that's 'from above'). dp[c-1] was just updated in this same row (that's 'from left'). So dp[c] += dp[c-1] achieves the same result as the 2D formula."),
        N.h4("Building the Solution"),
        N.para("Initialize dp = [0]*n with dp[0] = 1 (if no start obstacle). Then for each row: iterate c from 0 to n-1; if obstacle, set dp[c]=0; else dp[c] += dp[c-1]. After processing all rows, dp[-1] is the answer."),
    ]),
    N.h3("Code"),
    N.code(SPACE_OPT_CODE, "python"),
    N.callout("Key: dp[c] += dp[c-1] — before this line, dp[c] = value from row above (from above); dp[c-1] = value just set this row (from left). One in-place add handles both directions.", "💡", "green_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-force DFS", "O(2^(m+n))", "O(m+n)"],
        ["Memoization (top-down)", "O(m·n)", "O(m·n)"],
        ["Tabulation 2D (interview pick)", "O(m·n)", "O(m·n)"],
        ["Space-Optimized 1D", "O(m·n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Grid DP with Obstacles")])),
    N.callout(
        "When to recognize this pattern: grid navigation problem + moves restricted to a subset of directions (right/down only) + 'count distinct paths' or 'min/max path value' + optional obstacles or cell costs.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Grid DP technique:"),
    N.bullet(N.rich([("Unique Paths", {"bold": True}), (" (Medium) — Same grid DP without obstacles; purely combinatorial (#62)")])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium) — Minimize cost of a path; same recurrence shape, sum → min (#64)")])),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium) — 1D DP down a triangular structure; 'from above' dependency (#120)")])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), (" (Hard) — Fill DP backward from bottom-right to top-left; health constraint (#174)")])),
    N.bullet(N.rich([("Cherry Pickup", {"bold": True}), (" (Hard) — Two robots simultaneously on the same grid; 3D DP extension (#741)")])),
    N.bullet(N.rich([("Number of Paths with Max Score", {"bold": True}), (" (Hard) — Max score + count simultaneously in grid with obstacles (#1301)")])),
    N.para("These problems share the same core structure: dp[r][c] depends only on dp[r-1][c] and dp[r][c-1], filled row by row."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-pattern: Grid DP with Obstacles. Source: Guide Section 18 + Analysis.", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("unique_paths_ii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
