"""
gen_intersection_of_two_linked_lists.py
Rebuilds the Notion page for LC #160 Intersection of Two Linked Lists IN-PLACE.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8169-a9e3-c7da7522a3b0"
SLUG = "intersection_of_two_linked_lists"

# ── Step 1: Set properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=160,
    pattern="Linked List",
    subpatterns=["Two Pointers (Switch Heads)"],
    tc="O(m+n)",
    sc="O(1)",
    key_insight="Redirect each pointer to the other head on null; both travel m+n steps and land on the intersection simultaneously.",
    icon="🟢"
)
print("Properties set.")

# ── Step 2: Wipe existing body ────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} existing blocks.")

# ── Step 3: Build body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the heads of two singly linked-lists "),
        (("headA", {"code": True})),
        (" and "),
        (("headB", {"code": True})),
        (", return the node at which the two lists intersect. Return "),
        (("null", {"code": True})),
        (" if the two linked lists have no intersection. Note: the intersection is defined by reference (same node object), not by value equality. You may not alter the structures of the linked lists.")
    ])),
    N.divider(),
]

# ── Solution 1: Two-Pointer Switch Heads ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Two-Pointer Switch Heads (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have two lists of potentially different lengths that may share a tail. We want to find the first node they both point to — not a node with the same value, but the exact same object in memory."),
        N.h4("What Doesn't Work"),
        N.para("Naive two pointers: put a pointer at each head and advance them one step at a time. They'll go through their private prefixes at different paces, hit the shared section at different times, and never be in sync — unless the lists happen to be the same length. A hash set works but requires O(m) extra space."),
        N.h4("The Key Observation"),
        N.para("The problem with two pointers is a length-offset issue: list A has 'a' private nodes and list B has 'b' private nodes before the shared tail. If only we could equalize that offset… If pointer A could somehow travel 'b' extra nodes before entering the shared section, and pointer B could travel 'a' extra nodes, they'd arrive at the intersection at the same time."),
        N.h4("Building the Solution"),
        N.para("The switch-head trick does exactly this. When pointer A finishes list A (reaches null), redirect it to headB. When pointer B finishes list B, redirect it to headA. Pointer A now travels: (m-c) A-private + redirect + (n-c) B-private + c shared = m+n-c total steps to intersection. Pointer B travels: (n-c) B-private + redirect + (m-c) A-private + c shared = m+n-c total steps. They arrive simultaneously. For no-intersection (c=0), both travel m+n steps and land on null at the same time."),
        N.callout(
            "Analogy: Two people walk different-length trails that merge at a fork. When each reaches their trail's end, they teleport to the other trail's start. They both walk the same total distance and meet at the fork simultaneously.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def getIntersectionNode(headA, headB):\n"
        "    a, b = headA, headB           # Two runners, each at their own head\n"
        "    while a != b:                 # Loop until same node, or both null\n"
        "        a = a.next if a else headB  # Advance a; if null, redirect to headB\n"
        "        b = b.next if b else headA  # Advance b; if null, redirect to headA\n"
        "    return a                      # Intersection node, or None"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("a, b = headA, headB", {"code": True}), " — Initialize two pointers, one at each list's head. No extra data structures."])),
    N.para(N.rich([("while a != b:", {"code": True}), " — Continue until the pointers point to the same object. In Python, comparing ListNode objects with != uses identity by default (same as 'is not'). Also handles the no-intersection case: loop exits when both are None, since None is None is True."])),
    N.para(N.rich([("a = a.next if a else headB", {"code": True}), " — If a is currently not null, advance to the next node. If a is null (fell off the end), redirect to headB. The redirect happens AFTER a becomes null, not at the last node."])),
    N.para(N.rich([("b = b.next if b else headA", {"code": True}), " — Same logic for b, redirecting to headA. Each pointer crosses exactly once during the entire algorithm."])),
    N.para(N.rich([("return a", {"code": True}), " — The loop exited because a == b. Return either pointer — they're the same node object (the intersection), or both are None (no intersection)."])),
    N.divider(),
]

# ── Solution 2: Hash Set ──────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Hash Set (Good Starting Proposal)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to know if any node in list B is the same object as any node in list A. This is a classic 'seen before' problem — exactly what a hash set is for."),
        N.h4("What Doesn't Work"),
        N.para("Brute O(m*n): for each node in B, scan all of A looking for a match. Correct but too slow."),
        N.h4("The Key Observation"),
        N.para("We can preprocess list A into a set in O(m) time. Then a single scan of B with O(1) lookups per node finds the intersection in O(n) time. Total O(m+n), space O(m)."),
        N.h4("Building the Solution"),
        N.para("Walk all of A, adding each node reference to a Python set (which uses object identity for hashing ListNode objects). Then walk B — the first B node that's already in the set is the intersection. If we exhaust B without a match, return None."),
        N.callout("Use this approach as your first proposal in an interview, then offer the two-pointer O(1) space optimization.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def getIntersectionNode(headA, headB):\n"
        "    visited = set()               # Store node references from A\n"
        "    node = headA\n"
        "    while node:                   # Walk all of A\n"
        "        visited.add(node)         # Python sets store by id() for objects\n"
        "        node = node.next\n"
        "    node = headB\n"
        "    while node:                   # Walk B, check membership\n"
        "        if node in visited:       # Same object found in both lists\n"
        "            return node\n"
        "        node = node.next\n"
        "    return None                   # No intersection"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = set()", {"code": True}), " — A Python set that will hold node object references (by identity, not value)."])),
    N.para(N.rich([("visited.add(node)", {"code": True}), " — Python's set uses id(node) as the hash key for custom objects without __hash__, so this records the memory address of each A node."])),
    N.para(N.rich([("if node in visited:", {"code": True}), " — O(1) average membership test. If this B node's identity was seen in A, it's the intersection."])),
    N.para(N.rich([("return None", {"code": True}), " — Exhausted B without a match. No intersection exists."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Pointer Switch Heads (optimal)", "O(m+n)", "O(1)"],
        ["Hash Set", "O(m+n)", "O(m)"],
        ["Length Difference (explicit)", "O(m+n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Linked List — problems involving traversal, pointer manipulation, and structural properties of singly or doubly linked lists."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Pointers (Switch Heads) — a specialized technique where two pointers are redirected to each other's starting positions to equalize their travel distance and achieve synchronization without computing lengths explicitly."])),
    N.callout(
        "When to recognize this pattern: Two singly linked lists that might share a suffix (by reference). O(1) space required. Cannot modify the lists. Need to 'equalize' two sequences without knowing their relative lengths upfront.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same two-pointer / fast-slow pointer technique on linked lists:"),
    N.bullet(N.rich([("Linked List Cycle", {"bold": True}), " (Easy, #141) — Fast/slow pointers detect if a cycle exists; classic two-pointer on a single list."])),
    N.bullet(N.rich([("Linked List Cycle II", {"bold": True}), " (Medium, #142) — Find the cycle entry node; the math (Floyd's algorithm) parallels the m+n equalization here."])),
    N.bullet(N.rich([("Middle of the Linked List", {"bold": True}), " (Easy, #876) — Fast moves 2x, slow moves 1x; when fast hits end, slow is at midpoint."])),
    N.bullet(N.rich([("Remove Nth Node From End of List", {"bold": True}), " (Medium, #19) — Two pointers n steps apart; advance together until fast hits end."])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), " (Medium, #287) — Floyd's cycle detection on array indices; shares the offset-equalization math."])),
    N.bullet(N.rich([("Reorder List", {"bold": True}), " (Medium, #143) — Uses middle-finding (fast/slow) plus reversal; related composition of two-pointer techniques."])),
    N.para("These problems share the core technique: two pointers that travel different paths but are synchronized by a mathematical invariant (equal total distance, or equal speed with a fixed gap)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Linked List section, Fast-Slow Pointer / Two Pointer sub-patterns.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
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
