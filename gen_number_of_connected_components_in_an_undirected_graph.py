"""
Notion update script for: Number of Connected Components in an Undirected Graph
LeetCode #323 | Medium | Graph / Union-Find
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f0-bcd2-d279cfb2323c"
SLUG = "number_of_connected_components_in_an_undirected_graph"
GITHUB_URL = f"https://jayitsaha.github.io/Algorithms/{SLUG}_explainer.html"

# ── 1. Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=323,
    pattern="Graph",
    subpatterns=["Union-Find"],
    tc="O(n · α(n))",
    sc="O(n)",
    key_insight="Start with n components; each successful union (different roots) decrements the count by 1.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── 3. Build new body ────────────────────────────────────────────────────────
print("Building new body...")
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (" (number of nodes labeled 0 to n-1) and a list of undirected ", {}),
        ("edges", {"code": True}),
        (" where each edge ", {}),
        ("edges[i] = [u, v]", {"code": True}),
        (" represents a connection between nodes u and v, return the number of connected components in the graph.", {})
    ])),
    N.para(N.rich([
        ("Example: n=5, edges=[[0,1],[1,2],[3,4]] → ", {}),
        ("2", {"bold": True}),
        (" (groups {0,1,2} and {3,4})", {})
    ])),
    N.divider(),
]

# ── Solution 1: Union-Find (Interview Pick) ──────────────────────────────────
blocks += [
    N.h2("Solution 1 — Union-Find with Path Compression + Rank (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count how many 'clusters' of nodes exist when we're done connecting them via edges. Think of it as: how many independent islands remain after building all bridges?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each pair of nodes, run a BFS/DFS to check connectivity — O(n² · (n+e)). Even the simpler DFS approach (O(n+e) but O(n+e) space for adjacency list) requires storing the entire graph. We can do better."),
        N.h4("The Key Observation"),
        N.para("Start with components = n. Each edge either (a) connects two different components → components decreases by 1, or (b) connects two nodes already in the same component → no change. We just need to track which component each node belongs to and count successful merges."),
        N.h4("Building the Solution"),
        N.para("Union-Find (DSU) is the perfect data structure: parent[i] stores each node's 'representative' root, and rank[i] controls tree height to prevent degenerate chains. find() with path compression gives near-O(1) lookups. union() by rank keeps trees shallow."),
        N.callout(
            "Analogy: Think of each node as a city with its own mayor. When two cities merge (edge processed), one mayor becomes the 'super-mayor'. Path compression = each city calls the super-mayor directly, skipping intermediaries.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find (DSU)"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Bernard Galler and Michael Fischer (1964). The path-compression optimization was developed by Hopcroft & Ullman (1973); the inverse-Ackermann amortized bound was proved by Tarjan (1975). Widely used in Kruskal's MST algorithm.", {})
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("Two nodes u and v are in the same connected component if and only if ", {}),
        ("find(u) == find(v)", {"code": True}),
        (". The parent array encodes a forest of trees; each tree = one component; each tree has exactly one root (parent[root] == root).", {})
    ])),
    N.para(N.rich([
        ("Why union by rank works: ", {"bold": True}),
        ("Without rank, n successive merges can produce a degenerate chain of height n (find = O(n)). Rank ensures the height stays at O(log n) before compression. With path compression, amortized cost per operation = O(α(n)) — effectively constant for all practical inputs.", {})
    ])),
    N.para(N.rich([
        ("Recognize when: ", {"bold": True}),
        ('Problem says "group," "cluster," "connected," "reachable," or "merge" with nodes and edges. Canonical DSU problems: connected components, cycle detection, MST (Kruskal), island merging.', {})
    ])),
    N.h3("Code"),
    N.code("""def countComponents(n, edges):
    parent = list(range(n))   # parent[i] = i: each node is its own root
    rank   = [0] * n          # height of tree rooted at i
    components = n             # start: n isolated nodes = n components

    def find(x):               # find root with path compression
        if parent[x] != x:
            parent[x] = find(parent[x])  # flatten: point x directly to root
        return parent[x]

    def union(u, v):
        nonlocal components
        ru, rv = find(u), find(v)
        if ru == rv: return           # already connected, skip
        if rank[ru] < rank[rv]: ru, rv = rv, ru  # ensure ru is taller
        parent[rv] = ru               # attach shorter tree under taller
        if rank[ru] == rank[rv]: rank[ru] += 1   # grow height only when equal
        components -= 1               # successful merge: one fewer component

    for u, v in edges:
        union(u, v)
    return components"""),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = list(range(n))", {"code": True}), (" — Each node starts as its own root. parent[0]=0, parent[1]=1, etc.", {})])),
    N.para(N.rich([("rank = [0] * n", {"code": True}), (" — All trees start with height 0.", {})])),
    N.para(N.rich([("components = n", {"code": True}), (" — n isolated nodes = n components initially.", {})])),
    N.para(N.rich([("if parent[x] != x: parent[x] = find(parent[x])", {"code": True}), (" — Path compression: if x is not its own root, recurse and set x's parent directly to the root on the way back. Flattens future lookups.", {})])),
    N.para(N.rich([("if ru == rv: return", {"code": True}), (" — Same root = same component = cycle edge. Nothing to merge.", {})])),
    N.para(N.rich([("if rank[ru] < rank[rv]: ru, rv = rv, ru", {"code": True}), (" — Swap so ru is always the taller tree (we'll attach rv under ru).", {})])),
    N.para(N.rich([("parent[rv] = ru", {"code": True}), (" — Attach the shorter tree under the taller root.", {})])),
    N.para(N.rich([("if rank[ru] == rank[rv]: rank[ru] += 1", {"code": True}), (" — Only increment when merging two equal-height trees (combined height grows by 1).", {})])),
    N.para(N.rich([("components -= 1", {"code": True}), (" — Two components became one.", {})])),
    N.divider(),
]

# ── Solution 2: DFS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS (Simpler, O(n+e) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A connected component is all nodes reachable from a starting node. So: pick any unvisited node, run DFS to mark every node reachable from it as 'visited', count how many times you have to start a fresh DFS."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct and simple, but requires O(n+e) space for the adjacency list and visited set — more memory than Union-Find needs."),
        N.h4("The Key Observation"),
        N.para("The number of components equals the number of times we initiate a fresh DFS from an unvisited node. Each DFS explores exactly one complete component."),
        N.h4("Building the Solution"),
        N.para("Build an adjacency list from edges. Iterate 0..n-1. For each unvisited node, run DFS (marking all reachable nodes) and increment the counter."),
    ]),
    N.h3("Code"),
    N.code("""def countComponents(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)        # undirected: add both directions
    visited = set()
    def dfs(node):
        visited.add(node)
        for nb in adj[node]:
            if nb not in visited:
                dfs(nb)
    components = 0
    for i in range(n):
        if i not in visited:    # unvisited node = start of new component
            dfs(i)
            components += 1
    return components"""),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = {i: [] for i in range(n)}", {"code": True}), (" — Initialize adjacency list for each node.", {})])),
    N.para(N.rich([("adj[u].append(v); adj[v].append(u)", {"code": True}), (" — Undirected edge: add both directions.", {})])),
    N.para(N.rich([("visited = set()", {"code": True}), (" — Global set of visited nodes across all DFS calls.", {})])),
    N.para(N.rich([("if nb not in visited: dfs(nb)", {"code": True}), (" — Recurse only to unvisited neighbors to avoid infinite loops in cycles.", {})])),
    N.para(N.rich([("if i not in visited:", {"code": True}), (" — If node i hasn't been reached by any previous DFS, it's the start of a new undiscovered component.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Union-Find (path compress + rank)", "O(n · α(n))", "O(n)"],
        ["DFS / BFS", "O(n + e)", "O(n + e)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Union-Find (Disjoint Set Union)", {})])),
    N.callout(
        "When to recognize this pattern: The problem involves 'connected,' 'reachable,' 'group,' 'merge,' or 'cluster' with nodes and edges. Bonus signal: the problem needs only to know IF two things are connected (not the actual path). Union-Find answers connectivity queries in nearly O(1) after O(n) setup.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Union-Find / connectivity technique:"),
    N.bullet(N.rich([("Number of Islands (200)", {"bold": True}), (" (Medium) — BFS/DFS or DSU on a 2D grid; exactly the same counting logic", {})])),
    N.bullet(N.rich([("Redundant Connection (684)", {"bold": True}), (" (Medium) — find the edge that creates a cycle: the one where find(u)==find(v) before union", {})])),
    N.bullet(N.rich([("Graph Valid Tree (261)", {"bold": True}), (" (Medium) — valid tree iff exactly n-1 successful unions (no cycles, all nodes connected)", {})])),
    N.bullet(N.rich([("Accounts Merge (721)", {"bold": True}), (" (Medium) — DSU on email strings; merge accounts sharing an email address", {})])),
    N.bullet(N.rich([("Friend Circles (547)", {"bold": True}), (" (Medium) — adjacency matrix representation of this exact problem", {})])),
    N.bullet(N.rich([("Smallest String With Swaps (1202)", {"bold": True}), (" (Medium) — group indices by reachability via DSU, sort within each group", {})])),
    N.bullet(N.rich([("Min Cost to Connect All Points (1584)", {"bold": True}), (" (Medium) — Kruskal's MST using Union-Find on a dense Euclidean graph", {})])),
    N.para("These problems share the same core technique: maintain a parent forest, find roots with path compression, union by rank, count distinct roots."),
    N.divider(),
]

# ── Interactive Explainer embed ───────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(GITHUB_URL),
    N.para(N.rich([
        ("Step through the Union-Find algorithm visually — use Next/Prev or arrow keys to see each merge, path compression, and component count update.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
