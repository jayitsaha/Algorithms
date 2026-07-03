"""
gen_convert_sorted_list_to_binary_search_tree.py
Notion page for LeetCode #109 — Convert Sorted List to Binary Search Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── 1. Create page (notion_page_id is null) ──────────────────────────────────
PAGE_ID = N.create_page(
    "Convert Sorted List to Binary Search Tree",
    109,
    "Medium",
    "🟡"
)
print(f"Created page: {PAGE_ID}")

# ── 2. Set properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=109,
    pattern="Divide and Conquer",
    subpatterns=["Find Mid + Recurse"],
    tc="O(n log n)",
    sc="O(log n)",
    key_insight="Pick the linked-list median as BST root via fast/slow pointers; sever list and recurse on each half.",
    icon="🟡"
)
print("Properties set.")

# ── 3. Build body ─────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(
        "Given the head of a singly linked list where elements are sorted in ascending order, "
        "convert it to a height-balanced binary search tree. "
        "A height-balanced BST is one where the depth of the two subtrees of every node never differs by more than one."
    ),
    N.para("Example: -10 → -3 → 0 → 5 → 9  →  BST root=0, left subtree rooted at -3 (left child -10), right subtree rooted at 9 (left child 5)."),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Find Mid + Divide & Conquer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need a balanced BST from a sorted sequence. The list is already sorted — "
            "BST property is free! We just need to pick the right root at each level to achieve balance."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Using the head node as root always produces a right-skewed unbalanced tree. "
            "We also cannot use O(1) array indexing to jump to the middle — linked lists require traversal."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The median of a sorted sequence is the perfect BST root: everything to its left is smaller, "
            "everything to its right is larger. Picking the median gives equal-sized halves, "
            "guaranteeing height balance."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Use fast/slow pointers to find the middle in O(n). "
            "Step 2: Keep a prev pointer trailing slow so we can sever the list before the middle. "
            "Step 3: Create a TreeNode from the middle value. "
            "Step 4: Recurse on the left half (head to prev) for root.left and on the right half (slow.next onward) for root.right."
        ),
        N.callout(
            "Analogy: It is like binary search on a linked list — always cut at the midpoint and recurse on both halves. "
            "The tree you build IS the binary search decision tree.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def sortedListToBST(head):\n"
        "    if not head: return None\n"
        "    if not head.next: return TreeNode(head.val)\n"
        "    slow, fast, prev = head, head, None\n"
        "    while fast and fast.next:\n"
        "        prev = slow\n"
        "        slow = slow.next\n"
        "        fast = fast.next.next\n"
        "    prev.next = None          # sever: left half is head..prev\n"
        "    root = TreeNode(slow.val) # middle becomes root\n"
        "    root.left  = sortedListToBST(head)       # recurse left\n"
        "    root.right = sortedListToBST(slow.next)  # recurse right\n"
        "    return root\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head: return None", {"code": True}), " — base case: empty sublist produces no node."])),
    N.para(N.rich([("if not head.next: return TreeNode(head.val)", {"code": True}), " — single node: wrap in a leaf and return immediately."])),
    N.para(N.rich([("slow, fast, prev = head, head, None", {"code": True}), " — initialize both pointers at head; prev trails slow by one step."])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), " — continue while fast has at least two more nodes to advance."])),
    N.para(N.rich([("prev = slow; slow = slow.next; fast = fast.next.next", {"code": True}), " — advance slow one step, fast two steps, save previous position."])),
    N.para(N.rich([("prev.next = None", {"code": True}), " — CRITICAL: sever the list so the left recursive call only sees [head..prev], not the middle or right portion."])),
    N.para(N.rich([("root = TreeNode(slow.val)", {"code": True}), " — middle element becomes the root of this subtree."])),
    N.para(N.rich([("root.left = sortedListToBST(head)", {"code": True}), " — recurse on the left half (values smaller than root)."])),
    N.para(N.rich([("root.right = sortedListToBST(slow.next)", {"code": True}), " — recurse on the right half (values larger than root)."])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Convert to Array then Recurse"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "If we could use O(1) index access to jump to the midpoint, "
            "the recursion becomes trivial. Arrays give us this — linked lists do not."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "We cannot avoid the O(n) traversal cost when finding the middle of a linked list "
            "unless we convert it to an array first."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Pay O(n) space upfront to get O(1) midpoint access forever. "
            "The recursion then mirrors 'Convert Sorted Array to BST' exactly — a simpler problem."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Traverse the list once to collect all values into a Python list. "
            "Then run a recursive helper build(lo, hi) that picks mid = (lo+hi)//2 as the root "
            "and recurses on [lo, mid-1] and [mid+1, hi]."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def sortedListToBST_v2(head):\n"
        "    nums = []\n"
        "    while head:\n"
        "        nums.append(head.val)\n"
        "        head = head.next\n"
        "    def build(lo, hi):\n"
        "        if lo > hi: return None\n"
        "        mid = (lo + hi) // 2\n"
        "        node = TreeNode(nums[mid])\n"
        "        node.left  = build(lo, mid - 1)\n"
        "        node.right = build(mid + 1, hi)\n"
        "        return node\n"
        "    return build(0, len(nums) - 1)\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("while head: nums.append(head.val); head = head.next", {"code": True}), " — flatten linked list to array in one O(n) pass."])),
    N.para(N.rich([("if lo > hi: return None", {"code": True}), " — base case: empty range produces no node."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — O(1) midpoint — the key advantage over Solution 1."])),
    N.para(N.rich([("node.left = build(lo, mid-1); node.right = build(mid+1, hi)", {"code": True}), " — recurse on each half by adjusting index bounds."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Find Mid + Recurse (interview pick)", "O(n log n)", "O(log n)"],
        ["Array + Recurse", "O(n)", "O(n)"],
    ]),
    N.para(
        "Find Mid + Recurse is preferred when space matters (no extra array). "
        "Array + Recurse is preferred when the interviewer asks for optimal time complexity."
    ),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Divide and Conquer"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Find Mid + Recurse"])),
    N.callout(
        "When to recognize this pattern: problem says 'sorted linked list to height-balanced BST'; "
        "or any problem needing to find the middle of a linked list; "
        "or 'balanced' tree construction from a sorted input.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Convert Sorted Array to BST", {"bold": True}), " (Easy) — #108: identical idea but O(1) midpoint via array indexing; no fast/slow pointer needed"])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — #876: isolates the fast/slow pointer sub-skill used in step 2 of this problem"])),
    N.bullet(N.rich([("Sort List", {"bold": True}), " (Medium) — #148: merge sort on a linked list uses find-mid + sever as the split step — identical mechanics"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — #143: find mid, reverse second half, merge — the same three building blocks in a different order"])),
    N.bullet(N.rich([("Balance a Binary Search Tree", {"bold": True}), " (Medium) — #1382: inorder traversal to array then build balanced BST; cousin of this problem"])),
    N.bullet(N.rich([("Maximum Binary Tree", {"bold": True}), " (Medium) — #654: same recursive structure — find special element, recurse on two halves"])),
    N.para("These problems all share the core technique: find a special element in a linear structure, make it the root or split point, and recurse on both sides."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 8.2 (Divide and Conquer)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("convert_sorted_list_to_binary_search_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
