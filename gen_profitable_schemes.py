"""
gen_profitable_schemes.py — Notion page builder for Profitable Schemes (#879).
notion_page_id is null → create a new page, then populate it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ─── Step 0: Create page (no existing page) ───
PAGE_ID = N.create_page("Profitable Schemes", 879, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ─── Step 1: Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=879,
    pattern="Dynamic Programming",
    subpatterns=["3D DP Member and Profit"],
    tc="O(k·n·minProfit)",
    sc="O(n·minProfit)",
    key_insight="3D knapsack: dp[members][profit] counts subsets; clamp profit at minProfit to keep table finite.",
    icon="🔴"
)
print("Properties set.")

# ─── Step 2: No wipe needed (fresh page) ───
# N.wipe_page(PAGE_ID)  # skip on fresh create

# ─── Step 3: Build page body ───
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are "),
        ("n", {"code": True}),
        (" gang members and "),
        ("k", {"code": True}),
        (" crimes. Crime "),
        ("i", {"code": True}),
        (" requires "),
        ("group[i]", {"code": True}),
        (" members and generates "),
        ("profit[i]", {"code": True}),
        (" profit. Count the number of subsets of crimes ("),
        ("schemes", {"italic": True}),
        (") such that the total members used ≤ "),
        ("n", {"code": True}),
        (" AND the total profit ≥ "),
        ("minProfit", {"code": True}),
        (". Return the answer modulo 10⁹ + 7.")
    ])),
    N.divider()
]

# ─────────────────────────────────────────────────────────────────────────
# SOLUTION 1 — Tabulation (Bottom-Up DP) — Interview Pick
# ─────────────────────────────────────────────────────────────────────────
sol1_code = """\
def profitableSchemes(n: int, minProfit: int, group: list, profit: list) -> int:
    MOD = 10**9 + 7
    # dp[j][p] = number of crime subsets using exactly j members
    #            with profit clamped to min(actual_profit, minProfit)
    dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # empty set: 0 members, 0 profit

    for g, p in zip(group, profit):         # process each crime
        # Iterate backwards: 0/1 knapsack (avoid using same crime twice)
        for j in range(n, g - 1, -1):       # members: n down to g
            for k in range(minProfit, -1, -1):  # profit: minProfit down to 0
                new_k = min(k + p, minProfit)   # clamp profit at minProfit
                dp[j][new_k] = (dp[j][new_k] + dp[j - g][k]) % MOD

    # Sum all states that achieved the profit target
    return sum(dp[j][minProfit] for j in range(n + 1)) % MOD
"""

blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are counting 0/1 subsets of items (crimes) subject to TWO constraints simultaneously: total 'weight' (members) ≤ n (upper bound), and total 'value' (profit) ≥ minProfit (lower bound). This is a two-constraint counting knapsack."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: enumerate all 2^k subsets, check each. Exponential — fails for k=100. Greedy (take highest profit-per-member crimes first) cannot count all valid subsets — it finds one, not all."),
        N.h4("The Key Observation"),
        N.para("Only the (members_used, profit_so_far) state matters — not which specific crimes were picked. Two different crime combinations leading to the same (j, p) state are interchangeable for future decisions. This means DP is applicable."),
        N.h4("Building the Solution"),
        N.para("Define dp[j][p] = number of subsets using exactly j members with clamped profit p. Process crimes one by one. For each crime, iterate member dimension downward (0/1 knapsack) to avoid re-using the same crime. Clamp profit at minProfit to keep the table finite — any profit ≥ minProfit is 'done'. Sum dp[j][minProfit] for all j at the end."),
        N.callout("Analogy: It's a 2D knapsack. The member dimension is like weight capacity (don't exceed n), the profit dimension is like a target threshold (must reach minProfit). We fill the table bottom-up, accumulating counts.", "🧠", "blue_background"),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The count of valid subsets from crimes [0..i] with j members and clamped profit p = (subsets not including crime i) + (subsets including crime i, sourced from state j-g, p-profit_i). These two groups partition all valid subsets perfectly."),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("In a naive recursive approach, the sub-answer for 'crimes [0..i] using j members with profit p' would be computed from many different parent calls. DP memoizes it."),
    ])),
    N.code("""\
# The Recurrence:
#   dp[j][min(p + profit_i, minProfit)] += dp[j - group_i][p]
#
# Iterate j from n DOWN to group_i  (0/1 knapsack: crime used at most once)
# Iterate p from minProfit DOWN to 0 (same reason: avoid double-counting)
""", "python"),
    N.callout(
        "Profit Clamping: Any profit ≥ minProfit is 'equally done'. We collapse profit=4, profit=5, ... into a single bucket at index minProfit. This makes the DP table finite and exact.",
        "🔐", "purple_background"
    ),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}), " — Standard modulus for large-count problems. Apply at every addition."])),
    N.para(N.rich([("dp = [[0]*(minProfit+1) for _ in range(n+1)]", {"code": True}), " — 2D table: (n+1) rows (member counts 0..n) × (minProfit+1) columns (clamped profit 0..minProfit)."])),
    N.para(N.rich([("dp[0][0] = 1", {"code": True}), " — Base case: the empty subset uses 0 members and earns 0 profit. Exactly 1 way to do this."])),
    N.para(N.rich([("for g, p in zip(group, profit):", {"code": True}), " — Process each crime one at a time. g = members required, p = profit gained."])),
    N.para(N.rich([("for j in range(n, g - 1, -1):", {"code": True}), " — Iterate member count downward from n to g. Downward ensures we don't use crime i more than once (0/1 knapsack invariant)."])),
    N.para(N.rich([("for k in range(minProfit, -1, -1):", {"code": True}), " — Iterate profit level downward. Same reason: prevents a profit update from feeding into another update in the same crime pass."])),
    N.para(N.rich([("new_k = min(k + p, minProfit)", {"code": True}), " — Clamp the new profit at minProfit. If k + p exceeds minProfit, it goes into the 'achieved target' bucket."])),
    N.para(N.rich([("dp[j][new_k] = (dp[j][new_k] + dp[j-g][k]) % MOD", {"code": True}), " — Core update: subsets that previously had j-g members and profit k, when crime i is added, now have j members and clamped profit new_k. Accumulate modularly."])),
    N.para(N.rich([("return sum(dp[j][minProfit] for j in range(n+1)) % MOD", {"code": True}), " — Sum over all member counts 0..n. dp[j][minProfit] = subsets with exactly j members AND profit ≥ minProfit."])),
    N.divider()
]

# ─────────────────────────────────────────────────────────────────────────
# SOLUTION 2 — Memoization (Top-Down DP)
# ─────────────────────────────────────────────────────────────────────────
sol2_code = """\
from functools import lru_cache

def profitableSchemes(n: int, minProfit: int, group: list, profit: list) -> int:
    MOD = 10**9 + 7
    k = len(group)

    @lru_cache(maxsize=None)
    def dp(i: int, members: int, prof: int) -> int:
        \"\"\"Count valid subsets of crimes[i:] given members used so far
        and prof (clamped to minProfit) earned so far.\"\"\"
        if i == k:
            # Base case: all crimes considered
            return 1 if prof >= minProfit else 0

        # Option A: skip crime i
        ways = dp(i + 1, members, prof)

        # Option B: take crime i (only if members capacity allows)
        if members + group[i] <= n:
            new_prof = min(prof + profit[i], minProfit)
            ways += dp(i + 1, members + group[i], new_prof)

        return ways % MOD

    return dp(0, 0, 0)
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: Recursive Definition", [
        N.h4("Reframe the Problem"),
        N.para("Think recursively: at each crime, we make a binary decision — skip or take. The sub-problem is 'how many valid subsets can we form from crimes[i..k-1] given that we've already used some members and earned some profit?'"),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without memoization re-computes the same (i, members, prof) state exponentially many times. The state space is k × n × minProfit which is polynomial — memoization makes it efficient."),
        N.h4("The Key Observation"),
        N.para("The recursive function dp(i, members, prof) has only k × (n+1) × (minProfit+1) unique states. Memoize with lru_cache to avoid recomputation. The clamping of prof at minProfit is essential — it bounds the prof dimension."),
        N.h4("Building the Solution"),
        N.para("At crime i: try skip (recurse with i+1) and try take (if members+group[i] <= n, recurse with i+1 and updated members/profit). At base case i==k, return 1 if profit reached minProfit else 0. The clamping min(prof + profit[i], minProfit) ensures the state space stays bounded."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Python built-in memoization. Converts the recursive function into a memoized one. Each unique (i, members, prof) tuple is computed once."])),
    N.para(N.rich([("if i == k:", {"code": True}), " — Base case: we've decided on all k crimes. If profit reached minProfit, this is 1 valid scheme configuration; otherwise 0."])),
    N.para(N.rich([("ways = dp(i+1, members, prof)", {"code": True}), " — Skip crime i: move to next crime with unchanged state."])),
    N.para(N.rich([("if members + group[i] <= n:", {"code": True}), " — Capacity check: can we add this crime's crew? Only take if it doesn't exceed n."])),
    N.para(N.rich([("new_prof = min(prof + profit[i], minProfit)", {"code": True}), " — Clamp profit for memo key: any profit ≥ minProfit is equivalent."])),
    N.para(N.rich([("ways += dp(i+1, members+group[i], new_prof)", {"code": True}), " — Take crime i: recurse with updated state. Both branches added to total count."])),
    N.divider()
]

# ─────────────────────────────────────────────────────────────────────────
# COMPLEXITY TABLE
# ─────────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (enumerate subsets)", "O(2^k · k)", "O(k)"],
        ["Memoization (top-down)", "O(k · n · minProfit)", "O(k · n · minProfit)"],
        ["Tabulation (bottom-up) ✓", "O(k · n · minProfit)", "O(n · minProfit)"],
    ]),
    N.para("k = number of crimes, n = gang size, minProfit = profit threshold."),
    N.divider()
]

# ─────────────────────────────────────────────────────────────────────────
# PATTERN CLASSIFICATION
# ─────────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "3D DP Member and Profit (Multi-Constraint 0/1 Knapsack)"])),
    N.callout(
        "When to recognize this pattern: 'Count subsets satisfying TWO simultaneous constraints (one upper bound = capacity, one lower bound = threshold).' Each item used at most once. The lower-bound constraint should be clamped to keep the DP dimension finite.",
        "🔎", "green_background"
    ),
    N.para("Note: '3D DP Member and Profit' is a problem-specific sub-pattern within the broader 0/1 Knapsack family. The third dimension (crime index) is compressed away via in-place backward iteration, yielding a 2D table at any given time."),
    N.divider()
]

# ─────────────────────────────────────────────────────────────────────────
# RELATED PROBLEMS
# ─────────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (multi-dimensional 0/1 Knapsack counting):"),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), " (Medium) — Classic 0/1 knapsack: subset summing to half-total. Single constraint, bool answer. LeetCode #416."])),
    N.bullet(N.rich([("Ones and Zeroes", {"bold": True}), " (Medium) — 0/1 knapsack with TWO capacity constraints (count of 0s and 1s). Closest structural cousin. LeetCode #474."])),
    N.bullet(N.rich([("Target Sum", {"bold": True}), " (Medium) — Count ways to assign +/- signs to reach target sum. Counting knapsack, reducible to subset sum count. LeetCode #494."])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), " (Medium) — Minimize difference by optimal partitioning; reduces to partition knapsack. LeetCode #1049."])),
    N.bullet(N.rich([("Coin Change 2", {"bold": True}), " (Medium) — Count combinations to reach amount (unbounded knapsack). Iterate upward instead of downward. LeetCode #518."])),
    N.bullet(N.rich([("Number of Ways to Earn Points", {"bold": True}), " (Hard) — Bounded multi-item counting DP with two constraints; same 3D structure as this problem. LeetCode #2585."])),
    N.para("These problems all share the core technique: model as a counting knapsack, define DP state over constraint dimensions, and iterate constraint dimensions in the correct direction."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern verified via analysis as a specialized variant of 0/1 Knapsack.", "📚", "gray_background"),
]

# ─────────────────────────────────────────────────────────────────────────
# VISUAL EXPLAINER EMBED
# ─────────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("profitable_schemes")),
    N.para(N.rich([
        ("Step through the 3D DP table fill visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ─── Append all blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT profitable_schemes | html=OK | notion=OK | page_id={PAGE_ID}")
