"""
gen_candy_crush.py — Notion update for LeetCode #723 Candy Crush
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ff-a704-d318f79126a3"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=723,
    pattern="Matrix",
    subpatterns=["Mark + Gravity Simulation"],
    tc="O((R·C)²)",
    sc="O(1)",
    key_insight="Mark groups by negation (use abs() for comparison), crush all at once, then apply column gravity. Repeat until stable.",
    icon="🟡"
)
print("Properties OK")

# ── 2. Wipe old body ──────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build new body ─────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 2D integer board where non-zero values represent candy types and "),
        ("0", {"code": True}),
        (" means empty, simulate the Candy Crush game. Each round: find all horizontal/vertical groups of 3+ identical adjacent candies, crush them simultaneously (set to "),
        ("0", {"code": True}),
        ("), then apply gravity (non-zero candies fall to the bottom of each column). Repeat until no more groups exist. Return the final board.")
    ])),
    N.divider(),
]

# ── Solution 1 — In-Place Negation (Interview Pick) ───────────────────────
sol1_code = '''\
def candyCrush(board):
    R, C = len(board), len(board[0])
    while True:
        crushed = False
        # Phase 1: Mark horizontal groups of 3+
        for r in range(R):
            for c in range(C - 2):
                a = abs(board[r][c])
                if a and a == abs(board[r][c+1]) == abs(board[r][c+2]):
                    board[r][c]   = -abs(board[r][c])
                    board[r][c+1] = -abs(board[r][c+1])
                    board[r][c+2] = -abs(board[r][c+2])
                    crushed = True
        # Phase 2: Mark vertical groups of 3+
        for r in range(R - 2):
            for c in range(C):
                a = abs(board[r][c])
                if a and a == abs(board[r+1][c]) == abs(board[r+2][c]):
                    board[r][c]   = -abs(board[r][c])
                    board[r+1][c] = -abs(board[r+1][c])
                    board[r+2][c] = -abs(board[r+2][c])
                    crushed = True
        if not crushed:
            break           # Board is stable — done
        # Phase 3: Crush — zero out all marked (negative) cells
        for r in range(R):
            for c in range(C):
                if board[r][c] < 0:
                    board[r][c] = 0
        # Phase 4: Gravity — per column, sink non-zeros to bottom
        for c in range(C):
            nz = [board[r][c] for r in range(R) if board[r][c] != 0]
            gap = R - len(nz)
            for r in range(R):
                board[r][c] = 0 if r < gap else nz[r - gap]
    return board\
'''

blocks += [
    N.h2("Solution 1 — In-Place Negation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You're simulating a game loop. Each iteration: find groups, remove, drop. The question is HOW to find and remove correctly without mid-scan interference."),
        N.h4("What Doesn't Work"),
        N.para("Removing a candy immediately during the group scan changes the board mid-pass. A cell removed early may break a valid group that extended through it (or fail to extend to a cell that should have been part of the group). The result is incorrect — you'd miss groups or create false ones."),
        N.h4("The Key Observation"),
        N.para("The game rule says 'crush simultaneously.' This means: scan the FULL board first, collecting ALL groups, then apply all removals at once. You need a way to MARK a cell without actually removing it yet."),
        N.h4("Building the Solution"),
        N.para("Negate the cell's value as a mark flag. The value is preserved under abs(), so subsequent comparisons still work correctly. After the full mark pass, zero out all negatives. Use -abs(x) (not just -x) to handle cells marked multiple times — idempotent negation."),
        N.callout("Analogy: Put a sticky note on each candy to crush, then sweep all sticky-noted candies away. Don't remove mid-search or you'll miss some.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("R, C = len(board), len(board[0])", {"code": True}), " — Cache grid dimensions to avoid repeated len() calls inside nested loops."])),
    N.para(N.rich([("crushed = False", {"code": True}), " — Sentinel: did we mark anything in this round? If not, the board is already stable and we can exit."])),
    N.para(N.rich([("a = abs(board[r][c])", {"code": True}), " — Use abs() so already-negated (marked) cells still read as their original candy type for comparison."])),
    N.para(N.rich([("if a and a == abs(...) == abs(...)", {"code": True}), " — The 'a' check ensures we never treat empty cells (0) as a group. The chained equality checks all three in one expression."])),
    N.para(N.rich([("board[r][c] = -abs(board[r][c])", {"code": True}), " — Mark by negating. Using -abs() is idempotent: a cell already marked (-3) stays -3. Just using -board[r][c] would un-mark it!"])),
    N.para(N.rich([("if not crushed: break", {"code": True}), " — If the entire round produced no marks, no groups exist → board is stable → exit."])),
    N.para(N.rich([("if board[r][c] < 0: board[r][c] = 0", {"code": True}), " — Phase 3: crush. Every negative value is a candy that was marked for removal."])),
    N.para(N.rich([("nz = [board[r][c] for r in range(R) if board[r][c] != 0]", {"code": True}), " — Collect surviving candies in this column, top-to-bottom order."])),
    N.para(N.rich([("board[r][c] = 0 if r < gap else nz[r - gap]", {"code": True}), " — Write back: zeros fill the top gap slots, non-zeros fill the rest from the original order."])),
    N.divider(),
]

# ── Solution 2 — Explicit Set ─────────────────────────────────────────────
sol2_code = '''\
def candyCrush(board):
    R, C = len(board), len(board[0])
    changed = True
    while changed:
        crush = set()  # (r, c) pairs to zero out
        for r in range(R):
            for c in range(C - 2):
                if board[r][c] and board[r][c] == board[r][c+1] == board[r][c+2]:
                    crush |= {(r,c), (r,c+1), (r,c+2)}
        for r in range(R - 2):
            for c in range(C):
                if board[r][c] and board[r][c] == board[r+1][c] == board[r+2][c]:
                    crush |= {(r,c), (r+1,c), (r+2,c)}
        changed = bool(crush)
        for r, c in crush:
            board[r][c] = 0
        for c in range(C):
            nz = [board[r][c] for r in range(R) if board[r][c] != 0]
            gap = R - len(nz)
            for r in range(R):
                board[r][c] = 0 if r < gap else nz[r - gap]
    return board\
'''

blocks += [
    N.h2("Solution 2 — Explicit Crush Set (Cleaner, O(R·C) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same simulation, but instead of marking in-place, keep a separate set of coordinates to crush."),
        N.h4("What Doesn't Work"),
        N.para("Same as Solution 1 — removing mid-scan is wrong."),
        N.h4("The Key Observation"),
        N.para("A Python set naturally handles the case where a cell belongs to both a horizontal and vertical group — adding it twice still results in one entry."),
        N.h4("Building the Solution"),
        N.para("Collect all (r,c) pairs to crush into a set. No need for abs() or negation — the original board values are untouched during the scan. After scanning, zero out the set members, then apply gravity."),
        N.callout("Trade-off: cleaner code but O(R·C) extra space for the crush set. Solution 1 is preferred in interviews for the constant-space guarantee.", "⚖️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("crush = set()", {"code": True}), " — Collects (r,c) pairs for all candies to remove this round. Set ensures no duplicates (intersecting groups add same cell twice but it's deduplicated)."])),
    N.para(N.rich([("crush |= {(r,c),(r,c+1),(r,c+2)}", {"code": True}), " — Set union: add all three members of this group. If some were already in the set, that's fine."])),
    N.para(N.rich([("changed = bool(crush)", {"code": True}), " — If the set is empty, no groups were found → stable. If non-empty, we have work to do."])),
    N.para(N.rich([("for r,c in crush: board[r][c] = 0", {"code": True}), " — Crush phase: zero out every cell in the set simultaneously (actually sequential, but the set was built from the pre-crush board)."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["In-Place Negation (Solution 1)", "O((R·C)²)", "O(1)"],
        ["Explicit Crush Set (Solution 2)", "O((R·C)²)", "O(R·C)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Matrix — grid-based simulation with structural constraints"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Mark + Gravity Simulation — two-phase simultaneous removal + column gravity settling"])),
    N.callout(
        "When to recognize this pattern: (1) 'Repeat until stable/no more moves' → outer loop. "
        "(2) 'Remove/crush groups simultaneously' → mark phase before remove phase. "
        "(3) 'Elements fall after removal' → column-wise gravity (stable partition). "
        "(4) 'In-place O(1)' → negation as sentinel flag.",
        "🔎", "green_background"
    ),
    N.para("*Note: 'Mark + Gravity Simulation' is a problem-specific sub-pattern classification based on analysis; it is not listed by this exact name in the DSA Patterns Guide.*"),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related simulation techniques:"),
    N.bullet(N.rich([("Game of Life", {"bold": True}), " (Medium) — Simultaneous cell-state update; same in-place sentinel trick with 2-bit encoding (#289)"])),
    N.bullet(N.rich([("Set Matrix Zeroes", {"bold": True}), " (Medium) — Mark and apply in-place; use first row/col as sentinel to avoid extra space (#73)"])),
    N.bullet(N.rich([("Rotate Image", {"bold": True}), " (Medium) — In-place 90° rotation of a matrix; layer-by-layer swap technique (#48)"])),
    N.bullet(N.rich([("Spiral Matrix", {"bold": True}), " (Medium) — Directional traversal simulation with boundary bookkeeping (#54)"])),
    N.bullet(N.rich([("Zuma Game", {"bold": True}), " (Hard) — Remove groups of adjacent same-color balls for min moves; same group-collapse logic, DP on intervals (#488)"])),
    N.bullet(N.rich([("Falling Squares", {"bold": True}), " (Hard) — Squares fall and stack; gravity simulation on a 1D number line with interval merging (#699)"])),
    N.bullet(N.rich([("Remove Boxes", {"bold": True}), " (Hard) — Remove groups of identical boxes for max score; DP on groups with attached counts (#546)"])),
    N.para("These problems share the core idea: detect groups → handle simultaneously → apply a structural transform (gravity/rotation/traversal)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Matrix / Grid Problems section. Sub-Pattern: Mark + Gravity Simulation (Analysis classification).", "📚", "gray_background"),
]

# ── Visual Explainer Embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("candy_crush")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
