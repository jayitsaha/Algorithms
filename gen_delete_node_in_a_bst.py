"""
gen_delete_node_in_a_bst.py
Notion IN-PLACE update for: Delete Node in a BST (LeetCode #450)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e8-955e-f746426575e6"
SLUG    = "delete_node_in_a_bst"

# ── 1. Properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 450,
    pattern     = "Trees",
    subpatterns = ["Replace with Successor", "DFS: Postorder"],
    tc          = "O(h)",
    sc          = "O(h)",
    key_insight = "Replace target value with in-order successor (leftmost in right subtree), then delete that successor — it always has at most one child.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a Binary Search Tree (BST) and an integer ", {}),
        ("key", {"code": True}),
        (", delete the node with the given key in the BST and return the root node "
         "of the updated BST. The BST property must be maintained: for every node, "
         "all left descendants < node.val < all right descendants.", {}),
    ])),
    N.para("Constraints: -10^5 ≤ key, node.val ≤ 10^5. All node values are unique. "
           "root is a valid BST. The key may or may not exist in the BST."),
    N.divider(),
]

# ── Solution 1 — Recursive Successor Replacement ──
sol1_code = '''\
def deleteNode(root, key):
    if not root:
        return None                # key not in tree
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:                          # key == root.val -> found target
        if not root.left:
            return root.right      # Case 1 (leaf) or Case 2 (right child only)
        if not root.right:
            return root.left       # Case 2 (left child only)
        # Case 3: two children -> find in-order successor
        succ = root.right
        while succ.left:
            succ = succ.left       # leftmost = smallest in right subtree
        root.val = succ.val        # COPY successor value into target node
        root.right = deleteNode(root.right, succ.val)  # delete successor
    return root
'''

blocks += [
    N.h2("Solution 1 — Recursive Successor Replacement (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to remove a node from a BST while keeping all remaining nodes in valid BST order. "
               "The challenge: the node may have children that also need to stay in the tree. "
               "Think of it like removing a middle tile from a connected structure — the tiles on either side must reconnect."),
        N.h4("What Doesn't Work"),
        N.para("Simply unlinking the node breaks the tree for Case 3. If a node has two children, "
               "you cannot return either one without losing the other subtree. You must find a way to "
               "merge both subtrees into one valid BST."),
        N.h4("The Key Observation"),
        N.para("For a node with two children, the in-order successor (the smallest value in the right subtree) "
               "is the ONLY value that can legally occupy this position: it is larger than everything in the "
               "left subtree and smaller than everything else in the right subtree. And since it's the leftmost "
               "node in its subtree, it has no left child — so deleting it is always simple (Case 1 or 2)."),
        N.h4("Building the Solution"),
        N.para("Use the recursive return pattern: each call returns the updated subtree root. "
               "Navigate by BST property. When found, apply three-case analysis. "
               "For Case 3: find successor by going right then fully left. Copy its value. "
               "Recursively delete the successor from the right subtree."),
        N.callout(
            "Analogy: Think of replacing a departing employee with the most junior person "
            "who outranks everyone else in their team — they slot perfectly into the vacated role "
            "without disrupting the hierarchy.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return None", {"code": True}),
                   (" — Base case: if we fall off the tree, the key wasn't here. Return None cleanly.", {})])),
    N.para(N.rich([("if key < root.val:", {"code": True}),
                   (" — BST property: target must be in the left subtree. Recurse left.", {})])),
    N.para(N.rich([("root.left = deleteNode(root.left, key)", {"code": True}),
                   (" — Magic pattern: the recursive call returns the updated left subtree root. "
                    "Assigning it back to root.left updates the pointer automatically.", {})])),
    N.para(N.rich([("elif key > root.val:", {"code": True}),
                   (" — Target is in the right subtree. Symmetric case.", {})])),
    N.para(N.rich([("else:", {"code": True}),
                   (" — key == root.val. This is the node to delete. Enter the three-case logic.", {})])),
    N.para(N.rich([("if not root.left: return root.right", {"code": True}),
                   (" — Case 1 (no children at all) or Case 2 (right child only). "
                    "Return root.right — which is either the right child or None. "
                    "Parent's pointer is updated to skip the deleted node.", {})])),
    N.para(N.rich([("if not root.right: return root.left", {"code": True}),
                   (" — Case 2 with only a left child. Return it directly.", {})])),
    N.para(N.rich([("succ = root.right", {"code": True}),
                   (" — Case 3: begin successor search. Start at the right child.", {})])),
    N.para(N.rich([("while succ.left: succ = succ.left", {"code": True}),
                   (" — Walk left as far as possible. Stops at the leftmost node "
                    "(smallest in right subtree) = in-order successor.", {})])),
    N.para(N.rich([("root.val = succ.val", {"code": True}),
                   (" — Copy the successor's value into the current node. "
                    "We do NOT move the node object — just the value. "
                    "The current node now has the successor's value.", {})])),
    N.para(N.rich([("root.right = deleteNode(root.right, succ.val)", {"code": True}),
                   (" — Delete the original successor node from the right subtree. "
                    "Since the successor has no left child, this recursive call hits Case 1 or 2.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — Return the (possibly value-modified) current node. "
                    "This is what the parent will assign to its left or right pointer.", {})])),
    N.divider(),
]

# ── Solution 2 — Iterative ──
sol2_code = '''\
def deleteNode(root, key):
    parent, node, go_left = None, root, False
    # Phase 1: search for the target node
    while node and node.val != key:
        parent = node
        if key < node.val:
            node = node.left
            go_left = True
        else:
            node = node.right
            go_left = False
    if not node:
        return root                # key not found
    # Phase 2: determine replacement
    if not node.left:
        repl = node.right          # Case 1 or 2
    elif not node.right:
        repl = node.left           # Case 2
    else:
        # Case 3: find successor and relink
        repl = node.right
        prev = node
        while repl.left:
            prev, repl = repl, repl.left
        if prev != node:
            prev.left = repl.right
            repl.right = node.right
        repl.left = node.left
    # Phase 3: attach replacement
    if not parent:
        return repl                # deleted root itself
    if go_left:
        parent.left = repl
    else:
        parent.right = repl
    return root
'''

blocks += [
    N.h2("Solution 2 — Iterative (O(1) Extra Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same deletion logic, but without using the call stack. "
               "We explicitly track the parent node and direction to child "
               "so we can relink the tree manually."),
        N.h4("What Doesn't Work"),
        N.para("In the recursive version, the return value automatically updates parent pointers. "
               "Iteratively, we must do this manually — requiring us to track the parent and "
               "which direction (left/right) we came from."),
        N.h4("The Key Observation"),
        N.para("The same three-case logic applies. Case 3 is more complex iteratively because "
               "we need to physically relink the successor's parent pointer, not just copy a value. "
               "We track 'prev' (the parent of the successor) to handle this."),
        N.h4("Building the Solution"),
        N.para("Phase 1: walk down the tree tracking parent + direction until we find the target. "
               "Phase 2: determine the replacement node based on the three cases. "
               "Phase 3: attach the replacement to the parent (or return it as new root)."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("parent, node, go_left = None, root, False", {"code": True}),
                   (" — Track parent node and which direction we moved to reach current node.", {})])),
    N.para(N.rich([("while node and node.val != key:", {"code": True}),
                   (" — Search phase: walk down until we find the key or fall off the tree.", {})])),
    N.para(N.rich([("if not node: return root", {"code": True}),
                   (" — Key not found. Tree unchanged — return original root.", {})])),
    N.para(N.rich([("repl = node.right / repl = node.left", {"code": True}),
                   (" — Cases 1 and 2: replacement is simply the surviving child (or None).", {})])),
    N.para(N.rich([("while repl.left: prev, repl = repl, repl.left", {"code": True}),
                   (" — Case 3: find successor (leftmost in right subtree) "
                    "and track its parent (prev) for relinking.", {})])),
    N.para(N.rich([("if prev != node: prev.left = repl.right; repl.right = node.right", {"code": True}),
                   (" — If successor is not the immediate right child, "
                    "detach it from its parent and attach the node's full right subtree to it.", {})])),
    N.para(N.rich([("if not parent: return repl", {"code": True}),
                   (" — If we deleted the root, the replacement becomes the new root.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive (Successor) — Interview Pick", "O(h)", "O(h) call stack"],
        ["Iterative", "O(h)", "O(1) extra"],
    ]),
    N.para("h = tree height. O(log n) for balanced BST, O(n) for degenerate (sorted-input) tree."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (BST Operations)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Replace with Successor (Case 3), DFS: Postorder (recursive return pattern)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Delete a node from BST while maintaining order' → always 3-case successor analysis\n"
        "• 'Find next larger / in-order next element in BST' → go right then leftmost\n"
        "• 'Modify BST structure' → use recursive return pattern (root.child = recursive_call)\n"
        "• Any tree node has two children and needs removal → think successor/predecessor",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST modification / successor technique:"),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}),
                     (" (Easy, #701) — Same recursive navigation, simpler: leaf insertion only", {})])),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}),
                     (" (Easy, #700) — BST traversal without modification", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}),
                     (" (Medium, #230) — In-order traversal; same leftmost pattern for successor", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}),
                     (" (Medium, #98) — BST property checking using min/max bounds", {})])),
    N.bullet(N.rich([("Trim a Binary Search Tree", {"bold": True}),
                     (" (Medium, #669) — Selective deletion by range; same recursive return structure", {})])),
    N.bullet(N.rich([("Inorder Successor in BST", {"bold": True}),
                     (" (Medium, #285) — Finds the in-order successor directly; same go-right-then-leftmost logic", {})])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}),
                     (" (Medium, #538) — Reverse in-order (right-root-left) traversal", {})])),
    N.para("These problems share the core technique: navigating a BST using the left < root < right property, "
           "and using the recursive return pattern (or explicit parent tracking) for tree modification."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, BST Operations sub-pattern.",
              "📚", "gray_background"),
]

# ── Visual Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
