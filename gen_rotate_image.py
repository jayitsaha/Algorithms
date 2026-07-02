"""gen_rotate_image.py — Notion update for LeetCode #48 Rotate Image."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81c1-8d7b-c65fce3c4e3f"
SLUG = "rotate_image"

# Helper: inline code + plain text paragraph
def cline(code_text, rest):
    return N.para(N.rich([(code_text, {"code": True}), (rest, {})]))

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=48,
    pattern="Matrix",
    subpatterns=["Transpose + Reverse Rows"],
    tc="O(n^2)",
    sc="O(1)",
    key_insight="Transpose upper triangle then reverse each row — composing these equals 90 deg CW rotation in-place.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(
        "You are given an n x n 2D matrix representing an image. Rotate the matrix "
        "90 degrees clockwise in-place -- you must rotate the image without allocating "
        "another 2D matrix. Every cell matrix[i][j] maps to position matrix[j][n-1-i] "
        "after a 90 degree CW rotation."
    ),
    N.divider(),
]

# ── Solution 1 ──
SOL1_CODE = (
    "def rotate(matrix: list[list[int]]) -> None:\n"
    "    n = len(matrix)\n"
    "    # Step 1: Transpose -- reflect across main diagonal\n"
    "    for i in range(n):\n"
    "        for j in range(i + 1, n):   # upper triangle only\n"
    "            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n"
    "    # Step 2: Reverse each row in-place\n"
    "    for row in matrix:\n"
    "        row.reverse()\n"
)

blocks += [
    N.h2("Solution 1 -- Transpose + Reverse (Interview Pick)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to move every cell (i,j) to position (j, n-1-i) -- that is the 90 deg CW formula. "
            "The constraint is doing it without a second matrix."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The naive solution -- make a copy and apply the formula directly -- uses O(n^2) extra space, "
            "violating the in-place constraint. We need to find a sequence of in-place swaps."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A transpose maps (i,j) to (j,i). Reversing each row maps (j,i) to (j, n-1-i). "
            "Composing: (i,j) to (j, n-1-i). That is exactly the 90 deg CW formula. "
            "Both operations are trivially in-place."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: For each pair (i,j) where j > i (upper triangle only), swap matrix[i][j] with matrix[j][i]. "
            "Restricting to j > i ensures each pair is swapped exactly once -- iterating all j would swap "
            "each pair twice, undoing the work. "
            "Step 2: Iterate every row and call row.reverse()."
        ),
        N.callout(
            "Analogy: Fold a piece of paper along the diagonal (transpose), "
            "then flip it left-to-right (row reverse). The combination rotates content 90 deg clockwise.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    cline("n = len(matrix)", " -- get the dimension of the n x n square grid."),
    cline("for i in range(n):", " -- outer loop iterates row indices 0 to n-1."),
    cline("for j in range(i + 1, n):", " -- upper triangle only (j > i); avoids double-swapping each symmetric pair."),
    cline("matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]",
          " -- Python tuple swap exchanges both cells atomically; no temporary variable needed."),
    cline("for row in matrix:", " -- iterate all n rows after the full transpose is complete."),
    cline("row.reverse()",
          " -- Python built-in in-place reversal (two-pointer from ends to center). O(n) per row, O(n^2) total."),
    N.divider(),
]

# ── Solution 2 ──
SOL2_CODE = (
    "def rotate_extra(matrix: list[list[int]]) -> None:\n"
    '    """Brute-force: allocate copy, apply formula directly. O(n^2) space."""\n'
    "    n = len(matrix)\n"
    "    copy = [row[:] for row in matrix]   # deep copy\n"
    "    for i in range(n):\n"
    "        for j in range(n):\n"
    "            matrix[j][n - 1 - i] = copy[i][j]  # (i,j) -> (j, n-1-i)\n"
)

blocks += [
    N.h2("Solution 2 -- Extra Space, Direct Formula"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we allowed O(n^2) extra space, we could apply the rotation formula (i,j) to (j, n-1-i) directly from a copy."),
        N.h4("What Doesn't Work"),
        N.para("Reading from and writing to the same matrix causes values to be overwritten before being read. We must read from a copy."),
        N.h4("The Key Observation"),
        N.para("With a full copy, each destination cell can be written independently without conflicts."),
        N.h4("Building the Solution"),
        N.para("Deep-copy the matrix. For each (i,j), write copy[i][j] into matrix[j][n-1-i]. Simple and correct but O(n^2) space."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    cline("copy = [row[:] for row in matrix]",
          " -- shallow-copy each row into a new list (sufficient since elements are ints)."),
    cline("matrix[j][n-1-i] = copy[i][j]",
          " -- direct 90 deg CW formula. Reading from copy prevents clobbering unread values."),
    N.divider(),
]

# ── Solution 3 ──
SOL3_CODE = (
    "def rotate_layer(matrix: list[list[int]]) -> None:\n"
    '    """Layer-by-layer 4-cell cyclic swap. O(n^2) time, O(1) space."""\n'
    "    n = len(matrix)\n"
    "    for d in range(n // 2):            # layer depth\n"
    "        for k in range(d, n - 1 - d):  # position along edge\n"
    "            tmp = matrix[d][k]\n"
    "            matrix[d][k]         = matrix[n-1-k][d]\n"
    "            matrix[n-1-k][d]     = matrix[n-1-d][n-1-k]\n"
    "            matrix[n-1-d][n-1-k] = matrix[k][n-1-d]\n"
    "            matrix[k][n-1-d]     = tmp\n"
)

blocks += [
    N.h2("Solution 3 -- Layer-by-Layer Cyclic Swap"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think geometrically: a 90 deg CW rotation moves 4 cells in a cycle: top -> right -> bottom -> left -> top."),
        N.h4("What Doesn't Work"),
        N.para("Processing cells one-by-one without saving the displaced value causes overwriting. We need exactly one temporary variable for the 4-cell cycle."),
        N.h4("The Key Observation"),
        N.para("Process the matrix layer by layer (ring by ring) from outside in. Each group of 4 cells can be rotated with one temporary variable."),
        N.h4("Building the Solution"),
        N.para(
            "Outer loop: layer depth d from 0 to n//2-1. "
            "Inner loop: position k along the layer edge. "
            "Each iteration performs one 4-cell rotation: save top, shift left->top, bottom->left, right->bottom, saved top->right."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
    cline("for d in range(n // 2):", " -- process n//2 concentric rings. 3x3 has 1 ring; 4x4 has 2 rings."),
    cline("for k in range(d, n - 1 - d):", " -- positions along the current ring's edge."),
    cline("tmp = matrix[d][k]", " -- save the top-side value before the cycle begins."),
    cline("matrix[d][k] = matrix[n-1-k][d]", " -- move left side to top."),
    cline("matrix[n-1-k][d] = matrix[n-1-d][n-1-k]", " -- move bottom to left."),
    cline("matrix[n-1-d][n-1-k] = matrix[k][n-1-d]", " -- move right to bottom."),
    cline("matrix[k][n-1-d] = tmp", " -- move saved top to right. The 4-cell cycle is complete."),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Extra Space Copy", "O(n^2)", "O(n^2)"],
        ["Transpose + Reverse (Interview Pick)", "O(n^2)", "O(1)"],
        ["Layer Cyclic Swap", "O(n^2)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Matrix (2D Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Transpose + Reverse Rows", {})])),
    N.callout(
        "When to recognize this pattern: The problem says 'rotate n x n matrix in-place' or "
        "'no extra matrix'. Any in-place transformation of a square 2D grid involving rotation, "
        "flipping, or transposing. Signals: 'rotate 90 degrees', 'reflect across diagonal', 'flip image'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique (Matrix In-place Rotation / Transpose):"),
    N.bullet(N.rich([("Transpose Matrix", {"bold": True}), (" (Easy) -- Pure transpose: swap A[i][j] with A[j][i] for all i < j. (#867)", {})])),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}), (" (Medium) -- Traverse matrix along boundary layers shrinking inward. (#54)", {})])),
    N.bullet(N.rich([("Spiral Matrix II", {"bold": True}), (" (Medium) -- Fill matrix in spiral order using four-boundary tracking. (#59)", {})])),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}), (" (Medium) -- In-place marking using first row and column as sentinel flags. (#73)", {})])),
    N.bullet(N.rich([("Rotate Array", {"bold": True}), (" (Medium) -- 1D analogue: the reverse trick rotates elements in-place. (#189)", {})])),
    N.bullet(N.rich([("Game of Life", {"bold": True}), (" (Medium) -- In-place simulation encoding multi-state values per cell. (#289)", {})])),
    N.para(
        "These problems share the same core technique: in-place modification of a matrix or array "
        "using clever swap sequences, without allocating extra space proportional to input size."
    ),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md section 1.7 (Matrix / 2D Array). "
        "Sub-pattern 'Transpose + Reverse Rows' verified from Guide Section 1.7 table.",
        "📚", "gray_background"
    ),
]

# Interactive Explainer embed
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually -- use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
