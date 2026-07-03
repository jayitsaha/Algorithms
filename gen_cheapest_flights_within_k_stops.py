"""
Notion update for: Cheapest Flights Within K Stops (LC #787)
Page ID: 39193418-809c-812b-966a-ea744f95774e
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812b-966a-ea744f95774e"

print("Step 1: Set page properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=787,
    pattern="Graph",
    subpatterns=["Bellman-Ford K Iterations"],
    tc="O(K·E)",
    sc="O(n)",
    key_insight="Run Bellman-Ford for exactly k+1 rounds; copy dist to temp before each round to enforce the per-round edge limit.",
    icon="🟡"
)
print("  Properties set OK")

print("Step 2: Wipe existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks")

print("Step 3: Build new page body...")

PROBLEM_STATEMENT = (
    "There are n cities connected by flights. Each flight is [from, to, price]. "
    "Given src, dst, and k, find the cheapest price to reach dst from src with at most k stops. "
    "A 'stop' is an intermediate city. Return -1 if no such route exists.\n\n"
    "Constraints: 1 ≤ n ≤ 100, 0 ≤ flights.length ≤ (n*(n-1)/2), "
    "0 ≤ src, dst < n, src ≠ dst, 0 ≤ k < n, 1 ≤ price ≤ 10^4"
)

SOL1_CODE = '''\
def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    INF = float('inf')
    dist = [INF] * n          # cheapest cost to each city using <= i flights
    dist[src] = 0             # source: zero cost

    for i in range(k + 1):   # k stops = k+1 flights = k+1 rounds
        temp = dist[:]        # SNAPSHOT: freeze current dist before this round
        for u, v, w in flights:
            if dist[u] < INF:                        # only extend reachable cities
                temp[v] = min(temp[v], dist[u] + w)  # read dist (frozen), write temp
        dist = temp           # commit this round's updates

    return dist[dst] if dist[dst] < INF else -1
'''

SOL2_CODE = '''\
import heapq
from collections import defaultdict

def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    # State: (total_cost, current_city, stops_used_so_far)
    heap = [(0, src, 0)]
    best = {}   # (city, stops) -> min cost seen

    while heap:
        cost, u, stops = heapq.heappop(heap)
        if u == dst:
            return cost
        if stops > k:
            continue
        state = (u, stops)
        if best.get(state, float('inf')) <= cost:
            continue
        best[state] = cost
        for v, w in graph[u]:
            heapq.heappush(heap, (cost + w, v, stops + 1))

    return -1
'''

blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Key constraint: ", {"bold": True}),
        ("k stops = k+1 flights. The edge-count limit is what makes this different from standard shortest-path problems.")
    ])),
    N.divider(),
]

# ─── Solution 1: Bellman-Ford K Rounds ───
blocks += [
    N.h2("Solution 1 — Bellman-Ford K Rounds (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Find the minimum-cost path from src to dst in a weighted directed graph, but with a hard limit "
            "on the number of edges used: at most k+1 edges (k stops + 1). "
            "This is shortest-path with an edge-count constraint."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "DFS explores all paths — exponential. Standard Dijkstra finds the cheapest path but has no mechanism "
            "to track how many edges were used. Naive BFS (unweighted) gives hop count, not minimum cost."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Bellman-Ford has a round-based structure: after round i, dist[v] = shortest path using at most i edges. "
            "This is EXACTLY the invariant we need. We just run it k+1 times instead of n-1 times. "
            "One additional twist: we must copy dist to temp before each round to prevent chaining "
            "multiple flights within a single round."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize dist=[INF]*n, dist[src]=0.\n"
            "2. Repeat k+1 times: copy dist to temp, relax all edges reading from dist, then set dist=temp.\n"
            "3. After k+1 rounds, dist[dst] is the answer (or -1 if still INF)."
        ),
        N.callout(
            "Analogy: Imagine airline fare updates issued daily. Day 0: you can only reach airports with 0 flights. "
            "Day 1: airports reachable via 1 flight. Day 2: via 2 flights. Each day's prices are locked in "
            "before the next day's update — that's the temp-copy invariant.",
            "✈️", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Bellman-Ford"),
    N.para(N.rich([
        ("Bellman-Ford Algorithm", {"bold": True}),
        (" — Richard Bellman (1958) and Lester Ford (1956). Finds shortest paths in weighted directed graphs, "
         "including those with negative edge weights. Unlike Dijkstra, it doesn't require greedy selection — "
         "it systematically relaxes all edges in rounds.\n\n"),
        ("Core invariant: ", {"bold": True}),
        ("After round i, dist[v] = minimum cost path from src to v using at most i edges. "
         "Standard Bellman-Ford runs n-1 rounds (longest possible shortest path has n-1 edges). "
         "Here we run exactly k+1 rounds to enforce the flight limit.\n\n"),
        ("The copy trick: ", {"bold": True}),
        ("Reading from dist (frozen) and writing to temp ensures each round adds exactly one new edge to paths. "
         "Without this, a single round could chain multiple flights: updating dist[B] from dist[A], "
         "then updating dist[C] from the new dist[B] — two flights in one round.\n\n"),
        ("When to recognize: ", {"bold": True}),
        ("'Cheapest/shortest path' + 'at most K edges/stops/hops' → this algorithm. "
         "Also useful when negative weights are present (Dijkstra cannot handle them).")
    ])),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("INF = float('inf')", {"code": True}), " — sentinel value meaning 'city not yet reachable'"])),
    N.para(N.rich([("dist = [INF] * n", {"code": True}), " — array tracking cheapest cost to each city using ≤ i flights so far"])),
    N.para(N.rich([("dist[src] = 0", {"code": True}), " — we start at src with zero cost; it's always reachable for free"])),
    N.para(N.rich([("for i in range(k + 1):", {"code": True}), " — k stops = k+1 flights = k+1 rounds of relaxation"])),
    N.para(N.rich([("temp = dist[:]", {"code": True}), " — CRITICAL snapshot: all reads this round use frozen dist; writes go to temp"])),
    N.para(N.rich([("for u, v, w in flights:", {"code": True}), " — try every available flight in this round"])),
    N.para(N.rich([("if dist[u] < INF:", {"code": True}), " — only extend from cities that were reachable before this round (use dist, not temp)"])),
    N.para(N.rich([("temp[v] = min(temp[v], dist[u] + w)", {"code": True}), " — if this flight gives a cheaper route to v, update temp[v]"])),
    N.para(N.rich([("dist = temp", {"code": True}), " — commit round: temp's updates become the new dist for next round"])),
    N.para(N.rich([("return dist[dst] if dist[dst] < INF else -1", {"code": True}), " — unreachable destination returns -1"])),
    N.divider(),
]

# ─── Solution 2: Modified Dijkstra ───
blocks += [
    N.h2("Solution 2 — Modified Dijkstra with Stop State"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Embed the stop count into the search state. Instead of just (cost, city), track (cost, city, stops_used). "
            "Standard Dijkstra on this extended state space gives the minimum-cost path with the stop constraint."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard Dijkstra without stop-count in state would find the globally cheapest path, "
            "potentially ignoring paths that exceed k stops."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two different states (city_A, 2_stops) and (city_A, 3_stops) at the same physical city are DIFFERENT "
            "states — they have different remaining budgets. The state space has n*k entries. "
            "The min-heap ordering by cost still guarantees we find the optimal answer first."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build adjacency list from flights.\n"
            "2. Start heap with (0, src, 0): zero cost, at source, zero stops used.\n"
            "3. Expand cheapest state first. If city == dst, return cost.\n"
            "4. If stops > k, prune this branch.\n"
            "5. Use visited dict (city, stops) → min_cost to avoid redundant expansion."
        ),
        N.callout(
            "Trade-off: Dijkstra processes states in cost order so can exit early when dst is reached. "
            "Bellman-Ford always runs all k+1 rounds. For dense graphs or small k, Bellman-Ford is cleaner. "
            "For sparse graphs with large k, Dijkstra can be significantly faster.",
            "⚖️", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(list)", {"code": True}), " — adjacency list: city → list of (neighbor, price)"])),
    N.para(N.rich([("heap = [(0, src, 0)]", {"code": True}), " — (total_cost, current_city, stops_used_so_far); min-heap by cost"])),
    N.para(N.rich([("best = {}", {"code": True}), " — maps (city, stops) → min cost seen; prevents re-expanding dominated states"])),
    N.para(N.rich([("if u == dst: return cost", {"code": True}), " — heap is min-ordered, so first time we reach dst is cheapest"])),
    N.para(N.rich([("if stops > k: continue", {"code": True}), " — exceeded stop budget; prune this path"])),
    N.para(N.rich([("if best.get((u, stops), inf) <= cost:", {"code": True}), " — already found a cheaper way to reach this (city, stops) state"])),
    N.para(N.rich([("heapq.heappush(heap, (cost + w, v, stops + 1))", {"code": True}), " — extend path by one more flight, incrementing stop count"])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bellman-Ford K Rounds (Interview Pick)", "O((k+1) × E)", "O(n)"],
        ["Modified Dijkstra", "O(E × k × log(n×k))", "O(n × k)"],
        ["2D DP dp[stops][city]", "O(k × E)", "O(k × n)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph — Shortest Path with Constraints"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Bellman-Ford K Iterations (run exactly k+1 rounds with copy-before-relax)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Cheapest / shortest path' + 'at most K edges / stops / hops' → Bellman-Ford K rounds\n"
        "• Negative edge weights present → Bellman-Ford (Dijkstra cannot handle)\n"
        "• Edge-count constraint is the defining feature separating this from standard Dijkstra\n"
        "• If k is unlimited → reduce to standard Dijkstra / Bellman-Ford without the round limit",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique (Bellman-Ford / constrained shortest path):"),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), " (Medium) — Standard Bellman-Ford or Dijkstra, no stop limit. LeetCode #743."])),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), " (Medium) — Modified Dijkstra minimizing max edge weight on path. LeetCode #1631."])),
    N.bullet(N.rich([("Find the City With Smallest Neighbors at Threshold", {"bold": True}), " (Medium) — Floyd-Warshall all-pairs shortest path. LeetCode #1334."])),
    N.bullet(N.rich([("Minimum Cost to Reach Destination in Time", {"bold": True}), " (Hard) — DP on (time, node) state with hard time constraint. LeetCode #1928."])),
    N.bullet(N.rich([("Number of Ways to Arrive at Destination", {"bold": True}), " (Medium) — Count optimal paths via modified Dijkstra. LeetCode #1976."])),
    N.bullet(N.rich([("Minimum Number of Stops to Make Array Balanced", {"bold": True}), " (Medium) — Graph traversal with layered BFS. Similar K-hop structure."])),
    N.para("These problems share the same core technique: shortest path with an edge-count or hop-limit constraint, solved by bounding the number of Bellman-Ford relaxation rounds."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Algorithms section, Bellman-Ford sub-pattern", "📚", "gray_background"),
]

# ─── Visual Explainer embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("cheapest_flights_within_k_stops")),
    N.para(N.rich([
        ("Step through the Bellman-Ford algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
