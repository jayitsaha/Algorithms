"""Notion page rebuild for: Greatest Sum Divisible by Three (LC #1262)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8112-b203-fb25beb53a8b"
SLUG    = "greatest_sum_divisible_by_three"

# ─── 1. Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1262,
    pattern="Dynamic Programming",
    subpatterns=["Track Best for Each Mod"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track dp[3] = best sum per remainder mod 3; snapshot before updating to prevent double-use.",
    icon="🟡"
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Build body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the maximum possible sum of elements chosen from ", {}),
        ("nums", {"code": True}),
        (" such that the sum is divisible by three. You may pick any subset (including the empty subset, which sums to 0).", {})
    ])),
    N.para("Constraints: 1 ≤ nums.length ≤ 4×10⁴, 0 ≤ nums[i] ≤ 10⁴."),
    N.divider(),
]

# ── Solution 1: Tabulation ──
blocks += [
    N.h2("Solution 1 — Tabulation / Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the largest subset sum that is divisible by 3. A brute-force check of all 2^n subsets is exponential. The key is: we don't need to track exact sums — we only care about their remainder mod 3."),
        N.h4("What Doesn't Work"),
        N.para("Greedy fails: taking the largest elements first can lock you into a bad remainder. For example, [2,2,2,3]: greedy might pick 3 (rem=0, sum=3) and miss 2+2+2=6 (sum=6, rem=0). We need to consider all states simultaneously."),
        N.h4("The Key Observation"),
        N.para("When you add a number to a subset, the new sum's remainder mod 3 is (old_rem + num%3) % 3. This only depends on the old remainder (0, 1, or 2), not the actual sum. So instead of tracking all possible sums, we track only 3 values: the best sum for each possible remainder."),
        N.h4("Building the Solution"),
        N.para("Maintain dp[3] = [best sum with rem=0, best sum with rem=1, best sum with rem=2]. Start with dp=[0,-inf,-inf] (empty set is valid for rem=0). For each number: snapshot dp, then update each bucket based on transitions. Return dp[0]."),
        N.callout("Analogy: Three bank accounts — one per remainder. Each number transfers money from one account to another (mod shift). Keep only the best balance in each account. Answer = account 0.", "🏦", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def maxSumDivThree(nums):
    dp = [0, float('-inf'), float('-inf')]
    # dp[r] = max sum achievable with sum % 3 == r
    # -inf means "no valid subset with this remainder yet"
    for num in nums:
        new_dp = dp[:]          # CRITICAL: snapshot before updating
        r = num % 3             # this number's remainder mod 3
        for rem in range(3):
            if dp[rem] == float('-inf'):
                continue        # skip impossible states
            new_rem = (rem + r) % 3
            new_dp[new_rem] = max(new_dp[new_rem], dp[rem] + num)
        dp = new_dp             # commit updated state
    return dp[0]                # max sum with remainder 0 = answer
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0, float('-inf'), float('-inf')]", {"code": True}), (" — dp[0]=0 (empty set, rem=0 valid); dp[1]=dp[2]=-∞ (no valid non-zero-remainder subsets yet).", {})])),
    N.para(N.rich([("new_dp = dp[:]", {"code": True}), (" — Snapshot the current state before any updates. Critical to prevent adding the same number twice.", {})])),
    N.para(N.rich([("r = num % 3", {"code": True}), (" — The number's remainder mod 3 (0, 1, or 2). This determines how it shifts each DP bucket.", {})])),
    N.para(N.rich([("for rem in range(3):", {"code": True}), (" — Consider each existing state (0, 1, 2) as a potential 'source' for a transition.", {})])),
    N.para(N.rich([("if dp[rem] == float('-inf'): continue", {"code": True}), (" — Skip impossible states (no valid subset achieves this remainder yet).", {})])),
    N.para(N.rich([("new_rem = (rem + r) % 3", {"code": True}), (" — Adding num shifts the remainder by r, mod 3. E.g., rem=2, r=1 → new_rem=0.", {})])),
    N.para(N.rich([("new_dp[new_rem] = max(new_dp[new_rem], dp[rem] + num)", {"code": True}), (" — Keep the best: skip num (current new_dp value) or include it (old dp[rem] + num).", {})])),
    N.para(N.rich([("dp = new_dp", {"code": True}), (" — Commit the updated state for this number. Ready for the next iteration.", {})])),
    N.para(N.rich([("return dp[0]", {"code": True}), (" — The maximum sum divisible by 3. Always ≥ 0 since dp[0] was initialized to 0.", {})])),
    N.callout("⚠️ Common mistake: initializing dp=[0,0,0] instead of [0,-inf,-inf]. Setting dp[1]=0 falsely claims the empty set has remainder 1 — incorrect. Use -inf for all non-zero remainder buckets.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — Memoization / Top-Down DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with the natural recursive formulation: at each index, either skip the element or take it (shifting the running remainder). Then memoize on (index, running_remainder) to avoid recomputing overlapping subproblems."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes the same (index, remainder) states many times — once per distinct subset path that reaches them. With n=4×10⁴, this is far too slow."),
        N.h4("The Key Observation"),
        N.para("There are only n×3 unique (index, remainder) states. Memoizing ensures each is computed at most once. The recurrence: dp(i, rem) = max(dp(i+1, rem), nums[i] + dp(i+1, (rem+nums[i])%3))."),
        N.h4("Building the Solution"),
        N.para("Use lru_cache on the recursive function. At the base case (i==n), return 0 if rem==0 (accumulated sum is divisible by 3), else -inf. Time O(n×3)=O(n), Space O(n×3)=O(n) for cache + call stack."),
    ]),
    N.h3("Code"),
    N.code("""\
from functools import lru_cache

def maxSumDivThree_memo(nums):
    n = len(nums)

    @lru_cache(maxsize=None)
    def dp(i, rem):
        # dp(i, rem) = max additional sum from nums[i..n) given running remainder rem
        if i == n:
            return 0 if rem == 0 else float('-inf')
        skip = dp(i + 1, rem)
        take = nums[i] + dp(i + 1, (rem + nums[i]) % 3)
        return max(skip, take)

    return dp(0, 0)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("def dp(i, rem):", {"code": True}), (" — State: (index into nums, running remainder of accumulated sum mod 3).", {})])),
    N.para(N.rich([("if i == n: return 0 if rem == 0 else float('-inf')", {"code": True}), (" — Base case: all numbers processed. Valid only if remainder is 0 (subset sum is divisible by 3).", {})])),
    N.para(N.rich([("skip = dp(i + 1, rem)", {"code": True}), (" — Skip nums[i]: pass through without changing the running remainder.", {})])),
    N.para(N.rich([("take = nums[i] + dp(i + 1, (rem + nums[i]) % 3)", {"code": True}), (" — Take nums[i]: add it to the running sum, shifting remainder by nums[i]%3.", {})])),
    N.para(N.rich([("return max(skip, take)", {"code": True}), (" — Always pick the option that maximizes the total sum (with the divisibility constraint enforced at the base case).", {})])),
    N.para(N.rich([("return dp(0, 0)", {"code": True}), (" — Start at index 0 with running remainder 0 (empty set so far).", {})])),
    N.divider(),
]

# ── Why This is DP ──
blocks += [
    N.h2("🧠 Why This is Dynamic Programming"),
    N.h4("Optimal Substructure"),
    N.para("The maximum subset sum with remainder j using nums[0..i] decomposes into: either exclude nums[i] (use optimal answer for nums[0..i-1] at remainder j), or include it (use optimal answer for nums[0..i-1] at the source remainder that maps to j). Each choice only depends on the optimal sub-answers — classic DP."),
    N.h4("Overlapping Subproblems"),
    N.para("Many different subsets lead to the same (index, remainder) state. For example, {3,6} and {9} both reach (index=2, rem=0) if 9 were in the array. We only need to remember the best sum for each (i, rem) state, not which specific elements got us there."),
    N.code("""\
# The Recurrence Relation:
# Let r = num % 3 for the current number.
# For each valid old remainder rem in {0, 1, 2} where dp[rem] > -inf:
#   new_dp[(rem + r) % 3] = max(new_dp[(rem + r) % 3], dp[rem] + num)
#
# State transitions when r=1:  0->1, 1->2, 2->0
# State transitions when r=2:  0->2, 1->0, 2->1
# State transitions when r=0:  0->0, 1->1, 2->2 (no change)
""", "plain text"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsets)", "O(2^n)", "O(n)"],
        ["Memoization (top-down DP)", "O(n)", "O(n)"],
        ["Tabulation (bottom-up DP) ✓", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Track Best for Each Mod — maintain dp[k] = best value per remainder, update via modular transitions with snapshot.", {})])),
    N.callout(
        "When to recognize this pattern: 'Maximize/count subset sum with divisibility constraint', "
        "modular arithmetic limits the effective state space to k remainders, "
        "'sum divisible by k' or 'sum ≡ r (mod k)' appears in constraints.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (modular DP / track best per remainder):"),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), (" (Medium) — 0/1 knapsack tracking achievable sums; identical snapshot pattern. (#416)", {})])),
    N.bullet(N.rich([("Subarray Sum Divisible by K", {"bold": True}), (" (Medium) — Count subarrays with sum div by k; prefix-mod + hash map. (#974)", {})])),
    N.bullet(N.rich([("Make Sum Divisible by P", {"bold": True}), (" (Medium) — Remove smallest subarray so remaining sum div by p; prefix-mod + hash. (#1590)", {})])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), (" (Medium) — Minimize |S1-S2| via achievable subset sums DP; same O(n×target) structure. (#1049)", {})])),
    N.bullet(N.rich([("Coin Change", {"bold": True}), (" (Medium) — Unbounded knapsack; like mod-dp but track exact target reachability. (#322)", {})])),
    N.bullet(N.rich([("Count Vowels Permutation", {"bold": True}), (" (Hard) — DP per valid state transitions; same mod-3-style transition pattern. (#1220)", {})])),
    N.para("These problems share the core technique: compress the state space to a small fixed set (remainders, reachable-sum bits) and track the best value per state through modular transitions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → Track Best for Each Mod)", "📚", "gray_background"),
]

# ── Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended")
