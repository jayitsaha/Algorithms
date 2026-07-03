"""
gen_find_median_from_data_stream.py
Rebuilds the Notion page for LeetCode #295 Find Median from Data Stream (IN-PLACE).
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81f0-8f00-fd758dccb280"
SLUG    = "find_median_from_data_stream"

# ── 1. Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=295,
    pattern="Heaps",
    subpatterns=["Two Heaps"],
    tc="O(log n)",
    sc="O(n)",
    key_insight="Split stream into lower/upper halves: max-heap left + min-heap right. Median is at their tops in O(1).",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure that supports two operations: ", {}),
        ("addNum(int num)", {"code": True}),
        (" — adds a number from the data stream to the data structure, and ", {}),
        ("findMedian()", {"code": True}),
        (" — returns the median of all elements so far. ", {}),
        ("addNum", {"code": True}),
        (" must run in O(log n) and ", {}),
        ("findMedian", {"code": True}),
        (" must run in O(1).", {}),
    ])),
    N.callout(
        N.rich([
            ("Median: ", {"bold": True}),
            ("Middle element when count is odd; average of two middle elements when count is even. "
             "Example: [1,2,3] → 2.0 | [1,2,3,4] → 2.5", {}),
        ]),
        "📊", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Two Heaps (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Two Heaps: Max-Heap Left + Min-Heap Right (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to find the middle of a sorted version of all numbers seen so far — "
            "after each insertion. If we always knew the 'split point' between the smaller half "
            "and the larger half, the median would be right there. We don't need the full sorted "
            "order — just the max of the lower half and the min of the upper half."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Sorting all n elements after each insertion costs O(n log n) per add. "
            "Maintaining a sorted array with in-place insertion costs O(n) per add (shifting). "
            "Neither scales when you have millions of stream elements with frequent median queries."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The median is determined by just two values: the largest element of the lower half "
            "and the smallest element of the upper half. A max-heap exposes its maximum in O(1). "
            "A min-heap exposes its minimum in O(1). So: use a max-heap for the lower half, "
            "a min-heap for the upper half, keep them balanced in size, and you have O(1) median."
        ),
        N.h4("Building the Solution"),
        N.para(
            "addNum: (1) Always push to the left max-heap. (2) Always cross-push left's maximum "
            "to the right min-heap — this maintains the order invariant: left's max ≤ right's min. "
            "(3) If right grew larger than left, move right's minimum back to left — this restores "
            "the balance invariant: left can have at most 1 more element.\n\n"
            "findMedian: If equal sizes, average both tops. If left has one more, return left's top."
        ),
        N.callout(
            "Analogy: Imagine sorting students by height in two lines facing each other. "
            "The tallest in the 'short line' (left) and the shortest in the 'tall line' (right) "
            "are always at the boundary — the median is their average (or the tallest short student "
            "if odd count). You only ever need to look at the front of each line.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Two Heaps"),
    N.para(N.rich([
        ("Pattern: Two Heaps. ", {"bold": True}),
        ("Classic technique for streaming median. Maintains two complementary heaps: a max-heap "
         "for the lower half and a min-heap for the upper half, each exposing their boundary in O(1). "
         "The protocol — always push to left, always cross-push to right, rebalance if right > left "
         "— guarantees both invariants (order and balance) are maintained after every operation.", {}),
    ])),
    N.code(
        "# Core invariants after every addNum:\n"
        "# (1) ORDER: max(left) <= min(right)\n"
        "# (2) BALANCE: len(left) == len(right) or len(left) == len(right) + 1\n\n"
        "# addNum protocol (always 2-3 heap ops = O(log n)):\n"
        "# Step 1: heappush(left, -num)          <- push to left always\n"
        "# Step 2: heappush(right, -heappop(left)) <- cross-push (fixes order)\n"
        "# Step 3: if len(right) > len(left):    <- fix balance\n"
        "#             heappush(left, -heappop(right))\n\n"
        "# findMedian:\n"
        "# if len(left) > len(right): return -left[0]       <- odd: left's top\n"
        "# else: return (-left[0] + right[0]) / 2.0          <- even: avg tops"
    ),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "class MedianFinder:\n\n"
        "    def __init__(self):\n"
        "        self.left = []   # max-heap (stores negatives)\n"
        "        self.right = []  # min-heap (stores positives)\n\n"
        "    def addNum(self, num: int) -> None:\n"
        "        # Step 1: push to left max-heap\n"
        "        heapq.heappush(self.left, -num)\n"
        "        # Step 2: always cross-push left's max to right (fixes order invariant)\n"
        "        heapq.heappush(self.right, -heapq.heappop(self.left))\n"
        "        # Step 3: rebalance if right grew larger (fixes balance invariant)\n"
        "        if len(self.right) > len(self.left):\n"
        "            heapq.heappush(self.left, -heapq.heappop(self.right))\n\n"
        "    def findMedian(self) -> float:\n"
        "        if len(self.left) > len(self.right):\n"
        "            return float(-self.left[0])             # odd: left's top\n"
        "        return (-self.left[0] + self.right[0]) / 2.0  # even: average tops"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.left = []", {"code": True}), (" — max-heap implemented via negatives; left[0] = -(max element in left half)", {})])),
    N.para(N.rich([("self.right = []", {"code": True}), (" — standard min-heap; right[0] = min element in right half", {})])),
    N.para(N.rich([("heappush(self.left, -num)", {"code": True}), (" — push negated value; heap sorts by the stored value so the most-negative (= true maximum) floats to top", {})])),
    N.para(N.rich([("heappush(self.right, -heappop(self.left))", {"code": True}), (" — pop left's top (negate to get true value), push to right; restores order invariant unconditionally", {})])),
    N.para(N.rich([("if len(self.right) > len(self.left):", {"code": True}), (" — balance check: right must not exceed left in size", {})])),
    N.para(N.rich([("heappush(self.left, -heappop(self.right))", {"code": True}), (" — move right's minimum back to left (negate when pushing to simulate max-heap)", {})])),
    N.para(N.rich([("return float(-self.left[0])", {"code": True}), (" — odd total: left's top is the true median (negate the stored negative to get real value)", {})])),
    N.para(N.rich([("return (-self.left[0] + self.right[0]) / 2.0", {"code": True}), (" — even total: average of left's max and right's min; must divide by 2.0 to get float", {})])),
    N.callout(
        "Common Mistake: Forgetting negation. self.left stores negatives — every read needs -self.left[0] and every push needs -val. "
        "Missing a single negation corrupts the max-heap order silently.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: SortedList ──
blocks += [
    N.h2("Solution 2 — Python SortedList (Cleaner, Library-Dependent)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "If we maintain a sorted container that supports O(log n) insertion, "
            "then findMedian is just an O(1) index lookup at position n//2 or (n//2-1, n//2)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Python's built-in list requires O(n) to insert in sorted position (bisect.insort). "
            "That's O(n) per add — same problem as the naive approach."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Python's sortedcontainers.SortedList maintains a sorted list using a skip-list-like "
            "structure in C, giving O(log n) insert and O(1) index access. It's a drop-in for "
            "this problem but requires the sortedcontainers library (not in standard library)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Simply use SortedList.add(num) for insertion. For findMedian, access by index: "
            "if odd length, return data[n//2]; if even, return (data[n//2 - 1] + data[n//2]) / 2."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from sortedcontainers import SortedList\n\n"
        "class MedianFinder:\n\n"
        "    def __init__(self):\n"
        "        self.data = SortedList()  # maintains sorted order automatically\n\n"
        "    def addNum(self, num: int) -> None:\n"
        "        self.data.add(num)         # O(log n) insertion\n\n"
        "    def findMedian(self) -> float:\n"
        "        n = len(self.data)\n"
        "        mid = n // 2\n"
        "        if n % 2 == 1:\n"
        "            return float(self.data[mid])   # odd: exact middle\n"
        "        return (self.data[mid - 1] + self.data[mid]) / 2.0  # even: avg two midpoints"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("SortedList()", {"code": True}), (" — automatically maintains ascending sorted order on insertion and deletion", {})])),
    N.para(N.rich([("self.data.add(num)", {"code": True}), (" — O(log n) insertion using internal block structure in C; much faster than Python-level bisect.insort", {})])),
    N.para(N.rich([("n % 2 == 1", {"code": True}), (" — check if total count is odd", {})])),
    N.para(N.rich([("self.data[mid]", {"code": True}), (" — O(1) index access to the sorted list; the middle element is the median for odd count", {})])),
    N.para(N.rich([("(self.data[mid-1] + self.data[mid]) / 2.0", {"code": True}), (" — for even count: average of the two elements straddling the middle", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "addNum", "findMedian", "Space"],
        ["Two Heaps (Interview Pick)", "O(log n)", "O(1)", "O(n)"],
        ["SortedList (Python)", "O(log n)", "O(1)", "O(n)"],
        ["Naive: sort on query", "O(1)", "O(n log n)", "O(n)"],
        ["Naive: sorted insert", "O(n)", "O(1)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Two Heaps (Max Heap Left + Min Heap Right)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Stream of numbers + median query. Need max of lower half AND min of upper half simultaneously. "
             "'Running median', 'streaming median', or 'efficient median with dynamic insertions' in the problem statement. "
             "Any problem asking for the boundary between sorted lower/upper halves of a set.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Two Heaps technique:"),
    N.bullet(N.rich([("Sliding Window Median", {"bold": True}), (" (Hard) — Median in a fixed-size sliding window; extends two heaps with lazy deletion (#480)", {})])),
    N.bullet(N.rich([("IPO", {"bold": True}), (" (Hard) — Greedy capital selection using max-heap of profits unlocked by min-heap of capital costs (#502)", {})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), (" (Easy) — Single min-heap of size k; top is always the kth largest element (#703)", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Min-heap of meeting end times to count minimum rooms needed (#253)", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Min-heap over list node pointers efficiently merges k sorted streams (#23)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max-heap of task frequencies drives greedy cooldown scheduling (#621)", {})])),
    N.para("These problems all require fast access to boundary elements of dynamic sorted partitions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap section · Sub-Pattern: Two Heaps", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
