"""gen_meeting_rooms_ii.py — Notion page for Meeting Rooms II (#253)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-814b-8019-f6941fb998f7"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=253,
    pattern="Intervals",
    subpatterns=["Greedy + Heap"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by start; min-heap of end times lets you reuse the earliest-freeing room; heap size = answer.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ──
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} old blocks.")

# ── 3. Build body ──
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of meeting time intervals where ", {}),
        ("intervals[i] = [start_i, end_i]", {"code": True}),
        (", find the minimum number of conference rooms required so that all meetings can be held simultaneously.", {}),
    ])),
    N.para("Example: intervals = [[0,30],[5,10],[15,20]] → 2 rooms needed (meetings [0,30] and [5,10] overlap; [15,20] reuses the room after [5,10] ends)."),
    N.divider(),
]

# ── Solution 1: Min-Heap ──
blocks += [
    N.h2("Solution 1 — Greedy + Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The minimum number of rooms needed equals the maximum number of meetings simultaneously active at any point in time. We don't need to figure out which meetings share a room — just find the peak concurrent overlap."),
        N.h4("What Doesn't Work"),
        N.para("Comparing every pair of meetings for overlap is O(n²) — too slow. Scanning every time point is O(T) where T is the time range, which could be enormous. Neither approach scales."),
        N.h4("The Key Observation"),
        N.para("When a new meeting starts, we want to reuse a room if possible — specifically the room whose meeting ends earliest. If even the earliest-ending room isn't free yet, then no room is free. This is a minimum query — exactly what a min-heap provides in O(log n)."),
        N.h4("Building the Solution"),
        N.para("Sort meetings by start time (greedy ordering). Use a min-heap of end times. For each meeting: if heap root ≤ start (earliest room is free), pop+push (reuse). Otherwise push only (new room). Final heap size = rooms used = answer."),
        N.callout("Analogy: think of the heap as a row of hotel room keys, each tagged with checkout time. When a guest arrives, you grab the key with the earliest checkout and check — if they've left, hand it out. Otherwise, get a new key.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "import heapq\n\n"
        "def minMeetingRooms(intervals):\n"
        "    if not intervals:\n"
        "        return 0\n"
        "    intervals.sort(key=lambda x: x[0])    # sort by start time\n"
        "    heap = []                              # min-heap of end times\n"
        "    heapq.heappush(heap, intervals[0][1]) # allocate first room\n"
        "    for start, end in intervals[1:]:\n"
        "        if heap[0] <= start:              # earliest room is free?\n"
        "            heapq.heappop(heap)           #   yes: free it\n"
        "        heapq.heappush(heap, end)         # reuse freed room OR new room\n"
        "    return len(heap)                      # heap size = rooms needed"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort(key=lambda x: x[0])", {"code": True}), (" — Sort by start time. Greedy ordering ensures we process meetings in chronological arrival order.", {})])),
    N.para(N.rich([("heap = []", {"code": True}), (" — Min-heap to track end times of all currently occupied rooms. Smallest element = room freeing up soonest.", {})])),
    N.para(N.rich([("heapq.heappush(heap, intervals[0][1])", {"code": True}), (" — Allocate Room 1 for the first meeting. Always need at least one room.", {})])),
    N.para(N.rich([("if heap[0] <= start:", {"code": True}), (" — Check if the earliest-ending room finishes at or before our meeting starts. If yes, that room is free.", {})])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), (" — Remove the old end time, effectively 'freeing' that room slot.", {})])),
    N.para(N.rich([("heapq.heappush(heap, end)", {"code": True}), (" — Always push the new end time. If we popped, this reuses the room (net size unchanged). If we didn't pop, this adds a new room (size +1).", {})])),
    N.para(N.rich([("return len(heap)", {"code": True}), (" — Each heap entry represents one occupied room. Heap size = minimum rooms needed.", {})])),
    N.divider(),
]

# ── Solution 2: Sweep Line ──
blocks += [
    N.h2("Solution 2 — Sweep Line / Event Sorting"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of thinking about rooms, think about events in time. Each meeting generates two events: a start (+1 room needed) and an end (-1 room freed). If we process all events in chronological order, the running sum at any point tells us how many rooms are currently occupied. The peak of that sum is the answer."),
        N.h4("What Doesn't Work"),
        N.para("Treating start and end events identically (without tie-breaking) can give wrong results when a meeting ends exactly when another starts — we'd count them as simultaneously occupying rooms when actually one can reuse the other."),
        N.h4("The Key Observation"),
        N.para("Sort events by time, with ends (-1) before starts (+1) at the same timestamp. This ensures that when a room becomes free and a new meeting starts at the same time, we properly count the room as available (count goes down before going up)."),
        N.h4("Building the Solution"),
        N.para("Create (time, delta) events. Sort by (time, delta) — since -1 < +1, ends sort before starts at ties. Track running count; return its maximum."),
    ]),
    N.h3("Code"),
    N.code(
        "def minMeetingRooms_sweep(intervals):\n"
        "    events = []\n"
        "    for start, end in intervals:\n"
        "        events.append((start,  1))   # +1: meeting starts, need a room\n"
        "        events.append((end,   -1))   # -1: meeting ends, room freed\n"
        "    events.sort(key=lambda x: (x[0], x[1]))  # ties: ends before starts\n"
        "    rooms = max_rooms = 0\n"
        "    for _, delta in events:\n"
        "        rooms += delta\n"
        "        max_rooms = max(max_rooms, rooms)\n"
        "    return max_rooms"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("events.append((start, 1)) / (end, -1)", {"code": True}), (" — Model each meeting as two events: arrival (+1) and departure (-1).", {})])),
    N.para(N.rich([("events.sort(key=lambda x: (x[0], x[1]))", {"code": True}), (" — Sort chronologically. The tuple comparison means ties go in order (-1 end) before (+1 start) — this is crucial for correct boundary handling.", {})])),
    N.para(N.rich([("rooms += delta", {"code": True}), (" — Running count of concurrent meetings. +1 when a meeting starts, -1 when one ends.", {})])),
    N.para(N.rich([("max_rooms = max(max_rooms, rooms)", {"code": True}), (" — Track the peak concurrent count — that's our answer.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy + Min-Heap (pick)", "O(n log n)", "O(n)"],
        ["Sweep Line Events", "O(n log n)", "O(n)"],
        ["Brute Force (all pairs)", "O(n²)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals (Heap / Sweep Line subgroup)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Greedy + Heap — Event Scheduling Family", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Minimum resources (rooms, CPUs, servers) to handle all tasks'\n"
        "• 'Maximum simultaneous X' questions\n"
        "• Interval problems where you need to efficiently find the earliest-freeing slot\n"
        "• 'Can I reuse X after Y finishes?' → min-heap of end times",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Greedy + Heap / Sweep Line for interval scheduling):"),
    N.bullet(N.rich([("Meeting Rooms I", {"bold": True}), (" (Easy) — Can one person attend all meetings? Sort by start, check consecutive pairs for overlap. (#252)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — CPU scheduling with cooldowns; max-heap of task frequencies determines idle time. (#621)", {})])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), (" (Medium) — Meeting Rooms II with passenger capacity constraints; sweep line on pickup/dropoff points. (#1094)", {})])),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), (" (Medium) — Sort by start, greedily merge overlapping intervals. Same sort step as this problem. (#56)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Greedy on end times: keep earliest-ending non-overlapping interval. (#435)", {})])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}), (" (Hard) — Find gaps in the union of all employee schedules; merge intervals across lists. (#759)", {})])),
    N.bullet(N.rich([("Minimum Interval to Include Each Query", {"bold": True}), (" (Hard) — Offline queries + min-heap; similar event-driven sweep structure. (#1851)", {})])),
    N.para("These problems share the core technique: sort intervals by start time, then use a heap or event sweep to efficiently track active intervals."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap Patterns → Greedy + Heap (Event Scheduling)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("meeting_rooms_ii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
