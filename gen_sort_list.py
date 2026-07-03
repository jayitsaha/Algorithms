"""
gen_sort_list.py — Notion update for Sort List (#148, Medium, Merge Sort on Linked List)
Notion page ID: 39193418-809c-8190-8be2-c0978198d146 (update IN-PLACE)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8190-8be2-c0978198d146"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=148,
    pattern="Sorting",
    subpatterns=["Merge Sort on Linked List"],
    tc="O(n log n)",
    sc="O(log n)",
    key_insight="Merge sort is the natural O(n log n) sort for linked lists: fast/slow split + pointer-rewiring merge, no random access needed.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old content ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Rebuild body ───────────────────────────────────────────────────────
SOLUTION_1 = '''def sortList(head):
    # Base case: 0 or 1 nodes are already sorted
    if not head or not head.next:
        return head
    # ── SPLIT: fast/slow pointer to find midpoint ──
    slow, fast = head, head.next   # fast starts 1 ahead (prevents empty-right bug)
    while fast and fast.next:
        slow = slow.next           # tortoise: 1 step
        fast = fast.next.next      # hare: 2 steps
    mid = slow.next                # start of right half
    slow.next = None               # ★ disconnect! creates two independent chains
    # ── RECURSE ──
    left  = sortList(head)         # sort left half [head..slow]
    right = sortList(mid)          # sort right half [mid..end]
    # ── MERGE: combine two sorted lists ──
    dummy = ListNode(0)            # sentinel node
    cur = dummy
    while left and right:
        if left.val <= right.val:
            cur.next = left
            left = left.next
        else:
            cur.next = right
            right = right.next
        cur = cur.next
    cur.next = left or right       # attach non-empty remainder
    return dummy.next              # skip sentinel, return sorted head'''

SOLUTION_2 = '''def sortList_array(head):
    """Brute Force: collect values, sort array, write back — O(n log n) / O(n)"""
    if not head:
        return head
    # Collect all values into a Python list
    vals, cur = [], head
    while cur:
        vals.append(cur.val)
        cur = cur.next
    vals.sort()           # Python Timsort: O(n log n)
    # Write sorted values back into existing nodes
    cur = head
    for v in vals:
        cur.val = v
        cur = cur.next
    return head'''

SOLUTION_3 = '''def sortList_bottomUp(head):
    """Bottom-Up Iterative Merge Sort — O(n log n) / O(1) true constant space"""
    if not head:
        return head
    # Count total nodes
    n, node = 0, head
    while node:
        n += 1
        node = node.next
    dummy = ListNode(0)
    dummy.next = head
    size = 1
    while size < n:
        cur = dummy.next
        tail = dummy
        while cur:
            left = cur
            right = split_k(left, size)      # split off 'size' nodes
            cur   = split_k(right, size)     # split off 'size' nodes, rest is next batch
            merged_tail = merge_two(tail, left, right)
            tail = merged_tail
        size <<= 1   # double the merge window each pass
    return dummy.next

# Helper: split k nodes from list, return head of remainder
def split_k(node, k):
    for _ in range(k - 1):
        if node:
            node = node.next
    if not node:
        return None
    rest = node.next
    node.next = None
    return rest

# Helper: merge two sorted lists, attach to tail, return new tail
def merge_two(tail, l1, l2):
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1; l1 = l1.next
        else:
            tail.next = l2; l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    while tail.next:
        tail = tail.next
    return tail'''

blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("head", {"code": True}),
        (" of a linked list, return the list sorted in ", {}),
        ("ascending order", {"bold": True}),
        (". The problem asks for O(n log n) time and O(1) space (constant space means bottom-up iterative; top-down recursive is O(log n) space and is the interview standard).", {})
    ])),
    N.para("Example 1: head = [4,2,1,3]  →  Output: [1,2,3,4]"),
    N.para("Example 2: head = [-1,5,3,4,0]  →  Output: [-1,0,3,4,5]"),
    N.para("Constraints: list length 0..50,000. Node values -100,000..100,000."),
    N.divider(),
]

# Solution 1: Top-Down Merge Sort (Interview Pick)
blocks += [
    N.h2("Solution 1 — Top-Down Merge Sort (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("We need to sort a linked list in O(n log n). The key constraint is that linked lists don't support O(1) random access by index — reaching index k costs O(k). This rules out heapsort and efficient quicksort pivoting. But merge sort only needs sequential traversal, which linked lists provide natively. The two operations we need are: split a list in half, and merge two sorted lists — both are clean on linked lists."),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("Insertion sort is O(n²) — too slow. Quicksort's average case is O(n log n) but worst case O(n²) on a linked list without good pivot selection (and swapping pivots requires O(n) traversal). Heapsort requires building a heap which needs array-like random access. None of these fit."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("Merge sort decomposes naturally: (1) find the midpoint in O(n) using fast/slow pointers, (2) recursively sort each half, (3) merge two sorted lists in O(n) with only pointer rewiring. There is no random access required anywhere. Splitting and merging are the only primitives needed."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Initialize slow=head, fast=head.next (one ahead to handle 2-node edge case). Advance slow by 1 and fast by 2 until fast can't move — slow now sits at the last node of the left half. Set slow.next=None (CRITICAL: this disconnects the two halves). Recurse on each half. Then merge: use a dummy sentinel, compare front nodes, pick smaller, advance. At the end attach any remainder."),
        N.callout("Analogy: Like sorting a deck of cards by repeatedly splitting the deck in half until you have single cards, then merging pairs face-up — always picking the lower card from the front of either pile.", "🃏", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next:", {"code": True}), (" — Base case: 0 or 1 nodes are trivially sorted. Return immediately. This is the recursion's termination condition.", {})])),
    N.para(N.rich([("slow, fast = head, head.next", {"code": True}), (" — Initialize both pointers. fast starts one step ahead (at head.next, not head) to prevent the empty-right-half bug on 2-node lists.", {})])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), (" — Continue while fast can safely take 2 more steps. 'fast' checks fast itself isn't None; 'fast.next' checks fast.next isn't None (so fast.next.next is valid).", {})])),
    N.para(N.rich([("slow = slow.next; fast = fast.next.next", {"code": True}), (" — Tortoise/hare: slow moves 1 step, fast moves 2. When fast hits the end, slow is at the midpoint.", {})])),
    N.para(N.rich([("mid = slow.next", {"code": True}), (" — mid is the start of the right half.", {})])),
    N.para(N.rich([("slow.next = None", {"code": True}), (" — The critical disconnect. Without this, both recursive calls share the same chain and never terminate.", {})])),
    N.para(N.rich([("left = sortList(head); right = sortList(mid)", {"code": True}), (" — Recursively sort each half. Each returns its own fully sorted linked list.", {})])),
    N.para(N.rich([("dummy = ListNode(0); cur = dummy", {"code": True}), (" — Sentinel node eliminates special-casing the very first node attachment.", {})])),
    N.para(N.rich([("if left.val <= right.val: cur.next = left; left = left.next", {"code": True}), (" — Pick from left when it's ≤ right. Attach, advance left pointer.", {})])),
    N.para(N.rich([("else: cur.next = right; right = right.next", {"code": True}), (" — Pick from right when it's strictly smaller. Attach, advance right pointer.", {})])),
    N.para(N.rich([("cur = cur.next", {"code": True}), (" — Advance the result chain tail pointer.", {})])),
    N.para(N.rich([("cur.next = left or right", {"code": True}), (" — Attach whichever list still has nodes. 'left or right' returns left if truthy, else right. This attaches the remaining sorted suffix in one shot.", {})])),
    N.para(N.rich([("return dummy.next", {"code": True}), (" — Skip the sentinel; dummy.next is the true head of the sorted list.", {})])),
    N.callout("Key bug to avoid: forgetting slow.next = None before recursing. Both halves must be physically disconnected chains.", "⚠️", "yellow_background"),
    N.divider(),
]

# Solution 2: Brute Force Array
blocks += [
    N.h2("Solution 2 — Brute Force: Collect into Array, Sort, Rebuild"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("What if we didn't care about space? Sorting arrays is easy — Python's built-in sort is O(n log n). We can extract all values, sort them, then write them back into the existing nodes."),
        N.para(N.rich([("What Doesn't Work About This Long-Term", {"bold": True})])),
        N.para("This approach uses O(n) extra space for the values array. The problem asks for O(1) space. But this approach is an excellent first proposal in an interview — it shows you know how to solve the core problem before optimizing."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("The linked list structure doesn't change — we only overwrite the node values. This sidesteps all pointer manipulation. It's a valid solution, just space-suboptimal."),
        N.callout("Propose this approach first in an interview, then offer to optimize: 'I can solve this in O(n) extra space trivially — want me to then optimize to O(log n) or O(1) space?'", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("vals, cur = [], head", {"code": True}), (" — Initialize values list and a traversal pointer.", {})])),
    N.para(N.rich([("while cur: vals.append(cur.val); cur = cur.next", {"code": True}), (" — Single O(n) pass to collect all node values.", {})])),
    N.para(N.rich([("vals.sort()", {"code": True}), (" — Python's Timsort in O(n log n) time, O(n) space.", {})])),
    N.para(N.rich([("for v in vals: cur.val = v; cur = cur.next", {"code": True}), (" — Second O(n) pass to overwrite node values in sorted order. The node structure (next pointers) is untouched.", {})])),
    N.para(N.rich([("return head", {"code": True}), (" — Same head node, but now the values are sorted.", {})])),
    N.divider(),
]

# Solution 3: Bottom-Up (bonus)
blocks += [
    N.h2("Solution 3 — Bottom-Up Iterative Merge Sort (True O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("The top-down approach uses O(log n) call stack space. To eliminate it entirely, we reverse the recursion direction: start by merging pairs of single nodes, then pairs of 2-node lists, then pairs of 4-node lists, doubling each pass."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("After log(n) passes (each doubling the merge window), the entire list is sorted. Each pass is O(n) work. No recursion stack is ever used — just iterative pointer manipulation."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Count n (the list length). Start size=1. Each pass: sweep the list, split groups of 'size' nodes, merge adjacent pairs, stitch results together. Repeat with size*=2 until size >= n."),
        N.callout("Bottom-up is harder to implement correctly under interview pressure. Lead with top-down, offer bottom-up as the follow-up for O(1) space.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_3),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Array)", "O(n log n)", "O(n)"],
        ["Top-Down Merge Sort (Interview Pick)", "O(n log n)", "O(log n)"],
        ["Bottom-Up Merge Sort", "O(n log n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Merge Sort on Linked List", {})])),
    N.para(N.rich([("Related Sub-Skills: ", {"bold": True}), ("Fast/Slow Pointer (to find midpoint), Merge Two Sorted Lists (LeetCode #21)", {})])),
    N.callout(
        "When to recognize this pattern: Problem says 'sort a linked list' with O(n log n) time — merge sort is the only clean fit. Also any divide-and-conquer on a linked list that needs O(n) split + O(n) combine.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or closely related sub-skills:"),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), (" (Easy) — The exact merge sub-routine used in every merge step of this problem (#21)", {})])),
    N.bullet(N.rich([("Merge k Sorted Lists", {"bold": True}), (" (Hard) — Extends merge to k lists using a min-heap or divide-and-conquer on the merge step (#23)", {})])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), (" (Easy) — Fast/slow pointer technique in isolation — the split sub-skill used here (#876)", {})])),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), (" (Easy) — Fast/slow pointer for cycle detection; same pointer pair, different termination (#141)", {})])),
    N.bullet(N.rich([("Insertion Sort List", {"bold": True}), (" (Medium) — O(n²) alternative; shows exactly why merge sort wins for large inputs (#147)", {})])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), (" (Medium) — Core pointer manipulation on linked list sub-ranges, related structural skill (#92)", {})])),
    N.para("These problems share the core linked-list pointer manipulation and divide-and-conquer structure."),
]

# Embed explainer
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sort_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
