"""
gen_clone_graph.py — Notion update for Clone Graph (#133)
Run from the Algorithms/ directory: python3 gen_clone_graph.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8196-b2de-ec082b799f65"

# ── 1. Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=133,
    pattern="Graph",
    subpatterns=["DFS + Hash Map Clone"],
    tc="O(V+E)",
    sc="O(V)",
    key_insight="Register clone in visited map BEFORE recursing — this breaks cycles and ensures one clone per node.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a reference to a node in a connected undirected graph, return a "),
        ("deep copy", {"bold": True}),
        (" (clone) of the graph. Each node contains an integer "),
        ("val", {"code": True}),
        (" and a list "),
        ("neighbors", {"code": True}),
        (" of its adjacent nodes. The graph is represented as an adjacency list. "
         "Return the clone of the given node as a reference to the cloned graph.")
    ])),
    N.divider(),
]

# ── Solution 1: DFS + Hash Map ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — DFS + Hash Map Clone (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to visit every node in the graph exactly once (to create its clone), then wire up all the connections between clones exactly as they exist in the original. That's a graph traversal (DFS or BFS) plus a mapping from old nodes to new nodes."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion without tracking fails on cycles. In an undirected graph, node A's neighbor list contains node B, and node B's neighbor list contains node A. Without a visited check, cloning A recurses into B, which recurses into A again — infinite loop. We need to detect 'already cloned this node' before descending."),
        N.h4("The Key Observation"),
        N.para("A hash map from original_node → clone_node solves two problems at once: (1) it acts as a visited set to stop re-processing, and (2) it stores the clone objects so we can reconnect them as neighbors. When we encounter a node that's already in the map, we return its existing clone — no new object created."),
        N.h4("Building the Solution"),
        N.para("The trick is the ordering: create the clone, register it in the map, THEN recurse into neighbors. If you recurse first (before registering), a cycle back to the current node won't find it in the map and will create a duplicate. Always: create → register → recurse."),
        N.callout("Analogy: think of photocopying a web of connected documents. Before copying a document's links, you stamp it 'COPIED' and file the copy. When you encounter a link to an already-stamped document, you just attach the existing photocopy instead of copying again.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def cloneGraph(node):\n"
        "    if not node:\n"
        "        return None\n"
        "    visited = {}  # original_node -> clone_node\n"
        "    def dfs(n):\n"
        "        if n in visited:\n"
        "            return visited[n]  # Already cloned; return existing\n"
        "        clone = Node(n.val)   # Create clone with same value\n"
        "        visited[n] = clone    # REGISTER BEFORE recursing (cycle-breaker)\n"
        "        for nb in n.neighbors:\n"
        "            clone.neighbors.append(dfs(nb))  # Recurse; append clone\n"
        "        return clone\n"
        "    return dfs(node)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not node: return None", {"code": True}), " — Guard for the empty/null graph input."])),
    N.para(N.rich([("visited = {}", {"code": True}), " — Hash map: original node object → its clone. Serves as visited set AND clone registry."])),
    N.para(N.rich([("if n in visited: return visited[n]", {"code": True}), " — If we've already created a clone for n, return it immediately. Prevents infinite recursion on cycles."])),
    N.para(N.rich([("clone = Node(n.val)", {"code": True}), " — Create a new node with the same integer value. neighbors list starts empty."])),
    N.para(N.rich([("visited[n] = clone", {"code": True}), " — Register the clone BEFORE the neighbor loop. If any cycle brings DFS back to n, it will find this entry and return the clone instead of re-creating."])),
    N.para(N.rich([("for nb in n.neighbors: clone.neighbors.append(dfs(nb))", {"code": True}), " — For each original neighbor, recursively get its clone (fresh or cached) and link it to the current node's clone."])),
    N.para(N.rich([("return clone", {"code": True}), " — Return the fully-linked clone of this node up the call stack."])),
    N.para(N.rich([("return dfs(node)", {"code": True}), " — Start DFS from the given entry node; returns the clone of that node as the entry to the copied graph."])),
    N.divider(),
]

# ── Solution 2: BFS + Hash Map ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — BFS + Hash Map (Iterative, No Stack Overflow Risk)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal as DFS, but we process nodes level-by-level using a queue instead of depth-first using the call stack. The hash map plays the same dual role."),
        N.h4("What Doesn't Work"),
        N.para("For very large graphs (V close to Python's default recursion limit of ~1000), the DFS solution will crash with RecursionError. BFS eliminates this risk by using an explicit deque instead of the call stack."),
        N.h4("The Key Observation"),
        N.para("In BFS, we pre-clone nodes as soon as we discover them (first time they appear as a neighbor), then add them to the queue for later expansion. The neighbor wiring happens during expansion — after both endpoints exist in the map."),
        N.h4("Building the Solution"),
        N.para("Seed: pre-clone the starting node and put it in both visited and the queue. Each iteration: pop curr, iterate its neighbors. For unseen neighbors: create clone + enqueue. For all neighbors (seen or new): append their clone to curr's clone neighbors."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def cloneGraph(node):\n"
        "    if not node:\n"
        "        return None\n"
        "    visited = {node: Node(node.val)}  # Pre-clone start; seed map\n"
        "    queue = deque([node])             # BFS queue of original nodes\n"
        "    while queue:\n"
        "        curr = queue.popleft()        # Process next original node\n"
        "        for nb in curr.neighbors:     # For each original neighbor\n"
        "            if nb not in visited:     # First time? Create clone + enqueue\n"
        "                visited[nb] = Node(nb.val)\n"
        "                queue.append(nb)\n"
        "            visited[curr].neighbors.append(visited[nb])  # Wire clone\n"
        "    return visited[node]             # Return clone of starting node"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = {node: Node(node.val)}", {"code": True}), " — Pre-register the starting node's clone. This seeds both the visited map and covers the single-node edge case."])),
    N.para(N.rich([("queue = deque([node])", {"code": True}), " — BFS queue starts with the original starting node (not the clone — we traverse original graph, build clone graph)."])),
    N.para(N.rich([("if nb not in visited: visited[nb] = Node(nb.val); queue.append(nb)", {"code": True}), " — First time seeing a neighbor: create its clone and schedule it for expansion."])),
    N.para(N.rich([("visited[curr].neighbors.append(visited[nb])", {"code": True}), " — Always wire the edge in the clone, whether nb was new or already existed. This runs outside the 'if not in visited' block."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursion (no map)", "∞ (infinite loop on cycles)", "∞"],
        ["DFS + Hash Map (Interview Pick)", "O(V+E)", "O(V)"],
        ["BFS + Hash Map (Iterative)", "O(V+E)", "O(V)"],
    ]),
    N.para("V = number of nodes, E = number of edges. Both approaches visit each node once and each edge twice (from both endpoints in undirected graph). The hash map stores V entries."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS + Hash Map Clone"])),
    N.callout(
        "When to recognize this pattern: 'deep copy' a graph or any structure with cyclic references; "
        "node objects that reference other node objects; need to visit every node once AND reconstruct connections; "
        "'return a clone of the graph' — classic formulation.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS/BFS + Hash Map on graphs or cyclic structures):"),
    N.bullet(N.rich([("Copy List with Random Pointer", {"bold": True}), " (Medium) — Linked list deep copy with back-pointers; identical hash map pattern (#138)"])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), " (Medium) — DFS flood-fill on implicit grid graph; visited array as hash map substitute (#200)"])),
    N.bullet(N.rich([("Course Schedule", {"bold": True}), " (Medium) — DFS cycle detection on directed graph; colored visited states (#207)"])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium) — DFS backtracking on DAG; collect all paths from 0 to n-1 (#797)"])),
    N.bullet(N.rich([("Find if Path Exists in Graph", {"bold": True}), " (Easy) — BFS/DFS with visited set for reachability check (#1971)"])),
    N.bullet(N.rich([("Reconstruct Itinerary", {"bold": True}), " (Hard) — DFS Eulerian path with adjacency map via Hierholzer's algorithm (#332)"])),
    N.para("These problems share the core pattern: graph traversal where you need to track visited nodes AND store per-node data (clone, path, color) — the hash map is the structural solution."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Graph) | Sub-Pattern: DFS + Hash Map Clone | Source: Analysis", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ───────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("clone_graph")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the DFS call stack, the hash map being populated, and graph nodes transition "
         "from unvisited → active → cloned → done.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print("NOTION OK", PAGE_ID)
