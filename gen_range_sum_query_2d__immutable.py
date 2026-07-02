"""
gen_range_sum_query_2d__immutable.py
Notion IN-PLACE update for LeetCode #304 — Range Sum Query 2D - Immutable
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8155-9d10-f9c8662bbb88"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=304,
    pattern="Prefix Sum",
    subpatterns=["2D Prefix Sum"],
    tc="O(m·n) init, O(1) query",
    sc="O(m·n)",
    key_insight="Precompute top-left rectangle sums; answer any rectangle query in O(1) via inclusion-exclusion.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a 2D matrix ",
        ("matrix", {"code": True}),
        " that is initialized once and never changes, handle multiple calls to ",
        ("sumRegion(row1, col1, row2, col2)", {"code": True}),
        " which returns the sum of all elements inside the rectangle defined by its top-left corner ",
        ("(row1, col1)", {"code": True}),
        " and bottom-right corner ",
        ("(row2, col2)", {"code": True}),
        " (inclusive). Answer each query in O(1) time after O(m*n) preprocessing.",
    ])),
    N.divider(),
]

# ── Solution 1 — 2D Prefix Sum (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — 2D Prefix Sum (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The matrix never changes — we're paying a one-time preprocessing cost to answer every future query in constant time. The question is: what can we precompute that captures all possible rectangle sums efficiently?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: iterate every cell in the rectangle for each query — O(m·n) per query. With 10,000 queries on a 200×200 grid that's 400 million operations. Too slow. A row-only prefix sum reduces to O(m) per query — better, but still not O(1)."),
        N.h4("The Key Observation"),
        N.para("Extend the 1D prefix sum to 2D. In 1D: prefix[i] = sum of first i elements; range sum(l,r) = prefix[r+1] − prefix[l]. In 2D: define pre[i][j] = sum of the top-left rectangle from (0,0) to (i-1,j-1). Then ANY rectangle sum = four lookups via the inclusion-exclusion principle."),
        N.h4("Building the Solution"),
        N.para("1. Allocate a (m+1)×(n+1) table of zeros — the extra border acts as sentinels.\n2. Fill row-by-row: pre[i+1][j+1] = matrix[i][j] + pre[i][j+1] + pre[i+1][j] − pre[i][j].\n3. Query: pre[r2+1][c2+1] − pre[r1][c2+1] − pre[r2+1][c1] + pre[r1][c1]."),
        N.callout(
            "Analogy: Imagine each cell stores the total rainfall in the top-left quadrant of a city map. To find rainfall in any rectangular district, you take the big quadrant, cut away the strip above and strip to the left, and add back the corner that was removed twice.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class NumMatrix:\n"
        "    def __init__(self, matrix):\n"
        "        m, n = len(matrix), len(matrix[0])\n"
        "        self.pre = [[0]*(n+1) for _ in range(m+1)]\n"
        "        for i in range(m):\n"
        "            for j in range(n):\n"
        "                self.pre[i+1][j+1] = (\n"
        "                    matrix[i][j]\n"
        "                    + self.pre[i][j+1]\n"
        "                    + self.pre[i+1][j]\n"
        "                    - self.pre[i][j]\n"
        "                )\n\n"
        "    def sumRegion(self, r1, c1, r2, c2):\n"
        "        return (\n"
        "            self.pre[r2+1][c2+1]\n"
        "            - self.pre[r1][c2+1]\n"
        "            - self.pre[r2+1][c1]\n"
        "            + self.pre[r1][c1]\n"
        "        )"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.pre = [[0]*(n+1) for _ in range(m+1)]", {"code": True}), " — Allocate (m+1)x(n+1) zeros. Row 0 and col 0 are sentinel zeros — they mean 'sum of empty rectangle = 0' and eliminate boundary checks."])),
    N.para(N.rich([("self.pre[i+1][j+1] = matrix[i][j] + self.pre[i][j+1] + self.pre[i+1][j] - self.pre[i][j]", {"code": True}), " — Build recurrence: current cell + rectangle above + rectangle left minus overlapping corner (inclusion-exclusion for the fill step)."])),
    N.para(N.rich([("self.pre[r2+1][c2+1]", {"code": True}), " — Big top-left rectangle from (0,0) to (r2,c2). Includes our target region plus unwanted strips."])),
    N.para(N.rich([("- self.pre[r1][c2+1]", {"code": True}), " — Remove the strip above the query region: rows 0..r1-1, cols 0..c2."])),
    N.para(N.rich([("- self.pre[r2+1][c1]", {"code": True}), " — Remove the strip to the left: rows 0..r2, cols 0..c1-1."])),
    N.para(N.rich([("+ self.pre[r1][c1]", {"code": True}), " — The top-left corner (rows 0..r1-1, cols 0..c1-1) was subtracted twice above — add it back once to correct the over-subtraction."])),
    N.divider(),
]

# ── Solution 2 — Row-Only Prefix (partial optimization) ──
blocks += [
    N.h2("Solution 2 — Row-Only Prefix Sum"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Before discovering the full 2D prefix sum, a natural intermediate step is: precompute 1D prefix sums for each row. Then any row's column-range sum is O(1), and a rectangle query sums O(m) rows."),
        N.h4("What Doesn't Work"),
        N.para("O(m) per query — better than brute force O(m·n) but not O(1). For very tall matrices or many queries, still too slow."),
        N.h4("The Key Observation"),
        N.para("Extending this to columns too — i.e., computing prefix sums in both dimensions — gives the full 2D approach in Solution 1. The row-only version is a useful stepping stone that shows why two dimensions of prefix sums are needed."),
        N.h4("Building the Solution"),
        N.para("For each row, store the 1D prefix sum. For a sumRegion query, iterate each row and use the row's prefix sum to get the column range in O(1) — total O(m) per query."),
    ]),
    N.h3("Code"),
    N.code(
        "class NumMatrix:\n"
        "    def __init__(self, matrix):\n"
        "        self.row_pre = []\n"
        "        for row in matrix:\n"
        "            rp = [0]\n"
        "            for v in row:\n"
        "                rp.append(rp[-1] + v)\n"
        "            self.row_pre.append(rp)\n\n"
        "    def sumRegion(self, r1, c1, r2, c2):\n"
        "        total = 0\n"
        "        for r in range(r1, r2 + 1):\n"
        "            total += self.row_pre[r][c2+1] - self.row_pre[r][c1]\n"
        "        return total"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("rp = [0]; for v in row: rp.append(rp[-1] + v)", {"code": True}), " — Standard 1D prefix sum: rp[j+1] = sum of row[0..j]. O(n) per row."])),
    N.para(N.rich([("for r in range(r1, r2+1): total += self.row_pre[r][c2+1] - self.row_pre[r][c1]", {"code": True}), " — Sum each row's range [c1,c2] in O(1) using its prefix array. Total: O(m) per query."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Init Time", "Query Time", "Space"],
        ["Brute Force", "O(1)", "O(m·n)", "O(1)"],
        ["Row-Only Prefix Sum", "O(m·n)", "O(m)", "O(m·n)"],
        ["2D Prefix Sum (optimal)", "O(m·n)", "O(1)", "O(m·n)"],
        ["2D Fenwick Tree (mutable)", "O(m·n log m log n)", "O(log m log n)", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Prefix Sum (Section 1.3 of DSA_Patterns_and_SubPatterns_Guide.md)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "2D Prefix Sum — Extend the 1D prefix sum concept to two dimensions using the inclusion-exclusion principle for both table construction and rectangle query answering."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'sumRegion' or 'rectangle sum' on an IMMUTABLE 2D array\n"
        "• Multiple queries on the same static matrix\n"
        "• 'Count cells satisfying condition in a rectangle' → binary 2D prefix sum\n"
        "• Image processing: 'average pixel in a region' → integral image (identical concept)\n"
        "• Any problem where preprocessing is allowed and queries need O(1) answers",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 2D Prefix Sum / Prefix Sum technique:"),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), " (Easy) — 1D version; build intuition here first, then extend to 2D. LeetCode #303."])),
    N.bullet(N.rich([("Range Sum Query 2D — Mutable", {"bold": True}), " (Hard) — Same queries but matrix can be updated; requires 2D Binary Indexed Tree. LeetCode #308."])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), " (Medium) — 1D prefix sums + hash map; count subarrays with target sum. LeetCode #560."])),
    N.bullet(N.rich([("Count Sub-matrices That Sum to Target", {"bold": True}), " (Hard) — Fix two rows, apply 1D prefix + hash map on column sums. LeetCode #1074."])),
    N.bullet(N.rich([("Maximum Side Length of Square with Sum ≤ Threshold", {"bold": True}), " (Medium) — 2D prefix sum + binary search on side length. LeetCode #1292."])),
    N.bullet(N.rich([("Matrix Block Sum", {"bold": True}), " (Medium) — Each cell gets sum of its neighborhood via 2D prefix table. LeetCode #1314."])),
    N.para("These problems share the core technique of precomputing cumulative sums so rectangle/range queries reduce to constant-time arithmetic using the inclusion-exclusion principle."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 — Prefix Sum Pattern, Sub-Pattern: 2D Prefix Sum", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("range_sum_query_2d__immutable")),
    N.para(N.rich([
        ("Step through the algorithm visually — watch the prefix table build cell by cell, then see a query answered in O(1) using inclusion-exclusion. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK  {PAGE_ID}  ({len(blocks)} top-level blocks)")
