"""
gen_fibonacci_number.py
Notion IN-PLACE update for LeetCode #509 Fibonacci Number.
Run from the Algorithms/ directory alongside notion_lib.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-817b-9c54-d54e98003967"

# ── 1. Properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=509,
    pattern="Dynamic Programming",
    subpatterns=["Linear DP dp[i]=dp[i-1]+dp[i-2]"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Each F(n) depends only on F(n-1) and F(n-2) — slide two variables forward; no array needed.",
    icon="🟢"
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────
print("Building new content blocks...")

TABULATION_CODE = """\
def fib(n: int) -> int:
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr"""

DP_ARRAY_CODE = """\
def fib(n: int) -> int:
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]"""

MEMO_CODE = """\
def fib(n: int) -> int:
    memo = {}
    def dp(k):
        if k <= 1: return k
        if k in memo: return memo[k]
        memo[k] = dp(k-1) + dp(k-2)
        return memo[k]
    return dp(n)"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given ", ("n", {"code": True}),
        ", return ", ("F(n)", {"code": True}),
        " — the nth Fibonacci number, where ",
        ("F(0) = 0", {"code": True}), ", ",
        ("F(1) = 1", {"code": True}), ", and ",
        ("F(n) = F(n-1) + F(n-2)", {"code": True}),
        " for n ≥ 2. Constraints: 0 ≤ n ≤ 30."
    ])),
    N.divider(),
]

# ── Solution 1: Space-Optimized Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Space-Optimized Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to compute the nth term of a sequence defined by a recurrence. The sequence grows bottom-up: each value is completely determined by the two values before it."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion (return fib(n-1) + fib(n-2)) is correct but O(2ⁿ) — it recomputes fib(3) when evaluating both fib(5) and fib(4), and fib(2) even more times. For n=40, that's over a billion calls."),
        N.h4("The Key Observation"),
        N.para("Computing F(i) only ever needs F(i-1) and F(i-2). We don't need to remember anything older. Instead of a whole array or a recursion tree, just keep two variables — prev and curr — and slide them forward one step at a time."),
        N.h4("Building the Solution"),
        N.para("Initialize prev=F(0)=0 and curr=F(1)=1. Each iteration: compute next = prev+curr, then shift: prev←curr, curr←next. After n-1 iterations, curr = F(n). Use Python's simultaneous assignment to avoid the sequential-update bug."),
        N.callout("Analogy: Think of a 2-element sliding window moving rightward across the infinite Fibonacci tape. We only ever peek at the two cells behind us.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def fib(n: int) -> int:", {"code": True}), " — function signature; n is an integer in [0, 30]"])),
    N.para(N.rich([("if n <= 1: return n", {"code": True}), " — handles both base cases: F(0)=0 and F(1)=1 in one check; returns n directly"])),
    N.para(N.rich([("prev, curr = 0, 1", {"code": True}), " — initialize the rolling window: prev = F(0) = 0, curr = F(1) = 1"])),
    N.para(N.rich([("for _ in range(2, n + 1):", {"code": True}), " — iterate for i = 2, 3, ..., n (that's n-1 iterations total)"])),
    N.para(N.rich([("prev, curr = curr, prev + curr", {"code": True}), " — simultaneous assignment: evaluate right side using OLD values, then assign; this computes F(i) as prev+curr and slides the window forward"])),
    N.para(N.rich([("return curr", {"code": True}), " — after the loop, curr holds F(n); return it"])),
    N.callout("Why simultaneous assignment? If you write prev=curr then curr=prev+curr, the second line uses the already-overwritten prev. The tuple swap evaluates both right-hand sides first — so prev+curr uses the old prev. This is the canonical way to write Fibonacci in Python.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Full DP Array ──
blocks += [
    N.h2("Solution 2 — Full Tabulation Array (O(n) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of two rolling variables, allocate a full dp array of size n+1 and fill it left-to-right. This makes the recurrence relationship visually explicit."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct and easier to reason about, but uses O(n) space unnecessarily since we only ever read dp[i-1] and dp[i-2] to compute dp[i]."),
        N.h4("The Key Observation"),
        N.para("This is the 'gateway' DP solution — it directly mirrors the recurrence table. It's great for explanation and debugging, and can always be space-optimized afterward."),
        N.h4("Building the Solution"),
        N.para("Allocate dp[0..n]. Set base cases dp[0]=0, dp[1]=1. Fill: for i in 2..n: dp[i] = dp[i-1] + dp[i-2]. Return dp[n]."),
    ]),
    N.h3("Code"),
    N.code(DP_ARRAY_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * (n + 1)", {"code": True}), " — allocate array of zeros for indices 0 through n"])),
    N.para(N.rich([("dp[0], dp[1] = 0, 1", {"code": True}), " — seed the two base cases explicitly"])),
    N.para(N.rich([("dp[i] = dp[i-1] + dp[i-2]", {"code": True}), " — recurrence: look up two already-computed cells and sum them"])),
    N.para(N.rich([("return dp[n]", {"code": True}), " — the answer is stored at the last index"])),
    N.divider(),
]

# ── Solution 3: Memoization ──
blocks += [
    N.h2("Solution 3 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with the recursive definition directly — fib(n) = fib(n-1) + fib(n-2) — but add a cache. This is the most natural translation of the mathematical definition into code."),
        N.h4("What Doesn't Work (Without Memoization)"),
        N.para("Pure recursion recomputes fib(k) exponentially many times. For n=50, the naive tree has about 2^50 ≈ 10^15 nodes — completely impractical."),
        N.h4("The Key Observation"),
        N.para("Each fib(k) for k in 0..n is computed at most once. After the first computation we store it in memo[k] and return in O(1) for all future calls. The call tree becomes a linear chain."),
        N.h4("Building the Solution"),
        N.para("Wrap the recursion in a helper with a memo dict. Before recursing, check: if k in memo, return memo[k]. After computing, store: memo[k] = dp(k-1) + dp(k-2). Return memo[k]."),
        N.callout("Python shortcut: @lru_cache(None) or @cache above the function definition replaces the manual memo dict entirely — cleaner and Pythonic.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), " — cache mapping k → F(k), shared across all recursive calls"])),
    N.para(N.rich([("if k <= 1: return k", {"code": True}), " — base cases: dp(0)=0, dp(1)=1"])),
    N.para(N.rich([("if k in memo: return memo[k]", {"code": True}), " — cache hit: return stored result in O(1), skipping the entire sub-tree"])),
    N.para(N.rich([("memo[k] = dp(k-1) + dp(k-2)", {"code": True}), " — compute and store before returning; ensures each value computed exactly once"])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursion", "O(2ⁿ)", "O(n) stack"],
        ["Memoization (Top-Down)", "O(n)", "O(n)"],
        ["DP Array (Bottom-Up)", "O(n)", "O(n)"],
        ["Two Variables ✓ (Interview Pick)", "O(n)", "O(1)"],
        ["Matrix Exponentiation", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Why is This DP? ──
blocks += [
    N.h2("🔍 Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}), "F(n) is completely determined by F(n-1) and F(n-2). The optimal answer to the big problem is built exactly from optimal answers to smaller sub-problems."])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}), "Computing F(n) naively causes exponential recomputation. F(3) is called once when computing F(5) via the F(4) branch, and again directly from F(5). Memoization or tabulation ensures each value is computed exactly once."])),
    N.code("F(0) = 0          # base case\nF(1) = 1          # base case\nF(n) = F(n-1) + F(n-2)   # recurrence (n >= 2)", lang="python"),
    N.callout("When you see a problem whose definition is recursive and whose sub-calls repeat (overlap), that is the signature of a DP problem. Fibonacci is the purest example.", "🔑", "blue_background"),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Linear DP · dp[i] = dp[i-1] + dp[i-2] — fixed-width look-back recurrence"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem definition is explicitly recursive with 1-2 step look-back\n"
        "• 'Count ways to reach state i from i-1 or i-2'\n"
        "• 'Maximize/minimize using last 1 or 2 decisions'\n"
        "• Sequence where each term is built from a fixed number of previous terms",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Linear DP sub-pattern:"),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}), " (Easy) — ways(n) = ways(n-1) + ways(n-2). Fibonacci in disguise. #70"])),
    N.bullet(N.rich([("House Robber", {"bold": True}), " (Medium) — dp[i] = max(dp[i-1], dp[i-2]+nums[i]). Same 2-step look-back, richer decision. #198"])),
    N.bullet(N.rich([("Min Cost Climbing Stairs", {"bold": True}), " (Easy) — dp[i] = cost[i] + min(dp[i-1], dp[i-2]). Fibonacci with per-step cost. #746"])),
    N.bullet(N.rich([("Tribonacci Number", {"bold": True}), " (Easy) — T(n) = T(n-1)+T(n-2)+T(n-3). Extend to 3 rolling variables. #1137"])),
    N.bullet(N.rich([("Delete and Earn", {"bold": True}), " (Medium) — Reduce to House Robber on a frequency array; same linear DP. #740"])),
    N.bullet(N.rich([("Count Ways to Build Good Strings", {"bold": True}), " (Medium) — Generalized Fibonacci with variable step sizes. #2466"])),
    N.para("These problems share the same core technique: a fixed look-back recurrence where each state depends on the previous 1, 2, or k states."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → Linear DP)\nSub-Pattern verified: Linear DP dp[i]=dp[i-1]+dp[i-2]", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("fibonacci_number")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append in chunks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
