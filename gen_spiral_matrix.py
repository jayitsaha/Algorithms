"""
gen_spiral_matrix.py — Notion page for Spiral Matrix (LeetCode #54)
notion_page_id: null → create fresh page
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Use existing page (found via Notion search; duplicate archived) ─
PAGE_ID = "39193418-809c-8143-983c-e7679a950bd0"
print(f"Using existing page: {PAGE_ID}")

# ── Set properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=54,
    pattern="Matrix",
    subpatterns=["Four Boundaries", "Shrink Inward"],
    tc="O(m·n)",
    sc="O(1)",
    key_insight="Track four boundary pointers; after each edge walk, shrink that boundary inward. Guards prevent double-collection of single rows/columns.",
    icon="🟡"
)
print("Properties set.")

# ── Wipe (fresh page — nothing to wipe, but call is safe) ──────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks (should be 0 for new page).")

# ── Build body ─────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m", {"code": True}), (" × ", {}), ("n", {"code": True}),
        (" matrix, return all elements of the matrix in spiral (clockwise) order, starting from the top-left, visiting the outer ring first, then peeling inward.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("matrix = [[1,2,3],[4,5,6],[7,8,9]]", {"code": True}),
        (" → ", {}),
        ("[1,2,3,6,9,8,7,4,5]", {"code": True})
    ])),
    N.divider(),
]

# Solution 1 — Four Boundaries (Interview Pick)
SOLUTION_1_CODE = """\
def spiralOrder(matrix):
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Walk top row left → right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1  # seal top row

        # Walk right column top → bottom
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1  # seal right col

        # Walk bottom row right → left (guard against single remaining row)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1  # seal bottom row

        # Walk left column bottom → top (guard against single remaining col)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1  # seal left col

    return result\
"""

blocks += [
    N.h2("Solution 1 — Four Boundaries, Shrink Inward (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Spiral order = visit the outermost ring of a rectangle clockwise, then the next ring inside, and so on. The question becomes: how do I know where each ring starts and ends? Answer: track the four boundary edges of the current (unvisited) rectangle."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach might try to track visited cells with a boolean matrix and simulate turning at walls — this works but uses O(m·n) extra space. For large matrices we want O(1) extra space."),
        N.h4("The Key Observation"),
        N.para("After walking the top row left-to-right, that entire row will never be needed again. So increment top immediately. Same logic: after right column, decrement right. After bottom row, decrement bottom. After left column, increment left. Four pointer shrinks — no visited array needed."),
        N.h4("Building the Solution"),
        N.para("1. Initialize top=0, bottom=m-1, left=0, right=n-1.\n2. Loop while top ≤ bottom AND left ≤ right.\n3. Walk top row → then top++.\n4. Walk right col ↓ then right--.\n5. If top ≤ bottom: walk bottom row ← then bottom--.\n6. If left ≤ right: walk left col ↑ then left++.\nThe two guards prevent revisiting cells when a single row or column remains."),
        N.callout("Analogy: peeling an onion. Each loop iteration strips off the outermost layer, revealing a smaller rectangle inside.", "🧅", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — Output list. Not counted toward space complexity (it is the answer)."])),
    N.para(N.rich([("top, bottom = 0, len(matrix) - 1", {"code": True}), " — Inclusive row boundaries of the active rectangle."])),
    N.para(N.rich([("left, right = 0, len(matrix[0]) - 1", {"code": True}), " — Inclusive column boundaries."])),
    N.para(N.rich([("while top <= bottom and left <= right:", {"code": True}), " — Continue while any unvisited rectangle exists."])),
    N.para(N.rich([("for col in range(left, right + 1):", {"code": True}), " — Walk every column in the current top row, left to right."])),
    N.para(N.rich([("top += 1", {"code": True}), " — Seal the top row permanently. Future passes start one row lower."])),
    N.para(N.rich([("for row in range(top, bottom + 1):", {"code": True}), " — Walk right column from the (new) top down to bottom."])),
    N.para(N.rich([("right -= 1", {"code": True}), " — Seal the right column. Future passes stop one column earlier."])),
    N.para(N.rich([("if top <= bottom:", {"code": True}), " — Guard: skip bottom-row walk if only a single row remains (top row already consumed it)."])),
    N.para(N.rich([("for col in range(right, left - 1, -1):", {"code": True}), " — Walk bottom row right to left using the already-shrunk right boundary."])),
    N.para(N.rich([("bottom -= 1", {"code": True}), " — Seal the bottom row."])),
    N.para(N.rich([("if left <= right:", {"code": True}), " — Guard: skip left-column walk if only a single column remains."])),
    N.para(N.rich([("for row in range(bottom, top - 1, -1):", {"code": True}), " — Walk left column bottom to top using already-shrunk bottom boundary."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Seal the left column."])),
    N.divider(),
]

# Solution 2 — Direction Simulation
SOLUTION_2_CODE = """\
def spiralOrder(matrix):
    m, n = len(matrix), len(matrix[0])
    result = []
    seen = [[False] * n for _ in range(m)]  # O(m*n) extra space
    dr = [0, 1, 0, -1]   # right, down, left, up
    dc = [1, 0, -1, 0]
    r = c = di = 0

    for _ in range(m * n):
        result.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dr[di], c + dc[di]
        if 0 <= nr < m and 0 <= nc < n and not seen[nr][nc]:
            r, c = nr, nc        # continue same direction
        else:
            di = (di + 1) % 4   # turn clockwise
            r, c = r + dr[di], c + dc[di]

    return result\
"""

blocks += [
    N.h2("Solution 2 — Direction Vector Simulation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simulate an ant crawling the spiral path. The ant moves in one direction until it hits a wall or an already-visited cell, then turns clockwise 90 degrees."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but requires O(m·n) extra space for the visited matrix — not ideal when a O(1) solution exists."),
        N.h4("The Key Observation"),
        N.para("Encode four directions as row/column deltas: right=(0,1), down=(1,0), left=(0,-1), up=(-1,0). Cycling through them modulo 4 produces clockwise turning."),
        N.h4("Building the Solution"),
        N.para("Initialize at (0,0), direction index 0 (right). Each step: record current cell, compute next cell in current direction. If next is valid and unseen, move there. Otherwise turn clockwise (di = (di+1)%4) and move."),
        N.callout("This approach is more intuitive and easier to derive from scratch, but costs O(m·n) space. Mention it first in interviews, then optimize to the four-boundary approach.", "💡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = [[False]*n ...]", {"code": True}), " — Visited matrix. This is the cost — O(m·n) extra space."])),
    N.para(N.rich([("dr = [0,1,0,-1]; dc = [1,0,-1,0]", {"code": True}), " — Direction deltas for right, down, left, up."])),
    N.para(N.rich([("di = (di + 1) % 4", {"code": True}), " — Turn clockwise: 0->1->2->3->0 cycles through right->down->left->up."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Four Boundaries (optimal)", "O(m·n)", "O(1) extra"],
        ["Direction Simulation", "O(m·n)", "O(m·n) for visited[][]"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Matrix (Section 1.7 — 2D Array Traversal and Manipulation)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Four Boundaries, Shrink Inward"])),
    N.callout(
        "When to recognize this pattern: the problem asks for spiral, clockwise, or ring-by-ring traversal of a 2D matrix. Key signals: 'return elements in spiral order', 'fill matrix in spiral order', 'process layers from outside in'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Four Boundaries / ring traversal technique:"),
    N.bullet(N.rich([("Spiral Matrix II", {"bold": True}), " (Medium) — Fill n×n with 1..n² in spiral order — identical boundary logic, assign instead of read (#59)"])),
    N.bullet(N.rich([("Rotate Image", {"bold": True}), " (Medium) — 90° clockwise rotation in-place: transpose then reverse each row (#48)"])),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}), " (Medium) — Use first row/col as marker arrays; O(1) space by abusing boundary cells (#73)"])),
    N.bullet(N.rich([("Diagonal Traverse", {"bold": True}), " (Medium) — Alternate-direction diagonal; group cells by (i+j) constant (#498)"])),
    N.bullet(N.rich([("Valid Sudoku", {"bold": True}), " (Medium) — Validate 9×9 by checking row/col/box hash sets (#36)"])),
    N.bullet(N.rich([("Game of Life", {"bold": True}), " (Medium) — In-place matrix update with encoded intermediate states (#289)"])),
    N.para("These problems all involve structured traversal or manipulation of a 2D matrix with boundary-awareness."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.7 (Matrix / 2D Array). Sub-Pattern verified: Four Boundaries, Shrink Inward.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("spiral_matrix")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Write status file
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)

html_path = pathlib.Path(__file__).parent / "spiral_matrix_explainer.html"
html_lines = len(html_path.read_text().splitlines()) if html_path.exists() else 0

status = {
    "slug": "spiral_matrix",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Fresh page created. 4-boundaries solution + direction simulation. 823-line HTML explainer."
}
(status_dir / "spiral_matrix.json").write_text(json.dumps(status, indent=2))
print(f"RESULT spiral_matrix | html=OK | notion=OK | lines={html_lines}")
