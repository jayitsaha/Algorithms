"""gen_split_array_largest_sum.py — Notion page rebuild for LC #410."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8184-8621-d8087eedf6c5"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=410,
    pattern="Binary Search",
    subpatterns=["Binary Search on Sum"],
    tc="O(n log S)",
    sc="O(1)",
    key_insight="Binary search on the answer: feasibility check (greedy scan) in O(n), search range [max(nums), sum(nums)].",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ─────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", split ", {}),
        ("nums", {"code": True}),
        (" into ", {}),
        ("k", {"code": True}),
        (" non-empty contiguous subarrays such that the largest subarray sum is minimized. Return the minimized largest sum.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [7,2,5,10,8], k = 2  →  18", {"code": True}),
        ("  (optimal split: [7,2,5] | [10,8], sums 14 and 18, largest = 18).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Binary Search on the Answer ────────────────────────────────
blocks += [
    N.h2("Solution 1 — Binary Search on the Answer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have n numbers and k−1 allowed cut-points. Choosing which k−1 positions to cut is a combinatorial problem with C(n−1, k−1) possibilities — exponential. Instead of trying all splits, ask: 'For a given budget limit X, is it possible to split into ≤ k pieces with every piece summing to ≤ X?' This yes/no question is O(n) to answer."),
        N.h4("What Doesn't Work"),
        N.para("Brute force over all split positions is exponential. Dynamic programming is O(n²k) — too slow for n up to 1000 and k up to 50. We need O(n log S)."),
        N.h4("The Key Observation"),
        N.para("The function feasible(X) is monotone: if a limit X works, then X+1 also works (a looser limit can only make splitting easier). If X fails, X−1 also fails. This monotone step-function property means binary search converges to the exact minimum feasible X in O(log(sum−max)) iterations."),
        N.h4("Building the Solution"),
        N.para("Set lo = max(nums) (tightest valid lower bound) and hi = sum(nums) (guaranteed feasible upper bound). Binary search: for each mid, run a greedy O(n) feasibility check (extend each piece as far as possible; cut when adding the next element would exceed mid). If feasible, narrow hi = mid; else lo = mid + 1. When lo == hi, return lo."),
        N.callout("Analogy: imagine allocating tasks to k workers to minimize the slowest worker's load. You'd binary search on 'what if the slowest worker handles at most X units?' and check greedily if k workers suffice.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def splitArray(nums: list[int], k: int) -> int:
    def feasible(limit: int) -> bool:
        pieces, curr = 1, 0
        for num in nums:
            if curr + num > limit:
                pieces += 1
                curr = 0
                if pieces > k:
                    return False
            curr += num
        return True

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def splitArray(nums, k)", {"code": True}), (" — outer function takes the array and number of pieces.", {})])),
    N.para(N.rich([("def feasible(limit)", {"code": True}), (" — inner helper; O(n) greedy check: 'can we split using ≤ k pieces with each sum ≤ limit?'", {})])),
    N.para(N.rich([("pieces, curr = 1, 0", {"code": True}), (" — start counting from 1 piece (we've already begun one), running sum = 0.", {})])),
    N.para(N.rich([("if curr + num > limit", {"code": True}), (" — adding this element would exceed the budget; must start a new piece.", {})])),
    N.para(N.rich([("pieces += 1; curr = 0", {"code": True}), (" — increment piece count, reset running sum. The element will go into the new piece.", {})])),
    N.para(N.rich([("if pieces > k: return False", {"code": True}), (" — early exit: even greedy needs more than k pieces, so this limit is infeasible.", {})])),
    N.para(N.rich([("curr += num", {"code": True}), (" — add the element to the current piece's running sum.", {})])),
    N.para(N.rich([("lo, hi = max(nums), sum(nums)", {"code": True}), (" — search bounds: tightest possible answer (must hold max element) to loosest (one piece).", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — candidate for 'largest allowed subarray sum'.", {})])),
    N.para(N.rich([("hi = mid", {"code": True}), (" — feasible: answer is ≤ mid (keep mid as candidate, narrow from above).", {})])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), (" — infeasible: mid is too tight, must search higher.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — when lo == hi, both converge to the minimum feasible limit. That's the answer.", {})])),
    N.divider(),
]

# ── Solution 2: DP ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Dynamic Programming O(n²k)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("dp[i][j] = minimum possible 'largest sum' when splitting the first i elements into exactly j pieces. The answer is dp[n][k]."),
        N.h4("What Doesn't Work"),
        N.para("Brute force enumerates all split points. DP avoids re-computation of overlapping subproblems, but is still O(n²k) — practical for small n and k only."),
        N.h4("The Key Observation"),
        N.para("For dp[i][j], try all possible last-piece boundaries m (from j-1 to i-1). The last piece sums nums[m..i-1] (via prefix sum in O(1)). dp[i][j] = min over m of max(dp[m][j-1], sum(nums[m..i-1]))."),
        N.h4("Building the Solution"),
        N.para("Precompute prefix sums for O(1) range queries. Fill dp bottom-up: for each (i, j), try every split point m for the last piece. O(n²k) total. Use this to understand the problem structure, then use binary search for large inputs."),
    ]),
    N.h3("Code"),
    N.code(
"""def splitArray_dp(nums: list[int], k: int) -> int:
    n = len(nums)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    INF = float('inf')
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        for j in range(1, k + 1):
            for m in range(j - 1, i):
                last_sum = pre[i] - pre[m]
                dp[i][j] = min(dp[i][j], max(dp[m][j - 1], last_sum))

    return dp[n][k]""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("pre[i+1] = pre[i] + nums[i]", {"code": True}), (" — prefix sum so range sum nums[m..i-1] = pre[i] - pre[m] in O(1).", {})])),
    N.para(N.rich([("dp[i][j]", {"code": True}), (" — minimum 'largest sum' for first i elements split into j pieces.", {})])),
    N.para(N.rich([("dp[0][0] = 0", {"code": True}), (" — base case: 0 elements, 0 pieces, cost = 0.", {})])),
    N.para(N.rich([("for m in range(j-1, i)", {"code": True}), (" — try all possible last-piece starting points m. At least j-1 elements must be in the first j-1 pieces.", {})])),
    N.para(N.rich([("max(dp[m][j-1], last_sum)", {"code": True}), (" — the worst-case (largest) sum for this split is the max of the previous best and the new last piece.", {})])),
    N.para(N.rich([("return dp[n][k]", {"code": True}), (" — minimum largest sum for all n elements in k pieces.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all splits)", "O(C(n,k))", "O(k)"],
        ["DP (tabulation)", "O(n²k)", "O(nk)"],
        ["Binary Search on Answer ✓", "O(n log S)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search on Sum (Binary Search on Answer)", {})])),
    N.callout(
        "When to recognize this pattern: 'Minimise the maximum' or 'maximise the minimum' — "
        "split/allocate k groups/workers/days — answer is a number in a known range — "
        "feasibility check on the answer is O(n) greedy — monotone feasibility property holds.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Binary Search on Answer / Binary Search on Sum technique:"),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — minimise ship capacity so all packages ship in D days; identical feasibility check (#1011)", {})])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — minimise eating speed so Koko finishes H hours; same bisect-left + greedy check (#875)", {})])),
    N.bullet(N.rich([("Minimum Number of Days to Make m Bouquets", {"bold": True}), (" (Medium) — binary search on the day; O(n) feasibility scan (#1482)", {})])),
    N.bullet(N.rich([("Find the Smallest Divisor Given a Threshold", {"bold": True}), (" (Medium) — binary search on divisor; check ceiling-sum ≤ threshold (#1283)", {})])),
    N.bullet(N.rich([("Minimize Max Distance to Gas Station", {"bold": True}), (" (Hard) — BS on floating-point answer for minimising max gap (#774)", {})])),
    N.bullet(N.rich([("Painter's Partition Problem", {"bold": True}), (" (Hard) — k painters, n boards: minimise slowest painter's time — classic equivalent", {})])),
    N.bullet(N.rich([("Book Allocation (GFG)", {"bold": True}), (" (Hard) — m students, books: minimise max pages per student — same BS + greedy template", {})])),
    N.para("These problems all share the same core technique: binary search over the answer space with a greedy O(n) feasibility check leveraging a monotone property."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search. Sub-Pattern: Binary Search on Sum.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("split_array_largest_sum")),
    N.para(N.rich([("Step through the binary search on the answer visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
