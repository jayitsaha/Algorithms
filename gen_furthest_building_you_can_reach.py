"""
gen_furthest_building_you_can_reach.py
Notion IN-PLACE rebuild for LeetCode #1642 Furthest Building You Can Reach
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8160-9e6e-d4cac5d3ef7b"
SLUG = "furthest_building_you_can_reach"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1642,
    pattern="Heaps",
    subpatterns=["Greedy + Heap"],
    tc="O(n log k)",
    sc="O(k)",
    key_insight="Use a min-heap of size k to keep ladders on the k largest climbs; swap the minimum to bricks when over-committed.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} blocks.")

# ── 3. Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("heights", {"code": True}),
        (" representing building heights, and two integers ", {}),
        ("bricks", {"code": True}),
        (" and ", {}),
        ("ladders", {"code": True}),
        (". Moving left to right through the buildings, to step from building ", {}),
        ("i", {"code": True}),
        (" to building ", {}),
        ("i+1", {"code": True}),
        (": if heights[i+1] <= heights[i], move for free; otherwise use either ", {}),
        ("diff = heights[i+1] - heights[i]", {"code": True}),
        (" bricks or one ladder. Return the furthest building index you can reach.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 (Optimal) ──
SOL1_CODE = """\
import heapq

def furthestBuilding(heights: list[int], bricks: int, ladders: int) -> int:
    heap = []  # min-heap: gaps where ladders are assigned
    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff <= 0:
            continue              # downhill/flat: free
        heapq.heappush(heap, diff)
        if len(heap) > ladders:   # over-committed on ladders
            bricks -= heapq.heappop(heap)  # swap smallest to bricks
        if bricks < 0:
            return i              # can't afford it — stuck here
    return len(heights) - 1       # made it to the end!
"""

blocks += [
    N.h2("Solution 1 — Greedy + Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to go as far right as possible. Every upward gap must be covered by either bricks (exact cost = gap size) or a ladder (fixed cost = 1 ladder regardless of size). We want to maximise distance, so we need to minimise wasted resources."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach — always use bricks first, then ladders — fails because it wastes ladders on small climbs we could have paid cheaply with bricks. Any fixed priority scheme fails because we don't know the future gaps."),
        N.h4("The Key Observation"),
        N.para("A ladder saves more bricks on a large gap than a small one. Therefore, ladders should cover the k LARGEST gaps, and bricks should cover the rest. This is an invariant we can maintain dynamically using a min-heap of size k."),
        N.h4("Building the Solution"),
        N.para("Walk left to right. For each upward gap: tentatively assign a ladder (push to heap). If the heap exceeds the ladder count, we're over-committed — swap out the smallest ladder claim by popping the heap minimum and paying bricks for it. If bricks go negative, we can't make this jump; return the current index."),
        N.callout("Analogy: Imagine k VIP tickets for a concert. You give out tickets at the door to every group, but if you run out, you take the ticket back from the smallest group and charge them cash instead. VIP tickets always end up with the biggest groups.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), " — Min-heap to track gap sizes where ladders are currently assigned. Smallest gap is at the root."])),
    N.para(N.rich([("diff = heights[i+1] - heights[i]", {"code": True}), " — Height change. Negative or zero means downhill/flat — free to cross."])),
    N.para(N.rich([("if diff <= 0: continue", {"code": True}), " — Skip the heap logic entirely for free transitions."])),
    N.para(N.rich([("heapq.heappush(heap, diff)", {"code": True}), " — Tentatively assign a ladder to this gap. The heap now holds all gap sizes that currently have ladders."])),
    N.para(N.rich([("if len(heap) > ladders:", {"code": True}), " — We've over-committed: more active ladder assignments than actual ladders."])),
    N.para(N.rich([("bricks -= heapq.heappop(heap)", {"code": True}), " — Swap: remove the smallest ladder claim (heap min) and pay its gap size in bricks instead. The ladder stays on larger gaps."])),
    N.para(N.rich([("if bricks < 0: return i", {"code": True}), " — After the swap, if bricks are negative, we can't afford even the cheapest conversion. Return i (currently standing here; couldn't reach i+1)."])),
    N.para(N.rich([("return len(heights) - 1", {"code": True}), " — Survived all transitions — reached the final building."])),
    N.divider(),
]

# ── Solution 2 (Brute Force) ──
SOL2_CODE = """\
from itertools import combinations

def furthestBuilding_brute(heights, bricks, ladders):
    # Find all upward climbs
    climbs = []  # (index, diff)
    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff > 0:
            climbs.append((i, diff))

    # Try all ways to assign ladders to exactly min(ladders, len(climbs)) climbs
    best = 0
    n_climbs = len(climbs)
    for k in range(min(ladders, n_climbs) + 1):
        for ladder_set in combinations(range(n_climbs), k):
            # For climbs not in ladder_set, pay bricks
            b = bricks
            furthest = len(heights) - 1
            for j, (idx, diff) in enumerate(climbs):
                if j not in ladder_set:
                    b -= diff
                    if b < 0:
                        furthest = idx
                        break
            best = max(best, furthest)
    return best
"""

blocks += [
    N.h2("Solution 2 — Brute Force (All Assignments)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each subset of climbs, decide which ones get ladders and which get bricks. Try all possible assignments and keep the one that goes furthest."),
        N.h4("What Doesn't Work"),
        N.para("This is O(2^n) — exponential in the number of buildings. Fine for tiny examples; completely infeasible for n up to 100,000."),
        N.h4("The Key Observation"),
        N.para("The brute-force clarifies WHY the optimal assignment puts ladders on largest gaps — any permutation that doesn't is dominated by one that does. This motivates the greedy approach."),
        N.h4("Building the Solution"),
        N.para("Enumerate all combinations of k climbs to receive ladders. For each assignment, simulate the walk and track how far we go. Return the best across all assignments."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("climbs = [(i, diff) for i,diff if diff > 0]", {"code": True}), " — Collect all upward gaps and their indices."])),
    N.para(N.rich([("for ladder_set in combinations(...)", {"code": True}), " — Try every possible subset of climbs to assign ladders."])),
    N.para(N.rich([("b -= diff", {"code": True}), " — For non-ladder climbs, deduct the gap from bricks."])),
    N.para(N.rich([("if b < 0: furthest = idx; break", {"code": True}), " — Record where we got stuck."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all assignments)", "O(2^n)", "O(n)"],
        ["Greedy + Min-Heap (optimal) ✓", "O(n log k)", "O(k)"],
    ]),
    N.para("Where n = number of buildings and k = number of ladders. The heap never exceeds k+1 elements; each push/pop is O(log k)."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Heaps"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Greedy + Heap (Min Heap for Top-K / Min Heap for Ladders)"])),
    N.callout(
        "When to recognize this pattern: "
        "'K items of scarce resource A; unlimited of cheaper B; A saves more on larger instances.' "
        "→ Min-heap of size k. Push every element; pop when oversized. "
        "Also triggered by 'furthest you can reach' with a running cost that can fail.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Greedy + Heap technique:"),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), " (Easy) — Min-heap of size k; same invariant: heap root is the kth largest (#703)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two-heap trick: max-heap for lower half, min-heap for upper half (#295)"])),
    N.bullet(N.rich([("Minimum Cost to Connect Sticks", {"bold": True}), " (Medium) — Min-heap greedy: always merge the two smallest sticks to minimise cost (#1167)"])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — Max-heap greedy: always schedule the most frequent remaining task (#621)"])),
    N.bullet(N.rich([("K Closest Points to Origin", {"bold": True}), " (Medium) — Max-heap of size k to maintain k closest points (#973)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Min-heap of end-times for greedy room assignment (#253)"])),
    N.para("These problems all share the core pattern: maintain a bounded heap that holds the 'best k' items, swapping out the weakest when over capacity."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Heaps → Sub-Pattern: Greedy + Heap", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
