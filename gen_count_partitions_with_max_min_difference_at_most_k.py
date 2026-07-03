"""
gen_count_partitions_with_max_min_difference_at_most_k.py
Notion IN-PLACE update for LeetCode 3117.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c4-bcb8-eac40e0d1731"
SLUG = "count_partitions_with_max_min_difference_at_most_k"

# ── 1. Set page properties ─────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=3117,
    pattern="Monotonic Queue",
    subpatterns=["DP + Monotonic Deque"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Sliding window [left,i] with two monotonic deques gives O(1) max/min; prefix sum on dp gives O(1) range sum for DP transitions.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3. Build body blocks ──────────────────────────────────────
SOL1_CODE = '''\
from collections import deque

def countPartitions(nums: list[int], k: int) -> int:
    MOD = 10**9 + 7
    n = len(nums)
    dp = [0] * (n + 1)        # dp[i] = ways to partition nums[0..i-1]
    dp[0] = 1                  # base: empty prefix has 1 way
    prefix = [0] * (n + 2)    # prefix[i] = sum(dp[0..i-1])
    prefix[1] = 1
    mx_dq = deque()            # decreasing: front = idx of window max
    mn_dq = deque()            # increasing: front = idx of window min
    left = 0
    for i in range(n):
        # Maintain max-deque
        while mx_dq and nums[mx_dq[-1]] <= nums[i]:
            mx_dq.pop()
        mx_dq.append(i)
        # Maintain min-deque
        while mn_dq and nums[mn_dq[-1]] >= nums[i]:
            mn_dq.pop()
        mn_dq.append(i)
        # Shrink window until max - min <= k
        while nums[mx_dq[0]] - nums[mn_dq[0]] > k:
            left += 1
            if mx_dq[0] < left:
                mx_dq.popleft()
            if mn_dq[0] < left:
                mn_dq.popleft()
        # dp[i+1] = sum(dp[left..i]) via prefix
        dp[i + 1] = (prefix[i + 1] - prefix[left]) % MOD
        prefix[i + 2] = (prefix[i + 1] + dp[i + 1]) % MOD
    return dp[n]
'''

SOL2_CODE = '''\
def countPartitions_brute(nums: list[int], k: int) -> int:
    MOD, n = 10**9 + 7, len(nums)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        mn = mx = nums[i - 1]
        for j in range(i - 1, -1, -1):
            mn = min(mn, nums[j])
            mx = max(mx, nums[j])
            if mx - mn > k:
                break
            dp[i] = (dp[i] + dp[j]) % MOD
    return dp[n]
'''

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an integer array ", ("nums", {"code": True}),
        " of length ", ("n", {"code": True}),
        " and a non-negative integer ", ("k", {"code": True}),
        ", return the number of ways to partition ", ("nums", {"code": True}),
        " into one or more contiguous subarrays such that every subarray has (max − min) ≤ k. "
        "Return the count modulo 10⁹+7."
    ])),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — DP + Two Monotonic Deques (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are counting ways to cut an array into contiguous pieces where each piece's value-spread ≤ k. "
               "This is a combinatorial counting problem on partitions — a classic DP setup: "
               "dp[i] = number of valid partitions of the first i elements."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force inner loop: for each ending index i, scan left to find all valid starting points j. "
               "This is O(n) per i → O(n²) total. For n=10⁵ that is 10¹⁰ operations — TLE."),
        N.h4("The Key Observation"),
        N.para("As i grows, the leftmost valid starting point (left) only moves right — it never jumps back. "
               "This is the sliding window property. We do not need to rescan; we just maintain a pointer. "
               "The challenge becomes: how do we know the window [left,i] is valid? We need max−min in O(1)."),
        N.h4("Building the Solution"),
        N.para("(1) Use a max-deque (decreasing values, front = window max) and a min-deque (increasing values, "
               "front = window min). Each element is pushed once and popped at most once per deque → O(n) total. "
               "(2) Once we know the valid window [left,i], dp[i+1] = sum(dp[left..i]). Maintaining a prefix sum "
               "of dp makes this range query O(1). Combine all three → O(n) time, O(n) space."),
        N.callout("Analogy: Think of the deques as two sliding 'scorekeepers' — one tracks the running champion "
                  "(max) and the other tracks the running underdog (min). Whenever they differ by more than k, "
                  "we evict old records from the left until the scoreboard is valid again.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0]*(n+1); dp[0]=1", {"code": True}), " — 1-indexed DP array. dp[i] = ways to partition first i elements. dp[0]=1 is the base case (empty prefix)."])),
    N.para(N.rich([("prefix = [0]*(n+2); prefix[1]=1", {"code": True}), " — prefix[j] = dp[0]+dp[1]+...+dp[j-1]. Allows O(1) range sum of dp values."])),
    N.para(N.rich([("while mx_dq and nums[mx_dq[-1]] <= nums[i]: mx_dq.pop()", {"code": True}), " — Maintain the max-deque in decreasing order of values. An element dominated by nums[i] can never be the max of a future window that includes i."])),
    N.para(N.rich([("mx_dq.append(i)", {"code": True}), " — Push current index. mx_dq is now in decreasing value order; front = index of window max."])),
    N.para(N.rich([("while mn_dq and nums[mn_dq[-1]] >= nums[i]: mn_dq.pop()", {"code": True}), " — Mirror for min. Maintain increasing order; front = index of window min."])),
    N.para(N.rich([("while nums[mx_dq[0]] - nums[mn_dq[0]] > k:", {"code": True}), " — While window invalid: advance left. Evict stale front indices from either deque if they fall below left."])),
    N.para(N.rich([("dp[i+1] = (prefix[i+1] - prefix[left]) % MOD", {"code": True}), " — Sum dp[left..i] in O(1) via prefix difference. All starting positions in [left,i] give valid last-partition choices."])),
    N.para(N.rich([("prefix[i+2] = (prefix[i+1] + dp[i+1]) % MOD", {"code": True}), " — Extend prefix sum to include dp[i+1], ready for future iterations."])),
    N.para(N.rich([("return dp[n]", {"code": True}), " — dp[n] = ways to partition all n elements."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same DP structure but without the sliding window optimisation. For each ending index i, scan all "
               "possible starting points j backwards, updating running max and min until the window becomes invalid."),
        N.h4("What Doesn't Work"),
        N.para("This is correct but O(n²) — suitable only for n ≤ 10³ or for verifying the optimal solution."),
        N.h4("The Key Observation"),
        N.para("The inner loop can break early: as j decreases, max−min is monotone non-decreasing. Once it exceeds k, no smaller j can be valid."),
        N.h4("Building the Solution"),
        N.para("Straightforward nested-loop DP. O(n²) time, O(n) space. Correct but slow."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(n)"],
        ["DP + Two Monotonic Deques", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Queue (Section 6.4 of DSA Guide)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP + Monotonic Deque — sliding window max/min via two deques combined with prefix-sum DP transitions"])),
    N.callout(
        "When to recognise this pattern: (1) Count/optimise partitions of an array with a contiguous-window constraint. "
        "(2) Constraint involves sliding-window max and/or min. "
        "(3) DP recurrence sums over a range of dp values → add a prefix sum. "
        "(4) Left boundary is monotone (only moves right) → deque gives O(1) amortized.",
        "🔎", "green_background"
    ),
    N.para("Sub-pattern verified: Guide Section 6.4 (Monotonic Queue / Deque), entry: 'DP + Monotonic Deque'."),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DP + Monotonic Deque or sliding window max/min):"),
    N.bullet(N.rich([("Sliding Window Maximum (239)", {"bold": True}), " (Hard) — Core monotonic deque pattern; single decreasing deque for sliding max. The building block for this problem."])),
    N.bullet(N.rich([("Jump Game VI (1696)", {"bold": True}), " (Medium) — DP + monotonic deque; find max dp value in a window of size at most k. Identical structural pattern."])),
    N.bullet(N.rich([("Constrained Subsequence Sum (1425)", {"bold": True}), " (Hard) — DP + deque; optimise max of dp values over the last k indices. Direct sibling problem."])),
    N.bullet(N.rich([("Max Value of Equation (1499)", {"bold": True}), " (Hard) — Monotonic deque optimisation on a transformed expression with a window constraint."])),
    N.bullet(N.rich([("Find the Most Competitive Subsequence (1673)", {"bold": True}), " (Medium) — Monotonic stack with size constraint; same deque intuition."])),
    N.bullet(N.rich([("Minimum Number of K Consecutive Bit Flips (995)", {"bold": True}), " (Hard) — Sliding window with deque-based greedy."])),
    N.para("These problems all exploit the monotonic deque invariant: each element is pushed and popped at most once, giving O(n) total deque cost."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6.4 — Monotonic Queue (Deque)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
