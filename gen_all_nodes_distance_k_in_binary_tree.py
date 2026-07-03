"""gen_all_nodes_distance_k_in_binary_tree.py — Notion updater for LC #863."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812b-b87b-dddc46192d34"

# ── 1) Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=863,
    pattern="Graph",
    subpatterns=["Build Graph + BFS"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Convert tree to undirected graph by adding parent edges via DFS, then BFS from target for exactly K levels.",
    icon="🟡",
)
print("Properties set OK")

# ── 2) Wipe old content ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3) Build new content ────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary tree, a ", {}),
        ("target", {"code": True}),
        (" node, and an integer ", {}),
        ("k", {"code": True}),
        (", return a list of the values of all nodes that have a distance ", {}),
        ("k", {"code": True}),
        (" from the target node. Distance is measured in edges — one hop up or down the tree counts as 1.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("Tree 3→(5,1), 5→(6,2), 1→(0,8), 2→(7,4). target=5, k=2 → [7, 4, 1]. "
             "Node 1 is reached by going UP: 5→3→1.", {}),
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# Solution 1 — Build Graph + BFS
blocks += [
    N.h2("Solution 1 — Build Undirected Graph + BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need all nodes exactly K edges away from a target — edges can go both up and down the tree. "
            "The root obstacle is that standard tree traversal only moves parent→child. "
            "We can't reach ancestors or sibling subtrees without upward pointers."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive approach: find the target node, then try to walk K steps in all directions using "
            "a mix of tree DFS calls. This gets messy fast — to go 'upward' you'd need to re-traverse "
            "from the root, check at which depth target lives, then re-traverse again for sibling branches. "
            "This is O(n²) and error-prone."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A binary tree IS an undirected graph — we just strip the directionality of the edges. "
            "If we add parent pointers (adj[child] ↔ adj[parent]) during one DFS pass, every node "
            "can now see both its children and its parent as equal neighbors. "
            "Then BFS from the target for exactly K rounds gives us all distance-K nodes."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: DFS the tree once. For each parent-child pair, do adj[parent.val].append(child.val) "
            "AND adj[child.val].append(parent.val). "
            "Step 2: BFS from target.val. Use a visited set. Track distance level. "
            "After K rounds, whatever is in the queue is the answer."
        ),
        N.callout(
            "Analogy: Imagine a city where all roads are one-way (parent→child). "
            "We add reverse lanes on every road (parent←child). Now from any intersection, "
            "we can drive in all directions. BFS finds all locations exactly K blocks away.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict, deque\n"
        "\n"
        "def distanceK(root, target, k):\n"
        "    adj = defaultdict(list)\n"
        "\n"
        "    def build(node, parent):\n"
        "        if not node:\n"
        "            return\n"
        "        if parent:\n"
        "            adj[node.val].append(parent.val)   # upward edge\n"
        "            adj[parent.val].append(node.val)   # downward edge\n"
        "        build(node.left, node)\n"
        "        build(node.right, node)\n"
        "\n"
        "    build(root, None)\n"
        "\n"
        "    queue = deque([target.val])\n"
        "    visited = {target.val}\n"
        "    dist = 0\n"
        "\n"
        "    while queue and dist < k:\n"
        "        for _ in range(len(queue)):   # process entire current level\n"
        "            node = queue.popleft()\n"
        "            for nb in adj[node]:\n"
        "                if nb not in visited:\n"
        "                    visited.add(nb)\n"
        "                    queue.append(nb)\n"
        "        dist += 1\n"
        "\n"
        "    return list(queue)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = defaultdict(list)", {"code": True}), (" — adjacency list mapping each node value to a list of its neighbor values (children + parent).", {})])),
    N.para(N.rich([("def build(node, parent)", {"code": True}), (" — DFS helper that populates adj. Takes current node and its parent (None for root).", {})])),
    N.para(N.rich([("adj[node.val].append(parent.val)", {"code": True}), (" / ", {}), ("adj[parent.val].append(node.val)", {"code": True}), (" — add BOTH directions for every parent-child pair. This is the key transformation: tree edge becomes bidirectional graph edge.", {})])),
    N.para(N.rich([("build(node.left, node)", {"code": True}), (" / ", {}), ("build(node.right, node)", {"code": True}), (" — recurse, passing current node as the parent for children.", {})])),
    N.para(N.rich([("queue = deque([target.val])", {"code": True}), (" — BFS queue initialized with just the target. We use values (integers) as keys because all values are unique.", {})])),
    N.para(N.rich([("visited = {target.val}", {"code": True}), (" — mark target visited immediately to prevent BFS from returning to it through symmetric edges.", {})])),
    N.para(N.rich([("while queue and dist < k", {"code": True}), (" — keep expanding while queue has nodes AND we haven't reached distance k yet.", {})])),
    N.para(N.rich([("for _ in range(len(queue))", {"code": True}), (" — snapshot the current level's size. This inner loop processes all nodes at the current distance before incrementing dist.", {})])),
    N.para(N.rich([("for nb in adj[node]", {"code": True}), (" — iterate all neighbors: left child, right child, AND parent (thanks to the bidirectional edges we built).", {})])),
    N.para(N.rich([("if nb not in visited", {"code": True}), (" — only enqueue each node once, at its shortest (first-reached) distance.", {})])),
    N.para(N.rich([("dist += 1", {"code": True}), (" — one full level processed. All new nodes in queue are now at distance dist+1 from target.", {})])),
    N.para(N.rich([("return list(queue)", {"code": True}), (" — after exactly k expansions, queue holds all distance-k nodes. Convert deque to list.", {})])),
    N.divider(),
]

# Solution 2 — Pure DFS
blocks += [
    N.h2("Solution 2 — Pure DFS with Distance Tracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of building an explicit graph, we can use a recursive DFS that propagates "
            "distance information UPWARD through return values."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Simple downward collection from target works for nodes below the target, "
            "but completely misses nodes that require going up the tree first."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When DFS finds the target in a subtree at distance d below an ancestor, "
            "that ancestor is at distance d+1 from target. The OTHER child of that ancestor "
            "then becomes a starting point for collecting nodes at distance (k - d - 2) steps down."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Two helper functions: collect(node, dist) gathers all nodes exactly (k - dist) steps below 'node'. "
            "dfs(node) returns the distance from 'node' to target (-1 if not found). "
            "When target is found in a left/right subtree, we trigger collection in the opposite subtree "
            "at the adjusted distance, and check if the current ancestor itself is at distance k."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def distanceK(root, target, k):\n"
        "    res = []\n"
        "\n"
        "    def collect(node, dist):\n"
        "        \"\"\"Collect all nodes exactly k steps below 'node' (dist steps already taken).\"\"\"\n"
        "        if not node or dist > k:\n"
        "            return\n"
        "        if dist == k:\n"
        "            res.append(node.val)\n"
        "            return\n"
        "        collect(node.left, dist + 1)\n"
        "        collect(node.right, dist + 1)\n"
        "\n"
        "    def dfs(node):\n"
        "        \"\"\"Return distance from node to target. -1 if target not in subtree.\"\"\"\n"
        "        if not node:\n"
        "            return -1\n"
        "        if node == target:\n"
        "            collect(node, 0)  # gather nodes k steps below target\n"
        "            return 0\n"
        "        left = dfs(node.left)\n"
        "        if left != -1:           # target is in left subtree\n"
        "            collect(node.right, left + 2)  # explore right branch\n"
        "            if left + 1 == k:\n"
        "                res.append(node.val)\n"
        "            return left + 1\n"
        "        right = dfs(node.right)\n"
        "        if right != -1:          # target is in right subtree\n"
        "            collect(node.left, right + 2)\n"
        "            if right + 1 == k:\n"
        "                res.append(node.val)\n"
        "            return right + 1\n"
        "        return -1\n"
        "\n"
        "    dfs(root)\n"
        "    return res"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("collect(node, dist)", {"code": True}), (" — gathers all nodes exactly k steps below 'node', given that 'dist' steps have already been taken to reach 'node' from the target.", {})])),
    N.para(N.rich([("if dist == k: res.append(node.val)", {"code": True}), (" — we've taken exactly k steps from target — this is a result node.", {})])),
    N.para(N.rich([("dfs(node)", {"code": True}), (" — recursively finds target; returns the distance from 'node' to target, or -1 if target is not in this subtree.", {})])),
    N.para(N.rich([("if left != -1:", {"code": True}), (" — target was found in the left subtree at depth 'left'. The current node is at distance left+1 from target.", {})])),
    N.para(N.rich([("collect(node.right, left + 2)", {"code": True}), (" — we need to go from target UP to this node (left+1 steps), then DOWN into right subtree (+1 more = left+2 total so far).", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Build Graph + BFS (Solution 1)", "O(n)", "O(n)", "adj list + visited + queue"],
        ["Pure DFS (Solution 2)", "O(n)", "O(h)", "h = tree height; no extra adj list"],
        ["Naive re-traverse", "O(n²)", "O(n)", "Avoid — double work"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (BFS: Shortest Path Unweighted)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Build Graph + BFS — convert tree to undirected graph, then BFS for K levels", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('(1) "Distance from a node in all directions" in a tree — not just downward. '
             "(2) Need to traverse upward (toward root/ancestors). "
             "(3) Finding all nodes at exactly K hops from a source. "
             "(4) Unweighted shortest path on a graph or tree.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Build Graph / BFS technique:"),
    N.bullet(N.rich([("Binary Tree Diameter", {"bold": True}), (" (Easy) — Longest path in a tree; treats tree as undirected graph for distance computation (#543)", {})])),
    N.bullet(N.rich([("Time Needed to Inform All Employees", {"bold": True}), (" (Medium) — Build adjacency list from manager-report pairs, BFS/DFS from root to find max time (#1376)", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — BFS layer by layer on a grid graph; same level-count distance pattern (#1091)", {})])),
    N.bullet(N.rich([("Cousins in Binary Tree", {"bold": True}), (" (Easy) — BFS to find depth and parent of two nodes; needs same-level, different-parent check (#993)", {})])),
    N.bullet(N.rich([("Clone Graph", {"bold": True}), (" (Medium) — BFS on undirected graph with visited dict preventing revisits; same pattern (#133)", {})])),
    N.bullet(N.rich([("Find Leaves of Binary Tree", {"bold": True}), (" (Medium) — Uses 'height from leaf' concept; similar bottom-up distance tracking via DFS (#366)", {})])),
    N.para("These problems all share the core technique: treating tree or grid structures as bidirectional graphs and using BFS to measure distance level by level."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Graph Algorithms → BFS: Shortest Path Unweighted). Sub-Pattern: Build Graph + BFS · Source: Guide Section 6 + Analysis", "📚", "gray_background"),
]

# Interactive embed (last section)
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("all_nodes_distance_k_in_binary_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
