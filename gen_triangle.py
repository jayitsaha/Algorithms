"""
gen_triangle.py — Regenerate Notion page for Triangle (#120) in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81cc-814e-ecf33511e10b"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=120,
    pattern="Dynamic Programming",
    subpatterns=["Bottom-up DP"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Sweep bottom-up: dp[j] = triangle[i][j] + min(dp[j], dp[j+1]); return dp[0].",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
print("Wiping old content...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────
print("Building new content...")
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a triangle array, return the minimum path sum from top to bottom. "
         "At each step you may move to an adjacent number in the row below "
         "(adjacent means same index "),
        ("j", {"code": True}),
        (" or "),
        ("j+1", {"code": True}),
        (" in the next row). Each step you move to one of the two indices adjacent to the current index in the row below.")
    ])),
    N.para(N.rich([
        ("Example: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]. "
         "Optimal path: 2 → 3 → 5 → 1 = 11.")
    ])),
    N.divider(),
]

# Solution 1 — Bottom-Up Tabulation
SOLN1_CODE = """\
def minimumTotal(triangle: list[list[int]]) -> int:
    dp = triangle[-1][:]                   # copy last row (base case)
    for i in range(len(triangle)-2, -1, -1):   # sweep from 2nd-to-last row up
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j+1])  # best of two children
    return dp[0]                           # apex = global minimum path sum
"""

blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the minimum cost path from the top to any cell in the bottom row. "
            "Instead of asking 'where do I go from here?' (top-down, exponential), "
            "ask 'what is the best cost from here down to the bottom?' for every cell. "
            "If we know the answer for every cell in row i+1, we can answer for row i in O(row width) time."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy (always pick the smaller child) fails: on [[1],[2,3],[20,4,1]], greedy picks "
            "1→2→4 = 7 but optimal is 1→3→1 = 5. Greedy has no look-ahead. "
            "Brute force DFS explores all paths — O(2^n) for n rows, exponential."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Optimal substructure holds: min_path(i,j) = triangle[i][j] + min(min_path(i+1,j), min_path(i+1,j+1)). "
            "Subproblems overlap: cell (i,j) is reachable from two cells above, so a recursive solution "
            "recomputes it multiple times. Memoization or tabulation solves each cell exactly once."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base case: last row — each cell is a complete path. "
            "Copy it to dp[]. "
            "Then sweep upward: for each row i and each column j, "
            "dp[j] = triangle[i][j] + min(dp[j], dp[j+1]). "
            "After processing row 0 (the apex), dp[0] is the answer."
        ),
        N.callout(
            "Analogy: Imagine each cell is a city. You're building the best 'express route' map "
            "from every city to the coast (bottom row). Start by labeling coast cities with their "
            "own distance (0 extra), then work inland one row at a time — each inland city's "
            "best route = road cost + best route from its best coastal-facing neighbor.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLN1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = triangle[-1][:]", {"code": True}), " — Slice-copy the last row as base case. Slice avoids mutating the original input. Each dp[j] = triangle[last][j] (a complete path of length 1)."])),
    N.para(N.rich([("for i in range(len(triangle)-2, -1, -1):", {"code": True}), " — Walk from the second-to-last row up to row 0 (inclusive). The -1 step means we go in reverse."])),
    N.para(N.rich([("for j in range(len(triangle[i])):", {"code": True}), " — Row i has exactly i+1 elements. We update each column left-to-right."])),
    N.para(N.rich([("dp[j] = triangle[i][j] + min(dp[j], dp[j+1])", {"code": True}), " — The recurrence: current cell value + the lesser of the two children's min-path costs. dp[j] and dp[j+1] still hold the row-below values because we process left-to-right and never look right-of-j in the same pass."])),
    N.para(N.rich([("return dp[0]", {"code": True}), " — After the apex row (just one cell), dp[0] = minimum path sum from top to bottom."])),
    N.callout(
        "Warning: dp = triangle[-1] (no slice) would make dp a reference, not a copy. "
        "Modifying dp[j] would corrupt the original triangle. Always use [:] when you plan to mutate.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Top-Down Memoization
SOLN2_CODE = """\
from functools import lru_cache

def minimumTotal(triangle: list[list[int]]) -> int:
    n = len(triangle)

    @lru_cache(maxsize=None)
    def dp(i, j):
        # Returns min cost path from cell (i, j) down to the bottom row
        if i == n - 1:
            return triangle[i][j]   # base case: bottom row
        return triangle[i][j] + min(dp(i+1, j), dp(i+1, j+1))

    return dp(0, 0)   # start from the apex
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think recursively: 'What is the min-cost path from (i,j) to the bottom?' "
            "The answer depends on the same question for (i+1,j) and (i+1,j+1). "
            "This recursive structure maps naturally to a function dp(i, j)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without memoization, dp(i,j) is called once for each unique path that reaches (i,j) — "
            "that's O(2^n) calls total. With lru_cache, each (i,j) pair is computed once: O(n^2) distinct states."
        ),
        N.h4("The Key Observation"),
        N.para(
            "lru_cache automatically builds a memo table indexed by (i, j). "
            "The first time dp(i,j) is called it computes and stores the result. "
            "Every subsequent call is an O(1) cache hit. "
            "This top-down approach directly mirrors the recurrence and is easy to explain in interviews."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp(i, j) = min cost from (i,j) to bottom. "
            "Base case: i == n-1 → return triangle[i][j]. "
            "Recurrence: triangle[i][j] + min(dp(i+1,j), dp(i+1,j+1)). "
            "Entry point: dp(0, 0)."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Python's built-in memoization decorator. Caches results keyed by all arguments. maxsize=None means unlimited cache size."])),
    N.para(N.rich([("if i == n - 1: return triangle[i][j]", {"code": True}), " — Base case: bottom row cells have no children. The min path from here to the bottom is just the cell itself."])),
    N.para(N.rich([("return triangle[i][j] + min(dp(i+1, j), dp(i+1, j+1))", {"code": True}), " — Recurrence: pick the cheaper child path. Both sub-calls are O(1) after the first computation thanks to the cache."])),
    N.para(N.rich([("return dp(0, 0)", {"code": True}), " — Query the apex. The cache fills lazily from the bottom of each call stack up."])),
    N.callout(
        "Space trade-off: Top-down uses O(n²) space for the cache plus O(n) recursion stack depth. "
        "Bottom-up uses only O(n) for the rolling dp array. "
        "For very deep triangles (n > 1000), bottom-up avoids Python's recursion limit.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 3 — In-Place
SOLN3_CODE = """\
def minimumTotal(triangle: list[list[int]]) -> int:
    # Modify the triangle in-place — O(1) extra space
    for i in range(len(triangle)-2, -1, -1):
        for j in range(len(triangle[i])):
            triangle[i][j] += min(triangle[i+1][j], triangle[i+1][j+1])
    return triangle[0][0]
"""

blocks += [
    N.h2("Solution 3 — In-Place DP (O(1) Extra Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The rolling array in Solution 1 holds values from the row below. "
            "But those values ARE already stored in the triangle! "
            "If we are allowed to mutate the input, we can write the dp values "
            "directly into the triangle cells, eliminating the dp array entirely."
        ),
        N.h4("The Key Observation"),
        N.para(
            "triangle[i][j] += min(triangle[i+1][j], triangle[i+1][j+1]) overwrites "
            "each cell with its own min-path cost. After processing, triangle[0][0] holds the answer. "
            "This is the O(1) extra space variant — always mention it as the follow-up."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLN3_CODE),
    N.callout(
        "Trade-off: O(1) extra space but mutates the input. In interviews, always mention "
        "this trade-off explicitly: 'If the interviewer allows mutating input, this is more space-efficient.'",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DFS", "O(2ⁿ)", "O(n)"],
        ["Top-Down Memoization", "O(n²)", "O(n²)"],
        ["Bottom-Up Tabulation (✓ Interview Pick)", "O(n²)", "O(n)"],
        ["In-Place DP", "O(n²)", "O(1) extra"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming (Section 18 — 2D Grid DP)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Bottom-up DP (rolling 1D array, sweep from base row to apex)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Minimum/maximum path sum through a triangle or grid' — optimization over paths. "
        "(2) Movement restricted to adjacent cells (down, right-down). "
        "(3) Asked for optimal value, not path reconstruction. "
        "(4) Follow-up asks for O(n) space → rolling array replaces 2D table.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Bottom-up DP / 2D Grid):"),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), " (Medium) — Same recurrence on a rectangular grid: dp[i][j] = grid[i][j] + min(up, left). LeetCode #64"])),
    N.bullet(N.rich([("Unique Paths", {"bold": True}), " (Medium) — Count all paths instead of minimizing cost; dp[i][j] = dp[i-1][j] + dp[i][j-1]. LeetCode #62"])),
    N.bullet(N.rich([("Minimum Falling Path Sum", {"bold": True}), " (Medium) — Same bottom-up sweep on a square matrix with three parents per cell. LeetCode #931"])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), " (Hard) — Reverse DP (bottom-right to top-left) maintaining minimum health requirement. LeetCode #174"])),
    N.bullet(N.rich([("Cherry Pickup", {"bold": True}), " (Hard) — Two simultaneous paths through a grid, 3D DP state. LeetCode #741"])),
    N.bullet(N.rich([("Pascal's Triangle II", {"bold": True}), " (Easy) — Build a row of Pascal's triangle using same two-parent-sum recurrence. LeetCode #119"])),
    N.para("These problems share the core technique: sweep a 2D structure row-by-row (or column-by-column), using a rolling 1D array so that only one row of DP values is kept in memory at a time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18.5 (Dynamic Programming → 2D Grid DP). Sub-Pattern verified: Bottom-up DP · Source: Guide Section 18.5", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("triangle")),
    N.para(N.rich([("Step through the bottom-up DP sweep visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
