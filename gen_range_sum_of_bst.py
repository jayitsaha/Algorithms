"""
gen_range_sum_of_bst.py — Notion update for Range Sum of BST (#938)
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81e4-9b0c-c56ff1202bd8"
SLUG    = "range_sum_of_bst"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=938,
    pattern="Trees",
    subpatterns=["Prune Based on Range", "BST Property"],
    tc="O(n)",
    sc="O(h)",
    key_insight="BST ordering lets you skip entire subtrees: val<=low → prune left; val>=high → prune right.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old blocks ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a Binary Search Tree (BST) and two integers ", {}),
        ("low", {"code": True}),
        (" and ", {}),
        ("high", {"code": True}),
        (", return the sum of all node values in the BST that lie within the inclusive range [", {}),
        ("low", {"code": True}),
        (", ", {}),
        ("high", {"code": True}),
        ("]. Exploit the BST's ordering property to prune branches where no in-range nodes can exist.", {}),
    ])),
    N.para(N.rich([
        ("Example: root=[10,5,15,3,7,null,18], low=7, high=15 → Answer: 45 (7+10+13+15).", {"italic": True, "color": "gray"}),
    ])),
    N.divider(),
]

# ── Solution 1 — Recursive DFS with BST Pruning ────────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive DFS with BST Pruning (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to sum node values in a BST that fall within a given range. A BST has a crucial property: for any node, everything in its left subtree is smaller, everything in its right subtree is larger."),
        N.h4("What Doesn't Work"),
        N.para("A plain DFS visits every node regardless — it works but ignores the BST structure. For a large tree with a narrow range, we'd be doing enormous amounts of unnecessary work visiting nodes we know are out of range."),
        N.h4("The Key Observation"),
        N.para("If a node's value is <= low, its ENTIRE left subtree must also be < low (BST guarantee). We can skip that whole branch. Similarly, if val >= high, the entire right subtree is > high. This is called BST pruning."),
        N.h4("Building the Solution"),
        N.para("Three cases at each node: (1) val <= low → skip left, recurse right only. (2) val >= high → skip right, recurse left only. (3) val in (low, high) → add val, recurse BOTH children. For the boundary cases (val == low or val == high), the node itself IS in range and gets added in the third branch."),
        N.callout(
            "Analogy: Think of the BST as a sorted filing cabinet. If you want files labeled 7–15 and you're at drawer 5, you know all drawers to the LEFT of drawer 5 are labeled < 5 < 7 — don't open them. Jump straight to the right side.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def rangeSumBST(root, low, high):\n"
        "    if not root:\n"
        "        return 0\n"
        "    if root.val <= low:\n"
        "        # Left subtree all < root.val <= low — skip left entirely\n"
        "        return rangeSumBST(root.right, low, high)\n"
        "    if root.val >= high:\n"
        "        # Right subtree all > root.val >= high — skip right entirely\n"
        "        return rangeSumBST(root.left, low, high)\n"
        "    # low < root.val < high — node is in range\n"
        "    return (root.val\n"
        "          + rangeSumBST(root.left, low, high)\n"
        "          + rangeSumBST(root.right, low, high))"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return 0", {"code": True}), (" — Base case. Null node contributes nothing to the sum.", {})])),
    N.para(N.rich([("if root.val <= low:", {"code": True}), (" — Prune condition 1. If this node's value is at or below the range floor, every node in its LEFT subtree is strictly less than low — guaranteed by BST property. We don't need to check left at all. Recurse only right (higher values).", {})])),
    N.para(N.rich([("if root.val >= high:", {"code": True}), (" — Prune condition 2. Symmetric. If at or above the range ceiling, the entire RIGHT subtree is out of range. Recurse only left.", {})])),
    N.para(N.rich([("return root.val + recurse(left) + recurse(right)", {"code": True}), (" — The node is strictly inside (low, high). Add its value, then recurse both children because either subtree could contain more in-range nodes.", {})])),
    N.divider(),
]

# ── Solution 2 — Iterative BFS with Pruning ────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative BFS with Pruning"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal, but expressed iteratively. Use a queue (BFS) or stack (DFS) to process nodes. Apply the same pruning logic before enqueuing children."),
        N.h4("What Doesn't Work"),
        N.para("Deep recursion on a skewed BST (essentially a linked list) will hit Python's recursion limit (~1000 depth). Iteration avoids this pitfall entirely."),
        N.h4("The Key Observation"),
        N.para("The pruning logic is identical to the recursive version, just expressed as 'don't enqueue children that can't contain in-range values' rather than 'don't recurse into them'."),
        N.h4("Building the Solution"),
        N.para("Enqueue root. While queue is non-empty: dequeue a node, check its value. If val > low, enqueue left child (left might have values >= low). If val < high, enqueue right child (right might have values <= high). If val is in range, add to total."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def rangeSumBST(root, low, high):\n"
        "    total = 0\n"
        "    queue = deque([root])\n"
        "    while queue:\n"
        "        node = queue.popleft()\n"
        "        if not node:\n"
        "            continue\n"
        "        if low <= node.val <= high:\n"
        "            total += node.val\n"
        "        if node.val > low:   # left child might have values >= low\n"
        "            queue.append(node.left)\n"
        "        if node.val < high:  # right child might have values <= high\n"
        "            queue.append(node.right)\n"
        "    return total"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("total = 0; queue = deque([root])", {"code": True}), (" — Initialize accumulator and BFS queue with the root.", {})])),
    N.para(N.rich([("if not node: continue", {"code": True}), (" — Skip null nodes (children of leaf nodes).", {})])),
    N.para(N.rich([("if low <= node.val <= high: total += node.val", {"code": True}), (" — Add to sum if node is within the range.", {})])),
    N.para(N.rich([("if node.val > low: enqueue left", {"code": True}), (" — Only enqueue left child if current node's value is above low — otherwise left subtree is entirely below low.", {})])),
    N.para(N.rich([("if node.val < high: enqueue right", {"code": True}), (" — Only enqueue right child if current node's value is below high — otherwise right subtree is entirely above high.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive DFS (Pruned)", "O(n) worst, O(log n) typical", "O(h)"],
        ["Iterative BFS (Pruned)", "O(n) worst, O(log n) typical", "O(h)"],
    ]),
    N.para(N.rich([
        ("n", {"code": True}),
        (" = number of nodes; ", {}),
        ("h", {"code": True}),
        (" = tree height (O(log n) balanced, O(n) skewed). Pruning skips out-of-range subtrees, so in practice the traversal visits fewer than n nodes when the range is narrow.", {}),
    ])),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prune Based on Range, BST Property", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves a BST + a value constraint (range, target, nearest value)\n"
        "• You can determine 'entire subtree is irrelevant' from a single node's value\n"
        "• Left-subtree-all-smaller / right-subtree-all-larger reasoning applies\n"
        "• Keywords: 'given a BST', 'find nodes within range', 'trim BST'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST Property / Pruning technique:"),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}), (" (Easy) — Navigate left/right based on target vs. node value. Foundational BST search (#700).", {})])),
    N.bullet(N.rich([("Trim a Binary Search Tree", {"bold": True}), (" (Medium) — Remove nodes outside [low, high] from a BST. Almost identical pruning logic, but you're modifying structure not summing (#669).", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium) — Use BST invariant with min/max bounds at each node to verify ordering (#98).", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), (" (Medium) — BST inorder traversal = sorted sequence; count to find kth element (#230).", {})])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}), (" (Medium) — Reverse inorder (right-root-left) to accumulate suffix sums using BST ordering (#538).", {})])),
    N.bullet(N.rich([("Closest Binary Search Tree Value", {"bold": True}), (" (Easy) — BST search pruning to navigate toward the target and track closest value seen (#270).", {})])),
    N.para("These problems all exploit the same core BST guarantee: left subtree < current < right subtree, enabling directional pruning."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, BST Property sub-pattern. Sub-Pattern verified: 'Prune Based on Range' (Analysis; confirmed in Trees section of guide).", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the BST traversal visually — watch nodes get visited, pruned, or added to sum. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
