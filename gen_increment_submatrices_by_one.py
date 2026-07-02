"""
gen_increment_submatrices_by_one.py
Notion update for LeetCode #2536 — Increment Submatrices by One
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811e-840a-e5cee843e81a"

# ── 1) Properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2536,
    pattern="Prefix Sum",
    subpatterns=["2D Difference Array"],
    tc="O(q + n²)",
    sc="O(n²)",
    key_insight="Encode each rectangle with 4 corner markers in a (n+1)×(n+1) diff array; two prefix-sum sweeps reconstruct the full matrix in O(n²).",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a positive integer ", {}),
        ("n", {"code": True}),
        (", representing an ", {}),
        ("n × n", {"code": True}),
        (" matrix of zeros. You are also given a 2D integer array ", {}),
        ("queries", {"code": True}),
        (" where each query is ", {}),
        ("[r1, c1, r2, c2]", {"code": True}),
        (". For each query, increment the value of all cells ", {}),
        ("mat[i][j]", {"code": True}),
        (" by 1 for all ", {}),
        ("r1 ≤ i ≤ r2", {"code": True}),
        (" and ", {}),
        ("c1 ≤ j ≤ c2", {"code": True}),
        (". Return the matrix after applying all the queries.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: 2D Difference Array (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — 2D Difference Array (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to apply many 'add 1 to a rectangle' operations to an initially-zero matrix, then read the final state. The key observation: we never need to query the matrix mid-way — only at the very end. This is the classic 'offline batch update then read all' pattern."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach loops over every cell inside each rectangle — O(n²) per query, O(q·n²) total. For n=500, q=500, this is 62.5M operations. LeetCode's test cases will TLE this."),
        N.h4("The Key Observation"),
        N.para("The 1D difference array solves 'range addition, then read all values' in O(1) per update + O(n) final pass. For a range [l, r]: diff[l] += 1, diff[r+1] -= 1. Then prefix-sum recovers the values. The 2D version is the same idea — mark 4 corners of a rectangle, then do a 2D prefix sum (two passes: one per dimension)."),
        N.h4("Building the Solution"),
        N.para("Step 1: Allocate diff[n+1][n+1] — the guard row/column (index n) absorbs writes at r2+1 and c2+1 when queries touch the boundary. Step 2: For each query [r1,c1,r2,c2]: diff[r1][c1]+=1, diff[r1][c2+1]-=1, diff[r2+1][c1]-=1, diff[r2+1][c2+1]+=1 (inclusion-exclusion to cancel borders). Step 3: Row-wise prefix sum across all n rows. Step 4: Column-wise prefix sum across all n columns. Step 5: Return diff[:n][:n]."),
        N.callout(
            "Analogy: Think of turning on a sprinkler in a rectangular yard. The difference array marks 'start watering here' and 'stop watering here' at the borders. The prefix sum then 'flows' the water through the entire yard — each cell accumulates the total from all active sprinklers covering it.",
            "🌊", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        """def rangeAddQueries(n: int, queries: list[list[int]]) -> list[list[int]]:
    # (n+1)x(n+1) guard prevents out-of-bounds at r2+1, c2+1 boundaries
    diff = [[0] * (n + 1) for _ in range(n + 1)]

    # Step 1: Encode each query as 4 corner updates — O(1) per query
    for r1, c1, r2, c2 in queries:
        diff[r1][c1]     += 1   # start: top-left corner
        diff[r1][c2 + 1] -= 1   # cancel rightward propagation
        diff[r2 + 1][c1] -= 1   # cancel downward propagation
        diff[r2 + 1][c2 + 1] += 1  # fix double-cancellation at far corner

    # Step 2: Row-wise prefix sum — propagate values left to right
    for r in range(n):
        for c in range(1, n):
            diff[r][c] += diff[r][c - 1]

    # Step 3: Column-wise prefix sum — propagate values top to bottom
    for c in range(n):
        for r in range(1, n):
            diff[r][c] += diff[r - 1][c]

    # Return top-left n×n slice (discard guard row and column)
    return [row[:n] for row in diff[:n]]"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("diff = [[0]*(n+1) for _ in range(n+1)]", {"code": True}), (" — Allocate (n+1)×(n+1) array of zeros. The extra row and column absorb writes when queries touch the last row/column, eliminating the need for bounds checking.", {})])),
    N.para(N.rich([("diff[r1][c1] += 1", {"code": True}), (" — Place +1 at the top-left corner of the rectangle. This is the 'start incrementing here' signal.", {})])),
    N.para(N.rich([("diff[r1][c2+1] -= 1", {"code": True}), (" — Place -1 one column to the right of the rectangle. After the row prefix sum, this cancels the +1's rightward propagation beyond column c2.", {})])),
    N.para(N.rich([("diff[r2+1][c1] -= 1", {"code": True}), (" — Place -1 one row below the rectangle. After the column prefix sum, this cancels downward propagation beyond row r2.", {})])),
    N.para(N.rich([("diff[r2+1][c2+1] += 1", {"code": True}), (" — The far corner was double-subtracted by both -1 border markers. We add +1 to restore it to 0, so cells outside the rectangle don't get a spurious -1.", {})])),
    N.para(N.rich([("diff[r][c] += diff[r][c-1]", {"code": True}), (" — Row prefix sum: each cell accumulates the sum of all values to its left in the same row. After this pass, each (r,c) holds the net horizontal contribution from all queries affecting row r.", {})])),
    N.para(N.rich([("diff[r][c] += diff[r-1][c]", {"code": True}), (" — Column prefix sum: each cell accumulates from above. After this pass, each (r,c) holds its final answer — the count of queries whose rectangle contained it.", {})])),
    N.para(N.rich([("return [row[:n] for row in diff[:n]]", {"code": True}), (" — Slice off the guard row (index n) and guard column (index n) to return the n×n result.", {})])),
    N.divider(),
]

# ── Solution 2: Naive Brute Force ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Naive Brute Force"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading of the problem: for each query, literally increment every cell in the specified rectangle."),
        N.h4("What Doesn't Work"),
        N.para("This is O(q·n²) — for each of q queries we visit up to n² cells. For large inputs (n=500, q=500), this is ~62.5M operations and will TLE on LeetCode."),
        N.h4("The Key Observation"),
        N.para("We always start with this approach to verify correctness. During the interview, propose this first, state the time complexity, then improve to the difference array."),
        N.h4("Building the Solution"),
        N.para("Straightforward triple-loop: outer loop over queries, inner double-loop over cells in [r1..r2] × [c1..c2]."),
    ]),
    N.h3("Code"),
    N.code(
        """def rangeAddQueries_naive(n: int, queries: list[list[int]]) -> list[list[int]]:
    mat = [[0] * n for _ in range(n)]  # Initialize n×n matrix
    for r1, c1, r2, c2 in queries:
        for r in range(r1, r2 + 1):    # O(n) rows
            for c in range(c1, c2 + 1):  # O(n) cols
                mat[r][c] += 1         # Increment each cell: O(n²) per query
    return mat  # Total: O(q · n²)"""
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["2D Difference Array (optimal)", "O(q + n²)", "O(n²)"],
        ["Naive Brute Force", "O(q · n²)", "O(n²)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum (Section 1.3 of DSA Guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("2D Difference Array — extends the 1D Difference Array technique to two dimensions using 4-corner inclusion-exclusion encoding.", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Add a value to all cells in a rectangle' — batch, offline (all queries before any read). (2) 'Many range updates, then read all final values' — no mid-stream queries. (3) Matrix starts at a uniform value; operations are additive over rectangles. Signal words: 'increment submatrix', 'add to all cells in range', 'apply operations then return matrix'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Prefix Sum / Difference Array technique:"),
    N.bullet(N.rich([("Range Addition", {"bold": True}), (" (Medium, #370) — 1D version of this exact problem; the foundational difference array technique. Start here if new to the pattern.", {})])),
    N.bullet(N.rich([("Range Sum Query 2D - Immutable", {"bold": True}), (" (Medium, #304) — 2D prefix sum for read queries on a static matrix. Complementary skill.", {})])),
    N.bullet(N.rich([("Corporate Flight Bookings", {"bold": True}), (" (Medium, #1109) — 1D difference array for interval seat booking queries.", {})])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), (" (Medium, #1094) — 1D difference array on a timeline to check if capacity is ever exceeded.", {})])),
    N.bullet(N.rich([("Stamping the Grid", {"bold": True}), (" (Hard, #2132) — 2D difference array with a rectangle-coverage feasibility check.", {})])),
    N.bullet(N.rich([("Maximum Sum of Rectangle No Larger Than K", {"bold": True}), (" (Hard, #363) — 2D prefix sum combined with binary search in a sorted set.", {})])),
    N.bullet(N.rich([("Count of Subarrays with Fixed Bounds", {"bold": True}), (" (Hard, #2444) — Prefix sum variant tracking valid range boundaries.", {})])),
    N.para("These problems share the core technique: encode range updates as boundary markers, recover final values with prefix sums."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.3 (Prefix Sum Pattern). Sub-pattern '2D Difference Array' is an analysis-derived extension of the 1D Difference Array listed in the guide.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("increment_submatrices_by_one")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
