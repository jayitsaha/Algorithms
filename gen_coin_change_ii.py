"""
gen_coin_change_ii.py — Regenerate Notion page for Coin Change II (LeetCode #518)
Unbounded Knapsack / Count Combinations DP problem.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-8d3b-fca7af8a7f06"

# ─── 1. Properties ───────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=518,
    pattern="Dynamic Programming",
    subpatterns=["Unbounded Knapsack", "Count combinations"],
    tc="O(n x amount)",
    sc="O(amount)",
    key_insight="Outer loop over coins, inner over amounts: ensures combinations (not permutations) are counted exactly once.",
    icon="\U0001f7e1"
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping existing body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ─── 3. Build new body ───────────────────────────────────────────────────────
print("Building new body...")
blocks = []

# ── Problem statement ────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer ", {}),
        ("amount", {"code": True}),
        (" and an array ", {}),
        ("coins", {"code": True}),
        (" of distinct denominations. Return the number of ", {}),
        ("combinations", {"bold": True}),
        (" (not permutations) that make up that amount. You may use each coin an unlimited number of times. "
         "If no combination exists, return ", {}),
        ("0", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("amount = 5", {"code": True}),
        (", ", {}),
        ("coins = [1, 2, 5]", {"code": True}),
        (" => 4. Combinations: [5], [2,2,1], [2,1,1,1], [1,1,1,1,1].", {}),
    ])),
    N.callout(
        N.rich([
            ("Key constraint: ", {"bold": True}),
            ("Order does NOT matter. [1,2] and [2,1] are the same combination. "
             "This is the critical difference from Combination Sum IV (which counts permutations).", {}),
        ]),
        "\U0001f3af", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Tabulation (Interview Pick) ─────────────────────────────────
sol1_code = (
    "def change(amount: int, coins: list[int]) -> int:\n"
    "    dp = [0] * (amount + 1)   # dp[a] = ways to make amount a\n"
    "    dp[0] = 1                  # base case: empty combination\n"
    "\n"
    "    for c in coins:            # outer: process each coin denomination\n"
    "        for a in range(c, amount + 1):  # inner: amounts this coin reaches\n"
    "            dp[a] += dp[a - c]  # extend combinations that reach (a - c)\n"
    "\n"
    "    return dp[amount]\n"
    "\n"
    "# Time:  O(n * amount)  n = len(coins)\n"
    "# Space: O(amount)"
)

blocks += [
    N.h2("Solution 1 - Tabulation / Bottom-Up (Interview Pick)"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We are filling a knapsack of capacity amount. Each coin is an item with weight = its value. "
            "Items can be reused (unbounded). Instead of maximizing value, we count distinct ways to "
            "exactly fill the knapsack. The combinations (not permutations) constraint is the key twist."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive recursion without memoization is exponential. Even with memoization, iterating over "
            "coin order permutation-style would count [1,2] and [2,1] as separate paths — giving the "
            "wrong answer. Greedy fails: for amount=4, coins=[1,3], greedy picks 3, then is stuck."
        ),
        N.h4("The Key Observation"),
        N.para(
            "To count combinations (not permutations), process coins in a fixed outer order. "
            "For each coin c, ask: how many ways can I make each sub-amount a if I only use coin c "
            "and coins processed before c? This prevents re-ordering because once we are done with "
            "coin c, it can never appear after c in any combination."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize dp[0] = 1 (one way to make amount 0: the empty set). "
            "For each coin c, iterate a from c to amount: dp[a] += dp[a - c]. "
            "This adds one more coin c to every combination that already reaches a-c. "
            "The dp array at the end gives dp[amount] = total combinations."
        ),
        N.callout(
            N.rich([
                ("Analogy: ", {"bold": True}),
                ("Imagine filling a jar with marbles, processing one size at a time. "
                 "For each marble size, extend all partial fillings. By fixing the processing order, "
                 "you never double-count 'large then small' vs 'small then large'.", {}),
            ]),
            "\U0001f9e0", "blue_background"
        ),
    ]),

    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The number of combinations for amount a using coins up to index i equals (combinations "
         "using coins 0..i-1 only) + (combinations using coins 0..i for amount a - coins[i]).", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Without memoization, dp(amount=5) recomputes dp(3) via path 5->2->3 and separately "
         "via 5->1->4->3. Memoization or tabulation ensures each sub-amount is computed once.", {}),
    ])),

    N.h3("Recurrence Relation"),
    N.code(
        "# dp[a] = number of combinations that make amount a\n"
        "# Base case:\n"
        "dp[0] = 1     # one way to make 0: the empty set\n\n"
        "# Transition (for each coin c, each sub-amount a >= c):\n"
        "dp[a] += dp[a - c]\n\n"
        "# The outer coin loop is what ensures combinations (not permutations):\n"
        "# coin c is only ever appended to combinations of a-c, never placed 'before'\n"
        "# a denomination that was processed in a previous outer iteration.",
        "python"
    ),

    N.h3("Code"),
    N.code(sol1_code, "python"),

    N.h3("Line by Line"),
    N.para(N.rich([
        ("dp = [0] * (amount + 1)", {"code": True}),
        (" - Create DP table of size amount+1, all zeros. dp[a] = ways to make exactly amount a.", {}),
    ])),
    N.para(N.rich([
        ("dp[0] = 1", {"code": True}),
        (" - Base case: exactly 1 way to make amount 0 (use no coins). Seeds the entire table.", {}),
    ])),
    N.para(N.rich([
        ("for c in coins:", {"code": True}),
        (" - Outer loop: commit to each coin denomination before moving on. This is the combinations key.", {}),
    ])),
    N.para(N.rich([
        ("for a in range(c, amount + 1):", {"code": True}),
        (" - Inner loop left-to-right from c. Smaller amounts cannot use this coin. Left-to-right allows reuse.", {}),
    ])),
    N.para(N.rich([
        ("dp[a] += dp[a - c]", {"code": True}),
        (" - Core transition: every combination previously summing to (a-c) can become one summing to a by appending c.", {}),
    ])),
    N.para(N.rich([
        ("return dp[amount]", {"code": True}),
        (" - Final answer: total combinations that exactly make up the target amount.", {}),
    ])),
    N.callout(
        N.rich([
            ("Critical warning - loop order matters: ", {"bold": True}),
            ("If you swap the loops (outer=amounts, inner=coins), you count permutations instead! "
             "[1,2] and [2,1] become distinct paths — inflating the answer. "
             "Coins outer + amounts inner = combinations always.", {}),
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Memoization (Top-Down) ──────────────────────────────────────
sol2_code = (
    "from functools import cache\n\n"
    "def change(amount: int, coins: list[int]) -> int:\n"
    "    @cache\n"
    "    def dp(i: int, rem: int) -> int:\n"
    "        if rem == 0: return 1       # valid combination found\n"
    "        if i == len(coins) or rem < 0: return 0  # dead end\n"
    "\n"
    "        skip = dp(i + 1, rem)           # skip coin i\n"
    "        take = dp(i, rem - coins[i])    # use coin i (same i = unlimited reuse)\n"
    "        return skip + take\n\n"
    "    return dp(0, amount)\n\n"
    "# Time:  O(n * amount)  n * (amount+1) unique (i, rem) states\n"
    "# Space: O(n * amount)  memo table + O(n+amount) recursion stack"
)

blocks += [
    N.h2("Solution 2 - Memoization / Top-Down"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Define dp(i, rem) = ways to form rem using coins[i:]. "
            "At each state: skip coin i (move to i+1) or take coin i once (stay at i for unlimited reuse). "
            "Fixing the coin index i as a parameter prevents permutation counting."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization: state (i, rem) can be reached via multiple different "
            "prefixes of coin choices, causing exponential recomputation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "There are only n * (amount+1) unique states. Cache results: once we know how many ways "
            "to fill rem starting from coin index i, never recompute it."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base cases: rem==0 returns 1 (found combination), i>=len or rem<0 returns 0 (dead end). "
            "Memoize on (i, rem). Call dp(0, amount)."
        ),
        N.callout(
            N.rich([
                ("Why dp(i, rem - coins[i]) not dp(i+1, ...)?", {"bold": True}),
                (" Passing i+1 for 'take' means each coin used at most once (0/1 Knapsack). "
                 "Staying at i allows this coin to appear again in the next recursive call, "
                 "implementing unlimited reuse correctly.", {}),
            ]),
            "\U0001f4a1", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@cache", {"code": True}), (" - Memoization decorator. Caches by (i, rem) tuple.", {})])),
    N.para(N.rich([("if rem == 0: return 1", {"code": True}), (" - Reached target exactly: one valid combination.", {})])),
    N.para(N.rich([("if i == len(coins) or rem < 0: return 0", {"code": True}), (" - Dead-end: out of coins or overshot.", {})])),
    N.para(N.rich([("skip = dp(i + 1, rem)", {"code": True}), (" - Skip coin i: move to next denomination.", {})])),
    N.para(N.rich([("take = dp(i, rem - coins[i])", {"code": True}), (" - Use coin i once more, staying at i (unbounded).", {})])),
    N.para(N.rich([("return skip + take", {"code": True}), (" - Total combinations = ways skipping + ways taking coin i.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Interview?"],
        ["Brute Force (no memo)", "Exponential", "O(A/c) stack", "Never"],
        ["Tabulation (bottom-up)", "O(n x A)", "O(A)", "Best pick"],
        ["Memoization (top-down)", "O(n x A)", "O(n x A) + stack", "Good alternative"],
    ]),
    N.para("n = coin count, A = amount, c = smallest coin value."),
    N.para(N.rich([
        ("Interview Pick: Tabulation. ", {"bold": True}),
        ("Uses O(amount) space vs O(n x amount) for memoization, no call overhead, "
         "and is simpler to explain and trace on a whiteboard.", {}),
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("\U0001f3f7️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Unbounded Knapsack, Count Combinations", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Counting ways to reach a target sum from a set of elements. "
             "(2) Elements can be reused unlimited times. "
             "(3) Order does not matter (combinations). "
             "Signal words: 'number of ways', 'how many combinations', 'unlimited', 'distinct'. "
             "Contrast: if order matters (permutations) -> swap loops (see Combination Sum IV).", {}),
        ]),
        "\U0001f50e", "green_background"
    ),
    N.para(N.rich([
        ("The Definitive Loop Order Rule: ", {"bold": True}),
        ("Coins outer + amounts inner = combinations (this problem). "
         "Amounts outer + coins inner = permutations (Combination Sum IV). "
         "Memorize this distinction — it is asked in nearly every unbounded knapsack interview.", {}),
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("\U0001f517 Related Problems"),
    N.para("Problems using Unbounded Knapsack or the same counting DP structure:"),
    N.bullet(N.rich([
        ("Coin Change (LC 322)", {"bold": True}),
        (" (Medium) - Same coins, but minimize number of coins to reach amount. dp[a] = min(dp[a-c]+1).", {}),
    ])),
    N.bullet(N.rich([
        ("Combination Sum IV (LC 377)", {"bold": True}),
        (" (Medium) - Same setup but counts permutations: amounts outer, coins inner.", {}),
    ])),
    N.bullet(N.rich([
        ("Partition Equal Subset Sum (LC 416)", {"bold": True}),
        (" (Medium) - 0/1 Knapsack (each element once). Can you reach exactly sum/2?", {}),
    ])),
    N.bullet(N.rich([
        ("Perfect Squares (LC 279)", {"bold": True}),
        (" (Medium) - Unbounded knapsack with squares as denominations; minimum count.", {}),
    ])),
    N.bullet(N.rich([
        ("Climbing Stairs (LC 70)", {"bold": True}),
        (" (Easy) - Simplest unbounded DP: ways to reach n steps with 1 or 2 step jumps.", {}),
    ])),
    N.bullet(N.rich([
        ("Target Sum (LC 494)", {"bold": True}),
        (" (Medium) - Counting DP: assign +/- signs to elements to reach target.", {}),
    ])),
    N.bullet(N.rich([
        ("Integer Break (LC 343)", {"bold": True}),
        (" (Medium) - Unbounded factoring: each number 2..n is a 'coin'.", {}),
    ])),
    N.bullet(N.rich([
        ("Word Break (LC 139)", {"bold": True}),
        (" (Medium) - Unbounded knapsack on strings: can dictionary words tile the string?", {}),
    ])),
    N.para("These problems share the core technique: dp[a] += dp[a - item] with careful loop ordering."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18: Dynamic Programming -> Unbounded Knapsack",
        "\U0001f4da", "gray_background"
    ),
    N.divider(),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.h2("\U0001f3af Interactive Visual Explainer"),
    N.embed(N.embed_url_for("coin_change_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually - use Next/Prev or arrow keys to watch the DP table fill row by row.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ─── 4. Append blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
