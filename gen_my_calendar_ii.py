"""
gen_my_calendar_ii.py — Notion update for My Calendar II (LeetCode 731)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812c-8356-f35daf2c407b"

# ── 1. Set page properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=731,
    pattern="Trees",
    subpatterns=["Two Lists or Segment Tree"],
    tc="O(n) per call",
    sc="O(n)",
    key_insight="Track double-booked regions separately; reject new event only if it intersects any double-booked interval (triple booking). Order: check overlaps FIRST, then expand.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement a class ", {}),
        ("MyCalendarTwo", {"code": True}),
        (" that supports adding events. Each event is a ", {}),
        ("half-open interval", {"bold": True}),
        (" [start, end). An event can be booked only if it does NOT cause a ", {}),
        ("triple booking", {"bold": True}),
        (" — a moment in time covered by 3 or more events. Return ", {}),
        ("true", {"code": True}),
        (" if the event was booked successfully, ", {}),
        ("false", {"code": True}),
        (" otherwise. (Double-booking is allowed.)", {}),
    ])),
    N.divider(),
]

# Solution 1 — Two Lists
blocks += [
    N.h2("Solution 1 — Two Lists (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must accept events that don't triple-overlap any instant, and reject those that do. The hard part: how do we efficiently know if adding a new event would cause any moment to be covered by 3 events?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for every new event, check all pairs of existing events to see if all three overlap. O(n²) per booking. Too slow for large inputs."),
        N.h4("The Key Observation"),
        N.para("Instead of checking all triples, precompute where double-bookings already exist. A triple booking can only occur where a new event intersects a double-booked region. So the check reduces to: 'Does the new event overlap any interval in my double-booking list?' — an O(n) scan."),
        N.h4("Building the Solution"),
        N.para("Maintain two lists: calendar (all accepted events) and overlaps (all double-booked regions = pairwise intersections). On each book call: (1) if the new event overlaps any interval in overlaps → reject (triple booking). (2) Otherwise, compute all intersections with calendar events and add them to overlaps. (3) Append to calendar and return true."),
        N.callout("Analogy: Think of overlaps as a 'hot zone map'. New events can't enter the hot zones, but they extend hot zones by intersecting with existing bookings.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""class MyCalendarTwo:
    def __init__(self):
        self.calendar = []   # all accepted [start, end) bookings
        self.overlaps = []   # all double-booked regions

    def book(self, start: int, end: int) -> bool:
        # Step 1: Check for triple-booking risk
        for a, b in self.overlaps:
            if start < b and a < end:   # overlap with a double-booked region
                return False            # triple booking — reject

        # Step 2: Expand double-booked regions with new intersections
        for a, b in self.calendar:
            lo = max(start, a)
            hi = min(end, b)
            if lo < hi:                 # non-empty intersection
                self.overlaps.append((lo, hi))

        # Step 3: Accept the booking
        self.calendar.append((start, end))
        return True
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.calendar = []", {"code": True}), (" — Stores every accepted booking interval. Grows by 1 per successful book() call.", {})])),
    N.para(N.rich([("self.overlaps = []", {"code": True}), (" — Stores every double-booked region. This is the union of all pairwise intersections of events in calendar.", {})])),
    N.para(N.rich([("for a, b in self.overlaps:", {"code": True}), (" — Scan all known double-booked regions FIRST. This is the triple-booking guard.", {})])),
    N.para(N.rich([("if start < b and a < end:", {"code": True}), (" — Standard half-open interval overlap check: [start,end) overlaps [a,b) iff start<b AND a<end.", {})])),
    N.para(N.rich([("return False", {"code": True}), (" — The new event would turn a double-booked region into a triple-booked one. Reject it.", {})])),
    N.para(N.rich([("for a, b in self.calendar:", {"code": True}), (" — After the triple check passes, scan calendar to find new double-booked regions.", {})])),
    N.para(N.rich([("lo = max(start, a)", {"code": True}), (" — Intersection start: the later of the two intervals' starts.", {})])),
    N.para(N.rich([("hi = min(end, b)", {"code": True}), (" — Intersection end: the earlier of the two intervals' ends.", {})])),
    N.para(N.rich([("if lo < hi:", {"code": True}), (" — Intersection is non-empty (lo < hi means positive length region).", {})])),
    N.para(N.rich([("self.overlaps.append((lo, hi))", {"code": True}), (" — Record this new double-booked region for future triple-booking checks.", {})])),
    N.para(N.rich([("self.calendar.append((start, end))", {"code": True}), (" — Accept the booking by adding it to the full list.", {})])),
    N.divider(),
]

# Solution 2 — Segment Tree
blocks += [
    N.h2("Solution 2 — Segment Tree (O(log n) per call)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we do better than O(n) per booking? A segment tree on the time range can answer 'what is the maximum booking count in range [s,e)?' in O(log n), and update it in O(log n)."),
        N.h4("What Doesn't Work"),
        N.para("A static segment tree requires knowing the full time range upfront and uses O(MAX_TIME) space. Since times can be up to 10^9, we need a dynamic (implicit/lazy) segment tree."),
        N.h4("The Key Observation"),
        N.para("Use a dictionary-based segment tree. Each node stores the max count increment contributed by events fully covering its range. A range update [s,e) increments affected nodes, and the query returns the max count. If the result would reach 3, reject and undo."),
        N.h4("Building the Solution"),
        N.para("The update function recurses: if fully outside query range, return 0. If fully inside, increment this node's count and return it. Otherwise split and recurse. Return the max across subtree. If this max is >= 3 after update, we need to undo — but the two-lists approach is simpler in practice for interviews."),
    ]),
    N.h3("Code"),
    N.code(
"""class MyCalendarTwo:
    def __init__(self):
        self.tree = {}   # node_id -> booking count for that node

    def update(self, lo, hi, l, r, node):
        if lo >= r or hi <= l:
            return 0                             # out of range
        if lo <= l and r <= hi:
            self.tree[node] = self.tree.get(node, 0) + 1
            return self.tree[node]               # fully covered
        mid = (l + r) // 2
        left  = self.update(lo, hi, l, mid, 2 * node)
        right = self.update(lo, hi, mid, r, 2 * node + 1)
        return self.tree.get(node, 0) + max(left, right)

    def undo(self, lo, hi, l, r, node):
        if lo >= r or hi <= l:
            return
        if lo <= l and r <= hi:
            self.tree[node] = self.tree.get(node, 0) - 1
            return
        mid = (l + r) // 2
        self.undo(lo, hi, l, mid, 2 * node)
        self.undo(lo, hi, mid, r, 2 * node + 1)

    def book(self, start: int, end: int) -> bool:
        MAX = 10 ** 9
        if self.update(start, end, 0, MAX, 1) >= 3:
            self.undo(start, end, 0, MAX, 1)
            return False
        return True
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.tree = {}", {"code": True}), (" — Sparse dictionary-based segment tree. Only nodes that have been incremented exist.", {})])),
    N.para(N.rich([("if lo >= r or hi <= l: return 0", {"code": True}), (" — Query range [lo,hi) doesn't intersect node's range [l,r) — contribute nothing.", {})])),
    N.para(N.rich([("if lo <= l and r <= hi:", {"code": True}), (" — Node's range is fully inside query. Increment its counter and return the updated value.", {})])),
    N.para(N.rich([("return self.tree.get(node,0) + max(left, right)", {"code": True}), (" — Partial overlap: this node's count plus the max from children.", {})])),
    N.para(N.rich([("if self.update(...) >= 3:", {"code": True}), (" — After tentative update, if any region would be booked 3+ times, undo and reject.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time per call", "Space", "Notes"],
        ["Two Lists", "O(n)", "O(n)", "n = number of bookings so far"],
        ["Segment Tree", "O(log MAX_TIME)", "O(n log MAX_TIME)", "MAX_TIME = 10^9; sparse tree"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees (Segment Tree variant) / Interval Problems", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Lists or Segment Tree — track k-1 overlap levels to enforce k-booking limit", {})])),
    N.callout(
        "When to recognize this pattern: 'At most k events can overlap at any time' + online queries (events arrive one at a time). If k=2 and n is small, Two Lists is elegant. If k>2 or n is large, use segment tree or difference array.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique (interval overlap tracking and bounding):"),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), (" (Easy) — No double-bookings; single-list calendar scan", {})])),
    N.bullet(N.rich([("My Calendar III", {"bold": True}), (" (Hard) — Max k-booking count; difference array with sorted map or segment tree", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Min rooms = max simultaneous events; related overlap counting", {})])),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), (" (Medium) — Merge overlapping intervals; same [max(a,c), min(b,d)) intersection formula", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), (" (Medium) — Insert into sorted interval list; identical overlap check", {})])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}), (" (Hard) — Find gaps in merged employee schedules; interval overlap foundation", {})])),
    N.bullet(N.rich([("Range Module", {"bold": True}), (" (Hard) — Track which ranges are covered; segment tree of intervals", {})])),
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("my_calendar_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page {PAGE_ID}.")
print("NOTION OK", PAGE_ID)
