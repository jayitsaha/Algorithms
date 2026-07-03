"""gen_delete_node_in_a_linked_list.py — Notion updater for LC #237."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ec-a94d-f827b789d23c"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=237,
    pattern="Linked List",
    subpatterns=["Copy Next Node Value"],
    tc="O(1)",
    sc="O(1)",
    key_insight="Copy successor's value into node, then unlink the successor — works without access to the previous node.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is a singly-linked list and you are given only a reference to a node to be deleted. The node is guaranteed to be neither the head nor the tail. Delete the given node from the list.\n\n"
         "You are given only access to that node — not the head of the list.\n\n"
         "Example: List = [4, 5, 1, 9], node = 5 → Result: [4, 1, 9]\n"
         "Example: List = [4, 5, 1, 9], node = 1 → Result: [4, 5, 9]", {})
    ])),
    N.divider(),
]

# Solution 1 — Copy Next Value (Interview Pick)
SOLUTION_CODE = '''class Solution:
    def deleteNode(self, node: ListNode) -> None:
        node.val = node.next.val   # copy successor\'s value into current node
        node.next = node.next.next # unlink the now-duplicate successor node'''

blocks += [
    N.h2("Solution 1 — Copy Next Node Value (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Normally to delete a node from a linked list, you'd do prev.next = node.next. But we only have the node itself — not the head, not the previous node. So we need a strategy that works with forward references only."),
        N.h4("What Doesn't Work"),
        N.para("Setting node = None only rebinds a local Python variable — it doesn't modify the list at all. Traversing backwards is impossible in a singly-linked list. Without the head we can't find the predecessor."),
        N.h4("The Key Observation"),
        N.para("We can't delete THIS node. But we CAN delete node.next — because we are its predecessor. If we copy node.next's value into the current node first, then unlink node.next, the observable list is identical to having deleted the original node."),
        N.h4("Building the Solution"),
        N.para("Step 1: node.val = node.next.val — overwrite the target value with the successor's value.\nStep 2: node.next = node.next.next — unlink the now-duplicate successor.\nThe original value is gone from the sequence. The problem guarantees node is never the tail, so node.next always exists."),
        N.callout("Analogy: You're Actor A who must leave the stage but can't exit from the wings. So you take Actor B's lines and costume (copy the value), then Actor B quietly walks off (unlink). The audience sees the correct result.", "🎭", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("def deleteNode(self, node): ", {"code": True}),
        (" — Function takes only the node to delete. Return type is None since we modify in-place.", {})
    ])),
    N.para(N.rich([
        ("node.val = node.next.val", {"code": True}),
        (" — Overwrite the current node's value with its successor's value. The original value (the one we want to delete) is now gone from the list's value sequence.", {})
    ])),
    N.para(N.rich([
        ("node.next = node.next.next", {"code": True}),
        (" — Skip the now-duplicate successor node. It becomes unreferenced and will be garbage-collected. The list is now one node shorter and the deleted value is absent.", {})
    ])),
    N.divider(),
]

# Solution 2 — Explicit temp variable (more readable variant)
SOLUTION_2_CODE = '''class Solution:
    def deleteNode(self, node: ListNode) -> None:
        successor = node.next          # save reference to successor
        node.val = successor.val       # steal successor\'s value
        node.next = successor.next     # bypass successor; it\'s now orphaned'''

blocks += [
    N.h2("Solution 2 — Explicit Successor Variable (Equivalent, More Readable)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same core idea as Solution 1, but saves a reference to node.next before any modification. This makes the order of operations explicit and avoids any risk of confusion when reading the code."),
        N.h4("What Doesn't Work"),
        N.para("Updating node.next before copying the value would lose the reference to the successor. You must always copy the value FIRST, then update the pointer."),
        N.h4("The Key Observation"),
        N.para("Storing successor = node.next makes the two steps crystal clear: steal the value, then discard the now-redundant node object."),
        N.h4("Building the Solution"),
        N.para("Save the successor reference. Copy its value. Point our next past it. The successor is now unreachable and will be garbage-collected."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("successor = node.next", {"code": True}),
        (" — Cache the reference to the next node so we can access it after modifying node.next.", {})
    ])),
    N.para(N.rich([
        ("node.val = successor.val", {"code": True}),
        (" — Copy the successor's value into the current node. The 'deleted' value is now overwritten.", {})
    ])),
    N.para(N.rich([
        ("node.next = successor.next", {"code": True}),
        (" — Skip the successor. It's now detached from the chain and will be garbage-collected.", {})
    ])),
    N.callout(
        "⚠️ Common Wrong Answer: node = None — This only rebinds the local variable in Python. It does not modify the linked list. The previous node's .next still points to the original node object. Always mutate the node in-place (change .val and .next), never reassign the parameter.",
        "⚠️", "orange_background"
    ),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Copy Next Value (Solution 1 & 2)", "O(1)", "O(1)", "Two assignments — no traversal needed"],
        ["Standard deletion (if head given)", "O(n)", "O(1)", "Must traverse to find predecessor"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Copy Next Node Value — a non-tail-only deletion trick that avoids needing the previous node", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Function signature receives a node directly (not the head)\n"
        "• 'Delete a node without access to previous node'\n"
        "• Guaranteed the node is never the tail (so node.next always exists)\n"
        "• Any in-place list modification constrained to forward references only",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("This sub-pattern (Copy Next Node Value) is problem-specific and not a general traversal technique. It arises uniquely when deletion must occur without predecessor access, enabled by the non-tail guarantee.", {"italic": True})
    ])),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related linked list manipulation techniques:"),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), (" (Medium) — Two-pointer with gap N to find the predecessor of the target from the tail (#19)", {})])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), (" (Easy) — Classic in-place reversal using prev/curr/next three-pointer juggling (#206)", {})])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), (" (Medium) — Fast-slow pointer detection plus math to find cycle entry point (#142)", {})])),
    N.bullet(N.rich([("Remove Linked List Elements", {"bold": True}), (" (Easy) — Delete all nodes with given value; uses dummy-head pattern to cleanly handle head deletion (#203)", {})])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), (" (Easy) — Pointer manipulation to interleave two sorted chains in-place; fundamental list rewiring (#21)", {})])),
    N.bullet(N.rich([("Copy List with Random Pointer", {"bold": True}), (" (Medium) — Deep-copy with extra pointer; requires careful distinction between node identity and value (#138)", {})])),
    N.para("These problems share careful pointer rewiring as the core technique — understanding which nodes you can and cannot reach from a given reference."),
    N.divider(),
]

# Interactive Visual Explainer embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("delete_node_in_a_linked_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
