"""
gen_remove_covered_intervals.py
Notion in-place update for LeetCode #1288 Remove Covered Intervals.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b1-9cd0-fdb2cbf7cb9a"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1288,
    pattern="Intervals",
    subpatterns=["Sort + Track Max End"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort by start asc then end desc; an interval is covered iff its end <= max end seen among survivors.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of intervals ", {}),
        ("intervals", {"code": True}),
        (", where ", {}),
        ("intervals[i] = [li, ri]", {"code": True}),
        (", remove all intervals that are covered by another interval in the list. ", {}),
        ("An interval ", {}),
        ("[a, b]", {"code": True}),
        (" is covered by interval ", {}),
        ("[c, d]", {"code": True}),
        (" if ", {}),
        ("c <= a", {"code": True}),
        (" and ", {}),
        ("b <= d", {"code": True}),
        (". Return the number of remaining intervals.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Sort + Track Max End (Interview Pick) ──
sol1_code = """\
def removeCoveredIntervals(intervals):
    # Sort by start ascending; break ties by end descending
    # so that when starts are equal, the longer interval comes first.
    intervals.sort(key=lambda x: (x[0], -x[1]))

    count = 0
    max_end = 0   # largest right endpoint among survivors so far

    for start, end in intervals:
        if end > max_end:
            # This interval extends beyond max_end.
            # After sorting, start is >= all previous starts,
            # so if end also exceeds max_end, it cannot be covered.
            count += 1
            max_end = end
        # else: end <= max_end → covered by some earlier survivor; skip.

    return count
"""

blocks += [
    N.h2("Solution 1 — Sort + Track Max End (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count intervals that are NOT fully contained inside any other interval. "
               "An interval [a,b] is covered by [c,d] if c <= a AND b <= d — both its start is no earlier "
               "and its end is no later than the other interval. We want to discard every such covered interval "
               "and count the rest."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach checks every pair: for each interval i, scan all other intervals j "
               "to see if j covers i. This is O(n^2) — too slow for large inputs. We need to eliminate "
               "one of the two dimensions (start and end) so we only check one condition instead of two."),
        N.h4("The Key Observation"),
        N.para("If we SORT intervals by start ascending, then when processing interval [a, b], every "
               "previously seen interval [c, d] is guaranteed to have c <= a. The start condition for "
               "coverage is automatically satisfied by the sort order! Coverage then reduces to one check: "
               "is b <= max_end? where max_end is the largest end seen among all non-covered intervals so far."),
        N.h4("Building the Solution"),
        N.para("Sort by start ascending, with end DESCENDING as a tiebreaker (crucial for same-start intervals). "
               "Then scan left to right: if end > max_end, the interval is a survivor — increment count and "
               "update max_end. Otherwise it is covered — skip it. The tiebreaker ensures that when two "
               "intervals share a start, the longer (covering) one is processed first, preventing false positives."),
        N.callout(
            "Analogy: Imagine measuring land plots along a river. Sort by how far upstream each plot starts. "
            "Any new plot that does not extend further downstream than the longest plot seen so far is entirely "
            "inside it — it adds no new land. Only count plots that push the downstream boundary further.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("intervals.sort(key=lambda x: (x[0], -x[1]))", {"code": True}),
        (" — Sort by start ascending; negating end reverses its order so larger ends come first "
         "when starts are equal. This tiebreaker prevents counting a shorter same-start interval "
         "as a survivor before its larger covering parent.", {}),
    ])),
    N.para(N.rich([
        ("count = 0; max_end = 0", {"code": True}),
        (" — Initialize survivor count to 0 and the furthest right boundary seen to 0.", {}),
    ])),
    N.para(N.rich([
        ("for start, end in intervals:", {"code": True}),
        (" — Single linear pass through sorted intervals.", {}),
    ])),
    N.para(N.rich([
        ("if end > max_end:", {"code": True}),
        (" — After sorting, start >= all previous starts (sort guarantee). So coverage is "
         "entirely determined by whether end fits within max_end. If end exceeds max_end, "
         "the interval cannot be covered by anything seen so far.", {}),
    ])),
    N.para(N.rich([
        ("count += 1", {"code": True}),
        (" — This interval is a survivor — it contributes unique coverage on the number line.", {}),
    ])),
    N.para(N.rich([
        ("max_end = end", {"code": True}),
        (" — Advance the right boundary frontier to this interval's end.", {}),
    ])),
    N.para(N.rich([
        ("# else: covered, skip", {"code": True}),
        (" — end <= max_end means this interval's right bound fits within a survivor's range "
         "and its left bound is guaranteed valid by sort. It is covered; no action needed.", {}),
    ])),
    N.para(N.rich([
        ("return count", {"code": True}),
        (" — The number of non-covered intervals.", {}),
    ])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = """\
def removeCoveredIntervals_brute(intervals):
    n = len(intervals)
    covered = [False] * n
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = intervals[i]
            c, d = intervals[j]
            if c <= a and b <= d:
                covered[i] = True
                break
    return sum(1 for c in covered if not c)
"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The direct translation of the problem statement: for each interval, check every other "
               "interval to see if it is covered. No tricks required — just nested loops."),
        N.h4("What Doesn't Work"),
        N.para("This works correctly, but O(n^2) time is unacceptable for n up to 100,000. "
               "Use this as the baseline to verify your optimized solution."),
        N.h4("The Key Observation"),
        N.para("The coverage condition c <= a AND b <= d is checked for every pair (i, j). "
               "We mark interval i as covered if any j covers it. The final count is the number of unmarked intervals."),
        N.h4("Building the Solution"),
        N.para("Two nested loops. For each i, scan all j != i. If intervals[j] covers intervals[i], "
               "mark i and break. Count unmarked intervals at the end."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sort + Track Max End (Optimal)", "O(n log n)", "O(1)"],
        ["Brute Force", "O(n^2)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Track Max End", {})])),
    N.callout(
        "When to recognize this pattern: 'count/keep intervals that are not subsets of any other', "
        "'remove redundant intervals', any 1D containment problem where sorting fixes one dimension "
        "and a running maximum handles the other.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: The sub-pattern 'Sort + Track Max End' is classified based on analysis; "
         "it is a specialized technique within the broader Intervals / Greedy category.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely adjacent interval sorting + greedy technique:"),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}),
                     (" (Medium) — Sort by start, merge overlapping intervals with a running last pointer. LeetCode #56.", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}),
                     (" (Medium) — Insert new interval into sorted non-overlapping list and merge conflicts. LeetCode #57.", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}),
                     (" (Medium) — Min intervals to remove so no two overlap; greedy by earliest end. LeetCode #435.", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}),
                     (" (Medium) — Min rooms = max simultaneous overlaps; sweep line or heap. LeetCode #253.", {})])),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}),
                     (" (Medium) — Find intersections of two sorted interval lists using two pointers. LeetCode #986.", {})])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}),
                     (" (Hard) — Merge all employee schedule intervals, find gaps. LeetCode #759.", {})])),
    N.para("These problems share the core technique: sort intervals, then make greedy decisions by "
           "tracking a boundary (max_end, last merged end, etc.) across a single linear scan."),
    N.callout("📚 Reference: Intervals / Greedy section of DSA_Patterns_and_SubPatterns_Guide.md. "
              "Sub-pattern classification: Analysis (Sort + Track Max End).", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_covered_intervals")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
