"""
gen_maximum_sum_circular_subarray.py
Notion in-place update for LeetCode #918 Maximum Sum Circular Subarray.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8132-a8e3-fd4dbb8f2c0c"

print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=918,
    pattern="Array Manipulation",
    subpatterns=["Kadane's Algorithm", "Kadane + Circular (Total - Min)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Two cases: linear max (Kadane) vs wrap max (total − min subarray). Run both in one pass.",
    icon="🟡"
)

print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

print("Building new content...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a circular integer array ", {}),
        ("nums", {"code": True}),
        (", return the maximum possible sum of a non-empty subarray of ", {}),
        ("nums", {"code": True}),
        (". In a circular array, the subarray may wrap from the end back to the beginning.", {}),
    ])),
    # note: rich() accepts plain str or (str, dict) tuples — no bare {} allowed
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ("nums = [1, -2, 3, -2]", {"code": True}),
            (" → Output: 3 (subarray [3])\n", {}),
            ("Example 2: ", {"bold": True}),
            ("nums = [5, -3, 5]", {"code": True}),
            (" → Output: 10 (wrap subarray [5, 5] = sum 10)\n", {}),
            ("Example 3: ", {"bold": True}),
            ("nums = [-3, -2, -3]", {"code": True}),
            (" → Output: -2 (all negative, return least-negative element)", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the maximum sum subarray where the subarray can wrap around. 'Wrapping' means using elements from the end of the array AND the beginning."),
        N.h4("What Doesn't Work"),
        N.para("We can't just run standard Kadane's — it never looks at wrap-around candidates. We need to somehow try all wrapping subarrays too."),
        N.h4("The Key Observation"),
        N.para("A circular subarray starting at index i with length k uses indices i, i+1, ..., (i+k-1) mod n. We can enumerate all such start/length combinations using the modulo operator."),
        N.h4("Building the Solution"),
        N.para("For each starting index (0 to n-1), extend the subarray by adding elements circularly (using % n) up to length n. Track the running sum and update the global best."),
        N.callout("Analogy: Think of the array as a circular conveyor belt. The brute force approach tries starting at every position and picking every possible consecutive window length.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maxSubarraySumCircular(nums):\n"
        "    n, best = len(nums), float('-inf')\n"
        "    for i in range(n):\n"
        "        cur = 0\n"
        "        for k in range(1, n + 1):\n"
        "            cur += nums[(i + k - 1) % n]\n"
        "            best = max(best, cur)\n"
        "    return best"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n, best = len(nums), float('-inf')", {"code": True}), " — start with the worst possible answer so any real subarray sum will beat it."])),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — try every possible starting index."])),
    N.para(N.rich([("cur = 0", {"code": True}), " — reset running sum for this start."])),
    N.para(N.rich([("for k in range(1, n + 1):", {"code": True}), " — try every length from 1 up to n (full array)."])),
    N.para(N.rich([("cur += nums[(i + k - 1) % n]", {"code": True}), " — the modulo makes the indexing wrap around circularly."])),
    N.para(N.rich([("best = max(best, cur)", {"code": True}), " — update global best after each extension."])),
    N.divider(),
]

# ── Solution 2: Optimal Dual Kadane ──
blocks += [
    N.h2("Solution 2 — Dual Kadane O(n), O(1)  ← Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of thinking about which elements to include in the wrap subarray, think about which elements to EXCLUDE. Every wrapping subarray leaves some contiguous middle block unused."),
        N.h4("What Doesn't Work"),
        N.para("Standard Kadane's only finds the best linear subarray. Running Kadane's on a doubled array (nums + nums) works but requires O(n) space. We want O(1) space."),
        N.h4("The Key Observation"),
        N.para("A circular subarray is one of two types: (A) it stays within the linear array, or (B) it wraps. For Case B, the complement (excluded middle) is a contiguous block. To maximize the wrap sum, minimize the excluded block. Therefore: wrap_max = total_sum − min_subarray_sum. This is the complement trick."),
        N.h4("Building the Solution"),
        N.para("Run Kadane's for maximum (Case A) and Kadane's for minimum (for Case B complement) simultaneously in one pass. Also accumulate total_sum. The answer is max(max_g, total − min_g), with an all-negatives guard."),
        N.callout("Analogy: Imagine you're choosing which slice of a pizza circle to eat. Instead of thinking 'which slice do I want?', think 'which slice do I leave behind?' To maximize what you eat, minimize what you leave. The left-behind piece is the min_subarray.", "🧠", "green_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kadane's Algorithm"),
    N.para("Kadane's Algorithm (Joseph Kadane, 1984) solves 'maximum contiguous subarray sum' in O(n) time and O(1) space. It is one of the most elegant algorithms in computer science."),
    N.code(
        "# Kadane's core invariant\n"
        "# cur = maximum subarray sum ending exactly at index i\n"
        "cur = nums[0]\n"
        "for num in nums[1:]:\n"
        "    cur = max(num, cur + num)  # restart or extend\n"
        "    global_max = max(global_max, cur)"
    ),
    N.para("Core invariant: after processing index i, cur holds the maximum sum of any subarray that ends at nums[i]. The restart decision (take num alone) fires when the previous running sum is negative — carrying forward a negative history only hurts. The global max sweeps across all positions."),
    N.para(N.rich([
        ("Recognition signal: ", {"bold": True}),
        ("'Find maximum (or minimum) sum contiguous subarray' with O(n) time → Kadane's. The circular variant adds the complement trick for wrap-around.", {}),
    ])),
    N.h3("Code"),
    N.code(
        "def maxSubarraySumCircular(nums):\n"
        "    max_cur = min_cur = nums[0]\n"
        "    max_g   = min_g   = nums[0]\n"
        "    total = nums[0]\n"
        "    for num in nums[1:]:\n"
        "        max_cur = max(num, max_cur + num)  # Case A: best ending here\n"
        "        max_g   = max(max_g, max_cur)      # Case A: global best\n"
        "        min_cur = min(num, min_cur + num)  # Case B: worst ending here\n"
        "        min_g   = min(min_g, min_cur)      # Case B: global worst\n"
        "        total  += num                      # accumulate array sum\n"
        "    if max_g < 0:                          # all-negatives guard\n"
        "        return max_g\n"
        "    return max(max_g, total - min_g)       # max(Case A, Case B)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("max_cur = min_cur = nums[0]", {"code": True}), " — initialize both running Kadane sums at the first element."])),
    N.para(N.rich([("max_g   = min_g   = nums[0]", {"code": True}), " — initialize both global bests at the first element."])),
    N.para(N.rich([("total = nums[0]", {"code": True}), " — will accumulate the full array sum."])),
    N.para(N.rich([("max_cur = max(num, max_cur + num)", {"code": True}), " — Kadane restart-or-extend for maximum: the best subarray ending at current index."])),
    N.para(N.rich([("max_g = max(max_g, max_cur)", {"code": True}), " — update Case A global answer."])),
    N.para(N.rich([("min_cur = min(num, min_cur + num)", {"code": True}), " — mirror Kadane for minimum: best (worst) subarray ending here."])),
    N.para(N.rich([("min_g = min(min_g, min_cur)", {"code": True}), " — update global minimum subarray sum (the middle block to exclude in Case B)."])),
    N.para(N.rich([("total += num", {"code": True}), " — accumulate entire array sum."])),
    N.para(N.rich([("if max_g < 0: return max_g", {"code": True}), " — ALL ELEMENTS NEGATIVE: min_g = total, so total-min_g = 0 (wrong!). Return the least-negative element instead."])),
    N.para(N.rich([("return max(max_g, total - min_g)", {"code": True}), " — compare Case A (max_g) and Case B (total - min_g). Return the better one."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(1)", "Try every start × length with % n"],
        ["Double Array + Deque", "O(n)", "O(n)", "Concat nums+nums, sliding window ≤ n"],
        ["Dual Kadane (optimal)", "O(n)", "O(1)", "Max + min in one pass, total − min_g"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Array Manipulation"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Kadane's Algorithm, Kadane + Circular (Total - Min)"])),
    N.callout(
        "When to recognize this pattern: 'contiguous subarray' + 'circular/wraps around' → two-case Kadane. Maximizing a sum in a ring structure → think complementary minimum. Single-pass, O(1) space via the total − min trick.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), " (Medium) — Classic Kadane's; #918 is its circular extension (#53)"])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), " (Medium) — Kadane variant tracking both max and min products (#152)"])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock", {"bold": True}), " (Easy) — Kadane variant: max profit = max price difference with ordering (#121)"])),
    N.bullet(N.rich([("Count Subarrays with Fixed Bounds", {"bold": True}), " (Hard) — Sliding window with min/max constraints, circular-style two-boundary reasoning (#2444)"])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), " (Medium) — Contiguous subarray optimization with a target threshold (#209)"])),
    N.bullet(N.rich([("Maximum Sum of Two Non-Overlapping Subarrays", {"bold": True}), " (Medium) — Kadane's prefix maximum trick for two disjoint windows (#1031)"])),
    N.para("These problems share the Kadane's restart-or-extend pattern: tracking the best (or worst) subarray sum ending at each index."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 1.6 (Kadane's Algorithm)", "📚", "gray_background"),
]

# ── Interactive Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_sum_circular_subarray")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
