"""
gen_rotting_oranges.py — Notion update for LeetCode #994 Rotting Oranges.
Run from /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81aa-8fd9-fe6f734447d4"

# ── 1) Set page properties ──────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=994,
    pattern="Graph",
    subpatterns=["Multi-source BFS"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Seed BFS with ALL rotten oranges simultaneously; the BFS level count equals the minimum minutes to rot all reachable fresh oranges.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m×n", {"code": True}),
        (" grid where each cell can be ", {}),
        ("0", {"code": True}),
        (" (empty), ", {}),
        ("1", {"code": True}),
        (" (fresh orange), or ", {}),
        ("2", {"code": True}),
        (" (rotten orange). Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no fresh orange remains. If this is impossible, return ", {}),
        ("-1", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Multi-Source BFS (Interview Pick) ──────────────
blocks += [
    N.h2("Solution 1 — Multi-Source BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the minimum time for 'infection' to spread from multiple starting points to every reachable cell. This is equivalent to: what is the shortest distance from any initial rotten orange to each fresh orange? We want the maximum such shortest distance across all fresh oranges."),
        N.h4("What Doesn't Work"),
        N.para("Simulating minute by minute — scanning the entire grid each minute and spreading rot — is O((m·n)²). We re-scan cells we've already processed, which is wasteful."),
        N.h4("The Key Observation"),
        N.para("BFS processes cells in order of increasing distance from the source. If we start BFS from ALL rotten oranges simultaneously (all at distance 0), then each BFS level exactly corresponds to one minute of spreading. The answer is the level at which the last fresh orange is reached."),
        N.h4("Building the Solution"),
        N.para("1. Scan grid: enqueue every rotten orange (value=2) and count fresh oranges.\n2. Run standard BFS with level-by-level processing (snapshot queue size before each level).\n3. Each time we reach a fresh neighbor, mark it rotten and decrement the fresh count.\n4. After BFS, check if fresh == 0. If not, some orange was unreachable — return -1."),
        N.callout(
            "Analogy: Think of rotten oranges as campfires. Each minute, fires spread simultaneously to adjacent dry grass. The total burn time is the BFS level count — how many 'waves' of fire spread before every patch is burned.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def orangesRotting(grid: list[list[int]]) -> int:\n"
        "    rows, cols = len(grid), len(grid[0])\n"
        "    queue = deque()\n"
        "    fresh = 0\n\n"
        "    # Scan: seed multi-source BFS and count fresh\n"
        "    for r in range(rows):\n"
        "        for c in range(cols):\n"
        "            if grid[r][c] == 2:\n"
        "                queue.append((r, c))\n"
        "            elif grid[r][c] == 1:\n"
        "                fresh += 1\n\n"
        "    if fresh == 0:\n"
        "        return 0\n\n"
        "    minutes = 0\n"
        "    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]\n\n"
        "    while queue:\n"
        "        for _ in range(len(queue)):   # process one BFS level\n"
        "            r, c = queue.popleft()\n"
        "            for dr, dc in dirs:\n"
        "                nr, nc = r + dr, c + dc\n"
        "                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n"
        "                    grid[nr][nc] = 2   # mark visited immediately\n"
        "                    fresh -= 1\n"
        "                    queue.append((nr, nc))\n"
        "        minutes += 1\n\n"
        "    return minutes - 1 if fresh == 0 else -1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque()", {"code": True}), (" — BFS queue; will hold (row, col) coordinates of rotten oranges.", {})])),
    N.para(N.rich([("fresh = 0", {"code": True}), (" — countdown of remaining fresh oranges; used to detect the -1 case at the end.", {})])),
    N.para(N.rich([("if grid[r][c] == 2: queue.append((r, c))", {"code": True}), (" — every initially rotten orange enters the queue at the same time (level 0). This is the multi-source seed.", {})])),
    N.para(N.rich([("elif grid[r][c] == 1: fresh += 1", {"code": True}), (" — count total fresh oranges so we know when (or if) all of them rot.", {})])),
    N.para(N.rich([("if fresh == 0: return 0", {"code": True}), (" — early exit: no fresh oranges means nothing to rot, answer is 0.", {})])),
    N.para(N.rich([("for _ in range(len(queue))", {"code": True}), (" — snapshot the current level size BEFORE the inner loop. This ensures we process exactly one level per outer while iteration, not mixing levels.", {})])),
    N.para(N.rich([("grid[nr][nc] = 2", {"code": True}), (" — mark fresh orange as rotten immediately upon discovery (enqueue time, not dequeue time). This prevents it from being enqueued multiple times by different neighbors.", {})])),
    N.para(N.rich([("minutes += 1", {"code": True}), (" — incremented after every level, including the final empty-wave level. Subtract 1 at the end to compensate.", {})])),
    N.para(N.rich([("return minutes - 1 if fresh == 0 else -1", {"code": True}), (" — subtract 1 because the last loop iteration was an empty wave (queue had newly-rotted cells but no fresh neighbors to spread to). If fresh > 0, some orange was unreachable.", {})])),
    N.divider(),
]

# ── Solution 2: BFS with time in tuple ─────────────────────────
blocks += [
    N.h2("Solution 2 — BFS with Time in Queue Tuple (Alternate)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of tracking BFS levels explicitly, store the time each orange became rotten in the queue tuple. The answer is the maximum time at which any fresh orange was rotted."),
        N.h4("What Doesn't Work"),
        N.para("Tracking time per cell avoids the off-by-one bug of the level-based approach, but uses slightly more memory per queue entry (3-tuple instead of 2-tuple)."),
        N.h4("The Key Observation"),
        N.para("When we enqueue a newly-rotted orange, we record its time as parent_time + 1. The final answer is the maximum such time across all fresh-to-rotten transitions."),
        N.h4("Building the Solution"),
        N.para("Store (row, col, time) in the queue. Initialize rotten oranges with time=0. Track max_time as the maximum time any fresh orange is rotted. Return max_time if fresh==0."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def orangesRotting_v2(grid: list[list[int]]) -> int:\n"
        "    rows, cols = len(grid), len(grid[0])\n"
        "    queue = deque()\n"
        "    fresh = 0\n"
        "    max_time = 0\n\n"
        "    for r in range(rows):\n"
        "        for c in range(cols):\n"
        "            if grid[r][c] == 2:\n"
        "                queue.append((r, c, 0))  # (row, col, time_became_rotten)\n"
        "            elif grid[r][c] == 1:\n"
        "                fresh += 1\n\n"
        "    while queue:\n"
        "        r, c, t = queue.popleft()\n"
        "        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n"
        "                grid[nr][nc] = 2\n"
        "                fresh -= 1\n"
        "                max_time = t + 1\n"
        "                queue.append((nr, nc, t + 1))\n\n"
        "    return max_time if fresh == 0 else -1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("queue.append((r, c, 0))", {"code": True}), (" — initial rotten oranges are at time 0.", {})])),
    N.para(N.rich([("r, c, t = queue.popleft()", {"code": True}), (" — unpack the time this cell became rotten.", {})])),
    N.para(N.rich([("max_time = t + 1", {"code": True}), (" — update maximum rotten-time whenever a fresh orange is reached.", {})])),
    N.para(N.rich([("queue.append((nr, nc, t + 1))", {"code": True}), (" — propagate time: neighbor rots one minute after its source.", {})])),
    N.para(N.rich([("return max_time if fresh == 0 else -1", {"code": True}), (" — no off-by-one issue here: max_time is only updated on actual spreading, never on empty waves.", {})])),
    N.divider(),
]

# ── Brute Force ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force Simulation (O((m·n)²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly simulate the spreading process minute by minute. Each iteration scans the whole grid, finds rotten oranges, and spreads to fresh neighbors."),
        N.h4("What Doesn't Work"),
        N.para("This is O((m·n)²) — for a 10×10 grid, that's potentially 10,000 operations per minute × up to 100 minutes = 1,000,000 operations. For a 1,000×1,000 grid this is catastrophically slow."),
        N.h4("The Key Observation"),
        N.para("The brute force re-processes cells that are already rotten every minute, wasting work. BFS avoids this by only visiting each cell once."),
        N.h4("Building the Solution"),
        N.para("Copy the grid each minute to avoid same-minute cascade. Repeat until stable. This is useful for verifying the BFS solution but should not be used in production."),
    ]),
    N.h3("Code"),
    N.code(
        "def orangesRotting_brute(grid: list[list[int]]) -> int:\n"
        "    import copy\n"
        "    minutes = 0\n"
        "    while True:\n"
        "        changed = False\n"
        "        new_grid = copy.deepcopy(grid)\n"
        "        for r in range(len(grid)):\n"
        "            for c in range(len(grid[0])):\n"
        "                if grid[r][c] == 2:\n"
        "                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:\n"
        "                        nr, nc = r+dr, c+dc\n"
        "                        if 0<=nr<len(grid) and 0<=nc<len(grid[0]) and grid[nr][nc]==1:\n"
        "                            new_grid[nr][nc] = 2\n"
        "                            changed = True\n"
        "        if not changed:\n"
        "            break\n"
        "        grid = new_grid\n"
        "        minutes += 1\n"
        "    fresh = sum(row.count(1) for row in grid)\n"
        "    return minutes if fresh == 0 else -1"
    ),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Simulation", "O((m·n)²)", "O(m·n)"],
        ["Multi-Source BFS (Interview Pick)", "O(m·n)", "O(m·n)"],
        ["BFS with Time in Tuple", "O(m·n)", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (Section 17)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Multi-source BFS (Section 17.2)", {})])),
    N.callout(
        "When to recognize this pattern: 'minimum time/steps for something to spread simultaneously from multiple starting points'; 'distance to nearest X in a grid where X can be multiple cells'; any problem where several sources activate at the same time and expand outward.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Multi-source BFS technique:"),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), (" (Medium) — Distance to nearest 0; seed BFS from all zero cells simultaneously. LeetCode #542.", {})])),
    N.bullet(N.rich([("Walls and Gates", {"bold": True}), (" (Medium) — Fill INF cells with distance to nearest gate; multi-source BFS from all gates. LeetCode #286.", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}), (" (Medium) — BFS inward from Atlantic and Pacific borders simultaneously. LeetCode #417.", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — BFS from (0,0) with 8-directional moves. LeetCode #1091.", {})])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}), (" (Medium) — BFS from all border 'O' cells to protect them. LeetCode #130.", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Foundational graph grid traversal with BFS/DFS. LeetCode #200.", {})])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), (" (Hard) — BFS on word state space; each transform = one BFS level. LeetCode #127.", {})])),
    N.para("These problems share the core technique: BFS from one or more sources to find shortest distances in an unweighted graph (grid)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.2 — Graph BFS, Multi-source BFS", "📚", "gray_background"),
]

# ── Embed ───────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("rotting_oranges")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
