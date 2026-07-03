"""
gen_reverse_nodes_in_k_group.py
Notion in-place update for LeetCode #25 — Reverse Nodes in k-Group (Hard)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ae-a87c-c8f431eb511a"

# ── 1) Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=25,
    pattern="Linked List",
    subpatterns=["Reversal"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Save group_start before reversing k nodes; after reversal wire prev_tail→new_head and group_start→next_segment.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "), ("head", {"code": True}), (" of a linked list and an integer "),
        ("k", {"code": True}),
        (", reverse the nodes of the list "), ("k", {"code": True}),
        (" at a time, and return the modified list. "
         "k is a positive integer and is less than or equal to the length of the linked list. "
         "If the number of nodes is not a multiple of "), ("k", {"code": True}),
        (" then left-out nodes, in the end, should remain as it is."),
    ])),
    N.para(N.rich([
        ("Example 1: "), ("head = [1,2,3,4,5], k = 2", {"code": True}),
        (" → "), ("[2,1,4,3,5]", {"code": True}),
    ])),
    N.para(N.rich([
        ("Example 2: "), ("head = [1,2,3,4,5], k = 3", {"code": True}),
        (" → "), ("[3,2,1,4,5]", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1: Iterative with Dummy Head ─────────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative with Dummy Head (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to reverse every consecutive chunk of k nodes in a singly linked list, in-place, and leave any trailing chunk shorter than k untouched. Each chunk reversal is just the classic Reverse Linked List algorithm applied to a sub-chain."),
        N.h4("What Doesn't Work"),
        N.para("Collecting nodes into an array and rebuilding costs O(n) space. A naive recursive approach without careful pointer management loses track of the 'tail' of each reversed group, making reconnection impossible without O(n) extra references."),
        N.h4("The Key Observation"),
        N.para("After reversing k nodes starting at group_start, we end up with four important anchors: prev_tail (last confirmed node of the processed prefix), prev (new head of reversed group), group_start (new tail of reversed group), and cur (first node of the next group). These four anchors are exactly what we need to stitch the group back into the list with just two pointer assignments."),
        N.h4("Building the Solution"),
        N.para("Use a dummy node before the real head so that prev_tail always points to a real node — no special case for updating the head. Each iteration: (1) Check k nodes ahead; if null is hit early, we have a remainder — return. (2) Reverse k nodes with the 3-pointer technique. (3) Wire prev_tail.next = prev (new head) and group_start.next = cur (next segment); advance prev_tail = group_start."),
        N.callout("Analogy: Imagine a train with cars. Each group of k cars is uncoupled, flipped end-to-end, then reattached to the train. The dummy engine at the front ensures the first group is handled identically to all others.", "🚂", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseKGroup(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0)
    dummy.next = head
    prev_tail = dummy          # tail of last completed reversed group

    while True:
        # Phase 1: verify k nodes exist
        check = prev_tail
        for _ in range(k):
            check = check.next
            if check is None:
                return dummy.next  # remainder group, done

        # Phase 2: reverse k nodes
        group_start = prev_tail.next   # will become the group tail after reversal
        prev, cur = None, group_start
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        # Now: prev = new head, group_start = new tail, cur = next group start

        # Phase 3: stitch back
        prev_tail.next = prev        # connect prefix to new head
        group_start.next = cur       # connect new tail to next segment
        prev_tail = group_start      # advance: group_start is now the tail
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0)", {"code": True}), " — Create a fake node before the list. Eliminates the need to special-case updating the real head pointer."])),
    N.para(N.rich([("prev_tail = dummy", {"code": True}), " — This pointer always holds the tail of the most recently completed reversed group. Starts at dummy (nothing complete yet)."])),
    N.para(N.rich([("check = prev_tail; for _ in range(k): check = check.next", {"code": True}), " — Walk k steps from prev_tail. If any step hits None, fewer than k nodes remain — return immediately."])),
    N.para(N.rich([("group_start = prev_tail.next", {"code": True}), " — Save the first node of this group BEFORE reversing. After reversal, this node becomes the group tail and needs to be wired to the next segment."])),
    N.para(N.rich([("prev, cur = None, group_start", {"code": True}), " — Standard reversal initialization. prev=None so that after reversing, the old group head (new tail) naturally points to None — it will be overwritten by group_start.next = cur."])),
    N.para(N.rich([("for _ in range(k): nxt=cur.next; cur.next=prev; prev=cur; cur=nxt", {"code": True}), " — Classic 3-pointer reversal. After k iterations: prev=new head (old k-th node), cur=first node of the next group."])),
    N.para(N.rich([("prev_tail.next = prev", {"code": True}), " — Connect the previously processed segment to the reversed group's new head."])),
    N.para(N.rich([("group_start.next = cur", {"code": True}), " — Connect the reversed group's new tail (old group head) to the start of the next group. CRITICAL: without this line, group_start still points into the middle of the reversed group, creating a cycle."])),
    N.para(N.rich([("prev_tail = group_start", {"code": True}), " — Advance prev_tail: group_start is now the tail of this completed group. Loop restarts with the next group."])),
    N.divider(),
]

# ── Solution 2: Recursive ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive (Elegant, O(n/k) Stack)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("After reversing the first k nodes, the rest of the problem is identical — reverse k-groups starting from the (k+1)-th node. This self-similar structure screams recursion."),
        N.h4("The Key Observation"),
        N.para("After reversing the first k nodes: head (original first node) becomes the group tail, and prev (original k-th node) becomes the group head. We set head.next = recurse(cur, k) to attach the result of processing the rest, then return prev as the new head of this group."),
        N.h4("Building the Solution"),
        N.para("Base case: if fewer than k nodes remain (count < k), return head unchanged. Inductive step: reverse first k, recursively solve the rest, attach, and return the new head."),
    ]),
    N.h3("Code"),
    N.code("""\
def reverseKGroup(head: ListNode, k: int) -> ListNode:
    # Count k nodes to check availability
    cur, count = head, 0
    while cur and count < k:
        cur = cur.next
        count += 1
    if count < k:
        return head  # fewer than k nodes: base case, return unchanged

    # Reverse first k nodes
    prev, cur = None, head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    # prev = new head of this group
    # head = new tail of this group (old first node)
    # cur = first node of the next group

    head.next = reverseKGroup(cur, k)  # attach result of recursion
    return prev                         # prev is the new head
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("while cur and count < k: cur = cur.next; count += 1", {"code": True}), " — Walk up to k steps to count available nodes. If we exhaust k, count = k. If the list ends first, count < k."])),
    N.para(N.rich([("if count < k: return head", {"code": True}), " — Base case: fewer than k nodes remain; return them unchanged."])),
    N.para(N.rich([("Reverse first k nodes", {"bold": True}), " — Same 3-pointer technique as Solution 1. After k iterations, prev = new group head, head = new group tail, cur = next group."])),
    N.para(N.rich([("head.next = reverseKGroup(cur, k)", {"code": True}), " — Attach the result of recursively reversing the remaining groups. head is the current group's tail, so this wires tail → next group's new head."])),
    N.para(N.rich([("return prev", {"code": True}), " — Return the new head of this group (old k-th node) to the caller, which will assign it as the .next of the previous group's tail."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Iterative (Dummy Head)", "O(n)", "O(1)", "Interview pick. Each node visited at most twice."],
        ["Recursive", "O(n)", "O(n/k)", "Stack depth = number of full groups."],
        ["Collect + Rebuild", "O(n)", "O(n)", "Simplest to code but uses linear extra space."],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Reversal (Reverse Each K-Group)"])),
    N.callout(
        "When to recognize this pattern: 'reverse k consecutive linked list nodes', 'in-place segment reversal', 'swap pairs' (k=2 special case), any in-place linked list restructuring with O(1) space. The dummy head + three-phase loop (Check → Reverse → Connect) is the canonical approach.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Linked List Reversal):"),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), " (Easy) — Core building block: reverse an entire list with the 3-pointer approach. #206"])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), " (Medium) — This exact problem with k=2 hardcoded; simpler version. #24"])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), " (Medium) — Reverse between positions m and n; single-group reversal with stitching. #92"])),
    N.bullet(N.rich([("Rotate List", {"bold": True}), " (Medium) — Rotate right by k; uses tail-to-head reconnection, same pointer surgery. #61"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — Find middle, reverse second half, interleave; reversal as a sub-operation. #143"])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), " (Easy) — Reverse second half in O(1) space for comparison; same reversal pattern. #234"])),
    N.para("These problems all share the same core technique: in-place pointer reversal on a singly linked list, with careful anchor management to reconnect segments."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section, Sub-Pattern: Reversal", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("reverse_nodes_in_k_group")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
