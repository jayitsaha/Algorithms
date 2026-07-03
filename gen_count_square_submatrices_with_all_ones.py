"""
gen_count_square_submatrices_with_all_ones.py
Regenerate Notion page IN-PLACE for LC#1277 Count Square Submatrices with All Ones.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812d-952c-fb00d363a2b8"
SLUG    = "count_square_submatrices_with_all_ones"

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 1277,
    pattern     = "Dynamic Programming",
    subpatterns = ["DP: 2D Grid (Maximal Square)"],
    tc          = "O(m·n)",
    sc          = "O(1) in-place",
    key_insight = "dp[i][j] = min(top,left,diagonal)+1; sum all dp values = total square count",
    icon        = "🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"bold": True}),
        (" binary matrix, return the number of square submatrices that have all ones. "
         "Count squares of every size (1×1, 2×2, 3×3, …) across the entire matrix. "
         "Squares can overlap.", {})
    ])),
    N.para("Example: matrix = [[0,1,1,1],[1,1,1,1],[0,1,1,1]] → Output: 15  "
           "(10 ones give ten 1×1 squares, four 2×2 squares, one 3×3 square = 15 total)."),
    N.divider(),
]

# ── Solution 1: DP Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP Tabulation In-Place (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'how many k×k all-ones squares exist?', fix the bottom-right corner. "
               "Every square has exactly one bottom-right corner. If you know the largest all-ones square "
               "ending at (i,j) has side-length k, then exactly k squares end there (sizes 1×1 through k×k). "
               "Sum over all cells and you count all squares exactly once."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: iterate every possible (top-left corner, size) triple — O(m²·n²) time. "
               "For a 300×300 matrix that's billions of operations. TLE."),
        N.h4("The Key Observation"),
        N.para("dp[i][j] = side-length of largest all-ones square with bottom-right corner at (i,j). "
               "This value satisfies the recurrence: min(top, left, diagonal) + 1. "
               "The three neighbors tile the larger square — the minimum is the bottleneck (weakest link)."),
        N.h4("Building the Solution"),
        N.para("Step 1: Base cases — first row and first column cells can only form 1×1 squares. "
               "Step 2: For interior 1-cells: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1. "
               "Step 3: Accumulate total += dp[i][j]. Modify matrix in-place for O(1) space."),
        N.callout(
            "Analogy: Think of each cell asking its three neighbors 'how large a square can you support?' "
            "The most pessimistic answer (min) determines what this cell can extend to. "
            "Like a chain: it breaks at its weakest link.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def countSquares(matrix):\n"
        "    m, n = len(matrix), len(matrix[0])\n"
        "    total = 0\n"
        "    for i in range(m):\n"
        "        for j in range(n):\n"
        "            if matrix[i][j] and i > 0 and j > 0:\n"
        "                matrix[i][j] = 1 + min(\n"
        "                    matrix[i-1][j],   # top\n"
        "                    matrix[i][j-1],   # left\n"
        "                    matrix[i-1][j-1]  # diagonal\n"
        "                )\n"
        "            total += matrix[i][j]\n"
        "    return total"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(matrix), len(matrix[0])", {"code": True}),
                   (" — store dimensions for bounds checking.", {})])),
    N.para(N.rich([("total = 0", {"code": True}),
                   (" — accumulator: will hold sum of all dp[i][j] values.", {})])),
    N.para(N.rich([("for i in range(m): for j in range(n):", {"code": True}),
                   (" — scan every cell top-to-bottom, left-to-right. This ordering ensures both "
                    "row i-1 and column j-1 are already computed before we need them.", {})])),
    N.para(N.rich([("if matrix[i][j] and i > 0 and j > 0:", {"code": True}),
                   (" — three conditions: the cell is 1 (not 0), and it's an interior cell "
                    "(not the first row or column). Edge cells keep their matrix value as the base case.", {})])),
    N.para(N.rich([("matrix[i][j] = 1 + min(top, left, diagonal)", {"code": True}),
                   (" — overwrites the cell in-place with its dp value. The minimum of the three "
                    "neighboring dp values is the maximum square side we can extend, plus 1 for "
                    "including the current cell.", {})])),
    N.para(N.rich([("total += matrix[i][j]", {"code": True}),
                   (" — adds the dp value to total. A dp value of k means k distinct all-ones squares "
                    "(of sizes 1 through k) have their bottom-right corner here.", {})])),
    N.para(N.rich([("return total", {"code": True}),
                   (" — sum of all dp[i][j] = total count of all-ones squares across the matrix.", {})])),
    N.divider(),
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — DP Memoization (Top-Down)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same state definition as Solution 1: dp(i,j) = side-length of largest all-ones square "
               "with bottom-right at (i,j). But we derive it recursively instead of iteratively."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion re-computes the same (i,j) states many times "
               "(each cell can be a dependency for up to 3 others). Without caching: exponential."),
        N.h4("The Key Observation"),
        N.para("With @lru_cache, each (i,j) is computed exactly once. The recurrence is identical to "
               "tabulation — the only difference is the call direction (top-down vs bottom-up)."),
        N.h4("Building the Solution"),
        N.para("Base cases are the first natural recursive exits: 0-cell returns 0, edge cell returns 1. "
               "Otherwise recurse to three neighbors and take min + 1. Easier to write from the recurrence directly."),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def countSquares(matrix):\n"
        "    m, n = len(matrix), len(matrix[0])\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i, j):\n"
        "        if matrix[i][j] == 0:\n"
        "            return 0  # 0-cell: no square ends here\n"
        "        if i == 0 or j == 0:\n"
        "            return 1  # edge: only 1×1 possible\n"
        "        return 1 + min(dp(i-1, j), dp(i, j-1), dp(i-1, j-1))\n"
        "\n"
        "    return sum(dp(i, j) for i in range(m) for j in range(n))"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — Python's memoization decorator. Caches dp(i,j) after first computation. "
                    "Each of the m×n states is computed once in O(1), giving O(mn) total.", {})])),
    N.para(N.rich([("if matrix[i][j] == 0: return 0", {"code": True}),
                   (" — a 0-cell can't be the bottom-right corner of any square.", {})])),
    N.para(N.rich([("if i == 0 or j == 0: return 1", {"code": True}),
                   (" — edge cell with value 1: only a 1×1 square possible. No neighbors above or left.", {})])),
    N.para(N.rich([("return 1 + min(dp(i-1,j), dp(i,j-1), dp(i-1,j-1))", {"code": True}),
                   (" — same recurrence as tabulation. lru_cache ensures neighbors are already cached.", {})])),
    N.para(N.rich([("sum(dp(i,j) for ...)", {"code": True}),
                   (" — triggers computation for all cells and sums their dp values.", {})])),
    N.divider(),
]

# ── Why This Is DP ──
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   ("The largest all-ones square ending at (i,j) depends exactly on "
                    "the dp values of its three immediate neighbors — no cell further away matters. "
                    "The global optimum at each cell is fully determined by sub-cell optima.", {})])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   ("Each cell (i,j) is a dependency for up to three cells: (i+1,j), (i,j+1), "
                    "and (i+1,j+1). Without caching/tabulation, brute recursion would recompute "
                    "the same cell many times.", {})])),
    N.h3("The Recurrence Relation"),
    N.code(
        "# Base cases\n"
        "dp[i][j] = 0                                    # if matrix[i][j] == 0\n"
        "dp[i][j] = matrix[i][j]                         # if i == 0 or j == 0\n"
        "\n"
        "# Interior 1-cells\n"
        "dp[i][j] = min(dp[i-1][j],   # top neighbor\n"
        "               dp[i][j-1],   # left neighbor\n"
        "               dp[i-1][j-1]  # diagonal neighbor\n"
        "               ) + 1\n"
        "\n"
        "# Answer\n"
        "answer = sum(dp[i][j] for all i, j)"
    ),
    N.callout(
        "Why min of THREE neighbors? For a k×k all-ones square to end at (i,j), three sub-squares "
        "of size (k-1)×(k-1) must exist: ending at (i-1,j) for the top strip, at (i,j-1) for the "
        "left strip, and at (i-1,j-1) for the interior. The min is the weakest link. "
        "Together they tile the k×k region without gaps.",
        "📐", "blue_background"),
    N.callout(
        "Why summing works: Every all-ones square has a unique bottom-right corner. "
        "A cell with dp-value k is the corner of exactly k distinct squares (sizes 1 through k). "
        "Partitioning by bottom-right corner is a perfect partition — no double counting.",
        "🔐", "green_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(m²·n²)", "O(1)"],
        ["DP Tabulation In-Place ✓", "O(m·n)", "O(1) extra"],
        ["DP Memoization", "O(m·n)", "O(m·n) cache"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("DP: 2D Grid (Maximal Square) — recurrence dp[i][j] = min(3 neighbors) + 1. "
                    "Verified in DSA_Patterns_and_SubPatterns_Guide.md Section 18.", {})])),
    N.callout(
        "When to recognize this pattern: 'Count/find all-ones squares of any size in a binary grid.' "
        "Or: 'What is the largest all-ones square?' (Maximal Square family). "
        "Signals: binary matrix + square region + optimization/counting across all sizes.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP: 2D Grid technique:"),
    N.bullet(N.rich([("Maximal Square", {"bold": True}),
                     (" (Medium) — Identical recurrence; return max(dp)² instead of summing (#221)", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}),
                     (" (Medium) — 2D grid DP with obstacles; dp[i][j] = dp[i-1][j] + dp[i][j-1] (#63)", {})])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}),
                     (" (Medium) — dp[i][j] = min(above, left) + grid[i][j]; same scan order (#64)", {})])),
    N.bullet(N.rich([("Triangle", {"bold": True}),
                     (" (Medium) — Bottom-up DP on triangle grid; same neighbor-dependency structure (#120)", {})])),
    N.bullet(N.rich([("Maximal Rectangle", {"bold": True}),
                     (" (Hard) — Find max-area all-ones rectangle; uses histogram heights + stack (#85)", {})])),
    N.bullet(N.rich([("Number of Submatrices That Sum to Target", {"bold": True}),
                     (" (Hard) — 2D prefix sums + hash map counting; harder cousin (#1074)", {})])),
    N.para("These problems share the same core pattern: define a DP value per cell in a 2D grid, "
           "build each value from immediate neighbors, scan in topological order (top-to-bottom, left-to-right)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming) — "
              "Sub-Pattern: DP: 2D Grid (Maximal Square)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the DP table fill visually — use Next/Prev or arrow keys to see "
                    "each recurrence applied cell by cell with decision panels showing the min-of-three "
                    "computation.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
