"""
gen_add_two_numbers.py — Notion IN-PLACE update for Add Two Numbers (LC #2)
Run from the Algorithms directory: python3 gen_add_two_numbers.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c2-9822-c934d4621893"

# ─── Step 1: Set properties ───────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2,
    pattern="Linked List",
    subpatterns=["Digit by Digit with Carry"],
    tc="O(max(m,n))",
    sc="O(max(m,n))",
    key_insight="Traverse both lists simultaneously adding digits + carry; reversed order matches column-addition direction naturally.",
    icon="🟡"
)
print("Properties set.")

# ─── Step 2: Wipe old body ────────────────────────────────────────────────────
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ─── Step 3: Build body ───────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "You are given two non-empty linked lists representing two non-negative integers. "
    "The digits are stored in reverse order, and each of their nodes contains a single digit. "
    "Add the two numbers and return the sum as a linked list.\n\n"
    "You may assume the two numbers do not contain any leading zero, except the number 0 itself.\n\n"
    "Example: l1 = [2,4,3], l2 = [5,6,4]  →  Output: [7,0,8]  (342 + 465 = 807)"
)

SOLUTION_1_CODE = '''\
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)      # Sentinel node — real answer is dummy.next
    cur = dummy
    carry = 0

    while l1 or l2 or carry:          # Loop while any work remains
        v1 = l1.val if l1 else 0      # Safe extract: 0 if list exhausted
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry        # Column sum: digit + digit + carry-in
        carry = total // 10            # Carry out: 0 or 1
        cur.next = ListNode(total % 10)# New result node = units digit
        cur = cur.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next                  # Skip sentinel; return real head
'''

SOLUTION_2_CODE = '''\
# Recursive approach — elegant but O(max(m,n)) stack depth
def addTwoNumbers(l1, l2, carry=0):
    if not l1 and not l2 and carry == 0:
        return None
    v1 = l1.val if l1 else 0
    v2 = l2.val if l2 else 0
    total = v1 + v2 + carry
    node = ListNode(total % 10)
    node.next = addTwoNumbers(
        l1.next if l1 else None,
        l2.next if l2 else None,
        total // 10
    )
    return node
'''

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Optimal Iterative ──
blocks += [
    N.h2("Solution 1 — Digit-by-Digit Simulation with Dummy Head (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to add two numbers that are stored as linked lists in reverse order. "
            "Reframe: this is exactly elementary-school column addition. "
            "At each position (list node), we add two digits and a carry from the previous position, "
            "write the units digit as the result, and carry the tens digit forward."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Converting to integers works for small numbers but fails for arbitrarily large numbers — "
            "Python handles big ints, but real systems don't. The point of the linked-list representation "
            "is precisely to support numbers too large for native integer types. Avoid int() conversion in the interview."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The reversed storage is NOT a problem — it's a gift. Because the head is the ones digit, "
            "traversing left-to-right through both lists gives us exactly the right column order for addition. "
            "We never need to reverse anything. We just walk, compute, and build."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. We need a carry variable (starts at 0). "
            "2. We need to handle lists of different lengths — substitute 0 for exhausted lists. "
            "3. We need to handle a final carry after both lists end (999+1 → 1000). "
            "4. Use a dummy head to avoid special-casing the first result node. "
            "The loop condition while l1 or l2 or carry covers ALL cases in one expression."
        ),
        N.callout(
            "Analogy: Think of adding two columns of digits on paper. "
            "The reversed list is like reading the paper from right to left — "
            "ones first, then tens, then hundreds. Perfect order for carry propagation.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0)", {"code": True}),
                   " — Sentinel node. The real result list starts at dummy.next. "
                   "Avoids special-casing the first node append."])),
    N.para(N.rich([("cur = dummy", {"code": True}),
                   " — Build pointer. Always points to the last appended result node."])),
    N.para(N.rich([("carry = 0", {"code": True}),
                   " — Carry from previous column. Initialized to 0 before any column is processed."])),
    N.para(N.rich([("while l1 or l2 or carry:", {"code": True}),
                   " — The critical condition. Continues while: either input list has nodes, OR a carry "
                   "still needs to be emitted. All three edge cases handled in one line."])),
    N.para(N.rich([("v1 = l1.val if l1 else 0", {"code": True}),
                   " — Safe digit extraction. Returns 0 instead of raising AttributeError when l1 is None. "
                   "Handles lists of different lengths transparently."])),
    N.para(N.rich([("total = v1 + v2 + carry", {"code": True}),
                   " — Column sum. Max value is 9+9+1=19. Exactly the three values that determine the column output."])),
    N.para(N.rich([("carry = total // 10", {"code": True}),
                   " — Carry out. 19//10=1, 9//10=0. Integer division by 10 extracts the tens digit."])),
    N.para(N.rich([("cur.next = ListNode(total % 10)", {"code": True}),
                   " — Append result node. 19%10=9, 10%10=0. Modulo extracts the units digit."])),
    N.para(N.rich([("if l1: l1 = l1.next", {"code": True}),
                   " — Conditional advance. Only moves l1 if it's not already null (avoids None.next)."])),
    N.para(N.rich([("return dummy.next", {"code": True}),
                   " — Skip the sentinel node (which has value 0 and was never a real digit). "
                   "Returns the actual first result node."])),
    N.divider(),
]

# ── Solution 2: Recursive ──
blocks += [
    N.h2("Solution 2 — Recursive (Elegant, Interview Bonus)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The recursive structure follows naturally from the problem: "
            "the result for position i depends on the digits at position i and the carry from position i-1. "
            "That's a classic recursive definition."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "For very long lists (e.g., numbers with 10,000 digits), recursion hits Python's default "
            "stack limit (~1000 frames). The iterative solution is safer in production. "
            "Mention this trade-off before presenting the recursive version."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Add the current digits + carry, create a node for the current digit, "
            "then recurse for the rest. The base case is when both lists are exhausted AND carry is 0."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Pass carry as a parameter to the recursive call. "
            "Base case: return None when l1, l2, and carry are all zero. "
            "Current node value = (v1 + v2 + carry) % 10. "
            "Next node = recurse with l1.next, l2.next, and new carry."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not l1 and not l2 and carry == 0: return None", {"code": True}),
                   " — Base case: all input exhausted AND no carry left. Nothing more to produce."])),
    N.para(N.rich([("total = v1 + v2 + carry", {"code": True}),
                   " — Same column arithmetic as iterative version."])),
    N.para(N.rich([("node = ListNode(total % 10)", {"code": True}),
                   " — Create result node for this position."])),
    N.para(N.rich([("node.next = addTwoNumbers(l1.next, l2.next, total // 10)", {"code": True}),
                   " — Recurse for the next column, passing the carry. "
                   "The recursive call builds the rest of the list."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Iterative (Dummy Head)", "O(max(m,n))", "O(max(m,n))"],
        ["Recursive", "O(max(m,n))", "O(max(m,n)) stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Digit by Digit with Carry; Dummy Head (construction pattern)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Numbers encoded as linked lists or arrays. "
        "(2) Need to process corresponding positions of two sequences simultaneously. "
        "(3) A carry or borrow propagates between positions. "
        "(4) Problem mentions 'digits stored in reverse order' or 'most significant digit first'. "
        "Signal words: addition, subtraction, multiplication of large numbers, base conversion.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Plus One", {"bold": True}), " (Easy) — Increment integer array by 1; carry propagation from last digit (#66)"])),
    N.bullet(N.rich([("Add Binary", {"bold": True}), " (Easy) — Same digit-by-digit at base 2: digit=total%2, carry=total//2 (#67)"])),
    N.bullet(N.rich([("Add Strings", {"bold": True}), " (Easy) — Add two large numbers as strings; same carry logic, right-to-left traversal (#415)"])),
    N.bullet(N.rich([("Add Two Numbers II", {"bold": True}), " (Medium) — Most-significant-first; use stacks to reverse, then same carry algorithm (#445)"])),
    N.bullet(N.rich([("Multiply Strings", {"bold": True}), " (Medium) — Multiply large numbers as strings; distribute partial products with carry into result array (#43)"])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — Same dummy-head + parallel traversal pattern; merging instead of arithmetic (#21)"])),
    N.para("These problems share the same core technique: parallel traversal of two sequences with a running state (carry/borrow) that propagates between positions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section. Sub-Pattern: Digit by Digit with Carry", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("add_two_numbers")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Step 4: Append all blocks ────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
