"""
gen_meeting_rooms_iii.py
Notion in-place update for Meeting Rooms III (LeetCode 2402).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cd-b754-cc544e6c52ce"

# ── 1. Properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2402,
    pattern="Intervals",
    subpatterns=["Two Heaps"],
    tc="O(m log n)",
    sc="O(n)",
    key_insight="Two min-heaps: free (by room#) and busy (by end_time, room#) give O(log n) for both scheduling queries.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} old blocks.")

# ── 3. Build body blocks ───────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have ", {}),
        ("n", {"code": True}),
        (" rooms numbered ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n-1", {"code": True}),
        (" and a list of meetings ", {}),
        ("meetings[i] = [start_i, end_i]", {"code": True}),
        (" (sorted by start time). Schedule each meeting in the "
         "lowest-numbered available room. If all rooms are busy, delay it to start "
         "when the earliest-finishing room becomes free, preserving the meeting's "
         "original duration. Return the room number that hosted the most meetings "
         "(lowest number breaks ties).", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Two Heaps ──
SOL1_CODE = """\
import heapq

def mostBooked(n: int, meetings: list[list[int]]) -> int:
    meetings.sort()                      # process chronologically
    free = list(range(n))                # min-heap by room number
    heapq.heapify(free)
    busy = []                            # min-heap of (end_time, room_number)
    count = [0] * n

    for start, end in meetings:
        # Release all rooms that finished by this meeting's start time
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)

        if free:
            # Case A: assign to lowest-numbered free room
            room = heapq.heappop(free)
            count[room] += 1
            heapq.heappush(busy, (end, room))
        else:
            # Case B: delay — wait for earliest-finishing room
            end_time, room = heapq.heappop(busy)
            count[room] += 1
            new_end = end_time + (end - start)   # preserve duration!
            heapq.heappush(busy, (new_end, room))

    return count.index(max(count))       # first max = lowest room# on ties
"""

blocks += [
    N.h2("Solution 1 — Two Heaps (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each step you need two different 'minimum' answers: the minimum room number (when rooms are free) and the minimum end time (when all rooms are busy). Two different orderings → two data structures, each optimized for one query."),
        N.h4("What Doesn't Work"),
        N.para("A single sorted structure can only maintain one ordering. A linear scan (brute force) gives correct answers in O(n) per meeting — but with n, m up to 10^5 that's 10^10 operations, far too slow."),
        N.h4("The Key Observation"),
        N.para("Rooms move between two pools: 'free' and 'busy'. When free, you want the minimum room number. When all busy, you want the minimum end time. Two min-heaps — one per pool — give O(log n) for both queries."),
        N.h4("Building the Solution"),
        N.para("Free heap stores room numbers (keyed by room number). Busy heap stores (end_time, room_number) tuples — Python's tuple comparison gives free tie-breaking by room number at zero extra cost. Before each meeting: drain busy heap of expired rooms (end_time ≤ start) → push to free heap. Then assign per the rules."),
        N.callout(
            "Analogy: Imagine two queues at an airport desk. One queue is for passengers without tickets (free rooms, sorted by seat number). The other is for passengers waiting for their current flight to land (busy rooms, sorted by landing time). You always call from the first queue first; if empty, you pull the soonest-landing passenger from the second.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("meetings.sort()", {"code": True}), (" — sort all meetings by start time so we process them chronologically. O(m log m).", {})])),
    N.para(N.rich([("free = list(range(n)); heapq.heapify(free)", {"code": True}), (" — all n rooms start available. heapify is O(n).", {})])),
    N.para(N.rich([("busy = []", {"code": True}), (" — min-heap of (end_time, room_number) tuples. Starts empty.", {})])),
    N.para(N.rich([("while busy and busy[0][0] <= start:", {"code": True}), (" — rooms with end_time ≤ start have become free. Pop them and push their room numbers to the free heap.", {})])),
    N.para(N.rich([("if free:", {"code": True}), (" — at least one room is available. Pop the minimum (lowest-numbered) room, assign the meeting, push (end, room) to busy.", {})])),
    N.para(N.rich([("else:", {"code": True}), (" — all rooms occupied. Pop (end_time, room) from busy heap — the earliest-finishing room wins (ties broken by room number via tuple ordering).", {})])),
    N.para(N.rich([("new_end = end_time + (end - start)", {"code": True}), (" — CRITICAL: preserve meeting duration. The meeting starts at end_time (when the room frees), not at the original start.", {})])),
    N.para(N.rich([("return count.index(max(count))", {"code": True}), (" — index of first maximum = lowest-numbered room that tied for most meetings.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
SOL2_CODE = """\
def mostBooked_brute(n: int, meetings: list[list[int]]) -> int:
    meetings.sort()
    end_times = [0] * n          # end_times[i] = when room i next frees up
    count = [0] * n

    for start, end in meetings:
        chosen = -1
        # Scan all rooms for a free one (lowest index first)
        for i in range(n):
            if end_times[i] <= start:
                chosen = i
                break

        if chosen == -1:
            # All busy: pick earliest-finishing (lowest index on tie)
            chosen = min(range(n), key=lambda i: (end_times[i], i))
            end_times[chosen] += end - start   # delay: preserve duration
        else:
            end_times[chosen] = end

        count[chosen] += 1

    return count.index(max(count))
"""

blocks += [
    N.h2("Solution 2 — Brute Force Linear Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest correct approach: maintain an array of when each room becomes free. For each meeting, scan all rooms linearly."),
        N.h4("What Doesn't Work at Scale"),
        N.para("O(m*n) time — with m=n=100,000 this is 10^10 operations. Gets TLE on LeetCode. But it is perfectly correct and a great starting point to explain to an interviewer before optimizing."),
        N.h4("The Key Observation"),
        N.para("This directly implements the problem statement. The only insight is to use min() with a key=(end_time, index) for the delay case to handle tie-breaking correctly."),
        N.h4("Building the Solution"),
        N.para("end_times[i] tracks when room i next becomes free. Scan 0..n-1 for end_times[i] <= start (free room). If none, use min() to find earliest finish. Update end_times and count appropriately."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("end_times = [0] * n", {"code": True}), (" — when each room becomes free; initially all free at time 0.", {})])),
    N.para(N.rich([("for i in range(n): if end_times[i] <= start:", {"code": True}), (" — O(n) scan for first free room (lowest index wins naturally).", {})])),
    N.para(N.rich([("chosen = min(range(n), key=lambda i: (end_times[i], i))", {"code": True}), (" — find earliest-finishing room; tuple key breaks ties by room number.", {})])),
    N.para(N.rich([("end_times[chosen] += end - start", {"code": True}), (" — delay case: add duration (not set to end). Room becomes free later.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (linear scan)", "O(m · n)", "O(n)"],
        ["Two Heaps (optimal)", "O(m log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals — problems involving time ranges and scheduling.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Heaps — maintain two min-heaps to answer two different 'minimum' queries in O(log n) each.", {})])),
    N.callout(
        "When to recognize this pattern: (1) You need the minimum of two different orderings simultaneously. "
        "(2) Elements 'migrate' between two pools based on time/threshold events. "
        "(3) Scheduling problems with resource assignment + delay rules. "
        "(4) Keywords: 'lowest-numbered available', 'earliest-finishing', 'assign to best available'.",
        "🔎", "green_background"),
    N.para(N.rich([
        ("Source: ", {"bold": True}),
        ("DSA_Patterns_and_SubPatterns_Guide.md Section 14 (Intervals) — Sub-Pattern 'Two Heaps'. "
         "Also cross-listed under Section 13.2 (Heap: Two Heaps Pattern).", {}),
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Two Heaps / Heap-based Scheduling):"),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Count minimum rooms needed; one heap of end times, peak heap size = answer.", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Classic two heaps: max-heap for lower half, min-heap for upper half.", {})])),
    N.bullet(N.rich([("Process Tasks Using Servers", {"bold": True}), (" (Medium) — Identical two-heap setup: free servers (by weight, index) + busy servers (by end, weight, index).", {})])),
    N.bullet(N.rich([("IPO", {"bold": True}), (" (Hard) — Min heap by capital required unlocks projects; max heap by profit picks best available.", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Max heap of task frequencies; greedy cooldown scheduling.", {})])),
    N.bullet(N.rich([("Sliding Window Median", {"bold": True}), (" (Hard) — Two heaps with lazy deletion as the window slides forward.", {})])),
    N.bullet(N.rich([("Single-Threaded CPU", {"bold": True}), (" (Medium) — Sort tasks, use min-heap for available tasks by processing time.", {})])),
    N.para("These problems all share the core technique: use heap(s) to maintain efficient 'next best' access as the eligible set changes over time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 14 (Intervals) Table: Meeting Rooms III | Hard | Two Heaps. Also Section 13.2 (Two Heaps Pattern).", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("meeting_rooms_iii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
