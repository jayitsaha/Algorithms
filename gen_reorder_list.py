"""
gen_reorder_list.py — Notion IN-PLACE update for Reorder List (#143).
Run: python3 gen_reorder_list.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8153-b2b3-d5374afa19e1"

# ── 1) Set page properties ──────────────────────────────────────────────
print("Setting properties…")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=143,
    pattern="Linked List",
    subpatterns=["Find Mid + Reverse + Merge", "Fast-Slow Pointer", "Reversal"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Find midpoint with fast/slow, reverse second half in-place, interleave the two halves.",
    icon="🟡",
)
print("Properties set. ✓")

# ── 2) Wipe old body ────────────────────────────────────────────────────
print("Wiping existing blocks…")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks. ✓")

# ── 3) Rebuild body ─────────────────────────────────────────────────────
print("Building content blocks…")

PROBLEM_STMT = (
    "Given the head of a singly linked list L0 → L1 → … → Ln−1 → Ln, "
    "reorder it in-place to: L0 → Ln → L1 → Ln−1 → L2 → Ln−2 → … "
    "You may not modify the values in the list's nodes; only the node pointers may be changed."
)

SOL1_CODE = """\
def reorderList(head) -> None:
    if not head or not head.next:
        return

    # ── Phase 1: Find the middle ──
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next     # second half starts here
    slow.next = None       # SEVER: first half ends at null

    # ── Phase 2: Reverse second half ──
    prev, curr = None, second
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev          # new head of reversed second half

    # ── Phase 3: Interleave merge ──
    l1, l2 = head, second
    while l2:
        n1, n2 = l1.next, l2.next   # SAVE both nexts first
        l1.next = l2                 # insert l2 after l1
        l2.next = n1                 # attach remaining first half
        l1 = n1
        l2 = n2
"""

SOL2_CODE = """\
def reorderList(head) -> None:
    if not head:
        return
    # Collect all node references into an array
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    # Two-pointer weave from both ends
    l, r = 0, len(nodes) - 1
    while l < r:
        nodes[l].next = nodes[r]
        l += 1
        if l == r:
            break
        nodes[r].next = nodes[l]
        r -= 1
    nodes[r].next = None   # null-terminate the tail
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Find Mid + Reverse + Merge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to take the last node and put it second, take the second-to-last "
            "and put it fourth, etc. — all without extra memory. This is the same as: "
            "interleave the first half of the list with the reversed second half."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naively, you might try moving the last node to position 2 repeatedly. "
            "But finding the last node each time is O(n), and you'd do it n/2 times → O(n²). "
            "Too slow. Storing nodes in an array works (O(n) space) but the interviewer "
            "will ask you to eliminate that."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The reordered list is exactly: [first half] interleaved with [reversed second half]. "
            "Example [1,2,3,4,5]: first half = [1,2,3], reversed second half = [5,4]. "
            "Zip them: 1,5,2,4,3. ✓ Now we just need to do this with pointer operations."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1 (Find mid): fast/slow pointers — fast goes 2x so when it stops, slow is at center. "
            "Sever there. Step 2 (Reverse): classic prev/curr flip on the second half. "
            "Step 3 (Merge): two pointers l1/l2, each round save both nexts, wire l1→l2→saved_l1_next."
        ),
        N.callout(
            "Analogy: Think of two decks of cards. Cut the deck in half (find mid), "
            "flip the right half face-up (reverse), then riffle-shuffle them together (merge). "
            "That's exactly the three-phase algorithm.",
            "🃏", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not head or not head.next:", {"code": True}), " — Guard: 0 or 1 nodes are already in order; return immediately."])),
    N.para(N.rich([("slow, fast = head, head", {"code": True}), " — Both pointers start at the head. fast will travel 2× faster."])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), " — Continue while fast has at least two more nodes to step over."])),
    N.para(N.rich([("slow = slow.next; fast = fast.next.next", {"code": True}), " — slow advances 1, fast advances 2. After loop: slow is at the midpoint."])),
    N.para(N.rich([("second = slow.next; slow.next = None", {"code": True}), " — Capture the second half's head, then sever the list at the midpoint. Critical: without this sever, the merge phase creates cycles."])),
    N.para(N.rich([("prev, curr = None, second", {"code": True}), " — Setup for classic in-place reversal of the second half."])),
    N.para(N.rich([("nxt = curr.next; curr.next = prev", {"code": True}), " — Save next before flipping the pointer backward to prev."])),
    N.para(N.rich([("prev = curr; curr = nxt", {"code": True}), " — Advance both pointers. After loop, prev is the new head of the reversed second half."])),
    N.para(N.rich([("second = prev", {"code": True}), " — Capture the reversed second half's head (prev after reversal loop)."])),
    N.para(N.rich([("l1, l2 = head, second", {"code": True}), " — l1 walks the first half, l2 walks the reversed second half."])),
    N.para(N.rich([("n1, n2 = l1.next, l2.next", {"code": True}), " — CRITICAL: save both next pointers before any rewiring. Losing either means losing the rest of a half."])),
    N.para(N.rich([("l1.next = l2; l2.next = n1", {"code": True}), " — Wire: l1 → l2 → (saved l1.next). This inserts l2 between l1 and l1's original next."])),
    N.para(N.rich([("l1 = n1; l2 = n2", {"code": True}), " — Advance both to the next unprocessed nodes in their respective halves."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Collect Into Array (O(n) Space, Easier to Derive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we had random access (like an array), we'd just use two pointers — one from the left, one from the right — and rewire them inward. We can get random access by dumping all node references into a Python list."),
        N.h4("What Doesn't Work"),
        N.para("Linked lists don't support O(1) index access, so nodes[i] is O(n) without precomputation. That's why we first collect all nodes."),
        N.h4("The Key Observation"),
        N.para("Once nodes are in an array, indices l and r point to the front and back. We alternately link nodes[l] → nodes[r] → nodes[l+1] and so on. At each step we advance l forward and r backward."),
        N.h4("Building the Solution"),
        N.para("Collect all nodes into a list (O(n) pass). Two-pointer weave: nodes[l].next = nodes[r], then nodes[r].next = nodes[l+1]. Guard: if l == r after advancing l, we're at an odd-length middle — stop to avoid double-linking. Null-terminate at nodes[r]."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("nodes = []  +  while cur:", {"code": True}), " — One full pass to collect all node objects into a Python list. Now nodes[i] is O(1) access."])),
    N.para(N.rich([("l, r = 0, len(nodes) - 1", {"code": True}), " — Left pointer starts at head (index 0), right pointer at tail (index n-1)."])),
    N.para(N.rich([("nodes[l].next = nodes[r]; l += 1", {"code": True}), " — Link front to back, then move left pointer inward."])),
    N.para(N.rich([("if l == r: break", {"code": True}), " — Odd length: after incrementing l, if both pointers meet, the middle node is handled. Stop here to avoid wiring nodes[r].next = nodes[l] which would be a self-loop."])),
    N.para(N.rich([("nodes[r].next = nodes[l]; r -= 1", {"code": True}), " — Link back to (new) front, then move right pointer inward."])),
    N.para(N.rich([("nodes[r].next = None", {"code": True}), " — Set the tail's next to null. Without this, the tail still points to wherever it pointed in the original list."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Collect Into Array", "O(n)", "O(n)"],
        ["Find Mid + Reverse + Merge", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List Manipulation"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Find Mid + Reverse + Merge (Fast-Slow Pointer + In-Place Reversal + Two-Pointer Merge)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Reorder/rearrange a linked list in-place' with front-meets-back semantics. "
        "(2) 'Check if linked list is palindrome' — same three phases. "
        "(3) Any problem needing simultaneous traversal from both ends of a linked list without extra space. "
        "(4) O(1) space required with no random access — fast/slow pointer to find middle is your entry point.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}), "The compound sub-pattern 'Find Mid + Reverse + Merge' combines three primitives each addressable as standalone LeetCode problems (#876, #206, #21)."])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or direct building blocks:"),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy) — Pure fast/slow pointer; Phase 1 of this problem exactly. (#876)"])),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), " (Easy) — Classic three-pointer in-place reversal; Phase 2 of this problem. (#206)"])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), " (Easy) — Find mid, reverse second half, compare node-by-node. Identical three-phase decomposition. (#234)"])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), " (Hard) — Repeated in-place reversal of fixed-size chunks; extends the reversal phase. (#25)"])),
    N.bullet(N.rich([("Rotate List", {"bold": True}), " (Medium) — Find tail, find new tail at (n-k), relink — structured pointer manipulation with fast/slow ideas. (#61)"])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — The interleave merge is structurally identical (just non-sorted here). (#21)"])),
    N.bullet(N.rich([("Odd Even Linked List", {"bold": True}), " (Medium) — Separate odd-index and even-index nodes, then concatenate — a simpler rearrangement pattern. (#328)"])),
    N.para("These problems share the core technique: manipulate linked list structure entirely through pointer rewiring, with fast/slow as the mechanism for split-point discovery."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section. Sub-Pattern: Fast-Slow Pointer + Reversal + Merge", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("reorder_list")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
