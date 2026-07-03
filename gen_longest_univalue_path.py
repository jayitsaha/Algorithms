"""
gen_longest_univalue_path.py
Notion page creator/updater for LeetCode #687 Longest Univalue Path.
notion_page_id = None → create fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = None  # null → create new page

if PAGE_ID is None:
    PAGE_ID = N.create_page("Longest Univalue Path", 687, "Medium", "🟡")
    print(f"Created new page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=687,
    pattern="Trees",
    subpatterns=["Return Depth Track Max", "DFS Postorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="DFS helper returns arm length (one direction); global max tracks full span (left_arm + right_arm) at each node.",
    icon="🟡",
)
print("Properties set.")

# 2) No wipe needed (fresh page)

# 3) Build body blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the length of the longest path where each node in the path has the same value. The path does not need to pass through the root. The length of a path is measured in ", {}),
        ("edges", {"bold": True}),
        (", not nodes.", {}),
    ])),
    N.para("Example 1: root = [5,4,5,1,1,null,5] → Output: 2 (path 5→5→5 uses 2 edges)"),
    N.para("Example 2: root = [1,4,5,4,4,null,5] → Output: 2 (path 4←4→4 uses 2 edges)"),
    N.callout(
        "Constraint: Length is in EDGES, not nodes. A path through 3 same-value nodes = length 2.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 1: Optimal DFS ──
blocks += [
    N.h2("Solution 1 — DFS Postorder: Return Arm, Track Max (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest chain of same-valued nodes where the chain can 'turn' at any internal node. The path might span left and right subtrees of a deep node — it doesn't have to include the root."),
        N.h4("What Doesn't Work"),
        N.para("A simple recursive 'how deep can I go matching this value?' ignores paths that turn. If we only look in one direction from each node, we miss paths like 4←4→4 that bend at an interior node."),
        N.h4("The Key Observation"),
        N.para("At each node N, the longest univalue path THROUGH N is left_arm + right_arm, where each arm is 0 if the child's value doesn't match N's value, or (child's arm + 1) if it does. We track this sum globally across all nodes."),
        N.h4("Building the Solution"),
        N.para("Use DFS postorder (children before parent). Helper returns the best single-direction arm (for the parent to potentially extend). Separately update a global max with the combined span at each node."),
        N.callout(
            "Analogy: Think of each node as a 'relay station'. It can extend a univalue chain left and right only if the neighboring relay has the same 'color'. The station reports its longest single arm to its parent, but we separately record the widest span (left + right) that passes through it.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def longestUnivaluePath(root):\n"
        "    ans = 0\n"
        "    def dfs(node):\n"
        "        nonlocal ans\n"
        "        if not node: return 0\n"
        "        l = dfs(node.left)\n"
        "        r = dfs(node.right)\n"
        "        left_arm  = (l + 1) if node.left  and node.left.val  == node.val else 0\n"
        "        right_arm = (r + 1) if node.right and node.right.val == node.val else 0\n"
        "        ans = max(ans, left_arm + right_arm)\n"
        "        return max(left_arm, right_arm)\n"
        "    dfs(root)\n"
        "    return ans\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("ans = 0", {"code": True}), " — nonlocal tracker for the best path length seen so far across the entire tree."])),
    N.para(N.rich([("def dfs(node)", {"code": True}), " — helper that returns the arm length: longest univalue chain going DOWN from this node in ONE direction."])),
    N.para(N.rich([("if not node: return 0", {"code": True}), " — base case: null node contributes 0; the chain terminates here."])),
    N.para(N.rich([("l = dfs(node.left)", {"code": True}), " — recurse left first (postorder). Gets arm length from left child downward."])),
    N.para(N.rich([("r = dfs(node.right)", {"code": True}), " — recurse right. Gets arm length from right child downward."])),
    N.para(N.rich([("left_arm = (l+1) if ...", {"code": True}), " — extend left by 1 edge ONLY if left child exists AND its value matches current node's value. Otherwise reset to 0 (chain breaks)."])),
    N.para(N.rich([("right_arm = (r+1) if ...", {"code": True}), " — same logic for the right direction."])),
    N.para(N.rich([("ans = max(ans, left_arm + right_arm)", {"code": True}), " — the full path through this node spans both arms. Update global max. This is the 'diameter' at this node."])),
    N.para(N.rich([("return max(left_arm, right_arm)", {"code": True}), " — return only the BEST SINGLE ARM upward. The parent can only extend in one direction — it needs the single-direction max, not the sum."])),
    N.callout(
        "🚨 Classic Bug: returning left_arm + right_arm to the parent is WRONG. It tells the parent it can branch both ways, violating the 'no fork' property of a path. Always return max(left_arm, right_arm).",
        "🚨", "red_background"
    ),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Per-Node Arm Recomputation (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each node, independently compute how far the univalue chain extends left and right using that node's value as the target."),
        N.h4("What Doesn't Work (at scale)"),
        N.para("The arm() function is called fresh for every node in solve(). Subtrees get re-traversed multiple times. A balanced tree of height h has the root's subtree traversed at every ancestor — O(n) traversals × O(n) nodes = O(n²) total."),
        N.h4("The Key Observation"),
        N.para("The optimal solution avoids redundant work by combining the arm computation and the global max update into a single postorder pass. Each node's arm is computed exactly once and passed up to the parent."),
        N.h4("Building the Solution"),
        N.para("For each node, call arm(left_child, node.val) + arm(right_child, node.val). Recurse through the tree to find the maximum across all nodes."),
    ]),
    N.h3("Code"),
    N.code(
        "def longestUnivaluePath(root):\n"
        "    def arm(node, val):\n"
        "        if not node or node.val != val: return 0\n"
        "        return 1 + max(arm(node.left, val), arm(node.right, val))\n"
        "\n"
        "    def solve(node):\n"
        "        if not node: return 0\n"
        "        here = arm(node.left, node.val) + arm(node.right, node.val)\n"
        "        return max(here, solve(node.left), solve(node.right))\n"
        "\n"
        "    return solve(root)\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def arm(node, val)", {"code": True}), " — returns how far we can extend downward from node matching val. Stops when value changes or node is null."])),
    N.para(N.rich([("here = arm(left, val) + arm(right, val)", {"code": True}), " — compute the path width through this node by independently measuring both arms."])),
    N.para(N.rich([("return max(here, solve(left), solve(right))", {"code": True}), " — answer is the maximum of this node's path width vs. the best found anywhere in either subtree."])),
    N.callout(
        "Why O(n²): arm() is called inside solve() which itself traverses all n nodes. For each of n nodes, arm() traverses up to O(n) nodes in the subtree. Result: O(n²). The optimal DFS avoids this by sharing arm computation across the single postorder pass.",
        "💡", "gray_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS Postorder (Optimal)", "O(n)", "O(h)", "h = tree height; O(log n) balanced, O(n) skewed"],
        ["Brute Force (per-node arm)", "O(n²)", "O(h)", "arm() re-traverses subtree for each node"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS Postorder)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Return Depth, Track Max — DFS helper returns arm length upward; nonlocal variable tracks the global best diameter/span."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for the longest/shortest/heaviest PATH in a tree\n"
        "• The path can 'turn' at any node (passes through both left AND right subtrees)\n"
        "• The answer is not necessarily a root-to-leaf path\n"
        "• You need to report a different value upward vs. what you track globally\n"
        "Examples: Binary Tree Diameter, Max Path Sum, Longest Zigzag Path, this problem",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'Return Arm, Track Max' pattern or closely related DFS postorder technique:"),
    N.bullet(N.rich([("Binary Tree Diameter", {"bold": True}), " (Easy, #543) — Identical pattern without value constraint; arm = edge count, no equality check."])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard, #124) — Arm = max path gain going down one direction; ans tracks left_gain + right_gain + node.val globally."])),
    N.bullet(N.rich([("Longest Zigzag Path in a Binary Tree", {"bold": True}), " (Medium, #1372) — Arm carries direction state (left/right); flip direction at each step."])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), " (Medium, #337) — Postorder DFS returning a pair (rob_this, skip_this); parent picks the best combination."])),
    N.bullet(N.rich([("Diameter of N-ary Tree", {"bold": True}), " (Medium, #1522) — Same pattern generalized: sum the two longest arms across all children."])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}), " (Medium, #437) — DFS with prefix sum to count all paths summing to target anywhere in the tree."])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}), " (Medium, #1448) — DFS passing max-so-far downward; count nodes greater than or equal to all ancestors."])),
    N.para("These problems share the same core technique: postorder DFS where the helper returns a local property (arm length, gain, direction) and a global variable captures the best cross-node combination."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees, Sub-pattern: Return Depth, Track Max (DFS Postorder)", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_univalue_path")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# 4) Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# 5) Write status file
import json
status_dir = os.path.join(os.path.dirname(__file__), ".status")
os.makedirs(status_dir, exist_ok=True)
status_path = os.path.join(status_dir, "longest_univalue_path.json")
html_path = os.path.join(os.path.dirname(__file__), "longest_univalue_path_explainer.html")
html_lines = sum(1 for _ in open(html_path))
status = {
    "slug": "longest_univalue_path",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Full regeneration: 7-section HTML with tree SVG walkthrough, DFS postorder visualization, 13 steps."
}
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)

print(f"RESULT longest_univalue_path | html=OK | notion=OK | lines={html_lines}")
