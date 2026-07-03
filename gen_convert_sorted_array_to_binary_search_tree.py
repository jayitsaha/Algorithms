"""
gen_convert_sorted_array_to_binary_search_tree.py
Creates the Notion page for LeetCode #108 - Convert Sorted Array to Binary Search Tree
notion_page_id = None -> create fresh page
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 1: Create page (notion_page_id is null) ──────────────────────────────
# Use the page already created in previous attempt; set PAGE_ID directly
PAGE_ID = "39193418-809c-81eb-acff-cf246e6abcc2"
print(f"Using existing page: {PAGE_ID}")

# ── Step 2: Set properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=108,
    pattern="Trees",
    subpatterns=["Mid as Root / Recurse"],
    tc="O(n)",
    sc="O(log n)",
    key_insight="Always pick the middle element as root — it splits the array into equal halves, guaranteeing a height-balanced BST.",
    icon="🟢",
)
print("Properties set.")

# ── Step 3: Wipe (fresh page — nothing to wipe, but call for safety) ──────────
N.wipe_page(PAGE_ID)

# ── Step 4: Build body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an integer array ",
        ("nums", {"code": True}),
        " where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.\n\n"
        "A height-balanced BST is a binary tree in which the depth of the two subtrees of every node never differs by more than one.\n\n"
        "Example: nums = [-10, -3, 0, 5, 9] → [0, -3, 9, -10, null, 5] (one valid answer)"
    ])),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive Mid as Root (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have a sorted array and need a binary search tree where no subtree is 'lopsided' "
            "(height difference ≤ 1). The BST property says left < root < right. "
            "Since the array is already sorted, any contiguous subarray already satisfies the BST ordering — "
            "we just need to decide what becomes the ROOT of each subtree."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Picking the first (or last) element as root: if nums = [-10, -3, 0, 5, 9] and we pick -10, "
            "the left subtree is empty and the right subtree has 4 nodes — a height-4 chain on the right, "
            "height 0 on the left. That is unbalanced. Recursing with 'first element as root' throughout "
            "just produces a sorted linked-list masquerading as a tree."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For a BALANCED split, we want the left and right subtrees to have equal (or near-equal) sizes. "
            "The element that achieves this is the MIDDLE element — it has exactly ⌊n/2⌋ elements to its left "
            "and ⌈n/2⌉ - 1 elements to its right (or vice versa). This is binary search in reverse: "
            "instead of finding the mid to search, we use the mid to BUILD."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Pick mid = (lo + hi) // 2 as the current root.\n"
            "2. Create a TreeNode with nums[mid].\n"
            "3. Recursively build the left subtree from nums[lo .. mid-1] — same problem, smaller input.\n"
            "4. Recursively build the right subtree from nums[mid+1 .. hi] — same problem, smaller input.\n"
            "5. Base case: if lo > hi (empty range), return None.\n"
            "This is classic divide-and-conquer — split at midpoint, solve each half, combine."
        ),
        N.callout(
            "Analogy: Think of binary search. When you search, you always look at the middle to decide "
            "where to go next. Here, you always PLACE the middle element as the root, then recurse on "
            "the two halves. Same midpoint logic — but we're building, not searching.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class TreeNode:\n"
        "    def __init__(self, val=0, left=None, right=None):\n"
        "        self.val = val\n"
        "        self.left = left\n"
        "        self.right = right\n"
        "\n"
        "def sortedArrayToBST(nums: list[int]) -> TreeNode:\n"
        "    def helper(lo: int, hi: int) -> TreeNode:\n"
        "        if lo > hi:\n"
        "            return None\n"
        "        mid = (lo + hi) // 2\n"
        "        node = TreeNode(nums[mid])\n"
        "        node.left  = helper(lo, mid - 1)\n"
        "        node.right = helper(mid + 1, hi)\n"
        "        return node\n"
        "    return helper(0, len(nums) - 1)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def helper(lo, hi):", {"code": True}),
                   " — subproblem definition: build and return a height-balanced BST from nums[lo..hi]."])),
    N.para(N.rich([("if lo > hi: return None", {"code": True}),
                   " — base case: empty range means no node to create. Returns None, which becomes a leaf's child."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}),
                   " — integer floor division gives the lower-middle index for even-length ranges. Both choices (floor or ceil) produce valid balanced BSTs."])),
    N.para(N.rich([("node = TreeNode(nums[mid])", {"code": True}),
                   " — create the current root node with the middle value. This is the BST root for the current subrange."])),
    N.para(N.rich([("node.left = helper(lo, mid - 1)", {"code": True}),
                   " — recursively build the left subtree from all elements left of mid. Guaranteed to be smaller (BST property preserved)."])),
    N.para(N.rich([("node.right = helper(mid + 1, hi)", {"code": True}),
                   " — recursively build the right subtree from all elements right of mid. Guaranteed to be larger."])),
    N.para(N.rich([("return node", {"code": True}),
                   " — return the fully-built subtree rooted at this node up to the caller."])),
    N.para(N.rich([("return helper(0, len(nums) - 1)", {"code": True}),
                   " — kick off the recursion on the full array range [0, n-1]."])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The recursive solution works by maintaining call frames — each frame knows its (lo, hi) range. "
            "We can simulate the exact same logic iteratively using an explicit stack of (node, lo, hi) triples."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Trying to build the tree in a simple left-to-right loop fails because we need to know "
            "each node's (lo, hi) subrange context to correctly assign children. Without that context, "
            "we can't determine the mid for each subtree."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The recursive call stack holds (node, lo, hi) implicitly. We can make it explicit: "
            "push (node, lo, hi) onto a stack when we create a node but haven't yet computed its children. "
            "Pop it when we're ready to assign children — the lo/hi tell us the midpoint."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create root from nums[mid] of the full array.\n"
            "2. Push (root, 0, n-1) onto the stack.\n"
            "3. While stack is non-empty: pop (node, lo, hi), compute mid, create left child "
            "if lo <= mid-1 and push it, create right child if mid+1 <= hi and push it.\n"
            "4. Return root."
        ),
        N.callout(
            "Use this approach when the interviewer asks for an iterative solution or when recursion "
            "depth is a concern (very large arrays). The recursive approach is cleaner and preferred "
            "unless explicitly asked otherwise.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def sortedArrayToBST(nums: list[int]) -> TreeNode:\n"
        "    if not nums:\n"
        "        return None\n"
        "    n = len(nums)\n"
        "    mid = n // 2\n"
        "    root = TreeNode(nums[mid])\n"
        "    # Stack stores (node, lo, hi) — the node whose children we still need to assign\n"
        "    stack = [(root, 0, n - 1)]\n"
        "    while stack:\n"
        "        node, lo, hi = stack.pop()\n"
        "        m = (lo + hi) // 2\n"
        "        # Left child: subrange [lo, m-1]\n"
        "        if lo <= m - 1:\n"
        "            lm = (lo + m - 1) // 2\n"
        "            node.left = TreeNode(nums[lm])\n"
        "            stack.append((node.left, lo, m - 1))\n"
        "        # Right child: subrange [m+1, hi]\n"
        "        if m + 1 <= hi:\n"
        "            rm = (m + 1 + hi) // 2\n"
        "            node.right = TreeNode(nums[rm])\n"
        "            stack.append((node.right, m + 1, hi))\n"
        "    return root"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = [(root, 0, n-1)]", {"code": True}),
                   " — initialize with the root node and its full range context."])),
    N.para(N.rich([("node, lo, hi = stack.pop()", {"code": True}),
                   " — pop a node that needs its children assigned."])),
    N.para(N.rich([("m = (lo + hi) // 2", {"code": True}),
                   " — compute the midpoint of this node's range (same formula as recursive)."])),
    N.para(N.rich([("if lo <= m - 1:", {"code": True}),
                   " — left subrange is non-empty; create left child and push for later processing."])),
    N.para(N.rich([("if m + 1 <= hi:", {"code": True}),
                   " — right subrange is non-empty; create right child and push for later processing."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",          "Space"],
        ["Recursive Mid as Root", "O(n)",          "O(log n) — recursion depth = tree height"],
        ["Iterative with Stack",  "O(n)",          "O(log n) — explicit stack size = tree height"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Divide & Conquer on sorted arrays)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Mid as Root, Recurse — always pick the midpoint of the current range as the root to guarantee balance"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'sorted array/list → BST' or 'height-balanced BST'\n"
        "• You need to construct a tree where the depth constraint is explicit\n"
        "• You see divide-and-conquer opportunities (sorted input + midpoint split)\n"
        "• The recursive structure mirrors binary search (same mid-point logic, different direction)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Convert Sorted List to Binary Search Tree", {"bold": True}),
                     " (Medium) — Same idea but on a linked list; need slow/fast pointer to find mid each time"])),
    N.bullet(N.rich([("Balance a Binary Search Tree", {"bold": True}),
                     " (Medium) — In-order traversal to get sorted array, then apply this exact algorithm"])),
    N.bullet(N.rich([("Construct BST from Preorder Traversal", {"bold": True}),
                     " (Medium) — Different traversal, but same BST construction insight"])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}),
                     " (Medium) — Same binary midpoint logic, but for searching rather than building"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}),
                     " (Medium) — BST in-order traversal is sorted; inverse of building from sorted array"])),
    N.bullet(N.rich([("Merge Sort", {"bold": True}),
                     " — Exact same divide-and-conquer pattern: split at mid, recurse both halves, combine"])),
    N.para("These problems share the core technique: midpoint divide-and-conquer on sorted structures."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, Mid as Root sub-pattern. "
              "Also see Divide & Conquer patterns where mid-splitting guarantees balance.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("convert_sorted_array_to_binary_search_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write page_id back for status file ────────────────────────────────────────
print(f"PAGE_ID={PAGE_ID}")
