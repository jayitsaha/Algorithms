"""
gen_minimum_difficulty_of_a_job_schedule.py
Notion IN-PLACE update for LeetCode #1335: Minimum Difficulty of a Job Schedule
Run from the Algorithms directory: python3 gen_minimum_difficulty_of_a_job_schedule.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_curl as N

PAGE_ID = "39193418-809c-81bb-9c3d-e6178a91ff32"
SLUG = "minimum_difficulty_of_a_job_schedule"

# ── 1. Set properties ─────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1335,
    pattern="Dynamic Programming",
    subpatterns=["dp[day][job] with Max"],
    tc="O(d·n²)",
    sc="O(d·n)",
    key_insight="Partition jobs into d contiguous groups; dp[day][j] = min cost via recurrence + right-to-left running max.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You want to schedule a list of jobs in "), ("d", {"code": True}),
        (" days. Jobs must be done in the given order, and each day must have at least one job. "
         "The difficulty of a day is the "), ("maximum", {"bold": True}),
         (" difficulty among its jobs. Return the minimum total difficulty across all days, "
          "or -1 if it is not possible.")
    ])),
    N.para(N.rich([
        ("Constraint: "), ("jobDifficulty", {"code": True}), (" lengths must satisfy "),
        ("n >= d", {"code": True}), (" (otherwise impossible).")
    ])),
    N.divider()
]

# ── SOLUTION 1 — Bottom-Up DP ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Because jobs must stay in order, every valid schedule partitions the job array into exactly d contiguous non-empty chunks. The question becomes: how do we optimally split an array into d groups to minimize the sum of group-maxima?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force enumerates all C(n-1, d-1) splits — billions for n=300, d=10. Even a smarter recursion without memoization revisits the same subproblems exponentially."),
        N.h4("The Key Observation"),
        N.para("Two DP pillars hold: (1) Optimal substructure — the best cost for jobs 0..j in day days builds from the best cost for jobs 0..k in day-1 days, for any valid cut k. (2) Overlapping subproblems — many parent states ask 'best cost for 0..k in 2 days?' Memoize it once."),
        N.h4("Building the Solution"),
        N.para("Define dp[day][j] = min total difficulty to schedule jobs 0..j in exactly day days. Base case: dp[1][j] = max(jobs[0..j]) (one day, do all). Recurrence: dp[day][j] = min over k of (dp[day-1][k] + max(jobs[k+1..j])). Scan k right-to-left to maintain max in O(1) per step."),
        N.callout(
            "Analogy: Think of the jobs as a ribbon you must cut into exactly d pieces. Each cut costs the height of the tallest point in that piece. Scanning right-to-left lets you track the 'tallest point' as the piece grows, without restarting.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Why is This DP?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("dp[day][j] is built optimally from dp[day-1][k] for all valid k. The best suffix schedule is independent of how the prefix was arranged.\n"),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("The same (day, start_job) pair is queried from many different parent states. Memoizing avoids exponential recomputation.")
    ])),
    N.h3("Recurrence Relations"),
    N.code_block(
        "dp[1][j] = max(jobs[0 .. j])     # base: 1 day, all first j+1 jobs\n"
        "\n"
        "dp[day][j] = min over k in [day-2 .. j-1] of:\n"
        "                 dp[day-1][k] + max(jobs[k+1 .. j])\n"
        "\n"
        "Answer: dp[d][n-1]\n"
        "Guard:  if n < d: return -1\n"
        "\n"
        "# Key optimization: scan k right-to-left, maintain cur_max = max(jobs[k+1..j])\n"
        "# as window grows: O(1) per k step -> O(d*n^2) total instead of O(d*n^3)",
        "python"
    ),
    N.h3("Code"),
    N.code_block(
        "def minDifficulty(jobDifficulty: list[int], d: int) -> int:\n"
        "    n = len(jobDifficulty)\n"
        "    if n < d:\n"
        "        return -1\n"
        "    INF = float('inf')\n"
        "    # dp[day][j] = min cost to schedule jobs 0..j in exactly 'day' days\n"
        "    dp = [[INF] * n for _ in range(d + 1)]\n"
        "    # Base case: 1 day -- all jobs 0..j done, cost = prefix max\n"
        "    dp[1][0] = jobDifficulty[0]\n"
        "    for j in range(1, n):\n"
        "        dp[1][j] = max(dp[1][j - 1], jobDifficulty[j])\n"
        "    # Fill days 2..d\n"
        "    for day in range(2, d + 1):\n"
        "        for j in range(day - 1, n):   # j >= day-1: need 1 job per prior day\n"
        "            cur_max = 0               # max(jobs[k+1..j]) as window grows\n"
        "            for k in range(j - 1, day - 3, -1):  # k from j-1 down to day-2\n"
        "                cur_max = max(cur_max, jobDifficulty[k + 1])\n"
        "                if dp[day - 1][k] < INF:\n"
        "                    dp[day][j] = min(dp[day][j], dp[day - 1][k] + cur_max)\n"
        "    return dp[d][n - 1] if dp[d][n - 1] < INF else -1",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(jobDifficulty)", {"code": True}), (" — total number of jobs.")])),
    N.para(N.rich([("if n < d: return -1", {"code": True}), (" — impossible to give each day ≥1 job.")])),
    N.para(N.rich([("dp = [[INF]*n for _ in range(d+1)]", {"code": True}), (" — 2D table, all initialized to infinity (unreachable).")])),
    N.para(N.rich([("dp[1][0] = jobDifficulty[0]", {"code": True}), (" — base case: 1 day, 1 job, cost = that job's difficulty.")])),
    N.para(N.rich([("dp[1][j] = max(dp[1][j-1], jobDifficulty[j])", {"code": True}), (" — build prefix max for day=1 in a single left-to-right pass.")])),
    N.para(N.rich([("for day in range(2, d+1):", {"code": True}), (" — iterate over each subsequent day.")])),
    N.para(N.rich([("for j in range(day-1, n):", {"code": True}), (" — j must be ≥ day-1 so each prior day has ≥1 job.")])),
    N.para(N.rich([("cur_max = 0", {"code": True}), (" — reset the running maximum for today's window.")])),
    N.para(N.rich([("for k in range(j-1, day-3, -1):", {"code": True}), (" — scan cut-point k right-to-left: day−2 ≤ k ≤ j−1.")])),
    N.para(N.rich([("cur_max = max(cur_max, jobDifficulty[k+1])", {"code": True}), (" — job k+1 enters today's window; update running max O(1).")])),
    N.para(N.rich([("dp[day][j] = min(dp[day][j], dp[day-1][k] + cur_max)", {"code": True}), (" — try this cut; keep the best.")])),
    N.para(N.rich([("return dp[d][n-1]", {"code": True}), (" — final answer: all jobs scheduled in exactly d days.")])),
    N.divider()
]

# ── SOLUTION 2 — Memoization ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Easier to Derive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start from the recursive definition: 'What is the min cost if I have days_left days remaining and must schedule starting from job start?' This maps directly to a recursive function."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes the same (days_left, start) pairs exponentially. The state space is only d×n, so memoization is trivial."),
        N.h4("The Key Observation"),
        N.para("The base case is clean: if days_left == 1, we must do all remaining jobs in one day, so cost = max(jobs[start:]). For days_left > 1, try ending today at each valid position 'end'."),
        N.h4("Building the Solution"),
        N.para("Use @lru_cache. For each (days_left, start) pair, try all positions 'end' for today's last job. Maintain a running max left-to-right as end increases. Recurse on (days_left-1, end+1)."),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def minDifficulty(jobDifficulty: list[int], d: int) -> int:\n"
        "    n = len(jobDifficulty)\n"
        "    if n < d:\n"
        "        return -1\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(days_left: int, start: int) -> int:\n"
        "        # Base case: 1 day left, must do all remaining jobs\n"
        "        if days_left == 1:\n"
        "            return max(jobDifficulty[start:])\n"
        "        res, cur_max = float('inf'), 0\n"
        "        # Try ending today at each valid position\n"
        "        # Leave at least (days_left - 1) jobs for remaining days\n"
        "        for end in range(start, n - days_left + 1):\n"
        "            cur_max = max(cur_max, jobDifficulty[end])\n"
        "            res = min(res, cur_max + dp(days_left - 1, end + 1))\n"
        "        return res\n"
        "\n"
        "    return dp(d, 0)",
        "python"
    ),
    N.callout(
        "Warning: The memoization approach is easier to write from the recurrence, but the bottom-up version avoids recursion overhead and is easier to space-optimize. In interviews, explain both; implement bottom-up.",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bottom-Up DP + running max", "O(d·n²)", "O(d·n)"],
        ["Top-Down Memoization", "O(d·n²)", "O(d·n) memo + O(d) stack"],
        ["Space-optimized (2 rows)", "O(d·n²)", "O(n)"],
        ["DP + Monotonic Stack (advanced)", "O(d·n)", "O(d·n)"],
    ]),
    N.divider()
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("dp[day][job] with Max")])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Tasks/items must be processed in order' + 'split into exactly k groups'\n"
        "• 'Each group's cost = max (or min, or sum) of its elements'\n"
        "• 'Minimize total cost across all groups'\n"
        "• Two free dimensions (day index + job index) → 2D DP table\n"
        "• Inner loop requires an aggregator (max/min) → use running aggregate, not re-scan",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (contiguous partition DP with aggregator):"),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), (" (Hard) — Interval DP, try every 'last balloon to burst'; O(n³) (#312)")])),
    N.bullet(N.rich([("Maximum Profit in Job Scheduling", {"bold": True}), (" (Hard) — DP + binary search on non-overlapping time intervals (#1235)")])),
    N.bullet(N.rich([("Paint House III", {"bold": True}), (" (Hard) — dp[house][color][neighborhood_count]; contiguous same-color grouping (#1473)")])),
    N.bullet(N.rich([("Minimum Cost to Cut a Stick", {"bold": True}), (" (Hard) — Interval DP; cutting cost = length of current sub-stick (#1547)")])),
    N.bullet(N.rich([("Strange Printer", {"bold": True}), (" (Hard) — Interval DP on character runs; same aggregation structure (#664)")])),
    N.bullet(N.rich([("Minimum Falling Path Sum", {"bold": True}), (" (Medium) — Simple 2D DP with row-to-row transitions (#931)")])),
    N.bullet(N.rich([("Triangle", {"bold": True}), (" (Medium) — Bottom-up 2D DP; choose minimum path downward (#120)")])),
    N.para("These problems share the core technique: state = (position, group-count) and value = optimal aggregation over a contiguous segment."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18.5 (2D Grid / Multi-Day Dynamic Programming)\nSub-Pattern: dp[day][job] with Max · Source: Guide Section 18.5", "📖", "gray_background")
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
