"""
gen_n_queens.py — Notion update for N-Queens (LeetCode #51, Hard, Backtracking)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f8-8cec-fd63462a22e5"

# ── 1. Properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=51,
    pattern="Backtracking",
    subpatterns=["Column/Diagonal Tracking"],
    tc="O(n!)",
    sc="O(n²)",
    key_insight="Track occupied columns and diagonal IDs (r−c, r+c) in sets for O(1) conflict detection; backtrack by removing them.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (", return ", {}),
        ("all distinct solutions", {"bold": True}),
        (" to the N-Queens puzzle. Place ", {}),
        ("n", {"code": True}),
        (" queens on an n×n chessboard such that no two queens attack each other. "
         "A queen attacks along its row, column, and both diagonals. "
         "Each solution is a list of n strings where 'Q' marks a queen and '.' marks an empty cell.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Set Backtracking (Interview Pick) ─────────────────────
blocks += [
    N.h2("Solution 1 — Backtracking with Set Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need ALL valid configurations — not an optimum. Each decision (which column to put the queen in for a given row) can be validated instantly. If invalid, skip; if valid, recurse. After exploring, undo and try the next option. This is textbook backtracking."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all n^n placements and filter. For n=8 that's 8^8 = 16.7M boards to check. Too slow. We need early pruning."),
        N.h4("The Key Observation"),
        N.para("Since a queen attacks its entire row, exactly one queen must go in each row. So the search collapses to: 'for row 0, which column? for row 1, which column?' — at most n! states, not n^n. Additionally, diagonal conflicts can be detected in O(1) using the identities: r−c (main diagonal ↘) and r+c (anti-diagonal ↗) are constant along each diagonal."),
        N.h4("Building the Solution"),
        N.para("Maintain three sets: cols (occupied columns), diag (r−c values), anti (r+c values). For each row, try every column. If none of the three sets contain the candidate's identifiers, place the queen (add to all three sets), recurse to the next row, then remove (backtrack). At row==n, convert placement[] to board strings and record."),
        N.callout(
            "Analogy: Think of it as filling a Sudoku one row at a time. Before placing a digit (queen), check row, column, and box (diagonal). If invalid, try the next digit. If you get stuck, erase the last placed digit and try a different one — that's backtracking.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def solveNQueens(n: int) -> list[list[str]]:\n"
        "    cols, diag, anti = set(), set(), set()\n"
        "    placement = [-1] * n  # placement[row] = column of queen\n"
        "    results = []\n"
        "\n"
        "    def backtrack(row):\n"
        "        if row == n:  # base case: all rows filled\n"
        "            board = []\n"
        "            for r in range(n):\n"
        "                c = placement[r]\n"
        "                board.append('.' * c + 'Q' + '.' * (n - 1 - c))\n"
        "            results.append(board)\n"
        "            return\n"
        "        for col in range(n):\n"
        "            if (col in cols or\n"
        "                    row - col in diag or\n"
        "                    row + col in anti):\n"
        "                continue  # conflict — skip\n"
        "            # Place\n"
        "            cols.add(col)\n"
        "            diag.add(row - col)\n"
        "            anti.add(row + col)\n"
        "            placement[row] = col\n"
        "            backtrack(row + 1)\n"
        "            # Backtrack\n"
        "            cols.discard(col)\n"
        "            diag.discard(row - col)\n"
        "            anti.discard(row + col)\n"
        "\n"
        "    backtrack(0)\n"
        "    return results"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("cols, diag, anti = set(), set(), set()", {"code": True}),
                   (" — Three sets tracking occupied columns, main-diagonal IDs (r−c), and anti-diagonal IDs (r+c).", {})])),
    N.para(N.rich([("placement = [-1] * n", {"code": True}),
                   (" — Records which column holds the queen in each row; used to build boards at the base case.", {})])),
    N.para(N.rich([("if row == n:", {"code": True}),
                   (" — Base case: all n rows have queens. Build and record the board.", {})])),
    N.para(N.rich([("board.append('.' * c + 'Q' + '.' * (n - 1 - c))", {"code": True}),
                   (" — Construct each row string: c dots, then Q, then remaining dots.", {})])),
    N.para(N.rich([("for col in range(n):", {"code": True}),
                   (" — Try every column in this row.", {})])),
    N.para(N.rich([("if col in cols or row-col in diag or row+col in anti:", {"code": True}),
                   (" — O(1) conflict check against all three sets. Any hit → skip this column.", {})])),
    N.para(N.rich([("cols.add(col); diag.add(row-col); anti.add(row+col)", {"code": True}),
                   (" — PLACE: mark column and both diagonal IDs as occupied.", {})])),
    N.para(N.rich([("backtrack(row + 1)", {"code": True}),
                   (" — Recurse to place queen in the next row.", {})])),
    N.para(N.rich([("cols.discard(col); diag.discard(row-col); anti.discard(row+col)", {"code": True}),
                   (" — BACKTRACK: undo placement. discard() is safer than remove() (no KeyError).", {})])),
    N.divider(),
]

# ── Solution 2: Bitmask Backtracking ─────────────────────────────────
blocks += [
    N.h2("Solution 2 — Bitmask Backtracking (Faster Constants)"),
    N.toggle_h3("💡 Intuition: Integers as Bitmasks", [
        N.h4("Reframe the Problem"),
        N.para("Instead of Python sets (with hashing overhead), represent the occupied columns and diagonal offsets as integer bitmasks. Bit k = 1 means column k is occupied."),
        N.h4("The Key Observation"),
        N.para("For a given row, the 'available' columns are all columns NOT blocked by any queen above. Compute: available = ((1<<n)-1) & ~(cols | diag | anti). Then iterate over set bits using the 'lowest bit' trick: bit = available & (-available). This avoids a for-loop through all n columns."),
        N.h4("Building the Solution"),
        N.para("Pass cols, diag, anti as immutable integers to each recursive call. Shifting diag right and anti left each row naturally simulates the diagonal movement. No sets, no undo needed — we pass new values each time (functional style)."),
    ]),
    N.h3("Code"),
    N.code(
        "def solveNQueens(n: int) -> list[list[str]]:\n"
        "    results, placement = [], [-1] * n\n"
        "\n"
        "    def bt(row, cols, diag, anti):\n"
        "        if row == n:\n"
        "            results.append(\n"
        "                ['.' * placement[r] + 'Q' + '.' * (n-1-placement[r])\n"
        "                 for r in range(n)])\n"
        "            return\n"
        "        # Compute available columns (bits=1 means safe)\n"
        "        avail = ((1 << n) - 1) & ~(cols | diag | anti)\n"
        "        while avail:\n"
        "            bit = avail & (-avail)          # isolate lowest set bit\n"
        "            col = bit.bit_length() - 1      # column index\n"
        "            placement[row] = col\n"
        "            bt(row + 1,\n"
        "               cols | bit,\n"
        "               (diag | bit) >> 1,           # shift diag right each row\n"
        "               (anti | bit) << 1)            # shift anti left each row\n"
        "            avail &= avail - 1              # clear lowest set bit\n"
        "\n"
        "    bt(0, 0, 0, 0)\n"
        "    return results"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("avail = ((1<<n)-1) & ~(cols|diag|anti)", {"code": True}),
                   (" — n-bit mask of safe columns: all 1s initially, cleared for each occupied constraint.", {})])),
    N.para(N.rich([("bit = avail & (-avail)", {"code": True}),
                   (" — Two's-complement trick to isolate the lowest set bit (rightmost 1).", {})])),
    N.para(N.rich([("(diag | bit) >> 1", {"code": True}),
                   (" — Shifting diag right = diagonal constraints move one column right each row down, matching ↘ direction.", {})])),
    N.para(N.rich([("avail &= avail - 1", {"code": True}),
                   (" — Clears the lowest set bit, advancing to the next available column.", {})])),
    N.callout(
        "⚠️  Common Mistake: forgetting to restore state in the set-based version. In the bitmask version, this is naturally avoided because we pass new integer values to each recursive call rather than mutating shared state.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (n^n)", "O(n^n)", "O(n²)"],
        ["Set Backtracking ✓ (interview pick)", "O(n!)", "O(n²)"],
        ["Bitmask Backtracking", "O(n!)", "O(n) + O(n²) solutions"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Column/Diagonal Tracking", {})])),
    N.callout(
        "When to recognize this pattern: problem asks for ALL valid configurations, "
        "decisions can be validated immediately, and state can be undone (backtracked). "
        "Multiple conflict dimensions (column + two diagonals) → track each as a separate O(1) set.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Backtracking technique:"),
    N.bullet(N.rich([("N-Queens II", {"bold": True}), (" (Hard) — Count distinct solutions instead of enumerating boards (#52)", {})])),
    N.bullet(N.rich([("Sudoku Solver", {"bold": True}), (" (Hard) — Backtracking with row/col/box constraint sets, O(1) check per cell (#37)", {})])),
    N.bullet(N.rich([("Permutations", {"bold": True}), (" (Medium) — Backtrack through all orderings using a 'used' set (#46)", {})])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), (" (Medium) — Backtrack with remaining-target constraint, start-index pruning (#39)", {})])),
    N.bullet(N.rich([("Word Search", {"bold": True}), (" (Medium) — Backtracking on 2D grid with visited cell tracking (#79)", {})])),
    N.bullet(N.rich([("Generate Parentheses", {"bold": True}), (" (Medium) — Backtrack with open/close balance invariant (#22)", {})])),
    N.bullet(N.rich([("Combinations", {"bold": True}), (" (Medium) — Choose k from n with index-advance backtracking (#77)", {})])),
    N.para("These problems all share the same core technique: explore a decision tree, validate constraints at each node, recurse on valid choices, undo (backtrack) after each branch."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. Sub-Pattern: Column/Diagonal Tracking · Source: Analysis", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("n_queens")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append ────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
