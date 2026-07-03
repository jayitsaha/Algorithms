"""
gen_lowest_common_ancestor_of_a_binary_search_tree.py
Regenerates the Notion page for LC #235 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811b-a149-d902aa72d6d7"
SLUG    = "lowest_common_ancestor_of_a_binary_search_tree"

# ── 1. Set properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=235,
    pattern="Trees",
    subpatterns=["BST Property"],
    tc="O(h)",
    sc="O(1)",
    key_insight="Walk the BST: if both p,q < node go left; if both > node go right; otherwise the current node is the LCA.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a Binary Search Tree (BST) and two nodes ", {}),
        ("p", {"code": True}),
        (" and ", {}),
        ("q", {"code": True}),
        (", return their Lowest Common Ancestor (LCA). "
         "The LCA of two nodes is defined as the deepest node in the tree that is "
         "an ancestor of both p and q. A node is considered an ancestor of itself.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Iterative (Interview Pick) ───────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative BST Traversal (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the deepest node that lies on the path from root to p AND on the path from root to q. "
               "In other words, the first node where the two paths 'diverge'."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach might store the full root→p and root→q paths in two arrays, then scan "
               "from the end to find the last common node. That is O(h) time but O(h) space. It also ignores "
               "the BST ordering, which makes the problem much easier."),
        N.h4("The Key Observation"),
        N.para("In a BST, if both p and q are less than a node's value, BOTH must live in the left subtree. "
               "If both are greater, both live in the right subtree. The first node where they go in different "
               "directions (or one of them IS the node) is the LCA."),
        N.h4("Building the Solution"),
        N.para("Start at root. At each node:\n"
               "• If p.val < node.val AND q.val < node.val → go left (LCA is deeper in left subtree)\n"
               "• If p.val > node.val AND q.val > node.val → go right (LCA is deeper in right subtree)\n"
               "• Otherwise → this node is the LCA. Return it immediately."),
        N.callout(
            "Analogy: Imagine a street numbered 1–100. You're looking for the closest intersection "
            "of two delivery routes. If both destinations are below house #50, you only search the "
            "lower half — the BST property is that directional compass.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def lowestCommonAncestor(root, p, q):\n"
        "    node = root\n"
        "    while node:\n"
        "        if p.val < node.val and q.val < node.val:\n"
        "            node = node.left          # both in left subtree\n"
        "        elif p.val > node.val and q.val > node.val:\n"
        "            node = node.right         # both in right subtree\n"
        "        else:\n"
        "            return node               # split or one equals node → LCA found\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("node = root", {"code": True}),
                   (" — start traversal at the root; no extra space needed.", {})])),
    N.para(N.rich([("while node:", {"code": True}),
                   (" — the LCA is guaranteed to exist (p and q are in the BST), so we will always return before node becomes None.", {})])),
    N.para(N.rich([("if p.val < node.val and q.val < node.val:", {"code": True}),
                   (" — by BST property, both targets lie in the left subtree. The current node is a common ancestor but not the deepest — descend left.", {})])),
    N.para(N.rich([("elif p.val > node.val and q.val > node.val:", {"code": True}),
                   (" — same reasoning, both targets in right subtree, descend right.", {})])),
    N.para(N.rich([("else: return node", {"code": True}),
                   (" — either p and q are on opposite sides (split), or one of them equals node.val. Either way, this is the LCA.", {})])),
    N.divider(),
]

# ── Solution 2 — Recursive ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive BST Traversal"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same logic as Solution 1, expressed recursively. At each call we decide which subtree to recurse into."),
        N.h4("What Doesn't Work"),
        N.para("The recursive version uses O(h) call-stack space. For a skewed BST that is O(n). The iterative solution avoids this."),
        N.h4("The Key Observation"),
        N.para("The base case is the same 'split or match' condition. Tail recursion means Python will allocate a new frame per level of depth."),
        N.h4("Building the Solution"),
        N.para("Check both conditions. If neither fires, return root (the split case). This is elegant but inferior to iterative for space."),
    ]),
    N.h3("Code"),
    N.code(
        "def lowestCommonAncestor(root, p, q):\n"
        "    if p.val < root.val and q.val < root.val:\n"
        "        return lowestCommonAncestor(root.left, p, q)\n"
        "    if p.val > root.val and q.val > root.val:\n"
        "        return lowestCommonAncestor(root.right, p, q)\n"
        "    return root   # split or match — this is the LCA\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if p.val < root.val and q.val < root.val:", {"code": True}),
                   (" — both smaller → recurse left.", {})])),
    N.para(N.rich([("if p.val > root.val and q.val > root.val:", {"code": True}),
                   (" — both larger → recurse right.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — neither condition held: split or one equals root. Return root as LCA.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Iterative (Interview Pick)", "O(h)", "O(1)"],
        ["Recursive", "O(h)", "O(h) — call stack"],
        ["Path comparison (brute)", "O(h)", "O(h) — two path arrays"],
    ]),
    N.para("h = height of BST. O(log n) for a balanced BST, O(n) in the worst case for a skewed tree."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BST Property (Use BST Property)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "The problem mentions 'BST', 'binary search tree', or guarantees sorted node values. "
        "Any search, find, or navigate operation on a BST should immediately trigger: "
        "'Can I use the left < root < right ordering to skip an entire subtree?'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BST Property / Tree Ancestor):"),
    N.bullet(N.rich([("236. Lowest Common Ancestor of a Binary Tree", {"bold": True}),
                     (" (Medium) — General BT, no ordering. Recurse both subtrees, return non-null.", {})])),
    N.bullet(N.rich([("700. Search in a Binary Search Tree", {"bold": True}),
                     (" (Easy) — Navigate BST by comparing target to node.val.", {})])),
    N.bullet(N.rich([("450. Delete Node in a BST", {"bold": True}),
                     (" (Medium) — Find node via BST property, then restructure subtree.", {})])),
    N.bullet(N.rich([("98. Validate Binary Search Tree", {"bold": True}),
                     (" (Medium) — Verify BST property holds at every node.", {})])),
    N.bullet(N.rich([("1650. LCA of Binary Tree III (parent pointers)", {"bold": True}),
                     (" (Medium) — Two-pointer trick on ancestor chains (like linked list cycle).", {})])),
    N.bullet(N.rich([("1740. Find Distance in a Binary Tree", {"bold": True}),
                     (" (Medium) — Uses LCA as pivot to compute distance between two nodes.", {})])),
    N.para("These problems share the BST-property navigation: compare values to decide direction instead of exploring both subtrees."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, BST Property sub-pattern", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append ────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
