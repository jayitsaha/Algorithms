"""
gen_number_of_ways_to_paint_n_x_3_grid.py
Notion page generator for LeetCode #1411 — Number of Ways to Paint N x 3 Grid
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "number_of_ways_to_paint_n_x_3_grid"
NAME = "Number of Ways to Paint N x 3 Grid"
NUMBER = 1411
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "Dynamic Programming"
SUBPATTERNS = ["Two-Color and Three-Color Patterns"]

# ── Step 0: Create page (notion_page_id is null) ──────────────────────────────
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set Properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc="O(n)",
    sc="O(1)",
    key_insight="12 valid row patterns collapse into 2 states (2-color/3-color) by color symmetry; fixed transitions 3/2/2/2 drive O(n) O(1) DP.",
    icon=ICON
)
print("Properties set.")

# ── Step 2: Wipe (fresh page — nothing to wipe, but call for safety) ──────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks (fresh page).")

# ── Step 3: Build Body ────────────────────────────────────────────────────────

SOL1_CODE = """\
def numOfWays(n: int) -> int:
    MOD = 10**9 + 7
    # Base case: row 1 has 6 two-color and 6 three-color patterns
    t2, t3 = 6, 6
    for _ in range(n - 1):
        # Simultaneously update both states using OLD values
        t2, t3 = (3*t2 + 2*t3) % MOD, (2*t2 + 2*t3) % MOD
    return (t2 + t3) % MOD\
"""

SOL2_CODE = """\
from functools import lru_cache

def numOfWays(n: int) -> int:
    MOD = 10**9 + 7

    @lru_cache(maxsize=None)
    def dp(row, kind):
        # kind: 2 = two-color row, 3 = three-color row
        if row == 1:
            return 6  # 6 patterns of each type for first row
        if kind == 2:
            return (3 * dp(row-1, 2) + 2 * dp(row-1, 3)) % MOD
        else:
            return (2 * dp(row-1, 2) + 2 * dp(row-1, 3)) % MOD

    return (dp(n, 2) + dp(n, 3)) % MOD\
"""

RECURRENCE = """\
# Key recurrence (derived from exhaustive enumeration of valid transitions):
# t2[i] = 3 * t2[i-1] + 2 * t3[i-1]
# t3[i] = 2 * t2[i-1] + 2 * t3[i-1]
#
# Base case: t2[1] = 6, t3[1] = 6
# Answer: (t2[n] + t3[n]) % MOD
#
# Transition counts (verified by enumeration for e.g. R-G-R):
#   Two-color row  -> generates 3 two-color + 2 three-color next rows
#   Three-color row -> generates 2 two-color + 2 three-color next rows\
"""

PROBLEM_STATEMENT = (
    "You have a grid of n rows and 3 columns. You are given an integer n. "
    "Color each cell with one of 3 colors such that no two adjacent cells (sharing a side) "
    "have the same color. Return the number of valid colorings modulo 10^9 + 7."
)

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider()
]

# Solution 1 — Two-State DP (Interview Pick)
blocks += [
    N.h2("Solution 1 — Two-State Row DP, Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to count valid colorings of an n×3 grid where adjacent cells differ. "
            "A valid row of 3 cells with 3 colors has exactly 12 patterns. "
            "The key question: how many next-rows are compatible with each current row?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Tracking all 12 patterns individually requires 12 DP states that each transition "
            "into the others — manageable but verbose. Backtracking tries all possibilities "
            "and is O(12^n), which is exponential and far too slow for large n."
        ),
        N.h4("The Key Observation"),
        N.para(
            "By symmetry of the 3 colors, every two-color pattern (there are 6) generates "
            "exactly the same number of compatible next-row patterns. Same for every three-color "
            "pattern. So instead of tracking 12 individual counts, we track just 2 aggregates: "
            "t2 = total valid grids ending in any two-color row, t3 = total ending in any three-color row."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: count patterns for row 1 — t2 = 6, t3 = 6. "
            "Step 2: enumerate valid next rows for one two-color pattern (e.g. R-G-R) to get "
            "transition constants: 3 two-color + 2 three-color. Do the same for a three-color "
            "pattern (e.g. R-G-B): 2 two-color + 2 three-color. "
            "Step 3: iterate n-1 times applying the recurrence, mod 10^9+7 each step."
        ),
        N.callout(
            "Analogy: Think of t2 and t3 like two bank accounts that earn interest. "
            "Each period (row), t2 earns 3× its own balance plus 2× t3's balance; "
            "t3 earns 2× t2's balance plus 2× its own. Update both simultaneously at end of period.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(
        "Optimal substructure: the count of valid n-row grids ending in a two-color row "
        "depends directly on the counts for (n-1)-row grids. "
        "Overlapping subproblems: a naive recursion would recompute dp(row=4, two-color) "
        "from many branches; DP stores it once as t2."
    ),
    N.h3("Recurrence Relations"),
    N.code(RECURRENCE, "python"),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}), " — standard modulus for competitive programming; prevents integer overflow in large-n cases."])),
    N.para(N.rich([("t2, t3 = 6, 6", {"code": True}), " — base case: row 1 has exactly 6 two-color patterns and 6 three-color patterns."])),
    N.para(N.rich([("for _ in range(n - 1):", {"code": True}), " — we process rows 2 through n; that's n-1 iterations."])),
    N.para(N.rich([("t2, t3 = (3*t2 + 2*t3) % MOD, (2*t2 + 2*t3) % MOD", {"code": True}), " — simultaneous update using Python tuple assignment; both right-hand sides use the OLD t2 and t3 values. New t2: 3 contributions from each old two-color + 2 from each old three-color. New t3: 2 from each type."])),
    N.para(N.rich([("return (t2 + t3) % MOD", {"code": True}), " — sum both types to get total valid colorings for n rows."])),
    N.callout(
        "Warning: NEVER update t2 then compute t3 on separate lines using the new t2. "
        "The recurrence uses old values of both. Python tuple assignment evaluates all "
        "right-hand sides first, so t2, t3 = expr1, expr2 is safe.",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# Solution 2 — Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp(row, kind) = number of valid grids with the given row count where "
            "row 'row' uses 'kind' colors (2 or 3). The answer is dp(n,2) + dp(n,3)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization recomputes dp(row-1, 2) and dp(row-1, 3) "
            "multiple times — once from the kind=2 branch and once from kind=3. "
            "With memoization each (row, kind) pair is computed exactly once."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The state space is tiny: only 2n states (dp(row, 2) and dp(row, 3) for each row). "
            "Memoization makes this O(n) time and O(n) space. "
            "The recurrence is identical to the tabulation approach."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Use @lru_cache on a recursive dp function with parameters (row, kind). "
            "Base case: row == 1 returns 6 for either kind. "
            "Recursive case applies the same 3/2/2/2 transition constants."
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Python decorator that automatically memoizes the recursive function; avoids redundant computation."])),
    N.para(N.rich([("def dp(row, kind):", {"code": True}), " — state: row = which row (1 to n), kind = 2 (two-color) or 3 (three-color)."])),
    N.para(N.rich([("if row == 1: return 6", {"code": True}), " — base case: exactly 6 valid patterns of each type for the first row."])),
    N.para(N.rich([("3 * dp(row-1, 2) + 2 * dp(row-1, 3)", {"code": True}), " — two-color recurrence: 3 per prior two-color, 2 per prior three-color."])),
    N.para(N.rich([("2 * dp(row-1, 2) + 2 * dp(row-1, 3)", {"code": True}), " — three-color recurrence: 2 per prior two-color, 2 per prior three-color."])),
    N.para(N.rich([("return (dp(n, 2) + dp(n, 3)) % MOD", {"code": True}), " — sum both ending types for the final answer."])),
    N.divider()
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Backtracking", "O(12^n)", "O(n)"],
        ["Two-State DP Tabulation (optimal)", "O(n)", "O(1)"],
        ["Two-State DP Memoization", "O(n)", "O(n)"],
        ["Matrix Exponentiation", "O(log n)", "O(1)"]
    ]),
    N.divider()
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two-Color and Three-Color Patterns (State-based DP on row coloring)"])),
    N.callout(
        "When to recognize this pattern: grid coloring with adjacency constraints and small fixed width; "
        "symmetry between colors means only pattern type (not specific colors) matters; "
        "each row's valid next-row count depends only on current row type.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Paint House", {"bold": True}), " (Medium) — DP on row colors where adjacent houses differ; same row-state idea (#256)"])),
    N.bullet(N.rich([("Paint House II", {"bold": True}), " (Hard) — k colors, n houses; track minimum cost per ending color (#265)"])),
    N.bullet(N.rich([("Paint Fence", {"bold": True}), " (Medium) — color n posts with k colors, no 3 consecutive same; two-state DP (#276)"])),
    N.bullet(N.rich([("Student Attendance Record II", {"bold": True}), " (Hard) — count valid attendance strings with state transitions (#552)"])),
    N.bullet(N.rich([("Coloring a Border", {"bold": True}), " (Medium) — graph-based coloring with constraint propagation (#1034)"])),
    N.bullet(N.rich([("Number of Ways to Color a 3x3 Grid", {"bold": True}), " (Hard) — similar fixed-width grid coloring counting problem"])),
    N.para("These problems share state-based DP where each new element's count depends on a compressed state of the previous element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) | Problem entry line 941", "📚", "gray_background")
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | page_id={PAGE_ID}")
