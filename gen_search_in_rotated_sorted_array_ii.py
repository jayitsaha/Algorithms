"""
gen_search_in_rotated_sorted_array_ii.py
Notion update script for LeetCode #81 — Search in Rotated Sorted Array II
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8132-bc38-ee826bf7f4b3"
SLUG = "search_in_rotated_sorted_array_ii"

print(f"Setting properties for page {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=81,
    pattern="Binary Search",
    subpatterns=["BS: Rotated Array", "Handle Duplicates"],
    tc="O(log n) avg / O(n) worst",
    sc="O(1)",
    key_insight="Identify sorted half each iteration; when nums[lo]==nums[mid]==nums[hi] shrink both ends by 1.",
    icon="🟡"
)
print("Properties set.")

print("Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

print("Building new page body...")
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" sorted in non-decreasing order, which is then possibly rotated at an unknown pivot index, and an integer ", {}),
        ("target", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if ", {}),
        ("target", {"code": True}),
        (" exists in ", {}),
        ("nums", {"code": True}),
        (" and ", {}),
        ("false", {"code": True}),
        (" otherwise. The array may contain duplicates.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [2,5,6,0,0,1,2], target = 0 → true", {"code": True}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("nums = [2,5,6,0,0,1,2], target = 3 → false", {"code": True}),
    ])),
    N.callout(
        "Key constraint: the array may contain duplicates, which prevents always guaranteeing O(log n) — unlike #33 (no duplicates).",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 1 — Modified Binary Search ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Modified Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find a target in a sorted array that has been 'wrapped around' at a pivot. Standard binary search requires a fully sorted array. Here we have two sorted halves, plus the complication of duplicates."),
        N.h4("What Doesn't Work"),
        N.para("Naive binary search fails because we can't always tell whether to go left or right. In [1,1,1,3,1], with mid pointing to 1, we have no way of knowing whether 3 is to the left or right. We can't blindly go to whichever half is 'larger.'"),
        N.h4("The Key Observation"),
        N.para("After rotation, ANY window [lo, hi] must have at least one fully sorted half — unless all three of nums[lo], nums[mid], nums[hi] are equal (the duplicate ambiguity). When we can identify the sorted half, we check if the target's value falls within that half's range. If yes, search there. If no, search the other half."),
        N.h4("Building the Solution"),
        N.para("1) Compute mid. 2) If nums[mid] == target, done. 3) NEW CASE: if nums[lo]==nums[mid]==nums[hi], can't determine which side is sorted — shrink both ends by 1 (safe because those values equal nums[mid] which is not target). 4) Otherwise, check which half is sorted and whether target belongs there."),
        N.callout(
            "Analogy: Imagine searching for a name in a phone book that was torn and reassembled in two chunks. You can always tell which chunk is sorted by checking if the first page comes before the last page. But if all three pages you're looking at say the same name, you need to peek one page inward from each side.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def search(nums: list[int], target: int) -> bool:\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo <= hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if nums[mid] == target:\n"
        "            return True\n"
        "        # Duplicate ambiguity: cannot determine sorted half\n"
        "        if nums[lo] == nums[mid] == nums[hi]:\n"
        "            lo += 1  # safe: nums[lo] == nums[mid] != target\n"
        "            hi -= 1  # safe: nums[hi] == nums[mid] != target\n"
        "        elif nums[lo] <= nums[mid]:  # left half is sorted\n"
        "            if nums[lo] <= target < nums[mid]:\n"
        "                hi = mid - 1\n"
        "            else:\n"
        "                lo = mid + 1\n"
        "        else:  # right half is sorted\n"
        "            if nums[mid] < target <= nums[hi]:\n"
        "                lo = mid + 1\n"
        "            else:\n"
        "                hi = mid - 1\n"
        "    return False",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(nums) - 1", {"code": True}), (" — Standard binary search window covering the whole array.", {})])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), (" — Continue while there is at least one element in the search window.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Midpoint, floor-divided. Avoids overflow (though Python ints don't overflow).", {})])),
    N.para(N.rich([("if nums[mid] == target: return True", {"code": True}), (" — Direct hit. Return immediately without any further work.", {})])),
    N.para(N.rich([("if nums[lo] == nums[mid] == nums[hi]:", {"code": True}), (" — THE NEW CASE: all three endpoints equal. We cannot determine which half is sorted from endpoints alone.", {})])),
    N.para(N.rich([("lo += 1; hi -= 1", {"code": True}), (" — Safely discard both boundary elements. Both equal nums[mid] which ≠ target — zero information lost.", {})])),
    N.para(N.rich([("elif nums[lo] <= nums[mid]:", {"code": True}), (" — No break point in left half; [lo..mid] is a fully sorted ascending segment. Must use ≤ (not <) to handle lo==mid case.", {})])),
    N.para(N.rich([("if nums[lo] <= target < nums[mid]: hi = mid-1", {"code": True}), (" — Target falls within the sorted left segment's range. Eliminate right half.", {})])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — Target NOT in left segment range. It must be in the right portion. Eliminate left half.", {})])),
    N.para(N.rich([("else: (right half sorted)", {"code": True}), (" — Break point is in left half, so right half [mid..hi] is a clean sorted segment.", {})])),
    N.para(N.rich([("if nums[mid] < target <= nums[hi]: lo = mid+1", {"code": True}), (" — Target in the right sorted range. Search right.", {})])),
    N.para(N.rich([("else: hi = mid - 1", {"code": True}), (" — Target NOT in right range. Must be in left portion. Eliminate right.", {})])),
    N.para(N.rich([("return False", {"code": True}), (" — lo > hi: window exhausted without finding target.", {})])),
    N.divider(),
]

# ── Solution 2 — Linear Scan ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: Ignore the Structure", [
        N.h4("Reframe the Problem"),
        N.para("Simply check every element."),
        N.h4("What Doesn't Work"),
        N.para("This approach ignores the sorted structure entirely and cannot beat O(n)."),
        N.h4("The Key Observation"),
        N.para("Valid but suboptimal — mention this in an interview as the starting point, then improve to binary search."),
        N.h4("Building the Solution"),
        N.para("Python's 'in' operator performs a linear scan: target in nums."),
    ]),
    N.h3("Code"),
    N.code(
        "def search(nums: list[int], target: int) -> bool:\n"
        "    return target in nums  # O(n) linear scan",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("target in nums", {"code": True}), (" — Python's built-in membership test iterates left-to-right until a match is found or the list is exhausted. Always O(n).", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (avg)", "Time (worst)", "Space"],
        ["Linear Scan", "O(n)", "O(n)", "O(1)"],
        ["Modified Binary Search (Interview Pick)", "O(log n)", "O(n)", "O(1)"],
    ]),
    N.callout(
        "The O(n) worst case for binary search is unavoidable with duplicates. Consider [1,1,1,1,1], target=2: every iteration removes only 2 elements. No algorithm can guarantee O(log n) for this input without preprocessing.",
        "📊", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BS: Rotated Array, Handle Duplicates", {})])),
    N.callout(
        "When to recognize: input described as 'sorted array then rotated at unknown pivot' + may contain duplicates + asks for existence/index → Modified Binary Search with Duplicate Shrink. Key signal: O(1) space required.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), (" (Medium) — #33, same algorithm without duplicates; always O(log n), no shrink case needed", {})])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium) — #153, binary search for the rotation pivot (no duplicates)", {})])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array II", {"bold": True}), (" (Hard) — #154, identical shrink technique applied to finding minimum with duplicates", {})])),
    N.bullet(N.rich([("Peak Index in a Mountain Array", {"bold": True}), (" (Medium) — #852, binary search on bitonic (mountain) array for peak element", {})])),
    N.bullet(N.rich([("Find Peak Element", {"bold": True}), (" (Medium) — #162, generalized peak finding via binary search on any unsorted array with local peaks", {})])),
    N.bullet(N.rich([("Search a 2D Matrix II", {"bold": True}), (" (Medium) — #240, exploit sorted row/column structure; same 'eliminate half the search space' principle", {})])),
    N.para("These problems share the core technique: identify a monotone (sorted) region and use it to safely eliminate part of the search space."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search, Sub-Pattern: BS: Rotated Array", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
