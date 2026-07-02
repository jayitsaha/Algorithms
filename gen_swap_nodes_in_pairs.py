"""
gen_swap_nodes_in_pairs.py
Notion regeneration for LeetCode #24 — Swap Nodes in Pairs (Medium)
Pattern: Linked List | Sub-pattern: Iterative Pair Swap
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f6-a37b-ec9c0b5b2c74"
SLUG    = "swap_nodes_in_pairs"

# ── 1) Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 24,
    pattern     = "Linked List",
    subpatterns = ["Iterative Pair Swap"],
    tc          = "O(n)",
    sc          = "O(1)",
    key_insight = "Use a dummy head so every pair has a valid prev; save nxt before three-step rewire: prev→b, b→a, a→nxt.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build blocks ──────────────────────────────────────────────────────────
blocks = []

# PROBLEM
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("head", {"code": True}),
        (" of a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (only node pointer changes are allowed).", {}),
    ])),
    N.para("Example: 1→2→3→4 becomes 2→1→4→3."),
    N.divider(),
]

# ── SOLUTION 1 — ITERATIVE (Interview Pick) ──────────────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative with Dummy Head (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to reverse the order of every consecutive pair of nodes. We can't touch values, so we must rewire the .next pointers. The tricky part: the 'tail' of each swapped pair must point to the new head of the next pair — a cross-pair stitching problem."),
        N.h4("What Doesn't Work"),
        N.para("Swapping node values would violate the constraint. Converting to an array and back uses O(n) space. A naive single-pass without saving the 'rest of list' pointer loses access to the tail permanently."),
        N.h4("The Key Observation"),
        N.para("Every pair swap needs exactly three pointer rewires: prev.next = b (splice b to lead), b.next = a (b points back to a), a.next = nxt (a tails into the remaining list). These three steps, applied in order, completely swap the pair and reconnect the chain."),
        N.h4("Building the Solution"),
        N.para("Add a dummy head so every pair — including the first — has a valid predecessor (prev). Save nxt = b.next before any rewiring (otherwise b.next = a overwrites the only reference to the tail). After each swap, advance prev = a because a is now the rightmost placed node and sits directly before the next pair."),
        N.callout(
            "Analogy: imagine a two-car train. 'Swap carriages' means: detach the rear car, move it in front, reconnect the front car to whatever was behind. You need to save a reference to 'what was behind' before disconnecting.",
            "🧠",
            "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
"""def swapPairs(head: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0, head)   # sentinel — removes head special-case
    prev = dummy                # prev trails the current pair

    while prev.next and prev.next.next:
        a   = prev.next         # first node of pair
        b   = a.next            # second node of pair
        nxt = b.next            # save rest BEFORE any rewire

        prev.next = b           # ① splice b into lead position
        b.next    = a           # ② b points back to a (pair reversed)
        a.next    = nxt         # ③ a's tail reconnects to rest

        prev = a                # advance: a is now rightmost placed node

    return dummy.next           # new head (may differ from original)""",
        lang="python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0, head)", {"code": True}),
                   (" — Create a sentinel node whose ", {}),
                   ("next", {"code": True}),
                   (" points to head. This gives every pair a valid predecessor so the first pair needs no special handling.", {})])),
    N.para(N.rich([("prev = dummy", {"code": True}),
                   (" — ", {}),
                   ("prev", {"code": True}),
                   (" always points to the node immediately before the current pair we are about to swap.", {})])),
    N.para(N.rich([("while prev.next and prev.next.next:", {"code": True}),
                   (" — Guard: only enter the loop if a full pair (two nodes) exists. Handles odd-length lists transparently — the lone trailing node is never entered.", {})])),
    N.para(N.rich([("a = prev.next", {"code": True}),
                   (" — ", {}), ("b = a.next", {"code": True}),
                   (" — Label the two nodes of the current pair.", {})])),
    N.para(N.rich([("nxt = b.next", {"code": True}),
                   (" — Snapshot the rest of the list BEFORE touching any pointer. This is the most critical step: once we set ", {}),
                   ("b.next = a", {"code": True}),
                   (", this reference is overwritten forever.", {})])),
    N.para(N.rich([("prev.next = b", {"code": True}),
                   (" — Rewire ①: the predecessor now leads into b (which will front the swapped pair).", {})])),
    N.para(N.rich([("b.next = a", {"code": True}),
                   (" — Rewire ②: b now points back to a, reversing the pair.", {})])),
    N.para(N.rich([("a.next = nxt", {"code": True}),
                   (" — Rewire ③: a connects forward to the saved rest of the list. Pair is complete.", {})])),
    N.para(N.rich([("prev = a", {"code": True}),
                   (" — Advance: a is the rightmost placed node. Setting prev = a positions us right before the next pair (", {}),
                   ("prev.next", {"code": True}),
                   (" will be the next pair's first node).", {})])),
    N.para(N.rich([("return dummy.next", {"code": True}),
                   (" — Return the new head. Because the first pair is swapped, the new head is b (node 2 in the example), not the original head. dummy.next correctly tracks this.", {})])),
    N.divider(),
]

# ── SOLUTION 2 — RECURSIVE ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Recursion naturally models 'swap the current pair, then swap the rest.' The base case handles 0 or 1 node. The recursive case: identify a and b, set a.next = result of swapping the rest, set b.next = a, return b."),
        N.h4("What Doesn't Work"),
        N.para("A naive recursive implementation without the a.next assignment first would set b.next = a but leave a.next pointing to b — creating a two-node cycle."),
        N.h4("The Key Observation"),
        N.para("The order matters: a.next = swapPairs(b.next) BEFORE b.next = a. This way, a.next is correctly set to the recursive result before b.next overwrites any stale links."),
        N.h4("Building the Solution"),
        N.para("Two-line swap: a.next = swapPairs(b.next) stitches a into the recursively-solved tail; b.next = a makes b the local head. Return b."),
        N.callout("Recursion depth = n/2. For n=200000, this is 100000 stack frames — may cause stack overflow in production. Prefer iterative in interviews.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def swapPairs(head: Optional[ListNode]) -> Optional[ListNode]:
    # Base case: 0 or 1 node — nothing to swap
    if not head or not head.next:
        return head

    a, b = head, head.next

    # a tails into the recursively-swapped remainder
    a.next = swapPairs(b.next)

    # b leads this pair
    b.next = a

    return b   # b is now the head of this sub-list""",
        lang="python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next: return head", {"code": True}),
                   (" — Base case: a list of 0 or 1 node cannot be swapped; return as-is.", {})])),
    N.para(N.rich([("a, b = head, head.next", {"code": True}),
                   (" — Label the pair. a will trail, b will lead after the swap.", {})])),
    N.para(N.rich([("a.next = swapPairs(b.next)", {"code": True}),
                   (" — The crucial step: recursively swap everything past b, and wire a's tail into the result.", {})])),
    N.para(N.rich([("b.next = a", {"code": True}),
                   (" — Reverse the local pair: b points back to a.", {})])),
    N.para(N.rich([("return b", {"code": True}),
                   (" — b is the new local head (the first node of this swapped pair).", {})])),
    N.divider(),
]

# ── COMPLEXITY TABLE ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                    "Time",  "Space"],
        ["Iterative (dummy head)",       "O(n)",  "O(1)"],
        ["Recursive",                    "O(n)",  "O(n/2) — call stack"],
        ["Array convert + value swap",   "O(n)",  "O(n) — violates constraint"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Iterative Pair Swap", {})])),
    N.callout(
        "When to recognise this pattern: linked list + local structural rearrangement + pointer-only constraint + group-wise operation (pairs, k-groups). Signals: 'swap every two nodes', 'reverse k-group', 'no value modification'.",
        "🔎",
        "green_background"
    ),
    N.callout(
        "Key technique: dummy head eliminates head special-casing. Track prev + a + b + nxt. Three pointer rewires per pair. Advance prev = a (the trailing node after each swap).",
        "💡",
        "blue_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Iterative Pair Swap / linked list pointer rewiring technique:"),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}),
                     (" (Hard) — generalise pair swap to k nodes per group; same dummy + prev pattern, more bookkeeping per group", {})])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}),
                     (" (Easy) — foundational pointer rewiring; simpler but identical pointer-manipulation mindset", {})])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}),
                     (" (Medium) — reverse a contiguous sub-range; requires careful stitching at both boundaries", {})])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}),
                     (" (Medium) — two-pointer technique; also uses dummy head to handle edge cases at the head", {})])),
    N.bullet(N.rich([("Rotate List", {"bold": True}),
                     (" (Medium) — find k-th node from end and reconnect tail; pointer arithmetic + bookkeeping", {})])),
    N.bullet(N.rich([("Reorder List", {"bold": True}),
                     (" (Medium) — find midpoint, reverse second half, interleave; combines multiple pointer skills in one problem", {})])),
    N.para("These problems share the same core technique: maintain a prev pointer, snapshot a tail reference before rewiring, perform pointer surgery, then advance prev."),
    N.divider(),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── 4) Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
