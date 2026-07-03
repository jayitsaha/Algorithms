"""
gen_path_with_maximum_probability.py
Regenerates the Notion page for LeetCode #1514 Path with Maximum Probability
in-place (page_id = 39193418-809c-81d4-ab71-ecfe672b9fb2).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d4-ab71-ecfe672b9fb2"
SLUG = "path_with_maximum_probability"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1514,
    pattern="Graph",
    subpatterns=["Dijkstra's (Max Product)"],
    tc="O((E+V) log V)",
    sc="O(V+E)",
    key_insight="Modified Dijkstra: maximize probability product instead of minimizing distance sum; flip to max-heap by negating values.",
    icon="🟡"
)
print("Properties set OK.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an undirected weighted graph of ", {}),
        ("n", {"code": True}),
        (" nodes (0-indexed), represented by ", {}),
        ("edges", {"code": True}),
        (" — a list of ", {}),
        ("[u, v]", {"code": True}),
        (" pairs — and a parallel list ", {}),
        ("succProb", {"code": True}),
        (" of success probabilities for each edge. Given two nodes ", {}),
        ("start_node", {"code": True}),
        (" and ", {}),
        ("end_node", {"code": True}),
        (", find the path with the maximum probability of success to go from start to end and return its success probability. If no path exists between the two nodes, return 0. Answers within 1e-5 of the actual answer will be accepted.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Dijkstra (Interview Pick) ──────────────────────────────────
SOL1_CODE = '''\
import heapq
from collections import defaultdict

def maxProbability(n, edges, succProb, start, end):
    # Build undirected adjacency list
    graph = defaultdict(list)
    for (u, v), p in zip(edges, succProb):
        graph[u].append((v, p))
        graph[v].append((u, p))

    # prob[i] = best probability found so far to reach node i
    prob = [0.0] * n
    prob[start] = 1.0  # start with certainty

    # Max-heap using negated probabilities (Python heapq is min-heap)
    heap = [(-1.0, start)]

    while heap:
        neg_p, node = heapq.heappop(heap)
        p = -neg_p  # un-negate

        # Early exit: first pop of end_node is optimal (Dijkstra invariant)
        if node == end:
            return p

        # Stale entry: a better path was already found for this node
        if p < prob[node]:
            continue

        # Relax all neighbors
        for neighbor, edge_p in graph[node]:
            new_p = p * edge_p  # probabilities multiply
            if new_p > prob[neighbor]:
                prob[neighbor] = new_p
                heapq.heappush(heap, (-new_p, neighbor))

    return 0.0  # no path found
'''

blocks += [
    N.h2("Solution 1 — Modified Dijkstra with Max-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the path in a weighted graph that maximizes the product of edge weights (probabilities). This is an optimization over all paths between two nodes in a graph — classic single-source shortest path territory."),
        N.h4("What Doesn't Work"),
        N.para("BFS ignores edge weights entirely, finding shortest hop-count paths not highest-probability paths. DFS explores paths exhaustively in O(V!) worst case with no pruning. Neither gives a polynomial-time guarantee for the optimal answer."),
        N.h4("The Key Observation"),
        N.para("Dijkstra's algorithm works for any monotone path cost: a property that extending any path can only make the cost worse (or equal). For minimum sum: adding non-negative weights only increases cost. For maximum product: multiplying by values ≤ 1.0 only decreases probability. The same greedy invariant applies — the first time we reach a node via the priority queue, we have its optimal value."),
        N.h4("Building the Solution"),
        N.para("Swap: min-heap → max-heap (negate probabilities). Swap: addition → multiplication. Swap: 'distance' initialized to infinity → 'probability' initialized to 0.0. Start with prob[start]=1.0. The rest of Dijkstra is unchanged."),
        N.callout(
            "Analogy: Imagine each edge is a gate that lets you through with probability p. The total probability of walking a path is p1 × p2 × ... × pk. You want the path where the product of gate-success rates is highest. Dijkstra always tries the most promising gate sequence next.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra's Algorithm"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Edsger W. Dijkstra, 1956. Solves single-source shortest path on weighted graphs with non-negative edge weights. Time: O((V+E) log V) with a binary heap.\n\n", {}),
        ("Core invariant: ", {"bold": True}),
        ("When a node is extracted from the priority queue, its stored value is finalized — no future path can achieve a better value. This holds because extending any path by one more edge can only make the metric worse (add ≥ 0 for sum, multiply by ≤ 1 for product).\n\n", {}),
        ("Recognize when: ", {"bold": True}),
        ("Weighted graph + optimize a single path metric (sum, product, max-bottleneck) + all weights non-negative → reach for Dijkstra. The heap structure stays the same; only the relaxation formula changes.", {}),
    ])),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(list)", {"code": True}), (" — Adjacency list mapping each node to its (neighbor, probability) pairs.", {})])),
    N.para(N.rich([("for (u, v), p in zip(edges, succProb)", {"code": True}), (" — Pair each edge [u,v] with its success probability p. Add both directions since the graph is undirected.", {})])),
    N.para(N.rich([("prob = [0.0] * n; prob[start] = 1.0", {"code": True}), (" — Initialize all probabilities to 0 (unreachable). Set start to 1.0 — we are already here with certainty.", {})])),
    N.para(N.rich([("heap = [(-1.0, start)]", {"code": True}), (" — Seed the max-heap with start node at probability 1.0 (stored as -1.0 for min-heap trick).", {})])),
    N.para(N.rich([("neg_p, node = heapq.heappop(heap); p = -neg_p", {"code": True}), (" — Pop the node with highest probability. Un-negate to get actual probability.", {})])),
    N.para(N.rich([("if node == end: return p", {"code": True}), (" — Early exit! By Dijkstra's invariant, first time we pop end_node its probability is already optimal.", {})])),
    N.para(N.rich([("if p < prob[node]: continue", {"code": True}), (" — Stale entry check. A better path to this node was found after this entry was pushed. Skip it — lazy deletion.", {})])),
    N.para(N.rich([("new_p = p * edge_p", {"code": True}), (" — Compute probability of reaching neighbor via current node. Independent events multiply.", {})])),
    N.para(N.rich([("if new_p > prob[neighbor]:", {"code": True}), (" — Only update if we found a strictly better probability. This avoids redundant heap insertions.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (-new_p, neighbor))", {"code": True}), (" — Push with negated probability for max-heap behavior.", {})])),
    N.para(N.rich([("return 0.0", {"code": True}), (" — Heap exhausted without finding end_node — no path exists between start and end.", {})])),
    N.divider(),
]

# ── Solution 2: Bellman-Ford ───────────────────────────────────────────────
SOL2_CODE = '''\
def maxProbability_bellman(n, edges, succProb, start, end):
    prob = [0.0] * n
    prob[start] = 1.0

    # Relax all edges up to n-1 times
    for _ in range(n - 1):
        updated = False
        for (u, v), p in zip(edges, succProb):
            # Try relaxing in both directions (undirected)
            if prob[u] * p > prob[v]:
                prob[v] = prob[u] * p
                updated = True
            if prob[v] * p > prob[u]:
                prob[u] = prob[v] * p
                updated = True
        if not updated:
            break  # Early exit: no changes, converged

    return prob[end]  # 0.0 if unreachable
'''

blocks += [
    N.h2("Solution 2 — Bellman-Ford Relaxation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Bellman-Ford works by repeatedly relaxing all edges. After k passes, we have the optimal probability for all paths using at most k edges. After n-1 passes, we have the globally optimal probability (the longest simple path uses at most n-1 edges)."),
        N.h4("Why This Works Here"),
        N.para("In standard Bellman-Ford for shortest path, we propagate minimum distances. Here we propagate maximum probabilities. The update rule changes from 'dist[v] = min(dist[v], dist[u] + w)' to 'prob[v] = max(prob[v], prob[u] * w)'. The convergence guarantee is identical."),
        N.h4("Trade-off vs Dijkstra"),
        N.para("Bellman-Ford is O(V*E) — slower than Dijkstra's O((V+E) log V). However it is simpler to code from memory and does not require a heap. For this problem's constraints (n, edges ≤ 10,000), Dijkstra is significantly faster."),
        N.callout("Use Bellman-Ford when: edge weights can be negative (doesn't apply here, but useful general rule), or when you need a simple implementation and performance is not critical.", "⚖️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("prob = [0.0] * n; prob[start] = 1.0", {"code": True}), (" — Same initialization as Dijkstra.", {})])),
    N.para(N.rich([("for _ in range(n - 1):", {"code": True}), (" — The longest simple path in a graph with n nodes uses at most n-1 edges. After n-1 passes all optimal paths are found.", {})])),
    N.para(N.rich([("if prob[u] * p > prob[v]:", {"code": True}), (" — Relaxation for direction u→v. Update if we found a better probability path to v through u.", {})])),
    N.para(N.rich([("if prob[v] * p > prob[u]:", {"code": True}), (" — Relaxation for direction v→u. Undirected graph requires both directions.", {})])),
    N.para(N.rich([("if not updated: break", {"code": True}), (" — Optimization: if no relaxation happened this pass, no further passes will help. Converged early.", {})])),
    N.para(N.rich([("return prob[end]", {"code": True}), (" — Returns 0.0 if end was never reachable (prob[end] stays at initial 0.0).", {})])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bellman-Ford", "O(V × E)", "O(V)"],
        ["Dijkstra (max-heap) — Interview Pick", "O((E+V) log V)", "O(V+E)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dijkstra's (Max Product) — variant of Dijkstra adapted for probability maximization via max-heap and multiplication instead of addition", {})])),
    N.callout(
        "When to recognize this pattern: Weighted undirected/directed graph + find optimal path between two nodes + all edge weights non-negative + optimize a monotone path metric (sum, product, bottleneck) → Modified Dijkstra. The key signal is 'maximize/minimize path value' with non-negative weights.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium, #743) — Classic Dijkstra: find minimum time for signal to reach all nodes. Direct application.", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium, #787) — Modified Dijkstra / Bellman-Ford with a stop-count constraint added to the state.", {})])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), (" (Hard, #778) — Dijkstra minimizing the maximum elevation encountered on a path through a 2D grid.", {})])),
    N.bullet(N.rich([("Minimum Effort Path", {"bold": True}), (" (Medium, #1631) — Dijkstra minimizing the maximum absolute difference between adjacent cells on a grid path.", {})])),
    N.bullet(N.rich([("The Maze II", {"bold": True}), (" (Medium, #505) — Dijkstra on 2D grid with rolling ball mechanics; find shortest distance path.", {})])),
    N.bullet(N.rich([("Find the City With the Smallest Number of Neighbors at a Threshold Distance", {"bold": True}), (" (Medium, #1334) — Floyd-Warshall all-pairs shortest path; different algorithm but same pattern family.", {})])),
    N.para("These problems share the core technique: weighted graph traversal with priority-queue-based greedy expansion."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section → Dijkstra sub-pattern. Sub-pattern label: Dijkstra's (Max Product). Source: Analysis.", "📚", "gray_background"),
]

# ── Visual Explainer Embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch the max-heap evolve, see probability values update in real time, and observe how the greedy invariant guarantees optimality.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
