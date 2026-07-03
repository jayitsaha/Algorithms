"""gen_partition_equal_subset_sum.py — Notion page rebuild for LC #416."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8185-8753-cd8d2e027394"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=416,
    pattern="Dynamic Programming",
    subpatterns=["Subset Sum to Half", "DP: 0/1 Knapsack"],
    tc="O(n × sum/2)",
    sc="O(sum/2)",
    key_insight="Reframe: find any subset summing to total//2 using 0/1 knapsack DP with right-to-left update.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing body
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# 3) Build new body
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if you can partition the array into two subsets such that the sum of elements in both subsets is equal.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP Tabulation / Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If two subsets have equal sum, each must equal total/2. So: can any subset sum to exactly target = total // 2? This converts the partition question into the classic Subset Sum problem."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (sort descending, assign to lighter group) fails — early greedy choices foreclose valid later options. Brute force (try all 2^n subsets) is correct but O(2^n), timing out for n=200."),
        N.h4("The Key Observation"),
        N.para("In the brute-force recursion tree, many branches ask 'can I reach sum j using items i..n?' for the same (i, j) pairs — overlapping subproblems. DP avoids recomputation. State: (item index, remaining budget). At most n × target unique states."),
        N.h4("Building the Solution"),
        N.para("Use a 1D boolean DP array dp[0..target]. dp[j]=True means 'some subset of processed items sums to j.' Base: dp[0]=True. For each item num, scan j right-to-left: dp[j] |= dp[j-num]. Right-to-left enforces each item is used at most once (0/1 constraint)."),
        N.callout("Analogy: Packing a backpack one item at a time. For each item, scan from heaviest slot downward — if slot (j-weight) was fillable before, slot j is now fillable by adding this item. Scanning backwards prevents counting the same item twice.", "🎒", "blue_background"),
    ]),
    N.h3("🔬 Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("dp[j] after k items depends only on dp[j] and dp[j-num] from after k-1 items. Today's answer builds on yesterday's.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Naive recursion asks 'can I reach j from index i?' exponentially often. With n=20 items, 2^20 > 1M calls; many are identical. DP computes each (i, j) exactly once.", {}),
    ])),
    N.h3("📐 Recurrence Relation"),
    N.code(
        "dp[j] = dp[j] OR dp[j - num]   # after processing item num\n"
        "\n"
        "Base cases:\n"
        "  dp[0] = True   # empty subset always sums to 0\n"
        "  dp[j] = False  # for j > 0, before any items processed\n"
        "\n"
        "Answer: dp[target]  where target = sum(nums) // 2",
        "python"
    ),
    N.h3("Code"),
    N.code(
        "def canPartition(nums):\n"
        "    total = sum(nums)\n"
        "    if total % 2 != 0:\n"
        "        return False\n"
        "    target = total // 2\n"
        "    dp = [False] * (target + 1)\n"
        "    dp[0] = True\n"
        "    for num in nums:\n"
        "        for j in range(target, num - 1, -1):  # RIGHT-TO-LEFT!\n"
        "            dp[j] |= dp[j - num]\n"
        "        if dp[target]:\n"
        "            return True\n"
        "    return dp[target]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("total = sum(nums)", {"code": True}), " — Compute total sum once in O(n)."])),
    N.para(N.rich([("if total % 2 != 0: return False", {"code": True}), " — Odd total means no integer halves exist. O(1) early exit."])),
    N.para(N.rich([("target = total // 2", {"code": True}), " — We need to find exactly this sum in a subset."])),
    N.para(N.rich([("dp = [False] * (target + 1)", {"code": True}), " — Boolean array: dp[j] = 'can we make sum j?'"])),
    N.para(N.rich([("dp[0] = True", {"code": True}), " — Base case: the empty subset always achieves sum 0."])),
    N.para(N.rich([("for num in nums:", {"code": True}), " — Process each item exactly once (the '0/1' in 0/1 knapsack)."])),
    N.para(N.rich([("for j in range(target, num - 1, -1):", {"code": True}), " — RIGHT-TO-LEFT scan. Stops at j=num (can't place item in smaller slot)."])),
    N.para(N.rich([("dp[j] |= dp[j - num]", {"code": True}), " — If sum j-num was reachable before, sum j is now reachable by adding num."])),
    N.para(N.rich([("if dp[target]: return True", {"code": True}), " — Early exit: once target is reachable, no need to process more items."])),
    N.callout(
        "⚠️ Why right-to-left? If we scanned left-to-right, dp[j-num] might already reflect the current item (used twice). Right-to-left ensures dp[j-num] still holds the pre-item state.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization ──
blocks += [
    N.h2("Solution 2 — Memoization / Top-Down"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same reframe: find subset summing to target. Express as recursion: 'from index i with remaining budget rem, can we reach 0?' Natural to write recursively."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion (no cache) is O(2^n). At each item we branch: skip or take. The call tree doubles at each level."),
        N.h4("The Key Observation"),
        N.para("Many sub-calls repeat the same (i, remaining) state. Cache results to avoid recomputation. Each unique state is computed once: O(n × target) total."),
        N.h4("Building the Solution"),
        N.para("Define dp(i, rem): 'can we reach rem=0 using items i..n-1?' Base: rem=0→True, rem<0 or i=n→False. Cache (i, rem). Return dp(i+1, rem) OR dp(i+1, rem-nums[i])."),
    ]),
    N.h3("Code"),
    N.code(
        "def canPartition(nums):\n"
        "    total = sum(nums)\n"
        "    if total % 2 != 0:\n"
        "        return False\n"
        "    target = total // 2\n"
        "    memo = {}\n"
        "    def dp(i, rem):\n"
        "        if rem == 0:\n"
        "            return True\n"
        "        if rem < 0 or i == len(nums):\n"
        "            return False\n"
        "        if (i, rem) in memo:\n"
        "            return memo[(i, rem)]\n"
        "        result = (dp(i + 1, rem) or\n"
        "                  dp(i + 1, rem - nums[i]))\n"
        "        memo[(i, rem)] = result\n"
        "        return result\n"
        "    return dp(0, target)",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), " — Cache mapping (index, remaining) → bool. Avoids recomputing identical subproblems."])),
    N.para(N.rich([("if rem == 0: return True", {"code": True}), " — Hit target exactly! This branch of the recursion succeeded."])),
    N.para(N.rich([("if rem < 0 or i == len(nums): return False", {"code": True}), " — Overshot budget, or ran out of items. Dead end."])),
    N.para(N.rich([("if (i, rem) in memo: return memo[(i, rem)]", {"code": True}), " — Cache hit: we already know the answer for this state."])),
    N.para(N.rich([("result = dp(i+1, rem) or dp(i+1, rem-nums[i])", {"code": True}), " — Try both decisions: skip nums[i] (rem unchanged) or take it (rem reduced by nums[i])."])),
    N.para(N.rich([("memo[(i, rem)] = result", {"code": True}), " — Store before returning so future calls reuse this answer."])),
    N.divider(),
]

# ── Solution 3: Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force Backtracking (Understand, Don't Submit)"),
    N.h3("Code"),
    N.code(
        "def canPartition(nums):\n"
        "    total = sum(nums)\n"
        "    if total % 2: return False\n"
        "    target = total // 2\n"
        "    def bt(i, rem):\n"
        "        if rem == 0: return True\n"
        "        if rem < 0 or i == len(nums): return False\n"
        "        return bt(i + 1, rem) or bt(i + 1, rem - nums[i])  # O(2^n)\n"
        "    return bt(0, target)",
        "python"
    ),
    N.para("Same recursion as memoization but without any cache. At each of n items we branch 2 ways → 2^n leaf nodes. TLE for n > 25. Provided only to illustrate why memoization/tabulation is necessary."),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Backtracking)", "O(2^n)", "O(n)"],
        ["Memoization (Top-Down)", "O(n × sum/2)", "O(n × sum/2)"],
        ["Tabulation (Bottom-Up) ✓", "O(n × sum/2)", "O(sum/2)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP: 0/1 Knapsack — specifically the Subset Sum to Half variant"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Can a subset reach exactly sum X?' → 0/1 Knapsack (boolean dp)\n"
        "• Each element used at most once + capacity/budget constraint\n"
        "• State = (item index, remaining capacity): O(n × capacity) unique states\n"
        "• Right-to-left inner loop = 0/1 (each item once). Left-to-right = unbounded.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 0/1 Knapsack technique:"),
    N.bullet(N.rich([("Target Sum", {"bold": True}), " (Medium) — Count ways to assign +/- to reach target; same DP but count not boolean (#494)"])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), " (Medium) — Minimize |A-B|; find largest dp[j]=True for j≤total/2 (#1049)"])),
    N.bullet(N.rich([("Ones and Zeroes", {"bold": True}), " (Medium) — 2D knapsack: capacity is (zeros-count, ones-count); right-to-left on both dims (#474)"])),
    N.bullet(N.rich([("Coin Change", {"bold": True}), " (Medium) — Unbounded knapsack: items reusable → LEFT-to-right; compare/contrast with this problem (#322)"])),
    N.bullet(N.rich([("Number of Subsets with Target Sum", {"bold": True}), " (Medium) — Same structure but dp[j] += dp[j-num] (count, not boolean)"])),
    N.bullet(N.rich([("0/1 Knapsack (classic)", {"bold": True}), " (Hard) — Maximize value within weight; 2D or 1D rolling array, same right-to-left pattern"])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}), " (Medium) — Count ordered combos; left-to-right (items reusable); instructive contrast (#377)"])),
    N.para("These problems share the core recurrence: dp[j] = f(dp[j], dp[j-item]) iterated right-to-left for 0/1, left-to-right for unbounded."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming) → DP: 0/1 Knapsack", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("partition_equal_subset_sum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
