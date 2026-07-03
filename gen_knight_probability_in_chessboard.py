"""gen_knight_probability_in_chessboard.py — Notion updater for #688."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a5-aa86-d0aea96a42eb"

# ── 1. Set properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=688,
    pattern="Dynamic Programming",
    subpatterns=["dp[step][x][y] = probability"],
    tc="O(k·n²)",
    sc="O(n²)",
    key_insight="Track probability distribution dp[r][c] across board cells; spread /8 each step — off-board prob is lost; sum after k steps is the answer.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe existing body ────────────────────────────────────────────
print("Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ── 3. Build new body ────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("On an ", {}),
        ("n×n", {"code": True}),
        (" chessboard, a knight starts at position ", {}),
        ("(row, col)", {"code": True}),
        (" and makes exactly ", {}),
        ("k", {"code": True}),
        (" moves. At each move the knight picks one of up to 8 L-shape destinations uniformly at random (probability 1/8 each). If a move would land off the board, that path ends. Return the probability that the knight remains on the board after exactly ", {}),
        ("k", {"code": True}),
        (" moves.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Bottom-Up DP ────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the probability that a random sequence of k knight moves stays on the board. The naive view is: enumerate all 8^k move sequences and count valid ones. That is exponential. The DP insight is: instead of tracking paths, track a probability distribution — how much probability is \"at\" each cell after each step."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force DFS: recurse over all 8 choices at each step for k steps. Total nodes = 8^k (≈ 10^9 for k=10). Also, the subproblem 'what is the probability of being at cell (r,c) after m moves?' gets recomputed along every path that reaches it — classic overlapping subproblems."),
        N.h4("The Key Observation"),
        N.para("Probability is conserved. Start with total probability 1.0 at the start cell. At each step, spread each cell's probability equally to its valid knight destinations (÷8 per move). Probability that falls off the board is lost forever. After k steps, the sum of all remaining probability is exactly the answer — no path counting needed."),
        N.h4("Building the Solution"),
        N.para("State: dp[r][c] = probability of being at (r,c) after current step. Base: dp[row][col] = 1.0. Transition: for each (r,c) with dp[r][c] > 0, add dp[r][c]/8 to next_dp[nr][nc] for each valid knight destination. After k iterations, sum the entire grid."),
        N.callout("Analogy: Imagine pouring 1 cup of water at the start cell. At each step, each cell redistributes its water equally to its valid knight neighbors (losing the fraction that falls off the board). After k pours, the total remaining water is the probability.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def knightProbability(n: int, k: int, row: int, col: int) -> float:
    MOVES = [(-2,-1),(-2,1),(-1,-2),(-1,2),
             (1,-2),(1,2),(2,-1),(2,1)]
    dp = [[0.0]*n for _ in range(n)]
    dp[row][col] = 1.0
    for _ in range(k):
        ndp = [[0.0]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if dp[r][c] == 0:
                    continue
                for dr, dc in MOVES:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        ndp[nr][nc] += dp[r][c] / 8
        dp = ndp
    return sum(dp[r][c] for r in range(n) for c in range(n))"""),
    N.h3("Line by Line"),
    N.para(N.rich([("MOVES", {"code": True}), " — lists all 8 L-shape (dr, dc) deltas a knight can make from any position."])),
    N.para(N.rich([("dp = [[0.0]*n ...]", {"code": True}), " — n×n grid of floating-point probabilities, initially all zero."])),
    N.para(N.rich([("dp[row][col] = 1.0", {"code": True}), " — base case: the knight is certainly at the start position before any moves."])),
    N.para(N.rich([("for _ in range(k)", {"code": True}), " — repeat the spreading process exactly k times, once per move."])),
    N.para(N.rich([("ndp = [[0.0]*n ...]", {"code": True}), " — fresh output grid for this step. MUST be separate from dp to avoid using already-updated values as sources."])),
    N.para(N.rich([("if dp[r][c] == 0: continue", {"code": True}), " — skip zero-probability cells; they contribute nothing (optimization)."])),
    N.para(N.rich([("for dr, dc in MOVES", {"code": True}), " — try all 8 possible knight moves from cell (r, c)."])),
    N.para(N.rich([("if 0 <= nr < n and 0 <= nc < n", {"code": True}), " — bounds check: only valid (in-bounds) destinations receive probability. Off-board probability is silently discarded."])),
    N.para(N.rich([("ndp[nr][nc] += dp[r][c] / 8", {"code": True}), " — each of the 8 moves is equally likely (prob 1/8), so we spread 1/8 of the current cell's probability."])),
    N.para(N.rich([("dp = ndp", {"code": True}), " — advance state. The old dp is discarded; only O(n²) space is needed at any time."])),
    N.para(N.rich([("return sum(...)", {"code": True}), " — total remaining probability in the grid = probability of staying on the board for all k moves."])),
    N.divider(),
]

# ── Solution 2 — Memoization ──────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(moves, r, c) = probability that a knight at (r, c) with 'moves' remaining stays on the board for all remaining moves. This is a natural recursive formulation."),
        N.h4("What Doesn't Work"),
        N.para("Without memoization, the same (moves, r, c) triple gets recomputed along every path that reaches it — exponential work."),
        N.h4("The Key Observation"),
        N.para("Base cases: if (r, c) is off-board → 0.0. If moves == 0 → 1.0 (still on board, no moves left). Recursion: average the 8 children. With lru_cache, each of the O(k·n²) states is computed once."),
        N.h4("Building the Solution"),
        N.para("The recurrence dp(moves, r, c) = Σ dp(moves-1, r+dr, c+dc) / 8 follows directly from the uniform random choice interpretation."),
    ]),
    N.h3("Code"),
    N.code("""from functools import lru_cache

def knightProbability(n: int, k: int, row: int, col: int) -> float:
    MOVES = [(-2,-1),(-2,1),(-1,-2),(-1,2),
             (1,-2),(1,2),(2,-1),(2,1)]

    @lru_cache(maxsize=None)
    def dp(moves: int, r: int, c: int) -> float:
        # Off-board: this path is a failure
        if not (0 <= r < n and 0 <= c < n):
            return 0.0
        # No moves left and still on board: success
        if moves == 0:
            return 1.0
        # Average probability over all 8 moves
        return sum(dp(moves - 1, r + dr, c + dc)
                   for dr, dc in MOVES) / 8

    return dp(k, row, col)"""),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache", {"code": True}), " — memoizes on the tuple (moves, r, c). There are O(k·n²) unique states; each is computed exactly once."])),
    N.para(N.rich([("if not (0 <= r < n ...)", {"code": True}), " — combined bounds check. Off-board positions return 0.0 — they cannot contribute to staying on board."])),
    N.para(N.rich([("if moves == 0: return 1.0", {"code": True}), " — base case: we've made all k moves and we're on the board. This path succeeds with probability 1."])),
    N.para(N.rich([("return sum(...) / 8", {"code": True}), " — the probability of staying on board from (r, c) with 'moves' left equals the average survival probability over all 8 children."])),
    N.callout("⚠️ Space: lru_cache stores O(k·n²) entries — worse than bottom-up's O(n²). Prefer bottom-up in interviews.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Why is this DP ────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal substructure: ", {"bold": True}), "The probability of surviving from (r, c) with m moves remaining depends only on the survival probabilities of its 8 knight-neighbors with m-1 moves. Each step's state depends fully on the previous step — no need to recall full path history."])),
    N.para(N.rich([("Overlapping subproblems: ", {"bold": True}), "Many distinct k-step paths pass through the same (step, cell) pair. Without memoization or tabulation, these subproblems are recomputed exponentially many times. DP reduces O(8^k) to O(k·n²)."])),
    N.code("""# Recurrence relation:
# next_dp[nr][nc] += dp[r][c] / 8
#   for all (r,c) with dp[r][c] > 0
#   for all valid knight destinations (nr, nc)
#
# Equivalently (top-down):
# dp(m, r, c) = sum(dp(m-1, r+dr, c+dc) for dr,dc in MOVES) / 8
# Base: dp(0, r, c) = 1.0 if on board, else 0.0""", "python"),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-force DFS", "O(8^k)", "O(k)"],
        ["Memoization (top-down)", "O(k·n²)", "O(k·n²)"],
        ["Bottom-Up DP — Interview Pick", "O(k·n²)", "O(n²)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "dp[step][x][y] = probability (Probability DP / Grid Random Walk DP) — Guide Section 18.10"])),
    N.callout(
        "When to recognize this pattern: 'probability after k steps/moves', 'random walk on grid', 'fixed number of steps' — track a probability distribution over states, not individual paths. Spread each cell's probability to valid neighbors, divide by number of choices. Sum final distribution for total survival probability.",
        "🔎", "green_background"
    ),
    N.para("*Note: The sub-pattern 'dp[step][x][y] probability' is based on analysis of this problem class. It captures probability DP on a 2D grid iterated over a fixed number of steps.*"),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Probability DP / Random Walk DP):"),
]
related = [
    ("New 21 Game", "Medium", "Probability DP over score states after random card draws — same 'spread and accumulate' pattern (#837)"),
    ("Soup Servings", "Medium", "Expected probability DP over serving quantities — converges quickly for large N (#808)"),
    ("Number of Ways to Stay in the Same Place After Some Steps", "Hard", "1D random walk DP: count paths on linear array that return to origin after k steps (#1269)"),
    ("Minimum Path Sum", "Medium", "Same 2D grid DP structure — but minimizing cost instead of summing probability (#64)"),
    ("Unique Paths II", "Medium", "Count valid grid paths with obstacles — same forward-spread DP pattern but counting not probability (#63)"),
    ("Dice Roll Simulation", "Hard", "Probability/count DP where state includes last-used category and consecutive count (#1223)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))

blocks += [
    N.para("These problems share the 'forward spread' DP pattern: track a value (probability, count) per cell/state, iterate k times, spread to neighbors."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) · Sub-pattern: dp[step][x][y] probability", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("knight_probability_in_chessboard")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append in chunks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
