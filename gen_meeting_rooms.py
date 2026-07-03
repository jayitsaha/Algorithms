"""gen_meeting_rooms.py — Notion update for LeetCode #252 Meeting Rooms."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f7-a896-cfba63f89a7d"

# ─── 1. Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=252,
    pattern="Intervals",
    subpatterns=["Sort + Check Overlap"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort by start time; after sorting only adjacent pairs can conflict — check O(n) pairs.",
    icon="🟢"
)
print("Properties set OK")

# ─── 2. Wipe old body ─────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ─── 3. Build new body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of meeting time intervals where ",{}),
        ("intervals[i] = [start_i, end_i]",{"code":True}),
        (", determine if a person could attend all meetings. Return ",{}),
        ("True",{"code":True}),
        (" if the person can attend all meetings without any time conflict, otherwise return ",{}),
        ("False",{"code":True}),
        (".",{})
    ])),
    N.callout(
        N.rich([("Example 1: intervals = [[0,30],[5,10],[15,20]] → False  |  Example 2: intervals = [[0,6],[9,12],[15,20]] → True",{})]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ─── Solution 1: Sort + Linear Scan ───────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Sort + Linear Scan (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to check: do any two meetings in the list overlap in time? Two intervals [a,b] and [c,d] overlap when c < b (the later-starting one begins before the earlier-starting one ends)."),
        N.h4("What Doesn't Work"),
        N.para("Checking all pairs naively: O(n²) comparisons. For 10,000 meetings that's 100,000,000 comparisons — too slow. There's also no obvious hash-based shortcut since intervals are continuous ranges, not discrete values."),
        N.h4("The Key Observation"),
        N.para("After sorting by start time, any conflict between non-adjacent meetings implies a conflict between adjacent meetings. Proof: if meetings j and k conflict (k > j+1), then since meeting j+1 starts between j and k in sorted order, meetings j and j+1 also conflict. So checking only adjacent pairs is sufficient."),
        N.h4("Building the Solution"),
        N.para("Sort in O(n log n). Then scan O(n) adjacent pairs: if intervals[i][0] < intervals[i-1][1], return False immediately. If no pair conflicts, return True."),
        N.callout("Analogy: Imagine arranging appointments in a calendar by time. Two conflicting appointments always appear next to each other on the calendar — you'd never have to look across the whole day to find a clash.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def canAttendMeetings(intervals: list[list[int]]) -> bool:\n"
        "    intervals.sort(key=lambda x: x[0])      # Sort by start time O(n log n)\n"
        "    for i in range(1, len(intervals)):       # Scan adjacent pairs\n"
        "        if intervals[i][0] < intervals[i-1][1]:  # Overlap condition\n"
        "            return False                     # Fail fast\n"
        "    return True                              # No conflicts found"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort(key=lambda x: x[0])",{"code":True}),(" — Sort all meetings chronologically by their start time. This is the key step that makes O(n) scanning possible. Time: O(n log n).",{})])),
    N.para(N.rich([("for i in range(1, len(intervals)):",{"code":True}),(" — Start the loop at index 1. We compare each meeting against the one immediately before it in the sorted list.",{})])),
    N.para(N.rich([("if intervals[i][0] < intervals[i-1][1]:",{"code":True}),(" — Overlap check: does the current meeting start before the previous meeting ends? This is the only case where a conflict exists.",{})])),
    N.para(N.rich([("return False",{"code":True}),(" — Fail fast. One conflict is enough to make attendance impossible for all meetings.",{})])),
    N.para(N.rich([("return True",{"code":True}),(" — All adjacent pairs were non-conflicting. By our adjacency proof, this means ALL pairs are non-conflicting.",{})])),
    N.divider(),
]

# ─── Solution 2: Brute Force ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (All Pairs)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct interpretation: check every possible pair of meetings to see if any two overlap."),
        N.h4("What Doesn't Work (Why We Improve)"),
        N.para("This is O(n²) — for n=10,000 meetings, 50 million comparisons. Acceptable for small inputs during an interview to demonstrate correctness, but must be followed with the O(n log n) optimization."),
        N.h4("The Key Observation"),
        N.para("Two intervals [a,b] and [c,d] overlap iff NOT (a ends before c starts OR c ends before a starts). Simplified: a < d AND c < b."),
        N.h4("Building the Solution"),
        N.para("Double loop over all pairs. For each pair, apply the overlap test. Return False on first conflict, True if none found."),
    ]),
    N.h3("Code"),
    N.code(
        "def canAttendMeetings_brute(intervals: list[list[int]]) -> bool:\n"
        "    n = len(intervals)\n"
        "    for i in range(n):\n"
        "        for j in range(i + 1, n):\n"
        "            a, b = intervals[i], intervals[j]\n"
        "            # Overlap: NOT (a ends before b starts OR b ends before a starts)\n"
        "            if a[0] < b[1] and b[0] < a[1]:\n"
        "                return False\n"
        "    return True"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n): for j in range(i+1, n):",{"code":True}),(" — Double loop examines all n*(n-1)/2 pairs. O(n²).",{})])),
    N.para(N.rich([("if a[0] < b[1] and b[0] < a[1]:",{"code":True}),(" — Standard overlap condition. a[0] < b[1]: a starts before b ends. b[0] < a[1]: b starts before a ends. Both must be true for overlap.",{})])),
    N.divider(),
]

# ─── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (All Pairs)", "O(n²)", "O(1)", "Correct; too slow for large n"],
        ["Sort + Linear Scan ✓", "O(n log n)", "O(1)", "Optimal; standard interview answer"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold":True}), ("Intervals",{})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold":True}), ("Sort + Check Overlap",{})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold":True}),
                ("Problem involves time intervals + 'conflict/overlap/attend all' language. "
                 "Sorting by start time is always the first move. After sorting, adjacent pairs dominate. "
                 "Key signals: 'meeting rooms', 'can attend all', 'no overlaps'.",{})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sort + Check Overlap / Interval pattern):"),
    N.bullet(N.rich([("Meeting Rooms II",{"bold":True}), (" (Medium) — Minimum rooms needed; sort + min-heap of end times (#253)",{})])),
    N.bullet(N.rich([("Merge Intervals",{"bold":True}), (" (Medium) — Combine overlapping intervals; sort by start, extend end greedily (#56)",{})])),
    N.bullet(N.rich([("Non-overlapping Intervals",{"bold":True}), (" (Medium) — Fewest removals to make all disjoint; sort by end, greedy keep (#435)",{})])),
    N.bullet(N.rich([("Insert Interval",{"bold":True}), (" (Medium) — Insert one interval into sorted non-overlapping list and merge (#57)",{})])),
    N.bullet(N.rich([("Minimum Arrows to Burst Balloons",{"bold":True}), (" (Medium) — Count minimum non-overlapping groups; sort by end (#452)",{})])),
    N.bullet(N.rich([("Employee Free Time",{"bold":True}), (" (Hard) — Find gaps between merged intervals across employees (#759)",{})])),
    N.para("These problems share the core technique: sort intervals by start time, then use O(n) logic on the sorted sequence."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals Pattern · Sub-Pattern: Sort + Check Overlap · Source: Guide + Analysis", "📚", "gray_background"),
]

# ─── Visual Explainer embed ────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("meeting_rooms")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic":True,"color":"gray"})])),
]

# ─── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
