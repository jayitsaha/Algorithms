"""
gen_palindrome_linked_list.py
Notion in-place update for LeetCode #234 Palindrome Linked List.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81ff-993b-dcd7bd732739"
SLUG = "palindrome_linked_list"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=234,
    pattern="Linked List",
    subpatterns=["Fast-Slow Pointer", "Reversal"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Find middle with fast-slow pointers, reverse second half in-place, compare halves.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the head of a singly linked list, return ", {}),
        ("true", {"code": True}),
        (" if it is a palindrome or ", {}),
        ("false", {"code": True}),
        (" otherwise.", {}),
        ("\n\nConstraints: O(n) time, O(1) extra space.", {"italic": True, "color": "gray"}),
    ])),
    N.divider(),
]

# ── Solution 1 — Reverse Second Half (Interview Pick) ──────────────────────────
blocks += [
    N.h2("Solution 1 — Reverse Second Half (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to check if a linked list reads the same forwards and backwards — but we can't index randomly into a linked list like an array, and we're not allowed to use O(n) extra space to copy values."),
        N.h4("What Doesn't Work"),
        N.para("Array conversion: walk the list, append all values to a Python list, check if list == list[::-1]. Correct, but O(n) space. A stack holding the first half: also O(n/2) space. We need something truly in-place."),
        N.h4("The Key Observation"),
        N.para("A palindrome's first half equals its second half REVERSED. So if we reverse the second half in-place (modifying only pointers, not creating new nodes), we can compare two halves directly using two pointers — zero extra memory beyond a few pointer variables."),
        N.h4("Building the Solution"),
        N.para("This breaks into exactly 3 phases:\n1. Find the midpoint using the fast-slow (tortoise-hare) pointer pattern — fast moves 2×, when it can't advance slow is at the middle.\n2. Reverse the second half starting from slow.next (skip the center for odd-length lists) using the standard three-pointer reversal (prev / curr / nxt).\n3. Walk left from head and right from the reversed-half head, comparing values — any mismatch returns False, otherwise True."),
        N.callout(
            "Analogy: It's like folding a piece of paper in half and checking if every character on the left side matches the right side. The fold = find the middle. Flipping the right half = the in-place reversal. Overlapping = the comparison.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isPalindrome(head: ListNode) -> bool:\n"
        "    slow, fast = head, head          # both start at head\n"
        "    while fast and fast.next:        # fast moves 2x slower\n"
        "        slow = slow.next\n"
        "        fast = fast.next.next\n"
        "    # slow is now at the middle (for odd: true center; for even: end of first half)\n"
        "    prev, curr = None, slow.next     # skip center for odd; start reversal at slow.next\n"
        "    while curr:\n"
        "        nxt = curr.next              # save next before overwriting\n"
        "        curr.next = prev             # flip pointer backward\n"
        "        prev = curr                  # advance prev\n"
        "        curr = nxt                   # advance curr\n"
        "    # prev is now the head of the reversed second half\n"
        "    left, right = head, prev\n"
        "    while right:                     # reversed half may be shorter (odd lists)\n"
        "        if left.val != right.val:\n"
        "            return False\n"
        "        left = left.next\n"
        "        right = right.next\n"
        "    return True"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("slow, fast = head, head", {"code": True}), " — Initialize both pointers at the head. fast will move twice as fast, so when it reaches the end, slow is at the midpoint."])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), " — Both conditions needed: fast must exist (not gone past end) AND fast.next must exist (fast needs to take 2 steps safely)."])),
    N.para(N.rich([("slow = slow.next / fast = fast.next.next", {"code": True}), " — Advance at 1× and 2× speeds respectively. When the loop exits, slow is at the midpoint."])),
    N.para(N.rich([("prev, curr = None, slow.next", {"code": True}), " — For odd-length lists, slow lands on the center node — skip it. Start reversal from slow.next. prev=None will become the tail of the reversed sublist."])),
    N.para(N.rich([("nxt = curr.next", {"code": True}), " — Save next pointer before we overwrite curr.next. Critical — losing this reference would break the traversal."])),
    N.para(N.rich([("curr.next = prev", {"code": True}), " — The flip: point current node backward (toward the already-reversed portion)."])),
    N.para(N.rich([("prev = curr; curr = nxt", {"code": True}), " — Advance both: prev now includes current node in the reversed sublist; curr moves to the saved next."])),
    N.para(N.rich([("left, right = head, prev", {"code": True}), " — Set up the comparison. left walks the first half forward from head; right walks the reversed second half forward from prev (which is now the reversed-half head)."])),
    N.para(N.rich([("while right:", {"code": True}), " — Stop when the reversed half is exhausted. For odd-length lists this is 1 node shorter than the first half — that's correct because the center doesn't need comparison."])),
    N.para(N.rich([("if left.val != right.val: return False", {"code": True}), " — Mismatch found: the list is not a palindrome."])),
    N.para(N.rich([("return True", {"code": True}), " — All pairs in the two halves matched. The list is a palindrome."])),
    N.divider(),
]

# ── Solution 2 — Array Conversion ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Array Conversion (Simple, O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we could index the list randomly like an array, palindrome checking is trivial: compare position i with position n-1-i. We can't do that with a linked list directly — but we can copy the values into an array first."),
        N.h4("What Doesn't Work"),
        N.para("Nothing doesn't work here — this is the simplest correct approach. The only cost is O(n) extra space, which violates the follow-up constraint but is perfectly valid otherwise."),
        N.h4("The Key Observation"),
        N.para("Python's list supports two-pointer comparison with the slicing shortcut: vals == vals[::-1] checks all positions simultaneously. This makes the code a single clean return statement after collecting the values."),
        N.h4("Building the Solution"),
        N.para("Walk the linked list once, collecting each node's value into a list. Then use Python's built-in palindrome idiom: check if the list equals its own reverse. O(n) time, O(n) space."),
    ]),
    N.h3("Code"),
    N.code(
        "def isPalindrome(head: ListNode) -> bool:\n"
        "    vals = []\n"
        "    while head:\n"
        "        vals.append(head.val)\n"
        "        head = head.next\n"
        "    return vals == vals[::-1]    # True if forward == backward"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("vals = []", {"code": True}), " — Create an empty list to hold the node values."])),
    N.para(N.rich([("while head: vals.append(head.val); head = head.next", {"code": True}), " — Traverse the linked list, appending each node's value. O(n) pass."])),
    N.para(N.rich([("return vals == vals[::-1]", {"code": True}), " — Python creates a reversed copy of vals and compares element-by-element. Equivalent to checking all i: vals[i] == vals[n-1-i]. Simple and correct, O(n) space."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Array Conversion", "O(n)", "O(n)"],
        ["Reverse Second Half (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Fast-Slow Pointer (find middle), Reversal (reverse second half in-place)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Palindrome' + 'linked list' + 'O(1) space' → fast-slow + reverse second half\n"
        "• Need the midpoint of a singly linked list without knowing its length? → fast-slow pointer\n"
        "• Need to compare list against its reversed form → reverse one half in-place\n"
        "• Any linked list problem requiring O(1) space and a reversal → three-pointer trick (prev/curr/nxt)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Fast-Slow Pointer + Reversal):"),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), " (Easy) — Fast-slow: if they meet, there's a cycle. Core fast-slow pattern. (#141)"])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — Fast-slow to find the exact midpoint. Direct sub-skill of this problem. (#876)"])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), " (Easy) — The fundamental three-pointer (prev/curr/nxt) in-place reversal used here. (#206)"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — Combines all three phases: find middle, reverse second half, interleave. The 'boss fight' of this pattern. (#143)"])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), " (Medium) — Fast-slow to detect cycle entry point. Extends the fast-slow invariant. (#142)"])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), " (Hard) — Reversal applied to chunks of k nodes. Extension of the reversal sub-pattern. (#25)"])),
    N.para("These problems share the same core techniques: fast-slow pointer for O(1) midpoint finding, and in-place three-pointer reversal for O(1) space list restructuring."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6 (Linked List) — Sub-Patterns: Fast-Slow Pointer, Reversal", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
