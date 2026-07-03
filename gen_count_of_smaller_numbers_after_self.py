"""
gen_count_of_smaller_numbers_after_self.py
Rebuilds the Notion page for LC #315 Count of Smaller Numbers After Self.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8128-9c05-ff2e152e07fa"
SLUG    = "count_of_smaller_numbers_after_self"

# ─── 1) Properties ───────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=315,
    pattern="Advanced Data Structures",
    subpatterns=["BIT + Coordinate Compression", "Merge Sort (Inversion Count)"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Process right-to-left; BIT prefix query(rank-1) counts strictly smaller seen elements.",
    icon="🔴",
)

# ─── 2) Wipe old body ────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

# ─── 3) Build new body ───────────────────────────────────────────────────────
print("Building new body...")
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return an integer array ", {}),
        ("counts", {"code": True}),
        (" where ", {}),
        ("counts[i]", {"code": True}),
        (" is the number of elements to the right of ", {}),
        ("nums[i]", {"code": True}),
        (" that are strictly smaller than ", {}),
        ("nums[i]", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [5,2,6,1]", {"code": True}),
        (" → ", {}),
        ("[2,1,1,0]", {"code": True}),
        (" (5 has 2,1 smaller to right; 2 has 1; 6 has 1; 1 has none).", {}),
    ])),
    N.divider(),
]

# ─── Solution 1 — BIT + Coordinate Compression ───────────────────────────────
sol1_code = """\
from bisect import bisect_left

def countSmaller(nums):
    sorted_u = sorted(set(nums))            # coordinate compression
    rank = {v: i+1 for i, v in enumerate(sorted_u)}  # 1-indexed rank
    n, m = len(nums), len(sorted_u)
    bit = [0] * (m + 1)                     # Fenwick Tree, 1-indexed

    def update(i):
        while i <= m:
            bit[i] += 1
            i += i & (-i)                   # add lowest set bit (move to parent)

    def query(i):                           # prefix sum [1..i]
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)                   # strip lowest set bit (move to sibling)
        return s

    counts = [0] * n
    for i in range(n - 1, -1, -1):         # right to left
        r = rank[nums[i]]
        counts[i] = query(r - 1)           # count seen elements with rank < r
        update(r)                           # register current element
    return counts
"""

blocks += [
    N.h2("Solution 1 — BIT + Coordinate Compression (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each element, count how many elements to its right are strictly smaller. If we could process right-to-left and maintain a live count of seen values, we could answer each query immediately."),
        N.h4("What Doesn't Work"),
        N.para("Brute force (nested loops) is O(n²): for n=100,000 that is 10 billion operations — too slow. Sorting the array loses position information. A BST-based approach works but is complex to implement from scratch in an interview."),
        N.h4("The Key Observation"),
        N.para("A Binary Indexed Tree (Fenwick Tree) supports two O(log n) operations: point update (add 1 at rank r) and prefix sum query (count of elements with rank ≤ r). If we process right to left, all right-side elements are already registered when we reach position i. query(rank[nums[i]] - 1) gives exactly the count of strictly smaller seen elements."),
        N.h4("Building the Solution"),
        N.para("Step 1: Coordinate compress — map each value to its rank in sorted order (BIT requires integer indices in [1,m]). Step 2: For i from n-1 to 0: query BIT at rank-1 (count smaller), store as counts[i], then update BIT at rank (register element). Step 3: Return counts."),
        N.callout("Analogy: Imagine a library card catalog sorted by call number. Processing right-to-left, you add each book's call number to the catalog. For the current book, you count how many catalog entries have a lower call number — that's your answer in O(log n).", "🧠", "blue_background"),
    ]),
]

# Algorithm Deep-Dive
blocks += [
    N.h3("🔬 Algorithm Deep-Dive: Binary Indexed Tree (Fenwick Tree)"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Peter Fenwick, 1994. Class of problems: dynamic prefix sums over a frequency array. Supports point update + prefix sum query both in O(log n) with O(n) space.", {}),
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("bit[i]", {"code": True}),
        (" stores the cumulative count of elements in range ", {}),
        ("[i - lowbit(i) + 1 .. i]", {"code": True}),
        (" where ", {}),
        ("lowbit(i) = i & (-i)", {"code": True}),
        (" isolates the lowest set bit of i. This implicitly encodes a binary tree structure in a flat array.", {}),
    ])),
    N.code("# BIT core operations (1-indexed)\ndef update(i):\n    while i <= m:\n        bit[i] += 1\n        i += i & (-i)   # add lowest bit: move to parent\n\ndef query(i):           # prefix sum [1..i]\n    s = 0\n    while i > 0:\n        s += bit[i]\n        i -= i & (-i)   # strip lowest bit: move to left neighbor\n    return s\n\n# Example: query(6) traversal for n=8\n# i=6 → s+=bit[6]; i=6-2=4 → s+=bit[4]; i=4-4=0 stop\n# bit[6] covers [5..6], bit[4] covers [1..4] → sum covers [1..6]"),
    N.para(N.rich([
        ("Coordinate Compression: ", {"bold": True}),
        ("BIT indices must be in [1,m]. Values can be arbitrary (even negative). Map each unique value to its sorted rank: ", {}),
        ("sorted_u = sorted(set(nums)); rank = {v:i+1 for i,v in enumerate(sorted_u)}", {"code": True}),
        (". Only relative order matters, not actual values.", {}),
    ])),
    N.para(N.rich([
        ("When to recognize BIT: ", {"bold": True}),
        ('"Count of elements satisfying threshold dynamically" — any interleaved update+query pattern where queries ask for prefix counts. Classic signals: inversion count, smaller/larger to left/right, order statistics.', {}),
    ])),
]

blocks += [
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("sorted_u = sorted(set(nums))", {"code": True}), (" — Extract unique values and sort them. This is the domain for coordinate compression.", {})])),
    N.para(N.rich([("rank = {v: i+1 ...}", {"code": True}), (" — Map each value to its 1-indexed rank. 1-indexed because BIT uses index 0 as a sentinel.", {})])),
    N.para(N.rich([("bit = [0] * (m + 1)", {"code": True}), (" — BIT array of size m+1 (slots 1..m used; slot 0 unused as per BIT convention).", {})])),
    N.para(N.rich([("i += i & (-i)", {"code": True}), (" inside update — add lowest set bit moves to the parent node in the implicit BIT tree. This propagates the count upward.", {})])),
    N.para(N.rich([("i -= i & (-i)", {"code": True}), (" inside query — strip lowest set bit moves to the left sibling. This collects partial sums for the prefix.", {})])),
    N.para(N.rich([("for i in range(n-1, -1, -1)", {"code": True}), (" — Process right to left. When we process position i, all elements to the right (indices > i) are already in the BIT.", {})])),
    N.para(N.rich([("counts[i] = query(r - 1)", {"code": True}), (" — Prefix sum up to rank-1 = count of already-registered elements with rank strictly less than r = count of smaller elements to the right.", {})])),
    N.para(N.rich([("update(r)", {"code": True}), (" — Register nums[i] at its rank. Future queries from positions to the left will find it.", {})])),
    N.divider(),
]

# ─── Solution 2 — Modified Merge Sort ────────────────────────────────────────
sol2_code = """\
def countSmaller(nums):
    counts = [0] * len(nums)
    indexed = list(enumerate(nums))         # (original_index, value)

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left  = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        merged, l, r = [], 0, 0
        while l < len(left) and r < len(right):
            if left[l][1] > right[r][1]:   # left element larger: take it first
                # All remaining right elements are smaller than left[l]
                counts[left[l][0]] += len(right) - r
                merged.append(left[l]); l += 1
            else:
                merged.append(right[r]); r += 1
        while l < len(left):               # flush remaining left
            merged.append(left[l]); l += 1
        return merged + right[r:]

    merge_sort(indexed)
    return counts
"""

blocks += [
    N.h2("Solution 2 — Modified Merge Sort"),
    N.toggle_h3("💡 Intuition: Inversions During Merge", [
        N.h4("Reframe the Problem"),
        N.para("Count of smaller numbers to the right is equivalent to counting inversions per element. An inversion is a pair (i, j) where i < j but nums[i] > nums[j]."),
        N.h4("What Doesn't Work"),
        N.para("Standard merge sort loses original indices and doesn't count per-element. We need to track original positions through the sort."),
        N.h4("The Key Observation"),
        N.para("During the merge step of merge sort, when a right-half element is smaller than a left-half element and gets placed first, ALL remaining left-half elements (which are all ≥ current left element since left is sorted) each have this right element as a smaller element originally to their right."),
        N.h4("Building the Solution"),
        N.para("Pair each value with its original index. During merge: sort in descending order. When left[l] > right[r], all remaining right elements (r, r+1, ..., end) are smaller than left[l] — add len(right)-r to counts[left[l][0]]. This batches the count in O(1) per left element."),
        N.callout("The invariant: both halves are already sorted. When left[l] wins (is larger), every remaining right element is smaller than left[l]. We don't need to iterate — the count is exactly len(right) - r.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("indexed = list(enumerate(nums))", {"code": True}), (" — Store (original_index, value) pairs so we know which counts[] slot to update after sorting rearranges positions.", {})])),
    N.para(N.rich([("if left[l][1] > right[r][1]", {"code": True}), (" — Compare values. We are merging in descending order: larger elements go first.", {})])),
    N.para(N.rich([("counts[left[l][0]] += len(right) - r", {"code": True}), (" — All right elements from index r to end are smaller than left[l][1]. Since right is sorted, these are exactly the remaining right elements. Add them all at once.", {})])),
    N.para(N.rich([("return merged + right[r:]", {"code": True}), (" — Any remaining right elements need no count update (they are already smaller than all remaining left, but no left elements were processed after them).", {})])),
    N.divider(),
]

# ─── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(n)"],
        ["BIT + Coordinate Compression (Interview Pick)", "O(n log n)", "O(n)"],
        ["Modified Merge Sort", "O(n log n)", "O(n)"],
        ["SortedList (Python sortedcontainers)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Advanced Data Structures", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BIT + Coordinate Compression; Merge Sort (Inversion Count)", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Count of elements smaller/larger to the left/right' — dynamic order statistics. "
        "(2) Interleaved point updates and prefix sum queries (can't batch). "
        "(3) Values outside [1,n] range — always compress before using BIT. "
        "(4) 'Count inversions' — total inversions = sum of all counts[i].",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BIT + Coordinate Compression / Merge Sort Inversion technique:"),
    N.bullet(N.rich([("Reverse Pairs", {"bold": True}), (" (Hard) — Count pairs (i,j) where nums[i] > 2*nums[j]; same right-to-left BIT with modified query (#493)", {})])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), (" (Hard) — Count prefix sums falling in [lower, upper]; BIT on compressed prefix sums (#327)", {})])),
    N.bullet(N.rich([("Range Sum Query — Mutable", {"bold": True}), (" (Medium) — The foundational BIT problem: point update + range sum (#307)", {})])),
    N.bullet(N.rich([("Number of Pairs Satisfying Inequality", {"bold": True}), (" (Hard) — Count pairs with difference constraint; BIT + compression (#2426)", {})])),
    N.bullet(N.rich([("Falling Squares", {"bold": True}), (" (Hard) — Interval coordinate compression; max segment height query (#699)", {})])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), (" (Hard) — Compress x-coords; sweep with max heap or segment tree (#218)", {})])),
    N.bullet(N.rich([("K-th Smallest in Sorted Matrix", {"bold": True}), (" (Medium) — Binary search on answer; related order-statistics reasoning (#378)", {})])),
    N.para("These problems share the core technique: dynamic frequency histogram with O(log n) update and prefix query."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Advanced Data Structures section. Sub-pattern BIT + Coordinate Compression. Source: Analysis (not explicitly listed as a single entry in guide; derived from advanced DS section).", "📚", "gray_background"),
]

# ─── Embed ───────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
