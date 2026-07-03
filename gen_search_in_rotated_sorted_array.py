"""
gen_search_in_rotated_sorted_array.py
Notion page update for LC #33 – Search in Rotated Sorted Array
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8150-b42f-c661a8ab4382"

# ── 1. Set properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=33,
    pattern="Binary Search",
    subpatterns=["Identify Sorted Half"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="At any mid, one half is always sorted; check target against its range to decide direction.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3. Build body blocks ──────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" sorted in ascending order and then rotated at an unknown pivot, and an integer ", {}),
        ("target", {"code": True}),
        (", return the index of ", {}),
        ("target", {"code": True}),
        (" if it is in ", {}),
        ("nums", {"code": True}),
        (", or ", {}),
        ("-1", {"code": True}),
        (" if it is not. You must write an algorithm with O(log n) runtime complexity.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Identify Sorted Half (Optimal) ──
SOLUTION_1_CODE = """\
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:   # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1       # target in sorted left range
            else:
                lo = mid + 1       # target must be in right
        else:                       # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1       # target in sorted right range
            else:
                hi = mid - 1       # target must be in left
    return -1"""

blocks += [
    N.h2("Solution 1 — Identify Sorted Half (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to binary-search an array that is sorted but with one 'break' — the back portion was moved to the front. Standard binary search requires knowing which half the target is in, which normally relies on the array being fully sorted. We need a way to make that same decision despite the rotation."),
        N.h4("What Doesn't Work"),
        N.para("Naive binary search: 'if nums[mid] < target, go right'. This fails because nums[mid] might be in the high left run (e.g., 7 in [4,5,6,7,0,1,2]) while target is the low value 0 on the right. The comparison gives the wrong direction."),
        N.h4("The Key Observation"),
        N.para("A rotation creates exactly ONE drop. When you split the array at mid, that drop falls entirely in one half. The other half has no drop — it's fully sorted. You can always identify the sorted half by comparing nums[lo] to nums[mid]: if nums[lo] <= nums[mid], the left half is sorted; otherwise the right half is."),
        N.h4("Building the Solution"),
        N.para("Once you identify the sorted half, its range is known exactly: [nums[lo], nums[mid]) for left, (nums[mid], nums[hi]] for right. Check if target falls in that range. If yes, search there (eliminating the other half). If no, target must be in the other (possibly rotated) half. Either way, we halve the window — preserving O(log n)."),
        N.callout(
            "Analogy: Searching for a name in a phone book that was cut in half and reassembled backwards. One half is still in alphabetical order — figure out which half, check if the name starts with a letter in that half's range, and search there.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(nums) - 1", {"code": True}), " — Initialize search window to span entire array."])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), " — Use <= (not <) because a single remaining element (lo == hi) is still a valid candidate."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — Integer midpoint. In Python there is no integer overflow risk."])),
    N.para(N.rich([("if nums[mid] == target: return mid", {"code": True}), " — Lucky hit: target found, return immediately."])),
    N.para(N.rich([("if nums[lo] <= nums[mid]:", {"code": True}), " — No drop in [lo..mid]: the left half is fully sorted. Uses <= to correctly handle lo == mid (single-element left half)."])),
    N.para(N.rich([("if nums[lo] <= target < nums[mid]:", {"code": True}), " — Target within the sorted left range? Both bounds needed — strict < on mid (mid itself was already checked above)."])),
    N.para(N.rich([("hi = mid - 1", {"code": True}), " — Yes: target is in left, eliminate right half."])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), " (else branch) — No: target can't be in the sorted left, so it must be in the (possibly rotated) right half."])),
    N.para(N.rich([("else:", {"code": True}), " — The drop is in the left half, so the right half [mid..hi] is sorted."])),
    N.para(N.rich([("if nums[mid] < target <= nums[hi]:", {"code": True}), " — Target within sorted right range? Use strict < on mid (already checked) and <= on hi."])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), " — Yes: search right half."])),
    N.para(N.rich([("hi = mid - 1", {"code": True}), " — No: target must be in the left half."])),
    N.para(N.rich([("return -1", {"code": True}), " — Loop exhausted without finding target; it is not in the array."])),
    N.divider(),
]

# ── Solution 2: Linear Scan (Brute Force) ──
SOLUTION_2_CODE = """\
def search_linear(nums: list[int], target: int) -> int:
    for i, v in enumerate(nums):
        if v == target:
            return i
    return -1"""

blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Forget all structure — just find the target by looking at every element."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly, but runs in O(n) time. The problem explicitly requires O(log n), so this fails the constraint and would not be accepted by the judge for large inputs."),
        N.h4("The Key Observation"),
        N.para("Mention this to the interviewer as a baseline, then immediately offer the O(log n) solution. It demonstrates you understand correctness before optimization."),
        N.h4("Building the Solution"),
        N.para("Simply iterate with enumerate — if value matches target, return the index. After the loop, return -1. No edge case handling needed."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i, v in enumerate(nums):", {"code": True}), " — Scan every index and value."])),
    N.para(N.rich([("if v == target: return i", {"code": True}), " — Match found; return index immediately."])),
    N.para(N.rich([("return -1", {"code": True}), " — Completed full scan, target absent."])),
    N.callout("This is O(n) — propose it as baseline then optimize to the O(log n) solution above.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Linear Scan", "O(n)", "O(1)"],
        ["Identify Sorted Half (optimal)", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Identify Sorted Half"])),
    N.callout(
        "When to recognize this pattern: O(log n) required + sorted array with one structural anomaly (rotation) → binary search with modified condition. Key signal: 'rotated sorted array' + 'search'. Always ask: which half is sorted? Use that half's boundaries to decide direction.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search variants):"),
    N.bullet(N.rich([("Search in Rotated Sorted Array II", {"bold": True}), " (Medium) — Duplicates allowed; when nums[lo]==nums[mid], can't identify sorted half → lo++. Worst case O(n). (#81)"])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), " (Medium) — Binary search for the rotation pivot/minimum using the same sorted-half identification. (#153)"])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array II", {"bold": True}), " (Hard) — Duplicates version; worst case O(n). (#154)"])),
    N.bullet(N.rich([("Find Peak Element", {"bold": True}), " (Medium) — Binary search navigating by local slope: always move toward the larger neighbor. (#162)"])),
    N.bullet(N.rich([("Binary Search", {"bold": True}), " (Easy) — The standard template; master this before tackling rotated variants. (#704)"])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — Binary search on the answer space (not the array itself). (#875)"])),
    N.para("These problems all exploit partial ordering — a sorted structure with one controlled deviation — to achieve O(log n) search."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search) — Sub-Pattern: Identify Sorted Half", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("search_in_rotated_sorted_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
