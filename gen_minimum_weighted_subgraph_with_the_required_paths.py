"""
gen_minimum_weighted_subgraph_with_the_required_paths.py
Notion page generator for LeetCode 2203.
notion_page_id = None → create fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "minimum_weighted_subgraph_with_the_required_paths"
NAME = "Minimum Weighted Subgraph With the Required Paths"
NUMBER = 2203
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "Graph"
SUBPATTERNS = ["Dijkstra"]
TC = "O((V + E) log V)"
SC = "O(V + E)"
KEY_INSIGHT = "Run Dijkstra from src1, src2, and dest (on reversed graph); the answer is min over all v of d1[v]+d2[v]+d3[v]."

PAGE_ID = None   # null → create new page

if PAGE_ID is None:
    print("Creating new Notion page...")
    PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
    print(f"Created page: {PAGE_ID}")

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON,
)

# 2) Wipe any existing body (fresh page will have none, but safe to call)
print("Wiping existing body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body blocks
print("Appending body blocks...")
blocks = []

# ── Problem ──
PROBLEM_STMT = (
    "You are given an integer n denoting the number of nodes of a weighted directed graph. "
    "The nodes are numbered from 0 to n - 1. "
    "You are also given a 0-indexed array edges where edges[i] = [from_i, to_i, weight_i] "
    "denotes that there exists a directed edge from from_i to to_i with weight weight_i. "
    "You are given three distinct integers src1, src2, and dest denoting three distinct nodes of the graph. "
    "Return the minimum weight of a subgraph of the graph such that it is possible to reach dest "
    "from both src1 and src2 via a set of edges of this subgraph. "
    "In case such a subgraph does not exist, return -1."
)
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a directed weighted graph with ", {}),
        ("n", {"code": True}),
        (" nodes and edges ", {}),
        ("[from, to, weight]", {"code": True}),
        (", find the minimum total edge-weight subgraph that allows both ", {}),
        ("src1", {"code": True}),
        (" and ", {}),
        ("src2", {"code": True}),
        (" to reach ", {}),
        ("dest", {"code": True}),
        (". Return -1 if impossible.", {}),
    ])),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# ── Solution 1 — Dijkstra from 3 Sources (Interview Pick) ──
SOL1_CODE = '''\
import heapq
from collections import defaultdict

def minimumWeight(n, edges, src1, src2, dest):
    g  = defaultdict(list)   # original directed graph
    rg = defaultdict(list)   # reversed graph

    for u, v, w in edges:
        g[u].append((v, w))
        rg[v].append((u, w))  # reverse direction

    def dijkstra(src, graph):
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    d1 = dijkstra(src1, g)   # shortest from src1 to all nodes
    d2 = dijkstra(src2, g)   # shortest from src2 to all nodes
    d3 = dijkstra(dest, rg)  # reversed: cost from any node v to dest

    ans = float('inf')
    for v in range(n):
        ans = min(ans, d1[v] + d2[v] + d3[v])

    return ans if ans < float('inf') else -1
'''

blocks += [
    N.h2("Solution 1 — Dijkstra from 3 Sources (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need both src1 and src2 to reach dest via some subset of edges. "
            "Think visually: two paths converge on dest. They can run completely independently "
            "(paying full cost for two paths) or they can merge at some intermediate node v "
            "and share the tail v → dest. We want the cheapest option."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive approach: try all pairs of paths (one from src1, one from src2). "
            "Finding all shortest paths from every node to dest would require running Dijkstra "
            "n times — O(n × (V+E) log V), which is far too slow for n up to 10^5. "
            "We need a smarter way to get 'cost from v to dest' for every v at once."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Any optimal subgraph has a 'Y-shape': two branches from src1 and src2 merge "
            "at some node v, then share the path v → dest. "
            "So the cost equals d(src1→v) + d(src2→v) + d(v→dest). "
            "We need this for every candidate meeting node v."
        ),
        N.h4("Building the Solution"),
        N.para(
            "We need three arrays: d1[v] = shortest from src1 to v (one Dijkstra on original graph), "
            "d2[v] = shortest from src2 to v (one Dijkstra on original graph), "
            "d3[v] = shortest from v to dest. "
            "The trick for d3: if we REVERSE all edges and run Dijkstra from dest, "
            "then 'reversed distance from dest to v' = 'original distance from v to dest'. "
            "This gives us all d3 values in a single Dijkstra pass! "
            "Total: 3 Dijkstra runs. Then scan all v and return the minimum sum."
        ),
        N.callout(
            "Analogy: Think of dest as a city. Reversing roads and running Dijkstra from dest "
            "tells you how far each location is from the city — exactly what we need for d3.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra's Algorithm"),
    N.para(
        "Dijkstra's Algorithm (Edsger Dijkstra, 1956) finds shortest paths from a single source "
        "to all other nodes in a graph with non-negative edge weights. "
        "It greedily processes nodes in order of their current best-known distance."
    ),
    N.para(
        "Core invariant: when a node u is popped from the min-heap, dist[u] is finalized — "
        "no future relaxation can improve it. This is guaranteed because all edge weights ≥ 0, "
        "so any path going through a node further away cannot be shorter."
    ),
    N.para(
        "Recognize Dijkstra when: weighted directed/undirected graph, non-negative weights, "
        "single-source shortest paths, or 'minimum cost to reach X from Y'. "
        "Use Bellman-Ford instead if negative weights exist."
    ),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("g, rg = defaultdict(list), defaultdict(list)", {"code": True}),
        ("  — Create two adjacency lists: g for the original graph, rg for the reversed graph.", {}),
    ])),
    N.para(N.rich([
        ("g[u].append((v, w)); rg[v].append((u, w))", {"code": True}),
        ("  — Build both simultaneously: original edge u→v, reversed edge stored as v→u in rg.", {}),
    ])),
    N.para(N.rich([
        ("dist = [INF] * n; dist[src] = 0", {"code": True}),
        ("  — Initialize all distances to infinity except the source node (distance 0 to itself).", {}),
    ])),
    N.para(N.rich([
        ("if d > dist[u]: continue", {"code": True}),
        ("  — Skip stale heap entries: if we already found a shorter path, this entry is outdated.", {}),
    ])),
    N.para(N.rich([
        ("if nd < dist[v]: dist[v] = nd; heappush(...)", {"code": True}),
        ("  — Edge relaxation: if going through u gives a shorter path to v, update and re-queue.", {}),
    ])),
    N.para(N.rich([
        ("d3 = dijkstra(dest, rg)", {"code": True}),
        ("  — KEY TRICK: running Dijkstra from dest on the REVERSED graph gives d3[v] = cost of v→dest in original.", {}),
    ])),
    N.para(N.rich([
        ("ans = min(ans, d1[v] + d2[v] + d3[v])", {"code": True}),
        ("  — Try every node as the meeting point. INF + anything = INF, so invalid paths are auto-filtered.", {}),
    ])),
    N.para(N.rich([
        ("return ans if ans < float('inf') else -1", {"code": True}),
        ("  — If best answer is still INF, no valid subgraph exists; return -1.", {}),
    ])),
    N.divider(),
]

# ── Solution 2 — Brute Force (for context) ──
SOL2_CODE = '''\
# Brute force: for each node v, run separate Dijkstra from v to dest.
# Time: O(n × (V+E) log V) — TLE for large inputs.
# Shown here only to contrast with the optimal approach.

def minimumWeight_brute(n, edges, src1, src2, dest):
    from collections import defaultdict
    import heapq

    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))

    def dijkstra(src):
        INF = float(\'inf\')
        dist = [INF] * n
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in g[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    d1 = dijkstra(src1)
    d2 = dijkstra(src2)

    ans = float(\'inf\')
    for v in range(n):
        # Run Dijkstra from v to find cost to dest — O(n) extra runs!
        dv = dijkstra(v)
        if d1[v] < float(\'inf\') and d2[v] < float(\'inf\') and dv[dest] < float(\'inf\'):
            ans = min(ans, d1[v] + d2[v] + dv[dest])

    return ans if ans < float(\'inf\') else -1
'''

blocks += [
    N.h2("Solution 2 — Brute Force (O(n × (V+E) log V), TLE)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same observation: try every node v as the meeting point. But naively, to get cost(v→dest) we run a separate Dijkstra from each v."),
        N.h4("What Doesn't Work"),
        N.para(
            "This runs n Dijkstra passes — O(n × (V+E) log V). With n up to 100,000 this is "
            "completely infeasible. It's only useful for verifying correctness on tiny test cases."
        ),
        N.h4("The Key Observation"),
        N.para("The only thing we're missing from the optimal solution is the reversed-graph trick. Once you realize you can flip the edges and run Dijkstra from dest, the brute force becomes the optimal."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Dijkstra from 3 Sources (optimal)", "O((V + E) log V)", "O(V + E)"],
        ["Brute Force (n separate Dijkstras)", "O(n · (V+E) log V)", "O(V + E)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Shortest Paths — Dijkstra)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dijkstra (from 3 Sources / Multi-Source)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Directed weighted graph with non-negative weights. "
        "(2) Multiple sources must all reach a single destination. "
        "(3) You need 'cost from every node v to dest' efficiently → reverse edges, run Dijkstra from dest. "
        "(4) Answer formula involves combining distances from multiple sources at a meeting node.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra, shortest paths in weighted graphs):"),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium) — Single-source Dijkstra; find when all nodes are reached. (#743)", {})])),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), (" (Medium) — Dijkstra on a 2D grid minimizing maximum edge cost. (#1631)", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Modified Dijkstra/BFS with a hop-count constraint. (#787)", {})])),
    N.bullet(N.rich([("Shortest Path Visiting All Nodes", {"bold": True}), (" (Hard) — Dijkstra + bitmask state for multi-source traversal. (#847)", {})])),
    N.bullet(N.rich([("Find the City With the Smallest Number of Neighbors", {"bold": True}), (" (Medium) — Floyd-Warshall for all-pairs shortest paths. (#1334)", {})])),
    N.bullet(N.rich([("Minimum Cost to Reach Destination in Time", {"bold": True}), (" (Hard) — Time-constrained Dijkstra with an extra dimension. (#1928)", {})])),
    N.bullet(N.rich([("The Most Expensive Item in a Shop", {"bold": True}), (" (Hard) — Similar multi-source convergence pattern.", {})])),
    N.para("These problems share the same core technique: Dijkstra's algorithm with non-negative weights, often combined with graph transformation tricks (reversing edges, state augmentation)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7: Graph (Dijkstra)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
