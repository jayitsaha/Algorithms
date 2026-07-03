"""
gen_minimum_knight_moves.py
Regenerate the Notion page for Minimum Knight Moves (LeetCode #1197) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ff-a26c-e1abae7deff6"

print(f"[1/4] Setting page properties for {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1197,
    pattern="Graph",
    subpatterns=["BFS: Shortest Path Unweighted"],
    tc="O(|x|·|y|)",
    sc="O(|x|·|y|)",
    key_insight="Model as shortest path on unweighted graph; BFS guarantees minimum moves. Use abs(x),abs(y) symmetry to restrict search to first quadrant.",
    icon="🟡"
)
print("  properties set.")

print("[2/4] Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"  deleted {n_deleted} blocks.")

print("[3/4] Building new page body...")

PROBLEM_STATEMENT = (
    "Given two integers x and y, return the minimum number of moves of a knight "
    "to reach the point (x, y) from (0, 0) on an infinite chessboard. "
    "A knight can make 8 possible L-shaped moves: two squares in one direction "
    "then one square perpendicular (or vice versa). The answer is guaranteed to exist."
)

SOL1_CODE = """\
from collections import deque

def minKnightMoves(x: int, y: int) -> int:
    x, y = abs(x), abs(y)       # Symmetry: same answer in all 4 quadrants
    if x == 0 and y == 0:
        return 0                # Already at destination
    DIRS = [(1,2),(1,-2),(-1,2),(-1,-2),
            (2,1),(2,-1),(-2,1),(-2,-1)]
    queue = deque([(0, 0, 0)])  # (x_pos, y_pos, distance)
    visited = {(0, 0)}
    while queue:
        cx, cy, dist = queue.popleft()
        for dx, dy in DIRS:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) == (x, y):
                return dist + 1  # BFS guarantees min distance
            if (nx, ny) not in visited and nx >= -1 and ny >= -1:
                visited.add((nx, ny))  # Mark BEFORE enqueue
                queue.append((nx, ny, dist + 1))
"""

SOL2_CODE = """\
def minKnightMoves(x: int, y: int) -> int:
    x, y = abs(x), abs(y)
    if x + y == 0: return 0
    if x + y == 1: return 3       # Special case: (0,1) or (1,0) need 3 moves
    if x == 2 and y == 2: return 4  # Special case: would give 2 by formula
    t = max(max(x, y), (x + y + 2) // 3)
    return t + (t - x - y) % 2   # Parity correction for color constraint
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — BFS with Symmetry Reduction (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're not moving a chess piece — we're finding the shortest path in a graph. "
            "Board squares are nodes; valid knight moves are edges of weight 1. "
            "Minimum moves = shortest path length. This is textbook BFS territory."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "DFS: Finds some path but not the shortest — it might dive far in the wrong direction. "
            "Greedy (always move toward target): The knight's L-shape means 'closer to target' "
            "by Manhattan distance doesn't always mean fewer total moves. "
            "Dijkstra: Correct but wasteful — all edges weigh 1, so plain BFS is simpler and faster."
        ),
        N.h4("The Key Observation"),
        N.para(
            "BFS explores nodes in order of non-decreasing distance from the source. "
            "The FIRST time BFS reaches the target, the current distance is provably optimal — "
            "any shorter path would have been discovered in an earlier BFS level. "
            "Additionally: the board is 4-way symmetric, so abs(x), abs(y) reduces search to one quadrant."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Take abs(x), abs(y) — symmetry gives same answer in all quadrants.\n"
            "2. BFS from (0,0). For each node, try all 8 knight moves.\n"
            "3. If a neighbor equals (x,y), return current distance + 1.\n"
            "4. Allow coordinates down to -1 (not 0) — near-origin targets need this.\n"
            "5. Use deque.popleft() for O(1) dequeue (not list.pop(0) which is O(n)).\n"
            "6. Mark visited when enqueuing — prevents the same cell entering the queue multiple times."
        ),
        N.callout(
            "Analogy: Think of BFS as a stone dropped in a pond. "
            "Ripples expand outward in rings — ring 1 = all squares 1 move away, "
            "ring 2 = all squares 2 moves away. The first ring to touch (x,y) is the answer.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("x, y = abs(x), abs(y)", {"code": True}), " — Symmetry normalization: the knight's 8 moves are symmetric under axis reflection. answer(x,y) = answer(|x|,|y|). Work in first quadrant only."])),
    N.para(N.rich([("queue = deque([(0, 0, 0)])", {"code": True}), " — Start BFS with source (0,0) at distance 0. We store tuples of (x_position, y_position, distance_from_source)."])),
    N.para(N.rich([("visited = {(0, 0)}", {"code": True}), " — Prevent revisiting. Mark (0,0) visited immediately at initialization, not when dequeued."])),
    N.para(N.rich([("cx, cy, dist = queue.popleft()", {"code": True}), " — Dequeue front in O(1). With deque this is constant time; list.pop(0) would be O(n) and unacceptable for large BFS."])),
    N.para(N.rich([("if (nx, ny) == (x, y): return dist + 1", {"code": True}), " — Found target as a knight-move neighbor of current. BFS guarantees this is the minimum distance. Return dist (distance to current) + 1 (one more move to reach target)."])),
    N.para(N.rich([("nx >= -1 and ny >= -1", {"code": True}), " — Allow coordinates down to -1. Targets like (1,0) require a brief excursion into negative coordinates. Floor at -1 (not 0) handles this correctly without blowing up the search space."])),
    N.para(N.rich([("visited.add((nx, ny))", {"code": True}), " — Mark BEFORE appending to queue. If we mark only when dequeuing, the same cell can be enqueued multiple times (once per neighbor that discovers it), causing duplicate work."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Mathematical Closed Form (O(1) — bonus only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Can we compute the answer without BFS? The knight's move count follows a mathematical pattern "
            "based on the target coordinates. With enough analysis (or by studying the BFS outputs), "
            "a closed-form formula can be derived — but it's impossible to derive under interview pressure."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Simple Manhattan distance / 3 doesn't work because of parity constraints "
            "(the knight always changes color of square). "
            "The formula requires handling several edge cases manually."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The answer has a lower bound of max(max(x,y), (x+y+2)//3) from geometric constraints, "
            "plus a parity correction because the knight alternates between light and dark squares."
        ),
        N.h4("Building the Solution"),
        N.para(
            "This formula is best cited, not derived. In an interview, mention: "
            "'There is an O(1) mathematical solution, but I'd implement BFS for clarity and correctness. "
            "The formula is: t = max(max(x,y), (x+y+2)//3); return t + (t - x - y) % 2, "
            "with special cases for (0,1), (1,0), and (2,2).'"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS + Symmetry (Interview Pick)", "O(|x|·|y|)", "O(|x|·|y|)"],
        ["Bidirectional BFS (Advanced)", "O(√(|x|·|y|))", "O(√(|x|·|y|))"],
        ["Mathematical Formula", "O(1)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (BFS/DFS/Union-Find/Topological Sort)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Shortest Path Unweighted — explores nodes level by level; first time target is reached = minimum distance"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for minimum number of moves/steps/operations. "
        "(2) All transitions have equal cost (unweighted). "
        "(3) The search space can be modeled as a graph/grid. "
        "(4) If there's symmetry in the graph, exploit it to bound the search.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BFS: Shortest Path Unweighted):"),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), " (Medium) — 8-directional BFS; find shortest clear path from top-left to bottom-right (#1091)"])),
    N.bullet(N.rich([("01 Matrix", {"bold": True}), " (Medium) — Multi-source BFS from all 0s simultaneously to compute distance to nearest 0 for each cell (#542)"])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), " (Medium) — Multi-source BFS; BFS levels equal the time until all reachable oranges rot (#994)"])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), " (Hard) — BFS on implicit word graph; one-letter changes are edges; find shortest transformation sequence (#127)"])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), " (Medium) — BFS on combination lock state space; 4 dials × 2 directions = 8 neighbors per state (#752)"])),
    N.bullet(N.rich([("Sliding Puzzle", {"bold": True}), " (Hard) — BFS on 6!/2 valid board states; each blank-swap is one move (#773)"])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), " (Medium) — BFS/DFS from index 0; can we reach a zero-valued index via jump moves? (#1306)"])),
    N.para("These problems share the same core structure: model states as nodes, transitions as edges of equal weight, then use BFS for optimal shortest-path discovery."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph → BFS: Shortest Path Unweighted). Sub-Pattern verified: Guide Section 7 + Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_knight_moves")),
    N.para(N.rich([("Step through the BFS algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  built {len(blocks)} blocks.")

print("[4/4] Appending blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
