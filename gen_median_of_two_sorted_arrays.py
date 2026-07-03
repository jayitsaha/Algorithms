"""
gen_median_of_two_sorted_arrays.py
Regenerates the Notion page for LeetCode #4 — Median of Two Sorted Arrays
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ad-b67c-de969955c732"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=4,
    pattern="Binary Search",
    subpatterns=["Binary Search on Partition"],
    tc="O(log(min(m,n)))",
    sc="O(1)",
    key_insight="Binary search on partition index i in the shorter array; once i is fixed, j = half_len - i is determined, and we check n1L<=n2R AND n2L<=n1R for validity.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ──
BRUTE_CODE = '''\
def findMedianSortedArrays_brute(nums1, nums2):
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n//2-1] + merged[n//2]) / 2.0
'''

LINEAR_CODE = '''\
def findMedianSortedArrays_linear(nums1, nums2):
    m, n = len(nums1), len(nums2)
    total = m + n
    mid = total // 2
    i = j = 0
    prev = curr = 0
    for k in range(mid + 1):
        prev = curr
        if i < m and (j >= n or nums1[i] <= nums2[j]):
            curr = nums1[i]; i += 1
        else:
            curr = nums2[j]; j += 1
    if total % 2 == 1:
        return float(curr)
    return (prev + curr) / 2.0
'''

OPTIMAL_CODE = '''\
def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the shorter array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2  # left half size (+1 handles odd totals)
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2        # elements from nums1 in left half
        j = half_len - i          # elements from nums2 in left half
        n1L = nums1[i-1] if i > 0 else float('-inf')
        n1R = nums1[i]   if i < m else float('inf')
        n2L = nums2[j-1] if j > 0 else float('-inf')
        n2R = nums2[j]   if j < n else float('inf')
        if n1L <= n2R and n2L <= n1R:
            # Valid partition found
            max_left = max(n1L, n2L)
            if (m + n) % 2 == 1:
                return float(max_left)
            return (max_left + min(n1R, n2R)) / 2.0
        elif n1L > n2R:
            hi = i - 1   # took too many from nums1
        else:
            lo = i + 1   # took too few from nums1
'''

blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two sorted arrays "),
        ("nums1", {"code": True}),
        (" of size "),
        ("m", {"code": True}),
        (" and "),
        ("nums2", {"code": True}),
        (" of size "),
        ("n", {"code": True}),
        (", return the median of the two sorted arrays. The overall run time complexity must be "),
        ("O(log(m+n))", {"code": True}),
        (".")
    ])),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force: Merge and Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The median is the middle value of the combined sorted elements. If we had the merged sorted array, finding the median is trivial — it's the element(s) at the center."),
        N.h4("What Doesn't Work (Why We Go Beyond This)"),
        N.para("Concatenating and sorting takes O((m+n)log(m+n)) time and O(m+n) space. The problem explicitly requires O(log(m+n)), so this approach doesn't satisfy the constraint. However, it's a good starting point to verify your answer logic."),
        N.h4("The Key Observation"),
        N.para("For odd total length n: median = merged[n//2]. For even total length n: median = (merged[n//2-1] + merged[n//2]) / 2. This single formula works for both cases."),
        N.h4("Building the Solution"),
        N.para("Concatenate both arrays, sort, then index the middle. Use (m+n+1)//2 to identify the left-middle index."),
        N.callout("Analogy: Line up all students by height. The median is the student in the middle of the line.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("merged = sorted(nums1 + nums2)", {"code": True}), " — concatenate both arrays and sort. O((m+n)log(m+n)) time, O(m+n) space."])),
    N.para(N.rich([("n = len(merged)", {"code": True}), " — total number of elements."])),
    N.para(N.rich([("if n % 2 == 1", {"code": True}), " — odd total: return the single middle element at index n//2."])),
    N.para(N.rich([("return (merged[n//2-1] + merged[n//2]) / 2.0", {"code": True}), " — even total: average the two middle elements."])),
    N.divider(),
]

# ── Solution 2: Two-Pointer ──
blocks += [
    N.h2("Solution 2 — Two-Pointer (O(m+n), no extra space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We don't need the full merged array — we just need to reach the middle elements. We can simulate the merge with two pointers, stopping when we reach position mid."),
        N.h4("What Doesn't Work"),
        N.para("Creating the full merged array wastes memory. We only need the element(s) at index (m+n)//2 and optionally (m+n)//2-1."),
        N.h4("The Key Observation"),
        N.para("By advancing the smaller of nums1[i] and nums2[j] at each step, we simulate a merge traversal. After mid+1 advances, curr holds the right-middle element and prev holds the left-middle element."),
        N.h4("Building the Solution"),
        N.para("Use two indices i and j into nums1 and nums2. In each step, advance the pointer to the smaller element. After mid+1 steps, read off curr and prev."),
        N.callout("This is O(m+n) time and O(1) space — better than brute force, but still linear and doesn't satisfy the log constraint.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(LINEAR_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for k in range(mid + 1)", {"code": True}), " — advance mid+1 steps through the simulated sorted merge."])),
    N.para(N.rich([("prev = curr", {"code": True}), " — save the previous element before updating; needed to compute even-total average."])),
    N.para(N.rich([("if i < m and (j >= n or nums1[i] <= nums2[j])", {"code": True}), " — take from nums1 if it has elements left and is smaller (or nums2 is exhausted)."])),
    N.para(N.rich([("return (prev + curr) / 2.0", {"code": True}), " — even total: average the two elements at positions mid-1 and mid."])),
    N.divider(),
]

# ── Solution 3: Binary Search on Partition (Optimal) ──
blocks += [
    N.h2("Solution 3 — Binary Search on Partition (Optimal, Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The median defines a split of all elements into two equal halves. Instead of 'find the middle index,' think: 'find a partition of BOTH arrays so every element on the left ≤ every element on the right, and the halves are equal size.' This reformulation reveals a binary-searchable problem."),
        N.h4("What Doesn't Work"),
        N.para("Any linear scan (merge, two-pointer) is O(m+n) and violates the O(log) constraint. We need a way to cut the search space in half with each step."),
        N.h4("The Key Observation"),
        N.para("Once we fix how many elements from nums1 go to the left half (call it i), the count from nums2 is determined: j = half_len - i. As i increases, nums1's left boundary increases monotonically. Binary search on i finds the one valid partition in O(log(min(m,n))) steps."),
        N.h4("Building the Solution"),
        N.para("Binary search i in [0..m]. At each i, compute j = half_len - i. Check if n1L <= n2R and n2L <= n1R. If yes, compute median. If n1L > n2R, move left. Otherwise move right. Use ±infinity sentinels for boundary cases."),
        N.callout("Analogy: You have two decks of sorted cards on a table. You want to split BOTH decks simultaneously so the left piles together contain exactly half the cards, and the biggest card on any left pile is no bigger than the smallest card on any right pile. Binary search the split position in the smaller deck.", "🧠", "blue_background"),
    ]),
]

N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks (solutions 1-3 intros).")

blocks2 = []
blocks2 += [
    N.h3("🔬 Algorithm Deep-Dive: Binary Search on Partition"),
    N.para(N.rich([
        ("Core Insight: ", {"bold": True}),
        ("The partition of the combined elements at the median is uniquely determined by how many elements from nums1 appear on the left (call this "),
        ("i", {"code": True}),
        ("). Since j = half_len - i is then fixed, and the validity condition is monotone in i, binary search converges in O(log m) steps.")
    ])),
    N.para(N.rich([
        ("Why Only Four Comparisons Needed: ", {"bold": True}),
        ("Both arrays are independently sorted. If the four boundary values satisfy n1L ≤ n2R and n2L ≤ n1R, then ALL elements on the left are ≤ ALL elements on the right, by transitivity through the sorted order of each array.")
    ])),
    N.para(N.rich([
        ("Sentinel Trick: ", {"bold": True}),
        ("Use "),
        ("-infinity", {"code": True}),
        (" when i=0 (nothing from nums1 on left) and "),
        ("+infinity", {"code": True}),
        (" when i=m (all of nums1 on left). This makes the boundary checks work without special cases.")
    ])),
    N.callout(
        "When to recognize this pattern: Two sorted arrays + O(log) constraint. Also: 'Find kth smallest in two sorted arrays' uses the same idea, eliminating k/2 candidates per step.",
        "🔎", "green_background"
    ),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(nums1) > len(nums2): nums1, nums2 = nums2, nums1", {"code": True}), " — always binary search the shorter array so j stays in valid range [0..n]."])),
    N.para(N.rich([("half_len = (m + n + 1) // 2", {"code": True}), " — left half size. The +1 before // means odd totals get one extra element (the median itself) in the left half."])),
    N.para(N.rich([("lo, hi = 0, m", {"code": True}), " — search range: 0 means take nothing from nums1, m means take all."])),
    N.para(N.rich([("i = (lo + hi) // 2", {"code": True}), " — try taking i elements from nums1 for the left half."])),
    N.para(N.rich([("j = half_len - i", {"code": True}), " — compensate with j elements from nums2."])),
    N.para(N.rich([("n1L = nums1[i-1] if i > 0 else float('-inf')", {"code": True}), " — left boundary of nums1's contribution (-inf if empty)."])),
    N.para(N.rich([("n1R = nums1[i] if i < m else float('inf')", {"code": True}), " — right boundary of nums1's contribution (+inf if all taken)."])),
    N.para(N.rich([("n2L, n2R", {"code": True}), " — same boundary logic applied to nums2."])),
    N.para(N.rich([("if n1L <= n2R and n2L <= n1R", {"code": True}), " — valid partition: every left element ≤ every right element."])),
    N.para(N.rich([("max_left = max(n1L, n2L)", {"code": True}), " — the largest element in the combined left half."])),
    N.para(N.rich([("if (m+n) % 2 == 1: return float(max_left)", {"code": True}), " — odd total: the median IS max_left (middle element)."])),
    N.para(N.rich([("return (max_left + min(n1R, n2R)) / 2.0", {"code": True}), " — even total: average of two middle elements."])),
    N.para(N.rich([("elif n1L > n2R: hi = i - 1", {"code": True}), " — took too many from nums1 (n1L too large), shrink from right."])),
    N.para(N.rich([("else: lo = i + 1", {"code": True}), " — n2L > n1R: took too few from nums1, grow from left."])),
    N.callout("Common mistake: Forgetting to search the shorter array. If m > n and you search nums1, j could become negative for small i values, causing an index error.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks2 += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (merge + sort)", "O((m+n)log(m+n))", "O(m+n)"],
        ["Two-Pointer (count to median)", "O(m+n)", "O(1)"],
        ["Binary Search on Partition ✓", "O(log(min(m,n)))", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks2 += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search on Partition")])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Two sorted arrays with O(log) time required\n"
        "• 'Find kth element across two sorted arrays'\n"
        "• Need to split combined elements at a specific rank without merging\n"
        "• Any problem where choosing a split in one array determines the split in another",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks2 += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Find K-th Smallest Pair Distance", {"bold": True}), (" (Hard) — Binary search on answer distance with two-pointer counting to verify (#719)")])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — Binary search on eating speed; same 'search on the answer' template (#875)")])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — Binary search on ship capacity (#1011)")])),
    N.bullet(N.rich([("Split Array Largest Sum", {"bold": True}), (" (Hard) — Binary search on maximum subarray sum (#410)")])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), (" (Medium) — Binary search on value with count predicate (#287)")])),
    N.bullet(N.rich([("Search in Rotated Sorted Array", {"bold": True}), (" (Medium) — Classic binary search with modified boundary conditions (#33)")])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium) — Binary search identifying which unsorted half to discard (#153)")])),
    N.para("These problems share the core technique: binary search on a parameter where the feasibility check is monotone."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search). Sub-Pattern: Binary Search on Partition. Source: Guide Section 9 + Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks2 += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("median_of_two_sorted_arrays")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks2)
print(f"Appended {len(blocks2)} blocks (solution detail + complexity + pattern + related + embed).")
print("NOTION OK", PAGE_ID)
