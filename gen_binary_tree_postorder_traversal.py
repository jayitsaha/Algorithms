"""
gen_binary_tree_postorder_traversal.py
Notion in-place update for LeetCode #145 — Binary Tree Postorder Traversal
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81a2-bbcb-d224099b0bf4"
SLUG = "binary_tree_postorder_traversal"

print(f"[1/4] Setting page properties for {PAGE_ID} ...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=145,
    pattern="Trees",
    subpatterns=["DFS: Postorder", "Stack with Reverse"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Postorder [L,R,Root] reversed is [Root,R,L]; do that with a stack, then flip the result.",
    icon="🟢"
)
print("  Properties set.")

print("[2/4] Wiping existing page body ...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

print("[3/4] Building new page body ...")

# ── Batch 1: Problem + Solution 1 (Iterative: Stack + Reverse) ──────────────
RECURSIVE_CODE = """\
def postorderTraversal(root):
    if not root:
        return []
    left = postorderTraversal(root.left)
    right = postorderTraversal(root.right)
    return left + right + [root.val]
"""

ITERATIVE_CODE = """\
def postorderTraversal(root):
    if not root:
        return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]
"""

DEQUE_CODE = """\
from collections import deque

def postorderTraversal(root):
    if not root:
        return []
    dq, result = deque([root]), []
    while dq:
        node = dq.pop()
        result.appendleft(node.val)   # prepend instead of append
        if node.left:
            dq.append(node.left)
        if node.right:
            dq.append(node.right)
    return list(result)
"""

blocks1 = []

# Problem statement
blocks1 += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the root of a binary tree, return the postorder traversal of its nodes' values as a list of integers.\n\n"
         "Postorder traversal visits nodes in the order: "),
        ("Left subtree", {"bold": True}),
        (" → "),
        ("Right subtree", {"bold": True}),
        (" → "),
        ("Root", {"bold": True}),
        (" (root is visited last). "
         "Example: for tree [1, 2, 3, 4, 5] (root=1, left=2, right=3, 2.left=4, 2.right=5), "
         "postorder output is "),
        ("[4, 5, 2, 3, 1]", {"code": True}),
        (".")
    ])),
    N.divider(),
]

# Solution 1 — Iterative: Stack + Reverse (Interview Pick)
blocks1 += [
    N.h2("Solution 1 — Iterative: Stack + Reverse (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to collect tree node values in Left→Right→Root order. The challenge: an iterative approach must replicate what the call stack does automatically in recursion."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach of pushing right then left (like preorder) gives Root→Left→Right, not postorder. Simply reversing push order doesn't directly yield postorder."),
        N.h4("The Key Observation"),
        N.para("Postorder [L, R, Root] is the exact reverse of [Root, R, L]. And [Root, R, L] is preorder with left/right swapped — trivially done by pushing left before right on a stack (LIFO: right is processed first)."),
        N.h4("Building the Solution"),
        N.para("1. Initialize stack=[root], result=[]\n2. Pop node, append its value — this builds Root→R→L order\n3. Push left child, then push right child (right ends up on top)\n4. Repeat until stack empty\n5. Reverse the result → Left→Right→Root = postorder"),
        N.callout("Analogy: Postorder is preorder played backwards. Swap the speakers (left↔right), record the speech, then play it in reverse. You get postorder.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(ITERATIVE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return []", {"code": True}), " — Null root edge case: return empty list immediately."])),
    N.para(N.rich([("stack, result = [root], []", {"code": True}), " — Stack initialized with the root; result will collect values in Root→R→L order."])),
    N.para(N.rich([("while stack:", {"code": True}), " — Keep processing until every node has been visited."])),
    N.para(N.rich([("node = stack.pop()", {"code": True}), " — LIFO: pop the last-pushed node. This gives us the most recently added node."])),
    N.para(N.rich([("result.append(node.val)", {"code": True}), " — Collect this node's value. Order will be Root→Right→Left (pre-reversal)."])),
    N.para(N.rich([("if node.left: stack.append(node.left)", {"code": True}), " — Push left child first so it goes to the bottom of the stack."])),
    N.para(N.rich([("if node.right: stack.append(node.right)", {"code": True}), " — Push right child second — it sits on top and will be popped (processed) first. This achieves right-before-left ordering."])),
    N.para(N.rich([("return result[::-1]", {"code": True}), " — Reverse the Root→R→L list to get L→R→Root (postorder). One O(n) operation at the end."])),
    N.divider(),
]

N.append_blocks(PAGE_ID, blocks1)
print("  Batch 1 appended.")

# ── Batch 2: Solution 2 (Recursive) + Solution 3 (Deque) ─────────────────────
blocks2 = []

# Solution 2 — Recursive
blocks2 += [
    N.h2("Solution 2 — Recursive (Cleanest)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want: (postorder of left subtree) + (postorder of right subtree) + [root]. This naturally expresses as a recursive definition."),
        N.h4("What Doesn't Work"),
        N.para("A purely iterative approach without the reverse trick requires a more complex two-pass or visited-flag strategy. Recursion is simpler here."),
        N.h4("The Key Observation"),
        N.para("Postorder is self-similar: the postorder of a tree is the postorder of its left subtree, then the postorder of its right subtree, then the root. This recursive structure maps directly to code."),
        N.h4("Building the Solution"),
        N.para("Base case: null node → empty list.\nRecurse left: get full postorder of left subtree.\nRecurse right: get full postorder of right subtree.\nCombine: left + right + [root.val] (root goes last!)."),
        N.callout("Memory aid: The position of root.val in the return statement defines the traversal:\nleft + right + [root.val]  ← postorder (root last)\nleft + [root.val] + right  ← inorder (root middle)\n[root.val] + left + right  ← preorder (root first)", "🧠", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(RECURSIVE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return []", {"code": True}), " — Base case: null node contributes nothing. This terminates every branch of the recursion."])),
    N.para(N.rich([("left = postorderTraversal(root.left)", {"code": True}), " — Fully recurse into the left subtree. All of its descendants are visited before we proceed."])),
    N.para(N.rich([("right = postorderTraversal(root.right)", {"code": True}), " — Fully recurse into the right subtree."])),
    N.para(N.rich([("return left + right + [root.val]", {"code": True}), " — Combine: left subtree values, then right subtree values, then this node's value last (postorder definition)."])),
    N.divider(),
]

# Solution 3 — Deque (no reversal)
blocks2 += [
    N.h2("Solution 3 — Deque with appendleft (No Reversal Needed)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of collecting in Root→R→L and reversing, we can build the list in reverse order directly using a deque's appendleft (prepend) operation."),
        N.h4("The Key Observation"),
        N.para("appendleft inserts at the front of the deque. If we process nodes in Root→R→L order but prepend each value, the resulting list is L→R→Root. No explicit reversal needed."),
        N.h4("Building the Solution"),
        N.para("Use a deque. Pop from the right (like a stack). appendleft the value. Push right before left (so left is processed before right when popping). Result builds in postorder directly."),
    ]),
    N.h3("Code"),
    N.code(DEQUE_CODE),
    N.para("This variant avoids the final O(n) reversal by prepending to a deque. Same asymptotic complexity but slightly different constant. Useful if you want to avoid the reversal step conceptually."),
    N.divider(),
]

N.append_blocks(PAGE_ID, blocks2)
print("  Batch 2 appended.")

# ── Batch 3: Complexity + Pattern Classification + Related Problems ───────────
blocks3 = []

blocks3 += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Iterative: Stack + Reverse", "O(n)", "O(n)", "Interview pick; n for stack + result"],
        ["Recursive", "O(n)", "O(h)", "h=height; O(log n) balanced, O(n) skewed"],
        ["Deque (appendleft)", "O(n)", "O(n)", "No reversal; deque operations O(1)"],
    ]),
    N.divider(),
]

blocks3 += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS: Postorder, Stack with Reverse"])),
    N.callout(
        "When to recognize this pattern: 'Process children before their parent' → Postorder. "
        "'Delete a tree' → Postorder (free children before parent). "
        "'Evaluate expression tree' → Postorder (operands before operator). "
        "'Compute subtree aggregate bottom-up (height, size, sum)' → Postorder. "
        "Interviewer asks for iterative traversal → Stack + Reverse trick.",
        "🔎", "green_background"
    ),
    N.divider(),
]

blocks3 += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS: Postorder / Stack traversal):"),
    N.bullet(N.rich([("Binary Tree Preorder Traversal", {"bold": True}), " (Easy) — Same stack approach without reversal; push right before left (#144)"])),
    N.bullet(N.rich([("Binary Tree Inorder Traversal", {"bold": True}), " (Easy) — Stack with go-left-first loop, explicit visited tracking (#94)"])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — BFS with queue; collect per-level sublists (#102)"])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy) — Postorder DFS: height = 1 + max(L_height, R_height), computed bottom-up (#104)"])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), " (Easy) — Must compute left and right depths before updating global max at each node (#543)"])),
    N.bullet(N.rich([("Path Sum", {"bold": True}), " (Easy) — DFS traversal checking root-to-leaf path sums; return True at leaf (#112)"])),
    N.bullet(N.rich([("Delete Leaves With a Given Value", {"bold": True}), " (Medium) — Postorder essential: delete/modify children before reassigning parent pointer (#1325)"])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), " (Medium) — DFS passing current path value down, summing at leaves (#129)"])),
    N.para("These problems share the core technique of processing children before (or after, in preorder's case) the parent node."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees → DFS: Postorder. Sub-pattern verified from Guide + independent analysis.", "📚", "gray_background"),
]

# Embed section
blocks3 += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks3)
print("  Batch 3 appended.")

print("[4/4] Done!")
print(f"NOTION OK {PAGE_ID}")
