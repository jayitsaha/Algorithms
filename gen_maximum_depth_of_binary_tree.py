"""gen_maximum_depth_of_binary_tree.py — Notion updater for LeetCode #104."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8169-83a1-ed83d77e2ef5"
SLUG    = "maximum_depth_of_binary_tree"

# ── 1) Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Easy",
    number      = 104,
    pattern     = "Trees",
    subpatterns = ["DFS: Postorder"],
    tc          = "O(n)",
    sc          = "O(h)",
    key_insight = "Depth = 1 + max(left_depth, right_depth); postorder DFS bubbles results bottom-up.",
    icon        = "🟢",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return its ", {}),
        ("maximum depth", {"bold": True}),
        (" — the number of nodes along the longest path from the root node down to the farthest leaf node. A leaf is a node with no children. An empty tree has depth 0.", {}),
    ])),
    N.para("Example: root = [3, 9, 20, null, null, 15, 7] → Output: 3  (path: 3 → 20 → 15 or 3 → 20 → 7)"),
    N.divider(),
]

# ── Solution 1: Recursive DFS (Postorder) ─────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive DFS Postorder (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Forget about traversal order for a moment. Ask: what does the depth of a tree depend on? It depends on which subtree is deeper. Every node is the 'root' of its own subtree, so every node asks the same question recursively. This is the recursive substructure of the problem."),
        N.h4("What Doesn't Work"),
        N.para("You might try to count nodes level-by-level yourself — but that forces you to manage a queue, track levels, and write ~15 lines. Or you might try a single DFS that accumulates a running depth counter — but that requires tracking max globally, and it's easy to get off-by-one errors with the counter."),
        N.h4("The Key Observation"),
        N.para("The depth of any node N = 1 (for N itself) + the depth of whichever subtree is taller. This recurrence has a clean base case: an empty subtree has depth 0. Write the recurrence → you have the code."),
        N.h4("Building the Solution"),
        N.para("Step 1: Base case — if root is None, return 0. Step 2: Recurse left → get left subtree depth. Step 3: Recurse right → get right subtree depth. Step 4: Return 1 + max(left, right). The traversal is postorder: children are processed before the parent."),
        N.callout("Analogy: Think of the tree as a building. The height of the building is 1 (ground floor you're on) plus the height of the taller wing. Each wing asks the same question recursively. Leaves are single-floor rooms.", "🏢", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef maxDepth(root: Optional[TreeNode]) -> int:\n    if root is None:               # base case: empty subtree\n        return 0\n    left  = maxDepth(root.left)    # depth of left subtree\n    right = maxDepth(root.right)   # depth of right subtree\n    return 1 + max(left, right)    # +1 for this node; take deeper side"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if root is None: return 0", {"code": True}), (" — Base case. If the current node doesn't exist, the subtree is empty and has depth 0. Also handles input of an empty tree.", {})])),
    N.para(N.rich([("left = maxDepth(root.left)", {"code": True}), (" — Recurse into the left child. The call returns the maximum depth of the entire left subtree as an integer.", {})])),
    N.para(N.rich([("right = maxDepth(root.right)", {"code": True}), (" — Recurse into the right child. Same operation — returns the max depth of the right subtree.", {})])),
    N.para(N.rich([("return 1 + max(left, right)", {"code": True}), (" — The 1 counts the current node itself. max() picks whichever subtree is deeper — that determines the longest path going through this node.", {})])),
    N.divider(),
]

# ── Solution 2: BFS Level Order ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative BFS (Level Order)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of the tree level by level: root is level 1, root's children are level 2, etc. The maximum depth equals the total number of levels. If we can count levels during a BFS traversal, we have our answer."),
        N.h4("What Doesn't Work"),
        N.para("A naive BFS that just dequeues nodes won't naturally separate levels — all nodes get mixed together. We need to know when one level ends and the next begins."),
        N.h4("The Key Observation"),
        N.para("At the start of each BFS iteration, len(queue) tells us exactly how many nodes are on the current level. Process that many nodes (dequeue their count), enqueue their children, then increment depth. This snapshot trick perfectly separates levels."),
        N.h4("Building the Solution"),
        N.para("Initialize queue with root, depth=0. While queue: snapshot level_size = len(queue), process that many nodes (enqueue children), increment depth. Return depth when queue empties."),
        N.callout("When to prefer BFS: if the tree could be extremely deep (e.g. 10^5 chained nodes), Python's recursion limit (~1000 frames by default) would cause a RecursionError with the DFS approach. BFS avoids this by using an explicit deque.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\nfrom typing import Optional\n\ndef maxDepth(root: Optional[TreeNode]) -> int:\n    if not root:\n        return 0\n    queue, depth = deque([root]), 0\n    while queue:\n        for _ in range(len(queue)):   # process one level at a time\n            node = queue.popleft()\n            if node.left:  queue.append(node.left)\n            if node.right: queue.append(node.right)\n        depth += 1                    # finished one full level\n    return depth"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("queue, depth = deque([root]), 0", {"code": True}), (" — Initialize the BFS queue with the root; depth counter starts at 0.", {})])),
    N.para(N.rich([("for _ in range(len(queue))", {"code": True}), (" — Snapshot trick: at the start of each outer loop, len(queue) is exactly the number of nodes on the current level. We drain that many before incrementing depth.", {})])),
    N.para(N.rich([("if node.left: queue.append(node.left)", {"code": True}), (" — Enqueue children for the next level. Only enqueue non-null children (avoids sentinel None values in the queue).", {})])),
    N.para(N.rich([("depth += 1", {"code": True}), (" — We've fully processed one level — increment depth once per level, not once per node.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                  "Time",  "Space"],
        ["Recursive DFS (postorder)", "O(n)",  "O(h) — recursion stack, h = tree height"],
        ["Iterative BFS (level order)","O(n)", "O(w) — queue holds widest level, w can be O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS: Postorder", {}), (" — compute children before parent (bottom-up aggregation)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Maximum depth / height / size of a tree'\n"
        "• 'Check if tree is balanced / symmetric'\n"
        "• 'Compute a property that depends on subtrees'\n"
        "• Any bottom-up aggregation: the parent's answer is a function of its children's answers",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same DFS Postorder / Tree Height technique:"),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), (" (Easy) — Postorder: check |left_h - right_h| ≤ 1 at every node; return -1 as sentinel to short-circuit (#110)", {})])),
    N.bullet(N.rich([("Minimum Depth of Binary Tree", {"bold": True}), (" (Easy) — Similar but must reach actual leaf; single-child nodes need special handling (#111)", {})])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), (" (Easy) — At each node track left_h + right_h as candidate diameter; same postorder shape as depth (#543)", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Postorder with gain tracking; max contribution = max(0, left_gain) + max(0, right_gain) + val (#124)", {})])),
    N.bullet(N.rich([("Invert Binary Tree", {"bold": True}), (" (Easy) — Postorder swap: recurse into children, then swap them at the parent (#226)", {})])),
    N.bullet(N.rich([("Count Complete Tree Nodes", {"bold": True}), (" (Medium) — Postorder leverages height comparison for O(log²n) solution (#222)", {})])),
    N.para("These problems all share the same core technique: postorder DFS where the parent's answer is computed from both children's returned values."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section · Sub-Pattern: DFS: Postorder · Source: Guide Trees section + Analysis", "📚", "gray_background"),
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the recursive DFS — watch depths bubble up from leaves to root with each Next press.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
