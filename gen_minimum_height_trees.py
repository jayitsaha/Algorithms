"""
gen_minimum_height_trees.py
Regenerate the Notion page for LeetCode #310 — Minimum Height Trees.
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815d-b897-e16be6dbf0d2"
SLUG    = "minimum_height_trees"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty = "Medium",
    number     = 310,
    pattern    = "Graph",
    subpatterns = ["Remove Leaves Iteratively"],
    tc         = "O(n)",
    sc         = "O(n)",
    key_insight = "Peel leaves iteratively (like Kahn's sort); ≤2 survivors are the tree's center nodes.",
    icon       = "🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a tree of ", ("n", {"code": True}), " nodes (", ("0", {"code": True}),
        " to ", ("n-1", {"code": True}), ") and a list of ",
        ("edges", {"code": True}), " where each edge is an undirected connection ",
        "[", ("u", {"code": True}), ", ", ("v", {"code": True}), "], "
        "you can root the tree at any node. The height of the resulting rooted tree "
        "is the number of edges on the longest downward path from root to any leaf. "
        "Return a list of all nodes that, when chosen as root, produce the minimum "
        "possible height. There will be at most 2 such nodes."
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        "n=4, edges=[[1,0],[1,2],[1,3]] → output [1]. "
        "Node 1 is the center (star graph hub); height = 1. All other nodes give height = 2."
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        "n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]] → output [3,4]. "
        "Both nodes 3 and 4 give height 2; all others give height 3."
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        "1 ≤ n ≤ 2×10⁴. edges.length == n−1. All edges are unique. Tree is connected."
    ])),
    N.divider(),
]

# ── Solution 1 — Leaf Pruning (Interview Pick) ─────────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative Leaf Pruning (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the 'most central' node(s) — the one(s) where no branch is "
            "disproportionately long. Think of it as finding the center of the tree's "
            "diameter (longest path). A tree has 1 or 2 such centers. Instead of "
            "trying every root in O(n²), can we find the center structurally?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force (try every root, BFS to compute height each time) runs in O(n²) "
            "— n BFS operations each costing O(n). For n=20,000 this means 4×10⁸ "
            "operations — too slow. We need a smarter structural insight."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Leaves (degree-1 nodes) are NEVER the optimal root for n > 2. "
            "Proof: let u be a leaf with sole neighbor v. Height when rooting at u = "
            "1 + height(v). Height when rooting at v = height(v). So u is always "
            "strictly worse than v. We can safely peel away all current leaves."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Find all current leaves (degree == 1). "
            "2. Peel them: remove each leaf, decrement its neighbor's degree. If any "
            "neighbor's degree hits 1, it becomes the next leaf. "
            "3. Repeat until ≤ 2 nodes remain. "
            "4. The survivors are the centers — return them. "
            "This is structurally identical to Kahn's topological sort!"
        ),
        N.callout(
            "Analogy: Peeling an onion from the outside in. "
            "Each round removes the outermost ring of leaves. "
            "The innermost core — 1 or 2 nodes — is the tree center.",
            "🧅", "green_background"
        ),
    ]),
]

SOLUTION_1_CODE = '''\
def findMinHeightTrees(n: int, edges: list) -> list:
    if n <= 2:
        return list(range(n))          # trivially optimal for tiny trees

    adj = [set() for _ in range(n)]   # adjacency sets for O(1) removal
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # Initial leaves: degree == 1
    leaves = [i for i in range(n) if len(adj[i]) == 1]
    remaining = n

    while remaining > 2:              # peel until ≤ 2 nodes left
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            neighbor = next(iter(adj[leaf]))   # leaf has exactly 1 neighbor
            adj[neighbor].discard(leaf)         # remove this edge
            if len(adj[neighbor]) == 1:         # neighbor exposed as new leaf
                new_leaves.append(neighbor)
        leaves = new_leaves

    return leaves                     # 1 or 2 center node(s)
'''

blocks += [
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if n <= 2: return list(range(n))", {"code": True}),
                   " — Special case: 1 or 2 nodes, every node is an MHT root."])),
    N.para(N.rich([("adj = [set() for _ in range(n)]", {"code": True}),
                   " — Adjacency SETS (not lists) so we get O(1) discard when removing edges."])),
    N.para(N.rich([("for u, v in edges: adj[u].add(v); adj[v].add(u)", {"code": True}),
                   " — Build undirected graph: each edge added in both directions."])),
    N.para(N.rich([("leaves = [i for i in range(n) if len(adj[i]) == 1]", {"code": True}),
                   " — All nodes with exactly 1 neighbor are leaves — the outermost ring."])),
    N.para(N.rich([("remaining = n", {"code": True}),
                   " — Track how many nodes haven't been peeled yet."])),
    N.para(N.rich([("while remaining > 2:", {"code": True}),
                   " — Keep peeling as long as more than 2 nodes exist. Stop at 1 or 2 (both valid center counts)."])),
    N.para(N.rich([("remaining -= len(leaves)", {"code": True}),
                   " — Subtract this round's leaf count before processing (so we know when to stop)."])),
    N.para(N.rich([("neighbor = next(iter(adj[leaf]))", {"code": True}),
                   " — Each leaf has exactly 1 neighbor (by definition of degree 1). Get it in O(1)."])),
    N.para(N.rich([("adj[neighbor].discard(leaf)", {"code": True}),
                   " — Remove the edge: neighbor no longer 'sees' this leaf. Decrements neighbor's effective degree."])),
    N.para(N.rich([("if len(adj[neighbor]) == 1: new_leaves.append(neighbor)", {"code": True}),
                   " — If neighbor's degree dropped to 1, it's now a leaf for the next round."])),
    N.para(N.rich([("leaves = new_leaves", {"code": True}),
                   " — Advance to the next ring (inner layer)."])),
    N.para(N.rich([("return leaves", {"code": True}),
                   " — Remaining 1 or 2 nodes are the centers. Return them as the answer."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force BFS (O(n²) · Too Slow)"),
    N.toggle_h3("💡 Intuition: Why We Start Here", [
        N.h4("Reframe the Problem"),
        N.para(
            "The simplest approach: literally try every node as root, compute the tree "
            "height for each via BFS, find the minimum, collect all nodes achieving it."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "O(n²) time: n roots × O(n) BFS per root. For n=20,000 this is 4×10⁸ ops. "
            "TLEs on LeetCode but valid as a first approach to explain before optimizing."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Every BFS is independent — we're recomputing the same tree structure n times. "
            "There must be structural insight to avoid repeating this work. That insight "
            "is the leaf-peeling approach in Solution 1."
        ),
    ]),
]

SOLUTION_2_CODE = '''\
def findMinHeightTrees_brute(n: int, edges: list) -> list:
    if n == 1:
        return [0]
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs_height(root):
        seen = {root}
        queue = [root]
        h = 0
        while queue:
            nxt = []
            for node in queue:
                for nb in adj[node]:
                    if nb not in seen:
                        seen.add(nb)
                        nxt.append(nb)
            if nxt:
                h += 1
            queue = nxt
        return h

    heights = [bfs_height(i) for i in range(n)]  # O(n) x n = O(n^2)
    min_h = min(heights)
    return [i for i, h in enumerate(heights) if h == min_h]
'''

blocks += [
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def bfs_height(root):", {"code": True}),
                   " — Standard BFS from root; returns number of levels − 1 = height."])),
    N.para(N.rich([("heights = [bfs_height(i) for i in range(n)]", {"code": True}),
                   " — Run BFS from every possible root. O(n) × O(n) = O(n²) total."])),
    N.para(N.rich([("min_h = min(heights)", {"code": True}),
                   " — Find the minimum achievable height."])),
    N.para(N.rich([("return [i for i, h in enumerate(heights) if h == min_h]", {"code": True}),
                   " — Collect all roots that achieve the minimum height."])),
    N.callout(
        "Use this approach in interviews ONLY as a starting point. "
        "Immediately follow with: 'We can optimize to O(n) using leaf pruning...'",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force BFS", "O(n²)", "O(n)", "TLE for large n; good starting point"],
        ["Leaf Pruning (Optimal)", "O(n)", "O(n)", "Each node/edge processed once; interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Remove Leaves Iteratively (Topological Peel on Undirected Tree)"])),
    N.para(N.rich([
        "This pattern is structurally equivalent to ", ("Kahn's Algorithm", {"bold": True}),
        " for topological sorting: process nodes with degree 0 (or 1 for undirected trees) first, "
        "decrement neighbors, enqueue new zeros/ones, repeat. In this problem, degree-1 nodes are "
        "leaves (analogous to in-degree-0 nodes in a DAG)."
    ])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Tree structure (n nodes, n-1 edges, connected, no cycles). "
        "(2) Find 'center', 'centroid', or minimize a max-distance root metric. "
        "(3) Brute force is O(n²) — signal to find O(n) structural approach. "
        "(4) The answer is 1 or 2 nodes (hint: tree centers ≤ 2).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or adjacent technique:"),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}),
                     " (Medium) — Kahn's topological sort on directed graph; same degree-peeling mechanics (#210)"])),
    N.bullet(N.rich([("Find the Town Judge", {"bold": True}),
                     " (Easy) — Degree reasoning: find node with in-degree n-1 and out-degree 0 (#997)"])),
    N.bullet(N.rich([("Tree Diameter (Undirected)", {"bold": True}),
                     " (Medium) — Two-BFS to find longest path; centers lie at its midpoint (#1245)"])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}),
                     " (Hard) — Rerooting DP exploiting tree center properties; O(n) (#834)"])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}),
                     " (Medium) — Detect cycle in near-tree graph structure (#684)"])),
    N.bullet(N.rich([("All Nodes Distance K in Binary Tree", {"bold": True}),
                     " (Medium) — BFS from a node in a tree; graph conversion (#863)"])),
    N.para("These problems share the core insight: exploit tree structure to avoid brute-force O(n²) traversals."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph Section. "
        "Sub-Pattern: Remove Leaves Iteratively. Source: Analysis (new classification — "
        "Topological Peel on undirected tree).",
        "📚", "gray_background"
    ),
]

# ── Interactive Embed ──────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
