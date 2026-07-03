"""
gen_number_of_ways_to_arrive_at_destination.py
Rebuild Notion page for LC 1976 — Number of Ways to Arrive at Destination
Pattern: Dynamic Programming / Dijkstra + Count Paths
"""
import notion_lib as N

PAGE_ID = "39193418-809c-817e-8757-e387adbf6b7f"
SLUG    = "number_of_ways_to_arrive_at_destination"

# ── 1. Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1976,
    pattern="Dynamic Programming",
    subpatterns=["Dijkstra + Count Paths"],
    tc="O((n + m) log n)",
    sc="O(n + m)",
    key_insight=(
        "Run Dijkstra to find shortest-path distances; simultaneously maintain "
        "a ways[] array updated whenever a shorter or equal-cost path is found."
    ),
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Build body ─────────────────────────────────────────────────────────────
MOD = 10**9 + 7

blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(
        "You are in a city with n intersections numbered 0 to n-1 and m bidirectional "
        "roads, each with a travel time given in roads[i] = [u, v, time]. Find the "
        "number of ways to travel from intersection 0 to intersection n-1 in the "
        "shortest amount of time. Return the answer modulo 10^9 + 7."
    ),
    N.divider(),
]

# ── Solution 1 (Interview Pick) — Dijkstra + DP Count ─────────────────────────
blocks += [
    N.h2("Solution 1 — Dijkstra + DP Count (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the shortest travel time from node 0 to node n-1 AND the count "
            "of distinct paths achieving that minimum time. Two separate questions "
            "answered in a single pass."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "BFS only works on unweighted graphs. A plain BFS here ignores edge "
            "weights and will not find the true shortest time. Brute-force DFS over "
            "all paths is exponential — O(n!) in the worst case — too slow for "
            "n up to 200 with dense graphs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Dijkstra's algorithm processes nodes in non-decreasing distance order. "
            "At the moment we finalize the shortest distance to a node v, every "
            "shortest path to v has already been discovered. We can piggyback a "
            "ways[] counter: when we relax an edge (u→v) and find a strictly shorter "
            "path, we set ways[v] = ways[u]. When we find an equally short path, "
            "we add ways[u] to ways[v]. This is dynamic programming on the DAG of "
            "shortest paths."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build an adjacency list from the roads input.\n"
            "2. Initialize dist[0]=0, dist[others]=∞; ways[0]=1, ways[others]=0.\n"
            "3. Use a min-heap seeded with (0, 0) — (distance, node).\n"
            "4. Pop the node with minimum distance. If its recorded distance is stale "
            "(already improved), skip it.\n"
            "5. For each neighbor: if new_dist < dist[nb], relax and copy ways[u]. "
            "If new_dist == dist[nb], accumulate ways[u] into ways[nb].\n"
            "6. Return ways[n-1] % MOD."
        ),
        N.callout(
            "Analogy: Imagine counting highway routes on a map. Dijkstra finds the "
            "shortest route like a GPS. The ways[] array counts how many different "
            "roads achieve that exact fastest time — like counting alternate routes "
            "in your GPS that all take the same ETA.",
            "🗺️", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra + Counting"),
    N.para(
        "Dijkstra's Algorithm (Edsger Dijkstra, 1956) finds single-source shortest "
        "paths in a weighted graph with non-negative edge weights. It is a greedy "
        "algorithm that processes nodes in order of their currently-known shortest "
        "distance, using a min-priority queue.\n\n"
        "Core invariant: When a node is popped from the heap, its recorded distance "
        "is provably the true shortest distance from the source. This guarantee "
        "holds because all edge weights are non-negative — no future relaxation "
        "can discover a shorter path.\n\n"
        "Counting extension: Because Dijkstra finalizes distances in sorted order, "
        "when we finalize dist[u] and then look at edge u→v:\n"
        "  • If dist[u] + w < dist[v]: this is a new shortest path — ways[v] = ways[u]\n"
        "  • If dist[u] + w == dist[v]: additional shortest path — ways[v] += ways[u]\n\n"
        "Why it works: The ways[] propagation forms a DP over the implicit DAG of "
        "shortest-path edges. Since Dijkstra visits in topological order of distance, "
        "ways[u] is fully computed before it is used to update ways[v].\n\n"
        "Recognize when: 'Shortest path in weighted graph' + 'count paths' → "
        "Dijkstra with parallel ways[] array."
    ),
    N.code(
        "# Dijkstra + Count Paths template\n"
        "import heapq\n"
        "def count_shortest_paths(n, adj):\n"
        "    INF = float('inf')\n"
        "    dist = [INF] * n\n"
        "    ways = [0] * n\n"
        "    dist[0] = 0\n"
        "    ways[0] = 1\n"
        "    heap = [(0, 0)]  # (dist, node)\n"
        "    while heap:\n"
        "        d, u = heapq.heappop(heap)\n"
        "        if d > dist[u]:\n"
        "            continue  # stale entry\n"
        "        for v, w in adj[u]:\n"
        "            nd = d + w\n"
        "            if nd < dist[v]:\n"
        "                dist[v] = nd\n"
        "                ways[v] = ways[u]\n"
        "                heapq.heappush(heap, (nd, v))\n"
        "            elif nd == dist[v]:\n"
        "                ways[v] = (ways[v] + ways[u]) % (10**9+7)\n"
        "    return ways[n-1]",
        "python"
    ),
    N.h3("Code"),
    N.code(
        "import heapq\n"
        "from collections import defaultdict\n"
        "\n"
        "class Solution:\n"
        "    def countPaths(self, n: int, roads: list[list[int]]) -> int:\n"
        "        MOD = 10**9 + 7\n"
        "\n"
        "        # Build adjacency list (undirected)\n"
        "        adj = defaultdict(list)\n"
        "        for u, v, t in roads:\n"
        "            adj[u].append((v, t))\n"
        "            adj[v].append((u, t))\n"
        "\n"
        "        INF = float('inf')\n"
        "        dist = [INF] * n\n"
        "        ways = [0] * n\n"
        "        dist[0] = 0\n"
        "        ways[0] = 1        # one way to be at the start\n"
        "\n"
        "        heap = [(0, 0)]    # (cumulative_time, node)\n"
        "\n"
        "        while heap:\n"
        "            d, u = heapq.heappop(heap)\n"
        "\n"
        "            # Skip stale heap entries\n"
        "            if d > dist[u]:\n"
        "                continue\n"
        "\n"
        "            for v, w in adj[u]:\n"
        "                new_dist = d + w\n"
        "\n"
        "                if new_dist < dist[v]:\n"
        "                    # Found strictly shorter path to v\n"
        "                    dist[v] = new_dist\n"
        "                    ways[v] = ways[u]   # inherit count from u\n"
        "                    heapq.heappush(heap, (new_dist, v))\n"
        "\n"
        "                elif new_dist == dist[v]:\n"
        "                    # Found equally short alternative path\n"
        "                    ways[v] = (ways[v] + ways[u]) % MOD\n"
        "\n"
        "        return ways[n - 1]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}), " — standard modulus to keep counts from overflowing 64-bit integers."])),
    N.para(N.rich([("adj = defaultdict(list)", {"code": True}), " — adjacency list; each entry is a list of (neighbor, travel_time) pairs."])),
    N.para(N.rich([("for u, v, t in roads:", {"code": True}), " — each road is bidirectional so we add both directions to the adjacency list."])),
    N.para(N.rich([("dist = [INF] * n", {"code": True}), " — dist[i] holds the current best known distance from node 0 to node i; starts at infinity."])),
    N.para(N.rich([("ways = [0] * n", {"code": True}), " — ways[i] counts how many shortest paths from 0 reach node i."])),
    N.para(N.rich([("dist[0] = 0; ways[0] = 1", {"code": True}), " — base case: we are already at node 0 with distance 0 and exactly 1 way (do nothing)."])),
    N.para(N.rich([("heap = [(0, 0)]", {"code": True}), " — min-heap seeded with (distance=0, node=0). Python's heapq is a min-heap by default."])),
    N.para(N.rich([("d, u = heapq.heappop(heap)", {"code": True}), " — extract the node with the smallest tentative distance."])),
    N.para(N.rich([("if d > dist[u]: continue", {"code": True}), " — stale entry guard: if we've already found a better path to u, discard this heap entry."])),
    N.para(N.rich([("new_dist = d + w", {"code": True}), " — candidate distance to neighbor v via node u."])),
    N.para(N.rich([("if new_dist < dist[v]:", {"code": True}), " — found a strictly shorter path: update dist and reset ways to exactly ways[u] (previous count for v is obsolete)."])),
    N.para(N.rich([("ways[v] = ways[u]", {"code": True}), " — all shortest paths to v now go through u; inherit u's count."])),
    N.para(N.rich([("heapq.heappush(heap, (new_dist, v))", {"code": True}), " — push updated distance to heap for further relaxation."])),
    N.para(N.rich([("elif new_dist == dist[v]:", {"code": True}), " — found an equally short path: add ways[u] to ways[v] (additive counting)."])),
    N.para(N.rich([("ways[v] = (ways[v] + ways[u]) % MOD", {"code": True}), " — accumulate and apply modulo to prevent overflow."])),
    N.para(N.rich([("return ways[n - 1]", {"code": True}), " — the final answer: number of shortest paths from 0 to the last node."])),
    N.divider(),
]

# ── Solution 2 — Bellman-Ford Brute Force ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Bellman-Ford / DP Relaxation (Brute Force Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Bellman-Ford relaxes all edges n-1 times, guaranteeing shortest paths "
            "in a graph with no negative cycles. We can extend it to also count paths."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Bellman-Ford's O(n*m) complexity is significantly worse than Dijkstra's "
            "O((n+m) log n). For this problem with n ≤ 200 it's technically acceptable, "
            "but it's the wrong tool when all weights are non-negative. It also doesn't "
            "handle counting as cleanly because order of relaxation isn't guaranteed."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Run n-1 rounds of edge relaxations. In parallel, maintain a ways[] array. "
            "After all relaxations converge, ways[n-1] holds the count. However, "
            "because relaxations can happen in any order, you need an additional pass "
            "to propagate counts correctly — making the implementation more complex "
            "than the Dijkstra approach."
        ),
        N.h4("Building the Solution"),
        N.para(
            "This approach is presented for educational context only. In an interview, "
            "prefer Dijkstra. Bellman-Ford is the right choice when edge weights can be "
            "negative (not the case here)."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "# Bellman-Ford baseline — O(n * m), for reference only\n"
        "def countPaths_bf(n: int, roads: list[list[int]]) -> int:\n"
        "    MOD = 10**9 + 7\n"
        "    INF = float('inf')\n"
        "    dist = [INF] * n\n"
        "    ways = [0] * n\n"
        "    dist[0] = 0\n"
        "    ways[0] = 1\n"
        "\n"
        "    for _ in range(n - 1):           # n-1 relaxation rounds\n"
        "        for u, v, t in roads:\n"
        "            for a, b in [(u, v), (v, u)]:   # bidirectional\n"
        "                if dist[a] + t < dist[b]:\n"
        "                    dist[b] = dist[a] + t\n"
        "                    ways[b] = ways[a]\n"
        "                elif dist[a] + t == dist[b]:\n"
        "                    ways[b] = (ways[b] + ways[a]) % MOD\n"
        "\n"
        "    return ways[n - 1]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for _ in range(n - 1):", {"code": True}), " — Bellman-Ford guarantees convergence after n-1 rounds (shortest path can have at most n-1 edges)."])),
    N.para(N.rich([("for u, v, t in roads:", {"code": True}), " — iterate over all edges in arbitrary order each round."])),
    N.para(N.rich([("for a, b in [(u, v), (v, u)]:", {"code": True}), " — try both directions since roads are bidirectional."])),
    N.para(N.rich([("dist[a] + t < dist[b]:", {"code": True}), " — if going through a to b is shorter, update dist[b] and inherit count."])),
    N.para(N.rich([("elif dist[a] + t == dist[b]:", {"code": True}), " — if equally short, add ways[a] to ways[b]."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Dijkstra + Count (Interview Pick)", "O((n + m) log n)", "O(n + m)"],
        ["Bellman-Ford Baseline", "O(n × m)", "O(n + m)"],
    ]),
    N.divider(),
]

# ── Why is This DP? ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(
        "The ways[] array is a DP table where ways[v] = number of shortest paths from "
        "node 0 to node v. The recurrence is:\n\n"
        "  ways[v] = Σ ways[u]  for all edges (u, v) where dist[u] + weight(u,v) == dist[v]\n\n"
        "This satisfies both DP pillars:"
    ),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        "Every sub-path of a shortest path is itself a shortest path. If the shortest "
        "path from 0 to n-1 passes through node v, then the prefix from 0 to v must "
        "also be a shortest path from 0 to v."
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        "Multiple shortest paths to n-1 may share the same intermediate nodes. "
        "Computing ways[v] once and reusing it (rather than recomputing per path) "
        "is the DP optimization."
    ])),
    N.code(
        "# Recurrence relation\n"
        "# dist[v] = min(dist[u] + weight(u,v))   for all neighbors u of v\n"
        "# ways[v] = Σ ways[u]                     for edges where dist[u]+w == dist[v]\n"
        "#\n"
        "# Base case: dist[0] = 0, ways[0] = 1",
        "python"
    ),
    N.callout(
        "Key insight: Dijkstra processes nodes in topological order of their distance "
        "from the source. This means when we compute ways[v], all nodes u that "
        "contribute to ways[v] have already been fully computed — a perfect DP dependency order.",
        "🔑", "blue_background"
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Dijkstra + Count Paths"])),
    N.para(N.rich([("Also involves: ", {"bold": True}), "Graph — Dijkstra (shortest path in weighted graph)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Number of ways to reach destination in minimum time/cost'\n"
        "• 'Count shortest paths' in a weighted graph\n"
        "• Any problem combining Dijkstra shortest-path with path counting\n"
        "• Graphs with non-negative edge weights where you need both the optimal "
        "value AND a count of how many solutions achieve it",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra / shortest path / count):"),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), " (Medium, LC 743) — Pure Dijkstra to find max shortest distance; no counting."])),
    N.bullet(N.rich([("Path with Minimum Effort", {"bold": True}), " (Medium, LC 1631) — Dijkstra on a grid where edge weight = height difference."])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), " (Medium, LC 787) — Bellman-Ford variant with constraint on number of hops."])),
    N.bullet(N.rich([("Number of Shortest Paths in a Graph", {"bold": True}), " (Hard, LC 1786) — Direct sibling; count shortest paths excluding certain edges."])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium, LC 797) — DFS/BFS to count all paths in a DAG (unweighted)."])),
    N.bullet(N.rich([("Shortest Path Visiting All Nodes", {"bold": True}), " (Hard, LC 847) — BFS + bitmask DP; related 'count optimal paths' theme."])),
    N.bullet(N.rich([("Find the City With the Smallest Number of Neighbors at a Threshold Distance", {"bold": True}), " (Medium, LC 1334) — Floyd-Warshall all-pairs shortest paths."])),
    N.bullet(N.rich([("Second Minimum Time to Reach Destination", {"bold": True}), " (Hard, LC 2045) — Modified Dijkstra tracking both minimum and second-minimum times."])),
    N.para("These problems share the core technique: weighted graph + Dijkstra + dynamic programming on the shortest-path DAG."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Dynamic Programming / Graph Algorithms", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Push to Notion ─────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK  {PAGE_ID}  ({len(blocks)} blocks appended)")
