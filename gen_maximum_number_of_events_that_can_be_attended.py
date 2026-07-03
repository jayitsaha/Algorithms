"""
Notion regeneration script for:
  Maximum Number of Events That Can Be Attended (#1353)
Run from the Algorithms/ directory.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8172-8086-f5f39fe9be5c"
SLUG = "maximum_number_of_events_that_can_be_attended"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1353,
    pattern="Intervals",
    subpatterns=["Sort + Min Heap"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Greedy: on each day, attend the open event ending soonest (min-heap by end-day). Sort by start, sweep days, prune expired with heap[0] < day.",
    icon="🟡"
)
print("Properties set OK")

# ── Step 2: Wipe old body ───────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── Step 3: Build new body ──────────────────────────────────────────────────
PROBLEM_STMT = (
    "Given an array events where events[i] = [startDay, endDay], "
    "return the maximum number of events you can attend. "
    "You can attend an event i on any day d where startDay <= d <= endDay. "
    "You can only attend one event per day."
)

SOL1_CODE = """import heapq

def maxEvents(events: list) -> int:
    events.sort()                          # sort by start day
    n = len(events)
    i = 0
    heap = []                              # min-heap of end-days
    count = 0
    max_day = max(e[1] for e in events)   # upper bound of sweep
    for day in range(1, max_day + 1):
        # LOAD: push all events whose start <= today
        while i < n and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])
            i += 1
        # PRUNE: discard events that expired before today
        while heap and heap[0] < day:
            heapq.heappop(heap)
        # ATTEND: greedily attend the soonest-ending event
        if heap:
            heapq.heappop(heap)
            count += 1
    return count"""

SOL2_CODE = """def maxEvents_brute(events: list) -> int:
    # Sort by end day (urgency-first)
    events.sort(key=lambda e: e[1])
    used_days = set()
    count = 0
    for start, end in events:
        # Find the earliest free day in this event's window
        for day in range(start, end + 1):
            if day not in used_days:
                used_days.add(day)
                count += 1
                break
    return count"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# ── Solution 1: Optimal ──
blocks += [
    N.h2("Solution 1 — Sort + Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We are scheduling a series of events on a single-track calendar. "
            "Each event has a flexible window [start, end] — we can attend it on any single day within that range. "
            "We want to maximize the number of distinct events attended."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive approach: sort by end day and greedily scan each event's window for a free day. "
            "This works correctness-wise but costs O(n * window_length) — O(n²) in the worst case. "
            "For n = 10⁵ with events spanning 10⁵ days, this TLEs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Among all currently open events (started but not yet expired), "
            "always attend the one ending soonest. "
            "An event with deadline tomorrow is more constrained than one ending next week — "
            "skip it today and it may expire before we revisit it. "
            "The later-ending event can always be deferred."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1) Sort events by start day so we can efficiently load them into a data structure as days advance. "
            "2) Sweep days 1 → max_end. On each day: (a) push all events with start ≤ day into a min-heap (key = end-day). "
            "(b) Pop expired events where heap[0] < day — strictly less than, so events ending today are preserved. "
            "(c) If heap non-empty, pop the minimum (soonest-ending) and count it. "
            "Each event is pushed and popped at most once → O(n log n) total."
        ),
        N.callout(
            "Analogy: Think of a conference where every morning you look at your urgency inbox (min-heap) "
            "and attend the talk whose schedule closes soonest. You never regret this — "
            "skipping a tight deadline to attend something comfortable is always a mistake.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("events.sort()", {"code": True}), " — Sort events lexicographically by start day (Python tuple sort). Ties broken by end day, which is fine."])),
    N.para(N.rich([("i = 0", {"code": True}), " — Pointer into sorted events; tracks which events have been loaded into the heap."])),
    N.para(N.rich([("heap = []", {"code": True}), " — Python list used as a min-heap via heapq. Each entry is an end-day integer (min-heap key = end-day = urgency measure)."])),
    N.para(N.rich([("max_day = max(e[1] for e in events)", {"code": True}), " — The last possible event day; bounds the sweep so we stop early."])),
    N.para(N.rich([("for day in range(1, max_day + 1):", {"code": True}), " — Sweep every calendar day. We don't need to check days before the first event start."])),
    N.para(N.rich([("while i < n and events[i][0] <= day:", {"code": True}), " — LOAD phase: any event that has started on or before today becomes open."])),
    N.para(N.rich([("heapq.heappush(heap, events[i][1])", {"code": True}), " — Push the event's end-day onto the min-heap. The end-day is the urgency key."])),
    N.para(N.rich([("while heap and heap[0] < day:", {"code": True}), " — PRUNE phase: events with end < today have expired. Note: heap[0] < day (STRICT), not <=. Events ending today are still attendable."])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), " (inside prune loop) — Discard expired event. It cannot be attended anymore."])),
    N.para(N.rich([("if heap:", {"code": True}), " — ATTEND phase: is there any open event for today?"])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), " (inside attend block) — Pop the minimum end-day = the most urgent open event. We attend it today."])),
    N.para(N.rich([("count += 1", {"code": True}), " — We used today's slot for the soonest-ending event."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force (O(n²), for intuition)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Sort all events by their end day (urgency order). For each event, find the earliest free day in its window and attend it there."),
        N.h4("What Doesn't Work (scaling)"),
        N.para("For each event we scan up to (end - start + 1) days. If all events span 10⁵ days, this is O(n * 10⁵) total — TLE for large inputs."),
        N.h4("The Key Observation"),
        N.para("The correctness holds because we process events in urgency order. But efficiency is poor. This brute force is useful for small inputs and for building intuition."),
        N.h4("Building the Solution"),
        N.para("Sort by end day. Use a set of 'used_days'. For each event, iterate from start to end and take the first free day."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("events.sort(key=lambda e: e[1])", {"code": True}), " — Sort by end day (deadline order) so urgent events get first pick of free days."])),
    N.para(N.rich([("used_days = set()", {"code": True}), " — Track which days are already occupied."])),
    N.para(N.rich([("for day in range(start, end + 1):", {"code": True}), " — Try each day in the event's window from start to end."])),
    N.para(N.rich([("if day not in used_days:", {"code": True}), " — This day is free — attend the event here."])),
    N.para(N.rich([("break", {"code": True}), " — Stop searching once we've attended this event; move on to the next."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n² log n)", "O(n)"],
        ["Sort + Min-Heap (optimal)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sort + Min Heap"])),
    N.callout(
        "When to recognize this pattern: "
        "'Attend / process as many tasks/events as possible within [start, end] windows' + "
        "'one resource per time unit' + 'maximize count' → sort by start, sweep days, "
        "min-heap by deadline. If events carry values → switch to DP.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Min Heap or Greedy Interval technique:"),
]
related = [
    ("Maximum Number of Events That Can Be Attended II", "Hard", "Same problem but with event values; greedy fails, need DP + binary search (#1751)"),
    ("Single-Threaded CPU", "Medium", "Sort + min-heap; process tasks by shortest processing time when CPU is free (#1834)"),
    ("Meeting Rooms II", "Medium", "Minimum rooms needed; sweep line + min-heap on end-times (#253)"),
    ("Task Scheduler", "Medium", "Greedy scheduling with cooldown; max-heap by frequency (#621)"),
    ("Non-overlapping Intervals", "Medium", "Remove minimum intervals for non-overlapping; sort by end, greedy count (#435)"),
    ("Minimum Number of Arrows to Burst Balloons", "Medium", "Group overlapping intervals greedily by end (#452)"),
    ("Furthest Building You Can Reach", "Medium", "Greedy min-heap to manage limited ladders optimally (#1642)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}), f" ({diff}) — {note}"
    ])))

blocks += [
    N.para("These problems share the greedy core: prioritize by deadline (min-heap on end times) while sweeping through time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 14 (Intervals), line 748. Sub-Pattern: Sort + Min Heap.", "📚", "gray_background"),
]

# ── Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
