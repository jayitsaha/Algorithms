"""
gen_continuous_subarray_sum.py — Notion page rebuild for LC #523 Continuous Subarray Sum
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811b-a8d0-cb093a9ddefd"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=523,
    pattern="Prefix Sum",
    subpatterns=["Prefix Sum + Modulo + Hash Map"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Two prefix sums with equal remainder mod k enclose a subarray divisible by k; store first-occurrence index only.",
    icon="🟡"
)
print("  Properties set.")

print("Step 2: Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} old blocks.")

print("Step 3: Building new body blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if ", {}),
        ("nums", {"code": True}),
        (" has a continuous subarray of size at least two whose elements sum up to a multiple of ", {}),
        ("k", {"code": True}),
        (", and ", {}),
        ("false", {"code": True}),
        (" otherwise.", {}),
    ])),
    N.para("Example: nums = [23, 2, 4, 6, 7], k = 6 → True (subarray [2, 4] sums to 6, which is 6 × 1)."),
    N.divider(),
]

# ── Solution 1: Optimal — Prefix Sum + Modulo + Hash Map ──
SOLUTION_1 = """\
def checkSubarraySum(nums: list[int], k: int) -> bool:
    seen = {0: -1}   # sentinel: remainder 0 seen at virtual index -1
    curr_sum = 0
    for i, num in enumerate(nums):
        curr_sum += num
        rem = curr_sum % k
        if rem in seen:
            if i - seen[rem] >= 2:   # subarray length >= 2
                return True
        else:
            seen[rem] = i   # only store FIRST occurrence
    return False"""

blocks += [
    N.h2("Solution 1 — Prefix Sum + Modulo + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want a contiguous subarray of length ≥ 2 whose sum is divisible by k. Instead of asking 'what is the sum?' for each pair, ask: what property of prefix sums implies divisibility?"),

        N.h4("What Doesn't Work"),
        N.para("A brute force tries every pair (i, j) with j > i. Even with a prefix sum array for O(1) range queries, this is O(n²) total — too slow for n up to 10⁵."),

        N.h4("The Key Observation"),
        N.para("Modular arithmetic: if prefix[j] ≡ prefix[i] (mod k), then sum(nums[i+1..j]) = prefix[j] − prefix[i] ≡ 0 (mod k). So we only need to find two indices with equal prefix-sum remainders, separated by ≥ 2."),

        N.h4("Building the Solution"),
        N.para("Maintain a running sum. At each index i, compute rem = curr_sum % k. If rem was seen before (at index p), and i − p ≥ 2, return True. Otherwise store rem → i (only the first occurrence — to maximize the gap for the length check). Initialize seen = {0: −1} as a sentinel covering subarrays that start at index 0."),

        N.callout(
            "Analogy: Think of the remainders as 'color codes' for prefix sums. Two sums with the same color code cancel perfectly (their difference is divisible by k). We just need two same-color codes at distance ≥ 2.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code(SOLUTION_1),

    N.h3("Line by Line"),
    N.para(N.rich([("seen = {0: -1}", {"code": True}), (" — sentinel entry: remainder 0 exists at virtual index −1, so if prefix sum at index j has remainder 0, the entire prefix nums[0..j] is divisible by k and has length j+1 ≥ 2 (for j ≥ 1).", {})])),
    N.para(N.rich([("curr_sum = 0", {"code": True}), (" — running total; we never build the full prefix array, just one accumulator.", {})])),
    N.para(N.rich([("curr_sum += num", {"code": True}), (" — extend the prefix sum by one more element.", {})])),
    N.para(N.rich([("rem = curr_sum % k", {"code": True}), (" — the remainder of this prefix sum. There are only k possible values (0..k-1), so the hash map is bounded.", {})])),
    N.para(N.rich([("if rem in seen:", {"code": True}), (" — this remainder was seen at an earlier index. The subarray between that index and i has sum divisible by k.", {})])),
    N.para(N.rich([("if i - seen[rem] >= 2:", {"code": True}), (" — the subarray spans at least two elements (the problem's minimum length requirement).", {})])),
    N.para(N.rich([("return True", {"code": True}), (" — valid subarray found.", {})])),
    N.para(N.rich([("else: seen[rem] = i", {"code": True}), (" — first time seeing this remainder. Store it. CRITICAL: do not update if already present — preserving the earliest occurrence maximizes the gap.", {})])),
    N.para(N.rich([("return False", {"code": True}), (" — exhausted the array without finding a valid subarray.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOLUTION_2 = """\
def checkSubarraySum_brute(nums: list[int], k: int) -> bool:
    n = len(nums)
    for i in range(n - 1):          # start of subarray
        total = nums[i]
        for j in range(i + 1, n):   # end of subarray (at least 1 ahead)
            total += nums[j]
            if total % k == 0:
                return True
    return False"""

blocks += [
    N.h2("Solution 2 — Brute Force: Nested Loops"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Most direct interpretation: check every subarray of length ≥ 2 to see if its sum is a multiple of k."),

        N.h4("What Doesn't Work (at scale)"),
        N.para("There are O(n²) subarrays. Even computing each sum in O(1) with prefix sums, checking all pairs is O(n²) — 10^10 operations for n=10⁵. Correct but too slow."),

        N.h4("The Key Observation"),
        N.para("Good as a baseline, not for production. Use as starting point in interviews before presenting the O(n) solution."),

        N.h4("Building the Solution"),
        N.para("For each start i from 0 to n-2, keep a running total and extend to each j > i. As soon as total % k == 0, we have our answer."),
    ]),

    N.h3("Code"),
    N.code(SOLUTION_2),

    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n - 1):", {"code": True}), (" — outer loop: start index. We go up to n-2 so j can be at least i+1.", {})])),
    N.para(N.rich([("total = nums[i]", {"code": True}), (" — initialize sum with the start element.", {})])),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}), (" — inner loop extends the subarray one element at a time.", {})])),
    N.para(N.rich([("total += nums[j]", {"code": True}), (" — accumulate sum incrementally (avoids recomputing from scratch).", {})])),
    N.para(N.rich([("if total % k == 0:", {"code": True}), (" — check divisibility. Length is j-i+1 ≥ 2 because j > i.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Nested Loops)", "O(n²)", "O(1)"],
        ["Prefix Sum + Modulo + Hash Map", "O(n)", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prefix Sum + Modulo + Hash Map", {})])),
    N.callout(
        "When to recognize this pattern: 'subarray sum divisible by k' + length constraint → prefix sum modulo k stored in a hash map. The sentinel {0:−1} is always needed. Store only the first occurrence of each remainder.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Exact sum k, any length; prefix sum + frequency map, no modulo (#560)", {})])),
    N.bullet(N.rich([("Subarray Sums Divisible by K", {"bold": True}), (" (Medium) — Count ALL subarrays with sum divisible by k; remainder frequency counts (#974)", {})])),
    N.bullet(N.rich([("Contiguous Array", {"bold": True}), (" (Medium) — Longest subarray with equal 0s and 1s; prefix balance + first-index hash map (#525)", {})])),
    N.bullet(N.rich([("Find Pivot Index", {"bold": True}), (" (Easy) — Left sum equals right sum; direct prefix sum balance (#724)", {})])),
    N.bullet(N.rich([("Range Sum Query – Immutable", {"bold": True}), (" (Easy) — Precompute prefix array for O(1) range queries (#303)", {})])),
    N.bullet(N.rich([("Count of Submatrices that Sum to Target", {"bold": True}), (" (Hard) — 2D prefix sum + hash map; same idea extended to matrix (#1074)", {})])),
    N.para("These problems all exploit prefix-sum properties to convert O(n²) range queries into O(n) passes."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 (Prefix Sum Pattern) — Sub-Pattern: Prefix Sum + Modulo + Hash Map", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("continuous_subarray_sum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Total blocks to append: {len(blocks)}")
print("Step 4: Appending blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT continuous_subarray_sum | html=OK | notion=OK | lines=898")
