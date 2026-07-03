"""
gen_cherry_pickup.py — Notion page builder for Cherry Pickup (LeetCode #741).
Creates a NEW page (notion_page_id was null) then populates it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "cherry_pickup"
NAME = "Cherry Pickup"
NUMBER = 741
DIFFICULTY = "Hard"
ICON = "🔴"
PAGE_ID = None  # null → create fresh

# ── Step 1: Create the page ──────────────────────────────────────────────────
print("Creating Notion page...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created: {PAGE_ID}")

# ── Step 2: Set properties ───────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern="Dynamic Programming",
    subpatterns=["3D DP Two Paths"],
    tc="O(N³)",
    sc="O(N²)",
    key_insight="Model round-trip as two simultaneous forward paths; state=(t,c1,c2), row derived as t-c.",
    icon=ICON,
)
print("Properties set.")

# ── Step 3: No wipe (fresh page), append body blocks ─────────────────────────
print("Building blocks...")
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("n x n", {"code": True}),
        (" grid representing a field of cherries, each cell is one of three values:\n", {}),
        ("0", {"code": True}), (" — empty, ", {}),
        ("1", {"code": True}), (" — has a cherry (consumed when visited), ", {}),
        ("-1", {"code": True}), (" — thorn (impassable).\n\n", {}),
        ("Return the maximum number of cherries you can collect by following these rules:\n", {}),
        ("1. Starting at ", {}), ("(0,0)", {"code": True}), (" go to ", {}), ("(n-1,n-1)", {"code": True}),
        (" by moving right or down.\n", {}),
        ("2. Then return to ", {}), ("(0,0)", {"code": True}),
        (" by moving left or up, collecting cherries along the way.\n", {}),
        ("3. If you reach a thorn, stop immediately. Return 0 if no valid path exists.", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: 3D DP (Optimal / Interview Pick) ───
blocks += [
    N.h2("Solution 1 — 3D DP Two Paths (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The round-trip (go then return) is mathematically equivalent to two people SIMULTANEOUSLY walking from (0,0) to (n-1,n-1). The return path, when reversed, becomes an identical forward traversal. This transforms a tricky sequential problem into a clean joint-optimization problem over two synchronized walkers."),
        N.h4("What Doesn't Work"),
        N.para("Greedy: Run a greedy path once, collect cherries, mark them gone, then greedily run again. This FAILS. The first greedy pass may deplete cherries that, had they been left for cooperative joint optimization, would yield a higher combined total. The two passes are not independent — they share the same grid."),
        N.h4("The Key Observation"),
        N.para("Both walkers make the same number of total moves: each move is right (+col) or down (+row). After t steps, row + col = t for EACH walker. So we need only track (t, c1, c2) — the step count and each walker's column. Their row is always derived as r = t - c. This reduces a 4D state (r1,c1,r2,c2) to 3D (t,c1,c2)."),
        N.h4("Building the Solution"),
        N.para("Initialize dp[0][0] = grid[0][0] (both start at (0,0)). For each step t from 1 to 2*(n-1), for each valid column pair (c1 ≤ c2), compute r1=t-c1 and r2=t-c2. Skip if either cell is out of bounds or a thorn. Add cherries from both cells (once if c1==c2, twice if different). Look at 4 predecessor (dc1,dc2) combos from the previous step. Take the best valid predecessor and add current cherries."),
        N.callout("Analogy: Two friends picking fruit from a field. They start at the same corner and walk to the opposite corner simultaneously. When they happen to visit the same tree, they only grab one basket of fruit — it's already been picked. We plan BOTH routes together to maximize their combined haul.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def cherryPickup(grid: list[list[int]]) -> int:
    N = len(grid)
    NEG_INF = float('-inf')
    # dp[c1][c2] = max cherries for current step t
    dp = [[NEG_INF] * N for _ in range(N)]
    dp[0][0] = grid[0][0]  # Both start at (0,0)

    for t in range(1, 2 * N - 1):
        ndp = [[NEG_INF] * N for _ in range(N)]
        for c1 in range(max(0, t - N + 1), min(N, t + 1)):
            for c2 in range(c1, min(N, t + 1)):  # enforce c1 <= c2 (symmetry)
                r1, r2 = t - c1, t - c2
                if r1 >= N or r2 >= N:
                    continue
                if grid[r1][c1] == -1 or grid[r2][c2] == -1:
                    continue  # thorn — skip this state
                cherries = grid[r1][c1]
                if c1 != c2:
                    cherries += grid[r2][c2]  # distinct cells: add both
                best = NEG_INF
                for dc1 in (0, 1):     # P1 came from up (dc1=0) or left (dc1=1)
                    for dc2 in (0, 1): # P2 came from up (dc2=0) or left (dc2=1)
                        pc1, pc2 = c1 - dc1, c2 - dc2
                        if 0 <= pc1 <= pc2 < N:  # valid + maintain symmetry
                            best = max(best, dp[pc1][pc2])
                if best != NEG_INF:
                    ndp[c1][c2] = best + cherries
        dp = ndp

    return max(0, dp[N - 1][N - 1])
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("N = len(grid)", {"code": True}), " — grid is N×N; N determines step range."])),
    N.para(N.rich([("dp = [[NEG_INF]*N ...]", {"code": True}), " — 2D rolling array; NEG_INF means 'unreachable'."])),
    N.para(N.rich([("dp[0][0] = grid[0][0]", {"code": True}), " — both walkers start at (0,0); pick up cherry if present."])),
    N.para(N.rich([("for t in range(1, 2*N-1):", {"code": True}), " — total steps ranges from 1 to 2*(N-1); at 2*(N-1) both are at (N-1,N-1)."])),
    N.para(N.rich([("c1 range / c2 range", {"code": True}), " — valid columns for step t: max(0,t-N+1) to min(N,t+1). Enforce c1≤c2 by starting c2 at c1."])),
    N.para(N.rich([("r1, r2 = t-c1, t-c2", {"code": True}), " — key derivation: since row+col=t for each walker, row = t - col."])),
    N.para(N.rich([("if grid[r1][c1]==-1 ...", {"code": True}), " — thorn check; skip states involving impassable cells (propagates -∞)."])),
    N.para(N.rich([("cherries = ...", {"code": True}), " — if c1==c2, both at same cell → count once. Otherwise sum both."])),
    N.para(N.rich([("for dc1 in (0,1): for dc2 in (0,1):", {"code": True}), " — 4 predecessor combos: (came from up, came from up), (up,left), (left,up), (left,left)."])),
    N.para(N.rich([("0 <= pc1 <= pc2 < N", {"code": True}), " — predecessor must be in bounds AND maintain pc1≤pc2 symmetry."])),
    N.para(N.rich([("ndp[c1][c2] = best + cherries", {"code": True}), " — accumulate: best prior state plus current step's cherries."])),
    N.para(N.rich([("dp = ndp", {"code": True}), " — roll forward: next iteration's 'previous' is this iteration's result."])),
    N.para(N.rich([("return max(0, dp[N-1][N-1])", {"code": True}), " — return 0 if bottom-right is unreachable (-∞); otherwise the max cherry count."])),
    N.divider(),
]

# ─── Solution 2: Top-Down Memoization ───
blocks += [
    N.h2("Solution 2 — Top-Down DP with Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same two-path equivalence as Solution 1, but derived recursively. Define a function dfs(r1, c1, r2) that returns the max cherries from current positions to (N-1,N-1). Since both walkers move in sync, c2 is implicit: c2 = r1 + c1 - r2 (from t = r1+c1 = r2+c2)."),
        N.h4("What Doesn't Work"),
        N.para("Recursive without memoization leads to exponential time — the same (r1,c1,r2) state is visited many times through different call paths."),
        N.h4("The Key Observation"),
        N.para("By fixing r1 and c1 (P1's position), P2's column is determined: c2 = (r1+c1) - r2. So we only need to track (r1, c1, r2). Cache these states to avoid recomputation."),
        N.h4("Building the Solution"),
        N.para("Base case: if r1 or r2 out of bounds, or either cell is a thorn → return -∞. If both at (N-1,N-1) → return grid[N-1][N-1]. Recurse over 4 move combinations, memoize results."),
    ]),
    N.h3("Code"),
    N.code("""from functools import lru_cache

def cherryPickup(grid: list[list[int]]) -> int:
    N = len(grid)

    @lru_cache(maxsize=None)
    def dfs(r1, c1, r2):
        c2 = r1 + c1 - r2  # derived from t = r1+c1 = r2+c2
        # Bounds and thorn checks
        if r1 >= N or c1 >= N or r2 >= N or c2 >= N:
            return float('-inf')
        if grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')
        # Both reached end
        if r1 == N-1 and c1 == N-1:
            return grid[N-1][N-1]
        cherries = grid[r1][c1]
        if r1 != r2:  # different rows implies different cells (since t is same)
            cherries += grid[r2][c2]
        # Try all 4 move combinations: P1 moves (down or right), P2 moves (down or right)
        best = max(
            dfs(r1+1, c1,   r2+1),  # both go down
            dfs(r1+1, c1,   r2  ),  # P1 down, P2 right (c2 implicitly +1)
            dfs(r1,   c1+1, r2+1),  # P1 right, P2 down
            dfs(r1,   c1+1, r2  ),  # both go right
        )
        return cherries + best if best != float('-inf') else float('-inf')

    result = dfs(0, 0, 0)
    return max(0, result)
""", "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache", {"code": True}), " — Python's built-in memoization; caches (r1,c1,r2) results automatically."])),
    N.para(N.rich([("c2 = r1 + c1 - r2", {"code": True}), " — since both walkers are at step t = r1+c1, and t = r2+c2, so c2 = t - r2."])),
    N.para(N.rich([("r1 >= N or c1 >= N or r2 >= N or c2 >= N:", {"code": True}), " — out-of-bounds returns -∞ (unreachable sentinel)."])),
    N.para(N.rich([("if r1 == N-1 and c1 == N-1:", {"code": True}), " — base case: both reached destination (c2 must also be N-1 since t is symmetric)."])),
    N.para(N.rich([("if r1 != r2:", {"code": True}), " — different rows with same t means different cells (r1+c1=r2+c2=t, r1≠r2 → c1≠c2)."])),
    N.para(N.rich([("dfs(r1+1,c1,r2+1)", {"code": True}), " — both go down (row+1 for each). P2 col implicit via c2=t-r2."])),
    N.para(N.rich([("dfs(r1+1,c1,r2)", {"code": True}), " — P1 down, P2 right (P2 row stays, so P2 col increases via derived formula)."])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two greedy passes", "O(N²)", "O(1) — but INCORRECT"],
        ["Backtracking (brute force)", "O(4^(2N))", "O(N) stack"],
        ["3D DP + memoization (top-down)", "O(N³)", "O(N³) cache"],
        ["3D DP + rolling 2D (bottom-up) — optimal", "O(N³)", "O(N²)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "3D DP Two Paths (simultaneous multi-path DP on a grid)"])),
    N.callout(
        "When to recognize this pattern: 'round trip' on a grid where items are consumed; two traversals that share resources; maximize combined collection over two paths moving right/down; return path equivalent to second forward path.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Cherry Pickup II", {"bold": True}), " (Hard) — Two robots from top corners to bottom row simultaneously; same 3D DP two-path framework on a grid."])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), " (Medium) — Single-path DP on a grid; foundational for understanding the row+col=t step invariant."])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), " (Medium) — Count paths on a grid with obstacles; same (right/down) movement model."])),
    N.bullet(N.rich([("Dungeon Game", {"bold": True}), " (Hard) — Grid DP where path choice has downstream consequences; similar to one path being blocked by another's decision."])),
    N.bullet(N.rich([("Out of Boundary Paths", {"bold": True}), " (Medium) — Step-indexed DP on a grid where step count t is the DP dimension."])),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), " (Hard) — Interval DP where local decisions affect global context; same difficulty class."])),
    N.bullet(N.rich([("Ones and Zeroes", {"bold": True}), " (Medium) — 3D DP (two resource dimensions); good practice for multi-dimensional DP thinking."])),
    N.para("These problems share the core technique of modeling coordinated multi-agent decisions with synchronized step-count DP on a grid."),
    N.callout("📚 Guide Reference: Dynamic Programming section — '3D DP Two Paths' is a specialized sub-pattern for grid problems requiring simultaneous traversal optimization.", "📚", "gray_background"),
    N.divider(),
]

# ─── Interactive Visual Explainer ───
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
