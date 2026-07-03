import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8122-b3ae-e02cfa4c4ccf"
SLUG = "populating_next_right_pointers_in_each_node"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=116,
    pattern="Trees",
    subpatterns=["Level Order + Link Siblings"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Use already-linked level-i next pointers as a free linked list to wire level i+1 with O(1) space.",
    icon="🟡"
)
print("Properties set OK")

# 2) Wipe old body
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks")

# 3) Build body
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The tree is defined as:\n\n"),
        ("struct Node {\n  int val;\n  Node *left;\n  Node *right;\n  Node *next;\n}", {"code": True}),
        ("\n\nPopulate each node's ", {}),
        ("next", {"code": True}),
        (" pointer to point to its next right node. If there is no next right node, the ", {}),
        ("next", {"code": True}),
        (" pointer should be set to ", {}),
        ("null", {"code": True}),
        (" (the default). Return the root of the modified tree. Solve in O(1) extra space.", {})
    ])),
    N.divider()
]

# ── Solution 1 — BFS Queue ──
blocks += [
    N.h2("Solution 1 — BFS Queue (Interview Starting Point)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to link each node to its right neighbor on the same level. 'Same level' is exactly what BFS (level-order traversal) gives us — all nodes at the same depth are processed together."),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS doesn't group nodes by level — it goes deep first. We could track depth in a hash map, but that still requires O(n) storage and extra bookkeeping. BFS naturally groups by level."),
        N.h4("The Key Observation"),
        N.para("If we process nodes in BFS order and know how many belong to the current level (snapshot size = len(queue) before the inner loop), then for every node except the last in that level, q[0] (the front of the queue) is exactly the next right neighbor."),
        N.h4("Building the Solution"),
        N.para("1. Seed queue with root.\n2. Outer while loop: snapshot size = len(q).\n3. Inner for i in range(size): dequeue node. If i < size-1: node.next = q[0]. Enqueue left and right children.\n4. Repeat."),
        N.callout("Analogy: Imagine standing in a row of people (one level of the tree). Each person passes a 'next' tag to the person immediately to their right. The last person in the row keeps their tag blank (null).", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code("""from collections import deque

def connect(root):
    if not root:
        return None
    q = deque([root])
    while q:
        size = len(q)           # snapshot: nodes at THIS level
        for i in range(size):
            node = q.popleft()
            if i < size - 1:    # not the last node in this level?
                node.next = q[0]  # wire to the next node in queue
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return root"""),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque([root])", {"code": True}), (" — Seed the queue with root. deque gives O(1) popleft.")])),
    N.para(N.rich([("size = len(q)", {"code": True}), (" — Snapshot the number of nodes at the current level BEFORE we start adding children. Critical: without this snapshot we'd mix levels.")])),
    N.para(N.rich([("for i in range(size)", {"code": True}), (" — Process exactly size nodes, all belonging to this level.")])),
    N.para(N.rich([("if i < size - 1: node.next = q[0]", {"code": True}), (" — If this isn't the rightmost node of the level, q[0] is the next peer. Set next. The last node's next stays null.")])),
    N.para(N.rich([("q.append(node.left/right)", {"code": True}), (" — Enqueue children for the next level in left-to-right order.")])),
    N.divider()
]

# ── Solution 2 — O(1) Space ──
blocks += [
    N.h2("Solution 2 — O(1) Space Iteration (Optimal)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The BFS queue works but uses O(n) space. Can we exploit the structure we're building? After we link level i, those next pointers form a free linked list — we can traverse level i without any auxiliary storage."),
        N.h4("What Doesn't Work"),
        N.para("We can't drop the queue immediately — we still need to traverse each level. The question is: can we traverse level i using the pointers we've already set, rather than a queue?"),
        N.h4("The Key Observation"),
        N.para("YES. Once level i is fully linked, we can walk it via curr = curr.next. From each curr, we can reach curr.left and curr.right (the children on level i+1). So: walk level i, wire level i+1's next pointers as we go."),
        N.h4("Building the Solution"),
        N.para("Maintain leftmost = first node of the level whose children we're about to wire. Set curr = leftmost. Walk curr via curr.next:\n  1. curr.left.next = curr.right (same-parent link)\n  2. If curr.next: curr.right.next = curr.next.left (cross-parent link)\n  3. curr = curr.next\nWhen curr is null: leftmost = leftmost.left (drop one level down)."),
        N.callout("Key: There are exactly TWO wiring operations per node: (1) same-parent: left child -> right child, always valid. (2) cross-parent: right child -> sibling's left child, only when curr.next exists.", "🔑", "green_background")
    ]),
    N.h3("Code"),
    N.code("""def connect(root):
    if not root:
        return None
    leftmost = root           # anchor: leftmost node of level being wired
    while leftmost.left:      # stop at leaf level (no children)
        curr = leftmost
        while curr:           # walk across current level via next pointers
            # Same-parent link (always valid in perfect tree)
            curr.left.next = curr.right
            # Cross-parent link (only if sibling exists)
            if curr.next:
                curr.right.next = curr.next.left
            curr = curr.next  # advance along level
        leftmost = leftmost.left  # drop to next level
    return root"""),
    N.h3("Line by Line"),
    N.para(N.rich([("leftmost = root", {"code": True}), (" — Anchor pointer. Tracks the leftmost node of the level we're processing. Used to drop down after each level is wired.")])),
    N.para(N.rich([("while leftmost.left:", {"code": True}), (" — Continue while there are children to wire. When leftmost is a leaf node, leftmost.left is null and we stop.")])),
    N.para(N.rich([("curr = leftmost", {"code": True}), (" — Walk pointer for traversing the current level left to right via already-set next pointers.")])),
    N.para(N.rich([("curr.left.next = curr.right", {"code": True}), (" — Same-parent link: left child points to right child. Always valid since perfect tree guarantees both children exist.")])),
    N.para(N.rich([("if curr.next: curr.right.next = curr.next.left", {"code": True}), (" — Cross-parent link: curr's right child points to the left child of curr's right neighbor. This bridges different subtrees at the same level.")])),
    N.para(N.rich([("curr = curr.next", {"code": True}), (" — Advance to next node on this level. When curr becomes null, inner while exits.")])),
    N.para(N.rich([("leftmost = leftmost.left", {"code": True}), (" — Move anchor to the next level's leftmost node (always valid since leftmost.left is guaranteed by the outer while condition).")])),
    N.callout("⚠️ This O(1) approach ONLY works for perfect binary trees. For general trees (LeetCode #117), every node might have 0, 1, or 2 children — the cross-parent logic needs a dummy-head prev-pointer technique instead.", "⚠️", "yellow_background"),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Queue", "O(n)", "O(n) — queue holds up to n/2 nodes at leaf level"],
        ["O(1) Space Iteration (optimal)", "O(n)", "O(1) — only leftmost and curr pointers"],
        ["Recursive", "O(n)", "O(log n) — implicit call stack = tree height"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (BFS / Level Order)")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Level Order + Link Siblings")])),
    N.callout("When to recognize this pattern:\n• 'Connect/link nodes at the same level' → BFS\n• 'next pointer' or 'sibling pointer' in a tree → level-order thinking\n• 'Perfect binary tree' + 'O(1) space' → exploit already-set next pointers as a linked list\n• Any 'process level by level' tree problem → snapshot queue size before inner loop", "🔎", "green_background"),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Level Order + Link Siblings):"),
    N.bullet(N.rich([("Populating Next Right Pointers II", {"bold": True}), (" (Medium) — Same problem but general binary tree; use dummy-head prev-pointer trick (#117)")])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), (" (Medium) — Foundational BFS with level snapshots; collects nodes per level (#102)")])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), (" (Medium) — Take the last node from each BFS level (#199)")])),
    N.bullet(N.rich([("Maximum Width of Binary Tree", {"bold": True}), (" (Medium) — Track leftmost/rightmost index per BFS level (#662)")])),
    N.bullet(N.rich([("Find Largest Value in Each Tree Row", {"bold": True}), (" (Medium) — Track max value per BFS level (#515)")])),
    N.bullet(N.rich([("Average of Levels in Binary Tree", {"bold": True}), (" (Easy) — Compute average per BFS level (#637)")])),
    N.bullet(N.rich([("Binary Tree Zigzag Level Order Traversal", {"bold": True}), (" (Medium) — BFS with alternating direction per level (#103)")])),
    N.para("These problems share the same core technique: BFS with level snapshots, processing nodes left to right within each level."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5 (Trees → BFS: Level Order). Sub-Pattern: Level Order + Link Siblings. Source: Guide Section 5 + Analysis.", "📚", "gray_background")
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
