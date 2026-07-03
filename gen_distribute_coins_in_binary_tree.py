"""gen_distribute_coins_in_binary_tree.py — Notion update for LeetCode #979."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-819a-b581-ffe18682eeff"

# ─── 1. Set properties ───────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=979,
    pattern="Trees",
    subpatterns=["DFS: Postorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Each edge carries |excess| coins where excess = subtree_coins − subtree_nodes; sum |excess| over all edges.",
    icon="🟡",
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Build body blocks ────────────────────────────────────────────
SLUG = "distribute_coins_in_binary_tree"

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree with ", {}),
        ("n", {"code": True}),
        (" nodes. Each node in the tree has ", {}),
        ("node.val", {"code": True}),
        (" coins. There are ", {}),
        ("n", {"code": True}),
        (" coins in total (i.e. the sum of all ", {}),
        ("node.val", {"code": True}),
        (" values equals ", {}),
        ("n", {"code": True}),
        (").", {}),
    ])),
    N.para("In one move, you may choose two adjacent nodes and move one coin from one node to the other (a move may be from parent to child, or from child to parent). Return the minimum number of moves required to make every node have exactly one coin."),
    N.divider(),
]

# ── Solution 1 — Post-order DFS (Optimal / Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Post-order DFS: Excess Flow (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'which coins go where?', ask 'how many coins cross each edge?'. In a tree there is exactly one path between any two nodes — so coin flow is deterministic. Count coins crossing each edge; that's the number of moves."),
        N.h4("What Doesn't Work"),
        N.para("Simulating individual coin movements is O(n²) or worse — you'd keep scanning the tree to find and move one coin at a time. BFS processes nodes top-down (parent before children), so when visiting a node we don't yet know what its subtrees need."),
        N.h4("The Key Observation"),
        N.para("Define excess(subtree) = (coins in subtree) − (nodes in subtree). This is the net number of coins that must cross the edge above that subtree. Positive = surplus sent upward. Negative = deficit filled from above. Either way, |excess| moves happen on that edge."),
        N.h4("Building the Solution"),
        N.para("Use post-order DFS (children before parent). At each node, left = dfs(left_child) and right = dfs(right_child) give the signed excesses of each subtree. Add abs(left) + abs(right) to moves (those coins cross the left and right edges). Return node.val − 1 + left + right as this node's own excess for its parent."),
        N.callout(
            "Analogy: Each subtree is a factory. A factory with surplus ships up the supply chain. One in deficit requisitions from above. The distribution hub (parent) counts all shipments and requisitions — those are moves.",
            "🏭", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def distributeCoins(root):\n"
        "    moves = 0\n"
        "    def dfs(node):\n"
        "        nonlocal moves\n"
        "        if not node:\n"
        "            return 0\n"
        "        left  = dfs(node.left)\n"
        "        right = dfs(node.right)\n"
        "        moves += abs(left) + abs(right)\n"
        "        return node.val - 1 + left + right\n"
        "    dfs(root)\n"
        "    return moves\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("moves = 0", {"code": True}), " — global accumulator for total edge crossings (moves)"])),
    N.para(N.rich([("def dfs(node)", {"code": True}), " — inner helper that returns the signed excess of a subtree (coins − nodes)"])),
    N.para(N.rich([("nonlocal moves", {"code": True}), " — Python requires this to mutate the enclosing scope variable from within the nested function"])),
    N.para(N.rich([("if not node: return 0", {"code": True}), " — base case: null child has 0 coins and 0 demand, contributes nothing"])),
    N.para(N.rich([("left  = dfs(node.left)", {"code": True}), " — post-order: recurse left subtree FIRST, get its signed excess"])),
    N.para(N.rich([("right = dfs(node.right)", {"code": True}), " — then recurse right subtree, get its signed excess"])),
    N.para(N.rich([("moves += abs(left) + abs(right)", {"code": True}), " — coins crossing left edge + coins crossing right edge = moves contributed by this node's two child edges"])),
    N.para(N.rich([("return node.val - 1 + left + right", {"code": True}), " — this subtree's excess: own coins minus 1 reserved for self, plus children's net supply/demand flowing up"])),
    N.para(N.rich([("dfs(root)", {"code": True}), " — trigger the traversal; root has no parent edge, so its return value is intentionally discarded"])),
    N.para(N.rich([("return moves", {"code": True}), " — total minimum moves across all edges in the tree"])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Repeated Single-coin Moves"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct interpretation: repeatedly find a node with more than 1 coin, find a neighbor with fewer than 1, and move one coin. Count moves until stable."),
        N.h4("What Doesn't Work"),
        N.para("This approach requires multiple full tree scans — O(n) per scan, and potentially O(n) scans in the worst case (e.g., all coins at one node, all others at 0). Total O(n²) or worse. Not acceptable for interviews."),
        N.h4("The Key Observation"),
        N.para("This is purely illustrative — it confirms the answer is correct but is far too slow. The post-order approach replaces repeated simulation with a single O(n) pass by computing edge flows analytically."),
        N.h4("Building the Solution"),
        N.para("Use BFS/DFS to repeatedly find over-stocked and under-stocked adjacent pairs, move one coin, increment counter. Repeat until all nodes have exactly 1 coin. Terminate when stable."),
    ]),
    N.h3("Code"),
    N.code(
        "# Brute-force for illustration — O(n^2) time, NOT recommended\n"
        "def distributeCoins_brute(root):\n"
        "    from collections import deque\n"
        "    moves = 0\n"
        "    def get_nodes(node):\n"
        "        if not node: return []\n"
        "        return [node] + get_nodes(node.left) + get_nodes(node.right)\n"
        "    nodes = get_nodes(root)\n"
        "    changed = True\n"
        "    while changed:\n"
        "        changed = False\n"
        "        for node in nodes:\n"
        "            for child in [node.left, node.right]:\n"
        "                if child and node.val > 1 and child.val == 0:\n"
        "                    node.val -= 1; child.val += 1; moves += 1; changed = True\n"
        "                elif child and child.val > 1 and node.val == 0:\n"
        "                    child.val -= 1; node.val += 1; moves += 1; changed = True\n"
        "    return moves\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("get_nodes(node)", {"code": True}), " — collect all tree nodes into a flat list via DFS"])),
    N.para(N.rich([("while changed:", {"code": True}), " — keep scanning until no more coins can be moved"])),
    N.para(N.rich([("if node.val > 1 and child.val == 0:", {"code": True}), " — parent has surplus, child has deficit — transfer one coin"])),
    N.para(N.rich([("elif child.val > 1 and node.val == 0:", {"code": True}), " — child has surplus, parent has deficit — transfer one coin upward"])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Post-order DFS (Optimal)", "O(n)", "O(h)"],
        ["Brute Force", "O(n²+)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS: Postorder (Post-order Excess Flow)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves aggregating a resource (coins, distances) across tree edges\n"
        "• 'Minimum moves/transfers to equalize something across a tree'\n"
        "• A node's contribution to the answer depends on its children's computed values\n"
        "• Bottom-up computation: each subtree reports a value to its parent\n"
        "• The phrase 'one move per edge crossing' appears",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Post-order DFS / bottom-up subtree aggregation pattern:"),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard) — Post-order; return max gain upward; track global max using both children simultaneously."])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), " (Easy) — Post-order; return max depth; global diameter = max(left_depth + right_depth) seen at each node."])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), " (Easy) — Post-order; return height; check |left_h − right_h| ≤ 1 at each node before bubbling height up."])),
    N.bullet(N.rich([("Lowest Common Ancestor of Binary Tree", {"bold": True}), " (Medium) — Post-order; children report if they found p or q; parent decides if it becomes the LCA."])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}), " (Hard) — Two-pass DFS; first pass uses exact same subtree coin/node counting pattern as this problem."])),
    N.bullet(N.rich([("Delete Nodes and Return Forest", {"bold": True}), " (Medium) — Post-order; decide per node whether to detach subtrees based on children's results."])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), " (Medium) — Post-order with backtracking; accumulate path sums bottom-up, report valid root-to-leaf paths."])),
    N.para("These problems all share the core technique: process children first (post-order), let each subtree return a meaningful value upward, accumulate the global answer as you go."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 11: Tree Traversals → DFS: Postorder", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("Blocks appended.")
print("NOTION OK", PAGE_ID)
