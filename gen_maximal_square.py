"""
gen_maximal_square.py — Notion update for LeetCode #221 Maximal Square
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f9-b6ff-d341f3b652b6"

# ── 1) Set page properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=221,
    pattern="Dynamic Programming",
    subpatterns=["Min of Three Neighbors Plus One"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="dp[i][j] = min(top, left, diagonal) + 1 — the three neighbors cap the largest square at this bottom-right corner.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"bold": True}),
        (" binary matrix filled with ", {}),
        ("'0'", {"code": True}),
        ("s and ", {}),
        ("'1'", {"code": True}),
        ("s, find the largest square containing only ", {}),
        ("'1'", {"code": True}),
        ("s and return its ", {}),
        ("area", {"bold": True}),
        (".", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ('matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]', {"code": True}),
            (" → Output: ", {}),
            ("4", {"bold": True}),
            (" (a 2×2 square at rows 1–2, cols 2–3)", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — Tabulation (Interview Pick) ──
sol1_code = """\
def maximalSquare(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [[0]*n for _ in range(m)]   # dp[i][j] = side of largest square at (i,j)
    max_side = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '0':
                dp[i][j] = 0
            elif i == 0 or j == 0:       # base: edge rows/cols
                dp[i][j] = 1
            else:                        # interior '1' cell
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
            max_side = max(max_side, dp[i][j])
    return max_side * max_side           # area, not side!"""

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every '1' cell, ask: 'What is the largest all-ones square that fits with this cell as its bottom-right corner?' Define dp[i][j] = that side length. The answer is max(dp) squared."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each cell, try expanding a square and check all cells inside. This is O(m·n·min(m,n)²) — on a 300×300 grid, that's billions of checks. We re-examine the same interior cells over and over — classic overlapping subproblems signal."),
        N.h4("The Key Observation"),
        N.para("For a (k+1)×(k+1) square to fit at (i,j), three sub-squares of side ≥ k must exist: one ending at (i-1,j) (top), one at (i,j-1) (left), and one at (i-1,j-1) (diagonal). All three must support side k. The minimum of the three is the bottleneck. Therefore dp[i][j] = min(top, left, diagonal) + 1."),
        N.h4("Building the Solution"),
        N.para("1. Create dp table same size as input, all zeros. 2. Base cases: first row and column can only be 1×1 squares. 3. For interior cells with value '1', apply the min-of-three recurrence. 4. Track max_side throughout. 5. Return max_side²."),
        N.callout("Analogy: Think of each cell as asking its three neighbors — 'How big was the square you supported?' The smallest answer determines how much we can extend.", "🧠", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The largest square at (i,j) depends only on dp values at three adjacent cells — nothing further away is needed. "),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive check of 'are all cells in this candidate square 1?' would re-examine interior cells O(k²) times per corner. DP computes each cell once in O(1)."),
    ])),
    N.code(
        "# Recurrence:\n"
        "# If matrix[i][j] == '0':         dp[i][j] = 0\n"
        "# If i == 0 or j == 0 (edge):     dp[i][j] = 1   (if value is '1')\n"
        "# Else:                            dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1\n"
        "#\n"
        "# Why 'min of three'?\n"
        "# dp[i-1][j]   = largest square above       (vertical coverage)\n"
        "# dp[i][j-1]   = largest square to the left (horizontal coverage)\n"
        "# dp[i-1][j-1] = largest square diagonally  (the 'corner glue')\n"
        "# All three must be >= k for a (k+1)x(k+1) square to fit.",
        "python"
    ),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(matrix), len(matrix[0])", {"code": True}), (" — Get grid dimensions.", {})])),
    N.para(N.rich([("dp = [[0]*n for _ in range(m)]", {"code": True}), (" — Create DP table same shape as matrix, all zeros. dp[i][j] will store side lengths.", {})])),
    N.para(N.rich([("max_side = 0", {"code": True}), (" — Running maximum side length seen. We track side, not area, to simplify the update.", {})])),
    N.para(N.rich([("if matrix[i][j] == '0':", {"code": True}), (" — A zero cell: no square can end here. dp stays 0.", {})])),
    N.para(N.rich([("elif i == 0 or j == 0:", {"code": True}), (" — First row or first column: no room above or left, so maximum is 1×1. dp[i][j] = 1 only if the cell is '1' (which it must be since we failed the '0' check).", {})])),
    N.para(N.rich([("dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1", {"code": True}), (" — The heart of the algorithm. Three neighbors: top (vertical coverage), left (horizontal coverage), diagonal (the corner glue). Min is the bottleneck; +1 extends by this cell.", {})])),
    N.para(N.rich([("max_side = max(max_side, dp[i][j])", {"code": True}), (" — Update global maximum after each cell.", {})])),
    N.para(N.rich([("return max_side * max_side", {"code": True}), (" — Return AREA not side. This is the most common return-value bug — double check!", {})])),
    N.callout("⚠️ Most common bug: returning max_side instead of max_side * max_side. The problem asks for area!", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2 — Memoization ──
sol2_code = """\
def maximalSquare(matrix):
    m, n = len(matrix), len(matrix[0])
    memo = {}

    def dp(i, j):
        if i < 0 or j < 0: return 0          # out of bounds
        if matrix[i][j] == '0': return 0      # zero cell
        if (i, j) in memo: return memo[(i,j)] # cache hit
        result = min(dp(i-1,j), dp(i,j-1), dp(i-1,j-1)) + 1
        memo[(i, j)] = result
        return result

    ans = max(dp(i, j) for i in range(m) for j in range(n))
    return ans * ans"""

blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same recurrence as tabulation, but formulated as a recursive function: dp(i, j) returns the largest square with (i,j) as bottom-right. Recurse to the three neighbors, take the min, add 1."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization would recompute dp(i,j) from scratch every time it is referenced as a neighbor — exponential work. Memoization collapses this to O(m·n) total calls."),
        N.h4("The Key Observation"),
        N.para("The recursive structure directly mirrors the recurrence relation, making it easy to implement once you have the relation. Out-of-bounds cells return 0 (no square possible), zero cells return 0, everything else recurses."),
        N.h4("Building the Solution"),
        N.para("Base cases: i<0 or j<0 → 0 (boundary), matrix[i][j]=='0' → 0 (zero). Otherwise: min of three recursive calls + 1. Cache before returning. Call for all cells and take the max."),
        N.callout("Memoization is the natural translation of the recurrence into code. If the recurrence is clear, memoization follows directly. Tabulation requires flipping the perspective to iterative.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), (" — Dictionary cache: (i,j) → side length. Prevents re-computation.", {})])),
    N.para(N.rich([("if i < 0 or j < 0: return 0", {"code": True}), (" — Out-of-bounds base case. Simplifies the logic by allowing calls beyond grid edges.", {})])),
    N.para(N.rich([("if matrix[i][j] == '0': return 0", {"code": True}), (" — Zero cell: no square can end here.", {})])),
    N.para(N.rich([("if (i, j) in memo: return memo[(i,j)]", {"code": True}), (" — Cache hit: we already computed this cell's answer. Return immediately.", {})])),
    N.para(N.rich([("result = min(dp(i-1,j), dp(i,j-1), dp(i-1,j-1)) + 1", {"code": True}), (" — Same min-of-three recurrence, now expressed as recursive calls.", {})])),
    N.para(N.rich([("memo[(i, j)] = result", {"code": True}), (" — Cache before returning so future calls to this cell are O(1).", {})])),
    N.divider(),
]

# ── Solution 3 — Space-Optimized ──
sol3_code = """\
def maximalSquare(matrix):
    n = len(matrix[0])
    prev = [0] * n      # represents the previous row
    max_side = 0
    for row in matrix:
        curr = [0] * n
        diag = 0         # saves prev[j-1] before it's overwritten
        for j, val in enumerate(row):
            tmp = prev[j]   # save before potential overwrite
            if val == '1' and j > 0:
                curr[j] = min(prev[j], curr[j-1], diag) + 1
            elif val == '1':
                curr[j] = 1  # first column
            diag = tmp       # shift diagonal right
            max_side = max(max_side, curr[j])
        prev = curr
    return max_side * max_side"""

blocks += [
    N.h2("Solution 3 — Space-Optimized Rolling Row (O(n) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("When computing row i, we only ever look at row i-1 (via dp[i-1][j] and dp[i-1][j-1]) and the current row (dp[i][j-1]). We never look further back. So we can discard all rows before the previous one."),
        N.h4("The Key Challenge — Tracking the Diagonal"),
        N.para("The tricky part is dp[i-1][j-1]: as we process column j in the current row, prev[j-1] already contains the current row's value for column j-1 (since we process left-to-right). We must save the old prev[j-1] BEFORE it gets overwritten. That saved value is 'diag'."),
        N.callout("The diagonal tracking with 'diag = tmp' is the one subtle trick. Everything else is identical to the 2D solution.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol3_code, "python"),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(m·n·k²)", "O(1)", "k = min(m,n); TLE on large inputs"],
        ["Tabulation (Interview Pick)", "O(m·n)", "O(m·n)", "Clearest, easiest to explain"],
        ["Memoization", "O(m·n)", "O(m·n) + stack", "Top-down; natural from recurrence"],
        ["Rolling Row", "O(m·n)", "O(n)", "Space-optimal; diagonal tracking needed"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min of Three Neighbors Plus One (2D Grid DP)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Binary grid + 'largest square/rectangle' where ALL cells must satisfy a condition\n"
        "• Region size at (i,j) depends simultaneously on (i-1,j), (i,j-1), and (i-1,j-1)\n"
        "• Three neighbors matter (top + left + diagonal) → square shape; two → other shapes\n"
        "• 'Count all squares' variant → sum dp values instead of taking max",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 2D DP / Grid DP technique:"),
    N.bullet(N.rich([("Count Square Submatrices with All Ones", {"bold": True}), (" (Medium) — Same dp table, return sum instead of max. Each dp[i][j]=k contributes k new squares. (#1277)", {})])),
    N.bullet(N.rich([("Maximal Rectangle", {"bold": True}), (" (Hard) — Extend each row as histogram heights, apply monotonic stack per row. Harder extension of this problem. (#85)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Foundation for Maximal Rectangle; monotonic stack pattern. (#84)", {})])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium) — 2D DP grid; dp[i][j] = min(top, left) + cost. Same row-major traversal structure. (#64)", {})])),
    N.bullet(N.rich([("Unique Paths", {"bold": True}), (" (Medium) — 2D DP; dp[i][j] = dp[i-1][j] + dp[i][j-1]. Same dependency pattern. (#62)", {})])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), (" (Hard) — 2D DP traversed bottom-right to top-left; shows that traversal direction matters in 2D DP. (#174)", {})])),
    N.para("These problems share the core technique: define a meaningful quantity at each cell, fill row by row (or column by column), use previously computed neighbors."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) · Sub-Pattern: Min of Three Neighbors Plus One", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximal_square")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys to watch the DP table fill cell by cell.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
