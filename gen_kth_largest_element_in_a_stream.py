"""
gen_kth_largest_element_in_a_stream.py
Regenerates the Notion page for LeetCode #703 Kth Largest Element in a Stream.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8141-abc7-e3f790c7b88e"

# ── 1) Set page properties ────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=703,
    pattern="Heaps",
    subpatterns=["Min Heap of Size K"],
    tc="O(n log k)",
    sc="O(k)",
    key_insight="Maintain a min-heap of exactly k elements; heap[0] is always the k-th largest.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old content ───────────────────────────────────────────────────────
print("Wiping old content...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Build the new page body ────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a class ", {}),
        ("KthLargest", {"code": True}),
        (" that finds the ", {}),
        ("k", {"code": True}),
        ("-th largest element in a stream. Note that it is the ", {}),
        ("k", {"code": True}),
        ("-th largest element in the sorted order, not the ", {}),
        ("k", {"code": True}),
        ("-th distinct element. Implement ", {}),
        ("KthLargest(int k, int[] nums)", {"code": True}),
        (" which initializes the object with the integer ", {}),
        ("k", {"code": True}),
        (" and the stream of integers ", {}),
        ("nums", {"code": True}),
        (", and ", {}),
        ("int add(int val)", {"code": True}),
        (" which appends the integer ", {}),
        ("val", {"code": True}),
        (" to the stream and returns the element representing the ", {}),
        ("k", {"code": True}),
        ("-th largest element in the stream.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Min-Heap of Size K (Interview Pick) ─────────────────────────
blocks += [
    N.h2("Solution 1 — Min-Heap of Size K (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the k-th largest element across all values seen in the stream, and we need this answer to update efficiently every time a new value arrives. Re-stated: at any moment, we want the smallest element among the top-k values seen so far."),
        N.h4("What Doesn't Work"),
        N.para("Storing all elements and sorting on every add() call is O(n log n) per add — as the stream grows, this degrades badly. Keeping a max-heap of all n elements and popping k times is O(k log n) per query and uses O(n) memory for the whole stream."),
        N.h4("The Key Observation"),
        N.para("We don't need all n values — only the top-k. If we maintain a collection of exactly the k largest values seen so far, then by definition the k-th largest is the smallest in that collection. A min-heap of size k surfaces that minimum in O(1) at heap[0], and updates in O(log k) per add."),
        N.h4("Building the Solution"),
        N.para("1. Keep a min-heap that never exceeds k elements. 2. On each add(val): push val, then if size > k, pop the minimum (it can't be the k-th largest if k values are larger). 3. heap[0] is always the answer. For __init__, reuse add() to process the initial nums — avoids duplicated push+trim logic."),
        N.callout("Analogy: imagine a club with exactly k members ranked by skill. When a new applicant arrives, they challenge the weakest member. If they're stronger, the weakest is evicted. The weakest remaining member is always the k-th strongest overall. The min-heap IS that club with O(log k) challenges.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for num in nums:
            self.add(num)   # reuse add() — DRY pattern

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)       # O(log k) push
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)         # evict the minimum
        return self.heap[0]                  # k-th largest
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("import heapq", {"code": True}), (" — Python's built-in min-heap module. heap[0] is always the minimum.", {})])),
    N.para(N.rich([("self.k = k", {"code": True}), (" — Store k so add() can reference it for the size check.", {})])),
    N.para(N.rich([("self.heap = []", {"code": True}), (" — Start with an empty heap; will be capped at k elements.", {})])),
    N.para(N.rich([("for num in nums: self.add(num)", {"code": True}), (" — Feed each initial element through add() to build the top-k heap without duplicating logic.", {})])),
    N.para(N.rich([("heapq.heappush(self.heap, val)", {"code": True}), (" — O(log k) push. The heap may now have k+1 elements temporarily.", {})])),
    N.para(N.rich([("if len(self.heap) > self.k: heapq.heappop(self.heap)", {"code": True}), (" — If we exceeded k, pop the minimum. It's the (k+1)-th largest and doesn't belong in the top-k.", {})])),
    N.para(N.rich([("return self.heap[0]", {"code": True}), (" — The minimum of the top-k values is the k-th largest across all values seen. O(1) to read.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Sort on Every Add"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest mental model: keep all elements in a list. When asked for k-th largest, sort descending and return index k-1."),
        N.h4("What Doesn't Work"),
        N.para("Sorting is O(n log n) per add() call. As n grows, each call takes longer. This is fine for tiny inputs but unacceptable for streams with thousands of elements."),
        N.h4("The Key Observation"),
        N.para("The brute force establishes correctness and gives us a baseline. We mention it first in the interview to show we understand the problem, then optimize."),
        N.h4("Building the Solution"),
        N.para("Append val to a list. Sort descending. Return element at index k-1 (0-based). Simple and unambiguous but O(n log n) per add."),
    ]),
    N.h3("Code"),
    N.code("""\
class KthLargestBrute:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.data = list(nums)

    def add(self, val: int) -> int:
        self.data.append(val)
        self.data.sort(reverse=True)    # O(n log n) — slow
        return self.data[self.k - 1]   # k-th largest (0-based)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.data.append(val)", {"code": True}), (" — Add the new value to the list.", {})])),
    N.para(N.rich([("self.data.sort(reverse=True)", {"code": True}), (" — Sort descending: O(n log n). Most expensive part.", {})])),
    N.para(N.rich([("return self.data[self.k - 1]", {"code": True}), (" — Index k-1 in a 0-based sorted-desc list gives the k-th largest.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "add() Time", "__init__ Time", "Space"],
        ["Brute Force (sort)", "O(n log n)", "O(n log n)", "O(n)"],
        ["Min-Heap Size K (optimal)", "O(log k)", "O(n log k)", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Heap of Size K (Top-K streaming)", {})])),
    N.callout(
        "When to recognize this pattern: You see 'k-th largest/smallest' or 'top-k' with dynamic/streaming data. "
        "The need for efficient updates (not just a one-time query) is the key signal. Also applies when memory is constrained "
        "— you can't store all n elements but you can store k.",
        "🔎", "green_background"
    ),
    N.callout(
        "Note: Min Heap of Size K is classified under the Heaps pattern in the DSA Patterns Guide. "
        "It is distinct from Two Heaps (used for median), Merge K Sorted, and Greedy + Heap patterns.",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Min Heap of Size K technique:"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Static array version. Same heap approach O(n log k) or use Quickselect O(n) avg.", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps: max-heap for lower half + min-heap for upper half. Direct extension of this pattern.", {})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — Min-heap of size k over (frequency, element) pairs. Same trim-to-k logic.", {})])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), (" (Medium) — Max-heap of size k over distance. Discard farthest when size exceeds k.", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Min-heap stores one node per list; always pop the global minimum.", {})])),
    N.bullet(N.rich([("Ugly Number II", {"bold": True}), (" (Medium) — Min-heap generates k-th ugly number on demand.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max-heap greedily schedules most-frequent task; Greedy + Heap pattern.", {})])),
    N.para("These problems share the core technique: use a heap of bounded size k to track a running order statistic over dynamic data."),
    N.divider(),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("kth_largest_element_in_a_stream")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
