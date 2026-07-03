"""
Notion page rebuild for LeetCode #1584 — Min Cost to Connect All Points
Prim's MST (dense graph variant). Pattern: Graph / Prim's or Kruskal's MST
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8146-be5e-c60c1af852a7"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1584,
    pattern="Graph",
    subpatterns=["Prim's / Kruskal's MST"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Dense complete graph: array Prim's tracks min_dist to each unvisited node; greedy pick by Cut Property.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Build new body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("points", {"code": True}),
        (" representing ", {}),
        ("n", {"code": True}),
        (" points on a 2D plane where ", {}),
        ("points[i] = [xᵢ, yᵢ]", {"code": True}),
        (". The cost of connecting two points ", {}),
        ("[xᵢ, yᵢ]", {"code": True}),
        (" and ", {}),
        ("[xⱼ, yⱼ]", {"code": True}),
        (" is the Manhattan distance between them: ", {}),
        ("|xᵢ - xⱼ| + |yᵢ - yⱼ|", {"code": True}),
        (". Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.", {}),
    ])),
    N.para(N.rich([("Example: ", {"bold": True}), ("points = [[0,0],[2,2],[3,10],[5,2],[7,0]]", {"code": True}), (" → Output: 20", {})])),
    N.divider(),
]

# ── Solution 1: Prim's Array (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Prim's MST, Array-Based (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to connect ALL n points into one component at minimum total edge cost. With n points and every pair connected (Manhattan distance), we have a complete graph K_n. The structure we're building is a Minimum Spanning Tree — a tree that touches every node with exactly n−1 edges and minimum total weight."),
        N.h4("What Doesn't Work"),
        N.para("Greedy nearest-neighbor (always connect to the closest unconnected point from the last one you visited) does NOT give the MST. It builds a path, not a tree. It misses cheaper branching edges. Similarly, Dijkstra finds shortest paths between two nodes — it doesn't minimize the total cost of connecting ALL nodes."),
        N.h4("The Key Observation"),
        N.para("The MST Cut Property: at any point, if you divide the graph into the nodes already in your MST (set S) and the unvisited nodes (set V−S), the minimum-weight edge crossing this cut MUST belong to every MST. So greedily picking the cheapest frontier edge is always safe — no future choice can do better while avoiding a cycle."),
        N.h4("Building the Solution"),
        N.para("Track min_dist[j] = cheapest known single edge from any MST node to unvisited node j. Start: min_dist[0]=0, all others infinity. Each round: (1) pick the unvisited node u with smallest min_dist, (2) commit it to MST, (3) update min_dist for all unvisited nodes using distances from u. After n rounds, every node is in the MST."),
        N.h4("Why Not Use a Heap?"),
        N.para("For dense graphs (complete K_n), we have O(n²) edges. Using a min-heap would cost O(n² log n) to process all edges. But an O(n) scan to find the minimum each round costs only O(n²) total — same as just computing the distances. The array approach is simpler and faster for this problem."),
        N.callout("Analogy: Imagine building a city power grid. Every day, the engineer finds the cheapest new cable that extends the grid to one more unpowered building, then runs it. This greedy daily decision is always optimal by the Cut Property — no cheaper grid exists.", "🏙️", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Prim's MST"),
    N.para("Named after Robert Prim (1957), independently discovered by Vojtech Jarník (1930) and Edsger Dijkstra (1959). Finds the Minimum Spanning Tree of a connected weighted graph."),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("min_dist[j]", {"code": True}),
        (" always equals the minimum edge weight from any node currently in the MST to unvisited node j. Picking the minimum is justified by the MST Cut Property.", {}),
    ])),
    N.para(N.rich([
        ("Key Distinction from Dijkstra: ", {"bold": True}),
        ("Prim's uses ", {}),
        ("min_dist[v] = min(min_dist[v], edge_weight(u,v))", {"code": True}),
        (" (single edge), while Dijkstra uses ", {}),
        ("dist[v] = min(dist[v], dist[u] + edge_weight(u,v))", {"code": True}),
        (" (cumulative path). Mixing these up is the #1 interview mistake.", {}),
    ])),
    N.para(N.rich([
        ("Recognize Prim's when: ", {"bold": True}),
        ('"Minimum cost to connect ALL nodes" — especially in dense graphs where edge count is O(V²).', {}),
    ])),
    N.h3("Code"),
    N.code(
"""def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)
    in_mst = [False] * n
    min_dist = [float('inf')] * n
    min_dist[0] = 0          # Seed: node 0 costs nothing to start
    total_cost = 0

    for _ in range(n):
        # Pick cheapest unvisited node (O(n) scan)
        u = -1
        for i in range(n):
            if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):
                u = i

        in_mst[u] = True
        total_cost += min_dist[u]   # Add cheapest edge into u

        # Update all unvisited neighbors
        for v in range(n):
            if not in_mst[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if d < min_dist[v]:
                    min_dist[v] = d  # Found cheaper bridge to v from u

    return total_cost""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("in_mst = [False] * n", {"code": True}), (" — Boolean array; True once a node is permanently added to the MST.", {})])),
    N.para(N.rich([("min_dist = [float('inf')] * n; min_dist[0] = 0", {"code": True}), (" — Key data structure. Infinity means 'unreachable from current MST'. Setting min_dist[0]=0 seeds the algorithm at node 0 at zero cost.", {})])),
    N.para(N.rich([("for _ in range(n):", {"code": True}), (" — Loop exactly n times. Each iteration adds one node to the MST. After n iterations, all nodes are covered.", {})])),
    N.para(N.rich([("u = argmin(min_dist, not in_mst)", {"code": True}), (" — O(n) linear scan to find the unvisited node with the cheapest known edge from the MST. This is the 'dense Prim's' bottleneck — O(n) per outer iteration = O(n²) total.", {})])),
    N.para(N.rich([("in_mst[u] = True; total_cost += min_dist[u]", {"code": True}), (" — Commit node u. Add the edge cost (min_dist[u]) to the running total. The actual edge achieving this cost came from some previously committed node.", {})])),
    N.para(N.rich([("d = abs(points[u][0]-points[v][0]) + ...", {"code": True}), (" — Compute Manhattan distance on the fly. We never store the O(n²) edge list — distances are computed as needed.", {})])),
    N.para(N.rich([("if d < min_dist[v]: min_dist[v] = d", {"code": True}), (" — Relax: if node u offers a cheaper bridge to unvisited node v than what we previously knew, update. This is the key update step (analogous to Dijkstra's relaxation, but for single edges).", {})])),
    N.divider(),
]

# ── Solution 2: Kruskal's ──
blocks += [
    N.h2("Solution 2 — Kruskal's with Union-Find"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Still MST. Kruskal's takes a different angle: instead of growing from one node outward (Prim's), it processes ALL edges globally, sorted by weight, and greedily adds edges that don't form cycles using Union-Find."),
        N.h4("What Doesn't Work About Naive Greedy"),
        N.para("Without Union-Find, detecting cycles after adding an edge would require O(n) DFS each time — O(n²) total for cycle detection alone. Union-Find amortizes this to nearly O(1) per edge with path compression and union-by-rank."),
        N.h4("The Key Observation"),
        N.para("If we sort all edges by weight and process cheapest-first, we can safely add any edge whose two endpoints are in different connected components (no cycle created). The first n−1 edges we add that are non-cycle-forming give the MST."),
        N.h4("Why It's Slower for This Problem"),
        N.para("We must explicitly generate all O(n²) edges and sort them — O(n² log n) time and O(n²) space. Prim's avoids this entirely with O(n²) time and O(n) space. For this problem, Prim's dominates. Kruskal's shines on sparse graphs where E << n²."),
    ]),
    N.h3("Code"),
    N.code(
"""def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)

    # Generate all O(n²) edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
            edges.append((d, i, j))

    edges.sort()  # O(n² log n) — the bottleneck

    # Union-Find with path compression
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    cost, used = 0, 0
    for d, u, v in edges:
        pu, pv = find(u), find(v)
        if pu != pv:               # different components: safe to add
            parent[pu] = pv        # union
            cost += d
            used += 1
            if used == n - 1:      # MST complete: n−1 edges
                break

    return cost""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("edges.sort()", {"code": True}), (" — Sorts all n(n-1)/2 edges by cost. O(n² log n). For n=1000, this is ~500K edges sorted. Kruskal's bottleneck for dense graphs.", {})])),
    N.para(N.rich([("find(x)", {"code": True}), (" — Path-halving Union-Find: each node's parent skips one level each call. Near-O(1) amortized per call (inverse Ackermann function). Critical for Kruskal's efficiency.", {})])),
    N.para(N.rich([("if pu != pv", {"code": True}), (" — Only add edge if the two endpoints are in different components. This is Kruskal's cycle-prevention mechanism — connecting different components never creates a cycle.", {})])),
    N.para(N.rich([("if used == n - 1: break", {"code": True}), (" — Early exit once n−1 edges are added. MST is complete. Any further edges would form cycles (unnecessary).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Prim's Array (Interview Pick)", "O(n²)", "O(n)", "Best for dense/complete graphs"],
        ["Kruskal's + Union-Find", "O(n² log n)", "O(n²)", "Better for sparse graphs (E << n²)"],
        ["Prim's + Min-Heap", "O(n² log n)", "O(n²)", "Same as Kruskal's here; good for sparse"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — Minimum Spanning Tree", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prim's / Kruskal's MST", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("The problem asks to connect ALL nodes/cities/points at minimum total cost, using exactly n−1 edges, with no specified source or destination. Key phrase: 'minimum cost to connect all'. Distinguish from shortest-path ('minimum cost from A to B') which is Dijkstra or BFS.", {})]),
        "🔎", "green_background"
    ),
    N.para(N.rich([("Dense vs Sparse choice: ", {"bold": True}),
                   ("If every pair has an edge (complete graph, as here) → Prim's array O(n²). If explicit edge list given with E << n² → Kruskal's or heap-Prim's at O(E log V).", {})])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Prim's / Kruskal's MST technique:"),
    N.bullet(N.rich([("Connecting Cities With Minimum Cost", {"bold": True}), (" (Medium, #1135) — Same MST goal but with explicit sparse edge list; Kruskal's is the natural fit.", {})])),
    N.bullet(N.rich([("Optimize Water Distribution in a Village", {"bold": True}), (" (Hard, #1168) — Add a virtual node 0 for well-digging costs, then find MST of augmented graph.", {})])),
    N.bullet(N.rich([("Find Critical and Pseudo-Critical Edges in MST", {"bold": True}), (" (Hard, #1489) — Determine which edges must or may appear in every MST.", {})])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium, #743) — Dijkstra (shortest path, two specific nodes) vs this problem's Prim's (MST, all nodes). Great contrast problem.", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium, #684) — Union-Find to detect the first cycle-forming edge; conceptually inverse of Kruskal's.", {})])),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), (" (Medium, #1631) — Similar greedy graph traversal but minimizes the maximum single edge on a path (minimax).", {})])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), (" (Hard, #778) — Binary search + BFS / Dijkstra on grid; related MST-adjacent greedy graph structure.", {})])),
    N.para("These problems all share the core insight: MST algorithms guarantee minimum total connection cost via greedy edge selection validated by the Cut Property."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph Algorithms) · Sub-Pattern: Prim's / Kruskal's MST", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("min_cost_to_connect_all_points")),
    N.para(N.rich([
        ("Step through Prim's MST visually — watch min_dist[] update each round, see MST edges grow one by one, and follow the active code line. Use Next/Prev or ← → arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
