"""
gen_maximum_number_of_points_with_cost.py
Notion in-place update for LeetCode #1937 — Maximum Number of Points with Cost
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812c-b4ed-c5ae3ae90cf1"
SLUG = "maximum_number_of_points_with_cost"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1937,
    pattern="Dynamic Programming",
    subpatterns=["Optimize with Prefix Max"],
    tc="O(m·n)",
    sc="O(n)",
    key_insight="Split |j−k| into left/right prefix-max sweeps (each O(n)) to avoid O(n²) DP transition.",
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
        ("m × n", {"bold": True}),
        (" integer matrix ", {}),
        ("points", {"code": True}),
        (", you must pick exactly one cell per row to maximize total points. "
         "Each consecutive pair of picks has a penalty equal to the absolute column difference. "
         "Formally, if you pick column ", {}),
        ("c_r", {"code": True}),
        (" in row ", {}),
        ("r", {"code": True}),
        (", your score is: Σ points[r][c_r] − Σ |c_r − c_{r+1}|. "
         "Return the maximum achievable score.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — DP + Prefix-Max (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP + Prefix-Max Sweeps (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're selecting a path through the grid, one cell per row, maximizing value minus transition penalties. "
               "The penalty |c_r − c_{r+1}| couples consecutive row decisions — you cannot optimize each row independently."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (pick the maximum cell each row) ignores that a large value in a far column may impose huge penalties "
               "on every subsequent row. Brute force over all n^m paths is exponential. Naive DP with transition "
               "dp_new[j] = max_k(dp[k] − |j−k|) is O(n) per cell → O(m·n²) total — TLE for n=10⁵."),
        N.h4("The Key Observation"),
        N.para("The penalty |j−k| splits into two linear cases: (j−k) when approaching from the left (k ≤ j), "
               "and (k−j) when approaching from the right (k ≥ j). Each case is a running max with a −1 decrement "
               "per step — computable in O(n) with a single pass. Two passes (left then right) cover both cases."),
        N.h4("Building the Solution"),
        N.para("1. Base: dp[j] = points[0][j] (first row, no penalty). "
               "2. For each row: left[j] = max(left[j−1]−1, dp[j]) sweeps left→right. "
               "right[j] = max(right[j+1]−1, dp[j]) sweeps right→left. "
               "3. dp_new[j] = points[r][j] + max(left[j], right[j]). "
               "4. After all rows, answer = max(dp)."),
        N.callout(
            "Analogy: Think of left[] as 'the best value I can reach column j from, traveling rightward — penalty already paid.' "
            "Each column step eats one point of budget (the −1). Two sweeps cover all directions.",
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
    N.para(N.rich([("dp = points[0][:]", {"code": True}), (" — Copy first row as base case. dp[j] = best total ending at col j of row 0. No penalty on first row.", {})])),
    N.para(N.rich([("for r in range(1, m)", {"code": True}), (" — Process each row after the first, updating dp in-place.", {})])),
    N.para(N.rich([("left[0] = dp[0]", {"code": True}), (" — Leftmost column: no left predecessor exists. left[0] = dp[0] directly.", {})])),
    N.para(N.rich([("left[j] = max(left[j-1] - 1, dp[j])", {"code": True}), (" — Either continue from left (pay 1 penalty per step) or start fresh at column j. Encodes max over all k≤j of (dp[k] − (j−k)).", {})])),
    N.para(N.rich([("right[n-1] = dp[n-1]", {"code": True}), (" — Rightmost column: no right predecessor. Symmetric to left.", {})])),
    N.para(N.rich([("right[j] = max(right[j+1] - 1, dp[j])", {"code": True}), (" — Symmetric right sweep. Encodes max over all k≥j of (dp[k] − (k−j)).", {})])),
    N.para(N.rich([("dp = [points[r][j] + max(left[j], right[j]) for j in range(n)]", {"code": True}), (" — New dp: add current cell value to best predecessor (penalty already baked into left/right).", {})])),
    N.para(N.rich([("return max(dp)", {"code": True}), (" — Best column in the last row = global maximum score.", {})])),
    N.callout(
        "Why −1 per step? Moving one column rightward costs 1 unit of penalty. left[j] propagates the best value "
        "from the left while continuously subtracting the travel cost. This is equivalent to computing "
        "max_k(dp[k] + k) − j for all k ≤ j, but done in one O(n) pass instead of O(n²).",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Memoization ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (shows recurrence clearly)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(r, j) = maximum total score for any path ending at row r, column j. "
               "This directly states the subproblem."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes dp(r−1, k) for every (r, j) pair that considers k "
               "as a predecessor — exponential work."),
        N.h4("The Key Observation"),
        N.para("With memoization, each (r, j) state is computed exactly once. The recurrence is: "
               "dp(r, j) = points[r][j] + max over k of (dp(r−1, k) − |j−k|). "
               "This is O(n) per state, O(m·n²) total — correct but too slow for n=10⁵."),
        N.h4("Building the Solution"),
        N.para("Use Python's lru_cache. Base case: dp(0, j) = points[0][j]. "
               "Recursive case: dp(r, j) = points[r][j] + max(dp(r−1, k) − |j−k| for k in range(n)). "
               "Final answer: max(dp(m−1, j) for j in range(n))."),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The optimal path to (r, j) always uses an optimal path to some (r−1, k). "
         "If the sub-path were suboptimal, we could substitute a better one and improve the overall result.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Both dp(r, 2) and dp(r, 4) consider dp(r−1, 1) as a predecessor. Without memoization, "
         "dp(r−1, 1) is recomputed for every different j in row r.", {})
    ])),
    N.code(
        "dp(r, j) = points[0][j]                                 # base case, r=0\n"
        "dp(r, j) = points[r][j] + max(dp(r-1, k) - |j-k|)     # recurrence, r>0\n"
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
        "            return points[0][j]          # base case: just the cell value\n"
        "        best = max(\n"
        "            dp(r - 1, k) - abs(j - k)   # all predecessors, O(n) per call\n"
        "            for k in range(n)\n"
        "        )\n"
        "        return points[r][j] + best\n"
        "\n"
        "    return max(dp(m - 1, j) for j in range(n))",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoize all (r, j) calls. Without this, exponential recursion.", {})])),
    N.para(N.rich([("if r == 0: return points[0][j]", {"code": True}), (" — Base case: first row, no predecessor, no penalty.", {})])),
    N.para(N.rich([("dp(r-1, k) - abs(j-k)", {"code": True}), (" — Score of best path ending at (r−1, k), minus transition penalty. Scan all k to find the best.", {})])),
    N.para(N.rich([("return points[r][j] + best", {"code": True}), (" — Add current cell's value to the best predecessor.", {})])),
    N.callout(
        "IMPORTANT: This solution is O(m·n²) — TLE for large inputs (n up to 10⁵). "
        "Use it only to understand the recurrence. For the actual submission, use Solution 1.",
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
        ["Memoization (top-down)", "O(m·n²)", "O(m·n)", "Correct but TLE for large n"],
        ["Tabulation + Prefix Max", "O(m·n)", "O(n)", "Optimal — interview answer"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Optimize with Prefix Max — used when DP transition is dp_new[j] = f(j) + max_k(dp[k] − |j−k|), reducible from O(n²) to O(n) per row via left+right sweeps.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• DP transition involves max over previous states with LINEAR penalty tied to position (absolute difference)\n"
        "• Naive version checks all previous states → O(n) per cell → O(n²) per row\n"
        "• The term 'absolute column/index difference' appears in a row-by-row DP context\n"
        "• You need O(n) space (not O(m·n)) and O(m·n) time",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related DP + prefix-max / linear-penalty optimization:"),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — Max score jumping ≤k steps in 1D; use monotonic deque for O(n) window max instead of left/right sweeps. (#1696)", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum", {"bold": True}), (" (Medium) — Simpler version: move only to adjacent column each row (no prefix-max needed, just check 3 neighbors). (#931)", {})])),
    N.bullet(N.rich([("Minimum Falling Path Sum II", {"bold": True}), (" (Hard) — Non-adjacent columns, minimize instead of maximize; optimize with two running minimums. (#1289)", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Cooldown", {"bold": True}), (" (Medium) — State machine DP where transitions have costs between states; conceptually similar coupling. (#309)", {})])),
    N.bullet(N.rich([("Dice Roll Simulation", {"bold": True}), (" (Hard) — Multi-state DP where each cell depends on a range of previous values; similar prefix-sum optimization. (#1223)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Prefix-max via monotonic stack; avoids O(n²) neighbor scan. Same spirit of linear-pass optimization. (#84)", {})])),
    N.para("These problems share the core technique: avoid O(n²) DP transitions by computing prefix/suffix running maxima in O(n) sweeps."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: Optimize with Prefix Max. Classification: Analysis (DP variant for linear-distance transitions — not explicitly listed in guide as a named sub-pattern).", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
