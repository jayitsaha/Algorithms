import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8148-a6d4-d38a06226f78"

# 1) Set properties
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=2095,
    pattern="Linked List",
    subpatterns=["Fast-Slow Pointers"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Fast pointer at 2x speed finds middle in one pass; slow ends at predecessor for deletion.",
    icon="🟡"
)
print("Properties set OK")

# 2) Wipe existing content
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# 3) Build body blocks
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the ", {}),
        ("head", {"code": True}),
        (" of a linked list. Delete the ", {}),
        ("middle node", {"bold": True}),
        (" and return the modified ", {}),
        ("head", {"code": True}),
        (". The middle node of a linked list of size ", {}),
        ("n", {"code": True}),
        (" is the ⌊n/2⌋th node (0-indexed). For n=5, delete index 2. For n=4, delete index 2 as well (the second middle).", {})
    ])),
    N.divider(),
]

# Solution 1 — Elegant One-Pointer
blocks += [
    N.h2("Solution 1 — Elegant Fast-Slow (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You need to delete a node without knowing the list length. To delete a node in a singly linked list, you need its predecessor. So the real task is: find the node just before the middle, in one pass."),
        N.h4("What Doesn't Work"),
        N.para("You can't use indices — linked lists don't support random access. A brute-force two-pass approach (count length, then walk n//2 steps) is O(n) and correct, but wastes a full traversal just to count."),
        N.h4("The Key Observation"),
        N.para("If fast moves at 2x speed and slow at 1x, when fast exhausts the list, slow is at the midpoint. Choosing the loop condition 'while fast.next and fast.next.next' stops slow one step BEFORE the middle — making it the predecessor, ready for direct deletion."),
        N.h4("Building the Solution"),
        N.para("1. Edge case: if head.next is None, the single node is the middle — return None.\n2. Set slow = fast = head.\n3. Loop while fast.next and fast.next.next: advance slow by 1, fast by 2.\n4. When loop ends: slow.next IS the middle. Execute slow.next = slow.next.next.\n5. Return head."),
        N.callout("Analogy: Two runners on a track. The fast runner laps at 2x speed. When the fast runner hits the wall, the slow runner is exactly halfway. That halfway point is the predecessor to the middle.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def deleteMiddle(head):
    if not head or not head.next:
        return None
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    slow.next = slow.next.next
    return head""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next: return None", {"code": True}), (" — Edge case: empty list or single node (the only node is the middle, return None).", {})])),
    N.para(N.rich([("slow = fast = head", {"code": True}), (" — Both pointers start at head (index 0).", {})])),
    N.para(N.rich([("while fast.next and fast.next.next:", {"code": True}), (" — Continue while fast can still see 2 nodes ahead. This stops slow at the predecessor of the middle.", {})])),
    N.para(N.rich([("slow = slow.next", {"code": True}), (" — slow advances 1 step per iteration.", {})])),
    N.para(N.rich([("fast = fast.next.next", {"code": True}), (" — fast advances 2 steps per iteration — the speed differential creates the halving effect.", {})])),
    N.para(N.rich([("slow.next = slow.next.next", {"code": True}), (" — slow is now the predecessor; bypass slow.next (the middle node) by pointing directly to the node after it.", {})])),
    N.para(N.rich([("return head", {"code": True}), (" — head pointer unchanged; return it. The list is modified in-place.", {})])),
    N.divider(),
]

# Solution 2 — Explicit prev
blocks += [
    N.h2("Solution 2 — Explicit prev Pointer (Teaching-Friendly)"),
    N.toggle_h3("💡 Intuition", [
        N.h4("How It Differs"),
        N.para("Same fast-slow race, but we explicitly track a 'prev' pointer that lags 1 step behind slow. When the race ends, prev IS the predecessor to the middle (slow). This makes the deletion logic more explicit: prev.next = slow.next."),
        N.callout("The condition 'while fast and fast.next' with fast starting at head makes slow land ON the middle (not before it). So we need the trailing prev to perform deletion.", "🔎", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code("""def deleteMiddle(head):
    if not head.next:
        return None
    prev, slow, fast = None, head, head
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    prev.next = slow.next
    return head""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = slow = head, fast = head", {"code": True}), (" — Three pointers. prev will trail slow by 1 node.", {})])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), (" — Loop while fast can move at all and can see at least 1 more node.", {})])),
    N.para(N.rich([("prev = slow", {"code": True}), (" — CRITICAL: capture slow's current position before advancing. Must come BEFORE slow = slow.next.", {})])),
    N.para(N.rich([("slow = slow.next; fast = fast.next.next", {"code": True}), (" — Advance both pointers.", {})])),
    N.para(N.rich([("prev.next = slow.next", {"code": True}), (" — slow IS the middle; prev is its predecessor. Bypass slow.", {})])),
    N.divider(),
]

# Solution 3 — Two-Pass
blocks += [
    N.h2("Solution 3 — Two-Pass Count (Clearest Logic)"),
    N.h3("Code"),
    N.code("""def deleteMiddle(head):
    n, curr = 0, head
    while curr:
        n += 1
        curr = curr.next
    if n == 1:
        return None
    curr = head
    for _ in range(n // 2 - 1):
        curr = curr.next
    curr.next = curr.next.next
    return head""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n, curr = 0, head", {"code": True}), (" — Count the list length with one full traversal.", {})])),
    N.para(N.rich([("if n == 1: return None", {"code": True}), (" — Single node edge case.", {})])),
    N.para(N.rich([("for _ in range(n // 2 - 1):", {"code": True}), (" — Walk n//2 - 1 steps from head to land at the predecessor of the middle (index n//2).", {})])),
    N.para(N.rich([("curr.next = curr.next.next", {"code": True}), (" — Skip the middle node.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Passes"],
        ["Fast-Slow (Solution 1 & 2)", "O(n)", "O(1)", "1"],
        ["Two-Pass Count (Solution 3)", "O(n)", "O(1)", "2"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Fast-Slow Pointers", {})])),
    N.callout("When to recognize: Problem asks to find/delete middle of list, detect cycle, find start of cycle, find kth from end, or check palindrome — all without knowing the length in advance.", "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Fast-Slow Pointer technique:"),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), (" (Easy) — Same fast-slow setup; return slow directly instead of deleting (#876)", {})])),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), (" (Easy) — Fast and slow meet iff a cycle exists (#141)", {})])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), (" (Medium) — Find cycle entry using distance math after detection (#142)", {})])),
    N.bullet(N.rich([("Remove Nth Node From End", {"bold": True}), (" (Medium) — Two pointers N apart; advance together until fast hits null (#19)", {})])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), (" (Easy) — Find middle, reverse second half, compare halves (#234)", {})])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), (" (Medium) — Find middle, reverse second half, interleave the two halves (#143)", {})])),
    N.para("These problems all exploit the same core invariant: fast at 2x speed reaches the end when slow is at the midpoint."),
    N.callout("📚 Reference: Pattern Guide — Linked List → Fast-Slow Pointer sub-pattern", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("delete_the_middle_node_of_a_linked_list")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
