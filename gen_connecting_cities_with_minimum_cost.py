"""
Notion page rebuild for Connecting Cities With Minimum Cost (LC #1135).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81f9-bb23-c67c81c8f532"
SLUG    = "connecting_cities_with_minimum_cost"

# ── 1) Set page properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1135,
    pattern="Graph",
    subpatterns=["Kruskal's Algorithm"],
    tc="O(E log E)",
    sc="O(N)",
    key_insight="Sort edges by cost; use Union-Find to greedily accept cheapest edge that doesn't create a cycle (Kruskal's MST).",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old bulk body ─────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Rebuild body ───────────────────────────────────────────────────────

KRUSKAL_CODE = """\
def minimumCost(n: int, connections: list) -> int:
    parent = list(range(n + 1))   # 1-indexed, each city is its own root
    rank = [0] * (n + 1)          # for union by rank

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  # path compression
        return parent[x]

    def union(x, y) -> bool:
        rx, ry = find(x), find(y)
        if rx == ry: return False         # same component → would cycle
        if rank[rx] < rank[ry]: rx, ry = ry, rx
        parent[ry] = rx                   # attach smaller tree under larger
        if rank[rx] == rank[ry]: rank[rx] += 1
        return True

    connections.sort(key=lambda e: e[2])  # sort edges cheapest first
    total_cost = 0
    components = n
    for u, v, cost in connections:
        if union(u, v):                   # bridges two different components
            total_cost += cost
            components -= 1
            if components == 1:           # all cities connected — stop early
                return total_cost
    return -1                             # graph disconnected
"""

PRIMS_CODE = """\
import heapq
from collections import defaultdict

def minimumCost_prims(n: int, connections: list) -> int:
    graph = defaultdict(list)
    for u, v, w in connections:
        graph[u].append((w, v))
        graph[v].append((w, u))   # undirected

    heap = [(0, 1)]               # start from city 1 with cost 0
    visited = set()
    total = 0
    count = 0
    while heap and count < n:
        cost, city = heapq.heappop(heap)
        if city in visited: continue
        visited.add(city)
        total += cost
        count += 1
        for w, nxt in graph[city]:
            if nxt not in visited:
                heapq.heappush(heap, (w, nxt))
    return total if count == n else -1
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given ", {}),
        ("n", {"code": True}),
        (" cities labeled 1 through n, and a list ", {}),
        ("connections", {"code": True}),
        (" where each element is ", {}),
        ("[city1, city2, cost]", {"code": True}),
        (", representing a road between two cities with the given cost. "
         "Return the minimum cost to connect all cities such that every city is reachable "
         "from every other city. If it is impossible, return -1.", {})
    ])),
    N.para("This is the classic Minimum Spanning Tree (MST) problem. "
           "A spanning tree on n nodes requires exactly n−1 edges with no cycles. "
           "The MST is the spanning tree with minimum total weight."),
    N.divider(),
]

# ── Solution 1: Kruskal's ──
blocks += [
    N.h2("Solution 1 — Kruskal's + Union-Find (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to connect all n cities into one network at minimum total road cost. "
               "The cheapest connected network on n nodes is a tree (no cycles, exactly n-1 edges) "
               "— specifically a Minimum Spanning Tree (MST)."),
        N.h4("What Doesn't Work"),
        N.para("Trying all possible subsets of n-1 edges would be exponential: C(E, n-1) subsets to check. "
               "Even for 10 cities with 20 roads, that's C(20,9) = 167,960 subsets — completely impractical. "
               "We need a smarter, greedy approach."),
        N.h4("The Key Observation"),
        N.para("The Cut Property: for any partition of cities into two groups S and V-S, "
               "the minimum-weight road crossing the cut MUST appear in some MST. "
               "Therefore: if we always pick the cheapest available road that connects two "
               "previously-disconnected groups, we're guaranteed to build an MST."),
        N.h4("Building the Solution"),
        N.para("1. Sort all roads by cost — this lets us evaluate cheapest first (greedy). "
               "2. Use Union-Find to track which cities are already connected. "
               "3. For each road in sorted order: if it connects two different components, accept it; "
               "if it would connect cities already in the same component, skip it (would create a cycle). "
               "4. Stop when all cities are in one component (components count reaches 1)."),
        N.callout(
            "Analogy: Imagine laying cable between cities. You always build the cheapest "
            "road first that links two currently-disconnected regions. Union-Find is your map "
            "that instantly tells you whether two cities are already reachable from each other.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kruskal's MST (1956)"),
    N.para("Origin: Joseph Kruskal, 1956. Solves MST on weighted undirected graphs in O(E log E) time. "
           "Uses the greedy 'cheapest safe edge first' strategy, proven correct by the Cut Property. "
           "Commonly paired with Union-Find (Disjoint Set Union, DSU) for near-O(1) cycle detection. "
           "Alternative: Prim's algorithm (BFS + min-heap), better for dense graphs."),
    N.h3("Code"),
    N.code(KRUSKAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = list(range(n + 1))", {"code": True}),
                   (" — 1-indexed parent array. parent[i]=i means city i is its own root representative. Size n+1 because cities are labeled 1..n.", {})])),
    N.para(N.rich([("rank = [0] * (n + 1)", {"code": True}),
                   (" — Tree height proxy for union by rank optimization. Keeps trees shallow.", {})])),
    N.para(N.rich([("if parent[x] != x: parent[x] = find(parent[x])", {"code": True}),
                   (" — Path compression in find(): after reaching the root, every node along the path points directly to it. Flattens the tree for O(α(n)) amortized.", {})])),
    N.para(N.rich([("if rx == ry: return False", {"code": True}),
                   (" — Same root = same component = this edge would create a cycle. Return False to signal the caller to skip this edge.", {})])),
    N.para(N.rich([("if rank[rx] < rank[ry]: rx, ry = ry, rx", {"code": True}),
                   (" — Union by rank: ensure rx has the higher (or equal) rank before attaching. This keeps the tree height at O(log n).", {})])),
    N.para(N.rich([("parent[ry] = rx", {"code": True}),
                   (" — ry's entire subtree now belongs to rx's component. The merge is O(1).", {})])),
    N.para(N.rich([("connections.sort(key=lambda e: e[2])", {"code": True}),
                   (" — Sort all edges by cost ascending. This is O(E log E) and is the bottleneck of the entire algorithm.", {})])),
    N.para(N.rich([("if union(u, v):", {"code": True}),
                   (" — Attempt to merge u and v's components. Returns True if they were in different components (edge accepted) or False (edge would cycle).", {})])),
    N.para(N.rich([("if components == 1: return total_cost", {"code": True}),
                   (" — Early termination: once all cities are in one component, we have our MST. No need to process remaining edges.", {})])),
    N.para(N.rich([("return -1", {"code": True}),
                   (" — Exhausted all edges but components > 1 means the graph is disconnected — some cities are unreachable.", {})])),
    N.divider(),
]

# ── Solution 2: Prim's ──
blocks += [
    N.h2("Solution 2 — Prim's Algorithm (Min-Heap)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Prim's grows the MST from a single starting city. At each step, "
               "we add the cheapest road that connects a new city to our already-built tree."),
        N.h4("What Doesn't Work"),
        N.para("Naive Prim's (scan all edges each step) is O(V·E). We optimize "
               "with a min-heap that always gives us the cheapest available edge in O(log E)."),
        N.h4("The Key Observation"),
        N.para("At any point, the cheapest road from the 'visited' city set to an 'unvisited' city "
               "is always safe to include in the MST. This is the same Cut Property as Kruskal's, "
               "just applied differently: grow from one seed instead of merging components globally."),
        N.h4("Building the Solution"),
        N.para("Use a min-heap seeded with (0, start_city). Each step: pop cheapest (cost, city), "
               "skip if already visited, else add to MST (add cost, mark visited), push all "
               "unvisited neighbors. Stop when all n cities are visited or heap is exhausted."),
    ]),
    N.h3("Code"),
    N.code(PRIMS_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(0, 1)]", {"code": True}),
                   (" — Seed from city 1 with cost 0. City 1 is included 'for free' as the starting point.", {})])),
    N.para(N.rich([("if city in visited: continue", {"code": True}),
                   (" — A city may be in the heap multiple times (pushed by multiple neighbors). Skip duplicates.", {})])),
    N.para(N.rich([("total += cost; count += 1", {"code": True}),
                   (" — Accept this city into the MST: add its connecting edge cost, increment city count.", {})])),
    N.para(N.rich([("return total if count == n else -1", {"code": True}),
                   (" — If we visited all n cities, return total. Otherwise graph was disconnected.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Kruskal's + Union-Find", "O(E log E)", "O(N)", "Interview pick; simpler for sparse graphs"],
        ["Prim's + Min-Heap", "O(E log V)", "O(V+E)", "Better for dense graphs (V² edges)"],
        ["Brute Force", "Exponential", "O(N)", "Impractical; for intuition only"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Minimum Spanning Tree)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Kruskal's Algorithm + Union-Find (DSU)", {})])),
    N.callout(
        "When to recognize this pattern: 'connect all nodes/cities,' 'minimum cost,' "
        "weighted undirected edges, 'return -1 if impossible.' The combination of these signals "
        "points directly to MST. Union-Find is the default tool for cycle detection in Kruskal's. "
        "Also recognize Union-Find for: connected components, grouping/merging, detecting cycles.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Kruskal's MST / Union-Find):"),
    N.bullet(N.rich([("Min Cost to Connect All Points", {"bold": True}),
                     (" (Medium) — MST on a complete graph with Manhattan distance costs (#1584)", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}),
                     (" (Medium) — Find the edge that creates a cycle; use Union-Find to detect it (#684)", {})])),
    N.bullet(N.rich([("Number of Provinces", {"bold": True}),
                     (" (Medium) — Count disconnected components using Union-Find or DFS (#547)", {})])),
    N.bullet(N.rich([("Accounts Merge", {"bold": True}),
                     (" (Medium) — Group emails by owner using Union-Find on shared email addresses (#721)", {})])),
    N.bullet(N.rich([("Most Stones Removed with Same Row or Column", {"bold": True}),
                     (" (Medium) — Union-Find to group stones sharing row/column; count removable (#947)", {})])),
    N.bullet(N.rich([("Critical Connections in a Network", {"bold": True}),
                     (" (Hard) — Find bridges (edges whose removal disconnects graph) via Tarjan's DFS (#1192)", {})])),
    N.para("These problems share the core technique: Union-Find for near-O(1) component merging and cycle detection."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Algorithms section. "
        "Sub-Pattern: Kruskal's Algorithm. Source: Guide Graph section + Analysis.",
        "📚", "gray_background"
    ),
]

# ── Interactive Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
