"""
Notion update script for: Number of Longest Increasing Subsequence (LC #673)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b5-8997-ed149b41f6da"
SLUG = "number_of_longest_increasing_subsequence"

print(f"Setting properties on {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=673,
    pattern="Dynamic Programming",
    subpatterns=["DP with Count", "LIS (Longest Increasing Subsequence)"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Augment classic LIS DP with a parallel count array; reset count on new best, accumulate on tie.",
    icon="🟡"
)
print("Properties set.")

print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

print("Building new body...")
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the number of longest strictly increasing subsequences.\n\n"
         "Example 1: nums = [1,3,5,4,7] → 2  (two LIS of length 4: [1,3,5,7] and [1,3,4,7])\n"
         "Example 2: nums = [2,2,2] → 3  (each element alone is a LIS of length 1)\n\n"
         "Constraints: 1 ≤ nums.length ≤ 2000, -10⁶ ≤ nums[i] ≤ 10⁶", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Tabulation ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up DP (Tabulation) · Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Classic Longest Increasing Subsequence (LIS) DP computes, for each index i, the length of the longest increasing subsequence ending at i. This problem adds a second question: how many distinct such subsequences achieve that maximum length? The reframe: maintain TWO parallel arrays — one for lengths, one for counts — updated simultaneously with the same nested loop."),

        N.h4("What Doesn't Work"),
        N.para("Brute force generates all 2ⁿ subsequences and filters for increasing ones — exponential, completely infeasible. Even if we only track the single LIS, that gives us the length but loses all information about how many paths achieve it. We need to explicitly count paths as we build the DP table."),

        N.h4("The Key Observation"),
        N.para("When extending from index j to index i (where nums[j] < nums[i]), every single LIS ending at j becomes a valid LIS ending at i (by appending nums[i]). So count[j] paths transfer to count[i]. The two cases: (A) if length[j]+1 is STRICTLY GREATER than the current best at i, we've found a new champion — RESET count[i] to count[j], discarding inferior paths. (B) if length[j]+1 TIES the current best, we ADD count[j] to count[i] — two independent families of paths both achieve the same maximum."),

        N.h4("Building the Solution"),
        N.para("1. Initialize both arrays to 1 (base case: each element alone).\n"
               "2. For each i from 1 to n−1 (outer loop): for each j < i where nums[j] < nums[i] (inner loop):\n"
               "   • If length[j]+1 > length[i] → length[i] = length[j]+1; count[i] = count[j]  (RESET)\n"
               "   • If length[j]+1 == length[i] → count[i] += count[j]  (ACCUMULATE)\n"
               "3. After both loops: max_len = max(length). Return sum(count[i] for i where length[i] == max_len)."),

        N.callout(
            "Analogy: Think of count[i] as the number of 'trains' arriving at station i. A new faster train (longer LIS via j) replaces all old trains. An equally-fast new route adds more trains on the same schedule.",
            "🚆", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code("""\
def findNumberOfLIS(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    length = [1] * n   # length[i]: LIS length ending at index i
    count  = [1] * n   # count[i]: number of such LIS of that length
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    # New best: reset count to inherit from j
                    length[i] = length[j] + 1
                    count[i]  = count[j]
                elif length[j] + 1 == length[i]:
                    # Tie: accumulate paths from j
                    count[i] += count[j]
    max_len = max(length)
    return sum(c for l, c in zip(length, count) if l == max_len)
"""),

    N.h3("Line by Line"),
    N.para(N.rich([("length = [1] * n  ", {"code": True}), (" — Every element alone is an LIS of length 1. This is the DP base case.", {})])),
    N.para(N.rich([("count  = [1] * n  ", {"code": True}), (" — There is exactly 1 way to form that solo-element LIS. Parallel base case.", {})])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), (" — Outer loop: fix i as the ending index of the LIS we are computing.", {})])),
    N.para(N.rich([("for j in range(i):", {"code": True}), (" — Inner loop: try every earlier index j as a possible predecessor in the LIS.", {})])),
    N.para(N.rich([("if nums[j] < nums[i]:", {"code": True}), (" — Strictly increasing condition: j can only precede i if its value is strictly smaller.", {})])),
    N.para(N.rich([("if length[j]+1 > length[i]:", {"code": True}), (" — Case A (new best): extending from j gives a strictly longer LIS at i.", {})])),
    N.para(N.rich([("length[i] = length[j]+1; count[i] = count[j]  ", {"code": True}), (" — RESET: the new best length replaces the old; all count[j] paths from j now serve as count[i].", {})])),
    N.para(N.rich([("elif length[j]+1 == length[i]:", {"code": True}), (" — Case B (tie): extending from j ties the current best at i.", {})])),
    N.para(N.rich([("count[i] += count[j]  ", {"code": True}), (" — ACCUMULATE: two independent families of paths both achieve the same maximum length at i.", {})])),
    N.para(N.rich([("max_len = max(length)  ", {"code": True}), (" — One pass to find the globally longest LIS length.", {})])),
    N.para(N.rich([("return sum(c for l,c in zip(length,count) if l==max_len)  ", {"code": True}), (" — Sum counts at all indices achieving max_len. DO NOT return count[n-1] alone — the longest LIS may end anywhere.", {})])),

    N.divider(),
]

# ── Solution 2 — Memoization ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down DP (Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same subproblem structure as the tabulation approach, but expressed recursively. Define dp(i) = (best_length, count) ending at index i. Recurse on all j < i where nums[j] < nums[i], aggregate results using the same two-case rule."),

        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes dp(j) every time it is needed as a sub-call — exponential redundancy since many indices share predecessors."),

        N.h4("The Key Observation"),
        N.para("With @lru_cache, each dp(i) is computed exactly once. The recursion naturally expresses the dependency: dp(i) depends on dp(j) for all j < i with nums[j] < nums[i]. The memoization table stores (length, count) pairs indexed by i."),

        N.callout("Top-down is often easier to derive directly from the recurrence relation. If you think in terms of 'what does the answer at i depend on?' the recursive form flows naturally.", "💡", "green_background"),
    ]),

    N.h3("Code"),
    N.code("""\
from functools import lru_cache

def findNumberOfLIS(nums: list[int]) -> int:
    n = len(nums)

    @lru_cache(maxsize=None)
    def dp(i: int):
        # Returns (best_length, count) for LIS ending at index i
        best_len, best_cnt = 1, 1
        for j in range(i):
            if nums[j] < nums[i]:
                l, c = dp(j)          # cached: O(1) after first call
                if l + 1 > best_len:
                    best_len, best_cnt = l + 1, c   # RESET
                elif l + 1 == best_len:
                    best_cnt += c                   # ACCUMULATE
        return best_len, best_cnt

    all_dp = [dp(i) for i in range(n)]
    max_len = max(l for l, _ in all_dp)
    return sum(c for l, c in all_dp if l == max_len)
"""),

    N.h3("Why DP Works Here"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The best LIS ending at i is built from the best LIS ending at some prior j (where nums[j] < nums[i]), plus element i. The optimum of the sub-problem (best (length, count) at j) feeds directly into the optimum at i.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("dp(j) is needed by every i > j where nums[j] < nums[i]. Without memoization, this creates O(2ⁿ) redundant recomputation. With memoization, each dp(i) is computed exactly once — O(n²) total.", {})
    ])),

    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                   "Time",      "Space"],
        ["Brute Force (all subsets)", "O(2ⁿ)",     "O(n)"],
        ["DP + Count (Tabulation) ✓", "O(n²)",     "O(n)"],
        ["DP + Count (Memoization)",  "O(n²)",     "O(n)"],
        ["Fenwick/Segment Tree",       "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP with Count, LIS (Longest Increasing Subsequence)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for 'number of ways to achieve the optimal' — extend any DP with a count array. "
        "(2) Problem mentions 'longest increasing subsequence' explicitly — classic LIS DP structure applies. "
        "(3) 'How many distinct paths to the best outcome' — dual arrays (value + count), same nested loop.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (LIS DP variants, count extensions):"),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), (" (Medium, #300) — The base problem; same nested loop, return max(length) only", {})])),
    N.bullet(N.rich([("Longest Continuous Increasing Subsequence", {"bold": True}), (" (Easy, #674) — Contiguous-only LIS; O(n) single-pass", {})])),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}), (" (Hard, #354) — 2D LIS; sort one dimension, apply LIS on the other", {})])),
    N.bullet(N.rich([("Largest Divisible Subset", {"bold": True}), (" (Medium, #368) — LIS with divisibility condition; includes path reconstruction", {})])),
    N.bullet(N.rich([("Longest Arithmetic Subsequence", {"bold": True}), (" (Medium, #1027) — DP with fixed-difference constraint; hash map per index", {})])),
    N.bullet(N.rich([("Delete Columns to Make Sorted III", {"bold": True}), (" (Hard, #960) — LIS applied to column ordering in a 2D grid", {})])),
    N.bullet(N.rich([("Minimum Number of Removals to Make Mountain Array", {"bold": True}), (" (Hard, #1671) — Bi-tonic LIS variant", {})])),
    N.para("These problems share the core LIS DP structure: define dp[i] as the optimal value ending at index i, fill using a nested j < i loop, aggregate results at the end."),
    N.callout("📚 Guide Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18: Dynamic Programming → Sub-pattern: DP: LIS (Longest Increasing Subsequence)", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
