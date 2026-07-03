"""
gen_two_best_non_overlapping_events.py
Regenerate Notion page for LeetCode #2054 Two Best Non-Overlapping Events
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8187-8005-dd812dd591f5"
SLUG = "two_best_non_overlapping_events"

print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2054,
    pattern="Intervals",
    subpatterns=["Sort + Binary Search"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by start; binary search end-sorted prefix-max for best non-overlapping partner.",
    icon="🟡"
)
print("Properties set.")

print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── Build blocks ───
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a 0-indexed 2D integer array ", {}),
        ("events", {"code": True}),
        (" where ", {}),
        ("events[i] = [startTime_i, endTime_i, value_i]", {"code": True}),
        (". The ", {}),
        ("i", {"code": True}),
        ("-th event starts at ", {}),
        ("startTime_i", {"code": True}),
        (" and ends at ", {}),
        ("endTime_i", {"code": True}),
        (", and if you attend this event, you will receive a value of ", {}),
        ("value_i", {"code": True}),
        (". You can choose at most TWO non-overlapping events to attend such that the sum of their values is maximized. "
         "Return this maximum sum. Note that the start time and end time are inclusive: "
         "if you attend event i starting on day s, you cannot attend event j starting on day s (they overlap). "
         "Non-overlapping means endTime_i < startTime_j.", {}),
    ])),
    N.divider(),
]

# Solution 1: Sort + Binary Search (Interview Pick)
sol1_code = """\
from bisect import bisect_left

def maxTwoEvents(events):
    events.sort(key=lambda e: e[0])          # Sort by start time
    end_sorted = sorted(events, key=lambda e: e[1])  # Sort by end time
    ends = [e[1] for e in end_sorted]        # End-time array for binary search
    prefix_max = [0] * len(end_sorted)
    prefix_max[0] = end_sorted[0][2]         # Base case
    for i in range(1, len(end_sorted)):
        prefix_max[i] = max(prefix_max[i-1], end_sorted[i][2])
    ans = 0
    for start, end, val in events:
        ans = max(ans, val)                  # Solo attendance
        idx = bisect_left(ends, start) - 1  # Last event ending strictly before start
        if idx >= 0:
            ans = max(ans, val + prefix_max[idx])  # Paired value
    return ans\
"""

blocks += [
    N.h2("Solution 1 — Sort + Prefix-Max + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pick at most 2 non-overlapping events from a list to maximize total value. "
               "The brute force tries all O(n²) pairs. The key question: can we find the best compatible partner "
               "for each event efficiently?"),
        N.h4("What Doesn't Work"),
        N.para("O(n²) brute force: for each event, scan all other events for non-overlap — too slow for n=10⁵. "
               "Sorting by start alone doesn't help directly because we still need to know the best already-ended event."),
        N.h4("The Key Observation"),
        N.para("Fix one event as the 'current' (second) event. The best first event is the one with the highest value "
               "that ends STRICTLY before the current event starts. If we sort events by end time and precompute "
               "prefix maxima of values, we can answer 'best event ending before time T' in O(log n) via binary search."),
        N.h4("Building the Solution"),
        N.para("1. Sort events by start to iterate as 'current event'. "
               "2. Build a separate list sorted by end time. Extract ends[]. "
               "3. Build prefix_max[i] = max value in end_sorted[0..i]. "
               "4. For each current event: binary search ends[] for last index where end < start. "
               "5. paired_val = current_val + prefix_max[idx]. Update global ans."),
        N.callout(
            "Analogy: You're booking the 2nd meeting of your day. To find the most valuable meeting "
            "that already finished, you have a pre-sorted 'finished meetings board' with a running best pinned. "
            "One glance (binary search) gives the answer.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("events.sort(key=lambda e: e[0])", {"code": True}),
                   (" — Sort events by START time. We iterate these as 'current event' (potentially the second in a pair).", {})])),
    N.para(N.rich([("end_sorted = sorted(events, key=lambda e: e[1])", {"code": True}),
                   (" — Separate sort by END time. This is the structure we binary-search to find compatible partners.", {})])),
    N.para(N.rich([("ends = [e[1] for e in end_sorted]", {"code": True}),
                   (" — Extract just end times into a sorted array; needed as the target array for bisect_left.", {})])),
    N.para(N.rich([("prefix_max[i] = max(prefix_max[i-1], end_sorted[i][2])", {"code": True}),
                   (" — Running maximum of values. prefix_max[i] = best value among all events with end time ≤ ends[i].", {})])),
    N.para(N.rich([("ans = max(ans, val)", {"code": True}),
                   (" — Always consider attending this event alone (in case no compatible partner exists).", {})])),
    N.para(N.rich([("idx = bisect_left(ends, start) - 1", {"code": True}),
                   (" — bisect_left gives first position where ends[i] ≥ start. Subtracting 1 gives last position where ends[i] < start — strictly before our event begins.", {})])),
    N.para(N.rich([("if idx >= 0: ans = max(ans, val + prefix_max[idx])", {"code": True}),
                   (" — If a compatible partner exists, the best it can offer is prefix_max[idx] (running max up to that index). Add to current event's value.", {})])),
    N.divider(),
]

# Solution 2: Heap Sweep
sol2_code = """\
import heapq

def maxTwoEvents(events):
    events.sort()                                 # Sort by start time
    heap = []                                     # Min-heap of (end_time, value)
    best_ended = 0                                # Best value among finished events
    ans = 0
    for start, end, val in events:
        # Pop events that ended strictly before this event starts
        while heap and heap[0][0] < start:
            best_ended = max(best_ended, heapq.heappop(heap)[1])
        # Either attend alone or pair with best ended event
        ans = max(ans, val, val + best_ended)
        heapq.heappush(heap, (end, val))
    return ans\
"""

blocks += [
    N.h2("Solution 2 — Min-Heap Sweep Line"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Process events in start-time order. Maintain a heap of 'in-flight' events (started but not yet confirmed ended). When a new event starts, pop all heap items that ended before it — those are compatible partners."),
        N.h4("What Doesn't Work"),
        N.para("Without a heap, we'd have to scan all previous events to find ended ones — O(n²). The heap gives O(log n) ordering by end time."),
        N.h4("The Key Observation"),
        N.para("Sort by start time. Use a min-heap keyed on end time. For each new event, drain the heap of all events that ended before this one starts — these are all compatible 'first' events. Track the best value seen among drained events."),
        N.h4("Building the Solution"),
        N.para("1. Sort by start. 2. For each event, pop heap items with end < current start — update best_ended. "
               "3. ans = max(ans, val, val + best_ended). 4. Push current event onto heap. "
               "This is a natural 'sweep line' approach."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("events.sort()", {"code": True}),
                   (" — Sort by start time (tuple comparison: start first, then end, then val).", {})])),
    N.para(N.rich([("heap = []", {"code": True}),
                   (" — Min-heap of (end_time, value). Ordered by end_time so we can easily pop events that have ended.", {})])),
    N.para(N.rich([("while heap and heap[0][0] < start:", {"code": True}),
                   (" — While the event with earliest end time ended strictly before current event starts...", {})])),
    N.para(N.rich([("best_ended = max(best_ended, heapq.heappop(heap)[1])", {"code": True}),
                   (" — Pop it, update running max of ended event values.", {})])),
    N.para(N.rich([("ans = max(ans, val, val + best_ended)", {"code": True}),
                   (" — Three candidates: previous best, this event alone, this event + best ended partner.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (end, val))", {"code": True}),
                   (" — Add current event to heap so future events can pair with it.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Sort + Binary Search (Interview Pick)", "O(n log n)", "O(n)"],
        ["Min-Heap Sweep", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Binary Search", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Pick at most k non-overlapping intervals/events' with maximize/minimize\n"
        "• 'Best compatible partner for each element' where compatibility means non-overlap\n"
        "• Input is intervals with values → sort by start or end, precompute prefix/suffix extremes\n"
        "• 'Maximize sum of two items with a compatibility constraint' → fix one, binary search for the other",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Maximum Earnings From Taxi", {"bold": True}), (" (Medium) — Sort by end, DP[i] + binary search for non-overlapping predecessor (#2008)", {})])),
    N.bullet(N.rich([("Maximize Profit in Job Scheduling", {"bold": True}), (" (Hard) — Classic interval DP + binary search for max-weight non-overlapping jobs (#1235)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Minimum removals to make all intervals non-overlapping; sort by end (#435)", {})])),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), (" (Medium) — Insert intervals without overlap; binary search on sorted bookings (#729)", {})])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Sort by end, greedy non-overlapping scan (#452)", {})])),
    N.bullet(N.rich([("Maximum Number of Events That Can Be Attended", {"bold": True}), (" (Medium) — Greedy with heap; attend one event per day (#1353)", {})])),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}), (" (Medium) — Two-pointer merge of two sorted interval lists (#986)", {})])),
    N.para("These problems share the same core technique: sort intervals, precompute a running extreme (max/min/count), use binary search to answer compatibility queries in O(log n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section · Sub-Pattern: Sort + Binary Search", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
