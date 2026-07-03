"""
gen_binary_tree_zigzag_level_order_traversal.py
Notion update script for LeetCode #103 — Binary Tree Zigzag Level Order Traversal
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8143-a00e-d2194d14fbb5"
SLUG    = "binary_tree_zigzag_level_order_traversal"

print("Step 1: Set page properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=103,
    pattern="Trees",
    subpatterns=["BFS: Level Order"],
    tc="O(n)",
    sc="O(n)",
    key_insight="BFS with a left_to_right toggle: append on even levels, insert at 0 on odd levels.",
    icon="🟡"
)
print("  Properties set OK")

print("Step 2: Wipe existing body...")
removed = N.wipe_page(PAGE_ID)
print(f"  Removed {removed} old blocks")

print("Step 3: Rebuild page body...")
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "),
        ("root", {"code": True}),
        (" of a binary tree, return the "),
        ("zigzag level order traversal", {"bold": True}),
        (" of its nodes' values — i.e., from left to right, then right to left for the next level and alternate between."),
    ])),
    N.para("Example: tree [3, 9, 20, null, null, 15, 7] → [[3], [20, 9], [15, 7]]"),
    N.para("Constraints: number of nodes in [0, 2000], -100 ≤ node.val ≤ 100"),
    N.divider(),
]

# ── Solution 1 ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS with Direction Toggle (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is level-order traversal (BFS) with a twist: every other level must be listed in reverse. So the real question is — how do we collect each level's values in the right order without extra sorting?"),
        N.h4("What Doesn't Work"),
        N.para("A naive approach: run standard BFS to collect all levels, then go back and reverse the odd-indexed sublists. Correct, but requires a second pass and feels inelegant — we're doing extra work after the traversal."),
        N.h4("The Key Observation"),
        N.para("The BFS traversal order never changes — nodes are always dequeued left-to-right. The only difference is HOW we store each value. If we append on even levels and INSERT AT POSITION 0 on odd levels, we get the zigzag order on the fly without any reversal pass."),
        N.h4("Building the Solution"),
        N.para("1. Use a deque (not list) for O(1) popleft. 2. Snapshot level_size = len(queue) before the inner loop — this is what cleanly separates one level from the next. 3. Keep a boolean left_to_right flag. 4. After each level, flip the flag. Children are always enqueued left-then-right regardless."),
        N.callout("Analogy: Think of it like reading a book spine-first: even pages left-to-right, odd pages right-to-left. The pages don't move — only your reading direction alternates.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def zigzagLevelOrder(root):\n"
        "    if not root: return []\n"
        "    result = []\n"
        "    queue = deque([root])\n"
        "    left_to_right = True\n"
        "    while queue:\n"
        "        level_size = len(queue)   # snapshot before enqueuing children\n"
        "        level = []\n"
        "        for _ in range(level_size):\n"
        "            node = queue.popleft()\n"
        "            if left_to_right:\n"
        "                level.append(node.val)\n"
        "            else:\n"
        "                level.insert(0, node.val)\n"
        "            if node.left:  queue.append(node.left)\n"
        "            if node.right: queue.append(node.right)\n"
        "        result.append(level)\n"
        "        left_to_right = not left_to_right\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — import deque for O(1) left-pop; list.pop(0) is O(n)"])),
    N.para(N.rich([("if not root: return []", {"code": True}), " — edge case: empty tree returns empty list immediately"])),
    N.para(N.rich([("queue = deque([root])", {"code": True}), " — seed the BFS queue with the root node"])),
    N.para(N.rich([("left_to_right = True", {"code": True}), " — level 0 starts left-to-right; this flag alternates every level"])),
    N.para(N.rich([("level_size = len(queue)", {"code": True}), " — CRITICAL snapshot before the inner loop; separates current level from next"])),
    N.para(N.rich([("level = []", {"code": True}), " — fresh accumulator for this level's values"])),
    N.para(N.rich([("node = queue.popleft()", {"code": True}), " — O(1) deque pop from the front of the queue"])),
    N.para(N.rich([("level.append(node.val)", {"code": True}), " — even levels: append preserves left-to-right order"])),
    N.para(N.rich([("level.insert(0, node.val)", {"code": True}), " — odd levels: prepend reverses order on the fly (first popped ends at back)"])),
    N.para(N.rich([("if node.left/right: queue.append(...)", {"code": True}), " — always enqueue children left-then-right; direction toggle doesn't affect this"])),
    N.para(N.rich([("result.append(level)", {"code": True}), " — commit the completed level list to output"])),
    N.para(N.rich([("left_to_right = not left_to_right", {"code": True}), " — flip the flag for the next level"])),
    N.divider(),
]

# ── Solution 2 ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — BFS with End-of-Level Reverse"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same BFS approach, but instead of inserting at position 0 during collection, we collect the entire level in normal L→R order and reverse it in one shot at the end of each odd level."),
        N.h4("What Doesn't Work"),
        N.para("This IS the slightly simpler approach — easier to reason about because collection and ordering are decoupled. The downside is a separate reverse() call per odd level, which is still O(n) amortized."),
        N.h4("The Key Observation"),
        N.para("list.reverse() in Python is O(k) where k is the list length and happens in-place. Over all levels, the total reversal work is at most O(n). So this is still O(n) overall."),
        N.h4("Building the Solution"),
        N.para("Collect all nodes for the level into a list, extract their values, conditionally call reverse(), then append to result. Enqueue children from the collected node list."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def zigzagLevelOrder(root):\n"
        "    if not root: return []\n"
        "    result, queue, left_to_right = [], deque([root]), True\n"
        "    while queue:\n"
        "        level_size = len(queue)\n"
        "        level_nodes = [queue.popleft() for _ in range(level_size)]\n"
        "        level_vals  = [n.val for n in level_nodes]\n"
        "        if not left_to_right:\n"
        "            level_vals.reverse()   # in-place, O(k)\n"
        "        result.append(level_vals)\n"
        "        for node in level_nodes:\n"
        "            if node.left:  queue.append(node.left)\n"
        "            if node.right: queue.append(node.right)\n"
        "        left_to_right = not left_to_right\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("level_nodes = [queue.popleft() for _ in range(level_size)]", {"code": True}), " — capture all current-level nodes in one comprehension"])),
    N.para(N.rich([("level_vals = [n.val for n in level_nodes]", {"code": True}), " — extract values in L→R order (always)"])),
    N.para(N.rich([("if not left_to_right: level_vals.reverse()", {"code": True}), " — reverse in-place for R→L levels; no new list created"])),
    N.para(N.rich([("for node in level_nodes: ...", {"code": True}), " — enqueue children from captured nodes; safe because we already popped them all"])),
    N.callout("This variant is slightly easier to explain to an interviewer because collection and direction logic are cleanly separated. Solution 1 is marginally more efficient (no reverse() call).", "💡", "green_background"),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS + Toggle (insert at 0)", "O(n)", "O(n)", "One pass; insert at 0 is O(k) per call but O(n) amortized"],
        ["BFS + End Reverse", "O(n)", "O(n)", "One pass + one O(k) reverse per odd level; O(n) total"],
        ["DFS with depth tracking", "O(n)", "O(h)", "Call stack O(h); output still O(n); harder to explain zigzag order"],
    ]),
    N.callout("Space is O(n) because the BFS queue can hold up to the widest level — for a complete tree, the bottom level has ⌈n/2⌉ nodes.", "📐", "gray_background"),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Level Order (with Alternate Direction toggle)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Return nodes grouped by level' → BFS with level-size snapshot\n"
        "• 'Alternating / zigzag direction' → BFS + boolean toggle\n"
        "• 'Right side view / left side view' → BFS, take last/first per level\n"
        "• 'Sum or average at each depth' → BFS, aggregate per level batch\n"
        "• Any 'process level by level' wording on trees/graphs",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Level Order technique:"),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — same BFS, no direction toggle (#102)"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — BFS, collect last node per level (#199)"])),
    N.bullet(N.rich([("Average of Levels in Binary Tree", {"bold": True}), " (Easy) — BFS sum ÷ level_size (#637)"])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy) — BFS depth counter or DFS recursion (#104)"])),
    N.bullet(N.rich([("Populating Next Right Pointers in Each Node", {"bold": True}), " (Medium) — BFS, wire next pointers within each level (#116)"])),
    N.bullet(N.rich([("Find Bottom Left Tree Value", {"bold": True}), " (Medium) — BFS, track first node of the very last level (#513)"])),
    N.bullet(N.rich([("N-ary Tree Level Order Traversal", {"bold": True}), " (Medium) — same BFS skeleton, enqueue all children not just two (#429)"])),
    N.para("These problems all share the level-size-snapshot BFS skeleton. The zigzag variant adds only a direction toggle on top."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section: BFS: Level Order. Sub-Pattern source: Guide Trees section + Analysis.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
