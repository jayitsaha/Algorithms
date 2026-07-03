"""
gen_shortest_path_in_a_grid_with_obstacles_elimination.py
Generates the Notion page for LeetCode #1293.
notion_page_id = null -> create fresh page.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

SLUG = "shortest_path_in_a_grid_with_obstacles_elimination"
NAME = "Shortest Path in a Grid with Obstacles Elimination"
NUMBER = 1293
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "Graph"
SUBPATTERNS = ["BFS with State x y k"]  # comma-free for Notion multi_select

# ── Step 0: Create the page (notion_page_id is null) ──────────────
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc="O(m·n·k)",
    sc="O(m·n·k)",
    key_insight="BFS over 3D state (row, col, k_remaining); first dequeue of goal = shortest path",
    icon=ICON,
)
print("Properties set.")

# ── Step 2: Build body blocks ─────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m × n", {"bold": True}),
        (" grid where each cell is either 0 (empty) or 1 (obstacle). You can move in 4 directions. You want to find the minimum number of steps to walk from the upper left corner ", {}),
        ("(0, 0)", {"code": True}),
        (" to the lower right corner ", {}),
        ("(m-1, n-1)", {"code": True}),
        (" given that you can eliminate ", {}),
        ("at most k obstacles", {"bold": True}),
        (". Return the minimum number of steps, or -1 if it is not possible.", {}),
    ])),
    N.para("Constraints: 1 ≤ m, n ≤ 40, 1 ≤ k ≤ m*n, grid[i][j] is 0 or 1, grid[0][0] = grid[m-1][n-1] = 0."),
    N.divider(),
]

# ── Solution 1 — BFS with 3D State ──
SOL1_CODE = """\
from collections import deque

def shortestPath(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])

    # Shortcut: if budget >= Manhattan distance, go straight through
    if k >= m + n - 2:
        return m + n - 2

    # BFS over 3D state: (steps, row, col, k_remaining)
    queue = deque([(0, 0, 0, k)])
    visited = {(0, 0, k)}  # mark on enqueue to prevent duplicate entries

    while queue:
        steps, r, c, remaining = queue.popleft()

        # First time we reach the goal = minimum steps (BFS guarantee)
        if r == m - 1 and c == n - 1:
            return steps

        # Explore 4 cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                # grid[nr][nc] = 0 (empty) -> new_k unchanged
                # grid[nr][nc] = 1 (obstacle) -> new_k decremented by 1
                new_k = remaining - grid[nr][nc]
                if new_k >= 0 and (nr, nc, new_k) not in visited:
                    visited.add((nr, nc, new_k))
                    queue.append((steps + 1, nr, nc, new_k))

    return -1  # queue exhausted — destination unreachable
"""

blocks += [
    N.h2("Solution 1 — BFS with 3D State (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is a shortest-path problem on a grid where every step costs exactly 1. The extra twist is that we carry a 'budget' of k obstacle eliminations. Finding the minimum steps = BFS."),

        N.h4("What Doesn't Work"),
        N.para("Standard 2D BFS (tracking only (row, col) as visited) fails because reaching the same cell with different remaining k values creates genuinely different situations. Blocking a revisit with lower k might prevent a better future path. DFS fails because it has no shortest-path guarantee."),

        N.h4("The Key Observation"),
        N.para("Two states at the same cell (r, c) are only truly equivalent if they also have the same k_remaining. State (r, c, k=3) and (r, c, k=1) can lead to completely different future options. Expand the BFS state to include k_remaining, making it a 3D space: (row, col, k_remaining)."),

        N.h4("Building the Solution"),
        N.para("1) Check the Manhattan shortcut first (k >= m+n-2). 2) Initialize BFS with state (steps=0, r=0, c=0, k). 3) For each neighbor, compute new_k = remaining - grid[nr][nc] — this single subtraction handles obstacle (1) and empty (0) cells uniformly. 4) Only enqueue unvisited 3D states with new_k >= 0. 5) First dequeue of the goal = answer."),

        N.callout(
            "Analogy: Think of k as a 'fuel tank' that lets you drive through walls. Your 'car' state is not just your location but also how much fuel remains — two cars at the same location with different fuel levels are in genuinely different situations.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Code"),
    N.code(SOL1_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — Import deque for O(1) popleft(); a regular list would be O(n) for pop(0)."])),
    N.para(N.rich([("if k >= m + n - 2:", {"code": True}), " — Manhattan shortcut: the direct path from (0,0) to (m-1,n-1) is m+n-2 steps and contains at most m+n-3 intermediate cells. If k is large enough to eliminate all of them, just return the Manhattan distance."])),
    N.para(N.rich([("queue = deque([(0, 0, 0, k)])", {"code": True}), " — Initial state: 0 steps, at position (0,0), with k eliminations left. The tuple order (steps, r, c, remaining) is chosen for clean destructuring."])),
    N.para(N.rich([("visited = {(0, 0, k)}", {"code": True}), " — Mark the initial 3D state immediately. Marking on enqueue (not on dequeue) ensures each state enters the queue at most once, preventing exponential queue growth."])),
    N.para(N.rich([("steps, r, c, remaining = queue.popleft()", {"code": True}), " — FIFO dequeue: popleft() is O(1) for deque. This ensures BFS processes states in non-decreasing step order — the shortest-path guarantee."])),
    N.para(N.rich([("if r == m - 1 and c == n - 1: return steps", {"code": True}), " — BFS guarantee: the first time we dequeue the destination, it was reached in the fewest steps possible (all shorter paths were explored first)."])),
    N.para(N.rich([("new_k = remaining - grid[nr][nc]", {"code": True}), " — Elegant one-liner: grid[nr][nc] is 0 or 1. Subtracting it from remaining either leaves k unchanged (empty cell) or decrements it by 1 (obstacle). If new_k < 0, we can't afford this move."])),
    N.para(N.rich([("if new_k >= 0 and (nr, nc, new_k) not in visited:", {"code": True}), " — Two conditions: (1) we have enough budget, (2) this exact 3D state has not been seen before."])),
    N.para(N.rich([("return -1", {"code": True}), " — If the BFS queue empties without finding the destination, no valid path exists under the given constraints."])),

    N.divider(),
]

# ── Solution 2 — DFS (brute force, for contrast) ──
SOL2_CODE = """\
def shortestPath_dfs(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    best = [float('inf')]

    def dfs(r: int, c: int, steps: int, remaining: int, seen: set) -> None:
        if r == m - 1 and c == n - 1:
            best[0] = min(best[0], steps)
            return
        # Pruning: no point continuing if already worse than best
        if steps >= best[0]:
            return
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                new_k = remaining - grid[nr][nc]
                if new_k >= 0:
                    seen.add((nr, nc))
                    dfs(nr, nc, steps + 1, new_k, seen)
                    seen.remove((nr, nc))  # backtrack

    dfs(0, 0, 0, k, {(0, 0)})
    return best[0] if best[0] != float('inf') else -1
"""

blocks += [
    N.h2("Solution 2 — DFS with Backtracking (Brute Force, Do Not Use in Interview)"),
    N.toggle_h3("💡 Intuition: Why This Exists (and Why It's Slow)", [
        N.h4("Reframe the Problem"),
        N.para("Explore every possible path through the grid, tracking current position and remaining k. When we find the goal, update the minimum. Backtrack to try all alternatives."),

        N.h4("What Doesn't Work"),
        N.para("No global shortest-path guarantee without exhaustive exploration. The same cell is visited many times from different paths and different k values, leading to exponential time. Even with pruning (steps >= best), the worst case is factorial in grid size."),

        N.h4("The Key Observation"),
        N.para("DFS is conceptually simpler but fundamentally wrong for shortest-path: it finds A path but cannot guarantee it's the SHORTEST without trying all of them. BFS with level-order exploration gives the shortest path for free."),

        N.h4("Building the Solution"),
        N.para("Track (r, c) in a seen set. For each unvisited neighbor with new_k >= 0, recurse deeper. After the recursive call, remove from seen (backtrack) to allow this cell in other paths. Update best when goal is reached. Return best or -1."),
    ]),

    N.h3("Code"),
    N.code(SOL2_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("best = [float('inf')]", {"code": True}), " — Use a list (mutable container) so the nested function can update the outer variable without nonlocal declaration (Python 2 compatibility trick)."])),
    N.para(N.rich([("if steps >= best[0]: return", {"code": True}), " — Pruning: if we've already taken more steps than our current best answer, no need to continue this path — it cannot improve the answer."])),
    N.para(N.rich([("seen.remove((nr, nc))", {"code": True}), " — Backtracking: remove the cell from seen AFTER the recursive call returns, allowing it to be visited again in a sibling path. This is the classic DFS backtrack pattern."])),
    N.para(N.rich([("Note:", {"bold": True}), " DFS uses only 2D seen set (not 3D), which means it might revisit the same cell with different k values — this is intentional for DFS (we're exploring all paths), but it's also why it's so slow."])),

    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["BFS with 3D State (Interview Pick)", "O(m·n·k)", "O(m·n·k)", "Each 3D state visited once"],
        ["DFS with Backtracking", "Exponential", "O(m·n)", "Impractical for large inputs"],
        ["A* with Manhattan Heuristic", "O(m·n·k·log(m·n·k))", "O(m·n·k)", "Faster in practice; more complex"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (BFS Traversal)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS with State (x, y, k) — extend BFS state beyond position when a resource/budget affects path validity"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Grid problem asking for minimum steps (BFS reflex)\n"
        "• Extra resource or constraint that changes what paths are valid ('at most k eliminations/jumps/fuel')\n"
        "• Same cell reachable with different 'situations' that affect future options\n"
        "• Keywords: 'at most k obstacles/walls/jumps' in a grid or graph",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BFS with Extended State):"),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), " (Medium) — Standard BFS on grid, no special resource budget (#1091)"])),
    N.bullet(N.rich([("Minimum Obstacle Removal to Reach Corner", {"bold": True}), " (Hard) — 0-1 BFS variant; obstacle removal has binary cost, use deque trick (#2290)"])),
    N.bullet(N.rich([("Jump Game IV", {"bold": True}), " (Hard) — BFS with same-value teleport edges; extended state includes position and jump type (#1345)"])),
    N.bullet(N.rich([("Escape the Spreading Fire", {"bold": True}), " (Hard) — BFS with two evolving agents (you and the spreading fire) as combined state (#2258)"])),
    N.bullet(N.rich([("Cut Off Trees for Golf Event", {"bold": True}), " (Hard) — Repeated BFS with changing grid state after each tree removal (#675)"])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), " (Hard) — BFS on word graph; state = current word; classic BFS on abstract state space (#127)"])),
    N.bullet(N.rich([("Minimum Cost to Make at Least One Valid Path in a Grid", {"bold": True}), " (Hard) — 0-1 BFS with direction-change costs in state (#1368)"])),
    N.para("These problems share the same pattern: BFS extended with an additional state dimension beyond (row, col) to capture resources, constraints, or configuration that affect path optimality."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section (BFS: Shortest Path Unweighted, extended to BFS with State)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the BFS algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
