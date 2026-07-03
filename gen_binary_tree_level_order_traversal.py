"""
gen_binary_tree_level_order_traversal.py
Creates a NEW Notion page for LeetCode #102 — Binary Tree Level Order Traversal
(notion_page_id was null, so we call N.create_page first)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 1: Create the page (notion_page_id was null) ──────────────────────
PAGE_ID = N.create_page("Binary Tree Level Order Traversal", 102, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ── Step 2: Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=102,
    pattern="Trees",
    subpatterns=["BFS: Level Order"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Snapshot len(queue) at the start of each level to process exactly that many nodes before moving to the next level.",
    icon="🟡"
)
print("Properties set.")

# ── Step 3: Build body blocks ───────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the root of a binary tree, return the ", {}),
        ("level order traversal", {"bold": True}),
        (" of its node values (i.e., from left to right, level by level). Return the result as a list of lists — one inner list per level."),
    ])),
    N.para("Example: for the tree rooted at 3 with children 9 and 20, where 20 has children 15 and 7 → output [[3], [9, 20], [15, 7]]."),
    N.divider(),
]

# Solution 1 — BFS (Interview Pick)
sol1_code = """\
from collections import deque

def levelOrder(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        level_size = len(queue)   # FREEZE: nodes at this level
        level_vals = []
        for _ in range(level_size):
            node = queue.popleft()
            level_vals.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_vals)
    return result"""

blocks += [
    N.h2("Solution 1 — BFS with Level Snapshot (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to visit a tree's nodes grouped by their depth. A queue (FIFO) naturally processes nodes in the order they were discovered — which corresponds to level order. The sub-problem: how do we know when level k ends and level k+1 begins?"),
        N.h4("What Doesn't Work"),
        N.para("A plain BFS visits nodes in level order but doesn't naturally separate them into groups. We'd need extra bookkeeping. A naive approach might use a 'sentinel' or 'null marker' to delimit levels — but that's messy."),
        N.h4("The Key Observation"),
        N.para("When we start processing level k, the queue contains exactly the nodes at level k (because we enqueued them while processing level k-1). Snapshotting len(queue) before the inner loop gives us a stable count — even as we enqueue new children, we only dequeue the original batch."),
        N.h4("Building the Solution"),
        N.para("1. Seed queue with root. 2. Outer while loop: snapshot level_size = len(queue). 3. Inner for loop: dequeue level_size nodes, collect values, enqueue their children. 4. Append level_vals to result. Repeat until queue empty."),
        N.callout("Analogy: Imagine floors of a building. You're on floor 0 (root). You count everyone on floor 0 first — that's your 'snapshot'. You interview each and note who is on floor 1. Move to floor 1, count again, repeat.", "🏢", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — deque gives O(1) popleft; list.pop(0) is O(n) because it shifts all remaining elements."])),
    N.para(N.rich([("if not root: return []", {"code": True}), " — Guard clause for empty tree. Nothing to traverse."])),
    N.para(N.rich([("queue = deque([root])", {"code": True}), " — Seed BFS. The root is the only node at level 0."])),
    N.para(N.rich([("result = []", {"code": True}), " — Accumulates the sublists, one per level."])),
    N.para(N.rich([("while queue:", {"code": True}), " — Outer loop runs until every node has been processed."])),
    N.para(N.rich([("level_size = len(queue)", {"code": True}), " — CRITICAL: freeze the count of nodes at the current level before the inner loop runs."])),
    N.para(N.rich([("level_vals = []", {"code": True}), " — Fresh bucket for this level's values."])),
    N.para(N.rich([("for _ in range(level_size):", {"code": True}), " — Process exactly level_size nodes — no more, no fewer."])),
    N.para(N.rich([("node = queue.popleft()", {"code": True}), " — Dequeue front node in O(1)."])),
    N.para(N.rich([("level_vals.append(node.val)", {"code": True}), " — Record the node's value."])),
    N.para(N.rich([("if node.left / if node.right:", {"code": True}), " — Enqueue children only if they exist. They'll form the next level in the queue."])),
    N.para(N.rich([("result.append(level_vals)", {"code": True}), " — Level is complete; store its values. Outer loop continues for the next level."])),
    N.para(N.rich([("return result", {"code": True}), " — List of lists: one inner list per tree level."])),
    N.divider(),
]

# Solution 2 — DFS with depth
sol2_code = """\
def levelOrder_dfs(root):
    result = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):   # first visit to this depth
            result.append([])
        result[depth].append(node.val)
        dfs(node.left,  depth + 1)
        dfs(node.right, depth + 1)
    dfs(root, 0)
    return result"""

blocks += [
    N.h2("Solution 2 — DFS with Depth Parameter"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of managing a queue, use the call stack (recursion). Pass each node's depth as a parameter. When visiting a node at depth d, slot its value into result[d]."),
        N.h4("The Key Observation"),
        N.para("A preorder DFS (root, left, right) visits a node before any of its descendants. So the first time we encounter depth d, we open a new list. Subsequent visits to depth d append to that list."),
        N.h4("Why BFS is Still Preferred"),
        N.para("DFS uses O(h) call stack space where h is the tree height. For a skewed tree, h = n, giving O(n) stack frames — potential stack overflow on very deep trees. BFS uses O(w) queue space where w is the maximum width. Both are O(n) worst case, but BFS is the expected interview answer for level-order problems."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def dfs(node, depth):", {"code": True}), " — Recursive helper; depth tracks how far below root we are."])),
    N.para(N.rich([("if depth == len(result):", {"code": True}), " — If we've never visited this depth before, open a new list. This happens exactly once per depth level."])),
    N.para(N.rich([("result[depth].append(node.val)", {"code": True}), " — Slot the value into the correct level's sublist."])),
    N.para(N.rich([("dfs(node.left, depth + 1) / dfs(node.right, depth + 1)", {"code": True}), " — Recurse with incremented depth. Left subtree visited before right (preorder), so left nodes appear before right nodes in each level — correct behavior."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS with level snapshot (Interview Pick)", "O(n)", "O(n) — queue holds max one level (up to n/2 leaves)"],
        ["DFS with depth parameter", "O(n)", "O(h) — recursion stack; h = O(log n) balanced, O(n) skewed"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Level Order — process all nodes at depth d before depth d+1 using a queue with level-size snapshot."])),
    N.callout(
        "When to recognize this pattern: problem says 'level by level', 'row by row', 'layer by layer', or asks to group nodes by depth. Also used when you need the minimum depth (BFS hits the shallowest leaf first) or need to process siblings together.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Level-Order technique:"),
    N.bullet(N.rich([("103 — Binary Tree Zigzag Level Order Traversal", {"bold": True}), " (Medium) — Same BFS; reverse level list on odd levels."])),
    N.bullet(N.rich([("199 — Binary Tree Right Side View", {"bold": True}), " (Medium) — BFS; append only the last element of each level."])),
    N.bullet(N.rich([("637 — Average of Levels in Binary Tree", {"bold": True}), " (Easy) — BFS; compute mean of each level_vals list."])),
    N.bullet(N.rich([("515 — Find Largest Value in Each Tree Row", {"bold": True}), " (Medium) — BFS; track max per level."])),
    N.bullet(N.rich([("111 — Minimum Depth of Binary Tree", {"bold": True}), " (Easy) — BFS; return level count at first leaf node encountered."])),
    N.bullet(N.rich([("662 — Maximum Width of Binary Tree", {"bold": True}), " (Medium) — BFS with column index; track leftmost and rightmost per level."])),
    N.bullet(N.rich([("994 — Rotting Oranges", {"bold": True}), " (Medium) — Multi-source BFS on a grid; level counter gives minimum time."])),
    N.para("These problems all share the same core mechanism: a queue that processes nodes FIFO, with level boundaries detected via a frozen queue-length snapshot."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Trees / BFS: Level Order", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_tree_level_order_traversal")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("Blocks appended.")
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
