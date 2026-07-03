"""
gen_dungeon_game.py — Notion update for LeetCode #174 Dungeon Game.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a6-bfce-ed2c0fe8fa36"
SLUG = "dungeon_game"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=174,
    pattern="Dynamic Programming",
    subpatterns=["Reverse DP from End"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Work backwards: dp[i][j] = min HP to enter (i,j) and survive. dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]).",
    icon="🔴"
)
print("Properties set.")

# 2) Wipe existing body
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body
blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("The demons had captured the princess and imprisoned her in the bottom-right room of a ", {}),
        ("dungeon", {"code": True}),
        (" grid (", {}),
        ("m x n", {"code": True}),
        ("). The knight was initially positioned in the top-left room. The knight has an initial health point represented by a positive integer. If at any point his health drops to 0 or below, he dies immediately. Some rooms are guarded by demons (negative values), others contain magic orbs that increase health (positive values), and some are empty (value 0). The knight can only move ", {}),
        ("right", {"bold": True}),
        (" or ", {}),
        ("down", {"bold": True}),
        (" at each step. Return the knight's minimum initial health so that he can rescue the princess.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Bottom-Up Tabulation (Interview Pick) ─────────────────────
TABULATION_CODE = """def calculateMinimumHP(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0] * n for _ in range(m)]

    # Base case: princess cell
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])

    # Fill last row (only exit: right)
    for j in range(n-2, -1, -1):
        dp[m-1][j] = max(1, dp[m-1][j+1] - dungeon[m-1][j])

    # Fill last column (only exit: down)
    for i in range(m-2, -1, -1):
        dp[i][n-1] = max(1, dp[i+1][n-1] - dungeon[i][n-1])

    # Fill interior cells
    for i in range(m-2, -1, -1):
        for j in range(n-2, -1, -1):
            best = min(dp[i+1][j], dp[i][j+1])
            dp[i][j] = max(1, best - dungeon[i][j])

    return dp[0][0]"""

blocks += [
    N.h2("Solution 1 — Reverse DP: Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each cell, ask: 'What is the minimum HP I need when entering this cell to guarantee reaching the princess alive?' This is a function only of the cells ahead — making it computable backwards."),
        N.h4("What Doesn't Work"),
        N.para("Forward DP ('track max health at each cell') fails. A path arriving at (i,j) with high health may still die in future cells, while a lower-health path avoids deadly corridors. You cannot make locally optimal decisions without knowing the future."),
        N.h4("The Key Observation"),
        N.para("Define dp[i][j] = minimum HP to enter (i,j) and survive. The terminal condition (princess cell) is well-defined: max(1, 1 - dungeon[m-1][n-1]). Working backwards, each cell only depends on its two neighbors to the right and below — both already computed."),
        N.h4("Building the Solution"),
        N.para("1. Fill princess cell (base case). 2. Fill last row right-to-left (only exit: right). 3. Fill last column bottom-to-top (only exit: down). 4. Fill interior cells bottom-right to top-left — take min of two exits, apply recurrence, clamp at 1. 5. Return dp[0][0]."),
        N.callout("Analogy: Planning a mountain expedition backwards — at the summit you know exactly what you need to descend safely; then compute what you need at the midpoint to reach the summit; and so on back to base camp.", "🧠", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("dp[i][j] depends only on dp[i+1][j] and dp[i][j+1]. The minimum HP needed at any cell is determined entirely by the two cells ahead — a clean recursive sub-problem.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Cell (1,1) is reachable via (0,1)→(1,1) or (1,0)→(1,1). Without memoization, a brute-force recursive approach recomputes dp[1][1] once per path — exponentially wasteful for large grids.", {})
    ])),
    N.h3("The Recurrence"),
    N.code(
        "Base:     dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])\n"
        "Last row: dp[m-1][j]   = max(1, dp[m-1][j+1] - dungeon[m-1][j])\n"
        "Last col: dp[i][n-1]   = max(1, dp[i+1][n-1] - dungeon[i][n-1])\n"
        "Interior: best         = min(dp[i+1][j], dp[i][j+1])\n"
        "          dp[i][j]     = max(1, best - dungeon[i][j])",
        "text"
    ),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = ...", {"code": True}), " — grid dimensions.", {}])),
    N.para(N.rich([("dp = [[0]*n ...]", {"code": True}), " — DP table; dp[i][j] = min HP to enter (i,j) and survive to end.", {}])),
    N.para(N.rich([("dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])", {"code": True}), " — Base case: to survive the princess cell with ≥1 HP after entry.", {}])),
    N.para(N.rich([("for j in range(n-2, -1, -1):", {"code": True}), " — Fill last row right-to-left. Only exit is rightward.", {}])),
    N.para(N.rich([("for i in range(m-2, -1, -1):", {"code": True}), " — Fill last column bottom-to-top. Only exit is downward.", {}])),
    N.para(N.rich([("best = min(dp[i+1][j], dp[i][j+1])", {"code": True}), " — Knight will take the cheaper future path (min HP required).", {}])),
    N.para(N.rich([("dp[i][j] = max(1, best - dungeon[i][j])", {"code": True}), " — Min HP to enter this cell. Clamp at 1 (must be alive).", {}])),
    N.para(N.rich([("return dp[0][0]", {"code": True}), " — Minimum starting health for the knight.", {}])),
    N.callout(
        "⚠️ Why max(1, ...)? If dungeon[i][j] = +100 and dp[i+1][j] = 5, the formula gives 5−100 = −95. The knight can't have negative HP. max(1,...) enforces the physical constraint that the knight must always be alive (≥1 HP) to enter any room.",
        "⚠️", "orange_background"
    ),
    N.divider(),
]

# ── Solution 2: Top-Down Memoization ──────────────────────────────────────
MEMO_CODE = """from functools import lru_cache

def calculateMinimumHP(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])

    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        \"\"\"Returns min HP needed to enter (i,j) and reach the princess alive.\"\"\"
        if i == m-1 and j == n-1:
            return max(1, 1 - dungeon[i][j])  # base case
        exits = []
        if i + 1 < m:
            exits.append(dp(i+1, j))  # can go down
        if j + 1 < n:
            exits.append(dp(i, j+1))  # can go right
        return max(1, min(exits) - dungeon[i][j])

    return dp(0, 0)"""

blocks += [
    N.h2("Solution 2 — Reverse DP: Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same state definition — dp(i, j) = min HP to enter (i,j) and survive — but expressed recursively. Start at dp(0,0) and recurse outward, memoizing results."),
        N.h4("The Key Observation"),
        N.para("The recursion has the same structure as tabulation: dp(i,j) = max(1, min(dp(i+1,j), dp(i,j+1)) - dungeon[i][j]). With @lru_cache, each sub-problem is computed once."),
        N.h4("Building the Solution"),
        N.para("Define a recursive function dp(i,j) with base case at the princess cell. For interior cells, collect valid exits (down/right), take the minimum, apply the formula. lru_cache handles memoization automatically."),
        N.callout("Top-down is often easier to derive in an interview — write the recurrence as a recursive function and add caching. Bottom-up requires explicitly choosing fill order.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache", {"code": True}), " — Python decorator that caches dp(i,j) results; any repeat call returns instantly.", {}])),
    N.para(N.rich([("if i==m-1 and j==n-1:", {"code": True}), " — Base case: princess cell. Knight needs max(1, 1−dungeon[i][j]) HP.", {}])),
    N.para(N.rich([("exits.append(dp(i+1,j))", {"code": True}), " — Recurse into the cell below (if valid).", {}])),
    N.para(N.rich([("exits.append(dp(i,j+1))", {"code": True}), " — Recurse into the cell to the right (if valid).", {}])),
    N.para(N.rich([("return max(1, min(exits) - dungeon[i][j])", {"code": True}), " — Take cheaper exit, compute required entry HP, clamp at 1.", {}])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force DFS", "O(2^(m+n))", "O(m+n)", "All paths — exponential"],
        ["Tabulation DP", "O(m·n)", "O(m·n)", "Optimal; interview pick"],
        ["Memoization DP", "O(m·n)", "O(m·n)+stack", "Same; easier to derive"],
        ["Space-optimized DP", "O(m·n)", "O(n)", "Rolling 1D array"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Reverse DP from End — fill the DP table backwards from the terminal state when forward DP is blocked by future-dependency constraints.", {})])),
    N.callout(
        "When to recognize this pattern: grid with right/down moves + survival/constraint that depends on future cells + forward DP creates ambiguity + terminal condition is well-defined. Also: triangle problems (fill bottom-to-top), any problem where you know the end condition but not the beginning.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium) — Same grid DP; minimize total cost top-left→bottom-right. Forward DP works here — no survival constraint mid-path.", {})])),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium) — Classic reverse DP: fill a triangular array bottom-to-top for minimum path sum. Same backwards intuition.", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium) — Count all paths with obstacles; builds the same 2D DP spatial reasoning and fill-order discipline.", {})])),
    N.bullet(N.rich([("Cherry Pickup", {"bold": True}), (" (Hard) — Two agents traverse the same grid; extends to 3D DP. Same reverse-fill idea.", {})])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), (" (Medium) — Each cell's DP value depends on three neighboring cells. Classic 2D DP dependency pattern.", {})])),
    N.bullet(N.rich([("Coin Change", {"bold": True}), (" (Medium) — 'Min cost to reach a target' framing; same flavor of DP with a constraint that must hold end-to-end.", {})])),
    N.para("These problems share the core insight: define state as 'what do I need here to succeed?' and fill backwards from the known terminal condition."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18. Dynamic Programming → Sub-Pattern: Reverse DP from End.", "📚", "gray_background"),
]

# ── Visual Explainer embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch the DP table fill cell-by-cell from the princess room back to the knight's start.",
         {"italic": True, "color": "gray"})
    ])),
]

# 4) Append all blocks
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
