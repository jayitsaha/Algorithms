"""
gen_insert_into_a_sorted_circular_linked_list.py
Notion in-place rebuild for LeetCode #708.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8190-8f65-da540bc9c8a1"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=708,
    pattern="Linked List",
    subpatterns=["Find Correct Position"],
    tc="O(n)",
    sc="O(1)",
    key_insight="One descending edge (max→min seam) defines 3 insertion cases: normal gap, wrap-around extreme, all-same fallback.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old content ────────────────────────────────────────────────────
print("Wiping old blocks...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} blocks")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a reference to a node in a sorted circular singly linked list, insert a new node with value "),
        ("insertVal", {"code": True}),
        (" such that the list remains sorted in non-descending order. Return any node of the modified list. "
         "The head parameter can be null, indicating an empty list."),
    ])),
    N.divider(),
]

# ── Solution 1 ──────────────────────────────────────────────────────────────
SOLUTION_1_CODE = '''\
def insert(head, insertVal: int):
    new_node = Node(insertVal)
    if not head:
        new_node.next = new_node   # self-loop: a single-node circular list
        return new_node
    curr = head
    while True:
        # Case 1: value fits in a normal ascending gap
        if curr.val <= insertVal <= curr.next.val:
            break
        # Case 2: curr is the max node (wrap-around seam)
        if curr.val > curr.next.val:
            if insertVal >= curr.val or insertVal <= curr.next.val:
                break              # new max OR new min — both go here
        # Case 3: completed full circle (all values equal)
        if curr.next == head:
            break
        curr = curr.next
    # Wire new node between curr and curr.next
    new_node.next = curr.next      # MUST be first — saves the old next reference
    curr.next = new_node
    return head
'''

blocks += [
    N.h2("Solution 1 — Three-Case Circular Traversal (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A sorted circular linked list has values that increase as you traverse — until one 'seam' where the largest value wraps back to the smallest. Inserting into this structure means finding where in the circle a new value belongs."),
        N.h4("What Doesn't Work"),
        N.para("Converting to an array and sorting (O(n log n), O(n) space) ignores the fact the list is already sorted. You only need to find one correct insertion point — not re-sort everything."),
        N.h4("The Key Observation"),
        N.para("In a sorted circular list, every adjacent pair is non-descending EXCEPT the one seam from the max back to the min. This means there are exactly three scenarios for where a new value can go: (1) a normal ascending gap between two nodes, (2) at the seam because it's a new extreme, or (3) anywhere because all values are equal."),
        N.h4("Building the Solution"),
        N.para("Traverse with a curr pointer. At each pair (curr, curr.next), check if any of the three cases applies. If Case 1 or Case 2 matches, break and insert. If we complete a full circle, Case 3 fires and we insert after curr. After breaking, wire: new_node.next = curr.next first, then curr.next = new_node."),
        N.callout(
            "Analogy: Imagine values on a clock face, 1 o'clock to 12 o'clock. "
            "Insert a new 'time' by finding where it fits on the ascending arc, or at the midnight seam if it's a new record high or low.",
            "🕐", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("new_node = Node(insertVal)", {"code": True}), " — Create the new node before anything else. We'll wire its next pointer at the end."])),
    N.para(N.rich([("if not head:", {"code": True}), " — Handle the empty list specially: a single node in a circular list must point to itself (self-loop). Return it immediately."])),
    N.para(N.rich([("curr = head", {"code": True}), " — Start traversal from the given node. In a circular list, every starting point is equivalent."])),
    N.para(N.rich([("while True:", {"code": True}), " — Infinite loop with explicit break conditions. We're guaranteed to terminate because Case 3 catches the full-circle scenario."])),
    N.para(N.rich([("if curr.val <= insertVal <= curr.next.val:", {"code": True}), " — Case 1: normal ascending gap. The new value fits between curr and curr.next. Both nodes are on the ascending side of the seam."])),
    N.para(N.rich([("if curr.val > curr.next.val:", {"code": True}), " — Detect the seam: curr is the max, curr.next is the min. This descending edge is the unique wrap-around point in the circle."])),
    N.para(N.rich([("if insertVal >= curr.val or insertVal <= curr.next.val:", {"code": True}), " — Case 2: at the seam, check if insertVal is a new maximum (≥ curr.val) OR a new minimum (≤ curr.next.val). Both extremes insert at the same point."])),
    N.para(N.rich([("if curr.next == head: break", {"code": True}), " — Case 3: we've looped back to the start without matching. All values must be equal — insert anywhere."])),
    N.para(N.rich([("curr = curr.next", {"code": True}), " — Advance to the next node. We keep going until one of the three cases fires."])),
    N.para(N.rich([("new_node.next = curr.next", {"code": True}), " — CRITICAL: save the reference to curr's old next node into new_node.next BEFORE overwriting curr.next. Doing it in the wrong order creates a self-loop."])),
    N.para(N.rich([("curr.next = new_node", {"code": True}), " — Redirect curr to point to the new node. The chain is now: curr → new_node → (old curr.next) → ..."])),
    N.para(N.rich([("return head", {"code": True}), " — Return any node. The original head is still valid (we never moved it). The list is still circular and now contains the new value."])),
    N.divider(),
]

# ── Solution 2 ──────────────────────────────────────────────────────────────
SOLUTION_2_CODE = '''\
# Brute Force — for comparison only, not recommended
def insert_brute(head, insertVal: int):
    new_node = Node(insertVal)
    if not head:
        new_node.next = new_node
        return new_node
    # Collect all values from the circular list
    vals = []
    curr = head
    while True:
        vals.append(curr.val)
        curr = curr.next
        if curr == head:
            break
    vals.append(insertVal)
    vals.sort()  # O(n log n) — wastes the sorted structure
    # Rebuild the circular list from sorted values
    dummy = Node(0)
    tail = dummy
    for v in vals:
        tail.next = Node(v)
        tail = tail.next
    tail.next = dummy.next  # close the circle
    return dummy.next
'''

blocks += [
    N.h2("Solution 2 — Brute Force: Array + Sort + Rebuild"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Convert the circular list to a flat array of values, add the new value, sort it, then rebuild a new circular list. Simple to reason about but wasteful."),
        N.h4("What Doesn't Work"),
        N.para("Sorting is O(n log n) and requires O(n) extra space for the array. Rebuilding the list from scratch is also O(n). The sorted structure of the original list is completely ignored."),
        N.h4("The Key Observation"),
        N.para("Sorting works but is overkill. Since the list is already sorted, we only need to find one position — not sort everything. This is the insight that leads to the O(n) / O(1) solution."),
        N.h4("Building the Solution"),
        N.para("Collect all values into a list (O(n) time, O(n) space). Add insertVal. Sort (O(n log n)). Rebuild the circular list. Return any node. This is the brute force baseline — propose this first in an interview, then optimize."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("while True: ... if curr == head: break", {"code": True}), " — Traverse the circular list once to collect all values. Stop when we return to the starting node."])),
    N.para(N.rich([("vals.sort()", {"code": True}), " — Sort the collected values including the new one. O(n log n). This is the performance bottleneck — and it's unnecessary given the input is already sorted."])),
    N.para(N.rich([("tail.next = dummy.next", {"code": True}), " — Close the circle: the last node points back to the first node, creating a valid circular linked list."])),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Three-Case Traversal (Optimal)", "O(n)", "O(1)"],
        ["Brute Force (Array + Sort)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List (Section 5 — Basic Linked List Operations)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Find Correct Position — traverse to find the exact predecessor node before insertion"])),
    N.callout(
        "When to recognize this pattern: "
        "Problem says 'sorted circular linked list' + insert/delete. "
        "The sorted + circular combo means exactly one descending seam exists. "
        "Enumerate cases around that seam (normal gap, seam extremes, all-same). "
        "Also applies when you need the node just BEFORE the target position.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Find Correct Position / Linked List Manipulation):"),
    N.bullet(N.rich([("Rotate List", {"bold": True}), " (Medium) — Find the new head position after k rotations; locates the seam in the circular structure (#61)"])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Two-pointer to find the node just before the target; predecessor tracking (#19)"])),
    N.bullet(N.rich([("Partition List", {"bold": True}), " (Medium) — In-place restructuring; careful multi-pointer management required (#86)"])),
    N.bullet(N.rich([("Odd Even Linked List", {"bold": True}), " (Medium) — Rearrange by position index; track multiple pointers in one pass (#328)"])),
    N.bullet(N.rich([("Merge In Between Linked Lists", {"bold": True}), " (Medium) — Find exact splice points by position, then wire the second list in (#1669)"])),
    N.bullet(N.rich([("Copy List with Random Pointer", {"bold": True}), " (Medium) — Deep copy with additional pointers; wiring order is critical (#138)"])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium) — Find midpoint, reverse second half, interleave; multiple LL patterns combined (#143)"])),
    N.para("These problems all require finding or maintaining the correct pointer relationships in linked lists, often needing careful attention to predecessor nodes."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 5.1 (Linked Lists → Basic Linked List Operations). Sub-Pattern: Find Correct Position.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("insert_into_a_sorted_circular_linked_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
