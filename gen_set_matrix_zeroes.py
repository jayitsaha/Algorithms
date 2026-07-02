"""gen_set_matrix_zeroes.py — Notion update for LeetCode #73 Set Matrix Zeroes"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81af-a466-dc355953721e"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=73,
    pattern="Matrix",
    subpatterns=["Use First Row/Col as Markers"],
    tc="O(m·n)",
    sc="O(1)",
    key_insight="Use first row/col as marker arrays; capture border flags before marking.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old body ──
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} blocks")

# ── 3. Build body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"bold": True}),
        (" integer matrix, if an element is ", {}),
        ("0", {"code": True}),
        (", set its entire row and column to ", {}),
        ("0", {"code": True}),
        (". You must do it ", {}),
        ("in-place", {"bold": True}),
        (".", {})
    ])),
    N.para("Example: matrix = [[1,1,1],[1,0,1],[1,1,1]] → output [[1,0,1],[0,0,0],[1,0,1]]. The zero at (1,1) causes all of row 1 and all of col 1 to become zero."),
    N.callout("Constraints: m, n ≥ 1. In-place: you cannot allocate a full m×n copy. Follow-up asks for O(1) space after the O(m) or O(m+n) solutions.", "📋", "gray_background"),
    N.divider(),
]

# Solution 1 — O(1) Space
sol1_code = '''def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    # Phase 1: Check if first row/col originally have zeros
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    # Phase 2: Use first row/col as marker storage for interior
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0   # mark row i
                matrix[0][j] = 0   # mark col j
    # Phase 3: Zero interior cells based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    # Phase 4: Handle the border
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0'''

blocks += [
    N.h2("Solution 1 — First Row/Col as Markers, O(1) Space (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to record which rows and which columns contain at least one original zero, then zero those rows and columns. If we had an array of m booleans (row flags) and n booleans (col flags), we'd be done in two passes. The challenge is doing it in O(1) extra space."),
        N.h4("What Doesn't Work"),
        N.para("Zeroing immediately while scanning causes cascading corruption: newly-written zeros look like original zeros to later iterations, triggering extra rows and columns to be zeroed. Two separate passes (collect then modify) fix this — but naively require O(m+n) extra space for two sets."),
        N.h4("The Key Observation"),
        N.para("The matrix already has a first row (n cells — one per column) and a first column (m cells — one per row). These can act as our boolean flag arrays! We just need two extra scalar booleans to record whether the first row and first column themselves had original zeros, since we'll be overwriting them with markers."),
        N.h4("Building the Solution"),
        N.para("Phase 1: Save two booleans (first_row_zero, first_col_zero) by scanning only the border. Phase 2: Scan interior cells; when we find a zero at (i,j), write matrix[i][0]=0 and matrix[0][j]=0 as markers. Phase 3: Re-scan interior; if matrix[i][0]=0 OR matrix[0][j]=0, set matrix[i][j]=0. Phase 4: If the border flags were True, zero the first row and first column."),
        N.callout("Analogy: Imagine checking a hotel ledger. Instead of a separate piece of paper, you write X on the room number's row and column in the existing table header. Then go back and cross out every cell whose row or column header has an X.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(matrix), len(matrix[0])", {"code": True}), (" — capture dimensions for iteration bounds.", {})])),
    N.para(N.rich([("first_row_zero = any(...)", {"code": True}), (" — scan row 0 for zeros BEFORE we write any markers there. Saved as a boolean.", {})])),
    N.para(N.rich([("first_col_zero = any(...)", {"code": True}), (" — scan col 0 for zeros BEFORE we write any row-markers there. Saved as a boolean.", {})])),
    N.para(N.rich([("for i in range(1, m) / for j in range(1, n)", {"code": True}), (" — Phase 2: iterate over interior cells only (skip border row/col which we use as storage).", {})])),
    N.para(N.rich([("if matrix[i][j] == 0:", {"code": True}), (" — found an original zero in the interior.", {})])),
    N.para(N.rich([("matrix[i][0] = 0", {"code": True}), (" — write row-marker: 'row i needs to be zeroed'. Column 0 is our row-flag array.", {})])),
    N.para(N.rich([("matrix[0][j] = 0", {"code": True}), (" — write col-marker: 'col j needs to be zeroed'. Row 0 is our col-flag array.", {})])),
    N.para(N.rich([("Phase 3 loop: if matrix[i][0]==0 or matrix[0][j]==0:", {"code": True}), (" — if row i is marked OR col j is marked, zero this interior cell.", {})])),
    N.para(N.rich([("if first_col_zero:", {"code": True}), (" — finally: if col 0 originally had a zero, zero the entire first column.", {})])),
    N.para(N.rich([("if first_row_zero:", {"code": True}), (" — if row 0 originally had a zero, zero the entire first row.", {})])),
    N.divider(),
]

# Solution 2 — O(m+n) Space
sol2_code = '''def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    zero_rows, zero_cols = set(), set()
    # Pass 1: collect all positions of original zeros
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_cols.add(j)
    # Pass 2: apply zeroing
    for i in range(m):
        for j in range(n):
            if i in zero_rows or j in zero_cols:
                matrix[i][j] = 0'''

blocks += [
    N.h2("Solution 2 — Two Sets, O(m+n) Space (Start Here in Interview)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need two pieces of information: which rows have a zero, and which columns have a zero. A set for rows and a set for columns captures this cleanly."),
        N.h4("What Doesn't Work"),
        N.para("Single-pass modification fails due to cascading. We need the complete set of zero positions before changing anything."),
        N.h4("The Key Observation"),
        N.para("Two passes solve it: collect all (row, col) of zeros into two sets in pass 1, then in pass 2 zero any cell whose row or column is in those sets."),
        N.h4("Building the Solution"),
        N.para("Initialize two empty sets. Scan every cell; add row index to zero_rows and col index to zero_cols when the cell is zero. Then re-scan every cell and zero it if its row or column index is in either set. Clean and correct."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("zero_rows, zero_cols = set(), set()", {"code": True}), (" — two sets to track which rows and columns contain at least one original zero.", {})])),
    N.para(N.rich([("Pass 1 loop", {"code": True}), (" — scan all m×n cells; when we find a zero, record both its row and column index.", {})])),
    N.para(N.rich([("zero_rows.add(i); zero_cols.add(j)", {"code": True}), (" — we record but do NOT modify the matrix — avoiding cascading.", {})])),
    N.para(N.rich([("Pass 2 loop", {"code": True}), (" — re-scan; if i in zero_rows or j in zero_cols, zero the cell.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two Sets (O(m+n) space)", "O(m·n)", "O(m+n)"],
        ["First Row/Col Markers (O(1) space)", "O(m·n)", "O(1)"],
        ["Naive (incorrect — cascades)", "O(m·n) but wrong", "O(1)"],
    ]),
    N.para("Both correct solutions visit each cell at most twice — O(m·n). The space difference is the key trade-off: two sets use O(m+n) auxiliary memory; the marker approach uses only two boolean scalars (O(1))."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Matrix", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Use First Row/Col as Markers", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks you to zero (or flag) entire rows and columns based on interior cell values, in-place with O(1) space. The first row and first column already have one cell per column and per row respectively — they are a natural home for boolean flags. Signal combination: 'm×n matrix · in-place · O(1) space · mark rows/columns'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or pattern:"),
    N.bullet(N.rich([("Rotate Image", {"bold": True}), (" (Medium) — In-place 90° clockwise rotation using transpose + reverse; another 'use the matrix itself' trick (#48).", {})])),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}), (" (Medium) — Layer-by-layer traversal with shrinking boundary tracking; in-place state needed (#54).", {})])),
    N.bullet(N.rich([("Game of Life", {"bold": True}), (" (Medium) — In-place cell update using multi-state encoding to avoid extra space — same principle as markers (#289).", {})])),
    N.bullet(N.rich([("Search a 2D Matrix", {"bold": True}), (" (Medium) — Binary search exploiting sorted row/col structure in a 2D grid (#74).", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — DFS/BFS on a 2D grid with in-place marking of visited cells (#200).", {})])),
    N.bullet(N.rich([("Transpose Matrix", {"bold": True}), (" (Easy) — Swap matrix[i][j] with matrix[j][i] across the diagonal — basic in-place matrix manipulation (#867).", {})])),
    N.para("These problems share the core technique: exploit existing matrix structure (border cells, diagonals, encoding) to avoid allocating auxiliary space."),
    N.divider(),
]

# Interactive Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("set_matrix_zeroes")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
