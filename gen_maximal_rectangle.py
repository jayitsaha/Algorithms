"""
gen_maximal_rectangle.py — Notion update for Maximal Rectangle (LC #85)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import notion_lib as N
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-812f-be46-f0c3374c7f95"

# ── 1) Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=85,
    pattern="Dynamic Programming",
    subpatterns=["Histogram per Row", "Monotonic Stack (Previous Smaller)"],
    tc="O(m·n)",
    sc="O(n)",
    key_insight="Build heights[] as DP (consecutive 1s per column); solve Largest Rectangle in Histogram on each row via monotonic stack.",
    icon="🔴"
)
print("  -> properties OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  -> wiped {wiped} blocks")

# ── 3) Build new body ──────────────────────────────────────────────────
print("Building body blocks...")

SOL1_CODE = '''\
def maximalRectangle(matrix):
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n   # DP: consecutive 1s ending at row i per column
    max_area = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0
        max_area = max(max_area, largestRect(heights))
    return max_area

def largestRect(heights):
    stack = [-1]   # sentinel: left boundary before column 0
    max_a = 0
    for i, h in enumerate(heights + [0]):  # append 0 to flush all bars
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width  = i - stack[-1] - 1
            max_a  = max(max_a, height * width)
        stack.append(i)
    return max_a
'''

SOL2_CODE = '''\
def maximalRectangle_v2(matrix):
    """Explicit 2D heights table — clearer DP structure, O(mn) space."""
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                heights[i][j] = (heights[i-1][j] + 1) if i > 0 else 1
    max_area = 0
    for i in range(m):
        max_area = max(max_area, largestRect(heights[i]))
    return max_area

def largestRect(heights):
    stack = [-1]
    max_a = 0
    for i, h in enumerate(heights + [0]):
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width  = i - stack[-1] - 1
            max_a  = max(max_a, height * width)
        stack.append(i)
    return max_a
'''

SOL3_CODE = '''\
def maximalRectangle_bf(matrix):
    """Brute force O(m^2 * n): fix top & bottom rows, count valid column runs."""
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    max_area = 0
    for top in range(m):
        col_ok = [True] * n
        for bot in range(top, m):
            for j in range(n):
                col_ok[j] = col_ok[j] and matrix[bot][j] == '1'
            consec = 0
            for j in range(n - 1, -1, -1):
                consec = consec + 1 if col_ok[j] else 0
                max_area = max(max_area, consec * (bot - top + 1))
    return max_area
'''

blocks = []

# ── Problem statement ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(
        "Given a rows x cols binary matrix filled with '0's and '1's, "
        "find the largest rectangle containing only '1's and return its area."
    ),
    N.para(
        'Example: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],'
        '["1","1","1","1","1"],["1","0","0","1","0"]] -> Output: 6'
    ),
    N.para(
        "Constraints: 1 <= rows, cols <= 200. matrix[i][j] is '0' or '1'."
    ),
    N.divider(),
]

# ── Why Is This DP? ──────────────────────────────────────────────────
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The maximum all-1s rectangle with bottom edge at row i is determined by the "
         "histogram of heights at row i. The height of column j at row i depends only on "
         "row i-1: it's heights[i-1][j]+1 if cell is '1', else 0. Each subproblem (column "
         "height) depends on exactly one prior subproblem.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Each heights[j] value (the column's consecutive-1s count) is computed once and "
         "reused across the entire row scan. Without DP, you'd recount streaks from scratch "
         "for every (top_row, bottom_row) pair — O(m^2*n) vs O(mn).", {}),
    ])),
    N.callout(
        N.rich([
            ("Key Reduction: ", {"bold": True}),
            ("Every maximal rectangle has a unique bottom row. When we fix row i as the "
             "bottom, the problem reduces to Largest Rectangle in Histogram on heights[]. "
             "Iterating all rows and solving LRH on each gives the global maximum.", {}),
        ]),
        "💡", "blue_background"
    ),
    N.code(
        "# DP Recurrence (height update):\n"
        "heights[j] = heights[j] + 1    if matrix[i][j] == '1'\n"
        "heights[j] = 0                  if matrix[i][j] == '0'\n\n"
        "# Area when popping index k from monotonic stack:\n"
        "height = heights[k]\n"
        "width  = current_i - stack[-1] - 1   # left boundary from stack sentinel\n"
        "area   = height * width",
        "python"
    ),
    N.divider(),
]

# ── Solution 1: DP Heights + Monotonic Stack ───────────────────────
blocks += [
    N.h2("Solution 1 — DP Heights + Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "An all-1s rectangle is defined by four edges. Instead of iterating all four, "
            "fix the bottom row and ask: 'What's the tallest all-1s bar above each column?' "
            "That gives a histogram. The answer for any fixed bottom row is the LRH answer."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force O(m^2*n^2): iterate all (top, bottom, left, right) tuples and "
            "verify all cells are '1'. Too slow. Even O(m^2*n) (fix top/bottom row only) "
            "is too slow for 200x200 grids."
        ),
        N.h4("The Key Observation"),
        N.para(
            "heights[j] = number of consecutive '1's directly above (and including) row i "
            "in column j. Computed with a single DP step per row. Row i now gives a histogram, "
            "and LRH on a histogram runs in O(n) with a monotonic stack."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Initialize heights = [0]*n. "
            "Step 2: For each row i, update heights[j] (+1 if '1', reset to 0 if '0'). "
            "Step 3: Run largestRect(heights) using a monotonic increasing stack. Pop bars "
            "when a shorter bar arrives; popped bar's height is the bottleneck in some span; "
            "width = current_pos - new_stack_top - 1. "
            "Step 4: Track global maximum."
        ),
        N.callout(
            "Analogy: Think of each row as 'ground level' and look up. The columns of 1s "
            "above each cell are buildings. LRH finds the largest rectangle you can fit in "
            "the city skyline seen from that row.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Monotonic Stack for LRH"),
    N.para(
        "The Largest Rectangle in Histogram problem (#84) is solved with a monotonic "
        "increasing stack. The invariant: the stack holds bar indices in non-decreasing "
        "order of height. When a shorter bar arrives, every popped bar was the minimum in "
        "the span [stack_top+1 ... current_i-1]. This span is exactly the widest rectangle "
        "where that bar's height is achievable."
    ),
    N.para(
        "Sentinel -1: Initialize stack with [-1] so that when the leftmost bar is popped, "
        "width = i - (-1) - 1 = i (extends all the way to position 0). "
        "Sentinel 0 appended to heights forces all remaining bars to be flushed at the end."
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("heights = [0] * n", {"code": True}),
        (" — DP state array. heights[j] = consecutive '1's ending at current row in column j. "
         "A '0' cell resets this to 0.", {}),
    ])),
    N.para(N.rich([
        ("heights[j] += 1", {"code": True}),
        (" — DP recurrence: extend the upward streak of '1's.", {}),
    ])),
    N.para(N.rich([
        ("heights[j] = 0", {"code": True}),
        (" — A '0' cell destroys the streak; column can't be part of any rectangle bottomed here.", {}),
    ])),
    N.para(N.rich([
        ("largestRect(heights)", {"code": True}),
        (" — Solve LRH on the current histogram. O(n) amortized (each index pushed/popped once).", {}),
    ])),
    N.para(N.rich([
        ("stack = [-1]", {"code": True}),
        (" — Sentinel at index -1. Prevents empty-stack errors; gives correct width for leftmost bars.", {}),
    ])),
    N.para(N.rich([
        ("heights + [0]", {"code": True}),
        (" — Append a zero-height sentinel. Forces all remaining bars off the stack at the end.", {}),
    ])),
    N.para(N.rich([
        ("while stack[-1] != -1 and heights[stack[-1]] >= h:", {"code": True}),
        (" — Pop bars taller than current. Popped bar's height is the bottleneck in some span.", {}),
    ])),
    N.para(N.rich([
        ("width = i - stack[-1] - 1", {"code": True}),
        (" — New stack top is the left boundary (exclusive). Width = right_exclusive - left_exclusive - 1.", {}),
    ])),
    N.divider(),
]

# ── Solution 2: Full 2D DP Heights ─────────────────────────────────
blocks += [
    N.h2("Solution 2 — Explicit 2D Heights Table (DP Tabulation)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of a rolling 1D heights array, build the full 2D table heights[i][j] "
            "upfront, then apply LRH per row. More memory, but clearer DP subproblem structure."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "O(m*n) space for the 2D table is acceptable but unnecessary. The rolling array "
            "(Solution 1) achieves O(n) space with the same time complexity."
        ),
        N.h4("The Key Observation"),
        N.para(
            "heights[i][j] = heights[i-1][j] + 1 if matrix[i][j]=='1', else 0. "
            "Straightforward recurrence with base case heights[0][j] = 1 if matrix[0][j]=='1'."
        ),
        N.h4("Building the Solution"),
        N.para("Fill heights[][] in O(mn). For each row, solve LRH(heights[i]) in O(n). Same O(mn) total."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("heights[i][j] = (heights[i-1][j] + 1) if i > 0 else 1", {"code": True}),
        (" — DP recurrence: height above (i,j) = height above (i-1,j) + 1 when cell is '1'. Base case row 0 = 1.", {}),
    ])),
    N.para(N.rich([
        ("for i in range(m): max_area = max(max_area, largestRect(heights[i]))", {"code": True}),
        (" — Apply LRH to each precomputed histogram row.", {}),
    ])),
    N.callout(
        "Memory Trade-off: O(mn) space vs O(n) for Solution 1. In interviews, Solution 1 is preferred. "
        "Solution 2 is excellent for explaining the DP subproblem structure before optimizing memory.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 3: Brute Force ─────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force Row-Pair (O(m^2 * n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Fix a top row and a bottom row. A rectangle spanning those rows must have all "
            "columns continuously '1' from top to bottom. Count the longest run of valid "
            "columns -> width. Height = bottom - top + 1."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "O(m^2*n^2): iterate all four boundaries and verify cells. Quadruple loop — too slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A column's validity is monotone when extending downward: once a '0' appears, it "
            "stays invalid. col_ok[] can be updated incrementally in O(n) per step."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each top row, maintain col_ok[]. Extend bottom row downward, updating col_ok. "
            "Scan right-to-left counting consecutive valid columns. Area = consec x height."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("col_ok = [True] * n", {"code": True}),
        (" — Reset validity tracker for each new top row.", {}),
    ])),
    N.para(N.rich([
        ("col_ok[j] = col_ok[j] and matrix[bot][j] == '1'", {"code": True}),
        (" — Column j stays valid only if all cells from top to bot are '1'. Once False, stays False.", {}),
    ])),
    N.para(N.rich([
        ("consec = consec+1 if col_ok[j] else 0", {"code": True}),
        (" — Count rightward run of valid columns (right-to-left). Area = consec x (bot-top+1).", {}),
    ])),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DP Heights + Monotonic Stack (S1)", "O(m*n)", "O(n)"],
        ["Explicit 2D Heights Table (S2)", "O(m*n)", "O(m*n)"],
        ["Brute Force Row-Pair (S3)", "O(m^2*n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([
        ("Main Pattern: ", {"bold": True}),
        ("Dynamic Programming", {}),
    ])),
    N.para(N.rich([
        ("Sub-Pattern(s): ", {"bold": True}),
        ("Histogram per Row | Monotonic Stack (Previous Smaller)", {}),
    ])),
    N.callout(
        "When to recognize this pattern: Binary matrix + 'find largest rectangle/square of 1s'. "
        "The row-by-row histogram reduction is the canonical technique. "
        "Any time you see LeetCode #84 as a subtask, think 2D grid extension. "
        "Monotonic stack applies whenever you need the 'span of dominance' of each element.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([
        ("Largest Rectangle in Histogram", {"bold": True}),
        (" (Hard) — Core subproblem #84. Master this first; Maximal Rectangle directly calls it.", {}),
    ])),
    N.bullet(N.rich([
        ("Maximal Square", {"bold": True}),
        (" (Medium) — Same 2D binary matrix but squares only; uses pure 2D DP without monotonic stack (#221).", {}),
    ])),
    N.bullet(N.rich([
        ("Trapping Rain Water", {"bold": True}),
        (" (Hard) — Monotonic stack for water trapped between bars (#42).", {}),
    ])),
    N.bullet(N.rich([
        ("Sum of Subarray Minimums", {"bold": True}),
        (" (Medium) — Monotonic stack for span-of-dominance of each element (#907).", {}),
    ])),
    N.bullet(N.rich([
        ("Count Submatrices With All Ones", {"bold": True}),
        (" (Medium) — Histogram approach counts rectangles vs finds the max (#1504).", {}),
    ])),
    N.bullet(N.rich([
        ("Maximum Width Ramp", {"bold": True}),
        (" (Medium) — Monotonic stack for span/dominance problems (#962).", {}),
    ])),
    N.para(
        "These problems share the core technique: reduce 2D problem to repeated 1D "
        "subproblems using DP state per column, solved via monotonic stack."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). "
        "Sub-Pattern: Histogram per Row. Source: Guide Section 18 + Analysis.",
        "📚", "gray_background"
    ),
]

# ── Visual Explainer ────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximal_rectangle")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

print(f"  -> total blocks: {len(blocks)}")
print("Appending blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
