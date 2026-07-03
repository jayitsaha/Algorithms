"""
gen_sliding_window_median.py — Notion page builder for Sliding Window Median (#480)
Updates the existing page in-place via notion_lib.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8121-9d36-ee2f0f43920d"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=480,
    pattern="Heaps",
    subpatterns=["Two Heaps", "Lazy Deletion"],
    tc="O(n log k)",
    sc="O(k)",
    key_insight="Two heaps split the window into lower/upper halves; lazy deletion marks outgoing elements invalid rather than removing them from the heap directly.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ──────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an integer array ",
        ("nums", {"code": True}),
        " and an integer ",
        ("k", {"code": True}),
        ", there is a sliding window of size ",
        ("k", {"code": True}),
        " which is moving from the very left of the array to the very right. "
        "Return the median array for each window in the original array. "
        "The median of ",
        ("k", {"code": True}),
        " sorted values: the middle element if k is odd, or the average of the two "
        "middle elements if k is even. Answers within 10^-5 of the actual value are accepted."
    ])),
    N.divider()
]

# ── Solution 1: Two Heaps + Lazy Deletion ──────────────────────────
sol1_code = '''\
import heapq
from collections import defaultdict

def medianSlidingWindow(nums: list[int], k: int) -> list[float]:
    lo, hi = [], []          # lo: max-heap (stored negated); hi: min-heap
    invalid = defaultdict(int)  # lazy deletion counter
    lo_size = hi_size = 0   # effective (non-invalid) sizes

    def add_to_heap(x):
        nonlocal lo_size, hi_size
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x); lo_size += 1
        else:
            heapq.heappush(hi, x); hi_size += 1
        rebalance()

    def rebalance():
        nonlocal lo_size, hi_size
        if lo_size > hi_size + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
            lo_size -= 1; hi_size += 1
        elif hi_size > lo_size:
            heapq.heappush(lo, -heapq.heappop(hi))
            hi_size -= 1; lo_size += 1

    def clean(heap, is_lo):
        sign = -1 if is_lo else 1
        while heap and invalid[sign * heap[0]] > 0:
            invalid[sign * heap[0]] -= 1
            heapq.heappop(heap)

    def get_median():
        clean(lo, True); clean(hi, False)
        if lo_size == hi_size:
            return (-lo[0] + hi[0]) / 2.0
        return float(-lo[0])

    for x in nums[:k]:
        add_to_heap(x)
    result = [get_median()]

    for i in range(k, len(nums)):
        out = nums[i - k]
        invalid[out] += 1
        clean(lo, True); clean(hi, False)
        if lo and out <= -lo[0]:
            lo_size -= 1
        else:
            hi_size -= 1
        add_to_heap(nums[i])
        result.append(get_median())

    return result
'''

blocks += [
    N.h2("Solution 1 — Two Heaps + Lazy Deletion (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the median of a window that slides across an array. Median = middle element of sorted window. We need sorted order dynamically — inserting and removing elements as the window moves."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: sort each window in O(k log k), then O(nk log k) total. For n=10^5 and k=5*10^4, this is ~10^10 operations — TLE. We need O(log k) per step."),
        N.h4("The Key Observation"),
        N.para("The median sits at the boundary between the lower half and the upper half of sorted values. If we maintain a max-heap 'lo' for the lower half and a min-heap 'hi' for the upper half — always balanced — the median is always at the tops. This is the 'Find Median from Data Stream' trick (LeetCode #295)."),
        N.h4("Building the Solution"),
        N.para("The new challenge: elements must be REMOVED as the window slides. Heaps don't support arbitrary removal in O(log k). Solution: lazy deletion. When element x leaves the window, mark invalid[x] += 1. When x surfaces to the top of a heap in a future operation, discard it then. Track effective sizes (lo_size, hi_size) excluding invalid elements — these drive balance decisions, not len(lo)."),
        N.callout(
            "Analogy: Imagine a two-pile card game. 'lo' holds the smaller cards face-up, 'hi' holds the larger cards face-up. When a card 'leaves', put a sticky note on it. When that card appears on top, throw it away. You never have to dig through the pile.",
            "🃏", "blue_background"
        )
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Lazy Deletion on Heaps"),
    N.para(N.rich([
        ("Lazy deletion", {"bold": True}),
        (" is a general technique for supporting 'logical removal' from data structures that don't natively support arbitrary deletion. A deletion marker (here: an invalid counter) is inserted instead of performing the actual removal. The marked item is physically deleted when it is next accessed at the top of the structure. ", {}),
        ("Core invariant: ", {"bold": True}),
        "The physical heap top is always either a valid element or an invalid one that will be cleaned before any read. The effective sizes lo_size and hi_size count only valid elements and are maintained manually. ",
        ("Why it works: ", {"bold": True}),
        "Each element is pushed once (O(log k)) and cleaned at most once (O(log k)) — amortized O(log k) per element. The heap ordering property is never corrupted by invalid elements because we only ever observe valid tops."
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = [], []", {"code": True}), " — lo is Python's min-heap storing negated values (simulates max-heap); hi is a regular min-heap for the upper half."])),
    N.para(N.rich([("invalid = defaultdict(int)", {"code": True}), " — Maps each value to how many copies are marked for lazy removal. A value v with invalid[v]=2 means 2 occurrences should be discarded when they surface."])),
    N.para(N.rich([("lo_size = hi_size = 0", {"code": True}), " — Effective (non-invalid) counts. Critical: never use len(lo) or len(hi) for balance decisions — those include invalid elements."])),
    N.para(N.rich([("add_to_heap(x): if not lo or x <= -lo[0]", {"code": True}), " — Route x to lo if x is at most the current lo maximum (-lo[0]). Otherwise x belongs in hi."])),
    N.para(N.rich([("rebalance()", {"code": True}), " — If lo has more than 1 extra element (lo_size > hi_size+1), move lo's max to hi. If hi is larger (hi_size > lo_size), move hi's min to lo. One move per push."])),
    N.para(N.rich([("clean(heap, is_lo)", {"code": True}), " — Pop heap tops while they appear in the invalid map. sign=-1 for lo (values stored as negatives). Stale entries are discarded here."])),
    N.para(N.rich([("get_median()", {"code": True}), " — Clean both tops first. If lo_size == hi_size (even window), average lo.top and hi.top. Otherwise lo has one more and lo.top is the exact median."])),
    N.para(N.rich([("invalid[out] += 1", {"code": True}), " — Logically remove the outgoing element. Then clean heap tops so the lo[0] comparison below is against a valid element."])),
    N.para(N.rich([("if lo and out <= -lo[0]: lo_size -= 1", {"code": True}), " — Determine which side loses a valid slot. If out is at most lo.top, it was in lo; else it was in hi."])),
    N.divider()
]

# ── Solution 2: SortedList ──────────────────────────────────────────
sol2_code = '''\
from sortedcontainers import SortedList

def medianSlidingWindow(nums: list[int], k: int) -> list[float]:
    sl = SortedList(nums[:k])       # O(k log k) initialization
    result = []

    def median() -> float:
        if k % 2:                   # odd k: exact middle
            return float(sl[k // 2])
        return (sl[k // 2 - 1] + sl[k // 2]) / 2.0  # even k

    result.append(median())
    for i in range(k, len(nums)):
        sl.add(nums[i])             # O(log k) balanced BST insert
        sl.remove(nums[i - k])      # O(log k) balanced BST remove
        result.append(median())
    return result
'''

blocks += [
    N.h2("Solution 2 — SortedList (Cleaner, Same Complexity)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a sorted container that supports O(log k) insert and O(log k) delete-by-value, plus O(1) index access to find the median."),
        N.h4("The Key Observation"),
        N.para("Python's sortedcontainers.SortedList is backed by a skip-list / sorted array structure that supports all three operations. With it, the problem becomes trivially: insert new, remove old, read middle index."),
        N.h4("When to Use This"),
        N.para("When the interview environment allows sortedcontainers (common in online assessments), this is the cleanest solution. It avoids all the lazy deletion complexity while maintaining the same O(n log k) time bound."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("sl = SortedList(nums[:k])", {"code": True}), " — Initialize the sorted list with the first window. O(k log k)."])),
    N.para(N.rich([("sl[k // 2]", {"code": True}), " — For odd k, the middle index is k//2. SortedList supports O(1) index access."])),
    N.para(N.rich([("sl.add(nums[i])", {"code": True}), " — Insert the incoming element in sorted order. O(log k)."])),
    N.para(N.rich([("sl.remove(nums[i - k])", {"code": True}), " — Remove the outgoing element by value (removes one occurrence). O(log k)."])),
    N.divider()
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (sort each window)", "O(n·k log k)", "O(k)"],
        ["SortedList", "O(n log k)", "O(k)"],
        ["Two Heaps + Lazy Deletion (optimal)", "O(n log k) amortized", "O(k)"],
    ]),
    N.divider()
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Heaps"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Heaps, Lazy Deletion"])),
    N.callout(
        "When to recognize this pattern: You need the MEDIAN (or any order statistic) of a sliding window. "
        "Elements must be both inserted AND removed. A single heap doesn't suffice — you need two heaps "
        "to bracket the median from both sides. The deletion problem forces lazy deletion (or a sorted structure). "
        "Signals: 'sliding window', 'median', 'order statistic', 'dynamic sorted order'.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using Two-Heap or Lazy-Deletion-on-Heap patterns:"),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard, #295) — Prerequisite: same two-heap structure, no sliding window removal. Master this first.", {})])),
    N.bullet(N.rich([("IPO", {"bold": True}), (" (Hard, #502) — Greedy with two heaps: max-heap for profits of available projects, min-heap sorted by capital.", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard, #239) — Monotonic deque for window max; simpler than median since max-only requires one structure.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium, #621) — Max-heap to always schedule the highest-frequency remaining task.", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium, #253) — Min-heap of meeting end times; count max concurrent meetings.", {})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), (" (Easy, #703) — Min-heap of size k: top is always the kth largest seen.", {})])),
    N.bullet(N.rich([("Find K Closest Elements", {"bold": True}), (" (Medium, #658) — Binary search to find window start, then sliding window.", {})])),
    N.para("These problems share the core need for dynamic sorted-order maintenance with efficient median/boundary access."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap Patterns section, Two Heaps sub-pattern.", "📚", "gray_background"),
    N.divider()
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sliding_window_median")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys to walk through the two-heap state changes step by step.",
         {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
