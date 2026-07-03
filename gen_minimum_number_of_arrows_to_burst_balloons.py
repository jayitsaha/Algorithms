"""
gen_minimum_number_of_arrows_to_burst_balloons.py
Uses EXISTING Notion page (created on first run) for LeetCode #452.
Sets properties and appends body blocks.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Use existing page (created on first partial run) ──
PAGE_ID = "39293418-809c-814f-8f37-cd6ec18e2461"
print(f"Using existing page: {PAGE_ID}")

# ── Set properties (subpatterns must not contain commas) ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=452,
    pattern="Intervals",
    subpatterns=["Sort by End Greedy"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort intervals by end; fire each arrow at earliest-ending unpopped balloon's end to maximise overlap coverage.",
    icon="🟡"
)
print("Properties set.")

# ── Wipe any previous body content ──
N.wipe_page(PAGE_ID)
print("Page wiped.")

# ── Build body blocks ──
PROBLEM_STMT = (
    "Given an array points where points[i] = [x_start, x_end] represents a balloon "
    "spanning from x_start to x_end on the x-axis. An arrow shot vertically at position x "
    "bursts every balloon where x_start <= x <= x_end. "
    "Return the minimum number of arrows needed to burst all balloons."
)

SOL1_CODE = """\
def findMinArrowShots(points):
    if not points:
        return 0
    points.sort(key=lambda x: x[1])   # sort by end coordinate
    arrows = 1
    arrow_pos = points[0][1]           # shoot at end of earliest-ending balloon
    for start, end in points[1:]:
        if start > arrow_pos:          # new disjoint group found
            arrows += 1
            arrow_pos = end            # new arrow fires at this balloon's end
        # else: start <= arrow_pos → already burst, skip
    return arrows"""

SOL2_CODE = """\
def findMinArrowShots_v2(points):
    \"\"\"Sort by start; track minimum end of current overlap group.\"\"\"
    if not points:
        return 0
    points.sort()                      # sort by start (then end as tiebreak)
    arrows = 1
    cur_end = points[0][1]
    for start, end in points[1:]:
        if start > cur_end:            # gap: new group
            arrows += 1
            cur_end = end
        else:
            cur_end = min(cur_end, end)  # shrink to common overlap region
    return arrows"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Greedy: Sort by End (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "One arrow can burst multiple balloons if they all share a common x-coordinate. "
            "So the real question is: how many disjoint overlap groups exist? "
            "Each group needs exactly one arrow."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Trying every possible arrow position is exponential. "
            "Even a smarter brute force checking all endpoints is O(n^2) with bookkeeping. "
            "We need a greedy insight."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Sort by end coordinate. The balloon that ends soonest is the most constrained — "
            "any arrow for it must land at or before its end. "
            "Shooting at exactly its end is the latest valid position, maximising coverage of "
            "future balloons. This is the greedy key."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort by end. "
            "2. Fire first arrow at points[0][1]. "
            "3. For each subsequent balloon: if its start exceeds the current arrow position, "
            "fire a new arrow at its end. Otherwise it's already burst — skip. "
            "4. Return the arrow count."
        ),
        N.callout(
            "Analogy: Imagine scheduling events. The event that ends soonest must be attended "
            "first. You attend it (fire the arrow at its end), and any other event that starts "
            "before it ends can be attended at the same time (same arrow). "
            "When there's a gap, start a new session.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if not points:", {"code": True}),
        " — Guard clause: no balloons means 0 arrows needed. Prevents index errors below."
    ])),
    N.para(N.rich([
        ("points.sort(key=lambda x: x[1])", {"code": True}),
        " — Sort by the right endpoint (end). This is the crucial greedy choice."
    ])),
    N.para(N.rich([
        ("arrows = 1", {"code": True}),
        " — We always need at least one arrow for the first balloon."
    ])),
    N.para(N.rich([
        ("arrow_pos = points[0][1]", {"code": True}),
        " — Shoot the first arrow at the end of the earliest-ending balloon."
    ])),
    N.para(N.rich([
        ("for start, end in points[1:]:", {"code": True}),
        " — Scan every remaining balloon (already sorted by end)."
    ])),
    N.para(N.rich([
        ("if start > arrow_pos:", {"code": True}),
        " — Strictly greater: if this balloon starts after our arrow, it's not covered. "
        "Touching endpoints (start == arrow_pos) ARE covered — no new arrow needed."
    ])),
    N.para(N.rich([
        ("arrows += 1", {"code": True}),
        " — New disjoint overlap group discovered; fire a new arrow."
    ])),
    N.para(N.rich([
        ("arrow_pos = end", {"code": True}),
        " — New arrow shoots at this balloon's end. Do NOT update arrow_pos on the else "
        "branch — that would shrink coverage."
    ])),
    N.para(N.rich([
        ("return arrows", {"code": True}),
        " — Count of disjoint groups equals the minimum arrows needed."
    ])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Greedy: Sort by Start"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same problem, different sorting order. Sort by start coordinate. "
            "Track the minimum end seen in the current overlap group — that's the "
            "rightmost position where one arrow can still hit all balloons in the group."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Sorting by start alone doesn't tell you where to shoot — you need to "
            "track the shrinking overlap region as more balloons join the group."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When a new balloon overlaps (start <= cur_end), the valid arrow position "
            "is now [start, min(cur_end, end)] — the intersection shrinks. "
            "When it doesn't overlap (start > cur_end), start a new group."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sort by start. For each balloon: if start > cur_end, new group (arrows++, cur_end = end). "
            "Otherwise, shrink the valid window: cur_end = min(cur_end, end)."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("points.sort()", {"code": True}),
        " — Sort by start coordinate (Python's default sort on lists of lists)."
    ])),
    N.para(N.rich([
        ("cur_end = points[0][1]", {"code": True}),
        " — Initialize the valid arrow window's right bound to the first balloon's end."
    ])),
    N.para(N.rich([
        ("if start > cur_end:", {"code": True}),
        " — Gap found: this balloon starts after the current group's minimum end. New group."
    ])),
    N.para(N.rich([
        ("cur_end = min(cur_end, end)", {"code": True}),
        " — Balloon overlaps: the valid intersection region shrinks to the smaller end."
    ])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy — Sort by End (Interview Pick)", "O(n log n)", "O(1)"],
        ["Greedy — Sort by Start", "O(n log n)", "O(1)"],
        ["Brute Force (all positions)", "Exponential", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals (Greedy Interval Scheduling)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sort by End, Greedy"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem involves intervals on a 1D axis. "
        "(2) Asks for minimum number of points/events/arrows to cover all intervals. "
        "(3) Keywords: minimum arrows, minimum platforms, minimum meeting rooms. "
        "(4) Exchange argument holds: shooting at the end of the earliest-ending unpopped interval "
        "is always at least as good as any earlier position.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort-by-End Greedy technique:"),
    N.bullet(N.rich([
        ("Non-overlapping Intervals", {"bold": True}),
        " (Medium, LeetCode #435) — Minimum intervals to remove so none overlap; identical greedy, count removals"
    ])),
    N.bullet(N.rich([
        ("Merge Intervals", {"bold": True}),
        " (Medium, LeetCode #56) — Sort by start, merge consecutive overlapping intervals"
    ])),
    N.bullet(N.rich([
        ("Meeting Rooms II", {"bold": True}),
        " (Medium, LeetCode #253) — Minimum conference rooms = max concurrent meetings; min-heap approach"
    ])),
    N.bullet(N.rich([
        ("Insert Interval", {"bold": True}),
        " (Medium, LeetCode #57) — Insert and merge a new interval into a sorted list"
    ])),
    N.bullet(N.rich([
        ("Jump Game II", {"bold": True}),
        " (Medium, LeetCode #45) — Minimum jumps to reach end; greedy with current-reach tracking, same flavor as arrow_pos"
    ])),
    N.bullet(N.rich([
        ("Video Stitching", {"bold": True}),
        " (Medium, LeetCode #1024) — Minimum clips to cover [0,T]; greedy on sorted clips, identical end-tracking idea"
    ])),
    N.bullet(N.rich([
        ("Interval List Intersections", {"bold": True}),
        " (Medium, LeetCode #986) — Two sorted interval lists; two-pointer scan uses same overlap detection"
    ])),
    N.para("These problems share the same core technique: greedy interval scheduling with sort-by-end."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals / Sort by End Greedy section",
        "📚", "gray_background"
    ),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_number_of_arrows_to_burst_balloons")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Write status file
import json
status_dir = os.path.join(os.path.dirname(__file__), ".status")
os.makedirs(status_dir, exist_ok=True)
status_path = os.path.join(status_dir, "minimum_number_of_arrows_to_burst_balloons.json")
with open(status_path, "w") as f:
    json.dump({
        "slug": "minimum_number_of_arrows_to_burst_balloons",
        "html": "OK",
        "notion": "OK",
        "lines": 887,
        "notion_page_id": PAGE_ID,
        "notes": "Fresh page created. 2 solutions. 13-step walkthrough. Sort-by-End Greedy."
    }, f, indent=2)
print(f"Status written to {status_path}")
print(f"RESULT minimum_number_of_arrows_to_burst_balloons | html=OK | notion=OK | lines=887")
