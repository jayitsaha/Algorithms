"""
gen_maximum_profit_in_job_scheduling.py
Rebuild the Notion page for LeetCode #1235 - Maximum Profit in Job Scheduling
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# Override token (notion_lib.py was redacted; token is still valid)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-8127-856e-ee3d29fa1c17"
SLUG = "maximum_profit_in_job_scheduling"

# ─── Step 1: Set page properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1235,
    pattern="Dynamic Programming",
    subpatterns=["DP + Binary Search"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by end time; dp[i] = max(skip, dp[bisect_right(ends, start)] + profit).",
    icon="🔴",
)
print("Properties set.")

# ─── Step 2: Wipe the old body ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─── Step 3: Build the body blocks ────────────────────────────────────────────
blocks = []

# ── Problem Statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given ", {}),
        ("n", {"code": True}),
        (" jobs, where the ", {}),
        ("i", {"code": True}),
        ("-th job has start time ", {}),
        ("startTime[i]", {"code": True}),
        (", end time ", {}),
        ("endTime[i]", {"code": True}),
        (", and profit ", {}),
        ("profit[i]", {"code": True}),
        (". You want to find the maximum profit you can earn from scheduling non-overlapping jobs. "
         "Two jobs overlap if one starts before the other ends. A job that ends at time ", {}),
        ("t", {"code": True}),
        (" and another starting at time ", {}),
        ("t", {"code": True}),
        (" do NOT overlap.", {}),
    ])),
    N.callout(
        N.rich([
            ("Key Insight: ", {"bold": True}),
            ("Sort jobs by end time. Define dp[i] = max profit using first i sorted jobs. "
             "For each job: skip it (dp[i-1]) or take it (dp[j] + profit, where j = last compatible job found via binary search). "
             "This is Weighted Interval Scheduling — greedy fails, DP + binary search is optimal.", {}),
        ]),
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Solution 1: Tabulation + Binary Search
sol1_code = """\
from bisect import bisect_right

def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    # Sort by end time — essential for DP ordering
    jobs = sorted(zip(endTime, startTime, profit))
    ends = [j[0] for j in jobs]          # sorted end-times for binary search
    dp = [0] * (len(jobs) + 1)           # dp[i] = best profit from first i sorted jobs

    for i, (end, start, prof) in enumerate(jobs, 1):   # 1-indexed
        # Binary search: how many jobs end <= start of this job?
        j = bisect_right(ends, start)    # j = index = count of compatible jobs
        take = dp[j] + prof              # profit if we take this job
        skip = dp[i - 1]                 # profit if we skip this job
        dp[i] = max(take, skip)

    return dp[len(jobs)]
"""

blocks += [
    N.h2("Solution 1 — Tabulation + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to pick a non-overlapping subset of jobs maximizing total profit. "
               "This is Weighted Interval Scheduling — the 'with weights' version of maximum non-overlapping intervals."),
        N.h4("What Doesn't Work"),
        N.para("Greedy by highest profit may block many smaller profitable jobs. Greedy by earliest end time ignores profits. "
               "Neither greedy criterion always works when jobs have different values. A single high-value job can destroy an "
               "otherwise perfect combination of medium-value jobs."),
        N.h4("The Key Observation"),
        N.para("Sort jobs by end time. Then define dp[i] = max profit from first i sorted jobs. "
               "For each new job we have exactly two choices: skip it (carry forward dp[i-1]) or take it "
               "(add its profit to the best we could earn from all jobs finishing before it starts). "
               "We need to find 'last compatible job' efficiently — that's binary search on the sorted end-times."),
        N.h4("Building the Solution"),
        N.para("1. Sort by end time. 2. Initialize dp[0]=0. 3. For each job i: "
               "j = bisect_right(ends, start_i) gives count of jobs with end ≤ start_i. "
               "dp[j] = best profit from compatible jobs. dp[i] = max(dp[j]+profit_i, dp[i-1]). "
               "4. Answer = dp[n]. Each step O(log n) via binary search → O(n log n) total."),
        N.callout(
            "Analogy: Think of yourself as a freelancer scanning job postings sorted by deadline. "
            "For each new job, you instantly check 'what's the most I earned from jobs finishing before this one starts?' "
            "Then decide: take this new gig or stick with what I had?",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The optimal solution for n jobs either uses or skips job n. "
         "If it skips job n: answer = dp[n-1]. If it takes job n: answer = dp[last_compat(n)] + profit[n]. "
         "So dp[n] = max(dp[n-1], dp[last_compat(n)] + profit[n]). This is a valid optimal decomposition.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive solution would recompute dp[j] many times — every later job finding j as compatible "
         "would trigger redundant work. Tabulation computes each dp[i] exactly once.", {}),
    ])),
    N.code("""\
# Recurrence Relations
dp[0] = 0                                           # base case: no jobs
dp[i] = max(dp[i-1],                                # skip job i
            dp[last_compat(i)] + profit[i])         # take job i

where: last_compat(i) = bisect_right(ends, start[i])
       = number of sorted jobs with end time <= start of job i
       = the index j such that dp[j] = best profit from all jobs finishing before job i starts
"""),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("jobs = sorted(zip(endTime, startTime, profit))", {"code": True}),
                   (" — Zip the three arrays together, then sort by end time (first element of each tuple). "
                    "Putting end time first in the tuple makes sort() order by end time automatically.", {})])),
    N.para(N.rich([("ends = [j[0] for j in jobs]", {"code": True}),
                   (" — Extract just the end times into a separate sorted list. "
                    "This is the array we'll binary-search over at each step.", {})])),
    N.para(N.rich([("dp = [0] * (len(jobs) + 1)", {"code": True}),
                   (" — 1-indexed DP array. dp[0]=0 (base case). dp[i] = best profit from first i sorted jobs.", {})])),
    N.para(N.rich([("for i, (end, start, prof) in enumerate(jobs, 1):", {"code": True}),
                   (" — Iterate over sorted jobs. enumerate(..., 1) gives 1-based index i.", {})])),
    N.para(N.rich([("j = bisect_right(ends, start)", {"code": True}),
                   (" — Binary search: returns count of elements in ends[] that are ≤ start. "
                    "Since ends[] is sorted, this is O(log n). j is the count of jobs finishing before this job starts.", {})])),
    N.para(N.rich([("take = dp[j] + prof", {"code": True}),
                   (" — If we take this job: profit = best from compatible jobs (dp[j]) + this job's profit.", {})])),
    N.para(N.rich([("skip = dp[i - 1]", {"code": True}),
                   (" — If we skip: carry forward the best from previous i-1 jobs.", {})])),
    N.para(N.rich([("dp[i] = max(take, skip)", {"code": True}),
                   (" — Optimal substructure: take whichever option is more profitable.", {})])),
    N.para(N.rich([("return dp[len(jobs)]", {"code": True}),
                   (" — dp[n] holds the maximum profit achievable over all n jobs.", {})])),
    N.callout(
        "bisect_right vs bisect_left: Use bisect_right so that a job ending at t and one starting at t "
        "are treated as non-overlapping (end ≤ start is legal). bisect_left would wrongly exclude those boundary-touching jobs.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization (Top-Down)
sol2_code = """\
from bisect import bisect_left
from functools import lru_cache

def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    # Sort by start time for the top-down approach
    jobs = sorted(zip(startTime, endTime, profit))
    starts = [j[0] for j in jobs]

    @lru_cache(maxsize=None)
    def dp(i):
        # dp(i) = max profit from jobs[i..n-1]
        if i == len(jobs):
            return 0                                # base case: no more jobs
        # Option 1: skip job i
        skip = dp(i + 1)
        # Option 2: take job i — next compatible job starts >= end of job i
        next_j = bisect_left(starts, jobs[i][1])   # first job starting >= end_i
        take = jobs[i][2] + dp(next_j)
        return max(skip, take)

    return dp(0)
"""

blocks += [
    N.h2("Solution 2 — Memoization (Top-Down)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem, but now we define dp(i) = max profit from job i through end. "
               "We recurse forward, making skip/take decisions at each job."),
        N.h4("What Doesn't Work"),
        N.para("Without caching, pure recursion repeats work exponentially — dp(j) is called by every "
               "job i that finds j as its next compatible index."),
        N.h4("The Key Observation"),
        N.para("Sort by start time. For each job i: skip (recurse to dp(i+1)) or take (add profit, "
               "jump to first job starting >= end_i via bisect_left). Memoize with lru_cache."),
        N.h4("Building the Solution"),
        N.para("The top-down approach naturally follows the problem structure: at each position, decide "
               "greedily via memoized subproblems. Same O(n log n) complexity as tabulation."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("jobs = sorted(zip(startTime, endTime, profit))", {"code": True}),
                   (" — Sort by start time (not end time) for the top-down forward sweep.", {})])),
    N.para(N.rich([("def dp(i):", {"code": True}),
                   (" — Recursive function: returns max profit from jobs[i..n-1].", {})])),
    N.para(N.rich([("if i == len(jobs): return 0", {"code": True}),
                   (" — Base case: past the last job = zero profit.", {})])),
    N.para(N.rich([("next_j = bisect_left(starts, jobs[i][1])", {"code": True}),
                   (" — Find first job starting >= end of job i. bisect_left on start times gives the "
                    "first index where job i's end time fits.", {})])),
    N.para(N.rich([("return max(skip, take)", {"code": True}),
                   (" — Same optimal substructure: max of skip or take.", {})])),
    N.callout(
        "Note: Top-down sorts by start time and uses bisect_left on starts[]. "
        "Bottom-up sorts by end time and uses bisect_right on ends[]. "
        "Both give O(n log n). The tabulation approach (Solution 1) is slightly simpler to implement and avoids recursion stack overhead.",
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (2^n subsets)", "O(2^n · n)", "O(n)", "Only n ≤ 20"],
        ["DP + O(n) scan", "O(n²)", "O(n)", "Correct, too slow for large n"],
        ["Memoization + bisect", "O(n log n)", "O(n + stack)", "Top-down; elegant"],
        ["Tabulation + bisect_right", "O(n log n)", "O(n)", "Bottom-up; interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP + Binary Search", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Problems involving intervals with weights/profits where you must select a non-overlapping subset to maximize total value. "
             "Keywords: 'schedule', 'maximize profit', 'non-overlapping', 'weighted intervals'. "
             "The 'take or skip' structure combined with the need to find the 'last compatible' element efficiently signals DP + binary search.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Weighted Interval Scheduling / DP + Binary Search):"),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}),
                     (" (Medium) — Minimize intervals to remove; pure greedy (no profits). #435", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}),
                     (" (Medium) — Minimum meeting rooms; greedy + heap, not weighted DP. #253", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}),
                     (" (Medium) — Same skip/take DP template with positional (not temporal) constraints. #198", {})])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}),
                     (" (Medium) — Interval coverage; greedy by end time. #452", {})])),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}),
                     (" (Hard) — 2D sort + LIS via binary search; same Sort+DP+BS template. #354", {})])),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}),
                     (" (Medium) — Patience sorting: DP + binary search reduces O(n^2) to O(n log n). #300", {})])),
    N.bullet(N.rich([("Partition Array for Maximum Sum", {"bold": True}),
                     (" (Medium) — Interval DP; pick subarrays to maximize sum. #1043", {})])),
    N.para("These problems share the core technique: sort on a key dimension, define a DP over that ordering, "
           "and use binary search to jump to the 'last relevant' index in O(log n)."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 Dynamic Programming, Sub-Pattern: DP + Binary Search",
              "📚", "gray_background"),
]

# ── Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
