"""
gen_binary_tree_preorder_traversal.py
Regenerate the Notion page for Binary Tree Preorder Traversal (#144) in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8139-9761-deb0afc296c8"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=144,
    pattern="Trees",
    subpatterns=["DFS: Preorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Push right child before left child — LIFO ensures left-first processing in preorder.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ──────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, return the ", {}),
        ("preorder traversal", {"bold": True}),
        (" of its nodes' values. Preorder traversal visits nodes in Root → Left → Right order.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Iterative Stack (Interview Pick) ──────────────────
sol1_code = """\
def preorderTraversal(root):
    if not root:
        return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)         # PRE-order: output before children
        if node.right:
            stack.append(node.right)    # Push right FIRST (waits below left)
        if node.left:
            stack.append(node.left)     # Push left SECOND (processed first)
    return result"""

blocks += [
    N.h2("Solution 1 — Iterative Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Preorder traversal visits a node, then recursively visits its left subtree, then its right subtree. We need to collect node values in Root → Left → Right order."),

        N.h4("What Doesn't Work"),
        N.para("The naive recursive solution works but uses Python's hidden call stack. On a right-skewed tree with 10,000 nodes, each recursive call adds a stack frame — Python's default recursion limit of 1000 triggers a RecursionError. Also, concatenating lists (return [root.val] + preorder(left) + ...) creates O(n) intermediate lists, wasting memory."),

        N.h4("The Key Observation"),
        N.para("The call stack IS a stack data structure. When the runtime executes preorder recursively, it pushes a 'return address + arguments' frame for each call and pops it when the function returns. We can simulate this explicitly with a Python list used as a stack — giving us full control."),

        N.h4("Building the Solution"),
        N.para("Start: push root onto the stack. Each iteration: pop the top node (this is the current 'function call'), output its value (preorder: before children), then push its right child and then its left child. Since a stack is LIFO (last in, first out), the left child (pushed last) is popped first — guaranteeing left-before-right processing. We never push None, so no null dereference."),

        N.callout("Analogy: Think of a stack of books. You push Right, then Left on top. You pick up (pop) Left first — you read it completely (drain its subtree) before touching Right beneath it.", "🧠", "blue_background"),
    ]),

    N.h3("Code"),
    N.code(sol1_code),

    N.h3("Line by Line"),
    N.para(N.rich([("if not root:", {"code": True}), (" — edge case guard. An empty tree has no nodes to traverse; return [] immediately rather than pushing None.", {})])),
    N.para(N.rich([("stack, result = [root], []", {"code": True}), (" — initialize the explicit stack with the root node. The result list will collect preorder values.", {})])),
    N.para(N.rich([("while stack:", {"code": True}), (" — loop until every node has been popped (processed). Each node is pushed and popped exactly once.", {})])),
    N.para(N.rich([("node = stack.pop()", {"code": True}), (" — take the top item (LIFO). This is the node we will process in this iteration.", {})])),
    N.para(N.rich([("result.append(node.val)", {"code": True}), (" — PRE-order: append the value before pushing children. This is the defining preorder step.", {})])),
    N.para(N.rich([("if node.right: stack.append(node.right)", {"code": True}), (" — push right child FIRST. It waits beneath left on the stack.", {})])),
    N.para(N.rich([("if node.left: stack.append(node.left)", {"code": True}), (" — push left child SECOND. It sits on top and is popped next — ensuring left subtree drains completely before right.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — all n nodes visited exactly once. Time O(n), Space O(h).", {})])),

    N.divider(),
]

# ── Solution 2: Recursive DFS ──────────────────────────────────────
sol2_code = """\
def preorderTraversal(root):
    result = []
    def dfs(node):
        if not node:
            return
        result.append(node.val)   # PRE-order: before any recursive call
        dfs(node.left)            # Recurse entire left subtree first
        dfs(node.right)           # Then recurse entire right subtree
    dfs(root)
    return result"""

blocks += [
    N.h2("Solution 2 — Recursive DFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The preorder definition is recursive by nature: preorder(tree) = [root.val] + preorder(left) + preorder(right). We can directly encode this in code."),

        N.h4("What Doesn't Work"),
        N.para("On deeply skewed trees (like a right-skewed tree of 10,000 nodes), each recursive call adds a frame to Python's call stack. Python's default recursion limit is 1000, so this will raise RecursionError. This is why the iterative solution is preferred for production/interviews."),

        N.h4("The Key Observation"),
        N.para("The recursive structure mirrors the problem definition perfectly: at each node, append its value (pre = before), then fully process the left subtree (recurse), then fully process the right subtree (recurse). The base case is a null node — return immediately."),

        N.h4("Building the Solution"),
        N.para("Use a closure: define dfs(node) inside preorderTraversal that appends to the outer result list. Call dfs(node.left) before dfs(node.right). The call stack handles the 'waiting for left to finish before starting right' automatically."),

        N.callout("Interview note: Present this solution first (it's simpler to explain), then offer the iterative version as an improvement for deep trees.", "💡", "green_background"),
    ]),

    N.h3("Code"),
    N.code(sol2_code),

    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), (" — shared accumulator; captured by closure in dfs().", {})])),
    N.para(N.rich([("if not node: return", {"code": True}), (" — base case: null node means no value to append; unwind the recursion.", {})])),
    N.para(N.rich([("result.append(node.val)", {"code": True}), (" — PRE: append value immediately on entering this node, before any children.", {})])),
    N.para(N.rich([("dfs(node.left)", {"code": True}), (" — recurse into the entire left subtree. This call chain fully completes before the next line runs.", {})])),
    N.para(N.rich([("dfs(node.right)", {"code": True}), (" — only after left subtree is exhausted do we recurse right.", {})])),

    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Iterative Stack (Interview Pick)", "O(n)", "O(h)", "h = height; O(log n) balanced, O(n) skewed"],
        ["Recursive DFS", "O(n)", "O(h) call stack", "Same complexity; overflow risk on deep trees"],
        ["Morris Traversal", "O(n)", "O(1)", "Threads pointers; complex; rarely asked"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS: Preorder (Stack or Recursion)", {})])),
    N.callout(
        "When to recognize this pattern: problem asks for Root → Left → Right order; requires serializing a tree; needs to process a parent node before its children; collect root-to-leaf paths; clone/copy a tree structure.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS Preorder / Tree Traversal technique:"),
    N.bullet(N.rich([("Binary Tree Inorder Traversal", {"bold": True}), (" (Easy #94) — Left → Root → Right; iterative uses left-chain descent pattern", {})])),
    N.bullet(N.rich([("Binary Tree Postorder Traversal", {"bold": True}), (" (Easy #145) — Left → Right → Root; iterative trick: reversed preorder with L/R swapped", {})])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), (" (Medium #102) — BFS with a queue instead of DFS with a stack", {})])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), (" (Medium #114) — rearrange pointers in preorder sequence in-place", {})])),
    N.bullet(N.rich([("Binary Tree Paths", {"bold": True}), (" (Easy #257) — collect all root-to-leaf paths using preorder DFS with path accumulation", {})])),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Inorder Traversal", {"bold": True}), (" (Medium #105) — reconstruct tree given both traversal orders", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium #98) — inorder traversal gives sorted sequence for BST validation", {})])),
    N.para("These problems share the DFS traversal pattern; the order of output/processing relative to recursive calls determines preorder vs. inorder vs. postorder."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees → DFS: Preorder\nSub-Pattern verified: Guide + Analysis", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_tree_preorder_traversal")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ──────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
