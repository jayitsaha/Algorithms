"""
gen_non_overlapping_intervals.py
DSA Pipeline: Non-overlapping Intervals (#435, Medium)
notion_page_id = None → create fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "non_overlapping_intervals"
NAME = "Non-overlapping Intervals"
NUMBER = 435
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Intervals"
SUBPATTERNS = ["Sort by End Count Removals"]
TC = "O(n log n)"
SC = "O(1)"
KEY_INSIGHT = "Sort by end time; greedily keep earliest-finishing intervals — maximizing kept minimizes removals."

# ── Step 0: Create page (notion_page_id is null) ──────────────────────
print("Creating new Notion page...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"  Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON,
)
print("  Properties set.")

# ── Step 2: Build body blocks ──────────────────────────────────────────
print("Building page body...")
blocks = []

# ── Problem statement ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of ", {}),
        ("intervals", {"code": True}),
        (" where ", {}),
        ("intervals[i] = [start_i, end_i]", {"code": True}),
        (", return the minimum number of intervals you need to remove to make the rest non-overlapping. "
         "Note: Intervals that only touch at a point (e.g., [1,3] and [3,5]) are non-overlapping.", {}),
    ])),
    N.para("Example 1: intervals = [[1,2],[2,3],[3,4],[1,3]] → Output: 1 (remove [1,3])"),
    N.para("Example 2: intervals = [[1,2],[1,2],[1,2]] → Output: 2 (two duplicates removed)"),
    N.para("Example 3: intervals = [[1,2],[2,3]] → Output: 0 (already non-overlapping)"),
    N.divider(),
]

# ── Solution 1: Greedy (Interview Pick) ────────────────────────────────
SOL1_CODE = '''\
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    # Sort by end time — earliest finisher first
    intervals.sort(key=lambda x: x[1])
    count = 0                     # number of intervals to remove
    prev_end = float('-inf')      # end of last kept interval

    for start, end in intervals:
        if start >= prev_end:     # no overlap: keep this interval
            prev_end = end
        else:                     # overlap: remove current (later-ending)
            count += 1
    return count
'''

blocks += [
    N.h2("Solution 1 — Greedy: Sort by End (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Don't think 'minimum intervals to remove.' Instead ask: 'maximum intervals to keep?' "
               "Since removals = n − kept, maximizing kept automatically minimizes removals. "
               "This reframing transforms a confusing deletion problem into a clean selection problem."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all 2^n subsets and check non-overlap — O(2^n), completely infeasible. "
               "Sorting by start: fails because a long interval starting early blocks many future ones "
               "(e.g., [0,10] would be selected first, blocking [1,2],[2,3] — suboptimal). "
               "We need to sort by END, not start."),
        N.h4("The Key Observation"),
        N.para("The interval that ends earliest leaves the most room on the timeline for future intervals. "
               "By always selecting the compatible interval with the smallest end time, we greedily "
               "maximize the number of intervals we can fit — this is the Activity Selection Problem, "
               "one of the canonical greedy algorithms."),
        N.h4("Building the Solution"),
        N.para("1. Sort by end time. 2. Track prev_end = -∞ (end of last kept interval). "
               "3. For each interval: if start >= prev_end → no overlap, keep it, update prev_end. "
               "4. Else → conflict; remove the current interval (it ends later in sorted order); count++. "
               "5. Return count. The correctness follows from the exchange argument: keeping the "
               "earlier-ending interval can never be worse than keeping a later-ending one."),
        N.callout(
            "Analogy: Scheduling a room. If two speakers want the same slot, choose the one who finishes earlier — "
            "leaves more time for the rest of the conference. That's exactly what this algorithm does.",
            "🏛️", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort(key=lambda x: x[1])", {"code": True}),
                   (" — Sort by each interval's END value. This is the greedy insight: earliest-finishing interval first.", {})])),
    N.para(N.rich([("count = 0", {"code": True}),
                   (" — Running count of intervals we must remove.", {})])),
    N.para(N.rich([("prev_end = float('-inf')", {"code": True}),
                   (" — Tracks the end of the last kept interval. Starting at -∞ ensures the first interval is always kept (any start >= -∞).", {})])),
    N.para(N.rich([("if start >= prev_end:", {"code": True}),
                   (" — No overlap condition. Note >= (not >): touching at a single point is NOT overlapping per the problem definition.", {})])),
    N.para(N.rich([("prev_end = end", {"code": True}),
                   (" — Keep this interval; advance our boundary to its end. We do NOT increment count.", {})])),
    N.para(N.rich([("count += 1", {"code": True}),
                   (" — Overlap detected: remove the current interval (which ends later since we sorted by end). "
                    "Do NOT update prev_end — the earlier-ending interval stays as our reference.", {})])),
    N.para(N.rich([("return count", {"code": True}),
                   (" — Minimum intervals removed = number of times we encountered a conflict.", {})])),
    N.divider(),
]

# ── Solution 2: DP (O(n²) baseline) ───────────────────────────────────
SOL2_CODE = '''\
def eraseOverlapIntervals_dp(intervals: list[list[int]]) -> int:
    """O(n^2) DP — LIS-style longest non-overlapping chain."""
    if not intervals:
        return 0
    intervals.sort()                    # sort by start time
    n = len(intervals)
    dp = [1] * n                        # dp[i] = max non-overlapping count ending at i

    for i in range(1, n):
        for j in range(i):
            # intervals j and i are compatible if j ends before i starts
            if intervals[j][1] <= intervals[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)

    # max non-overlapping we can keep; rest must be removed
    return n - max(dp)
'''

blocks += [
    N.h2("Solution 2 — DP: Longest Non-overlapping Chain (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same as before: maximize kept intervals. Model it as the Longest Increasing Subsequence (LIS) problem "
               "applied to intervals: find the longest sequence of intervals where each starts after the previous ends."),
        N.h4("What Doesn't Work"),
        N.para("This DP is correct but runs in O(n²) — for n=10^4 that's 10^8 operations, which is too slow. "
               "We use it only to build intuition before jumping to the greedy."),
        N.h4("The Key Observation"),
        N.para("dp[i] = maximum number of non-overlapping intervals in any compatible chain ending at interval i. "
               "Answer = n - max(dp): the intervals NOT in our longest chain must be removed."),
        N.h4("Building the Solution"),
        N.para("Sort by start. For each i, check all j < i. If j ends before i starts (compatible), "
               "dp[i] = max(dp[i], dp[j] + 1). Base case: dp[i] = 1 (just interval i by itself). "
               "Final answer: n - max(dp)."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort()", {"code": True}),
                   (" — Sort by start time (for DP; different from greedy which sorts by end).", {})])),
    N.para(N.rich([("dp = [1] * n", {"code": True}),
                   (" — Each interval alone is a chain of length 1.", {})])),
    N.para(N.rich([("if intervals[j][1] <= intervals[i][0]:", {"code": True}),
                   (" — Interval j ends at or before interval i starts — they're compatible (non-overlapping).", {})])),
    N.para(N.rich([("dp[i] = max(dp[i], dp[j] + 1)", {"code": True}),
                   (" — Extend the chain: the best chain ending at i is either i alone, or the best chain ending at j, plus i.", {})])),
    N.para(N.rich([("return n - max(dp)", {"code": True}),
                   (" — Minimum removals = total - maximum chain we can keep.", {})])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Greedy (Sort by End)", "O(n log n)", "O(1)", "Interview pick — optimal"],
        ["DP (LIS-style)", "O(n²)", "O(n)", "Correct but too slow for n=10^4"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort by End, Count Removals (Activity Selection Greedy)", {})])),
    N.callout(
        "When to recognize this pattern: problem involves intervals with start/end times; "
        "asked to maximize compatible (non-overlapping) selections OR minimize removals/conflicts; "
        "keywords: 'non-overlapping', 'maximum non-conflicting', 'minimum to remove'; "
        "after reframing: 'pick the most items with no pairwise conflict' → Activity Selection greedy.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}),
                     (" (Medium, LC #452) — Identical greedy: sort by end, increment arrow count only when start > prev_end", {})])),
    N.bullet(N.rich([("Maximum Length of Pair Chain", {"bold": True}),
                     (" (Medium, LC #646) — Activity Selection on pairs (a,b), maximise chain length", {})])),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}),
                     (" (Medium, LC #56) — Sort by start, merge when overlap; complement of this problem", {})])),
    N.bullet(N.rich([("Meeting Rooms I", {"bold": True}),
                     (" (Easy, LC #252) — Can one person attend all meetings? Sort by start, check adjacents", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}),
                     (" (Medium, LC #253) — Minimum rooms needed; sort by start + min-heap on end times", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}),
                     (" (Medium, LC #57) — Merge a new interval into a sorted non-overlapping list", {})])),
    N.bullet(N.rich([("Video Stitching", {"bold": True}),
                     (" (Medium, LC #1024) — Cover range [0,T] with minimum clips; interval scheduling variant", {})])),
    N.para("These problems share the same core technique: sort intervals by end time, then greedily select compatible intervals."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section, Sort by End / Activity Selection", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ──────────────────────────────────────────────────
import json, pathlib, subprocess
html_path = pathlib.Path(__file__).parent / "non_overlapping_intervals_explainer.html"
html_lines = len(html_path.read_text().splitlines())

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": f"Greedy sort-by-end; {html_lines} lines; Notion page created fresh"
}
(status_dir / f"{SLUG}.json").write_text(json.dumps(status, indent=2))
print(f"RESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
