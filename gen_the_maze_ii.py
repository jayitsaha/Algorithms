"""
gen_the_maze_ii.py — Notion page generator for The Maze II (#505)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

SLUG = "the_maze_ii"
PAGE_ID = None  # will be created fresh

# ─── Step 1: Create the page ───
PAGE_ID = N.create_page("The Maze II", 505, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ─── Step 2: Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=505,
    pattern="Graph",
    subpatterns=["Dijkstra"],
    tc="O(m·n·log(m·n))",
    sc="O(m·n)",
    key_insight="Ball rolls until hitting a wall; each roll is a weighted edge — apply Dijkstra's shortest path on stopping positions.",
    icon="🟡"
)
print("Properties set.")

# ─── Step 3: Build body blocks ───
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There is a ball in a maze with empty spaces (", {}),
        ("0", {"code": True}),
        (") and walls (", {}),
        ("1", {"code": True}),
        ("). The ball can go in four directions (up, down, left, right) but it won't stop rolling until hitting a wall. Given the maze, the ball's ", {}),
        ("start", {"code": True}),
        (" position, and the ", {}),
        ("destination", {"code": True}),
        (", return the shortest distance (in steps) for the ball to reach the destination. If it cannot reach the destination, return ", {}),
        ("-1", {"code": True}),
        (".", {})
    ])),
    N.divider()
]

# Solution 1 — Dijkstra's (Interview Pick)
sol1_code = '''import heapq

def shortestDistance(maze, start, destination):
    m, n = len(maze), len(maze[0])
    dist = [[float('inf')] * n for _ in range(m)]
    dist[start[0]][start[1]] = 0
    heap = [(0, start[0], start[1])]   # (distance, row, col)

    while heap:
        d, r, c = heapq.heappop(heap)
        if [r, c] == destination:      # reached destination at optimal cost
            return d
        if d > dist[r][c]:             # stale entry — already processed shorter
            continue

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc, steps = r, c, 0
            # Roll until hitting wall or boundary
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr += dr
                nc += dc
                steps += 1
            new_d = d + steps
            if new_d < dist[nr][nc]:   # found shorter path to this stop?
                dist[nr][nc] = new_d
                heapq.heappush(heap, (new_d, nr, nc))

    return -1  # destination unreachable'''

blocks += [
    N.h2("Solution 1 — Dijkstra's with Rolling Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of each place the ball can stop (against a wall) as a node in a graph. The action of rolling in one direction until hitting a wall is an edge between two nodes, with weight = number of cells crossed. We need the shortest path (by total weight) from start-node to destination-node."),
        N.h4("What Doesn't Work"),
        N.para("Regular BFS assigns cost=1 per move. Here, one move crosses many cells. BFS would wrongly treat rolling 1 cell and rolling 10 cells as equally costly. Modified BFS with distance tracking works but re-visits cells many times — O(m²n²) worst case."),
        N.h4("The Key Observation"),
        N.para("This is a weighted shortest path problem on a graph where edge weights are non-negative (you always roll a non-negative number of steps). Dijkstra's algorithm is designed exactly for this: process nodes in order of true minimum distance using a min-heap."),
        N.h4("Building the Solution"),
        N.para("1. Build dist grid (all infinity, start=0). 2. Min-heap with (0, start). 3. Pop minimum. 4. If it's destination, return distance. 5. Simulate rolling in 4 directions — count steps until wall/boundary. 6. If new_dist < known dist, update and push. 7. Loop until heap empty → return -1."),
        N.callout("Analogy: Think of it like Google Maps routing in a city where you can only stop at intersections (walls). The heap always tries the closest intersection first — guaranteeing the first time you reach your destination is via the shortest route.", "🗺️", "blue_background")
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dijkstra's"),
    N.para(N.rich([
        ("Dijkstra's Algorithm", {"bold": True}),
        (" (Edsger W. Dijkstra, 1956) solves single-source shortest path in graphs with non-negative edge weights in O(E·log V) time with a binary heap.", {})
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("When a node is popped from the min-heap, its recorded distance is the true shortest path. No future path through an unprocessed node can be shorter, because all edges have non-negative weight.", {})
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ("'Shortest path' + 'variable non-negative edge weights'. If weights can be negative, use Bellman-Ford. If all weights are equal (=1), plain BFS suffices.", {})
    ])),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dist = [[inf]*n ...]", {"code": True}), (" — Initialize all distances to infinity; we haven't found any path yet.", {})])),
    N.para(N.rich([("dist[start[0]][start[1]] = 0", {"code": True}), (" — Cost to reach start from itself is 0.", {})])),
    N.para(N.rich([("heap = [(0, start_r, start_c)]", {"code": True}), (" — Min-heap tuple (distance, row, col). Python's heapq is a min-heap by default.", {})])),
    N.para(N.rich([("d, r, c = heapq.heappop(heap)", {"code": True}), (" — Extract the unvisited stopping position with smallest known distance.", {})])),
    N.para(N.rich([("if [r, c] == destination: return d", {"code": True}), (" — Dijkstra's guarantee: first time we pop destination, d is optimal.", {})])),
    N.para(N.rich([("if d > dist[r][c]: continue", {"code": True}), (" — Stale heap entry: a shorter path was already processed. Skip.", {})])),
    N.para(N.rich([("for dr, dc in [...]:", {"code": True}), (" — Try all 4 cardinal directions from this stopping position.", {})])),
    N.para(N.rich([("while 0 <= nr+dr < m ... and maze[nr+dr][nc+dc] == 0:", {"code": True}), (" — Check the NEXT cell (not current) — if it's valid and open, keep rolling.", {})])),
    N.para(N.rich([("nr += dr; nc += dc; steps += 1", {"code": True}), (" — Move one cell in the direction, count it.", {})])),
    N.para(N.rich([("if new_d < dist[nr][nc]:", {"code": True}), (" — Relaxation step: only update if we found a strictly shorter path to this stop.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — Heap exhausted without popping destination → unreachable.", {})])),
    N.divider()
]

# Solution 2 — BFS
sol2_code = '''from collections import deque

def shortestDistance_bfs(maze, start, destination):
    m, n = len(maze), len(maze[0])
    dist = [[float('inf')] * n for _ in range(m)]
    dist[start[0]][start[1]] = 0
    queue = deque([start])

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc, steps = r, c, 0
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr += dr; nc += dc; steps += 1
            if dist[r][c] + steps < dist[nr][nc]:
                dist[nr][nc] = dist[r][c] + steps
                queue.append([nr, nc])  # may re-enqueue if shorter path found later

    d = dist[destination[0]][destination[1]]
    return d if d != float('inf') else -1'''

blocks += [
    N.h2("Solution 2 — BFS with Distance Tracking (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Explore all possible stopping positions level by level. Track the minimum distance to each stop. Re-enqueue a stop whenever we find a shorter path to it."),
        N.h4("What Doesn't Work"),
        N.para("Simple BFS without distance tracking would stop at destination the first time it's reached — but that first visit isn't guaranteed to be the shortest path (unlike unit-cost BFS)."),
        N.h4("The Key Observation"),
        N.para("BFS with dist tracking is correct but slow: a cell may be enqueued many times as shorter paths are discovered through different routes. In the worst case this is O(m²n²)."),
        N.h4("Building the Solution"),
        N.para("Same rolling simulation as Dijkstra's, but use a regular FIFO queue. Update dist whenever a shorter path is found and re-enqueue the node. Check dist at the end.")
    ]),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque([start])", {"code": True}), (" — FIFO queue, not a priority queue. Does NOT process in distance order.", {})])),
    N.para(N.rich([("if dist[r][c] + steps < dist[nr][nc]:", {"code": True}), (" — Only update and re-enqueue if a shorter path was found.", {})])),
    N.para(N.rich([("return d if d != float('inf') else -1", {"code": True}), (" — Check final dist at destination; return -1 if never reached.", {})])),
    N.divider()
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS with distance tracking", "O(m²n²)", "O(m·n)"],
        ["Dijkstra's with min-heap (optimal)", "O(m·n·log(m·n))", "O(m·n)"],
    ]),
    N.divider()
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dijkstra (shortest path with non-negative weights, rolling simulation to generate edges)", {})])),
    N.callout(
        "When to recognize this pattern: 'shortest distance' in a grid where movement has variable cost; ball/robot rolls until blocked; each 'move' spans multiple cells. Any time you see grid traversal with non-unit step costs, think Dijkstra's over BFS.",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dijkstra / weighted grid shortest path):"),
    N.bullet(N.rich([("The Maze", {"bold": True}), (" (Medium) — Same rolling mechanic, only True/False reachability; BFS suffices (#490)", {})])),
    N.bullet(N.rich([("The Maze III", {"bold": True}), (" (Hard) — Dijkstra's + track lexicographically smallest direction string (#499)", {})])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium) — Classic Dijkstra's on explicit weighted graph (#743)", {})])),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), (" (Medium) — Dijkstra's on grid, edge weight = height difference between cells (#1631)", {})])),
    N.bullet(N.rich([("Shortest Path in a Grid with Obstacles Elimination", {"bold": True}), (" (Hard) — BFS with state (r, c, obstacles_remaining) (#1293)", {})])),
    N.bullet(N.rich([("Minimum Obstacle Removal to Reach Corner", {"bold": True}), (" (Medium) — 0-1 BFS variant on grid (#2290)", {})])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), (" (Medium) — Modified Dijkstra's / Bellman-Ford with constraint on hops (#787)", {})])),
    N.para("These problems share the core technique: model grid movement as a weighted graph and apply Dijkstra's shortest path."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section · Sub-Pattern: Dijkstra · Source: Guide Section + Analysis", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ─── Step 4: Append all blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ─── Step 5: Write status file ───
import json
status_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".status")
os.makedirs(status_dir, exist_ok=True)
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the_maze_ii_explainer.html")
html_lines = sum(1 for _ in open(html_path))
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notion_page_id": PAGE_ID,
    "notes": "Dijkstra with rolling simulation; 940-line HTML; fresh Notion page created"
}
with open(os.path.join(status_dir, f"{SLUG}.json"), "w") as f:
    json.dump(status, f, indent=2)
print(f"RESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
