"""
gen_rotate_list.py — Notion page update for LeetCode #61 Rotate List
Run from /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8115-8991-cb6496444396"

# ── 1. Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=61,
    pattern="Linked List",
    subpatterns=["Find New Head Position"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Form a circle (tail→head), walk n−k−1 steps to find new tail, cut. Two O(n) passes.",
    icon="🟡",
)
print("Properties set OK")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Build body ─────────────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "), ("head", {"code": True}), (" of a linked list, rotate the list to the right by "),
        ("k", {"code": True}), (" places. Rotating right by 1 means the last node becomes the new head.\n\n"),
        ("Example 1: head = [1,2,3,4,5], k = 2  →  [4,5,1,2,3]\n"),
        ("Example 2: head = [0,1,2], k = 4  →  [2,0,1]\n\n"),
        ("Constraints: list length 0–500, k ≥ 0."),
    ])),
    N.divider(),
]

# ── Solution 1 (optimal) ─────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Make Circular & Cut (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Rotating right by k = moving the last k nodes to the front. We need to find exactly ONE position in the list — the cut point — and rewire two pointers. No elements actually 'move'; only pointers change."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: perform k individual one-node rotations. Each rotation is O(n) (find the second-to-last node, detach the last, reattach at head). Total: O(n × k). When k is large (say 10^9), this is catastrophically slow even with modular normalization applied first."),
        N.h4("The Key Observation"),
        N.para("The rotated list is just the original list read starting from a different position. Specifically, the new head is at 0-indexed position n−k (after normalizing k). The structure of the list is unchanged — only the 'start' shifts. This screams 'circular list + cut'."),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Find n (list length) and the tail node in one pass.\n"
            "Step 2: k = k % n. If k=0, return head (full rotations cancel).\n"
            "Step 3: Connect tail.next = head to form a ring.\n"
            "Step 4: Walk n−k−1 steps from head to find the new tail (position n−k−1).\n"
            "Step 5: new_head = new_tail.next. Set new_tail.next = None. Return new_head."
        ),
        N.callout(
            "Analogy: Think of a clock. Rotating the hands by k hours is the same as pointing to a different number on the face — the clock itself doesn't change, you just re-label which position is '12 o'clock'. The circle + cut does exactly this.",
            "🕐", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def rotateRight(head, k):\n"
        "    if not head or not head.next or k == 0:\n"
        "        return head\n"
        "    tail, n = head, 1          # n=1: head already counted\n"
        "    while tail.next:\n"
        "        tail = tail.next       # walk to real tail\n"
        "        n += 1                 # count each node\n"
        "    k %= n                     # normalize: k=5 on n=5 → k=0\n"
        "    if k == 0: return head     # full rotation = no-op\n"
        "    tail.next = head           # form the circle\n"
        "    new_tail = head\n"
        "    for _ in range(n - k - 1):# walk to new tail position\n"
        "        new_tail = new_tail.next\n"
        "    new_head = new_tail.next   # node after new_tail = new head\n"
        "    new_tail.next = None       # break the circle\n"
        "    return new_head"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next or k == 0", {"code": True}), (" — Three early-exit conditions: empty list, single node (can't rotate), or k=0 (already in place). All return head unchanged.")])),
    N.para(N.rich([("tail, n = head, 1", {"code": True}), (" — Initialize tail at head (already counted once), n starts at 1. Counting begins before the loop.")])),
    N.para(N.rich([("while tail.next:", {"code": True}), (" — Advance until tail.next is None (real tail found). Each iteration also increments n.")])),
    N.para(N.rich([("k %= n", {"code": True}), (" — Normalize k. Rotating by n is the identity. k=7 on n=5 gives k=2 (same result). Prevents k > n issues.")])),
    N.para(N.rich([("tail.next = head", {"code": True}), (" — The circle trick: last node → first node. List is now a ring, allowing us to 'wrap around' without special-casing.")])),
    N.para(N.rich([("for _ in range(n - k - 1):", {"code": True}), (" — Walk n−k−1 steps from head. This lands at 0-indexed position n−k−1, which will become the new tail.")])),
    N.para(N.rich([("new_head = new_tail.next", {"code": True}), (" — The node immediately after new_tail is the new head (position n−k in the original list).")])),
    N.para(N.rich([("new_tail.next = None", {"code": True}), (" — Break the ring at this point. new_tail is now the last node (points to null). The ring becomes a list again.")])),
    N.divider(),
]

# ── Solution 2 (brute force) ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (Rotate One at a Time)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most literal interpretation: perform k single-step rotations. Each rotation takes the last node and makes it the new head. After k rotations, we have the answer."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly but is O(n × k). After normalizing k with mod n, k is at most n−1. So worst case is O(n²). For n=500, that's 250,000 operations — acceptable here but bad practice. For large constraints (n or k up to 10^9), this fails completely."),
        N.h4("The Key Observation"),
        N.para("The per-step rotation is: find the second-to-last node (O(n)), detach the last, re-link to head. Repeating this k times gives correct output. Use this to explain your brute force, then immediately propose the O(n) solution."),
        N.h4("Building the Solution"),
        N.para("Count n, normalize k. Then loop k times: each time, walk to the second-to-last node, take the last node, attach it to head, update head. This is the intuitive 'do what the problem says' approach."),
    ]),
    N.h3("Code"),
    N.code(
        "def rotateRight_brute(head, k):\n"
        "    if not head or not head.next: return head\n"
        "    n, cur = 0, head\n"
        "    while cur: n += 1; cur = cur.next   # count length\n"
        "    k %= n                               # normalize\n"
        "    for _ in range(k):                   # k one-step rotations\n"
        "        cur = head\n"
        "        while cur.next.next:             # find second-to-last\n"
        "            cur = cur.next\n"
        "        cur.next.next = head             # last → old head\n"
        "        head = cur.next                  # new head = last node\n"
        "        cur.next = None                  # detach\n"
        "    return head"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("while cur.next.next:", {"code": True}), (" — Walk until cur is the second-to-last node. cur.next is the last node. cur.next.next is None (end of list).")])),
    N.para(N.rich([("cur.next.next = head", {"code": True}), (" — The last node (cur.next) now points to the old head. This 'wraps' it to the front.")])),
    N.para(N.rich([("head = cur.next", {"code": True}), (" — New head is the old last node.")])),
    N.para(N.rich([("cur.next = None", {"code": True}), (" — Detach: cur (now second-to-last) loses its reference to the old last node. cur is the new tail.")])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (rotate one by one)", "O(n × k)", "O(1)"],
        ["Make Circular & Cut (optimal)", "O(n)", "O(1)"],
        ["Two-Pointer one-pass (follow-up)", "O(n)", "O(1)"],
    ]),
    N.callout(
        "Space is O(1) for all approaches — linked list rotation is purely pointer manipulation. "
        "No additional arrays or data structures needed.",
        "💾", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Find New Head Position")])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'rotate' a list or array — immediately think modular arithmetic\n"
        "• Need to find the k-th node from the end\n"
        "• Rearranging a contiguous block of nodes from tail to head\n"
        "• k could be very large → always reduce with mod n first",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Find New Head Position / positional linked list manipulation):"),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), (" (Medium) — Two pointers k+1 apart; when fast reaches end, slow is at n−k position. Same 'count from end' math. (#19)")])),
    N.bullet(N.rich([("Reverse Linked List II", {"bold": True}), (" (Medium) — Traverse to position left, reverse up to right, reconnect. Positional traversal then pointer manipulation. (#92)")])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), (" (Medium) — Find middle, reverse second half, interleave. Same 'split at position' pattern. (#143)")])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), (" (Easy) — Fast-slow pointer to find midpoint. Foundational for any linked list positional problem. (#876)")])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), (" (Medium) — Mathematical positional reasoning to find where the cycle starts. (#142)")])),
    N.bullet(N.rich([("Split Linked List in Parts", {"bold": True}), (" (Medium) — Divide list into k parts; uses mod arithmetic for remainder distribution across parts. (#725)")])),
    N.para("These problems share the core technique: traverse once to count, then use arithmetic to find the exact target position, then rewire pointers."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Linked List). Sub-Pattern: Find New Head Position.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("rotate_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
