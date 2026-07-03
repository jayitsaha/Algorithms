"""
gen_count_good_nodes_in_binary_tree.py
Regenerates the Notion page for LeetCode #1448: Count Good Nodes in Binary Tree
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8104-88f2-cd483fd49631"

# ── 1. Properties ─────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1448,
    pattern="Trees",
    subpatterns=["Track Max on Path", "DFS: Preorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Carry running max top-down; a node is good if node.val >= max_so_far.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────
SLUG = "count_good_nodes_in_binary_tree"

blocks = []

# ─── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary tree ", {}),
        ("root", {"code": True}),
        (", return the number of ", {}),
        ("good", {"bold": True}),
        (" nodes. A node ", {}),
        ("X", {"code": True}),
        (" is good if, in the path from root to ", {}),
        ("X", {"code": True}),
        (", there are no nodes with a value greater than ", {}),
        ("X", {"code": True}),
        ("'s value.", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Recursive DFS (Interview Pick) ───────────────
blocks += [
    N.h2("Solution 1 — Recursive DFS Preorder (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A node is 'good' if its value is ≥ every ancestor's value. "
            "Instead of checking all ancestors from scratch at each node (O(h) per node), "
            "observe that we only need one number from all ancestors: their maximum. "
            "If the node beats or ties the max ancestor value, it's good."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive approach: for each node, walk back up to root collecting all ancestor values, "
            "compute their max, compare. This is O(n·h) — O(n²) for skewed trees. "
            "We'd redo the same ancestor traversal for every node."
        ),
        N.h4("The Key Observation"),
        N.para(
            "As we descend the tree, the running maximum can only stay the same or increase. "
            "We can maintain it incrementally: when visiting a node, update max = max(max, node.val) "
            "and pass it to children. Each child inherits the exact max of all its ancestors for free."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Define dfs(node, max_so_far). "
            "2. Base case: null node → 0. "
            "3. is_good = 1 if node.val >= max_so_far else 0. "
            "4. new_max = max(max_so_far, node.val). "
            "5. Return is_good + dfs(left, new_max) + dfs(right, new_max). "
            "6. Call dfs(root, -inf) so root is always counted."
        ),
        N.callout(
            "Analogy: Imagine you're hiking downhill and keeping track of the highest peak you've passed. "
            "A valley is 'good' if it's at least as high as that previous peak record.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def goodNodes(self, root: TreeNode) -> int:\n"
        "    def dfs(node, max_so_far):\n"
        "        if not node:\n"
        "            return 0\n"
        "        is_good = 1 if node.val >= max_so_far else 0\n"
        "        new_max = max(max_so_far, node.val)\n"
        "        left  = dfs(node.left,  new_max)\n"
        "        right = dfs(node.right, new_max)\n"
        "        return is_good + left + right\n"
        "    return dfs(root, float('-inf'))"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def dfs(node, max_so_far):", {"code": True}), (" — inner helper that carries path context top-down.", {})])),
    N.para(N.rich([("if not node: return 0", {"code": True}), (" — base case: null subtree contributes 0 good nodes.", {})])),
    N.para(N.rich([("is_good = 1 if node.val >= max_so_far else 0", {"code": True}), (" — the core check: is this node not beaten by any ancestor?", {})])),
    N.para(N.rich([("new_max = max(max_so_far, node.val)", {"code": True}), (" — update max for children; this node now becomes an ancestor.", {})])),
    N.para(N.rich([("left = dfs(node.left, new_max)", {"code": True}), (" — recursively count good nodes in entire left subtree.", {})])),
    N.para(N.rich([("right = dfs(node.right, new_max)", {"code": True}), (" — same for right subtree.", {})])),
    N.para(N.rich([("return is_good + left + right", {"code": True}), (" — total = this node's contribution + both subtrees.", {})])),
    N.para(N.rich([("return dfs(root, float('-inf'))", {"code": True}), (" — launch with -inf so root always passes (handles negative root values too).", {})])),
    N.callout(
        "⚠️ Why -inf, not 0? If root value is negative (e.g., -5), using 0 would wrongly exclude it. "
        "float('-inf') ensures the root unconditionally qualifies as good.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ─── Solution 2: Iterative DFS ────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative DFS with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same logic as the recursive version, but instead of relying on Python's call stack "
            "to remember (node, max_so_far) pairs, we maintain an explicit stack ourselves."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Python's default recursion limit is ~1000 frames. A severely skewed binary tree "
            "(essentially a linked list) with 10,000 nodes would trigger RecursionError. "
            "The iterative version avoids this entirely."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The call stack in the recursive version holds frames of (node, max_so_far). "
            "We can replicate this exactly with an explicit stack of (node, max_so_far) tuples. "
            "The algorithm is identical — only the mechanism for tracking state changes."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Push (root, -inf) onto stack. While stack is non-empty: pop (node, max_so_far), "
            "apply the good-node check, compute new_max, push non-null children with new_max. "
            "Return total count."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def goodNodes(self, root: TreeNode) -> int:\n"
        "    count = 0\n"
        "    stack = [(root, float('-inf'))]\n"
        "    while stack:\n"
        "        node, max_so_far = stack.pop()\n"
        "        if node.val >= max_so_far:\n"
        "            count += 1\n"
        "        new_max = max(max_so_far, node.val)\n"
        "        if node.left:\n"
        "            stack.append((node.left,  new_max))\n"
        "        if node.right:\n"
        "            stack.append((node.right, new_max))\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = 0", {"code": True}), (" — accumulator for good nodes.", {})])),
    N.para(N.rich([("stack = [(root, float('-inf'))]", {"code": True}), (" — start: root with -inf ancestor max.", {})])),
    N.para(N.rich([("node, max_so_far = stack.pop()", {"code": True}), (" — get next node and its path context (LIFO order = DFS).", {})])),
    N.para(N.rich([("if node.val >= max_so_far: count += 1", {"code": True}), (" — same good-node check as recursive version.", {})])),
    N.para(N.rich([("new_max = max(max_so_far, node.val)", {"code": True}), (" — update max for this node's children.", {})])),
    N.para(N.rich([("if node.left: stack.append((node.left, new_max))", {"code": True}), (" — only push non-null children (avoids handling null in loop body).", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — total good nodes across entire tree.", {})])),
    N.divider(),
]

# ─── Complexity ───────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Recursive DFS", "O(n)", "O(h)", "Clean, interview-ready; h = tree height"],
        ["Iterative DFS", "O(n)", "O(h)", "Avoids Python recursion limit on skewed trees"],
        ["Brute force (full path)", "O(n·h)", "O(h)", "Re-scan all ancestors per node; O(n²) worst case"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Track Max on Path, DFS: Preorder", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) A node's property depends on all its ancestors. "
        "(2) That ancestor property can be reduced to a single value passed top-down (max, min, sum, XOR, bitmask). "
        "(3) The decision at a node uses only ancestor info — not descendant info (otherwise postorder).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'carry state top-down through DFS' technique:"),
    N.bullet(N.rich([("Path Sum", {"bold": True}), (" (Easy) — top-down DFS carrying running sum; check at leaves.", {})])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), (" (Medium) — same pattern, collect all valid root-to-leaf paths.", {})])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), (" (Medium) — carry partial decimal number being formed top-down.", {})])),
    N.bullet(N.rich([("Pseudo-Palindromic Paths in a Binary Tree", {"bold": True}), (" (Medium) — carry a bitmask of digit parities top-down.", {})])),
    N.bullet(N.rich([("Longest ZigZag Path in a Binary Tree", {"bold": True}), (" (Medium) — carry current direction and step-count top-down.", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — postorder variant: each child returns best upward contribution.", {})])),
    N.para("These problems share the same core technique: pass a summary of ancestor state as a parameter into each recursive call."),
    N.callout("📚 Pattern Source: Trees section — 'Track Max on Path' sub-pattern (DFS: Preorder with top-down accumulator).", "📚", "gray_background"),
]

# ─── Interactive Visual Explainer ────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
