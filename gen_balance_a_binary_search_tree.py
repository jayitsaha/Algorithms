"""
gen_balance_a_binary_search_tree.py
Notion page creation + body for LeetCode #1382 Balance a Binary Search Tree
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

SLUG = "balance_a_binary_search_tree"
NAME = "Balance a Binary Search Tree"
NUMBER = 1382
DIFFICULTY = "Medium"
ICON = "🟡"
PAGE_ID = "39293418-809c-811e-9a49-f10b10625bc4"  # already created

# ── Step 1: Set properties (use subpattern names without commas) ──
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern="Trees",
    subpatterns=["In-order to Array Rebuild", "DFS: Inorder"],
    tc="O(n)",
    sc="O(n)",
    key_insight="In-order traversal yields sorted values; pick the median as balanced root and recurse on both halves.",
    icon=ICON
)
print("Properties set.")

# ── Step 2: Wipe (fresh page — no wipe needed, but call for safety) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks (should be 0 for fresh page).")

# ── Step 3: Build body blocks ──
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("root", {"code": True}), " of a binary search tree, return ",
        "a balanced binary search tree with the same node values. ",
        "A balanced BST is one where the depth of the two subtrees of every node ",
        "never differs by more than 1. If there is more than one answer, return any of them."
    ])),
    N.divider(),
]

# ─── Solution 1 (Optimal - Interview Pick) ───
blocks += [
    N.h2("Solution 1 — In-Order + Sorted Array Rebuild (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a potentially skewed BST that is too tall. We need the same values arranged in a height-balanced tree. Two sub-questions: (1) how do I get all the values in sorted order cheaply? (2) how do I build an optimally balanced BST from a sorted sequence?"),
        N.h4("What Doesn't Work"),
        N.para("AVL rotations (LL, LR, RL, RR) are correct but notoriously complex to implement under interview pressure — multiple cases, pointer surgery, updating heights. Similarly, inserting nodes one-by-one into a new BST won't guarantee balance without a self-balancing tree structure."),
        N.h4("The Key Observation"),
        N.para("In-order traversal (Left → Root → Right) of ANY BST always visits nodes in sorted ascending order. This is a fundamental BST property. So Phase 1 is free: just do in-order DFS and collect values — no explicit sort needed. For Phase 2: the middle element of a sorted array is the perfect balanced BST root. It splits the array into two equal halves (±1 for odd/even), which become left and right subtrees by the same logic recursively."),
        N.h4("Building the Solution"),
        N.para("Step 1: In-order DFS collects all n values into a sorted array vals[]. O(n). Step 2: build(lo, hi) creates TreeNode(vals[mid]) as root, then recursively builds left = build(lo, mid-1) and right = build(mid+1, hi). The BST property is automatically preserved because vals is sorted: left subarray < mid < right subarray at every level. Balance is guaranteed because median split gives equal-size halves."),
        N.callout(
            "Analogy: Think of the sorted array as a phone book. The perfectly balanced index would put the entry at the exact middle as the root divider, left half for smaller entries, right half for larger. Apply this divider rule recursively to get a perfectly structured index.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""class Solution:
    def balanceBST(self, root: TreeNode) -> TreeNode:
        vals = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            vals.append(node.val)
            inorder(node.right)

        inorder(root)  # Phase 1: collect sorted values

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            node = TreeNode(vals[mid])
            node.left  = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(vals) - 1)  # Phase 2: rebuild balanced BST"""),
    N.h3("Line by Line"),
    N.para(N.rich([("vals = []", {"code": True}), " — Initialize empty list to collect in-order values. This will become a sorted array after Phase 1."])),
    N.para(N.rich([("def inorder(node):", {"code": True}), " — Recursive helper for in-order DFS. Left → Root → Right traversal."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — Base case: None node means empty subtree, nothing to visit."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Recurse left first: this ensures smaller values are visited before the current node."])),
    N.para(N.rich([("vals.append(node.val)", {"code": True}), " — Visit the current node: append its value. At this point all left descendants (smaller values) have already been appended."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Recurse right: append all larger values after the current node. Combined, the three lines produce sorted order."])),
    N.para(N.rich([("inorder(root)", {"code": True}), " — Kick off Phase 1. After this call, vals is a sorted array of all node values."])),
    N.para(N.rich([("def build(lo, hi):", {"code": True}), " — Divide-and-conquer helper. Works on the subarray vals[lo..hi]."])),
    N.para(N.rich([("if lo > hi: return None", {"code": True}), " — Base case: empty range means no node to create (this becomes a None child of the parent)."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — Compute the median index. This is the balanced split point: equal elements on each side (±1)."])),
    N.para(N.rich([("node = TreeNode(vals[mid])", {"code": True}), " — The median value becomes the root of this subtree."])),
    N.para(N.rich([("node.left = build(lo, mid - 1)", {"code": True}), " — Recursively build left subtree from the left half. All values < vals[mid] by sorted-array guarantee."])),
    N.para(N.rich([("node.right = build(mid + 1, hi)", {"code": True}), " — Recursively build right subtree from the right half. All values > vals[mid]."])),
    N.para(N.rich([("return build(0, len(vals) - 1)", {"code": True}), " — Kick off Phase 2 on the full sorted array. Returns the root of the new balanced BST."])),
    N.divider(),
]

# ─── Solution 2 ───
blocks += [
    N.h2("Solution 2 — Brute Force (Generic Binary Tree Approach)"),
    N.toggle_h3("💡 Intuition: Why This Is Suboptimal", [
        N.h4("Reframe the Problem"),
        N.para("The brute-force approach treats the BST as a generic binary tree — it collects values without using the BST's sorted-order property, then sorts them explicitly."),
        N.h4("What Doesn't Work"),
        N.para("If we don't use in-order traversal, the collected values are not sorted. We must call vals.sort() explicitly, costing O(n log n) — worse than the O(n) solution."),
        N.h4("The Key Observation"),
        N.para("This approach is valid for any binary tree (not just BSTs), but it wastes the BST's key property. The rebuild phase (build) is identical to Solution 1."),
        N.callout(
            "Use this when the input is a general binary tree (not a BST). For a BST, always use in-order traversal to get sorted order for free.",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""def balanceBST_brute(root):
    vals = []

    def collect(node):          # Any traversal order works
        if not node:
            return
        vals.append(node.val)   # Collect in preorder
        collect(node.left)
        collect(node.right)

    collect(root)
    vals.sort()                 # Explicit sort: O(n log n) — avoidable for BST!

    def build(lo, hi):          # Same rebuild phase as Solution 1
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(vals[mid])
        node.left  = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(vals) - 1)"""),
    N.h3("Line by Line"),
    N.para("collect() uses preorder traversal (any order works here since we sort later). After collect(), vals is unsorted. vals.sort() costs O(n log n). The build phase is identical to Solution 1. Total: O(n log n) time vs O(n) for Solution 1."),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["In-Order + Rebuild (S1)", "O(n)", "O(n)", "Interview pick. Space for vals[] array."],
        ["Brute Force (S2)", "O(n log n)", "O(n)", "Explicit sort. Works on any binary tree."],
        ["Day-Stout-Warren (DSW)", "O(n)", "O(1)", "In-place. Very complex. Not expected in interviews."],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Tree Traversal + Divide and Conquer Rebuild)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order to Array, Rebuild; DFS: Inorder (Left→Root→Right yields BST sorted order)"])),
    N.callout(
        "When to recognize this pattern: (1) Problem says 'balance' or 'height-balanced' a BST. (2) Problem gives a BST and asks you to restructure it. (3) Any problem needing sorted order from a BST — in-order traversal gives it for free. (4) 'Convert sorted array/list to balanced BST' — identical build() function.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (in-order traversal + sorted array rebuild):"),
    N.bullet(N.rich([("Convert Sorted Array to Binary Search Tree", {"bold": True}), " (Easy, #108) — The exact same build(lo, hi) function. Phase 1 is already done for you."])),
    N.bullet(N.rich([("Convert Sorted List to Binary Search Tree", {"bold": True}), " (Medium, #109) — Same idea with linked list input. Use slow/fast pointer to find median instead of index arithmetic."])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium, #230) — In-order traversal gives sorted order; stop at k-th element. Same Phase 1 pattern with early exit."])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium, #98) — Verify in-order traversal is strictly increasing. Same in-order DFS as Phase 1."])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium, #173) — Controlled in-order using an explicit stack. Streaming Phase 1 that yields one value at a time."])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), " (Easy, #110) — Check if a tree IS height-balanced. Use postorder DFS returning height; check |left-right| <= 1. Verifies the output of this problem."])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), " (Medium, #114) — Complementary problem: flatten (preorder) instead of balanced rebuild."])),
    N.para("These problems share the core insight: BST in-order traversal = sorted sequence, and sorted sequences enable optimal BST construction via median selection."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Trees, DFS: Inorder sub-pattern. Also see 'In-order to Array, Rebuild' technique in the Trees section.", "📚", "gray_background"),
]

# ─── Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
