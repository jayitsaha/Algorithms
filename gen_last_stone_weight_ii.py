"""
Notion page update for Last Stone Weight II (#1049, Medium, 0/1 Knapsack / Minimize Subset Difference).
Wipes existing thin content and rebuilds in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813c-8a53-cb3bc0ad6f47"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1049,
    pattern="Dynamic Programming",
    subpatterns=["Minimize Subset Difference"],
    tc="O(n·S)",
    sc="O(S)",
    key_insight="Assign +/- signs to stones; minimize |S-2P| by finding largest subset sum P <= S//2 via 0/1 Knapsack DP.",
    icon="🟡",
    status="Solved",
    source="LeetCode"
)
print("Properties set.")

# ── Step 2: Wipe old body ──────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── Step 3: Rebuild body ────────────────────────────────────────────────────
# We'll send in chunks because Notion limits 100 blocks/request (using chunk=40 in append_blocks)

TABULATION_CODE = """\
def lastStoneWeightII(stones: list[int]) -> int:
    total = sum(stones)              # S = sum of all stones
    target = total // 2             # maximize subset sum <= S//2
    dp = [False] * (target + 1)     # dp[j] = "can some subset sum to j?"
    dp[0] = True                    # base case: empty subset sums to 0
    for stone in stones:            # process each stone exactly once
        for j in range(target, stone - 1, -1):   # right-to-left: 0/1 knapsack
            dp[j] |= dp[j - stone]  # include stone if j-stone was reachable
    best_P = max(j for j in range(target + 1) if dp[j])  # largest reachable <= target
    return total - 2 * best_P       # |GroupB - GroupA| = S - 2*P (non-negative)\
"""

MEMOIZATION_CODE = """\
from functools import lru_cache

def lastStoneWeightII(stones: list[int]) -> int:
    total = sum(stones)
    target = total // 2

    @lru_cache(None)
    def can_reach(i: int, rem: int) -> bool:
        # Can stones[i:] form exactly rem?
        if rem == 0:
            return True
        if i == len(stones) or rem < 0:
            return False
        # Two choices: include stones[i] or skip it
        return can_reach(i + 1, rem - stones[i]) or can_reach(i + 1, rem)

    best_P = max(j for j in range(target + 1) if can_reach(0, j))
    return total - 2 * best_P\
"""

BRUTE_CODE = """\
from itertools import combinations

def lastStoneWeightII_brute(stones: list[int]) -> int:
    total, best = sum(stones), float('inf')
    for r in range(len(stones) + 1):
        for combo in combinations(stones, r):
            P = sum(combo)
            best = min(best, abs(total - 2 * P))
    return best  # O(2^n) -- too slow for n=30\
"""

RECURRENCE = """\
dp[j] = dp[j] OR dp[j - stone]

Meaning: "can I reach sum j?" = "was it reachable before?" OR "can I reach j-stone and then add stone?"
Base case: dp[0] = True (empty subset sums to 0)
Iterate j from target DOWN to stone -- ensures each stone used at most once (0/1 property)\
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("stones", {"code": True}),
        (" where ", {}),
        ("stones[i]", {"code": True}),
        (" is the weight of the ", {}),
        ("i", {"code": True}),
        ("-th stone.\n\n"
         "We play a game: on each turn, choose the two heaviest stones and smash them together. "
         "Suppose the two heaviest are x and y with x <= y:\n"
         "  - If x == y, both stones are destroyed.\n"
         "  - If x != y, the stone of weight x is destroyed and the stone of weight y has new weight y - x.\n\n"
         "At the end of the game, there is at most one stone left. "
         "Return the smallest possible weight of the left stone. If there are no stones left, return 0.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Tabulation (Interview Pick) ────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Every smash operation assigns a sign: one stone gets +1 (survivor), the other −1 (canceled). "
            "After all smashes, the result equals the absolute value of Σ(±stones[i]). "
            "If we assign each stone a sign ourselves — put some in Group A (+) and the rest in Group B (−) — "
            "the final answer equals |sum_A − sum_B|. Let total = sum_A + sum_B = S. "
            "Then the result = |S − 2 × sum_A|. To minimize this, maximize sum_A subject to sum_A ≤ S//2."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try all 2^n subsets for Group A and compute |S − 2P|. "
            "With n=30, this is 2^30 ≈ 1 billion operations — far too slow. "
            "Greedy (always take/leave the largest stone) fails because local choices don't guarantee "
            "the global minimum difference."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Maximizing sum_A ≤ S//2 is the classic 0/1 Knapsack problem: "
            "items = stones, knapsack capacity = S//2, item weight = stone weight, "
            "we want to fill the knapsack as full as possible. "
            "We don't need the actual value-to-weight ratio — all stones have equal 'value' per unit weight. "
            "We just track which sums are reachable: dp[j] = True if some subset of processed stones sums to j."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Compute total S = sum(stones), target = S // 2.\n"
            "2. Create dp[0..target] all False; set dp[0] = True.\n"
            "3. For each stone w, scan j from target DOWN to w: dp[j] |= dp[j - w].\n"
            "   Right-to-left ensures each stone is used at most once (0/1 property).\n"
            "4. Find best_P = max j with dp[j]=True.\n"
            "5. Return S − 2 × best_P."
        ),
        N.callout(
            "Analogy: You're dividing coins between two piggy banks to make them as equal as possible. "
            "You can't break coins. The 0/1 Knapsack DP tracks which totals are achievable for the first bank, "
            "then fills the second bank with everything else.",
            "🏦", "blue_background"
        ),
    ]),
    N.h3("Why Is This DP? (Optimal Substructure + Overlapping Subproblems)"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Whether sum j is reachable from the first i stones depends on: (a) was it reachable from i-1 stones "
         "(skip stone i), or (b) was j-w[i] reachable from i-1 stones (then add stone i). Each subproblem breaks "
         "into strictly smaller subproblems.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive approach recomputes 'can I form sum j from stones i..n-1?' many times via different "
         "paths. DP fills each dp[j] exactly once in O(n × S) total operations vs O(2^n) for recursion.", {})
    ])),
    N.h3("Recurrence Relation"),
    N.code(RECURRENCE, "plain text"),
    N.h3("Code"),
    N.code(TABULATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("total = sum(stones)", {"code": True}), (" — Sum all stone weights to get S. With n<=30, stones[i]<=100, S <= 3000.", {})])),
    N.para(N.rich([("target = total // 2", {"code": True}), (" — We want the largest subset sum <= S//2. Floor division handles odd S gracefully.", {})])),
    N.para(N.rich([("dp = [False] * (target + 1)", {"code": True}), (" — Boolean array of size target+1. dp[j] answers 'can some subset reach sum j?'", {})])),
    N.para(N.rich([("dp[0] = True", {"code": True}), (" — The empty subset always sums to 0. This is the base case that seeds all reachability.", {})])),
    N.para(N.rich([("for stone in stones:", {"code": True}), (" — Outer loop: each stone considered exactly once (this is what makes it 0/1, not unbounded).", {})])),
    N.para(N.rich([("for j in range(target, stone - 1, -1):", {"code": True}), (" — RIGHT-TO-LEFT is mandatory. Ensures that when we read dp[j-stone], it reflects state BEFORE this stone was considered. If left-to-right, we'd count the same stone twice.", {})])),
    N.para(N.rich([("dp[j] |= dp[j - stone]", {"code": True}), (" — OR update: 'can we reach j?' = 'was j reachable before?' OR 'was j-stone reachable, so we can add this stone?'", {})])),
    N.para(N.rich([("best_P = max(...)", {"code": True}), (" — Find the largest reachable sum <= target. This is Group A's sum; Group B gets the rest.", {})])),
    N.para(N.rich([("return total - 2 * best_P", {"code": True}), (" — GroupB - GroupA = (S - best_P) - best_P = S - 2*best_P. Factor of 2 because P is subtracted twice.", {})])),
    N.callout(
        "⚠️ Why total − 2*best_P, not total − best_P?\n"
        "Group B sum = S − best_P. Group A sum = best_P. Their difference = (S − best_P) − best_P = S − 2×best_P. "
        "The 2 comes from P appearing on both sides of the subtraction.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization (Top-Down) ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same reframe as Solution 1: minimize |S − 2P| by finding largest reachable subset sum P ≤ S//2."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without caching recomputes the same (i, rem) states exponentially many times."),
        N.h4("The Key Observation"),
        N.para(
            "Write the recurrence as a recursive function: can_reach(i, rem) = True if stones[i:] can form sum rem. "
            "Base cases: rem=0 → True; i exhausted or rem<0 → False. "
            "Two branches: include stones[i] (rem becomes rem-stones[i]) or skip (rem stays). "
            "Cache with lru_cache to avoid recomputation."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Same total, target setup.\n"
            "2. Define can_reach(i, rem) recursively with memoization.\n"
            "3. Iterate j from target down to 0, find largest j where can_reach(0, j)=True.\n"
            "4. Return total − 2 × best_P.\n\n"
            "Space is O(n × target) for the cache vs O(target) for tabulation. "
            "Tabulation is preferred in interviews for lower space and simpler code."
        ),
    ]),
    N.h3("Code"),
    N.code(MEMOIZATION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(None)", {"code": True}), (" — Python's built-in memoization decorator. Caches all (i, rem) results automatically.", {})])),
    N.para(N.rich([("def can_reach(i, rem):", {"code": True}), (" — Asks: can stones[i:] contribute a subset summing to rem?", {})])),
    N.para(N.rich([("if rem == 0: return True", {"code": True}), (" — We've exactly filled the target — success.", {})])),
    N.para(N.rich([("if i == len(stones) or rem < 0: return False", {"code": True}), (" — Ran out of stones, or overshot the target.", {})])),
    N.para(N.rich([("return can_reach(i+1, rem-stones[i]) or can_reach(i+1, rem)", {"code": True}), (" — Two branches: include stone i (subtract weight) or skip it (keep rem same).", {})])),
    N.divider(),
]

# ── Solution 3: Brute Force ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force (Establish Baseline, Then Reject)"),
    N.h3("Code"),
    N.code(BRUTE_CODE, "python"),
    N.para("Enumerate all 2^n subsets. For each subset compute |S − 2P|. Return the minimum. Correct but O(2^n) — unusable for n=30 (over 1 billion operations)."),
    N.divider(),
]

# ── Complexity Table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsets)", "O(2^n)", "O(n)"],
        ["Top-Down Memoization", "O(n·S)", "O(n·S)"],
        ["Bottom-Up Tabulation (Interview Pick)", "O(n·S)", "O(S)"],
    ]),
    N.para(
        "S = sum of all stones ≤ 30 × 100 = 3000. "
        "So O(n·S) = O(30 × 1500) = O(45,000) operations and O(1500) space. Very efficient."
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Minimize Subset Difference (0/1 Knapsack)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Partition items into two groups with minimum/equal difference'\n"
        "• Items with signs (+/-) canceling each other → think |S-2P|\n"
        "• 'Can a subset sum to exactly k?' → boolean 0/1 Knapsack\n"
        "• Each item used at most once + bounded total → 0/1 Knapsack\n"
        "• Signal: answer involves |difference of two groups|",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (0/1 Knapsack / Minimize Subset Difference):"),
    N.bullet(N.rich([
        ("Partition Equal Subset Sum", {"bold": True}),
        (" (Medium) — Exact same DP; asks if minimum difference = 0. The special case of this problem. (#416)", {})
    ])),
    N.bullet(N.rich([
        ("Target Sum", {"bold": True}),
        (" (Medium) — Count ways to assign +/− signs to reach a target sum; same sign-assignment reframe. (#494)", {})
    ])),
    N.bullet(N.rich([
        ("Coin Change", {"bold": True}),
        (" (Medium) — Unbounded Knapsack: unlimited coins, minimize count. Inner loop goes LEFT-to-right. (#322)", {})
    ])),
    N.bullet(N.rich([
        ("Ones and Zeroes", {"bold": True}),
        (" (Medium) — 2D 0/1 Knapsack: two resource constraints (count of 0s and 1s). (#474)", {})
    ])),
    N.bullet(N.rich([
        ("Subset Sum (GFG/Classic)", {"bold": True}),
        (" (Medium) — Foundational 0/1 Knapsack problem: boolean answer to 'can we reach sum k?'", {})
    ])),
    N.bullet(N.rich([
        ("Last Stone Weight", {"bold": True}),
        (" (Easy) — Greedy version: always smash two heaviest. Simpler O(n log n), different structure. (#1046)", {})
    ])),
    N.bullet(N.rich([
        ("Split Array With Same Average", {"bold": True}),
        (" (Hard) — Find subset whose average equals total average; harder Knapsack variant. (#805)", {})
    ])),
    N.para("These problems share the same core technique: 0/1 Knapsack DP with a 1D boolean array, right-to-left inner loop."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → DP: 0/1 Knapsack)", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("last_stone_weight_ii")),
    N.para(N.rich([
        ("Step through the 0/1 Knapsack DP visually — watch the dp[] table fill row by row. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
