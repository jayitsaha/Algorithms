"""
Notion page builder for LeetCode #510 — Inorder Successor in BST II
Run from Algorithms/ directory: python3 gen_inorder_successor_in_bst_ii.py
"""
import notion_lib as N

PAGE_ID = "39193418-809c-819f-bf40-d0bb64237075"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=510,
    pattern="Trees",
    subpatterns=["BST Property", "With Parent Pointers"],
    tc="O(h)",
    sc="O(1)",
    key_insight="Right subtree → leftmost; no right subtree → climb parent pointers until left-child ancestor.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a "),
        ("node", {"code": True}),
        (" in a Binary Search Tree. The node has a "),
        ("parent", {"code": True}),
        (" pointer in addition to "),
        ("left", {"code": True}),
        (" and "),
        ("right", {"code": True}),
        (". Find the in-order successor of "),
        ("node", {"code": True}),
        (", i.e., the node with the smallest key greater than "),
        ("node.val", {"code": True}),
        (". If no such node exists, return "),
        ("null", {"code": True}),
        ("."),
    ])),
    N.para("Constraints: each node has .val, .left, .right, .parent. You are NOT given the root."),
    N.divider(),
]

# ── Solution 1 — Optimal (Interview Pick) ──────────────────────────────────────
sol1_code = """\
def inorderSuccessor(node: 'Node') -> 'Node':
    # Case A: right subtree exists
    if node.right:
        curr = node.right
        while curr.left:
            curr = curr.left
        return curr          # leftmost of right subtree = successor

    # Case B: no right subtree — climb via parent pointers
    curr = node
    while curr.parent and curr == curr.parent.right:
        curr = curr.parent   # skip ancestors where we came from the right
    return curr.parent       # first ancestor we approached from the left (or None)
"""

blocks += [
    N.h2("Solution 1 — Parent-Pointer Walk (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the node with the smallest value strictly greater than node.val — using only the node and its parent-pointer chain. We cannot search top-down because we don't have the root."),
        N.h4("What Doesn't Work"),
        N.para("A standard BST search (top-down from root) is impossible — we only have the node itself. A full inorder traversal would need O(n) time and O(h) space (recursive stack) and also needs the root. Neither approach uses the parent pointer that the problem explicitly gives us."),
        N.h4("The Key Observation"),
        N.para("In a BST, the inorder successor is always in one of two locations: (A) the leftmost node of the right subtree if one exists, or (B) the nearest ancestor from whose left subtree this node belongs — reached by climbing parent pointers."),
        N.h4("Building the Solution"),
        N.para("Case A: node.right exists → go right, then left as far as possible. The leftmost node of any subtree is its minimum, so this is the smallest value greater than ours. Case B: no right child → start at curr = node, climb while curr is a right child (those parents are already before us in sorted order). Stop when curr is a left child — curr.parent is the successor."),
        N.callout("Analogy: Reading chapters in a book. If the current page has more sub-pages (right subtree), the very first sub-page (leftmost) is next. If not, you return to the chapter heading (nearest ancestor from the left) — that is the next thing you read.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if node.right:", {"code": True}), " — Branch: does a right subtree exist?"])),
    N.para(N.rich([("curr = node.right", {"code": True}), " — Case A: enter the right subtree."])),
    N.para(N.rich([("while curr.left:", {"code": True}), " — Walk left until we reach the leftmost node in the right subtree."])),
    N.para(N.rich([("curr = curr.left", {"code": True}), " — Each step finds a smaller value in the right subtree."])),
    N.para(N.rich([("return curr", {"code": True}), " — The leftmost node is the minimum of the right subtree = the successor."])),
    N.para(N.rich([("curr = node", {"code": True}), " — Case B: start at the node itself and prepare to climb."])),
    N.para(N.rich([("while curr.parent and curr == curr.parent.right:", {"code": True}), " — Keep climbing while we are a right child. Right-child ancestors appear BEFORE us in sorted order (BST property: our subtree is to their right, so they are smaller), so they cannot be the successor."])),
    N.para(N.rich([("curr = curr.parent", {"code": True}), " — Move up one level."])),
    N.para(N.rich([("return curr.parent", {"code": True}), " — After the loop, curr is either the root (parent=None → no successor) or a node whose parent we approached from the left side. That parent is the answer. IMPORTANT: return curr.parent, not curr."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ───────────────────────────────────────────────────
sol2_code = """\
def inorderSuccessor_bruteforce(root, node) -> 'Node':
    # Requires root — not given in this problem formulation.
    # Kept here for comparison only.
    prev, result = None, None

    def inorder(n):
        nonlocal prev, result
        if not n or result:
            return
        inorder(n.left)
        if prev is node:
            result = n
        prev = n
        inorder(n.right)

    inorder(root)
    return result   # O(n) time, O(h) space
"""

blocks += [
    N.h2("Solution 2 — Brute Force Inorder Traversal (for comparison)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Visit all nodes in sorted order; the node immediately after our target is the successor. Simple and correct, but requires the root (not given here) and visits all nodes."),
        N.h4("What Doesn't Work"),
        N.para("This approach is O(n) time — it must visit every node in the worst case. With parent pointers, we should be able to do O(h). This solution also needs the root pointer, which is not given in this problem."),
        N.h4("The Key Observation"),
        N.para("Track the 'previous' node during inorder traversal. The moment previous becomes our target node, the current node is the successor."),
        N.h4("Building the Solution"),
        N.para("Recursive inorder: go left → process root → go right. Keep a 'prev' pointer. When prev matches our target node, capture the current node as result and stop early."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("prev, result = None, None", {"code": True}), " — prev tracks the node visited just before current; result stores the answer."])),
    N.para(N.rich([("if prev is node: result = n", {"code": True}), " — The node immediately after our target in inorder = the successor."])),
    N.para(N.rich([("prev = n", {"code": True}), " — Always update prev so the next iteration can check."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Inorder", "O(n)", "O(h)", "Needs root; visits all nodes"],
        ["Parent-Pointer Walk (Optimal)", "O(h)", "O(1)", "Interview pick; two clean cases"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BST Property, With Parent Pointers, DFS: Inorder"])),
    N.callout(
        "When to recognize this pattern: BST + 'inorder successor/predecessor' + parent pointer given. Need O(1) space. Given specific node (not root). Need next/previous in sorted order without visiting all nodes.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BST inorder / successor / parent pointers):"),
    N.bullet(N.rich([("Inorder Successor in BST", {"bold": True}), " (Medium) — Given root + target value; use BST key comparison top-down (#285)"])),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}), " (Medium) — Successor used to replace a deleted node with two children (#450)"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) — Inorder traversal with a counter (#230)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — Inorder must produce strictly increasing sequence (#98)"])),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}), " (Medium) — Find correct leaf position using BST property (#701)"])),
    N.bullet(N.rich([("Find Inorder Predecessor (mirror)", {"bold": True}), " (Medium) — Go left then rightmost; or climb while left child"])),
    N.para("These problems all exploit the BST sorted-order property to navigate in O(h) time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, BST Property sub-pattern.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("inorder_successor_in_bst_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
