"""
run_max_points.py — wrapper that patches SSL then runs gen script
"""
import sys, os, ssl, urllib.request

# Patch urllib to use a default SSL context (fixes macOS Python 3.9 cert issue)
_orig_urlopen = urllib.request.urlopen
def _patched_urlopen(req, data=None, timeout=None, *, cafile=None, capath=None, cadefault=False, context=None):
    if context is None:
        context = ssl.create_default_context()
    return _orig_urlopen(req, data=data, timeout=timeout, context=context)
urllib.request.urlopen = _patched_urlopen

# Now import notion_lib with the patch in effect
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812c-b4ed-c5ae3ae90cf1"
SLUG = "maximum_number_of_points_with_cost"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1937,
    pattern="Dynamic Programming",
    subpatterns=["Optimize with Prefix Max"],
    tc="O(m·n)",
    sc="O(n)",
    key_insight="Split |j-k| into left/right prefix-max sweeps (O(n) each) to avoid O(n^2) DP transition.",
    icon="🟡",
    status="Solved",
    source="LeetCode",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m x n", {"bold": True}),
        (" integer matrix ", {}),
        ("points", {"code": True}),
        (", pick exactly one cell per row to maximize total score minus transition penalties. "
         "Consecutive picks at columns c_r and c_{r+1} cost |c_r - c_{r+1}|. "
         "Return the maximum achievable score.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — DP + Prefix-Max (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP + Prefix-Max Sweeps (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Select a path through the grid (one cell per row) to maximize total value minus transition penalties. "
               "The penalty |c_r - c_{r+1}| couples consecutive row decisions — you cannot optimize each row in isolation."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (pick max per row) ignores that a large cell in a far column imposes penalties on all future rows. "
               "Brute force is O(n^m). Naive DP: dp_new[j] = max_k(dp[k] - |j-k|) is O(n) per cell -> O(m*n^2) total. TLE for n=10^5."),
        N.h4("The Key Observation"),
        N.para("The penalty |j-k| splits into two linear cases: (j-k) when k <= j (left approach) and "
               "(k-j) when k >= j (right approach). Each is a running max decrementing by 1 per step — O(n) per pass."),
        N.h4("Building the Solution"),
        N.para("Base: dp[j] = points[0][j]. For each row: "
               "(1) left[j] = max(left[j-1]-1, dp[j]) sweeps left->right; "
               "(2) right[j] = max(right[j+1]-1, dp[j]) sweeps right->left; "
               "(3) dp_new[j] = points[r][j] + max(left[j], right[j]). "
               "Answer: max(dp)."),
        N.callout(
            "Analogy: left[j] is 'the best score I can arrive at column j carrying from the left, with all travel costs already paid.' "
            "Each step rightward eats one point. Two sweeps cover all directions in O(n).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def maxPoints(points: list[list[int]]) -> int:\n"
        "    m, n = len(points), len(points[0])\n"
        "    dp = points[0][:]               # base case: first row, no penalty\n"
        "    for r in range(1, m):\n"
        "        left = [0] * n\n"
        "        left[0] = dp[0]             # leftmost: no left predecessor\n"
        "        for j in range(1, n):\n"
        "            left[j] = max(left[j-1] - 1, dp[j])\n"
        "        right = [0] * n\n"
        "        right[n-1] = dp[n-1]        # rightmost: no right predecessor\n"
        "        for j in range(n-2, -1, -1):\n"
        "            right[j] = max(right[j+1] - 1, dp[j])\n"
        "        dp = [points[r][j] + max(left[j], right[j])\n"
        "              for j in range(n)]\n"
        "    return max(dp)",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = points[0][:]", {"code": True}),
                   (" — Base case: copy first row. No predecessor, no penalty.", {})])),
    N.para(N.rich([("left[0] = dp[0]", {"code": True}),
                   (" — Leftmost column has no left neighbor. Start left sweep here.", {})])),
    N.para(N.rich([("left[j] = max(left[j-1] - 1, dp[j])", {"code": True}),
                   (" — Extend left reach (pay 1 penalty) OR start fresh at j. Encodes max_{k<=j}(dp[k]-(j-k)).", {})])),
    N.para(N.rich([("right[n-1] = dp[n-1]", {"code": True}),
                   (" — Rightmost column: no right predecessor. Start right sweep here.", {})])),
    N.para(N.rich([("right[j] = max(right[j+1] - 1, dp[j])", {"code": True}),
                   (" — Symmetric right sweep: extend right reach (pay 1 penalty) OR start fresh at j. Encodes max_{k>=j}(dp[k]-(k-j)).", {})])),
    N.para(N.rich([("dp = [points[r][j] + max(left[j], right[j]) ...]", {"code": True}),
                   (" — New dp: current cell + best predecessor value (penalty embedded in left/right).", {})])),
    N.para(N.rich([("return max(dp)", {"code": True}),
                   (" — Best column in final row = global maximum score.", {})])),
    N.callout(
        "Why -1 per step? Moving one column rightward costs 1 unit of penalty. "
        "left[j] propagates the best value from the left while subtracting travel cost. "
        "Equivalent to computing max_k(dp[k]+k) - j for k<=j, but done in one O(n) pass.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (shows recurrence)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(r, j) = maximum total score ending at row r, column j. "
               "This directly encodes the subproblem."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes dp(r-1, k) for every (r,j) that considers k. Exponential."),
        N.h4("The Key Observation"),
        N.para("With lru_cache, each (r,j) state is computed once. "
               "Recurrence: dp(r,j) = points[r][j] + max_k(dp(r-1,k) - |j-k|). "
               "O(n) per state * O(m*n) states = O(m*n^2) total."),
        N.h4("Building the Solution"),
        N.para("Use Python's lru_cache. Base: dp(0,j) = points[0][j]. "
               "Recursive: try all k predecessors. Answer: max(dp(m-1,j) for j in range(n))."),
    ]),
    N.h3("Why This is DP — Two Pillars"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   ("Optimal path to (r,j) always uses optimal sub-path to some (r-1,k). "
                    "Substituting a better sub-path always improves overall result.", {})])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   ("Both dp(r,2) and dp(r,4) reference dp(r-1,1). Without memoization, dp(r-1,1) is recomputed once per j in row r.", {})])),
    N.code(
        "# Recurrence:\n"
        "dp(r, j) = points[0][j]                              # base case\n"
        "dp(r, j) = points[r][j] + max(dp(r-1,k) - abs(j-k)  # r > 0\n"
        "                             for k in range(n))\n"
        "answer   = max(dp(m-1, j) for j in range(n))",
        "python"
    ),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def maxPoints(points: list[list[int]]) -> int:\n"
        "    m, n = len(points), len(points[0])\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(r, j):\n"
        "        if r == 0:\n"
        "            return points[0][j]          # base case\n"
        "        best = max(\n"
        "            dp(r - 1, k) - abs(j - k)   # all predecessors — O(n)\n"
        "            for k in range(n)\n"
        "        )\n"
        "        return points[r][j] + best\n"
        "\n"
        "    return max(dp(m - 1, j) for j in range(n))",
        "python"
    ),
    N.callout(
        "IMPORTANT: Memoization is O(m*n^2) — TLE for large n. "
        "Use only to understand the recurrence. Submit Solution 1 (tabulation + prefix-max).",
        "🚨", "red_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n^m)", "O(m)", "Exponential — infeasible"],
        ["Memoization (top-down)", "O(m*n^2)", "O(m*n)", "Correct but TLE for large n"],
        ["Tabulation + Prefix Max", "O(m*n)", "O(n)", "Optimal — interview answer"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Optimize with Prefix Max — DP transition dp_new[j] = f(j) + max_k(dp[k] - |j-k|), "
                    "reducible from O(n^2) to O(n) per row using left+right prefix-max sweeps.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• DP transition involves max over previous states with linear penalty tied to position\n"
        "• Naive: O(n) per cell -> O(n^2) per row (check all previous states)\n"
        "• 'Absolute column/index difference' appears in a row-by-row DP context\n"
        "• Need O(n) space and O(m*n) time",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP + prefix-max / linear-penalty optimization:"),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}),
                     (" (Medium) — Max score jumping <=k steps; use monotonic deque for O(n) window max. (#1696)", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum", {"bold": True}),
                     (" (Medium) — Simpler version: adjacent column only, no prefix-max needed. (#931)", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum II", {"bold": True}),
                     (" (Hard) — Non-adjacent columns; optimize with two running minimums. (#1289)", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Cooldown", {"bold": True}),
                     (" (Medium) — State machine DP with coupled transitions between states. (#309)", {})])),
    N.bullet(N.rich([("Dice Roll Simulation", {"bold": True}),
                     (" (Hard) — Multi-state DP with range dependency; prefix-sum optimization. (#1223)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}),
                     (" (Hard) — Prefix-max via monotonic stack; avoids O(n^2) neighbor scan. (#84)", {})])),
    N.para("These problems share the core technique: reduce O(n^2) DP transitions to O(n) via prefix/suffix running maxima."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). "
        "Sub-Pattern: Optimize with Prefix Max. Source: Analysis.",
        "📚", "gray_background"
    ),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
