"""
gen_number_of_pairs_satisfying_inequality.py
Full Notion pipeline for LeetCode 2426 — Number of Pairs Satisfying Inequality
Pattern: Advanced Data Structures / BIT + Merge Sort
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

# ── Step 0: create page (notion_page_id is null) ──────────────────────────────
print("Creating new Notion page...")
PAGE_ID = N.create_page("Number of Pairs Satisfying Inequality", 2426, "Hard", "🔴")
print(f"  Created page: {PAGE_ID}")

# ── Step 1: set properties ────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2426,
    pattern="Advanced Data Structures",
    subpatterns=["BIT + Merge Sort"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Transform to A[k]=nums1[k]-nums2[k], then count pairs i<j with A[i]<=A[j]+diff using BIT with coordinate compression.",
    icon="🔴"
)
print("  Properties set.")

# ── Step 2: append body blocks ────────────────────────────────────────────────
print("Building Notion page body...")

PROBLEM_STMT = (
    "Given two 0-indexed integer arrays nums1 and nums2, each of length n, "
    "and an integer diff, return the number of pairs (i, j) such that i < j and "
    "nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff."
)

INTUITION_TRANSFORM = (
    "Rearranging: (nums1[i]-nums2[i]) - (nums1[j]-nums2[j]) <= diff. "
    "Define A[k] = nums1[k] - nums2[k]. The condition becomes A[i] - A[j] <= diff, "
    "i.e., A[i] <= A[j] + diff. For each j, count previous i's where A[i] <= A[j]+diff."
)

BIT_SOLUTION_CODE = '''\
from bisect import bisect_right

def numberOfPairs(nums1, nums2, diff):
    A = [a - b for a, b in zip(nums1, nums2)]
    # Coordinate compression
    vals = sorted(set(A + [a + diff for a in A]))
    rank = {v: i+1 for i, v in enumerate(vals)}
    m = len(vals)
    bit = [0] * (m + 1)

    def update(i):
        while i <= m:
            bit[i] += 1
            i += i & (-i)

    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    ans = 0
    for a in A:
        threshold_rank = rank[a + diff]
        ans += query(threshold_rank)
        update(rank[a])
    return ans\
'''

MERGE_SOLUTION_CODE = '''\
def numberOfPairs(nums1, nums2, diff):
    A = [a - b for a, b in zip(nums1, nums2)]

    def merge_sort(arr):
        if len(arr) <= 1:
            return 0, arr
        mid = len(arr) // 2
        lc, left  = merge_sort(arr[:mid])
        rc, right = merge_sort(arr[mid:])
        count = lc + rc
        # Count cross-half pairs: for each right[j], count left[i] <= right[j]+diff
        p = 0
        for rj in right:
            while p < len(left) and left[p] <= rj + diff:
                p += 1
            count += p
        # Standard merge
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged += left[i:] + right[j:]
        return count, merged

    ans, _ = merge_sort(A)
    return ans\
'''

BRUTE_CODE = '''\
def numberOfPairs(nums1, nums2, diff):
    n, ans = len(nums1), 0
    for i in range(n):
        for j in range(i+1, n):
            if nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff:
                ans += 1
    return ans\
'''

BIT_DEEP_DIVE = (
    "Binary Indexed Tree (BIT / Fenwick Tree), invented by Peter Fenwick (1994). "
    "Supports O(log n) prefix-sum queries and point-updates in O(n) space. "
    "Core operation: lowbit(i) = i & (-i) — the lowest set bit of i. "
    "Update: add to BIT[i], then BIT[i + lowbit(i)], etc. (propagate up). "
    "Query: sum BIT[i], then BIT[i - lowbit(i)], etc. (strip lowest bit, go down). "
    "Invariant: BIT[i] stores the sum for indices [i - lowbit(i) + 1 .. i]."
)

MERGE_DEEP_DIVE = (
    "Modified Merge Sort for inversion counting (classic Divide & Conquer). "
    "During the merge step of two sorted halves L and R: for each R[j], "
    "find how many L[i] satisfy L[i] <= R[j]+diff. Because L is sorted, "
    "a pointer p only ever advances — giving O(n) per merge level, O(n log n) total. "
    "This generalizes the classic 'count inversions' (where condition is L[i] > R[j])."
)

MERGE_NOTE = (
    "Note: Merge sort does not require coordinate compression because it works directly "
    "in value-space. However, it modifies the original array (returns sorted), so you "
    "must work on a copy of A. BIT approach preserves original array order."
)

# Build blocks list
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1 — BIT (Interview Pick)
blocks += [
    N.h2("Solution 1 — BIT + Coordinate Compression (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Two arrays, four terms — simplify first. Move all i-terms left and j-terms right: "
               "(nums1[i]-nums2[i]) - (nums1[j]-nums2[j]) <= diff. "
               "Define A[k] = nums1[k]-nums2[k]. Condition: A[i] <= A[j]+diff for i<j."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: check all O(n^2) pairs. With n up to 10^5, that's 10^10 operations — TLE. "
               "Sorting A[] alone loses the index-ordering constraint (we need i<j)."),
        N.h4("The Key Observation"),
        N.para("For each j (scanning left to right), we ask: how many already-seen values A[i] satisfy "
               "A[i] <= A[j]+diff? This is a prefix-count query on a dynamic multiset — exactly what a "
               "Binary Indexed Tree supports in O(log n) per query and update."),
        N.h4("Building the Solution"),
        N.para("1. Compute A[k]=nums1[k]-nums2[k]. "
               "2. Coordinate-compress all values (A[] union thresholds A[k]+diff) to 1-based ranks. "
               "3. Sweep j=0..n-1: query BIT up to rank(A[j]+diff), add to answer, insert rank(A[j]). "
               "Query before insert enforces the i<j constraint."),
        N.callout(
            "Analogy: Think of BIT as a running scoreboard. "
            "Each element 'registers its score' (update). When a new element arrives, "
            "it asks: how many registered scores are below my threshold? (query prefix sum). "
            "BIT answers in O(log n) instead of scanning all registered scores O(n).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Binary Indexed Tree"),
    N.para(BIT_DEEP_DIVE),
    N.code(
        "# BIT template\n"
        "bit = [0] * (m + 1)  # 1-indexed\n\n"
        "def update(i):  # add 1 at position i\n"
        "    while i <= m:\n"
        "        bit[i] += 1\n"
        "        i += i & (-i)  # move to next ancestor\n\n"
        "def query(i):  # prefix sum [1..i]\n"
        "    s = 0\n"
        "    while i > 0:\n"
        "        s += bit[i]\n"
        "        i -= i & (-i)  # strip lowest bit\n"
        "    return s\n\n"
        "# Generalize: for count of elements <= threshold\n"
        "# compress values to 1-based ranks, query prefix sum at rank(threshold)"
    ),
    N.h3("Code"),
    N.code(BIT_SOLUTION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("A = [a - b ...]", {"code": True}), " — transform problem: A[k] = nums1[k] - nums2[k]"])),
    N.para(N.rich([("vals = sorted(set(A + [a + diff ...]))", {"code": True}), " — collect all unique values: elements AND thresholds; both must be in rank map"])),
    N.para(N.rich([("rank = {v: i+1 ...}", {"code": True}), " — 1-based rank assignment; BIT indices must be >= 1"])),
    N.para(N.rich([("bit = [0] * (m + 1)", {"code": True}), " — BIT array of size m+1 (index 0 unused)"])),
    N.para(N.rich([("i += i & (-i)", {"code": True}), " — in update: move to parent by adding lowest set bit"])),
    N.para(N.rich([("i -= i & (-i)", {"code": True}), " — in query: strip lowest set bit to traverse ancestors"])),
    N.para(N.rich([("threshold_rank = rank[a + diff]", {"code": True}), " — the upper bound rank for this j: count elements with value <= a+diff"])),
    N.para(N.rich([("ans += query(threshold_rank)", {"code": True}), " — count all i < j with A[i] <= A[j]+diff"])),
    N.para(N.rich([("update(rank[a])", {"code": True}), " — insert current A[j] AFTER query (enforces i < j)"])),
    N.callout(
        "Warning: Always query BEFORE update. Updating first counts the pair (j,j) which is invalid.",
        "⚠️", "yellow_background"
    ),
    N.callout(
        "Warning: Include both A[k] and A[k]+diff in coordinate compression. Threshold values (A[j]+diff) must map to valid ranks or query will KeyError.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Merge Sort
blocks += [
    N.h2("Solution 2 — Merge Sort Inversion Counting"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same transformation: count pairs i<j where A[i] <= A[j]+diff. "
               "Think of it as counting 'modified non-inversions' across merge sort halves."),
        N.h4("What Doesn't Work"),
        N.para("Pure merge sort alone only sorts; it doesn't count cross-half pairs. "
               "We need to hook into the merge step to count before sorting."),
        N.h4("The Key Observation"),
        N.para("During merge of sorted halves L and R: for any R[j], all L[i] with L[i] <= R[j]+diff "
               "are valid (i was in left half, j in right half, so original index i < j). "
               "Since L is sorted, pointer p only moves forward — amortized O(1) per element."),
        N.h4("Building the Solution"),
        N.para("Recursively sort+count left half, sort+count right half. "
               "Then for the cross-half count: advance pointer p while L[p] <= R[j]+diff, "
               "add p to count for each R[j]. Finally merge the two sorted halves normally."),
        N.callout(
            "Analogy: Merge sort naturally produces sorted halves. We piggyback a pointer sweep "
            "onto the merge step — counting valid pairs for free while we sort.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Merge Sort Inversion Counting"),
    N.para(MERGE_DEEP_DIVE),
    N.para(MERGE_NOTE),
    N.h3("Code"),
    N.code(MERGE_SOLUTION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(arr) <= 1: return 0, arr", {"code": True}), " — base case: one element, zero pairs, already sorted"])),
    N.para(N.rich([("lc, left = merge_sort(arr[:mid])", {"code": True}), " — recurse left: returns (pair_count, sorted_left)"])),
    N.para(N.rich([("rc, right = merge_sort(arr[mid:])", {"code": True}), " — recurse right: returns (pair_count, sorted_right)"])),
    N.para(N.rich([("count = lc + rc", {"code": True}), " — start with pairs found entirely within each half"])),
    N.para(N.rich([("p = 0", {"code": True}), " — pointer into left half; never resets (monotonically advances)"])),
    N.para(N.rich([("while p < len(left) and left[p] <= rj + diff:", {"code": True}), " — advance while L[p] within threshold for this R[j]"])),
    N.para(N.rich([("count += p", {"code": True}), " — all left[0..p-1] satisfy condition for this right[j]"])),
    N.para(N.rich([("merged = []; while i < len(left) and j < len(right): ...", {"code": True}), " — standard O(n) merge for sorted output"])),
    N.divider(),
]

# Solution 3 — Brute Force
blocks += [
    N.h2("Solution 3 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check every (i,j) pair directly. Apply the inequality as stated."),
        N.h4("What Doesn't Work"),
        N.para("O(n^2) time. With n=10^5 this is 10^10 operations — about 100 seconds, TLE."),
        N.h4("The Key Observation"),
        N.para("This IS correct — just too slow. Use as a baseline to verify the optimal solution's output on small examples."),
        N.h4("Building the Solution"),
        N.para("Double loop: for each i in [0,n), for each j in (i,n), check condition. Increment counter if satisfied."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n): for j in range(i+1, n):", {"code": True}), " — iterate all valid pairs (i<j)"])),
    N.para(N.rich([("if nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff:", {"code": True}), " — apply the original inequality directly"])),
    N.para(N.rich([("ans += 1", {"code": True}), " — count valid pair"])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["BIT + Coordinate Compression", "O(n log n)", "O(n)"],
        ["Merge Sort Inversion Counting", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Advanced Data Structures (Guide Section 20)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BIT + Merge Sort (Guide Section 20.1 — Binary Indexed Tree / Segment Tree)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count pairs (i<j) where f(A[i]) <= g(A[j])' — BIT with sweep\n"
        "• Values can be large/negative — coordinate compress first\n"
        "• 'Count elements seen so far with value <= threshold' — BIT prefix query\n"
        "• Cross-half pair counting during sort — modified merge sort\n"
        "• n up to 10^5, need O(n log n) — BIT or Merge Sort",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BIT + Coordinate Compression / Merge Sort Inversion):"),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), " (Hard) — BIT + coordinate compression; for each num, count smaller elements to its right"])),
    N.bullet(N.rich([("Reverse Pairs", {"bold": True}), " (Hard) — Modified merge sort; count pairs where nums[i] > 2*nums[j], j>i"])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), " (Hard) — Merge sort; count prefix sums falling in [lower, upper]"])),
    N.bullet(N.rich([("Range Sum Query - Mutable", {"bold": True}), " (Medium) — Classic BIT use: point updates + range prefix sum queries"])),
    N.bullet(N.rich([("Range Sum Query 2D - Mutable", {"bold": True}), " (Medium) — 2D BIT extension of the 1D case"])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), " (Hard) — Segment Tree / BIT for max queries during line sweep"])),
    N.bullet(N.rich([("Number of Inversions", {"bold": True}), " (Classic) — Count pairs i<j where A[i]>A[j]; the direct predecessor to this problem"])),
    N.para("These problems share the core technique: dynamic prefix queries on a BIT or inversion counting via modified merge sort."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 20.1 — Binary Indexed Tree / Segment Tree", "📚", "gray_background"),
]

# Interactive embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_pairs_satisfying_inequality")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)

# ── Output the page ID for status file ────────────────────────────────────────
print(f"PAGE_ID={PAGE_ID}")
