"""gen_search_in_a_binary_search_tree.py — Notion rebuild for LC#700."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8165-b87b-f52c52189125"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=700,
    pattern="Trees",
    subpatterns=["Compare and Go Left/Right"],
    tc="O(h)",
    sc="O(h) recursive, O(1) iterative",
    key_insight="BST property lets us prune one entire subtree per comparison: go left if val < node, right if val > node.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the "), ("root", {"code": True}),
        (" of a binary search tree (BST) and an integer "), ("val", {"code": True}),
        (". Find and return the node in the BST such that the node's value equals "),
        ("val", {"code": True}),
        (". Return the subtree rooted at that node. If the node does not exist, return "),
        ("null", {"code": True}), (".")
    ])),
    N.divider(),
]

# ── Solution 1: Recursive ──
blocks += [
    N.h2("Solution 1 — Recursive (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find a specific value in a tree. Plain trees require checking every node (O(n)). But this is a BST — values are ordered. We want to exploit that order to skip large chunks of the tree."),
        N.h4("What Doesn't Work"),
        N.para("A plain DFS/BFS visits every node even when the target can be ruled out early. For a BST, this is wasteful — we throw away the ordering guarantee entirely."),
        N.h4("The Key Observation"),
        N.para("At any node with value v: if the target is smaller than v, it can ONLY be in the left subtree (BST property guarantees the right holds values ≥ v). If target is larger, it can only be in the right subtree. This binary elimination is exactly the same insight behind binary search on a sorted array."),
        N.h4("Building the Solution"),
        N.para("Three cases at each node: (1) null → return None (not found). (2) match → return the node. (3) smaller → recurse left. (4) larger → recurse right. Each recursive call reduces the problem to a strictly smaller subtree."),
        N.callout("Analogy: It's like searching a phone book. You open to the middle; if your name comes before the current page, tear out the right half and search the left half. Repeat. A BST is a phone-book-in-pointer form.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def searchBST(root, val):\n"
        "    if not root:           # Null: val not in this subtree\n"
        "        return None\n"
        "    if root.val == val:    # Found! Return the subtree rooted here.\n"
        "        return root\n"
        "    if val < root.val:     # Target smaller: must be LEFT\n"
        "        return searchBST(root.left, val)\n"
        "    return searchBST(root.right, val)  # Target larger: must be RIGHT",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root:", {"code": True}), " — Base case. If the current node is None (we fell off the tree), the value doesn't exist in this subtree. Return None, not False — the return type is TreeNode."])),
    N.para(N.rich([("if root.val == val:", {"code": True}), " — We found the target. Return root (the node itself), which gives the caller the entire subtree rooted here, including its children."])),
    N.para(N.rich([("if val < root.val:", {"code": True}), " — Target is smaller. BST property: every node reachable via root.right has value ≥ root.val > val. So val cannot be on the right. Recurse left only."])),
    N.para(N.rich([("return searchBST(root.right, val)", {"code": True}), " — Implicit else: val > root.val. BST property: every node reachable via root.left has value ≤ root.val < val. Recurse right only."])),
    N.divider(),
]

# ── Solution 2: Iterative ──
blocks += [
    N.h2("Solution 2 — Iterative (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive solution uses O(h) call-stack space — one frame per level traversed. For a degenerate BST (n=1,000,000 sorted values), that is 1M stack frames, which overflows the call stack."),
        N.h4("What Doesn't Work"),
        N.para("Adding memoization or tail-call optimization doesn't help in Python (no TCO). We need a fundamentally iterative design."),
        N.h4("The Key Observation"),
        N.para("The recursive solution never needs to backtrack — at each step there is only ONE direction to go (left or right, never both). This makes it a perfect candidate for iteration: replace the call stack with a single moving pointer curr."),
        N.h4("Building the Solution"),
        N.para("Start curr = root. Loop while curr is not null: compare curr.val with val, either return, move left, or move right. When the loop exits naturally (curr became null), return None."),
        N.callout("Pattern: Any tail-recursive function where there is only one recursive call per branch (not two) can be mechanically converted to a while-loop by turning 'curr = curr.left' into the loop's body.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def searchBST(root, val):\n"
        "    curr = root                # Start at root\n"
        "    while curr:                # Stop when curr is None (not found)\n"
        "        if curr.val == val:    # Match — return this subtree\n"
        "            return curr\n"
        "        elif val < curr.val:   # Go left: right side provably useless\n"
        "            curr = curr.left\n"
        "        else:                  # Go right: left side provably useless\n"
        "            curr = curr.right\n"
        "    return None                # Loop exited: value not in BST",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("curr = root", {"code": True}), " — Initialise the pointer at the root. We will move curr down the tree without using the call stack."])),
    N.para(N.rich([("while curr:", {"code": True}), " — Continue while we have a valid node. When curr becomes None, we've exhausted the relevant branch without finding val."])),
    N.para(N.rich([("if curr.val == val: return curr", {"code": True}), " — Match found. Return immediately. Same semantics as the recursive version."])),
    N.para(N.rich([("elif val < curr.val: curr = curr.left", {"code": True}), " — Move pointer left. No recursion, no stack frame. Equivalent to the recursive return searchBST(root.left, val)."])),
    N.para(N.rich([("else: curr = curr.right", {"code": True}), " — Move pointer right. Again, pointer arithmetic replaces a recursive call."])),
    N.para(N.rich([("return None", {"code": True}), " — The while loop ended because curr hit None. We traversed as far as the BST ordering could take us — val is not in the tree."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",           "Time",  "Space"],
        ["Recursive BST Search", "O(h)", "O(h)"],
        ["Iterative BST Search", "O(h)", "O(1)"],
        ["Full DFS (plain tree)", "O(n)", "O(h)"],
    ]),
    N.para(N.rich([
        ("h", {"bold": True}), (" = tree height. For a balanced BST, h = O(log n). For a degenerate (fully skewed) BST, h = O(n). Always state both cases in interviews.")
    ])),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (BST & Tries)")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Compare and Go Left/Right")])),
    N.callout(
        "When to recognise this pattern:\n"
        "• Problem explicitly says 'Binary Search Tree' (not just 'binary tree')\n"
        "• You need to find, insert, delete, or validate a specific value by magnitude\n"
        "• The key decision at each node is a three-way comparison: equal / less / greater\n"
        "• You want O(h) search instead of O(n) full scan — the ordering is the performance lever",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST traversal technique:"),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}), (" (Medium) — Navigate with same compare logic; wire new node at correct null leaf. #701")])),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}), (" (Medium) — Search for the node, then restructure using in-order successor or predecessor. #450")])),
    N.bullet(N.rich([("Closest Binary Search Tree Value", {"bold": True}), (" (Easy) — BST traversal tracking best abs(node.val − target) along the way. #270")])),
    N.bullet(N.rich([("Lowest Common Ancestor of a BST", {"bold": True}), (" (Medium) — If both p and q are smaller than root, go left; if both larger, go right; else root is LCA. #235")])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), (" (Medium) — BST ordering enforced via min/max range bounds passed through each recursive call. #98")])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), (" (Medium) — In-order traversal yields sorted sequence; count to the k-th element. #230")])),
    N.bullet(N.rich([("Range Sum of BST", {"bold": True}), (" (Easy) — Prune left subtree if all values too large; prune right if all values too small. #938")])),
    N.para("These problems all exploit the core BST invariant: left < node < right, holding recursively."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 12.1 — Binary Search Tree Operations, Sub-Pattern: Compare and Go Left/Right", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("search_in_a_binary_search_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
