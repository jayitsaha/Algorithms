"""
gen_bus_routes.py — Regenerate Notion page for Bus Routes (LC #815).
Run from the Algorithms directory: python3 gen_bus_routes.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81e5-8c75-ec488962286b"
SLUG = "bus_routes"

# ─── 1. Set properties ───────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=815,
    pattern="Graph",
    subpatterns=["BFS on Routes Graph"],
    tc="O(N·R)",
    sc="O(N·R)",
    key_insight="BFS over routes (not stops): board one route = one bus = one BFS level. Build stop→routes reverse index to bridge stops and routes.",
    icon="🔴"
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────────────
print("Wiping old page body...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} old blocks.")

# ─── 3. Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("routes", {"code": True}),
        (" where ", {}),
        ("routes[i]", {"code": True}),
        (" is a bus route that the ", {}),
        ("i", {"code": True}),
        ("-th bus repeats forever. You will start at the bus stop ", {}),
        ("source", {"code": True}),
        (" and want to reach the bus stop ", {}),
        ("target", {"code": True}),
        (". Return the least number of buses you must take to travel from ", {}),
        ("source", {"code": True}),
        (" to ", {}),
        ("target", {"code": True}),
        (". Return ", {}),
        ("-1", {"code": True}),
        (" if it is not possible.", {}),
    ])),
    N.para("Example: routes = [[1,2,7],[3,6,7]], source = 1, target = 6. Answer: 2. Take bus 0 (stops 1,2,7) to stop 7, then bus 1 (stops 3,6,7) to stop 6."),
    N.divider(),
]

# ── Solution 1 — BFS on Routes ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS on Routes Graph (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Find the minimum number of groups (bus routes) you must enter to get from a starting element (source stop) to a target element (target stop), where groups overlap at shared elements (stops)."),
        N.h4("What Doesn't Work"),
        N.para("BFS on stops with stop-to-stop edges: two stops are 'adjacent' if they share a route. This creates O(M²) edges per route of length M, which is expensive to build and — worse — each edge counts as one bus change, not zero. Riding the same bus from stop A to stop B would incorrectly count as 1 bus taken."),
        N.h4("The Key Observation"),
        N.para("Once you board a bus route, you can ride to ANY stop on that route for free. The cost is per ROUTE boarded, not per stop visited. So the BFS hop should be 'board a new route' = 1, not 'move to adjacent stop' = 1."),
        N.h4("Building the Solution"),
        N.para("1. Build stop→routes index: for each stop, which routes serve it? This is O(total stops). 2. BFS: each level = one more bus. For each stop in the current level, look up its routes. For each unvisited route, board it (mark visited) and add all its stops to the next level. First time target appears = minimum buses. 3. Two visited sets: stops (no re-enqueue) and routes (no re-expansion)."),
        N.callout("Analogy: Think of bus routes as 'teleporters'. Once you step into a teleporter (route), you instantly have access to all its exits (stops). The cost is entering the teleporter, not choosing which exit.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""from collections import defaultdict, deque

def numBusesToDestination(routes, source, target):
    if source == target:
        return 0

    # Build reverse index: stop -> list of route indices that serve it
    stop_to_routes = defaultdict(list)
    for i, route in enumerate(routes):
        for stop in route:
            stop_to_routes[stop].append(i)

    # BFS over stops, expanding by routes
    queue = deque([source])
    visited_stops = {source}
    visited_routes = set()
    buses = 0

    while queue:
        buses += 1  # boarding one more bus in this BFS level
        for _ in range(len(queue)):
            stop = queue.popleft()
            for ri in stop_to_routes[stop]:
                if ri in visited_routes:
                    continue
                visited_routes.add(ri)
                for next_stop in routes[ri]:
                    if next_stop == target:
                        return buses
                    if next_stop not in visited_stops:
                        visited_stops.add(next_stop)
                        queue.append(next_stop)

    return -1"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if source == target: return 0", {"code": True}), (" — trivial case: already at destination, zero buses needed.", {})])),
    N.para(N.rich([("stop_to_routes = defaultdict(list)", {"code": True}), (" — reverse index mapping each stop ID to all route indices that serve it. Built in O(total stops) time.", {})])),
    N.para(N.rich([("for i, route in enumerate(routes): for stop in route: stop_to_routes[stop].append(i)", {"code": True}), (" — populate the reverse index by iterating every stop on every route.", {})])),
    N.para(N.rich([("queue = deque([source]); visited_stops = {source}", {"code": True}), (" — seed BFS with the source stop. Mark it visited immediately to prevent re-enqueueing.", {})])),
    N.para(N.rich([("visited_routes = set()", {"code": True}), (" — track which routes have been boarded. KEY: without this, a route with M stops gets re-expanded M times — O(M²) wasted work.", {})])),
    N.para(N.rich([("buses += 1", {"code": True}), (" — increment at the top of each while iteration because every stop currently in the queue requires at least one more bus to process.", {})])),
    N.para(N.rich([("for _ in range(len(queue))", {"code": True}), (" — process exactly the stops queued in this BFS level (classic level-order BFS pattern). This ensures buses counts levels correctly.", {})])),
    N.para(N.rich([("if ri in visited_routes: continue", {"code": True}), (" — skip routes already boarded. This is the critical optimization that keeps complexity linear.", {})])),
    N.para(N.rich([("if next_stop == target: return buses", {"code": True}), (" — check target during route scanning (not on dequeue) to get the correct bus count immediately without an extra level increment.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — queue exhausted with no path found; target is unreachable from source.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Stop-Adjacency BFS (naive)", "O(M² per route) — TLE", "O(N²)"],
        ["BFS on Routes Graph (optimal)", "O(N · R)", "O(N · R)"],
    ]),
    N.para("N = total number of stops across all routes (sum of route lengths). R = number of routes. Each stop is enqueued at most once (O(N)). Each route is expanded at most once (O(N) total work across all route expansions). Building stop_to_routes index is O(N)."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (BFS — Shortest Path Unweighted)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS on Routes Graph", {})])),
    N.callout(
        "When to recognize this pattern: 'minimum number of buses/trains/flights', entities belong to groups (routes), movement within a group is free, transitions happen at shared members (stops), need a reverse index (element→which groups contain it). Key signal: you're counting group changes, not element changes.",
        "🔎", "green_background"
    ),
    N.para("Note: 'BFS on Routes Graph' is an extension of the standard BFS Shortest Path Unweighted sub-pattern, specialized for transportation/grouping problems. It is recognized as a named variant in competitive programming literature."),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (BFS with group/route expansion):"),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), (" (Hard) — Each word is a stop; one-letter-change connects words like routes connect stops. BFS over word-change groups. (#127)", {})])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}), (" (Hard) — BFS grouping array indices by value; expanding the whole group at once is the same 'route expansion' idea. (#1345)", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — Multi-source BFS; count minimum hops to reach target cell. (#1091)", {})])),
    N.bullet(N.rich([("Minimum Jumps to Reach Home", {"bold": True}), (" (Medium) — BFS on positions with forward/backward constraints; minimum jumps = minimum buses. (#1654)", {})])),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), (" (Medium) — Multi-source BFS from all 0s; find shortest distance to nearest 0 for every cell. (#542)", {})])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), (" (Medium) — BFS on 4-digit lock states; minimum turns = minimum buses. (#752)", {})])),
    N.para("These problems share the core technique: BFS where the hop unit is a 'group' or 'service', not an individual element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, BFS Shortest Path Unweighted. The 'BFS on Routes Graph' variant specializes this for transportation/grouping problems.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4. Append blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
