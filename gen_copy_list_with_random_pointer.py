"""gen_copy_list_with_random_pointer.py — Notion update for LeetCode #138"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e7-b263-d873c2297bc8"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=138,
    pattern="Linked List",
    subpatterns=["Hash Map or Interleaving"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Two-pass hash map: create all copy nodes in pass 1, then wire next and random in pass 2 using the old→new registry.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing content ───────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A linked list of nodes where each node has two pointers: "),
        ("next", {"code": True}),
        (" (points to the next node or null) and "),
        ("random", {"code": True}),
        (" (points to any node in the list or null). Return a "),
        ("deep copy", {"bold": True}),
        (" of the list — an entirely new list of new node objects with identical structure.")
    ])),
    N.divider(),
]

# ── Solution 1: Two-Pass Hash Map ──────────────────────────────────────────
SOLN1_CODE = """\
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}          # registry: original node → copy node
    # Pass 1: create all copy nodes (values only)
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
    # Pass 2: wire next and random for each copy
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
    return old_to_new[head]
"""

blocks += [
    N.h2("Solution 1 — Two-Pass Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Make a brand-new linked list that is structurally identical to the original — same values, same next chain, same random targets — but using entirely new node objects."),
        N.h4("What Doesn't Work"),
        N.para("A naive single pass fails because when you create a copy of node A and want to wire A'.random, its target might be a node you haven't created yet. You'd have nothing to point to."),
        N.h4("The Key Observation"),
        N.para("If we separate 'creation' from 'wiring,' we guarantee all copy nodes exist before any pointer is set. A hash map (old→new) makes every lookup O(1) regardless of order."),
        N.h4("Building the Solution"),
        N.para("Pass 1: walk the list, create Node(curr.val) for each, store old_to_new[curr] = copy. Pass 2: walk again, for each node look up its copy and set copy.next = old_to_new[curr.next] and copy.random = old_to_new[curr.random], guarding null pointers. Return old_to_new[head]."),
        N.callout("Analogy: Making a perfect photocopy of a web of sticky notes (Pass 1), then re-drawing all the arrows between the new notes (Pass 2). You can't draw arrows before all notes exist.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLN1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head:", {"code": True}), " — edge case: empty list returns null immediately."])),
    N.para(N.rich([("old_to_new = {}", {"code": True}), " — the registry mapping every original node to its copy."])),
    N.para(N.rich([("Pass 1 while curr:", {"code": True}), " — walk each original node once."])),
    N.para(N.rich([("old_to_new[curr] = Node(curr.val)", {"code": True}), " — create a new node with the same value; next and random default to null."])),
    N.para(N.rich([("Pass 2 — if curr.next:", {"code": True}), " — guard before lookup; if next is null, don't look up None (KeyError)."])),
    N.para(N.rich([("old_to_new[curr].next = old_to_new[curr.next]", {"code": True}), " — wire the copy's next to the copy of the original's next."])),
    N.para(N.rich([("if curr.random:", {"code": True}), " — same null guard for random pointer."])),
    N.para(N.rich([("old_to_new[curr].random = old_to_new[curr.random]", {"code": True}), " — wire copy's random to the copy of the original's random target."])),
    N.para(N.rich([("return old_to_new[head]", {"code": True}), " — the copy of the original head is the head of the deep-copied list."])),
    N.divider(),
]

# ── Solution 2: Interleaving (O(1) space) ─────────────────────────────────
SOLN2_CODE = """\
def copyRandomList(head):
    if not head: return None
    # Pass 1: interleave copies — A → A' → B → B' → ...
    curr = head
    while curr:
        copy = Node(curr.val)
        copy.next = curr.next
        curr.next = copy
        curr = copy.next
    # Pass 2: set random pointers using the interleave invariant
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next  # copy of random = random.next
        curr = curr.next.next  # skip over copy to next original
    # Pass 3: separate the two interleaved lists
    new_head = head.next
    curr = head
    while curr:
        orig_next = curr.next.next
        curr.next.next = orig_next.next if orig_next else None
        curr.next = orig_next
        curr = orig_next
    return new_head
"""

blocks += [
    N.h2("Solution 2 — O(1) Space: Interleaving (3 Passes)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we avoid the O(n) hash map? We need a way to look up 'what is the copy of node X?' — without storing a map."),
        N.h4("The Key Observation"),
        N.para("If we insert each copy immediately after its original, the copy is always exactly one step ahead: orig.next = copy. So orig.random.next gives us the copy of the random target — a built-in O(1) lookup using the list structure itself as the registry."),
        N.h4("Building the Solution"),
        N.para("Pass 1: interleave by inserting A' after A, B' after B, etc. Pass 2: set copy.random = orig.random.next (the interleave invariant). Pass 3: carefully separate the two interleaved lists, restoring the original and extracting the copy."),
        N.callout("Trade-off: Saves O(n) hash map space but requires three careful passes and delicate pointer surgery. Hash map approach is clearer in interviews.", "⚖️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("Pass 1:", {"bold": True}), " Insert each copy node directly after its original. After this, the list alternates: orig → copy → orig → copy → ..."])),
    N.para(N.rich([("curr.random.next", {"code": True}), " — Pass 2 key line: since copy of X is always at X.next, the copy of curr.random is at curr.random.next. No hash map needed."])),
    N.para(N.rich([("curr = curr.next.next", {"code": True}), " — in Pass 2 and 3, advance by 2 to skip over copy nodes to reach the next original."])),
    N.para(N.rich([("Pass 3:", {"bold": True}), " Re-link original nodes (skip copies) and simultaneously link copy nodes (skip originals). Restore the original list structure as a side effect."])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Pass Hash Map (Interview Pick)", "O(n)", "O(n)"],
        ["Interleaving (in-place)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Hash Map or Interleaving"])),
    N.callout(
        "When to recognize this pattern: 'deep copy' with non-sequential references; any pointer that can skip to an unprocessed node; 'clone a graph/tree/list with back-references'; need O(1) lookup from original → copy.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Hash Map clone or Interleaving):"),
    N.bullet(N.rich([("Clone Graph", {"bold": True}), " (Medium) — deep copy a graph using BFS/DFS + hash map (#133)"])),
    N.bullet(N.rich([("Copy Binary Tree with Random Pointer", {"bold": True}), " (Medium) — same hash map technique on a binary tree (#1485)"])),
    N.bullet(N.rich([("Flatten a Multilevel Doubly Linked List", {"bold": True}), " (Medium) — complex pointer re-wiring in a linked list (#430)"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — doubly linked list + hash map for O(1) operations (#146)"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — multi-pass linked list transformation (#143)"])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), " (Hard) — in-place linked list restructuring requiring careful pointer surgery (#25)"])),
    N.para("These problems share the same core technique: use a hash map (or in-place interleaving) to maintain a registry when pointers can reference nodes not yet processed."),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("copy_list_with_random_pointer")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
