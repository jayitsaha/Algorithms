"""gen_binary_tree_maximum_path_sum.py — Notion update for Binary Tree Maximum Path Sum (#124)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-817c-ab32-e9cfe0d770d4"
SLUG    = "binary_tree_maximum_path_sum"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=124,
    pattern="Trees",
    subpatterns=["Max of Paths Through Node"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Every path has a turning node; postorder DFS returns the best one-sided arm while updating a global ans with the two-sided candidate.",
    icon="🔴",
)
print("Properties set OK")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} old blocks")

# ── 3) Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the maximum ", {}),
        ("path sum", {"bold": True}),
        (" of any non-empty path. A path is any sequence of nodes where each pair of adjacent nodes has an edge between them. The path does not need to pass through the root, and a path must contain at least one node.", {}),
    ])),
    N.para("Example 1: root = [-10, 9, 20, null, null, 15, 7] → Output: 42 (path: 15 → 20 → 7)"),
    N.para("Example 2: root = [1, 2, 3] → Output: 6 (path: 2 → 1 → 3, with node 1 as turning point)"),
    N.callout("Constraint: The number of nodes in the tree is in the range [1, 3 × 10⁴]. Node values are in [−1000, 1000]. Values may be negative — initialize ans = float('-inf'), not 0.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 1: Postorder DFS (Optimal, Interview Pick) ──
SOLUTION_1_CODE = """\
def maxPathSum(root: TreeNode) -> int:
    ans = float('-inf')   # handles all-negative trees

    def dfs(node):
        nonlocal ans
        if not node:
            return 0          # null child contributes 0

        # Postorder: process children first
        left  = max(0, dfs(node.left))   # clamp: skip if negative
        right = max(0, dfs(node.right))  # clamp: skip if negative

        # Update global: this node as the turning point
        ans = max(ans, left + node.val + right)

        # Return best one-sided arm to parent
        return node.val + max(left, right)

    dfs(root)
    return ans
"""

SOLUTION_1_INTUITION = [
    N.h4("Reframe the Problem"),
    N.para("We want the maximum-sum sequence of connected nodes in the tree (no branching, no revisiting). The path can start and end anywhere. Reframe: 'find the best path by considering every possible topmost node as the turning point.'"),
    N.h4("What Doesn't Work"),
    N.para("Brute force: for each node as a turning point, run a separate DFS to get left and right arms. O(n²) total — each of O(n) nodes triggers an O(n) arm computation. We can do it in O(n) by merging the two passes."),
    N.h4("The Key Observation"),
    N.para("Every path has exactly one highest (turning) node. At that node, the path may go left, through the node, and right. Below the turning node, the path is a simple downward chain. If we fix the turning node, we just need the best downward arm on each side."),
    N.h4("Building the Solution"),
    N.para("Use postorder DFS (process children first). Each call returns the best one-sided arm from that node. At each node: (1) collect left and right arms (clamped to 0 if negative), (2) update global ans with left + node.val + right, (3) return node.val + max(left, right) as the arm to the parent. The two-sided value updates ans; the one-sided value is returned. One pass, O(n)."),
    N.callout("Analogy: imagine each node as a city. The 'turning point' city connects two highways coming from different directions. The DFS finds the best highway on each side, picks the best cross-city route for the global answer, and tells the parent city: 'the best highway I can extend is this one-directional road.'", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Postorder DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", SOLUTION_1_INTUITION),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("ans = float('-inf')", {"code": True}), (" — Initialize global answer to negative infinity so even all-negative trees return the correct (least-negative) single node.", {})])),
    N.para(N.rich([("if not node: return 0", {"code": True}), (" — Null child contributes 0 to any arm. This is the base case. We return 0 (not -inf) because the parent's max(0, ...) handles the decision of whether to include any arm.", {})])),
    N.para(N.rich([("left = max(0, dfs(node.left))", {"code": True}), (" — Recursively get the best arm from the left subtree. Clamping to 0 means: if the left subtree's best path is negative, we simply don't include it. The path can 'start fresh' at the current node.", {})])),
    N.para(N.rich([("right = max(0, dfs(node.right))", {"code": True}), (" — Same for the right subtree.", {})])),
    N.para(N.rich([("ans = max(ans, left + node.val + right)", {"code": True}), (" — Evaluate this node as the turning point. left + node.val + right covers all 4 path types: single node (both 0), left arm only (right 0), right arm only (left 0), and full bridge (both > 0). This is the two-sided path that updates the global answer.", {})])),
    N.para(N.rich([("return node.val + max(left, right)", {"code": True}), (" — Return the best ONE-SIDED arm to the parent. The parent can only extend us in one direction (otherwise the path would branch at us). Do NOT return the two-sided value here — that would allow the parent to create a forked path.", {})])),
    N.callout("Critical distinction: return value (one-sided arm) ≠ global ans update (two-sided candidate). These are two different values computed at every node simultaneously.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOLUTION_2_CODE = """\
def maxPathSum_brute(root: TreeNode) -> int:
    \"\"\"O(n²): separate arm computation per node as turning point.\"\"\"
    def best_arm(node: TreeNode) -> int:
        \"\"\"Returns max one-sided path sum starting at node.\"\"\"
        if not node:
            return 0
        return node.val + max(0, best_arm(node.left), best_arm(node.right))

    def solve(node: TreeNode) -> int:
        if not node:
            return float('-inf')
        left_arm  = max(0, best_arm(node.left))
        right_arm = max(0, best_arm(node.right))
        through_me = left_arm + node.val + right_arm
        return max(through_me, solve(node.left), solve(node.right))

    return solve(root)
"""

SOLUTION_2_INTUITION = [
    N.h4("Reframe the Problem"),
    N.para("Try every node as the turning point. For each, separately compute the best downward arm on each side and sum them up."),
    N.h4("What Doesn't Work"),
    N.para("This approach recomputes the best arm for each subtree from scratch for every potential turning-point node. For a balanced tree of height h, best_arm is called n times and costs O(n) each — O(n²) total. This is too slow for n = 30,000."),
    N.h4("The Key Observation"),
    N.para("When we call best_arm(node.left) at the root, we recompute the same arms that were computed when we called solve(node.left). The one-pass DFS (Solution 1) eliminates this redundancy by merging both computations."),
    N.h4("Building the Solution"),
    N.para("For each node: recursively get arms from left and right using best_arm(). Compute the turning-point candidate. Recurse into left and right subtrees via solve(). Take the max. Correct but O(n²) — use Solution 1 in interviews."),
]

blocks += [
    N.h2("Solution 2 — Brute Force Enumeration (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", SOLUTION_2_INTUITION),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("best_arm(node)", {"code": True}), (" — Returns the maximum one-sided path sum starting at this node. It computes this freshly each time it is called.", {})])),
    N.para(N.rich([("solve(node)", {"code": True}), (" — Tries node as the turning point, then recurses left and right. The three-way max gives the global answer for the subtree rooted at node.", {})])),
    N.para("This is O(n²) because best_arm is called inside solve, and both traverse the whole subtree. The optimal DFS (Solution 1) computes both in a single postorder pass."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",               "Time",   "Space",  "Notes"],
        ["Brute Force",            "O(n²)",  "O(h)",   "Re-computes arms from scratch for each turning point"],
        ["Postorder DFS (optimal)","O(n)",   "O(h)",   "One pass; h = O(log n) balanced, O(n) skewed"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Max of Paths Through Node (DFS Postorder)", {})])),
    N.callout(
        "When to recognize this pattern: 'find max/min sum/length path in binary tree (any start/end)' — especially when the recursive function needs both a return value (arm for parent) AND a side-effect (global answer update). The max(0, arm) clamping to allow 'starting fresh' is another strong signal.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same dual-role postorder DFS technique:"),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), (" (Easy) — Longest path by edge count; return depth to parent, update global diameter with left_depth + right_depth at each node. Exact same skeleton. (#543)", {})])),
    N.bullet(N.rich([("Longest Univalue Path", {"bold": True}), (" (Medium) — Max path length where all nodes share the same value; arm only extends if child value matches parent value. (#687)", {})])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}), (" (Medium) — Preorder DFS passing the max value seen so far; node is 'good' if its value >= the running max. (#1448)", {})])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}), (" (Medium) — Count paths summing to target from any node to any descendant; uses prefix sum stored in DFS state. (#437)", {})])),
    N.bullet(N.rich([("Distribute Coins in Binary Tree", {"bold": True}), (" (Medium) — Return excess coins from subtree to balance the tree; postorder, return value = coins to move, update global moves count. (#979)", {})])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), (" (Medium) — Compute the decimal number formed by root-to-leaf digits; preorder DFS passing accumulated number. (#129)", {})])),
    N.para("These problems share the core technique: postorder DFS where the recursive return value serves the parent, while a side-effect captures the global optimum at each node."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section. Sub-Pattern: Max of Paths Through Node. Source: Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the postorder DFS visually — use Next/Prev or arrow keys to watch each node compute its arm and update the global answer.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
