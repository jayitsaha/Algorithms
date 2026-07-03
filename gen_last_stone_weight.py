"""gen_last_stone_weight.py — Notion page rebuild for Last Stone Weight (#1046)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81aa-8ff4-f8d84c1af18a"

# ── 1. Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1046,
    pattern="Heaps",
    subpatterns=["Max Heap Simulation"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Use a max-heap (negate values in Python's min-heap) to always smash the two heaviest stones; push remainder back until 0 or 1 stone remains.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old content ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ─────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of integers ", {}),
        ("stones", {"code": True}),
        (" where ", {}),
        ("stones[i]", {"code": True}),
        (" is the weight of the i-th stone. We play a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights ", {}),
        ("x", {"code": True}),
        (" and ", {}),
        ("y", {"code": True}),
        (" with ", {}),
        ("x <= y", {"code": True}),
        (". The result of this smash is: if ", {}),
        ("x == y", {"code": True}),
        (", both stones are destroyed; if ", {}),
        ("x != y", {"code": True}),
        (", the stone of weight ", {}),
        ("x", {"code": True}),
        (" is destroyed and the stone of weight ", {}),
        ("y", {"code": True}),
        (" has new weight ", {}),
        ("y - x", {"code": True}),
        (". At the end of the game, there is at most one stone left. Return the weight of the last remaining stone. If there are no stones left, return 0.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Max Heap ──────────────────────────────────────────────────────
sol1_code = """import heapq

def lastStoneWeight(stones: list) -> int:
    heap = [-s for s in stones]    # negate all: min-heap acts as max-heap
    heapq.heapify(heap)            # O(n) heapify
    while len(heap) > 1:
        y = -heapq.heappop(heap)   # largest stone (most-negative popped)
        x = -heapq.heappop(heap)   # second largest; y >= x guaranteed
        if y > x:
            heapq.heappush(heap, -(y - x))  # remainder survives
        # if y == x: both destroyed, push nothing
    return -heap[0] if heap else 0  # un-negate survivor, or 0 if empty"""

blocks += [
    N.h2("Solution 1 — Max Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each round you need the two globally largest elements from a dynamic collection. After smashing, you might add a new element (the remainder) back. This is a sequence of: find-max, find-max, conditional-insert."),
        N.h4("What Doesn't Work"),
        N.para("Sorting the array each round is O(n log n) per smash, giving O(n² log n) total. Re-sorting just to find the top-2 is wasteful — we throw away all that ordering information after each round."),
        N.h4("The Key Observation"),
        N.para("We only ever need the maximum element — never a random element. A max-heap maintains the maximum at its root in O(1), and both extraction and insertion take O(log n). That is the exact operation profile we need."),
        N.h4("Building the Solution"),
        N.para("Python's heapq is a min-heap. Standard trick: negate all values. The smallest negative is the largest positive. Build with heapify O(n). Loop: pop twice for y and x. If y > x, push -(y-x). Exit when 0 or 1 stone remains. Return -heap[0] or 0."),
        N.callout("Analogy: Think of a demolition yard where a crane always picks the two heaviest steel balls and smashes them. The crane's magnet (heap) instantly finds the heaviest — it doesn't re-sort all the balls each time.", "🏗️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [-s for s in stones]", {"code": True}), (" — Negate every stone weight. Python's heapq is min-heap; negating maps max-heap operations to min-heap operations.", {})])),
    N.para(N.rich([("heapq.heapify(heap)", {"code": True}), (" — Build a valid heap in-place in O(n) using Floyd's sift-down algorithm. Faster than n individual heappush calls (O(n log n)).", {})])),
    N.para(N.rich([("while len(heap) > 1:", {"code": True}), (" — Keep smashing as long as 2 or more stones exist.", {})])),
    N.para(N.rich([("y = -heapq.heappop(heap)", {"code": True}), (" — Pop the smallest negative → un-negate → the largest stone. This is the heavier stone y.", {})])),
    N.para(N.rich([("x = -heapq.heappop(heap)", {"code": True}), (" — Pop next → second largest. y ≥ x is guaranteed by heap property.", {})])),
    N.para(N.rich([("if y > x:", {"code": True}), (" — If stones differ, a remainder exists.", {})])),
    N.para(N.rich([("heapq.heappush(heap, -(y - x))", {"code": True}), (" — Push the negated remainder back. The heap rebalances in O(log n).", {})])),
    N.para(N.rich([("return -heap[0] if heap else 0", {"code": True}), (" — If one stone remains, un-negate the heap root. If heap is empty, all stones cancelled — return 0.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force Sort ─────────────────────────────────────────────
sol2_code = """def lastStoneWeight_brute(stones: list) -> int:
    stones = list(stones)       # copy — don't mutate input
    while len(stones) > 1:
        stones.sort()           # O(n log n) per round — expensive
        y = stones.pop()        # largest (last after sort)
        x = stones.pop()        # second largest
        if y > x:
            stones.append(y - x)  # push remainder (will re-sort next round)
    return stones[0] if stones else 0"""

blocks += [
    N.h2("Solution 2 — Brute Force Sorting"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we always keep the list sorted, the two largest are at the end. We can pop them in O(1), compute the result, and append the remainder. The cost is the re-sort each round."),
        N.h4("What Doesn't Work"),
        N.para("Re-sorting O(n log n) every round gives O(n² log n) total. For n=30 stones this is manageable, but it is clearly wasteful — we only changed one or two elements, yet we re-sort everything."),
        N.h4("The Key Observation"),
        N.para("Correct but suboptimal. Useful as the 'obvious' solution to state before proposing the heap optimization. Always mention this in interviews first, then upgrade."),
        N.h4("Building the Solution"),
        N.para("Sort, pop last two (largest), compute smash, append remainder if any. Repeat. Return last element or 0."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Sort", "O(n² log n)", "O(1) extra"],
        ["Max Heap (optimal)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps / Priority Queue", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Max Heap Simulation (Greedy + Heap)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Repeatedly extract the maximum or minimum element. (2) Elements are dynamically added and removed across rounds. (3) Problem says 'smash', 'merge', or 'combine the two heaviest/lightest'. (4) You need top-k elements with updates.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Max Heap / Priority Queue):"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Max-heap pop k times; or min-heap of size k for streaming top-K (#215)", {})])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), (" (Medium) — Min-heap on Euclidean distance; pop k times for k closest (#973)", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two-heap pattern: max-heap for lower half, min-heap for upper half (#295)", {})])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), (" (Hard) — Min-heap merges k lists by always extracting the globally smallest node (#23)", {})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — Frequency map then heap-extract top k (#347)", {})])),
    N.bullet(N.rich([("Last Stone Weight II", {"bold": True}), (" (Medium) — Harder variant: partition stones into two groups to minimize |diff|; uses 0/1 Knapsack DP (#1049)", {})])),
    N.para("These problems share the core technique: use a heap to maintain dynamic access to the maximum (or minimum) element in O(log n) per operation."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap / Priority Queue section. Sub-Pattern: Max Heap Simulation (Greedy + Heap). Source: Analysis.", "📚", "gray_background"),
]

# ── Visual Explainer ──────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("last_stone_weight")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
