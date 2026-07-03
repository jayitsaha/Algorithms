"""
gen_flatten_binary_tree_to_linked_list.py
Notion update for LeetCode #114 — Flatten Binary Tree to Linked List
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f5-a748-f5d787911769"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=114,
    pattern="Trees",
    subpatterns=["Post-order Pointer Rewiring"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Reverse preorder (right→left→root) with a trailing prev pointer wires each node to its preorder successor in O(h) space.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, flatten it ", {}),
        ("in-place", {"bold": True}),
        (" into a linked list in preorder traversal order (root → left subtree → right subtree). "
         "After flattening, every node's ", {}),
        ("left", {"code": True}),
        (" child must be ", {}),
        ("null", {"code": True}),
        (" and the ", {}),
        ("right", {"code": True}),
        (" child points to the next node in preorder. The modification must be done in-place using O(1) extra space (no new nodes).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Reverse Preorder DFS (Interview Pick) ─────────────────────
sol1_code = """\
def flatten(root: TreeNode) -> None:
    prev = [None]             # list trick: lets inner function mutate the reference
    def dfs(node):
        if not node: return   # base case: null → nothing to do, prev unchanged
        dfs(node.right)       # CRITICAL: recurse right FIRST (reversed preorder)
        dfs(node.left)        # then recurse left
        node.right = prev[0]  # wire: this node's right → already-wired suffix
        node.left  = None     # clear left (left subtree folded into right chain)
        prev[0] = node        # advance: this node is new head of processed list
    dfs(root)                 # root processed last; becomes head of final list
"""

blocks += [
    N.h2("Solution 1 — Reverse Preorder DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to rewire the tree so every node's right pointer follows preorder order (root → left subtree → right subtree) and every left pointer is null. The key challenge: how do we know what each node's 'next' pointer should be without a separate pass?"),
        N.h4("What Doesn't Work"),
        N.para("A naive preorder DFS visits nodes left-to-right: 1,2,3,4,5,6. But when we process node 1, we don't yet know where node 2's chain ends (we haven't computed it). If we assign node1.right = node2 immediately, we lose the reference to the original right subtree (5,6). We'd need to save it first — leading to the O(n) list approach."),
        N.h4("The Key Observation"),
        N.para("Preorder is [1,2,3,4,5,6]. Reversed, that's [6,5,4,3,2,1]. If we visit nodes in reversed preorder, when we arrive at any node N, every node that should come AFTER N is already processed. We can safely wire N.right to prev without losing any reference."),
        N.h4("Building the Solution"),
        N.para("1. Visit in reverse preorder: recurse RIGHT first, then LEFT, then process the current node.\n2. Keep a prev pointer. Initially None (nothing comes after 6).\n3. At each node: wire node.right = prev, clear node.left, update prev = node.\n4. The recursion naturally handles the order — when we process a parent, both subtrees are already flattened."),
        N.callout("Analogy: Imagine building a chain of paper clips right-to-left. You always know what to clip the current piece onto because the right side is already built. The 'prev' pointer is your handle to the already-built right end.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = [None]", {"code": True}), (" — List trick: lets the nested dfs() function mutate this reference. Equivalent to nonlocal prev in Python 3.", {})])),
    N.para(N.rich([("def dfs(node)", {"code": True}), (" — Inner DFS. Visits: right subtree, left subtree, then processes the current node.", {})])),
    N.para(N.rich([("if not node: return", {"code": True}), (" — Base case: null node is silently skipped, prev is left unchanged.", {})])),
    N.para(N.rich([("dfs(node.right)", {"code": True}), (" — CRITICAL: recurse RIGHT first. This makes it reverse preorder instead of standard postorder.", {})])),
    N.para(N.rich([("dfs(node.left)", {"code": True}), (" — Recurse left second. After this returns, the left subtree is already wired and prev points to its leftmost node.", {})])),
    N.para(N.rich([("node.right = prev[0]", {"code": True}), (" — Wire this node's right to the already-processed suffix. prev holds all preorder successors of this node.", {})])),
    N.para(N.rich([("node.left = None", {"code": True}), (" — Clear left: the original left subtree is already woven into the right chain via prev.", {})])),
    N.para(N.rich([("prev[0] = node", {"code": True}), (" — Advance prev. This node is now the new earliest node in the processed portion.", {})])),
    N.para(N.rich([("dfs(root)", {"code": True}), (" — Kick off from root. Root is processed last (reverse preorder), correctly becoming the list head.", {})])),
    N.divider(),
]

# ── Solution 2: Collect Preorder + Rewire ─────────────────────────────────
sol2_code = """\
def flatten(root: TreeNode) -> None:
    nodes = []
    def preorder(n):
        if not n: return
        nodes.append(n)        # collect in preorder (root first)
        preorder(n.left)
        preorder(n.right)
    preorder(root)             # nodes = [1,2,3,4,5,6]
    for i in range(len(nodes) - 1):
        nodes[i].right = nodes[i + 1]  # wire each node to its successor
        nodes[i].left  = None          # clear left pointer
"""

blocks += [
    N.h2("Solution 2 — Collect Preorder + Re-wire"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest version: just do a preorder traversal, remember the order, and then re-wire the pointers. Two separate passes — one to determine order, one to apply it."),
        N.h4("What Doesn't Work"),
        N.para("Trying to wire pointers during a single forward preorder pass doesn't work cleanly: when you visit node 2, you don't yet know where the left subtree ends (you haven't traversed it). You'd need to save references, leading to complexity."),
        N.h4("The Key Observation"),
        N.para("By separating the traversal from the rewiring, each step is trivially simple. Preorder gives us the exact order we need. Re-wiring is just a linear scan through the collected list."),
        N.h4("Building the Solution"),
        N.para("Collect all nodes in preorder into a list. Then iterate the list: nodes[i].right = nodes[i+1], nodes[i].left = None. The last node's right stays None (no explicit assignment needed). O(n) time, O(n) space."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("nodes = []", {"code": True}), (" — Will hold all tree nodes in preorder order after the traversal.", {})])),
    N.para(N.rich([("nodes.append(n)", {"code": True}), (" — Collect the node before recursing into children — this is what makes it preorder (root before subtrees).", {})])),
    N.para(N.rich([("preorder(root)", {"code": True}), (" — After this call, nodes = [1, 2, 3, 4, 5, 6] for the example tree.", {})])),
    N.para(N.rich([("nodes[i].right = nodes[i+1]", {"code": True}), (" — Wire each node's right to the next node in preorder. The loop runs n-1 times.", {})])),
    N.para(N.rich([("nodes[i].left = None", {"code": True}), (" — Clear left pointers. The linked list uses only right pointers.", {})])),
    N.divider(),
]

# ── Solution 3: Morris-style Iterative ────────────────────────────────────
sol3_code = """\
def flatten(root: TreeNode) -> None:
    curr = root
    while curr:
        if curr.left:                       # only act when there's a left subtree
            prev = curr.left
            while prev.right:               # find rightmost node of left subtree
                prev = prev.right
            prev.right = curr.right         # stitch: rightmost of left → curr's right
            curr.right = curr.left          # move entire left subtree to the right
            curr.left  = None               # clear left pointer
        curr = curr.right                   # advance (always safe now)
"""

blocks += [
    N.h2("Solution 3 — Morris-style Iterative (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each node with a left subtree, we need to insert the entire left subtree between this node and its right child. The left subtree's last node (in preorder, which for a subtree is its rightmost node) must connect to the current node's right child."),
        N.h4("The Key Observation"),
        N.para("At any node with a left child: (a) find the rightmost node of the left subtree — call it 'tail'. (b) stitch tail.right = curr.right. (c) move the left subtree to the right: curr.right = curr.left. (d) clear curr.left. Now curr has no left child, and its right is the formerly-left subtree, followed naturally by the formerly-right subtree."),
        N.h4("Why This Works"),
        N.para("After stitching, curr's right subtree is [left_subtree → original_right_subtree]. Since we only modified curr's immediate left and right pointers (and the tail of the left subtree), the relative ordering within subtrees is preserved. We advance curr = curr.right and repeat."),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.h3("Line by Line"),
    N.para(N.rich([("curr = root", {"code": True}), (" — Start at the root. We'll walk right through the list as it gets built.", {})])),
    N.para(N.rich([("if curr.left", {"code": True}), (" — Only act when there's a left subtree to fold in. If no left child, just advance.", {})])),
    N.para(N.rich([("while prev.right: prev = prev.right", {"code": True}), (" — Walk to the rightmost node of the left subtree — where the left subtree's preorder sequence ends.", {})])),
    N.para(N.rich([("prev.right = curr.right", {"code": True}), (" — Stitch: tail of left subtree → original right child. This preserves the right subtree.", {})])),
    N.para(N.rich([("curr.right = curr.left; curr.left = None", {"code": True}), (" — Pivot: left subtree becomes the right child. Left pointer is cleared.", {})])),
    N.para(N.rich([("curr = curr.right", {"code": True}), (" — Advance to next node. The newly prepended subtree is processed in subsequent iterations.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Collect Preorder + Re-wire", "O(n)", "O(n)"],
        ["Reverse Preorder DFS (Interview Pick)", "O(n)", "O(h) — recursion stack"],
        ["Morris-style Iterative", "O(n) amortized", "O(1) — no extra memory"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Post-order Pointer Rewiring; DFS Preorder (output order); Morris Traversal (O(1) space variant)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('Problem says "flatten a tree into a linked list" using a specific traversal order. '
             'Asks you to rewire tree pointers in-place without allocating new nodes. '
             'Output structure uses existing left/right (or prev/next) pointers. '
             'Phrase "in-place" + "linked list" + "tree" together is the signal.', {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (post-order pointer rewiring / tree-to-list conversion):"),
    N.bullet(N.rich([("Convert Binary Search Tree to Sorted Doubly Linked List", {"bold": True}), (" (Medium) — Inorder DFS; rewire left/right as prev/next pointers in doubly linked list (#426)", {})])),
    N.bullet(N.rich([("Populating Next Right Pointers in Each Node", {"bold": True}), (" (Medium) — Wire .next pointers across the same level; perfect binary tree variant (#116)", {})])),
    N.bullet(N.rich([("Populating Next Right Pointers in Each Node II", {"bold": True}), (" (Medium) — Same but for any binary tree — level-order pointer threading (#117)", {})])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), (" (Medium) — Preorder DFS; track rightmost visible node per depth level (#199)", {})])),
    N.bullet(N.rich([("Serialize and Deserialize Binary Tree", {"bold": True}), (" (Hard) — Preorder traversal to encode tree; reconstruct by re-threading node references (#297)", {})])),
    N.bullet(N.rich([("Convert Sorted List to Binary Search Tree", {"bold": True}), (" (Medium) — Reverse problem: linked list → balanced BST using slow-fast pointer to find midpoint (#109)", {})])),
    N.para("These problems share the core technique: traversing a tree and directly rewiring its own pointer fields to produce a linear or hierarchical structure without extra allocation."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section. Sub-Pattern: Post-order Pointer Rewiring.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("flatten_binary_tree_to_linked_list")),
    N.para(N.rich([("Step through the reverse-preorder algorithm visually — use Next/Prev or arrow keys to see each node get wired into the linked list.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ──────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page {PAGE_ID}")
print("NOTION OK", PAGE_ID)
