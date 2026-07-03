"""
gen_maximal_rectangle.py — Notion update for Maximal Rectangle (LC #85)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Override token in notion_lib since it was redacted
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
print("  → properties OK")

# ── 2) Wipe old body ───────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  → wiped {wiped} blocks")

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
    stack = [-1]   # sentinel: left boundary before col 0
    max_a = 0
    for i, h in enumerate(heights + [0]):   # append 0 to flush all bars
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width  = i - stack[-1] - 1     # span where height was the min
            max_a  = max(max_a, height * width)
        stack.append(i)
    return max_a
'''

SOL2_CODE = '''\
def maximalRectangle_bf(matrix):
    """O(m^2 * n) brute force using row-pair DP."""
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    max_area = 0
    for top in range(m):
        col_ok = [True] * n  # column still all-1s from top to current bottom?
        for bot in range(top, m):
            for j in range(n):
                col_ok[j] = col_ok[j] and (matrix[bot][j] == '1')
            consec = 0
            for j in range(n - 1, -1, -1):
                consec = consec + 1 if col_ok[j] else 0
                max_area = max(max_area, consec * (bot - top + 1))
    return max_area
'''

SOL3_CODE = '''\
# Memoization (top-down) variant — same O(mn) idea, recursive
# Not commonly used for this problem (bottom-up is cleaner),
# but illustrates the subproblem structure.
from functools import lru_cache

def maximalRectangle_memo(matrix):
    if not matrix or not matrix[0]: return 0
    m, n = len(matrix), len(matrix[0])

    # Precompute heights: height[i][j] = consecutive 1s above (i,j)
    heights = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                heights[i][j] = (heights[i-1][j] + 1) if i > 0 else 1

    # For each row, solve LRH on heights[i]
    ans = 0
    for i in range(m):
        ans = max(ans, largestRect(heights[i]))
    return ans
'''

RECURRENCE = '''\
Height DP:
  heights[j] += 1  if matrix[i][j] == '1'
  heights[j]  = 0  if matrix[i][j] == '0'

Area when popping index k from stack:
  height = heights[k]
  width  = current_i - stack_top_after_pop - 1
  area   = height * width
'''

blocks = []

# ── Problem statement ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an ", ("m × n", {"bold": True}), " binary matrix of ",
        ("'0'", {"code": True}), "s and ", ("'1'", {"code": True}),
        "s, find the largest rectangle containing only ", ("'1'", {"code": True}),
        "s and return its area.\n\n"
        "Example: matrix = [['1','0','1','0','0'],['1','0','1','1','1'],"
        "['1','1','1','1','1'],['1','0','0','1','0']] → Output: 6"
    ])),
    N.divider(),
]

# ── Solution 1: DP Heights + Monotonic Stack (Interview Pick) ──────────
blocks += [
    N.h2("Solution 1 — DP Heights + Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every valid all-1s rectangle has a bottom row. Fix that bottom row and ask: what is the maximum height (consecutive 1s) in each column directly above it? That gives a histogram. The maximal rectangle with that bottom row equals the Largest Rectangle in Histogram (LRH) for that histogram."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try every pair of top-left and bottom-right corners and verify all cells. O(m²n²). A slight improvement: fix the top row and extend the bottom — O(m²n). Still too slow for large grids."),
        N.h4("The Key Observation"),
        N.para("The 2D problem reduces to m repeated 1D problems. Heights are computed via simple DP: heights[j] += 1 if cell is '1', else heights[j] = 0. Each 1D histogram can be solved in O(n) with a monotonic stack. Total: O(mn)."),
        N.h4("Building the Solution"),
        N.para("Step 1: Maintain heights[] array (length n, all zeros initially). Step 2: For each row i, update heights using the DP recurrence. Step 3: Run largestRect(heights) using a monotonic increasing stack. Step 4: Return the max area seen across all rows."),
        N.callout(
            "Analogy: Think of each row as the ground floor of a city skyline. "
            "heights[] gives the skyscraper heights at that ground level. "
            "Largest Rectangle in Histogram finds the biggest billboard that fits in the skyline.",
            "🏙️", "blue_background"
        ),
    ]),
    N.h3("Why Is This DP?"),
    N.para(N.rich([
        ("Optimal substructure: ", {"bold": True}),
        "heights[i][j] = heights[i-1][j] + 1 if matrix[i][j]=='1' else 0. Each cell's height depends only on the previous row's height.\n",
        ("Overlapping subproblems: ", {"bold": True}),
        "The heights array is reused across all histogram queries — we're not recomputing streaks from scratch each time."
    ])),
    N.callout(RECURRENCE, "📐", "gray_background"),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heights = [0] * n", {"code": True}), " — DP state: bar height per column, initialized to zero before any row is processed."])),
    N.para(N.rich([("if matrix[i][j] == '1': heights[j] += 1", {"code": True}), " — Extend the upward streak for this column by one."])),
    N.para(N.rich([("else: heights[j] = 0", {"code": True}), " — A '0' cell breaks the streak entirely. No rectangle can pass through a zero cell."])),
    N.para(N.rich([("max_area = max(max_area, largestRect(heights))", {"code": True}), " — Solve the histogram for this row and update the global maximum."])),
    N.para(N.rich([("stack = [-1]", {"code": True}), " — Sentinel index. When a bar is the leftmost, width = i - (-1) - 1 = i (full span to the left edge)."])),
    N.para(N.rich([("heights + [0]", {"code": True}), " — The appended 0 acts as a sentinel bar that forces all remaining bars to be popped and computed at the end."])),
    N.para(N.rich([("while stack[-1] != -1 and heights[stack[-1]] >= h:", {"code": True}), " — Pop while the bar on stack top is taller or equal to the current bar. We use >= to handle equal heights correctly."])),
    N.para(N.rich([("width = i - stack[-1] - 1", {"code": True}), " — After popping, the new stack top is the left boundary. Width = distance from new top + 1 to i - 1."])),
    N.para(N.rich([("max_a = max(max_a, height * width)", {"code": True}), " — Rectangle area with the popped bar as the height bottleneck."])),
    N.callout(
        "⚠️ Why heights[stack[-1]] >= h (not >)? "
        "Using >= ensures equal-height bars don't stack up incorrectly. "
        "When two adjacent bars have the same height, we pop the earlier one — "
        "its area will be recomputed correctly through the later bar's span.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Brute Force DP ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Row-Pair DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Fix the top row of the rectangle. Expand the bottom row downward one at a time. For each (top, bottom) pair, find the widest rectangle of all-1s columns spanning that height."),
        N.h4("What Doesn't Work"),
        N.para("Pure brute force checking every (top-left, bottom-right) corner pair: O(m²n²). This approach is only slightly better at O(m²n)."),
        N.h4("The Key Observation"),
        N.para("When we expand the bottom row, we can update which columns are still all-1s incrementally. A column is 'valid' for a (top, bottom) pair if every cell from top to bottom in that column is '1'. We can track this with a boolean array."),
        N.h4("Building the Solution"),
        N.para("For each top row, reset col_ok[j]=True for all j. For each bottom row: update col_ok[j] = col_ok[j] AND (matrix[bot][j]=='1'). Then scan from right to left counting consecutive valid columns and computing area."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("col_ok = [True] * n", {"code": True}), " — Tracks whether column j is all-1s from the current top row to the current bottom row."])),
    N.para(N.rich([("col_ok[j] = col_ok[j] and matrix[bot][j] == '1'", {"code": True}), " — Once a column hits a '0', it stays invalid for all further bottom extensions."])),
    N.para(N.rich([("consec * (bot - top + 1)", {"code": True}), " — Area = consecutive valid columns × height of the row range. We scan right-to-left so consec counts valid columns ending at position j."])),
    N.divider(),
]

# ── Solution 3: Memoization variant ───────────────────────────────────
blocks += [
    N.h2("Solution 3 — Top-Down (Precomputed Heights + Histogram)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Precompute the full heights table heights[i][j] = consecutive 1s above row i in column j (including row i). Then for each row, run the LRH algorithm on heights[i]. Same idea as Solution 1, but with explicit 2D precomputation instead of rolling update."),
        N.h4("The Key Observation"),
        N.para("Separating the precomputation from the histogram solving makes the DP structure explicit. heights[i][j] = heights[i-1][j]+1 if matrix[i][j]=='1' else 0. This is the same recurrence, made visible as a 2D table."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.callout(
        "This variant is useful for understanding: the 2D heights table is the explicit DP table. "
        "Solution 1's rolling update is just space-optimized: since each row only needs the previous row's heights, we can use O(n) instead of O(mn).",
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DP Heights + Monotonic Stack", "O(m·n)", "O(n)", "Interview pick — optimal"],
        ["Brute Force Row-Pair DP", "O(m²·n)", "O(n)", "Correct but TLEs on large input"],
        ["Pure Brute Force", "O(m²·n²)", "O(1)", "Correct, only for tiny grids"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Histogram per Row; Monotonic Stack (Previous Smaller)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Largest rectangle in binary matrix' → histogram reduction\n"
        "• 2D grid problem where each row can be treated as a 1D histogram base\n"
        "• 'Monotonic stack for span/dominance' → each bar's maximal span\n"
        "• Problem mentions DP + stack combination for 2D optimization",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (histogram DP / monotonic stack):"),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — The exact subproblem we solve per row. Master #84 before tackling #85."])),
    N.bullet(N.rich([("Maximal Square", {"bold": True}), " (Medium) — Largest all-1s square in binary matrix. Pure 2D DP, no stack needed. (#221)"])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Monotonic stack for 'water trapped between bars'. Same pop-and-compute mechanics. (#42)"])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — Monotonic stack to find each element's span as the minimum. (#907)"])),
    N.bullet(N.rich([("Maximum Width Ramp", {"bold": True}), " (Medium) — Monotonic stack for dominance/span problems. (#962)"])),
    N.bullet(N.rich([("Count Submatrices With All Ones", {"bold": True}), " (Medium) — Extends histogram counting to number of rectangles. (#1504)"])),
    N.para("These problems share the core technique: monotonic stack to efficiently compute for each bar the maximal span where it is the minimum/maximum."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Dynamic Programming → Histogram per Row; Section: Stack → Monotonic Stack (Previous Smaller)", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximal_rectangle")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
