"""gen_soup_servings.py — Rebuild Notion page for Soup Servings (LeetCode 808)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8169-a2f2-ccd97cea66e9"

# ─────────────────────────── 1) Set properties ───────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=808,
    pattern="Dynamic Programming",
    subpatterns=["Memoize Probabilities"],
    tc="O(n²/625) ≈ O(1) after scaling",
    sc="O(n²/625) ≈ O(1) after scaling",
    key_insight="Scale n by 25 so state space ≤ 32×32; probability converges to 1.0 for n>4800.",
    icon="🟡",
)
print("Properties set.")

# ─────────────────────────── 2) Wipe old body ───────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ─────────────────────────── 3) Build new body ───────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are two types of soup: type A and type B. Initially we have ", {}),
        ("n", {"code": True}),
        (" ml of each type. There are four kinds of operations, each equally likely (25% each):\n"
         "1. Serve 100 ml of A and 0 ml of B\n"
         "2. Serve 75 ml of A and 25 ml of B\n"
         "3. Serve 50 ml of A and 50 ml of B\n"
         "4. Serve 25 ml of A and 75 ml of B\n\n"
         "If the remaining soup is not enough for an operation, we will serve as much as we can. "
         "We stop serving once at least one soup runs out. "
         "Return the probability that soup A will be empty first, plus half the probability that "
         "A and B become empty at the same time.", {}),
    ])),
    N.callout(
        N.rich([("Constraints: ", {"bold": True}), ("0 <= n <= 10^9", {"code": True})]),
        "📌", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Memoized Recursion (Interview Pick) ─────────────────────
blocks += [
    N.h2("Solution 1 — Memoized Recursion (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want P(A empties first) + 0.5 × P(A and B empty together). "
            "Model this as: at each step choose uniformly from 4 operations, then recurse "
            "on reduced (a, b) amounts. The answer is a probability sum over all terminal states."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive recursion without memoization: at each call we branch 4 ways, and since "
            "n can be up to 10^9 the recursion tree is astronomically deep. We would recompute "
            "the same (a, b) states millions of times."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two key observations make this tractable:\n"
            "1. SCALE: All serving amounts (100, 75, 50, 25 ml) are multiples of 25. "
            "Dividing n by 25 (rounding up) reduces the state space from n × n to ≤ n/25 × n/25.\n"
            "2. CONVERGENCE: For large enough n (>4800), soup A empties first with probability "
            "so close to 1.0 (≥ 1 - 1e-6) that we can return 1.0 immediately. "
            "After scaling, the state space is at most 192 × 192 cells — manageable."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Handle n > 4800 → return 1.0 (proven empirically / by calculation).\n"
            "Step 2: Scale: n = ceil(n / 25) → now n ≤ 192 and units are in 25-ml chunks.\n"
            "Step 3: Define dp(a, b) = probability of achieving our scoring condition from "
            "state (a, b) where a, b are remaining servings in 25-ml units.\n"
            "Step 4: Base cases:\n"
            "   - a ≤ 0 and b ≤ 0 → both empty simultaneously → return 0.5\n"
            "   - a ≤ 0 → A is first empty → return 1.0\n"
            "   - b ≤ 0 → B is first empty → return 0.0\n"
            "Step 5: Recurrence: dp(a,b) = 0.25 × [dp(a-4,b) + dp(a-3,b-1) + dp(a-2,b-2) + dp(a-1,b-3)]"
        ),
        N.callout(
            "Analogy: Think of each step as rolling a 4-sided die. "
            "Each face drains different amounts from A and B. "
            "Memoization ensures we only compute each 'remaining soup' state once.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("🔬 Algorithm Deep-Dive: Probability Memoization"),
    N.para(
        "This is a classic Probability DP problem (Guide Section 18.10). "
        "The key pattern is: define dp(state) = probability of a 'winning' terminal condition "
        "being reached from state, accumulate probability mass at each step weighted by transition probability."
    ),
    N.code(
        "# Probability DP Template\n"
        "from functools import lru_cache\n"
        "def dp(state):\n"
        "    if is_terminal(state): return score(state)\n"
        "    return sum(prob_i * dp(next_state_i) for each operation i)\n\n"
        "# Works because:\n"
        "# - Terminal states have known scores\n"
        "# - Each transition has fixed probability\n"
        "# - Expected value is linear: E[sum] = sum[E]\n"
        "# - Memoization prevents recomputation of overlapping subproblems"
    ),
    N.para(
        "Why it works (invariant): dp(a, b) always returns the EXACT expected 'score' "
        "(where score = 1 for A-first, 0.5 for simultaneous, 0 for B-first) reachable from "
        "state (a, b). This is well-defined because the recursion is finite (amounts strictly "
        "decrease each step) and terminal states have exact scores."
    ),

    N.h3("Code"),
    N.code(
        "import math\n"
        "from functools import lru_cache\n\n"
        "def soupServings(n: int) -> float:\n"
        "    # Large n: A always runs out first (within floating-point tolerance)\n"
        "    if n > 4800:\n"
        "        return 1.0\n\n"
        "    # Scale: all operations are multiples of 25 ml\n"
        "    # Divide by 25, rounding up — now units are 25-ml chunks\n"
        "    n = math.ceil(n / 25)\n\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(a, b):\n"
        "        # Base cases — terminal states\n"
        "        if a <= 0 and b <= 0: return 0.5   # simultaneous empty\n"
        "        if a <= 0:            return 1.0   # A empties first ✓\n"
        "        if b <= 0:            return 0.0   # B empties first ✗\n\n"
        "        # 4 equally likely operations (each 25%)\n"
        "        # Operation amounts in 25-ml units: (4,0), (3,1), (2,2), (1,3)\n"
        "        return 0.25 * (\n"
        "            dp(a - 4, b    ) +   # serve 100ml A, 0ml B\n"
        "            dp(a - 3, b - 1) +   # serve 75ml A,  25ml B\n"
        "            dp(a - 2, b - 2) +   # serve 50ml A,  50ml B\n"
        "            dp(a - 1, b - 3)     # serve 25ml A,  75ml B\n"
        "        )\n\n"
        "    return dp(n, n)"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([
        ("if n > 4800: return 1.0", {"code": True}),
        (" — Mathematical shortcut: for large n, A's bias (operations drain A more on average) makes P(A first) ≥ 1 - 1e-6.", {}),
    ])),
    N.para(N.rich([
        ("n = math.ceil(n / 25)", {"code": True}),
        (" — Scale down. All 4 operations use multiples of 25 ml, so we can work in 25-ml units. "
         "Ceiling ensures we don't undercount partial portions.", {}),
    ])),
    N.para(N.rich([
        ("@lru_cache(maxsize=None)", {"code": True}),
        (" — Python's built-in memoization decorator. Caches dp(a, b) results so each state is computed once.", {}),
    ])),
    N.para(N.rich([
        ("if a <= 0 and b <= 0: return 0.5", {"code": True}),
        (" — Both soups run out simultaneously → contributes 0.5 to our score (half credit).", {}),
    ])),
    N.para(N.rich([
        ("if a <= 0: return 1.0", {"code": True}),
        (" — A runs out first → full credit (1.0). Note: this check must come AFTER the simultaneous check.", {}),
    ])),
    N.para(N.rich([
        ("if b <= 0: return 0.0", {"code": True}),
        (" — B runs out first → no credit (0.0).", {}),
    ])),
    N.para(N.rich([
        ("return 0.25 * (dp(a-4, b) + dp(a-3, b-1) + dp(a-2, b-2) + dp(a-1, b-3))", {"code": True}),
        (" — Each of 4 operations has equal 25% probability. "
         "The recurrence averages dp values across all possible next states. "
         "Amounts are in 25-ml units: op1 drains 4 units A, op2 drains 3A+1B, etc.", {}),
    ])),

    N.divider(),
]

# ── Solution 2 — Bottom-Up DP (Tabulation) ────────────────────────────────
blocks += [
    N.h2("Solution 2 — Bottom-Up DP (Tabulation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Convert the recursive memoized approach to an iterative one. "
            "Build a 2D table dp[a][b] filled from base cases upward."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Filling from (0,0) upward is tricky because dp(a,b) depends on states with SMALLER "
            "a and b — so we need to handle base cases carefully and fill in increasing order of a+b."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Since dp(a, b) depends on dp(a-4,b), dp(a-3,b-1), dp(a-2,b-2), dp(a-1,b-3), "
            "all of which have strictly smaller 'total soup' (a+b), we can fill the table "
            "in order of increasing a and b. Treat any index ≤ 0 as a base case."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Allocate a (n+1) × (n+1) table. "
            "For each (a, b) from (1,1) to (n,n): look up the 4 predecessor states "
            "(clamping negative indices to their terminal base-case values). "
            "Sum with weight 0.25."
        ),
    ]),

    N.h3("Code"),
    N.code(
        "import math\n\n"
        "def soupServings(n: int) -> float:\n"
        "    if n > 4800:\n"
        "        return 1.0\n\n"
        "    n = math.ceil(n / 25)\n\n"
        "    # dp[a][b] = probability score from state (a units A, b units B)\n"
        "    dp = [[0.0] * (n + 1) for _ in range(n + 1)]\n\n"
        "    def get(a, b):\n"
        "        \"\"\"Return dp value, handling base cases for out-of-bounds.\"\"\"\n"
        "        if a <= 0 and b <= 0: return 0.5\n"
        "        if a <= 0:            return 1.0\n"
        "        if b <= 0:            return 0.0\n"
        "        return dp[a][b]\n\n"
        "    for a in range(1, n + 1):\n"
        "        for b in range(1, n + 1):\n"
        "            dp[a][b] = 0.25 * (\n"
        "                get(a - 4, b    ) +\n"
        "                get(a - 3, b - 1) +\n"
        "                get(a - 2, b - 2) +\n"
        "                get(a - 1, b - 3)\n"
        "            )\n\n"
        "    return dp[n][n]"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([
        ("dp = [[0.0] * (n+1) for _ in range(n+1)]", {"code": True}),
        (" — Initialize (n+1)×(n+1) table. dp[0][0] and index 0 act as boundaries.", {}),
    ])),
    N.para(N.rich([
        ("def get(a, b)", {"code": True}),
        (" — Helper to handle base cases when a or b goes below 1 (out of table bounds).", {}),
    ])),
    N.para(N.rich([
        ("for a in range(1, n+1): for b in range(1, n+1):", {"code": True}),
        (" — Fill in increasing order. Since all 4 predecessor states have smaller indices, "
         "they are already computed.", {}),
    ])),
    N.para(N.rich([
        ("dp[a][b] = 0.25 * (get(a-4,b) + get(a-3,b-1) + get(a-2,b-2) + get(a-1,b-3))", {"code": True}),
        (" — Same recurrence as memoized approach. get() handles boundary cases transparently.", {}),
    ])),
    N.para(N.rich([
        ("return dp[n][n]", {"code": True}),
        (" — Final answer: probability score starting from full (n, n) state.", {}),
    ])),

    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Memoized Recursion (Interview Pick)", "O(n²/625) ≈ O(1) post-scale", "O(n²/625) ≈ O(1) post-scale"],
        ["Bottom-Up DP (Tabulation)", "O(n²/625) ≈ O(1) post-scale", "O(n²/625) ≈ O(1) post-scale"],
    ]),
    N.callout(
        "After scaling n → ceil(n/25), both solutions work on a grid of at most 192×192 cells. "
        "This is effectively O(1) since n is bounded by the 4800 cutoff.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Memoize Probabilities (Guide Section 18.10 — Probability DP)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("• Operations have fixed probabilities (e.g., equal/uniform choices)\n"
             "• You want P(event) across a sequence of random operations\n"
             "• The state space is (resource_1, resource_2) and resources strictly decrease\n"
             "• Terminal states have known probability scores\n"
             "• Key shortcut: look for large-n convergence to skip computation", {}),
        ]),
        "🔎", "green_background"
    ),
    N.para(
        "Sub-pattern verified from DSA_Patterns_and_SubPatterns_Guide.md Section 18.10 "
        "(Probability DP — 'Memoize Probabilities' is the exact label in the guide)."
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Probability DP / Memoize Probabilities technique:"),
    N.bullet(N.rich([
        ("Knight Probability in Chessboard", {"bold": True}),
        (" (Medium) — dp[step][x][y] = probability of still being on board; same probability accumulation.", {}),
    ])),
    N.bullet(N.rich([
        ("New 21 Game", {"bold": True}),
        (" (Medium) — Sliding window to compute probability of reaching target score; probability DP with prefix sum optimization.", {}),
    ])),
    N.bullet(N.rich([
        ("Dota2 Senate", {"bold": True}),
        (" (Medium) — Probability/queue simulation of resource depletion.", {}),
    ])),
    N.bullet(N.rich([
        ("Dice Roll Simulation", {"bold": True}),
        (" (Hard) — Count valid dice sequences; DP over (position, last_face, consecutive_count).", {}),
    ])),
    N.bullet(N.rich([
        ("Profitable Schemes", {"bold": True}),
        (" (Hard) — 3D DP (members × profit); count combinations weighted by probability-like constraints.", {}),
    ])),
    N.bullet(N.rich([
        ("Probability of a Path in a Grid", {"bold": True}),
        (" (conceptual) — dp[i][j] = probability of reaching cell; same state-based probability accumulation.", {}),
    ])),
    N.para(
        "These problems share the core technique: "
        "define dp(state) = probability/expected-value reachable from state, "
        "memoize to avoid recomputing overlapping subproblems, and handle terminal states explicitly."
    ),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18.10 — Probability DP", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("soup_servings")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ─────────────────────────── 4) Append all blocks ────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
