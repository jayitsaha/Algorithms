"""
gen_pascals_triangle.py — Notion IN-PLACE update for Pascal's Triangle (#118).
Run: python3 gen_pascals_triangle.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b8-b0ba-de70a040cd88"

# ── 1. Properties ──────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=118,
    pattern="Dynamic Programming",
    subpatterns=["Sum of Two Above"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="Each row is fully determined by the previous row: edge cells = 1, interior cells = sum of two parents above.",
    icon="🟢"
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("numRows", {"code": True}),
        (", return the first ", {}),
        ("numRows", {"code": True}),
        (" of Pascal's triangle. In Pascal's triangle, each number is the sum of the two numbers directly above it. The edges of every row are always 1.", {})
    ])),
    N.para("Example: numRows = 5 → [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"),
    N.divider(),
]

# ── Solution 1: Bottom-Up DP (Interview Pick) ──────────────────────────────────
sol1_code = """def generate(numRows: int) -> list[list[int]]:
    result = [[1]]                         # Seed: row 0 is always [1]
    for i in range(1, numRows):            # Build each new row from the previous
        prev = result[-1]                  # Fetch the last completed row (our DP "state")
        new_row = [1]                      # Left edge is always 1 — C(i,0) = 1
        for j in range(1, len(prev)):      # Interior positions: j = 1 to i-1
            new_row.append(prev[j-1] + prev[j])  # DP transition: sum of two parents above
        new_row.append(1)                  # Right edge is always 1 — C(i,i) = 1
        result.append(new_row)             # Store completed row — becomes "prev" next iteration
    return result"""

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to construct a 2D triangle where every cell either equals 1 (edges) or the sum of the two cells above it. This is equivalent to: given the previous row, produce the next row by summing adjacent pairs and wrapping with 1s."),
        N.h4("What Doesn't Work"),
        N.para("Computing each cell as a binomial coefficient C(n,k) = n!/(k!(n-k)!) requires factorial arithmetic and risks integer overflow. It's also harder to implement correctly. The row-by-row approach is simpler and overflow-safe since we only use additions."),
        N.h4("The Key Observation"),
        N.para("Each row is FULLY determined by the previous row. To build row i, we only need row i-1. This means we can build the entire triangle iteratively, storing each completed row and using it to derive the next — classic bottom-up DP tabulation."),
        N.h4("Building the Solution"),
        N.para("1. Seed: result = [[1]] (row 0 is the base case). 2. For each row i ≥ 1: grab prev = result[-1], start new_row = [1], compute interior cells via prev[j-1]+prev[j], append final 1, store new_row. 3. Return result."),
        N.callout("Analogy: Think of each row as a 'layer' of a pyramid. Each brick (cell) rests on two bricks below it and takes their combined weight. The two corner bricks always weigh 1. We build layer by layer from the top down.", "🧱", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Row i is completely determined by row i-1. The subproblem answer (prev row) directly produces the larger answer (current row). No need to recompute earlier rows.", {})
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive C(n,k) = C(n-1,k-1) + C(n-1,k) without memoization recomputes the same cells exponentially. Our tabulation computes each cell exactly once.", {})
    ])),
    N.code("# The Recurrence Relation:\n# dp[i][0] = 1                         (left edge base case)\n# dp[i][j] = dp[i-1][j-1] + dp[i-1][j] (DP transition for interior cells)\n# dp[i][i] = 1                         (right edge base case)\n#\n# This is Pascal's Identity: C(n,k) = C(n-1,k-1) + C(n-1,k)", "python"),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("result = [[1]]", {"code": True}), (" — Seed the DP table with the base case: row 0 is always a single element [1].", {})])),
    N.para(N.rich([("for i in range(1, numRows):", {"code": True}), (" — Build rows 1 through numRows-1. Row 0 is already seeded.", {})])),
    N.para(N.rich([("prev = result[-1]", {"code": True}), (" — Look up the last completed row. This is the subproblem result we stored and are now re-using.", {})])),
    N.para(N.rich([("new_row = [1]", {"code": True}), (" — Start the new row with the left edge. C(i,0) = 1 always — there is exactly one way to choose 0 items from i.", {})])),
    N.para(N.rich([("for j in range(1, len(prev)):", {"code": True}), (" — Iterate over interior positions. For row i, len(prev)=i so this runs i-1 times (positions 1 through i-1).", {})])),
    N.para(N.rich([("new_row.append(prev[j-1] + prev[j])", {"code": True}), (" — The core DP transition. prev[j-1] is the upper-left parent; prev[j] is the upper-right parent. Their sum is C(i,j).", {})])),
    N.para(N.rich([("new_row.append(1)", {"code": True}), (" — Append the right edge. C(i,i) = 1 always — there is exactly one way to choose all i items from i.", {})])),
    N.para(N.rich([("result.append(new_row)", {"code": True}), (" — Store the completed row. It becomes 'prev' in the next iteration — the DP table grows by one row.", {})])),
    N.callout("Common Mistake: Using range(len(prev)-1) instead of range(1, len(prev)) for the inner loop. The correct range gives j from 1 to len(prev)-1 inclusive, producing i-1 interior cells. Combined with two edge 1s, new_row has i+1 elements — exactly right for row i.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Memoized Recursion ─────────────────────────────────────────────
sol2_code = """from functools import lru_cache

def generate(numRows: int) -> list[list[int]]:
    @lru_cache(maxsize=None)
    def C(n, k):                           # C(n,k) = Pascal's entry at row n, col k
        if k == 0 or k == n:               # Base cases: edges of the triangle
            return 1
        return C(n-1, k-1) + C(n-1, k)    # Pascal's Identity — sum of two parents

    return [[C(i, j) for j in range(i + 1)] for i in range(numRows)]"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each cell C(n,k) is defined recursively: C(n,k) = C(n-1,k-1) + C(n-1,k) with base cases C(n,0) = C(n,n) = 1. This is a direct translation of Pascal's Identity into a recursive function."),
        N.h4("What Doesn't Work"),
        N.para("Without caching (lru_cache), the naive recursion computes the same cell multiple times — exponential blowup. For example, C(4,2) would be re-expanded every time it's referenced, rather than looked up."),
        N.h4("The Key Observation"),
        N.para("There are only O(n²) unique (n,k) pairs in an n-row triangle. By caching each computed value, every cell is computed at most once — O(n²) total. Memoization converts exponential recursion into polynomial work."),
        N.h4("Building the Solution"),
        N.para("Define C(n,k) recursively. Use @lru_cache to memoize. Then build the result by calling C(i,j) for all valid (i,j) pairs. Python's lru_cache handles all the bookkeeping automatically."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Decorate C with Python's memoization. All calls with the same (n,k) return the cached result instantly after the first computation.", {})])),
    N.para(N.rich([("if k == 0 or k == n: return 1", {"code": True}), (" — Base cases: left edge (k=0) and right edge (k=n) are always 1.", {})])),
    N.para(N.rich([("return C(n-1, k-1) + C(n-1, k)", {"code": True}), (" — Pascal's Identity. Recursively sum upper-left and upper-right parents. With memoization, each unique (n,k) is computed once.", {})])),
    N.para(N.rich([("[[C(i,j) for j in range(i+1)] for i in range(numRows)]", {"code": True}), (" — Build the full triangle by calling C for every valid cell position.", {})])),
    N.divider(),
]

# ── Complexity Table ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Factorial C(n,k) formula", "O(n²)", "O(n²)", "Overflow risk, complex code"],
        ["Bottom-Up DP (Sol 1) ✓", "O(n²)", "O(n²)", "Optimal; interview pick"],
        ["Memoized Recursion (Sol 2)", "O(n²)", "O(n²)", "Same complexity, recursive overhead"],
        ["k-th row only (in-place)", "O(k²)", "O(k)", "Space optimal for #119 variant"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sum of Two Above (2D DP table-building; each row derived from previous row)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Problem says each value is the sum of two adjacent values from the row/level above. (2) Output is a 2D structure where each row depends entirely on the previous row. (3) Combinatorics problems with triangular/pyramidal form. (4) 'Return all rows' — the DP table is the answer itself.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sum of Two Above / 2D DP table-building):"),
    N.bullet(N.rich([("Pascal's Triangle II", {"bold": True}), (" (Easy) — Return only the k-th row; space optimization to O(k) using in-place right-to-left update (#119)", {})])),
    N.bullet(N.rich([("Triangle (Min Path Sum)", {"bold": True}), (" (Medium) — Find minimum-cost path from apex to base; each step moves to adjacent elements below; DP on triangle structure (#120)", {})])),
    N.bullet(N.rich([("Unique Paths", {"bold": True}), (" (Medium) — Count paths in m×n grid; DP table where each cell = cell above + cell to the left — same 'sum of neighbors' pattern (#62)", {})])),
    N.bullet(N.rich([("Unique Paths II", {"bold": True}), (" (Medium) — Unique Paths with obstacles blocking cells; same 2D DP pattern, set blocked cells to 0 (#63)", {})])),
    N.bullet(N.rich([("Minimum Path Sum", {"bold": True}), (" (Medium) — Minimize cost on a path from top-left to bottom-right of a grid; 2D DP with directional transitions (#64)", {})])),
    N.para("These problems share the core technique: each cell in a 2D structure is computed from neighboring previously-computed cells, building the answer bottom-up."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: Sum of Two Above. Source: Analysis + Guide Section 18.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer embed ─────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("pascals_triangle")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch each row being built cell by cell from its predecessor.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
