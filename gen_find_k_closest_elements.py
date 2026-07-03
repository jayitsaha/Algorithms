"""
gen_find_k_closest_elements.py
Notion in-place update for: Find K Closest Elements (#658)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8196-9b84-f7172667306c"

# ─── 1. Properties ───────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=658,
    pattern="Binary Search",
    subpatterns=["Binary Search on Left Bound"],
    tc="O(log n + k)",
    sc="O(1)",
    key_insight="k closest elements in a sorted array are always contiguous — binary search for the window start index in [0, n-k].",
    icon="🟡",
)
print("Properties set.")

# ─── 2. Wipe old body ─────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ─── 3. Build new body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted integer array "),
        ("arr", {"code": True}),
        (", two integers "),
        ("k", {"code": True}),
        (" and "),
        ("x", {"code": True}),
        (", return the "),
        ("k", {"code": True}),
        (" closest integers to "),
        ("x", {"code": True}),
        (" in the array, sorted in ascending order. Closeness is measured by absolute difference |arr[i] - x|. When two elements are equally close, prefer the smaller one."),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("arr=[1,2,3,4,5], k=4, x=3  ->  [1,2,3,4]. Both [1,2,3,4] and [2,3,4,5] have total distance 4, but [1,2,3,4] wins the tiebreak (contains smaller elements)."),
    ])),
    N.divider(),
]

# ── Solution 1 — Binary Search on Left Bound ──
sol1_code = """\
def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1   # arr[mid] strictly farther — shift window right
        else:
            hi = mid       # arr[mid] as close or closer (tie → prefer smaller)
    return arr[lo : lo + k]
"""

blocks += [
    N.h2("Solution 1 — Binary Search on Left Bound (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The array is sorted. Sorted data always carries structure. The key simplification: k closest elements in a sorted array are always contiguous. You never need to scatter-pick — they form a window. So the problem becomes: where does the window start?"),
        N.h4("What Doesn't Work"),
        N.para("Sorting by distance to x (O(n log n)) ignores the sorted order entirely — it's wasteful. The two-pointer shrink approach (O(n-k)) works but isn't as fast as possible. We can binary search the window start."),
        N.h4("The Key Observation"),
        N.para("The window start index lives in [0, n-k]. That is a finite search space. If we pick any mid as candidate start, the window is arr[mid..mid+k-1]. The only question: should we shift right (lo = mid+1) or stay/shift left (hi = mid)? We answer by comparing the two competing endpoints: arr[mid] vs arr[mid+k]."),
        N.h4("Building the Solution"),
        N.para("If x - arr[mid] > arr[mid+k] - x, then arr[mid] is strictly farther from x than arr[mid+k]. Swapping arr[mid] out and arr[mid+k] in strictly improves the window — so mid cannot be optimal. Set lo = mid + 1. Otherwise arr[mid] is at least as close — on a tie, smaller wins (arr[mid] < arr[mid+k] since array is sorted) — so hi = mid. The loop terminates when lo == hi."),
        N.callout("Analogy: Imagine sliding a magnifying glass of width k along a ruler. You only need to compare the left edge and the first mark just to its right to decide whether to slide right or not.", "🔍", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(arr) - k", {"code": True}), " — Search space for window start: lo is the leftmost valid start (index 0), hi is the rightmost valid start (index n-k). Beyond n-k, fewer than k elements remain."])),
    N.para(N.rich([("while lo < hi:", {"code": True}), " — Standard 'find leftmost' binary search loop. Terminates when lo == hi (one candidate remains)."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — Safe integer midpoint. The candidate window is arr[mid..mid+k-1]."])),
    N.para(N.rich([("if x - arr[mid] > arr[mid + k] - x:", {"code": True}), " — Is arr[mid] strictly farther from x than arr[mid+k]? If yes, the window should shift right."])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), " — arr[mid] cannot be in the optimal window. All starts ≤ mid are eliminated."])),
    N.para(N.rich([("hi = mid", {"code": True}), " — arr[mid] is at least as close (or ties and arr[mid] is smaller). Keep mid in contention. Note: hi = mid not mid-1, because mid could itself be the answer."])),
    N.para(N.rich([("return arr[lo : lo + k]", {"code": True}), " — The optimal window of size k starting at lo. Already sorted because arr is sorted."])),
    N.callout("Why strict > and not >=? Ties break left: arr[mid] < arr[mid+k] (sorted order). So tied distances prefer arr[mid]. We only shift right when arr[mid] is STRICTLY farther.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2 — Two-Pointer Shrink ──
sol2_code = """\
def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    left, right = 0, len(arr) - 1
    while right - left >= k:          # keep shrinking until exactly k remain
        if x - arr[left] > arr[right] - x:
            left += 1                 # left endpoint farther — remove it
        else:
            right -= 1               # right endpoint farther or tied — remove it
    return arr[left : right + 1]
"""

blocks += [
    N.h2("Solution 2 — Two-Pointer Shrink"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with all n elements. We need to eliminate n-k of them, keeping the k closest. Since the answer is contiguous, at every step we only need to remove the farther of the two endpoints."),
        N.h4("The Key Observation"),
        N.para("Compare arr[left] and arr[right]. Whichever is farther from x gets removed. Ties remove the right (larger) endpoint. Repeat until exactly k elements remain."),
        N.h4("Building the Solution"),
        N.para("This runs in O(n-k) time — we do n-k removals, one per iteration. Space O(1). Simpler to explain than binary search, though asymptotically slower."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("left, right = 0, len(arr) - 1", {"code": True}), " — Start with the full array window."])),
    N.para(N.rich([("while right - left >= k:", {"code": True}), " — Keep looping while more than k elements remain."])),
    N.para(N.rich([("if x - arr[left] > arr[right] - x:", {"code": True}), " — If left endpoint is strictly farther, eliminate it."])),
    N.para(N.rich([("right -= 1", {"code": True}), " — Otherwise right endpoint is farther or tied (ties remove right = larger element)."])),
    N.para(N.rich([("return arr[left : right + 1]", {"code": True}), " — The remaining k elements."])),
    N.divider(),
]

# ── Solution 3 — Brute Force ──
sol3_code = """\
def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    # Sort by (distance, value), take first k, re-sort by value
    return sorted(sorted(arr, key=lambda a: (abs(a - x), a))[:k])
"""

blocks += [
    N.h2("Solution 3 — Sort by Distance (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct interpretation: compute distance from x for every element, sort by that distance, take the k smallest, then re-sort by value. Simple and correct."),
        N.h4("What Doesn't Work"),
        N.para("O(n log n) — ignores the sorted structure entirely. Use only as a sanity check or starting point in an interview. Always follow up with a faster approach."),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (sort by distance)", "O(n log n)", "O(n)"],
        ["Two-Pointer Shrink", "O(n − k)", "O(1)"],
        ["Binary Search on Left Bound ✓", "O(log(n−k) + k)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Binary Search on Left Bound — searching for the leftmost valid window start index, using the comparison x - arr[mid] > arr[mid+k] - x to eliminate the left side."])),
    N.callout(
        "When to recognize this pattern: (1) Sorted array + find k closest/best elements. (2) The answer is always a contiguous subarray of fixed size k. (3) You need a starting position, not a value. (4) Search space is [0, n-k] — a finite index space. (5) Loop termination is lo < hi with hi = mid (leftmost pattern).",
        "🔎",
        "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search on Left Bound / Answer):"),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — Binary search the answer (eating speed); lo=1, hi=max(piles). Same leftmost-valid-position pattern. (#875)"])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), " (Medium) — Binary search on minimum capacity. (#1011)"])),
    N.bullet(N.rich([("Find First and Last Position of Element in Sorted Array", {"bold": True}), " (Medium) — Binary search for leftmost and rightmost occurrences. (#34)"])),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), " (Easy) — Classic find-leftmost binary search; template: lo=0,hi=n,while lo<hi. (#35)"])),
    N.bullet(N.rich([("Find K-th Smallest Pair Distance", {"bold": True}), " (Hard) — Binary search on answer (distance value) + sliding window over sorted array. (#719)"])),
    N.bullet(N.rich([("Minimum Limit of Balls in a Bag", {"bold": True}), " (Medium) — Binary search on answer with feasibility check. (#1760)"])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), " (Medium) — Binary search for a leftmost property in a modified sorted array. (#153)"])),
    N.para("These problems all share the core technique: binary search to find the leftmost position satisfying a monotonic condition, with search space over indices or answer values rather than direct element values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search). Sub-Pattern: Binary Search on Left Bound (variant: BS on Answer space). Source: Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_k_closest_elements")),
    N.para(N.rich([
        ("Step through the binary search on window start visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
