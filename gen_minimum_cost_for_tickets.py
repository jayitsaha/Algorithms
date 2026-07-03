"""gen_minimum_cost_for_tickets.py — Notion in-place update for LeetCode #983."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-818a-830c-c829cfac1d4a"
SLUG = "minimum_cost_for_tickets"

# ── 1) Set page properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=983,
    pattern="Dynamic Programming",
    subpatterns=["Min Across Passes"],
    tc="O(365)",
    sc="O(365)",
    key_insight="On travel days, dp[d]=min(cost+dp[d-k]) for k=1,7,30; non-travel days carry forward dp[d-1].",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────────────────
print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body blocks ─────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have a list of travel ", {}),
        ("days", {"code": True}),
        (" — specific days of the year on which you will travel. You are given three pass options: a ", {}),
        ("1-day pass", {"bold": True}),
        (" at ", {}),
        ("costs[0]", {"code": True}),
        (", a ", {}),
        ("7-day pass", {"bold": True}),
        (" at ", {}),
        ("costs[1]", {"code": True}),
        (", and a ", {}),
        ("30-day pass", {"bold": True}),
        (" at ", {}),
        ("costs[2]", {"code": True}),
        (". Passes cover consecutive days starting from the purchase date. Return the minimum money needed to cover every travel day.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("days=[1,4,6,7,8,20], costs=[2,7,15] → 11. Strategy: $2 daily on day 1; $7 weekly on day 4 (covers 4–10); $2 daily on day 20. Total = 2+7+2 = $11.", {})
    ])),
    N.divider()
]

# ── SOLUTION 1: Tabulation (Interview Pick) ──────────────────────────────────
TABULATION_CODE = """\
def mincostTickets(days: list[int], costs: list[int]) -> int:
    travel = set(days)          # O(1) membership lookup
    last = days[-1]             # Last travel day bounds our loop
    dp = [0] * (last + 1)      # dp[0] = 0 base case

    for d in range(1, last + 1):
        if d not in travel:
            dp[d] = dp[d - 1]              # Non-travel: carry forward
        else:
            dp[d] = min(
                costs[0] + dp[d - 1],              # 1-day pass
                costs[1] + dp[max(0, d - 7)],      # 7-day pass (reach back 7)
                costs[2] + dp[max(0, d - 30)]      # 30-day pass (reach back 30)
            )

    return dp[last]
"""

blocks += [
    N.h2("Solution 1 — Tabulation / Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each day, we're asking: what is the cheapest way to ensure I'm covered on all travel days up through today? We want to fill in this 'minimum cost so far' for every day from 1 to the last travel day."),
        N.h4("What Doesn't Work"),
        N.para("Greedy fails: buying the cheapest pass today ignores that a 7-day pass might be more economical if you travel 5 times this week. A brute-force recursion trying all combinations is exponential — 3 choices per travel day gives 3^T possibilities."),
        N.h4("The Key Observation"),
        N.para("Two types of days exist: travel days (must be covered; buy one of three passes) and non-travel days (no pass needed; cost identical to the previous day). On travel days, a k-day pass bought today covers today back to day d-k+1, so the prior cost we look at is dp[d-k]."),
        N.h4("Building the Solution"),
        N.para("1. Build a set of travel days for O(1) lookup. 2. Allocate dp[0..last] with dp[0]=0. 3. For each day d: if non-travel, dp[d]=dp[d-1]; if travel, dp[d]=min(costs[0]+dp[d-1], costs[1]+dp[max(0,d-7)], costs[2]+dp[max(0,d-30)]). 4. Return dp[last]."),
        N.callout("Analogy: Imagine you're buying subway passes for a year. On days you don't ride, you don't buy anything. On ride days, you compare: buy a day pass, a weekly, or a monthly — whichever is cheapest given what you've already spent.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("travel = set(days)", {"code": True}), (" — Converts the days list to a set for O(1) membership testing. Without this, d not in travel would be O(T) per check, making the overall loop O(365·T) instead of O(365).", {})])),
    N.para(N.rich([("last = days[-1]", {"code": True}), (" — The days array is sorted. The last element is the furthest travel day we need to cover. We only need to fill dp up to this index — non-travel days beyond it add nothing.", {})])),
    N.para(N.rich([("dp = [0] * (last + 1)", {"code": True}), (" — Allocates dp[0..last]. dp[0] = 0 is the base case: zero cost through day zero (no days). All other entries start at 0 but will be overwritten.", {})])),
    N.para(N.rich([("for d in range(1, last + 1):", {"code": True}), (" — Iterates every calendar day from 1 to last, inclusive. Both travel and non-travel days must be processed so dp lookbacks work correctly.", {})])),
    N.para(N.rich([("if d not in travel: dp[d] = dp[d - 1]", {"code": True}), (" — Non-travel day: no pass needed. The minimum cost through today is the same as through yesterday. This is the 'skip' transition.", {})])),
    N.para(N.rich([("dp[d] = min(costs[0] + dp[d-1], ...)", {"code": True}), (" — Travel day: evaluate all three pass options and take the minimum. This is the core DP transition.", {})])),
    N.para(N.rich([("costs[1] + dp[max(0, d - 7)]", {"code": True}), (" — The 7-day pass reach-back. If I buy a 7-day pass on day d, it covers days [d-6..d]. I only need to have paid for days through d-7. max(0,...) prevents negative indexing when d<7.", {})])),
    N.para(N.rich([("costs[2] + dp[max(0, d - 30)]", {"code": True}), (" — Same logic for the 30-day pass. Reaches back 30 days. max(0,...) clamps to dp[0]=0 when d<30.", {})])),
    N.para(N.rich([("return dp[last]", {"code": True}), (" — The answer: minimum cost to cover all travel days. Non-travel days carry forward, so dp[last] contains the correct answer.", {})])),
    N.divider()
]

# ── SOLUTION 2: Memoization (Top-Down) ─────────────────────────────────────
MEMO_CODE = """\
from functools import lru_cache

def mincostTickets(days: list[int], costs: list[int]) -> int:
    travel = set(days)

    @lru_cache(None)
    def dp(d: int) -> int:
        if d > days[-1]:
            return 0                   # Past last travel day: no more cost
        if d not in travel:
            return dp(d + 1)           # Non-travel: skip to next day
        return min(
            costs[0] + dp(d + 1),      # 1-day pass: skip 1 day forward
            costs[1] + dp(d + 7),      # 7-day pass: skip 7 days forward
            costs[2] + dp(d + 30)      # 30-day pass: skip 30 days forward
        )

    return dp(days[0])
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Easier to Derive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Starting from the first travel day, what is the minimum cost from day d onward? This is a natural recursive framing."),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without caching recomputes dp(d) every time it is reached by different recursive branches — exponential time."),
        N.h4("The Key Observation"),
        N.para("The recurrence goes forward: on day d, buying a k-day pass means the next decision point is day d+k. Non-travel days just advance by 1. With lru_cache, each day is computed exactly once."),
        N.h4("Building the Solution"),
        N.para("Define dp(d) = min cost from day d to end. Base: d > last → 0. Non-travel: dp(d+1). Travel: min(costs[0]+dp(d+1), costs[1]+dp(d+7), costs[2]+dp(d+30)). This is the 'forward scan' counterpart to the backward-looking tabulation."),
        N.callout("The memoized solution is often the one you derive first on paper — write the recursion, add @lru_cache, and it's done. Then translate to tabulation for the iterative version.", "💡", "green_background")
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(None)", {"code": True}), (" — Python's built-in memoization decorator. Caches the return value of dp(d) after the first call. Subsequent calls with the same d return instantly.", {})])),
    N.para(N.rich([("if d > days[-1]: return 0", {"code": True}), (" — Base case: past the last travel day, no more cost is incurred. This terminates the recursion.", {})])),
    N.para(N.rich([("if d not in travel: return dp(d + 1)", {"code": True}), (" — Skip non-travel day. No pass purchased; recurse to tomorrow. Cost is unchanged.", {})])),
    N.para(N.rich([("return min(costs[0]+dp(d+1), ...)", {"code": True}), (" — Travel day. Try all three passes. A k-day pass on day d means the next relevant decision is day d+k. Take the cheapest.", {})])),
    N.para(N.rich([("return dp(days[0])", {"code": True}), (" — Start from the first travel day. All days before it don't need coverage, so they contribute 0 cost.", {})])),
    N.divider()
]

# ── Why DP section ──────────────────────────────────────────────────────────
RECURRENCE = """\
# Recurrence Relations

# NON-TRAVEL DAY:
dp[d] = dp[d - 1]

# TRAVEL DAY:
dp[d] = min(
    costs[0] + dp[d - 1],           # 1-day pass
    costs[1] + dp[max(0, d - 7)],   # 7-day pass
    costs[2] + dp[max(0, d - 30)]   # 30-day pass
)

# Base case:
dp[0] = 0
"""

blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The minimum cost to cover all travel days through day d depends on the optimal costs through days d-1, d-7, and d-30. If those are solved optimally, we can extend them with one pass purchase decision.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Without memoization, dp(5) would be recomputed every time it's needed — once for a 1-day pass on day 6, once for a 7-day pass on day 12, etc. DP stores each dp[d] once — O(365) total work.", {})
    ])),
    N.para(N.rich([
        ("Why not Greedy? ", {"bold": True}),
        ("Greedy picks the cheapest pass right now without knowing whether you'll travel 4 more times this week. A 7-day pass might look expensive today but save money over a cluster of upcoming travel days. DP considers all future patterns implicitly via the recurrence.", {})
    ])),
    N.code(RECURRENCE),
    N.callout("The max(0, d-k) clamping is critical: when d < k, d-k is negative. In Python, dp[-4] accesses near the END of the array, giving wildly wrong values. max(0, ...) correctly represents 'the pass covers everything from the start, so prior cost is dp[0] = 0'.", "⚠️", "yellow_background"),
    N.divider()
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (no cache)", "O(3^T)", "O(T)", "Exponential — unusable"],
        ["Top-Down Memoization", "O(365)", "O(365)", "Each day computed once; natural derivation"],
        ["Bottom-Up Tabulation ✓", "O(365)", "O(365)", "Interview pick; iterative, no stack"],
        ["Sliding Window (30-day buffer)", "O(365)", "O(30)", "Space-optimized follow-up"]
    ]),
    N.divider()
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Across Passes (DP over Calendar / Timeline)", {})])),
    N.callout(
        "When to recognize this pattern: 'Minimum cost to cover events on a timeline' + 'multiple pass durations' + 'some days require action, others don't' + 'answer is a single value at end of 1D array'. The multi-duration lookback (dp[d-1], dp[d-7], dp[d-30]) is the signature of this sub-pattern.",
        "🔎", "green_background"
    ),
    N.para("*Note: 'Min Across Passes' is classified under the broader DP → Unbounded Knapsack family, specialized for timeline coverage with variable durations.*"),
    N.divider()
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DP with multi-duration reach-back or unbounded pass selection):"),
    N.bullet(N.rich([("Coin Change", {"bold": True}), (" (Medium) — dp[amount]=min(dp[amount-coin]+1) for each coin; same reach-back concept on amounts (#322)", {})])),
    N.bullet(N.rich([("Coin Change II", {"bold": True}), (" (Medium) — Count ways to make amount with unlimited coins; same unbounded knapsack structure (#518)", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}), (" (Medium) — Skip or rob; dp[i]=max(dp[i-1], dp[i-2]+nums[i]); two-step lookback (#198)", {})])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (Medium) — Minimum jumps to reach end; dp[i]=min jumps reaching index i (#45)", {})])),
    N.bullet(N.rich([("Video Stitching", {"bold": True}), (" (Medium) — Cover a range with minimum clips; direct structural analog to pass coverage (#1024)", {})])),
    N.bullet(N.rich([("Paint House", {"bold": True}), (" (Medium) — Minimum cost to paint n houses with 3 colors; dp[i][color]=min cost through house i (#256)", {})])),
    N.bullet(N.rich([("Word Break", {"bold": True}), (" (Medium) — dp[i]: can we segment s[:i] using dictionary words? Multi-length lookback (#139)", {})])),
    N.para("These problems share the core technique: at each position, evaluate dp[pos-k] for multiple durations k, taking the minimum (or max) plus a per-step cost."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18: Dynamic Programming. Sub-pattern: Min Across Passes.", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ──────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. See how dp[] fills day by day, and watch the decision panel show all three pass options at every travel day.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── 4) Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
