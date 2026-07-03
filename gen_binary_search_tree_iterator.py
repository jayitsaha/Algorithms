"""
gen_binary_search_tree_iterator.py
Notion update for: Binary Search Tree Iterator (#173, Medium)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813f-b2a6-c9baf5fe9eee"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=173,
    pattern="Trees",
    subpatterns=["Controlled In-order Stack"],
    tc="O(1) amortized",
    sc="O(h)",
    key_insight="Maintain the left spine in a stack; top is always the next smallest node.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement the ", {}),
        ("BSTIterator", {"code": True}),
        (" class for a BST. The constructor takes the ", {}),
        ("root", {"code": True}),
        (" of a BST. ", {}),
        ("next()", {"code": True}),
        (" returns the next smallest integer. ", {}),
        ("hasNext()", {"code": True}),
        (" returns whether there is a next smallest number. Both must run in O(1) average time and use O(h) extra space, where h is the tree height.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Controlled In-order Stack ────────────────────────────────
blocks += [
    N.h2("Solution 1 — Controlled In-order Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a lazy iterator that yields BST values in ascending order one at a time, using only O(h) memory. In-order traversal (Left → Root → Right) of a BST naturally produces ascending order — so we need to simulate in-order traversal on demand."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: traverse the whole BST at __init__, store all values in a list, use an index. This is O(n) space — violates the constraint. We can't hold all n values at once."),
        N.h4("The Key Observation"),
        N.para("In in-order traversal, the next smallest node is always the leftmost reachable node from the current position. We can maintain this 'frontier' as a stack holding the left spine — the path from the current subtree root down to its deepest left descendant. The top of the stack is always the next value."),
        N.h4("Building the Solution"),
        N.para("Step 1: At init, push the left spine starting from root. Stack top = global minimum. Step 2: next() pops the top (the minimum), then pushes the left spine of its right child. Step 3: hasNext() checks if the stack is non-empty. Each node is pushed once and popped once → O(n) total, O(1) amortized."),
        N.callout("Analogy: Think of in-order traversal as reading a book from front to back. The stack holds your 'bookmarks' — the chapter headings (spine nodes) that tell you where to continue after finishing the current page (current node). When you finish reading a left section, you move to the chapter header, then bookmark its right subsections.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stack = []", {"code": True}), (" — Explicit stack replaces the implicit call stack of recursive in-order DFS.", {})])),
    N.para(N.rich([("self._push_left(root)", {"code": True}), (" — Load the initial left spine: push root and every left descendant until None. Stack top = global minimum.", {})])),
    N.para(N.rich([("while node:", {"code": True}), (" — Stop when we reach None (leaf's left child = None). This terminates the spine traversal.", {})])),
    N.para(N.rich([("self.stack.append(node)", {"code": True}), (" — Mark this node as 'pending' in the in-order traversal. It will be popped when all its left descendants have been visited.", {})])),
    N.para(N.rich([("node = node.left", {"code": True}), (" — Always go left to find the minimum of this subtree.", {})])),
    N.para(N.rich([("return len(self.stack) > 0", {"code": True}), (" — Non-empty stack means more nodes remain to be visited. O(1).", {})])),
    N.para(N.rich([("node = self.stack.pop()", {"code": True}), (" — Pop the top = the next smallest node. This simulates visiting the Node in Left→Node→Right.", {})])),
    N.para(N.rich([("self._push_left(node.right)", {"code": True}), (" — Now recurse right: push the left spine of the right subtree. This sets up the next frontier. If node.right is None, nothing is pushed.", {})])),
    N.para(N.rich([("return node.val", {"code": True}), (" — Return the value. Guaranteed ascending because we always pop the minimum first.", {})])),
    N.divider(),
]

# ── Solution 2 — Flatten List ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Flatten BST to List at Init"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If space were not a concern, the simplest approach is to do a full in-order traversal once at construction time and store all values in a sorted list. Then hasNext and next become trivial index operations."),
        N.h4("What Doesn't Work"),
        N.para("This uses O(n) space — forbidden by the problem's O(h) constraint. If the tree has 10 million nodes, we store 10 million values in memory. It also defeats the purpose of a lazy iterator: even if the caller only needs the first 5 values, we've already computed all n."),
        N.h4("The Key Observation"),
        N.para("This approach is correct but suboptimal. It's a valuable baseline to propose first in interviews to show you understand the problem, then optimize to the controlled stack approach."),
        N.h4("Building the Solution"),
        N.para("Run standard recursive in-order DFS and collect all values into a list. Use an index pointer for next() and hasNext(). Total: O(n) init, O(1) per operation, O(n) space."),
    ]),
    N.h3("Code"),
    N.code("""\
class BSTIterator:
    def __init__(self, root):
        self.vals = []
        self.idx = 0
        self._inorder(root)

    def _inorder(self, node):
        if not node:
            return
        self._inorder(node.left)
        self.vals.append(node.val)
        self._inorder(node.right)

    def hasNext(self) -> bool:
        return self.idx < len(self.vals)

    def next(self) -> int:
        val = self.vals[self.idx]
        self.idx += 1
        return val
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.vals = []; self.idx = 0", {"code": True}), (" — Store all values and a pointer. O(n) memory allocated upfront.", {})])),
    N.para(N.rich([("self._inorder(root)", {"code": True}), (" — Run full in-order traversal. Visits all n nodes, appending to vals.", {})])),
    N.para(N.rich([("return self.idx < len(self.vals)", {"code": True}), (" — Simple bounds check. O(1).", {})])),
    N.para(N.rich([("self.idx += 1", {"code": True}), (" — Advance the pointer after each call. O(1).", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",             "Init",  "hasNext", "next (amortized)", "Space"],
        ["Flatten to List",      "O(n)",  "O(1)",    "O(1)",             "O(n)"],
        ["Controlled Stack ✓",  "O(h)",  "O(1)",    "O(1)",             "O(h)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Controlled In-order Stack", {}), (" (lazy iterator variant of DFS: Inorder — simulates in-order traversal with an explicit stack, producing one value at a time in O(h) space)", {})])),
    N.callout(
        "When to recognize this pattern: BST + 'next smallest' + iterator interface + O(h) space constraint. Also: 'lazy evaluation' of traversal, 'pause and resume' traversal semantics. Any time you need to iterate a tree one node at a time without materializing the full traversal.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (controlled in-order stack / BST traversal):"),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), (" (Medium) — Call next() k times on this exact iterator. O(h) space, O(k) time. #230", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium) — In-order must produce strictly increasing sequence; same traversal logic. #98", {})])),
    N.bullet(N.rich([("Inorder Successor in BST", {"bold": True}), (" (Medium) — Find the node after p in in-order; essentially one step of this iterator. #285", {})])),
    N.bullet(N.rich([("All Elements in Two Binary Search Trees", {"bold": True}), (" (Medium) — Run two BSTIterators simultaneously and merge (two-pointer merge). #1305", {})])),
    N.bullet(N.rich([("Two Sum IV — Input is a BST", {"bold": True}), (" (Easy) — Use forward + backward BST iterators to find a pair summing to target. #653", {})])),
    N.bullet(N.rich([("Closest BST Value II", {"bold": True}), (" (Hard) — Maintain predecessor and successor stacks simultaneously to find k closest values. #272", {})])),
    N.para("These problems share the core technique: simulating in-order (or reverse in-order) traversal with an explicit stack that holds the current left (or right) spine."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS: Inorder sub-pattern. Controlled In-order Stack is a lazy iterator specialization.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("binary_search_tree_iterator")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
