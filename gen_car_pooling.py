"""gen_car_pooling.py — Notion update for Car Pooling (#1094)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8120-8277-fdeca53aa985"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1094,
    pattern="Intervals",
    subpatterns=["Difference Array or Sweep"],
    tc="O(n + K)",
    sc="O(K)",
    key_insight="Encode each trip as +numPass at from and -numPass at to in a diff array; one prefix-sum sweep recovers occupancy at every location.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} blocks.")

# ── 3) Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 2D integer array ", {}),
        ("trips", {"code": True}),
        (" where ", {}),
        ("trips[i] = [numPassengers, from, to]", {"code": True}),
        (" represents the i-th trip, and an integer ", {}),
        ("capacity", {"code": True}),
        (" representing the maximum number of passengers the vehicle can carry, return ", {}),
        ("True", {"code": True}),
        (" if it is possible to pick up and drop off all passengers for all the given trips, or ", {}),
        ("False", {"code": True}),
        (" otherwise. Passengers board at ", {}),
        ("from", {"code": True}),
        (" and exit AT ", {}),
        ("to", {"code": True}),
        (" (half-open interval [from, to)).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Difference Array ──
solution1_code = """\
def carPooling(trips, capacity):
    diff = [0] * 1001          # locations 0-1000 inclusive
    for numPass, start, end in trips:
        diff[start] += numPass  # passengers board
        diff[end]   -= numPass  # passengers exit at 'to'
    curr = 0
    for passengers in diff:
        curr += passengers      # prefix sum = occupancy here
        if curr > capacity:
            return False
    return True"""

blocks += [
    N.h2("Solution 1 — Difference Array (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each trip occupies the interval [from, to) on a 1D number line (the road). Multiple trips may overlap, stacking their passengers. We need to find whether the maximum stack height at any single point exceeds capacity."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach checks every trip at every location: O(n × K). For 1000 trips over 1001 locations that is one million operations — too slow for large input."),
        N.h4("The Key Observation"),
        N.para("We do NOT need to know the exact occupancy at every location during the build phase. We only need to know WHERE it changes. Each trip contributes exactly two change-points: +numPass at 'from' (passengers board) and -numPass at 'to' (passengers exit). That's O(1) work per trip."),
        N.h4("Building the Solution"),
        N.para("Allocate diff[0..1000] = 0. For each trip write diff[start] += numPass and diff[end] -= numPass. Then one forward prefix-sum sweep accumulates these deltas into actual occupancy at each location. Check capacity at every step. The sweep costs O(K) = O(1001) regardless of how many trips there are."),
        N.callout("Analogy: Think of the diff array as a 'delta ledger'. Instead of writing the full passenger count for every location in [from, to), you just log 'at from, add numPass; at to, remove numPass'. One sweep of the ledger gives you the real count at any point.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("diff = [0] * 1001", {"code": True}), " — allocate array covering all possible locations [0, 1000]; size 1001 for inclusive upper bound."])),
    N.para(N.rich([("diff[start] += numPass", {"code": True}), " — board event: from this location onward, numPass more passengers are in the car."])),
    N.para(N.rich([("diff[end] -= numPass", {"code": True}), " — exit event: AT the destination, these passengers leave (half-open interval). NOT end+1."])),
    N.para(N.rich([("curr = 0", {"code": True}), " — running prefix sum representing passengers currently in car."])),
    N.para(N.rich([("curr += passengers", {"code": True}), " — accumulate delta; curr now equals actual occupancy at this location."])),
    N.para(N.rich([("if curr > capacity: return False", {"code": True}), " — check AFTER the update; fail fast the moment any location overflows."])),
    N.para(N.rich([("return True", {"code": True}), " — no location exceeded capacity; all trips are feasible."])),
    N.callout("Key boundary rule: diff[end] -= numPass (NOT diff[end+1]). Passengers exit AT their destination. Wrong offset inflates occupancy by 1 extra location per trip.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Event Sorting ──
solution2_code = """\
def carPooling(trips, capacity):
    events = []
    for numPass, start, end in trips:
        events.append((start, +numPass))   # board (positive)
        events.append((end,   -numPass))   # exit (negative)
    # sort by location; at ties, exits (-) sort before boards (+)
    events.sort()
    curr = 0
    for loc, delta in events:
        curr += delta
        if curr > capacity:
            return False
    return True"""

blocks += [
    N.h2("Solution 2 — Event Sorting (Generalizes to Unbounded Coordinates)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each trip creates two events on the timeline: a 'board' event (positive) and an 'exit' event (negative). If we sort all events by location and sweep through them updating a running counter, we get the occupancy at every event point."),
        N.h4("What Doesn't Work"),
        N.para("Difference array requires a fixed-size array of K positions. When coordinates are unbounded (e.g., locations up to 10^9), allocating a 10^9 array is infeasible."),
        N.h4("The Key Observation"),
        N.para("We only care about locations where passengers board or exit — 2n event points at most. Sorting these 2n events and sweeping them gives the same information in O(n log n) time without any fixed-size allocation."),
        N.h4("Building the Solution"),
        N.para("For each trip append (start, +numPass) and (end, -numPass). Sort by (location, delta) so that at the same location exits (negative) are processed before boards (positive) — preventing false over-capacity at a simultaneous swap. Sweep and check."),
        N.callout("Tie-breaking matters: if a passenger exits and a new one boards at the same location, process the exit first. Python's default tuple sort handles this correctly since negative deltas sort before positive at the same location.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("events.append((start, +numPass))", {"code": True}), " — board event: at 'start', occupancy increases."])),
    N.para(N.rich([("events.append((end, -numPass))", {"code": True}), " — exit event: at 'end', occupancy decreases."])),
    N.para(N.rich([("events.sort()", {"code": True}), " — sort by (location, delta); negative deltas sort before positive at same location — exits before boards."])),
    N.para(N.rich([("curr += delta", {"code": True}), " — update running count with this event's delta."])),
    N.para(N.rich([("if curr > capacity: return False", {"code": True}), " — capacity check after each event."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (per location)", "O(n × K)", "O(K)"],
        ["Difference Array (Interview Pick)", "O(n + K)", "O(K), K=1001"],
        ["Event Sorting", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals (range overlap detection with resource constraints)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Difference Array or Sweep — encode interval boundaries as (+/-) deltas, recover point values with prefix sum"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Each operation affects a range [l, r] — does any point exceed a threshold?'\n"
        "• Passengers / seats / resources loaded for intervals on a bounded number line\n"
        "• Coordinates are small bounded integers (≤ 1000) → difference array wins\n"
        "• Coordinates are large or unbounded → event sorting with coordinate compression",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Difference Array or Sweep technique:"),
    N.bullet(N.rich([("Range Addition", {"bold": True}), " (Medium, #370) — given range update ops, compute final array; canonical difference array problem."])),
    N.bullet(N.rich([("Maximum Population Year", {"bold": True}), " (Easy, #1854) — count alive people per year; difference array on year range [1950, 2050]."])),
    N.bullet(N.rich([("Corporate Flight Bookings", {"bold": True}), " (Medium, #1109) — seat reservations are range additions; identical diff-array pattern."])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium, #253) — minimum rooms = max simultaneous meetings; event sort or diff array."])),
    N.bullet(N.rich([("My Calendar III", {"bold": True}), " (Hard, #732) — dynamic booking with max-k constraint; sorted-map difference array."])),
    N.bullet(N.rich([("Describe the Painting", {"bold": True}), " (Medium, #2021) — sweep line over painting intervals merging color sets."])),
    N.bullet(N.rich([("Count Subarrays with Fixed Bounds", {"bold": True}), " (Hard, #2444) — boundary tracking with sweep."])),
    N.para("These problems share the core idea: encode range changes as boundary events, recover point values with prefix sums, check constraints."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Intervals section\nSub-Pattern: Difference Array or Sweep · Source: Guide", "📚", "gray_background"),
]

# ── Interactive explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("car_pooling")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
