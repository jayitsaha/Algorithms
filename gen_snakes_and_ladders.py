"""
gen_snakes_and_ladders.py
Regenerate the Notion page for LeetCode #909 Snakes and Ladders in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f4-8c61-e53f4c08594f"
SLUG = "snakes_and_ladders"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=909,
    pattern="Graph",
    subpatterns=["BFS Shortest Path"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="BFS on an implicit graph treats cells as nodes and dice rolls as unit-cost edges; first reach of n² = minimum rolls.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(
        "Given an n×n board where cells are numbered 1 to n² in boustrophedon (zigzag from bottom) "
        "order, you start at cell 1. On each turn roll a die (1–6) and advance that many cells. "
        "If the destination has a snake or ladder (board[r][c] ≠ −1), you are transported there "
        "instantly at no extra roll cost. Return the minimum number of dice rolls to reach cell n², "
        "or −1 if impossible."
    ),
    N.divider(),
]

# ── Solution 1: BFS (Interview Pick) ──
sol1_code = """\
from collections import deque

def snakesAndLadders(board: list[list[int]]) -> int:
    n = len(board)

    def cell_to_rc(s):
        r = (s - 1) // n        # 0-indexed row from bottom
        c = (s - 1) % n         # col in that row (left-to-right by default)
        if r % 2 == 1:           # odd rows from bottom go right-to-left
            c = n - 1 - c
        return n - 1 - r, c     # convert to 0-indexed row from top

    visited = {1}
    q = deque([(1, 0)])          # (cell_number, rolls_so_far)

    while q:
        cell, rolls = q.popleft()
        for die in range(1, 7):
            nxt = cell + die
            if nxt > n * n:
                break            # break not continue (larger dice also exceed)
            r, c = cell_to_rc(nxt)
            if board[r][c] != -1:
                nxt = board[r][c]   # teleport (snake or ladder)
            if nxt == n * n:
                return rolls + 1    # BFS guarantees minimum
            if nxt not in visited:
                visited.add(nxt)    # mark at enqueue time
                q.append((nxt, rolls + 1))

    return -1                    # n² is unreachable
"""

blocks += [
    N.h2("Solution 1 — BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the MINIMUM number of dice rolls from cell 1 to cell n². "
            "'Minimum' with unit-cost moves (each roll costs 1 regardless of die value) "
            "is the hallmark of Breadth-First Search on an unweighted graph."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "DFS explores one path deeply and finds A path, not the SHORTEST one. "
            "Greedy (always roll the highest die) misses situations where a small roll "
            "lands on a ladder that shoots you far ahead. Cycles (snake → ladder → snake) "
            "mean we need a visited set or we loop forever."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Model the board as an implicit graph: cells = nodes, dice rolls = directed edges. "
            "From cell s, edges go to s+1, s+2, …, s+6 (after applying any teleport). "
            "All edges cost 1 roll. BFS on a uniform-weight graph gives shortest path."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Start BFS at cell 1, rolls=0. "
            "2. For each dequeued cell, try 6 dice outcomes. "
            "3. Convert cell number → (row, col) using boustrophedon formula. "
            "4. Apply snake/ladder teleport if present (free!). "
            "5. First time we reach n² = return rolls+1."
        ),
        N.callout(
            "Analogy: 'Think of it as water flooding the board level by level — level k is all "
            "cells reachable in exactly k rolls. The first level that touches the last cell is the answer.'",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: BFS Shortest Path"),
    N.para(
        "BFS (Breadth-First Search) systematically explores all nodes reachable in k steps "
        "before exploring nodes at k+1 steps. For any unweighted graph (or equivalently, "
        "uniform-weight graph), this guarantees that the first time any node is discovered, "
        "it is via the shortest path. Time: O(V+E). Here V=n² cells, E≤6n² edges → O(n²)."
    ),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def cell_to_rc(s):", {"code": True}), " — helper that converts 1-indexed cell number to (row, col) in the board array."])),
    N.para(N.rich([("r = (s-1) // n", {"code": True}), " — compute 0-indexed row from bottom (bottom row = 0)."])),
    N.para(N.rich([("c = (s-1) % n", {"code": True}), " — compute column offset within that row (left-to-right by default)."])),
    N.para(N.rich([("if r % 2 == 1: c = n-1-c", {"code": True}), " — odd rows from bottom are right-to-left; reverse the column index."])),
    N.para(N.rich([("return n-1-r, c", {"code": True}), " — convert row-from-bottom to 0-indexed row-from-top (array storage order)."])),
    N.para(N.rich([("visited = {1}", {"code": True}), " — mark cell 1 visited immediately to prevent re-enqueuing it."])),
    N.para(N.rich([("q = deque([(1, 0)])", {"code": True}), " — BFS queue storing (cell, rolls_to_reach_it)."])),
    N.para(N.rich([("cell, rolls = q.popleft()", {"code": True}), " — FIFO dequeue ensures level-by-level processing."])),
    N.para(N.rich([("for die in range(1, 7):", {"code": True}), " — try all 6 possible dice outcomes."])),
    N.para(N.rich([("if nxt > n*n: break", {"code": True}), " — break (not continue): larger dice also exceed the board limit."])),
    N.para(N.rich([("if board[r][c] != -1: nxt = board[r][c]", {"code": True}), " — apply snake or ladder teleport; no extra roll cost."])),
    N.para(N.rich([("if nxt == n*n: return rolls+1", {"code": True}), " — BFS guarantees this is the minimum roll count."])),
    N.para(N.rich([("visited.add(nxt)", {"code": True}), " — mark visited at ENQUEUE time (not dequeue) to prevent duplicate queue entries."])),
    N.divider(),
]

# ── Solution 2: BFS with Pre-flattened Board ──
sol2_code = """\
def snakesAndLadders(board: list[list[int]]) -> int:
    n = len(board)

    # Pre-flatten: flat[s] = teleport destination for cell s, or -1
    flat = [-1] * (n * n + 1)
    for s in range(1, n * n + 1):
        r = (s - 1) // n
        c = (s - 1) % n
        if r % 2 == 1:
            c = n - 1 - c
        flat[s] = board[n - 1 - r][c]  # -1 or teleport target

    from collections import deque
    visited = [False] * (n * n + 1)
    visited[1] = True
    q = deque([(1, 0)])

    while q:
        cell, rolls = q.popleft()
        for die in range(1, 7):
            nxt = cell + die
            if nxt > n * n:
                break
            if flat[nxt] != -1:
                nxt = flat[nxt]          # O(1) teleport lookup
            if nxt == n * n:
                return rolls + 1
            if not visited[nxt]:
                visited[nxt] = True
                q.append((nxt, rolls + 1))

    return -1
"""

blocks += [
    N.h2("Solution 2 — BFS with Pre-flattened Board"),
    N.toggle_h3("💡 Intuition: Why Pre-flatten?", [
        N.h4("Reframe the Problem"),
        N.para("Same BFS algorithm, but we pre-compute a 1D array indexed by cell number so the inner BFS loop is cleaner."),
        N.h4("The Key Observation"),
        N.para(
            "The cell_to_rc conversion inside the BFS loop is correct but visually noisy. "
            "Pre-computing flat[s] = teleport destination (or -1) for all cells once, "
            "then using flat[nxt] in O(1) during BFS, simplifies the hot path."
        ),
        N.h4("Building the Solution"),
        N.para("1. Allocate flat[1..n²]. 2. For each cell s, compute its (row,col) and store board[row][col]. 3. Run identical BFS using flat[nxt] instead of cell_to_rc."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("flat = [-1] * (n*n+1)", {"code": True}), " — 1D array, 1-indexed. flat[s] = board's value (teleport or -1) for cell s."])),
    N.para(N.rich([("flat[s] = board[n-1-r][c]", {"code": True}), " — stores the board value for each cell number, converting coordinates once up front."])),
    N.para(N.rich([("if flat[nxt] != -1: nxt = flat[nxt]", {"code": True}), " — clean O(1) teleport lookup inside the BFS loop."])),
    N.para("Rest of BFS is identical to Solution 1."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS (set-based visited)", "O(n²)", "O(n²)"],
        ["BFS (pre-flattened board)", "O(n²)", "O(n²) + flat[]"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS Shortest Path (Unweighted Graph)"])),
    N.callout(
        "When to recognize this pattern: 'Minimum steps/moves/rolls' + each move costs 1 (uniform weight) "
        "+ finite state space with possible cycles → BFS. If moves had different costs → Dijkstra.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Shortest Path technique:"),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), " (Medium) — BFS through 0-cells; 8-directional grid movement (#1091)"])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), " (Medium) — BFS on state space of 4-digit combination with dead-end pruning (#752)"])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), " (Medium) — BFS from index, jump ±arr[i], reach index with value 0 (#1306)"])),
    N.bullet(N.rich([("Minimum Knight Moves", {"bold": True}), " (Medium) — BFS minimum moves of chess knight to reach target (#1197)"])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), " (Hard) — BFS on word graph; minimum one-letter transformations (#127)"])),
    N.bullet(N.rich([("Sliding Puzzle", {"bold": True}), " (Hard) — BFS on board-state space with encoded hashing (#773)"])),
    N.para("These problems all share the same core technique: BFS on a finite state space with uniform edge costs."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, BFS: Shortest Path Unweighted.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append in chunks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Notion body written. Total blocks: {len(blocks)}")
print(f"NOTION OK {PAGE_ID}")
