"""
gen_remove_nth_node_from_end_of_list.py
Regenerates the Notion page for LeetCode #19 — Remove Nth Node From End of List
Update IN-PLACE (notion_page_id provided).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8178-94de-c6ab5618e407"

# ── 1) Properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=19,
    pattern="Linked List",
    subpatterns=["Two Pointers (N Gap)", "Dummy Head"],
    tc="O(L)",
    sc="O(1)",
    key_insight="Advance fast by n+1 steps; lockstep until fast=None; slow is then the predecessor of the nth-from-end node.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the head of a singly linked list, remove the ",
        ("n", {"code": True}),
        "-th node from the end of the list and return its head. The problem guarantees ",
        ("1 ≤ n ≤ length", {"code": True}),
        ", so ",
        ("n", {"code": True}),
        " is always valid. Solve it in one pass."
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        "head = [1,2,3,4,5], n = 2  →  [1,2,3,5]  (node '4', the 2nd from end, is removed)"
    ])),
    N.para(N.rich([
        ("Edge case: ", {"bold": True}),
        "n equals the list length → the head itself is the target. A dummy sentinel node handles this without a separate branch."
    ])),
    N.divider(),
]

# ── Solution 1 — One-Pass Two-Pointer Gap ─────────────────────────
blocks += [
    N.h2("Solution 1 — One-Pass Two-Pointer Gap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find and unlink a node that is n steps from the tail. To unlink it, we actually need its predecessor (n+1 from the end). If we can position a trailing pointer at that predecessor in a single pass, we're done."),
        N.h4("What Doesn't Work"),
        N.para("Without random access, we can't compute 'n from end' directly. A naive approach traverses once to count length L, then again L-n steps to the predecessor — two passes. We want to do it in one."),
        N.h4("The Key Observation"),
        N.para("If two pointers maintain a fixed gap of n+1 nodes between them, then when the leading pointer (fast) reaches None (past the tail), the trailing pointer (slow) is exactly n+1 behind — i.e., at the predecessor of the nth-from-end node."),
        N.h4("Building the Solution"),
        N.para("1. Create a dummy sentinel before head — this makes head-removal uniform (no special branch needed).\n2. Set fast = slow = dummy.\n3. Advance fast by n+1 steps. Now gap = n+1.\n4. Move both pointers one step at a time until fast is None. Gap is preserved.\n5. slow is now at the predecessor. Execute slow.next = slow.next.next to unlink.\n6. Return dummy.next (not head — head might have been removed)."),
        N.callout(
            "Analogy: Imagine two runners on a track. Runner A starts n+1 seconds before Runner B. When A finishes the race (hits the end), B is exactly n+1 seconds behind the finish line — which corresponds to the predecessor of the nth-from-end node.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""\
def removeNthFromEnd(head, n):
    dummy = ListNode(0)      # sentinel node before head
    dummy.next = head
    fast = slow = dummy      # both start at dummy
    for _ in range(n + 1):  # advance fast by n+1 steps
        fast = fast.next
    while fast is not None:  # lockstep until fast falls off end
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next   # unlink the nth-from-end node
    return dummy.next            # never return bare head"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0)", {"code": True}), " — Create a sentinel node. Its only purpose is to give slow a valid predecessor when the head needs to be removed."])),
    N.para(N.rich([("dummy.next = head", {"code": True}), " — Attach the real list to the dummy, making dummy position -1."])),
    N.para(N.rich([("fast = slow = dummy", {"code": True}), " — Both pointers begin at the dummy. Gap is currently 0."])),
    N.para(N.rich([("for _ in range(n + 1): fast = fast.next", {"code": True}), " — Advance fast exactly n+1 steps forward. After this loop, the distance from slow to fast is n+1 nodes. (n+1 not n, because we need slow to land at the predecessor, not the target itself.)"])),
    N.para(N.rich([("while fast is not None:", {"code": True}), " — Lockstep phase. Both pointers move together, preserving the gap."])),
    N.para(N.rich([("fast = fast.next; slow = slow.next", {"code": True}), " — Both advance one step. The gap remains n+1 throughout."])),
    N.para(N.rich([("slow.next = slow.next.next", {"code": True}), " — When fast is None, slow is at the predecessor of the target. This line bypasses the target node, effectively deleting it from the list."])),
    N.para(N.rich([("return dummy.next", {"code": True}), " — Return the actual head of the modified list. If n was equal to the list length, the original head was removed and dummy.next now points to the second node. Using the original head variable here would return a deleted node."])),
    N.divider(),
]

# ── Solution 2 — Two-Pass ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Two-Pass (Count Length, Then Walk)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we know the list length L, the nth-from-end node is at 1-indexed position L - n + 1. Its predecessor is at position L - n. Count L in one pass, then walk L - n steps from dummy in a second pass."),
        N.h4("What Doesn't Work"),
        N.para("This approach is perfectly correct — it's just less elegant because it makes two traversals. For large lists this doubles the constant factor. It's a fine starting point in an interview, after which you optimise to one pass."),
        N.h4("The Key Observation"),
        N.para("With a known length, the problem reduces to 'remove the (L-n)-th node from the front', which is trivially solved with a simple counter walk."),
        N.h4("Building the Solution"),
        N.para("Count L via a full traversal. Then walk a cursor from dummy exactly L-n steps — it lands at the predecessor. Unlink with cursor.next = cursor.next.next."),
        N.callout("Use this explanation in interviews before pivoting to the one-pass solution. It shows clear reasoning.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    L, cur = 0, head
    while cur:               # Pass 1: count length
        L += 1
        cur = cur.next
    cur = dummy
    for _ in range(L - n):  # Pass 2: walk to predecessor (L-n steps from dummy)
        cur = cur.next
    cur.next = cur.next.next
    return dummy.next"""),
    N.h3("Line by Line"),
    N.para(N.rich([("L = 0; while cur: L += 1; cur = cur.next", {"code": True}), " — First pass: count the list length L."])),
    N.para(N.rich([("for _ in range(L - n):", {"code": True}), " — Second pass from dummy. Walking L - n steps from dummy lands at the predecessor (position L - n from dummy = position L - n in the list, 1-indexed)."])),
    N.para(N.rich([("cur.next = cur.next.next", {"code": True}), " — Unlink the target."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",  "Space", "Passes"],
        ["Two-Pass (count+walk)", "O(L)",  "O(1)",  "2"],
        ["One-Pass Gap ✓",        "O(L)",  "O(1)",  "1"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Pointers (N Gap), Dummy Head"])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Remove k-th node from end' → two-pointer gap of k+1\n"
        "• 'Find middle of linked list' → fast at 2× speed, slow at 1×\n"
        "• 'Detect cycle / find cycle start' → same fast/slow family (Floyd's)\n"
        "• Whenever you need to measure distance from the tail without a second traversal\n"
        "• Whenever removing a list node and you need to avoid head-removal special cases → dummy head",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (two-pointer gap / dummy head):"),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — fast moves 2×, slow 1× → slow at middle when fast done (#876)"])),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), " (Easy) — fast/slow meet if there's a cycle; Floyd's detection (#141)"])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), " (Medium) — find cycle entry point using gap-reset after meeting (#142)"])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), " (Medium) — array treated as linked list, same Floyd's approach (#287)"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — find middle via fast/slow, reverse second half, merge (#143)"])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), " (Easy) — find middle, reverse second half, compare (#234)"])),
    N.para("These problems all exploit the idea that two pointers with a fixed speed ratio or fixed gap can measure structural properties of a linked list in a single pass."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List Patterns section.\nSub-Pattern: Two Pointers (N Gap) + Dummy Head · Source: Analysis + Guide", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_nth_node_from_end_of_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
