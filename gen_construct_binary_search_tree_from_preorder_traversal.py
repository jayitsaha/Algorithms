import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8111-864d-d655bc517e15"
SLUG = "construct_binary_search_tree_from_preorder_traversal"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1008,
    pattern="Trees",
    subpatterns=["Upper Bound Tracking"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Pass an upper bound into each recursive call; the shared index advances once per node, eliminating the O(n) split-scan per level.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Rebuild body
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("preorder", {"code": True}),
        (", which represents the preorder traversal of a BST (binary search tree), construct the tree and return its root node. It is guaranteed that there is always possible to find a BST for the given preorder sequence.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Upper Bound Tracking (Interview Pick) ──
SOL1_CODE = """\
class Solution:
    def bstFromPreorder(self, preorder):
        self.i = [0]          # mutable index shared across all recursive calls
        def build(upper):     # only place values strictly less than upper
            if self.i[0] == len(preorder):
                return None
            val = preorder[self.i[0]]
            if val >= upper:  # this value belongs to an ancestor, not here
                return None
            self.i[0] += 1   # commit: advance shared index
            node = TreeNode(val)
            node.left  = build(val)    # left child: tighter bound = current val
            node.right = build(upper)  # right child: inherits same upper bound
            return node
        return build(float('inf'))     # root has no upper constraint
"""

blocks += [
    N.h2("Solution 1 — Upper Bound Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a preorder traversal (Root → Left → Right) of a BST. We need to reverse-engineer the tree. The challenge: preorder of a general binary tree isn't uniquely decodable, but preorder of a BST IS — because the BST property tells us exactly which values go left vs. right."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach scans to find the split point at each level (first element > root). This is O(n) per level and O(n²) total for a skewed tree. We need to avoid redundant scanning."),
        N.h4("The Key Observation"),
        N.para("Instead of scanning for the split, we can pass a bound: any value in the current subtree must be strictly less than the 'upper' constraint from its parent. The moment we see a value >= upper, we know it belongs to a caller frame, not here — return None without advancing the index."),
        N.h4("Building the Solution"),
        N.para("Use a shared mutable index (self.i = [0]) that all recursive calls can advance. At each call: peek at preorder[i], check if val < upper. If yes, consume it (advance index) and recurse. Left call gets upper = node.val. Right call inherits same upper. This ensures exactly n advances total — O(n)."),
        N.callout("Analogy: The bound is like a checkpoint. When you're filling the left subtree, you can only use values below the parent's value. The moment you see a value that would cross the parent's barrier, stop — the parent's right subtree will handle it.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.i = [0]", {"code": True}), " — Create a mutable list wrapping the shared index. All recursive frames share this object; mutations are visible everywhere."])),
    N.para(N.rich([("def build(upper)", {"code": True}), " — Inner function. The parameter ", ("upper", {"code": True}), " is the exclusive maximum value allowed in this subtree."])),
    N.para(N.rich([("if self.i[0] == len(preorder): return None", {"code": True}), " — Base case: we've consumed all elements — nothing to place here."])),
    N.para(N.rich([("val = preorder[self.i[0]]", {"code": True}), " — Peek (don't commit yet) at the next preorder element."])),
    N.para(N.rich([("if val >= upper: return None", {"code": True}), " — This value doesn't belong in this subtree — index stays unchanged; caller will handle it."])),
    N.para(N.rich([("self.i[0] += 1", {"code": True}), " — Commit: this element is ours. Advance the shared index past it."])),
    N.para(N.rich([("node = TreeNode(val)", {"code": True}), " — Create the BST node for this position in the tree."])),
    N.para(N.rich([("node.left = build(val)", {"code": True}), " — Recurse left. Left subtree's upper bound tightens to the current node's value (all left descendants < this node)."])),
    N.para(N.rich([("node.right = build(upper)", {"code": True}), " — Recurse right. Right subtree inherits the same upper bound from this node's parent context."])),
    N.para(N.rich([("return build(float('inf'))", {"code": True}), " — Start with infinite upper bound: the root is unconstrained."])),
    N.divider(),
]

# ── Solution 2: Naive Split ──
SOL2_CODE = """\
def bstFromPreorder(self, preorder):
    if not preorder:
        return None
    root = TreeNode(preorder[0])   # first element is always root
    i = 1
    while i < len(preorder) and preorder[i] < root.val:
        i += 1                     # O(n) scan per level → O(n²) worst case
    root.left  = self.bstFromPreorder(preorder[1:i])
    root.right = self.bstFromPreorder(preorder[i:])
    return root
"""

blocks += [
    N.h2("Solution 2 — Naive Split Search (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("In preorder, the root comes first. All smaller values form the left subtree, all larger form the right. Find that split point, then recurse on each half."),
        N.h4("What Doesn't Work"),
        N.para("For a skewed BST (e.g., all values ascending), the split scan happens at every level, each O(n) → O(n²) total. Also, creating subarrays with slicing wastes O(n) memory per level."),
        N.h4("The Key Observation"),
        N.para("This is the direct translation of the recursive BST definition into code. Simple and correct — a good starting point in an interview before optimizing."),
        N.h4("Building the Solution"),
        N.para("Take preorder[0] as root. Scan forward to find first element > root — that's index i. Recurse on preorder[1:i] for left, preorder[i:] for right."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not preorder: return None", {"code": True}), " — Base case: empty array means no subtree to build."])),
    N.para(N.rich([("root = TreeNode(preorder[0])", {"code": True}), " — First element is always the root of this (sub)tree."])),
    N.para(N.rich([("while i < len and preorder[i] < root.val", {"code": True}), " — Scan for the split: all left elements are less than root."])),
    N.para(N.rich([("root.left = self.bstFromPreorder(preorder[1:i])", {"code": True}), " — Left subtree: elements from index 1 up to (not including) i."])),
    N.para(N.rich([("root.right = self.bstFromPreorder(preorder[i:])", {"code": True}), " — Right subtree: elements from i onward."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Split Search", "O(n²) worst / O(n log n) avg", "O(n²) due to slicing"],
        ["Upper Bound Tracking (optimal)", "O(n)", "O(n) stack + output tree"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (BST & Tries — Section 12.1)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Upper Bound Tracking"])),
    N.callout(
        "When to recognize this pattern: problem says 'reconstruct BST from traversal' or 'preorder/postorder of BST'. Key signal: BST property means you don't need inorder — the bound replaces the linear scan for the split point.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or closely related BST reconstruction/validation:"),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Inorder Traversal", {"bold": True}), " (Medium) — General tree needs both traversals; BST only needs preorder (#105)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — Same upper/lower bound range passed through recursion (#98)"])),
    N.bullet(N.rich([("Serialize and Deserialize BST", {"bold": True}), " (Medium) — Encode as preorder; decode with upper bound tracking (#449)"])),
    N.bullet(N.rich([("Verify Preorder Sequence in Binary Search Tree", {"bold": True}), " (Medium) — Check validity without building tree, monotonic stack (#255)"])),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}), " (Medium) — Same BST navigation by value comparison (#701)"])),
    N.bullet(N.rich([("Recover Binary Search Tree", {"bold": True}), " (Medium) — Find two swapped nodes via inorder, exploits BST order invariant (#99)"])),
    N.para("These problems share the core insight: BST property allows valid range to propagate through recursion, enabling O(n) construction/validation without additional data structures."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 12.1 — BST & Tries → Binary Search Tree Operations. Sub-Pattern: Upper Bound Tracking.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
