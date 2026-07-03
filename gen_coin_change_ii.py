"""
gen_coin_change_ii.py — Notion IN-PLACE update for Coin Change II (#518)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-8d3b-fca7af8a7f06"
SLUG = "coin_change_ii"

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=518,
    pattern="Dynamic Programming",
    subpatterns=["Count combinations (Unbounded Knapsack)"],
    tc="O(n·amount)",
    sc="O(amount)",
    key_insight="Coins in outer loop counts combinations (not permutations); forward inner loop allows unlimited coin reuse.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer ", {}),
        ("amount", {"code": True}),
        (" and an array of coin denominations ", {}),
        ("coins", {"code": True}),
        (". Each coin denomination has unlimited supply. Return the number of distinct ", {}),
        ("combinations", {"bold": True}),
        (" (not sequences — order does not matter) of coins that sum to exactly ", {}),
        ("amount", {"code": True}),
        (". If no combination exists, return 0.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("amount=5, coins=[1,2,5] → 4 combinations: [5], [2,2,1], [2,1,1,1], [1,1,1,1,1]", {}),
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Tabulation ──
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count distinct multisets of coins (order irrelevant) that sum to amount. This is a classic 'count the ways' problem with unlimited item reuse — the textbook Unbounded Knapsack setup."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force recursion tries all combinations but recomputes the same sub-amounts exponentially many times. For amount=30, the call tree has billions of nodes — clearly we need memoization or tabulation."),
        N.h4("The Key Observation"),
        N.para("If we know the number of ways to reach every amount smaller than x, we can compute ways to reach x in O(1) per coin: dp[x] += dp[x - coin]. The dependency graph is acyclic and computable bottom-up."),
        N.h4("Building the Solution"),
        N.para("Initialize dp[0]=1 (empty selection). For each coin denomination (outer loop), for each reachable amount x (inner loop, forward): dp[x] += dp[x-coin]. The coins-outer / amounts-inner arrangement ensures each combination is counted exactly once — once coin c is fully processed, no future coin can insert c 'earlier' in a combination."),
        N.callout("Analogy: Imagine filling a bucket to height x using blocks of various sizes, introduced one size at a time. Each new block size creates new towers but cannot rearrange the old ones. No duplication is possible.", "🧠", "blue_background"),
    ]),
    N.h3("Why is This DP?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("dp[x] depends only on dp[x-c] for each coin c. Larger problems reduce to smaller ones with no circular dependencies.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Naive recursion recomputes dp[2], dp[3], etc. dozens of times. DP computes each sub-amount exactly once and reuses the stored result.", {}),
    ])),
    N.h3("Recurrence Relations"),
    N.code(
        "Base case: dp[0] = 1  (one way to make 0: empty selection)\n"
        "\n"
        "Transition:\n"
        "  for coin in coins:          # outer: introduce one denomination at a time\n"
        "      for x in range(coin, amount+1):  # inner: forward direction = unbounded reuse\n"
        "          dp[x] += dp[x - coin]\n"
        "\n"
        "Reading dp[x] += dp[x-coin] aloud:\n"
        "  'Every combination reaching x-coin becomes a new combination reaching x'\n"
        "  (by appending exactly one coin of value coin)",
        "python"
    ),
    N.h3("Code"),
    N.code(
        "def change(amount: int, coins: list[int]) -> int:\n"
        "    dp = [0] * (amount + 1)   # dp[x] = # combinations summing to x\n"
        "    dp[0] = 1                 # base: 1 way to make 0 (empty selection)\n"
        "\n"
        "    for coin in coins:        # OUTER: introduce each denomination once\n"
        "        for x in range(coin, amount + 1):  # INNER: forward = reuse allowed\n"
        "            dp[x] += dp[x - coin]  # extend all combos reaching x-coin\n"
        "\n"
        "    return dp[amount]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * (amount + 1)", {"code": True}), (" — Create a DP table of size amount+1, all zeros. dp[x] will hold the combination count for each sub-amount.", {})])),
    N.para(N.rich([("dp[0] = 1", {"code": True}), (" — Base case: one way to make 0 (the empty set of coins). Without this seed, nothing propagates.", {})])),
    N.para(N.rich([("for coin in coins:", {"code": True}), (" — Outer loop. Process one denomination at a time. This is the key to counting combinations: each denomination is 'introduced' exactly once.", {})])),
    N.para(N.rich([("for x in range(coin, amount + 1):", {"code": True}), (" — Inner loop. Only amounts ≥ coin can include this coin. Forward iteration (coin→amount) is essential for unbounded reuse.", {})])),
    N.para(N.rich([("dp[x] += dp[x - coin]", {"code": True}), (" — Core update. All combinations that could reach x-coin can now reach x by appending one coin. This accumulates over all coins for each x.", {})])),
    N.para(N.rich([("return dp[amount]", {"code": True}), (" — Final answer: total distinct combinations summing exactly to amount.", {})])),
    N.callout(
        "CRITICAL — Loop Order: Coins OUTER, Amounts INNER = combinations. Swapping the order (amounts outer, coins inner) counts permutations instead — [1,2] and [2,1] would be counted as different answers. This single detail separates this problem from Combination Sum IV (#377).",
        "⚠️", "yellow_background"
    ),
    N.callout(
        "CRITICAL — Inner Loop Direction: Forward (coin→amount) allows unlimited reuse of the same coin. Backward (amount→coin) would restrict each coin to a single use (0/1 Knapsack). The direction encodes the 'unbounded supply' constraint.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Recursive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each step we have a choice: skip denomination coins[idx] (never use it again) or take one coin of coins[idx] (possibly use it again). This binary branching tree is the natural recursive structure."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without caching is exponential. dp(idx, remaining) is called with the same arguments from many different call paths — the cache eliminates this redundancy."),
        N.h4("The Key Observation"),
        N.para("Staying at the same index when taking a coin (not advancing to idx+1) is what grants unlimited reuse. Advancing idx permanently closes the door on that denomination, preventing out-of-order insertions."),
        N.h4("Building the Solution"),
        N.para("Two parameters fully define a subproblem: which denominations are still available (encoded as index idx) and how much amount remains. lru_cache memoizes (idx, remaining) pairs automatically."),
        N.callout("Because we always pass idx or idx+1 (never less), and we only advance or stay, every (idx, remaining) pair is computed at most once. Total states = n × (amount+1).", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def change(amount: int, coins: list[int]) -> int:\n"
        "    from functools import lru_cache\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(idx: int, remaining: int) -> int:\n"
        "        if remaining == 0:\n"
        "            return 1          # exact hit: valid combination found\n"
        "        if remaining < 0 or idx == len(coins):\n"
        "            return 0          # overshot or no more denominations\n"
        "        # Option A: skip coins[idx] entirely for this branch\n"
        "        skip = dp(idx + 1, remaining)\n"
        "        # Option B: take one more coin of coins[idx] (stay at idx for reuse)\n"
        "        take = dp(idx, remaining - coins[idx])\n"
        "        return skip + take\n"
        "\n"
        "    return dp(0, amount)",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoizes all (idx, remaining) calls. Without this, runtime is exponential.", {})])),
    N.para(N.rich([("if remaining == 0: return 1", {"code": True}), (" — Exact match: we've used coins summing to exactly the target. Count this as 1 valid combination.", {})])),
    N.para(N.rich([("if remaining < 0 or idx == len(coins): return 0", {"code": True}), (" — Either overshot (exceeded target) or exhausted all denominations with remaining > 0. Neither yields a valid combo.", {})])),
    N.para(N.rich([("skip = dp(idx + 1, remaining)", {"code": True}), (" — Permanently move past coins[idx]. This is the 'never use this denomination again' branch.", {})])),
    N.para(N.rich([("take = dp(idx, remaining - coins[idx])", {"code": True}), (" — Use one coin of coins[idx] and stay at idx. Staying = reuse allowed. The two options together enumerate all combinations without permutations.", {})])),
    N.para(N.rich([("return skip + take", {"code": True}), (" — Total combinations = ways without this coin + ways using this coin (possibly multiple times).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-Force Recursion", "Exponential", "O(amount) stack"],
        ["Top-Down Memoization", "O(n × amount)", "O(n × amount) cache + O(n) stack"],
        ["Bottom-Up Tabulation (optimal)", "O(n × amount)", "O(amount)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Count combinations (Unbounded Knapsack)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count the number of combinations/ways' phrasing (not min/max)\n"
        "• Items (coins) can be reused any number of times\n"
        "• Order does NOT matter (combinations, not sequences)\n"
        "• Budget-style constraint (sum must equal a target amount)\n"
        "Distinguish from: Combination Sum IV (#377) where order DOES matter (permutations).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Unbounded Knapsack / Count Combinations):"),
    N.bullet(N.rich([("Coin Change", {"bold": True}), (" (Medium) — Minimum coins to make amount; same structure, take min instead of sum (#322)", {})])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}), (" (Medium) — Count ordered sequences; swap to amounts-outer, coins-inner loop (#377)", {})])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), (" (Medium) — 0/1 Knapsack; each element used at most once; backward inner loop (#416)", {})])),
    N.bullet(N.rich([("Perfect Squares", {"bold": True}), (" (Medium) — Minimum perfect squares summing to n; unbounded reuse + take min (#279)", {})])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), (" (Medium) — Print all combinations via backtracking (not DP); unlimited reuse (#39)", {})])),
    N.bullet(N.rich([("Target Sum", {"bold": True}), (" (Medium) — Count assignments of +/- to sum to target; unbounded knapsack variant (#494)", {})])),
    N.para("These problems share the core technique: 1D DP table with a base case at 0, forward inner loop for reuse, and a carefully chosen loop order."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → Unbounded Knapsack)", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch the dp table fill cell by cell as each coin denomination is introduced.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
