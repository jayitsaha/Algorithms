"""
Notion update script for: Path With Maximum Minimum Value (#1102)
Run from /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81c6-a849-e6f51f61de7b"
SLUG = "path_with_maximum_minimum_value"

# ── Step 1: Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1102,
    pattern=["Graph"],
    subpatterns=["Binary Search + BFS or Dijkstra"],
    tc="O(mn log mn)",
    sc="O(mn)",
    key_insight="Max-heap Dijkstra: always expand cell with highest bottleneck score; min() update rule ensures optimality",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body ──
print("Wiping old body...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── Step 3: Build new body ──
blocks = []

# ── Problem ──
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    "You are given an m × n integer grid. Find a path from (0,0) to (m-1, n-1) "
    "moving only up/down/left/right. The score of a path is the minimum cell value "
    "along the path. Return the maximum score over all paths from top-left to bottom-right."
))
blocks.append(N.divider())

# ── Solution 1: Modified Dijkstra ──
blocks.append(N.h2("Solution 1 — Modified Dijkstra / Max-Min Heap (Interview Pick)"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "We want the path whose worst cell is as good as possible. Think of it as "
        "finding the path where the 'bottleneck' — the narrowest pipe — is maximized. "
        "A path's score can only stay the same or decrease as you add more cells (each "
        "new cell's value applies another min() operation)."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "BFS (level-order) and DFS explore by distance/depth, not by bottleneck value. "
        "Neither guarantees that the first time you reach the destination is via the "
        "optimal path. You need ordering by score, not by steps taken."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Standard Dijkstra finds shortest paths by always expanding the cheapest cell. "
        "The key insight: replace 'cheapest cumulative distance' with 'highest bottleneck "
        "score so far'. Use a max-heap. When a cell is popped, its score is optimal and final — "
        "no future path can improve it (all unexplored cells have lower or equal scores)."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Push (-grid[0][0], 0, 0) onto a max-heap (negate for Python's min-heap). "
        "2. Pop the cell with the highest score. If it's the destination, return score. "
        "3. For each unvisited neighbor, new_score = min(current_score, neighbor_value). "
        "4. Push (-new_score, nr, nc) and mark visited immediately on push. "
        "5. First pop of destination is guaranteed optimal."
    ),
    N.callout(
        "Analogy: You're routing water through a pipe network. The flow rate is limited "
        "by the narrowest pipe (minimum value). You want the route where even the narrowest "
        "pipe is as wide as possible. Always choose the best-available pipe next.",
        "🧠", "blue_background"
    )
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
"""import heapq

def maximumMinimumPath(grid):
    m, n = len(grid), len(grid[0])
    # Max-heap: negate values (Python heapq is min-heap)
    heap = [(-grid[0][0], 0, 0)]
    visited = [[False] * n for _ in range(m)]
    visited[0][0] = True
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while heap:
        score, r, c = heapq.heappop(heap)
        score = -score  # un-negate

        # First time we pop destination = optimal answer
        if r == m - 1 and c == n - 1:
            return score

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True  # mark on push, not pop
                new_score = min(score, grid[nr][nc])
                heapq.heappush(heap, (-new_score, nr, nc))"""
))

blocks.append(N.h3("Line by Line"))
lines = [
    ("heap = [(-grid[0][0], 0, 0)]", "Initialize max-heap with start cell. Negate value to use Python's min-heap as a max-heap. Score at start = its own cell value."),
    ("visited[0][0] = True", "Mark start as visited immediately — on push, not on pop. Prevents the same cell from being pushed multiple times."),
    ("score, r, c = heapq.heappop(heap); score = -score", "Pop the cell with the highest bottleneck score. Un-negate to get the real score."),
    ("if r == m-1 and c == n-1: return score", "If we just popped the destination, this score is the optimal answer. Return immediately."),
    ("visited[nr][nc] = True", "Mark neighbor visited before pushing. Prevents duplicate heap entries from different paths discovering the same cell."),
    ("new_score = min(score, grid[nr][nc])", "Bottleneck update: the path's new score is limited by the weaker of (current score) and (this neighbor's value)."),
    ("heapq.heappush(heap, (-new_score, nr, nc))", "Push with negated score for max-heap simulation. This neighbor will be processed in score order."),
]
for line, explanation in lines:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {})
    ])))
blocks.append(N.divider())

# ── Solution 2: Binary Search + BFS ──
blocks.append(N.h2("Solution 2 — Binary Search + BFS"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Instead of finding the optimal path directly, ask a simpler yes/no question: "
        "'Can we reach the destination using only cells with value ≥ T?' "
        "If yes for threshold T, the answer is at least T. Binary search to find the highest T."
    ),
    N.h4("The Key Observation"),
    N.para(
        "The answer is monotonic: if threshold T is achievable, every T' < T is also achievable "
        "(using more cells). This monotonicity enables binary search on the answer space [0, maxVal]. "
        "Each binary search step runs a BFS to check feasibility — O(mn) per check."
    ),
    N.callout(
        "When to prefer Binary Search + BFS: if cell values have small range (V << mn), "
        "this runs in O(mn * log V) which can beat Dijkstra's O(mn * log mn). "
        "For large V (values up to 10^9), Dijkstra is typically faster.",
        "🔎", "green_background"
    )
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
"""from collections import deque

def maximumMinimumPath(grid):
    m, n = len(grid), len(grid[0])

    def can_reach(threshold):
        # BFS: can we reach (m-1,n-1) using only cells >= threshold?
        if grid[0][0] < threshold or grid[m-1][n-1] < threshold:
            return False
        seen = {(0, 0)}
        q = deque([(0, 0)])
        while q:
            r, c = q.popleft()
            if r == m - 1 and c == n - 1:
                return True
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n
                        and (nr, nc) not in seen
                        and grid[nr][nc] >= threshold):
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return False

    lo, hi = 0, max(max(row) for row in grid)
    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper mid to avoid infinite loop
        if can_reach(mid):
            lo = mid  # achievable, try higher
        else:
            hi = mid - 1  # too restrictive
    return lo"""
))
blocks.append(N.divider())

# ── Complexity ──
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space"],
    ["Modified Dijkstra (Max-Min)", "O(mn · log(mn))", "O(mn)"],
    ["Binary Search + BFS", "O(mn · log V) — V = max value", "O(mn)"],
    ["Brute Force (all paths)", "Exponential", "O(mn)"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([
    ("Main Pattern: ", {"bold": True}),
    ("Graph (Section 17 — BFS and Shortest Path Algorithms)")
])))
blocks.append(N.para(N.rich([
    ("Sub-Pattern(s): ", {"bold": True}),
    ("Binary Search + BFS or Dijkstra (Guide Section 17.2 & 17.6)")
])))
blocks.append(N.callout(
    "When to recognize this pattern: 'maximize the minimum value on a path', "
    "'minimize the maximum cost on a path', 'find threshold T such that path exists using only values ≥ T'. "
    "Any bottleneck path problem in a grid or graph. Key signal: path score is determined by a single "
    "extremal cell (min or max), not by cumulative sum.",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same bottleneck path technique:"))
related = [
    ("Path With Minimum Effort", "Medium", "Minimize max abs-diff between adjacent cells; same Dijkstra, max() update instead of min() (#1631)"),
    ("Swim in Rising Water", "Hard", "Minimize the max cell encountered on any path; Binary Search + BFS or Dijkstra (#778)"),
    ("Shortest Path in Binary Matrix", "Medium", "Unweighted BFS on grid; prerequisite before weighted bottleneck variants (#1091)"),
    ("Network Delay Time", "Medium", "Classic Dijkstra with cumulative distance; baseline for understanding before max-min variant (#743)"),
    ("Path with Maximum Probability", "Medium", "Maximize product of probabilities; Dijkstra with max() and multiplication (#1514)"),
    ("Koko Eating Bananas", "Medium", "Binary search on answer; same monotonic feasibility check structure (#875)"),
    ("Capacity to Ship Packages", "Medium", "Binary search on capacity; identical 'find highest feasible threshold' pattern (#1011)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))
blocks.append(N.para("These problems all share the core technique: bottleneck path optimization via modified Dijkstra or binary search on the answer."))
blocks.append(N.callout(
    "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.2 (BFS) and Section 17.6 (Shortest Path Algorithms). "
    "Sub-Pattern: Binary Search + BFS or Dijkstra · Verified in Guide Section 17.2.",
    "📚", "gray_background"
))

# ── Embed ──
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for(SLUG)))
blocks.append(N.para(N.rich([
    ("Step through the Max-Min Dijkstra algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
