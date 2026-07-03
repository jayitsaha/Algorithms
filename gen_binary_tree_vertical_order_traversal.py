"""
gen_binary_tree_vertical_order_traversal.py
Notion IN-PLACE update for LeetCode #314 — Binary Tree Vertical Order Traversal
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81de-8b94-d8c7ace9c465"

# ── 1) Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=314,
    pattern="Trees",
    subpatterns=["Column Index + BFS"],
    tc="O(n)",
    sc="O(n)",
    key_insight="BFS with column index tracking: root=0, left=parent-1, right=parent+1; BFS gives top-to-bottom order for free.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the ", {}),
        ("vertical order traversal", {"bold": True}),
        (" of its nodes' values (i.e., from top to bottom, column by column). ", {}),
        ("If two nodes are in the same row and column, the order should be from left to right.", {}),
    ])),
    N.para("Example: root=[3,9,20,null,null,15,7] → [[9],[3,15],[20],[7]]"),
    N.divider(),
]

# ── Solution 1: BFS + Column Index (Interview Pick) ──────────────────────
blocks += [
    N.h2("Solution 1 — BFS + Column Index (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of shining vertical light beams through the tree. Each beam is a column. The root is at column 0. Every left-turn from any node moves one column left; every right-turn moves one column right. We need to collect all nodes per column, ordered top-to-bottom within each column."),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS visits nodes in pre/in/post order — not level-by-level. If you try DFS without tracking depth, a deep left-subtree node may be appended before a shallower right-subtree node in the same column, violating top-to-bottom order. You'd need to store (level, val) pairs and sort, adding O(n log n) complexity."),
        N.h4("The Key Observation"),
        N.para("BFS processes the tree level by level. All level-0 nodes are processed before level-1, level-1 before level-2, and so on. Therefore, if we group nodes by column index and append in BFS order, the within-column ordering is automatically top-to-bottom. No explicit sort is needed — BFS does it for free."),
        N.h4("Building the Solution"),
        N.para("1. Assign column 0 to root.\n2. Use a BFS deque storing (node, col) pairs.\n3. Maintain a defaultdict(list) mapping col → [values].\n4. Track min_col and max_col to avoid sorting dict keys at the end.\n5. On dequeue, append node.val to col_map[col], update min/max, enqueue children with col±1.\n6. After BFS completes, iterate range(min_col, max_col+1) to build the result list."),
        N.callout("Analogy: Imagine the tree printed on paper. Draw vertical lines at each column position. The nodes touching each line, read top-to-bottom, form one entry in the result. BFS is the natural 'read top-to-bottom' mechanism.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
from collections import defaultdict, deque

def verticalOrder(root):
    if not root:
        return []
    col_map = defaultdict(list)
    queue = deque([(root, 0)])
    min_col = max_col = 0
    while queue:
        node, col = queue.popleft()
        col_map[col].append(node.val)
        min_col = min(min_col, col)
        max_col = max(max_col, col)
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    return [col_map[c] for c in range(min_col, max_col + 1)]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import defaultdict, deque", {"code": True}), " — import deque for O(1) popleft (critical!) and defaultdict for auto-initializing column lists."])),
    N.para(N.rich([("if not root: return []", {"code": True}), " — base case: empty tree has no vertical columns."])),
    N.para(N.rich([("col_map = defaultdict(list)", {"code": True}), " — maps each column index to its list of values; auto-creates an empty list on first access to any column."])),
    N.para(N.rich([("queue = deque([(root, 0)])", {"code": True}), " — BFS queue initialized with root at column 0. Each item is a (TreeNode, column_index) pair."])),
    N.para(N.rich([("min_col = max_col = 0", {"code": True}), " — track the leftmost and rightmost columns seen so far. Avoids sorting dictionary keys at the end."])),
    N.para(N.rich([("node, col = queue.popleft()", {"code": True}), " — dequeue the next node. popleft() on a deque is O(1). If you used list.pop(0) instead, this would be O(n) per call — disaster for BFS."])),
    N.para(N.rich([("col_map[col].append(node.val)", {"code": True}), " — record this node's value under its column. Because BFS processes nodes top-to-bottom, appending in dequeue order gives correct within-column ordering."])),
    N.para(N.rich([("min_col = min(min_col, col)", {"code": True}), " — extend the tracked range leftward if this column is further left than any seen before."])),
    N.para(N.rich([("max_col = max(max_col, col)", {"code": True}), " — extend the tracked range rightward if this column is further right than any seen before."])),
    N.para(N.rich([("queue.append((node.left, col-1))", {"code": True}), " — left child is one column to the left. Enqueue only if it exists."])),
    N.para(N.rich([("queue.append((node.right, col+1))", {"code": True}), " — right child is one column to the right. Enqueue only if it exists."])),
    N.para(N.rich([("return [col_map[c] for c in range(min_col, max_col+1)]", {"code": True}), " — iterate from leftmost to rightmost column and collect each column's list. This produces the final left-to-right, top-to-bottom result."])),
    N.divider(),
]

# ── Solution 2: DFS with (level, val) sort ───────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS with (column, level) Tracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("DFS is simpler to write recursively. The challenge is that DFS doesn't inherently visit nodes top-to-bottom. To compensate, store the level (depth from root) alongside each value. Then sort within each column by level after the DFS completes."),
        N.h4("What Doesn't Work (Simpler)"),
        N.para("Pure DFS without level tracking would produce incorrect within-column ordering. For example, in a tree where nodes A (level 1) and B (level 3) share a column, DFS might visit B before A depending on the tree structure."),
        N.h4("The Key Observation"),
        N.para("Attach the level (depth) to each stored value. After the full DFS, sort each column's list by level to restore top-to-bottom order. This approach is O(n log n) but more naturally fits a recursive implementation."),
        N.h4("Building the Solution"),
        N.para("1. Run DFS passing (col, level).\n2. Store (level, val) pairs in col_map.\n3. After DFS, sort each column list by level.\n4. Sort column keys to produce left-to-right output."),
        N.callout("This approach is required for LC #987 (harder variant) where within same-level same-column nodes must be sorted by value — a constraint that breaks BFS's natural ordering guarantee.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def verticalOrder_dfs(root):
    col_map = defaultdict(list)  # col -> [(level, val), ...]

    def dfs(node, col, level):
        if not node:
            return
        col_map[col].append((level, node.val))
        dfs(node.left,  col - 1, level + 1)
        dfs(node.right, col + 1, level + 1)

    dfs(root, 0, 0)
    # Sort each column by level; sort column keys for left-to-right order
    return [[v for _, v in sorted(col_map[c])]
            for c in sorted(col_map.keys())]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("col_map[col].append((level, node.val))", {"code": True}), " — store a tuple (level, val) so we can sort by depth later. Without the level, we cannot reconstruct top-to-bottom ordering from a DFS visit sequence."])),
    N.para(N.rich([("sorted(col_map[c])", {"code": True}), " — sort each column's list by (level, val) tuples. Since tuples sort lexicographically, level is the primary sort key — guaranteeing top-to-bottom within a column."])),
    N.para(N.rich([("for c in sorted(col_map.keys())", {"code": True}), " — sort column indices (integers) from left to right. Unlike the BFS approach, we don't have min/max col here, so we sort the dictionary keys."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS + Column Index (Interview Pick)", "O(n)", "O(n)", "Preferred; BFS gives top-to-bottom for free"],
        ["DFS + (level, val) sort", "O(n log n)", "O(n)", "Needed for LC #987 variant; sort within columns"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Column Index + BFS (extends BFS: Level Order)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'vertical' or 'column' grouping of tree nodes\n"
        "• Need 'top-to-bottom within group' ordering → BFS instead of DFS\n"
        "• Need horizontal position of tree nodes → assign column index\n"
        "• Maximum width of binary tree → same column index idea per level\n"
        "• Key signal: 'vertical order', 'column by column', 'same vertical line'",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}), ("Column Index + BFS", {"italic": True}), (" is a specialization of BFS Level Order (guide Section 5) with an added horizontal position tracker. The sub-pattern is based on analysis.", {"italic": True})])),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (column index / BFS level-order):"),
    N.bullet(N.rich([("Vertical Order Traversal of a Binary Tree", {"bold": True}), " (#987, Hard) — same column index but sort by (level, val) within each column; BFS is insufficient for the tie-breaking rule."])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (#102, Medium) — pure BFS backbone; group by level instead of column. Core building block for this problem."])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (#199, Medium) — BFS level-order; pick the last node dequeued per level."])),
    N.bullet(N.rich([("Binary Tree Zigzag Level Order Traversal", {"bold": True}), " (#103, Medium) — BFS with a direction flag toggled each level."])),
    N.bullet(N.rich([("Maximum Width of Binary Tree", {"bold": True}), " (#662, Medium) — assign column index per node; width = max_col − min_col + 1 at each level."])),
    N.bullet(N.rich([("Find Leaves of Binary Tree", {"bold": True}), " (#366, Medium) — group nodes by their distance from the leaves (reverse depth); analogous grouping concept."])),
    N.para("These problems share the same core technique: BFS with a positional label (level, column, or width) attached to each queued node."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5: Trees → BFS: Level Order", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_tree_vertical_order_traversal")),
    N.para(N.rich([("Step through the BFS traversal visually — use Next/Prev or arrow keys to watch each node get placed in its column.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
