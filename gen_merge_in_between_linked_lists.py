"""
gen_merge_in_between_linked_lists.py
Regenerates the Notion page for LC #1669 — Merge In Between Linked Lists
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e0-b482-e33c526e50dd"

# ── 1. Properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1669,
    pattern="Linked List",
    subpatterns=["Link Manipulation"],
    tc="O(n+m)",
    sc="O(1)",
    key_insight="Find prevA (idx a-1), afterB (idx b+1), tail2; then two pointer rewires complete the splice.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two linked lists, "), ("list1", {"code": True}),
        (" and "), ("list2", {"code": True}),
        (", and two integers "), ("a", {"code": True}), (" and "), ("b", {"code": True}),
        (". Remove all nodes of "), ("list1", {"code": True}),
        (" from index "), ("a", {"code": True}), (" to index "), ("b", {"code": True}),
        (" (inclusive) and insert "), ("list2", {"code": True}),
        (" in their place. Return the head of the resulting linked list. "
         "Both "), ("list1", {"code": True}), (" and "), ("list2", {"code": True}),
        (" are non-empty. Constraints: "), ("1 ≤ a ≤ b < len(list1)", {"code": True}), (".")
    ])),
    N.divider(),
]

# ── Solution 1 — Optimal: Three-Anchor Pointer Surgery ──
sol1_code = '''\
def mergeInBetween(list1, a, b, list2):
    # Phase 1: walk to index a-1 (prevA)
    prev_a = list1
    for _ in range(a - 1):        # a-1 steps → land at index a-1
        prev_a = prev_a.next

    # Phase 2: walk to index b+1 (afterB)
    after_b = prev_a
    for _ in range(b - a + 2):    # (b+1) - (a-1) = b-a+2 steps
        after_b = after_b.next

    # Phase 3: walk list2 to its tail
    tail2 = list2
    while tail2.next:
        tail2 = tail2.next

    # Phase 4: two rewires
    prev_a.next = list2            # seam 1: attach list2 after prevA
    tail2.next  = after_b          # seam 2: attach afterB after tail2
    return list1
'''

blocks += [
    N.h2("Solution 1 — Three-Anchor Pointer Surgery (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to cut out a segment [a..b] from list1 and paste in list2. In a singly linked list, you can't step backward — so the trick is to remember exactly two cut-point nodes (the ones just BEFORE and just AFTER the removed segment) and one additional node (list2's tail). Then three saves + two pointer assignments do all the work."),
        N.h4("What Doesn't Work"),
        N.para("Copying values is unnecessary and O(n) space. Traversing twice (once to cut, once to find tail2) works but can be combined. There's no simpler approach than three traversals + two rewires — this IS the optimal."),
        N.h4("The Key Observation"),
        N.para("In any 'remove a range and insert a new segment' operation on a singly linked list, the minimum information needed is: (1) the node whose .next will change to skip the removed range → prevA; (2) the node that the new segment must ultimately point to → afterB; (3) the last node of the new segment → tail2. These three nodes plus two pointer assignments are both necessary and sufficient."),
        N.h4("Building the Solution"),
        N.para("Walk list1 a-1 steps to reach prevA (index a-1). From prevA, walk b-a+2 more steps to reach afterB (index b+1). Walk list2 to its tail. Then: prevA.next = list2; tail2.next = afterB. Return list1."),
        N.callout(
            "Analogy: it's like editing a document. Highlight text from position a to b (the 'removed segment'), then paste another document (list2) in that gap. The cursor positions before and after the highlight are your prevA and afterB.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("prev_a = list1", {"code": True}), " — Initialize prev_a at the head (index 0). We will walk it forward."])),
    N.para(N.rich([("for _ in range(a - 1)", {"code": True}), " — Loop a-1 times. Starting from index 0, after a-1 iterations we land at index a-1 (the node immediately before the removal zone)."])),
    N.para(N.rich([("prev_a = prev_a.next", {"code": True}), " — Advance one step each iteration."])),
    N.para(N.rich([("after_b = prev_a", {"code": True}), " — Reuse prev_a as the starting point for after_b. Both start at index a-1."])),
    N.para(N.rich([("for _ in range(b - a + 2)", {"code": True}), " — Walk b-a+2 steps. From index a-1, this lands at index (a-1) + (b-a+2) = b+1 — exactly one node past the removed segment."])),
    N.para(N.rich([("after_b = after_b.next", {"code": True}), " — Advance through the removed segment and one beyond."])),
    N.para(N.rich([("tail2 = list2; while tail2.next: tail2 = tail2.next", {"code": True}), " — Walk list2 to its last node (where .next is None). This is the node that will connect back into list1."])),
    N.para(N.rich([("prev_a.next = list2", {"code": True}), " — SEAM 1: Redirect prevA's forward pointer to list2's head. The removed nodes [a..b] now have no incoming references → garbage collected."])),
    N.para(N.rich([("tail2.next = after_b", {"code": True}), " — SEAM 2: Attach list2's tail to afterB, reconnecting the rest of list1."])),
    N.para(N.rich([("return list1", {"code": True}), " — The head of list1 never changed; return it."])),
    N.divider(),
]

# ── Solution 2 — Brute Force: Collect then Rebuild ──
sol2_code = '''\
def mergeInBetween_bruteforce(list1, a, b, list2):
    # Collect all list1 values except those at indices a..b
    vals1 = []
    cur, idx = list1, 0
    while cur:
        if idx < a or idx > b:
            vals1.append(cur.val)
        cur = cur.next
        idx += 1

    # Collect all list2 values
    vals2 = []
    cur = list2
    while cur:
        vals2.append(cur.val)
        cur = cur.next

    # Combine and rebuild
    all_vals = vals1[:a] + vals2 + vals1[a:]

    # Rebuild linked list from values (for illustration only)
    dummy = ListNode(0)
    node = dummy
    for v in all_vals:
        node.next = ListNode(v)
        node = node.next
    return dummy.next
'''

blocks += [
    N.h2("Solution 2 — Collect and Rebuild (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest mental model: extract all values from list1 excluding [a..b], insert all values from list2, then rebuild the linked list. Clear and easy to reason about."),
        N.h4("What Doesn't Work"),
        N.para("This uses O(n+m) extra space for the collected values plus O(n+m) space to build a new list — wasteful compared to the O(1) space in-place approach."),
        N.h4("The Key Observation"),
        N.para("Separating 'what values to keep' from 'how to structure them' makes the logic easier to verify. It's a correct but non-optimal solution that's good to describe first in an interview before proposing the O(1) space approach."),
        N.h4("Building the Solution"),
        N.para("Two passes over the lists to collect values, one merge of the arrays, one pass to build the output list."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("Traverse list1", {"bold": True}), " — collect values at indices < a and > b (skip the removal zone)."])),
    N.para(N.rich([("Traverse list2", {"bold": True}), " — collect all values."])),
    N.para(N.rich([("Combine", {"bold": True}), " — vals1[:a] + vals2 + vals1[a:] gives the merged value sequence."])),
    N.para(N.rich([("Rebuild", {"bold": True}), " — create new ListNode objects from the combined list."])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Three-Anchor Pointer Surgery (Optimal)", "O(n + m)", "O(1)"],
        ["Collect and Rebuild (Brute Force)", "O(n + m)", "O(n + m)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Link Manipulation — saving boundary pointers and rewiring .next references in-place"])),
    N.callout(
        "When to recognize this pattern: problem involves removing a contiguous range from a linked list / inserting another linked structure in-place / 'merge' or 'splice' operations on linked lists / O(1) space requirement with in-place pointer changes.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same link manipulation technique:"),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), " (Medium) — Same boundary identification (prevA, afterB); reverse the segment between them, then reconnect."])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Find the node just before the target, rewire its .next to skip one node."])),
    N.bullet(N.rich([("Rotate List", {"bold": True}), " (Medium) — Find new tail and new head by index, cut and reattach — identical save-then-rewire pattern."])),
    N.bullet(N.rich([("Split Linked List in Parts", {"bold": True}), " (Medium) — Walk to cut point, save the next node, null out the current .next — exact same discipline of saving before cutting."])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — Two-pointer interleaving via .next reassignments; builds intuition for link rewiring."])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), " (Medium) — Localize 2-node groups and rewire their .next pointers in a loop."])),
    N.para("These problems share the core discipline: identify boundary nodes, then rewire — never modify values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section, Link Manipulation sub-pattern.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("merge_in_between_linked_lists")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
