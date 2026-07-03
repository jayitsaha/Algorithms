"""
Notion regeneration script for: 01 Matrix (LeetCode #542)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81fb-9542-f8aaf7fbb190"

# ── 1. Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=542,
    pattern="Graph",
    subpatterns=["Multi-source BFS from 0s"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Seed all 0-cells into BFS queue simultaneously; first arrival at any 1-cell gives its minimum distance to nearest 0.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old body ──
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks")

# ── 3. Build new body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"bold": True}),
        (" binary matrix ", {}),
        ("mat", {"code": True}),
        (", return a matrix of the same dimensions where each cell contains the ", {}),
        ("distance", {"bold": True}),
        (" to its nearest ", {}),
        ("0", {"code": True}),
        (". Distance is measured in 4-directional steps (up, down, left, right). "
         "It is guaranteed that at least one 0 exists in the matrix.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("Input: [[0,0,0],[0,1,0],[1,1,1]]  →  Output: [[0,0,0],[0,1,0],[1,2,1]]", {"code": True})
    ])),
    N.para(N.rich([
        ("Edge cases: ", {"bold": True}),
        ("all cells are 0 (output = all 0s), single cell [[0]], large grids with deep clusters of 1s, "
         "1-cell grids with value 1 (distance = unreachable, but problem guarantees a 0 exists).", {})
    ])),
    N.divider()
]

# ── Solution 1 — Multi-Source BFS ──
blocks += [
    N.h2("Solution 1 — Multi-Source BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the shortest distance from every 1-cell to any 0-cell. "
               "This is a shortest-path problem on an unweighted grid where 0-cells are the 'destinations'."),
        N.h4("What Doesn't Work"),
        N.para("Running BFS from each 1-cell independently is correct but O(m²n²) — "
               "for a 300×300 grid that's 8.1 billion operations. Way too slow."),
        N.h4("The Key Observation"),
        N.para("Distance from a 1-cell to the nearest 0 equals distance from the nearest 0 to that 1-cell — "
               "it is symmetric! So instead of asking 'from each 1, find the nearest 0', "
               "we can ask 'from all 0s simultaneously, how far does BFS reach?' "
               "The first time BFS visits any 1-cell gives its optimal distance."),
        N.h4("Building the Solution"),
        N.para("Step 1: Set dist=0 for all 0-cells, dist=∞ for 1-cells, enqueue all 0-cells.\n"
               "Step 2: BFS expands level by level — first distance-1 neighbors, then distance-2, etc.\n"
               "Step 3: The update condition dist[nbr] > dist[curr]+1 acts as both 'update if better' "
               "and 'skip if already visited'.\n"
               "Result: One BFS pass, every cell visited exactly once — O(m·n)."),
        N.callout(
            "Analogy: Imagine all 0-cells as water sources. Water simultaneously spreads outward in all directions. "
            "The moment water first reaches a 1-cell, that's its distance to the nearest source.",
            "🌊", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def updateMatrix(mat: list[list[int]]) -> list[list[int]]:\n"
        "    m, n = len(mat), len(mat[0])\n"
        "    dist = [[float('inf')] * n for _ in range(m)]\n"
        "    q = deque()\n"
        "    \n"
        "    # Seed phase: initialize all 0-cells as sources\n"
        "    for r in range(m):\n"
        "        for c in range(n):\n"
        "            if mat[r][c] == 0:\n"
        "                dist[r][c] = 0\n"
        "                q.append((r, c))\n"
        "    \n"
        "    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]\n"
        "    \n"
        "    # BFS expansion\n"
        "    while q:\n"
        "        r, c = q.popleft()\n"
        "        for dr, dc in dirs:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < m and 0 <= nc < n:\n"
        "                if dist[nr][nc] > dist[r][c] + 1:\n"
        "                    dist[nr][nc] = dist[r][c] + 1\n"
        "                    q.append((nr, nc))\n"
        "    return dist"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}),
                   (" — deque provides O(1) popleft; list.pop(0) would be O(n).", {})])),
    N.para(N.rich([("dist = [[float('inf')] * n ...]", {"code": True}),
                   (" — initialize every cell to infinity. 0-cells will be overwritten. "
                    "Using inf (not -1) lets the update check ", {}),
                   ("dist[nr][nc] > dist[r][c]+1", {"code": True}),
                   (" work cleanly without special cases.", {})])),
    N.para(N.rich([("if mat[r][c] == 0: dist[r][c]=0; q.append((r,c))", {"code": True}),
                   (" — the seeding loop. Every 0-cell becomes a BFS source at distance 0. "
                    "All are enqueued simultaneously — this is what makes it 'multi-source'.", {})])),
    N.para(N.rich([("r, c = q.popleft()", {"code": True}),
                   (" — FIFO order guarantees we process shorter-distance cells first. "
                    "This is the BFS invariant: dequeued cell has its final optimal distance.", {})])),
    N.para(N.rich([("if dist[nr][nc] > dist[r][c] + 1:", {"code": True}),
                   (" — checks two things at once: (1) is this a shorter path? and (2) has this "
                    "cell been settled already? If dist[nr][nc] is already finite and ≤ the proposed "
                    "new distance, we skip it. No separate visited set needed.", {})])),
    N.para(N.rich([("dist[nr][nc] = dist[r][c] + 1; q.append((nr, nc))", {"code": True}),
                   (" — update neighbor's distance and enqueue it for further expansion. "
                    "Each cell is enqueued at most once.", {})])),
    N.divider()
]

# ── Solution 2 — DP Two-Pass ──
blocks += [
    N.h2("Solution 2 — DP Two-Pass (Space-Optimal Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we compute all distances without a queue? Think about it directionally: "
               "the nearest 0 to any cell must lie in one of four directions. "
               "We can handle all four directions with two diagonal sweeps."),
        N.h4("What Doesn't Work"),
        N.para("A single left-to-right scan only propagates distances from the top-left. "
               "A cell might have a nearer 0 below or to the right — one pass misses it."),
        N.h4("The Key Observation"),
        N.para("Two passes cover all four directions: "
               "Pass 1 (top→bottom, left→right) propagates from top and left neighbors. "
               "Pass 2 (bottom→top, right→left) propagates from bottom and right neighbors. "
               "Together they cover all four cardinal directions."),
        N.h4("Building the Solution"),
        N.para("Initialize: 0-cells start at 0, 1-cells start at m+n (the maximum possible distance).\n"
               "Pass 1: for each cell, take the min of its current value and 1 + top/left neighbor.\n"
               "Pass 2: for each cell, take the min of its current value and 1 + bottom/right neighbor.\n"
               "After both passes every cell holds the true minimum distance."),
    ]),
    N.h3("Code"),
    N.code(
        "def updateMatrix_dp(mat: list[list[int]]) -> list[list[int]]:\n"
        "    m, n = len(mat), len(mat[0])\n"
        "    INF = m + n  # max possible distance in any m×n grid\n"
        "    dist = [[0 if mat[r][c] == 0 else INF\n"
        "             for c in range(n)] for r in range(m)]\n"
        "    \n"
        "    # Pass 1: top-left to bottom-right\n"
        "    for r in range(m):\n"
        "        for c in range(n):\n"
        "            if r > 0:\n"
        "                dist[r][c] = min(dist[r][c], dist[r-1][c] + 1)\n"
        "            if c > 0:\n"
        "                dist[r][c] = min(dist[r][c], dist[r][c-1] + 1)\n"
        "    \n"
        "    # Pass 2: bottom-right to top-left\n"
        "    for r in range(m - 1, -1, -1):\n"
        "        for c in range(n - 1, -1, -1):\n"
        "            if r < m - 1:\n"
        "                dist[r][c] = min(dist[r][c], dist[r+1][c] + 1)\n"
        "            if c < n - 1:\n"
        "                dist[r][c] = min(dist[r][c], dist[r][c+1] + 1)\n"
        "    return dist"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("INF = m + n", {"code": True}),
                   (" — the maximum Manhattan distance between any two cells in an m×n grid is m+n-2. "
                    "Using m+n as the sentinel is safe and avoids float('inf').", {})])),
    N.para(N.rich([("Pass 1 (top→bottom, left→right)", {"bold": True}),
                   (" — at each cell, we know the optimal distance from the top (r-1) "
                    "and left (c-1) because those cells were already processed. "
                    "We relax the current cell using both.", {})])),
    N.para(N.rich([("Pass 2 (bottom→top, right→left)", {"bold": True}),
                   (" — handles bottom and right neighbors. "
                    "After both passes, every possible direction has been covered.", {})])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (BFS from each 1)", "O(m²n²)", "O(mn)"],
        ["Multi-Source BFS (Interview Pick)", "O(mn)", "O(mn)"],
        ["DP Two-Pass", "O(mn)", "O(1) extra"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Multi-source BFS from 0s", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Find distance from each cell to nearest X-type cell' "
        "on a grid. (2) All edges have equal cost (unweighted). (3) Multiple sources exist simultaneously. "
        "Signal: you want O(mn) — one BFS pass over the whole grid rather than one per cell.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Multi-source BFS):"),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}),
                     (" (Medium) — BFS from all rotten cells simultaneously; count time steps to rot all fresh (#994)", {})])),
    N.bullet(N.rich([("Walls and Gates", {"bold": True}),
                     (" (Medium) — Fill rooms with distance to nearest gate; identical multi-source setup (#286)", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}),
                     (" (Medium) — BFS from top-left to bottom-right on 0-cells; 8-directional (#1091)", {})])),
    N.bullet(N.rich([("As Far from Land as Possible", {"bold": True}),
                     (" (Medium) — Multi-source BFS from all land cells; find max water-distance (#1162)", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}),
                     (" (Medium) — BFS inward from two ocean borders; find cells reachable from both (#417)", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}),
                     (" (Medium) — BFS/DFS to mark connected 1-components; foundational grid traversal (#200)", {})])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}),
                     (" (Hard) — Multi-source BFS on an implicit graph with value-based jumps (#1345)", {})])),
    N.para("These problems share the core technique: BFS from multiple simultaneous sources, "
           "using FIFO queue ordering to guarantee that the first visit to any node is optimal."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, "
              "Sub-Pattern: Multi-source BFS from 0s", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("01_matrix")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})]))
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — {len(blocks)} blocks written to {PAGE_ID}")
