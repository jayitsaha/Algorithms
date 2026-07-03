"""
gen_car_fleet.py — Notion update for Car Fleet (LeetCode #853)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81df-9251-d6b6de50fb21"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=853,
    pattern="Stacks",
    subpatterns=["Sort + Stack by Time"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Compute solo arrival time per car; sort by position desc; push onto stack only when time > top (new fleet). Stack size = fleet count.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("target", {"code": True}),
        (" representing the destination and two integer arrays ", {}),
        ("position", {"code": True}),
        (" and ", {}),
        ("speed", {"code": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (", where ", {}),
        ("position[i]", {"code": True}),
        (" and ", {}),
        ("speed[i]", {"code": True}),
        (" are the position and speed of the ", {}),
        ("i", {"code": True}),
        ("-th car, return the number of car fleets that will arrive at the destination. "
         "A car fleet is a non-empty set of cars driving at the same position and speed. "
         "A car can never pass another, so it will be slowed down and catch up to the "
         "fleet in front of it.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──────────────────────────────────────────────────────────────
sol1_code = """\
def carFleet(target: int, position: list, speed: list) -> int:
    pairs = sorted(zip(position, speed), reverse=True)
    stack = []
    for pos, spd in pairs:
        time = (target - pos) / spd
        if not stack or time > stack[-1]:
            stack.append(time)   # new fleet
        # else: merges into fleet ahead (no push)
    return len(stack)
"""

blocks += [
    N.h2("Solution 1 — Sort + Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of simulating car positions at every moment, ask: 'What single number fully describes each car's fate?' Answer: its solo arrival time = (target − position) / speed. Two cars form a fleet if the one behind arrives at or before the one ahead. The problem reduces to counting how many strictly increasing arrival times exist when cars are ordered front-to-back."),
        N.h4("What Doesn't Work"),
        N.para("Simulating positions at each time step is O(n²) in the worst case: you'd need to check every pair. Even a greedy 'catch up' simulation requires careful bookkeeping and is error-prone."),
        N.h4("The Key Observation"),
        N.para("Arrival time encodes everything. A car behind with smaller time catches the fleet ahead. A car behind with strictly larger time creates a new fleet. Sort by position descending, process front-to-back, and maintain a monotonically increasing stack of fleet arrival times."),
        N.h4("Building the Solution"),
        N.para("1) Zip position+speed and sort descending by position (closest first). 2) For each car compute time = (target-pos)/spd. 3) If stack is empty or time > stack top, push (new fleet). Otherwise skip (merges). 4) Return len(stack)."),
        N.callout("Analogy: Imagine a highway with toll booths. Faster cars merge into the queue at the first booth ahead of them. The number of distinct 'car trains' at the exit = the answer.", "🚗", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("pairs = sorted(zip(position, speed), reverse=True)", {"code": True}),
        (" — Zip each car's position with its speed so they stay paired. Sort descending by position: this processes the car closest to the target first.", {}),
    ])),
    N.para(N.rich([
        ("stack = []", {"code": True}),
        (" — Will hold arrival times of distinct fleets in strictly increasing order.", {}),
    ])),
    N.para(N.rich([
        ("for pos, spd in pairs:", {"code": True}),
        (" — Iterate front-to-back. Each iteration evaluates one car against the fleet immediately ahead.", {}),
    ])),
    N.para(N.rich([
        ("time = (target - pos) / spd", {"code": True}),
        (" — Solo arrival time: how long this car takes if no one blocks it.", {}),
    ])),
    N.para(N.rich([
        ("if not stack or time > stack[-1]:", {"code": True}),
        (" — Stack empty (first car) OR this car is slower than all fleets ahead. 'Slower' means it takes longer → cannot catch the fleet in front → new fleet.", {}),
    ])),
    N.para(N.rich([
        ("stack.append(time)", {"code": True}),
        (" — Push the new fleet's arrival time. Stack stays monotonically increasing.", {}),
    ])),
    N.para(N.rich([
        ("# else:", {"code": True}),
        (" — If time <= stack[-1], this car arrives before or at the same time as the fleet ahead. It catches up and joins that fleet. No push needed.", {}),
    ])),
    N.para(N.rich([
        ("return len(stack)", {"code": True}),
        (" — Each stack entry = one distinct fleet. The stack size is the answer.", {}),
    ])),
    N.divider(),
]

# ── Solution 2 ──────────────────────────────────────────────────────────────
sol2_code = """\
def carFleet(target: int, position: list, speed: list) -> int:
    pairs = sorted(zip(position, speed), reverse=True)
    fleets = 0
    max_time = 0
    for pos, spd in pairs:
        time = (target - pos) / spd
        if time > max_time:
            fleets += 1
            max_time = time
    return fleets
"""

blocks += [
    N.h2("Solution 2 — Sort + max_time Counter (O(1) Extra Space)"),
    N.toggle_h3("💡 Intuition: Simplify the Stack", [
        N.h4("Reframe the Problem"),
        N.para("Observe that the stack is always monotonically increasing — each new entry is strictly larger than the one below. Therefore stack[-1] is always equal to the running maximum of all times pushed so far."),
        N.h4("What Doesn't Work"),
        N.para("You might think you need the full stack to track all fleet times. But for counting, you only ever compare against the top — which is the running maximum."),
        N.h4("The Key Observation"),
        N.para("Replace the entire stack with a single variable max_time. Whenever time > max_time, it's a new fleet — increment fleets and update max_time."),
        N.h4("Building the Solution"),
        N.para("Same sort. Same loop. Instead of push/pop, just compare time to max_time and update. Space drops to O(1) extra (O(n) for the sorted list which is unavoidable)."),
        N.callout("This is the same logic as Solution 1 — the stack is just tracked implicitly via max_time.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("max_time = 0", {"code": True}),
        (" — Tracks the arrival time of the most recently started fleet (equivalent to stack[-1]).", {}),
    ])),
    N.para(N.rich([
        ("if time > max_time:", {"code": True}),
        (" — Same condition as 'time > stack[-1]'. This car is slower than all existing fleets → new fleet.", {}),
    ])),
    N.para(N.rich([
        ("fleets += 1; max_time = time", {"code": True}),
        (" — Count the new fleet and update the running max (equivalent to pushing onto the stack).", {}),
    ])),
    N.divider(),
]

# ── Complexity Table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (pairwise)", "O(n²)", "O(1)"],
        ["Sort + Monotonic Stack", "O(n log n)", "O(n)"],
        ["Sort + max_time Counter", "O(n log n)", "O(1) extra"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Stack by Time (Monotonic Stack variant)", {})])),
    N.callout(
        "When to recognize this pattern: objects moving toward a common destination at different speeds; groups form when faster catches slower; need to count distinct groups that arrive. Also: any problem where ordering + running max/min determines group membership.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Stack / Sort + Stack):"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Classic monotonic stack: next warmer day (#739)", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Next greater element in O(n) via monotonic stack (#496)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Previous smaller element + stack for max area (#84)", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Stack tracks potential water barriers between walls (#42)", {})])),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), (" (Medium) — Monotonic stack for greedy smallest number (#402)", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Previous/next smaller element via stack (#907)", {})])),
    N.para("These problems share the core technique: maintain a stack (or running extreme value) to track relevant history as you scan in sorted/ordered fashion."),
    N.callout("📚 Pattern: Sort + Stack by Time is a Stacks sub-pattern. The key step is always converting 2D data (position+speed) into 1D (arrival time) before applying the stack.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("car_fleet")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
