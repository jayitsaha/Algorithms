"""
gen_climbing_stairs.py — Rebuild the Notion page for Climbing Stairs (#70) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-812a-97fe-e7b99e94dd01"
SLUG    = "climbing_stairs"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=70,
    pattern="Dynamic Programming",
    subpatterns=["Same as Fibonacci"],
    tc="O(n)",
    sc="O(1)",
    key_insight="dp[i] = dp[i-1] + dp[i-2]; same recurrence as Fibonacci; use two rolling variables for O(1) space.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build new body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are climbing a staircase. It takes ", {}),
        ("n", {"code": True}),
        (" steps to reach the top. Each time you can climb ", {}),
        ("1", {"code": True}),
        (" or ", {}),
        ("2", {"code": True}),
        (" steps. In how many distinct ways can you climb to the top?", {}),
    ])),
    N.para(N.rich([("Constraints: 1 ≤ n ≤ 45.", {"italic": True, "color": "gray"})])),
    N.divider(),
]

# ── Solution 1: Bottom-Up Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation, O(1) Space (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count distinct sequences of moves (each move is +1 or +2 steps) that sum to n. The question is: in how many ways can I write n as an ordered sum of 1s and 2s?"),
        N.h4("What Doesn't Work"),
        N.para("A naive recursion — try all combinations — works but has O(2ⁿ) time. It recomputes the same sub-problems exponentially. For n=50 this is completely infeasible."),
        N.h4("The Key Observation"),
        N.para("You can ONLY arrive at step n from step n-1 (by taking 1 step) or from step n-2 (by taking 2 steps). These two sources are mutually exclusive and exhaustive. So: ways(n) = ways(n-1) + ways(n-2). This is the Fibonacci recurrence."),
        N.h4("Building the Solution"),
        N.para("Set base cases dp[1]=1, dp[2]=2. Fill forward: for i=3 to n, dp[i] = dp[i-1] + dp[i-2]. Since we only ever look back 2 steps, we can use two variables (prev, curr) instead of an O(n) array, giving O(1) space."),
        N.callout("Analogy: Every staircase route is a binary string of 1s and 2s summing to n. Counting such strings is exactly Fibonacci. climbStairs(n) = Fibonacci(n+1).", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def climbStairs(n: int) -> int:
    if n <= 2:
        return n          # dp[1]=1, dp[2]=2
    prev, curr = 1, 2     # prev=dp[i-2], curr=dp[i-1]
    for i in range(3, n + 1):
        prev, curr = curr, prev + curr  # roll window
    return curr           # curr = dp[n]"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if n <= 2: return n", {"code": True}), " — Direct base cases: dp[1]=1, dp[2]=2. Return immediately."])),
    N.para(N.rich([("prev, curr = 1, 2", {"code": True}), " — Initialize rolling window. prev holds dp[i-2], curr holds dp[i-1]."])),
    N.para(N.rich([("for i in range(3, n + 1):", {"code": True}), " — Fill dp[3] through dp[n] iteratively."])),
    N.para(N.rich([("prev, curr = curr, prev + curr", {"code": True}), " — Simultaneous assignment: right side evaluated first. prev ← old curr (=dp[i-1]); curr ← old prev + old curr (=dp[i])."])),
    N.para(N.rich([("return curr", {"code": True}), " — After loop, curr holds dp[n]. Return it."])),
    N.divider(),
]

# ── Solution 2: Top-Down Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Write the recurrence directly as a recursive function: dp(n) = dp(n-1) + dp(n-2), dp(1)=1, dp(2)=2."),
        N.h4("What Doesn't Work"),
        N.para("Bare recursion (no cache) recomputes dp(k) for the same k many times — O(2ⁿ) total work."),
        N.h4("The Key Observation"),
        N.para("Each unique sub-problem dp(i) is called multiple times but always returns the same value. Cache the first result and return it on subsequent calls."),
        N.h4("Building the Solution"),
        N.para("Add a memo dictionary. Before computing dp(i), check if it is already cached. If yes, return cache[i]. If no, compute it, store it, and return it. This reduces each unique call to O(1) work."),
        N.callout("Trade-off: memoization is easier to derive directly from the recurrence, but uses O(n) stack space. Tabulation (Solution 1) is marginally more efficient for large n.", "⚖️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def climbStairs(n: int) -> int:
    memo = {}
    def dp(i):
        if i <= 2:
            return i          # base cases
        if i in memo:
            return memo[i]    # cache hit
        memo[i] = dp(i-1) + dp(i-2)  # recurrence
        return memo[i]
    return dp(n)"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), " — Initialize empty cache mapping step → ways."])),
    N.para(N.rich([("if i <= 2: return i", {"code": True}), " — Base cases: dp(1)=1, dp(2)=2."])),
    N.para(N.rich([("if i in memo: return memo[i]", {"code": True}), " — Cache hit: avoid recomputing a sub-problem we've already solved."])),
    N.para(N.rich([("memo[i] = dp(i-1) + dp(i-2)", {"code": True}), " — Apply recurrence and cache the result before returning."])),
    N.divider(),
]

# ── Why is this DP? ──
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.h3("Optimal Substructure"),
    N.para("The optimal (exact) answer for step n depends entirely on the exact answers for steps n-1 and n-2. We do not need to re-examine how we reached those steps — just how many ways there are."),
    N.h3("Overlapping Subproblems"),
    N.para("A naive recursion computes dp(n-1) and dp(n-2), each of which calls dp(n-2) and dp(n-3), and so on. The same sub-problems are hit exponentially many times."),
    N.callout("Recurrence: dp[i] = dp[i-1] + dp[i-2]\nBase cases: dp[1] = 1, dp[2] = 2\nThis is the Fibonacci recurrence — climbStairs(n) = Fibonacci(n+1).", "📐", "blue_background"),
    N.h3("State Machine"),
    N.para("State: dp[i] = number of distinct ways to reach exactly step i. Transition: from step i-1 (take 1 step) → adds dp[i-1] paths; from step i-2 (take 2 steps) → adds dp[i-2] paths. These contributions are disjoint."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursion", "O(2ⁿ)", "O(n)"],
        ["Memoization (top-down)", "O(n)", "O(n)"],
        ["Tabulation, 2-var rolling (Interview Pick)", "O(n)", "O(1)"],
        ["Matrix Exponentiation", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Same as Fibonacci (Linear DP with rolling window)"])),
    N.callout(
        "When to recognize this pattern: 'How many distinct ways to reach X?' with a fixed small set of step sizes. "
        "Current state depends only on the last k states. No global weight or ordering — pure counting. "
        "Keywords: 'distinct ways', 'reach top', 'cover floor', 'decode string'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Fibonacci / Linear DP technique:"),
    N.bullet(N.rich([("Min Cost Climbing Stairs", {"bold": True}), " (Easy) — dp[i] = cost[i] + min(dp[i-1], dp[i-2]); minimize cost instead of count ways (#746)"])),
    N.bullet(N.rich([("Fibonacci Number", {"bold": True}), " (Easy) — Literally the same recurrence; climbStairs(n) = fib(n+1) (#509)"])),
    N.bullet(N.rich([("House Robber", {"bold": True}), " (Medium) — dp[i] = max(dp[i-2]+nums[i], dp[i-1]); same two-variable rolling window, maximize instead of count (#198)"])),
    N.bullet(N.rich([("Decode Ways", {"bold": True}), " (Medium) — Count valid decodings of a digit string; 1- or 2-digit chunks → Fibonacci variant (#91)"])),
    N.bullet(N.rich([("Tribonacci Number", {"bold": True}), " (Easy) — dp[i] = dp[i-1] + dp[i-2] + dp[i-3]; same idea with 3-step window (#1137)"])),
    N.bullet(N.rich([("Jump Game", {"bold": True}), " (Medium) — Reachability variant: can you reach the end? Greedy often wins but DP framing is identical (#55)"])),
    N.bullet(N.rich([("N-th Tribonacci Number", {"bold": True}), " (Easy) — Generalization of Fibonacci to three predecessors (#1137)"])),
    N.para("These problems share the same core technique: linear DP where dp[i] sums (or takes max/min of) a fixed number of preceding states."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), Sub-Pattern: Same as Fibonacci", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
