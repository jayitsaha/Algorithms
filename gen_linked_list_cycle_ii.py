"""
gen_linked_list_cycle_ii.py — Notion page rebuild for LeetCode #142 Linked List Cycle II
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-817c-a81a-fa1d54f5b0c7"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=142,
    pattern="Linked List",
    subpatterns=["Floyd's: Reset One Pointer", "Fast-Slow Pointer"],
    tc="O(n)",
    sc="O(1)",
    key_insight="After fast/slow meet inside cycle, reset one pointer to head; both walk 1 step — they meet at cycle entry (F = n·C − a).",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("head", {"code": True}),
        (" of a linked list, return the node where the cycle begins. If there is no cycle, return ", {}),
        ("null", {"code": True}),
        (". You must not modify the linked list. The solution should use O(1) memory.", {}),
    ])),
    N.para(N.rich([
        ("Example: head = [3,1,2,4,5], pos = 1 (tail connects to node index 1). Return node at index 1 (value 1) — the cycle entry.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Floyd's Algorithm ──────────────────────────────────
blocks += [
    N.h2("Solution 1 — Floyd's Two-Phase Algorithm (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find where a loop in the list STARTS. Detecting the loop is the easier sub-problem (#141). The hard part is pinpointing the entry node without extra memory."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for every node, check if following .next eventually revisits it — O(n²). Hash set: store every visited node and return the first repeat — correct but O(n) space, not O(1)."),
        N.h4("The Key Observation"),
        N.para("Floyd's algorithm: slow (1 step) and fast (2 steps) will ALWAYS meet inside the cycle if one exists. The meeting point is not the entry, but it encodes the distance to the entry via the equation F = n·C − a."),
        N.h4("Building the Solution"),
        N.para("Phase 1: Run the fast/slow race until they meet (or fast hits null → no cycle). Phase 2: Reset one pointer to head. Walk both one step at a time. The algebraic identity F = n·C − a guarantees they converge exactly at the cycle entry after F steps."),
        N.callout("Analogy: Two runners on a track — one twice as fast. They meet at some point in the loop. That meeting point is 'F steps forward' from the start line, same as 'F steps forward' from their meeting point — because the loop wraps around.", "🏃", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Floyd's Cycle Detection"),
    N.para("Robert Floyd, 1967. Originally published for detecting loops in sequences and function iteration. Solves cycle DETECTION in O(n) time, O(1) space. Extended here for cycle ENTRY LOCATION."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("fast = 2 × slow always. When they meet: F + a + n·C = 2(F + a) → F = n·C − a. This means the distance from head to cycle entry equals the distance from the meeting point forward to cycle entry (modulo full loops).", {}),
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ("Any problem asking for cycle detection or cycle entry with O(1) space. Also applies to array problems where values encode a 'next pointer' (e.g., LeetCode #287 Find Duplicate Number).", {}),
    ])),
    N.h3("Code"),
    N.code("""def detectCycle(head):
    # Phase 1: Detect cycle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:          # Cycle confirmed; meeting point found
            # Phase 2: Locate cycle entry
            slow = head           # Reset one pointer to head
            while slow != fast:   # March both one step at a time
                slow = slow.next
                fast = fast.next
            return slow           # They meet exactly at cycle entry
    return None                   # No cycle"""),
    N.h3("Line by Line"),
    N.para(N.rich([("slow = fast = head", {"code": True}), (" — Initialize both pointers at the head before Phase 1.", {})])),
    N.para(N.rich([("while fast and fast.next:", {"code": True}), (" — Guard: fast.next.next requires both fast and fast.next to be non-null. If either is null, no cycle — exit loop.", {})])),
    N.para(N.rich([("slow = slow.next", {"code": True}), (" — slow moves 1 step per iteration throughout Phase 1.", {})])),
    N.para(N.rich([("fast = fast.next.next", {"code": True}), (" — fast moves 2 steps per iteration, guaranteed safe by the while guard.", {})])),
    N.para(N.rich([("if slow == fast:", {"code": True}), (" — Pointer collision inside the cycle. F = n·C − a now holds.", {})])),
    N.para(N.rich([("slow = head", {"code": True}), (" — THE KEY MOVE: reset slow to head. fast stays at the meeting point.", {})])),
    N.para(N.rich([("while slow != fast:", {"code": True}), (" — Both now advance 1 step at a time. They will meet in exactly F steps.", {})])),
    N.para(N.rich([("return slow", {"code": True}), (" — slow == fast at cycle entry. Return either (same node).", {})])),
    N.para(N.rich([("return None", {"code": True}), (" — Loop exited without meeting → no cycle in the list.", {})])),
    N.divider(),
]

# ── Solution 2: Hash Set ──────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Hash Set (Simpler, O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The cycle entry is simply the FIRST node you visit twice. Walk the list and remember every node seen. The first node already in your memory is the entry."),
        N.h4("What Doesn't Work"),
        N.para("We can't just compare values — different nodes can have the same value. We need to compare node objects (by identity/reference/memory address)."),
        N.h4("The Key Observation"),
        N.para("Python sets store object references. 'node in visited' checks if the exact same node object was seen before — no value comparison, true identity check."),
        N.h4("Building the Solution"),
        N.para("Walk node by node. Before adding each node to the set, check if it's already there. If yes — this is the cycle entry. If we reach null — no cycle."),
    ]),
    N.h3("Code"),
    N.code("""def detectCycle(head):
    visited = set()
    node = head
    while node:
        if node in visited:
            return node       # First repeated node = cycle entry
        visited.add(node)
        node = node.next
    return None               # Reached null = no cycle"""),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = set()", {"code": True}), (" — Empty set to track visited node objects by reference.", {})])),
    N.para(N.rich([("if node in visited:", {"code": True}), (" — O(1) average lookup. Checks object identity, not value.", {})])),
    N.para(N.rich([("visited.add(node)", {"code": True}), (" — Store the node object itself (its memory address is the hash key).", {})])),
    N.para(N.rich([("return None", {"code": True}), (" — node became null → list has no cycle.", {})])),
    N.callout("When to use hash set: in interviews, propose this first as the 'obvious' O(n) space solution. Then offer to optimize to Floyd's for O(1) space.", "💡", "green_background"),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Hash Set", "O(n)", "O(n)"],
        ["Floyd's Algorithm (Optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Linked List", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Floyd's: Reset One Pointer; Fast-Slow Pointer", {})])),
    N.callout(
        "When to recognize this pattern: Problem says 'cycle in linked list', 'detect loop', 'find where cycle begins'. Also: 'find duplicate in array of n+1 integers from 1..n' (encode as list). The O(1) space requirement is the signal to reach for Floyd's over hash set.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Floyd's fast/slow pointer):"),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), (" (Easy) — Phase 1 of Floyd's only; just detect, don't locate entry (#141)", {})])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), (" (Medium) — Array values act as 'next' pointers; cycle entry = duplicate (#287)", {})])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), (" (Easy) — When fast reaches end, slow is at middle; same two-speed logic (#876)", {})])),
    N.bullet(N.rich([("Happy Number", {"bold": True}), (" (Easy) — Digit-sum sequence either cycles or reaches 1; Floyd's detects both (#202)", {})])),
    N.bullet(N.rich([("Palindrome Linked List", {"bold": True}), (" (Easy) — Fast/slow to find midpoint, then reverse second half for comparison (#234)", {})])),
    N.para("These problems all share the core technique: two pointers at different speeds expose structural properties (cycles, midpoints) in O(1) space."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section. Sub-Pattern: Floyd's: Reset One Pointer. Source: Guide + Analysis.", "📚", "gray_background"),
]

# ── Interactive Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("linked_list_cycle_ii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
