"""
gen_maximal_square.py — Notion IN-PLACE rebuild for LeetCode #221 Maximal Square.
Run from the Algorithms directory: python3 gen_maximal_square.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81f9-b6ff-d341f3b652b6"

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=221,
    pattern="Dynamic Programming",
    subpatterns=["Min of Three Neighbors Plus One"],
    tc="O(m*n)",
    sc="O(m*n) -> O(n) with rolling row",
    key_insight="dp[i][j] = min(top, left, diagonal) + 1: three neighbors cap the largest square ending at this cell.",
    icon="🟡",
)
print("Properties set OK.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────────
print("Building new content blocks...")

TABULATION_CODE = (
    "def maximalSquare(matrix: list[list[str]]) -> int:\n"
    "    m, n = len(matrix), len(matrix[0])\n"
    "    dp = [[0] * n for _ in range(m)]   # dp[i][j] = side of largest sq ending here\n"
    "    max_side = 0\n"
    "\n"
    "    for i in range(m):\n"
    "        for j in range(n):\n"
    "            if matrix[i][j] == '0':\n"
    "                dp[i][j] = 0            # zero cell: no square can end here\n"
    "            elif i == 0 or j == 0:\n"
    "                dp[i][j] = 1            # edge row/col: at most 1x1 square\n"
    "            else:\n"
    "                dp[i][j] = min(\n"
    "                    dp[i-1][j],         # top neighbor\n"
    "                    dp[i][j-1],         # left neighbor\n"
    "                    dp[i-1][j-1]        # diagonal neighbor\n"
    "                ) + 1\n"
    "            max_side = max(max_side, dp[i][j])\n"
    "\n"
    "    return max_side * max_side          # area = side^2  (NOT just side!)\n"
)

MEMOIZATION_CODE = (
    "def maximalSquare(matrix: list[list[str]]) -> int:\n"
    "    m, n = len(matrix), len(matrix[0])\n"
    "    memo = {}\n"
    "\n"
    "    def dp(i: int, j: int) -> int:\n"
    "        \"\"\"Largest all-1s square with bottom-right at (i, j).\"\"\"\n"
    "        if i < 0 or j < 0:\n"
    "            return 0                    # out-of-bounds sentinel\n"
    "        if matrix[i][j] == '0':\n"
    "            return 0                    # zero cell: no square possible\n"
    "        if (i, j) in memo:\n"
    "            return memo[(i, j)]         # cache hit\n"
    "\n"
    "        result = min(dp(i-1, j), dp(i, j-1), dp(i-1, j-1)) + 1\n"
    "        memo[(i, j)] = result\n"
    "        return result\n"
    "\n"
    "    ans = max(dp(i, j) for i in range(m) for j in range(n))\n"
    "    return ans * ans\n"
)

ROLLING_ROW_CODE = (
    "def maximalSquare(matrix: list[list[str]]) -> int:\n"
    "    \"\"\"Space-optimized O(n) -- rolling single row instead of full dp table.\"\"\"\n"
    "    n = len(matrix[0])\n"
    "    prev = [0] * n      # represents dp[i-1][*]\n"
    "    max_side = 0\n"
    "\n"
    "    for row in matrix:\n"
    "        curr = [0] * n\n"
    "        diag = 0        # tracks dp[i-1][j-1] BEFORE prev[j-1] is overwritten\n"
    "        for j, val in enumerate(row):\n"
    "            tmp = prev[j]               # save dp[i-1][j] for next column's diag\n"
    "            if val == '1':\n"
    "                if j == 0:\n"
    "                    curr[j] = 1\n"
    "                else:\n"
    "                    curr[j] = min(prev[j], curr[j-1], diag) + 1\n"
    "            diag = tmp\n"
    "            max_side = max(max_side, curr[j])\n"
    "        prev = curr\n"
    "\n"
    "    return max_side * max_side\n"
)

blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(
        "Given an m x n binary matrix filled with '0's and '1's, find the largest square "
        "containing only 1s and return its area.\n\n"
        "Constraints: 1 <= m, n <= 300. matrix[i][j] is '0' or '1'.\n\n"
        "Example:\n"
        "  Input:  [[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],"
        "[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]\n"
        "  Output: 4  (the 2x2 block at rows 1-2, cols 2-3)\n\n"
        "Edge cases: all zeros -> 0, single '1' -> 1, all ones -> min(m,n)^2."
    ),
    N.divider(),
]

# ── Why is This DP? ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(
        "Two pillars confirm this is a DP problem:"
    ),
    N.para(N.rich([
        ("1. Optimal Substructure: ", {"bold": True}),
        ("The size of the largest square ending at (i,j) depends entirely on the sizes "
         "of the largest squares ending at (i-1,j), (i,j-1), and (i-1,j-1). The global "
         "problem reduces cleanly to smaller sub-problems of the same type.", {})
    ])),
    N.para(N.rich([
        ("2. Overlapping Subproblems: ", {"bold": True}),
        ("A naive approach that expands squares outward re-examines the same interior cells "
         "many times -- O(m*n*min(m,n)^2) time. DP computes each cell exactly once, "
         "storing the result for instant O(1) reuse.", {})
    ])),
    N.callout(
        "State Definition: dp[i][j] = the side length of the largest all-1s square whose "
        "bottom-right corner is exactly cell (i, j). Anchoring at the bottom-right corner "
        "gives a clean, non-overlapping decomposition of the problem.",
        "🔑", "blue_background"
    ),
    N.divider(),
]

# ── Recurrence Relation ────────────────────────────────────────────────────────
blocks += [
    N.h2("Recurrence Relation"),
    N.code(
        "if matrix[i][j] == '0':\n"
        "    dp[i][j] = 0      # no square can contain a 0\n\n"
        "if i == 0 or j == 0:  # edge row or column\n"
        "    dp[i][j] = int(matrix[i][j])  # at most 1x1, no room to expand\n\n"
        "else:  # interior '1' cell\n"
        "    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1",
        "python"
    ),
    N.para(
        "Proof sketch: For a square of side k+1 to have its bottom-right at (i,j), all "
        "three conditions must hold simultaneously: (a) dp[i-1][j] >= k (top covers k rows), "
        "(b) dp[i][j-1] >= k (left covers k columns), (c) dp[i-1][j-1] >= k (diagonal anchors "
        "the top-left corner). The minimum is the bottleneck; we can always extend by 1 "
        "from that minimum."
    ),
    N.para(
        "Why do we need all THREE neighbors? Top and left alone are not sufficient. "
        "Consider: a 2x1 block of ones above (dp[i-1][j]=2) and a 1x2 block to the left "
        "(dp[i][j-1]=2), but the diagonal (i-1,j-1) is 0. Without the diagonal check, "
        "we would incorrectly claim dp[i][j]=3. The diagonal is the 'corner glue' that "
        "ensures the full square interior is valid."
    ),
    N.divider(),
]

# ── Solution 1 — Tabulation (Interview Pick) ───────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Don't think globally: 'Is there a large square somewhere in the grid?' "
            "Think locally: 'For each cell, what is the largest square I can form if I "
            "use THIS cell as the bottom-right corner?' This local question has a crisp, "
            "computable answer from exactly three neighbors."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: for each cell, expand outward and check every cell in the candidate "
            "square. For a 300x300 grid, this is O(300*300*300^2) ~ 8 billion operations. "
            "The same interior cells are checked repeatedly as we expand different candidate squares."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Consider a 3x3 block of all '1's. Can (2,2) be the corner of a 3x3 square? "
            "Only if the 2x2 block ending at (1,2) is valid AND the 2x2 ending at (2,1) "
            "is valid AND the 2x2 ending at (1,1) is valid. All three must be >= 2. "
            "The diagonal (1,1) is the 'corner glue' -- without it, two independent 2x2 "
            "blocks might exist that don't overlap into a proper 3x3."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Define dp[i][j] = side of largest square with bottom-right at (i,j).\n"
            "Step 2: Base cases: first row/column can only be 0 or 1.\n"
            "Step 3: Fill row by row (left to right) -- all three dependencies are ready.\n"
            "Step 4: Track max_side. Return max_side * max_side (AREA, not side)."
        ),
        N.callout(
            "Analogy: Think of dp[i][j] as 'how far can I stretch a square carpet into "
            "the top-left corner from this cell?' The weakest of the three supporting walls "
            "(top, left, diagonal) limits how far you can stretch.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("m, n = len(matrix), len(matrix[0])", {"code": True}),
        (" -- extract grid dimensions.", {})
    ])),
    N.para(N.rich([
        ("dp = [[0]*n for _ in range(m)]", {"code": True}),
        (" -- dp table initialized to 0. dp[i][j] will hold the side length of the "
         "largest all-1s square with bottom-right at (i,j).", {})
    ])),
    N.para(N.rich([
        ("max_side = 0", {"code": True}),
        (" -- global tracker for the best side length seen so far.", {})
    ])),
    N.para(N.rich([
        ("for i in range(m): for j in range(n):", {"code": True}),
        (" -- row-major traversal. Ensures top (i-1,j), left (i,j-1), and diagonal "
         "(i-1,j-1) are always computed before we need them.", {})
    ])),
    N.para(N.rich([
        ("if matrix[i][j] == '0': dp[i][j] = 0", {"code": True}),
        (" -- zero cell: no all-ones square can end here. Set to 0 explicitly "
         "(already the default, but clarity matters in interviews).", {})
    ])),
    N.para(N.rich([
        ("elif i == 0 or j == 0: dp[i][j] = 1", {"code": True}),
        (" -- edge cells have no room above or to the left to form a larger square. "
         "Best case is a 1x1 square (if the cell itself is '1').", {})
    ])),
    N.para(N.rich([
        ("dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1", {"code": True}),
        (" -- the core recurrence. Three neighbors give us the largest guaranteed "
         "valid block in each direction. The minimum is the geometric bottleneck; "
         "+1 extends the square by one row and one column.", {})
    ])),
    N.para(N.rich([
        ("max_side = max(max_side, dp[i][j])", {"code": True}),
        (" -- update the global best after every cell. Runs in O(1) per cell.", {})
    ])),
    N.para(N.rich([
        ("return max_side * max_side", {"code": True}),
        (" -- the problem asks for AREA, not side length. Returning max_side directly "
         "is one of the most common bugs on this problem.", {})
    ])),
    N.callout(
        "Common mistake: returning max_side instead of max_side * max_side. "
        "The problem statement explicitly asks for the area of the largest square.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Memoization ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Express the same recurrence recursively. 'To find the largest square ending "
            "at (i,j), ask the three neighbors about their squares.' The recursion naturally "
            "follows the definition. Add a memo dictionary to cache sub-results."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization: each call branches into 3 sub-calls. "
            "Without caching, the same (i,j) is recomputed exponentially many times -- "
            "O(3^(m*n)) in the worst case."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The recursive structure mirrors tabulation exactly -- same recurrence, same "
            "base cases. The only difference is execution order: tabulation fills bottom-up "
            "systematically; memoization fills on-demand from the top. Both compute each "
            "(i,j) exactly once: O(m*n) total."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Define recursive function dp(i, j) = side of largest square ending at (i,j).\n"
            "Step 2: Base cases: return 0 for out-of-bounds or '0' cells.\n"
            "Step 3: Check memo cache before computing.\n"
            "Step 4: Recurse to three neighbors, take min+1, cache and return.\n"
            "Step 5: Call dp(i,j) for all (i,j), take max, return max^2."
        ),
    ]),
    N.h3("Code"),
    N.code(MEMOIZATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("memo = {}", {"code": True}),
        (" -- cache mapping (i, j) -> computed side length. Prevents recomputation "
         "of already-solved sub-problems.", {})
    ])),
    N.para(N.rich([
        ("def dp(i, j):", {"code": True}),
        (" -- recursive function defined inside maximalSquare to close over "
         "the matrix and memo dict.", {})
    ])),
    N.para(N.rich([
        ("if i < 0 or j < 0: return 0", {"code": True}),
        (" -- out-of-bounds sentinel. Treating missing neighbors as 0 unifies the "
         "edge case: min(0,...)+1 = 1, which is correct for edge cells with a '1'.", {})
    ])),
    N.para(N.rich([
        ("if matrix[i][j] == '0': return 0", {"code": True}),
        (" -- zero cell: no square can end here.", {})
    ])),
    N.para(N.rich([
        ("if (i, j) in memo: return memo[(i, j)]", {"code": True}),
        (" -- cache hit. This is the entire optimization -- avoids re-exploring "
         "already-solved sub-problems.", {})
    ])),
    N.para(N.rich([
        ("result = min(dp(i-1,j), dp(i,j-1), dp(i-1,j-1)) + 1", {"code": True}),
        (" -- same recurrence as tabulation, expressed recursively. Each sub-call "
         "is cached, so no cell is computed more than once.", {})
    ])),
    N.para(N.rich([
        ("memo[(i, j)] = result", {"code": True}),
        (" -- store BEFORE returning so any subsequent caller gets the cached value.", {})
    ])),
    N.para(N.rich([
        ("ans = max(dp(i,j) for i in range(m) for j in range(n))", {"code": True}),
        (" -- trigger computation for all cells. Memoization ensures each (i,j) "
         "is computed at most once regardless of call order.", {})
    ])),
    N.callout(
        "Tabulation vs Memoization: Both O(m*n) time. Tabulation avoids Python "
        "recursion stack overhead -- important for large 300x300 grids which could "
        "hit Python's default recursion limit. In interviews, tabulation is usually "
        "preferred for this reason.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Solution 3 — Rolling Row ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Space-Optimized Rolling Row (O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("The Space Optimization Insight"),
        N.para(
            "In tabulation, when computing row i we only ever look at row i-1. "
            "We never need rows i-2, i-3, etc. So instead of the full m*n table, "
            "we keep just two rows: prev (row i-1) and curr (row i), reducing "
            "space from O(m*n) to O(n)."
        ),
        N.h4("The Tricky Diagonal"),
        N.para(
            "There is a subtle trap: dp[i-1][j-1] (the diagonal neighbor) is prev[j-1] "
            "BEFORE we overwrite curr[j-1]. As we iterate j left-to-right, we've already "
            "written curr[j-1] by the time we compute curr[j]. So we must save prev[j] "
            "into 'diag' BEFORE computing curr[j], then shift diag = tmp at the END "
            "of each j iteration."
        ),
        N.callout(
            "The diagonal trap is the single hardest part of the space optimization. "
            "Save tmp = prev[j] BEFORE computing curr[j], then set diag = tmp at "
            "the END of each column iteration.",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(ROLLING_ROW_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("prev = [0] * n", {"code": True}),
        (" -- represents dp[i-1][*], the previous row. Initialized to all zeros "
         "(handles the implicit 'row -1' boundary).", {})
    ])),
    N.para(N.rich([
        ("curr = [0] * n", {"code": True}),
        (" -- represents dp[i][*], the current row being computed.", {})
    ])),
    N.para(N.rich([
        ("diag = 0", {"code": True}),
        (" -- will hold dp[i-1][j-1] for the CURRENT j, saved from the previous "
         "column's prev[j] before it gets shifted.", {})
    ])),
    N.para(N.rich([
        ("tmp = prev[j]", {"code": True}),
        (" -- save dp[i-1][j] BEFORE we move on. This saved value becomes the "
         "diagonal for the NEXT column (j+1).", {})
    ])),
    N.para(N.rich([
        ("curr[j] = min(prev[j], curr[j-1], diag) + 1", {"code": True}),
        (" -- same recurrence: top=prev[j], left=curr[j-1], diagonal=diag.", {})
    ])),
    N.para(N.rich([
        ("diag = tmp", {"code": True}),
        (" -- shift: what was dp[i-1][j] becomes dp[i-1][j-1] for the next iteration.", {})
    ])),
    N.para(N.rich([
        ("prev = curr", {"code": True}),
        (" -- after finishing row i, curr becomes prev for row i+1.", {})
    ])),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(m*n*min(m,n)^2)", "O(1)", "TLE on 300x300 grids"],
        ["Tabulation (Sol 1)", "O(m*n)", "O(m*n)", "Interview pick -- clearest code"],
        ["Memoization (Sol 2)", "O(m*n)", "O(m*n) + stack", "Top-down; may hit recursion limit"],
        ["Rolling Row (Sol 3)", "O(m*n)", "O(n)", "Space-optimal; tricky diagonal tracking"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Min of Three Neighbors Plus One (2D Grid DP)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "  - Binary grid + 'largest square' with uniform constraint\n"
        "  - Answer at (i,j) depends on top, left, and diagonal neighbors\n"
        "  - Brute force requires checking all cells in each candidate region\n"
        "  - Grid dimensions <= 300-500 (O(m*n) DP is fast enough)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same 2D Grid DP technique:"),
    N.bullet(N.rich([
        ("Count Square Submatrices with All Ones", {"bold": True}),
        (" (Medium, #1277) -- Same dp table; sum all dp[i][j] values instead of taking max. "
         "Each dp[i][j] = k means k new squares of sizes 1..k end at that cell.", {})
    ])),
    N.bullet(N.rich([
        ("Maximal Rectangle", {"bold": True}),
        (" (Hard, #85) -- Generalizes square to rectangle; build histogram heights "
         "per row then apply monotonic stack. Much harder.", {})
    ])),
    N.bullet(N.rich([
        ("Largest Rectangle in Histogram", {"bold": True}),
        (" (Hard, #84) -- Foundation sub-problem for Maximal Rectangle; "
         "monotonic stack pattern for 1D bar chart.", {})
    ])),
    N.bullet(N.rich([
        ("Dungeon Game", {"bold": True}),
        (" (Hard, #174) -- 2D DP on grid traversed bottom-right to top-left; "
         "shows DP traversal direction matters.", {})
    ])),
    N.bullet(N.rich([
        ("Unique Paths", {"bold": True}),
        (" (Medium, #62) -- Simpler 2D grid DP: dp[i][j] = dp[i-1][j] + dp[i][j-1]. "
         "Good warm-up before tackling Maximal Square.", {})
    ])),
    N.bullet(N.rich([
        ("Number of Islands", {"bold": True}),
        (" (Medium, #200) -- Same grid traversal but DFS/BFS; contrasts when to "
         "use DP versus graph search on grids.", {})
    ])),
    N.bullet(N.rich([
        ("Cherry Pickup II", {"bold": True}),
        (" (Hard, #1463) -- Advanced 3D grid DP with two-agent state; shows how "
         "state dimensions grow for multi-agent grid problems.", {})
    ])),
    N.para(
        "These problems share the core technique: define a DP state anchored at a grid cell, "
        "express its value from a small neighborhood of already-computed neighbors, fill in "
        "row-major order."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md -- Section 18 (Dynamic Programming) "
        "Sub-Pattern: Min of Three Neighbors Plus One (2D Grid DP)",
        "📚", "gray_background"
    ),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximal_square")),
    N.para(N.rich([
        ("Step through the DP table being filled cell by cell -- use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks built: {len(blocks)}")
