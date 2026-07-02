"""
gen_design_linked_list.py — Notion page builder for Design Linked List (#707).
Run: python3 gen_design_linked_list.py
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81e5-b61d-cd27b2ae2cb7"
SLUG = "design_linked_list"

# ─── 1. Properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=707,
    pattern="Linked List",
    subpatterns=["Sentinel Nodes"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Doubly-linked list with two permanent sentinel nodes eliminates all edge cases — every insert/delete is between two existing nodes.",
    icon="🟡"
)
print("Properties set.")

# ─── 2. Wipe old content ───
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ─── 3. Build body ───
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design your implementation of the linked list. You can choose to use a singly or doubly linked list.\n"
         "A node in a singly linked list should have two attributes: ", {}),
        ("val", {"code": True}),
        (" and ", {}),
        ("next", {"code": True}),
        (". A doubly linked list additionally has an attribute ", {}),
        ("prev", {"code": True}),
        (" to indicate the previous node.\n\n"
         "Implement the ", {}),
        ("MyLinkedList", {"code": True}),
        (" class:\n"
         "• get(index) — return the value of the index-th node (0-indexed), or -1 if invalid.\n"
         "• addAtHead(val) — insert a new node at the front.\n"
         "• addAtTail(val) — append a new node at the back.\n"
         "• addAtIndex(index, val) — insert before the index-th node; append if index=size; skip if index>size.\n"
         "• deleteAtIndex(index) — delete the index-th node if valid.", {})
    ])),
    N.divider(),
]

# ─── Solution 1 ───
sol1_code = '''class Node:
    def __init__(self, val=0):
        self.val  = val
        self.prev = None
        self.next = None

class MyLinkedList:
    def __init__(self):
        self.head = Node()          # dummy sentinel head — permanent
        self.tail = Node()          # dummy sentinel tail — permanent
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0               # track count for O(1) bounds check

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        cur = self.head.next        # start at real node 0
        for _ in range(index):
            cur = cur.next          # walk index steps
        return cur.val

    def addAtHead(self, val: int) -> None:
        self._insert_after(self.head, Node(val))

    def addAtTail(self, val: int) -> None:
        self._insert_after(self.tail.prev, Node(val))

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return
        prev = self.head
        for _ in range(index):      # walk index steps from sentinel
            prev = prev.next
        self._insert_after(prev, Node(val))

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        node = self.head.next
        for _ in range(index):
            node = node.next
        node.prev.next = node.next  # left bypass
        node.next.prev = node.prev  # right bypass
        self.size -= 1

    def _insert_after(self, prev, new):
        new.next  = prev.next       # Step 1: save old successor FIRST
        new.prev  = prev            # Step 2: back-wire new node
        prev.next.prev = new        # Step 3: old successor points back to new
        prev.next = new             # Step 4: predecessor points to new (LAST!)
        self.size += 1'''

sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We need a data container that supports random-access by index (like an array) but cheap insertions anywhere (like a list). The challenge is: linked lists have no index structure — we must traverse. The secondary challenge is boundary cases: head, tail, empty list."),
    N.h4("What Doesn't Work"),
    N.para("A naive implementation without sentinels must special-case inserting at the head (no predecessor), inserting into an empty list, and deleting the head or tail (must update self.head / self.tail references). This leads to 5+ if/else branches and subtle off-by-one bugs."),
    N.h4("The Key Observation"),
    N.para("If every node always has a non-null predecessor and non-null successor, then every insert and delete operation is identical: splice a node between its two existing neighbours. Two permanent dummy (sentinel) nodes — one at each end — guarantee this invariant forever."),
    N.h4("Building the Solution"),
    N.para("1. Create dummy_head and dummy_tail. Wire them together.\n2. Every insertion: find predecessor, call _insert_after(prev, new) — 4 pointer assignments in safe order.\n3. Every deletion: find target node, bypass it with 2 pointer assignments.\n4. Track size as int for O(1) bounds checking.\n5. addAtHead = insert after dummy_head. addAtTail = insert after dummy_tail.prev."),
    N.callout("Analogy: Think of dummy_head and dummy_tail as the permanent first and last pages in a binder. Real content goes in between. You never remove those cover pages — they ensure there is always a page before and after wherever you insert.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Doubly-Linked List with Sentinels (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("Node.__init__", {"code": True}), " — Plain data container. ", ("val", {"code": True}), " is the stored value; ", ("prev", {"code": True}), " and ", ("next", {"code": True}), " start as None."])),
    N.para(N.rich([("self.head = Node()", {"code": True}), " — Sentinel head. Never removed. Its external prev is always None."])),
    N.para(N.rich([("self.tail = Node()", {"code": True}), " — Sentinel tail. Never removed. Its external next is always None."])),
    N.para(N.rich([("self.head.next = self.tail; self.tail.prev = self.head", {"code": True}), " — Wire the two sentinels together. Empty list = H ↔ T."])),
    N.para(N.rich([("self.size = 0", {"code": True}), " — Integer counter for O(1) bounds checking on every operation."])),
    N.para(N.rich([("get: if index < 0 or index >= self.size: return -1", {"code": True}), " — Bounds check in O(1) before any traversal starts."])),
    N.para(N.rich([("cur = self.head.next", {"code": True}), " — Skip dummy_head; start at the first real node (index 0)."])),
    N.para(N.rich([("for _ in range(index): cur = cur.next", {"code": True}), " — Advance exactly index steps forward to reach the target."])),
    N.para(N.rich([("addAtHead: _insert_after(self.head, Node(val))", {"code": True}), " — Predecessor is always dummy_head. No empty-list special case needed."])),
    N.para(N.rich([("addAtTail: _insert_after(self.tail.prev, Node(val))", {"code": True}), " — self.tail.prev is either the last real node or dummy_head if empty. Both are valid predecessors."])),
    N.para(N.rich([("addAtIndex: if index > self.size: return", {"code": True}), " — index == size is valid (append); index > size is a silent no-op."])),
    N.para(N.rich([("deleteAtIndex: node.prev.next = node.next", {"code": True}), " — Left bypass: predecessor now points past the deleted node."])),
    N.para(N.rich([("node.next.prev = node.prev", {"code": True}), " — Right bypass: successor now points back past the deleted node. Both sides safely handled by the sentinel invariant."])),
    N.para(N.rich([("_insert_after step 1: new.next = prev.next", {"code": True}), " — Capture old successor BEFORE overwriting. This is the critical step."])),
    N.para(N.rich([("_insert_after step 2: new.prev = prev", {"code": True}), " — Back-wire the new node to its predecessor."])),
    N.para(N.rich([("_insert_after step 3: prev.next.prev = new", {"code": True}), " — Safe to use prev.next here because step 4 hasn't happened yet — prev.next still refers to the old successor."])),
    N.para(N.rich([("_insert_after step 4: prev.next = new", {"code": True}), " — LAST: predecessor now points to the new node. If done earlier, we lose the old successor reference."])),
    N.divider(),
]

# ─── Solution 2 ───
sol2_code = '''class MyLinkedList:
    class Node:
        def __init__(self, val=0):
            self.val  = val
            self.next = None   # singly-linked: no prev pointer

    def __init__(self):
        self.head = self.Node()  # single dummy head sentinel
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        cur = self.head.next
        for _ in range(index):
            cur = cur.next
        return cur.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)  # appending = inserting at size

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return
        prev = self.head
        for _ in range(index):
            prev = prev.next
        new = self.Node(val)
        new.next  = prev.next    # only 2 pointer assignments (no prev pointers)
        prev.next = new
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        prev = self.head
        for _ in range(index):  # walk to predecessor (one extra step vs doubly-linked)
            prev = prev.next
        prev.next = prev.next.next  # skip over target
        self.size -= 1'''

sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Simpler than doubly-linked: each node only needs a next pointer. The dummy head sentinel still handles all boundary cases for insertion. Deletion requires finding the predecessor explicitly since there is no prev pointer."),
    N.h4("What Doesn't Work"),
    N.para("Without even a single dummy head, addAtHead must update self.head — a special case. The single dummy head eliminates this. We lose O(1) addAtTail (no tail sentinel), but the code is simpler overall."),
    N.h4("The Key Observation"),
    N.para("A single dummy head is sufficient for most problems. For deletion, walk to the predecessor (index - 1 steps from dummy_head) and then skip over the target with prev.next = prev.next.next."),
    N.h4("Building the Solution"),
    N.para("1. Create one dummy head node.\n2. addAtIndex: walk index steps from dummy_head to find predecessor. Wire in new node with 2 pointer assignments.\n3. deleteAtIndex: walk index steps from dummy_head to find predecessor. Skip over target.\n4. addAtHead = addAtIndex(0), addAtTail = addAtIndex(size)."),
]

blocks += [
    N.h2("Solution 2 — Singly-Linked List with Dummy Head"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("Node", {"code": True}), " — Only val and next. No prev pointer — saves memory per node but requires predecessor tracking for deletion."])),
    N.para(N.rich([("self.head = Node()", {"code": True}), " — Single dummy head. Eliminates the addAtHead special case."])),
    N.para(N.rich([("addAtTail: addAtIndex(self.size, val)", {"code": True}), " — Delegating to addAtIndex with index=size means O(n) traversal. A tail pointer would make this O(1) but adds complexity."])),
    N.para(N.rich([("deleteAtIndex: walk to predecessor", {"code": True}), " — In singly-linked, we walk to index steps from dummy_head to get the predecessor, not the target."])),
    N.para(N.rich([("prev.next = prev.next.next", {"code": True}), " — One-liner bypass. Safe as long as prev.next (target) and prev.next.next (successor or None) exist."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "get", "addAtHead", "addAtTail", "addAtIndex / deleteAtIndex", "Space"],
        ["Singly-Linked + Dummy Head", "O(n)", "O(1)", "O(n)", "O(n)", "O(n)"],
        ["Doubly-Linked + 2 Sentinels (Interview Pick)", "O(n)", "O(1)", "O(1)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sentinel Nodes (Dummy Head + Dummy Tail)"])),
    N.callout(
        "When to recognize this pattern: Any time inserting at head/tail or deleting from boundary positions would require special-casing. Sentinel nodes collapse all these cases into one uniform operation. Also the foundation for LRU Cache (#146).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sentinel / doubly-linked list technique:"),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Doubly-linked list + hash map; sentinel pattern is the backbone (#146)"])),
    N.bullet(N.rich([("LFU Cache", {"bold": True}), " (Hard) — Two layers of doubly-linked lists with sentinels (#460)"])),
    N.bullet(N.rich([("Flatten a Multilevel Doubly Linked List", {"bold": True}), " (Medium) — Navigate and splice doubly-linked structure (#430)"])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), " (Medium) — Dummy head prevents head-mutation edge case in partial reversal (#92)"])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Dummy head eliminates special-case when the head is the node to remove (#19)"])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), " (Hard) — Dummy head accumulator for building the merged result list (#23)"])),
    N.para("These problems share the same core technique: permanent boundary sentinels so every structural operation is uniform."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section → Sentinel Nodes / Dummy Head sub-pattern.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
