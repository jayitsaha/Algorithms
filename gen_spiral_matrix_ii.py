"""
gen_spiral_matrix_ii.py — Notion update for LeetCode #59 Spiral Matrix II
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b0-aed3-f3b22eef4b89"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=59,
    pattern="Matrix",
    subpatterns=["Generate by Spiral Order"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="Four shrinking boundaries fill each spiral ring; shrink inward after every direction sweep.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build blocks ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a positive integer "), ("n", {"code": True}),
        (", generate an n×n matrix filled with elements from 1 to "),
        ("n²", {"code": True}),
        (" in spiral order (clockwise, starting from the top-left corner)."),
    ])),
    N.para("Example: n=3 → [[1,2,3],[8,9,4],[7,6,5]]"),
    N.divider(),
]

# ── Solution 1: Four-Boundary Simulation ──
solution1_code = """\
def generateMatrix(n: int) -> List[List[int]]:
    matrix = [[0]*n for _ in range(n)]   # n×n grid initialized to 0
    top, bottom, left, right = 0, n-1, 0, n-1  # four boundary pointers
    num = 1                                # next integer to place (1 → n²)
    while num <= n * n:                    # loop while unfilled cells remain
        for c in range(left, right+1):     # → fill top row left→right
            matrix[top][c] = num; num += 1
        top += 1                           # top row consumed; shrink down
        for r in range(top, bottom+1):     # ↓ fill right column top→bottom
            matrix[r][right] = num; num += 1
        right -= 1                         # right col consumed; shrink left
        for c in range(right, left-1, -1): # ← fill bottom row right→left
            matrix[bottom][c] = num; num += 1
        bottom -= 1                        # bottom row consumed; shrink up
        for r in range(bottom, top-1, -1): # ↑ fill left column bottom→top
            matrix[r][left] = num; num += 1
        left += 1                          # left col consumed; shrink right
    return matrix"""

blocks += [
    N.h2("Solution 1 — Four-Boundary Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to fill an n×n grid with integers 1..n² by tracing a clockwise spiral. The key reframe: a spiral is just four repeated straight-line sweeps (→ ↓ ← ↑) across the outermost unfilled ring, then the ring shrinks inward."),
        N.h4("What Doesn't Work"),
        N.para("Trying to track position and direction with a single pointer and turn logic (without boundaries) leads to messy edge-case handling — you must decide when to turn, which requires knowing the bounds of the unfilled region anyway."),
        N.h4("The Key Observation"),
        N.para("After sweeping a full edge (e.g., the top row), that row will NEVER be visited again. This lets us collapse a dimension immediately: increment top. We transform the 2D spiral problem into a series of 1D sweeps across shrinking boundaries."),
        N.h4("Building the Solution"),
        N.para("Initialize top=0, bottom=n-1, left=0, right=n-1, num=1. Loop: fill top row left→right (top+=1), right col top→bottom (right-=1), bottom row right→left (bottom-=1), left col bottom→top (left+=1). Repeat while num ≤ n²."),
        N.callout("Analogy: Peeling an onion. Each full rotation of → ↓ ← ↑ removes the outermost ring of the onion. Shrinking the boundaries is peeling off that layer.", "🧅", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("matrix = [[0]*n ...]", {"code": True}), " — Create the n×n output grid pre-filled with 0 (sentinel for 'not yet written')"])),
    N.para(N.rich([("top, bottom, left, right = 0, n-1, 0, n-1", {"code": True}), " — Four boundary pointers that define the rectangle of remaining unfilled cells"])),
    N.para(N.rich([("num = 1", {"code": True}), " — Counter for the next value to place; increments after every cell write"])),
    N.para(N.rich([("while num <= n * n:", {"code": True}), " — Loop while there are still cells to fill; terminates after exactly n² writes"])),
    N.para(N.rich([("for c in range(left, right+1):", {"code": True}), " — Sweep left→right across the current top boundary row"])),
    N.para(N.rich([("matrix[top][c] = num; num += 1", {"code": True}), " — Write the value and immediately advance the counter"])),
    N.para(N.rich([("top += 1", {"code": True}), " — The top row is fully consumed; pull the boundary down by 1"])),
    N.para(N.rich([("for r in range(top, bottom+1):", {"code": True}), " — Sweep top→bottom down the current right boundary column (note: uses updated top)"])),
    N.para(N.rich([("right -= 1", {"code": True}), " — Right column consumed; pull boundary left by 1"])),
    N.para(N.rich([("for c in range(right, left-1, -1):", {"code": True}), " — Sweep right→left across the current bottom row (uses updated right)"])),
    N.para(N.rich([("bottom -= 1", {"code": True}), " — Bottom row consumed; pull boundary up by 1"])),
    N.para(N.rich([("for r in range(bottom, top-1, -1):", {"code": True}), " — Sweep bottom→top up the current left column (uses updated bottom)"])),
    N.para(N.rich([("left += 1", {"code": True}), " — Left column consumed; pull boundary right by 1"])),
    N.para(N.rich([("return matrix", {"code": True}), " — Return the fully populated n×n spiral matrix"])),
    N.divider(),
]

# ── Solution 2: Direction Vector ──
solution2_code = """\
def generateMatrix(n: int) -> List[List[int]]:
    matrix = [[0]*n for _ in range(n)]
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]  # right, down, left, up
    d, r, c = 0, 0, 0                   # direction index, row, col
    for num in range(1, n*n+1):         # place values 1..n² in order
        matrix[r][c] = num
        nr = r + dirs[d][0]             # peek one step ahead
        nc = c + dirs[d][1]
        if not (0 <= nr < n and 0 <= nc < n and matrix[nr][nc] == 0):
            d = (d + 1) % 4             # turn clockwise if blocked
            nr = r + dirs[d][0]
            nc = c + dirs[d][1]
        r, c = nr, nc
    return matrix"""

blocks += [
    N.h2("Solution 2 — Direction Vector (Compact Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of tracking explicit boundaries, simulate a 'robot' that walks in a fixed direction, turns clockwise whenever blocked (out-of-bounds or already-filled cell), and places values as it goes."),
        N.h4("What Doesn't Work"),
        N.para("Naive simulation without a turn mechanism runs off the edge or overwrites cells. The solution: check one step ahead before moving; if blocked, rotate direction first."),
        N.h4("The Key Observation"),
        N.para("The four directions right→down→left→up form a cycle of period 4. Using (d+1)%4 as the direction index cleanly rotates clockwise. The already-filled cells (nonzero values) serve as a natural 'visited' marker — no separate visited array needed."),
        N.h4("Building the Solution"),
        N.para("Encode directions as (dr, dc) tuples. For each num from 1 to n²: write the value, look ahead, if blocked rotate direction index, then move. The for-loop over num guarantees exactly n² cells are written."),
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dirs = [(0,1),(1,0),(0,-1),(-1,0)]", {"code": True}), " — The four unit-step direction vectors: right, down, left, up"])),
    N.para(N.rich([("d, r, c = 0, 0, 0", {"code": True}), " — Start at direction index 0 (right), position (0,0)"])),
    N.para(N.rich([("for num in range(1, n*n+1):", {"code": True}), " — Iterate over the exact n² values to place"])),
    N.para(N.rich([("matrix[r][c] = num", {"code": True}), " — Write current value to current position"])),
    N.para(N.rich([("nr = r + dirs[d][0]; nc = c + dirs[d][1]", {"code": True}), " — Compute next position in current direction"])),
    N.para(N.rich([("if not (0<=nr<n and 0<=nc<n and matrix[nr][nc]==0):", {"code": True}), " — Check if next cell is valid (in bounds and unwritten)"])),
    N.para(N.rich([("d = (d + 1) % 4", {"code": True}), " — If blocked, rotate clockwise to next direction"])),
    N.para(N.rich([("r, c = nr, nc", {"code": True}), " — Move to the next position (using updated direction if we turned)"])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (Aux)", "Notes"],
        ["Four-Boundary (Optimal)", "O(n²)", "O(1)", "Each cell written exactly once; 4 int variables"],
        ["Direction Vector", "O(n²)", "O(1)", "Same; direction array is constant size"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Matrix (Section 1.7 — 2D Array Manipulation)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Generate by Spiral Order — fill a matrix cell-by-cell following a clockwise spiral path, shrinking boundaries after each ring edge"])),
    N.callout(
        "When to recognize this pattern: 'Fill/generate a matrix in spiral/clockwise order' — "
        "four shrinking boundaries, one sweep per direction, shrink after each sweep. "
        "Also applies to 'traverse the outermost ring, then next ring inward'. "
        "Signal: sequential fill of a 2D structure with a rotating direction.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (spiral traversal / matrix simulation):"),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}), " (Medium, #54) — Read the spiral order of an existing m×n matrix; same boundaries but read instead of write; add mid-loop guards for non-square input"])),
    N.bullet(N.rich([("Rotate Image", {"bold": True}), " (Medium, #48) — Rotate n×n matrix 90° clockwise in-place: transpose then reverse each row; pure matrix manipulation"])),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}), " (Medium, #73) — If matrix[i][j]==0, zero out its row and column; use first row/col as markers to achieve O(1) extra space"])),
    N.bullet(N.rich([("Diagonal Traverse", {"bold": True}), " (Medium, #498) — Walk anti-diagonals alternating up-right and down-left; i+j groups anti-diagonals"])),
    N.bullet(N.rich([("Game of Life", {"bold": True}), " (Medium, #289) — Simulate 2D board transitions in-place using encoded multi-state values to track old and new states simultaneously"])),
    N.bullet(N.rich([("Transpose Matrix", {"bold": True}), " (Easy, #867) — Swap A[i][j] and A[j][i]; foundational matrix operation underlying rotation"])),
    N.para("These problems all involve systematically traversing or generating a 2D grid with a structured positional discipline (boundaries, layers, or direction cycles)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.7 — 'Generate by Spiral Order' sub-pattern", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("spiral_matrix_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("Notion blocks appended.")
print("NOTION OK", PAGE_ID)
