"""
Notion page rebuild for: Minimum Cost to Connect Sticks (LeetCode #1167)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-810b-87c8-fd2bc1e75ec7"
SLUG = "minimum_cost_to_connect_sticks"

# ─── 1) Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1167,
    pattern="Heaps",
    subpatterns=["Min Heap Greedy"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Always merge the two smallest sticks first using a min-heap; smaller sticks in fewer merges = lower total cost.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe existing body ────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ─── 3) Build body blocks ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("sticks", {"code": True}),
        (" where ", {}),
        ("sticks[i]", {"code": True}),
        (" is the length of the i-th stick, combine all sticks into one. The cost of combining two sticks of lengths ", {}),
        ("a", {"code": True}),
        (" and ", {}),
        ("b", {"code": True}),
        (" is ", {}),
        ("a + b", {"code": True}),
        (". Return the minimum total cost.", {})
    ])),
    N.para("Example: sticks = [2,4,3] → merge (2,3)=5 cost 5, then (4,5)=9 cost 9 → total = 14."),
    N.divider(),
]

# ─── Solution 1: Min Heap Greedy (Optimal / Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — Min Heap Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each merge creates a composite stick whose length equals the merge cost — and that composite participates in all future merges. So the cost of a stick is effectively multiplied by how many rounds it is 'alive'. We want small sticks to participate in many rounds, large sticks in few."),
        N.h4("What Doesn't Work"),
        N.para("Merging sticks in arbitrary order or largest-first forces large values to be re-counted repeatedly. E.g., [1,8,3,5]: merge (8,5)=13 first → 13+3=16 → 16+1=17, total 46. Merging smallest-first gives total 30."),
        N.h4("The Key Observation"),
        N.para("If we always merge the two smallest sticks, we ensure that only small values grow early. The larger values stay small in count relative to the composite value. This is proven optimal by the exchange argument: any swap away from the greedy choice can be swapped back without increasing cost."),
        N.h4("Building the Solution"),
        N.para("We need the two smallest elements at every step. A sorted array requires re-sorting after each merge. A min-heap gives extract-min in O(log n) and insert in O(log n) — n-1 times total gives O(n log n)."),
        N.callout("Analogy: This is Huffman Coding! Huffman builds an optimal binary prefix tree by merging the two least-frequent symbols using a min-heap. Same greedy structure, same proof, different domain.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""import heapq

def connectSticks(sticks):
    heapq.heapify(sticks)      # O(n): convert to min-heap in-place
    total = 0                  # accumulate total merge cost
    while len(sticks) > 1:    # n-1 iterations until one stick remains
        a = heapq.heappop(sticks)   # O(log n): pop smallest
        b = heapq.heappop(sticks)   # O(log n): pop second smallest
        merged = a + b              # cost of this merge = new stick length
        total += merged             # add merge cost to running total
        heapq.heappush(sticks, merged)  # O(log n): push composite back
    return total               # minimum total cost"""),
    N.h3("Line by Line"),
    N.para(N.rich([("heapq.heapify(sticks)", {"code": True}), (" — Converts the list to a min-heap in O(n). The smallest element is always at index 0. This mutates the input in-place.", {})])),
    N.para(N.rich([("total = 0", {"code": True}), (" — Running cost accumulator. We add each merge cost to this.", {})])),
    N.para(N.rich([("while len(sticks) > 1:", {"code": True}), (" — We need exactly n-1 merges to reduce n sticks to 1. Loop exits when only the final stick remains.", {})])),
    N.para(N.rich([("a = heapq.heappop(sticks)", {"code": True}), (" — Remove and return the current minimum. The heap restructures to maintain the heap property in O(log n).", {})])),
    N.para(N.rich([("b = heapq.heappop(sticks)", {"code": True}), (" — Remove the new minimum (second smallest overall). Both pops cost O(log n).", {})])),
    N.para(N.rich([("merged = a + b", {"code": True}), (" — The merge cost equals the combined length. This is also the length of the new composite stick.", {})])),
    N.para(N.rich([("total += merged", {"code": True}), (" — Accumulate. Each of the n-1 merges contributes exactly merged to the total.", {})])),
    N.para(N.rich([("heapq.heappush(sticks, merged)", {"code": True}), (" — Insert the composite back so it can be merged again in future iterations. O(log n).", {})])),
    N.para(N.rich([("return total", {"code": True}), (" — After n-1 merges, total holds the minimum possible cost.", {})])),
    N.callout("Edge case: single stick → len == 1 on first check → loop never runs → return 0. Correct: no merge needed.", "⚠️", "yellow_background"),
    N.divider(),
]

# ─── Solution 2: Brute Force — Sort and Re-sort ───────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Sort and Re-sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same greedy insight — always merge the two smallest. The question is just: how do we find the two smallest efficiently?"),
        N.h4("What Doesn't Work (This Is It)"),
        N.para("Sort the array. Merge the first two. Re-sort. Repeat. This works correctly but requires O(n log n) per merge iteration, giving O(n² log n) total. For n = 10^4, that's 10^8 log operations — too slow."),
        N.h4("The Key Observation"),
        N.para("This brute-force teaches us WHY the heap is needed: maintaining sorted order after each insertion is the bottleneck. The heap solves exactly this with O(log n) insertion."),
        N.h4("Building the Solution"),
        N.para("Sort → merge first two → re-sort → repeat. Simple to code but not interview-quality for large n."),
    ]),
    N.h3("Code"),
    N.code("""def connectSticks_brute(sticks):
    sticks = sorted(sticks)   # O(n log n) initial sort
    total = 0
    while len(sticks) > 1:
        a = sticks.pop(0)     # O(n) shift — expensive!
        b = sticks.pop(0)     # O(n) shift
        merged = a + b
        total += merged
        # Re-insert in sorted position via binary search
        import bisect
        bisect.insort(sticks, merged)  # O(n) due to shift
    return total"""),
    N.h3("Line by Line"),
    N.para(N.rich([("sticks.pop(0)", {"code": True}), (" — Removes the first element (smallest), but shifts the entire array left — O(n). This is the performance killer.", {})])),
    N.para(N.rich([("bisect.insort(sticks, merged)", {"code": True}), (" — Binary search finds the insertion point in O(log n), but inserting into a list requires O(n) shifting. Still O(n) per operation.", {})])),
    N.callout("Use a deque for O(1) pop-left, but you'd still need binary search + O(n) shift for insert. The heap is strictly better.", "⚠️", "yellow_background"),
    N.divider(),
]

# ─── Complexity Table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (sort + re-sort)", "O(n² log n)", "O(1) extra", "Too slow for large n"],
        ["Min Heap Greedy (optimal)", "O(n log n)", "O(n)", "heapify O(n) + n-1 × O(log n) merges"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps (Priority Queue)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Heap Greedy — repeatedly extract two minimums, merge, push result back. Also known as Greedy + Heap.", {})])),
    N.callout("When to recognize this pattern: 'Repeatedly pick/combine the two smallest (or largest) elements.' 'Merge result re-enters the pool.' 'Minimize total cost of sequential operations.' — All signal a min/max-heap greedy.", "🔎", "green_background"),
    N.para("Connection to algorithms: this is structurally identical to Huffman Coding (optimal prefix codes) and related to Prim's MST algorithm (priority-queue based greedy)."),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Min Heap Greedy):"),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium, #215) — Min-heap of size K; after K pops, top = Kth largest.", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium, #253) — Min-heap to always free the earliest-ending meeting room.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium, #621) — Max-heap greedy to place highest-frequency tasks first.", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard, #23) — Min-heap to always pop the globally smallest node.", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard, #295) — Two heaps (max + min) to maintain median dynamically.", {})])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}), (" (Medium, #767) — Max-heap greedy to interleave highest-frequency characters.", {})])),
    N.bullet(N.rich([("Huffman Coding", {"bold": True}), (" (Classic) — Optimal prefix codes; structurally identical to this problem.", {})])),
    N.para("These problems share the core technique: use a heap to always operate on the globally smallest (or largest) value, maintaining greedy optimality in O(log n) per step."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section. Sub-Pattern: Min Heap Greedy (Greedy + Heap).", "📚", "gray_background"),
    N.divider(),
]

# ─── Interactive Visual Explainer embed ──────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
