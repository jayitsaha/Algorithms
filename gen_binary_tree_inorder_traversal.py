"""
gen_binary_tree_inorder_traversal.py
Notion in-place update for LeetCode #94 — Binary Tree Inorder Traversal
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8131-bf42-e51db318391f"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=94,
    pattern="Trees",
    subpatterns=["DFS: Inorder"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Push left spine, pop to visit, pivot right — iterative inorder using explicit stack.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── helpers ────────────────────────────────────────────────────────────────
def lbl(code_text, explanation):
    """Rich-text paragraph: code snippet bold-coded then plain explanation."""
    return N.para(N.rich([
        (code_text, {"code": True}),
        (" — " + explanation, {}),
    ]))

# ── 3. Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(
        "Given the root of a binary tree, return the inorder traversal of its node values. "
        "Inorder traversal visits nodes in the order: Left subtree -> Root -> Right subtree."
    ),
    N.divider(),
]

# ── Solution 1: Iterative Stack ──
ITERATIVE_CODE = """\
def inorderTraversal(root):
    result, stack = [], []
    curr = root
    while curr or stack:        # stop only when both exhausted
        while curr:             # dive left as far as possible
            stack.append(curr)  # push: visit me after my left is done
            curr = curr.left
        curr = stack.pop()      # backtrack: left subtree fully processed
        result.append(curr.val) # VISIT: append to output (Left done, Root here)
        curr = curr.right       # pivot to right subtree
    return result"""

blocks += [
    N.h2("Solution 1 — Iterative Stack (Interview Pick)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to visit every node in a binary tree in Left -> Root -> Right order and "
            "collect the values. The challenge: while recursion is natural, we may be asked for "
            "an iterative solution, or the tree may be very deep."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "BFS/level-order queue doesn't produce inorder. Visiting the current node immediately "
            "on arrival breaks the ordering guarantee — we'd visit roots before finishing their "
            "left subtrees (that's preorder, not inorder)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Inorder means the leftmost node in any subtree is visited first. If we push every "
            "node along the left spine onto a stack, LIFO ordering guarantees the deepest-left "
            "node surfaces first when we pop. After visiting it and exhausting its right subtree, "
            "the next pop gives its parent — exactly what inorder requires."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Maintain curr (current node) and an explicit stack. Inner loop: push curr, go left, "
            "repeat until null. Then pop: this node's left subtree is done — visit it, then set "
            "curr = right child. Outer loop stops when curr is null AND stack is empty."
        ),
        N.callout(
            "Analogy: descend a staircase hugging the left wall, marking each step as you go. "
            "When you hit the floor (null), retrace back up (pop) one step at a time, peeking "
            "right at each landing. That's exactly what this stack simulates.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(ITERATIVE_CODE),
    N.h3("Line by Line"),
    lbl("result, stack = [], []",
        "Two lists: result accumulates output; stack holds nodes whose left subtrees are in-progress"),
    lbl("curr = root",
        "Pointer to the node currently being explored; starts at root"),
    lbl("while curr or stack:",
        "Continue while work remains — curr to explore OR stack to drain; BOTH must be empty to stop"),
    lbl("while curr:",
        "Inner loop: descend the left spine of the current subtree"),
    lbl("stack.append(curr)",
        "Push node — a promise: 'visit me after my entire left subtree is processed'"),
    lbl("curr = curr.left",
        "Go to left child; if null, inner loop exits"),
    lbl("curr = stack.pop()",
        "Backtrack: the popped node's left subtree is fully processed"),
    lbl("result.append(curr.val)",
        "VISIT: record this node's value (Left done -> Root here -> Right next)"),
    lbl("curr = curr.right",
        "Pivot to right subtree; next iteration will push its left spine"),
    lbl("return result",
        "All n nodes visited exactly once; result contains inorder sequence"),
    N.callout(
        "Warning: the outer loop condition must be 'curr or stack', NOT just 'stack'. "
        "After popping a node and setting curr = right_child, the right child is not yet pushed. "
        "Checking only stack would exit the loop prematurely while curr still points to an unprocessed node.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Recursive DFS ──
RECURSIVE_CODE = """\
def inorderTraversal(root):
    result = []
    def dfs(node):
        if not node:
            return               # base case: null node, do nothing
        dfs(node.left)           # Left: recurse into left subtree first
        result.append(node.val)  # Root: visit current node after left done
        dfs(node.right)          # Right: recurse after visiting root
    dfs(root)
    return result"""

blocks += [
    N.h2("Solution 2 — Recursive DFS (Simplest, Same Complexity)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Inorder traversal is defined recursively: "
            "inorder(node) = inorder(node.left) + [node.val] + inorder(node.right). "
            "The recursive code is a direct line-for-line translation of this definition."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "There is nothing algorithmically wrong with recursion here — it is the natural "
            "expression. The only practical downsides: (1) uses the system call stack to depth O(h), "
            "and (2) may hit Python's recursion limit (~1000 frames) on pathologically deep trees."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Python evaluates dfs(node.left) completely before executing "
            "result.append(node.val), which completes before dfs(node.right). "
            "The call stack IS the traversal stack — recursion makes this implicit."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define an inner helper that captures result via closure. "
            "Base case: null node returns immediately. Otherwise: recurse left, "
            "append current val, recurse right. Call on root, return result."
        ),
        N.callout(
            "Interview tip: write the recursive version first — it is 5 clean lines. "
            "Then offer: 'If you want iterative to avoid recursion depth limits, I can "
            "refactor to use an explicit stack.' This demonstrates you know both approaches.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(RECURSIVE_CODE),
    N.h3("Line by Line"),
    lbl("def dfs(node):",
        "Inner helper function; captures result list via Python closure — no need to pass it as a parameter"),
    lbl("if not node: return",
        "Base case: null node contributes nothing; return immediately without appending"),
    lbl("dfs(node.left)",
        "Recurse left first — Python evaluates this call to completion before moving on"),
    lbl("result.append(node.val)",
        "Visit current node AFTER its entire left subtree is done"),
    lbl("dfs(node.right)",
        "Recurse right after visiting root — right subtree processed last"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Iterative Stack (Interview Pick)", "O(n)", "O(h)", "h = tree height; explicit stack depth"],
        ["Recursive DFS", "O(n)", "O(h)", "h = system call stack depth; identical asymptotically"],
        ["Morris Traversal", "O(n)", "O(1)", "Threads tree temporarily; advanced technique"],
    ]),
    N.para(
        "h = tree height. Balanced tree: h = O(log n). "
        "Skewed tree (all left or all right children): h = O(n) — worst case space. "
        "n = total number of nodes in the tree."
    ),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (Depth-First Search)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS: Inorder — Left -> Root -> Right; for BSTs yields sorted ascending order", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "- 'BST' + 'sorted order' in the same problem -> inorder traversal\n"
        "- 'kth smallest/largest in BST' -> inorder, stop at k-th pop\n"
        "- 'validate BST' -> inorder, check each value is strictly greater than previous\n"
        "- 'BST iterator' -> lazy iterative inorder\n"
        "- Any problem where Left -> Root -> Right visit order is explicitly needed",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique (DFS: Inorder / Tree Traversal):"),
    N.bullet(N.rich([
        ("Binary Tree Preorder Traversal", {"bold": True}),
        (" (Easy) — Same iterative skeleton; append value on push instead of pop (#144)", {}),
    ])),
    N.bullet(N.rich([
        ("Binary Tree Postorder Traversal", {"bold": True}),
        (" (Easy) — Process children before parent; classic for tree deletion/cleanup (#145)", {}),
    ])),
    N.bullet(N.rich([
        ("Validate Binary Search Tree", {"bold": True}),
        (" (Medium) — Run inorder and verify each value strictly greater than previous (#98)", {}),
    ])),
    N.bullet(N.rich([
        ("Kth Smallest Element in a BST", {"bold": True}),
        (" (Medium) — Iterative inorder; decrement k on each pop and stop when k reaches 0 (#230)", {}),
    ])),
    N.bullet(N.rich([
        ("Binary Search Tree Iterator", {"bold": True}),
        (" (Medium) — next() returns the next inorder value; implement as lazy iterative inorder (#173)", {}),
    ])),
    N.bullet(N.rich([
        ("Recover Binary Search Tree", {"bold": True}),
        (" (Medium) — Two nodes swapped; find the pair where prev > curr during inorder scan (#99)", {}),
    ])),
    N.bullet(N.rich([
        ("Balance a Binary Search Tree", {"bold": True}),
        (" (Medium) — Use inorder to extract sorted list, then build balanced BST from it (#1382)", {}),
    ])),
    N.para(
        "These problems share the same core technique: inorder traversal (iterative or recursive) "
        "to access nodes in Left -> Root -> Right order, leveraging the BST sorted-order property."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section. "
        "Sub-Pattern: DFS: Inorder. Source: Guide Trees Section.",
        "📚", "gray_background"
    ),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_tree_inorder_traversal")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
