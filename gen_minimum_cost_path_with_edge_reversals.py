"""
gen_minimum_cost_path_with_edge_reversals.py
Regenerates the Notion page for LC 2699 — Minimum Cost Path with Edge Reversals.
notion_page_id is null → create a new page.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create the page (notion_page_id is null) ──
PAGE_ID = N.create_page("Minimum Cost Path with Edge Reversals", 2699, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2699,
    pattern="Graph",
    subpatterns=["0-1 BFS"],
    tc="O(V + E)",
    sc="O(V + E)",
    key_insight="Model each directed edge as cost-0 (original) and cost-1 (reversed), then run 0-1 BFS with a deque.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing body (fresh page, but wipe for safety) ──
N.wipe_page(PAGE_ID)
print("Page wiped.")

# ── Step 3: Rebuild body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given ", {}),
        ("n", {"code": True}),
        (" nodes (labeled ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n-1", {"code": True}),
        (") and a list of ", {}),
        ("edges", {"code": True}),
        (" representing directed connections. Traversing an edge in its original direction costs ", {}),
        ("0", {"code": True}),
        (". Reversing an edge to traverse it in the opposite direction costs ", {}),
        ("1", {"code": True}),
        (". Return an array ", {}),
        ("answer", {"code": True}),
        (" of length n, where ", {}),
        ("answer[i]", {"code": True}),
        (" is the minimum cost (number of edge reversals) to travel from node ", {}),
        ("0", {"code": True}),
        (" to node ", {}),
        ("i", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: 0-1 BFS (Optimal, Interview Pick) ──
sol1_code = """\
from collections import deque

def minEdgeReversals(n, edges):
    # Build adjacency list with bidirectional edges
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))   # Original direction: free
        adj[v].append((u, 1))   # Reverse direction: costs 1 reversal

    # Initialize distances: source=0, all others=infinity
    dist = [float('inf')] * n
    dist[0] = 0
    dq = deque([0])

    while dq:
        u = dq.popleft()  # Always pop smallest-distance node
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:   # Found cheaper path to v
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)     # Free edge: push to front
                else:
                    dq.append(v)         # Cost-1 edge: push to back

    return dist
"""

sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We need the minimum number of times we have to 'flip' an edge to create a valid path from node 0 to every other node. This is just a shortest-path problem where the 'distance' to a node = minimum flips needed to reach it."),
    N.h4("What Doesn't Work"),
    N.para("Naive DFS or BFS ignores edge weights and gives wrong answers when some edges point backward. Bellman-Ford works but is O(V×E) — too slow. Dijkstra works correctly in O((V+E) log V) but is over-powered since all edge weights are only 0 or 1."),
    N.h4("The Key Observation"),
    N.para("When we model each original directed edge as two adjacency entries — (v, 0) for the free forward direction and (u, 1) for the paid reverse direction — we get a graph with only 0 and 1 edge weights. For such binary-weight graphs, a deque-based BFS (0-1 BFS) achieves O(V + E), beating Dijkstra by a log factor."),
    N.h4("Building the Solution"),
    N.para("The deque invariant: at any moment it holds nodes at distance d (front) and d+1 (back). Cost-0 edges produce neighbors at the same distance → appendleft. Cost-1 edges produce neighbors one step further → append. This ensures we always process the globally nearest node next, exactly like Dijkstra but without a heap."),
    N.callout("Analogy: Imagine a road network where some roads are one-way. You can drive any road in its legal direction for free, but you can bribe a guard $1 to drive the wrong way. 0-1 BFS finds the minimum bribe to reach every city.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — 0-1 BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("🔬 Algorithm Deep-Dive: 0-1 BFS"),
    N.para(N.rich([
        ("0-1 BFS", {"bold": True}),
        (" is a shortest-path algorithm for graphs where all edge weights are exactly 0 or 1. It uses a ", {}),
        ("deque", {"code": True}),
        (" (double-ended queue) instead of a min-heap. Neighbors reached via cost-0 edges are pushed to the ", {}),
        ("front", {"bold": True}),
        (" (same distance level); neighbors reached via cost-1 edges are pushed to the ", {}),
        ("back", {"bold": True}),
        (" (next distance level). This maintains the BFS invariant — nodes are always processed in non-decreasing distance order — in O(1) per operation, achieving O(V + E) total instead of Dijkstra's O((V+E) log V).", {}),
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("the deque holds nodes at distances d and d+1 only. When all cost-0 neighbors at level d are exhausted, the front shifts to d+1. This self-sorting property makes a heap redundant for binary weights.", {}),
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ("'minimum number of flips/changes/reversals to reach target', binary cost moves, grid with arrows where you pay 1 to change direction.", {}),
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = [[] for _ in range(n)]", {"code": True}), (" — adjacency list, one entry per node, holds (neighbor, cost) pairs.", {})])),
    N.para(N.rich([("adj[u].append((v, 0))", {"code": True}), (" — traverse original direction for free (cost 0).", {})])),
    N.para(N.rich([("adj[v].append((u, 1))", {"code": True}), (" — traverse reverse direction, pays 1 reversal (cost 1). This is the modeling trick.", {})])),
    N.para(N.rich([("dist = [float('inf')] * n; dist[0] = 0", {"code": True}), (" — all nodes start at infinite cost; source node 0 costs 0 reversals.", {})])),
    N.para(N.rich([("dq = deque([0])", {"code": True}), (" — seed the deque with the source node.", {})])),
    N.para(N.rich([("u = dq.popleft()", {"code": True}), (" — always pop from the front to process the node with the smallest current distance.", {})])),
    N.para(N.rich([("if dist[u] + w < dist[v]:", {"code": True}), (" — relaxation: only update if we found a strictly cheaper path to v.", {})])),
    N.para(N.rich([("dq.appendleft(v)", {"code": True}), (" — cost-0 edge: v is at the same BFS level, goes to the front.", {})])),
    N.para(N.rich([("dq.append(v)", {"code": True}), (" — cost-1 edge: v is one level further, goes to the back.", {})])),
    N.para(N.rich([("return dist", {"code": True}), (" — dist[i] = minimum reversals to reach node i from node 0.", {})])),
    N.divider(),
]

# ── Solution 2: Dijkstra ──
sol2_code = """\
import heapq

def minEdgeReversalsDijkstra(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))
        adj[v].append((u, 1))
    dist = [float('inf')] * n
    dist[0] = 0
    heap = [(0, 0)]   # (cost, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:   # Stale entry — cheaper path already found
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist
"""

sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Same as Solution 1 — shortest path with 0/1 edge weights. Here we use the standard Dijkstra approach as a stepping stone before the 0-1 BFS optimization."),
    N.h4("What Doesn't Work"),
    N.para("Unweighted BFS ignores edge costs entirely. We need a weighted shortest-path algorithm."),
    N.h4("The Key Observation"),
    N.para("Dijkstra with a min-heap correctly handles non-negative weights. The same two-entry adjacency list trick (forward=0, reverse=1) applies. This is the natural first solution; 0-1 BFS is the follow-up optimization."),
    N.h4("Building the Solution"),
    N.para("Use heapq to always pop the globally cheapest node. On pop, check if this is a stale entry (already found better) and skip if so. Otherwise relax all neighbors and push updated costs into the heap."),
]

blocks += [
    N.h2("Solution 2 — Dijkstra with Min-Heap"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(0, 0)]", {"code": True}), (" — min-heap stores (cost, node). heapq pops the smallest cost first.", {})])),
    N.para(N.rich([("if d > dist[u]: continue", {"code": True}), (" — stale entry guard: if we already found a cheaper path to u, skip this heap entry.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (dist[v], v))", {"code": True}), (" — push updated cost to heap. Multiple entries for same node may exist; stale ones are skipped.", {})])),
    N.callout("Dijkstra is O((V+E) log V) due to the heap operations. For binary 0/1 weights, 0-1 BFS achieves the same correctness in O(V+E). Always propose 0-1 BFS as the optimized solution in an interview.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["0-1 BFS (Optimal)", "O(V + E)", "O(V + E)"],
        ["Dijkstra", "O((V + E) log V)", "O(V + E)"],
        ["Brute-Force DFS", "O(V × E)", "O(V)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("0-1 BFS", {})])),
    N.callout(
        "When to recognize this pattern: 'minimum number of flips/reversals/changes' to traverse a graph or grid; edge weights are exactly 0 or 1; need shortest path faster than Dijkstra.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}), (" (Hard) — Grid with arrow directions; pay 1 to change arrow; classic 0-1 BFS (#1368)", {})])),
    N.bullet(N.rich([("Minimum Obstacle Removal to Reach Corner", {"bold": True}), (" (Hard) — Grid of 0s and 1s; removing an obstacle costs 1; 0-1 BFS (#2290)", {})])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium) — Standard Dijkstra for general weighted graphs; use when weights are not binary (#743)", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Modified Bellman-Ford or Dijkstra with k-hop constraint (#787)", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — BFS on unweighted grid; 0-1 BFS not needed since all costs equal (#1091)", {})])),
    N.bullet(N.rich([("Reachable Nodes In Subdivided Graph", {"bold": True}), (" (Hard) — Dijkstra on a modified graph with the same 'build a new adjacency list' modeling insight (#882)", {})])),
    N.para("These problems share the same core technique: model binary-cost traversals as a weighted graph, then apply 0-1 BFS or Dijkstra."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 17.6 (Graph → Shortest Path Algorithms). Sub-pattern: 0-1 BFS.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_cost_path_with_edge_reversals")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"PAGE_ID={PAGE_ID}")
