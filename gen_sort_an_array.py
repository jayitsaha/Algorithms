"""
gen_sort_an_array.py — Notion page rebuild for Sort an Array (LC #912)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8181-b7c4-e5d5aa71428a"

# ── 1) Set properties ──
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=912,
    pattern="Sorting",
    subpatterns=["Classic Merge Sort"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Split array in half, recursively sort each half, merge two sorted halves in O(n) with two pointers — guaranteed O(n log n) in all cases.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ──
MERGE_SORT_CODE = """\
def sortArray(nums):
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left  = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result += left[i:]
        result += right[j:]
        return result

    nums[:] = merge_sort(nums)
    return nums"""

QUICK_SORT_CODE = """\
import random

def sortArray(nums):
    def quick_sort(lo, hi):
        if lo >= hi:
            return
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        pivot, w = nums[hi], lo
        for r in range(lo, hi):
            if nums[r] <= pivot:
                nums[w], nums[r] = nums[r], nums[w]
                w += 1
        nums[w], nums[hi] = nums[hi], nums[w]
        quick_sort(lo, w - 1)
        quick_sort(w + 1, hi)

    quick_sort(0, len(nums) - 1)
    return nums"""

blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("nums", {"code": True}),
        (", sort the array in ascending order and return it. You must solve the problem without using any built-in functions that run in O(n log n) time or better.\n\n", {}),
        ("Constraints: ", {"bold": True}),
        ("1 ≤ nums.length ≤ 5×10⁴, -5×10⁴ ≤ nums[i] ≤ 5×10⁴", {}),
    ])),
    N.divider(),
]

# Solution 1 — Merge Sort
blocks += [
    N.h2("Solution 1 — Classic Merge Sort (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to sort an array without built-in sort. With n up to 5×10⁴, any O(n²) algorithm (Bubble, Insertion, Selection Sort) will time out with ~2.5 billion operations. We need an O(n log n) approach."),
        N.h4("What Doesn't Work"),
        N.para("Bubble Sort: for each element, repeatedly swap adjacent pairs until the largest bubbles to the end — O(n²) comparisons. Insertion Sort: insert each element into its correct position in a growing sorted prefix — O(n²) in the worst case. Both are too slow for n=50,000."),
        N.h4("The Key Observation"),
        N.para("Merging two already-sorted arrays is O(n): use two pointers, always pick the smaller front element. If we could somehow get both halves sorted before merging, the total work would be O(n) per merge × O(log n) merge levels = O(n log n). That's exactly what recursion gives us — sort each half by solving a smaller version of the same problem!"),
        N.h4("Building the Solution"),
        N.para("1. Base case: 0 or 1 element is already sorted — return immediately.\n2. Divide: split array at midpoint into left and right halves.\n3. Conquer: recursively sort each half (they become sorted by induction).\n4. Merge: combine two sorted halves into one sorted array using two pointers in O(n).\n5. By induction: every level produces a sorted result. The full array is sorted after the top-level merge."),
        N.callout("Analogy: Imagine sorting a deck of 52 cards by splitting it into two 26-card piles, sorting each pile (recursively), then interleaving the two sorted piles by always picking the smaller top card. This is exactly Merge Sort.", "🃏", "blue_background"),
    ]),

    N.h3("Code"),
    N.code(MERGE_SORT_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("def sortArray(nums):", {"code": True}), (" — Entry point; returns the sorted array.", {})])),
    N.para(N.rich([("def merge_sort(arr):", {"code": True}), (" — Recursive helper operating on a subarray.", {})])),
    N.para(N.rich([("if len(arr) <= 1:", {"code": True}), (" — Base case: 0 or 1 element needs no sorting. Return immediately — this is what stops the recursion.", {})])),
    N.para(N.rich([("mid = len(arr) // 2", {"code": True}), (" — Midpoint via floor division. For even-length arrays this gives equal halves; for odd-length the left half gets one fewer element.", {})])),
    N.para(N.rich([("left = merge_sort(arr[:mid])", {"code": True}), (" — Create a new subarray for the left half and recursively sort it. After this returns, ", {}), ("left", {"code": True}), (" is sorted.", {})])),
    N.para(N.rich([("right = merge_sort(arr[mid:])", {"code": True}), (" — Same for the right half. After this returns, ", {}), ("right", {"code": True}), (" is sorted.", {})])),
    N.para(N.rich([("return merge(left, right)", {"code": True}), (" — Merge the two sorted halves into one sorted array.", {})])),
    N.para(N.rich([("result = []", {"code": True}), (" — Output buffer that will hold the merged elements.", {})])),
    N.para(N.rich([("i = j = 0", {"code": True}), (" — Two pointers: ", {}), ("i", {"code": True}), (" scans left, ", {}), ("j", {"code": True}), (" scans right.", {})])),
    N.para(N.rich([("while i < len(left) and j < len(right):", {"code": True}), (" — Loop while both halves have unplaced elements.", {})])),
    N.para(N.rich([("if left[i] <= right[j]:", {"code": True}), (" — Compare front elements. Using ", {}), ("<=", {"code": True}), (" (not ", {}), ("<", {"code": True}), (") ensures stability — equal elements from the left half come first.", {})])),
    N.para(N.rich([("result.append(left[i]); i += 1", {"code": True}), (" — Place smaller-or-equal left element and advance the left pointer.", {})])),
    N.para(N.rich([("result.append(right[j]); j += 1", {"code": True}), (" — Otherwise right is strictly smaller; place it and advance the right pointer.", {})])),
    N.para(N.rich([("result += left[i:]", {"code": True}), (" — When right is exhausted, all remaining left elements are in sorted order — append them all at once.", {})])),
    N.para(N.rich([("result += right[j:]", {"code": True}), (" — When left is exhausted, drain remaining right elements. Exactly one of these two drain lines will add elements; the other adds nothing.", {})])),
    N.para(N.rich([("nums[:] = merge_sort(nums)", {"code": True}), (" — Slice assignment: mutates the ORIGINAL list object in-place. Writing ", {}), ("nums = ...", {"code": True}), (" would only rebind the local variable.", {})])),
    N.divider(),
]

# Solution 2 — Quick Sort
blocks += [
    N.h2("Solution 2 — Randomized Quick Sort (O(n log n) Average, O(1) Extra Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we sort in-place without O(n) auxiliary space? Merge Sort creates new arrays at each level. Quick Sort partitions the array around a 'pivot' element in-place, then recursively sorts each partition."),
        N.h4("What Doesn't Work"),
        N.para("Choosing a fixed pivot (first/last element) degrades to O(n²) on sorted or reverse-sorted arrays — the pivot is always the minimum/maximum, creating maximally unbalanced partitions of size 1 and n-1."),
        N.h4("The Key Observation"),
        N.para("A random pivot gives an expected O(n log n) performance because, on average, the pivot lands near the median. The probability of consistently bad pivots across all levels is astronomically low."),
        N.h4("Building the Solution"),
        N.para("1. Choose a random pivot index and swap it to the end.\n2. Partition: scan left-to-right with a 'write' pointer. Elements ≤ pivot go left of write; elements > pivot stay right.\n3. Place the pivot at the write position — this is its final sorted position.\n4. Recursively sort the left and right partitions.\n5. No merging needed — partitioning happens in-place."),
        N.callout("Quick Sort is cache-friendly (sequential memory access) and uses only O(log n) stack space. It's often faster in practice than Merge Sort despite the same asymptotic complexity. However, for this LeetCode problem, Merge Sort is safer (deterministic O(n log n)).", "⚡", "yellow_background"),
    ]),

    N.h3("Code"),
    N.code(QUICK_SORT_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("p = random.randint(lo, hi)", {"code": True}), (" — Choose a random pivot index in [lo, hi]. Randomization prevents O(n²) worst case on adversarial input.", {})])),
    N.para(N.rich([("nums[p], nums[hi] = nums[hi], nums[p]", {"code": True}), (" — Temporarily move pivot to the end so it's out of the way during partitioning.", {})])),
    N.para(N.rich([("pivot, w = nums[hi], lo", {"code": True}), (" — Remember pivot value. ", {}), ("w", {"code": True}), (" is the 'write' pointer — next slot for elements ≤ pivot.", {})])),
    N.para(N.rich([("for r in range(lo, hi):", {"code": True}), (" — Scan every element except the pivot (at hi).", {})])),
    N.para(N.rich([("if nums[r] <= pivot:", {"code": True}), (" — This element belongs in the left (smaller-or-equal) partition.", {})])),
    N.para(N.rich([("nums[w], nums[r] = nums[r], nums[w]; w += 1", {"code": True}), (" — Swap it to the write position and advance write. Elements at index < w are now all ≤ pivot.", {})])),
    N.para(N.rich([("nums[w], nums[hi] = nums[hi], nums[w]", {"code": True}), (" — Place the pivot at its final sorted position w. Everything left of w is ≤ pivot; everything right is > pivot.", {})])),
    N.para(N.rich([("quick_sort(lo, w-1); quick_sort(w+1, hi)", {"code": True}), (" — Recursively sort left and right partitions. The pivot itself is already in its correct position.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Stable?"],
        ["Classic Merge Sort (Interview Pick)", "O(n log n) — guaranteed", "O(n) — temp arrays", "Yes"],
        ["Randomized Quick Sort", "O(n log n) avg / O(n²) rare", "O(log n) — stack", "No"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Classic Merge Sort (Divide & Conquer)", {})])),
    N.callout("When to recognize this pattern: problem says 'sort without built-in' + large n (rules out O(n²)) — implement Merge Sort. Also when stability is required, when counting inversions, or when sorting linked lists.", "🔎", "green_background"),
    N.para(N.rich([("Note: ", {"italic": True}), ("'Classic Merge Sort' is the sub-pattern label used based on analysis. Merge Sort is a foundational divide-and-conquer sorting algorithm used across many problem variants.", {"italic": True})])),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Merge Sort / Divide & Conquer sorting):"),
    N.bullet(N.rich([("Merge Sorted Array", {"bold": True}), (" (Easy) — Core two-pointer merge operation; fill from the end to avoid overwriting (#88)", {})])),
    N.bullet(N.rich([("Sort List", {"bold": True}), (" (Medium) — Merge Sort on a linked list; find midpoint with fast/slow pointers (#148)", {})])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), (" (Hard) — Merge Sort + count inversions during the merge phase (#315)", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Divide-and-conquer merge of k sorted lists using a min-heap (#23)", {})])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Quickselect (partition without full sort, expected O(n)) (#215)", {})])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), (" (Hard) — Prefix sums + merge sort to count ranges satisfying a bound (#327)", {})])),
    N.para("These problems all leverage the merge step or divide-and-conquer structure of Merge Sort."),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sort_an_array")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
