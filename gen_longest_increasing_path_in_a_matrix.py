"""
gen_longest_increasing_path_in_a_matrix.py
Notion in-place rebuild for LeetCode #329.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# Override redacted token (same pattern as other gen scripts)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-8135-aa05-c4c1f1141be0"
SLUG = "longest_increasing_path_in_a_matrix"

print("Step 1: Set properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=329,
    pattern="Dynamic Programming",
    subpatterns=["DFS + Memoization"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Strictly increasing paths form a DAG — no cycles. DFS + memo computes longest path per cell in O(m·n) total.",
    icon="🔴"
)
print("Properties set OK")

print("Step 2: Wipe existing body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks")

print("Step 3: Build body blocks...")
blocks = []

# ── Problem ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"code": True}),
        (" integer matrix, return the length of the longest ", {}),
        ("strictly increasing", {"bold": True}),
        (" path. From each cell you may move in 4 directions (up, down, left, right). You may not move diagonally or outside the boundary.", {}),
    ])),
    N.para(N.rich([
        ("Example: matrix = [[9,9,4],[6,6,8],[2,1,1]] → Answer: 4", {"code": True}),
        (" (path: 1 → 2 → 6 → 9)", {}),
    ])),
    N.divider(),
]

# ── Solution 1: DFS + Memoization ─────────────────────────────────────
blocks += [
    N.h2("Solution 1 — DFS + Memoization (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Model each cell as a node in a directed graph. There is an edge from cell A to cell B only if B is adjacent and matrix[B] > matrix[A]. We want the longest path in this directed graph starting from any node."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force DFS from every cell recomputes the same 'interior' cells many times — exponential time. BFS finds shortest paths, not longest. Greedy (always going to the largest neighbor) can miss longer paths that go through smaller values first."),
        N.h4("The Key Observation"),
        N.para("The 'strictly increasing' constraint means there are no cycles — you can never revisit a cell, because that would require going both uphill and downhill. The graph is a Directed Acyclic Graph (DAG). Longest path on a DAG is solvable in polynomial time with DP."),
        N.h4("Building the Solution"),
        N.para("Define dfs(r, c) = longest increasing path starting at cell (r, c). Recurrence: dfs(r,c) = 1 + max(dfs(nr,nc)) for each valid neighbor with a larger value. Base: no valid neighbor → return 1. Memoize every cell. Outer answer = max(dfs(r,c)) over all cells."),
        N.callout(
            "Analogy: Think of the matrix as a mountain range. You can only walk uphill. The longest route from any valley to any peak, taking any uphill steps, is the answer. Because you can only go up, you never loop back — making DP safe.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def longestIncreasingPath(matrix):\n"
        "    if not matrix or not matrix[0]: return 0\n"
        "    ROWS, COLS = len(matrix), len(matrix[0])\n"
        "    memo = {}\n"
        "\n"
        "    def dfs(r, c):\n"
        "        if (r, c) in memo: return memo[(r, c)]\n"
        "        best = 1  # minimum: just this cell\n"
        "        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if (0 <= nr < ROWS and 0 <= nc < COLS\n"
        "                    and matrix[nr][nc] > matrix[r][c]):\n"
        "                best = max(best, 1 + dfs(nr, nc))\n"
        "        memo[(r, c)] = best\n"
        "        return best\n"
        "\n"
        "    return max(dfs(r, c) for r in range(ROWS) for c in range(COLS))",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), (" — cache mapping (r,c) to the longest path length from that cell. Initially empty.", {})])),
    N.para(N.rich([("if (r, c) in memo: return memo[(r, c)]", {"code": True}), (" — cache hit: we have already computed this cell's answer. Return it immediately in O(1).", {})])),
    N.para(N.rich([("best = 1", {"code": True}), (" — initialize to 1 because every cell is a valid path of length 1 by itself (the base case).", {})])),
    N.para(N.rich([("for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]", {"code": True}), (" — iterate over the 4 cardinal directions: right, left, down, up.", {})])),
    N.para(N.rich([("if in_bounds and matrix[nr][nc] > matrix[r][c]", {"code": True}), (" — only recurse if the neighbor is within the grid AND has a strictly larger value.", {})])),
    N.para(N.rich([("best = max(best, 1 + dfs(nr, nc))", {"code": True}), (" — 1 counts the current cell; dfs(nr, nc) gives the best path from the neighbor onwards. Take the maximum over all valid neighbors.", {})])),
    N.para(N.rich([("memo[(r, c)] = best", {"code": True}), (" — store the computed answer BEFORE returning. Must come before return so future calls can use the cache.", {})])),
    N.para(N.rich([("return max(dfs(r, c) for r in range(ROWS) for c in range(COLS))", {"code": True}), (" — try every cell as a starting point. Many will be cache hits. Return the global maximum.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force DFS (No Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same graph as Solution 1, but without caching. Explore all possible paths from every cell by recursion."),
        N.h4("What Doesn't Work (Why This is Slow)"),
        N.para("If cells A, B, C all have paths through cell D, dfs(D) is recomputed 3 times — once for each caller. In the worst case (a perfectly sorted matrix), this leads to exponential recomputation."),
        N.h4("The Key Observation"),
        N.para("The code is correct but slow. It is presented here to motivate why memoization is necessary — the transition from brute force to memoization is the entire insight."),
    ]),
    N.h3("Code"),
    N.code(
        "def longestIncreasingPath_brute(matrix):\n"
        "    ROWS, COLS = len(matrix), len(matrix[0])\n"
        "\n"
        "    def dfs(r, c):\n"
        "        best = 1\n"
        "        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if (0 <= nr < ROWS and 0 <= nc < COLS\n"
        "                    and matrix[nr][nc] > matrix[r][c]):\n"
        "                best = max(best, 1 + dfs(nr, nc))  # no cache\n"
        "        return best\n"
        "\n"
        "    return max(dfs(r, c) for r in range(ROWS) for c in range(COLS))",
        "python"
    ),
    N.callout(
        "⚠️  This is correct but exponentially slow. Every shared 'uphill' cell is recomputed independently for every path that passes through it. Adding memo = {} and two cache lines transforms this into O(m·n).",
        "⚠️", "red_background"
    ),
    N.divider(),
]

# ── Why Is This DP? ───────────────────────────────────────────────────
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The longest path from (r,c) equals 1 + the longest path among its valid neighbors. The global answer decomposes into independent per-cell subproblems.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Multiple starting cells may route through the same high-value cell. Without memoization, dfs(D) would be computed once per caller. With the cache, it is computed exactly once.", {}),
    ])),
    N.code(
        "# Recurrence:\n"
        "dfs(r, c) = 1 + max{ dfs(nr, nc) | (nr,nc) adjacent, matrix[nr][nc] > matrix[r][c] }\n"
        "dfs(r, c) = 1   # base case: no valid neighbor",
        "python"
    ),
    N.callout(
        "The strictly-increasing constraint makes the graph acyclic (a DAG). This is the key property that allows DP — without it, longest-path is NP-hard on general graphs.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DFS", "O(2^(m·n))", "O(m·n) stack"],
        ["DFS + Memoization ✓", "O(m·n)", "O(m·n)"],
        ["Topological Sort (BFS)", "O(m·n)", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS + Memoization (Graph DP on DAG)", {})])),
    N.callout(
        "When to recognize this pattern: Grid traversal with a monotonic constraint (strictly increasing/decreasing) that prevents cycles. Need to find the longest/shortest path starting from any cell. Many starting cells share common 'interior' subpaths, creating overlapping subproblems that memoization resolves.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS + Memoization / DP on DAG):"),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), (" (Medium) — 1D version of this problem; same strictly-increasing DP recurrence (#300)", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Grid DFS without memoization; no overlapping subproblems arise (#200)", {})])),
    N.bullet(N.rich([("Out of Boundary Paths", {"bold": True}), (" (Medium) — 3D DP (row, col, steps); DFS + memo is the cleanest approach (#576)", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium) — Grid DP with obstacles; tabulation or memo both work (#63)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Grid DFS with Trie; same grid traversal backbone (#212)", {})])),
    N.bullet(N.rich([("Cherry Pickup", {"bold": True}), (" (Hard) — Two-agent grid DP; 3D memoization on a shared grid (#741)", {})])),
    N.para("These problems all share the same core technique: define a subproblem per cell (or state), recurse with a constraint that prevents cycles, memoize each cell's result."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: DFS + Memoization. Classification source: Analysis (DP on DAG).", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
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
