"""
gen_binary_tree_paths.py — Notion in-place update for LeetCode #257 Binary Tree Paths
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81c1-b66e-c47ed5d591dc"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=257,
    pattern="Trees",
    subpatterns=["Build Path String", "DFS: Preorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="DFS preorder passes an immutable path string down; at each leaf, record it. Backtracking is free because Python strings are immutable.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# PROBLEM
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return all root-to-leaf paths in any order. A ", {}),
        ("leaf", {"code": True}),
        (" is a node with no children. Return each path as a string formatted like ", {}),
        ('"1->2->5"', {"code": True}),
        (", with ", {}),
        ('"->"', {"code": True}),
        (" separating node values.", {}),
    ])),
    N.divider(),
]

# SOLUTION 1 — Recursive DFS (Interview Pick)
sol1_code = '''\
def binaryTreePaths(root):
    result = []
    def dfs(node, path):
        if not node:
            return
        path += ("->" if path else "") + str(node.val)
        if not node.left and not node.right:
            result.append(path)
            return
        dfs(node.left, path)
        dfs(node.right, path)
    dfs(root, "")
    return result'''

blocks += [
    N.h2("Solution 1 — Recursive DFS with Path String (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to collect every root-to-leaf path as a formatted string. Think of it as: start at the root, walk down toward every leaf, and at each leaf write down what nodes you passed through."),
        N.h4("What Doesn't Work"),
        N.para("BFS (level-order traversal) would visit all nodes but it processes them level by level, not path by path. Reconstructing paths from a BFS queue is awkward — you'd need to carry path state per queue entry anyway. There's no simpler recursive approach: we genuinely need to go depth-first."),
        N.h4("The Key Observation"),
        N.para("DFS naturally follows one root-to-leaf path at a time before backtracking. If we build a path string as we descend, when we reach a leaf the string is exactly the root-to-leaf path for that leaf."),
        N.h4("Building the Solution"),
        N.para("Step 1: Write a helper dfs(node, path) where path = the string built from root to node's parent. Step 2: Extend path with the current node's value. Step 3: If leaf, record. Otherwise recurse left and right. The clever trick: use immutable strings — each recursive call creates a new string, so the parent's path is untouched when we backtrack."),
        N.callout(
            "Analogy: You're hiking a branching trail. At each fork you write down where you are on a NEW piece of paper (not erasing the old one). When you reach a dead end, your paper shows the full route. Backtracking is automatic — you never touched the old papers.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), (" — Outer list that will collect all completed root-to-leaf path strings.", {})])),
    N.para(N.rich([("def dfs(node, path):", {"code": True}), (" — Inner helper. ", {}), ("node", {"code": True}), (" = current tree node, ", {}), ("path", {"code": True}), (" = the string built from the root down to node's parent.", {})])),
    N.para(N.rich([("if not node: return", {"code": True}), (" — Base case: null child. Return immediately without doing anything. Handles missing left/right children cleanly.", {})])),
    N.para(N.rich([('path += ("->" if path else "") + str(node.val)', {"code": True}), (" — Extend the path. If path is empty (at root), no separator needed: just the value. Otherwise prepend ", {}), ('"->"', {"code": True}), (". Creates a NEW string — Python strings are immutable, so the parent's path is untouched.", {})])),
    N.para(N.rich([("if not node.left and not node.right:", {"code": True}), (" — Leaf check: a node is a leaf when BOTH children are None. This is the commit point.", {})])),
    N.para(N.rich([("result.append(path)", {"code": True}), (" — Record the completed root-to-leaf path. Then return — there is nowhere deeper to go.", {})])),
    N.para(N.rich([("dfs(node.left, path)", {"code": True}), (" — Recurse into left subtree. ", {}), ("path", {"code": True}), (" here is the string up-to-and-including this node. Both left and right calls get the exact same prefix.", {})])),
    N.para(N.rich([("dfs(root, \"\")", {"code": True}), (" — Kick off DFS from root with empty string. The first call will set path = str(root.val) with no separator.", {})])),
    N.divider(),
]

# SOLUTION 2 — Iterative DFS
sol2_code = '''\
def binaryTreePaths(root):
    if not root:
        return []
    result = []
    stack = [(root, str(root.val))]
    while stack:
        node, path = stack.pop()
        if not node.left and not node.right:
            result.append(path)
        if node.right:
            stack.append((node.right, path + "->" + str(node.right.val)))
        if node.left:
            stack.append((node.left,  path + "->" + str(node.left.val)))
    return result'''

blocks += [
    N.h2("Solution 2 — Iterative DFS with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same idea as Solution 1, but we replace the call stack with an explicit stack data structure. Each stack entry carries a (node, path_so_far) pair — the same information a recursive call frame would hold."),
        N.h4("What Doesn't Work"),
        N.para("Naive iteration without carrying the path would force us to reconstruct paths from scratch. By bundling path with each node in the stack, we avoid that problem entirely."),
        N.h4("The Key Observation"),
        N.para("A recursive DFS call stack and an explicit stack structure are equivalent. The stack entry (node, path) replaces the recursion frame. When we pop and process a node, we push its children with extended paths — exactly what recursion does automatically."),
        N.h4("Building the Solution"),
        N.para("Initialize the stack with (root, str(root.val)). On each iteration: pop (node, path), check if leaf, then push right child first and left child second (so left is popped next, preserving left-first order). Continue until stack empty."),
        N.callout("Use this version in production or for very deep trees (depth > 1000) to avoid Python's default recursion limit of ~1000 frames.", "⚡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return []", {"code": True}), (" — Early exit for empty tree. Without this, stack initialization would fail trying to access root.val.", {})])),
    N.para(N.rich([("stack = [(root, str(root.val))]", {"code": True}), (" — Start: one entry containing the root node and its value as a string (the initial path).", {})])),
    N.para(N.rich([("node, path = stack.pop()", {"code": True}), (" — Pop a (node, path) pair. This is the equivalent of 'entering a recursive call' for that node.", {})])),
    N.para(N.rich([("if not node.left and not node.right: result.append(path)", {"code": True}), (" — Leaf check: same condition as recursive version. Record and move on.", {})])),
    N.para(N.rich([("stack.append((node.right, path + \"->\" + ...))", {"code": True}), (" — Push right child FIRST. Since we use a stack (LIFO), right is pushed before left, so left is popped first — maintaining left-first DFS order.", {})])),
    N.divider(),
]

# COMPLEXITY TABLE
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Recursive DFS (string)", "O(n)", "O(h) call stack", "Cleanest; implicit backtrack via immutable strings"],
        ["Iterative DFS (stack)", "O(n)", "O(n) worst case", "Avoids Python recursion limit; safe for deep trees"],
    ]),
    N.divider(),
]

# PATTERN CLASSIFICATION
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Build Path String", {}), (" (DFS Preorder with path accumulation from root to leaf)", {})])),
    N.callout(
        "When to recognize this pattern: 'Return all root-to-leaf paths' → DFS preorder. 'Does any root-to-leaf path satisfy X?' → DFS + carry running value. Any time you must commit state at a leaf and need clean backtracking.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# RELATED PROBLEMS
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS preorder / build path):"),
    N.bullet(N.rich([("Path Sum", {"bold": True}), (" (Easy) — Does any root-to-leaf path sum to target? Same DFS, carry a running sum, check at leaf (#112)", {})])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), (" (Medium) — Return ALL paths summing to target; same DFS but uses a list with explicit pop() for backtracking (#113)", {})])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), (" (Medium) — Treat each path as a number (\"1->2->3\" = 123), sum all such numbers (#129)", {})])),
    N.bullet(N.rich([("Smallest String Starting From Leaf", {"bold": True}), (" (Medium) — Build reversed character path at each leaf, find the lexicographically smallest result (#988)", {})])),
    N.bullet(N.rich([("Pseudo-Palindromic Paths in Binary Tree", {"bold": True}), (" (Medium) — DFS with bitmask tracking digit frequencies along each root-to-leaf path (#1457)", {})])),
    N.para("These problems share the same core technique: preorder DFS with accumulated path state, committing at each leaf."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees / Path Sum sub-pattern. Sub-Pattern: Build Path String. Source: Analysis + Guide.", "📚", "gray_background"),
]

# EMBED
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_tree_paths")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
