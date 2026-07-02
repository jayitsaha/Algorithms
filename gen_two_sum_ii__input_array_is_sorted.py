"""
gen_two_sum_ii__input_array_is_sorted.py
Update the Notion page for: Two Sum II - Input Array Is Sorted (LC #167)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e5-971a-ed3591b5e534"
SLUG    = "two_sum_ii__input_array_is_sorted"

# ── 1) Properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=167,
    pattern="Two Pointers",
    subpatterns=["Two Pointers (Opposite Direction)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Place pointers at both ends; move the smaller-sum side inward exploiting sorted order.",
    icon="🟡",
)
print("Properties OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────
print("Wiping old page content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ── 3) Rebuild body ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 1-indexed sorted integer array ", {}),
        ("numbers", {"code": True}),
        (" and an integer ", {}),
        ("target", {"code": True}),
        (", find two numbers that add up to ", {}),
        ("target", {"code": True}),
        (" and return their indices as ", {}),
        ("[index1, index2]", {"code": True}),
        (" where ", {}),
        ("1 <= index1 < index2 <= numbers.length", {"code": True}),
        (". Exactly one solution is guaranteed. Must use O(1) extra space.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Two Pointers (Interview Pick)
blocks += [
    N.h2("Solution 1 — Two Pointers · O(n) · Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need two numbers in a sorted array that sum to a target, "
            "using only O(1) extra space. The sorted property is the key constraint "
            "that makes a linear-time constant-space solution possible."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A hash map (as in Two Sum I) would work but costs O(n) extra space — "
            "violating the constraint. Brute force checking every pair is O(n²). "
            "Binary search for each complement is O(n log n)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Start with the smallest (left) and largest (right) elements. "
            "Their sum tells us everything: if it's too small, we need a bigger left; "
            "if too big, we need a smaller right. Each comparison eliminates one element "
            "from further consideration."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Place left=0, right=n-1.\n"
            "2. Compute s = numbers[left] + numbers[right].\n"
            "3a. s == target → return [left+1, right+1] (1-indexed).\n"
            "3b. s < target → left += 1 (need a bigger left value).\n"
            "3c. s > target → right -= 1 (need a smaller right value).\n"
            "4. Repeat until found."
        ),
        N.callout(
            "Analogy: Imagine a balance scale. You put the lightest weight on one side "
            "and the heaviest on the other. Too heavy overall? Swap out the heaviest for the "
            "next-heaviest. Too light? Swap out the lightest for the next-lightest. "
            "You always know which side to adjust.",
            "🧠",
            "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def twoSum(numbers: List[int], target: int) -> List[int]:\n"
        "    left, right = 0, len(numbers) - 1  # start at both ends\n"
        "    while left < right:\n"
        "        s = numbers[left] + numbers[right]\n"
        "        if s == target:\n"
        "            return [left + 1, right + 1]  # 1-indexed\n"
        "        elif s < target:\n"
        "            left += 1   # need bigger left value\n"
        "        else:\n"
        "            right -= 1  # need smaller right value",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("left, right = 0, len(numbers) - 1", {"code": True}),
                   (" — Initialize left at the smallest element (index 0) and right at the largest "
                    "(last index). These are our two candidate pointers.", {})])),
    N.para(N.rich([("while left < right:", {"code": True}),
                   (" — Continue as long as we have two distinct elements to examine. "
                    "If left == right they'd be the same element — can't use one element twice.", {})])),
    N.para(N.rich([("s = numbers[left] + numbers[right]", {"code": True}),
                   (" — Compute the candidate sum for this iteration.", {})])),
    N.para(N.rich([("if s == target: return [left+1, right+1]", {"code": True}),
                   (" — Found the answer. Convert from 0-indexed to 1-indexed before returning.", {})])),
    N.para(N.rich([("elif s < target: left += 1", {"code": True}),
                   (" — Sum is too small. We need a bigger number. Moving left right gives us "
                    "a larger left value (since array is sorted), increasing s.", {})])),
    N.para(N.rich([("else: right -= 1", {"code": True}),
                   (" — Sum is too big. We need a smaller number. Moving right left gives us "
                    "a smaller right value, decreasing s.", {})])),
    N.divider(),
]

# Solution 2 — Binary Search
blocks += [
    N.h2("Solution 2 — Binary Search · O(n log n)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Fix one element (the 'first' of the pair) and binary-search for its complement "
            "in the remaining sorted subarray. Still uses sorted property, but less efficiently."
        ),
        N.h4("What Doesn't Work (as well)"),
        N.para(
            "This approach is correct but O(n log n) instead of O(n). The two-pointer approach "
            "is strictly better because it amortizes to O(1) per element across all iterations."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For each index i, the complement is target - numbers[i]. "
            "We can binary-search for this complement in numbers[i+1..n-1] in O(log n). "
            "Overall: O(n) × O(log n) = O(n log n)."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def twoSum(numbers: List[int], target: int) -> List[int]:\n"
        "    for i, num in enumerate(numbers):\n"
        "        complement = target - num\n"
        "        lo, hi = i + 1, len(numbers) - 1\n"
        "        while lo <= hi:\n"
        "            mid = (lo + hi) // 2\n"
        "            if numbers[mid] == complement:\n"
        "                return [i + 1, mid + 1]\n"
        "            elif numbers[mid] < complement:\n"
        "                lo = mid + 1\n"
        "            else:\n"
        "                hi = mid - 1",
        "python"
    ),
    N.divider(),
]

# Complexity Table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(1)", "Never use in interview"],
        ["Binary Search", "O(n log n)", "O(1)", "Fix one, binary-search for complement"],
        ["Two Pointers ✓", "O(n)", "O(1)", "Optimal — exploits sorted property fully"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Pointers (Opposite Direction)", {})])),
    N.callout(
        "When to recognize this pattern: Sorted array + two elements summing to a target "
        "+ O(1) space constraint. Also triggers for: Container With Most Water (maximize area), "
        "3Sum (fix one, two-pointer the rest), Valid Palindrome (compare from both ends).",
        "🔎",
        "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Two Pointers, Opposite Direction):"),
    N.bullet(N.rich([("Two Sum", {"bold": True}), " (Easy) — Unsorted: use hash map instead (#1)"])),
    N.bullet(N.rich([("3Sum", {"bold": True}), " (Medium) — Fix one element, run two pointers on the rest (#15)"])),
    N.bullet(N.rich([("3Sum Closest", {"bold": True}), " (Medium) — Track minimum distance to target (#16)"])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), " (Medium) — Maximize area; move smaller-height pointer (#11)"])),
    N.bullet(N.rich([("4Sum", {"bold": True}), " (Medium) — Fix two elements, two pointers on the rest (#18)"])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), " (Easy) — Pointers check chars from both ends (#125)"])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Opposite pointers track left/right max water (#42)"])),
    N.para("These problems share the same core technique: converging pointers from opposite ends of a sorted or symmetric structure."),
    N.divider(),
]

# Interactive Visual Explainer
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
