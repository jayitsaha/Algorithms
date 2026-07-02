"""gen_game_of_life.py — Notion update for Game of Life (LC #289)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-92e6-f013263c1ff9"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=289,
    pattern="Matrix",
    subpatterns=["Encode States In-place"],
    tc="O(m×n)",
    sc="O(1)",
    key_insight="Encode alive→dies as 2, dead→born as 3; check v in (1,2) for original aliveness; decode in pass 2.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"code": True}),
        (" grid (board) of cells, each either alive (", {}),
        ("1", {"code": True}),
        (") or dead (", {}),
        ("0", {"code": True}),
        ("), apply Conway's Game of Life rules simultaneously to every cell and update the board in-place.\n\n"
         "Rules:\n"
         "1. Live cell with < 2 live neighbors → dies (underpopulation)\n"
         "2. Live cell with 2 or 3 live neighbors → survives\n"
         "3. Live cell with > 3 live neighbors → dies (overpopulation)\n"
         "4. Dead cell with exactly 3 live neighbors → becomes alive (reproduction)\n\n"
         "Each cell checks all 8 neighbors (horizontal, vertical, diagonal). "
         "All transitions happen simultaneously — the next state is based on the current board, "
         "not any partially-updated board.", {})
    ])),
    N.divider(),
]

# ── Solution 1 ──
SOL1_CODE = '''\
def gameOfLife(board):
    m, n = len(board), len(board[0])
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),
            (0,1),(1,-1),(1,0),(1,1)]

    for r in range(m):
        for c in range(n):
            live = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n \\
                   and board[nr][nc] in (1, 2):
                    live += 1
            if board[r][c] == 1:
                if live < 2 or live > 3:
                    board[r][c] = 2   # alive → dying
            elif board[r][c] == 0:
                if live == 3:
                    board[r][c] = 3   # dead → born

    for r in range(m):
        for c in range(n):
            if board[r][c] == 2: board[r][c] = 0
            if board[r][c] == 3: board[r][c] = 1
'''

blocks += [
    N.h2("Solution 1 — Encode States In-place (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to apply four rules to every cell simultaneously. 'Simultaneously' means: "
               "the next state of each cell depends on the CURRENT board, not a partially-updated one. "
               "If we update cell (0,1) and then use its new value when computing (0,2)'s neighbor count, "
               "we corrupt the answer. The rules themselves are simple — the challenge is preserving "
               "original state while writing new state into the same grid."),
        N.h4("What Doesn't Work"),
        N.para("Updating cells sequentially without any encoding: updating (r,c) before (r,c+1) means "
               "(r,c+1) reads the wrong value for its left neighbor. We'd get incorrect neighbor counts "
               "for all cells that haven't been processed yet when they check a neighbor that already was."),
        N.h4("The Key Observation"),
        N.para("The board only uses values 0 and 1. We can use extra integer values (2 and 3) as "
               "'transition markers'. State 2 = was alive, will die. State 3 = was dead, will be born. "
               "The critical insight: board[nr][nc] in (1, 2) always recovers whether a cell was "
               "ORIGINALLY alive, regardless of encoding order. This replaces the need for a copy."),
        N.h4("Building the Solution"),
        N.para("Pass 1: scan every cell. Count live neighbors using the in (1,2) check. "
               "Apply rules: if alive and must die → mark 2; if dead and must be born → mark 3. "
               "No-change cells (1→1 and 0→0) stay as-is.\n\n"
               "Pass 2: decode. State 2 → 0 (dying → dead). State 3 → 1 (born → alive). "
               "States 0 and 1 are already correct. Done."),
        N.callout(
            "Analogy: imagine replacing a library's books one at a time. You mark each book 'TO REMOVE' "
            "or 'TO ADD' with a sticky note — the sticky note tells you the intent without yet removing "
            "or adding the book. Once all stickies are placed, you execute all changes at once.",
            "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(board), len(board[0])", {"code": True}),
                   (" — extract grid dimensions for bounds checking.", {})])),
    N.para(N.rich([("dirs = [...]", {"code": True}),
                   (" — the 8 direction offsets (dr, dc) covering all 8 neighbors.", {})])),
    N.para(N.rich([("for r in range(m) / for c in range(n)", {"code": True}),
                   (" — scan every cell in row-major order.", {})])),
    N.para(N.rich([("board[nr][nc] in (1, 2)", {"code": True}),
                   (" — CRITICAL: recovers original aliveness. State 1=lives, 2=dying; "
                    "both were originally alive. State 0=dead, 3=born; both were originally dead.", {})])),
    N.para(N.rich([("board[r][c] = 2", {"code": True}),
                   (" — encode 'was alive, will die'. Value 2 is still in (1,2) so future "
                    "neighbor counts correctly read this as an originally-alive cell.", {})])),
    N.para(N.rich([("board[r][c] = 3", {"code": True}),
                   (" — encode 'was dead, will be born'. Value 3 is NOT in (1,2) so future "
                    "neighbor counts correctly treat this as an originally-dead cell.", {})])),
    N.para(N.rich([("Pass 2: if board[r][c] == 2: board[r][c] = 0", {"code": True}),
                   (" — dying cells become dead.", {})])),
    N.para(N.rich([("if board[r][c] == 3: board[r][c] = 1", {"code": True}),
                   (" — born cells become alive. Two simple passes, O(1) space.", {})])),
    N.divider(),
]

# ── Solution 2 ──
SOL2_CODE = '''\
def gameOfLife(board):
    m, n = len(board), len(board[0])
    copy = [row[:] for row in board]  # snapshot
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),
            (0,1),(1,-1),(1,0),(1,1)]
    for r in range(m):
        for c in range(n):
            live = sum(
                copy[r+dr][c+dc]
                for dr, dc in dirs
                if 0 <= r+dr < m and 0 <= c+dc < n
            )
            if copy[r][c] == 1 and live not in (2, 3):
                board[r][c] = 0   # live → dies
            if copy[r][c] == 0 and live == 3:
                board[r][c] = 1   # dead → born
'''

blocks += [
    N.h2("Solution 2 — Copy Board (Simpler, O(mn) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simultaneous update constraint means we need to read from the original state "
               "and write to a separate result. The simplest way: make a copy of the board, "
               "always read from the copy, and write the next state into the original."),
        N.h4("What Doesn't Work"),
        N.para("Reading and writing the same board without a copy corrupts neighbor counts for "
               "cells processed later in the scan order."),
        N.h4("The Key Observation"),
        N.para("A copy of the board perfectly preserves the original state. We never need to "
               "worry about encoding order or intermediate states — we simply read from copy[r][c] "
               "and write to board[r][c]."),
        N.h4("Building the Solution"),
        N.para("Create copy = [row[:] for row in board]. Then for each cell, count live neighbors "
               "from copy (these values are always original). Apply rules and write to board directly. "
               "One pass, O(mn) space. This is the approach to mention first in an interview before "
               "optimizing to O(1) space."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("copy = [row[:] for row in board]", {"code": True}),
                   (" — shallow copy of each row; preserves original state for all neighbor reads.", {})])),
    N.para(N.rich([("live = sum(copy[r+dr][c+dc] ...)", {"code": True}),
                   (" — reads from copy, not board. Safe regardless of what we've written to board.", {})])),
    N.para(N.rich([("if copy[r][c]==1 and live not in (2,3): board[r][c]=0", {"code": True}),
                   (" — alive cell with <2 or >3 neighbors dies (rules 1 and 3).", {})])),
    N.para(N.rich([("if copy[r][c]==0 and live==3: board[r][c]=1", {"code": True}),
                   (" — dead cell with exactly 3 neighbors is born (rule 4). "
                    "Rule 2 (live cell stays alive with 2-3) is handled implicitly: "
                    "we only write to board when a change occurs.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Copy Board", "O(m×n)", "O(m×n)"],
        ["Encode In-place (Interview Pick)", "O(m×n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Matrix — problems that operate on 2D grids and require in-place modification.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Encode States In-place — when cells must update simultaneously from original state, "
                    "use extra integer states to encode the transition. Neighbor-counting recovers original "
                    "value via a simple membership check.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'in-place' and cells are binary (0/1) — room for extra states\n"
        "• All cells must update simultaneously from the original board\n"
        "• The word 'simultaneously' appears in the problem\n"
        "• Need to distinguish 'was X, becomes Y' vs 'was X, stays X' without a copy\n"
        "• A second decode pass can clean up intermediate states",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Encode States In-place technique:"),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}),
                     (" (Medium) — Use row[0] and col[0] as sentinel markers; first pass encodes, second pass applies.", {})])),
    N.bullet(N.rich([("Find All Numbers Disappeared in an Array", {"bold": True}),
                     (" (Easy) — Negate array values as presence markers; positives at end indicate missing numbers.", {})])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}),
                     (" (Medium) — Negate values as visited markers in-place; sign of arr[abs(val)] reveals duplicates.", {})])),
    N.bullet(N.rich([("First Missing Positive", {"bold": True}),
                     (" (Hard) — Cyclic sort or in-place negation encodes presence; linear scan finds the answer.", {})])),
    N.bullet(N.rich([("Rotate Image", {"bold": True}),
                     (" (Medium) — In-place 90° rotation: transpose matrix, then reverse each row. No extra space.", {})])),
    N.bullet(N.rich([("Spiral Matrix II", {"bold": True}),
                     (" (Medium) — Fill matrix in spiral order in-place with direction and bounds tracking.", {})])),
    N.para("These problems share the core technique: re-encode information into cell values to avoid "
           "auxiliary data structures, then decode in a final pass."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Matrix section, "
              "Sub-Pattern: Encode States In-place", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("game_of_life")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} block-items appended")
