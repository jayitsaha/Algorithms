"""
gen_triangle.py — Notion page builder for LeetCode #120 Triangle
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

# Override token (notion_lib.py was redacted; token is still valid)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-81cc-814e-ecf33511e10b"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=120,
    pattern="Dynamic Programming",
    subpatterns=["Bottom-up DP"],
    tc="O(n^2)",
    sc="O(n)",
    key_insight="Copy the last row as base case; propagate min costs upward row by row using dp[j] = triangle[i][j] + min(dp[j], dp[j+1]).",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
print("Wiping existing blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} blocks.")

# 3) Build body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a triangular array ", {}),
        ("triangle", {"code": True}),
        (", return the minimum path sum from top to bottom. At each step you may move to an adjacent number in the row below. From position ", {}),
        ("j", {"code": True}),
        (" in row ", {}),
        ("i", {"code": True}),
        (", you can move to position ", {}),
        ("j", {"code": True}),
        (" or ", {}),
        ("j+1", {"code": True}),
        (" in row ", {}),
        ("i+1", {"code": True}),
        (". Use O(n) extra space.", {})
    ])),
    N.divider(),
]

# Solution 1: Bottom-Up Tabulation
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the minimum total sum over all top-to-bottom paths. The cost of a path through cell (i, j) equals the cell value plus the cost of the best sub-path below (i, j). This is optimal substructure: global optimum = local choice + sub-optimal."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always pick the smaller neighbor) fails because local optimal choices can lead to globally suboptimal paths — a slightly worse cell now can open up a much cheaper path later. Brute-force DFS tries all 2^(n-1) paths, exponentially slow."),
        N.h4("The Key Observation"),
        N.para("Work bottom-up. If we already know the cheapest cost to reach the bottom from every cell in row i+1, we can compute the cheapest cost from every cell in row i in O(row length) time. The DP only ever needs the previous row."),
        N.h4("Building the Solution"),
        N.para("Initialize dp = copy of last row (base case). For each row from second-to-last to row 0: dp[j] = triangle[i][j] + min(dp[j], dp[j+1]). After processing row 0, dp[0] is the answer."),
        N.callout("Analogy: Imagine computing the cheapest way to reach the ground from each floor in a pyramid, starting from the ground floor and working upward. Each floor's cost = its value + the cheaper of the two stairways below.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minimumTotal(triangle: list[list[int]]) -> int:\n"
        "    dp = triangle[-1][:]                          # copy last row as base case\n"
        "    for i in range(len(triangle) - 2, -1, -1):   # row from second-to-last to 0\n"
        "        for j in range(len(triangle[i])):         # each cell in row i\n"
        "            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])  # value + best child\n"
        "    return dp[0]                                  # apex = global min path sum\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = triangle[-1][:]", {"code": True}), (" — Shallow copy of the last row. Each dp[j] = cost of being at position j of the bottom row. The [:] slice is critical: without it dp is an alias and would corrupt the input.", {})])),
    N.para(N.rich([("for i in range(len(triangle)-2, -1, -1):", {"code": True}), (" — Iterate rows from index n-2 down to 0. Range start: second-to-last row. End: -1 (exclusive). Step: -1 (decrement).", {})])),
    N.para(N.rich([("for j in range(len(triangle[i])):", {"code": True}), (" — Row i has i+1 cells; j iterates from 0 to i inclusive.", {})])),
    N.para(N.rich([("dp[j] = triangle[i][j] + min(dp[j], dp[j+1])", {"code": True}), (" — The recurrence. Current cell value plus the minimum of the two children below. Because j is processed left-to-right and we only read dp[j] and dp[j+1] (not yet overwritten), in-place update is correct.", {})])),
    N.para(N.rich([("return dp[0]", {"code": True}), (" — After processing row 0, dp[0] holds the minimum sum of any complete top-to-bottom path.", {})])),
    N.divider(),
]

# Solution 2: Memoization
blocks += [
    N.h2("Solution 2 — Memoization / Top-Down DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(i, j) = minimum cost of a path starting at cell (i, j) and reaching the bottom. The answer is dp(0, 0). This naturally maps to top-down recursion with caching."),
        N.h4("What Doesn't Work"),
        N.para("Without caching, dp(i+1, j) is called from both dp(i, j-1) and dp(i, j) — the same subproblem recomputed multiple times. Without memoization: O(2^n) calls."),
        N.h4("The Key Observation"),
        N.para("There are only O(n^2) unique (i, j) pairs. Cache each result the first time it is computed. Every subsequent call with the same (i, j) is O(1). Total: O(n^2) time."),
        N.h4("Building the Solution"),
        N.para("Write dp(i, j) recursively. Base: i == n-1 returns triangle[i][j]. Recursive: triangle[i][j] + min(dp(i+1, j), dp(i+1, j+1)). Decorate with @lru_cache."),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def minimumTotal(triangle: list[list[int]]) -> int:\n"
        "    n = len(triangle)\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i: int, j: int) -> int:\n"
        "        if i == n - 1:\n"
        "            return triangle[i][j]          # base case: at the bottom row\n"
        "        left  = dp(i + 1, j)               # recurse to left child\n"
        "        right = dp(i + 1, j + 1)           # recurse to right child\n"
        "        return triangle[i][j] + min(left, right)\n"
        "\n"
        "    return dp(0, 0)\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoizes results keyed on (i, j) tuple. First call computes the result; all subsequent calls with same (i, j) return it instantly from cache.", {})])),
    N.para(N.rich([("if i == n - 1: return triangle[i][j]", {"code": True}), (" — Base case: at the bottom row; no further descent possible, cost equals the cell value.", {})])),
    N.para(N.rich([("return triangle[i][j] + min(left, right)", {"code": True}), (" — Recurrence: current cell value plus the minimum of the two child sub-path costs, both already memoized.", {})])),
    N.callout("Space note: memoization stores all O(n^2) results plus the recursion call stack of depth O(n). Total space is O(n^2). Tabulation (Solution 1) achieves the same time with only O(n) extra space.", "⚠️", "yellow_background"),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute-Force DFS", "O(2^n)", "O(n) stack", "TLE on any real input"],
        ["Memoization (Solution 2)", "O(n^2)", "O(n^2)", "Good; space-heavy"],
        ["Tabulation (Solution 1)", "O(n^2)", "O(n)", "Interview pick — optimal time and space"],
    ]),
    N.divider(),
]

# Why DP
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.h3("1. Optimal Substructure"),
    N.para("The minimum path sum from cell (i, j) to the bottom = triangle[i][j] + min(best-from-(i+1,j), best-from-(i+1,j+1)). The global optimal decomposes into optimal independent subproblems."),
    N.h3("2. Overlapping Subproblems"),
    N.para("Interior cell (i, j) is reachable from both parent cells (i-1, j-1) and (i-1, j). In a naive DFS, the same (i, j) subproblem is recomputed by both parents. In a triangle of n rows the call tree has O(2^n) nodes without memoization. DP reduces this to O(n^2) unique states, each computed once."),
    N.h3("Recurrence Relation"),
    N.code(
        "# Bottom-up\n"
        "dp[j] = triangle[i][j] + min(dp[j], dp[j+1])\n"
        "  for i in range(len(triangle)-2, -1, -1)\n"
        "  for j in range(i+1)\n"
        "\n"
        "# Base case\n"
        "dp = triangle[-1][:]   # copy of last row\n"
        "\n"
        "# Answer\n"
        "dp[0]  # apex, after all rows processed\n"
    ),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bottom-up DP (Tabulation), Grid/Shape Path DP", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for min/max/count over all paths in a triangular or grid structure\n"
        "• Movement is constrained to adjacent cells — a small fixed neighborhood\n"
        "• Structure is acyclic (directed — you always move downward, no cycles)\n"
        "• Greedy fails: local choices don't guarantee global optimum\n"
        "• Brute-force path count grows exponentially with rows",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Bottom-up DP / Grid Path technique:"),
    N.bullet(N.rich([("Minimum Path Sum (64)", {"bold": True}), (" (Medium) — same DP pattern on a rectangular grid; move right or down only", {})])),
    N.bullet(N.rich([("Unique Paths II (63)", {"bold": True}), (" (Medium) — count paths (not min sum) in a grid with obstacles", {})])),
    N.bullet(N.rich([("Dungeon Game (174)", {"bold": True}), (" (Hard) — reverse bottom-up DP; maintain minimum health threshold at each cell", {})])),
    N.bullet(N.rich([("Pascal's Triangle (118)", {"bold": True}), (" (Easy) — generate the triangle; each cell = sum of two parents above (additive not min)", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum (931)", {"bold": True}), (" (Medium) — same bottom-up DP on a square matrix; step to any of 3 cells in the row below", {})])),
    N.bullet(N.rich([("Cherry Pickup (741)", {"bold": True}), (" (Hard) — two simultaneous path problems on the same grid; requires 3D DP state", {})])),
    N.para("These problems share the technique: define dp[j] as optimal cost to reach a boundary from position j, fill bottom-up (or top-down with memo), read apex or minimum."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18: Dynamic Programming", "📚", "gray_background"),
]

# Visual embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("triangle")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks written: {len(blocks)}")
