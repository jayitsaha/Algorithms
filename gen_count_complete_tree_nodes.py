"""
gen_count_complete_tree_nodes.py
Regenerates Notion page for LeetCode #222 Count Complete Tree Nodes IN-PLACE.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815d-991e-f05b47f1f738"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=222,
    pattern="Trees",
    subpatterns=["Left/Right Height Compare"],
    tc="O(log²n)",
    sc="O(log n)",
    key_insight="If left-spine height == right-spine height, the subtree is a perfect binary tree; count it instantly as (2^h - 1) and recurse only into the other half.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a ", {}),
        ("complete binary tree", {"bold": True}),
        (", return the number of the nodes in the tree.", {}),
        ("\n\nA complete binary tree is one in which every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible.", {}),
        ("\n\nDesign an algorithm that runs in less than O(n) time complexity.", {}),
        ("\n\nConstraints: the number of nodes in the tree is in the range [0, 5×10⁴], 0 ≤ Node.val ≤ 5×10⁴.", {}),
    ])),
    N.divider(),
]

# ─────── Solution 1: Brute Force DFS ───────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force DFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count every node in a binary tree. The simplest possible approach: visit every node exactly once and add 1 for each."),
        N.h4("What Doesn't Work"),
        N.para("Nothing 'doesn't work' here — brute force is correct but O(n). The problem explicitly asks for sub-linear time, so this serves only as a starting point to motivate the optimal approach."),
        N.h4("The Key Observation"),
        N.para("A simple recursive count works: a tree's node count equals 1 (the root) plus the count of the left subtree plus the count of the right subtree. This is the textbook postorder DFS."),
        N.h4("Building the Solution"),
        N.para("Base case: empty node returns 0. Recursive case: return 1 + countNodes(root.left) + countNodes(root.right). Every node is visited once, so time is O(n) and space is O(h) for the call stack where h is the height."),
        N.callout("Analogy: Count people in a room by pointing at each one and saying 'one more'. Simple but you must look at every person.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root:", {"code": True}), (" — Base case: empty tree has 0 nodes.", {})])),
    N.para(N.rich([("return 0", {"code": True}), (" — Return immediately for empty subtree.", {})])),
    N.para(N.rich([("return 1 + self.countNodes(root.left) + self.countNodes(root.right)", {"code": True}), (" — Count this node (1) plus recursively count both subtrees.", {})])),
    N.divider(),
]

# ─────── Solution 2: Left/Right Height Compare (OPTIMAL) ───────────────────
OPTIMAL_CODE = """class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        lh = self._height(root, left=True)   # left-spine depth
        rh = self._height(root, left=False)  # right-spine depth

        if lh == rh:
            # This subtree is a PERFECT binary tree
            # A perfect tree of height h has exactly 2^h - 1 nodes
            return (1 << lh) - 1
        else:
            # Not perfect: count root + recurse into both children
            # But ONE of the children is always perfect (we just don't know which)
            return 1 + self.countNodes(root.left) + self.countNodes(root.right)

    def _height(self, node: Optional[TreeNode], left: bool) -> int:
        h = 0
        while node:
            h += 1
            node = node.left if left else node.right
        return h"""

blocks += [
    N.h2("Solution 2 — Left/Right Height Compare (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The problem says 'complete binary tree' and 'less than O(n)'. These two constraints together are the signal: we must exploit the structure of completeness to skip large swaths of nodes."),
        N.h4("What Doesn't Work"),
        N.para("DFS that visits every node is O(n) — the problem explicitly forbids this. We need to count subtrees without visiting all their nodes."),
        N.h4("The Key Observation"),
        N.para("In a complete binary tree, at any node, if we walk only-left we reach the deepest left leaf, and if we walk only-right we reach the deepest right leaf. If these walks have the same length, the ENTIRE subtree rooted at this node is a PERFECT binary tree. A perfect tree of height h has exactly 2^h - 1 nodes — computable in O(1)."),
        N.h4("Building the Solution"),
        N.para("1. Compute left-spine height: descend always left until None. O(log n).\n2. Compute right-spine height: descend always right until None. O(log n).\n3. If equal: subtree is perfect. Return (1 << lh) - 1. No recursion needed.\n4. If not equal: recurse into both children. One of them will be detected as perfect at the next level."),
        N.callout("Key fact: In a complete binary tree, the left subtree and right subtree are ALWAYS complete. And at least one of them is guaranteed to be PERFECT. So we will always skip half the work at every level. This gives O(log n) levels × O(log n) height work = O(log²n) total.", "🎯", "green_background"),
        N.callout("Analogy: Imagine counting books on shelves. If a shelf is perfectly packed (all spots filled), you don't count — you just compute. Only uneven shelves need closer inspection.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Why One Subtree Is Always Perfect"),
    N.para("In a complete binary tree rooted at node X:\n- If lh == rh: The last level is fully filled within this subtree → PERFECT. Count = 2^lh - 1.\n- If lh > rh (always lh = rh+1 for complete trees): The last level has nodes but doesn't extend all the way right → root.right subtree is a perfect tree of height rh, and root.left subtree is complete (recurse into it).\n\nThis ensures each recursive call either terminates immediately (O(1) count) or recurses into a subtree half the size. Depth of recursion: O(log n). Work per level: O(log n) for height computation. Total: O(log²n)."),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root:", {"code": True}), (" — Empty tree: 0 nodes.", {})])),
    N.para(N.rich([("lh = self._height(root, left=True)", {"code": True}), (" — Walk left spine: count nodes from root to bottom-left leaf. O(log n).", {})])),
    N.para(N.rich([("rh = self._height(root, left=False)", {"code": True}), (" — Walk right spine: count nodes from root to bottom-right leaf. O(log n).", {})])),
    N.para(N.rich([("if lh == rh:", {"code": True}), (" — Equal heights mean every level is completely filled in this subtree → perfect binary tree.", {})])),
    N.para(N.rich([("return (1 << lh) - 1", {"code": True}), (" — Bit-shift computes 2^lh in O(1). Subtract 1 because a perfect tree of height h has 2^h - 1 nodes (not 2^h).", {})])),
    N.para(N.rich([("return 1 + self.countNodes(root.left) + self.countNodes(root.right)", {"code": True}), (" — Not perfect: count root + recurse. One child will be found perfect at next level.", {})])),
    N.para(N.rich([("while node:", {"code": True}), (" in _height — Walk spine until we fall off the tree.", {})])),
    N.para(N.rich([("h += 1", {"code": True}), (" — Count this node as one level of height.", {})])),
    N.para(N.rich([("node = node.left if left else node.right", {"code": True}), (" — Move left (for left-spine) or right (for right-spine).", {})])),
    N.callout("⚠️ Why (1 << lh) - 1 and NOT (1 << lh)? A perfect binary tree of height h (where h = number of nodes on the spine, counting root) has 2^h - 1 total nodes. Example: height 3 = 7 nodes (1 root + 2 level-2 + 4 leaves = 7). (1<<3) = 8, (1<<3)-1 = 7. ✓", "⚠️", "yellow_background"),
    N.divider(),
]

# ─────── Solution 3: Iterative / Binary Search variant ─────────────────────
ITER_CODE = """class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # Get tree height (number of levels)
        height = 0
        node = root
        while node.left:
            height += 1
            node = node.left

        # Binary search: how many nodes exist in the last level?
        # Last level nodes are indexed 0 to 2^height - 1 (left to right)
        lo, hi = 0, (1 << height) - 1

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._exists(root, height, mid):
                lo = mid
            else:
                hi = mid - 1

        # Total = all nodes above last level + (lo + 1) nodes in last level
        return (1 << height) - 1 + lo + 1

    def _exists(self, root, height, index):
        \"\"\"Check if the node at position 'index' in the last level exists.\"\"\"
        lo, hi = 0, (1 << height) - 1
        node = root
        for _ in range(height):
            mid = (lo + hi) // 2
            if index <= mid:
                node = node.left
                hi = mid
            else:
                node = node.right
                lo = mid + 1
        return node is not None"""

blocks += [
    N.h2("Solution 3 — Binary Search on Last Level"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For a complete tree of height h, all internal nodes are filled. The only question is: how many nodes exist in the last level? If we can binary search the last level, we avoid visiting most nodes."),
        N.h4("What Doesn't Work"),
        N.para("Scanning the entire last level node by node is O(n/2) = O(n). We need to binary-search it instead."),
        N.h4("The Key Observation"),
        N.para("The last level of a complete binary tree fills left-to-right. We can binary search for the rightmost present node: for candidate position mid, check if the node exists by navigating from root using binary path encoding. Each existence check takes O(h) = O(log n), and we do O(log n) binary search steps → O(log²n) total."),
        N.h4("Building the Solution"),
        N.para("1. Find tree height h. All nodes above last level: 2^h - 1.\n2. Binary search for the rightmost node at level h (positions 0 to 2^h - 1).\n3. To check if position mid exists: decode its binary path from root in O(h) steps.\n4. Total = (2^h - 1) + (rightmost position + 1)."),
    ]),
    N.h3("Code"),
    N.code(ITER_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("height = 0; while node.left: height += 1; node = node.left", {"code": True}), (" — Count levels by descending left spine. height = number of edges to bottom.", {})])),
    N.para(N.rich([("lo, hi = 0, (1 << height) - 1", {"code": True}), (" — Last level positions are 0-indexed from 0 to 2^height - 1.", {})])),
    N.para(N.rich([("mid = (lo + hi + 1) // 2", {"code": True}), (" — Upper-mid keeps search from infinite loop when lo+1 == hi.", {})])),
    N.para(N.rich([("self._exists(root, height, index)", {"code": True}), (" — Navigate from root to position index using binary path: left if index ≤ mid of current range, else right.", {})])),
    N.para(N.rich([("return (1 << height) - 1 + lo + 1", {"code": True}), (" — All nodes in full levels above last + (lo+1) nodes in last level.", {})])),
    N.divider(),
]

# ─────── Complexity ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DFS", "O(n)", "O(h) = O(log n) stack"],
        ["Left/Right Height Compare (Optimal)", "O(log²n)", "O(log n) stack"],
        ["Binary Search on Last Level", "O(log²n)", "O(log n) stack"],
    ]),
    N.para("h = tree height = O(log n) for a complete binary tree. The optimal solutions both run in O(log²n) because they do O(log n) recursive calls, each performing O(log n) work for height measurement."),
    N.divider(),
]

# ─────── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Left/Right Height Compare (Structure Exploitation)", {})])),
    N.callout(
        "When to recognize this pattern:\n• Problem involves a complete (or perfect) binary tree\n• Asked to count nodes faster than O(n)\n• Key words: 'complete binary tree', 'less than O(n)'\n• Clue: the tree structure itself gives you shortcut information",
        "🔎", "green_background"
    ),
    N.para("This sub-pattern exploits the structural guarantee of complete binary trees: one subtree is always a perfect binary tree and can be counted in O(1) using bit shifting. Verified against DSA_Patterns_and_SubPatterns_Guide.md Trees section."),
    N.divider(),
]

# ─────── Related Problems ────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same structure-exploitation technique on trees:"),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), (" (Easy) — Height measurement is the core sub-operation", {})])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), (" (Easy) — Also compares left and right subtree heights", {})])),
    N.bullet(N.rich([("Find Bottom Left Tree Value", {"bold": True}), (" (Medium) — Exploits level structure of complete binary tree", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), (" (Medium) — Uses structural property (BST ordering) to skip subtrees", {})])),
    N.bullet(N.rich([("Check Completeness of a Binary Tree", {"bold": True}), (" (Medium) — Directly tests the complete-tree property used here", {})])),
    N.bullet(N.rich([("Sum of Nodes with Even-Valued Grandparent", {"bold": True}), (" (Medium) — Recursive tree traversal with condition propagation", {})])),
    N.bullet(N.rich([("Perfect Binary Tree", {"bold": True}), (" (Easy/concept) — A perfect tree is the special case where lh==rh at every node", {})])),
    N.para("These problems share the core technique of using tree structure properties to avoid visiting all O(n) nodes when a structural guarantee lets you compute subtree results directly."),
    N.callout("📚 Pattern: Trees → Left/Right Height Compare. Related sub-patterns in DSA guide: DFS Postorder (tree height), BFS Level Order (count nodes per level), BST Property (skip subtrees based on ordering).", "📚", "gray_background"),
    N.divider(),
]

# ─────── Interactive Visual Explainer ────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("count_complete_tree_nodes")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
