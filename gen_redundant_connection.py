"""gen_redundant_connection.py — Notion update for Redundant Connection (LC #684)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81af-a05f-d2d000632de9"

# ── Step 1: Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=684,
    pattern="Graph",
    subpatterns=["Union-Find (Cycle Detection)"],
    tc="O(n·α(n))",
    sc="O(n)",
    key_insight="Process edges in order with Union-Find; the first edge where find(u)==find(v) (same root = already connected) creates a cycle — return it immediately.",
    icon="🟡"
)
print("Properties set OK.")

# ── Step 2: Wipe existing body ──
print("Wiping old blocks...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} blocks.")

# ── Step 3: Build body blocks ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("In an undirected graph that originally formed a tree with ", {}),
        ("n", {"code": True}),
        (" nodes (labeled 1 to n), one extra edge was added, creating exactly one cycle. ", {}),
        ("Return the redundant edge that forms the cycle. ", {}),
        ("If multiple edges qualify, return the one that appears last in the input. ", {}),
        ("Constraints: n nodes, n edges (one extra vs. a tree's n-1). ", {}),
        ("Nodes are 1-indexed. The input is guaranteed to have exactly one extra edge.", {})
    ])),
    N.divider(),
]

# Solution 1 — Union-Find (Interview Pick)
blocks += [
    N.h2("Solution 1 — Union-Find with Path Compression + Union by Rank (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're adding edges one by one. A tree never has a cycle. The first edge that connects two nodes already in the same component (already path-connected) is the one that closes the cycle. We just need a fast way to ask: 'Are u and v already connected?' after each edge addition."),
        N.h4("What Doesn't Work"),
        N.para("DFS per edge: for each edge [u,v], run a full DFS to check if v is reachable from u in the current graph. This is O(n) per edge × n edges = O(n²). Correct but too slow for large n."),
        N.h4("The Key Observation"),
        N.para("We need 'are u and v connected?' answered in nearly O(1) per query, with the ability to dynamically merge components as we add edges. This is exactly the Union-Find (Disjoint Set Union) data structure. find(x) returns the root representative of x's component. If find(u) == find(v) before union — they're already connected — this edge is redundant."),
        N.h4("Building the Solution"),
        N.para("1. Initialize parent[i]=i — every node is its own component. 2. For each edge [u,v]: compute find(u) and find(v) with path compression. 3. If roots match, return [u,v] immediately. 4. Otherwise, union the two components (attach smaller-rank root under larger) and continue. The first cycle-closing edge is the answer."),
        N.callout("Analogy: Think of each component as a country. 'find' looks up which country a node belongs to. 'union' merges two countries. When we try to connect two nodes already in the same country, we've found the redundant border — return it.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find (DSU)"),
    N.para(N.rich([
        ("Union-Find ", {"bold": True}),
        ("(Disjoint Set Union) was formalized by Galler & Fischer (1964) and optimized by Tarjan (1975). It maintains a partition of a set into disjoint subsets (connected components). Two operations: ", {}),
        ("find(x)", {"code": True}),
        (" — returns the root representative of x's component; ", {}),
        ("union(x,y)", {"code": True}),
        (" — merges x's and y's components. With path compression + union by rank, both operations run in amortized O(α(n)) — the inverse Ackermann function, effectively constant (≤ 4) for any practical input.", {})
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("parent[] encodes a forest of trees, one per component. The root of each tree is the component's champion. Two nodes are in the same component iff find(x)==find(y). Path compression flattens each tree toward the root on every find call, making future lookups O(1).", {})
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ("'group/merge elements dynamically', 'are X and Y connected?', 'detect cycles in undirected graph', 'connected components after each edge addition'. Union-Find does NOT handle directed graphs or edge deletions.", {})
    ])),
    N.h3("Code"),
    N.code(
        "def findRedundantConnection(edges: list[list[int]]) -> list[int]:\n"
        "    n = len(edges)\n"
        "    parent = list(range(n + 1))  # 1-indexed; parent[i] = i\n"
        "    rank = [0] * (n + 1)\n"
        "\n"
        "    def find(x: int) -> int:\n"
        "        if parent[x] != x:\n"
        "            parent[x] = find(parent[x])  # path compression\n"
        "        return parent[x]\n"
        "\n"
        "    def union(x: int, y: int) -> bool:\n"
        "        rx, ry = find(x), find(y)\n"
        "        if rx == ry:\n"
        "            return False  # already connected — cycle!\n"
        "        if rank[rx] < rank[ry]:\n"
        "            parent[rx] = ry\n"
        "        elif rank[rx] > rank[ry]:\n"
        "            parent[ry] = rx\n"
        "        else:\n"
        "            parent[ry] = rx\n"
        "            rank[rx] += 1\n"
        "        return True  # merged two distinct components\n"
        "\n"
        "    for u, v in edges:\n"
        "        if not union(u, v):   # union returns False → cycle\n"
        "            return [u, v]     # this edge is redundant"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(edges)", {"code": True}), (" — n edges implies n nodes (labeled 1..n); we use n as the size indicator.", {})])),
    N.para(N.rich([("parent = list(range(n + 1))", {"code": True}), (" — allocate n+1 slots (ignore index 0); parent[i]=i means each node is its own root initially.", {})])),
    N.para(N.rich([("rank = [0] * (n + 1)", {"code": True}), (" — rank[i] tracks subtree height for union-by-rank; keeps the forest shallow.", {})])),
    N.para(N.rich([("if parent[x] != x:", {"code": True}), (" — if x is not its own parent, it's not the root; recurse upward.", {})])),
    N.para(N.rich([("parent[x] = find(parent[x])", {"code": True}), (" — PATH COMPRESSION: on the way back from recursion, point x directly to the root. Future finds from x are O(1).", {})])),
    N.para(N.rich([("rx, ry = find(x), find(y)", {"code": True}), (" — compute root of each node before union; these are the component representatives.", {})])),
    N.para(N.rich([("if rx == ry: return False", {"code": True}), (" — CYCLE CHECK: same root means u and v are already in the same component. Returning False signals the caller to return [u,v].", {})])),
    N.para(N.rich([("rank[rx] < rank[ry]: parent[rx] = ry", {"code": True}), (" — UNION BY RANK: attach the shorter tree under the taller one to keep the forest shallow.", {})])),
    N.para(N.rich([("rank[rx] += 1", {"code": True}), (" — when ranks are equal, we break the tie and increment the winner's rank (tree grew by one level).", {})])),
    N.para(N.rich([("if not union(u, v): return [u, v]", {"code": True}), (" — process each edge; if union returns False (cycle detected), immediately return the current edge as the answer.", {})])),
    N.divider(),
]

# Solution 2 — DFS
blocks += [
    N.h2("Solution 2 — DFS Cycle Detection (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each edge [u,v] we add, check if there's already a path from u to v in the current graph. If yes, adding [u,v] creates a second path between u and v — a cycle. Return it."),
        N.h4("What Doesn't Work (Why We Need Union-Find)"),
        N.para("DFS is correct but expensive: O(n) per DFS × n edges = O(n²). For large inputs this TLEs. Union-Find solves the same 'already connected?' query in O(α(n)) instead of O(n)."),
        N.h4("The Key Observation"),
        N.para("The DFS approach works by maintaining the graph built so far. Before adding each edge, check reachability. If reachable, the new edge is redundant. The DFS explores existing edges, so it's correct but slow."),
        N.h4("Building the Solution"),
        N.para("Maintain adjacency list. For each [u,v]: run DFS from u with destination v. If v reachable, return [u,v]. Otherwise add [u,v] to graph and continue."),
    ]),
    N.h3("Code"),
    N.code(
        "def findRedundantConnection(edges: list[list[int]]) -> list[int]:\n"
        "    from collections import defaultdict\n"
        "    graph = defaultdict(set)\n"
        "\n"
        "    def has_path(src: int, dst: int, visited: set) -> bool:\n"
        "        if src == dst:\n"
        "            return True\n"
        "        visited.add(src)\n"
        "        return any(\n"
        "            has_path(nb, dst, visited)\n"
        "            for nb in graph[src]\n"
        "            if nb not in visited\n"
        "        )\n"
        "\n"
        "    for u, v in edges:\n"
        "        if has_path(u, v, set()):  # path exists → adding [u,v] creates cycle\n"
        "            return [u, v]\n"
        "        graph[u].add(v)\n"
        "        graph[v].add(u)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(set)", {"code": True}), (" — adjacency list; we build it incrementally, edge by edge.", {})])),
    N.para(N.rich([("if src == dst: return True", {"code": True}), (" — base case: we've found a path from src to dst in the existing graph.", {})])),
    N.para(N.rich([("visited.add(src)", {"code": True}), (" — mark visited to avoid revisiting in undirected graph cycles.", {})])),
    N.para(N.rich([("if has_path(u, v, set()):", {"code": True}), (" — before adding edge [u,v], check if v is already reachable from u. Fresh visited set each time.", {})])),
    N.para(N.rich([("graph[u].add(v); graph[v].add(u)", {"code": True}), (" — only add to graph if no path existed (edge is safe). Build graph incrementally for future DFS calls.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Union-Find (optimal)", "O(n·α(n)) ≈ O(n)", "O(n)"],
        ["DFS per edge", "O(n²)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Union-Find (Cycle Detection)", {})])),
    N.callout(
        "When to recognize this pattern: The problem involves an undirected graph being built edge-by-edge, and asks which edge closes the first cycle. Any query of the form 'are X and Y already connected?' repeated after each edge addition is a Union-Find signal. Keywords: 'redundant edge', 'cycle in undirected graph', 'connected components', 'spanning tree'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Union-Find / connected components):"),
    N.bullet(N.rich([("Number of Connected Components in an Undirected Graph", {"bold": True}), (" (Medium, #323) — Union-Find; count distinct roots after processing all edges.", {})])),
    N.bullet(N.rich([("Graph Valid Tree", {"bold": True}), (" (Medium, #261) — Union-Find: verify no cycle and exactly one component.", {})])),
    N.bullet(N.rich([("Accounts Merge", {"bold": True}), (" (Medium, #721) — Union-Find to merge accounts sharing any email address.", {})])),
    N.bullet(N.rich([("Most Stones Removed with Same Row or Column", {"bold": True}), (" (Medium, #947) — Union-Find to group stones in same row/column.", {})])),
    N.bullet(N.rich([("Satisfiability of Equality Equations", {"bold": True}), (" (Medium, #990) — Union-Find for transitive equality; check inequality constraints against the union.", {})])),
    N.bullet(N.rich([("Redundant Connection II", {"bold": True}), (" (Hard, #685) — Directed graph version; needs in-degree analysis combined with Union-Find.", {})])),
    N.bullet(N.rich([("Number of Islands II", {"bold": True}), (" (Hard, #305) — Online Union-Find as land cells are added dynamically.", {})])),
    N.para("These problems all share the core technique: Union-Find with find (path compression) + union (by rank) to maintain and query connected components in O(α(n)) amortized time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 8 (Graph → Union-Find / Connected Components). Sub-Pattern verified as 'Union-Find (Cycle Detection)' — Source: Guide Section 8 + Analysis.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("redundant_connection")),
    N.para(N.rich([
        ("Step through the Union-Find cycle detection algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Step 4: Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
