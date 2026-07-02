"""
gen_transpose_matrix.py
Notion update for LeetCode #867 — Transpose Matrix
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8146-aaf5-d7d5e6e0a925"
SLUG = "transpose_matrix"

# ── 1. Set properties ──────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=867,
    pattern="Matrix",
    subpatterns=["Swap A[i][j] with A[j][i]"],
    tc="O(m×n)",
    sc="O(m×n)",
    key_insight="Every element at (i,j) maps to (j,i) in the output; allocate an n×m result and apply the swap rule in a double loop.",
    icon="🟢",
)
print("Properties set OK")

# ── 2. Wipe old body ─────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build new body ────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 2D integer array ", {}),
        ("matrix", {"code": True}),
        (", return the ", {}),
        ("transpose", {"bold": True}),
        (" of ", {}),
        ("matrix", {"code": True}),
        (". The transpose of a matrix is the matrix flipped over its main diagonal, "
         "switching the row and column indices of the matrix.\n\n"
         "Example:\n"
         "  Input:  matrix = [[1,2,3],[4,5,6]]\n"
         "  Output: [[1,4],[2,5],[3,6]]\n\n"
         "  Input:  matrix = [[1,2],[3,4]]\n"
         "  Output: [[1,3],[2,4]]", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Direct Index Mapping (Interview Pick) ──
SOLUTION1_CODE = """\
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    m, n = len(matrix), len(matrix[0])   # m=rows, n=cols of input
    result = [[0] * m for _ in range(n)] # allocate n×m output (dimensions flipped)
    for i in range(m):                   # iterate each row of input
        for j in range(n):               # iterate each col of input
            result[j][i] = matrix[i][j]  # swap indices: (i,j) → (j,i)
    return result                        # all n×m cells assigned exactly once
"""

blocks += [
    N.h2("Solution 1 — Direct Index Mapping (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to 'flip' the matrix over its diagonal. What does that actually mean? "
               "The element at row i, column j should end up at row j, column i. "
               "That's the entire problem — a single index-swap rule applied to every cell."),
        N.h4("What Doesn't Work"),
        N.para("Trying to modify the matrix in-place for non-square shapes fails immediately: "
               "a 3×2 matrix cannot be transposed to a 2×3 matrix in the same memory — "
               "you'd be writing out-of-bounds. Even for square matrices, naively swapping "
               "every (i,j) with (j,i) swaps things back — you'd undo each swap!"),
        N.h4("The Key Observation"),
        N.para("The transpose is defined as: T[j][i] = A[i][j]. This is a pure mapping — "
               "no conditional logic, no special cases. Allocate a new n×m matrix and "
               "apply this rule to every (i,j) pair. Done."),
        N.h4("Building the Solution"),
        N.para("1. Read m = len(matrix) and n = len(matrix[0]).\n"
               "2. Allocate result = [[0]*m for _ in range(n)] — n rows, m cols.\n"
               "3. Nested loop: for i in range(m), for j in range(n): result[j][i] = matrix[i][j].\n"
               "4. Return result."),
        N.callout(
            "Analogy: Think of the matrix printed on paper. Rotate it 90° and look at it "
            "from behind — that's transposition. Rows became columns and columns became rows.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(matrix), len(matrix[0])", {"code": True}),
                   (" — Read the dimensions. m is number of rows, n is number of columns.", {})])),
    N.para(N.rich([("result = [[0] * m for _ in range(n)]", {"code": True}),
                   (" — Allocate the output matrix. It has n rows (one per column of input) "
                    "and m columns (one per row of input). Dimensions are swapped.", {})])),
    N.para(N.rich([("for i in range(m):", {"code": True}),
                   (" — Outer loop over each row index i of the original matrix.", {})])),
    N.para(N.rich([("for j in range(n):", {"code": True}),
                   (" — Inner loop over each column index j of the original matrix.", {})])),
    N.para(N.rich([("result[j][i] = matrix[i][j]", {"code": True}),
                   (" — The core operation: read from (i,j), write to (j,i). "
                    "This is exactly the transpose definition T[j][i] = A[i][j].", {})])),
    N.para(N.rich([("return result", {"code": True}),
                   (" — All m×n cells have been assigned exactly once. Return the transposed matrix.", {})])),
    N.divider(),
]

# ── Solution 2 — zip one-liner ──
SOLUTION2_CODE = """\
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]
    # zip(*matrix): unpacks matrix rows as arguments to zip.
    # zip groups elements by position across iterables:
    #   first group: matrix[0][0], matrix[1][0], ... (column 0)
    #   second group: matrix[0][1], matrix[1][1], ... (column 1)
    # Each group becomes a row in the result — exactly transposition.
"""

blocks += [
    N.h2("Solution 2 — zip(*matrix) One-liner (Pythonic)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Transposing means: collect all column-j elements as row j of the result. "
               "In Python, zip(*iterables) does exactly this — it groups the k-th element "
               "of each iterable together."),
        N.h4("The Key Observation"),
        N.para("zip(*matrix) is Python's built-in transpose for sequences of equal length. "
               "The * operator unpacks the rows as separate arguments to zip, so zip "
               "receives the rows as individual iterables and groups by index position."),
        N.h4("Building the Solution"),
        N.para("zip(*matrix) returns tuples (immutable), so wrap with list() to get the "
               "expected output format: [list(row) for row in zip(*matrix)]."),
        N.callout(
            "Interview note: This one-liner is impressive but harder to explain under pressure. "
            "Start with Solution 1 (explicit loops), then offer this as a cleaner Python version.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("zip(*matrix)", {"code": True}),
                   (" — * unpacks matrix rows as separate arguments. zip groups elements "
                    "by position: the k-th element from each row forms a tuple. "
                    "These tuples are the columns of the original = rows of the transpose.", {})])),
    N.para(N.rich([("list(row)", {"code": True}),
                   (" — Convert each tuple from zip into a list, as required by the return type.", {})])),
    N.divider(),
]

# ── Solution 3 — In-place for square matrices ──
SOLUTION3_CODE = """\
def transpose_square(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)             # must be square: n×n
    for i in range(n):
        for j in range(i + 1, n):  # j > i: only upper triangle
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]  # swap
    return matrix               # modified in-place, O(1) extra space
"""

blocks += [
    N.h2("Solution 3 — In-place Swap (Square Matrices Only, O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For square n×n matrices (m == n), the dimensions don't change after transposing. "
               "Can we avoid allocating a new matrix? Yes — swap symmetric pairs in-place."),
        N.h4("The Key Observation"),
        N.para("The transpose requires swapping matrix[i][j] with matrix[j][i]. "
               "We only need to do this for cells in the upper triangle (where j > i). "
               "The lower triangle and diagonal are handled automatically by the swaps."),
        N.h4("What Doesn't Work"),
        N.para("If we loop j in range(n) instead of range(i+1, n), we'd process each pair twice: "
               "once to swap (i,j)↔(j,i), then again to swap (j,i)↔(i,j) — undoing the first swap."),
        N.callout(
            "Warning: This only works for square matrices. For non-square (m ≠ n), "
            "the result has different dimensions — impossible to achieve in-place.",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}),
                   (" — Starting j at i+1 ensures we only visit the upper triangle (j > i). "
                    "This prevents double-swapping pairs.", {})])),
    N.para(N.rich([("matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]", {"code": True}),
                   (" — Python tuple swap: simultaneously swaps both positions with no temp variable.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Direct Index Mapping (Sol 1)", "O(m×n)", "O(m×n) — new result matrix"],
        ["zip(*matrix) (Sol 2)", "O(m×n)", "O(m×n) — new result matrix"],
        ["In-place Square Only (Sol 3)", "O(n²)", "O(1) — no extra array"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Matrix", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Swap A[i][j] with A[j][i]", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to 'transpose', 'reflect over diagonal', or 'swap rows and columns'\n"
        "• Building block for rotation problems (rotate 90°/180°/270°)\n"
        "• Any problem where you need to change which dimension is 'outer' vs 'inner'\n"
        "• Key signal: the output dimensions are the flipped input dimensions",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related matrix transformation technique:"),
    N.bullet(N.rich([("Rotate Image", {"bold": True}),
                     (" (Medium) — Rotate n×n matrix 90° clockwise in-place: "
                      "transpose then reverse each row. Builds directly on this problem. (#48)", {})])),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}),
                     (" (Medium) — Traverse matrix elements in spiral order using direction tracking. "
                      "Requires careful row/col boundary management. (#54)", {})])),
    N.bullet(N.rich([("Spiral Matrix II", {"bold": True}),
                     (" (Medium) — Fill a matrix in spiral order; inverse of Spiral Matrix. (#59)", {})])),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}),
                     (" (Medium) — Zero out rows and columns containing 0, using first row/col "
                      "as markers for O(1) space. In-place matrix modification. (#73)", {})])),
    N.bullet(N.rich([("Diagonal Traverse", {"bold": True}),
                     (" (Medium) — Traverse elements along anti-diagonals alternating direction. "
                      "Pure index arithmetic with direction flip. (#498)", {})])),
    N.bullet(N.rich([("Flipping an Image", {"bold": True}),
                     (" (Easy) — Horizontally flip each row, then invert each bit. "
                      "Per-row transformation similar in spirit to transpose row processing. (#832)", {})])),
    N.para("These problems share the core technique of using index arithmetic to transform matrix coordinates."),
    N.callout(
        "📚 Sub-Pattern: Swap A[i][j] with A[j][i] — Source: Analysis (matrix index transposition)",
        "📚", "gray_background"
    ),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
