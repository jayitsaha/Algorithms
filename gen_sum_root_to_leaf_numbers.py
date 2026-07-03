"""
gen_sum_root_to_leaf_numbers.py
Notion in-place rebuild for LeetCode #129 Sum Root to Leaf Numbers.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c2-a045-e77591b9f47f"

# ── 1) Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=129,
    pattern="Trees",
    subpatterns=["Pass Current Number Down"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Carry curr = curr*10 + node.val downward; return curr at each leaf — no path list needed.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree containing digits from ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("9", {"code": True}),
        (" only. Each root-to-leaf path in the tree represents a number. "
         "For example, the path ", {}),
        ("1 → 2 → 3", {"code": True}),
        (" represents the number ", {}),
        ("123", {"code": True}),
        (". Return the total sum of all root-to-leaf numbers. "
         "A leaf is a node with no children.", {})
    ])),
    N.divider()
]

# ── Solution 1 — DFS with Running Number ──
SOLN1_CODE = """\
def sumNumbers(root):
    def dfs(node, curr):
        if not node:
            return 0
        curr = curr * 10 + node.val
        if not node.left and not node.right:
            return curr
        return dfs(node.left, curr) + dfs(node.right, curr)
    return dfs(root, 0)
"""

blocks += [
    N.h2("Solution 1 — DFS with Running Number (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each root-to-leaf path spells out a decimal number, with the root digit "
               "as the most-significant digit. We want the sum of all such numbers across "
               "all leaves. The problem is really: 'traverse every root-to-leaf path and "
               "accumulate the number formed by that path.'"),
        N.h4("What Doesn't Work"),
        N.para("Storing the full path as a list at every node and joining/converting at the "
               "leaf works but costs O(n·h) space — we'd carry a growing list down every "
               "branch. Brute-force BFS with path strings has the same issue."),
        N.h4("The Key Observation"),
        N.para("We don't need the full path. As we walk one level deeper, the number "
               "formed so far transforms as: new_number = parent_number × 10 + current_digit. "
               "This is how humans build numbers digit by digit. One integer parameter "
               "is all we need to pass downward."),
        N.h4("Building the Solution"),
        N.para("Use preorder DFS (process current node before children). Pass an accumulator "
               "curr = 0 to the root call. At each node: curr = curr*10 + node.val. "
               "If it's a leaf, return curr. Otherwise return dfs(left, curr) + dfs(right, curr). "
               "The sums bubble up naturally."),
        N.callout(
            "Analogy: Reading a phone number digit by digit — you shift everything left and "
            "append the new digit. You don't write down every prefix; you just remember "
            "the running total.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOLN1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def sumNumbers(root):", {"code": True}),
                   (" — outer function, entry point for callers.", {})])),
    N.para(N.rich([("def dfs(node, curr):", {"code": True}),
                   (" — inner helper. ", {}),
                   ("curr", {"code": True}),
                   (" is the decimal integer formed by the path root → … → (exclusive of this node).", {})])),
    N.para(N.rich([("if not node: return 0", {"code": True}),
                   (" — null node (missing child) is not a valid path endpoint; contribute nothing.", {})])),
    N.para(N.rich([("curr = curr * 10 + node.val", {"code": True}),
                   (" — shift the running number left one decimal place and append this digit. "
                    "After this line, curr encodes root → … → this node inclusive.", {})])),
    N.para(N.rich([("if not node.left and not node.right:", {"code": True}),
                   (" — leaf check: a node is a leaf only when BOTH children are null.", {})])),
    N.para(N.rich([("return curr", {"code": True}),
                   (" — at a leaf, curr IS the complete root-to-leaf number. Return it.", {})])),
    N.para(N.rich([("return dfs(node.left, curr) + dfs(node.right, curr)", {"code": True}),
                   (" — internal node: sum paths through left subtree + right subtree. "
                    "Missing children return 0 via the null base case.", {})])),
    N.para(N.rich([("return dfs(root, 0)", {"code": True}),
                   (" — start with accumulator 0. First op: 0×10 + root.val = root.val. "
                    "Keeps update logic uniform at every node.", {})])),
    N.divider()
]

# ── Solution 2 — Iterative DFS ──
SOLN2_CODE = """\
def sumNumbers(root):
    if not root:
        return 0
    stack = [(root, 0)]
    total = 0
    while stack:
        node, curr = stack.pop()
        curr = curr * 10 + node.val
        if not node.left and not node.right:
            total += curr
        if node.right:
            stack.append((node.right, curr))
        if node.left:
            stack.append((node.left, curr))
    return total
"""

blocks += [
    N.h2("Solution 2 — Iterative DFS with Explicit Stack"),
    N.toggle_h3("💡 Intuition: Simulate the Call Stack Manually", [
        N.h4("Reframe the Problem"),
        N.para("Same goal as Solution 1, but we replace Python's implicit call stack with "
               "an explicit stack data structure. This avoids hitting Python's recursion "
               "limit on pathological trees with depth > 1000."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion hits Python's default ~1000-frame limit on skewed trees "
               "(a linked-list shaped tree of 10,000 nodes would crash)."),
        N.h4("The Key Observation"),
        N.para("Each stack frame in the recursive version holds exactly two things: "
               "the current node and curr. So the explicit stack stores (node, curr) "
               "pairs — a direct translation."),
        N.h4("Building the Solution"),
        N.para("Initialize stack = [(root, 0)]. On each iteration: pop a (node, curr) "
               "pair, compute curr = curr*10 + node.val, add to total if leaf, "
               "push children with the updated curr. Push right before left so "
               "left is popped first (preorder, left-to-right)."),
        N.callout("Trade-off: slightly more verbose than the recursive version "
                  "but safe for arbitrarily deep trees.", "⚖️", "gray_background")
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = [(root, 0)]", {"code": True}),
                   (" — initial stack entry: root node with accumulator 0.", {})])),
    N.para(N.rich([("node, curr = stack.pop()", {"code": True}),
                   (" — pop next node along with its inherited accumulated number.", {})])),
    N.para(N.rich([("curr = curr * 10 + node.val", {"code": True}),
                   (" — same digit-appending operation as the recursive version.", {})])),
    N.para(N.rich([("total += curr", {"code": True}),
                   (" — leaf reached; add the complete root-to-leaf number to total.", {})])),
    N.para(N.rich([("stack.append((node.right, curr))", {"code": True}),
                   (" — push right first so left is popped next (left-to-right preorder).", {})])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS with Running Number (Recursive)", "O(n)", "O(h)"],
        ["DFS with Running Number (Iterative)", "O(n)", "O(h)"],
    ]),
    N.para("h = tree height. O(log n) for balanced trees, O(n) for skewed (worst case)."),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Trees (DFS Preorder)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Pass Current Number Down", {})])),
    N.callout(
        "When to recognize this pattern: "
        "The problem involves root-to-leaf paths where each leaf's answer depends on ALL ancestor "
        "values (not just the immediate parent). You need to accumulate a value as you descend. "
        "Signal phrases: 'path forms a number', 'root-to-leaf path', 'sum of paths'. "
        "Contrast with Path Sum (subtract from target) or Binary Tree Max Path Sum (post-order, return max gain up).",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Path Sum", {"bold": True}),
                     (" (Easy, #112) — Preorder DFS; subtract from target instead of accumulating. Same skeleton.", {})])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}),
                     (" (Medium, #113) — Collect all root-to-leaf paths summing to target. Backtrack on path list.", {})])),
    N.bullet(N.rich([("Binary Tree Paths", {"bold": True}),
                     (" (Easy, #257) — Return all root-to-leaf path strings. Carry string down instead of integer.", {})])),
    N.bullet(N.rich([("Sum of Root to Leaf Binary Numbers", {"bold": True}),
                     (" (Easy, #1022) — Identical sub-pattern; replace × 10 with × 2 for binary representation.", {})])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}),
                     (" (Medium, #437) — Count any-node paths summing to target. Prefix sum + hashmap variant.", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}),
                     (" (Hard, #124) — Max sum over any node-to-node path. Post-order DFS: return max gain upward.", {})])),
    N.bullet(N.rich([("Smallest String Starting from Leaf", {"bold": True}),
                     (" (Medium, #988) — Carry path string down; compare strings at leaves.", {})])),
    N.para("These problems share the same preorder DFS skeleton: compute a value at the "
           "current node using the parent's passed-down parameter, recurse on children."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, "
              "DFS: Preorder / Path Sum sub-group.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sum_root_to_leaf_numbers")),
    N.para(N.rich([
        ("Step through the DFS traversal visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
