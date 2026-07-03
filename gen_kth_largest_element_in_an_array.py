"""
gen_kth_largest_element_in_an_array.py
Regenerates the Notion page for LeetCode #215 — Kth Largest Element in an Array.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f7-807c-c6db5b315f90"
SLUG = "kth_largest_element_in_an_array"

# ── 1. Set Properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=215,
    pattern="Sorting",
    subpatterns=["QuickSelect O(n) Average"],
    tc="O(n) average",
    sc="O(1)",
    key_insight="Map kth-largest to index n-k; partition around random pivot; recurse into one half only.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old content ──────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Build new body ────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "), ("nums", {"code": True}),
        (" and an integer "), ("k", {"code": True}),
        (", return the "), ("kth largest element", {"bold": True}),
        (" in the array. Note that it is the kth largest element in sorted order, not the kth distinct element. You must solve it in O(n) average time complexity.")
    ])),
    N.para(N.rich([
        ("Example 1: "), ("nums = [3,2,1,5,6,4], k = 2", {"code": True}),
        (" → "), ("5", {"bold": True}),
        (" (sorted: [1,2,3,4,5,6], index n−k = 4 → value 5).")
    ])),
    N.para(N.rich([
        ("Example 2: "), ("nums = [3,2,3,1,2,4,5,5,6], k = 4", {"code": True}),
        (" → "), ("4", {"bold": True}),
        (" (sorted: [1,2,2,3,3,4,5,5,6], index 9−4=5 → value 4).")
    ])),
    N.divider(),
]

# ── Solution 1: QuickSelect (Interview Pick) ──────────────────────────
sol1_code = '''\
import random

def findKthLargest(nums: list[int], k: int) -> int:
    target = len(nums) - k  # kth largest = (n-k)th smallest

    def partition(lo: int, hi: int) -> int:
        # Random pivot to avoid O(n^2) worst case
        pi = random.randint(lo, hi)
        nums[pi], nums[hi] = nums[hi], nums[pi]
        pivot = nums[hi]
        store = lo
        for i in range(lo, hi):
            if nums[i] <= pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        return store  # pivot's final sorted index

    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1   # target is in right half
        else:
            hi = p - 1   # target is in left half\
'''

blocks += [
    N.h2("Solution 1 — QuickSelect (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We don't need the array fully sorted — we only need to know where ONE element ends up. The kth largest element is at index n−k in the sorted-ascending array. If we could cheaply put one element at its sorted position without sorting everything else, we'd be done."),
        N.h4("What Doesn't Work"),
        N.para("Full sorting is O(n log n). That's the brute force — correct but sub-optimal. A heap of size k is O(n log k). For large k, this is barely better than sorting. We want O(n)."),
        N.h4("The Key Observation"),
        N.para("QuickSort's partition step places ONE element (the pivot) at its correct sorted index in O(n) time. After partitioning: everything left of the pivot is ≤ pivot, everything right is ≥ pivot. The pivot is permanently placed. If the pivot landed at our target index, we're done — no further recursion needed at all."),
        N.h4("Building the Solution"),
        N.para("Translate: kth largest = element at index target = n−k in sorted order. Pick a random pivot, partition the current subarray, get the pivot's final index p. If p == target, return nums[p]. If p < target, the answer is in the right half — narrow lo. If p > target, the answer is in the left half — narrow hi. Average case: each call halves remaining work → O(n + n/2 + n/4 + ...) = O(2n) = O(n)."),
        N.callout("Analogy: Imagine sorting a deck of cards by asking 'Is the 5th card from the left > or < this pivot?' You only flip the half that matters — you never touch the other half again.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: QuickSelect"),
    N.para(N.rich([
        ("QuickSelect", {"bold": True}),
        (" was introduced by Tony Hoare in 1961, the same year he published QuickSort. It solves the ", {}),
        ("order statistics problem", {"bold": True}),
        (": find the kth smallest/largest element in an unordered list. It is a specialization of QuickSort that avoids sorting the half that doesn't contain the answer.", {})
    ])),
    N.para(N.rich([
        ("Core invariant:", {"bold": True}),
        (" After partition(lo, hi) returns p, nums[p] is at its correct sorted position: nums[lo..p-1] ≤ nums[p] ≤ nums[p+1..hi]. This position is permanent.")
    ])),
    N.para(N.rich([
        ("Why it works:", {"bold": True}),
        (" Each partition call does O(hi−lo+1) work and places ONE element permanently. We only recurse into ONE subarray. Recurrence: T(n) = T(n/2) + O(n) → O(n) by geometric series.")
    ])),
    N.para(N.rich([
        ("When to recognize it:", {"bold": True}),
        (" Any problem asking 'find the kth smallest/largest' with O(n) time constraint. Also applicable to k-closest points, median finding, and top-k queries.")
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("target = len(nums) - k", {"code": True}), (" — Convert the problem: kth largest in descending order is the (n−k)th element in ascending order. This is our target index.")])),
    N.para(N.rich([("pi = random.randint(lo, hi)", {"code": True}), (" — Pick a random pivot index in the current range. Randomization prevents worst-case O(n²) on sorted/reverse-sorted inputs.")])),
    N.para(N.rich([("nums[pi], nums[hi] = nums[hi], nums[pi]", {"code": True}), (" — Move the pivot to the end of the current subarray. This keeps it out of the scan loop's way.")])),
    N.para(N.rich([("store = lo", {"code": True}), (" — The 'write pointer': marks where the next element that is ≤ pivot should go. Starts at the left boundary.")])),
    N.para(N.rich([("for i in range(lo, hi):", {"code": True}), (" — Scan every element in [lo, hi−1]. We skip hi because that's where our pivot is parked.")])),
    N.para(N.rich([("if nums[i] <= pivot:", {"code": True}), (" — If this element belongs in the left zone (≤ pivot), swap it with the store position and advance store.")])),
    N.para(N.rich([("nums[store], nums[hi] = nums[hi], nums[store]", {"code": True}), (" — After the scan, 'store' is the exact index where the pivot belongs. Place the pivot there.")])),
    N.para(N.rich([("return store", {"code": True}), (" — The pivot's final index p. Everything in [lo..p−1] ≤ nums[p] ≤ [p+1..hi]. Pivot is permanently placed.")])),
    N.para(N.rich([("if p == target: return nums[p]", {"code": True}), (" — Found it! Pivot landed exactly at target index. nums[p] is the kth largest.")])),
    N.para(N.rich([("elif p < target: lo = p + 1", {"code": True}), (" — Target is to the right of pivot. Discard the left half — we never touch it again.")])),
    N.para(N.rich([("else: hi = p - 1", {"code": True}), (" — Target is to the left of pivot. Discard the right half.")])),
    N.divider(),
]

# ── Solution 2: Min-Heap ─────────────────────────────────────────────
sol2_code = '''\
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, num)    # O(log k)
        if len(heap) > k:
            heapq.heappop(heap)      # Evict smallest; keep k largest
    return heap[0]                   # Smallest of the k largest = kth largest\
'''

blocks += [
    N.h2("Solution 2 — Min-Heap of Size k"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Imagine you're watching numbers arrive one by one and must always know the kth largest seen so far. You can't store everything — that's too much memory."),
        N.h4("What Doesn't Work"),
        N.para("Sorting after each element: O(n²) total. Max-heap of all elements: O(n) space but O(n log n) to build."),
        N.h4("The Key Observation"),
        N.para("A min-heap of exactly k elements always holds the k largest elements seen so far. The min-heap's minimum (heap[0]) is the smallest of those k — the kth largest overall. Whenever we see a new element larger than the current kth largest (heap[0]), we admit it and evict the old kth largest."),
        N.h4("Building the Solution"),
        N.para("Push each number. If heap grows beyond k, pop the minimum. After all n elements, heap[0] is the kth largest. Time: O(n log k). Space: O(k). This is optimal for the streaming case."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), (" — Python's heapq module always gives a min-heap. heap[0] is always the smallest element.")])),
    N.para(N.rich([("heapq.heappush(heap, num)", {"code": True}), (" — O(log k) push. Heap maintains the invariant: smallest element at root.")])),
    N.para(N.rich([("if len(heap) > k: heapq.heappop(heap)", {"code": True}), (" — When the heap exceeds k elements, pop the minimum. We always keep the k largest elements seen so far.")])),
    N.para(N.rich([("return heap[0]", {"code": True}), (" — After processing all n elements, the heap holds the top k largest. The minimum of those (heap[0]) is by definition the kth largest.")])),
    N.divider(),
]

# ── Solution 3: Sort ─────────────────────────────────────────────────
sol3_code = '''\
def findKthLargest(nums: list[int], k: int) -> int:
    nums.sort()          # O(n log n) Timsort in-place
    return nums[-k]      # -k indexes from end: -1=max, -2=2nd max, etc.\
'''

blocks += [
    N.h2("Solution 3 — Sort and Index (Simplest)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If the array were sorted ascending, the kth largest is at index n−k, or equivalently at index −k from the end."),
        N.h4("The Key Observation"),
        N.para("Python's sort is in-place and reliable. nums.sort() then nums[-k] is a one-liner. Propose this first in interviews to establish correctness, then optimize."),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Sort & Index", "O(n log n)", "O(1)", "Simplest; always correct"],
        ["Min-Heap (size k)", "O(n log k)", "O(k)", "Best for streaming / read-only array"],
        ["QuickSelect (random pivot)", "O(n) avg, O(n²) worst", "O(1)", "Optimal average; recommended"],
        ["Median of Medians", "O(n) worst", "O(log n)", "Guaranteed O(n) worst; high constants"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting (order statistics)")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("QuickSelect O(n) Average")])),
    N.callout(
        "When to recognize this pattern: Problem asks for 'kth largest/smallest'. Needs O(n) time with O(1) space. Equivalent phrasing: 'top-k elements', 'find the median', 'k closest points'. The key signal is that you need ONE element's rank, not a full sorted order.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same QuickSelect / order-statistic technique:"),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — QuickSelect by frequency or bucket sort; same partial-selection framing (#347)")])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), (" (Medium) — QuickSelect by Euclidean distance; exact same algorithm (#973)")])),
    N.bullet(N.rich([("Sort Colors", {"bold": True}), (" (Medium) — Dutch National Flag 3-way partition; generalization of the partition step (#75)")])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — Binary search on value space; same 'find kth element' framing (#378)")])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps for dynamic kth element; generalization of the heap approach (#295)")])),
    N.bullet(N.rich([("Wiggle Sort II", {"bold": True}), (" (Medium) — Requires finding the median via QuickSelect before interleaving (#324)")])),
    N.bullet(N.rich([("Third Maximum Number", {"bold": True}), (" (Easy) — Same concept: find 3rd distinct maximum using a sorted set of size 3 (#414)")])),
    N.para("These problems share the core technique: finding one element's rank without full sorting."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section, QuickSelect O(n) Average sub-pattern.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
