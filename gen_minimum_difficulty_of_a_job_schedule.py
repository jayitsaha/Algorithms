"""
gen_minimum_difficulty_of_a_job_schedule.py
Notion IN-PLACE update for LeetCode #1335 — Minimum Difficulty of a Job Schedule (Hard)
Pattern: Dynamic Programming | Sub-pattern: dp[day][job] with Max
Run: python3 gen_minimum_difficulty_of_a_job_schedule.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81bb-9c3d-e6178a91ff32"
SLUG    = "minimum_difficulty_of_a_job_schedule"

# ── 1. Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1335,
    pattern="Dynamic Programming",
    subpatterns=["dp[day][job] with Max", "Interval DP"],
    tc="O(d·n²)",
    sc="O(d·n)",
    key_insight=(
        "dp[day][j] = min cost to schedule jobs 0..j in exactly day days. "
        "Scan cut-point k right-to-left, maintain rolling max → O(d·n²)."
    ),
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} block(s).")

# ── 3. Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ════════════════════════════════════════════════════════════════════════════
# PROBLEM
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a list of jobs with integer difficulty ratings ", {}),
        ("jobDifficulty", {"code": True}),
        (", and an integer ", {}),
        ("d", {"code": True}),
        (" representing the number of working days. "
         "You must schedule every job across exactly ", {}),
        ("d", {"code": True}),
        (" days. Jobs must be performed in the given order (no reordering); "
         "each day must have at least one job. "
         "The difficulty of a day equals the ", {}),
        ("maximum", {"bold": True}),
        (" difficulty among all jobs done that day. "
         "Return the minimum total difficulty summed across all days, "
         "or ", {}),
        ("-1", {"code": True}),
        (" if it is impossible.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("jobDifficulty = [6,5,4,3,2,1], d = 2", {"code": True}),
        (" → ", {}),
        ("7", {"code": True}),
        ("  (schedule [6,5,4,3,2] | [1], cost = 6 + 1 = 7)", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ d ≤ n ≤ 300, 0 ≤ jobDifficulty[i] ≤ 1000", {"code": True}),
    ])),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# WHY IS THIS DP?  (DP deep-dive section per SKILL.md)
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The minimum cost for scheduling jobs 0..j in day days depends only on "
         "the minimum cost for jobs 0..k in day-1 days, for some cut-point k. "
         "No information about how the prefix was arranged is needed once we know "
         "its optimal cost — the global optimum is built from optimal subproblem solutions.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Without memoization, many different parent states ask 'best cost for jobs 0..k in 2 days?' "
         "That subproblem is the same regardless of which parent invokes it. "
         "Caching gives us each answer for free after the first computation.", {}),
    ])),
    N.h3("Recurrence Relations"),
    N.code(
        "# Base case (day = 1):\n"
        "#   dp[1][j] = max(jobs[0..j])          # one day: do all first j+1 jobs\n"
        "\n"
        "# Transition (day > 1):\n"
        "#   dp[day][j] = min over k in [day-2 .. j-1] of:\n"
        "#                    dp[day-1][k]  +  max(jobs[k+1 .. j])\n"
        "#\n"
        "#   Optimisation: scan k right-to-left, maintain cur_max = max(jobs[k+1..j])\n"
        "#   in O(1) per step → total O(d · n²) instead of O(d · n³)\n"
        "\n"
        "# Answer: dp[d][n-1]\n"
        "# Guard:  if n < d: return -1\n"
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# SOLUTION 1 — Bottom-Up DP  (Interview Pick)
# ════════════════════════════════════════════════════════════════════════════
SOLN1_CODE = """\
def minDifficulty(jobDifficulty: list[int], d: int) -> int:
    n = len(jobDifficulty)
    if n < d:
        return -1                         # impossible: < 1 job per day
    INF = float('inf')

    # dp[day][j] = min cost to schedule jobs 0..j in exactly 'day' days
    dp = [[INF] * n for _ in range(d + 1)]

    # Base case: 1 day — do all jobs 0..j; cost = prefix maximum
    dp[1][0] = jobDifficulty[0]
    for j in range(1, n):
        dp[1][j] = max(dp[1][j - 1], jobDifficulty[j])

    # Fill days 2 .. d
    for day in range(2, d + 1):
        # j must be >= day-1 so each prior day has at least 1 job
        for j in range(day - 1, n):
            cur_max = 0               # rolling max of jobs[k+1 .. j]
            # k = last job of the PREVIOUS day; scan right-to-left
            for k in range(j - 1, day - 3, -1):
                cur_max = max(cur_max, jobDifficulty[k + 1])
                if dp[day - 1][k] < INF:
                    dp[day][j] = min(dp[day][j], dp[day - 1][k] + cur_max)

    return dp[d][n - 1] if dp[d][n - 1] < INF else -1
"""

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Because jobs must stay in order, every valid schedule is a partition of the "
            "job array into exactly d contiguous non-empty chunks. "
            "The question becomes: how do we choose d-1 cut points to minimize "
            "the sum of chunk-maxima?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force tries all C(n-1, d-1) cut placements — billions when n=300, d=10. "
            "A naive O(d·n³) DP recomputes range-max for every inner window from scratch. "
            "We need the rolling-max trick to reach O(d·n²)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For a fixed (day, j) cell we need: min over all valid k of "
            "[dp[day-1][k] + max(jobs[k+1..j])]. "
            "If we scan k from j-1 down to day-2, each step adds exactly one new job "
            "(job k+1) to today's window. "
            "We maintain cur_max = max(jobs[k+1..j]) incrementally in O(1). "
            "This collapses the inner-loop cost from O(n) to O(1)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialise dp[1][j] = prefix max (base case: 1 day, all jobs in one chunk). "
            "2. For each subsequent day, for each job j, scan k right-to-left, "
            "maintaining cur_max. "
            "3. Take the minimum over all valid cuts. "
            "4. Answer is dp[d][n-1]."
        ),
        N.callout(
            "Analogy: Think of the job array as a ribbon you must cut into exactly d pieces. "
            "Each piece charges you the height of its tallest stripe. "
            "Scanning right-to-left means you grow the current piece one stripe at a time, "
            "always knowing the tallest stripe without rescanning.",
            "🧠", "blue_background",
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive — dp[day][job] with Rolling Max"),
    N.para(
        "This belongs to the Partition DP family: split an ordered sequence into k groups "
        "and optimise a per-group aggregate. The canonical form is dp[groups][pos]. "
        "The rolling-max trick (or a monotonic stack for O(d·n)) reduces the naive "
        "O(d·n³) to O(d·n²). "
        "Recognise this pattern when you see: contiguous groups, per-group cost = max/min/sum, "
        "exactly k groups, ordered items."
    ),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("dp[day][j]", {"code": True}),
        (" always holds the minimum achievable total difficulty for the first ", {}),
        ("j+1", {"code": True}),
        (" jobs scheduled across exactly ", {}),
        ("day", {"code": True}),
        (" days, regardless of how those days are split.", {}),
    ])),
    N.para(N.rich([
        ("When to recognise it: ", {"bold": True}),
        ("'tasks/items must stay in order' + 'split into exactly k contiguous groups' + "
         "'each group's cost = max/min/sum' + 'minimise total cost'. "
         "Two free dimensions → 2D DP. Inner aggregator needs running variable, not re-scan.", {}),
    ])),
    N.h3("Code"),
    N.code(SOLN1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(jobDifficulty)", {"code": True}),
                   (" — total number of jobs.", {})])),
    N.para(N.rich([("if n < d: return -1", {"code": True}),
                   (" — guard: can't give every day at least one job if there are fewer jobs than days.", {})])),
    N.para(N.rich([("dp = [[INF]*n for _ in range(d+1)]", {"code": True}),
                   (" — 2D table of size (d+1) × n; INF marks unreachable states. "
                    "Row 0 is unused; rows 1..d represent day counts.", {})])),
    N.para(N.rich([("dp[1][0] = jobDifficulty[0]", {"code": True}),
                   (" — base: 1 day, 1 job; cost = that job's difficulty.", {})])),
    N.para(N.rich([("dp[1][j] = max(dp[1][j-1], jobDifficulty[j])", {"code": True}),
                   (" — base: 1 day, first j+1 jobs all done today; cost = running prefix max.", {})])),
    N.para(N.rich([("for day in range(2, d+1):", {"code": True}),
                   (" — outer loop over each additional day (2 through d).", {})])),
    N.para(N.rich([("for j in range(day-1, n):", {"code": True}),
                   (" — j must be ≥ day-1: we need at least one job per past day.", {})])),
    N.para(N.rich([("cur_max = 0", {"code": True}),
                   (" — reset the rolling maximum for today's window each time we move to a new j.", {})])),
    N.para(N.rich([("for k in range(j-1, day-3, -1):", {"code": True}),
                   (" — k is the index of the last job completed on day-1. "
                    "Scan right-to-left: k ranges from j-1 down to day-2 (need ≥1 job/prior day).", {})])),
    N.para(N.rich([("cur_max = max(cur_max, jobDifficulty[k+1])", {"code": True}),
                   (" — as k decreases by 1, job k+1 enters today's window. "
                    "Update rolling max in O(1).", {})])),
    N.para(N.rich([("dp[day][j] = min(dp[day][j], dp[day-1][k] + cur_max)", {"code": True}),
                   (" — try cutting after job k: prior days cost dp[day-1][k], today costs cur_max.", {})])),
    N.para(N.rich([("return dp[d][n-1]", {"code": True}),
                   (" — all n jobs scheduled in exactly d days.", {})])),
    N.callout(
        "Common mistake: the inner loop bound day-3 (exclusive lower bound for range) "
        "encodes k ≥ day-2, ensuring the previous day+1 days collectively have ≥ day-1 jobs. "
        "Off-by-one here gives wrong answers or index errors.",
        "⚠️", "yellow_background",
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# SOLUTION 2 — Top-Down Memoization
# ════════════════════════════════════════════════════════════════════════════
SOLN2_CODE = """\
from functools import lru_cache

def minDifficulty(jobDifficulty: list[int], d: int) -> int:
    n = len(jobDifficulty)
    if n < d:
        return -1

    @lru_cache(maxsize=None)
    def dp(days_left: int, start: int) -> int:
        # Base case: 1 day left → must do all remaining jobs
        if days_left == 1:
            return max(jobDifficulty[start:])
        res, cur_max = float('inf'), 0
        # Try ending today at each valid position 'end'
        # Must leave >= days_left-1 jobs for remaining days
        for end in range(start, n - days_left + 1):
            cur_max = max(cur_max, jobDifficulty[end])
            res = min(res, cur_max + dp(days_left - 1, end + 1))
        return res

    return dp(d, 0)
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Easier to Derive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Start directly from the English description: 'I have days_left days remaining "
            "and must schedule jobs starting from index start. What is the minimum cost?' "
            "This is a natural recursive function. Add @lru_cache and it's DP."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion recomputes the same (days_left, start) pairs from many parent states. "
            "The state space is only d × n = 300 × 300 = 90,000 entries — tiny. "
            "Memoize and the exponential becomes polynomial."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The base case is clean: if days_left == 1, we have no choice — "
            "do all remaining jobs in one day, cost = max(jobs[start:]). "
            "For days_left > 1, we choose where today ends (index 'end') "
            "and recurse on tomorrow. Scan end left-to-right, maintaining cur_max."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Decorate the recursive function with @lru_cache. "
            "For each call dp(days_left, start): "
            "iterate end from start to n-days_left (leave room for remaining days). "
            "Maintain running max of today's jobs. "
            "Recurse. Return the minimum cost found."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLN2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — Python's memoization decorator. Caches every unique "
                    "(days_left, start) pair; returns the cached result on repeat calls.", {})])),
    N.para(N.rich([("if days_left == 1: return max(jobDifficulty[start:])", {"code": True}),
                   (" — base case: last day must include all remaining jobs, "
                    "cost = their maximum.", {})])),
    N.para(N.rich([("for end in range(start, n - days_left + 1):", {"code": True}),
                   (" — today can end at any position from start up to n-days_left. "
                    "The upper bound ensures at least one job per remaining day.", {})])),
    N.para(N.rich([("cur_max = max(cur_max, jobDifficulty[end])", {"code": True}),
                   (" — extend today's window by one job; update running max O(1).", {})])),
    N.para(N.rich([("res = min(res, cur_max + dp(days_left-1, end+1))", {"code": True}),
                   (" — try cutting here: today costs cur_max; recurse for remaining days.", {})])),
    N.callout(
        "The memoization approach is easier to derive from the recurrence relation and "
        "is equally correct. For interviews, explain the memoization version to show "
        "DP reasoning, then mention the bottom-up version is preferred for O(1) stack space.",
        "⚠️", "yellow_background",
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# COMPLEXITY TABLE
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bottom-Up DP + rolling max", "O(d·n²)", "O(d·n)"],
        ["Top-Down Memoization",       "O(d·n²)", "O(d·n) + O(d) stack"],
        ["Space-optimised (2 rows)",   "O(d·n²)", "O(n)"],
        ["DP + Monotonic Stack",       "O(d·n)",  "O(d·n)"],
    ]),
    N.para(N.rich([
        ("Space optimisation: ", {"bold": True}),
        ("dp[day] depends only on dp[day-1]. Keep two 1D arrays (", {}),
        ("prev", {"code": True}),
        (" and ", {}),
        ("curr", {"code": True}),
        (") and alternate, reducing space from O(d·n) to O(n).", {}),
    ])),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# PATTERN CLASSIFICATION
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("dp[day][job] with Max  (Partition DP / Interval DP)", {})])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Tasks/items must stay in order' + 'split into exactly k contiguous groups'\n"
        "• 'Each group's cost = max (or min, or sum) of its elements'\n"
        "• 'Minimise (or maximise) total cost across all groups'\n"
        "• Two free dimensions (group count + position) → 2D DP table\n"
        "• Inner aggregation needs a running variable, not a full re-scan",
        "🔎", "green_background",
    ),
    N.para(N.rich([
        ("Source: ", {"bold": True}),
        ("DSA_Patterns_and_SubPatterns_Guide.md Section 18 — Dynamic Programming. "
         "Sub-pattern 'dp[day][job] with Max' is a specialisation of Partition DP / Interval DP.", {}),
    ])),
    N.divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# RELATED PROBLEMS
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same contiguous Partition DP / dp[day][job] technique:"),
    N.bullet(N.rich([
        ("Paint House III", {"bold": True}),
        (" (Hard, #1473) — dp[house][colour][neighbourhood_count]; "
         "contiguous same-colour grouping with 3 dimensions.", {}),
    ])),
    N.bullet(N.rich([
        ("Minimum Cost to Cut a Stick", {"bold": True}),
        (" (Hard, #1547) — Interval DP; cutting cost = length of current sub-stick.", {}),
    ])),
    N.bullet(N.rich([
        ("Strange Printer", {"bold": True}),
        (" (Hard, #664) — Interval DP on character runs; same merging structure.", {}),
    ])),
    N.bullet(N.rich([
        ("Burst Balloons", {"bold": True}),
        (" (Hard, #312) — Classic Interval DP, try every 'last balloon to burst'.", {}),
    ])),
    N.bullet(N.rich([
        ("Maximum Profit in Job Scheduling", {"bold": True}),
        (" (Hard, #1235) — DP + binary search; non-overlapping time-interval partition.", {}),
    ])),
    N.bullet(N.rich([
        ("Split Array Largest Sum", {"bold": True}),
        (" (Hard, #410) — Partition into k groups, minimise largest sum; "
         "same DP structure or binary-search-on-answer.", {}),
    ])),
    N.bullet(N.rich([
        ("Minimum Falling Path Sum", {"bold": True}),
        (" (Medium, #931) — Simpler 2D DP with row-to-row transitions.", {}),
    ])),
    N.para(
        "These problems share the core technique: "
        "state = (position, group-count) and value = optimal aggregation over a contiguous segment."
    ),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md "
        "Section 18 — Dynamic Programming, Partition DP / Interval DP sub-patterns.",
        "📚", "gray_background",
    ),
]

# ════════════════════════════════════════════════════════════════════════════
# EMBED
# ════════════════════════════════════════════════════════════════════════════
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the DP table filling visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── 4. Append everything ────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
