"""
Notion updater for: Boundary of Binary Tree (LeetCode #545)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81d7-82f5-c8dee7d7c732"
SLUG = "boundary_of_binary_tree"

# ── Step 1: Set page properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=545,
    pattern="Trees",
    subpatterns=["Left Boundary + Leaves + Right"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Decompose boundary into three independent passes: left boundary (non-leaves top-down), all leaves (DFS left-to-right), right boundary (non-leaves top-down, reversed).",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── Step 3: Build body blocks ──
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the values of its ", {}),
        ("boundary", {"bold": True}),
        (" in anti-clockwise direction starting from the root. ", {}),
        ("The boundary includes the left boundary, the leaves, and the right boundary in order. "
         "Specifically: (1) the left boundary is the path from the root to the leftmost leaf, "
         "excluding the leaf itself; (2) the leaves are all nodes with no children, in left-to-right "
         "order; (3) the right boundary is the path from the root to the rightmost leaf, excluding "
         "the leaf itself, listed bottom-up (reversed).", {})
    ])),
    N.divider(),
]

# ── Solution 1: Three-Pass DFS (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Three-Pass DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Trace the tree outline anti-clockwise: down the left side, across the bottom, up the right side. "
               "This suggests three distinct groups of nodes, each collected with a simple independent traversal."),
        N.h4("What Doesn't Work"),
        N.para("A single DFS trying to handle all three cases at once becomes a tangle of conditionals — "
               "it's hard to know whether you're on the left boundary, a leaf, or the right boundary "
               "from inside a generic recursive call."),
        N.h4("The Key Observation"),
        N.para("The three groups are mutually exclusive: left boundary nodes are non-leaves on the leftmost path; "
               "leaves have no children; right boundary nodes are non-leaves on the rightmost path. "
               "An is_leaf() helper separates them cleanly."),
        N.h4("Building the Solution"),
        N.para("1. Add root first. 2. Iterative left-spine descent (prefer left child, skip leaves). "
               "3. DFS to collect all leaves left-to-right. 4. Iterative right-spine descent (prefer right child, skip leaves), "
               "collect into temp list, reverse and append."),
        N.callout("Analogy: Walking around a building anti-clockwise. Left wall (not corners), "
                  "floor (all corners), right wall (not corners) going up.", "🏢", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "class TreeNode:\n"
        "    def __init__(self, val=0, left=None, right=None):\n"
        "        self.val = val; self.left = left; self.right = right\n\n"
        "def boundaryOfBinaryTree(root):\n"
        "    if not root:\n"
        "        return []\n\n"
        "    def is_leaf(n):\n"
        "        return not n.left and not n.right\n\n"
        "    res = [root.val]\n"
        "    if is_leaf(root):\n"
        "        return res  # single-node tree\n\n"
        "    # Pass 1: Left boundary (top-down, exclude leaves)\n"
        "    node = root.left\n"
        "    while node:\n"
        "        if not is_leaf(node):\n"
        "            res.append(node.val)\n"
        "        node = node.left if node.left else node.right\n\n"
        "    # Pass 2: All leaves (left-to-right DFS)\n"
        "    def add_leaves(n):\n"
        "        if not n:\n"
        "            return\n"
        "        if is_leaf(n):\n"
        "            res.append(n.val)\n"
        "            return\n"
        "        add_leaves(n.left)\n"
        "        add_leaves(n.right)\n"
        "    add_leaves(root.left)\n"
        "    add_leaves(root.right)\n\n"
        "    # Pass 3: Right boundary (top-down, then reversed)\n"
        "    right_bd = []\n"
        "    node = root.right\n"
        "    while node:\n"
        "        if not is_leaf(node):\n"
        "            right_bd.append(node.val)\n"
        "        node = node.right if node.right else node.left\n"
        "    res.extend(reversed(right_bd))\n\n"
        "    return res"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("is_leaf(n)", {"code": True}), " — True if node has no children; the key predicate used in all three passes to prevent double-counting."])),
    N.para(N.rich([("res = [root.val]", {"code": True}), " — Root always starts the boundary; it is never a leaf in this context (handled separately above)."])),
    N.para(N.rich([("node = node.left if node.left else node.right", {"code": True}), " — Prefer left child when descending the left boundary; fall back to right only if left is absent."])),
    N.para(N.rich([("add_leaves(n.left); add_leaves(n.right)", {"code": True}), " — Recurse left before right so leaves are collected in left-to-right order."])),
    N.para(N.rich([("res.extend(reversed(right_bd))", {"code": True}), " — Collecting right boundary top-down then reversing gives the bottom-up (anti-clockwise) order."])),
    N.divider(),
]

# ── Solution 2: Recursive Variant ──
blocks += [
    N.h2("Solution 2 — Recursive Flag-Passing"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Pass a flag through recursion to tell each node whether it is on the left boundary, "
               "the right boundary, or neither. Each node adds itself appropriately."),
        N.h4("The Key Observation"),
        N.para("During DFS, a node on the left boundary passes the left-boundary flag to its left child; "
               "if no left child exists, the flag passes to the right child. Symmetric for right boundary. "
               "All other nodes are either interior (skipped) or leaves (always added)."),
        N.h4("When to Use"),
        N.para("This approach unifies the three passes into one recursion, which can be elegant. "
               "However it is harder to reason about and more error-prone in interviews. "
               "The three-pass iterative approach (Solution 1) is recommended for clarity."),
    ]),
    N.h3("Code"),
    N.code(
        "def boundaryOfBinaryTree(root):\n"
        "    res = []\n\n"
        "    def dfs(node, is_left_bd, is_right_bd):\n"
        "        if not node:\n"
        "            return\n"
        "        is_lf = not node.left and not node.right\n"
        "        # Add if: left boundary node, leaf, or right boundary node\n"
        "        if is_left_bd or is_lf:\n"
        "            res.append(node.val)\n"
        "        dfs(node.left,\n"
        "            is_left_bd,\n"
        "            is_right_bd and not node.right)\n"
        "        dfs(node.right,\n"
        "            is_left_bd and not node.left,\n"
        "            is_right_bd)\n"
        "        # Right boundary: add AFTER children (post-order = bottom-up)\n"
        "        if is_right_bd and not is_lf and not is_left_bd:\n"
        "            res.append(node.val)\n\n"
        "    dfs(root, True, True)\n"
        "    return res"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("is_left_bd, is_right_bd", {"code": True}), " — Boolean flags propagated through recursion to classify each node's role in the boundary."])),
    N.para(N.rich([("if is_left_bd or is_lf: res.append(node.val)", {"code": True}), " — Left boundary nodes and leaves are added before recursing (pre-order = top-down for left boundary)."])),
    N.para(N.rich([("if is_right_bd and not is_lf and not is_left_bd: res.append(node.val)", {"code": True}), " — Right boundary nodes added AFTER children (post-order = bottom-up order naturally)."])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Three-Pass DFS (Interview Pick)", "O(n)", "O(h) recursion stack"],
        ["Recursive Flag-Passing", "O(n)", "O(h) recursion stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Left Boundary + Leaves + Right (DFS: Preorder/Postorder hybrid)"])),
    N.callout(
        "When to recognize this pattern: problem mentions boundary, outline, perimeter, or silhouette of a binary tree. "
        "Any time you need left-spine + leaf-level + right-spine nodes in a specific traversal order.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique or closely related tree traversal concepts:"),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — collect rightmost node per level; shares the right-spine descent logic"])),
    N.bullet(N.rich([("Find Bottom Left Tree Value", {"bold": True}), " (Medium) — finding the leftmost leaf via DFS; shares the left-boundary descent concept"])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — BFS for level-by-level collection; alternative approach for boundary-adjacent problems"])),
    N.bullet(N.rich([("Vertical Order Traversal of Binary Tree", {"bold": True}), " (Hard) — classify nodes by column; similar per-node categorization"])),
    N.bullet(N.rich([("Binary Tree Zigzag Level Order Traversal", {"bold": True}), " (Medium) — alternating direction traversal; related anti-clockwise/clockwise ordering"])),
    N.bullet(N.rich([("Symmetric Tree", {"bold": True}), " (Easy) — compare left and right subtrees; same structural mirroring awareness as boundary"])),
    N.para("These problems share the core technique of traversing specific structural positions of a binary tree (spines, leaves, levels)."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS sub-patterns. Sub-pattern: Left Boundary + Leaves + Right (Analysis-based classification).", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
