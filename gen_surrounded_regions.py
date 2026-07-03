"""
gen_surrounded_regions.py
Regenerates the Notion page for Surrounded Regions (LeetCode #130) in-place.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81fd-ab9a-e9dc0303d6e4"

print(f"Working on page: {PAGE_ID}")

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=130,
    pattern="Graph",
    subpatterns=["DFS from Borders"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="DFS/BFS from border O's marks safe regions; all remaining O's are surrounded and captured.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing content ───────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build new body ──────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"code": True}),
        (" board containing characters ", {}),
        ("'X'", {"code": True}),
        (" and ", {}),
        ("'O'", {"code": True}),
        (", capture all regions that are surrounded by ", {}),
        ("'X'", {"code": True}),
        (". A region is captured by flipping all ", {}),
        ("'O'", {"code": True}),
        ("s into ", {}),
        ("'X'", {"code": True}),
        ("s in that surrounded region. An ", {}),
        ("'O'", {"code": True}),
        (" on the border or connected to a border ", {}),
        ("'O'", {"code": True}),
        (" is NOT surrounded and must not be flipped.", {}),
    ])),
    N.divider(),
]

# Solution 1 — DFS from Borders
sol1_code = '''def solve(board: list[list[str]]) -> None:
    if not board or not board[0]: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if (r < 0 or r >= rows or
                c < 0 or c >= cols or
                board[r][c] != 'O'):
            return
        board[r][c] = 'S'  # mark as safe sentinel
        dfs(r+1, c); dfs(r-1, c)
        dfs(r, c+1); dfs(r, c-1)

    # Phase 1: DFS from all border O's
    for r in range(rows):
        dfs(r, 0); dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c); dfs(rows - 1, c)

    # Phase 2 + 3: Flip surrounded O's, restore safe S's
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'S':
                board[r][c] = 'O\''''

blocks += [
    N.h2("Solution 1 — DFS from Borders (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The problem asks us to flip O's that are 'surrounded' by X's. But checking whether an O is surrounded means verifying ALL paths to the border are blocked — which is hard. Instead, ask the opposite: which O's are SAFE (not surrounded)? A safe O is simply one reachable from any border cell by a path through O's only."),
        N.h4("What Doesn't Work"),
        N.para("DFS from each interior O and checking if it escapes to the border is O((m·n)²) — too slow. Also, connected O-groups must be flipped atomically (all or none), making per-cell checking complex. The naive approach has both correctness and efficiency problems."),
        N.h4("The Key Observation"),
        N.para("Border cells are the ONLY exits from the grid. Any O that can reach a border is safe. Run DFS from all border O's simultaneously — this transitively discovers every safe O in a single O(m·n) sweep. What remains unmarked is provably surrounded."),
        N.h4("Building the Solution"),
        N.para("Phase 1: Scan four border edges, launching DFS from each O found. DFS marks reachable O's as sentinel 'S'. Phase 2: scan full board — any O is surrounded (flip to X). Phase 3: any S is safe (restore to O). The three-phase mark→flip→restore pattern solves the problem cleanly."),
        N.callout("Analogy: Border cells are 'exits'. O's connected to exits are free. Everything else is imprisoned and captured.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if not board or not board[0]: return", {"code": True}), (" — Guard against empty board or empty first row. Early exit before any computation.", {})])),
    N.para(N.rich([("rows, cols = len(board), len(board[0])", {"code": True}), (" — Cache dimensions to avoid recomputing inside DFS.", {})])),
    N.para(N.rich([("def dfs(r, c):", {"code": True}), (" — Inner function: recursively marks connected O's as safe. Closure over board, rows, cols.", {})])),
    N.para(N.rich([("if ... board[r][c] != 'O': return", {"code": True}), (" — Base cases: out-of-bounds OR cell is X (wall) OR cell is S (already safe). Only explore O cells.", {})])),
    N.para(N.rich([("board[r][c] = 'S'", {"code": True}), (" — Mark this O as safe with sentinel. This also prevents revisiting — DFS will skip 'S' cells on the next call.", {})])),
    N.para(N.rich([("dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)", {"code": True}), (" — Expand to all four directional neighbors.", {})])),
    N.para(N.rich([("for r in range(rows): dfs(r, 0); dfs(r, cols-1)", {"code": True}), (" — Phase 1a: scan left and right border columns for O seeds.", {})])),
    N.para(N.rich([("for c in range(cols): dfs(0, c); dfs(rows-1, c)", {"code": True}), (" — Phase 1b: scan top and bottom border rows for O seeds.", {})])),
    N.para(N.rich([("if board[r][c] == 'O': board[r][c] = 'X'", {"code": True}), (" — Phase 2: any remaining 'O' was never reached by border DFS → it's surrounded → capture.", {})])),
    N.para(N.rich([("elif board[r][c] == 'S': board[r][c] = 'O'", {"code": True}), (" — Phase 3: restore sentinels to 'O' — these were the safe, border-connected cells.", {})])),
    N.callout("Warning: Python's default recursion limit (~1000) can cause stack overflow on large boards (up to 200×200 = 40,000 cells). Mention BFS alternative in interviews.", "⚠️", "yellow_background"),
    N.divider(),
]

# Solution 2 — BFS from Borders
sol2_code = '''from collections import deque

def solve(board: list[list[str]]) -> None:
    if not board or not board[0]: return
    rows, cols = len(board), len(board[0])
    queue = deque()

    # Seed BFS with all border O's
    for r in range(rows):
        for c in [0, cols - 1]:
            if board[r][c] == 'O':
                queue.append((r, c))
                board[r][c] = 'S'
    for c in range(cols):
        for r in [0, rows - 1]:
            if board[r][c] == 'O':
                queue.append((r, c))
                board[r][c] = 'S'

    # BFS: expand all safe regions
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O':
                board[nr][nc] = 'S'
                queue.append((nr, nc))

    # Flip + Restore in one pass
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': board[r][c] = 'X'
            elif board[r][c] == 'S': board[r][c] = 'O\''''

blocks += [
    N.h2("Solution 2 — BFS from Borders (Production-Safe)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem inversion as Solution 1: find safe (border-connected) O's rather than surrounded ones. BFS provides an iterative alternative that avoids Python's recursion depth limits."),
        N.h4("What Doesn't Work"),
        N.para("Recursive DFS works correctly but may hit Python's default ~1000 frame call stack limit on boards with large connected O-regions. For production code on 200×200 boards with 40,000 cells, this is a real failure mode."),
        N.h4("The Key Observation"),
        N.para("BFS and DFS are interchangeable for graph reachability problems. Using a deque as an explicit stack/queue moves the call state from the Python call stack (limited) to heap memory (effectively unlimited). Same algorithm, different data structure, no recursion risk."),
        N.h4("Building the Solution"),
        N.para("Seed the queue with ALL border O's simultaneously (multi-source BFS). Mark each when enqueued to prevent re-queuing. BFS naturally expands level by level. After BFS, apply the same flip+restore pass as in Solution 1."),
        N.callout("Key difference from Solution 1: mark cells 'S' when ENQUEUED, not when dequeued. This prevents the same cell being added to the queue multiple times.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque()", {"code": True}), (" — BFS frontier. Deque allows O(1) popleft (queue) or pop (stack). Both orderings work for reachability.", {})])),
    N.para(N.rich([("board[r][c] = 'S'; queue.append((r, c))", {"code": True}), (" — Mark BEFORE enqueuing. If we mark only when dequeuing, the same cell can be enqueued multiple times from different neighbors, causing redundant work.", {})])),
    N.para(N.rich([("while queue: r, c = queue.popleft()", {"code": True}), (" — Process cells in FIFO order (BFS). For this problem, LIFO (stack/DFS) also works — ordering doesn't matter for reachability.", {})])),
    N.para(N.rich([("for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:", {"code": True}), (" — 4-directional neighbors: down, up, right, left.", {})])),
    N.para(N.rich([("if 0<=nr<rows and 0<=nc<cols and board[nr][nc]=='O':", {"code": True}), (" — Bounds check + only expand into unvisited O's (S is already safe, X is wall).", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Naive (DFS from each interior O)", "O((m·n)²)", "O(m·n)", "Too slow — each O triggers full DFS"],
        ["DFS from Borders (recursive)", "O(m·n)", "O(m·n)", "Elegant — risk of stack overflow in Python"],
        ["BFS from Borders (iterative) ✓", "O(m·n)", "O(m·n)", "Production-safe — recommended"],
        ["Union-Find", "O(m·n·α)", "O(m·n)", "Union O's with virtual border node"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — DFS/BFS traversal on a 2D grid.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS from Borders — flood-fill from border sources to identify/separate connected components by reachability from the grid edge.", {})])),
    N.callout(
        "When to recognize this pattern: 'surrounded by X', 'enclosed region', 'not reachable from border', 'safe vs captured' grid problems. Whenever the BORDER defines which cells survive, start DFS/BFS from the border.",
        "🔎",
        "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same multi-source DFS/BFS from borders or flood-fill technique:"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — DFS/BFS to count connected O-components; same grid traversal foundation. (#200)", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}), (" (Medium) — Multi-source DFS from TWO border sets (Pacific + Atlantic edges); intersection = answer. (#417)", {})])),
    N.bullet(N.rich([("Max Area of Island", {"bold": True}), (" (Medium) — DFS flood-fill to find largest connected region; track size during DFS. (#695)", {})])),
    N.bullet(N.rich([("Walls and Gates", {"bold": True}), (" (Medium) — Multi-source BFS from all gate cells; fills distances to nearest gate. (#286)", {})])),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), (" (Medium) — Multi-source BFS from all 0-cells; computes distance to nearest 0. (#542)", {})])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), (" (Medium) — Multi-source BFS from all initially rotten oranges; time-based expansion. (#994)", {})])),
    N.bullet(N.rich([("Flood Fill", {"bold": True}), (" (Easy) — Classic single-source DFS grid flood from a starting cell. (#733)", {})])),
    N.para("These problems all share the multi-source graph reachability technique: seed from known points, expand via DFS/BFS, use what was reached (or not reached) to determine the answer."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 8: Graph Traversal, DFS from Borders sub-pattern", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("surrounded_regions")),
    N.para(N.rich([("Step through the DFS-from-Borders algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
