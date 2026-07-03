"""
gen_reverse_linked_list_ii.py
Regenerate Notion page for: Reverse Linked List II (LC #92, Medium)
notion_page_id: null -> create fresh page
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

SLUG = "reverse_linked_list_ii"
NAME = "Reverse Linked List II"
NUMBER = 92
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Linked List"
SUBPATTERNS = ["Reverse Sublist (m to n)"]
TC = "O(n)"
SC = "O(1)"
KEY_INSIGHT = "Use a dummy head + head insertion: iteratively pull curr.next to just after prev, (right-left) times."

PAGE_ID = "39193418-809c-8131-a144-fa16461195c7"  # created in prior run

# ── Step 0: Resume check ─────────────────────────────────────────────────────
if PAGE_ID is None:
    # Search for existing page first to avoid duplicates
    import json, urllib.request, urllib.error, time
    TOKEN = N.TOKEN
    DB_ID = N.DB_ID
    HEADERS = N._HEADERS
    search_body = json.dumps({
        "filter": {"property": "Problem", "title": {"contains": NAME}}
    }).encode()
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{DB_ID}/query",
        data=search_body, method="POST", headers=HEADERS
    )
    try:
        with urllib.request.urlopen(req) as r:
            results = json.load(r).get("results", [])
        if results:
            PAGE_ID = results[0]["id"]
            print(f"Found existing page: {PAGE_ID}")
        else:
            PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
            print(f"Created new page: {PAGE_ID}")
    except Exception as e:
        PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
        print(f"Created new page (search failed: {e}): {PAGE_ID}")
else:
    print(f"Using existing page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────────────────
N.set_properties(PAGE_ID,
    difficulty=DIFFICULTY, number=NUMBER,
    pattern=PATTERN, subpatterns=SUBPATTERNS,
    tc=TC, sc=SC, key_insight=KEY_INSIGHT, icon=ICON)
print("Properties set.")

# ── Step 2: Wipe old content ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── Step 3: Build body blocks ─────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the head of a singly linked list and two integers ", {}),
        ("left", {"code": True}),
        (" and ", {}),
        ("right", {"code": True}),
        (" where 1 ≤ left ≤ right ≤ n (1-indexed), reverse the nodes of the list from position ", {}),
        ("left", {"code": True}),
        (" to position ", {}),
        ("right", {"code": True}),
        (", and return the reversed list. Do it in one pass.", {}),
    ])),
    N.para(N.rich([
        ("Example: head = [1,2,3,4,5], left = 2, right = 4  →  [1,4,3,2,5]", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1: One-Pass Head Insertion (Interview Pick) ─────────────────────
SOL1_CODE = '''def reverseBetween(head, left: int, right: int):
    dummy = ListNode(0)           # sentinel — handles left==1 cleanly
    dummy.next = head
    prev = dummy                  # anchor: stays at position left-1 forever
    for _ in range(left - 1):    # walk prev exactly (left-1) hops
        prev = prev.next
    curr = prev.next              # first node of sublist; becomes tail of reversed portion
    for _ in range(right - left): # (right-left) insertions — NOT right-left+1
        nxt = curr.next           # save the node to pull forward
        curr.next = nxt.next      # unlink nxt from its current position
        nxt.next = prev.next      # nxt will precede the current reversed-front
        prev.next = nxt           # insert nxt as new front of reversed portion
    return dummy.next             # true head (unchanged if left>1; new if left==1)'''

blocks += [
    N.h2("Solution 1 — One-Pass Head Insertion (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have a linked list and must reverse only the middle segment (positions left to right) in-place. The prefix and suffix stay untouched. Think of it as: save the junction before the segment, reverse the segment, reconnect."),
        N.h4("What Doesn't Work"),
        N.para("Naive two-pass: find start and end of sublist in pass 1, reverse in pass 2. Correct but verbose and requires tracking multiple nodes across passes. Also, if we collect nodes into an array, we use O(n) extra space — not in-place."),
        N.h4("The Key Observation"),
        N.para("Instead of reversing arrows in place (which requires tracking prev/curr/next across the whole sublist), we can 'insert' each subsequent node at the front of the growing reversed portion. curr starts as the first sublist node and never moves — it naturally becomes the tail. We loop exactly (right-left) times, pulling the node after curr to just after prev each time."),
        N.h4("Building the Solution"),
        N.para("1. Dummy node before head → prev = dummy. 2. Advance prev (left-1) times to reach the anchor. 3. curr = prev.next (first sublist node). 4. Loop (right-left) times: save nxt=curr.next, curr.next=nxt.next (skip nxt), nxt.next=prev.next (nxt will precede old front), prev.next=nxt (attach nxt as new front). 5. Return dummy.next."),
        N.callout(
            "Analogy: Sliding cards to the front. You want to reverse 3 cards in a row by repeatedly sliding the next card to the front of the group — 2 slides for 3 cards. curr is the original first card (stays as tail); prev is the stable card before the group.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0)", {"code": True}), (" — Sentinel node before head. When left==1, the head itself changes; dummy.next always gives the correct new head without any special-case branch.", {})])),
    N.para(N.rich([("prev = dummy", {"code": True}), (" — Anchor pointer. Will land at position left−1 and stay there forever. Everything gets inserted right after this node.", {})])),
    N.para(N.rich([("for _ in range(left - 1): prev = prev.next", {"code": True}), (" — Advance exactly (left−1) hops. After the loop, prev.next is the first node of the sublist.", {})])),
    N.para(N.rich([("curr = prev.next", {"code": True}), (" — First node of sublist. This is our stable tail reference — it never moves. After reversal it will be the rightmost node of the reversed sublist.", {})])),
    N.para(N.rich([("for _ in range(right - left):", {"code": True}), (" — Loop runs (right−left) times, NOT (right−left+1). curr is already positioned; we only insert the nodes that follow it.", {})])),
    N.para(N.rich([("nxt = curr.next", {"code": True}), (" — Save the node we are about to pull. Must be first — once curr.next changes, nxt is unreachable.", {})])),
    N.para(N.rich([("curr.next = nxt.next", {"code": True}), (" — Unlink nxt from its position. curr now skips directly to the node after nxt.", {})])),
    N.para(N.rich([("nxt.next = prev.next", {"code": True}), (" — nxt will precede whatever is currently at the front of the reversed portion. This creates the backward link.", {})])),
    N.para(N.rich([("prev.next = nxt", {"code": True}), (" — Attach nxt immediately after prev, making it the new front of the reversed sublist.", {})])),
    N.para(N.rich([("return dummy.next", {"code": True}), (" — The true head of the list. If left==1, this is the new head (the node that was at position right). Otherwise same as input head.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────────────
SOL2_CODE = '''def reverseBetween(head, left: int, right: int):
    if not head or left == right:
        return head
    nodes, curr = [], head
    while curr:                    # collect all nodes
        nodes.append(curr)
        curr = curr.next
    l, r = left - 1, right - 1    # convert to 0-indexed
    nodes[l:r+1] = nodes[l:r+1][::-1]   # reverse the slice
    for i in range(len(nodes) - 1):      # restitch .next pointers
        nodes[i].next = nodes[i+1]
    nodes[-1].next = None
    return nodes[0]'''

blocks += [
    N.h2("Solution 2 — Brute Force: Collect, Slice-Reverse, Rebuild"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we could treat the linked list like an array, reversing a subrange is trivial with Python's slice notation. So: convert list to array, do the slice reversal, convert back."),
        N.h4("What Doesn't Work About This"),
        N.para("It uses O(n) extra space — the nodes list holds all n node references. For an interview expecting O(1) space, this is suboptimal. However it's excellent as a first solution to propose before optimizing."),
        N.h4("The Key Observation"),
        N.para("Linked list nodes are objects — collecting their references in a list and reassigning .next pointers is valid. The nodes themselves don't move in memory, just the .next chains."),
        N.h4("Building the Solution"),
        N.para("Traverse the list, append each node to a list. Reverse nodes[l:r+1] in-place using slice assignment. Re-stitch .next from nodes[i] to nodes[i+1] for all i. Set nodes[-1].next = None. Return nodes[0]."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("while curr: nodes.append(curr)", {"code": True}), (" — O(n) pass to collect all node references into a Python list.", {})])),
    N.para(N.rich([("nodes[l:r+1] = nodes[l:r+1][::-1]", {"code": True}), (" — Python slice reversal in O(right−left+1) time. Straightforward and correct.", {})])),
    N.para(N.rich([("nodes[i].next = nodes[i+1]", {"code": True}), (" — Re-stitch: every node's .next points to the next node in the (now reordered) list.", {})])),
    N.para(N.rich([("nodes[-1].next = None", {"code": True}), (" — The last node must explicitly terminate the list.", {})])),
    N.para(N.rich([("return nodes[0]", {"code": True}), (" — nodes[0] is always the head (whether or not left==1, nodes[0] was the original or new head after the slice reversal).", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["One-Pass Head Insertion (Optimal)", "O(n)", "O(1)"],
        ["Brute Force (Collect & Reverse)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Reverse Sublist [m, n] (Notion tag: Reverse Sublist (m to n))", {})])),
    N.callout(
        "When to recognize this pattern: 'Reverse nodes between two positions' + 'in-place' + 'O(1) space'. Also recognizable in: reverse in k-groups, palindrome linked list check, any linked list surgery where a contiguous segment's arrows flip direction.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Reverse Sublist technique:"),
    N.bullet(N.rich([("Reverse Linked List", {"bold": True}), (" (Easy) — Full list reversal; the foundation this problem builds upon. LC #206", {})])),
    N.bullet(N.rich([("Reverse Nodes in k-Group", {"bold": True}), (" (Hard) — Apply this exact sublist reversal every k nodes. LC #25", {})])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), (" (Easy) — Reverse second half in-place to check palindrome. LC #234", {})])),
    N.bullet(N.rich([("Swap Nodes in Pairs", {"bold": True}), (" (Medium) — Special case: reverse every 2-node sublist. Same 3-pointer pattern. LC #24", {})])),
    N.bullet(N.rich([("Rotate List", {"bold": True}), (" (Medium) — Rearrange list segments via pointer surgery. LC #61", {})])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), (" (Medium) — Dummy head + two-pointer setup; same defensive pattern. LC #19", {})])),
    N.para("These problems all share the core technique: dummy head + careful pointer manipulation to reverse or rearrange a contiguous subchain."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Linked List → Reversal), Sub-Pattern: Reverse Sublist [m, n] (Guide notation). Notion tag: Reverse Sublist (m to n) — commas not allowed in Notion multi_select.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=989")
