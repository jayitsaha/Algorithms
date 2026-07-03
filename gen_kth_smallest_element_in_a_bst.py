"""
gen_kth_smallest_element_in_a_bst.py
Notion IN-PLACE update for LeetCode #230: Kth Smallest Element in a BST
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f3-9c56-d88bfe7fa732"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=230,
    pattern="Trees",
    subpatterns=["In-order to K-th"],
    tc="O(H + k)",
    sc="O(H)",
    key_insight="BST in-order traversal visits nodes in sorted ascending order; stop at k-th visit.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} existing blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the root of a binary search tree and an integer ",
        ("k", {"code": True}),
        ", return the k-th smallest value (1-indexed) of all the values of the nodes in the tree.",
    ])),
    N.para("Constraints: The number of nodes in the tree is n. 1 ≤ k ≤ n ≤ 10^4. 0 ≤ Node.val ≤ 10^4."),
    N.divider(),
]

# ── Solution 1 — Iterative In-Order (Interview Pick) ──────────────────────
blocks += [
    N.h2("Solution 1 — Iterative In-Order with Early Exit (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the k-th element of the BST's values when arranged in sorted ascending order. The question becomes: can we generate the sorted sequence on-the-fly, stopping once we reach position k?"),
        N.h4("What Doesn't Work"),
        N.para("Collecting all values into a list and sorting them is O(n log n) and O(n) space — it ignores the BST structure entirely. Even collecting all values via in-order traversal (O(n) time) stores all n values when we only need k of them."),
        N.h4("The Key Observation"),
        N.para("BST in-order traversal (Left → Node → Right) visits every node in sorted ascending order. This is guaranteed by the BST invariant: all left subtree values < node.val < all right subtree values, at every level. The k-th node visited IS the k-th smallest — no sorting needed."),
        N.h4("Building the Solution"),
        N.para("Use an iterative in-order with an explicit stack. Sink left as far as possible (leftmost = smallest). Pop the smallest, decrement k. If k == 0, return immediately. Pivot right and repeat. The stack holds 'pending ancestors' we backtrack to."),
        N.callout("Analogy: Imagine the BST is a sorted list folded into a tree. Unfolding it left-to-right (in-order) reveals the sorted sequence. We stop unfolding the moment we've counted k elements.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def kthSmallest(root, k):\n"
        "    stack = []\n"
        "    curr = root\n"
        "    while curr or stack:\n"
        "        while curr:\n"
        "            stack.append(curr)\n"
        "            curr = curr.left\n"
        "        curr = stack.pop()\n"
        "        k -= 1\n"
        "        if k == 0:\n"
        "            return curr.val\n"
        "        curr = curr.right"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Explicit stack to simulate recursion call stack; holds 'pending ancestor' nodes to backtrack to."])),
    N.para(N.rich([("curr = root", {"code": True}), " — Pointer to the current node we are descending into. Starts at the root."])),
    N.para(N.rich([("while curr or stack:", {"code": True}), " — Continue while either (a) there's unexplored tree to descend, or (b) the stack has ancestors to backtrack to. Critical: NOT just 'while curr' — curr can be None temporarily."])),
    N.para(N.rich([("while curr: stack.append(curr); curr = curr.left", {"code": True}), " — Inner loop: push curr and go left. This sinks all the way to the leftmost (smallest) reachable node, saving each ancestor on the stack."])),
    N.para(N.rich([("curr = stack.pop()", {"code": True}), " — Backtrack: pop the node with no more left children. This is the next smallest unvisited node in the entire tree."])),
    N.para(N.rich([("k -= 1", {"code": True}), " — Visit this node. Decrement the countdown. When k reaches 0, we've counted to the k-th smallest."])),
    N.para(N.rich([("if k == 0: return curr.val", {"code": True}), " — Early exit. Return the k-th node's value immediately. Nodes not yet visited (larger values) are ignored."])),
    N.para(N.rich([("curr = curr.right", {"code": True}), " — Pivot right. The right subtree contains values larger than curr. Go back to the outer loop and sink left into the right subtree next."])),
    N.divider(),
]

# ── Solution 2 — Recursive In-Order ───────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive In-Order (Cleaner to Derive, Same Complexity)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive formulation directly mirrors the mathematical definition of in-order traversal: inorder(left) → process root → inorder(right). A shared mutable counter tracks progress."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without a mutable counter cannot easily short-circuit (early exit) without exceptions or nonlocal variables. Python's call stack also has depth limits for highly skewed BSTs."),
        N.h4("The Key Observation"),
        N.para("If we store k and the result as instance variables (or in a nonlocal closure), each recursive call can check if we've already found the answer and skip further traversal. This is a clean early-exit mechanism for recursion."),
        N.h4("Building the Solution"),
        N.para("Define a nested inorder function. Use self.k (mutable) as the countdown. When self.k reaches 0, store self.result. The 'if self.result is not None: return' guard short-circuits remaining calls."),
    ]),
    N.h3("Code"),
    N.code(
        "def kthSmallest(root, k):\n"
        "    self.k = k\n"
        "    self.result = None\n"
        "    def inorder(node):\n"
        "        if not node or self.result is not None:\n"
        "            return\n"
        "        inorder(node.left)\n"
        "        self.k -= 1\n"
        "        if self.k == 0:\n"
        "            self.result = node.val\n"
        "            return\n"
        "        inorder(node.right)\n"
        "    inorder(root)\n"
        "    return self.result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.k = k; self.result = None", {"code": True}), " — Shared mutable state across all recursive calls. Python nonlocal or class instance attributes enable this."])),
    N.para(N.rich([("if not node or self.result is not None: return", {"code": True}), " — Base case: null node (leaf's child), OR we already found the answer — skip the entire remaining subtree."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Recurse left first (in-order: L → Root → R). Smaller values are visited before the current node."])),
    N.para(N.rich([("self.k -= 1; if self.k == 0: self.result = node.val; return", {"code": True}), " — Process (visit) this node. If countdown reaches zero, record the answer and return."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Recurse right. Only reached if we haven't found the answer yet (the guard at the top will short-circuit it otherwise)."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force — Collect + Sort", "O(n log n)", "O(n)", "Ignores BST structure"],
        ["Collect In-order Array", "O(n)", "O(n)", "Stores all values; no early exit"],
        ["Iterative In-order (optimal)", "O(H + k)", "O(H)", "Interview pick; true early exit"],
        ["Recursive In-order", "O(H + k)", "O(H)", "Same complexity; cleaner to derive"],
        ["Augmented BST (follow-up)", "O(H)", "O(n)", "Best for frequent queries + mutations"],
    ]),
    N.para("H = tree height = O(log n) for balanced BST, O(n) for worst-case skewed tree. k ≤ n always."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order to K-th (DFS Inorder + early exit counter)"])),
    N.callout(
        "When to recognize this pattern: BST + 'find k-th smallest/largest', "
        "BST + 'find values in a sorted range', BST + 'convert to sorted output', "
        "BST + 'validate sorted property'. Any time the problem exploits BST's intrinsic sorted structure.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (in-order traversal of a BST):"),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium) — Implement next()/hasNext() using the exact same iterative in-order stack technique (#173)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — In-order traversal must produce strictly increasing sequence to validate the BST property (#98)"])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}), " (Medium) — Reverse in-order (R→Root→L) with a running cumulative sum; same traversal framework (#538)"])),
    N.bullet(N.rich([("Range Sum of BST", {"bold": True}), " (Easy) — In-order with left/right subtree pruning based on range boundaries (#938)"])),
    N.bullet(N.rich([("Minimum Absolute Difference in BST", {"bold": True}), " (Easy) — In-order gives sorted sequence; track difference between consecutively visited values (#530)"])),
    N.bullet(N.rich([("Find Mode in Binary Search Tree", {"bold": True}), " (Easy) — In-order lets you count consecutive equal values without extra storage (#501)"])),
    N.para("These problems all exploit the BST in-order = sorted property. Master the iterative stack pattern and you solve all of them."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, DFS Inorder sub-pattern.", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("kth_smallest_element_in_a_bst")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
