"""
gen_maximum_difference_between_node_and_ancestor.py
Rebuilds the Notion page for LeetCode #1026 in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c9-b92f-ce62f50351ac"

# ── 1) Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1026,
    pattern="Trees",
    subpatterns=["Track Min/Max on Path"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Pass cur_min and cur_max down via DFS; at null leaf return cur_max - cur_min.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────────────────────
PROBLEM_STMT = (
    "Given the root of a binary tree, find the maximum value v for which there "
    "exist different nodes a and b where v = |a.val - b.val| and a is an ancestor of b. "
    "A node a is an ancestor of b if either: any child of a is equal to b or any child "
    "of a is an ancestor of b."
)

SOL1_CODE = """\
def maxAncestorDiff(root):
    def dfs(node, cur_min, cur_max):
        if not node:
            return cur_max - cur_min      # widest range on this complete path
        cur_min = min(cur_min, node.val)  # include current node as ancestor for children
        cur_max = max(cur_max, node.val)
        left  = dfs(node.left,  cur_min, cur_max)
        right = dfs(node.right, cur_min, cur_max)
        return max(left, right)
    return dfs(root, root.val, root.val)  # root.val: root is first ancestor
"""

SOL2_CODE = """\
def maxAncestorDiff(root):
    res = 0
    def dfs(node, path):
        nonlocal res
        for anc_val in path:             # compare with every ancestor — O(depth) per node
            res = max(res, abs(node.val - anc_val))
        if node.left:  dfs(node.left,  path + [node.val])
        if node.right: dfs(node.right, path + [node.val])
    dfs(root, [])
    return res
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Pass Min/Max Down DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Each node needs to be compared with all nodes on the path from the root "
            "down to it (its ancestors). The key word is 'path' — every ancestor lies "
            "on a single root-to-node route, which is exactly what a DFS call stack models."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Comparing every node with every other node is O(n^2). Even smarter, if we carry "
            "the full ancestor list as a parameter and compare against all of them, it is "
            "O(n * h) — up to O(n^2) on a skewed tree. We need to reduce what we track."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The maximum |ancestor - node| is always achieved by the most extreme ancestor "
            "— either the smallest or the largest value seen on the path. So instead of "
            "tracking all ancestors, we only need cur_min and cur_max."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. DFS down the tree, passing cur_min and cur_max as parameters.\n"
            "2. At each node: update cur_min = min(cur_min, node.val) and "
            "cur_max = max(cur_max, node.val) — this node becomes an ancestor for its children.\n"
            "3. At a null child (past leaf): the path is complete. Return cur_max - cur_min.\n"
            "4. Each node returns the maximum answer from its two subtrees."
        ),
        N.callout(
            "Analogy: Imagine hiking down a mountain path tracking the highest and lowest "
            "altitude points seen so far. At the trailhead (leaf), the widest elevation "
            "difference is simply highest - lowest. You never need to remember every step.",
            "🏔️", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("def dfs(node, cur_min, cur_max)", {"code": True}),
        (" — Inner helper function. Carries the running minimum and maximum values "
         "seen on the path from root to the current node's parent.")
    ])),
    N.para(N.rich([
        ("if not node: return cur_max - cur_min", {"code": True}),
        (" — Base case: we've gone past a leaf (node is None). The path is complete. "
         "Every value on this root-to-leaf path is an ancestor of every node below it, "
         "so the maximum |u - v| for any two values on this path equals cur_max - cur_min.")
    ])),
    N.para(N.rich([
        ("cur_min = min(cur_min, node.val)", {"code": True}),
        (" — Update the running minimum to include the current node. This node will be "
         "an ancestor for all nodes in its subtrees.")
    ])),
    N.para(N.rich([
        ("cur_max = max(cur_max, node.val)", {"code": True}),
        (" — Same for the running maximum.")
    ])),
    N.para(N.rich([
        ("left = dfs(node.left, cur_min, cur_max)", {"code": True}),
        (" — Recurse into the left subtree, passing the updated extremes.")
    ])),
    N.para(N.rich([
        ("right = dfs(node.right, cur_min, cur_max)", {"code": True}),
        (" — Recurse into the right subtree with the same updated extremes.")
    ])),
    N.para(N.rich([
        ("return max(left, right)", {"code": True}),
        (" — Return the best answer found in either subtree. This bubbles the global "
         "maximum back up to the root call.")
    ])),
    N.para(N.rich([
        ("return dfs(root, root.val, root.val)", {"code": True}),
        (" — Kick off DFS. Initialize cur_min = cur_max = root.val because the root "
         "itself is the first (and so far only) ancestor. No ancestor above root exists.")
    ])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Brute Force: Carry Full Ancestor List"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The most direct interpretation: for every node, compare it against every "
            "ancestor and track the global maximum difference."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This works correctly but is inefficient. For a balanced tree of height h, "
            "each node compares against O(h) ancestors — O(n log n) total. For a skewed "
            "tree (linked list shape), it degrades to O(n^2)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We carry the full path as a list. At each node, we compare it against every "
            "element in the list. Then we recurse, appending the current node to the list "
            "for its children. This is the baseline from which we optimize Solution 1."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Use a nonlocal variable res. DFS with a path list. At each node, update res "
            "with |node.val - anc_val| for every anc_val in path. Recurse children with "
            "path + [node.val]."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Pass Min/Max Down (Optimal)", "O(n)", "O(h) — recursion stack"],
        ["Brute Force (Full Path List)", "O(n·h)", "O(n·h) — list copies per level"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS Preorder / Path-based)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Min/Max on Path"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to compare each node with its ancestors (nodes on root-to-node path)\n"
        "• 'For each node, find the max/min over all ancestor values'\n"
        "• You need to propagate information top-down (root → leaves) rather than bottom-up\n"
        "• The optimal value among ancestors is an extreme (min or max), not a specific node",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (pass information down via DFS parameters):"),
    N.bullet(N.rich([
        ("Path Sum", {"bold": True}),
        (" (Easy) — Pass running sum down; check at leaves whether it equals target. [#112]")
    ])),
    N.bullet(N.rich([
        ("Path Sum II", {"bold": True}),
        (" (Medium) — Collect all root-to-leaf paths with target sum; carry partial path as parameter. [#113]")
    ])),
    N.bullet(N.rich([
        ("Sum Root to Leaf Numbers", {"bold": True}),
        (" (Medium) — Pass accumulated digit-number down each branch. [#129]")
    ])),
    N.bullet(N.rich([
        ("Count Good Nodes in Binary Tree", {"bold": True}),
        (" (Medium) — Pass cur_max down; count nodes where val >= cur_max. Same carry-down pattern. [#1448]")
    ])),
    N.bullet(N.rich([
        ("Longest Univalue Path", {"bold": True}),
        (" (Medium) — Track same-value chain length from ancestor to descendant. [#687]")
    ])),
    N.bullet(N.rich([
        ("Binary Tree Maximum Path Sum", {"bold": True}),
        (" (Hard) — Postorder: pass max one-sided gain upward; update global answer at each node. [#124]")
    ])),
    N.para("These problems share the core technique: carrying state downward through DFS parameters to avoid recomputing ancestor information."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS Preorder / Path Sum sub-pattern", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_difference_between_node_and_ancestor")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
