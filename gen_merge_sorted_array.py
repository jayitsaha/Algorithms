"""
gen_merge_sorted_array.py — Notion in-place update for Merge Sorted Array (#88)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8146-91a2-ddbfb18d6728"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=88,
    pattern="Two Pointers",
    subpatterns=["Merge from End (Opposite)"],
    tc="O(m+n)",
    sc="O(1)",
    key_insight="Fill nums1 from the end using three pointers — trailing zeros are empty seats, so backward merging never overwrites unread data.",
    icon="🟢"
)
print("  Properties set.")

print("Step 2: Wiping old page content...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks.")

print("Step 3: Building new content blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two integer arrays ", {}),
        ("nums1", {"code": True}), (" and ", {}), ("nums2", {"code": True}),
        (", sorted in non-decreasing order, and two integers ", {}),
        ("m", {"code": True}), (" and ", {}), ("n", {"code": True}),
        (", representing the number of elements in ", {}),
        ("nums1", {"code": True}), (" and ", {}), ("nums2", {"code": True}),
        (" respectively. ", {}),
        ("nums1", {"code": True}),
        (" has a length of ", {}), ("m + n", {"code": True}),
        (", where the last ", {}), ("n", {"code": True}),
        (" elements are set to ", {}), ("0", {"code": True}),
        (" and should be ignored. Merge ", {}), ("nums2", {"code": True}),
        (" into ", {}), ("nums1", {"code": True}),
        (" in-place so that ", {}), ("nums1", {"code": True}),
        (" is sorted in non-decreasing order.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3 → [1,2,2,3,5,6]", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force: Copy then Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("We have two sorted arrays and need to combine them into one sorted array in nums1's extra space. The simplest reading: just put all elements together and sort."),
        N.para(N.rich([("What Doesn't Work (Optimally)", {"bold": True})])),
        N.para("This approach is O((m+n) log(m+n)) — it completely discards the fact that both input arrays are already sorted. We're doing unnecessary work. It also can't easily beat this bound without exploiting the sorted property."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("The nums2 elements must fill the trailing zeros of nums1. Overwriting them then sorting is the naive restatement. It's correct — just not optimal."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Slice-assign nums2 into nums1[m:m+n] to replace the zeros, then call nums1.sort(). Two lines of Python — couldn't be simpler."),
        N.callout("Propose this first in any interview, then offer to optimize.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def merge(nums1: list, m: int, nums2: list, n: int) -> None:\n"
        "    nums1[m:m+n] = nums2  # Overwrite trailing zeros with nums2 values\n"
        "    nums1.sort()          # Sort the combined array in-place\n",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nums1[m:m+n] = nums2", {"code": True}), (" — Slice assignment replaces the n trailing zeros with nums2's actual values. No explicit loop needed.", {})])),
    N.para(N.rich([("nums1.sort()", {"code": True}), (" — Python's Timsort runs in O((m+n) log(m+n)). Modifies nums1 in-place; returns None.", {})])),
    N.divider(),
]

# ── Solution 2: Merge from End (Interview Pick) ──
blocks += [
    N.h2("Solution 2 — Merge from End (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("nums1 has m+n capacity: m real sorted elements, then n zeros. The zeros are reserved empty seats. We need to fill them with a sorted merge of both arrays without extra space."),
        N.para(N.rich([("What Doesn't Work — Forward Merge", {"bold": True})])),
        N.para("If we try to merge from the front, writing to nums1[0] overwrites real data before we've used it. We'd need an extra array to buffer the displaced elements — no longer O(1) space."),
        N.para(N.rich([("The Key Observation — Fill the Empty Seats Backward", {"bold": True})])),
        N.para("The empty seats are at the RIGHT of nums1. If we fill right-to-left — always placing the LARGER of the two current tails — we write into zeros first. By the time the write cursor reaches real nums1 data, those positions have already been consumed. No conflict."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Three pointers: p = m-1 (nums1 tail), q = n-1 (nums2 tail), k = m+n-1 (write cursor). Loop: compare nums1[p] and nums2[q], place the larger at nums1[k], decrement the used pointer and k. After the loop, copy any remaining nums2 elements (nums1 remainders are already in-place)."),
        N.callout("Analogy: Two sorted piles of cards, face-up. You always pick the higher top card and place it into a new deck from the back. Both piles shrink; the deck fills front-to-back (in reverse, right-to-left).", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def merge(nums1: list, m: int, nums2: list, n: int) -> None:\n"
        "    p = m - 1       # Pointer to last real element in nums1\n"
        "    q = n - 1       # Pointer to last element in nums2\n"
        "    k = m + n - 1   # Write cursor: rightmost slot in nums1\n"
        "\n"
        "    while p >= 0 and q >= 0:\n"
        "        if nums1[p] > nums2[q]:\n"
        "            nums1[k] = nums1[p]  # nums1's tail is larger\n"
        "            p -= 1\n"
        "        else:\n"
        "            nums1[k] = nums2[q]  # nums2's tail wins (or tie)\n"
        "            q -= 1\n"
        "        k -= 1  # Always advance write cursor\n"
        "\n"
        "    # Mop-up: copy remaining nums2 elements if any\n"
        "    while q >= 0:\n"
        "        nums1[k] = nums2[q]\n"
        "        q -= 1\n"
        "        k -= 1\n"
        "    # Note: remaining nums1 elements (p >= 0) are already in-place\n",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("p = m - 1", {"code": True}), (" — Index of the last real element in nums1 (not a zero).", {})])),
    N.para(N.rich([("q = n - 1", {"code": True}), (" — Index of the last element in nums2.", {})])),
    N.para(N.rich([("k = m + n - 1", {"code": True}), (" — Write cursor at the rightmost position of nums1 (a zero slot).", {})])),
    N.para(N.rich([("while p >= 0 and q >= 0:", {"code": True}), (" — Continue as long as both arrays have unread elements.", {})])),
    N.para(N.rich([("if nums1[p] > nums2[q]:", {"code": True}), (" — Compare current tails. Strict > means ties go to nums2 (else branch) — either is fine.", {})])),
    N.para(N.rich([("nums1[k] = nums1[p]; p -= 1", {"code": True}), (" — Place nums1's larger tail at write position. Retreat the nums1 read pointer.", {})])),
    N.para(N.rich([("nums1[k] = nums2[q]; q -= 1", {"code": True}), (" — Place nums2's tail at write position. Retreat the nums2 pointer.", {})])),
    N.para(N.rich([("k -= 1", {"code": True}), (" — Always advance the write cursor leftward after each placement.", {})])),
    N.para(N.rich([("while q >= 0:", {"code": True}), (" — Mop-up: nums2 still has elements. All are ≤ everything placed already.", {})])),
    N.para(N.rich([("nums1[k] = nums2[q]; q -= 1; k -= 1", {"code": True}), (" — Copy remaining nums2 elements to the front of nums1 in order.", {})])),
    N.para("Remaining nums1 elements (if p >= 0 at loop exit) are already at positions 0..p — correct by the invariant."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Copy + Sort", "O((m+n) log(m+n))", "O(1)"],
        ["Merge from End (Optimal)", "O(m+n)", "O(1)"],
    ]),
    N.para("Each of the m+n elements is placed exactly once in the optimal approach → O(m+n). Only three integer pointers as extra storage → O(1) space."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Merge from End (Opposite) — two read pointers converging from array tails, one write cursor filling backward", {})])),
    N.callout(
        "When to recognize this pattern: One sorted array has extra trailing capacity (zeros/null slots). In-place merge is required with O(1) space. Forward merging would create a read-write conflict → reverse direction. Three pointers needed: two reads + one write.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (merge / two-pointer from end):"),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), (" (Easy) — Linked list version; dummy head + two read pointers (#21)", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Generalize with a min-heap; O(N log k) (#23)", {})])),
    N.bullet(N.rich([("Sort Colors", {"bold": True}), (" (Medium) — Dutch National Flag: 3-way partition with three opposite-direction pointers (#75)", {})])),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}), (" (Medium) — Two-pointer scan over sorted interval lists (#986)", {})])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), (" (Medium) — Opposite-direction two pointers converging inward (#11)", {})])),
    N.bullet(N.rich([("Move Zeroes", {"bold": True}), (" (Easy) — Same-direction write-from-front partition (#283)", {})])),
    N.bullet(N.rich([("Remove Duplicates from Sorted Array", {"bold": True}), (" (Easy) — Same-direction two-pointer overwrite (#26)", {})])),
    N.para("These problems share the core technique: use pointer positions to enforce a read-write contract that avoids conflicts."),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("merge_sorted_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch how three pointers coordinate to fill slots from right to left without overwriting unread data.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Built {len(blocks)} top-level blocks.")

print("Step 4: Appending blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"  Done. PAGE_ID = {PAGE_ID}")
print(f"NOTION OK {PAGE_ID}")
