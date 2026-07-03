"""
Notion regeneration script for: Minimum Falling Path Sum (LeetCode #931)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
Pattern: Dynamic Programming — DP from Previous Row
"""
import sys

# ── patch token before importing notion_lib ──
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-8120-8965-fab494113861"

# ── 1. Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=931,
    pattern="Dynamic Programming",
    subpatterns=["DP from Previous Row"],
    tc="O(n^2)",
    sc="O(1) in-place",
    key_insight="Each cell's min cost = cell value + min of up-to-3 cells directly above; in-place tabulation needs O(1) extra space.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──
print("Wiping existing body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build the body ──
blocks = []

# ─── PROBLEM ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("n x n", {"code": True}),
        (" integer matrix ", {}),
        ("matrix", {"code": True}),
        (", return the minimum sum of any falling path through ", {}),
        ("matrix", {"code": True}),
        (". A falling path starts at any element in the first row and chooses one of the three elements directly below-left, directly below, or directly below-right in the next row. Formally, from ", {}),
        ("(r, c)", {"code": True}),
        (" you may move to ", {}),
        ("(r+1, c-1)", {"code": True}),
        (", ", {}),
        ("(r+1, c)", {"code": True}),
        (", or ", {}),
        ("(r+1, c+1)", {"code": True}),
        (". Boundary columns have at most 2 valid successors.", {}),
    ])),
    N.divider(),
]

# ─── SOLUTION 1 — BRUTE FORCE ───
blocks += [
    N.h2("Solution 1 — Brute Force: Recursive DFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The matrix is a weighted graph. You start at any cell in row 0 and walk down, choosing among 3 legal neighbours each time. You want the walk with the minimum total weight. The natural first instinct is to try every walk."),
        N.h4("What Doesn't Work"),
        N.para("Trying every path recursively is correct but exponential: at each of n rows you branch into up to 3 children, giving O(3^n) paths. For n=100 this is astronomical."),
        N.h4("The Key Observation"),
        N.para("Many sub-paths overlap. The minimum cost to reach (r, c) is computed identically regardless of which cell in row r-1 we came from. We recompute it for every path that passes through (r, c) — that is the inefficiency DP eliminates."),
        N.h4("Building the Solution"),
        N.para("Write dfs(r, c) that returns the min-cost path ending at (r, c): base case r=0 returns matrix[0][c]; recursive case returns matrix[r][c] + min over valid parents. Call min over all c in last row."),
        N.callout("Analogy: Navigating a waterfall, choosing at each rock which of 3 downstream rocks to land on. Naive = retrace every route from the top. Smart (DP) = remember the cheapest way to reach each rock.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def minFallingPathSum_brute(matrix):
    n = len(matrix)

    def dfs(r, c):
        if r == 0:
            return matrix[0][c]          # base case: first row
        best = float('inf')
        for dc in [-1, 0, 1]:           # three possible parent columns
            pc = c + dc
            if 0 <= pc < n:             # boundary check
                best = min(best, dfs(r - 1, pc))
        return matrix[r][c] + best      # accumulate

    return min(dfs(n - 1, c) for c in range(n))
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(matrix)", {"code": True}), (" — Grid is n x n; same value for rows and columns.", {})])),
    N.para(N.rich([("def dfs(r, c):", {"code": True}), (" — Inner recursive helper: what is the cheapest cost to end at cell (r, c)?", {})])),
    N.para(N.rich([("if r == 0: return matrix[0][c]", {"code": True}), (" — Base case: first row has no parents; total cost = the cell's own value.", {})])),
    N.para(N.rich([("for dc in [-1, 0, 1]:", {"code": True}), (" — Explore three diagonal offsets: upper-left, directly-above, upper-right.", {})])),
    N.para(N.rich([("if 0 <= pc < n:", {"code": True}), (" — Boundary guard: skip columns that fall outside the grid.", {})])),
    N.para(N.rich([("best = min(best, dfs(r - 1, pc))", {"code": True}), (" — Recurse to row above, tracking cheapest parent.", {})])),
    N.para(N.rich([("return matrix[r][c] + best", {"code": True}), (" — Add this cell's value to the min-cost path reaching it.", {})])),
    N.para(N.rich([("return min(dfs(n - 1, c) ...)", {"code": True}), (" — Run for all columns in last row; return the overall minimum.", {})])),
    N.divider(),
]

# ─── SOLUTION 2 — MEMOIZATION ───
blocks += [
    N.h2("Solution 2 — Top-Down DP: Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The brute-force DFS is correct but recomputes the same (r, c) subproblems many times. Once you know the cheapest cost to reach (r, c), cache it — never recompute it."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes dfs(r, c) once per path that passes through it. The number of such paths grows exponentially with n."),
        N.h4("The Key Observation"),
        N.para("The minimum cost to reach (r, c) depends ONLY on r and c, not on the specific path used to get there. Memoize on (r, c) for O(n^2) total calls with O(1) work each."),
        N.h4("Building the Solution"),
        N.para("Add @lru_cache to the recursive helper. Everything else is identical. Time drops from O(3^n) to O(n^2). Space is O(n^2) for the cache plus O(n) for the call stack."),
        N.callout("Memoization = recursion + memory. Top-down: start with the question you want answered, recurse toward base cases, cache results on the way back up.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""from functools import lru_cache

def minFallingPathSum_memo(matrix):
    n = len(matrix)

    @lru_cache(maxsize=None)
    def dp(r, c):
        if r == 0:
            return matrix[0][c]
        best = float('inf')
        for dc in [-1, 0, 1]:
            pc = c + dc
            if 0 <= pc < n:
                best = min(best, dp(r - 1, pc))  # cache hit on repeat visits
        return matrix[r][c] + best

    return min(dp(n - 1, c) for c in range(n))
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Python's built-in memoization decorator. Automatically caches results for every unique (r, c) argument pair.", {})])),
    N.para(N.rich([("def dp(r, c):", {"code": True}), (" — Same shape as brute-force; the cache makes it O(n^2) total.", {})])),
    N.para(N.rich([("best = min(best, dp(r - 1, pc))", {"code": True}), (" — On second+ visits to the same (r-1, pc), lru_cache returns immediately from the cache in O(1).", {})])),
    N.para(N.rich([("return min(dp(n-1, c) ...)", {"code": True}), (" — All n subproblems in the last row are already cached; this is now O(n).", {})])),
    N.divider(),
]

# ─── SOLUTION 3 — TABULATION IN-PLACE (OPTIMAL) ───
blocks += [
    N.h2("Solution 3 — Bottom-Up DP: Tabulation In-Place (Interview Pick) ✓"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'cheapest cost to reach (r,c)?' recursively from the bottom, flip the view: build a cost table row-by-row from the top. After processing row r, matrix[r][c] holds the minimum total cost of any falling path ending at (r, c)."),
        N.h4("What Doesn't Work (vs memoization)"),
        N.para("Memoization allocates O(n^2) cache storage and has function-call overhead. Tabulation updates the matrix in-place, needing O(1) extra space."),
        N.h4("The Key Observation"),
        N.para("Since we process rows strictly top-to-bottom, row r-1 always has its final values when we compute row r. We can safely overwrite matrix[r][c] in-place."),
        N.h4("Building the Solution"),
        N.para("Skip row 0 (base case). For rows 1..n-1, for each column c: gather up to 3 values from row r-1 (guarding boundaries), take the min, add to matrix[r][c], store back. Return min of last row."),
        N.callout("Think of it as a scoreboard that ratchets forward: each row accumulates the cheapest cost to reach it, so the last row directly shows the minimum cost to any exit cell.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The cheapest path to (r, c) consists of the cheapest path to one of its valid parents plus matrix[r][c]. The global optimum decomposes into locally optimal sub-decisions.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Cell (r, c) is a valid parent for up to 3 cells in row r+1. Without caching, its minimum cost would be recomputed by each of those children and their descendants.", {}),
    ])),
    N.h3("The Recurrence"),
    N.code(
"""# Recurrence (applied in-place):
# dp[r][c] = matrix[r][c] + min(
#     dp[r-1][c-1],   # upper-left  (only if c > 0)
#     dp[r-1][c],     # directly above
#     dp[r-1][c+1]    # upper-right (only if c < n-1)
# )
#
# Base case:  dp[0][c] = matrix[0][c]   (first row unchanged)
# Answer:     min(dp[n-1][c] for all c)
""", "python"),
    N.h3("Code"),
    N.code(
"""def minFallingPathSum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    for r in range(1, n):                        # skip row 0 (base case)
        for c in range(n):
            best = matrix[r - 1][c]             # directly above always valid
            if c > 0:
                best = min(best, matrix[r - 1][c - 1])   # upper-left
            if c < n - 1:
                best = min(best, matrix[r - 1][c + 1])   # upper-right

            matrix[r][c] += best                # accumulate in-place

    return min(matrix[-1])                      # minimum over last row
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(matrix)", {"code": True}), (" — Square grid: n rows, n columns. We iterate n-1 update passes.", {})])),
    N.para(N.rich([("for r in range(1, n):", {"code": True}), (" — Start at row 1. Row 0 needs no update: it is the base case where dp[0][c] = matrix[0][c] already.", {})])),
    N.para(N.rich([("for c in range(n):", {"code": True}), (" — Visit every column in the current row left-to-right.", {})])),
    N.para(N.rich([("best = matrix[r - 1][c]", {"code": True}), (" — Directly-above parent. Always in bounds (c is valid, r-1 >= 0). Initialize 'best' to this value.", {})])),
    N.para(N.rich([("if c > 0: best = min(best, matrix[r-1][c-1])", {"code": True}), (" — Upper-left parent. Guard: only exists when c > 0 (not the leftmost column).", {})])),
    N.para(N.rich([("if c < n-1: best = min(best, matrix[r-1][c+1])", {"code": True}), (" — Upper-right parent. Guard: only exists when c < n-1 (not the rightmost column).", {})])),
    N.para(N.rich([("matrix[r][c] += best", {"code": True}), (" — In-place update. This cell now stores the min total cost of any path ending at (r, c). No extra array needed.", {})])),
    N.para(N.rich([("return min(matrix[-1])", {"code": True}), (" — After all rows, the last row contains min path costs to each ending column. The answer is the smallest of these.", {})])),
    N.callout("Warning: This modifies the input matrix. If the caller needs the original preserved, clone first: import copy; matrix = copy.deepcopy(matrix).", "⚠️", "yellow_background"),
    N.callout("Space O(1): the DP table IS the matrix — no extra array allocated. The iteration uses O(1) loop variables.", "💡", "green_background"),
    N.divider(),
]

# ─── COMPLEXITY TABLE ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (DFS)", "O(3^n)", "O(n)", "Exponential — never use in practice"],
        ["Memoization (Top-Down DP)", "O(n^2)", "O(n^2)", "Cache all n^2 states; recursive call stack O(n)"],
        ["Tabulation In-Place (Interview Pick)", "O(n^2)", "O(1)", "Optimal — overwrites matrix in-place"],
    ]),
    N.divider(),
]

# ─── PATTERN CLASSIFICATION ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP from Previous Row", {})])),
    N.callout(
        "When to recognize this pattern: the problem asks for min/max cost of a path through a grid processed row-by-row; each cell's optimal value depends only on adjacent cells in the row directly above; no skipping rows or non-local dependencies. Signal phrases: 'falling path', 'triangle path', 'adjacent columns', 'grid path sum'.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("State: ", {"bold": True}),
        ("dp[r][c] = minimum total falling-path sum ending at cell (r, c). ", {}),
        ("Recurrence: ", {"bold": True}),
        ("dp[r][c] = matrix[r][c] + min(dp[r-1][c-1], dp[r-1][c], dp[r-1][c+1]) (skipping out-of-bounds). ", {}),
        ("Base case: ", {"bold": True}),
        ("dp[0][c] = matrix[0][c].", {}),
    ])),
    N.divider(),
]

# ─── RELATED PROBLEMS ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DP from Previous Row / Grid DP):"),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium, #120) — Falling path in a triangle; same row-to-row DP but only 2 children (adjacent+1 columns).", {})])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium, #64) — Grid DP from top-left to bottom-right; each cell depends on left and above.", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum II", {"bold": True}), (" (Hard, #1289) — Same problem but next row can skip ANY column except the direct one; track top-2 row minimums.", {})])),
    N.bullet(N.rich([("Paint House", {"bold": True}), (" (Medium, #256) — Row-by-row DP where the state is which color was chosen; must differ from the previous row.", {})])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), (" (Hard, #174) — Bottom-up row DP from destination to source for minimum health path.", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium, #63) — Count paths in grid with obstacles; row-by-row DP counting valid routes.", {})])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), (" (Medium, #221) — DP[r][c] depends on 3 neighbours: above, left, and upper-left diagonal.", {})])),
    N.para("These problems share the same structure: a DP table built row-by-row where each cell's optimal value depends on a bounded window of cells in the previous row."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: DP from Previous Row. Source: Guide Section 18 + Analysis.", "📚", "gray_background"),
    N.divider(),
]

# ─── EMBED ───
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed("https://jayitsaha.github.io/Algorithms/minimum_falling_path_sum_explainer.html"),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ──
print(f"Appending {len(blocks)} blocks in chunks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
