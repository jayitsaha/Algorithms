"""
gen_lowest_common_ancestor_of_a_binary_tree.py
Updates the Notion page for LeetCode #236 — Lowest Common Ancestor of a Binary Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b2-a16b-f118adc6a9d2"
SLUG = "lowest_common_ancestor_of_a_binary_tree"

# ── 1. Set Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=236,
    pattern="Trees",
    subpatterns=["LCA", "Find in Left/Right Subtrees"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Postorder DFS returns None/target/LCA; current node is LCA when both left and right are non-None.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes ",
        ("p", {"code": True}), " and ", ("q", {"code": True}),
        ". The LCA is defined as the deepest node that has both ",
        ("p", {"code": True}), " and ", ("q", {"code": True}),
        " as descendants. A node is allowed to be a descendant of itself."
    ])),
    N.divider(),
]

# ── Solution 1: Recursive Postorder DFS ──
blocks += [
    N.h2("Solution 1 — Recursive Postorder DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the deepest node whose subtree contains both p and q. If we think bottom-up: at each node, we ask its left and right subtrees whether they found p or q. If both sides found something, the current node is the split point — it's the LCA."),
        N.h4("What Doesn't Work"),
        N.para("A top-down approach (like checking each node if p and q are both in its subtree) requires O(n) work per node, giving O(n²) overall. We'd be re-exploring subtrees that were already searched."),
        N.h4("The Key Observation"),
        N.para("Postorder DFS (Left → Right → Root) lets us collect results from children BEFORE deciding at the parent. Each call can return one of three signals: None (neither target found), the target itself (one target found), or the LCA once determined. We reuse the return type for all three."),
        N.h4("Building the Solution"),
        N.para("Base cases: null → return None. root == p or root == q → return root (found a target; stop searching this branch). Then recurse into both subtrees. If both return non-None → current node is LCA (return root). Otherwise return whichever side is non-None (propagate upward)."),
        N.callout("Analogy: Think of DFS as reporters. Each reporter covers their region and sends up a message: 'Found p', 'Found q', 'Found both' (=LCA identified), or 'Found nothing'. The first reporter to receive BOTH 'Found p' from one direction and 'Found q' from the other shouts: I'm the LCA!", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def lowestCommonAncestor(root, p, q):\n"
        "    if root is None:\n"
        "        return None\n"
        "    if root == p or root == q:\n"
        "        return root\n"
        "    left  = lowestCommonAncestor(root.left,  p, q)\n"
        "    right = lowestCommonAncestor(root.right, p, q)\n"
        "    if left and right:\n"
        "        return root\n"
        "    return left or right"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if root is None:", {"code": True}), " — Base case: fell off the tree. Neither p nor q exists here. Return None."])),
    N.para(N.rich([("if root == p or root == q:", {"code": True}), " — Hit a target! Return this node as an upward signal. Don't recurse further into this branch."])),
    N.para(N.rich([("left = lca(root.left, p, q)", {"code": True}), " — Search entire left subtree for p and q. Result: None, p, q, or the LCA."])),
    N.para(N.rich([("right = lca(root.right, p, q)", {"code": True}), " — Search entire right subtree for p and q."])),
    N.para(N.rich([("if left and right: return root", {"code": True}), " — Both sides found something! p and q are in different subtrees — current node is definitionally the LCA. Return it."])),
    N.para(N.rich([("return left or right", {"code": True}), " — Only one side (or neither) found something. Propagate: left if left is non-None, else right (which may be None)."])),
    N.divider(),
]

# ── Solution 2: Iterative Parent Pointer Map ──
blocks += [
    N.h2("Solution 2 — Iterative with Parent Pointer Map"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we know each node's parent, we can find the LCA by: (1) collecting all ancestors of p into a set, then (2) walking q's ancestors upward until we hit one in p's ancestor set."),
        N.h4("What Doesn't Work"),
        N.para("We don't have parent pointers by default. We need to first traverse the tree to build a parent map — but once we have it, the LCA lookup is straightforward."),
        N.h4("The Key Observation"),
        N.para("The LCA is the first node on q's path-to-root that also appears on p's path-to-root. This is exactly the 'intersection of two linked lists' problem on the ancestor chains!"),
        N.h4("Building the Solution"),
        N.para("Use a stack-based DFS to build parent[node] = node's parent for every node until both p and q are mapped. Then collect all of p's ancestors into a set. Walk q upward via parent pointers until we reach a node in that set — that's the LCA."),
    ]),
    N.h3("Code"),
    N.code(
        "def lowestCommonAncestor(root, p, q):\n"
        "    parent = {root: None}\n"
        "    stack = [root]\n"
        "    while p not in parent or q not in parent:\n"
        "        node = stack.pop()\n"
        "        if node.left:\n"
        "            parent[node.left] = node\n"
        "            stack.append(node.left)\n"
        "        if node.right:\n"
        "            parent[node.right] = node\n"
        "            stack.append(node.right)\n"
        "    ancestors = set()\n"
        "    while p:\n"
        "        ancestors.add(p)\n"
        "        p = parent[p]\n"
        "    while q not in ancestors:\n"
        "        q = parent[q]\n"
        "    return q"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = {root: None}", {"code": True}), " — Initialize parent map; root's parent is None (it has none)."])),
    N.para(N.rich([("while p not in parent or q not in parent:", {"code": True}), " — Keep DFS'ing until both targets are recorded in the parent map."])),
    N.para(N.rich([("parent[node.left] = node", {"code": True}), " — Record parent relationship as we discover each child."])),
    N.para(N.rich([("while p: ancestors.add(p); p = parent[p]", {"code": True}), " — Collect ALL ancestors of p (including p itself) into a set."])),
    N.para(N.rich([("while q not in ancestors: q = parent[q]", {"code": True}), " — Walk q's ancestors upward until we hit one that p also has as an ancestor — that's the LCA."])),
    N.para(N.rich([("return q", {"code": True}), " — At this point q points to the first shared ancestor = the LCA."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive Postorder DFS (Interview Pick)", "O(n)", "O(h) — call stack"],
        ["Iterative — Parent Pointer Map", "O(n)", "O(n) — parent map"],
        ["BST Approach (value comparison)", "O(log n)", "O(1) — but BST only!"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS Postorder)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "LCA — Find in Left/Right Subtrees"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) The problem asks for a node that satisfies a property relative to two other nodes. "
        "(2) The answer requires knowing what BOTH subtrees contain simultaneously. "
        "(3) Phrase 'lowest / deepest / closest common' in the problem. "
        "(4) The return value of the recursive call can encode the answer (no global state needed).",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        "Source: Guide Section on Trees — LCA sub-pattern. This problem is the canonical example "
        "of the 'Find in Left/Right Subtrees' postorder DFS pattern."
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'Find in Left/Right Subtrees' postorder DFS technique:"),
    N.bullet(N.rich([("LCA of a Binary Search Tree", {"bold": True}), " (Easy) — Same idea; use value comparison for O(log n). LeetCode #235."])),
    N.bullet(N.rich([("LCA of Deepest Leaves", {"bold": True}), " (Medium) — Track depth alongside result; return LCA of all deepest leaves. LeetCode #1123."])),
    N.bullet(N.rich([("Smallest Subtree Enclosing Deepest Nodes", {"bold": True}), " (Medium) — Equivalent to LCA of deepest leaves. LeetCode #865."])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy) — Foundational postorder DFS; children's results combine at the parent. LeetCode #104."])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard) — Postorder DFS; propagate best path from each subtree upward. LeetCode #124."])),
    N.bullet(N.rich([("Step-By-Step Directions From a Binary Tree Node to Another", {"bold": True}), " (Medium) — Uses LCA as intermediate step. LeetCode #2096."])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), " (Medium) — DFS backtracking on binary tree; builds same traversal intuition. LeetCode #113."])),
    N.para("These problems share the same core technique: postorder DFS that propagates partial results from children up to the parent for a combined decision."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, LCA sub-pattern.", "📚", "gray_background"),
]

# ── Embed ──
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
