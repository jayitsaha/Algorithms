"""
gen_balanced_binary_tree.py
Notion in-place update for LeetCode #110 Balanced Binary Tree.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f6-837f-ee6671b8af6f"
SLUG = "balanced_binary_tree"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=110,
    pattern="Trees",
    subpatterns=["Check Height Difference"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Postorder DFS: return height if subtree balanced, -1 sentinel if not — fuses height computation and balance check in a single O(n) pass.",
    icon="🟢",
    status="Solved",
    source="LeetCode"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, determine if it is ", {}),
        ("height-balanced", {"bold": True}),
        (". A binary tree is height-balanced if, for every node in the tree, "
         "the height of its left subtree and the height of its right subtree "
         "differ by at most 1.", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("number of nodes in [0, 5000], node values in [-10^4, 10^4].", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Postorder DFS with Sentinel (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — Postorder DFS with −1 Sentinel (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every node in the tree, the height of its left and right subtrees must differ by at most 1. This condition must hold at EVERY node — not just the root. So we need to visit all nodes and check each one's local balance condition."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: write isBalanced recursively, and call a separate height(node) function for each node. This is O(n²) — height() traverses the entire subtree below each node, and there are O(n) nodes. For a skewed tree of n nodes, this is O(n²) total work."),
        N.h4("The Key Observation"),
        N.para("When we recurse into a child and it returns its height, we've already done the traversal work. We can check balance AND return the height in the same call. We just need a way to signal 'something went wrong below' — use −1 as a sentinel since heights are always non-negative integers."),
        N.h4("Building the Solution"),
        N.para("Define an inner helper check(node) that returns: (a) the actual height of the subtree if it is balanced, or (b) -1 if any node in the subtree is unbalanced. Use postorder DFS (left → right → root). At each node: check left child, propagate -1 if it failed, check right child, propagate -1 if it failed, check |left_h - right_h| <= 1. If balanced, return 1 + max(left_h, right_h)."),
        N.callout(
            "Analogy: building inspection. Each floor checks itself and the two floors below. If any floor sends up a red flag (-1), immediately pass it up without inspecting further. If the top floor gets no red flag, the building is safe.",
            "🏗️", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isBalanced(root: TreeNode) -> bool:\n"
        "    def check(node):\n"
        "        if node is None:                    # base case: null node\n"
        "            return 0                        # height 0, trivially balanced\n"
        "        left_h = check(node.left)           # postorder: recurse left first\n"
        "        if left_h == -1:                    # left subtree unbalanced → propagate\n"
        "            return -1\n"
        "        right_h = check(node.right)         # postorder: recurse right\n"
        "        if right_h == -1:                   # right subtree unbalanced → propagate\n"
        "            return -1\n"
        "        if abs(left_h - right_h) > 1:       # check THIS node's balance condition\n"
        "            return -1\n"
        "        return 1 + max(left_h, right_h)     # balanced → return actual height\n"
        "    return check(root) != -1                # outer wrapper"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def isBalanced(root)", {"code": True}), (" — outer function; takes the root of the binary tree.", {})])),
    N.para(N.rich([("def check(node):", {"code": True}), (" — inner helper that does all the work. Returns height (≥0) or −1 (failure).", {})])),
    N.para(N.rich([("if node is None: return 0", {"code": True}), (" — base case. Null node has height 0 and is always balanced. Stops the recursion at leaf boundaries.", {})])),
    N.para(N.rich([("left_h = check(node.left)", {"code": True}), (" — postorder step 1: recurse into left child before processing current node.", {})])),
    N.para(N.rich([("if left_h == -1: return -1", {"code": True}), (" — early termination. If left subtree already failed, no point checking right.", {})])),
    N.para(N.rich([("right_h = check(node.right)", {"code": True}), (" — postorder step 2: recurse into right child.", {})])),
    N.para(N.rich([("if right_h == -1: return -1", {"code": True}), (" — same early termination for right subtree.", {})])),
    N.para(N.rich([("if abs(left_h - right_h) > 1: return -1", {"code": True}), (" — postorder step 3: check THIS node's local balance. If heights differ by more than 1, this is the culprit.", {})])),
    N.para(N.rich([("return 1 + max(left_h, right_h)", {"code": True}), (" — node is balanced. Return actual height so parent can use it. Height = 1 (for this node) + max child height.", {})])),
    N.para(N.rich([("return check(root) != -1", {"code": True}), (" — if helper never returned -1, tree is fully balanced. Clean one-liner outer.", {})])),
    N.divider(),
]

# ── Solution 2: Naive Top-Down (for explanation) ──────────────────────────────
blocks += [
    N.h2("Solution 2 — Naive Top-Down Recursion (O(n²), good as starting point)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of the recursive definition directly: a tree is balanced if the root's subtrees differ in height by at most 1, AND both subtrees are themselves balanced. Write this literally."),
        N.h4("What Doesn't Work Well"),
        N.para("This direct translation calls height() for each node, and height() itself traverses the entire subtree. Since height() is O(n) and we call it for each of the O(n) nodes, total time is O(n²). For a balanced tree this is O(n log n), but for a skewed tree it's O(n²)."),
        N.h4("The Key Observation"),
        N.para("This is the 'obvious' approach to present first in an interview. Say you'll start with it, then optimize to O(n) with the postorder sentinel approach."),
    ]),
    N.h3("Code"),
    N.code(
        "def isBalanced(root: TreeNode) -> bool:\n"
        "    if not root:\n"
        "        return True\n"
        "    def height(node):\n"
        "        if not node:\n"
        "            return 0\n"
        "        return 1 + max(height(node.left), height(node.right))\n"
        "    # Check root, then recurse on children\n"
        "    if abs(height(root.left) - height(root.right)) > 1:\n"
        "        return False\n"
        "    return isBalanced(root.left) and isBalanced(root.right)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return True", {"code": True}), (" — empty tree is trivially balanced.", {})])),
    N.para(N.rich([("def height(node):", {"code": True}), (" — separate helper that computes height via postorder DFS. O(n) per call.", {})])),
    N.para(N.rich([("abs(height(root.left) - height(root.right)) > 1", {"code": True}), (" — check balance at current root. Each height() call traverses the subtree — O(n) work.", {})])),
    N.para(N.rich([("return isBalanced(root.left) and isBalanced(root.right)", {"code": True}), (" — recurse on both children. Each call again invokes height() for their subtrees → redundant work.", {})])),
    N.callout(
        "Why this is O(n²): height() is called once per node of isBalanced, and each height() call visits all nodes below. For a balanced tree: O(n log n). For a skewed linked-list tree: O(n²). Always propose Solution 1 as the optimal follow-up.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Postorder DFS with Sentinel (Solution 1)", "O(n)", "O(h)"],
        ["Naive Top-Down (Solution 2)", "O(n²)", "O(h)"],
    ]),
    N.para("h = tree height. O(log n) for balanced trees, O(n) worst case for skewed trees."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Check Height Difference (via DFS: Postorder)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks to validate or compute a property that must hold at every node, "
        "(2) the property at a node depends on properties of its children (height, sum, path), "
        "(3) a naive approach would recompute subtree info repeatedly — merge it into one pass using a sentinel return value.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Postorder DFS / bottom-up height computation):"),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), (" (Easy) — Simpler version: just return 1 + max(left, right) without balance check. (#104)", {})])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), (" (Easy) — Track global max diameter while computing depths postorder. Same single-pass fusion. (#543)", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Postorder: compute max contribution per node, update global max. Sentinel via negative tracking. (#124)", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium) — Postorder DFS passing valid range [min, max] down; failure propagated similarly. (#98)", {})])),
    N.bullet(N.rich([("Convert Sorted Array to Binary Search Tree", {"bold": True}), (" (Easy) — Build the balanced tree from scratch — motivation for why balance matters. (#108)", {})])),
    N.bullet(N.rich([("Balance a Binary Search Tree", {"bold": True}), (" (Medium) — Inorder traversal to get sorted array, then rebuild balanced BST. Uses height-balance as the goal. (#1382)", {})])),
    N.para("All these problems share the core technique: process children before the parent (postorder), carry computed values upward, and short-circuit on failure."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS: Postorder sub-pattern", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the postorder DFS visually — use Next/Prev or arrow keys to see how heights compute bottom-up and how the −1 sentinel propagates on failure.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
