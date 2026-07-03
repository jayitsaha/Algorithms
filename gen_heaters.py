"""
gen_heaters.py — Notion updater for LeetCode #475 Heaters
Updates the existing page in-place via notion_lib.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cc-b624-fdf3005ed643"

# 1. Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=475,
    pattern="Binary Search",
    subpatterns=["Binary Search Closest"],
    tc="O((m+n) log n)",
    sc="O(1)",
    key_insight="For each house, binary search the sorted heaters to find nearest neighbor; answer = max of per-house min distances.",
    icon="🟡"
)
print("Properties set.")

# 2. Wipe old body
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3. Rebuild body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Winter is coming. Given two arrays ", {}),
        ("houses", {"code": True}),
        (" and ", {}),
        ("heaters", {"code": True}),
        (" representing positions on a number line, every heater has the same radius ", {}),
        ("r", {"code": True}),
        (". A house is warmed if there is at least one heater within radius ", {}),
        ("r", {"code": True}),
        (" of it. Return the minimum radius such that all houses are warmed.", {})
    ])),
    N.divider(),
]

# Solution 1 — Sort + Binary Search (optimal)
blocks += [
    N.h2("Solution 1 — Sort + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need one radius r that covers every house. Each house has a 'minimum required radius' — the distance to its nearest heater. If we know this per-house minimum, the global answer is their maximum: r must be at least as large as the hardest house's requirement."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each house, scan all heaters to find the nearest one. O(m×n) — TLE when m, n ≈ 25,000."),
        N.h4("The Key Observation"),
        N.para("If heaters are sorted, the nearest heater to any house is always one of the two neighbors at the binary search boundary. bisect_left gives the first heater >= house; the element just before is the last heater < house. One of these two is the nearest."),
        N.h4("Building the Solution"),
        N.para("Sort heaters once (O(n log n)). For each house, call bisect_left (O(log n)) to find pos. Right neighbor: heaters[pos] if pos < n, else inf. Left neighbor: heaters[pos-1] if pos > 0, else inf. Nearest distance = min(right, left). Update ans = max(ans, nearest)."),
        N.callout("Analogy: like finding the nearest bus stop on a sorted route — the closest stop is either the one just before or just after your position. Check both, take the shorter walk.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""from bisect import bisect_left

def findRadius(houses, heaters):
    heaters.sort()          # Sort once: O(n log n)
    ans = 0
    for house in houses:
        pos = bisect_left(heaters, house)          # First heater >= house
        right = heaters[pos] - house if pos < len(heaters) else float('inf')
        left  = house - heaters[pos-1] if pos > 0 else float('inf')
        ans = max(ans, min(right, left))           # Nearest heater; update max
    return ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("heaters.sort()", {"code": True}), " — Sort heaters ascending. Enables binary search. O(n log n) one-time cost."])),
    N.para(N.rich([("ans = 0", {"code": True}), " — Running maximum of per-house minimum distances. Starts at 0; grows as we process houses."])),
    N.para(N.rich([("for house in houses:", {"code": True}), " — Iterate every house. m iterations total."])),
    N.para(N.rich([("pos = bisect_left(heaters, house)", {"code": True}), " — Binary search in sorted heaters. Returns leftmost index where house could be inserted. O(log n)."])),
    N.para(N.rich([("right = heaters[pos] - house if pos < len(heaters) else float('inf')", {"code": True}), " — Distance to right neighbor (first heater >= house). Use inf if no right neighbor exists."])),
    N.para(N.rich([("left = house - heaters[pos-1] if pos > 0 else float('inf')", {"code": True}), " — Distance to left neighbor (last heater < house). Use inf if no left neighbor exists."])),
    N.para(N.rich([("ans = max(ans, min(right, left))", {"code": True}), " — Nearest heater distance = min of both neighbors. Update global maximum."])),
    N.para(N.rich([("return ans", {"code": True}), " — The minimum radius that covers all houses."])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force O(m×n)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly apply the definition: for each house, check every heater and find the minimum distance. Accumulate the global maximum."),
        N.h4("What Doesn't Work"),
        N.para("This is O(m×n) — quadratic. With m, n up to 25,000 this is 625 million operations, causing TLE. But it's a valid starting point to propose in interviews."),
        N.h4("The Key Observation"),
        N.para("No clever trick here — just a nested loop. The correct answer comes out, but too slowly. Propose this first, then optimize."),
        N.h4("Building the Solution"),
        N.para("For each house: compute abs(house - h) for every heater h, take the min. Update the global max. Return global max."),
    ]),
    N.h3("Code"),
    N.code("""def findRadius_brute(houses, heaters):
    ans = 0
    for house in houses:
        nearest = min(abs(house - h) for h in heaters)
        ans = max(ans, nearest)
    return ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("min(abs(house - h) for h in heaters)", {"code": True}), " — Scan all heaters, find the minimum absolute distance to this house. O(n) per house."])),
    N.para(N.rich([("ans = max(ans, nearest)", {"code": True}), " — Track the maximum nearest-heater distance across all houses."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(m×n)", "O(1)"],
        ["Sort + Binary Search (optimal)", "O((m+n) log n)", "O(1)"],
        ["Binary Search on Answer", "O((m+n) × log V)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Binary Search Closest — find the nearest element in a sorted array using bisect_left, then check both boundary neighbors"])),
    N.callout(
        "When to recognize this pattern: 'Find nearest / closest element in a sorted collection', 'Minimum radius / distance / range to cover all items', repeated nearest-neighbor queries on a static sorted array, any minimax framing (minimize the maximum cost across all items).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Binary Search Closest technique:"),
    N.bullet(N.rich([("Find K Closest Elements", {"bold": True}), " (Medium) — bisect to anchor, shrink window to k nearest"])),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), " (Easy) — pure bisect_left; classic insertion point query"])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — BS on answer: min speed k to eat all bananas in h hours"])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), " (Medium) — BS on answer: min capacity covering all packages"])),
    N.bullet(N.rich([("Minimize Maximum Distance to Gas Station", {"bold": True}), " (Hard) — same minimax on a number line; BS on answer"])),
    N.bullet(N.rich([("Magnetic Force Between Two Balls", {"bold": True}), " (Medium) — BS on minimum distance; check feasibility with greedy"])),
    N.para("These problems share the core technique: sort a reference array, binary search for neighbors, take min-distance to find nearest, accumulate max across all queries."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9: Binary Search", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("heaters")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
