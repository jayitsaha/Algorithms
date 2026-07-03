"""
gen_minimum_number_of_work_sessions_to_finish_the_tasks.py
Notion page builder for LeetCode #1986 – Minimum Number of Work Sessions to Finish the Tasks
Pattern: Dynamic Programming > Bitmask DP Sessions and Time
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39293418-809c-81b7-affe-d96cc5885ff4"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1986,
    pattern="Dynamic Programming",
    subpatterns=["Bitmask DP Sessions and Time"],
    tc="O(2^n * n)",
    sc="O(2^n)",
    key_insight="Encode which tasks are done as a bitmask; for each state, greedily pack tasks into the current session, counting a new session only when the current overflows.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Build the body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given ", {}),
        ("n", {"code": True}),
        (" tasks labeled ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("n-1", {"code": True}),
        (" where ", {}),
        ("tasks[i]", {"code": True}),
        (" is the amount of time needed to finish the ", {}),
        ("i", {"code": True}),
        ("-th task. You can work for ", {}),
        ("sessionTime", {"code": True}),
        (" hours in each work session. Once you start a task, you must finish it in the same session. "
         "You may start a new session at any time. Return the minimum number of work sessions to finish all the tasks, "
         "assuming you choose optimally to work on tasks.", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 <= n <= 14", {"code": True}),
        (", ", {}),
        ("1 <= sessionTime <= 15", {"code": True}),
        (", ", {}),
        ("1 <= tasks[i] <= sessionTime", {"code": True}),
        (". Note: n ≤ 14 is a strong hint toward bitmask DP — 2^14 = 16 384 states.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Bitmask DP (Interview Pick) ───────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bitmask DP Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have n ≤ 14 tasks. We must assign every task to a session (a 'bin') where the total time in each bin ≤ sessionTime. We want to minimize the number of bins. This is essentially a variant of Bin Packing — NP-hard in general, but tractable here because n ≤ 14 lets us enumerate all 2^n subsets."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (fill each session as full as possible) fails because early choices can block better packings later. Plain recursion without memoization is O(n! × 2^n) — exponential in the worst sense. We need a smarter state representation."),
        N.h4("The Key Observation"),
        N.para("Since n ≤ 14, every possible subset of tasks can be represented as a bitmask (integer 0..2^n-1). The bit at position i is 1 if task i is done, 0 if not. With this encoding, the full state of 'which tasks are done' is a single integer — perfect for DP. The recurrence: to compute dp[mask] = minimum sessions to finish the tasks in mask, we try adding one more task at a time, packing greedily within each session."),
        N.h4("Building the Solution"),
        N.para("Key insight: when building dp[mask], we greedily find the 'current session load' by scanning a sub-mask of mask — summing tasks in that sub-mask until we exceed sessionTime. The number of complete sessions used is dp[mask without the sub-mask bits] + 1. We take the minimum over all valid sub-masks. Alternatively (the cleaner recurrence): dp[0] = 0. For each mask, pick the lowest unset bit i (the 'next task to schedule'), then try adding task i to an existing partially-filled session — track current session time in the state — or start a new session."),
        N.callout(
            "Analogy: Think of the bitmask as a 14-bit 'TO-DO checklist'. dp[mask] = fewest sessions to check off exactly the items that are checked in mask. We build from empty checklist (dp[0]=0) up to all-checked (dp[(1<<n)-1]).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Bitmask DP"),
    N.para(N.rich([
        ("Bitmask DP", {"bold": True}),
        (" (also called subset DP) is the canonical technique when:", {}),
    ])),
    N.bullet("The number of elements n is small (≤ 20, typically ≤ 14)."),
    N.bullet("The state of the problem can be described by 'which elements have been processed'."),
    N.bullet("We need to optimize over all assignments/permutations of elements to groups."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("dp[mask]", {"code": True}),
        (" = the minimum number of work sessions to finish all tasks in ", {}),
        ("mask", {"code": True}),
        (" optimally. The transition adds one task (bit) at a time and either packs it into the current partial session or opens a new one.", {}),
    ])),
    N.para(N.rich([
        ("Recognise when: ", {"bold": True}),
        ("n ≤ 14–20, 'assign items to groups', 'minimize groups', 'all subsets', 'subset sum'. The 2^n state space is the tell.", {}),
    ])),
    N.h3("Code"),
    N.code("""\
from functools import lru_cache

class Solution:
    def minSessions(self, tasks: list[int], sessionTime: int) -> int:
        n = len(tasks)
        FULL = (1 << n) - 1  # bitmask with all tasks done

        # dp[mask] = (min_sessions, current_session_remaining_time)
        # We iterate over all masks in increasing order.
        # State: (sessions_used, time_left_in_current_session)
        # Use BFS/DP with state = (mask, time_left).

        INF = float('inf')
        # dp[mask] = min sessions to finish tasks in mask
        # time_left[mask] = time remaining in the last session at optimal dp[mask]
        dp = [INF] * (1 << n)
        rest = [0] * (1 << n)  # remaining time in current session at state mask
        dp[0] = 0
        rest[0] = sessionTime  # no tasks done; current session is fully empty

        for mask in range(1, 1 << n):
            for i in range(n):
                if not (mask >> i & 1):
                    continue  # task i not in this mask, skip
                prev = mask ^ (1 << i)  # mask with task i removed
                if dp[prev] == INF:
                    continue
                # Option A: fit task i into the current partial session
                if rest[prev] >= tasks[i]:
                    if dp[prev] < dp[mask] or (dp[prev] == dp[mask] and rest[prev] - tasks[i] > rest[mask]):
                        dp[mask] = dp[prev]
                        rest[mask] = rest[prev] - tasks[i]
                # Option B: start a new session for task i
                new_sessions = dp[prev] + 1
                new_rest = sessionTime - tasks[i]
                if new_sessions < dp[mask] or (new_sessions == dp[mask] and new_rest > rest[mask]):
                    dp[mask] = new_sessions
                    rest[mask] = new_rest

        return dp[FULL]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("FULL = (1 << n) - 1", {"code": True}), (" — Bitmask where every bit is 1 = all n tasks are done. This is our goal state.", {})])),
    N.para(N.rich([("dp = [INF] * (1 << n)", {"code": True}), (" — For each of the 2^n subsets, store the minimum sessions needed. Initialize to infinity (unreachable).", {})])),
    N.para(N.rich([("rest = [0] * (1 << n)", {"code": True}), (" — For each subset state, store the remaining time in the 'current partial session' when we reach that state optimally. Tracking this avoids needing another dimension in the DP.", {})])),
    N.para(N.rich([("dp[0] = 0; rest[0] = sessionTime", {"code": True}), (" — Base case: no tasks done, 0 sessions used, and the current session is completely empty (sessionTime hours available).", {})])),
    N.para(N.rich([("for mask in range(1, 1 << n):", {"code": True}), (" — Iterate over all non-empty subsets in increasing bit order. Smaller masks are always computed before larger ones, ensuring the recurrence is correct.", {})])),
    N.para(N.rich([("for i in range(n): if not (mask >> i & 1): continue", {"code": True}), (" — Only consider tasks that ARE in this mask. We try removing each one to find which predecessor state led to mask.", {})])),
    N.para(N.rich([("prev = mask ^ (1 << i)", {"code": True}), (" — The predecessor state: mask minus task i. XOR with the i-th bit toggles it off.", {})])),
    N.para(N.rich([("if rest[prev] >= tasks[i]:", {"code": True}), (" — Option A: can we fit task i into the current partial session without starting a new one? If yes, do it (same session count, but less time remains).", {})])),
    N.para(N.rich([("new_sessions = dp[prev] + 1", {"code": True}), (" — Option B: start a new session just for task i. Cost increases by 1.", {})])),
    N.para(N.rich([("return dp[FULL]", {"code": True}), (" — Answer: minimum sessions to finish ALL tasks (the all-ones mask).", {})])),
    N.divider(),
]

# ── Solution 2 — Top-Down Memoization ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same bitmask idea, but we express it recursively: dp(mask, time_left) = minimum additional sessions to finish the tasks NOT yet in mask, given that the current session has time_left hours remaining."),
        N.h4("What Doesn't Work"),
        N.para("Without memoization this is still exponential — the same (mask, time_left) combination appears repeatedly in the recursion tree."),
        N.h4("The Key Observation"),
        N.para("The state is (remaining_tasks_mask, time_remaining_in_current_session). There are 2^n × sessionTime possible states, each computed once. For n=14 and sessionTime=15 that's 16384 × 15 ≈ 245K states — fast."),
        N.h4("Building the Solution"),
        N.para("Base case: mask == 0 → all tasks done → return 0. For each unscheduled task i (bit i is set in remaining), try adding it to the current session (if time allows) or starting a new session. Take the minimum."),
        N.callout("Top-down is often easier to derive first in an interview — write the recursion naturally, add @lru_cache, done. Then mention the bottom-up approach as the space-optimisable version.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""\
from functools import lru_cache

class Solution:
    def minSessions(self, tasks: list[int], sessionTime: int) -> int:
        n = len(tasks)

        @lru_cache(maxsize=None)
        def dp(mask: int, time_left: int) -> int:
            \"\"\"Min extra sessions to finish tasks in `mask`, with `time_left`
            remaining in the current session.\"\"\"
            if mask == 0:
                return 0  # all tasks done
            best = float('inf')
            for i in range(n):
                if not (mask >> i & 1):
                    continue  # task i already done (bit is 0)
                task_time = tasks[i]
                remaining = mask ^ (1 << i)  # mark task i as done
                if time_left >= task_time:
                    # Fit into current session (no new session cost)
                    best = min(best, dp(remaining, time_left - task_time))
                else:
                    # Must start a new session (+1 cost)
                    best = min(best, 1 + dp(remaining, sessionTime - task_time))
            return best

        # Start: all tasks pending, one session already open (cost 0)
        # The +1 for the very first session is counted by the caller.
        # Actually we count sessions opened: first call already has 1 session.
        return 1 + dp((1 << n) - 1, sessionTime)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Python's built-in memoization decorator. Caches every (mask, time_left) pair automatically.", {})])),
    N.para(N.rich([("def dp(mask, time_left)", {"code": True}), (" — mask encodes which tasks STILL NEED to be done (bit 1 = pending, bit 0 = done). time_left is the free time remaining in the current session.", {})])),
    N.para(N.rich([("if mask == 0: return 0", {"code": True}), (" — All tasks finished. No more sessions needed.", {})])),
    N.para(N.rich([("if time_left >= task_time:", {"code": True}), (" — Fit task i into the current session. We don't add 1 because no new session is opened.", {})])),
    N.para(N.rich([("1 + dp(remaining, sessionTime - task_time)", {"code": True}), (" — Open a new session (cost +1). The new session starts with sessionTime minus the time consumed by task i.", {})])),
    N.para(N.rich([("return 1 + dp((1 << n) - 1, sessionTime)", {"code": True}), (" — The outer +1 accounts for the very first session we open at the start. All task bits set = all tasks pending.", {})])),
    N.divider(),
]

# ── Solution 3 — Brute Force DFS ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force DFS (Conceptual Starting Point)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every permutation of tasks; greedily assign them to sessions in order. Keep a counter of how many sessions we've opened."),
        N.h4("What Doesn't Work"),
        N.para("For n=14 there are 14! ≈ 87 billion permutations. This is completely intractable. Pruning helps but not enough. This approach is for building intuition only."),
        N.h4("The Key Observation"),
        N.para("Two orderings that assign the same SUBSET of tasks to the same sessions are equivalent. This is the insight that leads to bitmask DP — we care about which tasks are grouped, not their order."),
    ]),
    N.h3("Code"),
    N.code("""\
class Solution:
    def minSessions(self, tasks: list[int], sessionTime: int) -> int:
        n = len(tasks)
        self.ans = n  # worst case: one session per task

        def dfs(i: int, sessions: list[int]):
            if i == n:
                self.ans = min(self.ans, len(sessions))
                return
            seen = set()
            for j, s in enumerate(sessions):
                if s in seen:
                    continue  # prune symmetric branches
                seen.add(s)
                if s + tasks[i] <= sessionTime:
                    sessions[j] += tasks[i]
                    dfs(i + 1, sessions)
                    sessions[j] -= tasks[i]
            # Start a new session
            sessions.append(tasks[i])
            dfs(i + 1, sessions)
            sessions.pop()

        tasks.sort(reverse=True)  # prune: try large tasks first
        dfs(0, [])
        return self.ans
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("tasks.sort(reverse=True)", {"code": True}), (" — Pruning heuristic: assigning large tasks first fills sessions tighter and cuts branches earlier.", {})])),
    N.para(N.rich([("seen = set()", {"code": True}), (" — If two sessions have the same remaining capacity, we don't need to try both — they're symmetric. Prune by session capacity value.", {})])),
    N.para(N.rich([("sessions.append(tasks[i]); dfs(i+1, sessions); sessions.pop()", {"code": True}), (" — Try opening a new session for task i (backtracking).", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bitmask DP Bottom-Up", "O(2^n × n)", "O(2^n)"],
        ["Bitmask DP Top-Down", "O(2^n × n × sessionTime)", "O(2^n × sessionTime)"],
        ["Brute Force DFS", "O(n! / pruning)", "O(n)"],
    ]),
    N.callout(
        "Bottom-up bitmask DP is the interview pick. For n=14: 2^14 × 14 = ~230K operations — extremely fast. "
        "Top-down with the (mask, time_left) state is also acceptable but uses more memory.",
        "⚡", "yellow_background"
    ),
    N.divider(),
]

# ── Why is this DP? ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.h3("Optimal Substructure"),
    N.para(
        "The optimal assignment for a subset of tasks (mask) can be built from the optimal assignment for any "
        "sub-subset (mask minus one task). Adding one more task either fits into the current partial session "
        "or triggers a new one — both are computed from already-solved sub-problems."
    ),
    N.h3("Overlapping Subproblems"),
    N.para(
        "Many different orderings of tasks lead to the same 'which tasks remain' state. Without memoization, "
        "a naive recursion recomputes the same (mask, time_left) state exponentially many times. "
        "Memoization reduces this to O(2^n × n × sessionTime) unique states."
    ),
    N.h3("Recurrence Relation"),
    N.code("""\
# Bottom-up recurrence:
# dp[mask] = min sessions to finish tasks in mask
# rest[mask] = time remaining in current (partial) session at that optimal state

# For each task i in mask (bit i is 1):
#   prev = mask ^ (1 << i)
#   Option A (same session):  dp[prev],     rest[prev] - tasks[i]   (if rest[prev] >= tasks[i])
#   Option B (new session):   dp[prev] + 1, sessionTime - tasks[i]
# Take the option that minimizes dp[mask]; break ties by maximizing rest[mask].
""", "python"),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bitmask DP Sessions and Time", {})])),
    N.callout(
        "When to recognize this pattern: n ≤ 14–20 items that must be ASSIGNED to groups/bins. "
        "The problem asks to minimize groups (or sessions, buckets, trips). "
        "Constraints say 'tasks[i] ≤ sessionTime'. "
        "The key tell: 2^n is manageable (n ≤ 20 → 1M states). "
        "Bitmask DP turns 'which items are done' into a single integer — the state key.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Bitmask DP):"),
    N.bullet(N.rich([("Travelling Salesman Problem / Shortest Path Visiting All Nodes", {"bold": True}), (" (Hard) — Classic bitmask DP: dp[mask][city] = min cost to visit cities in mask ending at city.", {})])),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets", {"bold": True}), (" (Medium) — Assign numbers to k buckets; bitmask encodes which numbers are used.", {})])),
    N.bullet(N.rich([("Campus Bikes II", {"bold": True}), (" (Hard) — Assign workers to bikes (bitmask over bikes); minimize total distance.", {})])),
    N.bullet(N.rich([("Fair Distribution of Cookies", {"bold": True}), (" (Medium) — Distribute cookie bags to k children; bitmask DP or DFS with pruning.", {})])),
    N.bullet(N.rich([("Minimum Number of Work Sessions (this problem)", {"bold": True}), (" (Medium) — Bin packing with sessionTime limit; 2^n × n bitmask DP.", {})])),
    N.bullet(N.rich([("Stickers to Spell Word", {"bold": True}), (" (Hard) — Bitmask DP over target characters; dp[mask] = min stickers to cover characters in mask.", {})])),
    N.bullet(N.rich([("Maximum AND Sum of Array", {"bold": True}), (" (Hard) — Assign n numbers to slots (bitmask DP over slots).", {})])),
    N.para("These problems all share the same bitmask DP structure: encode 'which items are handled' as a subset bitmask, build dp from empty set to full set."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) > DP: Bitmask. Sub-Pattern: Bitmask DP Sessions and Time.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_number_of_work_sessions_to_finish_the_tasks")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
