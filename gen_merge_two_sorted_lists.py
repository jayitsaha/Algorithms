"""
gen_merge_two_sorted_lists.py
Regenerate the Notion page for LeetCode #21 Merge Two Sorted Lists in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c6-b418-cb786ecb3ae1"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=21,
    pattern="Linked List",
    subpatterns=["Recursive Merge"],
    tc="O(m+n)",
    sc="O(m+n)",
    key_insight="Pick the smaller head, then recursively wire its .next to the merge of its remainder and the other list.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────
print("Wiping old page content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given the heads of two sorted linked lists ", {}),
        ("list1", {"code": True}),
        (" and ", {}),
        ("list2", {"code": True}),
        (". Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.", {})
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("The number of nodes in both lists is in [0, 50]. Node values are in [-100, 100]. Both lists are sorted in non-decreasing order.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Recursive ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive Merge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have two sorted sequences and need one sorted sequence. The key question at each step is simply: which of the two current heads is smaller? That node belongs next in the merged result."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach might collect all values, sort them, then rebuild a list. This is O((m+n) log(m+n)) time and O(m+n) space. It also doesn't use the fact that both inputs are already sorted — we can do O(m+n) time by leveraging the sorted property."),
        N.h4("The Key Observation"),
        N.para("The next node in the merged result is always the smaller of the two current heads. After choosing it, the problem reduces to: merge the rest of that chosen list with the entire other list. This is the same problem on a smaller input — perfect for recursion."),
        N.h4("Building the Solution"),
        N.para("Define merge(l1, l2). Base cases: if l1 is null return l2; if l2 is null return l1. Then compare heads: if l1.val <= l2.val, set l1.next = merge(l1.next, l2) and return l1. Otherwise set l2.next = merge(l1, l2.next) and return l2. Each call advances exactly one pointer."),
        N.callout(
            "Analogy: Two sorted decks of cards face-up. Always take the smaller top card. After taking it, the problem is identical — just with one fewer card in that deck.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def mergeTwoLists(l1, l2):\n"
        "    if l1 is None:    # Base case: l1 exhausted\n"
        "        return l2\n"
        "    if l2 is None:    # Base case: l2 exhausted\n"
        "        return l1\n"
        "    if l1.val <= l2.val:\n"
        "        l1.next = mergeTwoLists(l1.next, l2)  # l1 wins\n"
        "        return l1\n"
        "    else:\n"
        "        l2.next = mergeTwoLists(l1, l2.next)  # l2 wins\n"
        "        return l2"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if l1 is None: return l2", {"code": True}), (" — Base case: l1 has no nodes left. The remaining l2 is already sorted, so return it as-is. This terminates the recursion.", {})])),
    N.para(N.rich([("if l2 is None: return l1", {"code": True}), (" — Symmetric base case for l2 being exhausted.", {})])),
    N.para(N.rich([("if l1.val <= l2.val:", {"code": True}), (" — Compare the two heads. Tie goes to l1 (either works; this choice is arbitrary).", {})])),
    N.para(N.rich([("l1.next = mergeTwoLists(l1.next, l2)", {"code": True}), (" — Wire l1's next to the result of merging l1's remainder with the full l2. We advance only l1; l2 is passed unchanged.", {})])),
    N.para(N.rich([("return l1", {"code": True}), (" — Return l1 as the head of this sub-merge. The caller will wire this node as its own .next.", {})])),
    N.para(N.rich([("l2.next = mergeTwoLists(l1, l2.next)", {"code": True}), (" — Symmetric for the l2 branch: advance l2, pass l1 forward unchanged.", {})])),
    N.divider(),
]

# ── Solution 2: Iterative ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative with Dummy Head (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same comparison logic as recursive, but we simulate it with a loop. We maintain a 'current tail' pointer and keep attaching the smaller head to it."),
        N.h4("What Doesn't Work"),
        N.para("The recursive version uses O(m+n) call stack space. For very long lists (millions of nodes), this causes a stack overflow. We need an iterative approach."),
        N.h4("The Key Observation"),
        N.para("We need to track 'where does the next node attach?' A dummy sentinel node as the starting point lets cur.next always be valid — no special case for the first node."),
        N.h4("Building the Solution"),
        N.para("Create dummy = ListNode(0), cur = dummy. While both lists are non-empty, compare heads, attach the smaller to cur.next, advance that list and advance cur. When one list empties, attach the other's remainder in O(1). Return dummy.next."),
        N.callout(
            "The dummy node trick: start cur pointing at a throwaway node so we never have to ask 'is this the first node?'. The answer is always dummy.next.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def mergeTwoLists(l1, l2):\n"
        "    dummy = ListNode(0)   # Sentinel head\n"
        "    cur = dummy           # Trailing pointer\n"
        "    while l1 and l2:\n"
        "        if l1.val <= l2.val:\n"
        "            cur.next = l1\n"
        "            l1 = l1.next\n"
        "        else:\n"
        "            cur.next = l2\n"
        "            l2 = l2.next\n"
        "        cur = cur.next\n"
        "    cur.next = l1 or l2   # Attach remainder\n"
        "    return dummy.next"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0); cur = dummy", {"code": True}), (" — Sentinel and trailing pointer. cur.next will always be the next slot to fill.", {})])),
    N.para(N.rich([("while l1 and l2:", {"code": True}), (" — Loop while both lists have nodes. As soon as one is exhausted, we exit.", {})])),
    N.para(N.rich([("cur.next = l1; l1 = l1.next", {"code": True}), (" — Attach l1's node, advance l1. We do NOT advance cur yet.", {})])),
    N.para(N.rich([("cur = cur.next", {"code": True}), (" — Now advance cur so it points to the node we just attached. Ready for next iteration.", {})])),
    N.para(N.rich([("cur.next = l1 or l2", {"code": True}), (" — After loop, one list is empty. Attach the other's entire remainder in O(1) — it's already sorted.", {})])),
    N.para(N.rich([("return dummy.next", {"code": True}), (" — Skip the sentinel; the real merged head is one position ahead.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive (Interview Pick)", "O(m+n)", "O(m+n) — call stack"],
        ["Iterative (Dummy Head)", "O(m+n)", "O(1) — just 3 pointers"],
    ]),
    N.para("Both solutions visit every node exactly once and perform O(1) work per node. The iterative solution is preferred in production due to its O(1) space usage."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Recursive Merge — pick the smaller head, recursively merge its remainder with the other list", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Merge two sorted sequences' → always think merge\n"
        "• Linked list + in-place manipulation → re-wire .next pointers\n"
        "• Problem structure mirrors recursive data structure → try recursion\n"
        "• Appears as subproblem in Sort List (#148) and Merge K Sorted Lists (#23)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Recursive Merge / Linked List Merge technique:"),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Apply this merge with a min-heap or divide-and-conquer (#23)", {})])),
    N.bullet(N.rich([("Sort List", {"bold": True}), (" (Medium) — Merge sort on linked list; the merge step is this exact function (#148)", {})])),
    N.bullet(N.rich([("Merge Sorted Array", {"bold": True}), (" (Easy) — Same merge idea on arrays; fill from the back for O(1) space (#88)", {})])),
    N.bullet(N.rich([("Add Two Numbers", {"bold": True}), (" (Medium) — Simultaneous traversal of two linked lists, similar structure (#2)", {})])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), (" (Easy) — Another recursive linked-list pattern; builds result bottom-up (#206)", {})])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), (" (Medium) — Combines find-middle, reverse, and merge into one problem (#143)", {})])),
    N.para("These problems share the same core technique: merge sorted sequences by always choosing the local minimum head."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section → Merge sub-pattern", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("merge_two_sorted_lists")),
    N.para(N.rich([
        ("Step through the recursive algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
