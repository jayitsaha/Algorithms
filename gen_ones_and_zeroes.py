"""
gen_ones_and_zeroes.py — Notion page for LeetCode #474 Ones and Zeroes
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ─── Create page (notion_page_id is null — fresh page) ───
PAGE_ID = N.create_page("Ones and Zeroes", 474, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ─── Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=474,
    pattern="Dynamic Programming",
    subpatterns=["2D Knapsack Zeros and Ones"],
    tc="O(L·m·n)",
    sc="O(m·n)",
    key_insight="2D 0/1 Knapsack: dp[i][j] = max strings using ≤i zeros ≤j ones; reverse traversal prevents double-counting.",
    icon="🟡"
)
print("Properties set.")

# ─── Build body blocks ───
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of binary strings ", {}),
        ("strs", {"code": True}),
        (" and two integers ", {}),
        ("m", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (". Return the size of the largest subset of ", {}),
        ("strs", {"code": True}),
        (" such that there are at most ", {}),
        ("m", {"code": True}),
        (" 0's and ", {}),
        ("n", {"code": True}),
        (" 1's in the subset. A set ", {}),
        ("x", {"code": True}),
        (" is a subset of a set ", {}),
        ("y", {"code": True}),
        (" if all elements of ", {}),
        ("x", {"code": True}),
        (" are also elements of ", {}),
        ("y", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# Solution 1 — Bottom-Up Tabulation
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each binary string, we make a binary choice: include it in the subset or skip it. We have two limited budgets (zeros and ones). We want to maximize the count of included strings. This is selection under two simultaneous constraints — exactly the 2D 0/1 Knapsack."),
        N.h4("What Doesn't Work"),
        N.para("A greedy approach (pick shortest strings first, or fewest zeros first) fails because choosing a cheap string early can block a better combination later. Brute force over all 2^L subsets is O(2^L · L) — TLE for L up to 600."),
        N.h4("The Key Observation"),
        N.para("At any point during processing, the only information we need to decide whether to take a string is: how much of the zero-budget remains and how much of the one-budget remains. This 2D state (rem_zeros, rem_ones) is exactly what dp[i][j] encodes. Processing strings one at a time and updating the table in reverse order gives us the correct 0/1 (no-reuse) behavior."),
        N.h4("Building the Solution"),
        N.para("Define dp[i][j] = max strings selectable from strings seen so far within budget (i zeros, j ones). Base: all zeros (no strings → 0). For each string (z zeros, o ones): update dp[i][j] = max(dp[i][j], dp[i-z][j-o]+1) for i from m down to z, j from n down to o. Reverse traversal ensures dp[i-z][j-o] is from the prior round — before this string was considered — so it cannot be counted twice."),
        N.callout("Analogy: Packing a suitcase with two limits (weight AND volume). You pick items one by one and check against both limits. The table tracks the best packing for every possible remaining budget combination.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def findMaxForm(strs, m, n):
    dp = [[0]*(n+1) for _ in range(m+1)]
    for s in strs:
        z = s.count('0')
        o = s.count('1')
        for i in range(m, z-1, -1):
            for j in range(n, o-1, -1):
                dp[i][j] = max(dp[i][j],
                               dp[i-z][j-o] + 1)
    return dp[m][n]"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [[0]*(n+1)...]", {"code": True}), (" — Initialize (m+1)×(n+1) table, all zeros. dp[i][j] = 0 means 'using at most i zeros and j ones, we can select 0 strings (none processed yet).'", {})])),
    N.para(N.rich([("for s in strs:", {"code": True}), (" — Process each binary string one at a time; each is either taken or skipped.", {})])),
    N.para(N.rich([("z = s.count('0')", {"code": True}), (" — Count this string's zero-cost.", {})])),
    N.para(N.rich([("o = s.count('1')", {"code": True}), (" — Count this string's one-cost.", {})])),
    N.para(N.rich([("for i in range(m, z-1, -1):", {"code": True}), (" — Reverse sweep of the zero dimension. We go from m down to z (inclusive). If i < z, we can't afford this string anyway, so we skip those cells.", {})])),
    N.para(N.rich([("for j in range(n, o-1, -1):", {"code": True}), (" — Reverse sweep of the one dimension. Same reasoning: stop at o.", {})])),
    N.para(N.rich([("dp[i][j] = max(dp[i][j], dp[i-z][j-o] + 1)", {"code": True}), (" — The knapsack update. Left side of max: skip this string (keep old dp[i][j]). Right side: take this string — the best count with (i-z) zero budget and (j-o) one budget, plus 1 for this string. We pick whichever is larger.", {})])),
    N.para(N.rich([("return dp[m][n]", {"code": True}), (" — Final answer: maximum strings within the full budget (m zeros, n ones).", {})])),
    N.divider(),
]

# Solution 2 — Top-Down Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Write the recurrence directly as a recursive function: dp(idx, rem_z, rem_o) = max strings selectable from strs[idx:] with rem_z zeros and rem_o ones remaining. At each call, skip or take strs[idx] and recurse."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes the same (idx, rem_z, rem_o) state exponentially many times. The key overlapping subproblem: after taking 'str A' and then 'str B', the remaining budget is the same as after taking 'str B' and then 'str A' — same state, same answer."),
        N.h4("The Key Observation"),
        N.para("Cache the result for each unique (idx, rem_z, rem_o) triplet. Since there are L × (m+1) × (n+1) unique states, the total work is O(L·m·n) — same as tabulation, but with added overhead of Python function calls and the LRU cache."),
        N.h4("Building the Solution"),
        N.para("Use Python's @lru_cache decorator on the recursive dp function. Precompute (z, o) for each string. Base case: idx == len(strs) → return 0. Recursive case: max(skip, take) where take requires rem_z >= z and rem_o >= o."),
    ]),
    N.h3("Code"),
    N.code("""from functools import lru_cache

def findMaxForm(strs, m, n):
    counts = [(s.count('0'), s.count('1')) for s in strs]

    @lru_cache(maxsize=None)
    def dp(idx, rem_z, rem_o):
        if idx == len(counts): return 0
        z, o = counts[idx]
        skip = dp(idx+1, rem_z, rem_o)
        take = 0
        if rem_z >= z and rem_o >= o:
            take = 1 + dp(idx+1, rem_z-z, rem_o-o)
        return max(skip, take)

    return dp(0, m, n)"""),
    N.h3("Line by Line"),
    N.para(N.rich([("counts = [...]", {"code": True}), (" — Precompute (z, o) pairs once outside the memoized function. If done inside, the string.count() calls would repeat and the cache key would still work, but precomputing is cleaner.", {})])),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Cache results keyed by (idx, rem_z, rem_o). Since these are integers, hashing is fast. maxsize=None means unlimited cache size.", {})])),
    N.para(N.rich([("if idx == len(counts): return 0", {"code": True}), (" — Base case: processed all strings, no more to select. Answer is 0.", {})])),
    N.para(N.rich([("skip = dp(idx+1, rem_z, rem_o)", {"code": True}), (" — Option A: skip strs[idx], budget unchanged.", {})])),
    N.para(N.rich([("if rem_z >= z and rem_o >= o: take = 1 + dp(idx+1, rem_z-z, rem_o-o)", {"code": True}), (" — Option B: take strs[idx] only if budget allows. Reduce both budgets and add 1 to the count.", {})])),
    N.para(N.rich([("return max(skip, take)", {"code": True}), (" — Best of skip and take — the recurrence relation.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all 2^L subsets)", "O(2^L · L)", "O(L)"],
        ["Memoization (top-down)", "O(L·m·n)", "O(L·m·n)"],
        ["Tabulation (bottom-up) ✓", "O(L·m·n)", "O(m·n)"],
    ]),
    N.divider(),
]

# Why DP section (special for DP problems)
blocks += [
    N.h2("🧠 Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The best subset for budget (i, j) depends on the best subset for budget (i-z, j-o). The overall optimum is built from sub-problem optima — you can make the take/skip decision for each string independently given the remaining budget.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursion over strings[idx:] with remaining budget (rem_z, rem_o) recomputes the same (idx, rem_z, rem_o) states from multiple paths. The number of unique states is L × (m+1) × (n+1) — polynomial, not exponential.", {}),
    ])),
    N.code("# Recurrence relation\n# dp[i][j] = max strings from strings-so-far using ≤i zeros, ≤j ones\n#\n# For each string (z zeros, o ones):\n# dp[i][j] = max(dp[i][j],          <- skip\n#               dp[i-z][j-o] + 1)  <- take\n#\n# Traversal: i from m down to z, j from n down to o (0/1 trick)\n# Base case: dp[i][j] = 0 for all i, j (no strings yet)\n# Answer: dp[m][n]"),
    N.callout("Key DP Invariant: After processing the first k strings, dp[i][j] holds the maximum count of strings selectable from those k strings within budget (i zeros, j ones). Each string either improves cells or leaves them unchanged — it never decreases any cell.", "🔐", "blue_background"),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("2D Knapsack Zeros and Ones (extended 0/1 Knapsack with two independent weight dimensions)", {})])),
    N.callout("When to recognize this pattern: 'Select a subset of items' + 'stay within two independent budgets simultaneously.' Each item has two costs. You optimize a count or value. One budget → 1D dp array. Two budgets → 2D dp table. K budgets → K-dimensional dp.", "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (0/1 Knapsack family):"),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), (" (Medium) — Classic 1D knapsack: can we fill a capacity equal to sum/2? (#416)", {})])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), (" (Medium) — Partition stones into two most-equal groups via knapsack (#1049)", {})])),
    N.bullet(N.rich([("Target Sum", {"bold": True}), (" (Medium) — Assign +/− signs to reach a target; reduces to counting knapsack (#494)", {})])),
    N.bullet(N.rich([("Coin Change", {"bold": True}), (" (Medium) — Unbounded knapsack (coins can be reused); forward traversal; minimize count (#322)", {})])),
    N.bullet(N.rich([("Coin Change II", {"bold": True}), (" (Medium) — Count number of ways to make amount; unbounded counting knapsack (#518)", {})])),
    N.bullet(N.rich([("0/1 Knapsack (classic)", {"bold": True}), (" (Medium) — Single weight dimension; select items to maximize value without exceeding capacity", {})])),
    N.bullet(N.rich([("Maximum Profit in Job Scheduling", {"bold": True}), (" (Hard) — DP with time as the single resource dimension (#1235)", {})])),
    N.para("These problems share the same core technique: binary item selection (take or skip) with a fixed budget, solved by building a DP table that tracks the best outcome for every possible remaining budget."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → DP: 0/1 Knapsack). Sub-Pattern: 2D Knapsack Zeros and Ones.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("ones_and_zeroes")),
    N.para(N.rich([("Step through the 2D knapsack algorithm visually — use Next/Prev or arrow keys to see each dp[i][j] decision.", {"italic": True, "color": "gray"})])),
]

# ─── Append all blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
