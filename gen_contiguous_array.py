"""gen_contiguous_array.py — Notion page for LC #525 Contiguous Array."""
import sys
sys.path.insert(0, "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms")
import notion_lib as N

# ── Step 0: Page was already created in prior run ──
PAGE_ID = "39193418-809c-8125-b380-c24841f228bb"
print("Using existing page:", PAGE_ID)

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=525,
    pattern="Array Manipulation",
    subpatterns=["Transform 0 to -1", "Prefix Sum + Hash Map"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Replace 0 with -1; equal 0s and 1s becomes subarray sum 0; use prefix sum + hash map storing first index of each prefix sum.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe (fresh page — nothing to wipe, but safe to call) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks (expected 0 for new page).")

# ── Step 3: Build body blocks ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary array ", {}),
        ("nums", {"code": True}),
        (", return the maximum length of a contiguous subarray with an equal number of 0s and 1s.", {})
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("nums = [0, 1]", {"code": True}),
        (" → output ", {}),
        ("2", {"code": True}),
        (" (the entire array has one 0 and one 1).", {})
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("nums = [0, 1, 0]", {"code": True}),
        (" → output ", {}),
        ("2", {"code": True}),
        (" (either [0,1] or [1,0]).", {})
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ nums.length ≤ 10⁵, nums[i] is 0 or 1.", {})
    ])),
    N.divider()
]

# Solution 1 — Optimal
sol1_code = """\
def findMaxLength(nums):
    seen = {0: -1}           # prefix sum 0 was "seen" before the array starts
    prefix = 0               # running sum: 1 → +1, 0 → -1
    best = 0                 # track longest balanced subarray length
    for i, num in enumerate(nums):
        prefix += 1 if num == 1 else -1   # apply 0→-1 transform inline
        if prefix in seen:                # same prefix seen before!
            best = max(best, i - seen[prefix])  # subarray from seen[prefix]+1 to i
        else:
            seen[prefix] = i             # store FIRST occurrence only
    return best
"""

blocks += [
    N.h2("Solution 1 — Prefix Sum + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest subarray where count(0s) == count(1s). Position doesn't matter — only the balance between 0s and 1s matters."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all pairs (i, j) and count 0s and 1s in each range — O(n²) time. Too slow for n up to 10⁵. Even with prefix sums to check any range in O(1), enumerating all pairs is still O(n²)."),
        N.h4("The Key Observation"),
        N.para("Replace every 0 with −1. Now 'equal 0s and 1s' becomes 'subarray sum = 0' (each −1 cancels a +1). This transforms the problem into the classic 'subarray sum equals K' pattern with K = 0."),
        N.h4("Building the Solution"),
        N.para("Track a running prefix sum. If the same prefix sum appears at index j and later at index k, then sum(j+1..k) = prefix[k] − prefix[j] = 0 — that subarray is balanced. Store the FIRST index of each prefix sum in a hash map so we always get the longest possible subarray. Add sentinel {0: -1} to handle balanced subarrays starting at index 0."),
        N.callout("Analogy: Imagine walking right on a number line. Seeing a 1 steps right (+1), a 0 steps left (−1). If you're ever at the same position you stood before, the path in between was perfectly balanced.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = {0: -1}", {"code": True}), (" — Sentinel: prefix sum 0 'was seen' before the array, at virtual index −1. Enables balanced subarrays starting at index 0.", {})])),
    N.para(N.rich([("prefix = 0", {"code": True}), (" — Running sum. We'll add +1 for each 1 and −1 for each 0.", {})])),
    N.para(N.rich([("best = 0", {"code": True}), (" — Tracks the maximum balanced subarray length seen so far.", {})])),
    N.para(N.rich([("prefix += 1 if num == 1 else -1", {"code": True}), (" — Apply the 0→−1 transform on the fly; no need to build a new array.", {})])),
    N.para(N.rich([("if prefix in seen:", {"code": True}), (" — This prefix sum was recorded at an earlier index. The subarray between then and now sums to zero.", {})])),
    N.para(N.rich([("best = max(best, i - seen[prefix])", {"code": True}), (" — Length = current index − first-seen index. Not +1 because seen[prefix] is the index before the subarray.", {})])),
    N.para(N.rich([("seen[prefix] = i", {"code": True}), (" — Only record first occurrence. If overwritten with a later index, future matches would yield shorter subarrays.", {})])),
    N.divider()
]

# Solution 2 — Brute Force
sol2_code = """\
def findMaxLength_brute(nums):
    n, best = len(nums), 0
    for i in range(n):           # try every starting index
        zeros = ones = 0
        for j in range(i, n):   # extend window one step at a time
            if nums[j] == 0:
                zeros += 1
            else:
                ones += 1
            if zeros == ones:    # balanced subarray found
                best = max(best, j - i + 1)
    return best
"""

blocks += [
    N.h2("Solution 2 — Brute Force (Start Here, Then Optimize)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Count 0s and 1s in every possible subarray. Return the length of the longest one where both counts match."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) and exceeds time limits for n = 10⁵. But it's the right starting point to propose before optimizing."),
        N.h4("The Key Observation"),
        N.para("There are O(n²) subarrays. For each we can maintain running counts in O(1) per step. The outer loop fixes the start, the inner loop extends the right boundary."),
        N.h4("Building the Solution"),
        N.para("For each starting index i, reset counts to 0. Extend j from i to n-1, counting 0s and 1s. Whenever zeros == ones, update best."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Outer loop: try every possible starting index.", {})])),
    N.para(N.rich([("zeros = ones = 0", {"code": True}), (" — Reset counts for this starting index.", {})])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), (" — Inner loop: extend window right one element at a time.", {})])),
    N.para(N.rich([("if zeros == ones:", {"code": True}), (" — Current window is balanced — record its length.", {})])),
    N.divider()
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Prefix Sum + Hash Map", "O(n)", "O(n)"],
    ]),
    N.divider()
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Transform 0 to -1, Prefix Sum + Hash Map", {})])),
    N.callout(
        "When to recognize this pattern: binary array + 'equal count of two values' + 'longest subarray' → always try 0→−1 transform then prefix sum + hash map. Also applies when the problem asks for 'subarray sum = K' with longest length.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Prefix Sum + Hash Map):"),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Identical structure, any target K, not just 0. LC #560", {})])),
    N.bullet(N.rich([("Maximum Size Subarray Sum Equals k", {"bold": True}), (" (Medium) — Longest subarray with sum k; exact same hash map trick. LC #325", {})])),
    N.bullet(N.rich([("Binary Subarrays with Sum", {"bold": True}), (" (Medium) — Count binary subarrays with target sum; 0→−1 helps. LC #930", {})])),
    N.bullet(N.rich([("Count Number of Nice Subarrays", {"bold": True}), (" (Medium) — Odd numbers as 1, evens as 0, prefix sum approach. LC #1248", {})])),
    N.bullet(N.rich([("Continuous Subarray Sum", {"bold": True}), (" (Medium) — Prefix sum modulo K, store remainder in map. LC #523", {})])),
    N.bullet(N.rich([("Find Pivot Index", {"bold": True}), (" (Easy) — Prefix sum from both sides; same balance invariant. LC #724", {})])),
    N.para("These problems share the same core technique: transform the constraint, track prefix sums, use a hash map to record first-seen positions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 (Array Manipulation → Prefix Sum Pattern). Sub-Pattern: Transform 0 to -1, Prefix Sum + Hash Map. Source: Guide Section 1.3", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("contiguous_array")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
