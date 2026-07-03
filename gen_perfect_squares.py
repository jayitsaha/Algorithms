"""
Notion page regeneration for Perfect Squares (LeetCode #279).
Runs in-place on existing page: 39193418-809c-8138-b0f8-f85c1b21a0b7
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8138-b0f8-f85c1b21a0b7"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=279,
    pattern="Dynamic Programming",
    subpatterns=["Unbounded Knapsack (Min squares summing to n)"],
    tc="O(n√n)",
    sc="O(n)",
    key_insight="Treat perfect squares as reusable coins; dp[i] = min(dp[i-s²]+1) for all s² ≤ i",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
print("Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────
print("Rebuilding page body...")

TABULATION_CODE = '''\
def numSquares(n: int) -> int:
    dp = [float('inf')] * (n + 1)   # dp[i] = min squares summing to i
    dp[0] = 0                        # base: 0 squares needed for 0
    for i in range(1, n + 1):
        s = 1
        while s * s <= i:            # try every perfect square ≤ i
            dp[i] = min(dp[i], dp[i - s*s] + 1)   # use one s², solve rest
            s += 1
    return dp[n]
'''

MEMOIZATION_CODE = '''\
from functools import lru_cache

def numSquares(n: int) -> int:
    @lru_cache(maxsize=None)
    def dp(rem):
        if rem == 0:
            return 0
        best = float('inf')
        s = 1
        while s * s <= rem:
            best = min(best, dp(rem - s*s) + 1)
            s += 1
        return best
    return dp(n)
'''

BRUTE_FORCE_CODE = '''\
def numSquares_brute(n: int) -> int:
    """Exponential — for illustration only. DO NOT submit."""
    def rec(rem):
        if rem == 0:
            return 0
        best = float('inf')
        s = 1
        while s * s <= rem:
            best = min(best, rec(rem - s*s) + 1)   # recomputes same sub-targets!
            s += 1
        return best
    return rec(n)
'''

blocks = []

# ── Problem ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (", return the minimum number of perfect square numbers that sum to ", {}),
        ("n", {"code": True}),
        (". A perfect square is an integer that is the square of an integer: 1, 4, 9, 16, …", {}),
    ])),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ("n = 12 → ", {"code": True}),
            ("3", {}),
            ("  (4 + 4 + 4 = 12)\n", {}),
            ("Example 2: ", {"bold": True}),
            ("n = 13 → ", {"code": True}),
            ("2", {}),
            ("  (4 + 9 = 13)", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Tabulation DP ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of perfect squares {1, 4, 9, 16, …} as coin denominations and n as the target amount. "
               "We want the minimum number of coins to exactly reach n, where each denomination can be used "
               "as many times as needed. This is Coin Change with a specific coin set."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always pick the largest square ≤ remaining) fails. For n=12: greedy picks 9, "
               "then 1+1+1 → 4 squares. But 4+4+4=12 uses only 3. Greedy's local best leads to a globally "
               "suboptimal result. We need to explore all choices."),
        N.h4("The Key Observation"),
        N.para("Two DP pillars: (1) Optimal Substructure — the minimum squares for n depends on optimal "
               "answers for n-s². (2) Overlapping Subproblems — naïve recursion recomputes dp[8] dozens "
               "of times (needed for dp[9], dp[12], dp[17], ...). Building bottom-up or memoizing eliminates this."),
        N.h4("Building the Solution"),
        N.para("Define dp[i] = minimum squares summing to i. Base: dp[0]=0. "
               "Recurrence: dp[i] = min(dp[i−s²]+1) for all s with s²≤i. "
               "Fill bottom-up i=1..n. For each i, try all squares 1², 2², ... up to floor(√i)²."),
        N.callout(
            "Analogy: Coin Change with coins={1,4,9,16,...}. dp[0]=0 is the empty register. "
            "Each coin (square) we 'insert' adds 1 to the count. We minimize total coins inserted.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Why Is This DP? The Two Pillars"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("If the optimal solution for n uses square s² as the last square, "
         "then the remaining n−s² must also be solved optimally. "
         "We can't do better by solving the subproblem suboptimally.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("dp[8] is needed when computing dp[9] (via 1), dp[12] (via 4), dp[17] (via 9), "
         "dp[24] (via 16) — all reuse the same precomputed value. Without caching, "
         "this causes exponential redundancy.", {}),
    ])),
    N.code(
        "# Recurrence Relation\n"
        "dp[0] = 0\n"
        "dp[i] = min(dp[i - s*s] + 1)\n"
        "        for all s = 1, 2, 3, ...  where s*s <= i\n\n"
        "# Perfect squares to try for target i:\n"
        "# s=1 → s²=1,  s=2 → s²=4,  s=3 → s²=9,  s=4 → s²=16, ...",
        "python"
    ),
    N.h3("Code"),
    N.code(TABULATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [float('inf')] * (n + 1)", {"code": True}),
                   ("  — Create array of size n+1, all initialized to infinity (unreached). "
                    "We're minimizing, so infinity is our 'worst case before any update.'", {})])),
    N.para(N.rich([("dp[0] = 0", {"code": True}),
                   ("  — Base case anchor: 0 squares needed to reach sum = 0. "
                    "Every valid chain of recurrences terminates here.", {})])),
    N.para(N.rich([("for i in range(1, n + 1):", {"code": True}),
                   ("  — Outer loop: target values from 1 up to n (inclusive). "
                    "Each iteration finalizes dp[i] exactly.", {})])),
    N.para(N.rich([("s = 1", {"code": True}),
                   ("; ", {}),
                   ("while s * s <= i:", {"code": True}),
                   ("  — Inner loop: try each perfect square s²=1,4,9,16,... as long as it doesn't exceed target i.", {})])),
    N.para(N.rich([("dp[i] = min(dp[i], dp[i - s*s] + 1)", {"code": True}),
                   ("  — Core recurrence: if we use one copy of s², the remainder is i−s². "
                    "dp[i−s²] was already finalized (it's smaller than i). Add 1 for the square we just used. "
                    "Take minimum over all tried squares.", {})])),
    N.para(N.rich([("return dp[n]", {"code": True}),
                   ("  — After filling dp[1..n] in order, dp[n] is the exact minimum.", {})])),
    N.callout(
        "⚠️ Why float('inf') not 0? We minimize — infinity means 'no valid combination found yet.' "
        "Any real path produces a finite count that replaces it. If we used 0, every cell would appear "
        "'solved' immediately — wrong! Only dp[0] = 0 is genuinely zero.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization DP"),
    N.toggle_h3("💡 Intuition: Same Recurrence, Recursive Derivation", [
        N.h4("Reframe the Problem"),
        N.para("Ask: 'What is the minimum squares for n?' Directly translate to: "
               "dp(n) = min(dp(n−s²)+1) for each valid s. This is the memoized top-down version "
               "of the same recurrence — you derive the recursive formula first, then add @lru_cache."),
        N.h4("What Doesn't Work"),
        N.para("The same recursion without caching: exponential. dp(n−s²) is called repeatedly "
               "for the same rem values across different call sites. @lru_cache eliminates this."),
        N.h4("The Key Observation"),
        N.para("The recursive structure is identical to the iterative one — the difference is that "
               "top-down only computes sub-problems actually reachable from n, while bottom-up "
               "fills all dp[0..n] regardless. For this problem they're equivalent in practice."),
        N.h4("Building the Solution"),
        N.para("Write the naive recursion (base: rem==0, return 0; else try all squares). "
               "Add @lru_cache. Done. Python's lru_cache handles the memo table automatically."),
    ]),
    N.h3("Code"),
    N.code(MEMOIZATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   ("  — Python decorator that stores results of dp(rem) in a dict. "
                    "When dp(rem) is called again with the same rem, it returns the cached result "
                    "in O(1) instead of recomputing.", {})])),
    N.para(N.rich([("def dp(rem):", {"code": True}),
                   ("  — rem = the remaining sum we need to cover with perfect squares.", {})])),
    N.para(N.rich([("if rem == 0: return 0", {"code": True}),
                   ("  — Base case: nothing remaining, need 0 more squares.", {})])),
    N.para(N.rich([("best = min(best, dp(rem - s*s) + 1)", {"code": True}),
                   ("  — Recursive call: solve rem−s² optimally, add 1 for the square we used. "
                    "lru_cache ensures each unique rem is computed only once.", {})])),
    N.callout(
        "Tabulation vs Memoization: Both are O(n√n) time, O(n) space. "
        "Tabulation avoids recursion depth limits (Python default: 1000). "
        "Memoization is easier to derive directly from the recurrence. "
        "In interviews, start with memoization to show derivation, then offer tabulation.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Solution 3: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force Recursion (TLE, for intuition only)"),
    N.para("The same recursion as memoization but WITHOUT caching. Exponential time because "
           "identical sub-problems are recomputed: dp(4) is called when processing dp(5), dp(8), "
           "dp(13), dp(20), etc. — each time spawning a full new recursion tree."),
    N.code(BRUTE_FORCE_CODE, "python"),
    N.callout(
        "DO NOT submit this. For n=100 it may run in time, but for n=10000 it TLEs. "
        "The only purpose of showing this is to make overlapping subproblems visible — "
        "every call to rec(4) repeats the exact same work.",
        "⚠️", "red_background"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Recursion", "O(n^(n/2))", "O(n) stack", "TLE for n > ~30"],
        ["Memoization (Top-Down)", "O(n√n)", "O(n)", "Easier to derive; stack depth"],
        ["Tabulation (Bottom-Up) ✓", "O(n√n)", "O(n)", "Iterative; no stack; interview pick"],
    ]),
    N.para(N.rich([
        ("O(n√n) justification: ", {"bold": True}),
        ("Outer loop runs n times. For each target i, the inner loop runs at most ⌊√i⌋ ≤ √n times. "
         "Total operations: Σ(i=1 to n) √i ≈ O(n√n).", {}),
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Unbounded Knapsack (Min squares summing to n) — each square can be reused "
                    "as many times as needed (unbounded); we minimize count (knapsack objective).", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Minimum number of items from a set that sum to n' + items reusable → Unbounded Knapsack. "
        "(2) Outer loop = targets 1..n; inner loop = items (squares). "
        "(3) 'Greedy fails' is a hint DP might be needed. "
        "(4) The same problem with single-use items would be 0/1 Knapsack (items outer, targets inner backward).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Unbounded Knapsack technique:"),
    N.bullet(N.rich([("Coin Change", {"bold": True}),
                     (" (Medium) — Min coins for amount; identical structure, arbitrary coins (#322)", {})])),
    N.bullet(N.rich([("Coin Change II", {"bold": True}),
                     (" (Medium) — Count ways to make amount; unbounded, count not min (#518)", {})])),
    N.bullet(N.rich([("Minimum Cost For Tickets", {"bold": True}),
                     (" (Medium) — Day-indexed DP; 1/7/30-day passes; same min-cost idea (#983)", {})])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}),
                     (" (Medium) — Count ordered ways to sum to target; unbounded, order matters (#377)", {})])),
    N.bullet(N.rich([("Integer Break", {"bold": True}),
                     (" (Medium) — Split n, maximize product; DP with multiplication (#343)", {})])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}),
                     (" (Medium) — 0/1 knapsack (single-use items); contrast to unbounded (#416)", {})])),
    N.para("These problems all reduce to: 'optimize over combinations of items (reusable or not) summing to a target.'"),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18.3 (Unbounded Knapsack). "
        "Sub-Pattern label used: 'Unbounded Knapsack (Min squares summing to n)' "
        "— source: Guide Section 18.3.",
        "📚", "gray_background"
    ),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("perfect_squares")),
    N.para(N.rich([
        ("Step through the DP table fill visually — use Next/Prev or arrow keys. "
         "Each step shows which square is being tried, the recurrence decision (both options with formulas), "
         "and the live dp array updating.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
