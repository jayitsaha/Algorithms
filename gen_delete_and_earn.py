"""
gen_delete_and_earn.py
Regenerates the Notion page for Delete and Earn (#740) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813e-9cfd-e8ac46e9e8ad"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=740,
    pattern="Dynamic Programming",
    subpatterns=["Transform to House Robber"],
    tc="O(n + M)",
    sc="O(M)",
    key_insight="Taking value x deletes x±1 forever, so take all copies of x at once: this transforms to House Robber on sum[v]=v×count(v).",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
print("Wiping old blocks...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} blocks.")

# 3) Rebuild body
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("nums", {"code": True}),
        (". In one operation you may pick any value ", {}),
        ("x", {"code": True}),
        (", earn ", {}),
        ("x", {"code": True}),
        (" points, then all elements equal to ", {}),
        ("x−1", {"code": True}),
        (" and ", {}),
        ("x+1", {"code": True}),
        (" are permanently deleted. Repeat until empty. Return maximum total points.", {})
    ])),
    N.para("Example: nums = [3, 4, 2]. Taking 4 deletes all 3s and 5s (+4). Then taking 2 deletes all 1s and 3s (+2). Total = 6. Taking 3 instead would delete 2 and 4 and yield only 3."),
    N.divider(),
]

# Solution 1 — Tabulation (Interview Pick)
blocks += [
    N.h2("Solution 1 — Tabulation Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pick elements to delete, but the deletion rule entangles values. The key observation: if I take ANY copy of value x, the rule removes all x-1 and x+1 regardless. So there is no reason not to take ALL copies of x — they become free once we pay the adjacency penalty once."),
        N.h4("What Doesn't Work"),
        N.para("Greedy: taking the largest value first seems natural, but in [3,4,2] taking 4 (largest) only gives 4, while taking 2+4=6. Greedy ignores the combinatorial interplay between adjacent values."),
        N.h4("The Key Observation"),
        N.para("'Take all copies or none per value' means the problem lives on the value axis: define sum[v] = v × count(v). Now we must choose a subset of values 0..M with no two adjacent, maximizing sum. That is verbatim House Robber."),
        N.h4("Building the Solution"),
        N.para("Step 1: Build total[v] = v × count(v) in one pass over nums. Step 2: Run House Robber on total[] with two rolling variables prev2, prev1. Recurrence: curr = max(prev1, prev2 + total[v]). Return prev1 after processing all values."),
        N.callout("Analogy: Imagine values on a street of houses. Each house has a safe worth total[v] dollars. Rob a house → alarm triggers and neighboring houses (v-1, v+1) lock permanently. Grab all the cash in each house you choose to rob.", "🏠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def deleteAndEarn(nums):
    M = max(nums)                        # largest value; DP range = [0..M]
    total = [0] * (M + 1)               # total[v] = v * count(v)
    for n in nums:
        total[n] += n                    # add n each time; 3 threes -> total[3]=9
    if M == 1: return total[1]          # edge case
    prev2 = total[0]                    # dp[0]: best using only value 0
    prev1 = max(total[0], total[1])     # dp[1]: best using values 0 or 1
    for v in range(2, M + 1):
        curr = max(prev1, prev2 + total[v])   # skip v OR take all v's
        prev2, prev1 = prev1, curr             # roll the window
    return prev1                        # dp[M] = answer"""),
    N.h3("Line by Line"),
    N.para(N.rich([("M = max(nums)", {"code": True}), " — The largest value determines our DP table size. We'll build a sum array indexed 0..M."])),
    N.para(N.rich([("total = [0] * (M + 1)", {"code": True}), " — Each index v stores v × count(v), the total points earned by taking every copy of value v."])),
    N.para(N.rich([("total[n] += n", {"code": True}), " — Incrementally adds n for each occurrence, giving sum total over all copies of that value."])),
    N.para(N.rich([("prev2 = total[0]", {"code": True}), " — dp[0]: best earnings considering only value 0. Almost always 0 since 0 × count = 0."])),
    N.para(N.rich([("prev1 = max(total[0], total[1])", {"code": True}), " — dp[1]: should we take all 0s or all 1s? Take the better one."])),
    N.para(N.rich([("curr = max(prev1, prev2 + total[v])", {"code": True}), " — Core recurrence: skip v (keep prev1) vs take all v's (prev2 was dp[v-2], add sum[v])."])),
    N.para(N.rich([("prev2, prev1 = prev1, curr", {"code": True}), " — Roll window: discard oldest dp value; only last two are ever needed."])),
    N.para(N.rich([("return prev1", {"code": True}), " — After loop: prev1 holds dp[M], the maximum earnings over all values."])),
    N.callout("⚠️ Why total[n] += n, not += 1? We want the total POINTS earned from all copies of value n (n × count), not just the count of copies.", "⚠️", "yellow_background"),
    N.divider(),
]

# Solution 2 — Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same transform as Solution 1. The difference is execution order: instead of filling the DP table bottom-up, we express the recurrence recursively and let the cache handle memoization."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without caching recomputes dp(v-1) an exponential number of times — once from dp(v), once from dp(v+1), etc."),
        N.h4("The Key Observation"),
        N.para("With @lru_cache, each dp(v) is computed exactly once. The top-down call order is dp(M) → dp(M-1), dp(M-2) → ... → dp(1), dp(0). Same work, different traversal."),
        N.h4("Building the Solution"),
        N.para("After the same pre-processing, define a recursive function dp(v) with base cases dp(0) and dp(1), and decorate with @lru_cache. Call dp(M)."),
    ]),
    N.h3("Code"),
    N.code("""\
def deleteAndEarn(nums):
    M = max(nums)
    total = [0] * (M + 1)
    for n in nums:
        total[n] += n
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(v):
        if v == 0: return total[0]
        if v == 1: return max(total[0], total[1])
        return max(dp(v-1), dp(v-2) + total[v])
    return dp(M)"""),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Memoizes every call to dp(v). The cache stores results so each unique v is computed only once."])),
    N.para(N.rich([("dp(v)", {"code": True}), " — Returns the maximum earnings considering values 0 through v."])),
    N.para(N.rich([("return max(dp(v-1), dp(v-2) + total[v])", {"code": True}), " — Identical recurrence to tabulation: skip v or take it (must skip v-1)."])),
    N.callout("Top-down is easier to derive from the recurrence equation but has O(M) call stack depth. For very large M, tabulation is safer. Both give O(n + M) time.", "💡", "gray_background"),
    N.divider(),
]

# Why DP section (DP-specific requirement)
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}), "The best strategy for values 0..v decomposes into exactly two cases: skip v (best for 0..v-1) or take v (best for 0..v-2 + sum[v]). Knowing dp[v-1] and dp[v-2] is sufficient — no other history is needed."])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}), "A naive recursive solution recomputes dp[v-1] for every value that considers skipping down from higher indices. With n values from 0 to M, this leads to O(2^M) recomputation without memoization."])),
    N.code("# Recurrence:\n# sum[v]  = v × count(v)              (pre-processing)\n# dp[v]   = max(dp[v-1], dp[v-2] + sum[v])  (House Robber)\n#\n# Base cases:\n# dp[0] = sum[0]\n# dp[1] = max(sum[0], sum[1])"),
    N.para("The state is simply the current value index v. Each state is solved in O(1) using two previously computed states. Total: O(M) DP states × O(1) per state = O(M) time."),
    N.callout("State machine intuition: at each value v you make a binary decision — SKIP v (move to v+1 with same earnings) or TAKE v (move to v+1 after adding sum[v] and losing access to v-1). These are the only two transitions.", "🔀", "purple_background"),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsets)", "O(2^n)", "O(n)"],
        ["Memoization (top-down)", "O(n + M)", "O(M) + O(M) stack"],
        ["Tabulation (bottom-up) ✓", "O(n + M)", "O(M) total[]"],
    ]),
    N.para("n = len(nums), M = max(nums). The O(M) for total[] dominates for sparse inputs where M >> n."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Transform to House Robber (value-axis linear DP with adjacent exclusion)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Taking one instance of a value prevents taking adjacent values\n"
        "• Items can be bucketed (all copies of same value behave identically)\n"
        "• 'Maximize sum where no two adjacent values are both chosen'\n"
        "• The exclusion constraint is on values, not positions",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (House Robber / Linear DP):"),
    N.bullet(N.rich([("House Robber", {"bold": True}), " (Medium) — The exact same recurrence; dp[i] = max(dp[i-1], dp[i-2] + nums[i]). Core pattern. (#198)"])),
    N.bullet(N.rich([("House Robber II", {"bold": True}), " (Medium) — Circular variant: run House Robber twice excluding first or last element, take max. (#213)"])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), " (Medium) — House Robber on binary tree; each node returns a (take, skip) pair. (#337)"])),
    N.bullet(N.rich([("Paint House", {"bold": True}), " (Medium) — Multi-state linear DP; choose color per house avoiding same adjacent color. (#256)"])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — Non-adjacent max sum with a window of k; monotonic deque optimization. (#1696)"])),
    N.bullet(N.rich([("Coin Change 2", {"bold": True}), " (Medium) — Unbounded knapsack on values; related value-indexed DP. (#518)"])),
    N.para("These problems share the core House Robber recurrence: dp[i] = max(dp[i-1], dp[i-2] + value[i])."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), Sub-Pattern: Transform to House Robber", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("delete_and_earn")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
