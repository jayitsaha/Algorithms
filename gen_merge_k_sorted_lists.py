"""gen_merge_k_sorted_lists.py — Notion update for Merge k Sorted Lists (#23)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81b5-a657-d5130f7c1c44"
SLUG    = "merge_k_sorted_lists"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=23,
    pattern="Heaps",
    subpatterns=["Min Heap with K Pointers"],
    tc="O(N log k)",
    sc="O(k)",
    key_insight="Heap of k fronts: always pop the global minimum in O(log k); push next node from same list.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of ", {}),
        ("k", {"code": True}),
        (" linked lists, each sorted in ascending order. Merge all of them into one sorted linked list and return it.", {}),
    ])),
    N.para("Example: lists = [[1,4,5],[1,3,4],[2,6]] → Output: 1→1→2→3→4→4→5→6"),
    N.divider(),
]

# ── Solution 1: Min-Heap ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Min-Heap with K Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have k sorted sequences and need to interleave them into one sorted sequence. At any point, the next output node must be the smallest un-output node across all lists."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: collect all N values, sort them O(N log N), rebuild. Correct, but ignores that all inputs are already sorted — we're throwing away structure. A naive linear scan over k heads each time is O(N·k) — too slow when k is large."),
        N.h4("The Key Observation"),
        N.para("Because each list is sorted, the global minimum at any moment is always among the k current front elements. We never need to look past position 0 of each list. A min-heap maintains the minimum of k items in O(log k) and supports replacement in O(log k)."),
        N.h4("Building the Solution"),
        N.para("1) Seed heap with all k list heads. 2) Pop minimum → append to output. 3) Push popped node's next (if any) back into heap. 4) Repeat. Heap size stays ≤ k throughout. Total: N pops + up to N pushes, each O(log k) → O(N log k)."),
        N.callout(
            "Analogy: Imagine k sorted stacks of papers on a table. A robot picks the top paper with the smallest number, places it on the result pile, then exposes the next paper from that same stack. The robot only ever looks at k top-papers at once — a min-heap IS the robot.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: heapq in Python"),
    N.para("Python's heapq module implements a binary min-heap. Key operations: heappush (O(log n)) and heappop (O(log n)). Crucially, Python compares tuples lexicographically — push (val, idx, node) so that equal values are broken by idx (a unique counter), preventing Python from comparing ListNode objects directly (which raises TypeError since ListNode has no __lt__)."),
    N.h3("Code"),
    N.code(
        "import heapq\n"
        "def mergeKLists(lists):\n"
        "    dummy = ListNode(0)   # sentinel head\n"
        "    tail = dummy\n"
        "    heap = []\n"
        "    idx = 0               # unique tie-breaker\n"
        "    for node in lists:\n"
        "        if node:          # skip null lists\n"
        "            heapq.heappush(heap, (node.val, idx, node))\n"
        "            idx += 1\n"
        "    while heap:\n"
        "        val, _, node = heapq.heappop(heap)  # O(log k)\n"
        "        tail.next = node\n"
        "        tail = tail.next\n"
        "        if node.next:\n"
        "            heapq.heappush(heap, (node.next.val, idx, node.next))\n"
        "            idx += 1\n"
        "    return dummy.next     # skip sentinel"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dummy = ListNode(0)", {"code": True}), " — Sentinel node; the actual merged list starts at dummy.next. Simplifies edge cases (empty output)."])),
    N.para(N.rich([("tail = dummy", {"code": True}), " — tail tracks where to append the next node in the output."])),
    N.para(N.rich([("heap = []; idx = 0", {"code": True}), " — Empty min-heap. idx is our unique integer counter for tie-breaking."])),
    N.para(N.rich([("for node in lists: if node:", {"code": True}), " — Skip null list heads. Null = empty list, nothing to seed."])),
    N.para(N.rich([("heapq.heappush(heap, (node.val, idx, node))", {"code": True}), " — Push a 3-tuple. Python min-heap compares by first element (val), then second (idx) if tied. Never reaches node comparison."])),
    N.para(N.rich([("val, _, node = heapq.heappop(heap)", {"code": True}), " — Extract the globally smallest front node. _ discards the idx we don't need after popping."])),
    N.para(N.rich([("tail.next = node; tail = tail.next", {"code": True}), " — Append popped node to output list; advance tail."])),
    N.para(N.rich([("if node.next:", {"code": True}), " — If this list has more nodes, push the next one to maintain the heap invariant."])),
    N.para(N.rich([("return dummy.next", {"code": True}), " — Skip the dummy sentinel; return the real merged list head."])),
    N.divider(),
]

# ── Solution 2: Divide & Conquer ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Divide & Conquer Pair-Merge"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Merging k lists is equivalent to: merge pairs of 2 lists repeatedly until 1 list remains. Like a tournament bracket — each round halves the number of lists."),
        N.h4("What Doesn't Work"),
        N.para("Merging sequentially (merge list 0+1, then result+list 2, etc.) is O(N·k) — each merge is O(current_size + list_i_size), and the current list grows each time."),
        N.h4("The Key Observation"),
        N.para("Pair-merging in parallel keeps the total work per round O(N) (each node is touched once per round). With log k rounds, total = O(N log k) — same as heap but without heapq overhead."),
        N.h4("Building the Solution"),
        N.para("Each round: zip adjacent pairs (lists[0]+lists[1], lists[2]+lists[3], ...). For odd k, the last list passes through unmated. After log k rounds, 1 merged list remains."),
    ]),
    N.h3("Code"),
    N.code(
        "def mergeKLists(lists):\n"
        "    if not lists:\n"
        "        return None\n"
        "    while len(lists) > 1:\n"
        "        merged = []\n"
        "        for i in range(0, len(lists), 2):\n"
        "            l1 = lists[i]\n"
        "            l2 = lists[i+1] if i+1 < len(lists) else None\n"
        "            merged.append(mergeTwoLists(l1, l2))\n"
        "        lists = merged\n"
        "    return lists[0]\n"
        "\n"
        "def mergeTwoLists(l1, l2):\n"
        "    dummy = ListNode(0)\n"
        "    tail = dummy\n"
        "    while l1 and l2:\n"
        "        if l1.val <= l2.val:\n"
        "            tail.next = l1; l1 = l1.next\n"
        "        else:\n"
        "            tail.next = l2; l2 = l2.next\n"
        "        tail = tail.next\n"
        "    tail.next = l1 or l2\n"
        "    return dummy.next"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("while len(lists) > 1:", {"code": True}), " — Keep halving until one list remains. log k iterations total."])),
    N.para(N.rich([("for i in range(0, len(lists), 2):", {"code": True}), " — Iterate by pairs. Pairs (lists[0],lists[1]), (lists[2],lists[3]), etc."])),
    N.para(N.rich([("l2 = lists[i+1] if i+1 < len(lists) else None", {"code": True}), " — Handle odd k: last list merges with None (effectively passes through)."])),
    N.para(N.rich([("lists = merged", {"code": True}), " — Replace lists with the merged results. Half as many lists next round."])),
    N.para(N.rich([("tail.next = l1 or l2", {"code": True}), " — Attach the non-exhausted tail; avoids a second while loop."])),
    N.divider(),
]

# ── Solution 3: Brute Force ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force: Collect All + Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Flatten all k lists into one array of values, sort it, then rebuild a linked list. Ignores sorted structure entirely but is very simple to code."),
        N.h4("What Doesn't Work (Why We Optimize)"),
        N.para("Sorting N items is O(N log N) regardless of k. When k is small (e.g. k=3, N=10^6), log k ≈ 1.6 vs log N ≈ 20 — the heap approach is over 10x fewer comparisons. The brute force also uses O(N) extra space to store all values."),
        N.h4("When This IS Acceptable"),
        N.para("Brute force is perfectly fine if k is close to N (e.g., k=N with 1-element lists) or in a quick prototype. Always propose it first in an interview before optimizing."),
    ]),
    N.h3("Code"),
    N.code(
        "def mergeKLists(lists):\n"
        "    vals = []\n"
        "    for node in lists:\n"
        "        while node:\n"
        "            vals.append(node.val)\n"
        "            node = node.next\n"
        "    vals.sort()  # O(N log N)\n"
        "    dummy = tail = ListNode(0)\n"
        "    for v in vals:\n"
        "        tail.next = ListNode(v)\n"
        "        tail = tail.next\n"
        "    return dummy.next"
    ),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",             "Time",        "Space"],
        ["Brute Force (sort)",   "O(N log N)",  "O(N)"],
        ["Naive K-scan",         "O(N·k)",      "O(1)"],
        ["Min-Heap ✓",           "O(N log k)",  "O(k)"],
        ["Divide & Conquer",     "O(N log k)",  "O(log k)"],
    ]),
    N.para("N = total nodes across all lists. k = number of lists. When k << N the heap approach greatly outperforms the brute force."),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Heaps"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Min Heap with K Pointers (Merge K Sorted)"])),
    N.callout(
        "When to recognize this pattern: 'Merge k sorted [lists / arrays / streams]' → min-heap of k fronts. "
        "'K-th smallest across k sorted structures' → same heap, stop after k pops. "
        "'Sorted matrix with sorted rows/cols' → treat rows as k lists. "
        "Any time you need the minimum from k sorted sources repeatedly and efficiently.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Merge K Sorted / Min-Heap technique:"),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), " (Easy) — Two-pointer merge; the building block for this problem (#21)"])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), " (Medium) — Same min-heap; matrix rows = k sorted lists (#378)"])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold": True}), " (Medium) — Heap over k sorted pair-streams (#373)"])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold": True}), " (Hard) — Min-heap + sliding window; direct extension (#632)"])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), " (Hard) — Two Heaps sub-pattern; related heap usage (#295)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Min-heap tracks room end-times; Greedy + Heap (#253)"])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), " (Medium) — Heap for Top K sub-pattern; same heapq mechanics (#347)"])),
    N.para("These problems share the same core technique: maintain a min-heap of k representatives; pop minimum, advance that stream."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Heaps → Sub-Pattern: Merge K Sorted", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all ───────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
