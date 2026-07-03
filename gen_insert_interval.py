"""
gen_insert_interval.py — Notion update for LC #57 Insert Interval
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8185-b569-ced68ce3d108"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=57,
    pattern="Intervals",
    subpatterns=["Merge with New"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Sweep left-to-right: copy intervals before the new one, expand new to absorb all overlapping ones, then copy intervals after.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of non-overlapping intervals ", {}),
        ("intervals", {"code": True}),
        (" where ", {}),
        ("intervals[i] = [start_i, end_i]", {"code": True}),
        (" represent the start and end of the i-th interval, sorted in ascending order by ", {}),
        ("start_i", {"code": True}),
        (". You are also given an interval ", {}),
        ("newInterval = [start, end]", {"code": True}),
        (" that represents the start and end of another interval. Insert ", {}),
        ("newInterval", {"code": True}),
        (" into ", {}),
        ("intervals", {"code": True}),
        (" so that ", {}),
        ("intervals", {"code": True}),
        (" is still sorted in ascending order by ", {}),
        ("start_i", {"code": True}),
        (" and ", {}),
        ("intervals", {"code": True}),
        (" still does not have any overlapping intervals (merge overlapping intervals if necessary). Return ", {}),
        ("intervals", {"code": True}),
        (" after the insertion.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 (Interview Pick) ──
intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("You have a sorted, non-overlapping calendar. Add one new event. If it conflicts with existing events, merge the conflicts. Output the clean calendar."),
    N.h4("What Doesn't Work"),
    N.para("Brute force: append newInterval, re-sort everything, then do a merge pass. This costs O(n log n) and is unnecessary — the input is already sorted, so sorting again wastes that structure."),
    N.h4("The Key Observation"),
    N.para("Every existing interval falls into exactly one of three zones relative to newInterval: (1) completely before it (end < new.start), (2) overlapping it (start <= new.end AND end >= new.start), or (3) completely after it (start > new.end). Since the input is sorted, these zones are contiguous — we process them in order with three sequential while-loops."),
    N.h4("Building the Solution"),
    N.para("Phase 1: Copy intervals whose end < newInterval.start directly to result. Phase 2: While intervals[i].start <= newInterval.end, absorb the interval by expanding newInterval (take min of starts, max of ends). Phase 3: Copy remaining intervals. The merged newInterval is appended once after Phase 2."),
    N.callout("Analogy: Think of inserting a new meeting into a calendar. Scan left to right. Before the new meeting: leave as-is. Overlapping the new meeting: cancel them and extend your new meeting. After your meeting: leave as-is. You touch each event exactly once.", "🧠", "blue_background"),
]

sol1_code = '''\
def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: copy intervals completely before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: merge all overlapping intervals into newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)  # insert the fully-merged interval

    # Phase 3: copy intervals completely after newInterval
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
'''

blocks += [
    N.h2("Solution 1 — Three-Phase Linear Sweep (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_children),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — Output list. Grows in three sequential phases as we sweep through intervals."])),
    N.para(N.rich([("i = 0", {"code": True}), " — Index pointer sweeping left to right through intervals. We never go backward."])),
    N.para(N.rich([("while i < n and intervals[i][1] < newInterval[0]", {"code": True}), " — Phase 1 condition: current interval ends strictly before new interval starts. Zero overlap possible."])),
    N.para(N.rich([("result.append(intervals[i]); i += 1", {"code": True}), " — Copy the 'before' interval unchanged to output. Advance i."])),
    N.para(N.rich([("while i < n and intervals[i][0] <= newInterval[1]", {"code": True}), " — Phase 2 condition: current interval starts at or before new interval ends → they overlap. (Phase 1 already guarantees this interval's end >= new interval's start.)"])),
    N.para(N.rich([("newInterval[0] = min(newInterval[0], intervals[i][0])", {"code": True}), " — Expand the merged interval leftward: take the earlier of the two starts."])),
    N.para(N.rich([("newInterval[1] = max(newInterval[1], intervals[i][1])", {"code": True}), " — Expand the merged interval rightward: take the later of the two ends."])),
    N.para(N.rich([("result.append(newInterval)", {"code": True}), " — After all overlapping intervals are absorbed, insert the fully merged newInterval. This happens exactly once."])),
    N.para(N.rich([("while i < n:", {"code": True}), " — Phase 3: all remaining intervals start after newInterval ends. They cannot overlap each other or the merged result."])),
    N.para(N.rich([("result.append(intervals[i]); i += 1", {"code": True}), " — Copy 'after' intervals unchanged. Advance i until done."])),
    N.divider(),
]

# ── Solution 2 (Brute Force) ──
intuition2_children = [
    N.h4("Reframe the Problem"),
    N.para("Insert the new interval anywhere and then sort — treating this as a generic merge intervals problem."),
    N.h4("What Doesn't Work About This Approach"),
    N.para("It's correct but O(n log n) due to sorting. We throw away the sorted precondition, making it strictly worse than the linear approach."),
    N.h4("The Key Observation"),
    N.para("If we append newInterval to intervals and sort, we can then run the standard merge-intervals sweep: one pass, merging whenever the current interval overlaps the last result interval."),
    N.h4("Building the Solution"),
    N.para("Append newInterval, sort by start. Initialize result with the first interval. For each subsequent interval: if it overlaps result[-1], merge by taking max of ends. Otherwise, append as a new interval."),
]

sol2_code = '''\
def insert_brute(intervals, newInterval):
    # Append newInterval and sort — O(n log n)
    all_intervals = intervals + [newInterval]
    all_intervals.sort(key=lambda x: x[0])

    result = [all_intervals[0]]
    for start, end in all_intervals[1:]:
        if start <= result[-1][1]:
            # Overlaps last result interval — merge
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
'''

blocks += [
    N.h2("Solution 2 — Brute Force: Append, Sort, Merge"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition2_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("all_intervals = intervals + [newInterval]", {"code": True}), " — Create a new list containing all intervals plus the new one. We make a copy to avoid mutating the input."])),
    N.para(N.rich([("all_intervals.sort(key=lambda x: x[0])", {"code": True}), " — Sort by start time. This is the O(n log n) step that we avoid in Solution 1."])),
    N.para(N.rich([("result = [all_intervals[0]]", {"code": True}), " — Initialize result with the first (earliest) interval."])),
    N.para(N.rich([("if start <= result[-1][1]:", {"code": True}), " — Current interval's start is at or before last result interval's end → overlap. Merge by extending the end."])),
    N.para(N.rich([("result[-1][1] = max(result[-1][1], end)", {"code": True}), " — Extend the last result interval's end to cover the current interval."])),
    N.para(N.rich([("else: result.append([start, end])", {"code": True}), " — No overlap — this is a new non-overlapping interval. Add it to result."])),
    N.callout("Use Solution 1 (three-phase sweep) in interviews — it runs in O(n) and demonstrates that you recognize and exploit the sorted structure. Solution 2 is acceptable if you forget the sorted precondition, but mention it immediately and upgrade.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (append + sort + merge)", "O(n log n)", "O(n)"],
        ["Three-Phase Linear Sweep (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals — problems where input consists of sorted or unsortable ranges that must be combined, compared, or queried."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Merge with New — inserting one new interval into an existing sorted, non-overlapping interval list, merging all overlaps by expanding the new interval."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Input is described as 'sorted intervals' or 'non-overlapping intervals'\n"
        "• You are given a new interval to 'insert'\n"
        "• Problem asks to 'merge overlapping' after insertion\n"
        "• Calendar / meeting scheduling / range booking context\n"
        "• You need to find the union of a set of ranges after adding one more",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core interval technique:"),
    N.bullet(N.rich([("56. Merge Intervals", {"bold": True}), " (Medium) — Generalization: sort all intervals, then merge any that overlap. Same min/max expansion logic but applied to every adjacent pair."])),
    N.bullet(N.rich([("252. Meeting Rooms", {"bold": True}), " (Easy) — Check if any two intervals overlap; uses the same two-interval overlap condition: start_i <= end_j AND end_i >= start_j."])),
    N.bullet(N.rich([("253. Meeting Rooms II", {"bold": True}), " (Medium) — Minimum rooms for all meetings; sort events + min-heap or two-pointer, same interval intuition."])),
    N.bullet(N.rich([("986. Interval List Intersections", {"bold": True}), " (Medium) — Two-pointer merge across two sorted interval lists; same zone logic applied simultaneously to two arrays."])),
    N.bullet(N.rich([("759. Employee Free Time", {"bold": True}), " (Hard) — Find gaps in merged intervals across multiple employee schedules; extension of merge intervals across multiple lists."])),
    N.bullet(N.rich([("715. Range Module", {"bold": True}), " (Hard) — Dynamic insertions into an ordered interval set; the core insertion/merge logic from this problem, applied repeatedly."])),
    N.para("These problems all share the core observation: intervals on a sorted timeline can be processed in a single left-to-right sweep, with overlaps resolved by min/max expansion."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section (Merge with New sub-pattern).", "📚", "gray_background"),
]

# ── Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("insert_interval")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
