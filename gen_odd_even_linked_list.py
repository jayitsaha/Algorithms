"""gen_odd_even_linked_list.py — Notion update for LeetCode #328 Odd Even Linked List"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811f-9278-eae930f5d189"
SLUG = "odd_even_linked_list"

# ── 1) Set page properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=328,
    pattern="Linked List",
    subpatterns=["Two Separate Lists"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Maintain two chain tails (odd/even); rewire next pointers to separate interleaved groups, then stitch even chain onto odd chain's tail.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(
        N.rich([
            ("Given the head of a singly linked list, group all the nodes with odd indices together "
             "followed by the nodes with even indices, and return the reordered list.\n\n"
             "The first node is considered odd, the second node is even, and so on.\n\n"
             "Note that the relative order inside both the even and odd groups should remain "
             "as it was in the input.\n\n"
             "You must solve the problem in "),
            ("O(n)", {"code": True}),
            (" time complexity and "),
            ("O(1)", {"code": True}),
            (" extra space complexity."),
        ])
    ),
    N.para(N.rich([
        ("Example 1: "), ("head = [1,2,3,4,5]", {"code": True}),
        (" → Output: "), ("[1,3,5,2,4]", {"code": True}),
        ("\nExample 2: "), ("head = [2,1,3,5,6,4,7]", {"code": True}),
        (" → Output: "), ("[2,3,6,7,1,5,4]", {"code": True}),
    ])),
    N.divider(),
]

# Solution 1 — Two Separate Lists (Interview Pick)
solution1_code = """\
def oddEvenList(head):
    if not head or not head.next:
        return head
    odd = head          # tail of odd chain (starts at pos 1)
    even = head.next    # tail of even chain (starts at pos 2)
    even_head = even    # SAVE: needed to attach after loop
    while even and even.next:
        odd.next = even.next   # Step 1: odd tail skips over even
        odd = odd.next         # Step 2: advance odd tail
        even.next = odd.next   # Step 3: even tail skips over (advanced) odd
        even = even.next       # Step 4: advance even tail
    odd.next = even_head       # stitch: odd chain tail → even chain head
    return head
"""

blocks += [
    N.h2("Solution 1 — Two Separate Lists (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have a list where odd-indexed and even-indexed nodes are interleaved: "
            "odd, even, odd, even, … We need to 'unzip' these two interleaved sub-lists "
            "and concatenate them. The key constraint is O(1) space — we cannot store values in arrays."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Collecting all values into two arrays (odds[], evens[]) and overwriting node values "
            "is correct but uses O(n) space. Building a new list of new nodes also uses O(n) space. "
            "Both violate the constraint. We need to work purely with pointer re-wiring."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Every odd-indexed node's .next pointer currently points to an even-indexed node. "
            "Every even-indexed node's .next pointer currently points to the next odd-indexed node. "
            "We can redirect these pointers to skip over the 'other group' — building two separate "
            "chains simultaneously without any extra allocation."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Maintain two 'chain tails': odd (starts at head) and even (starts at head.next). "
            "Save even_head = even before the loop (to attach later). "
            "Each iteration: (1) odd.next = even.next — odd tail skips to next odd. "
            "(2) odd = odd.next — advance odd tail. "
            "(3) even.next = odd.next — even tail skips to next even. "
            "(4) even = even.next — advance even tail. "
            "After loop: odd.next = even_head to concatenate."
        ),
        N.callout(
            "Analogy: Imagine two queues at an airport check-in, one for odd-row seats and one for even-row seats. "
            "Passengers arrive interleaved. A coordinator pulls each person into their correct queue as they arrive, "
            "maintaining original arrival order within each queue. At the end, the odd queue boards first.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(solution1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next:", {"code": True}),
                   " — Guard clause. If 0 or 1 nodes, no reordering needed; return immediately."])),
    N.para(N.rich([("odd = head", {"code": True}),
                   " — odd pointer starts at position 1 (the first odd-indexed node); it is the current tail of the odd chain."])),
    N.para(N.rich([("even = head.next", {"code": True}),
                   " — even pointer starts at position 2 (the first even-indexed node); current tail of the even chain."])),
    N.para(N.rich([("even_head = even", {"code": True}),
                   " — CRITICAL: save the start of the even chain before any rewiring. Used for the final concatenation."])),
    N.para(N.rich([("while even and even.next:", {"code": True}),
                   " — Loop while there's an even node AND a next odd node after it. Handles both odd-length and even-length lists."])),
    N.para(N.rich([("odd.next = even.next", {"code": True}),
                   " — Step 1: odd tail skips over the current even node to point at the next odd node."])),
    N.para(N.rich([("odd = odd.next", {"code": True}),
                   " — Step 2: advance odd tail to that next odd node. MUST happen before Step 3."])),
    N.para(N.rich([("even.next = odd.next", {"code": True}),
                   " — Step 3: even tail skips over the (just-advanced) odd node to point at the next even node."])),
    N.para(N.rich([("even = even.next", {"code": True}),
                   " — Step 4: advance even tail."])),
    N.para(N.rich([("odd.next = even_head", {"code": True}),
                   " — Concatenate: the tail of the odd chain now points to the head of the even chain."])),
    N.para(N.rich([("return head", {"code": True}),
                   " — head (position 1) is still the start of the result list."])),
    N.divider(),
]

# Solution 2 — Value Overwrite (naive)
solution2_code = """\
def oddEvenList(head):
    odds, evens, node, pos = [], [], head, 1
    while node:
        (odds if pos % 2 else evens).append(node.val)
        node, pos = node.next, pos + 1
    node = head
    for val in odds + evens:
        node.val, node = val, node.next
    return head
"""

blocks += [
    N.h2("Solution 2 — Value Overwrite with Arrays (Naive, O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Collect odd-indexed values and even-indexed values into separate lists, then write them back in order."),
        N.h4("What Doesn't Work for Large Inputs"),
        N.para(
            "This uses O(n) extra space (two arrays of values). For the interview, always mention this as "
            "the naive starting point and then offer to optimize to O(1) space using pointer rewiring."
        ),
        N.h4("The Key Observation"),
        N.para("We can overwrite node values in-place with the reordered sequence. No new nodes needed. "
               "But we still need O(n) space for the value arrays — so this is the sub-optimal approach."),
        N.h4("Building the Solution"),
        N.para("Single pass to collect values by index parity. Then second pass to overwrite node values. "
               "Simple and correct, but uses O(n) space."),
    ]),
    N.h3("Code"),
    N.code(solution2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("odds, evens", {"code": True}), " — Two arrays to collect values by index parity."])),
    N.para(N.rich([("(odds if pos % 2 else evens).append(node.val)", {"code": True}),
                   " — Route each value to its group based on 1-based position parity."])),
    N.para(N.rich([("for val in odds + evens:", {"code": True}),
                   " — Concatenate the two value lists; overwrite node values in order."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Value Overwrite (arrays)", "O(n)", "O(n)"],
        ["Two Separate Lists ✓ (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Separate Lists"])),
    N.callout(
        "When to recognize this pattern: 'reorder linked list in-place by index or value property', "
        "'group nodes while preserving relative order', 'O(1) space' + linked list. "
        "Also applies when you need to partition a list into exactly two groups and concatenate them.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Two Separate Lists / Partition):"),
    N.bullet(N.rich([("Partition List", {"bold": True}),
                     " (Medium) — Partition by value < x: same two-chain pattern, different split criterion (#86)"])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}),
                     " (Medium) — Fast/slow pointer to find split point, then pointer rewiring (#19)"])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}),
                     " (Medium) — Splice out segment, reverse in-place, reattach — extended pointer rewiring (#92)"])),
    N.bullet(N.rich([("Sort List", {"bold": True}),
                     " (Medium) — Merge sort on linked list: split into two chains, sort, merge (#148)"])),
    N.bullet(N.rich([("Split Linked List in Parts", {"bold": True}),
                     " (Medium) — Partition into k nearly-equal sub-chains using tail-tracking technique (#725)"])),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}),
                     " (Easy) — Classic fast/slow two-pointer; builds the same structural reasoning (#141)"])),
    N.para("These problems share the core technique: maintaining one or more chain tails, rewiring "
           "next pointers in a single pass, then stitching chains together at the end."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section · "
              "Sub-Pattern: Two Separate Lists (verified in Guide)", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks: {len(blocks)}")
