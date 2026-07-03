"""
gen_ipo.py — Notion page builder for IPO (LeetCode #502).
Run from the Algorithms directory:  python3 gen_ipo.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-a072-d7c41236376e"

# ── 1. Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=502,
    pattern="Heaps",
    subpatterns=["Greedy + Heap", "Min Heap Capital + Max Heap Profit"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort projects by capital in a min-heap; greedily pick max-profit affordable project via max-heap each round.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are a startup founder with initial capital ", {}),
        ("w", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (" projects. Project ", {}),
        ("i", {"code": True}),
        (" requires minimum capital ", {}),
        ("capital[i]", {"code": True}),
        (" to start and yields profit ", {}),
        ("profits[i]", {"code": True}),
        (" on completion. Profits accumulate — earnings from one project add to your wallet before the next. Complete at most ", {}),
        ("k", {"code": True}),
        (" projects (in any order) to maximise your final capital. Return the maximised capital.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 (optimal) ──────────────────────────────────────────────────────
SOL1_CODE = """\
import heapq

def findMaximizedCapital(k, w, profits, capital):
    min_heap = list(zip(capital, profits))
    heapq.heapify(min_heap)          # O(n) build; cheapest capital at top
    max_heap = []                    # unlocked projects (negated profits)

    for _ in range(k):               # at most k rounds
        while min_heap and min_heap[0][0] <= w:
            c, p = heapq.heappop(min_heap)
            heapq.heappush(max_heap, -p)   # negate: simulate max-heap
        if not max_heap:
            break                    # nothing affordable — wallet can't grow
        w += -heapq.heappop(max_heap)      # pick best profit

    return w
"""

blocks += [
    N.h2("Solution 1 — Two-Heap Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to pick at most k projects that maximise total profit, where each project is only available if our current wallet meets its minimum capital. Projects unlock dynamically as we earn more."),
        N.h4("What Doesn't Work"),
        N.para("Trying all C(n,k) subsets is exponential. Sorting by profit alone ignores capital requirements — we might greedily pick a high-profit project we can't afford. Sorting by capital alone misses the maximum-profit objective."),
        N.h4("The Key Observation"),
        N.para("At any wallet size w, the set of affordable projects is fixed (those with capital[i] ≤ w). From this set, we should always pick the maximum-profit project. After earning that profit, the feasible set can only grow (wallet increases). This greedy choice is globally optimal because profits ≥ 0 and project order doesn't change total gain."),
        N.h4("Building the Solution"),
        N.para("Two problems: (1) efficiently find projects that just became affordable as w grows — min-heap by capital. (2) efficiently find the best affordable project — max-heap by profit. Each round: drain the min-heap into the max-heap for everything we can afford, then pop the max. O(n log n) total."),
        N.callout("Analogy: It's like a job marketplace where your salary unlocks higher-paying jobs. Always apply for the highest-paying job you currently qualify for. Your salary keeps growing, opening more doors. Never pass up the best available opportunity.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("min_heap = list(zip(capital, profits))", {"code": True}), (" — Pair each project as (cap, profit). Tuples compare by first element (capital), making the min-heap sort by capital automatically.", {})])),
    N.para(N.rich([("heapq.heapify(min_heap)", {"code": True}), (" — O(n) in-place heap construction. Always faster than n individual heappush calls (O(n log n)).", {})])),
    N.para(N.rich([("max_heap = []", {"code": True}), (" — The 'available' pool starts empty. Projects move here from min_heap when unlocked.", {})])),
    N.para(N.rich([("for _ in range(k):", {"code": True}), (" — At most k rounds. We break early if no project is affordable.", {})])),
    N.para(N.rich([("while min_heap and min_heap[0][0] <= w:", {"code": True}), (" — While the cheapest locked project is within budget, unlock it. min_heap[0] is the heap top (O(1) peek).", {})])),
    N.para(N.rich([("heapq.heappush(max_heap, -p)", {"code": True}), (" — Negation trick: push -profit so Python's min-heap behaves as a max-heap. The largest profit sits at -max_heap[0].", {})])),
    N.para(N.rich([("if not max_heap: break", {"code": True}), (" — If max_heap is empty after the unlock phase, no project is currently affordable. Since we can't earn anything, the wallet can never grow — break immediately.", {})])),
    N.para(N.rich([("w += -heapq.heappop(max_heap)", {"code": True}), (" — Pop the best profit (negate the negated value to recover real profit) and add to wallet.", {})])),
    N.divider(),
]

# ── Solution 2 (brute force for contrast) ─────────────────────────────────────
SOL2_CODE = """\
def findMaximizedCapital_sort(k, w, profits, capital):
    # Pair and sort all projects by required capital
    projects = sorted(zip(capital, profits))
    import heapq
    max_heap = []
    i = 0
    for _ in range(k):
        # Add all newly affordable projects
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(max_heap, -projects[i][1])
            i += 1
        if not max_heap:
            break
        w += -heapq.heappop(max_heap)
    return w
"""

blocks += [
    N.h2("Solution 2 — Sort + Max-Heap (Equivalent, Different Build)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of building a heap from all projects and popping by capital, we pre-sort by capital and use a pointer to track which projects are now affordable."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly but requires O(n log n) upfront sorting, same asymptotic cost as Solution 1. The advantage is conceptual clarity — the sorted array makes the 'unlock' step very explicit."),
        N.h4("The Key Observation"),
        N.para("If projects are sorted by capital, we just advance a pointer i while projects[i][0] <= w. This is equivalent to the min-heap drain but more readable for interviews."),
        N.h4("Building the Solution"),
        N.para("Sort by capital once O(n log n). Then each round: advance pointer, add affordable profits to max-heap, pop max. Total time O(n log n) same as Solution 1."),
        N.callout("Note: This approach and Solution 1 are essentially the same algorithm. Solution 1 uses heapify() which is slightly cleaner. Solution 2 uses sorting, which may be more intuitive to derive.", "💡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("projects = sorted(zip(capital, profits))", {"code": True}), (" — Sort all projects by required capital ascending. O(n log n).", {})])),
    N.para(N.rich([("while i < len(projects) and projects[i][0] <= w:", {"code": True}), (" — Advance pointer to include all newly affordable projects. i never resets — each project is processed at most once amortized.", {})])),
    N.para(N.rich([("heapq.heappush(max_heap, -projects[i][1])", {"code": True}), (" — Same negation trick for max-heap simulation.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                   "Time",        "Space"],
        ["Two-Heap Greedy (optimal)",  "O(n log n)",  "O(n)"],
        ["Sort + Max-Heap",            "O(n log n)",  "O(n)"],
        ["Brute Force (all subsets)",  "O(2^n)",      "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Greedy + Heap", {}), (" / ", {}), ("Min Heap Capital + Max Heap Profit", {})])),
    N.callout(
        N.rich([
            ("When to recognise this pattern: ", {"bold": True}),
            ('"Maximise after at most k operations" + items unlock as a resource grows + local greedy is globally optimal (non-negative gains). Need O(log n) best-available query each step.', {}),
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: The 'Min Heap Capital + Max Heap Profit' sub-pattern label is a problem-specific application of the broader Greedy + Heap pattern. Not listed verbatim in the guide — classified by analysis.", {"italic": True, "color": "gray"})])),
    N.divider(),
]

# ── Related problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (Greedy + Heap):"),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Min-heap of end times; greedily reuse earliest-ending room.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max-heap by frequency; always schedule most-frequent task first (#621).", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps maintain lower/upper halves for O(1) median (#295).", {})])),
    N.bullet(N.rich([("Minimum Cost to Hire K Workers", {"bold": True}), (" (Hard) — Sort by wage/quality ratio; max-heap drops most expensive worker (#857).", {})])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}), (" (Medium) — Max-heap by character frequency for greedy placement avoiding repeats (#767).", {})])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), (" (Easy) — Min-heap of size k maintains the k largest seen so far (#703).", {})])),
    N.para("These problems share the same core technique: a heap dynamically tracks the optimal candidate from a changing feasible set."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section. Sub-Pattern: Greedy + Heap. Source: Analysis.", "📚", "gray_background"),
]

# ── Embed section ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("ipo")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
