"""
gen_sudoku_solver.py — Notion updater for Sudoku Solver (LeetCode #37)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8115-884b-c5edac353103"
SLUG    = "sudoku_solver"

# ── 1) Set page properties ────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=37,
    pattern="Backtracking",
    subpatterns=["Constraint Propagation + Backtrack"],
    tc="O(9^m)",
    sc="O(m)",
    key_insight="Try each valid digit at every empty cell; undo (backtrack) if recursion fails — the 'choose, explore, unchoose' template.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Rebuild body ──────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Write the function "), ("solveSudoku(board)", {"code": True}),
        (" that fills a 9×9 board in-place. Given cells contain digits "),
        ("'1'-'9'", {"code": True}), (" and empty cells are "), ("'.'", {"code": True}),
        (". Fill every empty cell such that every row, every column, and every 3×3 sub-box contains "
         "each digit 1–9 exactly once. The puzzle is guaranteed to have exactly one solution.")
    ])),
    N.divider(),
]

# ── Solution 1: Backtracking ─────────────────────────────────────────
SOL1_CODE = """\
def solveSudoku(board):
    def is_valid(row, col, num):
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for i in range(9):
            if board[row][i] == num: return False    # row conflict
            if board[i][col] == num: return False    # col conflict
            if board[box_r + i // 3][box_c + i % 3] == num:
                return False                         # box conflict
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] != '.': continue
                for num in '123456789':
                    if is_valid(r, c, num):
                        board[r][c] = num            # PLACE
                        if backtrack(): return True  # RECURSE
                        board[r][c] = '.'            # UNDO
                return False  # no digit worked
        return True           # board complete

    backtrack()
"""

blocks += [
    N.h2("Solution 1 — Backtracking with Constraint Check (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to assign a digit from {1-9} to each empty cell such that "
               "no digit repeats in any row, column, or 3×3 box. The board is modified in-place. "
               "Think of it as filling slots one-at-a-time while respecting hard rules."),
        N.h4("What Doesn't Work"),
        N.para("We can't use a greedy approach because a locally valid placement may globally "
               "block future cells. We can't use DP because the constraints are global (row, col, box) "
               "rather than local to a fixed prefix. We need to explore — but intelligently."),
        N.h4("The Key Observation"),
        N.para("Every empty cell is a choice point with at most 9 options. Many options are immediately "
               "ruled out by constraints. If we try a digit and all subsequent placements fail, we can "
               "UNDO that choice and try another — this is backtracking. The search is feasible because "
               "constraints prune most branches."),
        N.h4("Building the Solution"),
        N.para("Step 1: Find the next empty cell (scan top-left to bottom-right). "
               "Step 2: For that cell, try each digit d in '1'-'9'. "
               "Step 3: If d is valid (not in same row, col, or box), place d and recurse. "
               "Step 4: If recursion returns True, we are done — return True. "
               "Step 5: If recursion returns False, undo d and try the next digit. "
               "Step 6: If all 9 digits fail, return False (signal backtrack to parent)."),
        N.callout(
            "Analogy: Think of solving Sudoku by hand. You write a candidate digit in pencil. "
            "If you later find it creates a contradiction, you erase it and try a different digit. "
            "Backtracking is automated erasing.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def is_valid(row, col, num):", {"code": True}),
                   " — checks all three constraint groups for the candidate digit num at position (row, col)."])),
    N.para(N.rich([("box_r, box_c = 3*(row//3), 3*(col//3)", {"code": True}),
                   " — computes the top-left corner of the 3×3 box. Integer division groups rows 0-2, 3-5, 6-8 into box rows 0, 1, 2."])),
    N.para(N.rich([("for i in range(9)", {"code": True}),
                   " — a single loop that simultaneously checks all 9 cells in the row, all 9 in the column, and all 9 in the box."])),
    N.para(N.rich([("board[box_r + i//3][box_c + i%3]", {"code": True}),
                   " — clever indexing to iterate over all 9 box cells: i//3 cycles {0,0,0,1,1,1,2,2,2} for box rows; i%3 cycles {0,1,2,0,1,2,...} for box cols."])),
    N.para(N.rich([("def backtrack():", {"code": True}),
                   " — the recursive solver. Returns True if the board is fully solved, False if a dead end is reached."])),
    N.para(N.rich([("if board[r][c] != '.': continue", {"code": True}),
                   " — skip pre-filled cells; only process empty cells."])),
    N.para(N.rich([("board[r][c] = num", {"code": True}),
                   " — PLACE: tentatively assign the digit. This modifies the board in-place."])),
    N.para(N.rich([("if backtrack(): return True", {"code": True}),
                   " — RECURSE: try to solve the rest of the board. If it succeeds, propagate True up the call stack."])),
    N.para(N.rich([("board[r][c] = '.'", {"code": True}),
                   " — UNDO: this digit led to failure. Restore the empty cell before trying the next candidate."])),
    N.para(N.rich([("return False", {"code": True}),
                   " (inside the cell loop) — all 9 digits failed for this cell; signal the parent to backtrack."])),
    N.para(N.rich([("return True", {"code": True}),
                   " (after the outer loops) — the scan found no empty cell, meaning the board is fully solved."])),
    N.divider(),
]

# ── Solution 2: Optimized with sets ──────────────────────────────────
SOL2_CODE = """\
def solveSudoku(board):
    rows  = [set() for _ in range(9)]  # digits used in each row
    cols  = [set() for _ in range(9)]  # digits used in each column
    boxes = [set() for _ in range(9)]  # digits used in each 3x3 box
    empty = []                         # (r, c) for all empty cells

    for r in range(9):
        for c in range(9):
            if board[r][c] != '.':
                d  = board[r][c]
                bi = (r // 3) * 3 + c // 3
                rows[r].add(d); cols[c].add(d); boxes[bi].add(d)
            else:
                empty.append((r, c))

    def backtrack(idx):
        if idx == len(empty):
            return True          # all empty cells filled
        r, c = empty[idx]
        bi   = (r // 3) * 3 + c // 3
        for d in '123456789':
            if d not in rows[r] and d not in cols[c] and d not in boxes[bi]:
                board[r][c] = d
                rows[r].add(d); cols[c].add(d); boxes[bi].add(d)
                if backtrack(idx + 1):
                    return True
                board[r][c] = '.'
                rows[r].discard(d); cols[c].discard(d); boxes[bi].discard(d)
        return False

    backtrack(0)
"""

blocks += [
    N.h2("Solution 2 — Optimized with Pre-computed Constraint Sets"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same backtracking logic, but eliminate repeated scanning. The bottleneck in Solution 1 "
               "is is_valid(), which scans up to 27 cells (9 per constraint group) for every digit tried. "
               "We can do this in O(1) using hash sets."),
        N.h4("What Doesn't Work"),
        N.para("Solution 1's is_valid() is O(27) per call. With up to 9 candidates per cell and ~50 empty "
               "cells, that's thousands of O(27) scans per backtrack path. While correct, it's slower than necessary."),
        N.h4("The Key Observation"),
        N.para("Pre-compute three arrays of sets: rows[r], cols[c], boxes[b]. Each set stores which digits "
               "are already used. Validity becomes a 3-way set membership test: O(1). When we place/undo a digit, "
               "we add/discard from all three sets in O(1). We also pre-collect empty cells so we don't re-scan the "
               "entire board on each recursive call."),
        N.h4("Building the Solution"),
        N.para("One-time O(81) setup: iterate the board, add given digits to their row/col/box sets, "
               "and record empty cell positions. Then backtrack over the empty list by index — when idx reaches "
               "len(empty), the board is solved. Each placement updates all three sets; each undo discards from them."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("rows/cols/boxes = [set() for _ in range(9)]", {"code": True}),
                   " — 9 sets each. rows[r] contains digits already placed in row r; same for cols and boxes."])),
    N.para(N.rich([("bi = (r//3)*3 + c//3", {"code": True}),
                   " — box index 0-8. (r//3)*3 gives box row offset {0,3,6} and c//3 gives box col offset {0,1,2}."])),
    N.para(N.rich([("empty.append((r, c))", {"code": True}),
                   " — collect all empty positions upfront. Avoids re-scanning the full board every recursive call."])),
    N.para(N.rich([("if idx == len(empty): return True", {"code": True}),
                   " — base case: all empty cells have been filled successfully."])),
    N.para(N.rich([("if d not in rows[r] and d not in cols[c] and d not in boxes[bi]:", {"code": True}),
                   " — O(1) validity check using set membership instead of O(27) scanning."])),
    N.para(N.rich([("rows[r].add(d); cols[c].add(d); boxes[bi].add(d)", {"code": True}),
                   " — update all three constraint sets when placing a digit."])),
    N.para(N.rich([("rows[r].discard(d); cols[c].discard(d); boxes[bi].discard(d)", {"code": True}),
                   " — undo constraint set updates when backtracking. discard() is safe even if d is absent."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (no pruning)", "O(9^81)", "O(81)", "Infeasible — no constraint checking"],
        ["Solution 1 — Backtracking", "O(9^m)", "O(m)", "m = empty cells; is_valid O(27)"],
        ["Solution 2 — Set-Optimized", "O(9^m)", "O(m+81)", "is_valid O(1); 3-5x faster in practice"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Constraint Propagation + Backtrack"])),
    N.callout(
        "When to recognize this pattern: 'Fill a grid / place items with hard constraints', "
        "'Find all valid arrangements', 'Does a valid configuration exist?', "
        "choices at each step can be undone if they lead to failure.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same Backtracking technique:"),
    N.bullet(N.rich([("Valid Sudoku", {"bold": True}),
                     " (#36, Medium) — Validate a board (not solve it) — uses same row/col/box constraint groups"])),
    N.bullet(N.rich([("N-Queens", {"bold": True}),
                     " (#51, Hard) — Place N queens on N×N board — identical backtrack template, different constraints"])),
    N.bullet(N.rich([("Word Search", {"bold": True}),
                     " (#79, Medium) — Find word in 2D grid — DFS + backtrack on grid cells"])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}),
                     " (#39, Medium) — Generate all combinations summing to target — choose, recurse, unchoose"])),
    N.bullet(N.rich([("Permutations", {"bold": True}),
                     " (#46, Medium) — Generate all orderings — pure backtracking template"])),
    N.bullet(N.rich([("Letter Combinations of Phone Number", {"bold": True}),
                     " (#17, Medium) — Enumerate all button-press sequences — tree of choices"])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}),
                     " (#131, Medium) — Partition string into all-palindrome substrings"])),
    N.para("These problems share the core backtracking template: choose a candidate, recurse, unchoose on failure."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. "
              "Sub-Pattern: Constraint Propagation + Backtrack", "📚", "gray_background"),
]

# ── Interactive Embed ──────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append in safe chunks ──────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks.")
print("NOTION OK", PAGE_ID)
