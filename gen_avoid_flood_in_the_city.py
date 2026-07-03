"""
gen_avoid_flood_in_the_city.py
Notion in-place update for LeetCode #1488 – Avoid Flood in The City
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ee-909c-da34ff05c64c"
SLUG = "avoid_flood_in_the_city"

# ── 1) Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1488,
    pattern="Greedy",
    subpatterns=["Greedy Empty Selection"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Use earliest available sunny day in conflict window to retroactively drain a lake before it floods; binary search on sorted set of sunny indices.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("rains", {"code": True}),
        (" where ", {}),
        ("rains[i] > 0", {"code": True}),
        (" means it rains on lake ", {}),
        ("rains[i]", {"code": True}),
        (" on day ", {}),
        ("i", {"code": True}),
        (", and ", {}),
        ("rains[i] = 0", {"code": True}),
        (" means it is a sunny day where you can drain exactly one lake of your choice. "
         "Return an array ans such that: for each rain day, ans[i] = -1; for each sunny day, "
         "ans[i] = the lake you chose to drain. If no valid schedule exists (a lake would flood), return []. "
         "A lake floods if it rains on it again before it has been drained.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Greedy + SortedList (Optimal) ──
sol1_code = """\
from sortedcontainers import SortedList

def avoidFlood(rains):
    n = len(rains)
    ans = [-1] * n           # rain days stay -1; sunny days get lake number
    full = {}                # lake -> day it last rained (lake is now full)
    sunny = SortedList()     # sorted set of available sunny-day indices

    for i, r in enumerate(rains):
        if r == 0:               # sunny day: collect, assign later
            sunny.add(i)
            ans[i] = 1           # placeholder; overwritten if conflict triggers it
        elif r in full:          # lake r already full -- conflict!
            # Find earliest sunny day strictly after last rain of r and before today
            idx = sunny.bisect_right(full[r])
            if idx == len(sunny) or sunny[idx] >= i:
                return []        # no valid sunny in window -- impossible
            j = sunny[idx]
            ans[j] = r           # retroactively assign: drain lake r on day j
            sunny.remove(j)      # consume this sunny day
            full[r] = i          # lake r refills from today's rain
        else:                    # first rain on lake r
            full[r] = i

    return ans               # leftover sunnies keep placeholder 1\
"""

blocks += [
    N.h2("Solution 1 — Greedy + SortedList (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of it as a scheduling problem: sunny days are 'free action slots' and rains on already-full lakes are 'deadlines.' You must use a free slot before the deadline to prevent flooding. The question becomes: which slot to use for which deadline?"),
        N.h4("What Doesn't Work"),
        N.para("Naive approach: when a conflict appears (lake k rains while full), scan backward through the window to find any unused sunny day. This is O(n) per conflict and O(n²) overall — TLE for n=100,000. We need to find the earliest valid slot in O(log n)."),
        N.h4("The Key Observation"),
        N.para("When lake r rains a second time on day i, ANY sunny day in the open window (full[r], i) is a valid assignment. Among those, choosing the EARLIEST one is optimal — it leaves later sunny days available for future conflicts (exchange argument: no other lake needs the earlier slot if the later one also works)."),
        N.h4("Building the Solution"),
        N.para("Maintain sunny day indices in a SortedList. On each rain conflict, call bisect_right(full[r]) to find the first sunny index after the lake's last rain. If that index is also before today (< i), assign it retroactively and remove it. Otherwise, return []."),
        N.callout(
            "Analogy: Managing a shared conference room. Each 'rain' books a room; you must schedule a cleaning (sunny day) between consecutive bookings of the same room. Always assign the earliest available cleaning slot — this leaves later slots open for other rooms.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("ans = [-1] * n", {"code": True}), " — Default output: all rain days will be -1. Sunny days start with placeholder 1 (overwritten when a conflict forces an assignment)."])),
    N.para(N.rich([("full = {}", {"code": True}), " — Maps lake → day of its most recent rain. This is the 'last filled' record. If a lake is in full, it is currently full and a second rain would flood it."])),
    N.para(N.rich([("sunny = SortedList()", {"code": True}), " — Keeps available sunny-day indices in sorted order. Supports O(log n) insert, O(log n) remove, and O(log n) binary search."])),
    N.para(N.rich([("sunny.add(i)", {"code": True}), " — On a sunny day: add this day's index to the sorted set. It's now available as a drain slot for any future conflict."])),
    N.para(N.rich([("ans[i] = 1", {"code": True}), " — Placeholder value. If this sunny day is never claimed by a conflict, it stays 1 (draining lake 1 is harmless if lake 1 is not full)."])),
    N.para(N.rich([("idx = sunny.bisect_right(full[r])", {"code": True}), " — Binary search: find the first sunny index strictly greater than full[r] (the day lake r last rained). This is the earliest candidate drain slot."])),
    N.para(N.rich([("if idx == len(sunny) or sunny[idx] >= i", {"code": True}), " — Two impossible conditions: (1) no sunny day at all after last_rain[r], or (2) the earliest candidate is today or later (too late — lake already flooded by today's rain)."])),
    N.para(N.rich([("ans[j] = r", {"code": True}), " — Retroactive assignment: day j (a past sunny day) is now designated to drain lake r. This 'rewrites history' safely since we haven't committed j to anything yet."])),
    N.para(N.rich([("sunny.remove(j)", {"code": True}), " — Consume this sunny day from the sorted set. O(log n). It can no longer be used for any other lake."])),
    N.para(N.rich([("full[r] = i", {"code": True}), " — Update: lake r was drained on day j, then refilled by today's rain. Its new 'last filled' day is i."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
sol2_code = """\
def avoidFlood_brute(rains):
    \"\"\"O(n^2) — for understanding; TLE for n=100000\"\"\"
    ans = [1] * len(rains)   # init all sunny as 1 (placeholder)
    full = {}
    for i, r in enumerate(rains):
        if r == 0:
            continue         # will be handled retroactively
        ans[i] = -1
        if r in full:        # conflict: lake r already full
            found = False
            for j in range(full[r] + 1, i):   # O(n) backward scan
                if rains[j] == 0 and ans[j] != -1:
                    ans[j] = r
                    found = True
                    break
            if not found:
                return []
        full[r] = i
    return ans\
"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²) (for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem, but we detect conflicts only when they happen and search backward through the window naively — no data structure needed."),
        N.h4("What Doesn't Work (Why We Optimize)"),
        N.para("The backward scan is O(n) per conflict. In the worst case (half the days are sunnies, half are conflicting rains), this is O(n²/4) = O(n²) total. For n=100,000, this is 10^10 operations — too slow."),
        N.h4("The Key Observation"),
        N.para("This brute force is correct but slow. The O(log n) improvement comes from replacing the linear scan with a binary search on a sorted set of available sunny indices."),
        N.h4("Building the Solution"),
        N.para("Scan left to right. For each rain conflict, scan linearly from full[r]+1 to i-1 for any unused sunny day. First found: assign. None found: return []."),
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
        ["Brute Force (linear scan)", "O(n²)", "O(n)"],
        ["Greedy + SortedList (Optimal)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Greedy Empty Selection"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) You have 'free action' days that must be used for something — but which thing is unknown until later. "
        "(2) Events create deadlines: 'use a free slot before this deadline or fail.' "
        "(3) You need to match free slots to deadlines optimally — greedy (earliest slot) + binary search.",
        "🔎", "green_background"
    ),
    N.para("Note: 'Greedy Empty Selection' is the sub-pattern name used here — it describes the pattern where empty/free/sunny slots are strategically assigned to prevent future constraint violations. This classification is analysis-based."),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (greedy assignment of free actions to satisfy future deadlines):"),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — Assign tasks to time slots with mandatory cooldown between same-task repeats; greedy frequency-based scheduling (#621)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Minimum conference rooms needed for overlapping meetings; greedy heap/events-based (#253)"])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — Remove fewest intervals to make the rest non-overlapping; greedy earliest-end-time (#435)"])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), " (Medium) — Minimum jumps to reach end; greedy choose furthest reachable from current window (#45)"])),
    N.bullet(N.rich([("Minimum Arrows to Burst Balloons", {"bold": True}), " (Medium) — Fewest arrows to pop all balloon intervals; greedy interval coverage (#452)"])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), " (Medium) — Capacity scheduling with pick-up and drop-off events; greedy events processing (#1094)"])),
    N.para("These problems share the same core technique: greedy assignment of limited resources (actions/slots) to satisfy time-bounded constraints, often combined with a sorted structure for efficient lookup."),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
