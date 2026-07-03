"""
gen_maximum_width_of_binary_tree.py
Regenerates the Notion page for LeetCode #662 Maximum Width of Binary Tree IN-PLACE.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8143-9209-cce982eb04ec"

# ── 1) Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=662,
    pattern="Trees",
    subpatterns=["Track Index Per Level", "BFS: Level Order"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Assign virtual heap-array indices; level width = rightmost_idx - leftmost_idx + 1; normalize each level to prevent 2^depth overflow.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ──
PROBLEM_STATEMENT = (
    "Given the root of a binary tree, return the maximum width of the tree. "
    "The width of one level is defined as the length from the leftmost to the rightmost non-null node, "
    "including the null nodes between them. The answer is guaranteed to be in the range of a 32-bit signed integer."
)

SOL1_CODE = """\
from collections import deque

def widthOfBinaryTree(root) -> int:
    if not root:
        return 0
    max_width = 0
    queue = deque([(root, 0)])       # (node, virtual_index)
    while queue:
        level_size = len(queue)
        _, first_idx = queue[0]      # leftmost index this level
        last_idx = first_idx
        for _ in range(level_size):
            node, idx = queue.popleft()
            idx -= first_idx         # NORMALIZE: prevent 2^depth overflow
            last_idx = idx           # rightmost = last processed
            if node.left:
                queue.append((node.left,  2 * idx))
            if node.right:
                queue.append((node.right, 2 * idx + 1))
        # first_idx normalized to 0, so width = last_idx + 1
        max_width = max(max_width, last_idx + 1)
    return max_width
"""

SOL2_CODE = """\
def widthOfBinaryTree(root) -> int:
    left_most = {}    # depth -> leftmost index at that depth
    ans = [0]
    def dfs(node, depth, idx):
        if not node:
            return
        # preorder: left before right ensures first visit = leftmost
        if depth not in left_most:
            left_most[depth] = idx
        ans[0] = max(ans[0], idx - left_most[depth] + 1)
        dfs(node.left,  depth + 1, 2 * idx)
        dfs(node.right, depth + 1, 2 * idx + 1)
    dfs(root, 0, 1)   # 1-based index avoids 0*2=0 edge case
    return ans[0]
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — BFS with Virtual Index Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the widest 'row' in a binary tree — measuring from the leftmost to rightmost "
            "non-null node including any null gaps in between. This is not simply counting non-null "
            "nodes per level. It's measuring positional span."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Counting non-null nodes per level is wrong — it ignores gaps. Materializing all null "
            "nodes with a full serialization is exponential (2^depth nodes at depth d). We need "
            "to measure positions without materializing them."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Recall the heap array representation of binary trees: if a node has virtual index i, "
            "its left child has index 2i and right child has index 2i+1. This assigns a unique "
            "position to every slot (real or null) at every depth. Width = rightmost_index - leftmost_index + 1 "
            "captures all positions including nulls between the endpoints."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Use BFS (natural for per-level processing). Carry (node, virtual_index) pairs in the queue. "
            "At each level, peek at the first node's index (leftmost). Normalize all indices by "
            "subtracting this leftmost — otherwise indices reach 2^depth and overflow. "
            "After processing all nodes on the level, width = last_idx + 1 (since first is normalized to 0). "
            "Update max_width. Enqueue children with indices 2*idx and 2*idx+1."
        ),
        N.callout(
            "Analogy: Think of each tree level as a ruler where root is tick-mark 0. "
            "Left child inherits position 2x, right child 2x+1. Width = rightmost tick - leftmost tick + 1. "
            "Null nodes occupy tick marks between real nodes but we never draw them — the arithmetic captures them.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque([(root, 0)])", {"code": True}), " — Initialize BFS queue with root at virtual index 0."])),
    N.para(N.rich([("level_size = len(queue)", {"code": True}), " — Snapshot queue size before inner loop so we process exactly one level per outer iteration."])),
    N.para(N.rich([("_, first_idx = queue[0]", {"code": True}), " — Peek (don't pop) to get the leftmost index. This is the normalization base."])),
    N.para(N.rich([("idx -= first_idx", {"code": True}), " — NORMALIZE: shift all indices so the leftmost becomes 0. Prevents 2^depth integer overflow."])),
    N.para(N.rich([("last_idx = idx", {"code": True}), " — Track the most recent (rightmost) normalized index. BFS processes left-to-right, so last = rightmost."])),
    N.para(N.rich([("queue.append((node.left, 2*idx))", {"code": True}), " — Left child gets index 2i (heap-array rule). Only enqueue if left child exists."])),
    N.para(N.rich([("queue.append((node.right, 2*idx+1))", {"code": True}), " — Right child gets index 2i+1. Only enqueue if right child exists."])),
    N.para(N.rich([("max_width = max(max_width, last_idx + 1)", {"code": True}), " — Width = last_idx + 1 since first_idx normalized to 0. Update running maximum."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — DFS with Depth-to-LeftmostIndex Map"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal — but instead of BFS, we use preorder DFS (root → left → right). The key: preorder visits the leftmost node at each depth first, so the first time we reach a new depth, we record the leftmost index."),
        N.h4("What Doesn't Work"),
        N.para("Random DFS order (without left-first guarantee) could register a non-leftmost node first. We need preorder specifically."),
        N.h4("The Key Observation"),
        N.para("In preorder DFS visiting left subtree before right, the first time we see depth d, it's always the leftmost node. Store that index. For every subsequent node at depth d, compute width = current_idx - leftmost_idx + 1."),
        N.h4("Building the Solution"),
        N.para("Recursive DFS with parameters (node, depth, idx). Maintain a dict: depth → leftmost_index. On first visit to a depth, record the index. On every visit, update ans with current width. Use 1-based indexing to avoid 0*2=0 ambiguity at the root."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("left_most = {}", {"code": True}), " — Maps depth to the leftmost virtual index seen at that depth."])),
    N.para(N.rich([("if depth not in left_most", {"code": True}), " — Preorder DFS: first visit to each depth is always leftmost. Record it."])),
    N.para(N.rich([("ans[0] = max(ans[0], idx - left_most[depth] + 1)", {"code": True}), " — Width = current index minus leftmost at this depth, plus 1."])),
    N.para(N.rich([("dfs(root, 0, 1)", {"code": True}), " — Start with 1-based index. With 0-based, left child of root would be 2*0=0 which equals root — use 1 to avoid confusion."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS + Virtual Index (Interview Pick)", "O(n)", "O(n) — queue holds up to n/2 nodes at widest level"],
        ["DFS + Depth Map", "O(n)", "O(h) — call stack depth; O(log n) balanced, O(n) skewed"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Index Per Level, BFS: Level Order"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for 'width' or 'span' of a tree level including nulls. "
        "(2) Need position of a node among all possible slots at its depth. "
        "(3) Level-order (BFS) property that depends on structural position, not just values. "
        "(4) 'Is binary tree complete?' — index gaps mean it's not.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS level-order / tree index tracking technique:"),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — Classic BFS; groups nodes by level. Foundation for all level-order variants. (#102)"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — BFS; return last node at each level. (#199)"])),
    N.bullet(N.rich([("Check Completeness of a Binary Tree", {"bold": True}), " (Medium) — BFS + virtual index: if any index gap exists, tree is not complete. (#958)"])),
    N.bullet(N.rich([("Find Bottom Left Tree Value", {"bold": True}), " (Medium) — BFS; first node of the last level. (#513)"])),
    N.bullet(N.rich([("Maximum Level Sum of a Binary Tree", {"bold": True}), " (Medium) — BFS per level; track max sum. (#1161)"])),
    N.bullet(N.rich([("Populating Next Right Pointers", {"bold": True}), " (Medium) — BFS level linking; virtual index helps reason about neighbors. (#116)"])),
    N.para("These problems share the BFS level-order traversal pattern. Width of Binary Tree adds the virtual index trick to measure positional gaps without materializing null nodes."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees Section (BFS: Level Order). Sub-Pattern: Track Index Per Level — Analysis classification (BFS Level Order variant).", "📚", "gray_background"),
]

# Interactive Explainer embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_width_of_binary_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
