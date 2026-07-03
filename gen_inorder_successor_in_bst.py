"""
gen_inorder_successor_in_bst.py
Regenerate the Notion page for #285 Inorder Successor in BST — in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8106-b6b9-e57829789e7f"
SLUG = "inorder_successor_in_bst"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=285,
    pattern="Trees",
    subpatterns=["Go Right or Up-Left"],
    tc="O(h)",
    sc="O(1)",
    key_insight="Walk root-down: if node.val > p.val, record as candidate and go left; else go right. Last candidate = successor.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────
print("Wiping old page body...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary search tree and a node ", {}),
        ("p", {"code": True}),
        (" in it, return the in-order successor of ", {}),
        ("p", {"code": True}),
        (" in the BST, or ", {}),
        ("null", {"code": True}),
        (" if no such node exists. The in-order successor of a node ", {}),
        ("p", {"code": True}),
        (" is the node with the smallest key greater than ", {}),
        ("p.val", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Iterative BST Walk (Interview Pick) ─────────────────────
sol1_code = """\
def inorderSuccessor(root, p):
    successor = None          # best candidate seen so far
    node = root               # start walk at root
    while node:
        if node.val > p.val:  # valid candidate: strictly greater than p
            successor = node  # record it
            node = node.left  # go left: might find smaller valid candidate
        else:                 # node.val <= p.val: too small or is p
            node = node.right # go right: successors must be larger
    return successor          # smallest valid candidate, or None
"""

blocks += [
    N.h2("Solution 1 — Iterative BST Walk (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the smallest node with value strictly greater than p.val in a BST. In sorted order (which BST inorder gives us), this is simply the next node after p. But doing a full inorder traversal wastes time — we can use the BST structure to navigate directly."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force full inorder traversal visits every node: O(n) time, O(h) space. This completely ignores the BST property. We can do better by exploiting the fact that at every node we know exactly which subtree can contain the successor."),
        N.h4("The Key Observation"),
        N.para("At any node in the BST: if node.val > p.val, this node is a valid successor candidate, and the left subtree might have a smaller valid one. If node.val <= p.val, this node cannot be a successor, and we must go right. This gives us a root-to-leaf path traversal — O(h)."),
        N.h4("Building the Solution"),
        N.para("Walk from root. Keep a 'successor' variable for the best candidate. At each node: if node.val > p.val, record it and go left. Otherwise go right. When we fall off the tree, the recorded candidate is the answer. This handles Case A (p has right child → we traverse into it and take lefts) and Case B (no right child → we recorded an ancestor on the way down) with the same code."),
        N.callout("Analogy: Imagine you're hunting for a number in a sorted list, but you can only see one number at a time. Each time you see a number bigger than your target, write it down (it might be the answer) and look at smaller numbers to its left. Each time you see a number too small, look to the right. When you fall off the end, your last note is the answer.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("successor = None", {"code": True}), (" — Initialize best candidate as None. Updated only when we find a node with value > p.val.", {})])),
    N.para(N.rich([("node = root", {"code": True}), (" — Start our walk at the root. We'll traverse downward, never revisiting.", {})])),
    N.para(N.rich([("while node:", {"code": True}), (" — Continue while there are more nodes to examine. Terminates when we fall off the tree (reach None).", {})])),
    N.para(N.rich([("if node.val > p.val:", {"code": True}), (" — This node's value is strictly greater than p's value, so it's a valid successor candidate.", {})])),
    N.para(N.rich([("successor = node", {"code": True}), (" — Record this node as the best known answer. It replaces any previous candidate because it's smaller (we came from a left turn).", {})])),
    N.para(N.rich([("node = node.left", {"code": True}), (" — Go LEFT. The left subtree of this node contains values in range (p.val, node.val). If any exist, they're better candidates.", {})])),
    N.para(N.rich([("node = node.right", {"code": True}), (" — node.val <= p.val. Not a valid candidate. Go RIGHT to find larger values.", {})])),
    N.para(N.rich([("return successor", {"code": True}), (" — Return the best candidate found, or None if p was the largest node in the BST.", {})])),
    N.callout("Key: every time we go LEFT, we record the current node as a candidate. Every time we go RIGHT, we do not. At the end, the last recorded candidate is the minimum over all 'left-turn ancestors' of p — exactly the inorder successor.", "🔐", "blue_background"),
    N.divider(),
]

# ── Solution 2: Inorder Traversal ──────────────────────────────────────
sol2_code = """\
def inorderSuccessor(root, p):
    result = [None]
    found = [False]
    def inorder(node):
        if not node or result[0]: return   # prune once found
        inorder(node.left)                 # visit left subtree
        if found[0] and not result[0]:     # p was visited last step
            result[0] = node               # this node = successor
        if node is p:                      # use 'is' not '==' (identity)
            found[0] = True
        inorder(node.right)                # visit right subtree
    inorder(root)
    return result[0]
"""

blocks += [
    N.h2("Solution 2 — Inorder Traversal (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("BST inorder traversal visits nodes in sorted ascending order. The inorder successor of p is simply the NEXT node visited after p in this traversal."),
        N.h4("What Doesn't Work"),
        N.para("We cannot just look at p.val + 1 because BSTs have arbitrary value gaps. We must actually traverse to find the next node."),
        N.h4("The Key Observation"),
        N.para("If we do a standard DFS inorder traversal and track whether we've seen p yet, the very first node we visit AFTER p is the successor."),
        N.h4("Building the Solution"),
        N.para("Use a recursive inorder traversal. Keep a 'found' flag. When we visit p (using node is p for identity), set found = True. The next node we visit (in inorder) is the answer."),
        N.callout("Important: Use 'node is p' not 'node.val == p.val'. BSTs can have duplicate values, and we need to find the specific node p, not just any node with the same value.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("result = [None], found = [False]", {"code": True}), (" — Use mutable containers so nested function can write to them (Python closure limitation).", {})])),
    N.para(N.rich([("if not node or result[0]: return", {"code": True}), (" — Base case: prune if we're at None or already found the answer (early exit optimization).", {})])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), (" — Visit left subtree first (inorder = left, root, right).", {})])),
    N.para(N.rich([("if found[0] and not result[0]: result[0] = node", {"code": True}), (" — p was visited in the previous visit. This is the very next node in inorder — the successor!", {})])),
    N.para(N.rich([("if node is p: found[0] = True", {"code": True}), (" — Mark p as found. Critically uses 'is' (object identity) not '==' (value equality).", {})])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), (" — Visit right subtree last.", {})])),
    N.divider(),
]

# ── Complexity table ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Inorder Traversal (Brute Force)", "O(n)", "O(h)"],
        ["Iterative BST Walk (Optimal)", "O(h)", "O(1)"],
    ]),
    N.para("h = height of tree. O(log n) for balanced BST, O(n) for skewed tree. Optimal solution uses zero extra space."),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Go Right or Up-Left (BST Inorder Successor)", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks for 'smallest node greater than X in BST' or 'largest node less than X in BST'. No parent pointers given. O(h) time expected. Signals: 'inorder successor', 'inorder predecessor', 'next in BST', 'floor/ceiling in BST'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BST navigation, inorder properties):"),
    N.bullet(N.rich([("Inorder Successor in BST II", {"bold": True}), (" (Medium) — Same problem WITH parent pointers; walk right-child-leftmost or walk up until left turn (#510)", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), (" (Medium) — Inorder traversal stop at kth visit; same sorted-order BST property (#230)", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium) — Inorder gives sorted sequence; verify each < next (#98)", {})])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), (" (Medium) — next() returns inorder successor lazily using a stack (#173)", {})])),
    N.bullet(N.rich([("Closest Binary Search Tree Value", {"bold": True}), (" (Easy) — Root-down BST walk tracking nearest value; same navigation logic (#270)", {})])),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}), (" (Easy) — Foundational BST navigation: go left if smaller, right if larger (#700)", {})])),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}), (" (Medium) — BST walk to find insertion spot; same root-down decision logic (#701)", {})])),
    N.para("These problems share the core technique: exploit the BST property to navigate directly to the answer in O(h) without visiting every node."),
    N.callout("📚 Reference: Trees section of DSA_Patterns_and_SubPatterns_Guide.md — BST Property sub-patterns.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer embed ──────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
