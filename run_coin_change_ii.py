"""
Wrapper that injects the valid Notion token before running gen_coin_change_ii.py.
This avoids modifying notion_lib.py (which is protected).
"""
import sys, os

# Patch the token before notion_lib is imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import notion_lib and patch token in-memory
import notion_lib as N
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS = {
    "Authorization": f"Bearer {N.TOKEN}",
    "Notion-Version": N.NOTION_VERSION,
    "Content-Type": "application/json",
}

# Now patch sys.modules so gen script reuses the patched instance
import importlib
sys.modules['notion_lib'] = N

# Run the gen script logic inline (avoids double-import issues)
PAGE_ID = "39193418-809c-81d8-8d3b-fca7af8a7f06"

print("Step 1: Setting page properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=518,
    pattern="Dynamic Programming",
    subpatterns=["Unbounded Knapsack"],
    tc="O(n x amount)",
    sc="O(amount)",
    key_insight="Outer loop coins, inner loop amounts: ensures combinations (not permutations) are counted.",
    icon="\U0001f7e1"
)
print("  Properties set.")

print("Step 2: Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks.")

print("Step 3: Building new page body...")
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer "), ("amount", {"code": True}),
        (" and an array "), ("coins", {"code": True}),
        (" of distinct denominations. You have an unlimited supply of each coin. "
         "Return the number of distinct "),
        ("combinations", {"bold": True}),
        (" (order doesn't matter) that sum exactly to "), ("amount", {"code": True}), ("."),
    ])),
    N.para(N.rich([
        ("Example: "), ("amount = 5", {"code": True}), (", "),
        ("coins = [1, 2, 5]", {"code": True}),
        (" => return 4. Combinations: [5], [2,2,1], [2,1,1,1], [1,1,1,1,1]."),
    ])),
    N.callout(
        N.rich([
            ("Key distinction: ", {"bold": True}),
            ("[1,2] and [2,1] count as ONE combination. Only distinct unordered groupings are counted. "
             "This shapes the entire loop structure.")
        ]),
        "\U0001f4a1", "green_background"
    ),
    N.divider(),
]

# Solution 1 - Tabulation
sol1_code = (
    "def change(amount: int, coins: list[int]) -> int:\n"
    "    dp = [0] * (amount + 1)      # dp[i] = ways to make amount i\n"
    "    dp[0] = 1                    # base: empty combination\n"
    "\n"
    "    for coin in coins:           # OUTER: process each denomination fully\n"
    "        for a in range(coin, amount + 1):  # INNER: amounts this coin reaches\n"
    "            dp[a] += dp[a - coin]           # accumulate new combinations\n"
    "\n"
    "    return dp[amount]            # total distinct combinations\n"
    "\n"
    "# Time:  O(n * amount)  n = len(coins)\n"
    "# Space: O(amount)\n"
)

blocks += [
    N.h2("Solution 1 - Tabulation / Bottom-Up (Interview Pick)"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Count unordered selections (baskets of coins) from unlimited supply that sum to target. "
               "Every combination for amount A that includes coin c comes from a combination for A-c."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force recursion is exponential. Greedy only finds one combination. "
               "We need DP to count all valid groupings systematically."),
        N.h4("The Key Observation"),
        N.para("dp[a] += dp[a - coin]: every combination reaching a-coin can be extended by one coin to reach a. "
               "Accumulate this across all coin denominations."),
        N.h4("Building the Solution"),
        N.para("1. dp[0..amount] = 0, dp[0] = 1.\n"
               "2. For each coin (outer), for each amount a >= coin (inner): dp[a] += dp[a-coin].\n"
               "3. Coins outer = combinations (not permutations). Return dp[amount]."),
        N.callout(
            "Analogy: Stamp Book. Complete all arrangements using only 1-cent stamps, then add 2-cent, etc. "
            "Each denomination adds on top of existing counts without reordering.",
            "\U0001f9e0", "blue_background"
        ),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   ("Count for amount A is directly built from counts for smaller amounts (A-coin). "
                    "No need to recompute from scratch.")])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   ("Without caching, the count for 'amount 3' is recomputed many times across different "
                    "recursive paths. DP computes each sub-amount once.")])),
    N.h3("Recurrence Relation"),
    N.code(
        "dp[0] = 1                    # base: one empty combination reaches 0\n"
        "dp[a] += dp[a - coin]        # for each coin <= a\n\n"
        "# Left-to-right inner loop enables unlimited coin reuse (Unbounded Knapsack).\n"
        "# When dp[a] reads dp[a-coin], that entry may already include this same coin.\n"
        "# This is intentional and correct.\n"
    ),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * (amount + 1)", {"code": True}),
                   (" - 1D array size amount+1. Index i = target amount i.")])),
    N.para(N.rich([("dp[0] = 1", {"code": True}),
                   (" - Base: exactly one combination sums to 0 (empty selection). Seeds all future accumulation.")])),
    N.para(N.rich([("for coin in coins:", {"code": True}),
                   (" - Outer loop over denominations. Processing each coin completely first gives combinations.")])),
    N.para(N.rich([("for a in range(coin, amount + 1):", {"code": True}),
                   (" - Start at 'coin': amounts below coin cannot include it. Left-to-right enables reuse.")])),
    N.para(N.rich([("dp[a] += dp[a - coin]", {"code": True}),
                   (" - The recurrence: extend combinations reaching a-coin by appending this coin.")])),
    N.para(N.rich([("return dp[amount]", {"code": True}),
                   (" - Final answer: total distinct combinations for the full target.")])),
    N.callout(
        N.rich([
            ("Critical warning: ", {"bold": True}),
            ("Swapping loops (amounts outer, coins inner) counts permutations instead! "
             "[1,2] and [2,1] become separate — inflating the answer. "
             "Always: coins outer, amounts inner for combinations.")
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 - Memoization
sol2_code = (
    "from functools import cache\n\n"
    "def change(amount: int, coins: list[int]) -> int:\n"
    "    @cache\n"
    "    def dp(i: int, rem: int) -> int:\n"
    "        if rem == 0:\n"
    "            return 1              # valid combination found\n"
    "        if i == len(coins) or rem < 0:\n"
    "            return 0              # no coins left or overshot\n"
    "\n"
    "        skip = dp(i + 1, rem)          # skip coin[i] entirely\n"
    "        take = dp(i, rem - coins[i])   # use coin[i] (same i = unlimited)\n"
    "        return skip + take\n\n"
    "    return dp(0, amount)\n\n"
    "# Time:  O(n * amount)  unique (i, rem) states\n"
    "# Space: O(n * amount)  memo table + recursion stack\n"
)

blocks += [
    N.h2("Solution 2 - Memoization / Top-Down"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define recursive function dp(i, rem) = ways to form rem using coins[i:]. "
               "At each state: skip this denomination or take this coin (unlimited reuse)."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion recomputes (i, remaining) pairs exponentially. "
               "Memoization caches each unique state exactly once."),
        N.h4("The Key Observation"),
        N.para("dp(i, rem) = dp(i+1, rem) [skip] + dp(i, rem-coins[i]) [take]. "
               "Passing same i for 'take' enables unlimited use of this coin."),
        N.h4("Building the Solution"),
        N.para("Base: rem==0 -> 1, i>=len or rem<0 -> 0.\n"
               "Cache on (i, rem). Call dp(0, amount). "
               "O(n*amount) unique states, each O(1) work."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("@cache", {"code": True}),
                   (" - Python memoization decorator: auto-caches by (i, rem) arguments.")])),
    N.para(N.rich([("if rem == 0: return 1", {"code": True}),
                   (" - Reached target exactly: one valid combination found.")])),
    N.para(N.rich([("if i == len(coins) or rem < 0: return 0", {"code": True}),
                   (" - Out of coin types or overshot: invalid path.")])),
    N.para(N.rich([("skip = dp(i + 1, rem)", {"code": True}),
                   (" - Skip this denomination entirely, try next.")])),
    N.para(N.rich([("take = dp(i, rem - coins[i])", {"code": True}),
                   (" - Use this coin. Same i = can pick this denomination again (unbounded).")])),
    N.para(N.rich([("return skip + take", {"code": True}),
                   (" - Total = ways skipping this denomination + ways including it.")])),
    N.callout(
        N.rich([
            ("Why dp(i, ...) not dp(i+1, ...) for take? ", {"bold": True}),
            ("Passing i+1 would mean use each coin at most once (0/1 Knapsack). "
             "Staying at i allows this denomination again on the next call.")
        ]),
        "\U0001f4a1", "green_background"
    ),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Interview?"],
        ["Brute Force (no memo)", "Exponential", "O(A/c) stack", "Never"],
        ["Tabulation (bottom-up)", "O(n x A)", "O(A)", "Best pick"],
        ["Memoization (top-down)", "O(n x A)", "O(n x A) + stack", "Good alternative"],
    ]),
    N.para("n = coin count, A = amount, c = smallest coin value"),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("\U0001f3f7️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Unbounded Knapsack (Count Combinations)")])),
    N.callout(
        N.rich([
            ("When to recognize: ", {"bold": True}),
            ("'Count the number of ways to reach target X' + unlimited items + combinations (not permutations). "
             "Signals: 'infinite supply', 'number of combinations', 'distinct ways'. "
             "Constraints: amount <= 5000, len(coins) <= 300.")
        ]),
        "\U0001f50e", "green_background"
    ),
    N.para(N.rich([
        ("Loop order rule: ", {"bold": True}),
        ("Coins outer + Amounts inner = Combinations. "
         "Amounts outer + Coins inner = Permutations. "
         "This separates Coin Change II (this problem) from Combination Sum IV.")
    ])),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("\U0001f517 Related Problems"),
    N.para("Problems using Unbounded Knapsack or the same counting DP structure:"),
    N.bullet(N.rich([("Coin Change", {"bold": True}),
                     (" (Medium) - Minimum coins to reach target; same dp array with min() instead of sum")])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}),
                     (" (Medium) - Same setup but counts permutations; swap loop order")])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}),
                     (" (Medium) - 0/1 Knapsack; each element used at most once; reverse inner loop")])),
    N.bullet(N.rich([("Perfect Squares", {"bold": True}),
                     (" (Medium) - Unbounded Knapsack with squares as denominations; minimum count")])),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}),
                     (" (Easy) - Simplest unbounded DP; excellent entry point for this pattern")])),
    N.bullet(N.rich([("Target Sum", {"bold": True}),
                     (" (Medium) - Counting DP; assign +/- to elements to reach target")])),
    N.bullet(N.rich([("Integer Break", {"bold": True}),
                     (" (Medium) - Unbounded factoring; same recurrence structure")])),
    N.para("These problems share the core technique: accumulate sub-solution counts across a 1D dp array."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md - Section 18: Dynamic Programming -> Unbounded Knapsack",
        "\U0001f4da", "gray_background"
    ),
]

# Embed
blocks += [
    N.divider(),
    N.h2("\U0001f3af Interactive Visual Explainer"),
    N.embed(N.embed_url_for("coin_change_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually - use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("  Blocks appended successfully.")

print("\nNOTION OK", PAGE_ID)
