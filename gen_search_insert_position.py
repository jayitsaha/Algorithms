"""
gen_search_insert_position.py
Regenerate the Notion page for Search Insert Position (LeetCode #35) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f0-8a27-d7c9ca66e234"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=35,
    pattern="Binary Search",
    subpatterns=["Lower Bound"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="When binary search exits, lo is always the first index where nums[lo] >= target — the insert position, whether or not target was found.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted array of distinct integers ", {}),
        ("nums", {"code": True}),
        (" and a ", {}),
        ("target", {"code": True}),
        (" value, return the index if the target is found. If not found, return the index where it would be inserted in order. You must write an algorithm with ", {}),
        ("O(log n)", {"code": True}),
        (" runtime complexity.", {}),
    ])),
    N.para("Example: nums = [1, 3, 5, 6], target = 5 → 2 (found at index 2)"),
    N.para("Example: nums = [1, 3, 5, 6], target = 2 → 1 (would be inserted at index 1)"),
    N.para("Example: nums = [1, 3, 5, 6], target = 7 → 4 (would be inserted at end)"),
    N.divider(),
]

# ── Solution 1: Binary Search (Interview Pick) ─────────────────────────────────
blocks += [
    N.h2("Solution 1 — Binary Search: Lower Bound (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the first position in the sorted array where nums[i] >= target. That's it. Whether target exists or not, that index is our answer — it's either the element itself or where we'd slot the value in."),
        N.h4("What Doesn't Work"),
        N.para("Linear scan works (O(n)) but completely ignores the sorted property. The problem requires O(log n), which is a direct hint that binary search is expected."),
        N.h4("The Key Observation"),
        N.para("Binary search on a sorted array halves the search space each step. Here the key twist is: when the loop exits, lo always lands at the first index >= target, regardless of whether target was found. We don't need a special post-loop check."),
        N.h4("Building the Solution"),
        N.para("Start: lo=0, hi=n-1. Each step compute mid = lo + (hi-lo)//2. If nums[mid] == target: return mid. If nums[mid] < target: the answer is to the right, so lo = mid+1. If nums[mid] > target: the answer is at mid or to the left, so hi = mid-1. When lo > hi, return lo."),
        N.callout("Analogy: Searching for a word in a printed dictionary. You open to the middle. If the word comes after, tear off the left half; if before, the right half. When you've narrowed to a single page and the word isn't there, that page is where it would be added — that's lo.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Lower Bound Binary Search"),
    N.para(N.rich([
        ("Lower Bound", {"bold": True}),
        (" is the classical version of binary search that finds the first index satisfying a monotonic condition (here: nums[i] >= target). It is sometimes called ", {}),
        ("bisect_left", {"code": True}),
        (" in Python's standard library. Unlike standard binary search which only detects presence, lower bound always returns a meaningful position even when the target is absent.", {}),
    ])),
    N.para("Core invariant: At all times, the insert position lies within [lo, hi+1]. When lo > hi, this range collapses to {lo}, which is the answer."),
    N.para("Why hi = mid - 1 and not hi = mid: With the while lo <= hi form, using hi = mid would cause an infinite loop when lo == hi == mid (window never shrinks). Always use strict reduction: lo = mid+1 or hi = mid-1."),
    N.h3("Code"),
    N.code(
        "def searchInsert(nums, target):\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo <= hi:\n"
        "        mid = lo + (hi - lo) // 2\n"
        "        if nums[mid] == target:\n"
        "            return mid\n"
        "        elif nums[mid] < target:\n"
        "            lo = mid + 1\n"
        "        else:\n"
        "            hi = mid - 1\n"
        "    return lo"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(nums) - 1", {"code": True}), (" — Initialize closed window [lo, hi] covering the full array.", {})])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), (" — Continue as long as the window is non-empty.", {})])),
    N.para(N.rich([("mid = lo + (hi - lo) // 2", {"code": True}), (" — Midpoint using overflow-safe form (habit from C/Java; same result as (lo+hi)//2 in Python).", {})])),
    N.para(N.rich([("if nums[mid] == target:", {"code": True}), (" — Exact match found; return current index immediately.", {})])),
    N.para(N.rich([("elif nums[mid] < target:", {"code": True}), (" — mid is too small; target must be strictly to the right, so advance lo past mid.", {})])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), (" — Eliminate mid and everything left; lo now points to the first unconsidered right candidate.", {})])),
    N.para(N.rich([("hi = mid - 1", {"code": True}), (" — nums[mid] > target: eliminate mid and everything right; hi retreats past mid.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — Loop exited with lo > hi. lo is the first index where nums[lo] >= target — the insert position.", {})])),
    N.callout(
        "⚠️ Why return lo and not hi+1? Both equal the same value when the loop exits (lo == hi+1), but lo is the cleaner and more idiomatic choice. hi+1 also works but is unnecessarily verbose.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Linear Scan (Brute Force) ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force, O(n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Scan from left to right. The first element >= target is the answer. If we reach the end, return n (insert at end)."),
        N.h4("What Doesn't Work About This"),
        N.para("It works correctly but runs in O(n) time, ignoring the sorted order. For large arrays this is far too slow. The problem explicitly requires O(log n), so this is only useful as a baseline to show you understand the naive solution before optimizing."),
        N.h4("The Key Observation"),
        N.para("Still, it's worth showing: the condition 'n >= target' unifies the found and not-found cases in a single check, just like binary search does with lo."),
        N.callout("Present this first in an interview, then say 'since the array is sorted I can do O(log n) with binary search' — it signals structured thinking.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def searchInsert(nums, target):\n"
        "    for i, n in enumerate(nums):\n"
        "        if n >= target:\n"
        "            return i\n"
        "    return len(nums)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i, n in enumerate(nums):", {"code": True}), (" — Scan left to right, getting index and value.", {})])),
    N.para(N.rich([("if n >= target:", {"code": True}), (" — First element >= target is either the element itself (n==target) or the gap (n>target). Both cases are the insert position.", {})])),
    N.para(N.rich([("return len(nums)", {"code": True}), (" — All elements were less than target; insert at the end.", {})])),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Linear Scan (Brute Force)", "O(n)", "O(1)"],
        ["Binary Search — Lower Bound (Optimal)", "O(log n)", "O(1)"],
        ["bisect.bisect_left (library)", "O(log n)", "O(1)"],
    ]),
    N.para("Binary search is the expected solution. The O(log n) requirement is directly implied by the sorted input — any time you see 'sorted array' + 'find position/value', reach for binary search first."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Lower Bound (BS: First/Last Occurrence)", {})])),
    N.para(N.rich([
        ("Verified against: ", {"bold": True}),
        ("DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search) — Lower Bound sub-pattern.", {"italic": True}),
    ])),
    N.callout(
        "🔎 When to recognize this pattern:\n"
        "• Input array is sorted (ascending or descending)\n"
        "• Asked to find a value OR the position where it would be inserted\n"
        "• Constraint says O(log n) or n can be very large\n"
        "• Problem phrasing: 'first index where condition holds', 'leftmost occurrence', 'insert to maintain sort order'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Binary Search / Lower Bound technique:"),
    N.bullet(N.rich([("Binary Search", {"bold": True}), (" (Easy) — Pure binary search: return index of exact target, -1 if not found. No insert logic. (#704)", {})])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), (" (Easy) — Lower bound variant: monotonic False/True sequence, find first True using the same lo/hi template. (#278)", {})])),
    N.bullet(N.rich([("Guess Number Higher or Lower", {"bold": True}), (" (Easy) — Same lo/hi template but with API feedback (Higher/Lower/Correct) instead of array comparison. (#374)", {})])),
    N.bullet(N.rich([("Find First and Last Position of Element in Sorted Array", {"bold": True}), (" (Medium) — Run two binary searches: lower bound for left edge, upper bound for right edge. (#34)", {})])),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), (" (Medium) — Binary search with rotation detection: first determine which half is sorted, then binary search that half. (#33)", {})])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium) — Same lo/hi skeleton; condition tells you which half the minimum is in. (#153)", {})])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — Binary search on the answer space (eating speed), not the array itself. Feasibility is monotonic. (#875)", {})])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — Same answer-space binary search template; monotonic feasibility condition. (#1011)", {})])),
    N.para("These problems share the same core technique: eliminate half the search space per iteration using a monotonic condition. Master the lo/hi/mid invariant once and you can solve all of them."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search patterns (Standard, Lower Bound, Rotated Array, On Answer)", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("search_insert_position")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Notion OK — appended {len(blocks)} blocks to {PAGE_ID}")
