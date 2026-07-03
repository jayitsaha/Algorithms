import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-810a-97b8-c271665d5585"

# 1) Set page properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=99,
    pattern="Trees",
    subpatterns=["In-order Find Two Swapped"],
    tc="O(n)",
    sc="O(h)",
    key_insight="In-order traversal of a BST gives sorted order; two swapped nodes create 1-2 inversions — find them with a prev pointer and swap their values.",
    icon="🟡"
)
print("Properties set OK")

# 2) Wipe old content
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# 3) Rebuild body
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(
        "You are given the root of a binary search tree (BST) where exactly two nodes "
        "have been swapped by mistake. Recover the BST without changing its structure "
        "(only swap the values back)."
    ),
    N.callout(
        "Example: root=[3,1,4,null,null,2] → in-order gives [1,3,2,4] — nodes with values "
        "3 and 2 are swapped. Fix: swap their values → root=[2,1,4,null,null,3] → in-order [1,2,3,4] ✓",
        "📌", "gray_background"
    ),
    N.divider()
]

# ── Solution 1: Optimal ──
blocks += [
    N.h2("Solution 1 — In-order Traversal with prev Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A correct BST's in-order traversal (Left → Node → Right) always produces a "
            "strictly increasing sequence. Two swapped nodes break this sorted order. "
            "So the problem reduces to: find the anomalies in an otherwise-sorted sequence."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A brute force approach (collect all nodes, sort values, reassign) is O(n log n) "
            "and O(n) space. We can do better since we know exactly two values are wrong — "
            "we just need to find the one or two inversions in the traversal."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two swapped values in a sorted sequence create at most 2 'inversions' — places "
            "where prev.val > curr.val. At the first inversion, prev is the misplaced large node. "
            "At the second inversion (if any), curr is the misplaced small node. "
            "Adjacent swaps create only 1 inversion; non-adjacent create 2."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Perform in-order DFS, tracking prev node.\n"
            "2. At each step, if prev.val > node.val: it's an inversion.\n"
            "   - First inversion: set first = prev, second = node.\n"
            "   - Any later inversion: update second = node.\n"
            "3. After traversal: swap first.val and second.val."
        ),
        N.callout(
            "Analogy: Imagine a sorted bookshelf. Two books are swapped. Walk left to right — "
            "you'll find at most two spots where the book in your hand is smaller than the one "
            "you just passed. The first mis-ordered book (too large) and the last mis-ordered "
            "book (too small) are your two swapped books.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
        "def recoverTree(root):\n"
        "    first = second = None\n"
        "    class Sentinel: val = float('-inf')\n"
        "    prev = Sentinel()\n"
        "\n"
        "    def inorder(node):\n"
        "        nonlocal first, second, prev\n"
        "        if not node:\n"
        "            return\n"
        "        inorder(node.left)             # Left\n"
        "        if prev.val > node.val:        # Inversion check\n"
        "            if first is None:\n"
        "                first = prev           # First inversion: lock first\n"
        "            second = node              # Always update second\n"
        "        prev = node                    # Advance prev\n"
        "        inorder(node.right)            # Right\n"
        "\n"
        "    inorder(root)\n"
        "    first.val, second.val = second.val, first.val  # Swap values only\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("first = second = None", {"code": True}), " — two pointers we need to locate: the misplaced large node and the misplaced small node."])),
    N.para(N.rich([("class Sentinel: val = float('-inf')", {"code": True}), " — dummy node so the first comparison (prev.val > node.val) never falsely triggers on the very first visited node."])),
    N.para(N.rich([("prev = Sentinel()", {"code": True}), " — prev starts as the sentinel; will be replaced by the first actual node visited."])),
    N.para(N.rich([("nonlocal first, second, prev", {"code": True}), " — required in Python so the nested function can mutate the outer function's variables."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — base case: null node means nothing to process; simply return up the call stack."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — visit the entire left subtree first (the L in Left → Node → Right)."])),
    N.para(N.rich([("if prev.val > node.val:", {"code": True}), " — in a correct BST this is always False; a True means the sorted order is violated here."])),
    N.para(N.rich([("if first is None: first = prev", {"code": True}), " — first inversion only: prev is the misplaced large node. We never update first again."])),
    N.para(N.rich([("second = node", {"code": True}), " — always update second at every inversion. On the first inversion, node is the candidate for small. On the second inversion, node is the actual small — overwriting second with the correct value."])),
    N.para(N.rich([("prev = node", {"code": True}), " — advance prev to current node BEFORE recursing right. Critical: right subtree must compare against current node as its predecessor."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — visit right subtree last (the R in Left → Node → Right)."])),
    N.para(N.rich([("first.val, second.val = second.val, first.val", {"code": True}), " — swap only the integer values in the two nodes. Tree structure (all pointers) is unchanged."])),
    N.divider()
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Collect In-order Array (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Collect all nodes in in-order order (giving almost-sorted sequence), sort the values, and assign each node its correct value."),
        N.h4("What Doesn't Work"),
        N.para("O(n log n) sort and O(n) extra space is wasteful since we know only two values are wrong. But this is a great starting point to propose before optimizing."),
        N.h4("The Key Observation"),
        N.para("If you sort the in-order sequence and pair it with the original node order, any node where node.val != sorted_val[i] is one of the two wrong nodes."),
        N.h4("Building the Solution"),
        N.para("1. DFS in-order to collect nodes.\n2. Extract their values, sort.\n3. Assign sorted values back to nodes in order.")
    ]),
    N.h3("Code"),
    N.code(
        "def recoverTree(root):\n"
        "    nodes = []\n"
        "    def inorder(n):\n"
        "        if n:\n"
        "            inorder(n.left)\n"
        "            nodes.append(n)\n"
        "            inorder(n.right)\n"
        "    inorder(root)\n"
        "    vals = sorted(n.val for n in nodes)  # what values should be\n"
        "    for node, v in zip(nodes, vals):\n"
        "        node.val = v                      # restore correct value\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nodes = []", {"code": True}), " — list to collect TreeNode objects in in-order sequence."])),
    N.para(N.rich([("nodes.append(n)", {"code": True}), " — append current node object (not just its value) so we can modify it later."])),
    N.para(N.rich([("vals = sorted(n.val for n in nodes)", {"code": True}), " — extract all values and sort them; this gives what the in-order sequence SHOULD be."])),
    N.para(N.rich([("node.val = v", {"code": True}), " — assign each node in traversal order its correct sorted value, restoring BST property."])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Collect + sort (brute force)", "O(n log n)", "O(n)"],
        ["In-order + prev pointer (optimal)", "O(n)", "O(h)  (O(log n) balanced, O(n) worst)"],
        ["Morris Traversal (advanced)", "O(n)", "O(1)  — no recursion stack"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS In-order)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order Find Two Swapped — track a prev pointer during in-order DFS; detect inversions (prev.val > curr.val) to identify the two misplaced nodes"])),
    N.callout(
        "When to recognize this pattern: BST + 'validate / fix / find anomaly in node values' → in-order traversal gives sorted sequence → look for inversions. "
        "Also applies to: Validate BST (#98), Kth Smallest in BST (#230), BST Iterator (#173).",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS In-order / BST Property):"),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — in-order traversal must be strictly increasing; same prev-pointer check (#98)"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) — in-order traversal, return on k-th node visited (#230)"])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}), " (Medium) — reverse in-order (R→N→L) builds suffix sums (#538)"])),
    N.bullet(N.rich([("Minimum Absolute Difference in BST", {"bold": True}), " (Easy) — minimum diff is always between adjacent in-order nodes; track prev (#530)"])),
    N.bullet(N.rich([("Balance a Binary Search Tree", {"bold": True}), " (Medium) — in-order gives sorted array, then rebuild balanced BST (#1382)"])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium) — simulate in-order traversal iteratively with a stack (#173)"])),
    N.para("These problems share the same core technique: exploiting the BST in-order sorted-sequence property."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Trees → DFS: Inorder / BST Property). Sub-Pattern: In-order Find Two Swapped · Source: Analysis", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("recover_binary_search_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
