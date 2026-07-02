import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81fd-bba7-f2b93fabca57"

# 1) Set properties
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=36,
    pattern="Matrix",
    subpatterns=["Hash Sets for Row/Col/Box"],
    tc="O(1)",
    sc="O(1)",
    key_insight="Single pass: track seen values in 9 hash sets per row, col, and 3x3 box; box_idx = (r//3)*3+(c//3).",
    icon="\U0001f7e1"
)
print("Properties set.")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# 3) Build body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        (
            "Determine if a 9x9 Sudoku board is valid. Only filled cells need to be validated:\n"
            "1. Each row must contain digits 1-9 without repetition.\n"
            "2. Each column must contain digits 1-9 without repetition.\n"
            "3. Each of the nine 3x3 sub-boxes must contain digits 1-9 without repetition.\n"
            "Empty cells are shown as ",
            {}
        ),
        ("'.'", {"code": True}),
        (". You only need to validate filled cells -- the board does not need to be solvable.", {})
    ])),
    N.divider()
]

# Solution 1
SOL1 = (
    "def isValidSudoku(board):\n"
    "    rows  = [set() for _ in range(9)]\n"
    "    cols  = [set() for _ in range(9)]\n"
    "    boxes = [set() for _ in range(9)]\n"
    "\n"
    "    for r in range(9):\n"
    "        for c in range(9):\n"
    "            val = board[r][c]\n"
    "            if val == '.':\n"
    "                continue\n"
    "            box_idx = (r // 3) * 3 + (c // 3)\n"
    "            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:\n"
    "                return False\n"
    "            rows[r].add(val)\n"
    "            cols[c].add(val)\n"
    "            boxes[box_idx].add(val)\n"
    "    return True"
)

blocks += [
    N.h2("Solution 1 — Single Pass + Hash Sets (Interview Pick)"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have a 9x9 grid. For each filled number, ensure it hasn't appeared anywhere else "
            "in its row, column, or 3x3 box. Three independent uniqueness constraints to check simultaneously."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Three separate passes (one for rows, one for cols, one for boxes) is correct but wasteful "
            "-- you visit each cell 3 times. We can check all 3 constraints in a single pass."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A hash set membership check is O(1). If we maintain one set per row, one per column, and one "
            "per box, we can check all three constraints at each cell in O(1) and return False the moment "
            "we find a conflict."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create 3x9 sets (9 rows + 9 cols + 9 boxes = 27 sets total).\n"
            "2. Scan each cell. Skip '.'.\n"
            "3. For filled cells, compute box_idx = (r//3)*3 + (c//3). This maps the 9 boxes to indices 0-8.\n"
            "4. Check membership in all 3 sets. If found -> return False.\n"
            "5. Add to all 3 sets and continue.\n"
            "6. Return True if no conflict found."
        ),
        N.callout(
            "Box formula: Row-group (0/1/2) x 3 + Col-group (0/1/2) = box index. "
            "E.g., cell (4,7): (4//3)*3 + (7//3) = 1*3 + 2 = 5 -> box 5.",
            "\U0001f9e0",
            "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL1),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("rows = [set() for _ in range(9)]", {"code": True}),
        (" -- 9 independent sets, one per row. rows[i] tracks which values have been seen in row i.", {})
    ])),
    N.para(N.rich([
        ("cols / boxes", {"code": True}),
        (" -- same idea for columns and the nine 3x3 sub-boxes.", {})
    ])),
    N.para(N.rich([
        ("if val == '.':", {"code": True}),
        (" -- skip empty cells, they have no constraint implications.", {})
    ])),
    N.para(N.rich([
        ("box_idx = (r // 3) * 3 + (c // 3)", {"code": True}),
        (
            " -- integer-divides row and col by 3 to get which box-row (0/1/2) and box-col (0/1/2) "
            "we're in. Multiply row-box by 3, add col-box -> unique box number 0-8.",
            {}
        )
    ])),
    N.para(N.rich([
        ("if val in rows[r] or val in cols[c] or val in boxes[box_idx]:", {"code": True}),
        (" -- O(1) set lookup for all three constraints. First failure returns immediately (fail-fast).", {})
    ])),
    N.para(N.rich([
        ("rows[r].add(val)", {"code": True}),
        (
            " + cols/boxes adds -- register this value in all three tracking sets so future cells "
            "in the same row/col/box will catch a duplicate.",
            {}
        )
    ])),
    N.divider()
]

# Solution 2
SOL2 = (
    "def isValidSudoku(board):\n"
    "    def has_dup(unit):\n"
    "        nums = [x for x in unit if x != '.']\n"
    "        return len(nums) != len(set(nums))\n"
    "\n"
    "    for i in range(9):\n"
    "        # Check row i\n"
    "        if has_dup(board[i]):\n"
    "            return False\n"
    "        # Check column i\n"
    "        if has_dup(board[r][i] for r in range(9)):\n"
    "            return False\n"
    "        # Check box i (row-major ordering)\n"
    "        br, bc = (i // 3) * 3, (i % 3) * 3\n"
    "        box = [board[br+dr][bc+dc] for dr in range(3) for dc in range(3)]\n"
    "        if has_dup(box):\n"
    "            return False\n"
    "    return True"
)

blocks += [
    N.h2("Solution 2 — Three-Pass Brute Force"),
    N.toggle_h3("\U0001f4a1 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Check each constraint (rows, columns, boxes) independently. For each of the 9 rows/cols/boxes, "
            "extract the unit and verify no duplicates."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Nothing breaks correctness-wise, but this visits the board 3x and materializes temporary lists. "
            "Fine for a 9x9 fixed board, but less elegant."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Converting a list to a set removes duplicates. If len(set(unit)) < len(unit), there's a duplicate."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Write a helper has_dup(unit). Loop i from 0-8: check row i, col i, and box i separately "
            "using the same helper."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("has_dup(unit)", {"code": True}),
        (" -- filters out '.' cells, converts remainder to set, checks if any duplicate existed.", {})
    ])),
    N.para(N.rich([
        ("board[i]", {"code": True}),
        (" -- the full row i (a list of 9 values).", {})
    ])),
    N.para(N.rich([
        ("board[r][i] for r in range(9)", {"code": True}),
        (" -- column i: iterate all rows, take the i-th element each time.", {})
    ])),
    N.para(N.rich([
        ("br, bc = (i//3)*3, (i%3)*3", {"code": True}),
        (" -- top-left corner of box i. i//3 gives the box row (0/1/2), i%3 gives the box col (0/1/2).", {})
    ])),
    N.divider()
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Three-Pass Brute Force", "O(81) = O(1)", "O(9) = O(1)"],
        ["Single-Pass Hash Sets ✓", "O(81) = O(1)", "O(27) = O(1)"],
    ]),
    N.divider()
]

# Pattern Classification
blocks += [
    N.h2("\U0001f3f7️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Matrix / Grid Traversal", {})])),
    N.para(N.rich([
        ("Sub-Pattern(s): ", {"bold": True}),
        ("Hash Sets for Row/Col/Box — simultaneous multi-constraint uniqueness tracking", {})
    ])),
    N.callout(
        "When to recognize this pattern: Grid or matrix + uniqueness per row/col/region. "
        "Constraint: each 'unit' (row, column, sub-grid) must have unique values. "
        "Signal: multiple independent constraints, each reducible to "
        "'has this value appeared in this dimension before?'",
        "\U0001f50e",
        "green_background"
    ),
    N.divider()
]

# Related Problems
blocks += [
    N.h2("\U0001f517 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([
        ("Sudoku Solver", {"bold": True}),
        (" (Hard) — Backtracking using this exact validator as the check function", {})
    ])),
    N.bullet(N.rich([
        ("N-Queens", {"bold": True}),
        (" (Hard) — Row/col/diagonal uniqueness via sets, same pattern", {})
    ])),
    N.bullet(N.rich([
        ("Set Matrix Zeroes", {"bold": True}),
        (" (Medium) — Track row/col state in a single pass", {})
    ])),
    N.bullet(N.rich([
        ("Word Search", {"bold": True}),
        (" (Medium) — Grid traversal with visited state", {})
    ])),
    N.bullet(N.rich([
        ("Find the Duplicate Number", {"bold": True}),
        (" (Medium) — Hash set membership = duplicate detection", {})
    ])),
    N.bullet(N.rich([
        ("Number of Islands", {"bold": True}),
        (" (Medium) — Grid traversal with state tracking", {})
    ])),
    N.para(
        "These problems share the core technique: use O(1) set membership checks to detect duplicates "
        "or visited states across constrained dimensions."
    ),
    N.callout(
        "\U0001f4da Reference: Grid/Matrix section of DSA_Patterns_and_SubPatterns_Guide.md "
        "— Hash Sets for Row/Col/Box sub-pattern.",
        "\U0001f4da",
        "gray_background"
    ),
    N.divider()
]

# Embed
blocks += [
    N.h2("\U0001f3af Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_sudoku")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
