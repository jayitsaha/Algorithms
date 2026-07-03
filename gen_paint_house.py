"""
gen_paint_house.py — Notion page rebuild for Paint House (LC #256)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-813c-b933-d9fa5df29357"

# ─── 1. Set properties ───────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=256,
    pattern="Dynamic Programming",
    subpatterns=["Min of Other Colors"],
    tc="O(n)",
    sc="O(1)",
    key_insight="dp[i][c] = costs[i][c] + min of the other two colors from dp[i-1]; roll three variables instead of a table.",
    icon="🟡"
)
print("  Properties OK")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

# ─── 3. Rebuild body ─────────────────────────────────────────────────────────
print("Rebuilding body...")

SOL1_CODE = """\
def minCost(costs: list[list[int]]) -> int:
    r, g, b = costs[0]          # Base case: house 0, no predecessor
    for cr, cg, cb in costs[1:]:
        r, g, b = (cr + min(g, b),   # new r = paint red + cheapest non-red prev
                   cg + min(r, b),   # new g = paint green + cheapest non-green prev
                   cb + min(r, g))   # new b = paint blue + cheapest non-blue prev
                                     # All three use OLD r, g, b via tuple assignment
    return min(r, g, b)          # min over all terminal colors"""

SOL2_CODE = """\
from functools import lru_cache

def minCost(costs: list[list[int]]) -> int:
    n = len(costs)
    @lru_cache(maxsize=None)
    def dp(i, c):
        # Min cost to paint houses 0..i with house i = color c
        if i == 0:
            return costs[0][c]
        return costs[i][c] + min(
            dp(i - 1, j) for j in range(3) if j != c
        )
    return min(dp(n - 1, c) for c in range(3))"""

RECURRENCE = """\
dp[i][R] = costs[i][R] + min(dp[i-1][G], dp[i-1][B])
dp[i][G] = costs[i][G] + min(dp[i-1][R], dp[i-1][B])
dp[i][B] = costs[i][B] + min(dp[i-1][R], dp[i-1][G])

Space optimization: keep only (r, g, b) — the previous row — instead of a full n×3 table."""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("n", {"code": True}),
        (" houses in a row. Each house can be painted with one of three colors: red, green, or blue. "
         "The cost of painting house ", {}),
        ("i", {"code": True}),
        (" with color ", {}),
        ("j", {"code": True}),
        (" is ", {}),
        ("costs[i][j]", {"code": True}),
        (". No two adjacent houses may have the same color. "
         "Return the minimum cost to paint all houses.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("costs = [[17,2,17],[16,16,5],[14,3,19]]. "
         "Optimal: G(2) → B(5) → G(3) = $10. "
         "Edge cases: n=1 (pick min of 3 directly); all equal costs; "
         "extreme differences that punish greedy choices.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Tabulation / rolling vars ────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Space-Optimized Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each house you choose one of 3 colors. The constraint is local: only the previous house's color matters. So at every position, you need to track exactly 3 numbers: the cheapest total cost to have reached this house with each color. No history beyond the previous step is needed."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always pick the cheapest non-adjacent color) fails because a locally cheap choice may block access to cheaper colors later. Brute force (try all 3^n sequences) is O(3^n) — infeasible for large n."),
        N.h4("The Key Observation"),
        N.para("The cost of painting house i red depends only on the cheapest way to have painted house i−1 in any non-red color. With only 3 colors, 'non-red' = min(green, blue). This gives a clean recurrence: dp[i][c] = costs[i][c] + min(dp[i-1][j] for j ≠ c)."),
        N.h4("Building the Solution"),
        N.para("Since each row only depends on the previous row, we don't need a table. Keep three rolling variables r, g, b. Update all three simultaneously (Python tuple assignment) to avoid using partially-updated values. After all houses, return min(r, g, b)."),
        N.callout("Analogy: Like a relay race where each runner (house) can pass the baton to either of the other two runners (colors). You track the cheapest cumulative time for each color to hold the baton, updated each leg.", "🧠", "blue_background"),
    ]),
    N.h3("The Recurrence"),
    N.code(RECURRENCE),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("r, g, b = costs[0]", {"code": True}),
                   (" — Base case: house 0 has no predecessor. DP cost = painting cost directly. r=costs[0][0] (red), g=costs[0][1] (green), b=costs[0][2] (blue).", {})])),
    N.para(N.rich([("for cr, cg, cb in costs[1:]:", {"code": True}),
                   (" — Unpack each subsequent house's three costs as cr (red), cg (green), cb (blue).", {})])),
    N.para(N.rich([("r, g, b = (cr + min(g, b), ...)", {"code": True}),
                   (" — Simultaneous tuple assignment. Evaluate all three expressions using OLD r, g, b, then assign. New r = cost to paint red + min of other two colors from previous step.", {})])),
    N.para(N.rich([("cg + min(r, b)", {"code": True}),
                   (" — New g: paint green + cheapest prior non-green (min of old r and old b).", {})])),
    N.para(N.rich([("cb + min(r, g)", {"code": True}),
                   (" — New b: paint blue + cheapest prior non-blue (min of old r and old g). Tuple assignment ensures all three expressions see the old values.", {})])),
    N.para(N.rich([("return min(r, g, b)", {"code": True}),
                   (" — After all houses processed, pick the terminal color with the lowest total cost.", {})])),
    N.callout("⚠️ Simultaneous update is CRITICAL. Never write r = cr+min(g,b) then g = cg+min(r,b) on separate lines — the second line would use the NEWLY computed r, which is wrong. Always use tuple assignment.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Memoization ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Memoization Top-Down"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Recursively: the cheapest way to paint house n−1 with color c = costs[n-1][c] + min(cheapest way to paint houses 0..n-2 with any non-c color). This has the structure of overlapping subproblems, which lru_cache handles automatically."),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without memoization recomputes dp(i, c) many times — once for each path that reaches state (i, c). With memoization, each (i, c) pair is computed exactly once."),
        N.h4("The Key Observation"),
        N.para("There are only 3n distinct (house, color) states. With caching, each state is solved in O(1) amortized time → O(n) total. The recursion naturally expresses the recurrence and is easier to derive from the problem statement."),
        N.h4("Building the Solution"),
        N.para("Define dp(i, c) = min cost for houses 0..i with house i = color c. Base case: dp(0, c) = costs[0][c]. Recurrence: dp(i, c) = costs[i][c] + min(dp(i-1, j) for j != c). Decorate with @lru_cache."),
        N.callout("Top-down is often easier to derive in interviews because it mirrors the problem definition directly. Bottom-up (tabulation) is more efficient in practice (no call stack overhead).", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — Memoize all (i, c) pairs. There are at most 3n unique pairs, so cache size is O(n).", {})])),
    N.para(N.rich([("def dp(i, c):", {"code": True}),
                   (" — Returns the minimum cost to paint houses 0..i with house i painted color c.", {})])),
    N.para(N.rich([("if i == 0: return costs[0][c]", {"code": True}),
                   (" — Base case: first house, no predecessor constraint.", {})])),
    N.para(N.rich([("costs[i][c] + min(dp(i-1, j) for j in range(3) if j != c)", {"code": True}),
                   (" — Recursive case: current cost plus the cheapest valid predecessor (any color ≠ c at the prior house).", {})])),
    N.para(N.rich([("return min(dp(n-1, c) for c in range(3))", {"code": True}),
                   (" — Try all three terminal colors, return the minimum.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all paths)", "O(3^n)", "O(n)"],
        ["Memoization (top-down)", "O(n)", "O(n)"],
        ["Tabulation + rolling vars ✓", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min of Other Colors", {})])),
    N.callout(
        "When to recognize this pattern: sequence of n items, each with a small fixed set of k choices, "
        "adjacent choices constrained (can't repeat), minimize/maximize total. "
        "Recurrence shape: dp[i][c] = cost[i][c] + min of OTHER choices from dp[i-1].",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (constrained adjacent DP / Min of Other Colors):"),
    N.bullet(N.rich([("Paint House II", {"bold": True}), (" (Hard) — k colors; O(n·k) with running-min + second-min trick instead of O(n·k²) naïve. #265", {})])),
    N.bullet(N.rich([("Paint Fence", {"bold": True}), (" (Medium) — n posts, k colors, at most 2 same-color adjacent; DP on (same, diff) state. #276", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}), (" (Medium) — binary constraint: rob or not; dp[i] = max(dp[i-2]+val, dp[i-1]). #198", {})])),
    N.bullet(N.rich([("House Robber II", {"bold": True}), (" (Medium) — circular arrangement; run two overlapping linear sub-problems. #213", {})])),
    N.bullet(N.rich([("Minimum Cost For Tickets", {"bold": True}), (" (Medium) — travel passes over days; DP with multi-day coverage windows. #983", {})])),
    N.bullet(N.rich([("Delete and Earn", {"bold": True}), (" (Medium) — reduces to house robber after value-counting; adjacent values excluded. #740", {})])),
    N.para("These problems share the core insight: at each step, the optimal decision depends on a bounded prior state, and selecting one choice restricts adjacent choices."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) · Sub-Pattern: Min of Other Colors", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("paint_house")),
    N.para(N.rich([("Step through the DP row by row — each step shows the decision panel with both color options and formulas. Use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — {len(blocks)} blocks appended to {PAGE_ID}")
