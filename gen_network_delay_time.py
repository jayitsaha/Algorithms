"""gen_network_delay_time.py — Notion update for Network Delay Time (#743)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8185-8181-ebf1580d95e9"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=743,
    pattern="Graph",
    subpatterns=["Dijkstra"],
    tc="O((V+E) log V)",
    sc="O(V+E)",
    key_insight="SSSP from k via Dijkstra; answer = max(shortest paths). Return -1 if any node unreachable.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks")

# ── 3) Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a network of ", {}),
        ("n", {"code": True}),
        (" nodes labelled 1 to n. A list of travel times as directed edges ", {}),
        ("times[i] = (u, v, w)", {"code": True}),
        (", where ", {}),
        ("u", {"code": True}),
        (" is the source node, ", {}),
        ("v", {"code": True}),
        (" is the target node, and ", {}),
        ("w", {"code": True}),
        (" is the travel time. A signal is sent from node ", {}),
        ("k", {"code": True}),
        (". Return the minimum time it takes for all the ", {}),
        ("n", {"code": True}),
        (" nodes to receive the signal. If it is impossible, return ", {}),
        ("-1", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Dijkstra with Min-Heap ──
blocks += [
    N.h2("Solution 1 — Dijkstra with Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The signal's arrival time at node v = the shortest-path distance from k to v, over all possible directed paths. The network delay = the time until the LAST node receives the signal = max of all shortest-path distances."),
        N.h4("What Doesn't Work"),
        N.para("BFS finds shortest paths in unweighted graphs (each edge costs 1). Here edges have different weights — BFS would give wrong distances. A simple DFS explores all paths but recomputes overlapping sub-paths, leading to exponential time."),
        N.h4("The Key Observation"),
        N.para("If all edge weights are non-negative, we can use a greedy approach: always commit to the node with the smallest current tentative distance. Once we 'settle' that node, no future path can improve its distance (adding more non-negative edges can only increase cost)."),
        N.h4("Building the Solution"),
        N.para("1. Initialize dist[k]=0, dist[all others]=∞. Push (0, k) to a min-heap.\n2. Pop cheapest node u. Skip if stale (d > dist[u]).\n3. Relax each neighbor v: if dist[u]+w < dist[v], update and push new candidate.\n4. After heap empties, return max(dist.values()) or -1 if any node unreachable."),
        N.callout("Analogy: Like GPS routing — always commit to the closest unvisited city on the map. Greedily build the shortest path tree one node at a time.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra's Algorithm"),
    N.para(N.rich([
        ("Dijkstra's Algorithm", {"bold": True}),
        (" (Edsger Dijkstra, 1956) — Solves Single-Source Shortest Path (SSSP) on graphs with non-negative edge weights. Time: O((V+E) log V) with binary heap.", {}),
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("When node u is extracted from the min-heap with distance d, d IS the final shortest distance to u. Any alternative path must pass through an unvisited node x with heap distance ≥ d, and all future edges add ≥ 0 weight — so no alternative can beat d.", {}),
    ])),
    N.para(N.rich([
        ("Stale Entry Handling: ", {"bold": True}),
        ("When we find a better path to v, we push (new_dist, v) but the old entry stays in the heap. When the old entry is popped, we check d > dist[u] — if so, skip it (lazy deletion). This avoids costly decrease-key operations.", {}),
    ])),
    N.h3("Code"),
    N.code("""import heapq

def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    # Build adjacency list (directed graph)
    graph = {}
    for u, v, w in times:
        graph.setdefault(u, []).append((v, w))

    # Initialize distances
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0

    # Min-heap: (distance, node)
    heap = [(0, k)]

    while heap:
        d, u = heapq.heappop(heap)

        # Skip stale entries
        if d > dist[u]:
            continue

        # Relax all outgoing edges
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    ans = max(dist.values())
    return ans if ans < float('inf') else -1"""),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = {}", {"code": True}), (" — Adjacency list mapping each node to its outgoing (neighbor, weight) pairs.", {})])),
    N.para(N.rich([("for u, v, w in times:", {"code": True}), (" — Build directed graph. graph.setdefault(u, []) handles nodes with no prior entry.", {})])),
    N.para(N.rich([("dist = {i: float('inf') for i in range(1, n+1)}", {"code": True}), (" — Initialize all distances to infinity (unreachable).", {})])),
    N.para(N.rich([("dist[k] = 0", {"code": True}), (" — Source node k costs 0 to reach itself.", {})])),
    N.para(N.rich([("heap = [(0, k)]", {"code": True}), (" — Seed the min-heap with the source at distance 0.", {})])),
    N.para(N.rich([("d, u = heapq.heappop(heap)", {"code": True}), (" — Extract node u with smallest current tentative distance d.", {})])),
    N.para(N.rich([("if d > dist[u]: continue", {"code": True}), (" — Stale entry: we already found a shorter path to u and updated dist[u]. Skip this outdated heap entry.", {})])),
    N.para(N.rich([("nd = d + w", {"code": True}), (" — Candidate distance to v if we go through u.", {})])),
    N.para(N.rich([("if nd < dist[v]:", {"code": True}), (" — We found a shorter path to v! Update best known distance.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (nd, v))", {"code": True}), (" — Push the improved candidate into the heap for future processing.", {})])),
    N.para(N.rich([("return ans if ans < float('inf') else -1", {"code": True}), (" — If any node still has distance ∞, the graph is disconnected from k.", {})])),
    N.divider(),
]

# ── Solution 2: Bellman-Ford ──
blocks += [
    N.h2("Solution 2 — Bellman-Ford (Handles Negative Weights)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of greedily picking the cheapest node, we brute-force: relax every single edge in the graph, n-1 times. By the end, all shortest paths (which have at most n-1 edges) are fully computed."),
        N.h4("What Doesn't Work"),
        N.para("Doing this only once isn't enough — improvements 'ripple through' the graph. If we improve dist[u] in round 1, dist[v] (reachable from u) might improve in round 2, and so on."),
        N.h4("The Key Observation"),
        N.para("In a graph of n nodes, any shortest path visits at most n-1 edges (no shortest path has cycles in a graph with non-negative weights). So n-1 rounds of 'relax all edges' is always sufficient."),
        N.h4("Building the Solution"),
        N.para("Initialize dist[k]=0, others ∞. Repeat n-1 times: for each edge (u,v,w), if dist[u]+w < dist[v], update dist[v]. Return max(dist) or -1."),
    ]),
    N.h3("Code"),
    N.code("""def networkDelayTime_bf(times: list[list[int]], n: int, k: int) -> int:
    dist = [float('inf')] * (n + 1)  # 1-indexed
    dist[k] = 0

    for _ in range(n - 1):           # Relax n-1 times
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    ans = max(dist[1:])               # Nodes 1..n
    return -1 if ans == float('inf') else ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dist = [float('inf')] * (n+1)", {"code": True}), (" — 1-indexed array; dist[0] unused. All start unreachable.", {})])),
    N.para(N.rich([("for _ in range(n - 1):", {"code": True}), (" — At most n-1 edges in any acyclic shortest path. Each round propagates improvements one hop further.", {})])),
    N.para(N.rich([("if dist[u] + w < dist[v]: dist[v] = dist[u] + w", {"code": True}), (" — Edge relaxation: if path through u is better, update v.", {})])),
    N.para(N.rich([("ans = max(dist[1:])", {"code": True}), (" — The bottleneck node determines the answer.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Bellman-Ford", "O(V·E)", "O(V)", "Safe with negative weights; not needed here"],
        ["Dijkstra (array scan)", "O(V²)", "O(V)", "Better for very dense graphs"],
        ["Dijkstra (min-heap) ✓", "O((V+E) log V)", "O(V+E)", "Optimal for sparse graphs — Interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dijkstra — Single-Source Shortest Path with non-negative weights", {})])),
    N.callout(
        "When to recognize: Weighted directed/undirected graph + 'minimum time/cost to reach all/some nodes from a single source' + non-negative weights. Keywords: signal propagation, network delay, shortest path, minimum travel time.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra SSSP):"),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Dijkstra/Bellman-Ford with a hop-count constraint. State = (cost, node, stops_remaining). (#787)", {})])),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), (" (Medium) — Dijkstra where edge cost = |height_diff|, minimize max edge on path. (#1631)", {})])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), (" (Hard) — Dijkstra minimizing max elevation encountered on path to bottom-right. (#778)", {})])),
    N.bullet(N.rich([("Find the City With Smallest Number of Neighbors", {"bold": True}), (" (Medium) — All-pairs shortest path via Floyd-Warshall or running Dijkstra n times. (#1334)", {})])),
    N.bullet(N.rich([("Shortest Path with Alternating Colors", {"bold": True}), (" (Medium) — BFS/Dijkstra with state (node, last_edge_color). (#1129)", {})])),
    N.bullet(N.rich([("Minimum Cost to Reach City With Discounts", {"bold": True}), (" (Medium) — Dijkstra with state (node, discounts_used). (#2093)", {})])),
    N.para("These problems share the core pattern: model state as a node, use a min-heap to always expand the cheapest frontier, relax edges greedily."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Sub-Patterns → Dijkstra", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("network_delay_time")),
    N.para(N.rich([
        ("Step through Dijkstra's algorithm visually — use Next/Prev or arrow keys to see each greedy extraction and edge relaxation.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} blocks to {PAGE_ID}")
