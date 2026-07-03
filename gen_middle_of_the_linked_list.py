"""
gen_middle_of_the_linked_list.py
Notion page builder for LeetCode #876 — Middle of the Linked List
Pattern: Linked List | Subpattern: Slow = 1, Fast = 2 (Guide Section 5.3)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8160-a922-c5b495728f00"  # already created

# ── Step 0: create the page ───────────────────────────────────────────────────
if PAGE_ID is None:
    PAGE_ID = N.create_page("Middle of the Linked List", 876, "Easy", "🟢")
    print(f"Created page: {PAGE_ID}")
else:
    print(f"Using existing page: {PAGE_ID}")

# ── Step 1: set properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=876,
    pattern="Linked List",
    subpatterns=["Slow=1 Fast=2"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Fast pointer moves 2x, slow moves 1x; when fast exits, slow is at middle.",
    icon="🟢",
)
print("Properties set.")

# ── Step 2: wipe any existing body ───────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Step 3: build body blocks ─────────────────────────────────────────────────

# ── Problem Statement ──────────────────────────────────────────────────────────
blocks = []
blocks.append(N.h2("Problem"))
blocks.append(N.para(N.rich([
    "Given the head of a singly linked list, return the middle node of the linked list. "
    "If there are two middle nodes, return the ",
    ("second", {"bold": True}),
    " middle node."
])))
blocks.append(N.divider())

# ── Solution 1 — Fast & Slow Pointers (Interview Pick) ───────────────────────
blocks.append(N.h2("Solution 1 — Fast & Slow Pointers (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "A linked list has no index and no stored length. You cannot do arr[n//2]. "
        "The only operation available is following the .next pointer one step at a time. "
        "So finding the middle means: how do I stop at the exact halfway point without "
        "knowing the total length in advance?"
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "The brute-force approach traverses the entire list to count n nodes, "
        "then resets to head and walks n//2 steps. This is correct and O(n) time O(1) space, "
        "but it visits every node twice — two full passes. We want a single-pass solution."
    ),
    N.h4("The Key Observation"),
    N.para(
        "If pointer A moves at speed 1 and pointer B moves at speed 2, "
        "when B has walked k steps, A has walked k/2 steps. "
        "When B exits the list (walked n steps), A is at position n/2 — the middle. "
        "We don't need to know n in advance. The speed ratio does the math for us automatically."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Place slow and fast at head. "
        "2. Each iteration: slow.next (1 step), fast.next.next (2 steps). "
        "3. Loop condition: 'while fast and fast.next' — ensures we can safely do the 2-step advance. "
        "4. When loop exits, slow is at the middle. "
        "For even-length lists, slow lands on the second middle (exactly what the problem wants)."
    ),
    N.callout(
        "Analogy: Two runners on a track. Runner A jogs at half the speed of Runner B. "
        "When B crosses the finish line, A is exactly at the halfway mark. "
        "No stopwatch needed — the speed ratio gives us the midpoint automatically.",
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("🔬 Algorithm Deep-Dive: Floyd's Tortoise and Hare"))
blocks.append(N.para(N.rich([
    ("Floyd's Tortoise and Hare", {"bold": True}),
    " — Origin: Robert W. Floyd, 1967. Originally designed for cycle detection in sequences, "
    "but the same speed-ratio invariant enables middle-finding.\n\n"
    "Core invariant: after k iterations, fast is at position 2k and slow is at position k "
    "(both measured from head). When fast can no longer advance (position ≥ n), slow is at n/2.\n\n"
    "Why it works: the 2:1 speed ratio is a linear relationship. Slow's position is always "
    "exactly half of fast's position. No arithmetic, no counters — the pointer movement "
    "encodes the computation.\n\n"
    "Recognize when: any linked-list problem asking for a positional fraction of the list "
    "(middle, 1/3rd, kth from end variants), or cycle detection/start-of-cycle."
])))
blocks.append(N.divider())

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def middleNode(head):\n"
    "    slow = fast = head\n"
    "    while fast and fast.next:\n"
    "        slow = slow.next\n"
    "        fast = fast.next.next\n"
    "    return slow",
    "python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("slow = fast = head", {"code": True}),
    " — Both pointers start at the first node. They race from the same position."
])))
blocks.append(N.para(N.rich([
    ("while fast and fast.next:", {"code": True}),
    " — Two-part guard: (1) fast must not be None so we can read fast.next; "
    "(2) fast.next must not be None so we can safely do fast.next.next. "
    "If either is None, we've reached the end."
])))
blocks.append(N.para(N.rich([
    ("slow = slow.next", {"code": True}),
    " — Tortoise takes 1 step."
])))
blocks.append(N.para(N.rich([
    ("fast = fast.next.next", {"code": True}),
    " — Hare takes 2 steps. Safe because we confirmed fast.next ≠ None in the loop condition."
])))
blocks.append(N.para(N.rich([
    ("return slow", {"code": True}),
    " — Loop exited because fast can't take 2 more steps. "
    "Slow has traveled exactly half of fast's distance — it is at the middle node."
])))
blocks.append(N.divider())

# ── Solution 2 — Two-Pass Count ───────────────────────────────────────────────
blocks.append(N.h2("Solution 2 — Two-Pass Length Count (Brute Force)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "If we know the total length n, we can simply walk n//2 steps from head. "
        "The challenge is we don't know n — so we learn it first, then walk."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "For a single-pass solution with only one pointer, we'd need to know "
        "in advance when to stop — which requires knowing n. That's circular. "
        "Hence the two-pass approach: learn n, then use it."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Any traversal that reaches the null sentinel has counted all n nodes. "
        "After that first pass, n//2 gives us the middle index in a second pass."
    ),
    N.h4("Building the Solution"),
    N.para(
        "Pass 1: traverse entire list, count n. "
        "Pass 2: reset to head, advance n//2 times, return current."
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def middleNode(head):\n"
    "    n, cur = 0, head\n"
    "    while cur:\n"
    "        n += 1\n"
    "        cur = cur.next\n"
    "    cur = head\n"
    "    for _ in range(n // 2):\n"
    "        cur = cur.next\n"
    "    return cur",
    "python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("n, cur = 0, head", {"code": True}),
    " — Initialize counter and traversal pointer."
])))
blocks.append(N.para(N.rich([
    ("while cur: n += 1; cur = cur.next", {"code": True}),
    " — Count every node. After this, n = total number of nodes."
])))
blocks.append(N.para(N.rich([
    ("cur = head", {"code": True}),
    " — Reset to head for the second traversal."
])))
blocks.append(N.para(N.rich([
    ("for _ in range(n // 2): cur = cur.next", {"code": True}),
    " — Advance exactly n//2 steps. Integer division naturally gives the "
    "second middle for even-length lists."
])))
blocks.append(N.para(N.rich([
    ("return cur", {"code": True}),
    " — cur is now at the middle node."
])))
blocks.append(N.divider())

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution",                        "Time",  "Space",  "Passes"],
    ["Fast & Slow Pointers (Optimal)",  "O(n)",  "O(1)",   "1"],
    ["Two-Pass Count",                  "O(n)",  "O(1)",   "2"],
    ["Array Copy",                      "O(n)",  "O(n)",   "1"],
]))
blocks.append(N.divider())

# ── Pattern Classification ────────────────────────────────────────────────────
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([
    ("Main Pattern: ", {"bold": True}),
    "Linked List (Section 5 — Linked List Patterns)"
])))
blocks.append(N.para(N.rich([
    ("Sub-Pattern(s): ", {"bold": True}),
    "Slow=1 Fast=2 (Guide Section 5.3: Fast and Slow Pointers / Floyd's Cycle)"
])))
blocks.append(N.callout(
    "When to recognize this pattern:\n"
    "• Problem involves a singly linked list with no length field\n"
    "• Need to find a fractional position (middle, 1/3, etc.) in one pass\n"
    "• Keywords: 'middle node', 'cycle detection', 'palindrome linked list'\n"
    "• Any two-speed traversal where you want to stop at a relative position",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──────────────────────────────────────────────────────────
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique (Fast-Slow Pointers):"))
related = [
    ("Linked List Cycle",                         "Easy",   "#141 — Detect cycle; fast/slow meet if and only if cycle exists"),
    ("Linked List Cycle II",                       "Medium", "#142 — Find cycle start; Floyd's full algorithm with pointer reset"),
    ("Palindrome Linked List",                     "Easy",   "#234 — Find middle, reverse second half in-place, compare"),
    ("Delete the Middle Node of a Linked List",    "Medium", "#2095 — Variant: stop slow one step early to get predecessor of middle"),
    ("Happy Number",                               "Easy",   "#202 — Fast/slow on digit-square sequence; cycle = not happy"),
    ("Remove Nth Node From End of List",           "Medium", "#19 — N-gap two-pointer variant to isolate Nth from end"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        f" ({diff}) — {note}"
    ])))
blocks.append(N.para(
    "These problems share the core technique of using two pointers at different speeds "
    "to exploit the 2:1 distance ratio for positional targeting on linked lists."
))
blocks.append(N.callout(
    "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 5.3 — "
    "Fast and Slow Pointers (Floyd's Cycle). Sub-Pattern: Slow=1 Fast=2.",
    "📚", "gray_background"
))

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("middle_of_the_linked_list")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
