"""
Notion updater for: Find the Kth Largest Integer in the Array
LeetCode #1985 | Medium | Sorting + String Compare + QuickSelect
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8143-8c79-f4a527e831f7"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1985,
    pattern="Sorting",
    subpatterns=["String Compare + QuickSelect"],
    tc="O(n) avg",
    sc="O(1)",
    key_insight="Compare numeric strings by length first, then lexicographically; QuickSelect finds k-th largest in O(n) average without full sort.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} blocks.")

# ── 3. Build new body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of strings ", {}),
        ("nums", {"code": True}),
        (" where each string represents a non-negative integer (no leading zeros). You are also given an integer ", {}),
        ("k", {"code": True}),
        (". Return the ", {}),
        ("k", {"code": True}),
        ("-th largest integer in ", {}),
        ("nums", {"code": True}),
        (" as a string. Note: numbers can be up to 100 digits long — too large for standard 64-bit integers in most languages.", {}),
    ])),
    N.para("Example: nums=[\"3\",\"6\",\"7\",\"10\",\"2\"], k=2 → \"7\" (sorted desc: 10,7,6,3,2 → 2nd is 7)"),
    N.divider(),
]

# ── Solution 1: Custom Sort ──
blocks += [
    N.h2("Solution 1 — Custom Sort (Interview Starting Point)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("We need the k-th largest numeric string. If we could sort them in numeric descending order, the answer is at index k-1. The challenge: sorting these strings as numbers. Alphabetical order fails (\"10\" < \"2\" alphabetically). We need a custom comparator."),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("Direct alphabetical sort: \"10\" comes before \"2\" because '1' < '2' character-wise, but numerically 10 > 2. Also int() parsing fails for very large numbers in Java/C++/Go (but works in Python with arbitrary precision)."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("For non-negative integers with NO leading zeros: (1) a longer string is always a larger number; (2) if two strings have the same length, lexicographic order matches numeric order (left-most differing digit determines the winner). This gives a complete, correct ordering."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Write a comparator: if len(a) != len(b), longer wins. Else, compare lexicographically. Sort with this comparator ascending, return nums[-k] for the k-th largest."),
        N.callout("Analogy: Think of numbers in decimal. If one has more digits it's always bigger (no leading zeros). If same digits, compare left-to-right — exactly what lex comparison does.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code('''from functools import cmp_to_key

def kthLargestNumber_sort(nums, k):
    def cmp(a, b):
        # If different lengths: longer string = bigger number
        if len(a) != len(b):
            return len(a) - len(b)   # negative=a<b, positive=a>b
        # Same length: lexicographic order matches numeric order
        return (a > b) - (a < b)     # -1, 0, or 1

    nums.sort(key=cmp_to_key(cmp))   # ascending sort
    return nums[-k]                  # k-th largest = index -k'''),
    N.h3("Line by Line"),
    N.para(N.rich([("cmp(a, b)", {"code": True}), (" — custom comparator returning negative/0/positive for a<b/a==b/a>b", {})])),
    N.para(N.rich([("if len(a) != len(b)", {"code": True}), (" — length check: a number with more digits is always larger (no leading zeros)", {})])),
    N.para(N.rich([("return len(a) - len(b)", {"code": True}), (" — negative means a shorter = a smaller; positive means a longer = a bigger", {})])),
    N.para(N.rich([("return (a > b) - (a < b)", {"code": True}), (" — same-length strings: lex order matches numeric order; returns -1/0/1", {})])),
    N.para(N.rich([("nums.sort(key=cmp_to_key(cmp))", {"code": True}), (" — Python's sort using our custom comparator; O(n log n)", {})])),
    N.para(N.rich([("return nums[-k]", {"code": True}), (" — ascending sort, so k-th largest is at index -k (from the end)", {})])),
    N.divider(),
]

# ── Solution 2: QuickSelect ──
blocks += [
    N.h2("Solution 2 — QuickSelect (Optimal, O(n) Average — Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("We need ONE specific element — the k-th largest. Sorting every element just to find one is wasteful. Can we narrow down to the answer without a full sort?"),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("Full sort is O(n log n). A simple linear scan finds the maximum but not the k-th largest without k passes. We need something smarter that exploits the partition idea."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("After partitioning around a pivot, the pivot ends up at its exact sorted position p. If p == target, done. If p < target, the k-th element must be to the right. If p > target, it must be to the left. We recurse only into one half each time — cutting work geometrically."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Target index = n - k (k-th largest in ascending order). Lomuto partition: walk pointer i from lo to hi-1, swap elements <= pivot to the front (store position), finally place pivot at store. Recurse into only the relevant half until p == target."),
        N.callout("Analogy: Like binary search but for finding position rather than value. Each round, we eliminate one half of the remaining candidates without inspecting it further.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code('''def kthLargestNumber(nums, k):
    def num_gt(a, b):
        """Return True if string a represents a numerically greater value than b."""
        if len(a) != len(b):
            return len(a) > len(b)   # longer string = bigger number
        return a > b                  # same length: lex order = numeric order

    def partition(lo, hi):
        """Lomuto partition: pivot = nums[hi]. Returns pivot\'s final sorted index."""
        pivot = nums[hi]
        store = lo                    # next position for elements <= pivot
        for i in range(lo, hi):
            if not num_gt(nums[i], pivot):  # nums[i] <= pivot
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]  # place pivot
        return store                  # pivot is now at its final sorted position

    target = len(nums) - k            # k-th largest in ascending array = index n-k
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == target:
            return nums[p]            # pivot landed exactly where we need it!
        elif p < target:
            lo = p + 1                # answer is to the right of pivot
        else:
            hi = p - 1                # answer is to the left of pivot'''),
    N.h3("Line by Line"),
    N.para(N.rich([("num_gt(a, b)", {"code": True}), (" — string comparator: True if a > b numerically. Handles different-length and same-length cases.", {})])),
    N.para(N.rich([("pivot = nums[hi]", {"code": True}), (" — Lomuto scheme picks last element as pivot. Simple; randomizing improves worst case.", {})])),
    N.para(N.rich([("store = lo", {"code": True}), (" — marks the boundary: everything at index < store is numerically <= pivot.", {})])),
    N.para(N.rich([("if not num_gt(nums[i], pivot)", {"code": True}), (" — checks if nums[i] <= pivot; if so, swap into the 'small' region and advance store.", {})])),
    N.para(N.rich([("nums[store], nums[hi] = nums[hi], nums[store]", {"code": True}), (" — places pivot at its final sorted position. All elements left are smaller, all right are larger.", {})])),
    N.para(N.rich([("target = len(nums) - k", {"code": True}), (" — maps k-th largest to 0-indexed position in ascending sorted array.", {})])),
    N.para(N.rich([("if p == target: return nums[p]", {"code": True}), (" — pivot landed exactly at our target position — this is the answer.", {})])),
    N.para(N.rich([("elif p < target: lo = p+1", {"code": True}), (" — answer is to the right; narrow window from the left.", {})])),
    N.para(N.rich([("else: hi = p-1", {"code": True}), (" — answer is to the left; narrow window from the right.", {})])),
    N.callout("QuickSelect Deep-Dive: Invented by Tony Hoare (1961), same inventor as QuickSort. Core invariant: after partition, pivot is at exact final sorted position. Work: n + n/2 + n/4 + ... = 2n = O(n) average. Unlike QuickSort, we recurse only ONE half per round. Worst case O(n²) on adversarial input with last-element pivot — fix by randomizing: swap random index with hi before partitioning.", "🔬", "blue_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Custom Sort", "O(n log n · L)", "O(log n)"],
        ["QuickSelect (avg)", "O(n · L)", "O(1)"],
        ["QuickSelect (worst)", "O(n² · L)", "O(1)"],
        ["Min-Heap size k", "O(n log k · L)", "O(k)"],
    ]),
    N.para("L = average string length (up to 100). Custom Sort and Min-Heap are deterministically bounded; QuickSelect's average is achieved with random pivot selection."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("String Compare + QuickSelect (custom comparator for numeric strings; partition-based selection)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Problem asks for k-th largest/smallest element. "
        "(2) Data is given as strings representing numbers. "
        "(3) O(n) time is expected or hinted. "
        "(4) The array can be mutated in-place. "
        "Signal words: 'k-th largest', 'numeric strings', 'find without sorting all'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (QuickSelect / custom comparator / k-th order statistic):"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium, LC 215) — classic QuickSelect with integer comparator", {})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium, LC 347) — QuickSelect on frequency map values", {})])),
    N.bullet(N.rich([("Find K Closest Points to Origin", {"bold": True}), (" (Medium, LC 973) — QuickSelect on Euclidean distances", {})])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}), (" (Medium, LC 451) — custom comparator on character frequency", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium, LC 378) — binary search variant for k-th order", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard, LC 295) — two-heap approach for dynamic k=n/2", {})])),
    N.bullet(N.rich([("Largest Number", {"bold": True}), (" (Medium, LC 179) — custom sort comparator for digit strings", {})])),
    N.para("These problems share the insight: define a correct ordering (comparator), then either sort with it or use QuickSelect to find a specific position."),
    N.callout("Sub-Pattern verified via Analysis — 'String Compare + QuickSelect' combines the custom string comparator technique with the QuickSelect algorithm. The sorting pattern is confirmed in DSA_Patterns_and_SubPatterns_Guide.md.", "📚", "gray_background"),
]

# ── Interactive Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_the_kth_largest_integer_in_the_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
