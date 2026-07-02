"""gen_remove_duplicates_from_sorted_list_ii.py
Notion update script for LeetCode #82 — Remove Duplicates from Sorted List II.
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81aa-90a2-f55e492ce304"
SLUG = "remove_duplicates_from_sorted_list_ii"

# ─── Step 1: Set properties ───
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=82,
    pattern="Linked Lists",
    subpatterns=["Skip All Duplicates"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Use a dummy sentinel + two pointers: prev (last confirmed unique) never moves during a skip; inner while loop exhausts the entire duplicate group before relinking.",
    icon="🟡",
)
print("Properties set.")

# ─── Step 2: Wipe existing body ───
print("Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ─── Step 3: Build new body ───
SOL1_CODE = '''\
def deleteDuplicates(head: ListNode) -> ListNode:
    dummy = ListNode(0, head)   # sentinel; always returns dummy.next as new head
    prev = dummy                # prev = tail of confirmed-clean result list

    while prev.next:            # iterate while there's a candidate to inspect
        curr = prev.next        # curr = node currently under examination
        if curr.next and curr.val == curr.next.val:
            # Peek ahead: same value → duplicate run detected
            dup_val = curr.val              # record the value to eliminate
            while curr and curr.val == dup_val:
                curr = curr.next            # advance past ALL copies; prev stays still
            prev.next = curr               # bypass: cut the entire run from the chain
        else:
            # Current node is unique — safe to include
            prev = prev.next               # lock curr into result; advance prev

    return dummy.next           # dummy.next is the new head of the cleaned list
'''

SOL2_CODE = '''\
def deleteDuplicates_set(head):
    """Two-pass hash-set approach. O(n) time, O(n) space. Works on unsorted lists too."""
    seen, multi = set(), set()
    curr = head
    while curr:                             # Pass 1: identify all duplicate values
        if curr.val in seen:
            multi.add(curr.val)
        seen.add(curr.val)
        curr = curr.next
    dummy = ListNode(0, head)
    curr = dummy
    while curr.next:                        # Pass 2: rebuild list omitting multi values
        if curr.next.val in multi:
            curr.next = curr.next.next      # skip node
        else:
            curr = curr.next
    return dummy.next
'''

SOL3_CODE = '''\
def deleteDuplicates_recursive(head):
    """Elegant recursive approach. O(n) time, O(n) implicit call-stack space."""
    if not head or not head.next:
        return head                         # base case: 0 or 1 node — always safe
    if head.val == head.next.val:
        # head is part of a duplicate group: skip until the group ends
        val = head.val
        while head and head.val == val:
            head = head.next
        return deleteDuplicates_recursive(head)   # recurse on remainder
    else:
        # head is unique: keep it; recurse on tail
        head.next = deleteDuplicates_recursive(head.next)
        return head
'''

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the head of a sorted linked list, delete all nodes that have duplicate numbers, "
        "leaving only distinct numbers from the original list. Return the head of the cleaned list.\n\n"
        "Example: ",
        ("1 → 2 → 2 → 3 → 3 → 4", {"code": True}),
        " → ",
        ("1 → 4", {"code": True}),
        " (both 2s and all 3s removed completely).\n\n"
        "Constraints: The list is sorted in ascending order. "
        "Values in range [−100, 100]. Length [0, 300].",
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Dummy Head + Skip All (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to walk a sorted list and remove every value that appears more than once. "
            "The list is sorted, so all copies of any value cluster together in a contiguous run. "
            "That simplifies detection: a value is duplicated iff curr.val == curr.next.val."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive 'keep one copy' approach (advance curr once, stitch around the duplicate) "
            "only removes one copy. If there are three 3s, two remain. "
            "We need to exhaust the entire group before relinking. "
            "Also, if head itself is duplicated, we'd have no stable predecessor to relink — "
            "we'd need ugly special-case code to find the new head."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The core insight is the two-role invariant: prev is the LAST CONFIRMED UNIQUE node "
            "(never advances into a duplicate group), and curr walks ahead to find the boundary. "
            "After the inner loop, prev.next = curr bypasses the entire group in one assignment. "
            "A dummy sentinel before head removes the 'what is the new head?' edge case entirely."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: dummy.next = head; prev = dummy.\n"
            "Step 2: outer loop while prev.next exists.\n"
            "Step 3: curr = prev.next. Peek: if curr.next has same value, record dup_val.\n"
            "Step 4: inner while advances curr past ALL nodes with dup_val. prev stays still.\n"
            "Step 5: prev.next = curr (bypass). On else branch: prev = prev.next (advance safely).\n"
            "Step 6: return dummy.next."
        ),
        N.callout(
            "Analogy: imagine a printer queue where some jobs are marked 'error' in groups. "
            "Your 'prev' pointer is the last successfully printed job. When you see a group of error jobs, "
            "you fast-forward the queue past the entire error group before relinking — you never print "
            "any of them, not even one.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0, head)", {"code": True}), " — Create a sentinel node whose .next points to head. Value 0 is safe (all real values ≥ −100, but dummy is never in the result)."])),
    N.para(N.rich([("prev = dummy", {"code": True}), " — prev is the tail of our confirmed-clean result list. It starts at dummy (the result is currently empty)."])),
    N.para(N.rich([("while prev.next:", {"code": True}), " — Loop while there is a candidate node to evaluate. When prev.next is null the list is exhausted."])),
    N.para(N.rich([("curr = prev.next", {"code": True}), " — The node currently under examination."])),
    N.para(N.rich([("if curr.next and curr.val == curr.next.val:", {"code": True}), " — Peek ahead. Two conditions: next exists, AND next has the same value. Both must hold to signal a duplicate run."])),
    N.para(N.rich([("dup_val = curr.val", {"code": True}), " — Record the value we need to eliminate so the inner loop can compare."])),
    N.para(N.rich([("while curr and curr.val == dup_val:", {"code": True}), " — Inner skip loop. Advance curr past EVERY node in the group. prev does NOT move."])),
    N.para(N.rich([("curr = curr.next", {"code": True}), " — Move curr forward through the duplicate group one node at a time."])),
    N.para(N.rich([("prev.next = curr", {"code": True}), " — Bypass: this single assignment cuts the entire run (all copies) out of the result chain."])),
    N.para(N.rich([("prev = prev.next", {"code": True}), " — Else branch: curr is unique. Advance prev to include it in the result."])),
    N.para(N.rich([("return dummy.next", {"code": True}), " — The cleaned list's head. Works correctly even if the original head was deleted."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Hash Set (Two Pass)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Collect all values that appear more than once (pass 1), "
            "then rebuild the list keeping only values NOT in that set (pass 2)."
        ),
        N.h4("What Doesn't Work (Why Not Always Use This)"),
        N.para(
            "This approach is O(n) space. It works on unsorted lists too, "
            "but it wastes memory when the sorted property lets us detect duplicates in-place. "
            "In an interview, the hash set solution is acceptable if you mention its space cost."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two passes: one to identify duplicate values into a set, "
            "one to filter them out. Simpler logic, but requires O(n) extra memory."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Pass 1: walk list, track seen values; any value seen twice goes into 'multi'.\n"
            "Pass 2: walk with dummy + curr; if curr.next.val in multi, skip it; else advance."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("seen, multi = set(), set()", {"code": True}), " — seen = any occurrence; multi = appeared 2+ times."])),
    N.para(N.rich([("if curr.val in seen: multi.add(curr.val)", {"code": True}), " — Second time we see this value, mark it as a duplicate."])),
    N.para(N.rich([("while curr.next:", {"code": True}), " — Pass 2: walk list and skip any node whose value is in multi."])),
    N.para(N.rich([("if curr.next.val in multi: curr.next = curr.next.next", {"code": True}), " — Skip node. Note we do NOT advance curr (the next node might also be a multi value)."])),
    N.divider(),
]

# ── Solution 3 ──
blocks += [
    N.h2("Solution 3 — Recursive"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The recursive structure mirrors the problem: 'clean the head, then clean the rest'. "
            "If head is a duplicate, skip it (and its whole group) then recurse. "
            "If head is unique, link it to the recursive result of the tail."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The recursive approach uses O(n) implicit call-stack space (one frame per node). "
            "For very long lists (n = 300 is fine, but n = 10^4 would risk stack overflow). "
            "Elegant and correct, but not space-optimal."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Base case: 0 or 1 node — always return head.\n"
            "Recursive case A: head.val == head.next.val → skip entire group, recurse on remainder.\n"
            "Recursive case B: head is unique → head.next = recurse(head.next); return head."
        ),
        N.h4("Building the Solution"),
        N.para(
            "No dummy needed — recursion naturally handles the 'new head' question by returning "
            "from the base case upward. Very clean, but O(n) stack space."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next: return head", {"code": True}), " — Base case: 0 or 1 node is always clean, return as-is."])),
    N.para(N.rich([("if head.val == head.next.val:", {"code": True}), " — head is part of a duplicate group."])),
    N.para(N.rich([("while head and head.val == val: head = head.next", {"code": True}), " — Exhaust the entire group, same as the iterative inner loop."])),
    N.para(N.rich([("return deleteDuplicates_recursive(head)", {"code": True}), " — Recurse on what follows the group. head now points at the first node after the group (or null)."])),
    N.para(N.rich([("head.next = deleteDuplicates_recursive(head.next)", {"code": True}), " — head is unique: keep it, recurse on its tail."])),
    N.divider(),
]

blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution",                    "Time", "Space",   "Notes"],
    ["Hash Set (Two Pass)",         "O(n)", "O(n)",    "Works unsorted; wasteful memory"],
    ["Dummy + Skip All (Optimal)",  "O(n)", "O(1)",    "Interview pick"],
    ["Recursive",                   "O(n)", "O(n) stack", "Elegant; beware deep lists"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked Lists (Section 5, DSA_Patterns_and_SubPatterns_Guide.md — §5.1 Basic Linked List Operations)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Skip All Duplicates — detect a run (peek via curr.next), exhaust it with an inner loop, bypass with prev.next = curr."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Sorted linked list problem\n"
        "• 'Delete all nodes with duplicate values' (not keep one, delete ALL)\n"
        "• Head might itself be deleted → always add dummy sentinel\n"
        "• O(1) space required\n"
        "• Groups of same-value nodes need to be bypassed atomically",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Remove Duplicates from Sorted List", {"bold": True}), " (Easy) — Keep one copy per value; simpler (no skip-all, no inner loop)"])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Dummy sentinel + two-pointer gap; same dummy pattern"])),
    N.bullet(N.rich([("Partition List", {"bold": True}), " (Medium) — Dummy head for two separate chains; same sentinel motivation"])),
    N.bullet(N.rich([("Delete the Middle Node of a Linked List", {"bold": True}), " (Medium) — Fast-slow with prev staying behind; same 'anchor' invariant"])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), " (Medium) — Dummy head + careful relinking of pairs"])),
    N.bullet(N.rich([("Remove Duplicates from Sorted Array II", {"bold": True}), " (Medium) — Skip-group concept on arrays with a write-pointer"])),
    N.bullet(N.rich([("Odd Even Linked List", {"bold": True}), " (Medium) — Two sub-lists separated and relinked; similar pointer choreography"])),
    N.para("These problems share the core technique: a dummy sentinel to avoid head-special-cases, and a predecessor pointer that stays still while the cursor fast-forwards through a group."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5.1 (Linked Lists: Basic Operations), Sub-Pattern: Skip All Duplicates", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys to see each pointer move, duplicate group detection, and bypass in action.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Append all blocks ───
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
