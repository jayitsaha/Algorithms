"""
gen_valid_triangle_number.py
Regenerate Notion page for #611 Valid Triangle Number in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8159-b046-ecc2fff3f302"

# ── 1. Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=611,
    pattern="Mathematics & Geometry",
    subpatterns=["Sort + Two Pointers"],
    tc="O(n²)",
    sc="O(1)",
    key_insight="Sort first; fix largest side k and two-pointer the prefix: when left+right>k, count right-left pairs in O(1).",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Build body blocks ────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the number of triplets chosen from the array that can make triangles "
         "if we take them as side lengths of a triangle. A triangle is valid if any two "
         "sides sum to strictly more than the third side.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Sort + Two Pointers (Interview Pick) ──────────────
blocks += [
    N.h2("Solution 1 — Sort + Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count triplets (a, b, c) from the array that satisfy the triangle inequality: a+b>c, a+c>b, b+c>a. Naively, that's three conditions per triplet, and checking all triplets is O(n³)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force — three nested loops checking all C(n,3) triplets — is O(n³). For n=1000 that's 10⁹ operations. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("If we SORT the array so a ≤ b ≤ c, then b+c>a and a+c>b are automatically satisfied (c alone is already ≥ a and ≥ b). Only a+b>c can fail. Three conditions become ONE."),
        N.h4("Building the Solution"),
        N.para("Fix k (largest side, scanning right to left). Use two pointers left=0, right=k-1 on the prefix. If nums[left]+nums[right]>nums[k]: ALL indices from left to right-1 paired with right also satisfy the condition (sorted order guarantees this). Count (right-left) pairs in O(1) and shrink right. Else: nums[left] is too small; advance left. Inner loop is O(n) per k → total O(n²)."),
        N.callout(
            "Analogy: Imagine shopping for a bookcase. You fix the longest plank (k). Two helpers hold planks at opposite ends of the remaining pile. If their combined length exceeds the fixed plank, everyone between them also works — count them all at once and move the right helper inward.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def triangleNumber(nums: list[int]) -> int:\n"
        "    nums.sort()                # O(n log n); reduces 3 conditions to 1\n"
        "    n = len(nums)\n"
        "    count = 0\n"
        "    for k in range(n - 1, 1, -1):  # k = largest side index\n"
        "        left, right = 0, k - 1     # two pointers on prefix\n"
        "        while left < right:\n"
        "            if nums[left] + nums[right] > nums[k]:\n"
        "                count += right - left  # all (left..right-1, right) are valid\n"
        "                right -= 1\n"
        "            else:\n"
        "                left += 1\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}),
                   (" — Sort ascending so nums[i] ≤ nums[j] ≤ nums[k] for i<j<k. Reduces triangle check to one inequality.", {})])),
    N.para(N.rich([("count = 0", {"code": True}),
                   (" — Running total of valid triplets.", {})])),
    N.para(N.rich([("for k in range(n-1, 1, -1)", {"code": True}),
                   (" — k is the index of the LARGEST side. Iterate from n-1 down to 2 (need at least two elements to the left).", {})])),
    N.para(N.rich([("left, right = 0, k - 1", {"code": True}),
                   (" — Two pointers span the entire prefix [0..k-1].", {})])),
    N.para(N.rich([("if nums[left] + nums[right] > nums[k]", {"code": True}),
                   (" — Check if the current pair satisfies the triangle condition.", {})])),
    N.para(N.rich([("count += right - left", {"code": True}),
                   (" — ALL indices from left to right-1 paired with right are valid (sorted monotonicity). Batch count in O(1).", {})])),
    N.para(N.rich([("right -= 1", {"code": True}),
                   (" — This right value's contribution is fully accounted for; shrink inward.", {})])),
    N.para(N.rich([("else: left += 1", {"code": True}),
                   (" — nums[left] is too small even for this right; advancing left increases the sum.", {})])),
    N.para(N.rich([("return count", {"code": True}),
                   (" — Total valid triangles found.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force O(n³) ─────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force O(n³)"),
    N.toggle_h3("💡 Intuition: The Naive Approach", [
        N.h4("Reframe the Problem"),
        N.para("Check every possible triplet directly. After sorting, only one condition needs checking."),
        N.h4("What Doesn't Work (at scale)"),
        N.para("Three nested loops over n elements: O(n³) time. For n=1000, that's ~10⁹ operations — TLE on LeetCode. But useful as a reference implementation to verify the optimized solution."),
        N.h4("The Key Observation"),
        N.para("Even here, sorting first reduces the three triangle inequalities to one (nums[i]+nums[j]>nums[k] for sorted i<j<k), which simplifies the innermost check."),
        N.h4("Building the Solution"),
        N.para("Fix i (smallest), j (middle), k (largest). Check nums[i]+nums[j]>nums[k]. If yes, it's a valid triangle."),
    ]),
    N.h3("Code"),
    N.code(
        "def triangleNumber_brute(nums: list[int]) -> int:\n"
        "    nums.sort()  # still sort so only one condition\n"
        "    count = 0\n"
        "    n = len(nums)\n"
        "    for i in range(n - 2):\n"
        "        for j in range(i + 1, n - 1):\n"
        "            for k in range(j + 1, n):\n"
        "                if nums[i] + nums[j] > nums[k]:\n"
        "                    count += 1\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("Three nested loops", {"bold": True}),
                   (" — i is the smallest element index, j is middle, k is largest. The condition nums[i]+nums[j]>nums[k] is the only one that can fail in sorted order.", {})])),
    N.para(N.rich([("Time: O(n³)", {"bold": True}),
                   (" — C(n,3) triplets, each checked in O(1). Correct but too slow for n > ~300.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (3 loops)", "O(n³)", "O(1)"],
        ["Sort + Two Pointers (optimal)", "O(n²)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Mathematics & Geometry (Section 19 of DSA Guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Sort + Two Pointers", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Count triplets satisfying a geometric/inequality condition. "
        "(2) After sorting, the constraint reduces to a single comparison. "
        "(3) Monotonicity of sorted order allows batch counting — when one pair works, all pairs between them also work.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Two Pointers technique:"),
    N.bullet(N.rich([("3Sum", {"bold": True}),
                     (" (Medium) — Fix one element, two-pointer the rest for a target sum. The classic template for this pattern. (#15)", {})])),
    N.bullet(N.rich([("3Sum Closest", {"bold": True}),
                     (" (Medium) — Same fix-one, two-pointer setup; track minimum difference from target instead of exact match. (#16)", {})])),
    N.bullet(N.rich([("Two Sum II", {"bold": True}),
                     (" (Medium) — The inner two-pointer building block on a sorted array. (#167)", {})])),
    N.bullet(N.rich([("4Sum", {"bold": True}),
                     (" (Medium) — Extends the pattern by fixing two elements; same two-pointer inner loop. (#18)", {})])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}),
                     (" (Medium) — Opposite-direction two pointers on a sorted-ish structure using monotonicity to prune. (#11)", {})])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}),
                     (" (Hard) — Counting pairs satisfying an inequality; merge sort or BIT approach. (#315)", {})])),
    N.para("These problems share the core technique: sort to establish monotonicity, then use two pointers to count or find pairs/triplets in linear or near-linear time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 19 — Mathematics & Geometry, Sub-Pattern: Sort + Two Pointers", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_triangle_number")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks pushed: {len(blocks)}")
