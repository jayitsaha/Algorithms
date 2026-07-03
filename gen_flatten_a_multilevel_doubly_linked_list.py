"""
Notion updater for: Flatten a Multilevel Doubly Linked List (#430)
PAGE_ID: 39193418-809c-81a5-8ca1-cf4f83522721
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a5-8ca1-cf4f83522721"
SLUG = "flatten_a_multilevel_doubly_linked_list"

# ── 1) Set page properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=430,
    pattern="Linked List",
    subpatterns=["DFS / Stack"],
    tc="O(n)",
    sc="O(d)",
    key_insight="Use an explicit stack to save 'next' continuations when splicing child chains in DFS order; update both prev and next at every splice.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} existing blocks.")

# ── 3) Build and append new body ──────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the ", {}),
        ("head", {"code": True}),
        (" of a doubly linked list. Each node has a ", {}),
        ("prev", {"code": True}),
        (", ", {}),
        ("next", {"code": True}),
        (", and ", {}),
        ("child", {"code": True}),
        (" pointer. The ", {}),
        ("child", {"code": True}),
        (" pointer (when non-null) points to the head of another doubly linked list that may itself have children. Flatten all levels into a single-level doubly linked list in DFS (depth-first) order: when you encounter a node with a child, fully exhaust the child chain before continuing with the node's original ", {}),
        ("next", {"code": True}),
        (". All ", {}),
        ("child", {"code": True}),
        (" pointers must be cleared. Return ", {}),
        ("head", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Iterative Stack (Interview Pick) ──────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative Stack / DFS Splice (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to linearize a tree-like structure into a single chain. The 'child' pointers make nodes act like tree nodes with two children: next (right sibling) and child (left subtree in DFS terms). The output is a DFS preorder traversal of this implicit tree."),
        N.h4("What Doesn't Work"),
        N.para("A naive recursive approach that just collects all values and rebuilds the list works but uses O(n) space. We want to do the splicing in-place as we traverse, which requires tracking where to 'resume' after each child chain ends."),
        N.h4("The Key Observation"),
        N.para("When we dive into a child list, we temporarily 'pause' the main list. This is exactly DFS: push the continuation (curr.next) onto a stack, process the child chain entirely, then pop the continuation when the child chain ends (curr.next becomes None)."),
        N.h4("Building the Solution"),
        N.para("Walk curr through the list. When curr.child is found: push curr.next (if not None) to save it, redirect curr.next = curr.child, set child.prev = curr, clear child. When curr.next is None and stack non-empty: pop and reattach, setting the prev pointer too."),
        N.callout(
            "Analogy: Imagine reading a book with footnotes. When you hit a footnote marker, you jump to the footnotes section (push bookmark), read until footnote ends, then return to where you left off (pop bookmark). The stack is your list of bookmarks.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def flatten(head):\n"
        "    if not head:\n"
        "        return None\n"
        "    curr = head\n"
        "    stack = []  # saves paused 'next' continuations\n"
        "    while curr:\n"
        "        if curr.child:\n"
        "            # Save the 'right side' before diving into child\n"
        "            if curr.next:\n"
        "                stack.append(curr.next)\n"
        "            # Splice: wire curr -> child head\n"
        "            curr.next = curr.child\n"
        "            curr.child.prev = curr  # doubly linked!\n"
        "            curr.child = None       # clear child pointer\n"
        "        # At tail of a sub-list with saved continuations: rejoin\n"
        "        if not curr.next and stack:\n"
        "            top = stack.pop()\n"
        "            curr.next = top\n"
        "            top.prev = curr  # doubly linked!\n"
        "        curr = curr.next\n"
        "    return head",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head:", {"code": True}), " — edge case: empty list returns None immediately."])),
    N.para(N.rich([("curr = head; stack = []", {"code": True}), " — walking pointer starts at head; stack will hold saved 'next' pointers for each open sub-list level."])),
    N.para(N.rich([("while curr:", {"code": True}), " — visit every node exactly once; loop exits when curr reaches None."])),
    N.para(N.rich([("if curr.child:", {"code": True}), " — check if this node opens a new sub-list that must be spliced in."])),
    N.para(N.rich([("if curr.next: stack.append(curr.next)", {"code": True}), " — only push if right-side exists; pushing None would cause null-pointer bugs later."])),
    N.para(N.rich([("curr.next = curr.child", {"code": True}), " — splice: redirect the forward link to the child head."])),
    N.para(N.rich([("curr.child.prev = curr", {"code": True}), " — fix the backward pointer; this is a doubly linked list."])),
    N.para(N.rich([("curr.child = None", {"code": True}), " — the problem requires clearing all child pointers in the result."])),
    N.para(N.rich([("if not curr.next and stack:", {"code": True}), " — reached the tail of a sub-list with saved continuations to rejoin."])),
    N.para(N.rich([("top = stack.pop(); curr.next = top; top.prev = curr", {"code": True}), " — pop the saved node and wire it in; update both forward and backward links."])),
    N.para(N.rich([("curr = curr.next", {"code": True}), " — advance to the next node (which may be the newly spliced child head or the newly rejoined continuation)."])),
    N.divider(),
]

# ── Solution 2: Recursive ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive DFS (Elegant Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive insight: to flatten a list, walk it. When you find a child, recursively flatten it first (or find its tail), splice the flattened child chain in, then continue. The call stack acts as the explicit stack."),
        N.h4("What Doesn't Work"),
        N.para("Pure top-down recursion that returns the flattened list from each child and rebuilds is correct but harder to reason about. The approach below is iterative with an inner tail-finding loop — cleaner."),
        N.h4("The Key Observation"),
        N.para("Once we find a node with a child, we need to: (1) find the tail of the child chain, (2) splice child chain between curr and curr.next, (3) reconnect curr.next after the child tail. Finding the tail is a linear scan of the child chain."),
        N.callout("Trade-off: Recursive version uses the call stack (O(d) frames). For extremely deep nesting, this risks stack overflow. The iterative version is safer in production.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def flatten(head):\n"
        "    if not head:\n"
        "        return None\n"
        "    curr = head\n"
        "    while curr:\n"
        "        if curr.child:\n"
        "            child_head = curr.child\n"
        "            # Find the tail of the child chain\n"
        "            tail = child_head\n"
        "            while tail.next:\n"
        "                tail = tail.next\n"
        "            # Save original next\n"
        "            nxt = curr.next\n"
        "            # Splice child chain in\n"
        "            curr.next = child_head\n"
        "            child_head.prev = curr\n"
        "            curr.child = None\n"
        "            # Reattach original next after child tail\n"
        "            tail.next = nxt\n"
        "            if nxt:\n"
        "                nxt.prev = tail\n"
        "        curr = curr.next\n"
        "    return head",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("tail = child_head; while tail.next: tail = tail.next", {"code": True}), " — walk to the end of the child chain to find where to reattach curr.next."])),
    N.para(N.rich([("curr.next = child_head; child_head.prev = curr", {"code": True}), " — splice child chain in; fix the backward pointer."])),
    N.para(N.rich([("tail.next = nxt; if nxt: nxt.prev = tail", {"code": True}), " — reconnect the original next after the child tail; guard against None."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Iterative Stack (Interview Pick)", "O(n)", "O(d) — explicit stack depth"],
        ["Recursive / Iterative Tail-Find", "O(n)", "O(d) — call stack depth"],
    ]),
    N.para("n = total number of nodes. d = maximum nesting depth. Best case (flat list): O(1) extra space. Worst case (chain of children d=n): O(n) space."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS / Stack — use an explicit stack (or recursion) to traverse multi-level structures depth-first, splicing sub-chains into the main chain as we go."])),
    N.callout(
        "When to recognize this pattern: The problem involves a linked list (or any linear structure) where nodes have a 'child' or secondary pointer to another list/subtree. The output requires depth-first ordering — children before siblings. A stack naturally models the DFS backtracking needed to rejoin the main chain after exhausting each child.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS / Stack technique on linked structures:"),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), " (Medium, #114) — DFS splice on a binary tree: right child plays the role of 'next', left child is the child sub-chain."])),
    N.bullet(N.rich([("Copy List with Random Pointer", {"bold": True}), " (Medium, #138) — Complex pointer tracking in a singly linked list with an extra random pointer."])),
    N.bullet(N.rich([("Insert into a Sorted Circular Linked List", {"bold": True}), " (Medium, #708) — Careful pointer manipulation in a circular doubly linked structure."])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), " (Hard, #25) — Splice reversed sub-groups back into the main list using saved pointers."])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), " (Hard, #23) — Repeatedly splice sorted sub-chains using a min-heap for ordering."])),
    N.bullet(N.rich([("Convert Binary Search Tree to Sorted Doubly Linked List", {"bold": True}), " (Medium, #426) — DFS inorder traversal to build a doubly linked list from a BST."])),
    N.para("These problems share the core technique: identifying sub-chains to splice, tracking where to rejoin the main chain, and carefully updating both prev and next pointers."),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch how the stack saves and restores continuations as the child chain is spliced in.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append in chunks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
