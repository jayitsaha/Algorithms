"""
gen_minimum_path_sum.py — Notion page for LeetCode #64 Minimum Path Sum
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Page already created in previous run ──
PAGE_ID = "39293418-809c-819a-aa2b-c75513d286f6"
print(f"Using existing page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=64,
    pattern="Dynamic Programming",
    subpatterns=["Min From Up or Left"],
    tc="O(m·n)",
    sc="O(1)",
    key_insight="dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]): minimum cost from above or left, no extra space needed.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe any existing body then rebuild ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"bold": True}),
        (" grid filled with non-negative numbers, find a path from the top-left corner to the bottom-right corner that minimizes the sum of all numbers along its path. You may only move ", {}),
        ("right", {"bold": True}),
        (" or ", {}),
        ("down", {"bold": True}),
        (" at each step.", {})
    ])),
    N.para(N.rich([
        ("Example: grid = [[1,3,1],[1,5,1],[4,2,1]] → Output: ", {}),
        ("7", {"bold": True}),
        (" (path: 1→3→1→1→1)", {"italic": True})
    ])),
    N.divider(),
]

# ── Solution 1: In-Place Bottom-Up Tabulation ──
SOL1_CODE = """def minPathSum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue                         # base case: starting cell
            elif i == 0:
                grid[i][j] += grid[i][j-1]      # first row: only from left
            elif j == 0:
                grid[i][j] += grid[i-1][j]      # first col: only from above
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])  # interior: min of two predecessors
    return grid[m-1][n-1]"""

blocks += [
    N.h2("Solution 1 — In-Place Bottom-Up Tabulation (Interview Pick ✓)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the minimum-cost path from the top-left to the bottom-right of a grid, moving only right or down. Rather than trying all paths, we ask: 'What is the cheapest way to reach each individual cell?' If we can answer that for every cell, the answer for the destination cell is our answer."),
        N.h4("What Doesn't Work"),
        N.para("Greedy — always move to the cheaper immediate neighbor — fails because a locally cheap step can lead into expensive territory later. For example, going down (cost 1) instead of right (cost 3) looks good, but may put you in front of a costly cell next. Brute force DFS tries all 2^(m+n-2) paths — exponential and far too slow."),
        N.h4("The Key Observation"),
        N.para("Every cell can be reached from exactly two predecessors: the cell directly above, or the cell directly to its left (boundary cells have only one). Therefore: the cheapest way to reach (i,j) = min(cheapest way to reach (i-1,j), cheapest way to reach (i,j-1)) + grid[i][j]. This is a clean recurrence with no cycles — the constraint 'only right or down' prevents any cell from being its own ancestor."),
        N.h4("Building the Solution"),
        N.para("1. Fill top-left first (base case, value stays as-is). 2. Fill first row left-to-right: only one predecessor each, so it's a running prefix sum. 3. Fill first column top-to-bottom: same, running prefix sum. 4. Fill all interior cells using min(from above, from left) + this cell's cost. 5. Answer is bottom-right cell."),
        N.callout("Analogy: Think of dp[i][j] as 'the cheapest toll road from the entrance to this junction.' Once computed for all junctions in order, the exit toll is your answer.", "🛣️", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The optimal path to (i,j) must pass through either (i-1,j) or (i,j-1). Whichever predecessor has the cheaper optimal path determines the last step. So dp[i][j] depends on optimal solutions to smaller subproblems — exactly what DP requires.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive DFS would recompute dp[1][1] many times — once for every path that visits it. There are exponentially many such paths. DP computes each cell exactly once and reuses the cached value.", {})
    ])),
    N.code("""# The Recurrence:
# dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
#
# Boundary cases:
# dp[0][0] = grid[0][0]                        (base)
# dp[0][j] = grid[0][j] + dp[0][j-1]          (first row: only from left)
# dp[i][0] = grid[i][0] + dp[i-1][0]          (first col: only from above)"""),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(grid), len(grid[0])", {"code": True}), (" — Extract the number of rows and columns.", {})])),
    N.para(N.rich([("for i in range(m): for j in range(n):", {"code": True}), (" — Process every cell in row-major order (left→right, top→bottom). This fill order guarantees both predecessors are computed before we need them.", {})])),
    N.para(N.rich([("if i == 0 and j == 0: continue", {"code": True}), (" — Top-left corner has no predecessors; its value is already correct. Skip.", {})])),
    N.para(N.rich([("elif i == 0: grid[i][j] += grid[i][j-1]", {"code": True}), (" — First row: the only way here is from the left. Accumulate a running prefix sum.", {})])),
    N.para(N.rich([("elif j == 0: grid[i][j] += grid[i-1][j]", {"code": True}), (" — First column: the only way here is from above. Accumulate a running prefix sum downward.", {})])),
    N.para(N.rich([("else: grid[i][j] += min(grid[i-1][j], grid[i][j-1])", {"code": True}), (" — Interior cell: the core recurrence. Take the cheaper of the two predecessors (both already hold their final dp values). Add this cell's own cost.", {})])),
    N.para(N.rich([("return grid[m-1][n-1]", {"code": True}), (" — After filling all cells, the bottom-right holds the minimum path sum.", {})])),
    N.callout("Note: This approach mutates the input grid. In interviews, ask 'may I modify the input?' If not, use a separate dp array (same logic, O(mn) space).", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Top-Down Memoization ──
SOL2_CODE = """from functools import lru_cache

def minPathSum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])

    @lru_cache(maxsize=None)
    def dp(i, j):
        # Returns: minimum cost path from (0,0) to (i,j)
        if i == 0 and j == 0:
            return grid[0][0]           # base case
        if i == 0:
            return grid[i][j] + dp(i, j-1)   # first row: only from left
        if j == 0:
            return grid[i][j] + dp(i-1, j)   # first col: only from above
        # Interior: min of two predecessors
        return grid[i][j] + min(dp(i-1, j), dp(i, j-1))

    return dp(m-1, n-1)   # ask: min cost to reach destination?"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recurrence dp(i,j) = grid[i][j] + min(dp(i-1,j), dp(i,j-1)) maps directly into a recursive function. Without caching, this would re-evaluate dp(1,1) for every path that visits it. With an LRU cache, each (i,j) pair is computed exactly once."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization: exponential time O(2^(m+n)) because the same subproblems are recomputed repeatedly along different paths."),
        N.h4("The Key Observation"),
        N.para("lru_cache stores dp(i,j) the first time it is computed. Subsequent calls with the same (i,j) return the cached answer immediately. The recursion tree has O(mn) unique nodes, each computed once — O(mn) total work."),
        N.h4("Building the Solution"),
        N.para("Define dp(i,j) recursively following the recurrence. Add @lru_cache. Ask for dp(m-1, n-1). Python resolves all dependencies bottom-up via the call stack."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoize all (i,j) pairs. First call computes; subsequent calls return cached result in O(1).", {})])),
    N.para(N.rich([("def dp(i, j):", {"code": True}), (" — Recursive function: returns the minimum cost to reach cell (i,j) from (0,0).", {})])),
    N.para(N.rich([("if i == 0 and j == 0: return grid[0][0]", {"code": True}), (" — Base case: starting cell, no predecessors.", {})])),
    N.para(N.rich([("if i == 0: return grid[i][j] + dp(i, j-1)", {"code": True}), (" — Top row: recurse left only.", {})])),
    N.para(N.rich([("if j == 0: return grid[i][j] + dp(i-1, j)", {"code": True}), (" — Left column: recurse up only.", {})])),
    N.para(N.rich([("return grid[i][j] + min(dp(i-1,j), dp(i,j-1))", {"code": True}), (" — Interior: take cheaper recursive subproblem result.", {})])),
    N.para(N.rich([("return dp(m-1, n-1)", {"code": True}), (" — Kick off the recursion by asking for the bottom-right corner.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DFS", "O(2^(m+n))", "O(m+n) stack"],
        ["Memoization (top-down)", "O(m·n)", "O(m·n) cache + O(m+n) stack"],
        ["Tabulation (separate dp)", "O(m·n)", "O(m·n)"],
        ["In-Place Tabulation (Interview Pick ✓)", "O(m·n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min From Up or Left (grid path DP)", {})])),
    N.para(N.rich([("State Definition: ", {"bold": True}), ("dp[i][j] = minimum path cost from (0,0) to (i,j)", {})])),
    N.callout(
        "When to recognize this pattern: Grid problem + move right/down only + minimize/maximize/count paths → 2D DP. "
        "The key signal is restricted movement (no cycles possible), giving each cell at most 2 predecessors. "
        "If move set includes left/up, you need Dijkstra instead.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (grid path DP):"),
    N.bullet(N.rich([("Unique Paths", {"bold": True}), (" (Medium, #62) — Count distinct paths right-or-down; dp[i][j] = dp[i-1][j] + dp[i][j-1] (addition instead of min)", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium, #63) — Same but with obstacles; set dp=0 for blocked cells", {})])),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium, #120) — 1D variable-width grid; min path sum from top, fill bottom-up", {})])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), (" (Medium, #221) — dp[i][j] = min(up, left, diagonal) + 1 for largest all-1 square", {})])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), (" (Hard, #174) — Same right/down grid but fill bottom-right → top-left (health constraint reverses dependency)", {})])),
    N.bullet(N.rich([("Cherry Pickup", {"bold": True}), (" (Hard, #741) — Two simultaneous agents on grid; 3D DP on (row, col1, col2)", {})])),
    N.para("These problems all share the same core: restricted movement on a 2D grid allows clean subproblem decomposition with only 1-2 predecessors per cell."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: Min From Up or Left. Source: Guide Section 18.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_path_sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Each step shows the DP table filling progressively with decision panels showing min(up, left) choices.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
