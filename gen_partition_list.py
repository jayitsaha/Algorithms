"""
gen_partition_list.py
Regenerates the Notion page for LeetCode #86 Partition List IN-PLACE.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8127-a53e-c163a9d0f2cf"

# ── 1) Set properties ──────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=86,
    pattern="Linked List",
    subpatterns=["Two Lists (< and >=)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Split into two dummy-headed sub-lists (less / gteq), walk once, join — order preserved automatically.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────
print("Wiping old blocks...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the head of a linked list and a value ", {}),
        ("x", {"code": True}),
        (", partition it such that all nodes less than ", {}),
        ("x", {"code": True}),
        (" come before nodes greater than or equal to ", {}),
        ("x", {"code": True}),
        (". Preserve the original relative order of the nodes in each of the two partitions.", {}),
    ])),
    N.para(N.rich([
        ("Example: head = [1,4,3,2,5,2], x = 3  →  Output: [1,2,2,4,3,5]", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1: Two Dummy Lists (Interview Pick) ───────────
blocks += [
    N.h2("Solution 1 — Two Dummy Lists (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to rearrange nodes into two groups while preserving their relative order within each group. This is stable partitioning on a linked list."),
        N.h4("What Doesn't Work"),
        N.para("Swapping nodes in-place (like array two-pointer partition) would violate relative order — swapping node(4) with node(2) would break the order of other nodes in their group."),
        N.h4("The Key Observation"),
        N.para("If we build two separate sub-lists by appending nodes in traversal order, relative order is automatically preserved — any node visited earlier will be appended earlier."),
        N.h4("Building the Solution"),
        N.para("1) Create two dummy sentinel nodes (less_dummy, gteq_dummy). 2) Walk the original list; for each node, append to the appropriate sub-list. 3) Null-terminate the gteq list. 4) Connect the tails."),
        N.callout(
            "Analogy: It's like sorting mail into two trays as it arrives on the conveyor belt — you just drop each piece into the correct tray in arrival order. At the end, stack tray 1 on top of tray 2.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def partition(head, x):\n"
        "    less_dummy = ListNode(0)   # sentinel for 'less than x' sub-list\n"
        "    gteq_dummy = ListNode(0)   # sentinel for '>= x' sub-list\n"
        "    less_tail  = less_dummy    # tail pointer for less-list\n"
        "    gteq_tail  = gteq_dummy    # tail pointer for gteq-list\n"
        "    curr = head                # walk the original list\n"
        "    while curr:\n"
        "        if curr.val < x:\n"
        "            less_tail.next = curr    # append to less-list\n"
        "            less_tail = less_tail.next\n"
        "        else:\n"
        "            gteq_tail.next = curr   # append to gteq-list\n"
        "            gteq_tail = gteq_tail.next\n"
        "        curr = curr.next       # advance walker\n"
        "    gteq_tail.next = None      # CRITICAL: prevent cycle\n"
        "    less_tail.next = gteq_dummy.next  # join: less → gteq\n"
        "    return less_dummy.next     # skip sentinel, return real head"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("less_dummy = ListNode(0)", {"code": True}), " — Sentinel node for the 'less than x' sub-list. Never holds real data, just gives us a stable head to append to.")])),
    N.para(N.rich([("gteq_dummy = ListNode(0)", {"code": True}), " — Same idea for the '>= x' sub-list."])),
    N.para(N.rich([("less_tail = less_dummy", {"code": True}), " — Tail pointer starts at the dummy. We always append after tail, then advance tail."])),
    N.para(N.rich([("curr = head", {"code": True}), " — Walker pointer for the original list."])),
    N.para(N.rich([("while curr:", {"code": True}), " — Process every node exactly once. O(n) iterations total."])),
    N.para(N.rich([("if curr.val < x:", {"code": True}), " — Strictly less-than. Nodes equal to x go into the gteq group."])),
    N.para(N.rich([("less_tail.next = curr", {"code": True}), " — Splice current node onto the less-list tail."])),
    N.para(N.rich([("less_tail = less_tail.next", {"code": True}), " — Advance tail to the node we just appended."])),
    N.para(N.rich([("curr = curr.next", {"code": True}), " — Advance walker before we lose the reference to next."])),
    N.para(N.rich([("gteq_tail.next = None", {"code": True}), " — CRITICAL: The last gteq node still has its old .next pointer. Sever it to prevent a cycle in the merged list."])),
    N.para(N.rich([("less_tail.next = gteq_dummy.next", {"code": True}), " — Connect: less-list's tail → gteq-list's real head (skip the sentinel)."])),
    N.para(N.rich([("return less_dummy.next", {"code": True}), " — Skip the sentinel, return the first real node."])),
    N.divider(),
]

# ── Solution 2: Collect + Rebuild (Brute Force) ───────────
blocks += [
    N.h2("Solution 2 — Collect Values and Rebuild (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest approach: collect all 'less' values, collect all 'gteq' values, build a brand new list."),
        N.h4("What Doesn't Work Well"),
        N.para("This approach is correct but allocates O(n) new ListNode objects — wasting memory when we could simply rewire the existing nodes."),
        N.h4("The Key Observation"),
        N.para("It's easy to understand and implement, making it a good starting point to explain before optimizing to in-place pointer manipulation."),
        N.h4("Building the Solution"),
        N.para("Walk the list, append values to two Python lists. Walk the combined list, build new ListNodes. Return head."),
    ]),
    N.h3("Code"),
    N.code(
        "def partition_brute(head, x):\n"
        "    less_vals, gteq_vals = [], []\n"
        "    curr = head\n"
        "    while curr:\n"
        "        if curr.val < x:\n"
        "            less_vals.append(curr.val)\n"
        "        else:\n"
        "            gteq_vals.append(curr.val)\n"
        "        curr = curr.next\n"
        "    # Rebuild from scratch\n"
        "    dummy = ListNode(0)\n"
        "    tail = dummy\n"
        "    for v in less_vals + gteq_vals:\n"
        "        tail.next = ListNode(v)\n"
        "        tail = tail.next\n"
        "    return dummy.next"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("less_vals, gteq_vals = [], []", {"code": True}), " — Two Python lists to hold values separated by the partition."])),
    N.para(N.rich([("curr = head; while curr:", {"code": True}), " — Walk the entire linked list."])),
    N.para(N.rich([("less_vals.append(curr.val)", {"code": True}), " — Collect values, not nodes. Easy but lossy — we'd need to create new nodes."])),
    N.para(N.rich([("for v in less_vals + gteq_vals:", {"code": True}), " — Concatenate both value lists. Build new ListNode for each."])),
    N.para(N.rich([("return dummy.next", {"code": True}), " — Skip sentinel, return real head of rebuilt list."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two Dummy Lists (Optimal)", "O(n)", "O(1)"],
        ["Collect + Rebuild (Brute Force)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Lists (< and >=) — build two dummy-headed sub-lists, walk once, join at end"])),
    N.callout(
        "When to recognize this pattern: 'Partition a linked list while preserving relative order.' "
        "Any time you see 'rearrange linked list nodes by a condition without losing their order.' "
        "Two groups + ordered? Two dummy lists + join. Three groups? Three dummy lists.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Two-List / Dummy-Head pattern:"),
    N.bullet(N.rich([("Odd Even Linked List", {"bold": True}), " (Medium) — Two lists (odd-indexed, even-indexed), then join. Exact same skeleton as Partition List."])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — Dummy head + merge by value comparison. Foundational linked list pattern."])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium) — Dummy head + two-pointer gap to simplify head-removal edge case."])),
    N.bullet(N.rich([("Sort List", {"bold": True}), " (Medium) — Merge sort on linked list uses sub-list splitting and joining repeatedly."])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), " (Hard) — Complex relinking with dummy + tail pointers."])),
    N.bullet(N.rich([("Sort Colors", {"bold": True}), " (Medium) — Array analogue: Dutch National Flag, the same stable-partition idea applied to arrays."])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), " (Medium) — Linked list relinking with dummy head to avoid edge cases."])),
    N.para("These problems share the core technique: dummy head eliminates empty-list edge cases; tail pointer gives O(1) append; traverse once."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Linked List → Dummy Head pattern", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("partition_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
