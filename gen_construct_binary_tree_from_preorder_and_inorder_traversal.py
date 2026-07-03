"""
Notion update script for:
  LeetCode #105 – Construct Binary Tree from Preorder and Inorder Traversal
  Page ID: 39193418-809c-81a4-aeb9-eea768113afd
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a4-aeb9-eea768113afd"
SLUG    = "construct_binary_tree_from_preorder_and_inorder_traversal"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty   = "Medium",
    number       = 105,
    pattern      = "Trees",
    subpatterns  = ["Find Root in Inorder"],
    tc           = "O(n)",
    sc           = "O(n)",
    key_insight  = "preorder[0] is always root; find it in inorder to split left/right subtrees",
    icon         = "🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("preorder", {"code": True}),
        (" and ", {}),
        ("inorder", {"code": True}),
        (" where ", {}),
        ("preorder", {"code": True}),
        (" is the preorder traversal of a binary tree and ", {}),
        ("inorder", {"code": True}),
        (" is the inorder traversal of the same tree, construct and return the binary tree. "
         "All values in the tree are unique.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Optimal – Recursive with Hash Map ──────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive with Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to rebuild a binary tree from two different 'views' of it. "
            "Think of it as: preorder gives us roots in the right order (root before its children), "
            "while inorder tells us which nodes belong to the left vs. right subtree of any given root. "
            "Together, they completely determine the tree."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: For each node, linearly scan the inorder array to find where to split. "
            "This is O(n) per node × n nodes = O(n²) total. For a tree with 10⁵ nodes, that's "
            "10¹⁰ operations — too slow. Also, creating new array slices at every recursion level "
            "adds O(n²) space overhead."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Preorder traversal visits Root → Left → Right. So preorder[0] is the root of the "
            "whole tree. After we create that root and find it in the inorder array at position mid, "
            "we know: the left subtree has exactly (mid - in_left) nodes, and those are the next "
            "(mid - in_left) elements in preorder. This is the crucial insight that lets us maintain "
            "a single advancing pointer through preorder."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Pre-build idx_map = {value: inorder_index} for O(1) lookups. "
            "Step 2: Keep pre_idx as a shared mutable counter starting at 0. "
            "Step 3: In each recursive call helper(in_left, in_right): "
            "take preorder[pre_idx] as root, advance pre_idx, find mid = idx_map[root_val], "
            "recurse LEFT (in_left..mid-1) then RIGHT (mid+1..in_right). "
            "Left-before-right ordering matches preorder's left-before-right structure."
        ),
        N.callout(
            "Analogy: preorder is like a to-do list of roots, top to bottom. "
            "inorder is the map that tells you 'everyone to the left of this person belongs to their left team'. "
            "You just read the next name from the to-do list and use the map to assign their team.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
"""def buildTree(preorder, inorder):
    idx_map = {v: i for i, v in enumerate(inorder)}
    pre_idx = [0]  # mutable so inner function can advance it

    def helper(in_left, in_right):
        if in_left > in_right:
            return None
        root_val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        root = TreeNode(root_val)
        mid = idx_map[root_val]
        root.left  = helper(in_left, mid - 1)
        root.right = helper(mid + 1, in_right)
        return root

    return helper(0, len(inorder) - 1)"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("idx_map = {v: i for i, v in enumerate(inorder)}", {"code": True}),
        (" — Build a hash map from each value to its index in the inorder array. "
         "Enables O(1) lookup of any root's split position. Done once before recursion.", {}),
    ])),
    N.para(N.rich([
        ("pre_idx = [0]", {"code": True}),
        (" — A list wrapper around an integer index so the nested function can mutate it. "
         "This pointer always points to the next unprocessed preorder element (the root of the current subtree).", {}),
    ])),
    N.para(N.rich([
        ("if in_left > in_right: return None", {"code": True}),
        (" — Base case: the inorder range is empty, meaning this subtree has no nodes. "
         "Return None without advancing pre_idx.", {}),
    ])),
    N.para(N.rich([
        ("root_val = preorder[pre_idx[0]]", {"code": True}),
        (" — The next element in preorder IS the root of this subtree, by the definition of preorder traversal.", {}),
    ])),
    N.para(N.rich([
        ("pre_idx[0] += 1", {"code": True}),
        (" — Consume this root from the preorder sequence. The next call will pick up from here.", {}),
    ])),
    N.para(N.rich([
        ("mid = idx_map[root_val]", {"code": True}),
        (" — O(1) lookup: find root's position in inorder. Everything at indices < mid is in the left subtree; > mid is in the right subtree.", {}),
    ])),
    N.para(N.rich([
        ("root.left  = helper(in_left, mid - 1)", {"code": True}),
        (" — Recurse on the left portion of inorder. Left-first ensures pre_idx walks through left-subtree preorder elements before right-subtree ones.", {}),
    ])),
    N.para(N.rich([
        ("root.right = helper(mid + 1, in_right)", {"code": True}),
        (" — Recurse on the right portion of inorder. By now pre_idx has advanced past all left-subtree nodes.", {}),
    ])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Array Slicing"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The simplest recursive formulation: if I have preorder and inorder arrays for a subtree, "
            "preorder[0] is the root. I split both arrays at that point and recurse."
        ),
        N.h4("What Doesn't Work (for large inputs)"),
        N.para(
            "inorder.index(value) is O(n) — scanning the entire inorder array each call. "
            "With n recursive calls, this is O(n²). Additionally, array slicing creates new list "
            "objects at every recursion level, using O(n²) total memory. Good for understanding "
            "but fails at scale."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The correctness is the same; the cost is in repeated linear scans. The upgrade to "
            "Solution 1 is simply precomputing those scans."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Take preorder[0] as root. Find its index mid in inorder using .index(). "
            "Left subtree gets preorder[1:mid+1] and inorder[:mid]. "
            "Right subtree gets preorder[mid+1:] and inorder[mid+1:]. Recurse."
        ),
    ]),
    N.h3("Code"),
    N.code(
"""def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])   # O(n) per call
    root.left  = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:],  inorder[mid+1:])
    return root"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if not preorder or not inorder: return None", {"code": True}),
        (" — Base case: empty arrays mean no subtree to build.", {}),
    ])),
    N.para(N.rich([
        ("mid = inorder.index(preorder[0])", {"code": True}),
        (" — Linear scan to find the root's position in inorder. O(n) per call, O(n²) total.", {}),
    ])),
    N.para(N.rich([
        ("preorder[1:mid+1]", {"code": True}),
        (" — The next (mid) preorder elements belong to the left subtree (mid = size of left subtree).", {}),
    ])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",   "Space"],
        ["Brute Force (Slicing)", "O(n²)",  "O(n²)"],
        ["Optimal (Hash Map) ✓",  "O(n)",   "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (DFS: Preorder / Divide and Conquer on traversal arrays)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Find Root in Inorder", {})])),
    N.callout(
        "When to recognize this pattern: "
        "You are given two traversal arrays of the same binary tree (one of which is inorder). "
        "You need to reconstruct the tree. Preorder or postorder gives roots; inorder gives the left/right split. "
        "Each recursive call peels off one root and divides the remaining nodes into two subtrees.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([
        ("Construct Binary Tree from Inorder and Postorder Traversal", {"bold": True}),
        (" (Medium) — Mirror: postorder's last element is root; build right-to-left (#106)", {}),
    ])),
    N.bullet(N.rich([
        ("Construct Binary Tree from Preorder and Postorder Traversal", {"bold": True}),
        (" (Medium) — Unique reconstruction for full binary trees only (#889)", {}),
    ])),
    N.bullet(N.rich([
        ("Serialize and Deserialize Binary Tree", {"bold": True}),
        (" (Hard) — Encode tree to string and decode back; same DFS preorder structure (#297)", {}),
    ])),
    N.bullet(N.rich([
        ("Construct BST from Preorder Traversal", {"bold": True}),
        (" (Medium) — BST property replaces inorder as the discriminant for left/right (#1008)", {}),
    ])),
    N.bullet(N.rich([
        ("Binary Tree Inorder Traversal", {"bold": True}),
        (" (Easy) — Prerequisite: must understand inorder output to exploit it for reconstruction (#94)", {}),
    ])),
    N.bullet(N.rich([
        ("Recover Binary Search Tree", {"bold": True}),
        (" (Medium) — Inorder of BST must be sorted; deviations reveal swapped nodes (#99)", {}),
    ])),
    N.para("These problems share the core technique: using inorder to split a tree into left/right subtrees."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section. "
              "Sub-pattern: Find Root in Inorder (Analysis classification).", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
