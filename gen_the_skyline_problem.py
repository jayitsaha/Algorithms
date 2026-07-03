"""
gen_the_skyline_problem.py
Notion regeneration script for The Skyline Problem (LC #218)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8164-ab93-fc0c4c7a137e"
SLUG = "the_skyline_problem"

# ── 1) Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=218,
    pattern="Advanced Data Structures",
    subpatterns=["Events + Max Heap"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sweep line: emit start/end events sorted by x, maintain active heights in a max-heap with lazy deletion; emit a key point whenever the max height changes.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} old blocks.")

# ── 3) Build new body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A city's skyline is the outer contour of the silhouette formed by all its buildings as viewed from a distance. Given the locations and heights of all buildings as a list ", {}),
        ("buildings", {"code": True}),
        (" where each ", {}),
        ("buildings[i] = [left_i, right_i, height_i]", {"code": True}),
        (", return the skyline formed by these buildings collectively. The skyline should be represented as a list of ", {}),
        ('[xi, yi]', {"code": True}),
        (" key points where the height of the outermost skyline changes. The last key point always has a height of 0 (the ground).", {}),
    ])),
    N.para(N.rich([
        ("Example: buildings = [[2,9,10],[3,7,15],[5,12,12]] → output: [[2,10],[3,15],[7,12],[9,12],[12,0]]", {"italic": True}),
    ])),
    N.divider(),
]

# ── Solution 1: Sweep Line + Max Heap (Interview Pick) ──────────────────────
SOL1_CODE = '''\
import heapq
from collections import defaultdict

def getSkyline(buildings):
    # Build events: (x, -H) for start, (x, +H) for end
    # Negative H for starts: sorts before ends at same x, taller first
    events = []
    for L, R, H in buildings:
        events.append((L, -H))   # start
        events.append((R,  H))   # end
    events.sort()                # lex sort: by x then by h

    result = []
    max_heap = [0]               # min-heap w/ negated heights; 0 = ground sentinel
    active = defaultdict(int)
    active[0] = 1                # ground is always active

    for x, h in events:
        if h < 0:                # start event
            heapq.heappush(max_heap, h)
            active[-h] += 1
        else:                    # end event
            active[h] -= 1      # lazy deletion — do not remove from heap yet

        # Clean stale entries from heap top
        while active[-max_heap[0]] == 0:
            heapq.heappop(max_heap)

        cur_max = -max_heap[0]   # current tallest active building
        if not result or result[-1][1] != cur_max:
            result.append([x, cur_max])  # height changed → new key point

    return result
'''

blocks += [
    N.h2("Solution 1 — Sweep Line + Max Heap with Lazy Deletion (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find every x-position where the height of the tallest visible building changes. Think of a vertical sweep line moving left to right — at each building's left edge the tallest might rise, at each right edge it might fall. Between edges, nothing changes."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: for each unique x-position (2n of them), scan all n buildings and find the tallest one that covers x. This is O(n²). Correct but too slow for n = 10,000."),
        N.h4("The Key Observation"),
        N.para("The skyline can only change at building edges. So we only need to check at 2n event positions, not at every x on the continuous number line. If we could answer 'what is the current max height?' in O(log n) after each event, we'd have an O(n log n) solution overall."),
        N.h4("Building the Solution"),
        N.para("Model each building as two events: a start (left edge, height rises) and an end (right edge, height may fall). Sort events by x. Maintain a max-heap of currently-active building heights. On a start event, push the height. On an end event, mark it as removed (lazy deletion — we can't remove from the middle of a heap efficiently). Before reading the max, pop any stale heap tops. If the max changed, emit a key point."),
        N.callout(
            "Analogy: imagine a city zoning inspector walking from west to east with a clipboard. Each time she passes a building's left wall she writes it on the list; each time she passes a right wall she crosses it off. She always looks at the tallest item on her list — if it changed, she marks a 'height change' on her skyline drawing.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Sweep Line"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Sweep-line algorithms were formalized by Shamos & Hoey (1976) for computational geometry. They solve 2D problems by reducing them to a sequence of 1D queries as a vertical line sweeps one coordinate axis.", {}),
    ])),
    N.para(N.rich([
        ("Core pattern: ", {"bold": True}),
        ("Extract events at boundary x-coordinates → sort → maintain a status structure (heap, BST, sorted set) describing the current active cross-section → at each event, update structure and query max/min/count.", {}),
    ])),
    N.para(N.rich([
        ("Invariant: ", {"bold": True}),
        ("After processing all events at position x, the max-heap's valid top equals the height of the tallest building whose x-range contains x — exactly the skyline height.", {}),
    ])),
    N.para(N.rich([
        ("Lazy Deletion: ", {"bold": True}),
        ("Python's heapq has no O(log n) arbitrary removal. Solution: store a 'remaining count' map (", {}),
        ("active[h]", {"code": True}),
        ("). On end events, decrement the count. Before reading the heap top, pop while the top's count is 0. Each element is pushed and popped at most once → O(n log n) total.", {}),
    ])),
    N.code(
        "# Encoding trick for automatic tie-breaking:\n"
        "# Start: (L, -H)  →  negative H, sorts before positive at same x\n"
        "#                  →  more-negative (taller) sorts before less-negative at same x\n"
        "# End:   (R, +H)  →  positive H, sorts after starts at same x\n"
        "events.sort()  # one sort handles ALL tie-breaking cases"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("events = [(L,-H) for start, (R,+H) for end]", {"code": True}), (" — Build 2n events. Start events use negative height so they sort before end events at the same x. Taller starts (more-negative h) sort before shorter starts automatically.", {})])),
    N.para(N.rich([("events.sort()", {"code": True}), (" — Lexicographic sort on tuples. At same x: -H < +H so starts come first; among starts at same x, -15 < -10 so taller comes first. All tie-breaking handled by this one line.", {})])),
    N.para(N.rich([("max_heap = [0]; active[0] = 1", {"code": True}), (" — Seed with height 0 (ground sentinel) that never expires. Prevents empty-heap errors and correctly generates the final [x, 0] key point when all buildings end.", {})])),
    N.para(N.rich([("heapq.heappush(max_heap, h)  # h < 0", {"code": True}), (" — Push the negated height. Python's min-heap then naturally gives the most-negative = largest positive height at the top.", {})])),
    N.para(N.rich([("active[-h] += 1", {"code": True}), (" — Increment active count for this height value (using +height as the key). Supports multiple buildings of the same height.", {})])),
    N.para(N.rich([("active[h] -= 1  # end event", {"code": True}), (" — Decrement count for the ending building. We do NOT call heapq.heappop here — lazy deletion means we defer cleanup.", {})])),
    N.para(N.rich([("while active[-max_heap[0]] == 0: heapq.heappop(max_heap)", {"code": True}), (" — Lazy cleanup: pop stale top entries (buildings whose count dropped to 0) before reading the max.", {})])),
    N.para(N.rich([("cur_max = -max_heap[0]", {"code": True}), (" — Negate the heap top back to get the actual maximum height.", {})])),
    N.para(N.rich([("if not result or result[-1][1] != cur_max: result.append([x, cur_max])", {"code": True}), (" — Only emit a key point when the height actually changes. The 'not result' check handles the very first key point.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ─────────────────────────────────────────────────
SOL2_CODE = '''\
def getSkyline_brute(buildings):
    # Collect all unique x-positions (left and right edges)
    xs = sorted(set(x for L, R, H in buildings for x in (L, R)))
    result, prev = [], 0
    for x in xs:
        # For each x, find the tallest building whose range covers x
        # Use half-open [L, R) so end events don't count at their own x
        max_h = max((H for L, R, H in buildings if L <= x < R), default=0)
        if max_h != prev:
            result.append([x, max_h])
            prev = max_h
    return result
# Time: O(n^2) — O(n) candidates * O(n) scan per candidate
# Space: O(n) for xs list and result
'''

blocks += [
    N.h2("Solution 2 — Brute Force (O(n²), mention first in interviews)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading: for every x-position where something might change (building edges), ask 'what is the tallest building that covers this x?'"),
        N.h4("What Doesn't Work"),
        N.para("This approach correctly solves the problem but requires O(n) time per query and there are O(n) candidate x-positions — giving O(n²) total. For n = 10,000 this is 10^8 operations, too slow."),
        N.h4("The Key Observation"),
        N.para("Use the half-open interval convention [L, R): a building at left=5 starts contributing from x=5, and a building at right=9 stops contributing before x=9. This ensures the end of one building and the start of another at the same x are handled correctly."),
        N.h4("Building the Solution"),
        N.para("Collect all distinct x-coordinates (2n of them). For each, use a max generator expression over all buildings. If the max differs from the previous emitted height, emit a key point."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("xs = sorted(set(...))", {"code": True}), (" — Collect all building left/right edges as candidate x-positions. Deduplicate (set) and sort. O(n log n).", {})])),
    N.para(N.rich([("max((H for L,R,H in buildings if L <= x < R), default=0)", {"code": True}), (" — Half-open interval check. ", {}), ("L <= x < R", {"code": True}), (" means building covers x (strictly: its right wall is not visible at x=R). O(n) per x.", {})])),
    N.para(N.rich([("if max_h != prev", {"code": True}), (" — Only append when height changes. Handles consecutive x-positions with the same height.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Sweep Line + Max Heap", "O(n log n)", "O(n)", "Sort 2n events; each building pushed/popped once"],
        ["Brute Force", "O(n²)", "O(n)", "O(n) candidates × O(n) scan; correct but slow"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Advanced Data Structures (Sweep Line + Ordered Structure)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Events + Max Heap, Lazy Deletion", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("You see intervals [L, R] on an axis with a value (height, priority). You need max/min/count of ACTIVE intervals at query positions. Efficient updates needed as intervals start and end. Keywords: buildings, activity, overlap, 'what is active at time t', 'the tallest/deepest covering x'.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sweep-line or event-driven technique:"),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Min-heap of end-times counts minimum meeting rooms; same event-based sweep structure.", {})])),
    N.bullet(N.rich([("Minimum Interval to Include Each Query", {"bold": True}), (" (Hard) — Sort queries + events; heap of active intervals keyed by length.", {})])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}), (" (Hard) — Merge all employee intervals via sweep; find uncovered gaps.", {})])),
    N.bullet(N.rich([("Rectangle Area II", {"bold": True}), (" (Hard) — Sweep line over rectangles; compute union area with segment tree or coordinate compression.", {})])),
    N.bullet(N.rich([("My Calendar III", {"bold": True}), (" (Hard) — Dynamic interval booking; sweep to find max concurrent bookings.", {})])),
    N.bullet(N.rich([("Number of Flowers in Full Bloom", {"bold": True}), (" (Hard) — Count active flowers at each query time; binary search on sorted start/end arrays.", {})])),
    N.bullet(N.rich([("Maximum Population Year", {"bold": True}), (" (Easy) — Simplest sweep-line: difference array over birth/death years.", {})])),
    N.para("These problems share the core skeleton: events at start/end boundaries → sort → maintain active set or max/count → query at each event."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Advanced Data Structures section (Events + Heap sub-pattern). Sub-pattern classification is based on analysis; this specific sub-pattern may not be listed verbatim in the guide.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the sweep-line algorithm visually — use Next/Prev or arrow keys to watch the heap and skyline evolve event by event.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append blocks ────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
