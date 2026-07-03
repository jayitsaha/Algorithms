"""
Notion update script for: Is Graph Bipartite? (LeetCode #785)
Runs in-place on the existing page: 39193418-809c-819a-a8c9-f35ae8914424
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-819a-a8c9-f35ae8914424"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=785,
    pattern="Graph",
    subpatterns=["DFS 2-Coloring"],
    tc="O(V + E)",
    sc="O(V)",
    key_insight="Assign alternating colors via DFS; a same-color neighbor proves an odd cycle exists.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is an undirected graph with ", {}),
        ("n", {"code": True}),
        (" nodes, where each node is numbered between ", {}),
        ("0", {"code": True}),
        (" and ", {}),
        ("n - 1", {"code": True}),
        (". You are given a 2D array ", {}),
        ("graph", {"code": True}),
        (", where ", {}),
        ("graph[u]", {"code": True}),
        (" is an array of nodes that node ", {}),
        ("u", {"code": True}),
        (" is adjacent to. Return ", {}),
        ("true", {"code": True}),
        (" if and only if the graph is bipartite — i.e., its nodes can be split into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — DFS 2-Coloring ───────────────────────────────────────────
dfs_code = """\
def isBipartite(graph):
    n = len(graph)
    color = [-1] * n         # -1 = unvisited, 0 = Group A, 1 = Group B

    def dfs(node, c):
        color[node] = c      # Assign this color to the current node
        for nei in graph[node]:
            if color[nei] == c:      # Same color as us → odd cycle!
                return False
            if color[nei] == -1:     # Unvisited → assign opposite color
                if not dfs(nei, 1 - c):
                    return False
        return True

    for i in range(n):
        if color[i] == -1:           # Handle disconnected components
            if not dfs(i, 0):
                return False
    return True
"""

blocks += [
    N.h2("Solution 1 — DFS 2-Coloring (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Bipartite means: can we paint every node red or blue such that no two adjacent nodes share a color? This is a graph 2-coloring problem. The key constraint is that neighbors must always differ in color — which is a constraint propagation problem, perfect for DFS."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach would try all 2^n colorings and check each — that's exponential. Sorting or hashing nodes doesn't help because bipartiteness depends on graph structure, not node values."),
        N.h4("The Key Observation"),
        N.para("Once you pick a color for any node, all reachable nodes' colors are completely determined — neighbors get the opposite color, their neighbors get back to the original, and so on. There are no choices once you start. This means DFS can propagate colors automatically, and we just need to detect contradictions."),
        N.h4("Building the Solution"),
        N.para("1. Initialize color[-1, -1, ..., -1] (all unvisited). 2. For each unvisited node, call dfs(node, 0). 3. In DFS: assign color c, then for each neighbor — if same color → return False; if unvisited → recurse with color 1-c. 4. Repeat for all components (critical: disconnected graphs need this outer loop!)."),
        N.callout(
            "Analogy: Think of it as a party seating problem. You're seating guests at two tables (A and B). Every pair who 'dislike each other' (are connected) must sit at different tables. Start seating anyone at Table A, then force all their 'disliked' guests to Table B, then force THEIR disliked guests to Table A — if you ever have to seat someone at a table where a 'disliked' person already sits, the seating is impossible.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(dfs_code),
    N.h3("Line by Line"),
    N.para(N.rich([("color = [-1] * n", {"code": True}), (" — Initialize all nodes as unvisited (-1). We'll use 0 for Group A and 1 for Group B.", {})])),
    N.para(N.rich([("def dfs(node, c)", {"code": True}), (" — Helper that tries to color 'node' with color 'c' and propagates to its neighbors.", {})])),
    N.para(N.rich([("color[node] = c", {"code": True}), (" — Mark this node with the assigned color before exploring its neighbors.", {})])),
    N.para(N.rich([("if color[nei] == c: return False", {"code": True}), (" — A neighbor already has the same color as us → we've found an odd cycle → not bipartite.", {})])),
    N.para(N.rich([("if color[nei] == -1: if not dfs(nei, 1 - c)", {"code": True}), (" — Neighbor is unvisited: assign the opposite color (1-0=1, 1-1=0) and recurse. Propagate failure upward.", {})])),
    N.para(N.rich([("for i in range(n): if color[i] == -1", {"code": True}), (" — Outer loop handles disconnected components. We must start DFS from every unvisited node, not just node 0.", {})])),
    N.para(N.rich([("return True", {"code": True}), (" — All components successfully 2-colored without conflict → graph is bipartite.", {})])),
    N.divider(),
]

# ── Solution 2 — BFS 2-Coloring ───────────────────────────────────────────
bfs_code = """\
from collections import deque

def isBipartite(graph):
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue                      # Already visited
        color[start] = 0                  # Seed this component
        q = deque([start])
        while q:
            u = q.popleft()               # Process next node
            for v in graph[u]:
                if color[v] == -1:        # Unvisited → color opposite
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]: # Same color → conflict
                    return False
    return True
"""

blocks += [
    N.h2("Solution 2 — BFS 2-Coloring (Iterative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal as DFS, but BFS processes nodes level by level. Each BFS 'level' naturally corresponds to alternating colors: level 0 = color 0, level 1 = color 1, level 2 = color 0, etc. This makes BFS very intuitive for 2-coloring."),
        N.h4("What Doesn't Work"),
        N.para("DFS can hit Python's recursion limit on large, deep graphs. BFS using a deque is fully iterative and avoids this limitation — important for production code or when n can be very large."),
        N.h4("The Key Observation"),
        N.para("In BFS, when you dequeue node u and examine its neighbor v: if v is unvisited, you assign it the opposite color of u. If v is already colored the same as u, there's a conflict. The BFS order ensures every node is processed once, and every edge is checked once."),
        N.h4("Building the Solution"),
        N.para("For each unvisited node: seed it with color 0 and add to queue. In the BFS loop: dequeue u, for each neighbor v — if unvisited, color it 1-color[u] and enqueue; if same color as u → return False. Handle all components with the outer for loop."),
    ]),
    N.h3("Code"),
    N.code(bfs_code),
    N.h3("Line by Line"),
    N.para(N.rich([("color[start] = 0; q = deque([start])", {"code": True}), (" — Seed the component: assign color 0 to the starting node and begin BFS from it.", {})])),
    N.para(N.rich([("u = q.popleft()", {"code": True}), (" — Process the node at the front of the BFS queue.", {})])),
    N.para(N.rich([("if color[v] == -1:", {"code": True}), (" — Unvisited neighbor: assign opposite color (1 - color[u]) and enqueue for later processing.", {})])),
    N.para(N.rich([("elif color[v] == color[u]: return False", {"code": True}), (" — Already-visited neighbor with the same color: odd cycle found, not bipartite.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS 2-Coloring", "O(V + E)", "O(V)", "Recursive; visits each node and edge once"],
        ["BFS 2-Coloring", "O(V + E)", "O(V)", "Iterative; safer for large inputs"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — DFS/BFS traversal for structural property detection", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS 2-Coloring (Bipartite check) — verified from DSA_Patterns_and_SubPatterns_Guide.md Section 8 (Graph), Bipartite sub-pattern", {})])),
    N.callout(
        "When to recognize this pattern: 'Can we divide nodes into two groups?' / 'Can we 2-color this graph?' / 'Does this graph contain an odd cycle?' / Graph where edges represent conflicts or opposition between pairs of nodes.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Algorithm Deep-Dive: ", {"bold": True}),
        ("DFS 2-Coloring is a special case of graph k-coloring where k=2. For k=2, the problem is solvable in O(V+E) polynomial time by propagating colors greedily. For k≥3 (general graph coloring), the problem is NP-complete. The correctness follows from the König-Egerváry theorem: a graph is bipartite iff it has no odd-length cycle.", {})
    ])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS/BFS 2-coloring or graph traversal technique:"),
    N.bullet(N.rich([("Possible Bipartition", {"bold": True}), (" (Medium, LC 886) — Build graph from 'dislikes' pairs, then check bipartite. Identical algorithm; builds the graph from input pairs first.", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium, LC 200) — DFS/BFS graph traversal to count connected components. Same exploration pattern without the coloring.", {})])),
    N.bullet(N.rich([("Course Schedule", {"bold": True}), (" (Medium, LC 207) — DFS cycle detection in directed graph. Related: uses DFS to detect structural impossibility.", {})])),
    N.bullet(N.rich([("Graph Valid Tree", {"bold": True}), (" (Medium, LC 261) — Check if graph is a valid tree (connected + no cycles). DFS traversal with cycle detection.", {})])),
    N.bullet(N.rich([("Number of Connected Components", {"bold": True}), (" (Medium, LC 323) — Count components using DFS/BFS. Same 'iterate over all unvisited nodes' outer loop pattern.", {})])),
    N.bullet(N.rich([("Find if Path Exists in Graph", {"bold": True}), (" (Easy, LC 1971) — Basic BFS/DFS reachability. Good warm-up before bipartite check.", {})])),
    N.bullet(N.rich([("All Paths from Source to Target", {"bold": True}), (" (Medium, LC 797) — DFS backtracking on DAG. Builds graph DFS traversal intuition.", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium, LC 684) — Find the extra edge in a cycle. Related via Union-Find (alternative to DFS 2-coloring for some graph problems).", {})])),
    N.para("These problems all share the same core technique: systematic DFS/BFS traversal that propagates a property (color, visited, parent) and detects violations."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 8 (Graph Traversal), DFS 2-Coloring / Bipartite sub-pattern", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("is_graph_bipartite")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
