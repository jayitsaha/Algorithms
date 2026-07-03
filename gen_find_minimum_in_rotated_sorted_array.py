"""
gen_find_minimum_in_rotated_sorted_array.py
Regenerates the Notion page for LeetCode #153 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815e-90b5-d88a1cee361a"

# ── 1. Set Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=153,
    pattern="Binary Search",
    subpatterns=["BS: Rotated Array"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Compare nums[mid] to nums[hi] to determine which sorted run mid is in; use hi=mid (not mid-1) to preserve the minimum as a candidate.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build the full body ─────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Suppose an array of length ", {}),
        ("n", {"code": True}),
        (" sorted in ascending order is ", {}),
        ("rotated", {"bold": True}),
        (" between ", {}),
        ("1", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (" times. For example, the array ", {}),
        ("[0, 1, 2, 4, 5, 6, 7]", {"code": True}),
        (" might become ", {}),
        ("[4, 5, 6, 7, 0, 1, 2]", {"code": True}),
        (" if rotated 4 times. Given the sorted rotated array ", {}),
        ("nums", {"code": True}),
        (" of unique elements, return the minimum element in ", {}),
        ("O(log n)", {"bold": True}),
        (" time.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Binary Search (Interview Pick) ────────────────────────────────
blocks += [
    N.h2("Solution 1 — Binary Search on Pivot (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the 'drop point' in a rotated sorted array — the single index where the array value jumps down. This drop point is where the left sorted run ends and the smaller right sorted run begins. The minimum is the first element of the right run."),
        N.h4("What Doesn't Work"),
        N.para("Linear scan (O(n)) works but wastes the sorted structure. Sorting again is O(n log n) and even worse. We need to exploit the fact that the array is mostly sorted to jump O(log n) steps at a time."),
        N.h4("The Key Observation"),
        N.para("A rotated sorted array consists of exactly two ascending sub-sequences. At any midpoint, comparing nums[mid] to nums[hi] unambiguously tells us which sub-sequence mid falls in: if nums[mid] > nums[hi], mid is in the large left run (minimum is right); if nums[mid] <= nums[hi], mid is in the small right run (minimum is at mid or left)."),
        N.h4("Building the Solution"),
        N.para("Maintain lo and hi pointers bounding the search window. Each iteration: compute mid, compare to nums[hi], eliminate half the window. When lo == hi, one candidate remains — that's the minimum. Use hi = mid (not mid-1) when mid could be the answer."),
        N.callout("Analogy: Imagine a mountain range with one valley. Standing at any peak (mid), you look right (hi). If the right peak is lower, the valley is to the right. If the right peak is higher, the valley is to the left or at your feet.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def findMin(nums: list[int]) -> int:\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if nums[mid] > nums[hi]:\n"
        "            lo = mid + 1   # Min is right of mid\n"
        "        else:\n"
        "            hi = mid       # Min is at mid or left\n"
        "    return nums[lo]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(nums) - 1", {"code": True}), (" — Initialize search window to the full array.", {})])),
    N.para(N.rich([("while lo < hi:", {"code": True}), (" — Keep searching while more than one element remains in the window. Exit when lo==hi (single candidate).", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Integer midpoint. With lo < hi, we always have mid < hi, guaranteeing progress.", {})])),
    N.para(N.rich([("if nums[mid] > nums[hi]:", {"code": True}), (" — If mid's value exceeds hi's value, mid is in the large left ascending run. Minimum cannot be here or to the left.", {})])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), (" — Safe to exclude mid and everything left of it. Minimum must be strictly right of mid.", {})])),
    N.para(N.rich([("else: hi = mid", {"code": True}), (" — Mid is in the small right run (or array is fully sorted). Mid itself might be the minimum, so we keep it with hi=mid (not mid-1).", {})])),
    N.para(N.rich([("return nums[lo]", {"code": True}), (" — Loop exited with lo==hi. The single remaining element is the minimum. nums[lo] == nums[hi] at this point.", {})])),
    N.divider(),
]

# ── Solution 2 — Linear Scan ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we have no constraint on time complexity, we can simply scan every element and track the smallest value seen."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly but runs in O(n). It ignores the sorted structure entirely, making it unsuitable when O(log n) is required."),
        N.h4("The Key Observation"),
        N.para("There's a shortcut for arrays: the minimum is the first element where a 'drop' occurs — nums[i] > nums[i+1]. But even finding this drop is O(n) in the worst case."),
        N.h4("Building the Solution"),
        N.para("Iterate through all elements, maintain a running minimum. Return it at the end. Equivalent to Python's built-in min(nums)."),
        N.callout("Present this as your starting point in an interview: 'The naive solution is O(n) linear scan. We can do much better — O(log n) — by exploiting the sorted structure.'", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def findMin(nums: list[int]) -> int:\n"
        "    # Option A: simple built-in\n"
        "    return min(nums)\n\n"
        "    # Option B: find the drop point\n"
        "    for i in range(len(nums) - 1):\n"
        "        if nums[i] > nums[i + 1]:\n"
        "            return nums[i + 1]\n"
        "    return nums[0]  # Array not rotated",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("min(nums)", {"code": True}), (" — Python's built-in performs O(n) linear scan under the hood. Correct but not O(log n).", {})])),
    N.para(N.rich([("if nums[i] > nums[i + 1]:", {"code": True}), (" — Finds the drop point: the first index where the sequence 'falls'. The element right after the drop is the minimum.", {})])),
    N.para(N.rich([("return nums[0]", {"code": True}), (" — If no drop is found, the array is fully sorted (not rotated). The minimum is the first element.", {})])),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",      "Space", "Notes"],
        ["Linear Scan / min()",   "O(n)",      "O(1)",  "Correct but ignores sorted structure"],
        ["Binary Search (optimal)","O(log n)", "O(1)",  "Halves search space each iteration — interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BS: Rotated Array — binary search where the sorted array has been rotated and we need to find the pivot/minimum.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'sorted array that has been rotated'\n"
        "• Requirement is O(log n) time\n"
        "• Need to find minimum, maximum, or a specific target in rotated data\n"
        "• Key question is always: 'which sorted run is mid in?'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BS: Rotated Array):"),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), (" (Medium, #33) — Find a target value; locate which sorted half target is in, then binary search that half.", {})])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array II", {"bold": True}), (" (Hard, #154) — Same but with duplicates; add elif nums[mid]==nums[hi]: hi -= 1 case.", {})])),
    N.bullet(N.rich([("Search in Rotated Sorted Array II", {"bold": True}), (" (Medium, #81) — Search with duplicates; O(n) worst case due to ambiguous duplicates.", {})])),
    N.bullet(N.rich([("Find Peak Element", {"bold": True}), (" (Medium, #162) — Binary search for local maximum using similar midpoint-vs-neighbor comparison logic.", {})])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), (" (Easy, #278) — Classic binary search boundary; good warm-up for understanding lo/hi invariants.", {})])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium, #875) — Binary search on answer space (not array); same O(log n) elimination idea.", {})])),
    N.para("These problems all share the core technique: using binary search with a predicate that determines which half of a structured space to eliminate."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search) · Sub-Pattern: BS: Rotated Array · Verified: Guide Section 9", "📚", "gray_background"),
]

# ── Embed Visual Explainer ────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_minimum_in_rotated_sorted_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
