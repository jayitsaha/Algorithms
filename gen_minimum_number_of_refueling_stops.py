"""
gen_minimum_number_of_refueling_stops.py
Notion update script for LeetCode #871 — Minimum Number of Refueling Stops
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819d-9451-d88ab1f066e1"
SLUG = "minimum_number_of_refueling_stops"

# ── 1) Properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=871,
    pattern="Greedy",
    subpatterns=["Max Heap for Passed Stations"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Drive forward collecting station fuels in a max-heap; retroactively refuel at the richest passed station whenever you run out.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old content ──────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ─────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A car starts at position "), ("0", {"code": True}), (" with "), ("startFuel", {"code": True}),
        (" litres of fuel. Each unit of fuel moves 1 unit of distance. Given "), ("target", {"code": True}),
        (" distance and gas "), ("stations[i] = [position, fuelAvailable]", {"code": True}),
        (" (sorted by position), return the minimum number of refueling stops needed to reach "),
        ("target", {"code": True}), (". Return "), ("-1", {"code": True}), (" if it is impossible to reach the target."),
    ])),
    N.divider(),
]

# Solution 1 — Greedy + Max Heap
sol1_code = """import heapq

def minRefuelStops(target: int, startFuel: int, stations: list) -> int:
    heap = []          # max-heap of negated fuel values (passed stations)
    fuel = startFuel   # current tank level
    stops = 0          # refueling stop count
    prev = 0           # last visited position

    for pos, cap in stations + [[target, 0]]:
        fuel -= pos - prev          # deduct fuel for distance traveled
        while fuel < 0 and heap:    # stuck: retroactively refuel with best passed station
            fuel -= heapq.heappop(heap)  # pop negated max → adds fuel
            stops += 1              # count one more stop
        if fuel < 0:                # heap empty, still negative → impossible
            return -1
        heapq.heappush(heap, -cap)  # record this station's fuel as future option
        prev = pos                  # advance position

    return stops"""

blocks += [
    N.h2("Solution 1 — Greedy + Max-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to minimize the count of discrete 'stop' actions that collectively provide enough fuel to traverse the full distance. We're not picking which stations to stop at upfront — we're choosing the minimum-size subset."),
        N.h4("What Doesn't Work"),
        N.para("'Greedy nearest' (stop at every station) is suboptimal — you may stop when you don't need to, and miss better stations further ahead. 'Greedy threshold' (stop when fuel < k) also fails because the threshold is problem-dependent."),
        N.h4("The Key Observation"),
        N.para("You only need to stop when you absolutely must (fuel runs out). And when forced to stop, you should retroactively pick the richest station you've already passed — that maximizes the fuel gained per stop."),
        N.h4("Building the Solution"),
        N.para("1. Drive forward, recording each station's fuel in a max-heap (but don't stop yet). 2. When fuel goes negative, pop the max from the heap (retroactive refuel). 3. Count each pop as one stop. 4. If heap empties while still stuck, return -1."),
        N.callout("Analogy: Imagine a road trip where you can magically 'retroactively' decide to have stopped at any gas station you passed. You'd wait until the tank is empty, then pick the gas station with the cheapest (most) fuel.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), " — Max-heap storing negated fuel values of passed stations (Python's heapq is a min-heap; negating simulates a max-heap)."])),
    N.para(N.rich([("fuel = startFuel", {"code": True}), " — Current tank level. Decreases as we travel, increases when we retroactively refuel."])),
    N.para(N.rich([("stops = 0", {"code": True}), " — Counts how many retroactive refueling stops we've made."])),
    N.para(N.rich([("prev = 0", {"code": True}), " — Tracks the last position we visited, used to compute distance traveled."])),
    N.para(N.rich([("stations + [[target, 0]]", {"code": True}), " — Appends the target as a virtual station with 0 fuel. This makes the final leg (last station → target) use the same loop logic as all other legs."])),
    N.para(N.rich([("fuel -= pos - prev", {"code": True}), " — Subtract fuel consumed traveling from the previous position to the current station."])),
    N.para(N.rich([("while fuel < 0 and heap:", {"code": True}), " — If we ran out of fuel (fuel < 0) AND we have options in the heap, retroactively refuel. Repeat until fuel is non-negative or heap empties."])),
    N.para(N.rich([("fuel -= heapq.heappop(heap)", {"code": True}), " — Pop the maximum fuel value (stored negated). Subtracting a negative value adds fuel. e.g., fuel -= (-60) → fuel += 60."])),
    N.para(N.rich([("stops += 1", {"code": True}), " — Each retroactive pop represents one refueling stop."])),
    N.para(N.rich([("if fuel < 0: return -1", {"code": True}), " — Heap exhausted but still stuck. No combination of passed stations can bridge the gap. Return -1."])),
    N.para(N.rich([("heapq.heappush(heap, -cap)", {"code": True}), " — Store this station's fuel as a future option. Negated for max-heap behavior."])),
    N.para(N.rich([("return stops", {"code": True}), " — All segments (including final leg via virtual target) processed. Return the minimum stop count."])),
    N.divider(),
]

# Solution 2 — DP O(n^2)
sol2_code = """def minRefuelStops_dp(target: int, startFuel: int, stations: list) -> int:
    n = len(stations)
    # dp[i] = maximum distance reachable using exactly i refueling stops
    dp = [0] * (n + 1)
    dp[0] = startFuel  # with 0 stops, we can go as far as startFuel

    for i, (pos, fuel) in enumerate(stations):
        # Iterate backwards to avoid using station i twice
        for t in range(i, -1, -1):
            if dp[t] >= pos:  # can reach station i with t stops
                dp[t + 1] = max(dp[t + 1], dp[t] + fuel)

    # Find minimum stops where we can reach target
    for i, reach in enumerate(dp):
        if reach >= target:
            return i
    return -1"""

blocks += [
    N.h2("Solution 2 — Dynamic Programming O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of it as: given exactly i stops, what is the maximum distance I can reach? If for some i, that maximum distance >= target, return i."),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS/recursion would be O(2^n) — trying all subsets of stations to stop at. We need to avoid recomputation."),
        N.h4("The Key Observation"),
        N.para("dp[i] = max distance reachable with exactly i stops. Transition: if dp[t] >= station[j].position, then stopping at station j with t stops gives us dp[t+1] = max(dp[t+1], dp[t] + station[j].fuel)."),
        N.h4("Building the Solution"),
        N.para("Process stations in order. For each station j, update dp[j+1] from dp[t] for all t where dp[t] can reach station j. Iterate t backwards to prevent using the same station twice."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * (n + 1)", {"code": True}), " — dp[i] = max reachable distance using exactly i stops. Initialize all to 0."])),
    N.para(N.rich([("dp[0] = startFuel", {"code": True}), " — With 0 stops, we can reach exactly startFuel distance."])),
    N.para(N.rich([("for t in range(i, -1, -1):", {"code": True}), " — Iterate backwards over stop counts to avoid counting station i twice in the same 'stops' budget."])),
    N.para(N.rich([("if dp[t] >= pos:", {"code": True}), " — Can we reach station i with t stops? Only then can we refuel here."])),
    N.para(N.rich([("dp[t + 1] = max(dp[t + 1], dp[t] + fuel)", {"code": True}), " — If we stop here (t→t+1 stops), we can reach dp[t] + station_fuel."])),
    N.para(N.rich([("for i, reach in enumerate(dp):", {"code": True}), " — Find the minimum i where we can reach target. This is our answer."])),
    N.divider(),
]

# Complexity Table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Greedy + Max-Heap", "O(n log n)", "O(n)", "Interview pick; optimal"],
        ["DP (dp[i] = max reach)", "O(n²)", "O(n)", "Easier to derive; slower"],
        ["Brute Force (all subsets)", "O(2ⁿ)", "O(n)", "Infeasible; understanding only"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Max Heap for Passed Stations — greedily defer decisions, retroactively pick the best passed option when forced."])),
    N.callout(
        "When to recognize this pattern: 'Minimum number of X to reach/achieve Y' where resources are encountered sequentially, you can defer choices, and optimal choice = maximum value each time.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Max Heap Greedy / retroactive optimal selection):"),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), " (Medium) — Minimum jumps to reach end; greedy on reachable range (similar minimize-count structure)"])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), " (Medium) — Capacity-constrained ride scheduling; heap by trip-end time"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Minimum rooms; min-heap of end times for greedy room reuse"])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — Max-heap to greedily schedule most-frequent tasks first"])),
    N.bullet(N.rich([("Minimum Cost to Connect Sticks", {"bold": True}), " (Medium) — Min-heap Huffman greedy: pick cheapest two each round"])),
    N.bullet(N.rich([("IPO / Maximize Capital", {"bold": True}), " (Hard) — Two heaps: unlock projects by capital, pick max profit greedily"])),
    N.bullet(N.rich([("Furthest Building You Can Reach", {"bold": True}), " (Medium) — Min-heap: greedily replace cheapest ladder use with bricks (similar deferred choice)"])),
    N.para("These problems share the core technique: defer decisions and use a heap to efficiently retrieve the optimal past option when forced."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Greedy + Heap (Max Heap for Passed Stations)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append blocks ─────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
