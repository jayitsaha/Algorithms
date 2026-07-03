"""
gen_gas_station.py — Notion update for LeetCode #134 Gas Station
Pattern: Greedy / Start Where Deficit Recovers
"""
import sys
sys.path.insert(0, "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms")
import notion_lib as N

PAGE_ID = "39193418-809c-816a-b2d8-d705263d9856"

# ── 1. Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=134,
    pattern="Greedy",
    subpatterns=["Start Where Deficit Recovers"],
    tc="O(n)",
    sc="O(1)",
    key_insight="If total net gain >= 0, a valid start always exists; jump past any station that makes running tank negative.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old bulk body ───────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Build new body ───────────────────────────────────────────────────────
PROBLEM_STMT = (
    "You are given two integer arrays gas and cost of length n, representing n gas stations "
    "arranged in a circle. At station i you receive gas[i] units of fuel and spend cost[i] "
    "units to travel to station i+1 (the last station wraps back to 0). "
    "Your car starts with an empty tank and unlimited capacity. "
    "Return the index of the starting station from which you can complete the entire circuit "
    "exactly once, or -1 if it is not possible. It is guaranteed that the answer is unique if it exists."
)

SOL1_CODE = """\
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    total_tank = 0   # tracks global feasibility
    curr_tank  = 0   # tracks tank from current candidate start
    start      = 0   # candidate starting station

    for i in range(len(gas)):
        net = gas[i] - cost[i]   # net gain at station i
        total_tank += net
        curr_tank  += net

        # Running tank went negative — start cannot be any station
        # from the old `start` up to and including i
        if curr_tank < 0:
            start     = i + 1   # try next station as new candidate
            curr_tank = 0       # reset running tank

    # If total is negative no solution exists
    return start if total_tank >= 0 else -1
"""

SOL1_LINE_BY_LINE = [
    ("total_tank = 0", "Accumulates net gain across ALL stations to check global feasibility at the end."),
    ("curr_tank = 0", "Tracks running fuel balance from the current candidate start position."),
    ("start = 0", "Current candidate starting index; shifts right whenever we hit a deficit."),
    ("for i in range(len(gas)):", "Single left-to-right pass through all n stations."),
    ("net = gas[i] - cost[i]", "Net gain: positive means surplus, negative means we lose fuel here."),
    ("total_tank += net", "Add to global accumulator — determines overall feasibility."),
    ("curr_tank += net", "Add to local accumulator — measures if starting from `start` works so far."),
    ("if curr_tank < 0:", "Tank went negative: starting from `start` through i is impossible."),
    ("start = i + 1", "Every station from old start to i is a bad start; jump to i+1 as new candidate."),
    ("curr_tank = 0", "Reset running balance for the new candidate start."),
    ("return start if total_tank >= 0 else -1", "If total net >= 0 the answer exists and is `start`; else no solution."),
]

SOL2_CODE = """\
def canCompleteCircuit_brute(gas: list[int], cost: list[int]) -> int:
    n = len(gas)
    for start in range(n):
        tank = 0
        completed = True
        for step in range(n):
            i = (start + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                completed = False
                break
        if completed:
            return start
    return -1
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two integer arrays "), ("gas", {"code": True}),
        (" and "), ("cost", {"code": True}),
        (" of length "), ("n", {"code": True}),
        (", representing "), ("n", {"code": True}),
        (" gas stations arranged in a circle. "
         "At station "), ("i", {"code": True}),
        (" you receive "), ("gas[i]", {"code": True}),
        (" units of fuel and spend "), ("cost[i]", {"code": True}),
        (" units to travel to the next station. "
         "Your car starts with an empty tank (unlimited capacity). "
         "Return the starting index from which you can complete the full circuit, "
         "or "), ("-1", {"code": True}),
        (" if impossible. The answer is unique if it exists."),
    ])),
    N.divider(),
]

# Solution 1 — Greedy (Interview Pick)
blocks += [
    N.h2("Solution 1 — Greedy One-Pass (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Replace each station with its net gain: net[i] = gas[i] - cost[i]. "
            "We need to find a starting index such that every prefix of the circular "
            "traversal beginning there has a non-negative running sum."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force tries every starting station and simulates the full loop — O(n²). "
            "For n = 10⁵ that's 10¹⁰ operations: far too slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two independent facts: "
            "(1) If the sum of all net gains is negative, the trip is globally impossible — "
            "no starting point can compensate for an overall deficit. "
            "(2) If the running tank from candidate start drops below zero at station i, "
            "then EVERY station from the old start through i is also invalid — "
            "none of them can accumulate enough surplus to survive past i."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Maintain two counters: total_tank (global sum) and curr_tank (local sum from current "
            "candidate). Scan left to right. Whenever curr_tank < 0, discard all stations from "
            "start to i as candidates and jump to i+1. At the end, if total_tank >= 0, "
            "the last candidate start is the answer."
        ),
        N.callout(
            "Analogy: Imagine a relay race where each runner gains or loses energy. "
            "If the team's total energy is non-negative, they can finish. "
            "Whenever a sub-team's accumulated energy goes negative, the next runner "
            "must be the fresh starting point.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
]

for line, explanation in SOL1_LINE_BY_LINE:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation),
    ])))

blocks += [N.divider()]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force (Try Every Start)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The most direct interpretation: for each possible starting index, "
            "simulate the entire circuit and check if the tank ever goes negative."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "O(n²) time. For large inputs (n = 10⁵) this is too slow for competitive "
            "settings, but it is perfectly correct and a valid starting point to discuss."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We try each of the n starting positions and walk n steps (with modular indexing). "
            "If the tank never drops below zero in a full circuit, return that start."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Outer loop over start indices 0..n-1. Inner loop over n steps using "
            "(start + step) % n for circular indexing. Exit inner loop early on first "
            "negative tank. Return start if the inner loop completes."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("for start in range(n):", {"code": True, "bold": True}),
        (" — Try each station as a potential starting point."),
    ])),
    N.para(N.rich([
        ("for step in range(n):", {"code": True, "bold": True}),
        (" — Simulate n steps of the circuit."),
    ])),
    N.para(N.rich([
        ("i = (start + step) % n", {"code": True, "bold": True}),
        (" — Wrap-around index for circular traversal."),
    ])),
    N.para(N.rich([
        ("tank += gas[i] - cost[i]", {"code": True, "bold": True}),
        (" — Update running fuel balance."),
    ])),
    N.para(N.rich([
        ("if tank < 0: break", {"code": True, "bold": True}),
        (" — This start is bad; break early."),
    ])),
    N.para(N.rich([
        ("if completed: return start", {"code": True, "bold": True}),
        (" — Full circuit succeeded with this start."),
    ])),
    N.divider(),
]

# Complexity Table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy One-Pass (Optimal)", "O(n)", "O(1)"],
        ["Brute Force", "O(n²)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Start Where Deficit Recovers"])),
    N.callout(
        "When to recognize this pattern: "
        "Circular traversal, feasibility question, 'can you complete a loop', "
        "array of gains and costs, uniqueness guarantee of the answer. "
        "Key signal: running prefix sum that can go negative → greedy restart.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Greedy technique:"),
    N.bullet(N.rich([("Jump Game", {"bold": True}), " (Medium) — greedy reachability, scan once tracking max reach."])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), " (Medium) — greedy BFS-like, count minimum jumps."])),
    N.bullet(N.rich([("Candy", {"bold": True}), " (Hard) — two-pass greedy satisfying neighbor constraints."])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), " (Medium) — greedy scheduling based on frequency."])),
    N.bullet(N.rich([("Partition Labels", {"bold": True}), " (Medium) — greedy interval merging, single pass."])),
    N.bullet(N.rich([("Assign Cookies", {"bold": True}), " (Easy) — greedy matching of resources to demands."])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — greedy removal by earliest end time."])),
    N.para("These problems share the core greedy theme: make the locally best decision and prove it leads to the global optimum."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy section", "📚", "gray_background"),
    N.divider(),
]

# Visual Explainer embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("gas_station")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── 4. Append all blocks ────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
