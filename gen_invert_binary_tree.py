"""gen_invert_binary_tree.py — Regenerate Notion page for Invert Binary Tree (#226)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8117-8b3a-d220b5126b2d"

# ── 1) Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=226,
    pattern="Trees",
    subpatterns=["Swap Children"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Swap left and right children at every node; recurse postorder on each subtree.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build full body ─────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, invert the tree (produce its mirror image), and return its root. "
         "Every node's left and right children must be swapped — recursively, all the way down to the leaves.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Recursive DFS (Interview Pick)
SOL1_CODE = """\
def invertTree(root):
    if root is None:
        return None
    invertTree(root.left)    # mirror the left subtree
    invertTree(root.right)   # mirror the right subtree
    root.left, root.right = root.right, root.left  # swap
    return root"""

blocks += [
    N.h2("Solution 1 — Recursive DFS Postorder (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need every node in the tree to have its left and right children exchanged. "
               "Not just the root — every single node. That's the entire definition of a mirror image."),
        N.h4("What Doesn't Work"),
        N.para("You can't just swap the root's two children and call it done — the subtrees "
               "themselves are still in their original un-mirrored form. You'd get the outer "
               "shell mirrored but the insides wrong."),
        N.h4("The Key Observation"),
        N.para("Each subtree is itself a binary tree — the same problem, just smaller. "
               "This screams recursion: if we can invert any subtree, we can invert the whole tree "
               "by inverting both halves and then swapping them at the root."),
        N.h4("Building the Solution"),
        N.para("Base case: null node is already its own mirror — return None. "
               "Recursive step: (1) invert the left subtree, (2) invert the right subtree, "
               "(3) swap the two now-mirrored subtrees at the current node. "
               "The call stack handles all the bookkeeping automatically."),
        N.callout(
            "Analogy: Flipping a book open to the middle, then flipping each half individually. "
            "Each flip is the same action — just applied to a smaller portion.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("def invertTree(root):", {"code": True}),
                   (" — function signature; takes a TreeNode or None, returns the same.", {})])),
    N.para(N.rich([("if root is None: return None", {"code": True}),
                   (" — base case: null node is trivially its own mirror. Also handles all leaves' None-children.", {})])),
    N.para(N.rich([("invertTree(root.left)", {"code": True}),
                   (" — recursive leap of faith: assume this correctly mirrors the entire left subtree.", {})])),
    N.para(N.rich([("invertTree(root.right)", {"code": True}),
                   (" — same for the right subtree. Both are now fully mirrored when these calls return.", {})])),
    N.para(N.rich([("root.left, root.right = root.right, root.left", {"code": True}),
                   (" — Python tuple swap (atomic, no temp variable). Places the two mirrored subtrees in their mirror positions.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — CRITICAL: return the node. Callers (and LeetCode) need the reference. Omitting this returns None from every frame.", {})])),
    N.divider(),
]

# Solution 2 — Iterative BFS
SOL2_CODE = """\
from collections import deque

def invertTree(root):
    if not root:
        return None
    q = deque([root])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    return root"""

blocks += [
    N.h2("Solution 2 — Iterative BFS (Queue)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Visit every node and swap its children. The traversal order doesn't matter "
               "for correctness — only that every node is visited exactly once."),
        N.h4("What Doesn't Work"),
        N.para("Using a regular Python list with pop(0) for the queue is O(n) per dequeue "
               "— O(n²) total. Always use collections.deque for O(1) popleft."),
        N.h4("The Key Observation"),
        N.para("BFS naturally visits every node once. For each dequeued node: swap its children, "
               "then enqueue the (already-swapped) non-null children for later processing. "
               "No recursion stack means no stack overflow risk for deep trees."),
        N.h4("Building the Solution"),
        N.para("Seed the queue with the root. Loop: dequeue a node, swap its children immediately, "
               "enqueue non-null children. When queue is empty, every node has been swapped. Return root."),
        N.callout("Use this when: tree depth could be very large (>10^4 nodes in a skewed chain) "
                  "and Python's default recursion limit of 1000 frames could be hit.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}),
                   (" — deque gives O(1) popleft. Using list.pop(0) would be O(n) per call.", {})])),
    N.para(N.rich([("if not root: return None", {"code": True}),
                   (" — guard for empty tree input.", {})])),
    N.para(N.rich([("q = deque([root])", {"code": True}),
                   (" — initialize queue with just the root; we'll process level-by-level.", {})])),
    N.para(N.rich([("node = q.popleft()", {"code": True}),
                   (" — dequeue from the front (BFS order).", {})])),
    N.para(N.rich([("node.left, node.right = node.right, node.left", {"code": True}),
                   (" — swap children at this node immediately.", {})])),
    N.para(N.rich([("if node.left/right: q.append(...)", {"code": True}),
                   (" — enqueue non-null children for processing. Only enqueue after the swap, so children are in their new positions.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — root value is unchanged; its subtrees are now mirrored.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Recursive DFS (Interview Pick)", "O(n)", "O(h)", "h=O(log n) balanced, O(n) skewed"],
        ["Iterative BFS", "O(n)", "O(w)", "w=max width; O(n) for perfect binary tree"],
        ["Iterative DFS (explicit stack)", "O(n)", "O(h)", "Same as recursive, explicit stack object"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Swap Children (DFS Postorder)", {})])),
    N.callout(
        "When to recognize this pattern: 'Mirror', 'invert', or 'flip' a tree — swap children at each node via DFS. "
        "Also: 'apply operation to every node' → DFS or BFS. "
        "If result requires a subtree to be fully processed before modifying the parent → postorder DFS.",
        "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Swap Children / Tree DFS):"),
    N.bullet(N.rich([("Symmetric Tree", {"bold": True}),
                     (" (Easy) — Check if tree is its own mirror without modifying it; parallel DFS on both halves (#101)", {})])),
    N.bullet(N.rich([("Flip Equivalent Binary Trees", {"bold": True}),
                     (" (Medium) — Determine if one tree can become another via selective child swaps (#951)", {})])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}),
                     (" (Easy) — Same DFS skeleton; return max(left_depth, right_depth) + 1 at each node (#104)", {})])),
    N.bullet(N.rich([("Same Tree", {"bold": True}),
                     (" (Easy) — Check structural and value equality using parallel recursive DFS (#100)", {})])),
    N.bullet(N.rich([("Merge Two Binary Trees", {"bold": True}),
                     (" (Easy) — Combine two trees by visiting corresponding nodes simultaneously (#617)", {})])),
    N.para("These problems all share the same core technique: recurse over tree nodes with DFS, applying a local operation (swap, compare, merge) at each node."),
    N.callout("📚 Reference: Trees section (Swap Children sub-pattern)", "📚", "gray_background"),
]

# Visual Explainer embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("invert_binary_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
