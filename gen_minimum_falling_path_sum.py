"""
gen_minimum_falling_path_sum.py
Notion IN-PLACE update for LeetCode #931 — Minimum Falling Path Sum.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8120-8965-fab494113861"
SLUG = "minimum_falling_path_sum"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=931,
    pattern="Dynamic Programming",
    subpatterns=["DP from Previous Row"],
    tc="O(n²)",
    sc="O(1)",
    key_insight="dp[r][c] = matrix[r][c] + min of up to 3 parents in row r−1; modify in-place for O(1) space.",
    icon="🟡"
)
print("Properties OK")

# ── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} old blocks")

# ── 3. Rebuild body ─────────────────────────────────────────────────────────
print("Building new body blocks...")

TABULATION_CODE = """\
def minFallingPathSum(matrix):
    n = len(matrix)
    for r in range(1, n):
        for c in range(n):
            best = matrix[r-1][c]           # start with directly-above parent
            if c > 0:
                best = min(best, matrix[r-1][c-1])   # upper-left
            if c < n-1:
                best = min(best, matrix[r-1][c+1])   # upper-right
            matrix[r][c] += best            # in-place: cumulative min cost
    return min(matrix[n-1])                 # cheapest path end in last row"""

MEMO_CODE = """\
from functools import lru_cache

def minFallingPathSum(matrix):
    n = len(matrix)

    @lru_cache(maxsize=None)
    def dp(r, c):
        if r == 0:
            return matrix[0][c]          # base case: top row
        parents = [c]
        if c > 0:   parents.append(c - 1)
        if c < n-1: parents.append(c + 1)
        return matrix[r][c] + min(dp(r - 1, pc) for pc in parents)

    return min(dp(n - 1, c) for c in range(n))"""

RECURRENCE = """\
dp[r][c] = matrix[r][c] + min(dp[r-1][c-1], dp[r-1][c], dp[r-1][c+1])
           (include only valid neighbours — skip out-of-bounds)

Base case : dp[0][c] = matrix[0][c]   for all c
Answer    : min(dp[n-1][c])           for all c"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an ", ("n", {"code": True}), " × ", ("n", {"code": True}),
        " integer matrix, return the minimum sum of any falling path through the matrix. "
        "A falling path starts at any element in the first row and chooses from each row "
        "to move to the element in the next row that is directly below, diagonally below-left, "
        "or diagonally below-right."
    ])),
    N.divider()
]

# ── Solution 1: Tabulation ──
blocks += [
    N.h2("Solution 1 — In-place Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the cheapest sum from any top-row cell down to the last row, "
               "moving one step diagonally or straight each row. "
               "This is an optimization over all possible paths."),
        N.h4("What Doesn't Work"),
        N.para("Greedy fails: always choosing the smallest neighbour is shortsighted. "
               "A locally cheap step may lead to expensive options in later rows. "
               "Brute-force DFS tries every possible path — O(3ⁿ) time, impractical for n > 10."),
        N.h4("The Key Observation"),
        N.para("The optimal cost to reach (r, c) depends only on the three cells directly "
               "above it: (r−1, c−1), (r−1, c), (r−1, c+1). "
               "If we know the minimum cost to reach each of those three cells, we can compute "
               "(r, c) in O(1). This is optimal substructure — the foundation of DP."),
        N.h4("Building the Solution"),
        N.para("Process rows top to bottom. Row 0 is the base case (no parents). "
               "For each subsequent row, for each column, take the min of valid parents "
               "in the previous row and add the current cell's value. "
               "Since row r only reads row r−1 (already computed), we can overwrite the matrix "
               "in-place — reducing extra space to O(1)."),
        N.callout(
            "Analogy: Imagine water flowing down a hillside. Each drop takes the steepest "
            "(cheapest) path available to it. After the rain settles, every spot on the "
            "ground holds the total elevation drop of the cheapest path that reached it "
            "from the top. That is exactly what our DP table holds.",
            "🌧️", "blue_background")
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        "The best path to (r, c) is (best path to its cheapest parent) + value at (r, c). "
        "Any globally optimal path contains optimal sub-paths — swap in a cheaper sub-path "
        "and you'd improve the global answer, contradiction."
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        "Cell (r−1, c) is a valid parent of (r, c−1), (r, c), and (r, c+1). "
        "A brute-force recursion would recompute it three times. "
        "DP computes it once and reuses the result."
    ])),
    N.h3("Recurrence Relation"),
    N.code(RECURRENCE, "plain text"),
    N.h3("Code"),
    N.code(TABULATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(matrix)", {"code": True}), " — matrix is n×n; n gives both dimensions."])),
    N.para(N.rich([("for r in range(1, n)", {"code": True}), " — start from row 1; row 0 is already the base case."])),
    N.para(N.rich([("for c in range(n)", {"code": True}), " — process every column in the current row."])),
    N.para(N.rich([("best = matrix[r-1][c]", {"code": True}), " — initialize with directly-above parent (always valid)."])),
    N.para(N.rich([("if c > 0: best = min(best, matrix[r-1][c-1])", {"code": True}), " — check upper-left if not in leftmost column."])),
    N.para(N.rich([("if c < n-1: best = min(best, matrix[r-1][c+1])", {"code": True}), " — check upper-right if not in rightmost column."])),
    N.para(N.rich([("matrix[r][c] += best", {"code": True}), " — overwrite cell: self-value + cheapest parent cost = total min cost to reach here."])),
    N.para(N.rich([("return min(matrix[n-1])", {"code": True}), " — every last-row cell holds the min cost to reach it; global min is the answer."])),
    N.callout(
        "⚠️  Common mistake: writing matrix[r][c] = best (losing the cell's own contribution) "
        "instead of matrix[r][c] += best. The cell's value is the cost of visiting that position.",
        "⚠️", "yellow_background"),
    N.divider()
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(r, c) = minimum falling path sum that ends at cell (r, c). "
               "Start from any last-row cell and recurse upward."),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without a cache recomputes dp(r, c) up to 3 times "
               "for each downstream cell. The cache eliminates all redundant calls."),
        N.h4("The Key Observation"),
        N.para("The recurrence dp(r, c) = matrix[r][c] + min(dp(r−1, pc) for valid parents pc) "
               "directly translates to code. @lru_cache handles memoization automatically."),
        N.h4("Building the Solution"),
        N.para("Write the recursion exactly as the recurrence. Base case: r=0 returns the cell value. "
               "Recursive case: call dp for each valid parent column in row r−1, take the min, add self."),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — memoize every (r, c) call; each of n² pairs computed once."])),
    N.para(N.rich([("if r == 0: return matrix[0][c]", {"code": True}), " — base case: top row has no parents, cost = cell value."])),
    N.para(N.rich([("parents = [c]", {"code": True}), " — always include directly-above column."])),
    N.para(N.rich([("if c > 0: parents.append(c-1)", {"code": True}), " — upper-left if within bounds."])),
    N.para(N.rich([("if c < n-1: parents.append(c+1)", {"code": True}), " — upper-right if within bounds."])),
    N.para(N.rich([("return matrix[r][c] + min(dp(r-1, pc)...)", {"code": True}), " — recurse to each parent, add self value."])),
    N.para(N.rich([("min(dp(n-1, c) for c in range(n))", {"code": True}), " — query all last-row endpoints, return the minimum."])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-force DFS", "O(3ⁿ)", "O(n)"],
        ["Memoization (top-down)", "O(n²)", "O(n²)"],
        ["In-place Tabulation ✓", "O(n²)", "O(1)"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "DP from Previous Row (grid path variant)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Grid path problem with downward-only movement (no returning up)\n"
        "• Each cell's answer depends on a small, bounded window of the previous row\n"
        "• Multiple valid starting positions AND/OR ending positions\n"
        "• 'Minimum / maximum sum over any falling path from top to bottom'",
        "🔎", "green_background"),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP from Previous Row technique:"),
    N.bullet(N.rich([("Triangle", {"bold": True}), " (Medium, #120) — Min path in a variable-width triangle; same row-by-row DP"])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), " (Medium, #64) — Grid DP, right/down moves only; classic 2D table"])),
    N.bullet(N.rich([("Minimum Falling Path Sum II", {"bold": True}), " (Hard, #1289) — Any column (not adjacent) in next row; track top-2 minima per row"])),
    N.bullet(N.rich([("Paint House", {"bold": True}), " (Medium, #256) — Row DP where adjacent rows cannot share the same color"])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), " (Hard, #174) — Backward DP from bottom-right; minimum health along a path"])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), " (Medium, #221) — 2D grid DP where each cell depends on 3 neighbours; largest all-1 square"])),
    N.para("These problems share the core technique: each row's DP values are built from a bounded window of the previous row, enabling O(1) or O(n) space optimization."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) · Sub-Pattern: DP from Previous Row", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
