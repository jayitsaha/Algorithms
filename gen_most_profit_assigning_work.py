"""
Notion regeneration script for Most Profit Assigning Work (#826).
Run: cd /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms && python3 gen_most_profit_assigning_work.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8152-bdb8-d7c4c8150487"

# ── 1) Properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=826,
    pattern="Greedy",
    subpatterns=["Sort + Two Pointers"],
    tc="O(n log n + m log m)",
    sc="O(n)",
    key_insight="Sort jobs by difficulty, sort workers by ability; sweep with a running-max profit pointer that never resets.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──
print("Wiping existing page body...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Build body blocks ──
SOL1_CODE = """\
def maxProfitAssignment(difficulty, profit, worker):
    # Pair (difficulty, profit) and sort by difficulty ascending
    jobs = sorted(zip(difficulty, profit))
    # Sort workers by ability ascending (weakest first)
    worker.sort()
    # total = answer accumulator; best_profit = running max; j = job pointer
    total = best_profit = j = 0
    for ability in worker:
        # Unlock all jobs this worker can do (inner loop total O(n) across all workers)
        while j < len(jobs) and jobs[j][0] <= ability:
            best_profit = max(best_profit, jobs[j][1])  # running max — profit is NOT monotone
            j += 1
        # This worker earns the best profit among all jobs with difficulty <= ability
        total += best_profit
    return total
"""

SOL2_CODE = """\
def maxProfitAssignment(difficulty, profit, worker):
    # O(n x m) brute force — correct but TLE for n, m ~ 10^4
    total = 0
    for ability in worker:
        best = 0
        for d, p in zip(difficulty, profit):
            if d <= ability:
                best = max(best, p)
        total += best
    return total
"""

SOL3_CODE = """\
import bisect

def maxProfitAssignment(difficulty, profit, worker):
    # Build prefix-max profit array over jobs sorted by difficulty
    jobs = sorted(zip(difficulty, profit))
    diffs = [j[0] for j in jobs]
    # prefix_max[i] = max profit among jobs[0..i]
    prefix_max = []
    running = 0
    for _, p in jobs:
        running = max(running, p)
        prefix_max.append(running)
    total = 0
    for ability in worker:
        # Binary search: find rightmost job with difficulty <= ability
        idx = bisect.bisect_right(diffs, ability) - 1
        if idx >= 0:
            total += prefix_max[idx]
    return total
"""

blocks = []

# ── Problem statement ──
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    "You have n jobs. Each job i has a difficulty difficulty[i] and a profit profit[i]. "
    "You also have m workers. Worker k can complete job i if difficulty[i] <= worker[k]. "
    "Every worker can be assigned at most one job, but multiple workers can be assigned "
    "the same job. Return the maximum sum of profits achievable. A worker that cannot do "
    "any job earns 0."
))
blocks.append(N.divider())

# ── Solution 1 — Greedy: Sort + Two Pointers ──
blocks.append(N.h2("Solution 1 — Greedy: Sort + Two Pointers (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "We need to pair each worker with the job that earns them the most money, given "
        "their ability cap. Since unlimited workers can do the same job, there is no "
        "resource conflict — each worker's optimal choice is completely independent."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Naively, for each worker we scan all n jobs to find the maximum-profit one they "
        "qualify for. That's O(n x m) — TLE when n, m ~ 10^4. We need to avoid re-scanning "
        "jobs already seen by previous (weaker) workers."
    ),
    N.h4("The Key Observation"),
    N.para(
        "If we sort workers by ability (weakest first) and sort jobs by difficulty, then as "
        "we process each successive worker, we only ever unlock MORE jobs — never fewer. "
        "This monotone property means a single job pointer j can sweep jobs left to right "
        "and never needs to reset. The critical insight: profit is NOT monotone with difficulty, "
        "so we track a running maximum best_profit rather than just looking at the latest job."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1) Sort jobs by difficulty. 2) Sort workers by ability. 3) Maintain j=0 and "
        "best_profit=0. 4) For each worker (weakest to strongest): advance j while "
        "jobs[j].difficulty <= ability, updating best_profit = max(best_profit, jobs[j].profit). "
        "5) Add best_profit to total. j's total movement across all workers is at most n — amortized O(1)."
    ),
    N.callout(
        "Analogy: Think of job difficulty as a 'height bar' and each worker's ability as how high they can reach. "
        "Sort workers shortest to tallest; as you walk through them, lower the bar step by step. "
        "Track the best prize seen at any reachable height — that's your running max.",
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(SOL1_CODE))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("jobs = sorted(zip(difficulty, profit))", {"code": True}),
    " — Pair each difficulty with its profit, then sort the pairs by difficulty ascending. "
    "zip() creates (diff, profit) tuples; sorted() sorts by the first element (diff) by default."
])))
blocks.append(N.para(N.rich([
    ("worker.sort()", {"code": True}),
    " — Sort the worker ability array in-place, ascending. Weakest worker processed first."
])))
blocks.append(N.para(N.rich([
    ("total = best_profit = j = 0", {"code": True}),
    " — Initialize three variables: total accumulates the answer, "
    "best_profit tracks the running maximum profit over all unlocked jobs, "
    "j is the job pointer starting at index 0."
])))
blocks.append(N.para(N.rich([
    ("for ability in worker:", {"code": True}),
    " — Process workers weakest-to-strongest. Each iteration handles one worker."
])))
blocks.append(N.para(N.rich([
    ("while j < len(jobs) and jobs[j][0] <= ability:", {"code": True}),
    " — Advance j as long as there are more jobs AND the next job's difficulty is within "
    "this worker's ability. This 'unlocks' all newly feasible jobs for this worker."
])))
blocks.append(N.para(N.rich([
    ("best_profit = max(best_profit, jobs[j][1])", {"code": True}),
    " — Update running max. We do NOT just use jobs[j][1] because a harder job "
    "might have a lower profit than an easier one. The max ensures we remember the peak."
])))
blocks.append(N.para(N.rich([
    ("j += 1", {"code": True}),
    " — Advance job pointer. Crucially, j NEVER resets to 0. Across all workers, "
    "j makes at most n total steps — O(n) amortized."
])))
blocks.append(N.para(N.rich([
    ("total += best_profit", {"code": True}),
    " — This worker earns best_profit (the highest-profit job they qualify for). "
    "Add it to the running total. If no jobs were unlocked, best_profit=0."
])))
blocks.append(N.divider())

# ── Solution 2 — Brute Force ──
blocks.append(N.h2("Solution 2 — Brute Force: Nested Loops (Reference)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("Direct simulation: for each worker, examine every job and pick the best one they qualify for."),
    N.h4("What Doesn't Work"),
    N.para(
        "This is O(n x m) — correct but too slow when n and m reach 10^4 (10^8 operations). "
        "Use it to verify correctness, not in production."
    ),
    N.h4("The Key Observation"),
    N.para("No clever insight — just iterate. Useful as a baseline to test the greedy solution against."),
    N.h4("Building the Solution"),
    N.para(
        "For each worker: scan all jobs, pick max profit among those with difficulty <= ability."
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(SOL2_CODE))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("for ability in worker:", {"code": True}),
    " — Outer loop over each worker."
])))
blocks.append(N.para(N.rich([
    ("for d, p in zip(difficulty, profit):", {"code": True}),
    " — Inner loop over all jobs. This is the O(n x m) bottleneck — every worker re-scans every job."
])))
blocks.append(N.para(N.rich([
    ("if d <= ability: best = max(best, p)", {"code": True}),
    " — If qualified, track best profit seen. Same running-max logic as the optimal solution."
])))
blocks.append(N.divider())

# ── Solution 3 — Binary Search + Prefix Max ──
blocks.append(N.h2("Solution 3 — Binary Search + Prefix Max (Alternative Optimal)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Precompute a prefix-max array: prefix_max[i] = maximum profit among jobs[0..i] "
        "(sorted by difficulty). Then for each worker, binary search for the rightmost "
        "feasible job index and look up the prefix max — O(log n) per worker."
    ),
    N.h4("What Doesn't Work"),
    N.para("If we binary search without the prefix max, we'd need a second scan to find max profit up to that index — defeating the point."),
    N.h4("The Key Observation"),
    N.para(
        "After sorting jobs by difficulty, build prefix_max so each index holds the best "
        "profit achievable from any job with difficulty <= jobs[i].difficulty. "
        "Binary search gives the rightmost reachable index in O(log n), and prefix_max "
        "gives the answer in O(1)."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1) Sort jobs by difficulty. 2) Build prefix_max array in one pass. "
        "3) For each worker: bisect_right on difficulties array to find insertion point, "
        "subtract 1 to get rightmost feasible index, add prefix_max[idx] to total."
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(SOL3_CODE))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("diffs = [j[0] for j in jobs]", {"code": True}),
    " — Extract just the difficulty values into a list for bisect operations."
])))
blocks.append(N.para(N.rich([
    ("prefix_max[i] = running max of profit[0..i]", {"code": True}),
    " — One-pass prefix max. prefix_max[-1] = max profit across ALL jobs."
])))
blocks.append(N.para(N.rich([
    ("bisect.bisect_right(diffs, ability) - 1", {"code": True}),
    " — Finds the index of the rightmost job with difficulty <= ability. "
    "bisect_right gives the insertion point (one past the last match), so subtract 1."
])))
blocks.append(N.divider())

# ── Complexity Table ──
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space", "Notes"],
    ["Brute Force", "O(n x m)", "O(1)", "TLE for large inputs"],
    ["Greedy Sort + Two Pointers", "O(n log n + m log m)", "O(n)", "Optimal; interview pick"],
    ["Binary Search + Prefix Max", "O(n log n + m log n)", "O(n)", "Same asymptotic; useful when workers are queried dynamically"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sort + Two Pointers (monotone sweep with running max)"])))
blocks.append(N.callout(
    "When to recognize this pattern:\n"
    "• 'Each agent independently picks the best item within their threshold' → sort both, two-pointer sweep\n"
    "• 'Multiple agents can use the same resource' → independent assignments → greedy is globally optimal\n"
    "• Sorted feasibility window that only expands (monotone) → running max/min + single O(n+m) sweep\n"
    "• 'Maximize total by pairing from two independent sorted arrays' → sort + two-pointer or binary search",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique (Greedy / Sort + Two Pointers):"))
blocks.append(N.bullet(N.rich([
    ("Assign Cookies", {"bold": True}), " (Easy) — Match smallest sufficient cookie to each child greedily (#455)"
])))
blocks.append(N.bullet(N.rich([
    ("Boats to Save People", {"bold": True}), " (Medium) — Sort + converging two-pointer to pair heaviest + lightest (#881)"
])))
blocks.append(N.bullet(N.rich([
    ("Advantage Shuffle", {"bold": True}), " (Medium) — Sort + greedy assignment to maximize 'wins' against opponent (#870)"
])))
blocks.append(N.bullet(N.rich([
    ("Two City Scheduling", {"bold": True}), " (Medium) — Sort by cost difference, greedy assignment to minimize total (#1029)"
])))
blocks.append(N.bullet(N.rich([
    ("Maximum Units on a Truck", {"bold": True}), " (Easy) — Sort descending by units/box, greedily fill truck (#1710)"
])))
blocks.append(N.bullet(N.rich([
    ("IPO", {"bold": True}), " (Hard) — Greedy with max-heap: sort by capital, unlock feasible projects, pick highest profit (#502)"
])))
blocks.append(N.bullet(N.rich([
    ("Find Right Interval", {"bold": True}), " (Medium) — Sort + binary search to match interval endpoints (#436)"
])))
blocks.append(N.para("These problems share the core technique: sort one or both arrays to establish a monotone feasibility property, then sweep efficiently."))
blocks.append(N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy section. Sub-pattern: Sort + Two Pointers (monotone sweep). Verified via analysis (not explicitly listed in guide under this exact label).", "📚", "gray_background"))

# ── Interactive Visual Explainer ──
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("most_profit_assigning_work")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
])))

# ── 4) Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
