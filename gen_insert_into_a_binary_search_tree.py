"""
Notion regeneration for: Insert into a Binary Search Tree (LeetCode #701)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c5-aef1-e8b8e8a6937e"
SLUG    = "insert_into_a_binary_search_tree"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=701,
    pattern="Trees",
    subpatterns=["Find Correct Leaf Position"],
    tc="O(h)",
    sc="O(h)",
    key_insight="BST property guides every step: smaller->left, larger->right, null->insert here. New values always become leaves.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the ", {}),
        ("root", {"code": True}),
        (" node of a binary search tree (BST) and a ", {}),
        ("value", {"code": True}),
        (" to insert into the tree. Return ", {}),
        ("the root node of the BST after the insertion", {"bold": True}),
        (". It is guaranteed that the new value does not exist in the original BST. "
         "You may return any valid BST satisfying the constraints.", {})
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Recursive BST Descent (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the one correct empty slot in the tree where the new value belongs while preserving BST order. The BST property narrows the search at every step so we never examine the whole tree."),
        N.h4("What Doesn't Work"),
        N.para("A naive brute force would scan every node to find an empty child slot, then validate BST order — O(n) time with complex checks. We don't need any of that."),
        N.h4("The Key Observation"),
        N.para("The BST invariant is a GPS: if val < node.val, the new node MUST go left (placing it in the right subtree would violate BST order). If val > node.val, it MUST go right. This eliminates exactly half the remaining tree at every step, guiding us directly to the unique insertion point."),
        N.h4("Building the Solution"),
        N.para("Define: 'given a subtree root, insert val and return the updated subtree root.' Base case: root is None -> return TreeNode(val) (slot found). Recursive case: compare val vs root.val, recurse into the correct child, assign result back, return root."),
        N.callout(
            "Analogy: BST insertion is like navigating with street signs. At every intersection the sign says 'smaller values <- left, larger values -> right.' Follow the signs until the road ends -- that's your destination.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class TreeNode:\n"
        "    def __init__(self, val=0, left=None, right=None):\n"
        "        self.val = val\n"
        "        self.left = left\n"
        "        self.right = right\n\n"
        "def insertIntoBST(root: TreeNode, val: int) -> TreeNode:\n"
        "    # Base case: empty slot found -- this is the insertion point\n"
        "    if root is None:\n"
        "        return TreeNode(val)\n"
        "    # BST property: val must live in the left subtree\n"
        "    if val < root.val:\n"
        "        root.left = insertIntoBST(root.left, val)\n"
        "    # val must live in the right subtree\n"
        "    else:\n"
        "        root.right = insertIntoBST(root.right, val)\n"
        "    # Return current root (unchanged) so parent links hold\n"
        "    return root"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if root is None:", {"code": True}), " -- Base case. When we recurse past a leaf's child pointer, root is None. This is the exact slot where val belongs."])),
    N.para(N.rich([("return TreeNode(val)", {"code": True}), " -- Create the new leaf and return it upward. The caller assigns this to its .left or .right, wiring the new node into the tree."])),
    N.para(N.rich([("if val < root.val:", {"code": True}), " -- BST comparison. If val is smaller it can only legally live in the left subtree. Going right would place it larger than root -- invalid."])),
    N.para(N.rich([("root.left = insertIntoBST(root.left, val)", {"code": True}), " -- CRITICAL: the assignment. Without it, the newly created TreeNode is returned but never attached; parent's .left stays None."])),
    N.para(N.rich([("return root", {"code": True}), " -- Return the current node unchanged. Its value didn't change -- only one child pointer was updated. This preserves all ancestor links."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Iterative BST Descent (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive approach uses O(h) call-stack space. Since we traverse only a single root-to-leaf path with no backtracking, we can replace the call stack with a simple pointer variable."),
        N.h4("What Doesn't Work"),
        N.para("The recursive version works perfectly -- this is a space optimization, not a bug fix. The recursive version is preferred in interviews for clarity."),
        N.h4("The Key Observation"),
        N.para("Unlike deletion (which may need parent information), insertion only needs to know the current node. Walk down until a null child slot is found, then attach directly. No need to remember the path above."),
        N.h4("Building the Solution"),
        N.para("Walk with a curr pointer. At each step, check if the appropriate child (left if val < curr.val, right otherwise) is None. If so, attach the new node and break. Otherwise descend. Return the original root unchanged."),
    ]),
    N.h3("Code"),
    N.code(
        "def insertIntoBST(root: TreeNode, val: int) -> TreeNode:\n"
        "    if not root:\n"
        "        return TreeNode(val)  # Empty tree\n"
        "    curr = root\n"
        "    while True:\n"
        "        if val < curr.val:\n"
        "            if curr.left is None:\n"
        "                curr.left = TreeNode(val)  # Attach and stop\n"
        "                break\n"
        "            curr = curr.left  # Keep descending\n"
        "        else:\n"
        "            if curr.right is None:\n"
        "                curr.right = TreeNode(val)  # Attach and stop\n"
        "                break\n"
        "            curr = curr.right  # Keep descending\n"
        "    return root  # Original root unchanged"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("curr = root", {"code": True}), " -- Start at root. This pointer walks down the tree without call-stack overhead."])),
    N.para(N.rich([("if curr.left is None:", {"code": True}), " -- Check the child slot BEFORE descending. If null, attach the new node and break."])),
    N.para(N.rich([("curr = curr.left", {"code": True}), " -- Descend only if the child exists. Iterative equivalent of the recursive call."])),
    N.para(N.rich([("return root", {"code": True}), " -- The original root is returned unchanged. We mutated the child pointer directly so no return-value juggling needed."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive (Interview Pick)", "O(h)", "O(h) call stack"],
        ["Iterative", "O(h)", "O(1) extra"],
    ]),
    N.para("h = height of the tree. Balanced BST: h = O(log n). Skewed (degenerate) BST: h = O(n) worst case."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Find Correct Leaf Position (BST Property)"])),
    N.callout(
        "When to recognize this pattern: Problem involves a BST + find/insert/delete a value. "
        "You can eliminate half the tree at each step using the BST invariant (left < root < right). "
        "New values always end up as leaves. Signal phrases: 'insert into BST', 'search in BST', 'valid BST'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST Guided Descent / BST Property technique:"),
    N.bullet(N.rich([("Search in a BST", {"bold": True}), " (Easy) -- Same descent, return the found node or None (#700)"])),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}), " (Medium) -- Descend to find target, handle 3 deletion cases (#450)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) -- Verify BST invariant via in-order traversal or min/max bounds (#98)"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) -- In-order traversal gives sorted sequence; return kth element (#230)"])),
    N.bullet(N.rich([("Lowest Common Ancestor of a BST", {"bold": True}), " (Medium) -- BST property enables O(h) LCA without full tree scan (#235)"])),
    N.bullet(N.rich([("Closest Binary Search Tree Value", {"bold": True}), " (Easy) -- Descend while tracking minimum absolute difference (#270)"])),
    N.para("These problems share the core insight: BST property eliminates half the tree at every comparison, achieving O(h) instead of O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md -- Section: Trees -> BST Property. Sub-Pattern: Find Correct Leaf Position.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
