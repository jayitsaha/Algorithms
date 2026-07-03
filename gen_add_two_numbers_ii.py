import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8181-8a76-d400428fb45d"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=445,
    pattern="Linked List",
    subpatterns=["Stack or Reverse"],
    tc="O(m+n)",
    sc="O(m+n)",
    key_insight="Push both lists onto stacks; pop digit-by-digit to add right-to-left; prepend each result node to get MSD-first output.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
print("Wiping old body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} blocks.")

# 3) Build new body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\n"),
        ("Example: ", {"bold": True}),
        ("l1 = 7→2→4→3", {"code": True}),
        (" (= 7243), "),
        ("l2 = 5→6→4", {"code": True}),
        (" (= 564). Result: "),
        ("7→8→0→7", {"code": True}),
        (" (= 7807). "),
        ("You may not modify the input lists.", {"bold": True}),
    ])),
    N.divider(),
]

# Solution 1 — Two Stacks
sol1_code = '''def addTwoNumbers(l1, l2):
    s1, s2 = [], []
    while l1:
        s1.append(l1.val); l1 = l1.next
    while l2:
        s2.append(l2.val); l2 = l2.next
    carry, head = 0, None
    while s1 or s2 or carry:
        d1 = s1.pop() if s1 else 0
        d2 = s2.pop() if s2 else 0
        total = d1 + d2 + carry
        carry = total // 10
        node = ListNode(total % 10)
        node.next = head
        head = node
    return head'''

blocks += [
    N.h2("Solution 1 — Two Stacks (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to add two numbers whose digits are stored most-significant first, but addition naturally proceeds least-significant first (right to left). The problem is really: how do we access a left-to-right structure in reverse order?"),
        N.h4("What Doesn't Work"),
        N.para("Naively iterating both lists forward and adding gives wrong results because carries propagate rightward, but we haven't seen the rightmost digits yet. We would need to accumulate all digits first before computing — that's the hint for a stack."),
        N.h4("The Key Observation"),
        N.para("A stack is Last-In, First-Out. If we push digits from left to right (MSD first), popping gives them right to left (LSD first). This transforms our MSD-first traversal into the LSD-first access that addition requires — without reversing the list."),
        N.h4("Building the Solution"),
        N.para("Push all of l1 onto s1, all of l2 onto s2. Then pop both simultaneously: pop gives the ones digit first, then tens, then hundreds, etc. For each pair, compute total = d1 + d2 + carry, digit = total % 10, new carry = total // 10. Prepend a ListNode(digit) to the result head each time."),
        N.callout(
            "Analogy: Think of the stacks as two calculators reading the number aloud from right to left. You line up the digits column by column — ones, tens, hundreds — add each column, carry overflow to the next. The prepend trick means the last digit you compute (the leading digit) ends up at the front of the result automatically.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("s1, s2 = [], []", {"code": True}), " — Two Python lists used as stacks. Python's list.append() and list.pop() give O(1) stack operations."])),
    N.para(N.rich([("while l1: s1.append(l1.val); l1 = l1.next", {"code": True}), " — Traverse l1 node by node, pushing each digit value. After this loop, s1[-1] is the ones digit (LSD) of l1."])),
    N.para(N.rich([("while l2: s2.append(l2.val); l2 = l2.next", {"code": True}), " — Same for l2. s2[-1] is the ones digit of l2."])),
    N.para(N.rich([("carry, head = 0, None", {"code": True}), " — carry starts at 0. head starts as None (empty result list). head grows via prepending."])),
    N.para(N.rich([("while s1 or s2 or carry:", {"code": True}), " — Critical: we continue while ANY of the three is non-zero. Forgetting the carry check drops the leading digit when a final carry produces an extra digit (e.g., 99 + 1 = 100)."])),
    N.para(N.rich([("d1 = s1.pop() if s1 else 0", {"code": True}), " — Pop the LSD from s1. If s1 is already empty (l1 was shorter), contribute 0 for this position."])),
    N.para(N.rich([("d2 = s2.pop() if s2 else 0", {"code": True}), " — Same for s2/l2."])),
    N.para(N.rich([("total = d1 + d2 + carry", {"code": True}), " — Sum this position's two digits plus any carry from the previous (less significant) position."])),
    N.para(N.rich([("carry = total // 10", {"code": True}), " — Integer division gives 1 if total >= 10, else 0. Max possible carry is 1 because max total = 9+9+1 = 19."])),
    N.para(N.rich([("node = ListNode(total % 10)", {"code": True}), " — Modulo gives the digit for this position (0-9)."])),
    N.para(N.rich([("node.next = head; head = node", {"code": True}), " — Prepend: connect new node to the front of the existing result, then make it the new head. This ensures that when we compute the MSD (last iteration), it lands at the head."])),
    N.para(N.rich([("return head", {"code": True}), " — head now points to the most significant digit of the result, satisfying the MSD-first output requirement."])),
    N.divider(),
]

# Solution 2 — Reverse in-place
sol2_code = '''def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt
    return prev

def addTwoNumbers(l1, l2):
    l1 = reverseList(l1)   # now LSD-first, like problem #2
    l2 = reverseList(l2)
    carry, head = 0, None
    while l1 or l2 or carry:
        d1 = l1.val if l1 else 0
        d2 = l2.val if l2 else 0
        if l1: l1 = l1.next
        if l2: l2 = l2.next
        total = d1 + d2 + carry
        carry = total // 10
        node = ListNode(total % 10)
        node.next = head; head = node
    return head'''

blocks += [
    N.h2("Solution 2 — Reverse In-Place (O(1) extra space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If both lists were LSD-first (like LeetCode #2), the solution would be trivial: just walk both lists forward and add with carry. So the question becomes: what's the cheapest way to make them LSD-first?"),
        N.h4("What Doesn't Work"),
        N.para("We can't just pretend the list is reversed without actually reversing it — accessing a singly linked list in reverse requires either O(n) extra space (stack) or O(n) time to reverse."),
        N.h4("The Key Observation"),
        N.para("Reversing a singly linked list in-place takes O(n) time and O(1) extra space. If mutation of the input is allowed, we can reverse both l1 and l2, reduce this to the simpler problem #2, then prepend the result nodes to get MSD-first output."),
        N.h4("Building the Solution"),
        N.para("Reverse l1 and l2 in-place using the classic pointer-swap trick. Then walk both reversed lists forward simultaneously, adding with carry. Prepend each result node (same trick as Solution 1) to avoid a final reversal of the output."),
        N.callout("Trade-off: This uses O(1) extra space (no stacks) but modifies the input lists. Always clarify with your interviewer whether mutation is permitted before choosing this approach.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("reverseList(head)", {"code": True}), " — Classic in-place linked list reversal. At each step, redirect curr.next to prev, then advance both pointers. Returns the new head (old tail)."])),
    N.para(N.rich([("l1 = reverseList(l1)", {"code": True}), " — After reversal, l1's head is now the ones digit — same structure as problem #2. This mutates the original l1."])),
    N.para(N.rich([("while l1 or l2 or carry:", {"code": True}), " — Same loop condition as Solution 1. Now we walk forward through the reversed lists instead of popping stacks."])),
    N.para(N.rich([("node.next = head; head = node", {"code": True}), " — Still prepend! Even though we're adding forward through reversed inputs, we still prepend so the final output is MSD-first."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Mutates Input?"],
        ["Two Stacks (Interview Pick)", "O(m+n)", "O(m+n)", "No"],
        ["Reverse In-Place", "O(m+n)", "O(1) extra", "Yes"],
        ["Convert to int, add, convert back", "O(m+n)", "O(m+n)", "No"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack or Reverse"])),
    N.callout(
        "When to recognize this pattern: You need to process a singly linked list in reverse order without a reversal pointer. Any problem where MSD-first list must be accessed LSD-first for computation. 'Do not modify the input' + reverse-order traversal = reach for a stack.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Stack or Reverse technique on linked lists:"),
    N.bullet(N.rich([("Add Two Numbers", {"bold": True}), " (Medium #2) — Same problem but LSD-first; no reversal or stacks needed"])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), " (Easy #234) — Use stack or reverse second half to compare from both ends"])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), " (Easy #206) — The core subroutine used in Solution 2"])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), " (Medium #92) — Reverse a subportion between positions m and n"])),
    N.bullet(N.rich([("Plus One Linked List", {"bold": True}), " (Medium #369) — Add 1 to a MSD-first list; same stack trick applies"])),
    N.bullet(N.rich([("Next Greater Node in Linked List", {"bold": True}), " (Medium #1019) — Monotonic stack applied to a linked list"])),
    N.para("These problems share the core technique: use a stack (or in-place reversal) to convert left-to-right linked list traversal into right-to-left access for computation."),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed("https://jayitsaha.github.io/Algorithms/add_two_numbers_ii_explainer.html"),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
