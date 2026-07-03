"""
gen_k_closest_points_to_origin.py
Rebuilds the Notion page for LeetCode #973 K Closest Points to Origin in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-814d-ad9b-fe87091ff992"
SLUG    = "k_closest_points_to_origin"

# ── 1. Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=973,
    pattern="Heaps",
    subpatterns=["Max Heap of Size K"],
    tc="O(n log k)",
    sc="O(k)",
    key_insight="Maintain a max heap of size k; the root is always the current farthest candidate. Negate distances to simulate max-heap with Python's min-heap.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ──────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of ", {}),
        ("points", {"code": True}),
        (" on a 2D plane where ", {}),
        ("points[i] = [xi, yi]", {"code": True}),
        (", return the ", {}),
        ("k", {"code": True}),
        (" closest points to the origin ", {}),
        ("(0, 0)", {"code": True}),
        (". Euclidean distance is √(xi² + yi²). The answer may be returned in any order.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("points = [[1,3],[-2,2]], k = 1", {"code": True}),
        (" → ", {}),
        ("[[-2,2]]", {"code": True}),
        (" (dist=√8 < dist=√10)", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Max Heap of Size K ──
SOL1_CODE = """\
import heapq

def kClosest(points, k):
    heap = []                                    # max heap via negation
    for x, y in points:
        dist_sq = x*x + y*y                      # squared distance; skip sqrt
        heapq.heappush(heap, (-dist_sq, x, y))   # negate: largest dist at root
        if len(heap) > k:                        # heap over capacity?
            heapq.heappop(heap)                  # evict farthest (root)
    return [[x, y] for (_, x, y) in heap]        # extract coordinates"""

blocks += [
    N.h2("Solution 1 — Max Heap of Size K (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the k smallest distances among n points. 'Smallest k values from a stream' is the canonical max-heap-of-size-k problem."),
        N.h4("What Doesn't Work"),
        N.para("Sorting all n points gives O(n log n) — correct but wasteful when k ≪ n. We sorted far more than necessary."),
        N.h4("The Key Observation"),
        N.para("We only need to track k candidates at any time. A max heap capped at k acts as a 'club with k spots': the farthest current member (heap root) is always the one to kick out when a better candidate arrives."),
        N.h4("Building the Solution"),
        N.para("Push each point as (-dist_sq, x, y) — negated so Python's min-heap behaves as a max-heap. After each push, if heap size exceeds k, pop the root (most-negative key = largest actual distance). After n points, heap holds exactly the k closest."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}),
                    ("A nightclub with k=2 spots. Each new arrival challenges the current 'most distant from origin' member. If the newcomer is closer, they get in and the farthest member leaves.", {})]),
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), (" — Initialize empty list; will be used as a max heap via negation.", {})])),
    N.para(N.rich([("dist_sq = x*x + y*y", {"code": True}), (" — Squared Euclidean distance. No sqrt needed — same ordering, avoids floating-point.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (-dist_sq, x, y))", {"code": True}), (" — Push negative distance. Most-negative = largest actual distance floats to root.", {})])),
    N.para(N.rich([("if len(heap) > k:", {"code": True}), (" — Check if heap is over capacity.", {})])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), (" — Evict the root = the current farthest point (most-negative key). Heap back to size k.", {})])),
    N.para(N.rich([("return [[x, y] for (_, x, y) in heap]", {"code": True}), (" — Unpack tuples; discard negated distance (_ ), keep x and y coordinates.", {})])),
    N.callout(
        N.rich([("Warning: ", {"bold": True}),
                ("Forgetting to negate (-dist_sq) makes heappush behave as a min-heap, evicting the CLOSEST points — exactly backwards. Always negate for max-heap simulation in Python.", {})]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Sort All ──
SOL2_CODE = """\
def kClosest(points, k):
    points.sort(key=lambda p: p[0]**2 + p[1]**2)  # sort all by squared distance
    return points[:k]                              # first k are closest"""

blocks += [
    N.h2("Solution 2 — Sort All Points"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we sort all n points by distance, the first k are trivially the answer."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n log n) — correct but not optimal. When k = 1 and n = 10^6, sorting 10^6 points to find 1 is wasteful."),
        N.h4("The Key Observation"),
        N.para("Sorting is O(n log n) regardless of k. Best when k ≈ n (you needed to sort most of them anyway) or when simplicity matters most."),
        N.h4("Building the Solution"),
        N.para("Sort in-place by lambda p: p[0]**2 + p[1]**2 (squared distance), then slice the first k. Python's sort is O(n log n), stable, and in-place."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("points.sort(key=lambda p: p[0]**2 + p[1]**2)", {"code": True}), (" — Sort all n points by squared distance ascending. O(n log n).", {})])),
    N.para(N.rich([("return points[:k]", {"code": True}), (" — Slice the first k points; these have the smallest distances. O(k) slice operation.", {})])),
    N.divider(),
]

# ── Solution 3 — QuickSelect ──
SOL3_CODE = """\
import random

def kClosest(points, k):
    def dist(p): return p[0]**2 + p[1]**2

    def quickselect(lo, hi):
        pivot = dist(points[random.randint(lo, hi)])  # random pivot
        l, r, m = lo, hi, lo                          # 3-way DNF partition
        while m <= r:
            d = dist(points[m])
            if d < pivot:
                points[l], points[m] = points[m], points[l]; l += 1; m += 1
            elif d > pivot:
                points[m], points[r] = points[r], points[m]; r -= 1
            else:
                m += 1
        if k <= l:    return quickselect(lo, l-1)   # answer in left
        elif k <= m:  return                        # answer spans pivot
        else:         return quickselect(m, hi)     # answer in right

    quickselect(0, len(points) - 1)
    return points[:k]"""

blocks += [
    N.h2("Solution 3 — QuickSelect (O(n) Average)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We don't need to SORT all n points — we just need to PARTITION them so the k closest end up on one side. This is exactly what QuickSelect does."),
        N.h4("The Key Observation"),
        N.para("QuickSelect is like quicksort but only recurses into the partition containing the answer. Average O(n) because we halve the search space each time."),
        N.h4("Building the Solution"),
        N.para("Use a random pivot and 3-way Dutch National Flag partition. After partitioning, check which side index k falls on; recurse only there. In-place, no extra space."),
        N.callout(
            "Risk: Worst case O(n²) with adversarial input (use random pivot to mitigate). Hard to implement correctly under interview pressure. Use heap solution unless interviewer asks for O(n).",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Sort All Points", "O(n log n)", "O(1)", "Simplest; best when k ≈ n"],
        ["Max Heap of k (Interview Pick)", "O(n log k)", "O(k)", "Optimal for k ≪ n; handles streams"],
        ["QuickSelect", "O(n) avg / O(n²) worst", "O(1)", "Best avg; tricky; in-place"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Max Heap of Size K", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ('Any "find k smallest/largest/closest/most-frequent" from n items. '
                 'Key signals: (1) output size k is a parameter, (2) k ≪ n possible, '
                 '(3) data may be a stream. The max heap of size k maintains the best k '
                 'candidates in O(k) space, processing each new element in O(log k).', {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Max Heap of Size K technique:"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Min heap of size k; root is the kth largest. LeetCode #215", {})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — Heap by frequency count; bucket sort alternative. LeetCode #347", {})])),
    N.bullet(N.rich([("Top K Frequent Words", {"bold": True}), (" (Medium) — Same pattern with lexicographic tiebreaker. LeetCode #692", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps (max + min) to maintain running median. LeetCode #295", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — Min heap with (val, row, col) for multi-source merge. LeetCode #378", {})])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}), (" (Medium) — Max heap by character frequency, then reconstruct string. LeetCode #451", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy + max heap; always schedule most-frequent remaining task. LeetCode #621", {})])),
    N.para("These problems share the core pattern: maintain a bounded heap of size k as a sliding filter over n elements."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section. Sub-Pattern: Max Heap of Size K · Source: Analysis", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
