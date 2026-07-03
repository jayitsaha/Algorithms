"""
gen_sum_of_left_leaves.py — Notion updater for LeetCode #404 Sum of Left Leaves
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8155-86d2-f24352b1f6c5"
SLUG    = "sum_of_left_leaves"

# ─── 1) Set / update properties ───────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=404,
    pattern="Trees",
    subpatterns=["Track Left Child Flag", "DFS: Postorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Pass an is_left boolean flag from parent to child; at a leaf, count its value only if the flag is True.",
    icon="🟢",
)
print("Properties set.")

# ─── 2) Wipe old thin content ──────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ─── 3) Rebuild body ──────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the sum of all left leaves.\n\nA leaf is a node with no children. A left leaf is a leaf that is the left child of its parent.", {}),
    ])),
    N.para(N.rich([
        ("Example:\n", {"bold": True}),
        ("Input: root = [3,9,20,null,null,15,7]\n"
         "Output: 24\n"
         "Explanation: 9 and 15 are left leaves. 7 is a right leaf (skipped).", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Recursive DFS with is_left flag ──
sol1_code = """\
def sumOfLeftLeaves(root):
    def dfs(node, is_left):
        if not node:
            return 0
        if not node.left and not node.right:   # leaf node
            return node.val if is_left else 0  # only left leaves count
        return (dfs(node.left,  True)          # left child: flag = True
              + dfs(node.right, False))        # right child: flag = False
    return dfs(root, False)  # root has no parent → False
"""

blocks += [
    N.h2("Solution 1 — Recursive DFS with is_left Flag (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to sum leaf values, but only for leaves that are left children. "
               "The problem reduces to: traverse every node, and whenever you land on a leaf, "
               "decide whether to count it based on which side you arrived from."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach is to inspect each node's left child: "
               "'if node.left has no children, add node.left.val.' This works but is awkward — "
               "every internal node must peek one level ahead. It also does not generalize well."),
        N.h4("The Key Observation"),
        N.para("A node cannot know if it's a left or right child — it has no pointer to its parent. "
               "But the parent always knows! When a parent makes a recursive call into its left child, "
               "it can pass True; when it recurses into its right child, it passes False. "
               "This is the 'track left child flag' pattern."),
        N.h4("Building the Solution"),
        N.para("1. Define dfs(node, is_left). "
               "2. Base case: if node is null, return 0. "
               "3. Leaf + is_left=True → return node.val. "
               "4. Leaf + is_left=False → return 0. "
               "5. Otherwise recurse: dfs(left, True) + dfs(right, False). "
               "6. Entry point: dfs(root, False) — root has no parent."),
        N.callout(
            "Analogy: Imagine a factory inspection. A supervisor walks the tree and "
            "shouts 'left side!' or 'right side!' to each worker before entering their section. "
            "Workers at the end of a corridor (leaves) count their parts only if the supervisor "
            "shouted 'left side!' on the way in.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("def dfs(node, is_left):", {"code": True}), " — inner recursive helper; is_left carries the flag from parent."])),
    N.para(N.rich([("if not node: return 0", {"code": True}), " — base case: null node contributes 0."])),
    N.para(N.rich([("if not node.left and not node.right:", {"code": True}), " — both children absent → this is a leaf."])),
    N.para(N.rich([("return node.val if is_left else 0", {"code": True}), " — count only if we arrived via a left edge."])),
    N.para(N.rich([("dfs(node.left, True)", {"code": True}), " — left child always has is_left=True by definition."])),
    N.para(N.rich([("dfs(node.right, False)", {"code": True}), " — right child always has is_left=False."])),
    N.para(N.rich([("return dfs(root, False)", {"code": True}), " — root has no parent so its flag starts as False."])),
    N.divider(),
]

# ── Solution 2 — Iterative DFS ──
sol2_code = """\
def sumOfLeftLeaves(root):
    if not root:
        return 0
    stack = [(root, False)]   # each entry: (node, is_left)
    total = 0
    while stack:
        node, is_left = stack.pop()
        if not node.left and not node.right:  # leaf
            if is_left:
                total += node.val
        else:
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, True))
    return total
"""

blocks += [
    N.h2("Solution 2 — Iterative DFS with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same idea as Solution 1, but we simulate the call stack ourselves. "
               "This avoids Python's recursion limit for extremely deep trees."),
        N.h4("What Doesn't Work"),
        N.para("Standard iterative DFS without the flag would lose the left/right context. "
               "We must store (node, is_left) pairs together."),
        N.h4("The Key Observation"),
        N.para("Any recursive DFS can be converted to iterative by replacing the call stack "
               "with an explicit stack. The key is to push tuples of all the state that the "
               "recursive function receives as parameters: (node, is_left)."),
        N.h4("Building the Solution"),
        N.para("Push (root, False) initially. Each iteration: pop (node, is_left). "
               "If leaf and is_left → add to total. Else push (right, False) then (left, True). "
               "Order matters: push right before left so left is processed first (LIFO)."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = [(root, False)]", {"code": True}), " — seed the stack with root and its False flag."])),
    N.para(N.rich([("node, is_left = stack.pop()", {"code": True}), " — unpack both pieces of state from each entry."])),
    N.para(N.rich([("if not node.left and not node.right:", {"code": True}), " — leaf detection."])),
    N.para(N.rich([("if is_left: total += node.val", {"code": True}), " — count only left leaves."])),
    N.para(N.rich([("stack.append((node.right, False))", {"code": True}), " — push right before left so left is processed first."])),
    N.para(N.rich([("stack.append((node.left, True))", {"code": True}), " — left child always gets True."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",           "Time", "Space", "Notes"],
        ["Recursive DFS + flag", "O(n)", "O(h)", "Cleanest — interview pick"],
        ["Iterative DFS + stack","O(n)", "O(h)", "Avoids recursion limit; same Big-O"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Track Left Child Flag · DFS: Postorder"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem distinguishes left vs right children or subtrees\n"
        "• You need information about how a node was reached (side, depth, path)\n"
        "• The parent has context that the node cannot derive itself\n"
        "• Any need to pass state top-down through a tree traversal",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same context-propagation-in-DFS technique:"),
    N.bullet(N.rich([("Path Sum", {"bold": True}), " (Easy) — DFS carries cumulative sum down; check target at leaf nodes (#112)"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — pass depth down; collect last node seen at each level (#199)"])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}), " (Medium) — DFS carries max-value-on-path; count nodes >= that max (#1448)"])),
    N.bullet(N.rich([("Symmetric Tree", {"bold": True}), " (Easy) — mirrored DFS compares left subtree with right subtree (#101)"])),
    N.bullet(N.rich([("Find Leaves of Binary Tree", {"bold": True}), " (Medium) — postorder DFS returns height; group nodes by height (#366)"])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), " (Medium) — DFS carries accumulated number down to each leaf (#129)"])),
    N.para("These problems all share the technique: pass parent-side context as a DFS parameter."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5: Trees\n"
              "Sub-Pattern: Track Left Child Flag (context propagation in DFS) · Source: Analysis",
              "📚", "gray_background"),
]

# ── Interactive Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
