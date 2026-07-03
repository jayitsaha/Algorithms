"""
gen_target_sum.py — Notion in-place update for LeetCode #494 Target Sum.
Run from the Algorithms/ directory alongside notion_lib.py.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819b-83c9-d67c98f588cf"

# ── 1) Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=494,
    pattern="Dynamic Programming",
    subpatterns=["Count Subsets to Target"],
    tc="O(n·S) where S=(total+target)/2",
    sc="O(S)",
    key_insight="Partition into '+' subset P and '−' subset N; P=(total+target)/2=S; count subsets summing to S using 0/1 Knapsack DP.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("target", {"code": True}),
        (". For each element in the array you must assign either a '+' or '−' sign. "
         "Evaluate the expression and count the number of distinct sign assignments "
         "whose result equals ", {}),
        ("target", {"code": True}),
        (". Each element must be used exactly once.\n\n"
         "Example: nums=[1,1,1,1,1], target=3  →  Answer: 5\n"
         "  (−1+1+1+1+1, +1−1+1+1+1, +1+1−1+1+1, +1+1+1−1+1, +1+1+1+1−1)", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP Tabulation / Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Don't think about sign assignments directly — think about partitioning the array. "
            "Every valid assignment splits nums into two disjoint subsets: P (assigned '+') and N "
            "(assigned '−'). The condition sum(P) − sum(N) = target, combined with "
            "sum(P) + sum(N) = total, gives sum(P) = (total + target) / 2. "
            "So we just need to count subsets of nums that sum to S = (total + target) / 2."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try all 2^n sign combinations. For n=20 that's ~1 million — borderline. "
            "A pure recursive DFS without caching has 2^n leaves; many subtrees share the same "
            "(index, remaining_sum) state and are recomputed exponentially."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The state (which index we're at, how much sum remains) fully determines the count of "
            "valid completions. This is the overlapping-subproblems signal for DP. "
            "The number of distinct (index, remaining) pairs is O(n × 2·total) — polynomial. "
            "The partition insight reduces this further: we only need dp[j] for j = 0..S, "
            "and S ≤ total ≤ 1000 (given constraints)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Compute S = (total + target) // 2. Guard: if (total+target) is odd or S < 0, return 0.\n"
            "2. Init dp = [0]*(S+1), dp[0] = 1.\n"
            "3. For each num in nums: sweep j from S down to num: dp[j] += dp[j-num].\n"
            "4. Return dp[S].\n\n"
            "The reverse sweep (j: S → num) is the 0/1 Knapsack trick: it guarantees dp[j-num] "
            "still holds the count from BEFORE this item was processed, so each item is used at most once."
        ),
        N.callout(
            "Analogy: Imagine filling a bag of capacity S. Each item (num) can go in once. "
            "dp[j] = ways to exactly fill capacity j. Adding an item: for each capacity j (high to low), "
            "inherit the ways to fill j-num from before. High-to-low prevents double-counting.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def findTargetSumWays(nums: list[int], target: int) -> int:\n"
        "    total = sum(nums)\n"
        "    # Guard: S must be a non-negative integer\n"
        "    if (total + target) % 2 != 0:\n"
        "        return 0\n"
        "    S = (total + target) // 2\n"
        "    if S < 0:\n"
        "        return 0\n"
        "    # dp[j] = number of subsets summing to j\n"
        "    dp = [0] * (S + 1)\n"
        "    dp[0] = 1  # base: one way to form sum 0 (take nothing)\n"
        "    for num in nums:\n"
        "        # Reverse sweep: 0/1 Knapsack — each item used at most once\n"
        "        for j in range(S, num - 1, -1):\n"
        "            dp[j] += dp[j - num]\n"
        "    return dp[S]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("total = sum(nums)", {"code": True}), " — sum all elements; needed to compute the partition target S."])),
    N.para(N.rich([("if (total + target) % 2 != 0", {"code": True}), " — S = (total+target)/2 must be an integer; if the sum is odd it's impossible."])),
    N.para(N.rich([("S = (total + target) // 2", {"code": True}), " — S is the required sum of the positive-sign subset P."])),
    N.para(N.rich([("if S < 0", {"code": True}), " — S must be non-negative (subset sums ≥ 0 for non-negative inputs); guard against impossible targets."])),
    N.para(N.rich([("dp = [0] * (S + 1)", {"code": True}), " — 1D DP array; dp[j] will hold the count of subsets summing to j."])),
    N.para(N.rich([("dp[0] = 1", {"code": True}), " — Base case: one way to form sum 0 (the empty subset)."])),
    N.para(N.rich([("for num in nums:", {"code": True}), " — Outer loop processes each number exactly once (O(n) iterations)."])),
    N.para(N.rich([("for j in range(S, num - 1, -1):", {"code": True}), " — Inner loop sweeps backwards (0/1 Knapsack): ensures dp[j-num] hasn't been updated yet this pass."])),
    N.para(N.rich([("dp[j] += dp[j - num]", {"code": True}), " — If we include this num: all ways to reach sum j-num extend to reach j by adding num."])),
    N.para(N.rich([("return dp[S]", {"code": True}), " — dp[S] = number of '+' subsets summing to S = total valid sign assignments."])),
    N.divider(),
]

# ── Solution 2 — Memoization ──
blocks += [
    N.h2("Solution 2 — Memoization / Top-Down DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think recursively: at each index i with remaining target r, we have two choices — "
            "assign '+' (recurse with r-nums[i]) or assign '−' (recurse with r+nums[i]). "
            "The total ways = ways from '+' choice + ways from '−' choice."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without caching has 2^n calls — exponential. But notice that many "
            "different paths reach the same (i, remaining) state. The state space is only "
            "O(n × 2·total) — we should cache each unique (i, remaining) pair."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The memoization state is (i, remaining). Once computed, it's reused by any path "
            "that arrives at index i needing remaining sum. With lru_cache, Python handles "
            "the memo table automatically."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp(i, remaining) = number of ways to assign signs to nums[i:] such that "
            "their signed sum = remaining. Base: dp(n, 0) = 1, dp(n, x≠0) = 0. "
            "Transition: dp(i, r) = dp(i+1, r-nums[i]) + dp(i+1, r+nums[i])."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n\n"
        "def findTargetSumWays(nums: list[int], target: int) -> int:\n"
        "    n = len(nums)\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i: int, remaining: int) -> int:\n"
        "        # Base case: used all numbers\n"
        "        if i == n:\n"
        "            return 1 if remaining == 0 else 0\n"
        "        # Try assigning '+' and '−' to nums[i]\n"
        "        add = dp(i + 1, remaining - nums[i])\n"
        "        sub = dp(i + 1, remaining + nums[i])\n"
        "        return add + sub\n"
        "    return dp(0, target)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Memoizes all (i, remaining) pairs automatically; turns exponential into polynomial."])),
    N.para(N.rich([("def dp(i, remaining)", {"code": True}), " — State: i = current index, remaining = how much signed sum we still need from nums[i:]."])),
    N.para(N.rich([("if i == n: return 1 if remaining == 0 else 0", {"code": True}), " — All numbers used: valid iff remaining is exactly 0."])),
    N.para(N.rich([("add = dp(i+1, remaining - nums[i])", {"code": True}), " — Assign '+': nums[i] contributes positively, reduces remaining."])),
    N.para(N.rich([("sub = dp(i+1, remaining + nums[i])", {"code": True}), " — Assign '−': nums[i] contributes negatively, increases remaining."])),
    N.para(N.rich([("return add + sub", {"code": True}), " — Total ways from this state = sum of both branches."])),
    N.divider(),
]

# ── Why DP section ──
blocks += [
    N.h2("🧠 Why Is This Dynamic Programming?"),
    N.para(
        "Two pillars of DP are satisfied here:\n\n"
        "1) Optimal Substructure: The count of valid sign assignments for nums[i:] with target r "
        "depends only on the count for nums[i+1:] with targets r-nums[i] and r+nums[i]. "
        "The full answer is built from solutions to smaller subproblems.\n\n"
        "2) Overlapping Subproblems: Many different sign sequences for nums[0:i] can produce "
        "the same 'remaining' sum at index i. Without caching, we'd recompute dp(i, remaining) "
        "exponentially many times. With memoization, each (i, remaining) pair is computed once."
    ),
    N.callout(
        "Recurrence: dp[j] = dp[j] + dp[j - num]  (sweeping j from S down to num, for each num)\n"
        "Base: dp[0] = 1\n"
        "Answer: dp[S] where S = (sum(nums) + target) // 2",
        "📐", "gray_background"
    ),
    N.para(
        "The partition trick is the key optimization: instead of tracking (index, remaining) "
        "with a 2D table, we observe that every valid assignment is determined by which elements "
        "are in the '+' subset. That subset must sum to exactly S = (total+target)/2. "
        "So the 2D problem (n × 2·total states) collapses to a 1D problem (S+1 states)."
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DFS", "O(2^n)", "O(n) stack"],
        ["Memoization (top-down)", "O(n × total)", "O(n × total)"],
        ["DP Tabulation (Interview Pick)", "O(n × S)", "O(S)"],
    ]),
    N.para(
        "S = (total+target)/2 ≤ total ≤ 1000 (per constraints). "
        "So the tabulation runs in at most O(20000) operations — essentially O(1) in practice."
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Count Subsets to Target (0/1 Knapsack Count)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count ways to assign +/−' → subset partition trick\n"
        "• 'Count subsets summing to K' → dp[j] += dp[j-num], reverse sweep\n"
        "• Items used exactly once, counting (not optimizing) → 0/1 Knapsack count\n"
        "• Non-negative integers in nums, target can be positive or negative",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Count Subsets to Target / 0/1 Knapsack):"),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), " (Medium) — 0/1 Knapsack existence check: can we split into two equal-sum halves? (#416)"])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), " (Medium) — Same partition insight: minimize |P−N| by maximizing P ≤ total/2 (#1049)"])),
    N.bullet(N.rich([("Ones and Zeroes", {"bold": True}), " (Medium) — 2D 0/1 Knapsack with two capacity dimensions: counts of 0s and 1s (#474)"])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}), " (Medium) — Count ordered ways to reach target with unlimited items; unbounded + order matters (#377)"])),
    N.bullet(N.rich([("Count of Subsets with Given Sum", {"bold": True}), " (Medium) — Exact same dp[j] += dp[j-num] template; pure counting variant"])),
    N.bullet(N.rich([("Number of Dice Rolls With Target Sum", {"bold": True}), " (Medium) — Each die is an item with k face values; count ways to sum to target (#1155)"])),
    N.para("These problems all share the same core technique: 0/1 Knapsack count — dp[j] += dp[j-num] with a reversed inner loop."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming). Sub-Pattern verified via analysis (Count Subsets to Target is a recognized DP variant of 0/1 Knapsack).", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("target_sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
