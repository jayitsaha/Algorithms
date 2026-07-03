"""
gen_coin_change.py — Notion in-place update for Coin Change (LC #322).
Run from the Algorithms/ directory alongside notion_lib.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8191-baeb-de9453cc34d0"
SLUG    = "coin_change"

# ─────────────────────────────────────────────────────────────
# 1) Set page properties
# ─────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=322,
    pattern="Dynamic Programming",
    subpatterns=["Unbounded Knapsack"],
    tc="O(amount × n)",
    sc="O(amount)",
    key_insight="dp[a] = min(dp[a-c]+1) for all coins c; fill left-to-right for unlimited reuse.",
    icon="🟡",
)
print("Properties set.")

# ─────────────────────────────────────────────────────────────
# 2) Wipe existing thin content
# ─────────────────────────────────────────────────────────────
print("Wiping old content...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ─────────────────────────────────────────────────────────────
# 3) Build body blocks
# ─────────────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array "), ("coins", {"code": True}),
        (" representing coins of different denominations and an integer "),
        ("amount", {"code": True}), (" representing a total amount of money.\n\n"
        "Return the fewest number of coins that you need to make up that amount. "
        "If that amount of money cannot be made up by any combination of the coins, return "),
        ("-1", {"code": True}), (".\n\nYou may assume that you have an infinite number of each kind of coin."),
    ])),
    N.divider(),
]

# ── Solution 1 — Bottom-Up Tabulation ────────────────────────
sol1_code = """\
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)   # dp[a] = min coins to make amount a
    dp[0] = 0                             # Base: 0 coins for 0 amount
    for a in range(1, amount + 1):        # Fill amounts left-to-right
        for c in coins:                   # Try each denomination
            if c <= a:                    # Only use coin if it fits
                dp[a] = min(dp[a], dp[a - c] + 1)  # 1 coin + optimal remainder
    return dp[amount] if dp[amount] != float('inf') else -1
"""

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the minimum number of coins to hit a target. "
               "Each coin reduces the remaining target — so the optimal answer for "
               "amount A is built from the optimal answer for A minus whichever coin we pick last. "
               "That recursive dependency on sub-problems screams Dynamic Programming."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always take the largest coin) fails. "
               "With coins=[1,3,4] and amount=6: greedy picks 4+1+1=3 coins, but 3+3=2 coins is optimal. "
               "Greedy has no look-ahead. Brute-force recursion tries all paths but recomputes the same "
               "sub-amounts exponentially — O(n^amount)."),
        N.h4("The Key Observation"),
        N.para("If we know the optimal solution for every amount smaller than A, "
               "we can compute the optimal for A by trying each coin c: "
               "dp[A] = min over all c of (dp[A-c] + 1). "
               "We just need to ensure smaller amounts are solved first — that's the left-to-right fill order."),
        N.h4("Building the Solution"),
        N.para("1. Create dp[0..amount] initialized to infinity (unreachable).\n"
               "2. Set dp[0] = 0 (zero coins for zero amount).\n"
               "3. For a = 1 to amount: try each coin c. If c <= a, update dp[a] = min(dp[a], dp[a-c]+1).\n"
               "4. Return dp[amount] if finite, else -1."),
        N.callout("Analogy: Think of the DP table as a recipe book. "
                  "dp[a] is the minimum-ingredient recipe for dish 'a'. "
                  "Each new dish is made by taking any coin 'c' and looking up the recipe for 'a-c'.",
                  "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [float('inf')] * (amount + 1)", {"code": True}),
                   " — Create table of size amount+1. All infinity means 'not yet reachable'."
                   " We index from 0 to amount inclusive."])),
    N.para(N.rich([("dp[0] = 0", {"code": True}),
                   " — Base case: it costs zero coins to make zero. This is the seed that all other values derive from."])),
    N.para(N.rich([("for a in range(1, amount + 1):", {"code": True}),
                   " — Outer loop: fill amounts from 1 up to target. Left-to-right ensures dp[a-c] is finalized before dp[a]."])),
    N.para(N.rich([("for c in coins:", {"code": True}),
                   " — Inner loop: try every available denomination. We want the minimum across all choices."])),
    N.para(N.rich([("if c <= a:", {"code": True}),
                   " — Guard: only try coin c if it doesn't exceed the current amount. Using coin 3 when we need only 2 is invalid."])),
    N.para(N.rich([("dp[a] = min(dp[a], dp[a - c] + 1)", {"code": True}),
                   " — Core recurrence: using coin c costs 1, plus the optimal solution for the remaining (a-c). "
                   "Take the minimum across all coins."])),
    N.para(N.rich([("return dp[amount] if dp[amount] != float('inf') else -1", {"code": True}),
                   " — If dp[amount] is still infinity, no combination reached the target. Return -1."])),
    N.divider(),
]

# ── Solution 2 — Top-Down Memoization ───────────────────────
sol2_code = """\
def coinChange(coins: list[int], amount: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(rem):
        if rem == 0:
            return 0                        # Base: 0 coins for 0 remaining
        if rem < 0:
            return float('inf')             # Coin exceeded remaining — invalid
        return min(dp(rem - c) + 1 for c in coins)  # Try all coins, cache result

    ans = dp(amount)
    return ans if ans != float('inf') else -1
"""

blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: Recursive Structure Made Explicit", [
        N.h4("Reframe the Problem"),
        N.para("Same recurrence as Solution 1, but expressed recursively. "
               "dp(rem) = minimum coins to make 'rem' amount. "
               "This matches the mathematical recurrence directly."),
        N.h4("What Doesn't Work"),
        N.para("Without memoization (lru_cache), this is the exponential brute-force — "
               "the same sub-problems are recomputed over and over. "
               "With memoization, each unique 'rem' value is computed exactly once."),
        N.h4("The Key Observation"),
        N.para("lru_cache turns the exponential recursion tree into a DAG (directed acyclic graph) "
               "where each node is computed once. The recursion makes the recurrence relation "
               "visually obvious — dp(rem) = min(dp(rem-c)+1 for c in coins) is exactly the formula."),
        N.h4("Building the Solution"),
        N.para("1. Define recursive dp(rem).\n"
               "2. Base cases: rem==0 → return 0; rem<0 → return inf (overshot).\n"
               "3. Recursive case: try all coins, return minimum dp(rem-c)+1.\n"
               "4. lru_cache handles memoization automatically."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   " — Python's built-in memoization. Stores results of dp(rem) keyed by rem. "
                   "On repeat calls with same rem, returns cached result immediately."])),
    N.para(N.rich([("def dp(rem):", {"code": True}),
                   " — Recursive function: returns minimum coins to make exactly 'rem'."])),
    N.para(N.rich([("if rem < 0: return float('inf')", {"code": True}),
                   " — If a coin c exceeded the remaining amount, this branch is invalid. "
                   "Returning inf ensures it's never chosen as a minimum."])),
    N.para(N.rich([("min(dp(rem - c) + 1 for c in coins)", {"code": True}),
                   " — Try every coin. dp(rem-c) gives the optimal for the reduced amount; +1 for the current coin."])),
    N.divider(),
]

# ── Why DP section ───────────────────────────────────────────
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   "The optimal solution for amount A contains the optimal solution for amount A-c "
                   "(for whichever coin c is chosen last). If we could do better for A-c, we could improve A — contradiction."])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   "Without memoization, dp(5) is recomputed as a subproblem of dp(6) via coin=1, "
                   "AND as a subproblem of other calls. With coins=[1] and amount=100, the naive tree "
                   "has exponential branching. DP memoizes each sub-amount and solves it exactly once."])),
    N.code("Recurrence:\ndp[0] = 0                                            (base case)\ndp[a] = min(dp[a-c] + 1)  for all coins c where c <= a\nReturn: dp[amount]  if finite, else -1", "plain text"),
    N.para(N.rich([("Unbounded Knapsack (1D): ", {"bold": True}),
                   "In 0/1 Knapsack each item used at most once, requiring 2D dp[item][capacity] "
                   "and right-to-left filling to prevent reuse. Here, coins are unlimited — "
                   "a 1D array filled left-to-right correctly allows coin c to appear multiple times "
                   "because dp[a-c] may itself already contain coin c."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Recursion", "O(n^amount)", "O(amount) stack"],
        ["Top-Down Memoization", "O(amount × n)", "O(amount)"],
        ["Bottom-Up Tabulation (optimal)", "O(amount × n)", "O(amount)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Unbounded Knapsack — 1D DP, items reusable, fill left-to-right, outer=amount inner=items"])),
    N.callout("When to recognize this pattern:\n"
              "• 'Minimum/maximum/count using items with unlimited supply'\n"
              "• 'Coins can be reused any number of times'\n"
              "• Greedy fails (no canonical denomination structure)\n"
              "• Signature: dp[a] = opt(dp[a-item] + cost) with 1D table", "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Unbounded Knapsack technique:"),
    N.bullet(N.rich([("Coin Change II", {"bold": True}),
                     " (Medium) — Count number of combinations; change min→sum, dp[0]=1 (#518)"])),
    N.bullet(N.rich([("Perfect Squares", {"bold": True}),
                     " (Medium) — Min perfect squares summing to n; same recurrence, coins=squares (#279)"])),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}),
                     " (Easy) — Count ways with 1 or 2 steps; simplest unbounded DP (#70)"])),
    N.bullet(N.rich([("Word Break", {"bold": True}),
                     " (Medium) — Segment string with dictionary; each word reusable (#139)"])),
    N.bullet(N.rich([("Integer Break", {"bold": True}),
                     " (Medium) — Maximize product of parts; unlimited factor reuse (#343)"])),
    N.bullet(N.rich([("Minimum Cost For Tickets", {"bold": True}),
                     " (Medium) — 1/7/30-day tickets for minimum travel cost (#983)"])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}),
                     " (Medium) — Contrast: 0/1 Knapsack (each element once, right-to-left fill) (#416)"])),
    N.para("These problems share the core structure: minimize/count/check a target using unlimited items, "
           "with a 1D DP table filled left-to-right."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), "
              "Sub-pattern: Unbounded Knapsack. Source: Guide Section 18", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the DP table being filled cell by cell — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ─────────────────────────────────────────────────────────────
# 4) Append all blocks
# ─────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
