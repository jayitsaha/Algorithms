"""
gen_validate_binary_search_tree.py
Notion in-place update for LeetCode #98 — Validate Binary Search Tree
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c8-bf7e-e75a50e35d5c"
SLUG    = "validate_binary_search_tree"

# ── 1. Set properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=98,
    pattern="Trees",
    subpatterns=["In-order Increasing Check"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Carry inherited bounds (low, high) through DFS; every node must be strictly inside its ancestor-derived range.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "),
        ("root", {"code": True}),
        (" of a binary tree, determine if it is a valid binary search tree (BST). "
         "A valid BST is defined as follows:\n"
         "• The left subtree of a node contains only nodes with keys strictly less than the node's key.\n"
         "• The right subtree of a node contains only nodes with keys strictly greater than the node's key.\n"
         "• Both the left and right subtrees must also be binary search trees."),
    ])),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────────────
SOLUTION_1_CODE = """\
def isValidBST(root: TreeNode) -> bool:
    def validate(node, low, high):
        if node is None:
            return True                          # null subtree is always valid
        if node.val <= low or node.val >= high:
            return False                         # out of inherited range
        return (validate(node.left,  low, node.val)   # go left: tighten upper bound
             and validate(node.right, node.val, high)) # go right: tighten lower bound
    return validate(root, float('-inf'), float('inf'))  # root: unconstrained
"""

blocks += [
    N.h2("Solution 1 — DFS with Inherited Bounds (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to verify that every node in the tree satisfies the BST property globally — "
               "not just relative to its immediate parent. The question becomes: "
               "what range of values is each node allowed to have, given all the decisions "
               "(left/right turns) taken to reach it from the root?"),
        N.h4("What Doesn't Work"),
        N.para("Checking only parent-child pairs misses global violations. Example: root=5, right child=4, "
               "with 4's children being 3 and 6. Every adjacent pair looks valid, but 4 is a right child of 5 "
               "and must be greater than 5. Local checks cannot catch this."),
        N.h4("The Key Observation"),
        N.para("Each node inherits constraints from ALL its ancestors — not just its parent. "
               "When we go left from a node with value V, the entire left subtree must be less than V. "
               "When we go right, the entire right subtree must be greater than V. "
               "These constraints accumulate as we descend: each node receives a range (low, high) that "
               "captures every ancestor's contribution."),
        N.h4("Building the Solution"),
        N.para("1. Start at root with range (-∞, +∞) — no ancestor constraints yet.\n"
               "2. Null node → return True (base case; empty subtree is valid).\n"
               "3. Check: node.val must be strictly inside (low, high). If not → return False.\n"
               "4. Recurse left with upper bound tightened to node.val.\n"
               "5. Recurse right with lower bound tightened to node.val.\n"
               "6. Return the AND of both recursive results."),
        N.callout(
            "Analogy: Think of the bounds as a narrowing corridor. The root can be any value. "
            "As you descend left, the ceiling drops to your parent's value. As you descend right, "
            "the floor rises to your parent's value. A valid BST means every node fits within its corridor.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def validate(node, low, high):", {"code": True}),
                   " — Inner helper that receives the current node plus the inherited valid range (low, high). "
                   "This range encodes all constraints from every ancestor above this node."])),
    N.para(N.rich([("if node is None: return True", {"code": True}),
                   " — Base case. An empty subtree trivially satisfies BST property. "
                   "Handles leaf children without any special-casing."])),
    N.para(N.rich([("if node.val <= low or node.val >= high:", {"code": True}),
                   " — The core check. The node's value must be strictly inside (low, high). "
                   "Using <= and >= enforces strict BST ordering — equal values are violations. "
                   "If this fails, we return False immediately (fail fast)."])),
    N.para(N.rich([("validate(node.left, low, node.val)", {"code": True}),
                   " — Recurse left. The new upper bound becomes node.val, because everything in the "
                   "left subtree must be less than the current node. The lower bound is unchanged."])),
    N.para(N.rich([("validate(node.right, node.val, high)", {"code": True}),
                   " — Recurse right. The new lower bound becomes node.val, because everything in the "
                   "right subtree must be greater than the current node. The upper bound is unchanged."])),
    N.para(N.rich([("validate(root, float('-inf'), float('inf'))", {"code": True}),
                   " — Entry point. Using float infinity means the root runs the exact same comparison "
                   "logic as every other node — no special root handling needed."])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────────────
SOLUTION_2_CODE = """\
def isValidBST(root: TreeNode) -> bool:
    prev = [float('-inf')]       # tracks last in-order value seen
    def inorder(node):
        if node is None: return True
        if not inorder(node.left): return False   # recurse LEFT first
        if node.val <= prev[0]: return False       # must be strictly greater than previous
        prev[0] = node.val                         # update previous
        return inorder(node.right)                 # recurse RIGHT last
    return inorder(root)
"""

blocks += [
    N.h2("Solution 2 — In-Order Traversal with Previous Value Tracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A valid BST's in-order traversal (left → root → right) always visits nodes in "
               "strictly increasing order. This is a fundamental property of BSTs — it follows "
               "directly from the definition. We can exploit this: instead of reasoning about bounds, "
               "just traverse in-order and check that each value is strictly greater than the previous."),
        N.h4("What Doesn't Work"),
        N.para("Simply collecting all values into a list and then checking if the list is sorted works "
               "but uses O(n) extra space for the list. We can do it with O(1) extra space by checking "
               "incrementally during traversal, failing early on the first violation."),
        N.h4("The Key Observation"),
        N.para("In-order traversal is left-root-right. When we visit a node (the 'root' step), "
               "all nodes in its left subtree have already been visited. So prev holds the maximum "
               "value in the left subtree. The BST property requires current > prev at every step."),
        N.h4("Building the Solution"),
        N.para("1. Initialize prev = -∞ (no node visited yet).\n"
               "2. Traverse in-order (left first, then current node, then right).\n"
               "3. After visiting left subtree, check: current value must be > prev.\n"
               "4. Update prev = current value.\n"
               "5. Recurse right. If any check fails, propagate False upward."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = [float('-inf')]", {"code": True}),
                   " — We use a list (single-element) so the nested function can mutate it. "
                   "Alternatively use nonlocal in Python 3. Initialized to -∞ since no node is visited yet."])),
    N.para(N.rich([("if not inorder(node.left): return False", {"code": True}),
                   " — Recurse left FIRST (in-order = left → root → right). "
                   "Short-circuit: if left subtree fails, return immediately."])),
    N.para(N.rich([("if node.val <= prev[0]: return False", {"code": True}),
                   " — The in-order check. After visiting the entire left subtree, "
                   "prev holds the maximum value in it. Current node must be strictly greater. "
                   "Uses <= to reject duplicates (strict BST)."])),
    N.para(N.rich([("prev[0] = node.val", {"code": True}),
                   " — Update prev to current. All future nodes to the right must be greater than this."])),
    N.para(N.rich([("return inorder(node.right)", {"code": True}),
                   " — Recurse right LAST (in-order). Result propagates up — if right fails, the whole call fails."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS with Bounds (Interview Pick)", "O(n)", "O(h)"],
        ["In-Order Traversal", "O(n)", "O(h)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order Increasing Check / BST Property / DFS: Inorder"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks to validate a property on a binary tree — think DFS with top-down state. "
        "(2) Property involves relationships across multiple levels, not just parent-child — carry bounds. "
        "(3) BST operations (search, insert, validate, kth element) — exploit strict ordering. "
        "(4) 'In-order' mentioned or implied (sorted order, increasing sequence) — traverse left-root-right.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}),
                     " (Medium) — In-order traversal, count nodes until reaching the kth (#230)"])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}),
                     " (Medium) — Implement in-order iterator using a controlled stack (#173)"])),
    N.bullet(N.rich([("Recover Binary Search Tree", {"bold": True}),
                     " (Hard) — Two nodes swapped; detect the two out-of-order elements via in-order (#99)"])),
    N.bullet(N.rich([("Lowest Common Ancestor of a BST", {"bold": True}),
                     " (Medium) — Exploit BST ordering to descend toward both target nodes (#235)"])),
    N.bullet(N.rich([("Convert Sorted Array to BST", {"bold": True}),
                     " (Easy) — Divide and conquer: pick midpoint as root to guarantee balance (#108)"])),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}),
                     " (Easy) — Exploit ordering: eliminate half the tree at each step (#700)"])),
    N.para("These problems share the same core insight: BSTs have a strict global ordering property "
           "that can be exploited via in-order traversal (which yields sorted order) or via "
           "top-down DFS with inherited range bounds."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5 (Trees → DFS: Inorder / BST Property). "
        "Sub-pattern: In-order Increasing Check. Source: Guide Section 5.",
        "📚", "gray_background"
    ),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ─────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print(f"NOTION OK {PAGE_ID}")
