"""
Notion regeneration script for:
  LeetCode #426 — Convert Binary Search Tree to Sorted Doubly Linked List
  Page ID: 39193418-809c-81f7-bee8-f7934409fd26
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f7-bee8-f7934409fd26"
SLUG    = "convert_binary_search_tree_to_sorted_doubly_linked_list"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=426,
    pattern="Trees",
    subpatterns=["In-order + Link Nodes"],
    tc="O(n)",
    sc="O(h)",
    key_insight="BST in-order traversal visits nodes in sorted order; wire prev↔node at each visit then close the circle.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Convert a BST to a sorted circular doubly linked list in-place. Reuse the tree's existing node objects — just rewire the "),
        ("left", {"code": True}),
        (" (becomes "),
        ("prev", {"code": True}),
        (") and "),
        ("right", {"code": True}),
        (" (becomes "),
        ("next", {"code": True}),
        (") pointers. The result must be sorted ascending and circular (tail.right = head, head.left = tail). Return the head (minimum node). Do not allocate new nodes."),
    ])),
    N.divider(),
]

# ── Solution 1 ──
SOL1_CODE = """\
def treeToDoublyList(root):
    if not root:
        return None
    head, prev = None, None

    def inorder(node):
        nonlocal head, prev
        if not node:
            return
        inorder(node.left)          # ① recurse left: visit smaller nodes first
        if prev is None:
            head = node             # first visit = minimum = head (set once)
        else:
            prev.right = node       # forward link: prev → node
            node.left = prev        # backward link: node ← prev
        prev = node                 # advance prev to current
        inorder(node.right)         # ③ recurse right: visit larger nodes

    inorder(root)
    head.left = prev                # close circle: head's prev → tail
    prev.right = head               # close circle: tail's next → head
    return head
"""

blocks += [
    N.h2("Solution 1 — Recursive In-Order DFS with prev Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a sorted linked list from a BST, in-place. 'Sorted' screams in-order traversal. 'In-place' means reusing the left/right pointers. The question reduces to: how do we wire nodes together as we visit them in order?"),
        N.h4("What Doesn't Work"),
        N.para("Collecting all values into an array and rebuilding wastes O(n) space. Sorting the values and creating new nodes wastes O(n) time and space. Neither uses the existing node structure."),
        N.h4("The Key Observation"),
        N.para("BST in-order traversal visits nodes in strictly ascending order. At the moment we visit node n, the immediately preceding visited node is exactly n's predecessor in sorted order. If we wire them together at that moment, we build the DLL incrementally — one link per visit."),
        N.h4("Building the Solution"),
        N.para("Track two outer pointers: head (set once, on the first/minimum node) and prev (the last node fully wired into the list). At each in-order visit: if prev is None this is the head; otherwise wire prev.right = node and node.left = prev. Advance prev. After traversal, close the circle with two assignments."),
        N.callout("Analogy: Like threading pearls on a string as you pick them up in sorted order — you connect each new pearl to the last one. At the end, connect the last pearl back to the first to make a bracelet.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return None", {"code": True}), " — Empty tree guard. No nodes to link, return None immediately."])),
    N.para(N.rich([("head, prev = None, None", {"code": True}), " — head will be set to the minimum node (once). prev tracks the last node linked into the DLL."])),
    N.para(N.rich([("nonlocal head, prev", {"code": True}), " — Allows the nested function to modify the outer head and prev variables, not create new local ones."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — Base case: null child encountered, stop recursing down this path."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Step ①: recurse into left subtree first. Ensures all smaller nodes are processed before the current node."])),
    N.para(N.rich([("if prev is None: head = node", {"code": True}), " — First node visited (the global minimum). Set head exactly once and only here."])),
    N.para(N.rich([("prev.right = node", {"code": True}), " — Wire the forward link: prev's right (next) pointer points to current node."])),
    N.para(N.rich([("node.left = prev", {"code": True}), " — Wire the backward link: current node's left (prev) pointer points back to prev."])),
    N.para(N.rich([("prev = node", {"code": True}), " — Advance prev to the current node. Restores the invariant for the next visit."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Step ③: recurse into right subtree. All larger nodes processed after current."])),
    N.para(N.rich([("head.left = prev", {"code": True}), " — After full traversal: close the circle — head's 'prev' pointer → tail (maximum node)."])),
    N.para(N.rich([("prev.right = head", {"code": True}), " — Close the circle — tail's 'next' pointer → head (minimum node). List is now circular."])),
    N.para(N.rich([("return head", {"code": True}), " — Return the minimum node. Caller can traverse the full sorted circular DLL from here."])),
    N.divider(),
]

# ── Solution 2 ──
SOL2_CODE = """\
def treeToDoublyList(root):
    \"\"\"Iterative in-order using an explicit stack. Avoids Python recursion limits.\"\"\"
    if not root:
        return None
    head, prev = None, None
    stack = []
    node = root
    while node or stack:
        # Push the entire left spine onto the stack
        while node:
            stack.append(node)
            node = node.left
        # Pop: this is the next in-order node
        node = stack.pop()
        # Process (same logic as recursive version)
        if prev is None:
            head = node
        else:
            prev.right = node
            node.left = prev
        prev = node
        # Move to right subtree (may be None, triggering another pop)
        node = node.right
    # Close the circle
    head.left = prev
    prev.right = head
    return head
"""

blocks += [
    N.h2("Solution 2 — Iterative In-Order with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal as Solution 1, but avoid recursion. For very deep/degenerate BSTs, Python's default recursion limit (~1000) can cause a RecursionError."),
        N.h4("What Doesn't Work"),
        N.para("Recursion depth proportional to tree height. For a balanced BST of n=100k, height ~17, fine. For a degenerate BST (sorted input), height = n = 100k — will hit recursion limit."),
        N.h4("The Key Observation"),
        N.para("Any recursion can be simulated with an explicit stack. In-order traversal: push the entire left spine, then pop and process, then move right. Repeating this process yields exactly in-order sequence."),
        N.h4("Building the Solution"),
        N.para("Use a stack and a node pointer. Inner while loop pushes left spine. Pop = next in-order node to process. After processing, move to right subtree. Repeat. Same linking logic and circle-close as the recursive version."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("while node or stack:", {"code": True}), " — Continue while there are unvisited nodes (node is not None) or nodes waiting on the stack."])),
    N.para(N.rich([("while node: stack.append(node); node = node.left", {"code": True}), " — Push entire left spine. This simulates the recursive descent into the left subtree."])),
    N.para(N.rich([("node = stack.pop()", {"code": True}), " — Pop the next node to process. This is the leftmost unprocessed node — the next in in-order sequence."])),
    N.para(N.rich([("node = node.right", {"code": True}), " — Move to right subtree. If None, the next iteration will pop from the stack instead."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive In-Order (Interview Pick)", "O(n)", "O(h)"],
        ["Iterative In-Order (explicit stack)", "O(n)", "O(h)"],
        ["Collect values + rebuild (naive)", "O(n)", "O(n)"],
        ["Morris In-Order (bonus)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS: In-order)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order + Link Nodes — in-order DFS traversal where each visited node is wired to its predecessor to build a linked structure in sorted order."])),
    N.callout(
        "When to recognize this pattern: (1) Problem involves a BST and requires sorted output. (2) Asks for in-place conversion of BST to linked list or array. (3) Asks to 'iterate BST in sorted order' without extra space. (4) Problem says 'reuse node pointers' — left/right already provide two pointers, same count as doubly linked list needs.",
        "🔎", "green_background"
    ),
    N.para("Note: The sub-pattern 'In-order + Link Nodes' is based on analysis. BST in-order traversal is a well-established technique; the structural relinking aspect makes this a specialized application."),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (in-order traversal + BST structural manipulation):"),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) — In-order traversal, count k steps, early exit when k reached. Same traversal, different goal. (#230)"])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium) — Lazy in-order traversal with explicit stack; next() returns next in-order value. (#173)"])),
    N.bullet(N.rich([("Increasing Order Search Tree", {"bold": True}), " (Easy) — In-order traversal, relink each node as a right-only chain (no left children). Simpler version of this problem. (#897)"])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), " (Medium) — Pre-order traversal with prev pointer; relink nodes into a right-spine singly linked list. Same pointer-reuse pattern, different traversal order. (#114)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — In-order traversal; each node must strictly exceed the previous visited node. Uses prev tracking for validation. (#98)"])),
    N.bullet(N.rich([("Balance a Binary Search Tree", {"bold": True}), " (Medium) — In-order traversal to collect sorted array, then rebuild a balanced BST. Two-step: traverse + rebuild. (#1382)"])),
    N.para("These problems all hinge on the same core insight: in-order traversal of a BST yields sorted order, and processing nodes in that order enables sorted manipulation without extra sorting."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS: Inorder sub-pattern.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the in-order traversal visually — watch the DLL grow and the circle close. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK  {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
