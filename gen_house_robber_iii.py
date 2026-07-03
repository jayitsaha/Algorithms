"""
gen_house_robber_iii.py — DSA pipeline: House Robber III (#337)
Tree DP sub-pattern: "Return rob and not-rob pair"
notion_page_id = null → create new page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ─── 1. Create the page (null → create) ───────────────────────────────────────
PAGE_ID = N.create_page("House Robber III", 337, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ─── 2. Set properties ────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=337,
    pattern="Dynamic Programming",
    subpatterns=["Return rob and not-rob pair"],
    tc="O(n)",
    sc="O(h)  # h = tree height, O(log n) balanced / O(n) skewed",
    key_insight="For each node, return a pair (rob_this, skip_this); parent picks max without global memo.",
    icon="🟡",
)
print("Properties set.")

# ─── 3. Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "The thief has found himself a new place for his burglary again. There is only one entrance to this area, called the ",
        ("root", {"code": True}),
        ". Besides the ",
        ("root", {"code": True}),
        ", each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a ",
        ("binary tree", {"bold": True}),
        ". It will automatically contact the police if two directly-linked houses were broken into on the same night.\n\n"
        "Given the ",
        ("root", {"code": True}),
        " of the binary tree, return the maximum amount of money the thief can rob without alerting the police.",
    ])),
    N.callout(
        N.rich([
            ("Constraint: ", {"bold": True}),
            "You cannot rob two adjacent nodes (parent and child). Grand-children are fine.",
        ]),
        "🚨", "red_background"
    ),
    N.divider(),
]

# ── Solution 1 — Tree DP Pair (Optimal, Interview Pick) ───────────────────────
SOL1_CODE = '''\
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def rob(root: Optional[TreeNode]) -> int:
    def dp(node):
        # Base case: null node contributes 0 either way
        if not node:
            return (0, 0)          # (rob_this_node, skip_this_node)

        left_rob, left_skip   = dp(node.left)
        right_rob, right_skip = dp(node.right)

        # If we rob this node: children MUST be skipped
        rob_this  = node.val + left_skip + right_skip

        # If we skip this node: children can be robbed OR skipped (take max)
        skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)

        return (rob_this, skip_this)

    rob_root, skip_root = dp(root)
    return max(rob_root, skip_root)
'''

blocks += [
    N.h2("Solution 1 — Tree DP Pair (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "You're walking a binary tree deciding at each node: rob it or skip it. "
            "The rule: if you rob a node, you cannot rob its direct children. "
            "Think of it as a tree where each node must decide independently based on what its subtrees report."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive DFS with a global memo keyed on 'node + can_rob_flag' works but is cumbersome. "
            "A greedy 'rob every other level' fails because trees aren't uniform — "
            "the best choice at one branch might differ from another. "
            "Recursing with just a single return value forces you to recompute or miss out on information."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Instead of returning ONE number per node, return TWO: "
            "(profit if we rob this node, profit if we skip this node). "
            "With both values from each child, the parent has everything it needs to compute its own pair — "
            "no global state, no memo dictionary needed."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Postorder DFS: process children before parent (bottom-up).\n"
            "2. Base case: null node → return (0, 0).\n"
            "3. Get (left_rob, left_skip) from left child, same from right.\n"
            "4. rob_this = node.val + left_skip + right_skip  (children must be skipped)\n"
            "5. skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)  (children choose freely)\n"
            "6. Return (rob_this, skip_this) to parent.\n"
            "7. At root, answer = max(rob_root, skip_root)."
        ),
        N.callout(
            "Analogy: Think of each node as a manager who asks both their direct reports: "
            "'What's your profit if I promote you (rob)? What if I don't (skip)?' "
            "Then the manager picks the best plan for themselves given those answers.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def dp(node):", {"code": True}), " — Inner postorder DFS; takes a node, returns a 2-tuple."])),
    N.para(N.rich([("if not node: return (0, 0)", {"code": True}), " — Null node: no value whether robbed or skipped."])),
    N.para(N.rich([("left_rob, left_skip = dp(node.left)", {"code": True}), " — Recurse left; unpack the pair."])),
    N.para(N.rich([("right_rob, right_skip = dp(node.right)", {"code": True}), " — Same for right child."])),
    N.para(N.rich([("rob_this = node.val + left_skip + right_skip", {"code": True}), " — Rob current node: must skip both children (use their skip values)."])),
    N.para(N.rich([("skip_this = max(left_rob, left_skip) + max(right_rob, right_skip)", {"code": True}), " — Skip current: each child is free to be robbed or skipped independently."])),
    N.para(N.rich([("return (rob_this, skip_this)", {"code": True}), " — Bubble both options up to parent."])),
    N.para(N.rich([("return max(rob_root, skip_root)", {"code": True}), " — At root: pick whichever option yields more money."])),
    N.divider(),
]

# ── Solution 2 — Memoized DFS (top-down, with flag) ─────────────────────────
SOL2_CODE = '''\
from functools import lru_cache

def rob(root) -> int:
    @lru_cache(maxsize=None)
    def dfs(node, can_rob: bool):
        if node is None:
            return 0
        # Option A: skip this node — children can be robbed
        skip = dfs(node.left, True) + dfs(node.right, True)
        if not can_rob:
            return skip
        # Option B: rob this node — children must be skipped
        rob_it = node.val + dfs(node.left, False) + dfs(node.right, False)
        return max(skip, rob_it)

    return dfs(root, True)
'''

blocks += [
    N.h2("Solution 2 — Memoized DFS (Top-Down)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Model it as: at each node, you receive a flag 'can_rob' from your parent. Recurse with that constraint."),
        N.h4("What Doesn't Work"),
        N.para(
            "Without memoization, this DFS re-explores the same node with the same flag repeatedly when the tree has repeated subtree shapes. "
            "With @lru_cache, each (node, can_rob) pair is computed at most once."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The state is (node_id, can_rob). Two nodes at different tree positions are distinct even if they have the same value. "
            "Python's lru_cache uses object identity for node references, so this is safe."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. dfs(node, can_rob=True): entry point.\n"
            "2. Always compute 'skip' = dfs(left, True) + dfs(right, True).\n"
            "3. If can_rob=False, return skip immediately.\n"
            "4. Otherwise compute 'rob_it' and return max(skip, rob_it)."
        ),
        N.callout(
            "This approach is more natural to derive from scratch but slightly slower in practice "
            "due to lru_cache overhead. The pair approach (Solution 1) is preferred.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " — Memoize on (node, can_rob); Python caches by argument identity."])),
    N.para(N.rich([("skip = dfs(left, True) + dfs(right, True)", {"code": True}), " — If we skip this node, children are unconstrained."])),
    N.para(N.rich([("if not can_rob: return skip", {"code": True}), " — Parent robbed us; can only skip. No choice."])),
    N.para(N.rich([("rob_it = node.val + dfs(left, False) + dfs(right, False)", {"code": True}), " — Rob this node; children forced to skip."])),
    N.para(N.rich([("return max(skip, rob_it)", {"code": True}), " — Pick whichever option is more profitable."])),
    N.divider(),
]

# ── Solution 3 — Brute Force (no memo) ────────────────────────────────────────
SOL3_CODE = '''\
def rob(root) -> int:
    if not root:
        return 0
    # Rob this node: skip children, but can rob grandchildren
    rob_this = root.val
    if root.left:
        rob_this += rob(root.left.left) + rob(root.left.right)
    if root.right:
        rob_this += rob(root.right.left) + rob(root.right.right)
    # Skip this node: recurse normally into children
    skip_this = rob(root.left) + rob(root.right)
    return max(rob_this, skip_this)
'''

blocks += [
    N.h2("Solution 3 — Brute Force Recursion (Exponential)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most natural approach: at each node, try both options and take the max."),
        N.h4("What Doesn't Work"),
        N.para(
            "This re-visits subtrees exponentially many times. For a balanced tree of depth d, "
            "time is O(2^d) = O(n^1.585) approximately. For a skewed tree of n nodes, it's O(2^n). "
            "This is the baseline to improve from — always present this first, then optimize."
        ),
        N.h4("The Key Observation"),
        N.para("Subproblems overlap: rob(node) is called many times for the same node. That's the cue for memoization (Solution 2) or bottom-up DP (Solution 1)."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.callout(
        N.rich([
            ("Time: O(2^n) worst case — ", {"bold": True}),
            "each node spawns two recursive calls without sharing. Only good for understanding; never submit this.",
        ]),
        "⚠️", "orange_background"
    ),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(2^n)", "O(h)", "Exponential overlapping calls"],
        ["Memoized DFS", "O(n)", "O(n)", "n states × O(1) work each; cache size O(n)"],
        ["Tree DP Pair ✓", "O(n)", "O(h)", "No memo dict; stack space only. O(log n) balanced."],
    ]),
    N.divider(),
]

# ── Why is this DP? ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        "The maximum profit for a subtree rooted at node X depends only on the maximum profits from X.left and X.right. "
        "Larger problems decompose cleanly into smaller, independent subproblems.",
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        "In the brute-force version, rob(node) is called repeatedly for the same node from different ancestors. "
        "Memoizing (or bottom-up pairing) eliminates this redundancy.",
    ])),
    N.callout(
        N.rich([
            ("Recurrence: ", {"bold": True}),
            "rob(node) = max(\n"
            "  node.val + rob_skip(left) + rob_skip(right),   # rob this\n"
            "  rob_best(left) + rob_best(right)               # skip this\n"
            ")\nwhere rob_skip(x) = 'profit if x is skipped' and rob_best(x) = max of both options.",
        ]),
        "📐", "blue_background"
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Return rob and not-rob pair (Tree DP)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem is on a tree (binary or N-ary)\n"
        "• Each node must make a binary choice (include/exclude)\n"
        "• Adjacent nodes (parent-child) have conflicting constraints\n"
        "• You find yourself wanting to know BOTH 'what if I take this' AND 'what if I skip this'\n"
        "• Returning a tuple instead of a scalar from each recursive call is the unlock.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Guide Reference: ", {"bold": True}),
        "DSA_Patterns_and_SubPatterns_Guide.md, Section 18 (Dynamic Programming) → DP: Tree sub-pattern.",
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Tree DP / rob-and-not-rob pair):"),
    N.bullet(N.rich([("House Robber", {"bold": True}), " (Easy) — 1D array version; DP[i] = max(rob i, skip i)"])),
    N.bullet(N.rich([("House Robber II", {"bold": True}), " (Medium) — Circular array; run linear DP twice with/without first element"])),
    N.bullet(N.rich([("Binary Tree Cameras", {"bold": True}), " (Hard) — Tree DP returning a 3-state tuple per node"])),
    N.bullet(N.rich([("Distribute Coins in Binary Tree", {"bold": True}), " (Medium) — Postorder; pass excess/deficit up the tree"])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}), " (Hard) — Two DFS passes; re-root technique is related Tree DP idea"])),
    N.bullet(N.rich([("Maximum Product of Splitted Binary Tree", {"bold": True}), " (Medium) — Postorder subtree sums; pick best split"])),
    N.bullet(N.rich([("Delete Nodes And Return Forest", {"bold": True}), " (Medium) — Postorder; decisions affect tree structure"])),
    N.para("These problems share the core technique: return structured information (a tuple/state) up the tree in postorder, letting each parent compute its answer in O(1) from children's reports."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — DP: Tree", "📚", "gray_background"),
]

# ── Visual Explainer Embed ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("house_robber_iii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ─── 5. Write status file ─────────────────────────────────────────────────────
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
html_lines = len(open(pathlib.Path(__file__).parent / "house_robber_iii_explainer.html").readlines())
status = {
    "slug": "house_robber_iii",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Tree DP pair; new Notion page created; HTML pre-existing (966 lines, passed resume check)"
}
(status_dir / "house_robber_iii.json").write_text(json.dumps(status, indent=2))
print(f"RESULT house_robber_iii | html=OK | notion=OK | lines={html_lines}")
