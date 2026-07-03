"""gen_symmetric_tree.py — Notion update for Symmetric Tree (#101)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ab-80da-dc9cb0172da5"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=101,
    pattern="Trees",
    subpatterns=["Compare Left/Right Mirrors"],
    tc="O(n)",
    sc="O(h)",
    key_insight="isMirror(L, R): cross children — L.left with R.right, L.right with R.left.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "),
        ("root", {"code": True}),
        (" of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).\n\n"),
        ("Example 1: root = [1,2,2,3,4,4,3] → True\n", {}),
        ("Example 2: root = [1,2,2,null,3,null,3] → False\n\n", {}),
        ("Constraints: The number of nodes is in [1, 1000]. Node values in [-100, 100].", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Recursive ──
sol1_code = """\
def isSymmetric(root):
    def isMirror(left, right):
        if not left and not right: return True   # both null → mirrors
        if not left or not right:  return False  # one null → asymmetric
        if left.val != right.val:  return False  # values differ → not mirrors
        outer = isMirror(left.left,  right.right)  # outer pair: crossed
        inner = isMirror(left.right, right.left)   # inner pair: crossed
        return outer and inner
    return isMirror(root.left, root.right)
"""

blocks += [
    N.h2("Solution 1 — Recursive Mirror Comparison (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of thinking 'is this whole tree symmetric?', ask a simpler question: 'are these two subtrees mirror images of each other?' Define a helper isMirror(L, R) that answers this. The full problem becomes isMirror(root.left, root.right)."),
        N.h4("What Doesn't Work"),
        N.para("Comparing the left subtree with itself rotated would require building a new tree. Serializing and reversing strings would work but is roundabout. The recursive approach exploits the tree's natural self-similar structure."),
        N.h4("The Key Observation"),
        N.para("Mirror is NOT the same as identical. For L and R to be mirrors: L.left must mirror R.right (outer pair — both point away from the axis) AND L.right must mirror R.left (inner pair — both point toward the axis). This crossing is the core insight."),
        N.h4("Building the Solution"),
        N.para("Base cases first: (None, None) → True (matching empty positions). (None, node) or (node, None) → False (structural mismatch). Then: if values differ → False. Finally: return isMirror(L.left, R.right) AND isMirror(L.right, R.left)."),
        N.callout("Analogy: Fold the tree down its center axis. Every node on the left must touch a node of equal value on the right. The outermost nodes touch the other outermost nodes; the innermost nodes touch each other.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def isSymmetric(root):", {"code": True}), " — Entry point. The root is the axis of symmetry and has no counterpart; we only compare its two children."])),
    N.para(N.rich([("def isMirror(left, right):", {"code": True}), " — Helper that checks if two subtrees are mirrors. Returns True iff the subtrees are structural and value mirrors."])),
    N.para(N.rich([("if not left and not right: return True", {"code": True}), " — Both null: matching empty positions are trivially mirrors."])),
    N.para(N.rich([("if not left or not right: return False", {"code": True}), " — Exactly one is null: structural mismatch, cannot be mirrors."])),
    N.para(N.rich([("if left.val != right.val: return False", {"code": True}), " — Both exist but different values: not mirrors."])),
    N.para(N.rich([("outer = isMirror(left.left, right.right)", {"code": True}), " — Outer pair: L's left child vs R's right child. Both face away from the axis."])),
    N.para(N.rich([("inner = isMirror(left.right, right.left)", {"code": True}), " — Inner pair: L's right child vs R's left child. Both face toward the axis."])),
    N.para(N.rich([("return outer and inner", {"code": True}), " — Both crossed pairs must mirror for this level to mirror."])),
    N.para(N.rich([("return isMirror(root.left, root.right)", {"code": True}), " — Start the check by comparing the two halves of the root."])),
    N.divider(),
]

# ── Solution 2 — Iterative BFS ──
sol2_code = """\
from collections import deque

def isSymmetric(root):
    q = deque([(root.left, root.right)])   # seed with initial mirror pair
    while q:
        L, R = q.popleft()               # dequeue one should-be-mirror pair
        if not L and not R: continue     # both null → OK
        if not L or not R: return False  # structural mismatch
        if L.val != R.val: return False  # value mismatch
        q.append((L.left, R.right))      # enqueue outer pair
        q.append((L.right, R.left))      # enqueue inner pair
    return True                          # all pairs passed
"""

blocks += [
    N.h2("Solution 2 — Iterative BFS with Queue"),
    N.toggle_h3("💡 Intuition: Why Iterative?", [
        N.h4("Reframe the Problem"),
        N.para("Same logic as the recursive approach, but we simulate the call stack explicitly using a queue of mirror-pairs."),
        N.h4("What Doesn't Work"),
        N.para("For very deep (skewed) trees, the recursive solution uses O(n) call stack depth — risk of stack overflow. The iterative approach avoids this."),
        N.h4("The Key Observation"),
        N.para("Every recursive call pops two nodes and pushes two pairs. A queue does exactly this. We maintain an invariant: every pair in the queue is a (should-be-mirror) pair."),
        N.h4("Building the Solution"),
        N.para("Seed queue with (root.left, root.right). Loop: dequeue a pair, apply same 3 checks as recursive. If all pass, enqueue children in crossed order. If queue empties without failure → True."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque([(root.left, root.right)])", {"code": True}), " — Queue seeded with the initial mirror-pair: the two halves of the root."])),
    N.para(N.rich([("L, R = q.popleft()", {"code": True}), " — Dequeue one pair that should be mirrors."])),
    N.para(N.rich([("if not L and not R: continue", {"code": True}), " — Both null: matching empty positions, no children to enqueue."])),
    N.para(N.rich([("if not L or not R: return False", {"code": True}), " — One null: structural mismatch caught immediately."])),
    N.para(N.rich([("if L.val != R.val: return False", {"code": True}), " — Values differ: not mirrors."])),
    N.para(N.rich([("q.append((L.left, R.right))", {"code": True}), " — Enqueue outer pair for future verification."])),
    N.para(N.rich([("q.append((L.right, R.left))", {"code": True}), " — Enqueue inner pair for future verification."])),
    N.para(N.rich([("return True", {"code": True}), " — Queue exhausted without any violation: tree is symmetric."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Recursive", "O(n)", "O(h) call stack", "Elegant, direct — interview pick"],
        ["Iterative BFS", "O(n)", "O(w) queue", "Better for very deep/skewed trees"],
    ]),
    N.para("n = number of nodes. h = tree height (O(log n) balanced, O(n) worst for skewed). w = max tree width (at most n/2 at the widest level for a full tree)."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Compare Left/Right Mirrors — simultaneous DFS on two subtrees with crossed child comparison."])),
    N.callout(
        "When to recognize this pattern: tree asks about left-right symmetry or equality; problem compares two subtrees simultaneously; structure is self-similar and recursive; keywords: 'mirror', 'symmetric', 'same as', 'invert'.",
        "🔎", "green_background"
    ),
    N.para("Note: 'Compare Left/Right Mirrors' is the specific sub-pattern for this problem. It is a specialization of DFS on trees where two pointers traverse the tree simultaneously. The critical technique is the crossed comparison of children."),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (simultaneous tree traversal / left-right comparison):"),
    N.bullet(N.rich([("Same Tree", {"bold": True}), " (Easy) — Are two trees structurally identical with equal values? Similar but no crossing needed (#100)"])),
    N.bullet(N.rich([("Invert Binary Tree", {"bold": True}), " (Easy) — Swap left and right at every node; produces the mirror of a tree (#226)"])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}), " (Easy) — Compare left/right heights at each node; postorder recursion (#110)"])),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy) — Recursive tree height with null base case; same skeleton (#104)"])),
    N.bullet(N.rich([("Path Sum", {"bold": True}), " (Easy) — Root-to-leaf DFS with running state; same recursive tree pattern (#112)"])),
    N.bullet(N.rich([("Subtree of Another Tree", {"bold": True}), " (Easy) — Uses isSameTree as a helper at each node — mirrors this sub-pattern (#572)"])),
    N.bullet(N.rich([("Count Complete Tree Nodes", {"bold": True}), " (Medium) — Simultaneously traverse leftmost and rightmost paths to detect completeness (#222)"])),
    N.para("These problems share the same core technique: recursive traversal that compares two tree positions simultaneously."),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("symmetric_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
