"""
gen_construct_binary_tree_from_inorder_and_postorder_traversal.py
Regenerates the Notion page for LeetCode #106.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811e-bfc6-fbe352083e3b"
SLUG = "construct_binary_tree_from_inorder_and_postorder_traversal"

# ── 1. Properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=106,
    pattern="Trees",
    subpatterns=["Build Right Subtree First"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Last element of postorder is the root; find it in inorder to split left vs right subtrees recursively.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build new body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("inorder", {"code": True}),
        (" and ", {}),
        ("postorder", {"code": True}),
        (" representing the inorder and postorder traversal of a binary tree, construct and return the binary tree.", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ n ≤ 3000. ", {}),
        ("All values in ", {}),
        ("inorder", {"code": True}),
        (" and ", {}),
        ("postorder", {"code": True}),
        (" are unique. Both arrays represent the traversals of the same binary tree.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Naive
blocks += [
    N.h2("Solution 1 — Naive Recursive with Array Slicing (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to rebuild a tree from two traversal sequences. Think of it as: each array encodes the tree from a different angle. Can we extract the root at each level and recurse?"),
        N.h4("What Doesn't Work"),
        N.para("We cannot reconstruct from postorder alone — we'd know roots but not whether children are left or right. We cannot reconstruct from inorder alone — we'd know left/right groups but not which element is root. We need both."),
        N.h4("The Key Observation"),
        N.para("Postorder always ends with the root: [left nodes] [right nodes] ROOT. So postorder[-1] is always the root of the current subtree. Once we have the root, we find it in inorder — everything left of it is the left subtree, everything right is the right subtree."),
        N.h4("Building the Solution"),
        N.para("Base case: empty arrays → return None. Extract root from postorder[-1]. Find its index in inorder (call it mid). Left subtree gets inorder[:mid] and postorder[:mid]. Right subtree gets inorder[mid+1:] and postorder[mid:-1]. Recurse on both."),
        N.callout("Analogy: Imagine peeling the last layer of an onion (postorder root), then using the exposed pattern (inorder) to identify left and right halves. Repeat on each half.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def buildTree(inorder, postorder):
    if not inorder or not postorder:
        return None
    root_val = postorder[-1]          # last elem = current root
    root = TreeNode(root_val)
    mid = inorder.index(root_val)     # O(n) scan — bottleneck
    root.left  = buildTree(inorder[:mid], postorder[:mid])
    root.right = buildTree(inorder[mid+1:], postorder[mid:-1])
    return root"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if not inorder or not postorder", {"code": True}), (" — Base case: empty subtree returns None (leaf's children, or completely empty tree).", {})])),
    N.para(N.rich([("root_val = postorder[-1]", {"code": True}), (" — The last element of postorder is always the root of the current subtree. This is the defining property of postorder traversal.", {})])),
    N.para(N.rich([("mid = inorder.index(root_val)", {"code": True}), (" — Linear O(n) scan to find root's position in inorder. This is the O(n²) bottleneck — repeated at each level.", {})])),
    N.para(N.rich([("root.left = buildTree(inorder[:mid], postorder[:mid])", {"code": True}), (" — Left inorder slice has mid elements; left postorder slice also has exactly mid elements (same node count).", {})])),
    N.para(N.rich([("root.right = buildTree(inorder[mid+1:], postorder[mid:-1])", {"code": True}), (" — Right inorder excludes root; right postorder excludes the first mid elements (left nodes) and the last element (current root).", {})])),
    N.divider(),
]

# Solution 2 — Optimal
blocks += [
    N.h2("Solution 2 — HashMap + Index Pointers (O(n) — Interview Pick) ✓"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The naive approach is correct but slow because .index() scans the entire inorder array at each level. Can we precompute inorder positions?"),
        N.h4("What Doesn't Work"),
        N.para("Simply memoizing .index() results helps but doesn't eliminate the O(n²) array copying from slicing. We need to eliminate both the scan AND the copies."),
        N.h4("The Key Observation"),
        N.para("If we precompute a val→index hash map for inorder, each lookup is O(1). Then instead of slicing arrays, we pass index boundaries (in_left, in_right). For postorder, we maintain a single mutable pointer that decrements as we consume roots — going right-to-left mirrors the reverse postorder sequence."),
        N.h4("Building the Solution"),
        N.para("Precompute idx_map. Use post_idx as a pointer starting at len-1. In each call: if window is empty return None; consume postorder[post_idx] as root, decrement post_idx; find mid = idx_map[root_val]; recurse RIGHT first (to consume postorder in correct order), then LEFT."),
        N.callout("The right-first recursion is the key trick: reading postorder backwards gives Root, Right subtree roots, Left subtree roots. Recursing right first keeps post_idx aligned with this reversed order.", "🔑", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code("""def buildTree(inorder, postorder):
    idx_map = {v: i for i, v in enumerate(inorder)}  # O(n) precompute
    post_idx = [len(postorder) - 1]  # mutable pointer (list for closure mutation)

    def build(in_left, in_right):
        if in_left > in_right:
            return None
        root_val = postorder[post_idx[0]]  # consume root from right-to-left
        post_idx[0] -= 1
        root = TreeNode(root_val)
        mid = idx_map[root_val]            # O(1) lookup
        root.right = build(mid + 1, in_right)  # RIGHT FIRST!
        root.left  = build(in_left, mid - 1)
        return root

    return build(0, len(inorder) - 1)"""),
    N.h3("Line by Line"),
    N.para(N.rich([("idx_map = {v: i for i, v in enumerate(inorder)}", {"code": True}), (" — Build val→inorder_index map in O(n). All future lookups are O(1) instead of O(n).", {})])),
    N.para(N.rich([("post_idx = [len(postorder) - 1]", {"code": True}), (" — Mutable pointer wrapped in a list so the nested function can decrement it (Python closure mutation requires mutable container or nonlocal).", {})])),
    N.para(N.rich([("if in_left > in_right: return None", {"code": True}), (" — Empty window means no node here. This handles leaf children and empty subtrees.", {})])),
    N.para(N.rich([("root_val = postorder[post_idx[0]]; post_idx[0] -= 1", {"code": True}), (" — Read and consume the current root from postorder, right-to-left. Each call gets the next root in reverse postorder.", {})])),
    N.para(N.rich([("mid = idx_map[root_val]", {"code": True}), (" — O(1) lookup of root's inorder index. This is what makes the algorithm O(n) overall.", {})])),
    N.para(N.rich([("root.right = build(mid+1, in_right)", {"code": True}), (" — Recurse RIGHT before left. Reversed postorder gives us right subtree roots next, so we must consume them first.", {})])),
    N.para(N.rich([("root.left = build(in_left, mid-1)", {"code": True}), (" — Then recurse left. The postorder pointer is now pointing at the left subtree's roots.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursive (slicing + .index)", "O(n²)", "O(n²)"],
        ["HashMap + Index Pointers (Interview Pick)", "O(n)", "O(n)"],
        ["Iterative with Stack", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Build Right Subtree First (reading postorder right-to-left while recursing right before left)", {})])),
    N.callout(
        "When to recognize this pattern: Problem gives you two traversals of a binary tree and asks you to reconstruct it. Key signal: 'given inorder and postorder/preorder.' The traversal that puts root first (preorder) or last (postorder) identifies the root; inorder splits left from right.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Inorder Traversal", {"bold": True}), (" (Medium) — Mirror problem; first element of preorder is root (#105)", {})])),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Postorder Traversal", {"bold": True}), (" (Medium) — Not uniquely solvable; combine first preorder + last postorder (#889)", {})])),
    N.bullet(N.rich([("Serialize and Deserialize Binary Tree", {"bold": True}), (" (Hard) — Encode/decode any binary tree — reconstruct-from-encoding theme (#297)", {})])),
    N.bullet(N.rich([("Maximum Binary Tree", {"bold": True}), (" (Medium) — Divide-and-conquer: max element is root, recurse on halves (#654)", {})])),
    N.bullet(N.rich([("Binary Tree Inorder Traversal", {"bold": True}), (" (Easy) — Foundation: understand inorder before using it to reconstruct (#94)", {})])),
    N.bullet(N.rich([("Recover Binary Search Tree", {"bold": True}), (" (Medium) — Exploit that inorder of BST must be sorted; find swapped nodes (#99)", {})])),
    N.para("These problems share the core technique of using traversal order to identify roots and recursively partition subtrees."),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
