"""
gen_matrix_block_sum.py — Regenerate Notion page for Matrix Block Sum (#1314).
Run: cd ~/Documents/PersonalSkillUp/Algorithms && python3 gen_matrix_block_sum.py
"""
import notion_lib as N

PAGE_ID = "39193418-809c-813e-b319-d5e09decaa98"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1314,
    pattern="Prefix Sum",
    subpatterns=["2D Prefix Sum"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Build a (m+1)×(n+1) prefix table once; answer each k-radius rectangle query in O(1) with the 4-corner inclusion-exclusion formula.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────
BRUTE_CODE = """\
def matrixBlockSum(mat, k):
    m, n = len(mat), len(mat[0])
    ans = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for r in range(max(0, i-k), min(m, i+k+1)):
                for c in range(max(0, j-k), min(n, j+k+1)):
                    ans[i][j] += mat[r][c]
    return ans
"""

OPTIMAL_CODE = """\
def matrixBlockSum(mat, k):
    m, n = len(mat), len(mat[0])

    # Phase 1: Build (m+1)x(n+1) prefix table
    P = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            P[i][j] = (mat[i-1][j-1]
                     + P[i-1][j]    # strip above
                     + P[i][j-1]    # strip left
                     - P[i-1][j-1]) # subtract double-counted corner

    # Phase 2: Answer each rectangle query in O(1)
    ans = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            r1, c1 = max(0, i-k), max(0, j-k)
            r2, c2 = min(m-1, i+k), min(n-1, j+k)
            ans[i][j] = (P[r2+1][c2+1]
                        - P[r1][c2+1]
                        - P[r2+1][c1]
                        + P[r1][c1])
    return ans
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an ", ("m", {"bold": True}), "×", ("n", {"bold": True}),
        " integer matrix ", ("mat", {"code": True}),
        " and an integer ", ("k", {"code": True}),
        ", return a matrix ", ("answer", {"code": True}),
        " where ", ("answer[i][j]", {"code": True}),
        " is the sum of all ", ("mat[r][c]", {"code": True}),
        " for ", ("i−k ≤ r ≤ i+k", {"code": True}),
        " and ", ("j−k ≤ c ≤ j+k", {"code": True}),
        " — clamped to the matrix boundaries.",
    ])),
    N.divider(),
]

# Solution 1 — Brute Force
blocks += [
    N.h2("Solution 1 — Brute Force (O(m·n·(2k+1)²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every cell (i,j), we need to sum all mat values inside a square window of radius k centered at (i,j), clamped to the matrix edges."),
        N.h4("What Doesn't Work Well"),
        N.para("The natural approach: for each cell, loop over its window and sum the values. This is O(m·n·(2k+1)²). It works for small k but explodes for k=100: each of m·n cells reads ~40,000 values, many shared with its neighbors."),
        N.h4("The Key Observation"),
        N.para("The brute force isn't wrong — it's just wasteful. Adjacent output cells share enormous overlapping rectangles. We recompute the same sums repeatedly instead of reusing them."),
        N.h4("Building the Solution"),
        N.para("Straightforward 4-loop implementation: two outer loops over (i,j), two inner loops over the clamped window. Simple to code and verify, but serves as the starting point before optimizing."),
        N.callout("Analogy: Adding up the same receipts every time you need a monthly total, instead of keeping a running total.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(mat), len(mat[0])", {"code": True}), " — Get matrix dimensions."])),
    N.para(N.rich([("ans = [[0]*n for _ in range(m)]", {"code": True}), " — Allocate output matrix, same shape as mat."])),
    N.para(N.rich([("for i, for j", {"code": True}), " — Outer loops iterate over every output cell (i,j)."])),
    N.para(N.rich([("for r in range(max(0,i-k), min(m,i+k+1))", {"code": True}), " — Inner loop clamps row range to [0, m-1]."])),
    N.para(N.rich([("for c in range(...)", {"code": True}), " — Inner loop clamps column range to [0, n-1]."])),
    N.para(N.rich([("ans[i][j] += mat[r][c]", {"code": True}), " — Accumulate window sum. Note: same mat cells read again and again for nearby output cells."])),
    N.divider(),
]

# Solution 2 — 2D Prefix Sum (optimal)
blocks += [
    N.h2("Solution 2 — 2D Prefix Sum (O(m·n)) · Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each output cell asks for the sum of a rectangle in mat. All these rectangles overlap massively. The bottleneck is summing them from scratch each time."),
        N.h4("What Doesn't Work"),
        N.para("Brute force re-sums the same cells for every query. For a 100×100 matrix with k=50, each query sums ~10,000 cells = 1,000,000 × 10,000 = 10^10 operations. Completely unusable."),
        N.h4("The Key Observation"),
        N.para("We can precompute a 2D prefix table P where P[i][j] = sum of mat[0..i-1][0..j-1]. Then any sub-rectangle sum is just a 4-corner arithmetic expression — O(1). This is the 2D extension of the classic 1D prefix sum array."),
        N.h4("Building the Solution"),
        N.para("Step 1: Build P using inclusion-exclusion: P[i][j] = mat[i-1][j-1] + P[i-1][j] + P[i][j-1] - P[i-1][j-1]. Step 2: For each (i,j), clamp the window bounds, then compute the rectangle sum in one formula using the 4-corner lookup."),
        N.callout("Analogy: Precompute 'prefix expenses' so you can instantly answer 'total spent in March' without re-adding every transaction.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("P = [[0]*(n+1) for _ in range(m+1)]", {"code": True}), " — Allocate (m+1)×(n+1) table initialized to zero. The extra row/column at index 0 acts as a zero border eliminating boundary checks."])),
    N.para(N.rich([("for i in range(1, m+1): for j in range(1, n+1):", {"code": True}), " — Fill in 1-indexed order; all dependencies (above, left, corner) are already computed."])),
    N.para(N.rich([("P[i][j] = mat[i-1][j-1] + P[i-1][j] + P[i][j-1] - P[i-1][j-1]", {"code": True}), " — Inclusion-exclusion: current cell + above strip + left strip − doubly-counted top-left corner."])),
    N.para(N.rich([("r1, c1 = max(0, i-k), max(0, j-k)", {"code": True}), " — Clamp top-left corner of the query window to the matrix boundary."])),
    N.para(N.rich([("r2, c2 = min(m-1, i+k), min(n-1, j+k)", {"code": True}), " — Clamp bottom-right corner similarly."])),
    N.para(N.rich([("ans[i][j] = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]", {"code": True}), " — 4-corner query: big rectangle minus top strip minus left strip plus double-subtracted corner."])),
    N.callout(N.rich([
        ("⚠️ Off-by-one alert:", {"bold": True}),
        " The query uses ", ("P[r2+1][c2+1]", {"code": True}),
        " NOT ", ("P[r2][c2]", {"code": True}),
        " because P is 1-indexed relative to mat. Forgetting the +1 silently drops the last row and column of every window.",
    ]), "⚠️", "yellow_background"),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (extra)"],
        ["Brute Force", "O(m·n·(2k+1)²)", "O(1)"],
        ["2D Prefix Sum (optimal)", "O(m·n)", "O(m·n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Prefix Sum (Array Manipulation)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "2D Prefix Sum"])),
    N.callout(N.rich([
        ("When to recognize this pattern: ", {"bold": True}),
        "Problem asks for the sum of all elements in a rectangle or square neighborhood. "
        "Multiple cells query overlapping sub-rectangles of the same immutable matrix. "
        "Keywords: 'sum of all mat[r][c] within range', 'k-radius window sum', 'neighborhood sum for every cell'.",
    ]), "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (2D Prefix Sum / Rectangle Sum Queries):"),
    N.bullet(N.rich([("Range Sum Query 2D — Immutable", {"bold": True}), " (Medium) — Classic 2D prefix table for arbitrary rectangle queries (#304)"])),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), " (Easy) — 1D ancestor: prefix[r+1] - prefix[l] for range sums (#303)"])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), " (Medium) — 1D prefix sums + hash map to count subarrays with target sum (#560)"])),
    N.bullet(N.rich([("Number of Submatrices That Sum to Target", {"bold": True}), " (Hard) — 2D prefix + hash map; the 2D analogue of #560 (#1074)"])),
    N.bullet(N.rich([("Max Sum of Rectangle No Larger Than K", {"bold": True}), " (Hard) — 2D prefix + sorted set for bounded rectangle sums (#363)"])),
    N.bullet(N.rich([("Count Submatrices With All Ones", {"bold": True}), " (Medium) — Row-wise prefix sums to count all-ones rectangles (#1504)"])),
    N.para("These problems share the core technique: precompute prefix sums to turn expensive repeated range queries into O(1) lookups."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 — Prefix Sum Pattern. Sub-pattern: 2D Prefix Sum. Source: Guide Section 1.3 + Analysis.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("matrix_block_sum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ───────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print(f"NOTION OK {PAGE_ID}")
