"""
gen_optimize_water_distribution_in_a_village.py
Rebuild Notion page for: Optimize Water Distribution in a Village (LC #1168)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-811e-8e3e-e324b309ecd5"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1168,
    pattern="Graph",
    subpatterns=["Virtual Node + MST", "Union-Find"],
    tc="O(E log E)",
    sc="O(V + E)",
    key_insight="Add virtual node 0; connecting to it = drilling a well. Find MST of augmented graph with Kruskal's + Union-Find.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "There are n houses in a village. We want to supply water to all houses by building wells "
    "and laying pipes. For each house i, we can either dig a well inside it directly with cost "
    "wells[i-1] (0-indexed), or connect it to another house with a pipe. Each pipe has a cost "
    "and connects exactly two houses. The goal is to supply water to all houses at minimum total cost.\n\n"
    "Input:\n"
    "  n = number of houses\n"
    "  wells[i] = cost to dig a well at house i+1\n"
    "  pipes = list of [house1, house2, cost] triplets\n\n"
    "Return the minimum total cost to supply water to all n houses.\n\n"
    "Example: n=3, wells=[1,2,2], pipes=[[1,2,1],[2,3,1]] → Output: 3\n"
    "  (Dig well at house 1 for cost 1; pipe house1→house2 for cost 1; pipe house2→house3 for cost 1)"
)

SOLUTION1_CODE = """\
def minCostToSupplyWater(n: int, wells: list[int], pipes: list[list[int]]) -> int:
    # Add virtual node 0: each well = edge from 0 to house i
    edges = [(w, 0, i + 1) for i, w in enumerate(wells)]
    # Add all pipe edges (reformat to cost-first)
    edges += [(c, u, v) for u, v, c in pipes]
    # Sort by cost — Kruskal's processes cheapest first
    edges.sort()

    # Union-Find with path compression
    parent = list(range(n + 1))  # nodes 0..n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # path compression
        return parent[x]

    total = 0
    for cost, u, v in edges:
        pu, pv = find(u), find(v)
        if pu != pv:          # different components: safe to merge
            parent[pu] = pv   # union
            total += cost     # add to MST
    return total\
"""

SOLUTION2_CODE = """\
import heapq

def minCostToSupplyWater_prim(n: int, wells: list[int], pipes: list[list[int]]) -> int:
    # Build adjacency list (include virtual node 0)
    adj = [[] for _ in range(n + 1)]
    for i, w in enumerate(wells):
        adj[0].append((w, i + 1))  # virtual node 0 → house i+1
        adj[i + 1].append((w, 0))
    for u, v, c in pipes:
        adj[u].append((c, v))
        adj[v].append((c, u))

    # Prim's: start from node 0
    visited = set()
    heap = [(0, 0)]  # (cost, node)
    total = 0
    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        total += cost
        for edge_cost, neighbor in adj[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (edge_cost, neighbor))
    return total\
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Kruskal's ──
blocks += [
    N.h2("Solution 1 — Virtual Node + Kruskal's MST (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The problem mixes two types of decisions: drill a well (fixed cost per house) or lay a pipe "
            "(cost between two houses). This feels complex. Simplify: 'getting water' means being connected "
            "to any water source. What if we model the water source itself as a node? Then ALL options "
            "(wells and pipes) become edges in a graph, and we just need the cheapest way to connect "
            "every house to this source node — a Minimum Spanning Tree."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try all 2^n subsets of houses to drill wells, then compute min pipe cost for "
            "each. This is exponential. Greedy without unification: should we drill cheap wells or use "
            "cheap pipes first? It's unclear which to prioritize without comparing them on equal footing."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Add a virtual node 0. 'Drilling a well at house i' = adding an edge between node 0 and node i "
            "with cost wells[i-1]. Node 0 is the unlimited water source. Now every choice is just an edge. "
            "The minimum cost to connect all nodes (0..n) in this augmented graph is exactly the answer. "
            "This is the Minimum Spanning Tree of the augmented graph."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create edge list: for each house i, add (wells[i-1], 0, i+1). For each pipe [u,v,c], add (c,u,v).\n"
            "2. Sort edges by cost.\n"
            "3. Initialize Union-Find for nodes 0..n.\n"
            "4. Kruskal's: iterate sorted edges. If edge (u,v) connects two different components, add it to MST.\n"
            "5. Return total MST cost."
        ),
        N.callout(
            "Analogy: Think of node 0 as a municipal water tower. 'Digging a well' = building a private pipeline "
            "directly to the tower. 'Laying a pipe' = connecting your house to your neighbor's. Kruskal's finds "
            "the cheapest network that hooks every house to the tower (directly or via neighbors).",
            "🏗️", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kruskal's + Union-Find"),
    N.para(
        "Kruskal's Algorithm (Joseph Kruskal, 1956) builds a Minimum Spanning Tree by greedily selecting "
        "the cheapest edge that doesn't form a cycle. It works on any connected weighted graph.\n\n"
        "Core invariant: at every step, selected edges form a minimum-cost spanning forest (acyclic subgraph). "
        "Adding a cross-component edge is always safe by the Cut Property of MSTs.\n\n"
        "Cycle detection is handled by Union-Find (Disjoint Set Union). 'find(x)' returns the root of x's "
        "component. If find(u) == find(v), they're in the same component → adding edge (u,v) creates a cycle → skip.\n\n"
        "Path Compression: when find(x) traces up to root r, it rewires parent[x] = r for all ancestors. "
        "This makes future find() calls O(1) amortized. Combined with union by rank, Union-Find operations "
        "run in O(α(n)) ≈ O(1) amortized (α = inverse Ackermann function).\n\n"
        "When to recognize Kruskal's: problem asks for minimum cost to 'connect' nodes, costs are on edges, "
        "graph connectivity matters."
    ),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("edges = [(w, 0, i+1) for i, w in enumerate(wells)]", {"code": True}),
                   " — Create virtual edges. wells[0] is cost for house 1, so we use i+1 for 1-indexed house number."])),
    N.para(N.rich([("edges += [(c, u, v) for u, v, c in pipes]", {"code": True}),
                   " — Append pipe edges. Reformat from [u,v,c] to (c,u,v) so tuples sort by cost first."])),
    N.para(N.rich([("edges.sort()", {"code": True}),
                   " — Sort all edges by cost (first element of each tuple). This is the O(E log E) step."])),
    N.para(N.rich([("parent = list(range(n + 1))", {"code": True}),
                   " — Initialize Union-Find: n+1 nodes (0 through n), each its own root."])),
    N.para(N.rich([("if parent[x] != x: parent[x] = find(parent[x])", {"code": True}),
                   " — Path compression: recursively find root and flatten the tree for O(1) future calls."])),
    N.para(N.rich([("pu, pv = find(u), find(v)", {"code": True}),
                   " — Find the root/representative of each endpoint's component."])),
    N.para(N.rich([("if pu != pv:", {"code": True}),
                   " — Different roots = different components = adding this edge is safe (no cycle)."])),
    N.para(N.rich([("parent[pu] = pv", {"code": True}),
                   " — Union: merge the two components by making one root point to the other."])),
    N.para(N.rich([("total += cost", {"code": True}),
                   " — This edge is in the MST; accumulate its cost."])),
    N.para(N.rich([("return total", {"code": True}),
                   " — After processing all edges, total is the minimum cost to connect all nodes (all houses get water)."])),
    N.divider(),
]

# ── Solution 2: Prim's ──
blocks += [
    N.h2("Solution 2 — Virtual Node + Prim's MST"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same augmented graph as before. But instead of sorting all edges and processing them globally "
            "(Kruskal's), Prim's algorithm grows the MST one node at a time, always expanding by the cheapest "
            "available edge from the current tree boundary."
        ),
        N.h4("What's Different from Kruskal's?"),
        N.para(
            "Kruskal's is edge-centric: processes all edges sorted globally. Prim's is vertex-centric: starts "
            "at one node and greedily expands. Prim's is better when the graph is dense (many edges), "
            "because it explores only edges adjacent to the current MST. Kruskal's is better for sparse graphs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Start Prim's from virtual node 0. The min-heap always contains the cheapest way to reach an "
            "unvisited node. Popping from the heap gives the next cheapest expansion. We visit n+1 nodes total "
            "(0 through n), so we do exactly n+1 heap pops for MST."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build adjacency list including virtual node 0.\n"
            "2. Start heap with (0, 0) — zero cost to reach node 0 itself.\n"
            "3. Pop (cost, node): if visited, skip. Else mark visited and add cost to total.\n"
            "4. Push all neighbors of node to heap.\n"
            "5. Return total after n+1 nodes are visited."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("adj[0].append((w, i+1)); adj[i+1].append((w, 0))", {"code": True}),
                   " — Add bidirectional virtual edges from node 0 to each house."])),
    N.para(N.rich([("heap = [(0, 0)]", {"code": True}),
                   " — Start Prim's from node 0 with cost 0 (we're already there)."])),
    N.para(N.rich([("if node in visited: continue", {"code": True}),
                   " — Skip nodes already in MST. A node may appear multiple times in the heap."])),
    N.para(N.rich([("total += cost", {"code": True}),
                   " — First time we pop a node = cheapest way to reach it = its MST edge cost."])),
    N.para(N.rich([("heapq.heappush(heap, (edge_cost, neighbor))", {"code": True}),
                   " — Explore all neighbors: they might be reachable more cheaply via current node."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Virtual Node + Kruskal's (sort)", "O(E log E)", "O(V)", "E = n + pipes, V = n+1. Dominated by sort."],
        ["Virtual Node + Prim's (heap)", "O((V+E) log V)", "O(V+E)", "Better for dense graphs."],
        ["Brute Force (all subsets)", "O(2^n · n²)", "O(n)", "Unusable for n > 20."],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (MST — Minimum Spanning Tree)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Virtual Node + MST, Union-Find (Kruskal's), Greedy Edge Selection"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem mentions nodes with both 'self-cost' and 'connection cost'\n"
        "• Need all nodes 'connected to a resource' at minimum total cost\n"
        "• Two types of decisions can be unified via a virtual node\n"
        "• The phrase 'supply X to all nodes' where X has a source",
        "🔎", "green_background"
    ),
    N.callout(
        "Key trick: When a problem has heterogeneous connection types (self-supply vs. peer connection), "
        "model the 'free resource' as a virtual node 0. Convert self-supply costs to edges between that node "
        "and the house. All options become edges → apply standard MST algorithms unchanged.",
        "🧠", "blue_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same MST / Union-Find / Virtual Node technique:"),
    N.bullet(N.rich([("Min Cost to Connect All Points", {"bold": True}),
                     " (Medium) — MST on complete graph; try Prim's with dense graph optimization"])),
    N.bullet(N.rich([("Connecting Cities With Minimum Cost", {"bold": True}),
                     " (Medium) — Direct Kruskal's MST application"])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}),
                     " (Medium) — Union-Find detects the first cycle-forming edge"])),
    N.bullet(N.rich([("Number of Operations to Make Network Connected", {"bold": True}),
                     " (Medium) — Count extra edges; Union-Find counts components"])),
    N.bullet(N.rich([("Find Critical and Pseudo-Critical Edges in MST", {"bold": True}),
                     " (Hard) — Compare MST costs including/excluding each edge"])),
    N.bullet(N.rich([("Number of Islands II", {"bold": True}),
                     " (Hard) — Dynamic Union-Find as land cells are added one at a time"])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}),
                     " (Hard) — Binary search + BFS, or Dijkstra/Kruskal variant on grid"])),
    N.para("These problems share the same core technique: model connectivity as graph edges and apply greedy MST or Union-Find."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, Union-Find / MST sub-patterns.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("optimize_water_distribution_in_a_village")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
