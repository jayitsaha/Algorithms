"""
gen_diagonal_traverse.py
Creates the Diagonal Traverse (LC #498) Notion page from scratch.
notion_page_id = null → create a new page.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Use the already-created page ────────────────────────────────────
# Page was created in the first run; use the returned ID directly.
PAGE_ID = "39193418-809c-8125-8b40-e85a4bb8af75"
print(f"Using page: {PAGE_ID}")

# ── Step 1: Set properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=498,
    pattern="Matrix",
    subpatterns=["Diagonal Groups", "Alternate Direction"],
    tc="O(m·n)",
    sc="O(min(m,n))",
    key_insight="Cells with the same r+c form one anti-diagonal; even diagonals go up-right (reverse collected order), odd go down-left.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Build body blocks ─────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"code": True}),
        (" matrix ", {}),
        ("mat", {"code": True}),
        (", return all elements of ", {}),
        ("mat", {"code": True}),
        (" in diagonal order. Traverse each anti-diagonal alternating direction: "
         "even-indexed diagonals go up-right (↗), odd-indexed go down-left (↙). "
         "An anti-diagonal is the set of cells where r+c is constant.", {})
    ])),
    N.para(N.rich([
        ("Example: mat=[[1,2,3],[4,5,6],[7,8,9]] → [1,2,4,7,5,3,6,8,9]", {"code": True})
    ])),
    N.divider(),
]

# ── Solution 1: Diagonal Groups (Interview Pick) ──────────────────────────────
blocks += [
    N.h2("Solution 1 — Diagonal Groups + Reverse (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of thinking about movement direction, think about grouping. "
               "Which cells share a diagonal? All cells (r, c) where r+c is the same value. "
               "That single observation restructures the whole problem."),
        N.h4("What Doesn't Work"),
        N.para("Naive simulation: track current position and a direction flag, then update "
               "direction on every boundary hit. This requires handling 4 boundary types "
               "(top, bottom, left, right walls) with correct priority at corners — easy to "
               "get one case wrong under interview pressure."),
        N.h4("The Key Observation"),
        N.para("r + c is constant along every anti-diagonal. For an m×n matrix, r+c ranges "
               "from 0 to m+n-2, giving exactly m+n-1 diagonals. Even-indexed diagonals "
               "should go up-right in the output; odd-indexed down-left. If we always collect "
               "in down-left order (r increases), we just reverse even diagonals. That's one "
               "if-statement instead of complex boundary logic."),
        N.h4("Building the Solution"),
        N.para("For diagonal d: the valid rows are r_start = max(0, d-(n-1)) to "
               "r_end = min(d, m-1). The column is c = d - r. Collect mat[r][d-r] for all "
               "valid r, then reverse if d is even. Append to result."),
        N.callout(
            "Analogy: Imagine anti-diagonals as rows in a tilted grid. Collect each "
            "'tilted row' top-to-bottom, then optionally flip it before outputting. "
            "The flip rule is just 'even diagonals flip' — one rule, all cases handled.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def findDiagonalOrder(mat):\n"
        "    m, n = len(mat), len(mat[0])\n"
        "    result = []\n"
        "    for d in range(m + n - 1):\n"
        "        diag = []\n"
        "        r = max(0, d - (n - 1))\n"
        "        while r <= min(d, m - 1):\n"
        "            diag.append(mat[r][d - r])\n"
        "            r += 1\n"
        "        if d % 2 == 0:\n"
        "            diag.reverse()\n"
        "        result.extend(diag)\n"
        "    return result"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(mat), len(mat[0])", {"code": True}),
                   (" — capture matrix dimensions upfront.", {})])),
    N.para(N.rich([("result = []", {"code": True}),
                   (" — output array, built one diagonal at a time.", {})])),
    N.para(N.rich([("for d in range(m + n - 1):", {"code": True}),
                   (" — d is the anti-diagonal index; equals r+c for every cell on that diagonal.", {})])),
    N.para(N.rich([("diag = []", {"code": True}),
                   (" — fresh buffer per diagonal.", {})])),
    N.para(N.rich([("r = max(0, d - (n - 1))", {"code": True}),
                   (" — starting row: clamp so column c = d-r stays ≤ n-1.", {})])),
    N.para(N.rich([("while r <= min(d, m - 1):", {"code": True}),
                   (" — upper bound: r can't exceed the last row; c = d-r can't go negative (requires r ≤ d).", {})])),
    N.para(N.rich([("diag.append(mat[r][d - r])", {"code": True}),
                   (" — c = d - r is always valid here; collect the cell.", {})])),
    N.para(N.rich([("r += 1", {"code": True}),
                   (" — walk down-left: r increases, c decreases.", {})])),
    N.para(N.rich([("if d % 2 == 0: diag.reverse()", {"code": True}),
                   (" — even diagonals go up-right in output; our collection was down-left, so reverse.", {})])),
    N.para(N.rich([("result.extend(diag)", {"code": True}),
                   (" — append all elements of this diagonal (after optional reversal).", {})])),
    N.divider(),
]

# ── Solution 2: Simulation ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Pure Simulation (O(1) Extra Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Walk through every cell one at a time, moving diagonally. "
               "Maintain a direction flag. When you hit a wall, turn. "
               "This directly simulates what the problem describes."),
        N.h4("What Doesn't Work Naively"),
        N.para("Checking 'is r < 0?' and 'is c >= n?' every step without priority "
               "leads to corner bugs. At corner (0, n-1) when going up, both the "
               "top-wall and right-wall conditions fire — you must know which takes priority."),
        N.h4("The Key Observation"),
        N.para("When going up (↗): right wall has priority over top wall. "
               "When going down (↙): bottom wall has priority over left wall. "
               "This priority ordering prevents double-movement at corners."),
        N.h4("Building the Solution"),
        N.para("Use a boolean going_up. Each step: append current cell, then compute "
               "the next position. If going up and hit right wall → slide down (r+1), flip. "
               "If hit top wall → slide right (c+1), flip. Otherwise move normally (r-1, c+1). "
               "Mirror logic for going down."),
        N.callout("This approach is O(1) extra space since no temporary diag[] buffer is needed. "
                  "The tricky part is the corner priority — always check the more-constrained "
                  "wall first (right before top when going up; bottom before left when going down).",
                  "⚠️", "yellow_background"),
    ]),

    N.h3("Code"),
    N.code(
        "def findDiagonalOrder(mat):\n"
        "    m, n = len(mat), len(mat[0])\n"
        "    r, c, going_up = 0, 0, True\n"
        "    result = []\n"
        "    for _ in range(m * n):\n"
        "        result.append(mat[r][c])\n"
        "        if going_up:\n"
        "            if c == n - 1:          # hit right wall\n"
        "                r += 1; going_up = False\n"
        "            elif r == 0:            # hit top wall\n"
        "                c += 1; going_up = False\n"
        "            else:\n"
        "                r -= 1; c += 1\n"
        "        else:\n"
        "            if r == m - 1:          # hit bottom wall\n"
        "                c += 1; going_up = True\n"
        "            elif c == 0:            # hit left wall\n"
        "                r += 1; going_up = True\n"
        "            else:\n"
        "                r += 1; c -= 1\n"
        "    return result"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("r, c, going_up = 0, 0, True", {"code": True}),
                   (" — start at top-left; first diagonal goes up-right.", {})])),
    N.para(N.rich([("for _ in range(m * n):", {"code": True}),
                   (" — exactly m*n cells to visit.", {})])),
    N.para(N.rich([("result.append(mat[r][c])", {"code": True}),
                   (" — collect current cell before computing next position.", {})])),
    N.para(N.rich([("if c == n-1: r += 1; going_up = False", {"code": True}),
                   (" — right wall when going up: slide down (not right!) and flip direction.", {})])),
    N.para(N.rich([("elif r == 0: c += 1; going_up = False", {"code": True}),
                   (" — top wall: slide right and flip. Note: elif prevents double-move at corner.", {})])),
    N.para(N.rich([("if r == m-1: c += 1; going_up = True", {"code": True}),
                   (" — bottom wall when going down: slide right and flip.", {})])),
    N.para(N.rich([("elif c == 0: r += 1; going_up = True", {"code": True}),
                   (" — left wall: slide down and flip. Corner priority: bottom before left.", {})])),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Diagonal Groups + Reverse", "O(m·n)", "O(min(m,n))"],
        ["Pure Simulation", "O(m·n)", "O(1) extra"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Matrix", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Diagonal Groups, Alternate Direction", {})])),
    N.callout(
        "When to recognize this pattern: Problem asks to 'traverse diagonally', "
        "'zigzag order', or 'collect elements along anti-diagonals'. Key signal: "
        "r+c constant on each anti-diagonal. The number m+n-1 appearing → count of diagonals.",
        "🔎", "green_background"
    ),
    N.para("Note: This sub-pattern classification is based on analysis of the diagonal "
           "grouping technique used. The r+c = constant invariant is the defining characteristic."),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (diagonal grouping / matrix traversal):"),
    N.bullet(N.rich([("Diagonal Traverse II", {"bold": True}),
                     (" (Medium) — Same anti-diagonal pattern on a jagged list-of-lists. "
                      "r+c grouping with irregular row lengths. (#1424)", {})])),
    N.bullet(N.rich([("Toeplitz Matrix", {"bold": True}),
                     (" (Easy) — Verify all anti-diagonals have the same value using r-c "
                      "or r+c grouping. (#766)", {})])),
    N.bullet(N.rich([("Sort the Matrix Diagonally", {"bold": True}),
                     (" (Medium) — Collect each main diagonal (r-c = constant), sort it, "
                      "place back. (#1329)", {})])),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}),
                     (" (Medium) — Layer-by-layer boundary traversal; different pattern but "
                      "same 'structured matrix traversal' category. (#54)", {})])),
    N.bullet(N.rich([("Rotate Image", {"bold": True}),
                     (" (Medium) — In-place matrix index manipulation: transpose then reflect. "
                      "Understanding r/c index relationships. (#48)", {})])),
    N.bullet(N.rich([("Search a 2D Matrix II", {"bold": True}),
                     (" (Medium) — Staircase search from corner using row/column ordering. "
                      "Matrix structure exploitation. (#240)", {})])),
    N.para("These problems share the core technique: identifying a structural invariant "
           "(r+c, r-c, or layer index) to systematically group and traverse matrix cells."),
    N.callout("📚 Pattern: Matrix traversal via index invariants. "
              "r+c = anti-diagonal; r-c = main diagonal; layer index = spiral layer.",
              "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("diagonal_traverse")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("Notion body appended. DONE.")
print(f"PAGE_ID: {PAGE_ID}")
