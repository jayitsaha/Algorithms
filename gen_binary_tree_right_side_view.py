"""
gen_binary_tree_right_side_view.py
Notion IN-PLACE update for: Binary Tree Right Side View (#199)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c8-b8ad-fa30f94807e3"
SLUG    = "binary_tree_right_side_view"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 199,
    pattern     = "Trees",
    subpatterns = ["BFS: Level Order", "Last Node Each Level"],
    tc          = "O(n)",
    sc          = "O(w) — max width of tree",
    key_insight = "BFS level order: last node dequeued at each depth is the rightmost visible node.",
    icon        = "🟡",
)
print("properties OK")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"wiped {wiped} blocks")

# ── 3. Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, imagine yourself standing on the right side of it. "
         "Return the values of the nodes you can see ordered from top to bottom. "
         "Each visible node is the rightmost node at its depth level.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: BFS Level Order ─────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS Level Order (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Standing to the right means you see exactly one node per level — the rightmost one. "
               "The problem reduces to: 'traverse the tree level by level and collect the last node at each level.'"),
        N.h4("What Doesn't Work"),
        N.para("Simply following right-child pointers until null misses cases where a node has only a "
               "left child. For example: if node 3 has no right child but node 2 (its left sibling) has "
               "a right child node 5, then node 5 IS visible — a pure right-pointer traversal would miss it entirely."),
        N.h4("The Key Observation"),
        N.para("BFS processes nodes level by level, left to right (because children are enqueued left-first, right-second). "
               "The last node dequeued within each level group is always the rightmost at that depth."),
        N.h4("Building the Solution"),
        N.para("Use a deque. Seed with root. Outer loop = one level. Snapshot level_size = len(q) before inner loop. "
               "Inner loop: dequeue level_size nodes, enqueue their children. After inner loop: node = last dequeued = rightmost. "
               "Append node.val to result."),
        N.callout(
            "Analogy: Imagine photographing each row of a stadium from the right side — "
            "you always capture the person at the far right end of each row. BFS gives you each row; "
            "level_size snapshot isolates it.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def rightSideView(root):\n"
        "    if not root:\n"
        "        return []\n"
        "    q = deque([root])\n"
        "    result = []\n"
        "    while q:\n"
        "        level_size = len(q)          # snapshot: nodes at current depth\n"
        "        for _ in range(level_size):\n"
        "            node = q.popleft()        # FIFO dequeue\n"
        "            if node.left:\n"
        "                q.append(node.left)\n"
        "            if node.right:\n"
        "                q.append(node.right)\n"
        "        result.append(node.val)      # last dequeued = rightmost\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}),
                   (" — import the deque class for O(1) popleft", {})])),
    N.para(N.rich([("if not root: return []", {"code": True}),
                   (" — null tree has no visible nodes", {})])),
    N.para(N.rich([("q = deque([root])", {"code": True}),
                   (" — seed BFS queue with just the root", {})])),
    N.para(N.rich([("level_size = len(q)", {"code": True}),
                   (" — CRITICAL snapshot: captures how many nodes belong to this level, "
                    "before children are enqueued", {})])),
    N.para(N.rich([("for _ in range(level_size):", {"code": True}),
                   (" — loop exactly current-level count times (not more, not less)", {})])),
    N.para(N.rich([("node = q.popleft()", {"code": True}),
                   (" — FIFO dequeue; leftmost of this level goes first", {})])),
    N.para(N.rich([("if node.left: q.append(node.left)", {"code": True}),
                   (" — enqueue left child for the next level (left before right preserves order)", {})])),
    N.para(N.rich([("if node.right: q.append(node.right)", {"code": True}),
                   (" — enqueue right child; enqueued after left so it comes later", {})])),
    N.para(N.rich([("result.append(node.val)", {"code": True}),
                   (" — outside the inner for-loop: node is the LAST dequeued at this depth = rightmost", {})])),
    N.divider(),
]

# ── Solution 2: DFS Right-First ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS Right-First (Recursive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we always visit the right subtree before the left subtree, then at any given depth, "
               "the first node we encounter is the rightmost one."),
        N.h4("What Doesn't Work"),
        N.para("Standard preorder DFS (left before right) would give the leftmost node first at each depth — "
               "we'd need to overwrite, not just append."),
        N.h4("The Key Observation"),
        N.para("depth == len(result) is True exactly once per depth level: on the very first visit. "
               "Going right-first guarantees that first visit is the rightmost node."),
        N.h4("Building the Solution"),
        N.para("Define dfs(node, depth). If node is null, return. "
               "If depth == len(result): this is the first visit at this depth — append node.val. "
               "Then recurse right (depth+1) then left (depth+1)."),
    ]),
    N.h3("Code"),
    N.code(
        "def rightSideView(root):\n"
        "    result = []\n"
        "    def dfs(node, depth):\n"
        "        if not node:\n"
        "            return\n"
        "        if depth == len(result):     # first visit at this depth\n"
        "            result.append(node.val)  # rightmost because we go right-first\n"
        "        dfs(node.right, depth + 1)   # right subtree first\n"
        "        dfs(node.left, depth + 1)    # then left subtree\n"
        "    dfs(root, 0)\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if depth == len(result):", {"code": True}),
                   (" — len(result) equals how many depths we've already captured. "
                    "If depth equals that count, this depth hasn't been seen yet — first visit.", {})])),
    N.para(N.rich([("dfs(node.right, depth + 1)", {"code": True}),
                   (" — recurse right FIRST; guarantees right side is visited before left", {})])),
    N.para(N.rich([("dfs(node.left, depth + 1)", {"code": True}),
                   (" — left subtree is explored, but depth check prevents overwriting rightmost", {})])),
    N.divider(),
]

# ── Complexity table ─────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS Level Order (pick)", "O(n)", "O(w) max-width", "Queue holds at most one level; O(n/2) for perfect tree"],
        ["DFS Right-First", "O(n)", "O(h) height", "O(log n) balanced; O(n) skewed tree"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("BFS: Level Order, Last Node Each Level", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks for 'one value per level' or "
        "'something visible from one side' → BFS level order with level_size snapshot. "
        "Signals: 'right/left side view', 'average per level', 'maximum per level', 'zigzag traversal'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS level order technique:"),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}),
                     (" (Medium) — Collect all nodes per level, not just last (#102)", {})])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal II", {"bold": True}),
                     (" (Medium) — Same as #102 but return levels bottom-up (#107)", {})])),
    N.bullet(N.rich([("Average of Levels in Binary Tree", {"bold": True}),
                     (" (Easy) — BFS inner loop; compute average per level (#637)", {})])),
    N.bullet(N.rich([("Find Largest Value in Each Tree Row", {"bold": True}),
                     (" (Medium) — BFS inner loop; track max per level (#515)", {})])),
    N.bullet(N.rich([("Maximum Width of Binary Tree", {"bold": True}),
                     (" (Medium) — BFS with position IDs; width = rightmost - leftmost + 1 (#662)", {})])),
    N.bullet(N.rich([("Binary Tree Zigzag Level Order Traversal", {"bold": True}),
                     (" (Medium) — BFS per-level; alternate left/right append direction (#103)", {})])),
    N.para("These problems share the same BFS skeleton: outer loop = one level, inner loop = level_size nodes."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees Section · BFS: Level Order", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ─────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the BFS level-order traversal visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"total blocks: {len(blocks)}")
