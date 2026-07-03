"""
gen_my_calendar_i.py — Notion page builder for My Calendar I (#729)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e8-a402-e30f4bbac68f"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=729,
    pattern="Trees",
    subpatterns=["BST/TreeMap Interval Check"],
    tc="O(n log n) avg",
    sc="O(n)",
    key_insight="Keep booked intervals in a BST sorted by start; at each node go left if e<=node.start, right if s>=node.end, else conflict.",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
print("Building blocks...")
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement a ", {}),
        ("MyCalendar", {"code": True}),
        (" class that stores events as half-open intervals ", {}),
        ("[start, end)", {"code": True}),
        (". Call ", {}),
        ("book(start, end)", {"code": True}),
        (" to add an event. If the event would cause a double-booking (any overlap with an existing event), return ", {}),
        ("False", {"code": True}),
        (" without adding it; otherwise add it and return ", {}),
        ("True", {"code": True}),
        (". A double-booking occurs when two events share at least one time in common.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Manual BST (Interview Pick)
SOLN1_CODE = """class Node:
    def __init__(self, s, e):
        self.start, self.end = s, e
        self.left = self.right = None

class MyCalendar:
    def __init__(self):
        self.root = None

    def book(self, start: int, end: int) -> bool:
        result = self._insert(self.root, start, end)
        if result is None:
            return False
        self.root = result
        return True

    def _insert(self, node, s, e):
        if node is None:
            return Node(s, e)          # empty slot → insert here
        if e <= node.start:            # new event ends before node → go left
            node.left = self._insert(node.left, s, e)
            if node.left is None:
                return None            # conflict propagated up
        elif s >= node.end:            # new event starts after node ends → go right
            node.right = self._insert(node.right, s, e)
            if node.right is None:
                return None            # conflict propagated up
        else:
            return None                # OVERLAP DETECTED → return False signal
        return node                    # rebuild BST path"""

blocks += [
    N.h2("Solution 1 — Manual BST (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure that stores intervals and quickly answers: 'does this new interval overlap any stored interval?' The brute-force answer is scan all stored intervals — O(n). Can we skip checking most intervals?"),
        N.h4("What Doesn't Work"),
        N.para("A plain sorted array of starts doesn't help — you'd still need to check all intervals with start < end. A hash map doesn't help because intervals aren't discrete keys. We need structural ordering."),
        N.h4("The Key Observation"),
        N.para("If intervals are sorted by start time, for new [s, e) we can binary search to find where s would go. Only the interval just before (predecessor: largest start <= s) and just after (successor: smallest start > s) can possibly conflict. The BST captures this ordering in a tree structure so we navigate directly to potential conflicts."),
        N.h4("Building the Solution"),
        N.para("At each BST node [ns, ne): if our new event ends before ns (e <= ns), no overlap is possible here — go left where starts are even smaller. If our new event starts after ne (s >= ne), no overlap here — go right. Otherwise we've found an overlap. If we reach null, there's an empty slot — insert there."),
        N.callout("Analogy: It's like finding your seat in a theater — walk left if your row number is smaller than the current sign, right if larger, or if you're in the same row already, conflict!", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLN1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("Node.__init__", {"code": True}), " — BST node stores one booked interval [start, end) and left/right child pointers (both None initially)."])),
    N.para(N.rich([("self.root = None", {"code": True}), " — The BST starts empty; the first booking becomes the root."])),
    N.para(N.rich([("result = self._insert(self.root, start, end)", {"code": True}), " — Try to insert; returns the (possibly new) root node, or None to signal a conflict."])),
    N.para(N.rich([("if result is None: return False", {"code": True}), " — None return from _insert means a conflict was detected somewhere in the tree."])),
    N.para(N.rich([("self.root = result", {"code": True}), " — Update root (necessary because the first call returns a brand-new Node as the root)."])),
    N.para(N.rich([("if node is None: return Node(s, e)", {"code": True}), " — We've navigated to an empty leaf position — this is where the new event belongs. Insert and signal success."])),
    N.para(N.rich([("if e <= node.start:", {"code": True}), " — The new event ends at or before this node starts. No overlap possible. Recurse left (all left-subtree events have even smaller starts)."])),
    N.para(N.rich([("elif s >= node.end:", {"code": True}), " — The new event starts at or after this node ends. No overlap possible. Recurse right."])),
    N.para(N.rich([("else: return None", {"code": True}), " — Neither non-overlap condition holds: s < node.end AND node.start < e → OVERLAP DETECTED. Return None to propagate the conflict signal upward."])),
    N.para(N.rich([("return node", {"code": True}), " — Return the current node so the parent can reassign node.left or node.right, maintaining BST structure."])),
    N.divider(),
]

# Solution 2 — SortedList
SOLN2_CODE = """from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.cal = SortedList()   # sorted by (start, end) tuples

    def book(self, start: int, end: int) -> bool:
        i = self.cal.bisect_left((start, end))  # insertion position
        # Check predecessor: does it end after our start?
        if i > 0 and self.cal[i - 1][1] > start:
            return False
        # Check successor: does it start before our end?
        if i < len(self.cal) and self.cal[i][0] < end:
            return False
        self.cal.add((start, end))
        return True"""

blocks += [
    N.h2("Solution 2 — SortedList with Binary Search"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem: check two neighbors in a sorted structure. But instead of building a BST manually, use Python's SortedList which maintains sorted order automatically and provides O(log n) bisect."),
        N.h4("The Key Observation"),
        N.para("After finding insertion position i, only two candidates can conflict: cal[i-1] (predecessor, largest start <= ours) and cal[i] (successor, smallest start > ours). For the predecessor: it ends after our start? Conflict. For the successor: it starts before our end? Conflict."),
        N.h4("Building the Solution"),
        N.para("bisect_left((start, end)) gives us position i. Check pred: cal[i-1][1] > start means predecessor's end is after our start → overlap. Check succ: cal[i][0] < end means successor's start is before our end → overlap. Why only these two? Everything before pred starts earlier and ends earlier (no overlap possible), everything after succ starts later (no overlap possible)."),
        N.callout("SortedList guarantees O(log n) even for sorted input — unlike a manual BST which degenerates to O(n). Use this in production.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("SortedList()", {"code": True}), " — From the sortedcontainers library; maintains items in sorted order. Tuples (start, end) sort by start first, then end — perfect for our use case."])),
    N.para(N.rich([("bisect_left((start, end))", {"code": True}), " — Binary search for where (start, end) would be inserted. O(log n). Returns index i such that all cal[j] for j < i have start <= our start."])),
    N.para(N.rich([("cal[i-1][1] > start", {"code": True}), " — Predecessor's end time is after our start → they overlap. Note: if cal[i-1][1] == start, they're adjacent (not overlapping), so we use strict >."])),
    N.para(N.rich([("cal[i][0] < end", {"code": True}), " — Successor's start time is before our end → they overlap. If cal[i][0] == end, they're adjacent (OK), so strict <."])),
    N.para(N.rich([("self.cal.add((start, end))", {"code": True}), " — Insert the new interval in O(log n). SortedList maintains sorted order automatically."])),
    N.divider(),
]

# Solution 3 — Brute Force
SOLN3_CODE = """class MyCalendar:
    def __init__(self):
        self.events = []   # unsorted list of booked intervals

    def book(self, start: int, end: int) -> bool:
        for s, e in self.events:
            if s < end and start < e:   # universal overlap test
                return False
        self.events.append((start, end))
        return True"""

blocks += [
    N.h2("Solution 3 — Brute Force (Propose First in Interviews)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest correct approach: for each new booking, check it against every stored booking using the overlap condition. Store bookings in a plain list."),
        N.h4("The Key Observation"),
        N.para("The overlap condition s < end AND start < e is the primitive test. Once you can do this correctly, you can optimize. Propose brute force first, then optimize."),
        N.callout("Always start here in an interview — it shows you understand the problem before optimizing.", "🎯", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(SOLN3_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for s, e in self.events:", {"code": True}), " — Iterate over every booked interval. O(n) per call — this is the bottleneck."])),
    N.para(N.rich([("if s < end and start < e:", {"code": True}), " — The universal overlap test. Equivalent to: NOT (e <= s OR end <= s). If both conditions hold, intervals share a common time."])),
    N.para(N.rich([("self.events.append((start, end))", {"code": True}), " — No conflict found; add to the unordered list."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time / call", "n calls total", "Space"],
        ["Brute Force", "O(n)", "O(n²)", "O(n)"],
        ["Manual BST (Interview Pick)", "O(log n) avg", "O(n log n) avg", "O(n)"],
        ["SortedList", "O(log n)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (BST property used to maintain sorted order of intervals for O(log n) conflict detection)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BST/TreeMap Interval Check — insert intervals into a BST sorted by start time; navigate left/right to find or rule out conflicts in O(log n) per operation"])),
    N.callout(
        "When to recognize this pattern: 'Add intervals dynamically and check for overlap' — especially if you need better than O(n) per query. Key signals: calendar/scheduling problems, no double-booking constraint, dynamic insertion. The 3-way BST decision (go left / go right / conflict) is the signature move.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BST/sorted interval management):"),
    N.bullet(N.rich([("My Calendar II", {"bold": True}), " (Medium) — Allow at most 2 simultaneous bookings; track 'already overlapping' intervals separately (#731)"])),
    N.bullet(N.rich([("My Calendar III", {"bold": True}), " (Hard) — Return max K simultaneous bookings; use difference array or segment tree (#732)"])),
    N.bullet(N.rich([("Meeting Rooms", {"bold": True}), " (Easy) — Can one person attend all meetings? Sort by start, check adjacent pairs for overlap (#252)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Min rooms needed; min-heap or sorted event sweep with two counters (#253)"])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), " (Medium) — Insert into sorted non-overlapping interval list; merge as needed (#57)"])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — Minimum removals to eliminate all overlaps; greedy by end time (#435)"])),
    N.bullet(N.rich([("Data Stream as Disjoint Intervals", {"bold": True}), " (Hard) — Merge streaming integers into sorted disjoint intervals; SortedList ideal (#352)"])),
    N.para("These problems share the core technique: maintain sorted order of intervals to enable O(log n) conflict/neighbor queries."),
    N.callout("Sub-pattern Source: Analysis — BST/TreeMap Interval Check is the standard name for this technique in interval scheduling literature.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("my_calendar_i")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
