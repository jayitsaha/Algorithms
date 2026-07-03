"""
gen_graph_valid_tree.py — Notion update for Graph Valid Tree (#261)
Run from the Algorithms directory alongside notion_lib.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-814f-a8bc-df9070830cdb"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=261,
    pattern="Graph",
    subpatterns=["n-1 Edges + No Cycle"],
    tc="O(n · α(n))",
    sc="O(n)",
    key_insight="Tree iff len(edges)==n-1 AND no cycle; Union-Find detects cycle when find(u)==find(v).",
    icon="🟡"
)
print("Properties set ✓")

# ── 2) Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks ✓")

# ── 3) Build body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have ", {}),
        ("n", {"code": True}),
        (" nodes labeled ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n-1", {"code": True}),
        (" and a list of undirected ", {}),
        ("edges", {"code": True}),
        (". Return ", {}),
        ("true", {"code": True}),
        (" if these edges make a valid tree — a connected acyclic undirected graph with exactly n nodes.", {}),
    ])),
    N.para("Constraints: 1 ≤ n ≤ 2000, 0 ≤ edges.length ≤ 5000, edges[i] has exactly 2 nodes, no self-loops, no repeated edges."),
    N.divider(),
]

# Solution 1 — Union-Find
sol1_code = '''def validTree(n: int, edges: list) -> bool:
    if len(edges) != n - 1:          # n-1 edge check: O(1) early exit
        return False
    parent = list(range(n))           # parent[i]=i: each node is its own root
    rank = [0] * n                    # rank[i]=0: used for union-by-rank

    def find(x):                      # Find root with path compression
        if parent[x] != x:
            parent[x] = find(parent[x])   # Compress: point x directly to root
        return parent[x]

    def union(x, y) -> bool:          # Returns False if cycle detected
        rx, ry = find(x), find(y)     # Find roots of both nodes
        if rx == ry:                  # Same root = same component = CYCLE!
            return False
        if rank[rx] < rank[ry]:       # Attach smaller tree under larger
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:                         # Equal rank: pick one, bump its rank
            parent[ry] = rx
            rank[rx] += 1
        return True

    return all(union(u, v) for u, v in edges)  # Process all; any False = cycle'''

blocks += [
    N.h2("Solution 1 — Union-Find (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A valid tree is a connected acyclic undirected graph. We need to verify two conditions: (1) all nodes can reach each other, and (2) no cycles exist. The key mathematical shortcut: an undirected graph on n nodes is a tree iff it has exactly n−1 edges AND is connected — and these two facts together with no-cycle are equivalent."),
        N.h4("What Doesn't Work"),
        N.para("Naive DFS cycle detection for each edge is O(n) per edge = O(n²) total. Building a full adjacency list and doing BFS works in O(n) but requires O(n) setup. We want something that detects cycles incrementally as we process each edge."),
        N.h4("The Key Observation"),
        N.para("If we maintain groups (components) of already-connected nodes, adding edge (u,v) creates a cycle if and only if u and v are already in the same group. Union-Find maintains these groups in near-O(1) per operation. We also know the graph must have exactly n-1 edges to be a tree — check that first."),
        N.h4("Building the Solution"),
        N.para("1. Check len(edges)==n-1 (O(1)). 2. Initialize Union-Find: parent[i]=i. 3. For each edge (u,v): find roots. Same root → cycle → return False. Different roots → union (merge sets). 4. If all edges processed without cycle → return True."),
        N.callout("Analogy: Think of it like social groups. Union-Find tracks which group each person belongs to. Adding a friendship between two people from different groups merges them. Adding a friendship between two people already in the same group is redundant and creates a social 'cycle'. We're just checking if any redundant connection exists.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find (Disjoint Set Union)"),
    N.para("Origin: Tarjan (1975). Solves the dynamic connectivity problem — efficiently tracks which components nodes belong to as edges are added online (one at a time)."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("All nodes with the same root are in the same connected component. find(x) returns the canonical representative (root) of x's component in near O(1) with path compression.", {}),
    ])),
    N.para(N.rich([
        ("Path compression: ", {"bold": True}),
        ("When find(x) traverses the ancestor chain to reach the root, it sets parent[x] = root for every node on the path. Future find calls on these nodes take O(1).", {}),
    ])),
    N.para(N.rich([
        ("Union by rank: ", {"bold": True}),
        ("Always attach the root of the shallower tree under the root of the deeper tree. This prevents degenerate O(n) chains and keeps tree height at O(log n) before compression.", {}),
    ])),
    N.para(N.rich([
        ("Combined complexity: ", {"bold": True}),
        ("O(α(n)) amortized per operation — inverse Ackermann function, ≤4 for any n that fits in the universe. Practically O(1).", {}),
    ])),
    N.code('''def find(x):
    """Find root with path compression."""
    if parent[x] != x:
        parent[x] = find(parent[x])  # Point x directly to root
    return parent[x]

def union(x, y):
    """Merge sets; returns False if cycle (same root)."""
    rx, ry = find(x), find(y)
    if rx == ry: return False        # Same component = cycle
    if rank[rx] < rank[ry]: parent[rx] = ry
    elif rank[rx] > rank[ry]: parent[ry] = rx
    else: parent[ry] = rx; rank[rx] += 1
    return True'''),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(edges) != n - 1:", {"code": True}), (" — O(1) early exit. A tree on n nodes must have exactly n-1 edges. This single check eliminates disconnected graphs (too few edges) and graphs with cycles (too many edges).", {})])),
    N.para(N.rich([("parent = list(range(n))", {"code": True}), (" — Initialize: each node i has parent[i]=i, meaning each node is its own root = n separate isolated components.", {})])),
    N.para(N.rich([("rank = [0] * n", {"code": True}), (" — All trees start at height 0. Used by union-by-rank to keep the Union-Find tree shallow.", {})])),
    N.para(N.rich([("if parent[x] != x:", {"code": True}), (" — x is not its own root, meaning it has an ancestor. We need to recurse upward to find the true root.", {})])),
    N.para(N.rich([("parent[x] = find(parent[x])", {"code": True}), (" — Path compression: after finding the root, make x point directly to it. All intermediate nodes also get compressed on the recursive unwind.", {})])),
    N.para(N.rich([("rx, ry = find(x), find(y)", {"code": True}), (" — Find the canonical representative of each node's component. Both calls benefit from path compression.", {})])),
    N.para(N.rich([("if rx == ry: return False", {"code": True}), (" — Same root = same component = adding this edge creates a cycle. This is the cycle detection condition.", {})])),
    N.para(N.rich([("if rank[rx] < rank[ry]: parent[rx] = ry", {"code": True}), (" — Union by rank: attach smaller-rank tree under larger-rank tree to keep tree height minimal.", {})])),
    N.para(N.rich([("else: parent[ry] = rx; rank[rx] += 1", {"code": True}), (" — Equal ranks: arbitrary choice (rx as new root), then bump rx's rank since the merged tree is now one level taller.", {})])),
    N.para(N.rich([("return all(union(u, v) for u, v in edges)", {"code": True}), (" — Process all edges. Python's all() short-circuits on first False (first cycle detected), returning False immediately.", {})])),
    N.divider(),
]

# Solution 2 — BFS
sol2_code = '''from collections import defaultdict, deque

def validTree(n: int, edges: list) -> bool:
    if len(edges) != n - 1:
        return False                         # Same O(1) edge count guard

    adj = defaultdict(list)                  # Build adjacency list (undirected)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = {0}                            # BFS from node 0
    queue = deque([0])

    while queue:
        node = queue.popleft()
        for nei in adj[node]:
            if nei not in visited:           # Only visit new nodes
                visited.add(nei)
                queue.append(nei)

    return len(visited) == n                 # All n nodes reachable = connected'''

blocks += [
    N.h2("Solution 2 — BFS (Conceptually Transparent)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Since we already check n-1 edges (which guarantees acyclicity is the only remaining concern), we just need to verify connectivity. BFS from any node: if it visits all n nodes, the graph is connected. With n-1 edges and full connectivity, no cycle can exist."),
        N.h4("What Doesn't Work"),
        N.para("Pure cycle detection via DFS with parent tracking needs O(n + e) and is correct, but adds complexity because you must track the parent to avoid false cycle detection on undirected edges. BFS avoids this by only marking unvisited nodes."),
        N.h4("The Key Observation"),
        N.para("After the n-1 edge count check, we only need to confirm that all nodes are reachable from any starting node. BFS from node 0 and count visited nodes is the simplest implementation of this check."),
        N.h4("Building the Solution"),
        N.para("1. Check len(edges)==n-1. 2. Build adjacency list (both directions for undirected). 3. BFS from node 0, marking visited nodes. 4. If len(visited)==n after BFS, all nodes reached = connected = valid tree."),
        N.callout("When to prefer BFS: If you're more comfortable with BFS than Union-Find, or if an interviewer wants to see a graph traversal approach. Union-Find is more elegant and teaches a fundamental data structure. Both are acceptable.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = defaultdict(list)", {"code": True}), (" — Build the undirected graph as an adjacency list. Each edge (u,v) is stored as v in adj[u] and u in adj[v].", {})])),
    N.para(N.rich([("visited = {0}", {"code": True}), (" — Start BFS from node 0. Mark it visited before enqueuing to prevent duplicate processing.", {})])),
    N.para(N.rich([("if nei not in visited:", {"code": True}), (" — Only add unvisited neighbors to the queue. For undirected graphs, the reverse edge (parent) would be in adj[node] too, so this check prevents us from going back.", {})])),
    N.para(N.rich([("return len(visited) == n", {"code": True}), (" — If all n nodes were reachable from node 0 (via the n-1 edges), the graph is connected. Combined with no-cycle (guaranteed by n-1 edges + connectivity theorem), this is a valid tree.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Union-Find (Interview Pick)", "O(n · α(n)) ≈ O(n)", "O(n)"],
        ["BFS", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — specifically the problem of determining if a set of edges forms a valid spanning tree.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("n-1 Edges + No Cycle — the canonical signature for a valid tree. Uses Union-Find for cycle detection.", {})])),
    N.para(N.rich([("Algorithm: ", {"bold": True}), ("Union-Find (Disjoint Set Union) with path compression and union by rank — O(α(n)) ≈ O(1) amortized per operation.", {})])),
    N.callout("When to recognize this pattern:\n• Problem asks to validate whether edges form a tree or forest\n• Detect cycle in an undirected graph\n• Count connected components dynamically\n• Merge groups/clusters as connections are added\n• 'Can we connect all nodes with given edges?' (spanning tree variant)\nKey signal: n nodes + edge list + connectivity/cycle question = Union-Find territory.", "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same n-1 Edges + No Cycle technique or Union-Find:"),
    N.bullet(N.rich([("Number of Connected Components in an Undirected Graph", {"bold": True}), (" (Medium) — Count distinct roots remaining after all unions. (#323)", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium) — Return the first edge whose union() returns False (the cycle-forming edge). (#684)", {})])),
    N.bullet(N.rich([("Redundant Connection II", {"bold": True}), (" (Hard) — Directed graph variant with more complex cycle + in-degree invariants. (#685)", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Grid connected components via DFS or Union-Find on 2D cells. (#200)", {})])),
    N.bullet(N.rich([("Accounts Merge", {"bold": True}), (" (Medium) — Group accounts sharing emails using Union-Find keyed on email strings. (#721)", {})])),
    N.bullet(N.rich([("Most Stones Removed with Same Row or Column", {"bold": True}), (" (Medium) — Union-Find on row/column identifiers to count connected stone groups. (#947)", {})])),
    N.bullet(N.rich([("Minimum Spanning Tree (Kruskal's algorithm)", {"bold": True}), (" — Union-Find is the core data structure of Kruskal's MST: sort edges by weight, add non-cycle-forming ones greedily.", {})])),
    N.para("These problems share the same core technique: Union-Find for dynamic component tracking and cycle detection in undirected graphs."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph Algorithms), Sub-Pattern: n-1 Edges + No Cycle, line 881.", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("graph_valid_tree")),
    N.para(N.rich([("Step through the Union-Find algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
