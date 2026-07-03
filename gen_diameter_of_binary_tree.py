"""
gen_diameter_of_binary_tree.py
Notion page update for LeetCode #543 – Diameter of Binary Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8104-ac7a-d4c79a066524"

# ── 1. Properties ───────────────────────────────────────────────────────────
print("Setting properties…")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=543,
    pattern="Trees",
    subpatterns=["Max Left + Right Depth"],
    tc="O(n)",
    sc="O(h)",
    key_insight="At every node, the diameter candidate = left_depth + right_depth; postorder DFS computes this in a single O(n) pass.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old content ─────────────────────────────────────────────────────
print("Wiping old blocks…")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("root", {"code": True}),
        " of a binary tree, return the length of the ",
        ("diameter", {"bold": True}),
        " of the tree. The diameter is the length of the longest path between any two nodes, measured in number of edges. The path does not need to pass through the root.",
    ])),
    N.divider(),
]

# ── Solution 1: Postorder DFS ──
sol1_code = """\
def diameterOfBinaryTree(self, root):
    self.diameter = 0
    def dfs(node):
        if not node:
            return 0
        L = dfs(node.left)
        R = dfs(node.right)
        self.diameter = max(self.diameter, L + R)
        return 1 + max(L, R)
    dfs(root)
    return self.diameter"""

blocks += [
    N.h2("Solution 1 — Postorder DFS + Global Max (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every path in a binary tree has a unique highest node — the point where the path turns from going left-down to going right-down. The length of the path through that turning point is the sum of the depths of its left and right subtrees. We need to find the maximum of this sum across all nodes."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach computes left depth + right depth only at the root. This misses cases where the longest path is entirely within a subtree and never crosses the root. A slightly better brute force calls a separate depth() helper at every node, but this recomputes depths repeatedly, giving O(n²) time."),
        N.h4("The Key Observation"),
        N.para("The DFS function must serve two purposes simultaneously: (1) return the depth of the current subtree to its parent, and (2) update a global maximum with left_depth + right_depth at the current node. Crucially, the returned value (1 + max(L, R)) and the diameter candidate (L + R) are different — combining both in one pass gives O(n)."),
        N.h4("Building the Solution"),
        N.para("Use a nested dfs() function. Base case: null → 0. Recurse left, recurse right. Update self.diameter with L+R (path through this node). Return 1+max(L,R) to the parent (the single best arm downward). After dfs(root) completes, self.diameter holds the answer."),
        N.callout("Analogy: Think of each node as a city. Its 'left arm' reaches to the western frontier, its 'right arm' reaches east. The longest road through the city = west distance + east distance. The global max of this across all cities is the longest highway in the country.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.diameter = 0", {"code": True}), " — Initialize the global max to 0. A single node (no edges) has diameter 0."])),
    N.para(N.rich([("def dfs(node):", {"code": True}), " — Nested helper that returns the depth (max edges downward) and updates self.diameter as a side effect."])),
    N.para(N.rich([("if not node: return 0", {"code": True}), " — Base case: null node contributes zero depth. Every leaf's two children are null and return 0."])),
    N.para(N.rich([("L = dfs(node.left)", {"code": True}), " — Postorder step 1: recurse into left subtree. L = maximum depth reachable going left."])),
    N.para(N.rich([("R = dfs(node.right)", {"code": True}), " — Postorder step 2: recurse into right subtree. R = maximum depth reachable going right."])),
    N.para(N.rich([("self.diameter = max(self.diameter, L + R)", {"code": True}), " — The path through this node uses BOTH arms: L + R edges. Update global max if this is the best so far."])),
    N.para(N.rich([("return 1 + max(L, R)", {"code": True}), " — Return the depth to this node's parent: 1 edge (to connect this node to parent) + the longer of the two arms. We take max (not sum) because a parent can only travel down one side."])),
    N.para(N.rich([("dfs(root)", {"code": True}), " — Start the traversal. The return value at the top level is the root's depth, which we discard."])),
    N.para(N.rich([("return self.diameter", {"code": True}), " — The accumulated global max is the answer."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = """\
def depth(node):
    if not node:
        return 0
    return 1 + max(depth(node.left), depth(node.right))

def diameterOfBinaryTree(root):
    if not root:
        return 0
    through_root = depth(root.left) + depth(root.right)
    left_diam    = diameterOfBinaryTree(root.left)
    right_diam   = diameterOfBinaryTree(root.right)
    return max(through_root, left_diam, right_diam)"""

blocks += [
    N.h2("Solution 2 — Brute Force: Separate depth() Call"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every node, compute the path length through it (left_depth + right_depth), then recursively check the subtrees for potentially longer paths within them."),
        N.h4("What Doesn't Work"),
        N.para("This is the 'obvious first attempt'. It's correct but calls depth() once per node from every ancestor, leading to O(n²) time on unbalanced trees."),
        N.h4("The Key Observation"),
        N.para("This approach correctly identifies all three types of candidates (through root, in left subtree, in right subtree) but computes depths redundantly. Solution 1 eliminates this by merging depth computation and diameter update into a single DFS pass."),
        N.h4("Building the Solution"),
        N.para("Write a separate depth() helper. At each recursive call of diameterOfBinaryTree, compute the candidate through the current root, then take the max with both subtree diameters. Simple and correct, but not optimal."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def depth(node):", {"code": True}), " — Standalone depth helper. Returns the maximum number of edges on any downward path from node."])),
    N.para(N.rich([("through_root = depth(root.left) + depth(root.right)", {"code": True}), " — Candidate path that crosses the current root. Calls depth() on both subtrees."])),
    N.para(N.rich([("left_diam = diameterOfBinaryTree(root.left)", {"code": True}), " — Recursively find the diameter entirely within the left subtree."])),
    N.para(N.rich([("right_diam = diameterOfBinaryTree(root.right)", {"code": True}), " — Same for the right subtree."])),
    N.para(N.rich([("return max(through_root, left_diam, right_diam)", {"code": True}), " — Best among: path through this node, or path purely in left, or path purely in right."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Postorder DFS (Sol 1 — optimal)", "O(n)", "O(h) call stack"],
        ["Brute Force (Sol 2)", "O(n²) worst case", "O(h) call stack"],
        ["Iterative Postorder", "O(n)", "O(n) explicit stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Max Left + Right Depth (Postorder DFS — return depth, update global max)"])),
    N.callout(
        "When to recognize this pattern: The problem asks for a 'longest path' or 'maximum path sum' between any two nodes in a binary tree. The path is allowed to use both left and right children of some pivot node. The DFS must return a different quantity (depth / single arm) than what it contributes to the answer (both arms summed).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same postorder DFS + global max technique:"),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard, #124) — Identical pattern: update global with L+R+node.val; return max(L,R)+node.val to parent. Handles negative values."])),
    N.bullet(N.rich([("Longest Univalue Path", {"bold": True}), " (Medium, #687) — Diameter variant: arms only count if the child value matches the current node value."])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy, #104) — The simpler version: pure depth DFS, no global max needed."])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), " (Easy, #110) — Uses the same depth function; checks |left−right| ≤ 1 at every node."])),
    N.bullet(N.rich([("Diameter of N-Ary Tree", {"bold": True}), " (Medium, #1522) — Generalize to k children: track top-two child depths, sum them as diameter candidate."])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), " (Medium, #337) — Postorder DP on tree: each call returns a pair (rob, skip); bottom-up decision at every node."])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), " (Medium, #113) — Root-to-leaf DFS with path tracking; simpler as it only follows one arm at a time."])),
    N.para("These problems share the same core technique: postorder DFS where information flows bottom-up, and a global max is updated at each node with a combined value from both children."),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("diameter_of_binary_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append in chunks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks…")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
