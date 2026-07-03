"""
Notion body rebuild for LeetCode #698 — Partition to K Equal Sum Subsets
DP: Bitmask DP (Subset Mask + Current Sum)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81e7-84e6-c38dc4eed33f"
SLUG = "partition_to_k_equal_sum_subsets"

# ── Wipe existing body ──
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} blocks")

def lbl(code_text, explanation):
    """Line-by-line para: code snippet + plain text explanation."""
    return N.para(N.rich([
        (code_text, {"code": True}),
        (" — " + explanation, {}),
    ]))

# ── Build body ──
blocks = []

# ───────────────── Problem ─────────────────
blocks += [
    N.h2("Problem"),
    N.para(
        "Given an integer array nums and an integer k, return True if it is possible to "
        "divide this array into k non-empty subsets whose sums are all equal. "
        "Each element must be assigned to exactly one subset."
    ),
    N.para(
        "Example: nums = [4, 3, 2, 3, 5, 2, 1], k = 4 → True (subsets: [5], [1,4], [2,3], [2,3])"
    ),
    N.para(
        "Constraints: 1 ≤ k ≤ len(nums) ≤ 16, 0 < nums[i] < 10000."
    ),
    N.divider(),
]

# ───────────────── Solution 1 — Bitmask DP (Interview Pick) ─────────────────
blocks += [
    N.h2("Solution 1 — Bitmask DP (Bottom-Up) — Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to partition n elements (n ≤ 16) into k groups each summing to "
            "target = sum/k. A subset of indices can be represented as a bitmask of n bits. "
            "The key question: can we greedily fill one bucket at a time using elements not yet used?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Plain DFS/backtracking without memoization is O(k * 2^n) in the worst case but "
            "recomputes the same 'remaining elements' state multiple times. "
            "For n=16 without pruning or memoization, this TLEs. "
            "The insight: two different orderings of the same subset of picked elements "
            "are equivalent — memoize by WHICH elements have been used (the bitmask)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "dp[mask] = the current running sum within the active (not yet complete) bucket, "
            "given that bits set in 'mask' are the elements already placed. "
            "When the running sum hits 'target', we finish a bucket and reset to 0. "
            "dp[(1<<n)-1] == 0 means all elements are placed and every bucket was perfectly filled."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Compute target = total / k. If not integer or any element > target → False.\n"
            "2. Initialize dp[0] = 0 (no elements used, running sum = 0).\n"
            "3. For each mask from 0 to (1<<n)-1: if dp[mask] is valid (not -1), try adding each "
            "element not yet in mask. New running sum = (dp[mask] + nums[i]) % target. "
            "If reachable, set dp[mask | (1<<i)] = new sum.\n"
            "4. Return dp[(1 << n) - 1] == 0."
        ),
        N.callout(
            "Analogy: Imagine n=16 switches, each ON or OFF. A bitmask is a snapshot of "
            "which switches are on. We build up states by flipping switches (adding elements) "
            "one at a time. dp[mask] tells us: given this exact set of switches is ON, "
            "how full is our current partial bucket? When it reaches target, the bucket "
            "empties and we continue filling the next one.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Bitmask DP Deep-Dive"),
    N.para(
        "Bitmask DP compresses exponential subset spaces into a polynomial-sized DP table. "
        "For n ≤ 20, the number of subsets 2^n is at most ~1M — tractable. "
        "Core invariant: dp[mask] is well-defined only for reachable states "
        "(those reachable by valid element placements). We propagate forward: "
        "for each valid state dp[mask], we extend to dp[mask | (1<<i)] for each unset bit i. "
        "The modular sum dp[mask] % target naturally resets the bucket counter — "
        "no need to track 'how many buckets completed' explicitly."
    ),
    N.h3("Code"),
    N.code(
        "def canPartitionKSubsets(nums, k):\n"
        "    total = sum(nums)\n"
        "    if total % k != 0:\n"
        "        return False\n"
        "    target = total // k\n"
        "    if max(nums) > target:\n"
        "        return False\n"
        "\n"
        "    n = len(nums)\n"
        "    dp = [-1] * (1 << n)   # dp[mask] = running sum in current bucket; -1 = unreachable\n"
        "    dp[0] = 0              # base case: nothing used, running sum = 0\n"
        "\n"
        "    for mask in range(1 << n):\n"
        "        if dp[mask] == -1:\n"
        "            continue       # unreachable state, skip\n"
        "        for i in range(n):\n"
        "            if mask & (1 << i):   # element i already used\n"
        "                continue\n"
        "            nxt = dp[mask] + nums[i]\n"
        "            if nxt > target:\n"
        "                continue       # would overflow current bucket\n"
        "            dp[mask | (1 << i)] = nxt % target  # fill in next state\n"
        "\n"
        "    return dp[(1 << n) - 1] == 0  # all elements used, last bucket exactly filled\n",
        "python"
    ),
    N.h3("Line by Line"),
    lbl("total = sum(nums)", "Sum all elements to know the grand total."),
    lbl("if total % k != 0", "If total isn't divisible by k, equal partition is impossible."),
    lbl("target = total // k", "Each of the k subsets must sum to exactly this value."),
    lbl("if max(nums) > target", "A single element bigger than target can never fit in any subset."),
    lbl("dp = [-1] * (1 << n)", "Allocate 2^n slots. -1 = state not yet reached (unreachable)."),
    lbl("dp[0] = 0", "With zero elements placed, the current bucket running sum is 0."),
    lbl("for mask in range(1 << n)", "Iterate over all 2^n possible subsets from smallest to largest bitmask."),
    lbl("if dp[mask] == -1: continue", "Skip unreachable states — no valid path led here."),
    lbl("if mask & (1 << i)", "Bit i is set means nums[i] already placed; skip it."),
    lbl("nxt = dp[mask] + nums[i]", "Tentatively add nums[i] to the current bucket's running sum."),
    lbl("if nxt > target: continue", "Would overflow the bucket — skip this element."),
    lbl("dp[mask | (1 << i)] = nxt % target",
        "Mark new state: running sum resets to 0 when it hits target (% target), "
        "otherwise keeps the running total. This encodes bucket completion implicitly."),
    lbl("return dp[(1 << n) - 1] == 0",
        "All n bits set = all elements placed. Running sum == 0 means the last bucket "
        "also hit exactly target with no overflow."),
    N.divider(),
]

# ───────────────── Solution 2 — Backtracking + Pruning ─────────────────
blocks += [
    N.h2("Solution 2 — Backtracking with Pruning (DFS)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Try to fill each of the k buckets one at a time. For the current bucket, "
            "search through unused elements and try adding them. When a bucket reaches "
            "target, start filling the next bucket with remaining elements."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without pruning, we would explore O(k^n) orderings. Key pruning tricks: "
            "sort descending (large elements constrain first, fail faster); "
            "if current element equals the previous element and prev was skipped, skip this one too; "
            "skip duplicates at the same recursion level."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two empty buckets are interchangeable. If we fail to fill a bucket starting "
            "with element x at position i, we will also fail with another empty bucket "
            "starting with the same x. Use a visited array or sort+skip duplicate "
            "bucket-start values."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort nums descending. Compute target.\n"
            "2. Recurse: pick elements for the current bucket until it is full.\n"
            "3. When full, recurse for next bucket (k-1 remaining).\n"
            "4. Base case: k == 1 means all remaining elements must sum to target by construction.\n"
            "5. Prune: if current bucket sum + next element > target, or skip duplicate-start."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def canPartitionKSubsets(nums, k):\n"
        "    total = sum(nums)\n"
        "    if total % k != 0:\n"
        "        return False\n"
        "    target = total // k\n"
        "    nums.sort(reverse=True)\n"
        "    if nums[0] > target:\n"
        "        return False\n"
        "    used = [False] * len(nums)\n"
        "\n"
        "    def backtrack(k, bucket_sum, start):\n"
        "        if k == 0:\n"
        "            return True   # all buckets filled\n"
        "        if bucket_sum == target:\n"
        "            return backtrack(k - 1, 0, 0)  # start fresh for next bucket\n"
        "        prev = -1\n"
        "        for i in range(start, len(nums)):\n"
        "            if used[i] or nums[i] + bucket_sum > target:\n"
        "                continue\n"
        "            if nums[i] == prev:   # skip duplicate bucket-start\n"
        "                continue\n"
        "            used[i] = True\n"
        "            if backtrack(k, bucket_sum + nums[i], i + 1):\n"
        "                return True\n"
        "            used[i] = False\n"
        "            prev = nums[i]\n"
        "        return False\n"
        "\n"
        "    return backtrack(k, 0, 0)\n",
        "python"
    ),
    N.h3("Line by Line"),
    lbl("nums.sort(reverse=True)",
        "Descending sort ensures big elements are tried first, pruning impossible branches quickly."),
    lbl("if k == 0: return True", "All k buckets have been exactly filled."),
    lbl("if bucket_sum == target: return backtrack(k-1, 0, 0)",
        "Current bucket is full; start the next one from scratch at index 0."),
    lbl("if nums[i] == prev: continue",
        "Avoid trying the same value twice at the same level — major pruning for duplicate values."),
    lbl("used[i] = True / used[i] = False",
        "Classic backtracking: mark element as used before recursing, unmark on return."),
    N.divider(),
]

# ───────────────── Why DP / Recurrence ─────────────────
blocks += [
    N.h2("🧠 Why is This Dynamic Programming?"),
    N.para(
        "Optimal Substructure: The question 'can remaining elements (given by ~mask) be "
        "partitioned into k - completed_buckets subsets?' depends only on WHICH elements "
        "remain, not the order they were placed. This is substructure."
    ),
    N.para(
        "Overlapping Subproblems: In pure backtracking, the same set of remaining elements "
        "can be reached via many orderings. dp[mask] caches the result for each specific subset, "
        "so each of the 2^n states is computed only once."
    ),
    N.h3("📐 Recurrence Relation"),
    N.code(
        "# dp[mask] = running sum in the currently-being-filled bucket\n"
        "# given that elements with bits set in 'mask' have been placed.\n"
        "#\n"
        "# Base case:\n"
        "dp[0] = 0\n"
        "#\n"
        "# Transition: for each unset bit i in mask\n"
        "#   if dp[mask] + nums[i] <= target:\n"
        "#       dp[mask | (1<<i)] = (dp[mask] + nums[i]) % target\n"
        "#\n"
        "# Answer:\n"
        "dp[(1<<n)-1] == 0\n",
        "python"
    ),
    N.para(
        "The modulo operation is elegant: when the running sum equals exactly target, "
        "(target % target) = 0, meaning the next element starts a fresh bucket automatically. "
        "No need to count buckets — just check whether the final state sum is 0."
    ),
    N.divider(),
]

# ───────────────── Complexity ─────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bitmask DP (Bottom-Up)", "O(n · 2^n)", "O(2^n)"],
        ["Backtracking + Pruning", "O(k · 2^n) worst", "O(n) recursion"],
    ]),
    N.para(
        "Bitmask DP guarantees each of 2^n states is visited at most once. "
        "At each state we try all n elements — O(n * 2^n) total. "
        "Space is the dp table of size 2^n. "
        "Backtracking can be faster in practice due to early termination, "
        "but worst-case is exponential without strong pruning."
    ),
    N.divider(),
]

# ───────────────── Pattern Classification ─────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Subset Mask + Current Sum, DP: Bitmask", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Small n (≤ 20) with exponential subset space\n"
        "• Partition into k groups or cover all elements exactly once\n"
        "• State depends on WHICH elements used, not order\n"
        "• Backtracking recomputes the same remaining-element sets → memoize by mask",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ───────────────── Related Problems ─────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Bitmask DP / Subset DP):"),
    N.bullet(N.rich([
        ("Partition Equal Subset Sum #416", {"bold": True}),
        (" (Medium) — Simpler: 2 subsets, classic 0/1 knapsack bitmask", {}),
    ])),
    N.bullet(N.rich([
        ("Shortest Path Visiting All Nodes #847", {"bold": True}),
        (" (Hard) — Bitmask DP on graph nodes, similar state compression", {}),
    ])),
    N.bullet(N.rich([
        ("Beautiful Arrangement #526", {"bold": True}),
        (" (Medium) — Bitmask DP on permutations", {}),
    ])),
    N.bullet(N.rich([
        ("Maximum Students Taking Exam #1349", {"bold": True}),
        (" (Hard) — Bitmask DP on seating rows", {}),
    ])),
    N.bullet(N.rich([
        ("Campus Bikes II #1066", {"bold": True}),
        (" (Hard) — Bitmask DP on assignment problem", {}),
    ])),
    N.bullet(N.rich([
        ("Minimum XOR Sum of Two Arrays #1879", {"bold": True}),
        (" (Hard) — Bitmask DP on pairing", {}),
    ])),
    N.bullet(N.rich([
        ("Fair Distribution of Cookies #2305", {"bold": True}),
        (" (Medium) — Backtracking on equal distribution, similar structure", {}),
    ])),
    N.para(
        "These problems share the core technique: represent selected elements as a bitmask, "
        "memoize by mask to avoid recomputing the same subset states."
    ),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming) — DP: Bitmask",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ───────────────── Embed ─────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
