"""
gen_unique_paths.py — Notion page builder for Unique Paths (LC #62).
Run: python3 gen_unique_paths.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c0-84ec-ce7a9b65b13c"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=62,
    pattern="Dynamic Programming",
    subpatterns=["Sum from Top and Left"],
    tc="O(m·n)",
    sc="O(n)",
    key_insight="Each cell can only be reached from above or left; dp[i][j] = dp[i-1][j] + dp[i][j-1]; compress to 1D with dp[j] += dp[j-1].",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
print("Wiping old body...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
print("Building body...")
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is a robot on an ", {}),
        ("m × n", {"code": True}),
        (" grid. The robot is initially located at the ", {}),
        ("top-left corner", {"bold": True}),
        (" (i.e., ", {}),
        ("grid[0][0]", {"code": True}),
        ("). The robot tries to move to the ", {}),
        ("bottom-right corner", {"bold": True}),
        (" (i.e., ", {}),
        ("grid[m-1][n-1]", {"code": True}),
        ("). The robot can only move either ", {}),
        ("down", {"bold": True}),
        (" or ", {}),
        ("right", {"bold": True}),
        (" at any point in time. Given the two integers ", {}),
        ("m", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (", return the number of possible unique paths that the robot can take to reach the bottom-right corner. The test cases are generated so that the answer will be less than or equal to 2 × 10^9.", {}),
    ])),
    N.callout(
        N.rich([("Example: m=3, n=7 → 28. Example: m=3, n=2 → 3.", {})]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — 1D DP (Interview Pick) ────────────────────────────────────
blocks += [
    N.h2("Solution 1 — 1D DP, Space-Optimized (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count paths, not find the shortest one. With only two moves allowed (right, down), every path to cell (r,c) must pass through either (r-1,c) or (r,c-1). So the number of paths to (r,c) equals the sum of paths to those two cells. This is a textbook recurrence."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force DFS explores every path: O(2^(m+n)) time. For m=20, n=20 this is ~10^12 operations. A recursive solution without memoization recomputes the same cells hundreds of times — dp(2,2) is reached via dp(1,2) AND dp(2,1), both of which compute it independently."),
        N.h4("The Key Observation"),
        N.para("Because the robot can only move right or down, each cell (r,c) can only be entered from exactly two cells: (r-1,c) and (r,c-1). These two entry points are always disjoint (different last-move direction), so their path counts add without double-counting. This gives the recurrence: dp[r][c] = dp[r-1][c] + dp[r][c-1]."),
        N.h4("Building the Solution"),
        N.para("Base case: row 0 and column 0 are all 1 (only one forced path — straight right or straight down). Then fill left-to-right, top-to-bottom. For space optimization: we only ever read from the row above (dp[r-1][c]) and the current row's left neighbor (dp[r][c-1]). A 1D array updated in-place captures both: before update, dp[c] = old row value = 'from above'; dp[c-1] = just updated = 'from left'."),
        N.callout("Analogy: Think of it like Pascal's Triangle. Each interior entry is the sum of the entry above and the entry to its left. The DP table for Unique Paths IS a generalized Pascal's Triangle.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def uniquePaths(m: int, n: int) -> int:\n"
        "    dp = [1] * n         # Row 0: all 1s (base case)\n"
        "    for r in range(1, m):  # Process each row after the first\n"
        "        for c in range(1, n):  # Col 0 stays 1 always; start at col 1\n"
        "            dp[c] += dp[c - 1]  # dp[c] (from above) += dp[c-1] (from left)\n"
        "    return dp[n - 1]     # Bottom-right cell = answer"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [1] * n", {"code": True}), (" — Create a 1D array of length n, all initialized to 1. This represents the top row of the DP table: from (0,0), there is exactly one path (go right) to every cell in the first row.", {})])),
    N.para(N.rich([("for r in range(1, m):", {"code": True}), (" — Outer loop over rows 1 through m-1. Row 0 is already handled by initialization.", {})])),
    N.para(N.rich([("for c in range(1, n):", {"code": True}), (" — Inner loop over columns 1 through n-1. Column 0 is never touched (stays 1, representing the single path straight down).", {})])),
    N.para(N.rich([("dp[c] += dp[c - 1]", {"code": True}), (" — The core recurrence. ", {}), ("dp[c]", {"code": True}), (" before this line holds the previous row's value (paths from above). ", {}), ("dp[c-1]", {"code": True}), (" was already updated this row iteration (paths from left). Adding them in-place is safe because we go left-to-right.", {})])),
    N.para(N.rich([("return dp[n - 1]", {"code": True}), (" — After all rows, the last element holds the count of paths to the bottom-right corner.", {})])),
    N.divider(),
]

# ── Solution 2 — Full 2D DP ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Full 2D DP Tabulation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same recurrence as Solution 1, but store the entire m×n table explicitly. This makes the dependency clear: dp[r][c] reads from dp[r-1][c] (directly above) and dp[r][c-1] (directly left)."),
        N.h4("What Doesn't Work"),
        N.para("The 2D table uses O(m·n) space. For m=n=100 this is 10,000 integers — fine in practice, but unnecessary once we recognize only the previous row is ever needed."),
        N.h4("The Key Observation"),
        N.para("Initialize every cell to 1 with [[1]*n for _ in range(m)]. This simultaneously handles the base cases for row 0 (top row) and column 0 (left column) without any special-casing in the loops."),
        N.h4("Building the Solution"),
        N.para("Fill the table row by row, column by column, starting at (1,1). Each interior cell reads from the already-computed cells directly above and to the left. Answer is at dp[m-1][n-1]."),
    ]),
    N.h3("Code"),
    N.code(
        "def uniquePaths_2D(m: int, n: int) -> int:\n"
        "    dp = [[1] * n for _ in range(m)]  # Init all to 1 (handles base cases)\n"
        "    for r in range(1, m):  # Skip row 0 (all already 1)\n"
        "        for c in range(1, n):  # Skip col 0 (all already 1)\n"
        "            dp[r][c] = dp[r-1][c] + dp[r][c-1]  # Classic recurrence\n"
        "    return dp[m-1][n-1]  # Answer at bottom-right"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [[1]*n for _ in range(m)]", {"code": True}), (" — Build an m×n 2D table, every cell initialized to 1. Row 0 and column 0 are already correct base cases.", {})])),
    N.para(N.rich([("for r in range(1, m)", {"code": True}), (" + ", {}), ("for c in range(1, n):", {"code": True}), (" — Skip row 0 and col 0 (base cases, never overwritten). Process all interior cells.", {})])),
    N.para(N.rich([("dp[r][c] = dp[r-1][c] + dp[r][c-1]", {"code": True}), (" — 2D recurrence in its explicit form. ", {}), ("dp[r-1][c]", {"code": True}), (" = paths from above (previous row, same column). ", {}), ("dp[r][c-1]", {"code": True}), (" = paths from left (same row, previous column — already updated).", {})])),
    N.para(N.rich([("return dp[m-1][n-1]", {"code": True}), (" — The bottom-right cell holds the total path count.", {})])),
    N.divider(),
]

# ── Solution 3 — Top-Down Memoization ─────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start from the destination and ask: how many ways could I have arrived here? This is the top-down perspective. Define a recursive function dp(r, c) = number of paths from (0,0) to (r,c), and cache results to avoid recomputation."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion (without caching) re-explores every subpath. dp(2,2) will be called from dp(3,2) and dp(2,3) independently, and each of those trees is identical. This creates exponential blowup."),
        N.h4("The Key Observation"),
        N.para("There are only m×n distinct (r,c) pairs. Once we compute dp(r,c) and cache it, every subsequent call for the same (r,c) is O(1). @lru_cache(None) handles this automatically in Python."),
        N.h4("Building the Solution"),
        N.para("Base case: if r==0 or c==0, return 1. Recursive case: return dp(r-1,c) + dp(r,c-1). The cache ensures O(m·n) total work. Space is O(m·n) for the cache plus O(m+n) for the recursion stack."),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def uniquePaths_memo(m: int, n: int) -> int:\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(r, c):\n"
        "        if r == 0 or c == 0: return 1  # Base: first row/col always 1 path\n"
        "        return dp(r-1, c) + dp(r, c-1)  # From above + from left\n"
        "    return dp(m-1, n-1)  # Query the target cell"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Tells Python to cache every call to ", {}), ("dp(r, c)", {"code": True}), (". The first time dp(1,1) is called, it computes and stores 2. Every later call for dp(1,1) returns 2 instantly.", {})])),
    N.para(N.rich([("if r == 0 or c == 0: return 1", {"code": True}), (" — Base case: any cell in the first row (r=0) or first column (c=0) has exactly one path — the straight line.", {})])),
    N.para(N.rich([("return dp(r-1, c) + dp(r, c-1)", {"code": True}), (" — Recurse into two subproblems: paths via cell above, plus paths via cell to the left. Both are cached after first call.", {})])),
    N.para(N.rich([("return dp(m-1, n-1)", {"code": True}), (" — Kick off the recursion from the target. Python's recursion limit is ~1000; for m,n ≤ 100, the max depth is ~200, which is fine.", {})])),
    N.divider(),
]

# ── Solution 4 — Combinatorics ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 4 — Mathematical Combinatorics (O(1) Space Bonus)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every valid path consists of exactly (m-1) down moves and (n-1) right moves — a total of (m+n-2) moves. A path is uniquely determined by choosing which of those moves are 'down' (the rest are 'right'). So we're choosing (m-1) positions from (m+n-2) total positions."),
        N.h4("The Key Observation"),
        N.para("This is directly the binomial coefficient C(m+n-2, m-1). In Python, math.comb computes this exactly in O(min(m,n)) time with O(1) space. It's the most elegant solution, but harder to generalize to variants like obstacles."),
        N.h4("Building the Solution"),
        N.para("Return comb(m + n - 2, m - 1). Verify: m=3, n=7 → comb(8, 2) = 28. m=3, n=2 → comb(3, 2) = 3. Both match expected outputs."),
    ]),
    N.h3("Code"),
    N.code(
        "from math import comb\n"
        "\n"
        "def uniquePaths_math(m: int, n: int) -> int:\n"
        "    # Total moves: (m-1) down + (n-1) right = (m+n-2) moves\n"
        "    # Choose which (m-1) moves are 'down' → C(m+n-2, m-1)\n"
        "    return comb(m + n - 2, m - 1)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("return comb(m + n - 2, m - 1)", {"code": True}), (" — Computes C(m+n-2, m-1): the number of ways to choose which (m-1) of (m+n-2) total moves are downward. Python's built-in handles large numbers exactly with no overflow.", {})])),
    N.callout(
        N.rich([("Why mention this in an interview? ", {"bold": True}), ("It shows mathematical maturity. Present the DP solution first (more generalizable), then mention the combinatorial shortcut as a 'bonus observation'. Never lead with it unless asked for the optimal solution by all metrics.", {})])
        , "💡", "green_background"
    ),
    N.divider(),
]

# ── Why is This DP? ────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("This problem satisfies BOTH pillars of dynamic programming:", {"bold": True}),
    ])),
    N.para(N.rich([
        ("1. Optimal Substructure: ", {"bold": True}),
        ("The count of paths to (r, c) depends only on two smaller subproblems: paths to (r-1, c) and paths to (r, c-1). If those counts are correct, the sum is correct. No other cells are needed.", {}),
    ])),
    N.para(N.rich([
        ("2. Overlapping Subproblems: ", {"bold": True}),
        ("In naive recursion, dp(1,1) is called from dp(2,1) → dp(1,1) AND from dp(1,2) → dp(1,1). For a 5×5 grid there are thousands of duplicate calls. Memoization or tabulation reduces total work to O(m·n) unique subproblems.", {}),
    ])),
    N.callout(
        N.rich([
            ("The Recurrence: ", {"bold": True}),
            ("dp[r][c] = dp[r-1][c] + dp[r][c-1]\n", {"code": True}),
            ("Base: dp[0][c] = 1 for all c; dp[r][0] = 1 for all r\n", {"code": True}),
            ("1D form: dp[c] += dp[c-1] (left-to-right, for each row after row 0)", {"code": True}),
        ]),
        "📐", "blue_background"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursion", "O(2^(m+n))", "O(m+n) stack"],
        ["Memoization (Top-Down)", "O(m·n)", "O(m·n) + O(m+n) stack"],
        ["2D DP Tabulation", "O(m·n)", "O(m·n)"],
        ["1D DP (Interview Pick) ✓", "O(m·n)", "O(n)"],
        ["Combinatorics", "O(min(m,n))", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Sum from Top and Left (2D Grid DP)", {})])),
    N.para(N.rich([("Technique: ", {"bold": True}), ("dp[i][j] = dp[i-1][j] + dp[i][j-1]; compress to 1D rolling array", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Grid-based counting/optimization problem · Robot can only move right/down (monotone moves) · Each cell depends on its immediate top and left neighbors · 'Count all paths' or 'minimum cost path' in a 2D grid", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sum from Top and Left DP pattern:"),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium, LC #63) — Same grid DP; set dp[r][c]=0 for obstacle cells. Obstacle blocks all paths through it.", {})])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium, LC #64) — Replace count with minimum cost: dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c].", {})])),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium, LC #120) — Triangular grid DP; dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) + triangle[i][j].", {})])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), (" (Medium, LC #221) — dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1 for '1' cells.", {})])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), (" (Hard, LC #174) — Same grid structure but fill backwards (bottom-right to top-left) to track minimum health.", {})])),
    N.bullet(N.rich([("Pascal's Triangle", {"bold": True}), (" (Easy, LC #118) — Structural analogue: triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j]. Unique Paths values appear as diagonals of Pascal's Triangle.", {})])),
    N.bullet(N.rich([("Count Square Submatrices with All Ones", {"bold": True}), (" (Medium, LC #1277) — Neighbor-sum DP variant; same 2D grid tabulation approach.", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum", {"bold": True}), (" (Medium, LC #931) — Rows depend on previous row's 3 neighbors (above-left, above, above-right).", {})])),
    N.para("These problems all share the core technique: fill a grid table row-by-row where each cell's value depends on immediate neighbors in previous rows/columns."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) · Sub-Pattern: Sum from Top and Left", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("unique_paths")),
    N.para(N.rich([("Step through the DP table filling cell-by-cell — use Next/Prev or arrow keys. Each step shows the decision panel with both neighbors and their contributions.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
