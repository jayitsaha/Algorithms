"""
gen_min_cost_climbing_stairs.py
Regenerate Notion page for Min Cost Climbing Stairs (LC #746).
notion_page_id = None → create fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── 1. Create the page (notion_page_id was null) ────────────────────────────
PAGE_ID = N.create_page("Min Cost Climbing Stairs", 746, "Easy", "🟢")
print(f"Created page: {PAGE_ID}")

# ── 2. Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=746,
    pattern="Dynamic Programming",
    subpatterns=["Min of Two Predecessors"],
    tc="O(n)",
    sc="O(1)",
    key_insight="dp[i] = cost[i] + min(dp[i-1], dp[i-2]); answer = min(dp[-1], dp[-2]) since the top floor has no toll.",
    icon="🟢"
)
print("Properties set.")

# ── 3. Append body blocks ───────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("cost", {"code": True}),
        (" where ", {}),
        ("cost[i]", {"code": True}),
        (" is the cost of step ", {}),
        ("i", {"code": True}),
        (" on a staircase. Once you pay the cost you can climb either one or two steps. You can either start from the step with index ", {}),
        ("0", {"code": True}),
        (", or the step with index ", {}),
        ("1", {"code": True}),
        (". Return the minimum cost to reach the top of the floor (one step past the last index).", {})
    ])),
    N.divider(),
]

# ── Solution 1: Bottom-Up Tabulation O(1) ───────────────────────────────────
TABULATION_CODE = """\
def minCostClimbingStairs(cost):
    prev2 = cost[0]           # dp[0]: base case — start freely at stair 0
    prev1 = cost[1]           # dp[1]: base case — start freely at stair 1
    for i in range(2, len(cost)):
        curr = cost[i] + min(prev1, prev2)  # toll at i + cheapest predecessor
        prev2 = prev1         # slide window: old prev1 becomes new two-back
        prev1 = curr          # new curr becomes new one-back
    return min(prev1, prev2)  # top has no toll; exit from last or 2nd-to-last"""

blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation, O(1) Space (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the cheapest sequence of landings from start to the top. Each stair i can only be reached by jumping from stair i-1 (one step) or stair i-2 (two steps). The cheapest total cost to land on i is therefore: the toll at i plus the minimum of the cheapest way to land on i-1 or i-2."),
        N.h4("What Doesn't Work"),
        N.para("Greedy — always choosing the cheaper next step — fails because a cheap stair might funnel you into an expensive stair with no escape. You need to account for the full downstream impact of each choice, not just the immediate cost. Brute-force recursion works logically but recomputes identical sub-problems exponentially (O(2^n)), making it impractical for large inputs."),
        N.h4("The Key Observation"),
        N.para("Every stair has exactly two predecessors. The optimal path to stair i is fully determined by the optimal paths to stairs i-1 and i-2 — no other history matters. This is the optimal substructure property. Furthermore, dp(i) is called repeatedly in naive recursion from multiple callers — overlapping subproblems. Both conditions confirm DP."),
        N.h4("Building the Solution"),
        N.para("1. Define dp[i] = minimum total cost to step ON stair i (toll paid on landing, plus cumulative cost from the start). 2. Base cases: dp[0] = cost[0], dp[1] = cost[1] (start freely at either). 3. Recurrence: dp[i] = cost[i] + min(dp[i-1], dp[i-2]). 4. Answer: min(dp[n-1], dp[n-2]) — the top floor is a free exit, reached from the last or second-to-last stair. 5. Space optimization: since each step only looks back 2, two rolling variables replace the full array, dropping space from O(n) to O(1)."),
        N.callout("Analogy: Each stair is a toll booth. You always came from one of the two booths behind you. Pick whichever predecessor's accumulated tab is smaller, pay your booth, then move on.", "🧠", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The cheapest path to the top passes through stair n-1 or n-2. Each of those is itself a DP sub-problem of the same shape — the global optimum is built from local optima. ", {}),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("dp(5) would be computed by both dp(6) and dp(7) in naive recursion. Without caching the exponential blowup is O(2^n). DP ensures each state is computed exactly once.", {}),
    ])),
    N.code("""\
# Recurrence Relations
dp[0] = cost[0]
dp[1] = cost[1]
dp[i] = cost[i] + min(dp[i-1], dp[i-2])   # for i >= 2
answer = min(dp[n-1], dp[n-2])              # top floor has no toll"""),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("prev2 = cost[0]", {"code": True}), (" — dp[0] base case: cost of starting at stair 0, no prior stairs. This is the anchor for all future two-back lookups.", {})])),
    N.para(N.rich([("prev1 = cost[1]", {"code": True}), (" — dp[1] base case: cost of starting at stair 1. You can begin here for free; the toll is just cost[1] itself.", {})])),
    N.para(N.rich([("for i in range(2, len(cost)):", {"code": True}), (" — Iterate forward from stair 2 to the last stair, filling dp left to right.", {})])),
    N.para(N.rich([("curr = cost[i] + min(prev1, prev2)", {"code": True}), (" — Pay the toll at stair i, then add the cheaper of the two predecessor accumulated costs (prev1 = dp[i-1], prev2 = dp[i-2]).", {})])),
    N.para(N.rich([("prev2 = prev1", {"code": True}), (" — Slide the window: the old one-back becomes the new two-back. CRITICAL: do this BEFORE updating prev1, or you corrupt the window.", {})])),
    N.para(N.rich([("prev1 = curr", {"code": True}), (" — The freshly computed dp[i] becomes the new one-back for the next iteration.", {})])),
    N.para(N.rich([("return min(prev1, prev2)", {"code": True}), (" — The top floor has no toll. You exit from the last stair (prev1 = dp[n-1]) or the second-to-last (prev2 = dp[n-2]). Return the cheaper exit.", {})])),
    N.callout("⚠️  Swap order matters: prev2 = prev1 MUST come before prev1 = curr. Reversing the assignment silently overwrites prev1 with curr before prev2 can capture the old prev1 — a subtle bug that produces wrong results without any error message.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Top-Down Memoization ────────────────────────────────────────
MEMO_CODE = """\
from functools import lru_cache

def minCostClimbingStairs(cost):
    n = len(cost)

    @lru_cache(None)
    def dp(i):
        # Returns: minimum cost to have stepped ON stair i
        if i <= 1:
            return cost[i]     # base case: start freely at 0 or 1
        return cost[i] + min(dp(i - 1), dp(i - 2))

    return min(dp(n - 1), dp(n - 2))"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The memoization approach derives directly from the recurrence. Write the recursive definition literally: dp(i) = cost[i] + min(dp(i-1), dp(i-2)). Add an @lru_cache decorator to cache each (i,) call. Now every sub-problem is computed at most once, and the recursion tree collapses from O(2^n) to O(n) time and O(n) space."),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without the cache is O(2^n) — exponential in the number of stairs. The cache is the only thing that makes top-down efficient. Without it, dp(40) would require over a billion calls."),
        N.h4("The Key Observation"),
        N.para("Memoization and tabulation always produce the same answer — they are two implementations of the same recurrence. Memoization is lazily evaluated (only computes what is actually called), while tabulation eagerly fills every cell. For this problem all cells are needed anyway, so both are O(n)."),
        N.h4("Building the Solution"),
        N.para("1. Define the recursive function dp(i) with the same recurrence. 2. Add @lru_cache(None) to auto-memoize. 3. Call min(dp(n-1), dp(n-2)) as the answer. The cache handles everything else automatically."),
        N.callout("Memoization is often the easiest approach to derive in an interview since it is a direct translation of the recurrence. Propose it first, then offer to convert to bottom-up for O(1) space.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(None)", {"code": True}), (" — Python decorator that caches the return value of dp(i) keyed by the argument i. The first call to dp(5) computes and stores the result; all subsequent calls to dp(5) immediately return the cached value.", {})])),
    N.para(N.rich([("if i <= 1: return cost[i]", {"code": True}), (" — Base cases: dp(0) = cost[0], dp(1) = cost[1]. These are the recursion terminators; without them the function would recurse infinitely.", {})])),
    N.para(N.rich([("return cost[i] + min(dp(i-1), dp(i-2))", {"code": True}), (" — The recurrence: pay toll at i, add the minimum of the two predecessor costs. lru_cache ensures each dp(k) is computed once regardless of how many callers request it.", {})])),
    N.para(N.rich([("return min(dp(n-1), dp(n-2))", {"code": True}), (" — Same exit logic as tabulation: minimum of the last two stairs (the top floor is toll-free).", {})])),
    N.divider(),
]

# ── Complexity table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Recursion", "O(2^n)", "O(n) stack"],
        ["Memoization (top-down)", "O(n)", "O(n) cache + stack"],
        ["Tabulation O(1) — Interview Pick", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min of Two Predecessors (1-D DP)", {})])),
    N.callout(
        "When to recognize this pattern: Linear sequence + each element reachable from 1 or 2 prior positions + optimization goal (min/max) that accumulates along the path + Fibonacci-shaped dependency (dp[i] depends on exactly dp[i-1] and dp[i-2]) + no branching state required.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Min of Two Predecessors / 1-D DP technique:"),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}), (" (Easy) — Count paths (pure Fibonacci); same structure without costs. LeetCode #70", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}), (" (Medium) — Max sum with no adjacent picks; dp[i] = max(dp[i-1], dp[i-2]+nums[i]) — same two-predecessor shape. LeetCode #198", {})])),
    N.bullet(N.rich([("House Robber II", {"bold": True}), (" (Medium) — Circular array; run the same recurrence twice: once excluding the first element, once excluding the last. LeetCode #213", {})])),
    N.bullet(N.rich([("Delete and Earn", {"bold": True}), (" (Medium) — Transform to House Robber after bucketing each value's total points. LeetCode #740", {})])),
    N.bullet(N.rich([("Fibonacci Number", {"bold": True}), (" (Easy) — The pure dependency structure without any cost layer; same O(1) rolling window. LeetCode #509", {})])),
    N.bullet(N.rich([("Jump Game", {"bold": True}), (" (Medium) — Reachability variant; greedy works but DP provides a clean mental model. LeetCode #55", {})])),
    N.para("These problems all share the core template: dp[i] references dp[i-1] and dp[i-2], enabling O(1) space with two rolling variables."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18.1 (Dynamic Programming → 1-D Dynamic Programming). Sub-Pattern verified as 'Min of Two Predecessors' via guide + analysis.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("min_cost_climbing_stairs")),
    N.para(N.rich([
        ("Step through the DP table fill visually — use Next/Prev or arrow keys. Each step shows the decision panel (which predecessor wins), variable tracker, and active code line.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"PAGE_ID={PAGE_ID}")
