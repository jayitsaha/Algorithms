"""
Notion regeneration for: Critical Connections in a Network (#1192, Hard)
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819c-9858-c0c06e2b3a6d"

# ── 1) Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1192,
    pattern="Graph",
    subpatterns=["Tarjan's Bridge Finding"],
    tc="O(V+E)",
    sc="O(V+E)",
    key_insight="Edge (u,v) is a bridge iff low[v] > disc[u] — the child's subtree cannot reach back to u via any back-edge.",
    icon="🔴"
)
print("Properties set OK")

# ── 2) Wipe existing body ─────────────────────────────────────────────────────
print("Wiping old body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} blocks")

# ── 3) Build body ─────────────────────────────────────────────────────────────
SOLUTION_1 = '''from collections import defaultdict

def criticalConnections(n, connections):
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    disc = [-1] * n
    low  = [-1] * n
    timer = [0]
    bridges = []

    def dfs(node, parent):
        disc[node] = low[node] = timer[0]
        timer[0] += 1
        for nei in graph[node]:
            if nei == parent:
                continue
            if disc[nei] == -1:           # tree edge
                dfs(nei, node)
                low[node] = min(low[node], low[nei])
                if low[nei] > disc[node]: # bridge condition
                    bridges.append([node, nei])
            else:                         # back edge
                low[node] = min(low[node], disc[nei])

    dfs(0, -1)
    return bridges'''

SOLUTION_2 = '''# Brute force: remove each edge, check connectivity with BFS/DFS
from collections import defaultdict, deque

def criticalConnections_brute(n, connections):
    def is_connected(skip_u, skip_v):
        adj = defaultdict(list)
        for u, v in connections:
            if (u == skip_u and v == skip_v) or (u == skip_v and v == skip_u):
                continue
            adj[u].append(v)
            adj[v].append(u)
        visited = set()
        q = deque([0])
        while q:
            node = q.popleft()
            if node in visited:
                continue
            visited.add(node)
            for nei in adj[node]:
                if nei not in visited:
                    q.append(nei)
        return len(visited) == n

    bridges = []
    for u, v in connections:
        if not is_connected(u, v):
            bridges.append([u, v])
    return bridges
# Time: O(E * (V+E)) — TLE on large inputs'''

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("n", {"code": True}),
        (" servers numbered ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n - 1", {"code": True}),
        (" connected by undirected server-to-server ", {}),
        ("connections", {"code": True}),
        (" where ", {}),
        ("connections[i] = [a, b]", {"code": True}),
        (" represents a connection between servers ", {}),
        ("a", {"code": True}),
        (" and ", {}),
        ("b", {"code": True}),
        (". Any server can reach any other server directly or indirectly through the network. A critical connection is a connection that, if removed, will make some servers unable to reach some other server. Return all critical connections in the network in any order.", {})
    ])),
    N.para("Example: n=4, connections=[[0,1],[1,2],[2,0],[1,3]] → Output: [[1,3]]"),
    N.divider(),
]

# Solution 1 — Tarjan's Bridge Finding (optimal, interview pick)
blocks += [
    N.h2("Solution 1 — Tarjan's Bridge Finding (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Which edges, if removed, would increase the number of connected components? Equivalently: which edges are NOT part of any cycle? An edge in a cycle always has an alternative path — remove it and the cycle still connects both endpoints. So we need to find edges that are the sole connection between two parts of the graph."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each edge, remove it and run BFS/DFS to check if the graph stays connected. This is O(E × (V+E)). For n=100,000 and dense graphs, this is far too slow."),
        N.h4("The Key Observation"),
        N.para("During a DFS on an undirected graph, every edge is either a tree edge (connects unvisited node) or a back edge (connects to an already-visited ancestor). An edge (u,v) is a bridge iff v's subtree in the DFS tree has NO back-edge to u or any ancestor of u. If such a back-edge existed, it would provide an alternative path, making (u,v) redundant."),
        N.h4("Building the Solution"),
        N.para("Assign each node two values: disc[v] = discovery timestamp (when first visited, never changes), and low[v] = minimum disc reachable from v's subtree via at most one back-edge. As DFS unfolds: on back-edge to ancestor a, low[v] = min(low[v], disc[a]); on returning from child w, low[v] = min(low[v], low[w]). After processing child w, if low[w] > disc[v], edge (v,w) is a bridge — child's subtree cannot reach back to v or above."),
        N.callout("Analogy: Think of disc[v] as each server's 'join time' and low[v] as 'earliest server reachable from my team via any shortcut cable (back-edge)'. If my team's best shortcut only reaches servers that joined after my boss, then my boss-to-me cable is critical.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Tarjan's Bridge Finding"),
    N.para("Tarjan's bridge-finding algorithm (Robert Tarjan, 1974) is a linear-time O(V+E) DFS algorithm for finding all bridges in an undirected graph. It uses two integer arrays (disc and low) and a global timer."),
    N.para("Core invariant: After fully processing node v, low[v] = min { disc[x] | x reachable from v's subtree via zero or more tree edges and at most one back-edge }. This means low[v] captures how 'high' (early in DFS order) v's subtree can 'see.'"),
    N.para("Why it works: A tree edge (u → v) is a bridge iff v's subtree cannot see any ancestor at or above u. 'At or above u' means disc ≤ disc[u]. If low[v] ≤ disc[u], a back-edge in v's subtree reaches u or above — alternative path exists, not a bridge. If low[v] > disc[u], no such path — bridge."),
    N.para("Recognize when: 'critical edge', 'bridge', 'single point of failure' in an undirected graph, find edges whose removal disconnects the graph."),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(list)", {"code": True}), (" — adjacency list for undirected graph.")])),
    N.para(N.rich([("for u, v in connections: graph[u].append(v); graph[v].append(u)", {"code": True}), (" — store each edge in both directions since the graph is undirected.")])),
    N.para(N.rich([("disc = [-1] * n; low = [-1] * n", {"code": True}), (" — initialize both arrays to -1 (sentinel for 'not yet visited').")])),
    N.para(N.rich([("timer = [0]", {"code": True}), (" — use a list so the inner dfs() function can mutate it (Python closure doesn't allow reassigning outer ints directly).")])),
    N.para(N.rich([("disc[node] = low[node] = timer[0]; timer[0] += 1", {"code": True}), (" — stamp discovery time. low starts equal to disc and only decreases.")])),
    N.para(N.rich([("if nei == parent: continue", {"code": True}), (" — skip the edge back to our parent. In an undirected graph, edge (u,v) is stored as both u→v and v→u. Without this, v would always see u as a 'back-edge', incorrectly lowering low[v] and hiding bridges.")])),
    N.para(N.rich([("if disc[nei] == -1:", {"code": True}), (" — tree edge: neighbor not yet visited. Recurse, then propagate low value upward.")])),
    N.para(N.rich([("low[node] = min(low[node], low[nei])", {"code": True}), (" — after child returns, pull up the lowest ancestor reachable from the child's subtree.")])),
    N.para(N.rich([("if low[nei] > disc[node]:", {"code": True}), (" — bridge condition: child's subtree cannot reach node or any ancestor of node. This tree edge is the only path — it's a bridge.")])),
    N.para(N.rich([("else: low[node] = min(low[node], disc[nei])", {"code": True}), (" — back-edge to already-visited neighbor. Update low with disc[nei] (NOT low[nei] — see warning below).")])),
    N.callout("⚠️ Critical bug: on back-edges, always use disc[nei], NOT low[nei]. Using low[nei] can propagate stale low values incorrectly across back-edges, causing false bridges.", "⚠️", "yellow_background"),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force (Remove + BFS)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Direct interpretation: 'critical connection' = removing it disconnects the graph. So try removing each edge and check if the graph is still connected."),
        N.h4("What Doesn't Work"),
        N.para("This works correctly but is too slow. For each of E edges, we rebuild the adjacency list (O(E)) and run a full BFS/DFS (O(V+E)). Total: O(E × (V+E)). For typical constraints n,E up to 100,000 this is ~10^10 operations — Time Limit Exceeded."),
        N.h4("The Key Observation"),
        N.para("The brute force is correct but wasteful: we're re-examining the entire graph for every single edge. Tarjan's algorithm amortizes this work into a single O(V+E) DFS pass."),
        N.h4("Building the Solution"),
        N.para("For each edge (u,v): remove it from the graph, BFS from node 0, check if all n nodes are reachable. If not, (u,v) is a bridge."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("is_connected(skip_u, skip_v)", {"code": True}), (" — helper: rebuild adjacency list excluding edge (skip_u, skip_v), then BFS from 0 to count reachable nodes.")])),
    N.para(N.rich([("if len(visited) == n:", {"code": True}), (" — all n nodes reachable → still connected → not a bridge.")])),
    N.para(N.rich([("for u, v in connections: if not is_connected(u, v):", {"code": True}), (" — try removing each edge; if graph disconnects, it's a bridge.")])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (remove + BFS per edge)", "O(E × (V+E))", "O(V+E)"],
        ["Tarjan's Bridge Finding (Interview Pick)", "O(V+E)", "O(V+E)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (DFS-based, bridge detection)")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Tarjan's Bridge Finding (disc/low timestamps in undirected DFS)")])),
    N.callout(
        "When to recognize this pattern: 'critical edge', 'single point of failure', 'bridge', or 'edge whose removal disconnects the graph' in an undirected connected graph. Also watch for related: Articulation Points (same algorithm, finds critical nodes instead of critical edges).",
        "🔎", "green_background"
    ),
    N.para("Note: Tarjan's Bridge Finding is a named classic sub-pattern in competitive programming and graph theory. It generalizes to Tarjan's SCC algorithm for directed graphs using a similar disc/low approach with an explicit stack."),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Articulation Points / Critical Nodes", {"bold": True}), (" (Hard) — same Tarjan DFS, condition: low[child] >= disc[node] for non-root nodes.")])),
    N.bullet(N.rich([("Number of Connected Components in Undirected Graph", {"bold": True}), (" (Medium) — foundational DFS/Union-Find; knowing connected components is prerequisite to reasoning about bridges.")])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium) — find an edge that IS in a cycle (opposite: bridges are edges NOT in any cycle). Use Union-Find.")])),
    N.bullet(N.rich([("Graph Valid Tree", {"bold": True}), (" (Medium) — verify graph has no cycles (n-1 edges, fully connected). Cycle detection underlies bridge thinking.")])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), (" (Medium) — topological sort via DFS with state tracking (white/gray/black); shares DFS timestamp mental model.")])),
    N.bullet(N.rich([("Minimum Number of Days to Disconnect Island", {"bold": True}), (" (Hard) — bridge-like reasoning on grid graphs; finding minimal edge cuts.")])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), (" (Medium) — DFS path enumeration in DAG; good warmup for graph DFS before bridge problems.")])),
    N.para("These problems all involve DFS-based graph analysis. Tarjan's bridge-finding is the most advanced single-pass technique — master it and articulation points come free."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, Tarjan's Bridge Finding sub-pattern.", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("critical_connections_in_a_network")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
