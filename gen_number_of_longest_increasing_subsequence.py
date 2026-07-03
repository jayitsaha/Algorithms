"""
Notion regeneration script for:
  LeetCode #673 — Number of Longest Increasing Subsequence
  Pattern: Dynamic Programming
  Sub-Pattern: DP with Count (extends DP: LIS)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81b5-8997-ed149b41f6da"
SLUG    = "number_of_longest_increasing_subsequence"

# ── Step 1: Set page properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 673,
    pattern     = "Dynamic Programming",
    subpatterns = ["DP with Count"],
    tc          = "O(n^2)",
    sc          = "O(n)",
    key_insight = "Extend LIS DP with a parallel count array: reset count on new best length, accumulate count on tie.",
    icon        = "\U0001f7e1",
)
print("Properties OK.")

# ── Step 2: Wipe old body ─────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── Step 3: Rebuild body ──────────────────────────────────────────────────────

TABULATION_CODE = """\
def findNumberOfLIS(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    length = [1] * n   # length[i] = LIS length ending at i
    count  = [1] * n   # count[i]  = # of such LIS

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    # Found strictly longer path via j: RESET
                    length[i] = length[j] + 1
                    count[i]  = count[j]
                elif length[j] + 1 == length[i]:
                    # Tied: ACCUMULATE
                    count[i] += count[j]

    max_len = max(length)
    return sum(c for l, c in zip(length, count) if l == max_len)
"""

MEMO_CODE = """\
from functools import lru_cache

def findNumberOfLIS(nums: list[int]) -> int:
    n = len(nums)

    @lru_cache(maxsize=None)
    def dp(i: int):
        # Returns (best_length, count) for LIS ending at index i
        best_len, best_cnt = 1, 1
        for j in range(i):
            if nums[j] < nums[i]:
                sub_len, sub_cnt = dp(j)
                if sub_len + 1 > best_len:
                    best_len, best_cnt = sub_len + 1, sub_cnt
                elif sub_len + 1 == best_len:
                    best_cnt += sub_cnt
        return best_len, best_cnt

    all_dp  = [dp(i) for i in range(n)]
    max_len = max(l for l, _ in all_dp)
    return sum(c for l, c in all_dp if l == max_len)
"""

RECURRENCE = """\
Base case:  length[i] = 1,  count[i] = 1  for all i

For each j < i where nums[j] < nums[i]:

  Case A: strictly better path through j
    if length[j] + 1 > length[i]:
        length[i] = length[j] + 1
        count[i]  = count[j]         <- RESET (old paths now suboptimal)

  Case B: equally long path through j (a tie)
    elif length[j] + 1 == length[i]:
        count[i] += count[j]         <- ACCUMULATE (more ways to reach same length)

Answer = sum( count[i] for all i where length[i] == max(length) )
"""

blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an integer array ",
        ("nums", {"code": True}),
        ", return the number of longest strictly increasing subsequences. "
        "A subsequence is formed by choosing elements from the array in their "
        "original relative order (not necessarily contiguous), such that each "
        "chosen value is strictly greater than the previous one. "
        "For example, nums = [1, 3, 5, 4, 7] has answer 2 because both "
        "[1, 3, 5, 7] and [1, 3, 4, 7] are longest increasing subsequences of length 4."
    ])),
    N.divider(),
]

# ── Solution 1 — Tabulation ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up DP (Tabulation) — Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need two facts for every index i simultaneously: (1) the length of the "
            "longest strictly increasing subsequence that ends exactly at position i, and "
            "(2) how many distinct such subsequences of that maximum length exist. "
            "Classic LIS only tracks (1). We add (2) with a parallel count array."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The O(n log n) patience-sorting LIS (binary search on a tails array) gives "
            "the global LIS length but discards per-position count information. "
            "We cannot extend it to count solutions without fundamentally restructuring it. "
            "Brute force over all 2^n subsequences is correct but exponential."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The classic O(n^2) LIS DP is easily extended. Instead of one array dp[i] = length, "
            "we maintain two: length[i] = best LIS length ending at i, and count[i] = number of "
            "distinct LIS of that best length ending at i. The nested loop structure is identical; "
            "we just add a two-case rule for updating count alongside length."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize both arrays to 1. For outer i from 1 to n-1, inner j from 0 to i-1: "
            "if nums[j] < nums[i], check if length[j]+1 beats or ties length[i]. "
            "On a new best: update length, RESET count = count[j]. "
            "On a tie: ACCUMULATE count += count[j]. "
            "After loops: sum count[i] over all i with maximum length."
        ),
        N.callout(
            "Analogy: Imagine tracking the best running route to each city on a road network. "
            "Each city stores both the shortest distance and the number of shortest-path routes. "
            "When a new route is strictly shorter: replace the distance, reset the count. "
            "When it ties the current best: keep the distance, add to the count.",
            "🧠", "blue_background"
        ),
    ]),
    N.h4("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        "The best LIS ending at i is built by extending the best LIS ending at some earlier j. "
        "The sub-answer (length[j], count[j]) feeds directly into the main answer (length[i], count[i])."
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        "Many positions i look back at the same j. Without memoization, naive recursion "
        "recomputes the same dp(j) repeatedly across all i > j. Storing results lets each position "
        "be solved exactly once."
    ])),
    N.h4("Recurrence Relations"),
    N.code(RECURRENCE, lang="python"),
    N.h3("Code"),
    N.code(TABULATION_CODE, lang="python"),
    N.h3("Line by Line"),
    N.para(N.rich([("length = [1] * n", {"code": True}), " — Base case: every element forms a LIS of length 1 by itself."])),
    N.para(N.rich([("count = [1] * n", {"code": True}), " — Base case: there is exactly 1 way to form a single-element LIS."])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), " — Outer loop: fix the ending index i and compute the best LIS ending exactly at i."])),
    N.para(N.rich([("for j in range(i):", {"code": True}), " — Inner loop: try every previous index j as a predecessor."])),
    N.para(N.rich([("if nums[j] < nums[i]:", {"code": True}), " — Strictly increasing check: can only extend an LIS ending at j by appending nums[i] if nums[j] < nums[i]."])),
    N.para(N.rich([("if length[j]+1 > length[i]:", {"code": True}), " — Case A: path through j is strictly longer than the best seen so far for i."])),
    N.para(N.rich([("length[i] = length[j]+1; count[i] = count[j]", {"code": True}), " — RESET: update length to new best, replace count with count[j] (discard all shorter paths)."])),
    N.para(N.rich([("elif length[j]+1 == length[i]:", {"code": True}), " — Case B: another path of equal optimal length — a tie!"])),
    N.para(N.rich([("count[i] += count[j]", {"code": True}), " — ACCUMULATE: add count[j] ways to count[i] (both sets of paths are optimal)."])),
    N.para(N.rich([("max_len = max(length)", {"code": True}), " — Find the globally maximum LIS length across all positions."])),
    N.para(N.rich([("return sum(c for l,c in ...)", {"code": True}), " — Sum count[i] for all i where length[i] equals the global max. Do not return count[n-1] alone!"])),
    N.callout(
        "Critical bug to avoid: returning count[n-1] alone. The LIS may end at ANY index, "
        "not just the last element. Always collect from all indices achieving the maximum length.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Memoization ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down DP (Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp(i) recursively as: the (best_length, count) pair for longest increasing "
            "subsequences ending at index i. This maps directly to the recurrence — base case "
            "returns (1, 1), recursive case tries all valid predecessors."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive recursion without caching recomputes dp(j) for the same j from many different "
            "parents i > j, causing exponential time in the worst case."
        ),
        N.h4("The Key Observation"),
        N.para(
            "With lru_cache, each dp(i) is computed exactly once and its result cached. "
            "Total work is n unique subproblems × O(n) work each = O(n^2). "
            "Same asymptotic complexity as tabulation, but follows the recursive definition directly."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Decorate dp(i) with @lru_cache. Inside, start with (best_len, best_cnt) = (1, 1). "
            "For each valid j, call dp(j) (cached), apply the same reset/accumulate logic. "
            "Trigger all dp(i) calls, then aggregate."
        ),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE, lang="python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Memoization: caches dp(i) result keyed by i; future calls with same i return cached value in O(1)."])),
    N.para(N.rich([("def dp(i):", {"code": True}), " — Returns (best_length, count) for the longest increasing subsequence ending exactly at index i."])),
    N.para(N.rich([("best_len, best_cnt = 1, 1", {"code": True}), " — Base case: each element alone forms a length-1 LIS, exactly 1 way."])),
    N.para(N.rich([("sub_len, sub_cnt = dp(j)", {"code": True}), " — Recursive call (memoized): get optimal (length, count) for LIS ending at j."])),
    N.para(N.rich([("if sub_len + 1 > best_len:", {"code": True}), " — Found strictly better path through j: update length, reset count."])),
    N.para(N.rich([("elif sub_len + 1 == best_len:", {"code": True}), " — Tied path through j: accumulate count."])),
    N.para(N.rich([("all_dp = [dp(i) for i in range(n)]", {"code": True}), " — Force computation of all n subproblems (each computed once due to caching)."])),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                        "Time",      "Space"],
        ["Brute Force (all subsequences)",  "O(2^n)",    "O(n)"],
        ["DP Tabulation (Interview Pick)",  "O(n^2)",    "O(n)"],
        ["DP Memoization",                  "O(n^2)",    "O(n) + stack"],
        ["Segment Tree / BIT",              "O(n log n)","O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP with Count (extends the DP: LIS sub-pattern)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'How many ways to achieve the optimal?' — run a parallel count array. "
        "(2) Problem is LIS or a variant, and asks for count of optimal subsequences. "
        "(3) 'Count distinct paths/sequences satisfying a condition' with an optimization objective.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique or closely related pattern:"),
    N.bullet(N.rich([
        ("Longest Increasing Subsequence", {"bold": True}),
        " (Medium) — Base LIS problem: same loop, one array, return max(length). LC #300."
    ])),
    N.bullet(N.rich([
        ("Russian Doll Envelopes", {"bold": True}),
        " (Hard) — 2D LIS: sort, then run LIS on heights. LC #354."
    ])),
    N.bullet(N.rich([
        ("Largest Divisible Subset", {"bold": True}),
        " (Medium) — LIS with divisibility condition plus path reconstruction. LC #368."
    ])),
    N.bullet(N.rich([
        ("Distinct Subsequences", {"bold": True}),
        " (Hard) — Count subsequences matching a target; 2D count DP. LC #115."
    ])),
    N.bullet(N.rich([
        ("Unique Paths", {"bold": True}),
        " (Medium) — Simpler 'DP with Count' in a grid. LC #62."
    ])),
    N.bullet(N.rich([
        ("Longest Arithmetic Subsequence", {"bold": True}),
        " (Medium) — LIS variant with fixed difference; hash map per index. LC #1027."
    ])),
    N.bullet(N.rich([
        ("Delete Columns to Make Sorted III", {"bold": True}),
        " (Hard) — LIS applied to column ordering. LC #960."
    ])),
    N.para(
        "These problems all share the core technique: DP where each state tracks "
        "both an optimal value AND a count of ways to achieve that optimum."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming, DP: LIS). "
        "Sub-Pattern: DP with Count. Source: Guide Section 18 + Analysis.",
        "📚", "gray_background"
    ),
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Upload ────────────────────────────────────────────────────────────────────
print(f"Uploading {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
