"""
gen_sum_of_distances_in_tree.py
Regenerates the Notion page for Sum of Distances in Tree (LC #834).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "sum_of_distances_in_tree"
PAGE_ID = None  # null → create new

# ── Step 0: Create page ────────────────────────────────────────────
if PAGE_ID is None:
    PAGE_ID = N.create_page("Sum of Distances in Tree", 834, "Hard", "🔴")
    print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=834,
    pattern="Dynamic Programming",
    subpatterns=["Rerooting DP", "Tree DP"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Root at 0, compute subtree distances (DFS1). Then reroot each node in O(1): ans[child] = ans[parent] + n - 2*count[child].",
    icon="🔴",
)
print("Properties set.")

# ── Step 2: Wipe old body ─────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body ────────────────────────────────────────────
blocks = []

# ── Problem ─────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is an undirected connected tree with ", {}),
        ("n", {"code": True}),
        (" nodes labelled ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n-1", {"code": True}),
        (" and ", {}),
        ("n-1", {"code": True}),
        (" edges. You are given the integer ", {}),
        ("n", {"code": True}),
        (" and the array ", {}),
        ("edges", {"code": True}),
        (" where ", {}),
        ("edges[i] = [ai, bi]", {"code": True}),
        (" indicates there is an edge between nodes ", {}),
        ("ai", {"code": True}),
        (" and ", {}),
        ("bi", {"code": True}),
        (" in the tree. Return an array ", {}),
        ("ans", {"code": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (" where ", {}),
        ("ans[i]", {"code": True}),
        (" is the sum of the distances between the ", {}),
        ("ith", {}),
        (" node in the tree and all other nodes.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Rerooting DP ────────────────────────────────────
sol1_code = """\
def sumOfDistancesInTree(n: int, edges: list[list[int]]) -> list[int]:
    from collections import defaultdict
    import sys
    sys.setrecursionlimit(50000)

    # Build undirected adjacency list
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    count = [1] * n   # count[i] = size of subtree rooted at i (DFS1)
    ans   = [0] * n   # ans[i]   = sum of distances from i (final answer)

    def dfs1(node, parent):
        \"\"\"Post-order: children computed before parent.\"\"\"
        for child in graph[node]:
            if child == parent:
                continue          # avoid going back up the tree
            dfs1(child, node)
            count[node] += count[child]           # accumulate subtree size
            ans[node]   += ans[child] + count[child]  # distances in subtree

    def dfs2(node, parent):
        \"\"\"Pre-order (rerooting): parent answer ready before children.\"\"\"
        for child in graph[node]:
            if child == parent:
                continue
            # Rerooting formula: moving root from node to child
            # count[child] nodes get 1 closer, (n-count[child]) get 1 farther
            ans[child] = ans[node] + n - 2 * count[child]
            dfs2(child, node)

    dfs1(0, -1)   # populate count[] and ans[0]
    dfs2(0, -1)   # propagate to every other node
    return ans
"""

intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We want the sum of distances from every node to every other node. "
           "Brute-force BFS from each of n nodes is O(n²) — too slow for n=30000. "
           "Can we reuse information across nodes?"),
    N.h4("What Doesn't Work"),
    N.para("Running BFS/DFS from every node individually is correct but O(n²). "
           "Memoizing the BFS doesn't help because each BFS explores the full tree from a different root. "
           "We need a smarter relationship between the answers for adjacent nodes."),
    N.h4("The Key Observation"),
    N.para("When you move from node u to an adjacent node v, exactly two groups of nodes are affected: "
           "the count[v] nodes in v's subtree each get 1 step CLOSER, "
           "and the (n - count[v]) nodes outside v's subtree each get 1 step FARTHER. "
           "Net change: ans[v] = ans[u] + (n - count[v]) - count[v] = ans[u] + n - 2*count[v]."),
    N.h4("Building the Solution"),
    N.para("Step 1: Root the tree at node 0. DFS1 (post-order) computes count[v] (subtree size) "
           "and ans[0] (sum of distances from root). "
           "Step 2: DFS2 (pre-order) applies the rerooting formula to every other node in O(1) each. "
           "Two DFS passes = O(n) total."),
    N.callout(
        "Analogy: Imagine a company org-chart. HR (root) knows the total commute distance for all employees. "
        "When a manager (child) takes over as acting CEO, employees in their division get closer, "
        "everyone else gets farther. We adjust the total by that exact difference.",
        "🧠", "blue_background"
    ),
]

blocks += [
    N.h2("Solution 1 — Rerooting Tree DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_children),
    N.h3("🔬 Algorithm Deep-Dive: Rerooting DP"),
    N.para(N.rich([
        ("Rerooting DP", {"bold": True}),
        (" is a tree DP technique where you compute a quantity for one fixed root, "
         "then re-derive the quantity for every other node in O(1) per node by "
         "'shifting' the root across each edge. ", {}),
        ("Origin:", {"bold": True}),
        (" Classical competitive programming technique, widely used in problems "
         "where a per-node global property depends on the full tree structure. ", {}),
        ("Core invariant:", {"bold": True}),
        (" After DFS1, count[v] = |subtree(v)| and ans[root] is correct. "
         "After DFS2, ans[v] is correct for every v. "
         "The rerooting formula bridges these two facts.", {}),
    ])),
    N.code(
        "# Rerooting Identity (derivation)\n"
        "# When root moves from u to adjacent child v:\n"
        "#   - count[v] nodes in v's subtree: each distance decreases by 1 → contribution: -count[v]\n"
        "#   - n-count[v] nodes outside subtree: each distance increases by 1 → contribution: +(n-count[v])\n"
        "# Net: ans[v] = ans[u] + (n - count[v]) - count[v]\n"
        "#             = ans[u] + n - 2*count[v]\n"
        "#\n"
        "# DFS1 recurrences:\n"
        "#   count[v] = 1 + sum(count[c] for c in children(v))\n"
        "#   ans[v]   = sum(ans[c] + count[c] for c in children(v))\n"
        "#              ^ distances within subtree ^ each node in c's subtree is 1 hop farther\n",
        lang="python"
    ),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(set)", {"code": True}),
                   (" — Adjacency list for the undirected tree. Each edge stored in both directions.", {})])),
    N.para(N.rich([("count = [1] * n", {"code": True}),
                   (" — count[i] starts at 1 (the node itself). DFS1 will add each child's subtree size.", {})])),
    N.para(N.rich([("ans = [0] * n", {"code": True}),
                   (" — ans[i] will hold the final answer for node i. DFS1 fills ans[0] correctly; DFS2 fills the rest.", {})])),
    N.para(N.rich([("if child == parent: continue", {"code": True}),
                   (" — In an undirected tree, each node connects to its parent AND all children. "
                    "We skip the parent edge to avoid infinite recursion.", {})])),
    N.para(N.rich([("count[node] += count[child]", {"code": True}),
                   (" — Post-order aggregation: after recursing into child, add its subtree size to the current node's count.", {})])),
    N.para(N.rich([("ans[node] += ans[child] + count[child]", {"code": True}),
                   (" — ans[child] = sum of internal distances within child's subtree. "
                    "+count[child] = the one extra edge hop from node to every node in that subtree.", {})])),
    N.para(N.rich([("ans[child] = ans[node] + n - 2 * count[child]", {"code": True}),
                   (" — The rerooting formula. Shift root from node to child: "
                    "(n-count[child]) nodes get farther (+), count[child] nodes get closer (-).", {})])),
    N.callout(
        "⚠️ Python recursion limit: for n=30000 on a path graph, "
        "recursion depth = n. Add sys.setrecursionlimit(50000) or convert to iterative DFS with an explicit stack.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Brute Force ────────────────────────────────────
sol2_code = """\
def sumOfDistancesInTree_BF(n: int, edges: list[list[int]]) -> list[int]:
    \"\"\"O(n²) brute force: BFS from every node.\"\"\"
    from collections import deque, defaultdict
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def bfs(src):
        dist = [-1] * n
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return sum(dist)

    return [bfs(i) for i in range(n)]
"""

intuition2_children = [
    N.h4("Reframe the Problem"),
    N.para("For each node, compute the sum of shortest-path distances to all others. "
           "In a tree, the unique path between any two nodes is the shortest path."),
    N.h4("What Doesn't Work (Why Brute Force Fails)"),
    N.para("BFS from a single source takes O(n). Doing this for all n sources costs O(n²). "
           "For n=30000, that's 9×10⁸ operations — times out in Python."),
    N.h4("The Key Observation"),
    N.para("This approach is conceptually simple and correct. "
           "It serves as the baseline to verify the rerooting DP output during development and testing."),
    N.h4("Building the Solution"),
    N.para("For each node i, run BFS/DFS to compute all distances, then sum them. "
           "O(n) per node × n nodes = O(n²). Only use for small n or verification."),
]

blocks += [
    N.h2("Solution 2 — Brute Force BFS (O(n²), for reference)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition2_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("bfs(src)", {"code": True}),
                   (" — Standard BFS from source node. Visits all n nodes in O(n).", {})])),
    N.para(N.rich([("return [bfs(i) for i in range(n)]", {"code": True}),
                   (" — Run BFS from every node. O(n) × n = O(n²) total.", {})])),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force BFS", "O(n²)", "O(n)", "TLE for n=30000"],
        ["Rerooting Tree DP", "O(n)", "O(n)", "Optimal — Interview Pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Rerooting DP, Tree DP", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for a value computed from the perspective of EVERY node in a tree\n"
        "• The value has a natural subtree aggregation in post-order DFS\n"
        "• Moving the root across an edge changes the value in a predictable O(1) way\n"
        "• Keywords: 'for each node', 'sum of distances', 'minimum path sum to all nodes'",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"bold": True}),
        ("'Rerooting DP' is a specialized sub-pattern of Tree DP. "
         "Verified against DSA Patterns Guide Section 18 (Dynamic Programming → Tree DP).", {}),
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same rerooting / tree DP technique:"),
    N.bullet(N.rich([("Distribution of Coins in Binary Tree", {"bold": True}),
                     (" (Medium) — Post-order tree DP: compute subtree excess/deficit to minimize moves.", {})])),
    N.bullet(N.rich([("House Robber III", {"bold": True}),
                     (" (Medium) — Tree DP with two states per node (rob/skip), aggregated post-order.", {})])),
    N.bullet(N.rich([("Count Nodes Equal to Average of Subtree", {"bold": True}),
                     (" (Medium) — Return (sum, count) from each DFS call; check condition at each node.", {})])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}),
                     (" (Medium) — Topological peeling to find centroid; centroid minimizes max distance (related to rerooting logic).", {})])),
    N.bullet(N.rich([("Binary Tree Cameras", {"bold": True}),
                     (" (Hard) — Greedy tree DP with 3 states per node, aggregated post-order.", {})])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}),
                     (" (Medium) — DFS with prefix sums to count paths; conceptually a tree DP.", {})])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}),
                     (" (Easy) — Post-order DFS aggregating max depth; the diameter is the max sum of two children depths.", {})])),
    N.para("These problems all share tree structure + DFS aggregation. "
           "Rerooting DP specifically applies when you need the answer for EVERY node, not just the root."),
    N.callout("📚 Reference: DSA Patterns Guide Section 18 — Dynamic Programming → Tree DP", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ─────────────────────────────────────────────
import json, pathlib
html_path = pathlib.Path(__file__).parent / "sum_of_distances_in_tree_explainer.html"
html_lines = len(html_path.read_text().splitlines()) if html_path.exists() else 0

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
status = {
    "slug": SLUG,
    "html": "OK" if html_lines >= 700 else "FAIL:too_short",
    "notion": "OK",
    "lines": html_lines,
    "notion_page_id": PAGE_ID,
    "notes": f"Rerooting DP, two-pass DFS, n=6 tree walkthrough, {html_lines} HTML lines",
}
(status_dir / f"{SLUG}.json").write_text(json.dumps(status, indent=2))
print(f"RESULT {SLUG} | html={'OK' if html_lines>=700 else 'FAIL'} | notion=OK | lines={html_lines}")
