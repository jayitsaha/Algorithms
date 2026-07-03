"""
gen_merge_intervals.py — Rebuild Notion page for LeetCode #56 Merge Intervals.
Run from the Algorithms/ directory: python3 gen_merge_intervals.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a8-b72b-f5e1238af76c"

# ── 1. Properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=56,
    pattern="Intervals",
    subpatterns=["Sort + Extend"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by start time so overlaps become adjacent; scan left-to-right, extend with max() or start a new group.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────
print("Wiping old blocks...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3. Build body blocks ──────────────────────────────────────

PROBLEM_STMT = (
    "Given an array of intervals where intervals[i] = [start_i, end_i], "
    "merge all overlapping intervals and return an array of the non-overlapping "
    "intervals that cover all the intervals in the input.\n\n"
    "Example 1:\n"
    "  Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]\n"
    "  Output: [[1,6],[8,10],[15,18]]\n"
    "  Explanation: [1,3] and [2,6] overlap (2 ≤ 3), merge to [1,6].\n\n"
    "Example 2:\n"
    "  Input:  intervals = [[1,4],[4,5]]\n"
    "  Output: [[1,5]]\n"
    "  Explanation: [1,4] and [4,5] touch at 4, merge to [1,5].\n\n"
    "Constraints: 1 ≤ intervals.length ≤ 10^4; intervals[i].length == 2; "
    "0 ≤ start_i ≤ end_i ≤ 10^4"
)

SOL1_CODE = """\
def merge(intervals):
    intervals.sort(key=lambda x: x[0])  # Sort by start time
    merged = [intervals[0]]             # Seed with first interval

    for s, e in intervals[1:]:
        if s <= merged[-1][1]:          # Overlap or touch?
            merged[-1][1] = max(merged[-1][1], e)  # Extend (max handles containment)
        else:
            merged.append([s, e])       # Gap: start a new group

    return merged
"""

SOL2_CODE = """\
def merge_verbose(intervals):
    \"\"\"Same logic, more explicit variable names for clarity.\"\"\"
    intervals.sort(key=lambda x: x[0])
    result = [list(intervals[0])]      # Copy first interval

    for start, end in intervals[1:]:
        last_start, last_end = result[-1]

        if start <= last_end:          # Overlapping or touching
            result[-1][1] = max(last_end, end)   # Extend the merge window
        else:                          # Disjoint gap
            result.append([start, end])

    return result
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Sort + Scan (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have intervals scattered on a number line. We need to find the minimum "
            "set of intervals that covers the same total range. Two intervals should "
            "become one whenever they share any point — including touching at an endpoint."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive pair-wise approach checks every interval against every other: O(n²). "
            "Worse, when two intervals merge, the resulting interval might overlap a third — "
            "requiring multiple passes. Without structure, this is hard to control."
        ),
        N.h4("The Key Observation"),
        N.para(
            "If we sort intervals by start time, overlapping intervals become adjacent "
            "in the array. Proof: if B overlaps A (B.start ≤ A.end), and we sorted by "
            "start (B.start ≥ A.start), then B appears immediately after A. No interval "
            "can sit between them in sorted order while also overlapping A but not being "
            "adjacent to it. This means we only ever compare neighbors — O(n) scan."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort by start: O(n log n).\n"
            "2. Seed result with intervals[0].\n"
            "3. For each subsequent interval [s, e]: if s ≤ merged[-1][1] → overlap → "
            "   extend end with max(). Else → gap → append new group.\n"
            "4. The max() is critical: if the new interval is contained within the current "
            "   window (e.g., [2,3] inside [1,10]), plain assignment would shrink the window "
            "   to [1,3]. max(10, 3) = 10 keeps the correct wider end."
        ),
        N.callout(
            "Analogy: Imagine painting a wall. You have strips of tape already applied. "
            "Sort the strips by their left edge. Scan left to right — if the next strip "
            "starts before your current rightmost tape ends, just extend the tape to "
            "whichever end is further right. If there's a gap, start a new strip.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("intervals.sort(key=lambda x: x[0])", {"code": True}),
        " — Sort in-place by the start of each interval. This is the foundational step. "
        "O(n log n). After this, any interval that overlaps its predecessor appears immediately after it."
    ])),
    N.para(N.rich([
        ("merged = [intervals[0]]", {"code": True}),
        " — Seed the result list with the first interval (already the smallest start after sorting). "
        "The loop starts at index 1, always comparing against ", ("merged[-1]", {"code": True}), "."
    ])),
    N.para(N.rich([
        ("for s, e in intervals[1:]:", {"code": True}),
        " — Unpack each remaining interval into its start ", ("s", {"code": True}),
        " and end ", ("e", {"code": True}), ". We iterate in sorted order."
    ])),
    N.para(N.rich([
        ("if s <= merged[-1][1]:", {"code": True}),
        " — The overlap (or touch) check. If the new interval's start is ≤ the current "
        "window's end, they share at least one point and must be merged. Note: ≤ (not <) "
        "handles intervals that touch at a single point like [1,3] and [3,5]."
    ])),
    N.para(N.rich([
        ("merged[-1][1] = max(merged[-1][1], e)", {"code": True}),
        " — Extend the current window's end. We use ", ("max()", {"code": True}),
        " not plain assignment because the new interval might be entirely contained "
        "(e.g., e=3 when merged[-1][1]=10). Plain assignment would shrink the window "
        "catastrophically. max() ensures the window only grows."
    ])),
    N.para(N.rich([
        ("merged.append([s, e])", {"code": True}),
        " — No overlap: start a fresh merge group. The previous window is finalized — "
        "no future interval can overlap it (because future starts are all ≥ current s > last end)."
    ])),
    N.para(N.rich([
        ("return merged", {"code": True}),
        " — The complete list of merged, non-overlapping intervals covering all input ranges."
    ])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Verbose / Readable Version"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same algorithm as Solution 1, but written with explicit variable names "
            "(last_start, last_end) instead of direct indexed access. This version trades "
            "brevity for readability and is helpful for understanding the logic during "
            "a first pass."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "No change from Solution 1. The algorithm is identical; only the style differs."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Unpacking into named variables (last_start, last_end) makes each decision "
            "explicit. In an interview, writing this version first then refactoring to "
            "Solution 1 shows clean thinking progression."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Same four steps as Solution 1. The only addition: we copy intervals[0] with "
            "list() to avoid mutating the original. In practice, Solution 1 is preferred "
            "for interviews — it's shorter and equally readable once you know the pattern."
        ),
        N.callout(
            "Interview tip: Start by writing the verbose version to reason through the logic, "
            "then offer to clean it up to the compact form. This demonstrates both correctness "
            "and refactoring ability.",
            "🎤", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("result = [list(intervals[0])]", {"code": True}),
        " — Creates a mutable copy of the first interval. Using ",
        ("list()", {"code": True}),
        " prevents aliasing: if we mutate result[-1], we don't accidentally mutate the original input."
    ])),
    N.para(N.rich([
        ("last_start, last_end = result[-1]", {"code": True}),
        " — Unpack the current merge window's bounds into named variables for clarity. "
        "Note: this snapshot may be stale after an extend — use ", ("result[-1][1]", {"code": True}),
        " if you need the live value mid-loop."
    ])),
    N.para(N.rich([
        ("result[-1][1] = max(last_end, end)", {"code": True}),
        " — Identical in effect to Solution 1. Extend the window's right boundary. "
        "max() handles containment where end < last_end."
    ])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Sort + Scan (optimal)", "O(n log n)", "O(n)", "Sort dominates; scan is O(n)"],
        ["Verbose Version", "O(n log n)", "O(n)", "Identical; style differs only"],
        ["Pre-sorted input", "O(n)", "O(n)", "Skip sort; same scan"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sort + Extend"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'merge overlapping intervals' or 'collapse ranges'\n"
        "• Input is a list of [start, end] pairs and output is also intervals\n"
        "• Need to find covered / uncovered regions on a number line\n"
        "• Sorting by start time makes intervals adjacent for a greedy scan",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Intervals — Sort + Extend/Greedy):"),
    N.bullet(N.rich([
        ("Insert Interval", {"bold": True}),
        " (Medium) — Insert into a sorted non-overlapping list and merge. Binary search or linear scan. #57"
    ])),
    N.bullet(N.rich([
        ("Non-overlapping Intervals", {"bold": True}),
        " (Medium) — Minimum removals to make all intervals non-overlapping. Sort by end + greedy. #435"
    ])),
    N.bullet(N.rich([
        ("Meeting Rooms II", {"bold": True}),
        " (Medium) — Minimum rooms needed for all meetings. Sort + min-heap on end times. #253"
    ])),
    N.bullet(N.rich([
        ("Employee Free Time", {"bold": True}),
        " (Hard) — Merge all employees' intervals, find the gaps between groups. #759"
    ])),
    N.bullet(N.rich([
        ("Minimum Number of Arrows to Burst Balloons", {"bold": True}),
        " (Medium) — Sort by end, place arrows greedily at overlapping balloon clusters. #452"
    ])),
    N.bullet(N.rich([
        ("Range Addition", {"bold": True}),
        " (Medium) — Difference array for interval-based range updates. #370"
    ])),
    N.bullet(N.rich([
        ("Interval List Intersections", {"bold": True}),
        " (Medium) — Find all intersections of two sorted interval lists. Two-pointer on both lists. #986"
    ])),
    N.para("These problems all share the core insight: sort intervals by start (or end) time to impose structure on otherwise scattered ranges, then make greedy left-to-right decisions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section\nSub-Pattern: Sort + Extend · Source: Guide + Analysis", "📚", "gray_background"),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("merge_intervals")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ──────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
