"""
gen_binary_tree_cameras.py — Notion page builder for Binary Tree Cameras (#968).
Run from the Algorithms/ directory alongside notion_lib.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "binary_tree_cameras"
PAGE_ID = None   # null → create new page

# ─── Step 0: Create the page (since PAGE_ID is None) ───
print("Creating new Notion page for Binary Tree Cameras...")
PAGE_ID = N.create_page("Binary Tree Cameras", 968, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ─── Step 1: Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=968,
    pattern="Dynamic Programming",
    subpatterns=["Post-order 3 States", "DP: Tree"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Post-order DFS with 3 states per node: 0=not covered, 1=has camera, 2=covered. Greedily place camera when a child is uncovered; null nodes return 2 (covered).",
    icon="🔴",
    status="Solved",
    source="LeetCode"
)
print("Properties set.")

# ─── Step 2: Build page body ───
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary tree, return the minimum number of cameras needed to monitor every node. A camera at node ", {}),
        ("X", {"code": True}),
        (" covers ", {}),
        ("X", {"code": True}),
        (" itself, its parent, and its direct children. You may install cameras on any subset of nodes.", {})
    ])),
    N.para("Constraints: 1 ≤ nodes ≤ 1000. Node values are 0. Note: null children do NOT need to be monitored — only actual tree nodes must be covered."),
    N.divider(),
]

# ── Solution 1: Post-order Tree DP (Interview Pick) ──
solution1_code = """\
def minCameraCover(root) -> int:
    cameras = 0           # nonlocal counter

    def dfs(node):
        nonlocal cameras
        if node is None:
            return 2      # null = treated as "covered"; no monitoring needed

        left  = dfs(node.left)   # post-order: process left subtree first
        right = dfs(node.right)  # then right subtree

        if left == 0 or right == 0:
            # A child is uncovered — MUST place camera here (greedy)
            cameras += 1
            return 1      # state 1: this node has a camera

        if left == 1 or right == 1:
            # A child has a camera — this node is covered by it
            return 2      # state 2: covered (no camera needed here)

        # Both children are covered (state 2) but no camera — this node is NOT covered
        return 0          # state 0: not covered, signal parent to rescue

    if dfs(root) == 0:
        # Root has no parent; if it's not covered, install final camera
        cameras += 1
    return cameras"""

solution1_linebyelline = [
    N.para(N.rich([("cameras = 0", {"code": True}), (" — Nonlocal integer counter. We use nonlocal so the inner function dfs() can mutate it.", {})])),
    N.para(N.rich([("def dfs(node)", {"code": True}), (" — Inner DFS function. Returns an integer state (0, 1, or 2) for the given node.", {})])),
    N.para(N.rich([("if node is None: return 2", {"code": True}), (" — Base case. Null nodes are conceptually 'already covered'; returning 2 prevents us from ever installing a camera to cover a null child.", {})])),
    N.para(N.rich([("left = dfs(node.left)", {"code": True}), (" — Post-order: recurse into the left subtree. We now know the state of the entire left subtree.", {})])),
    N.para(N.rich([("right = dfs(node.right)", {"code": True}), (" — Recurse into the right subtree. Both children are now resolved before we act.", {})])),
    N.para(N.rich([("if left == 0 or right == 0", {"code": True}), (" — The greedy condition: if ANY child is uncovered (state 0), we MUST place a camera at the current node. This is the earliest efficient placement — the camera simultaneously covers the current node, the uncovered child, and the parent above.", {})])),
    N.para(N.rich([("cameras += 1; return 1", {"code": True}), (" — Install camera. Return state 1 to signal our parent that we have a camera (so the parent is covered).", {})])),
    N.para(N.rich([("if left == 1 or right == 1", {"code": True}), (" — If any child has a camera, it covers us. We are 'covered' (state 2). No camera needed here.", {})])),
    N.para(N.rich([("return 2", {"code": True}), (" — State 2: covered. We pass a 'don't worry about me' signal upward. The parent can freely return state 0 if it too has no camera children.", {})])),
    N.para(N.rich([("return 0", {"code": True}), (" — Fall-through: both children are in state 2 (covered, no cameras), so no camera reaches us. We are NOT covered. Signal upward so our parent can place a camera.", {})])),
    N.para(N.rich([("if dfs(root) == 0: cameras += 1", {"code": True}), (" — Root edge case: the root has no parent. If it's uncovered after the full DFS, we must place the final camera at the root itself.", {})])),
    N.para(N.rich([("return cameras", {"code": True}), (" — Final answer: total cameras placed.", {})])),
]

intuition1_children = [
    N.h4("Reframe the Problem"),
    N.para("We need to cover every node with minimum cameras. A camera covers 3 levels: the node itself, its parent, and its children. The question becomes: where should we NOT place cameras to minimize their total number?"),
    N.h4("What Doesn't Work"),
    N.para("Brute force — try every subset of nodes as camera positions, verify coverage, track minimum — is O(2^n) and completely infeasible for n=1000. A greedy top-down approach fails because you don't know yet whether children will 'rescue' the current node with a camera."),
    N.h4("The Key Observation"),
    N.para("Cameras are most efficient when placed ABOVE leaves, not at leaves. A camera at a leaf covers only 2 nodes (itself + parent). A camera at the parent of two leaves covers 4 nodes (itself + parent + 2 children). So: never eagerly place a camera at a leaf — let the leaf bubble state 0 up to its parent, forcing the parent to install."),
    N.h4("Building the Solution"),
    N.para("Encode this greedy bottom-up rule as a post-order DFS returning 3 states. State 0 = 'I'm uncovered, parent must act.' State 1 = 'I have a camera, I cover my parent.' State 2 = 'I'm covered, parent need not worry.' Process null nodes as state 2 so leaves never install a camera for their null children."),
    N.callout("Analogy: Think of the tree as a security guard staffing problem. Guards at ground level (leaves) can only protect a small area. Guards at supervisor nodes (internal nodes) protect a larger radius. Hire supervisors first — they're more cost-effective.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Post-order Tree DP: 3 States (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition1_children),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
] + solution1_linebyelline + [N.divider()]

# ── Solution 2: Greedy Iterative (Bottom-up BFS order) ──
solution2_code = """\
from collections import defaultdict

def minCameraCover(root) -> int:
    # Build parent map + post-order traversal order
    parent = {root: None}
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # Process in reverse (post-order) using sets
    covered = set([None])   # null is always covered
    has_camera = set()
    cameras = 0

    for node in reversed(order):
        if (node.left not in covered or node.right not in covered):
            # A child is uncovered — place camera here
            cameras += 1
            has_camera.add(node)
            covered.add(node)
            if parent[node]:
                covered.add(parent[node])
            if node.left:  covered.add(node.left)
            if node.right: covered.add(node.right)
        elif node in has_camera:
            covered.add(node)
            if parent[node]:
                covered.add(parent[node])

    # Check root
    if root not in covered:
        cameras += 1

    return cameras"""

intuition2_children = [
    N.h4("Reframe the Problem"),
    N.para("Same greedy rule, but implemented iteratively using explicit post-order traversal and set-based coverage tracking instead of recursive state returns."),
    N.h4("What Doesn't Work"),
    N.para("For very deep trees (e.g., n=1000, path-like), recursion could hit Python's recursion limit (~1000). The iterative version avoids this risk."),
    N.h4("The Key Observation"),
    N.para("We can replicate post-order processing by reversing the DFS traversal order (pre-order reversed ≈ post-order). Use sets to track which nodes are covered and which have cameras."),
    N.h4("Building the Solution"),
    N.para("Build a parent map and a pre-order traversal. Process in reverse (simulating post-order). Use 'covered' and 'has_camera' sets. The logic mirrors the recursive solution exactly."),
]

blocks += [
    N.h2("Solution 2 — Iterative Greedy (Explicit Stack, Avoids Recursion Limit)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition2_children),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = {root: None}", {"code": True}), (" — Track each node's parent for the 'cover parent' step when placing a camera.", {})])),
    N.para(N.rich([("order = []; stack = [root]", {"code": True}), (" — Collect nodes in pre-order (root → left → right).", {})])),
    N.para(N.rich([("for node in reversed(order)", {"code": True}), (" — Reversed pre-order approximates post-order: leaves appear before their parents.", {})])),
    N.para(N.rich([("covered = set([None])", {"code": True}), (" — Null is pre-covered; same logic as 'if node is None: return 2' in the recursive version.", {})])),
    N.para(N.rich([("if node.left not in covered or node.right not in covered", {"code": True}), (" — Equivalent to 'left==0 or right==0': a child is uncovered → install camera here.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                     "Time",     "Space"],
        ["Recursive Post-order (3 States)", "O(n)",  "O(h)"],
        ["Iterative Greedy (Sets)",         "O(n)",  "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming (Tree DP)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Post-order 3 States, DP: Tree", {})])),
    N.callout(
        "When to recognize this pattern: binary tree + optimization (min/max cameras/cost) + each node's decision depends on both children's resolved state → post-order DFS with state return. The 3-state design (not covered / has camera / covered by child) is the minimal information needed to propagate correct greedy decisions upward.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Tree DP / Post-order State Propagation):"),
    N.bullet(N.rich([("House Robber III", {"bold": True}), (" (Medium) — Return (rob, not_rob) pair per node; maximum money without robbing adjacent nodes. Same Tree DP post-order pattern. (#337)", {})])),
    N.bullet(N.rich([("Distribute Coins in Binary Tree", {"bold": True}), (" (Medium) — Post-order: return net excess coins per subtree; accumulate absolute flows. (#979)", {})])),
    N.bullet(N.rich([("Delete Nodes and Return Forest", {"bold": True}), (" (Medium) — Post-order with parent-context set; conditionally detach and collect subtree roots. (#1110)", {})])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), (" (Easy) — Post-order returning height; update global diameter at each node as left_h + right_h. (#543)", {})])),
    N.bullet(N.rich([("Largest BST Subtree", {"bold": True}), (" (Medium) — Post-order returning (size, min, max) tuple to validate BST property bottom-up. (#333)", {})])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), (" (Medium) — Post-order pointer rewiring; process right → left → root. (#114)", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Post-order: max gain from left/right, update global max at each node. (#124)", {})])),
    N.para("These problems share the core technique: post-order DFS where each node returns a compact state/value representing the optimal solution for its subtree, and the parent uses those values to make the locally greedy decision."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → Tree DP). Sub-Pattern: Post-order 3 States · Source: Guide Section 18.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the post-order traversal: leaves first, then their parent receives their states and makes the greedy camera decision.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Step 3: Append all blocks ───
print(f"Appending {len(blocks)} blocks to page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("Blocks appended successfully.")
print(f"NOTION OK {PAGE_ID}")
