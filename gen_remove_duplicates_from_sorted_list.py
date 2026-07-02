import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-810c-bc88-cb04b086c98f"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=83,
    pattern="Linked List",
    subpatterns=["Compare Adjacent Nodes"],
    tc="O(n)",
    sc="O(1)",
    key_insight="In a sorted list, duplicates are adjacent — bypass curr.next when curr.val == curr.next.val; never need extra space.",
    icon="🟢"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "),
        ("head", {"code": True}),
        (" of a "),
        ("sorted", {"bold": True}),
        (" linked list, delete all duplicates such that each element appears only once. Return the linked list "),
        ("sorted", {"italic": True}),
        (" as well.\n\nExample 1: head = [1,1,2] → [1,2]\nExample 2: head = [1,1,2,3,3] → [1,2,3]\n\nConstraints: The number of nodes in the list is in the range [0, 300]. Node values are in [-100, 100]. The list is guaranteed to be sorted in ascending order."),
    ])),
    N.divider(),
]

# ── Solution 1: Optimal (Single Pointer) ──
sol1_code = '''\
def deleteDuplicates(head):
    curr = head                        # walking pointer; head stays fixed
    while curr and curr.next:          # need both curr and a next to compare
        if curr.val == curr.next.val:  # adjacent equal = duplicate
            curr.next = curr.next.next # bypass: skip the duplicate node
        else:
            curr = curr.next           # advance to next distinct value
    return head                        # head was never moved'''

blocks += [
    N.h2("Solution 1 — Single Pointer, In-Place Bypass (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want each value to appear exactly once. Because the list is sorted, equal values always sit next to each other. So 'remove duplicates' becomes: 'whenever the node I'm looking at equals the next node, remove the next node.'"),
        N.h4("What Doesn't Work"),
        N.para("A hash set (O(n) space) works for unsorted lists but wastes space here. Sorting again would be pointless — the list is already sorted. We don't need any extra structure."),
        N.h4("The Key Observation"),
        N.para("Sorted order makes duplicates adjacent. A single pointer can compare curr to curr.next. If they match: bypass. If not: advance. This is the entire algorithm."),
        N.h4("Building the Solution"),
        N.para("1. Set curr = head.\n2. While curr and curr.next exist:\n   a. If curr.val == curr.next.val: curr.next = curr.next.next (bypass). Do NOT advance.\n   b. Else: curr = curr.next (advance).\n3. Return head.\n\nThe 'do NOT advance after bypass' rule is critical: there may be a chain of 3+ identical values."),
        N.callout(
            "Analogy: Proofreading a sorted dictionary printout. Point finger at a word, compare to next. Same? Cross out the next, keep finger. Different? Slide finger forward. Done when finger falls off the page.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("curr = head", {"code": True}), " — Walking pointer initialized to head. head is stored separately so we can return it unchanged at the end."])),
    N.para(N.rich([("while curr and curr.next:", {"code": True}), " — Loop needs two nodes: curr to read, curr.next to compare. If either is None, there is nothing left to check."])),
    N.para(N.rich([("if curr.val == curr.next.val:", {"code": True}), " — Adjacent equal values in a sorted list must be duplicates. This is the core check."])),
    N.para(N.rich([("curr.next = curr.next.next", {"code": True}), " — The bypass. We route around the duplicate. curr does NOT advance; the new curr.next might also equal curr.val (triple+ run)."])),
    N.para(N.rich([("else: curr = curr.next", {"code": True}), " — Values differ. The current node is confirmed unique in its neighborhood. Advance."])),
    N.para(N.rich([("return head", {"code": True}), " — head never moved. We only ever modified .next pointers, never head itself. Return directly."])),
    N.divider(),
]

# ── Solution 2: Hash Set (brute force / unsorted) ──
sol2_code = '''\
def deleteDuplicates_hash(head):
    seen = set()
    dummy = ListNode(0, head)   # sentinel simplifies head-removal
    prev, curr = dummy, head
    while curr:
        if curr.val in seen:
            prev.next = curr.next   # unlink duplicate
        else:
            seen.add(curr.val)
            prev = curr             # only advance prev for kept nodes
        curr = curr.next
    return dummy.next'''

blocks += [
    N.h2("Solution 2 — Hash Set with Two Pointers (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Works for both sorted AND unsorted lists. We track every value we've seen in a set. If we encounter a value we've seen before, remove its node."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly, but uses O(n) space for the hash set — wasteful when the input is sorted. Use Solution 1 for sorted lists."),
        N.h4("The Key Observation"),
        N.para("A dummy head node simplifies the two-pointer pattern. prev points to the last kept node; curr scans forward. When curr is a duplicate, we set prev.next = curr.next, unlinking it without touching prev itself."),
        N.h4("Building the Solution"),
        N.para("1. Create dummy node pointing to head.\n2. prev = dummy, curr = head.\n3. For each curr: if seen, unlink it via prev.next = curr.next. If not seen, record it and advance prev.\n4. Always advance curr.\n5. Return dummy.next."),
        N.callout("Use this approach only when the list is NOT guaranteed to be sorted, or when asked about a general deduplication algorithm.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = set()", {"code": True}), " — Hash set to record all distinct values encountered so far."])),
    N.para(N.rich([("dummy = ListNode(0, head)", {"code": True}), " — Sentinel node. Avoids special-casing when the head itself must be removed."])),
    N.para(N.rich([("if curr.val in seen:", {"code": True}), " — O(1) hash set lookup. If we've seen this value, it's a duplicate — unlink."])),
    N.para(N.rich([("prev.next = curr.next", {"code": True}), " — Bypass: prev skips over curr, so curr is no longer in the chain."])),
    N.para(N.rich([("seen.add(curr.val)", {"code": True}), " — First occurrence: record the value, advance prev to curr."])),
    N.para(N.rich([("return dummy.next", {"code": True}), " — dummy.next skips the sentinel and gives us the real head."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Single Pointer (Optimal)", "O(n)", "O(1)"],
        ["Hash Set (Brute Force)", "O(n)", "O(n)"],
        ["Recursive", "O(n)", "O(n) stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Compare Adjacent Nodes — scan with single pointer, compare curr to curr.next, bypass duplicates by rewiring .next."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Sorted linked list' + 'remove duplicates' → immediately think Compare Adjacent Nodes\n"
        "• In-place linked list modification with O(1) space required\n"
        "• Any 'keep first occurrence, discard subsequent repeats' on a sorted structure\n"
        "• When sorted order guarantees equal elements are always neighbours",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (sorted in-place pointer operations):"),
    N.bullet(N.rich([("Remove Duplicates from Sorted List II", {"bold": True}), " (Medium) — Remove ALL nodes with any duplicate values; needs dummy head + prev pointer. (#82)"])),
    N.bullet(N.rich([("Remove Duplicates from Sorted Array", {"bold": True}), " (Easy) — Same logic on an array: write pointer overwrites duplicates in-place. (#26)"])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — Compare adjacent list heads, weave sorted lists together. (#21)"])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Two-pointer with n-gap to locate and remove a specific node. (#19)"])),
    N.bullet(N.rich([("Delete Node in a Linked List", {"bold": True}), " (Medium) — Node removal without access to head; copy-forward trick. (#237)"])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — Fast/slow pointer traversal to find the midpoint. (#876)"])),
    N.para("These problems all share the core technique: traversing a linked list with a pointer and making in-place .next modifications."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section. Sub-Pattern: Compare Adjacent Nodes. Verified via Guide + analysis.", "📚", "gray_background"),
]

# ── Interactive Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_duplicates_from_sorted_list")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
