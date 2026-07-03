"""
gen_average_of_levels_in_binary_tree.py
Notion in-place update for LeetCode #637 — Average of Levels in Binary Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f6-b6d1-f82fcca49512"
SLUG    = "average_of_levels_in_binary_tree"

# ── 1. Properties ─────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Easy",
    number      = 637,
    pattern     = "Trees",
    subpatterns = ["BFS: Level Order"],
    tc          = "O(n)",
    sc          = "O(w) max width",
    key_insight = "Snapshot level_size=len(queue) before the inner BFS loop to isolate each level.",
    icon        = "🟢",
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ─────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the average value of the nodes on each level "
         "in the form of an array of doubles. Answers within ", {}),
        ("10^-5", {"code": True}),
        (" of the actual answer will be accepted.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: BFS Level Order ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS Level Order (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the average node value at each depth of the tree. Averages require knowing the sum and count of values at each depth. The challenge is grouping nodes by their depth efficiently."),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS visits nodes in depth-first order (root → left subtree → right subtree), mixing nodes from different levels. To separate levels we'd need to track depth separately in a DFS. More importantly, we'd have to scan ALL nodes before computing any average — no natural grouping."),
        N.h4("The Key Observation"),
        N.para("BFS with a queue visits nodes level by level: all depth-0 nodes, then all depth-1 nodes, and so on. If we can identify where one level ends and the next begins, we can sum and count per level in a single pass. The observation: at the START of each BFS iteration, the queue holds EXACTLY all nodes of one level — because we only enqueue children (the next level) during the current iteration."),
        N.h4("Building the Solution"),
        N.para("Seed the queue with the root. Before the inner loop, capture level_size = len(queue). Process exactly that many nodes: dequeue each, add its value to level_sum, and push its non-null children. After the inner loop, level_sum / level_size gives the average for this level. The snapshot of level_size is the key — it prevents the newly enqueued children from inflating the current level count."),
        N.callout("Analogy: Think of a theme park with guests entering floor by floor. Before opening each floor's gate, count the people in the lobby — that count is fixed even as new people arrive from the floor below. Process exactly that many, then move to the next floor.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""from collections import deque

def averageOfLevels(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)   # snapshot: exact count for this level
        level_sum = 0
        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_sum / level_size)  # float division
    return result""",
        "python",
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), (" — Import deque for O(1) popleft(). A plain list.pop(0) is O(n) per call.", {})])),
    N.para(N.rich([("if not root: return []", {"code": True}), (" — Guard: empty tree has no levels.", {})])),
    N.para(N.rich([("queue = deque([root])", {"code": True}), (" — Seed BFS with the root; represents level 0.", {})])),
    N.para(N.rich([("while queue:", {"code": True}), (" — Each outer iteration processes one complete level.", {})])),
    N.para(N.rich([("level_size = len(queue)", {"code": True}), (" — CRITICAL snapshot. Children enqueued later do not affect this count.", {})])),
    N.para(N.rich([("level_sum = 0", {"code": True}), (" — Fresh accumulator for this level.", {})])),
    N.para(N.rich([("for _ in range(level_size):", {"code": True}), (" — Process exactly the nodes belonging to this level.", {})])),
    N.para(N.rich([("node = queue.popleft()", {"code": True}), (" — O(1) dequeue from front.", {})])),
    N.para(N.rich([("level_sum += node.val", {"code": True}), (" — Add node's value to this level's running total.", {})])),
    N.para(N.rich([("if node.left: queue.append(node.left)", {"code": True}), (" — Enqueue left child for the NEXT level.", {})])),
    N.para(N.rich([("if node.right: queue.append(node.right)", {"code": True}), (" — Enqueue right child for the NEXT level.", {})])),
    N.para(N.rich([("result.append(level_sum / level_size)", {"code": True}), (" — Float division gives the level average.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — One float per level, top to bottom.", {})])),
    N.divider(),
]

# ── Solution 2: DFS with depth tracking ───────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS with Depth Tracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of BFS we can use recursive DFS, threading a depth parameter through each call. We maintain two parallel arrays: sums[d] = total of all values at depth d, and counts[d] = number of nodes at depth d."),
        N.h4("What Doesn't Work"),
        N.para("A plain DFS returns values in pre/in/post-order, mixing depths. We need per-depth bookkeeping."),
        N.h4("The Key Observation"),
        N.para("When we visit a node for the first time at a new depth d (where d == len(sums)), we expand the arrays by appending 0. On subsequent visits to the same depth, we just add to the existing entry. At the end, zip(sums, counts) gives us all we need to compute averages."),
        N.h4("Building the Solution"),
        N.para("DFS with depth argument. On entry: if depth is new, extend sums and counts. Always add node.val to sums[depth] and increment counts[depth]. Recurse on left (depth+1) and right (depth+1). Finally, return [s/c for s,c in zip(sums,counts)]."),
        N.callout("When to prefer DFS: Tree is very wide (e.g., near-complete binary tree). BFS queue space = O(w) = O(n/2). DFS call stack = O(h) = O(log n) for a balanced tree — much better in this case.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def averageOfLevels(root):
    sums, counts = [], []

    def dfs(node, depth):
        if not node:
            return
        if depth == len(sums):          # first time at this depth
            sums.append(0)
            counts.append(0)
        sums[depth]   += node.val
        counts[depth] += 1
        dfs(node.left,  depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [s / c for s, c in zip(sums, counts)]""",
        "python",
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("sums, counts = [], []", {"code": True}), (" — Two parallel lists, indexed by depth.", {})])),
    N.para(N.rich([("if depth == len(sums):", {"code": True}), (" — First visit to this depth; expand both lists.", {})])),
    N.para(N.rich([("sums[depth] += node.val", {"code": True}), (" — Accumulate value for this depth.", {})])),
    N.para(N.rich([("counts[depth] += 1", {"code": True}), (" — Count this node.", {})])),
    N.para(N.rich([("dfs(node.left, depth + 1)", {"code": True}), (" — Recurse with depth incremented.", {})])),
    N.para(N.rich([("return [s / c for s, c in zip(sums, counts)]", {"code": True}), (" — Compute averages after DFS completes.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Level Order (Sol 1)", "O(n)", "O(w) — max width"],
        ["DFS Depth Tracking (Sol 2)", "O(n)", "O(h) — tree height"],
    ]),
    N.para("Both solutions visit every node exactly once: O(n) time. Space differs: BFS queue holds at most one full level (max width w); DFS call stack goes as deep as the tree height h. For balanced trees O(h) = O(log n), much better than O(w) = O(n/2). For skewed trees O(h) = O(n), worse than BFS."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Level Order"])),
    N.callout(
        "When to recognize BFS Level Order: problem asks for per-level aggregation (average, max, min, count), "
        "node values level by level, rightmost/leftmost node per level, connecting siblings at the same level. "
        "Signal phrases: 'each level', 'level by level', 'depth by depth'.",
        "🔎",
        "green_background",
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Level-Order technique:"),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium #102) — same skeleton, collect node values into sublists"])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal II", {"bold": True}), " (Medium #107) — same, then reverse the output"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium #199) — BFS; take the last node per level"])),
    N.bullet(N.rich([("Find Largest Value in Each Tree Row", {"bold": True}), " (Medium #515) — BFS; track max instead of sum per level"])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy #104) — count outer-loop iterations in BFS"])),
    N.bullet(N.rich([("Minimum Depth of Binary Tree", {"bold": True}), " (Easy #111) — BFS stops at first leaf node"])),
    N.bullet(N.rich([("Populating Next Right Pointers", {"bold": True}), " (Medium #116/#117) — BFS; connect same-level nodes"])),
    N.bullet(N.rich([("N-ary Tree Level Order Traversal", {"bold": True}), " (Medium #429) — same pattern, enqueue all children not just left/right"])),
    N.para("These problems share the same core technique: snapshot level_size before the inner BFS loop."),
    N.divider(),
]

# ── Interactive Visual Explainer embed ───────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the BFS algorithm visually — use Next/Prev or arrow keys. "
         "Watch the queue, level_size snapshot, running sum, and result array update in real time.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
