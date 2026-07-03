"""gen_reverse_linked_list.py — Notion update for LeetCode #206 Reverse Linked List."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ca-a9e7-c282a5eed8db"
SLUG = "reverse_linked_list"

print(f"Step 1: Setting properties for page {PAGE_ID}")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=206,
    pattern="Linked List",
    subpatterns=["Iterative Pointer Reversal"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Save curr.next before redirecting; prev is the new head when curr reaches None.",
    icon="🟢"
)
print("  Properties set OK")

print("Step 2: Wiping existing page body")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

print("Step 3: Building new body blocks")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "), ("head", {"code": True}),
        (" of a singly linked list, reverse the list, and return the reversed list's head.\n\n"),
        ("Example: "), ("1 → 2 → 3 → 4 → 5 → None", {"code": True}),
        ("  becomes  "), ("5 → 4 → 3 → 2 → 1 → None", {"code": True}), (".\n\n"),
        ("Constraints: the number of nodes is in range [0, 5000]; values in [-5000, 5000]."),
    ])),
    N.divider(),
]

# ── Solution 1: Iterative ──
iterative_code = """\
def reverseList(head):
    prev = None        # The predecessor; starts None (head becomes new tail → points to None)
    curr = head        # The node we are currently reversing; starts at head
    while curr:        # Keep going until we fall off the end of the list
        nxt = curr.next      # Save successor FIRST — after redirect, curr.next is gone
        curr.next = prev     # THE REVERSAL: point this node backward
        prev = curr          # Advance prev to the node we just reversed
        curr = nxt           # Advance curr to the node we saved earlier
    return prev        # curr is None (past end); prev is the original tail = new head"""

blocks += [
    N.h2("Solution 1 — Iterative Three-Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to flip every arrow in the chain. Each node currently points to its successor; we need it to point to its predecessor. But predecessors aren't stored — we only know where to go next."),
        N.h4("What Doesn't Work"),
        N.para("You can't iterate backward (singly linked, no prev pointer). Collecting all values into a list and re-assigning works but uses O(n) space — not in-place and wastes memory. Recursion works but also uses O(n) stack space."),
        N.h4("The Key Observation"),
        N.para("The moment you overwrite curr.next, you permanently lose the link to the rest of the list. So: save curr.next in a temporary variable FIRST, then redirect, then advance. This single \"save before redirect\" insight is the whole algorithm."),
        N.h4("Building the Solution"),
        N.para("You need to know: (1) where you came from (prev), (2) where you are (curr), (3) where you're going next (nxt). That's 3 things → 3 pointers. Initialize prev = None (head will become the new tail, pointing to None). Walk forward: save, redirect, advance, advance. When curr hits None, prev is at the last node = new head."),
        N.callout("Analogy: Laying a one-way road in reverse. Pick up each road sign behind you and place it facing the other direction. The third pointer (nxt) is your GPS to find the next section before you remove the old sign.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(iterative_code),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = None", {"code": True}), (" — Initialize prev to None. The original head will become the new tail, and tails point to None. This is the correct initial \"previous\" for the first node.")])),
    N.para(N.rich([("curr = head", {"code": True}), (" — Start at the head. We'll walk curr forward through the list, reversing one node per iteration.")])),
    N.para(N.rich([("while curr:", {"code": True}), (" — Loop until curr is None (we've stepped past the last node). When it exits, every node has been reversed.")])),
    N.para(N.rich([("nxt = curr.next", {"code": True}), (" — CRITICAL: save the next node before overwriting curr.next. Without this, redirecting curr.next would make the rest of the list unreachable.")])),
    N.para(N.rich([("curr.next = prev", {"code": True}), (" — THE REVERSAL: redirect this node's next pointer to point backward. The forward connection to nxt is intentionally severed here.")])),
    N.para(N.rich([("prev = curr", {"code": True}), (" — Advance prev. The node we just reversed is now the rightmost member of the growing reversed chain.")])),
    N.para(N.rich([("curr = nxt", {"code": True}), (" — Advance curr to the node we saved. This is safe because nxt was saved before the redirect.")])),
    N.para(N.rich([("return prev", {"code": True}), (" — Loop exits when curr = None. prev is at the last node we processed = the original tail = the new head.")])),
    N.divider(),
]

# ── Solution 2: Recursive ──
recursive_code = """\
def reverseList(head):
    if not head or not head.next:  # Base case: empty list OR last node
        return head                # This IS the new head — return it
    new_head = reverseList(head.next)  # Recurse: reverse the tail; bubbles up the last node
    head.next.next = head              # The node after us should now point BACK to us
    head.next = None                   # Cut our forward link (we become the new tail eventually)
    return new_head                    # Propagate the original tail as the new head"""

blocks += [
    N.h2("Solution 2 — Recursive"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The list can be thought of recursively: reverse(head) = reverse(tail) + point tail's last element back at head, then cut head's forward link."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion without the fix-up (head.next.next = head; head.next = None) just finds the end but doesn't reverse anything."),
        N.h4("The Key Observation"),
        N.para("Once we recurse all the way to the last node, we have the new head. As the call stack unwinds, each frame gets a chance to redirect 'the node after me should point back at me' and 'cut my forward link'. Two pointer operations per frame."),
        N.h4("Building the Solution"),
        N.para("Base: if head is None or the last node, return head (this IS the new head). Recurse on head.next. When recursion returns, head.next still points to the next node. Set head.next.next = head (reverse). Set head.next = None (cut). Return new_head unchanged."),
        N.callout("Trace on 1 → 2 → 3: recurse to 3 (base, new_head=3). Unwind at 2: 3.next=2, 2.next=None. Unwind at 1: 2.next=1, 1.next=None. Return 3. Done.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(recursive_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next: return head", {"code": True}), (" — Base case. Empty list → return None. Single node → it becomes the new head, return it.")])),
    N.para(N.rich([("new_head = reverseList(head.next)", {"code": True}), (" — Recurse all the way to the end. new_head will be the original last node — it stays fixed as the return value throughout.")])),
    N.para(N.rich([("head.next.next = head", {"code": True}), (" — head.next is the node just after us (not yet unlinked). We make IT point back at US — this is the reversal step.")])),
    N.para(N.rich([("head.next = None", {"code": True}), (" — Cut our forward link. We're temporarily setting ourselves as a tail. As calls unwind, a later node will redirect its pointer to us, overwriting this None (except for the true tail — node 1 — which stays None).")])),
    N.para(N.rich([("return new_head", {"code": True}), (" — Propagate the real new head (original last node) all the way back up the call stack.")])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Iterative (Interview Pick)", "O(n)", "O(1)"],
        ["Recursive", "O(n)", "O(n) call stack"],
        ["Collect into stack/array", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Iterative Pointer Reversal")])),
    N.callout(
        "When to recognize this pattern: problem says \"reverse the linked list\" or \"reverse from i to j\"; "
        "linked list re-wiring where in-place O(1) space is desired; "
        "palindrome linked list (reverse second half); "
        "k-group reversal (apply in chunks).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Iterative Pointer Reversal):"),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), (" (Medium) — Reverse only positions [left, right]; locate the left-1 node, reverse the segment, reconnect (#92)")])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), (" (Hard) — Apply reversal in k-node chunks; careful group counting and reconnection (#25)")])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), (" (Easy) — Reverse second half in-place, compare to first half, optionally restore (#234)")])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), (" (Medium) — Find middle (fast/slow), reverse second half, weave the two halves together (#143)")])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), (" (Medium) — Mini-reversal of adjacent pairs; same pointer-wiring logic applied in pairs (#24)")])),
    N.bullet(N.rich([("Rotate List", {"bold": True}), (" (Medium) — Conceptually a rotation; find new tail, form ring, break at new head (#61)")])),
    N.para("These problems all share the core technique: redirect next pointers in-place as you traverse."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section · Sub-Pattern: Iterative Pointer Reversal", "📚", "gray_background"),
]

# ── Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
