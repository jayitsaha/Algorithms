"""gen_making_a_large_island.py — Notion in-place update for Making A Large Island (#827)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8167-afaa-edc593faec0f"

# ── 1) Properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=827,
    pattern="Graph",
    subpatterns=["Label Islands + Try Flip"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="Label each island once with DFS (label≥2), store sizes; for each 0-cell sum unique neighbor island sizes + 1.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an n×n binary grid. You are allowed to change at most one ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("1", {"code": True}),
        (". Return the size of the largest island in the grid after applying this operation.\n\n"
         "An island is a 4-directionally connected group of 1s. "
         "If the grid already has no 0s, return the size of the largest existing island.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ("grid = [[1,0],[0,1]] → 3\n", {}),
            ("Flip (0,1): connects island at (0,0) and island at (1,1). Result: 3 cells.\n\n", {}),
            ("Example 2: ", {"bold": True}),
            ("grid = [[1,1],[1,0]] → 4\n", {}),
            ("Flip (1,1): completes the entire 2×2 grid into one island of size 4.", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Optimal — Label Islands + Try Flip ─────────────
BRUTE_CODE = '''\
# Brute Force — O(n^4)
def largestIsland_brute(grid):
    n = len(grid)

    def bfs(r, c, visited):
        size = 0
        queue = [(r, c)]
        visited.add((r, c))
        while queue:
            cr, cc = queue.pop()
            size += 1
            for nr, nc in [(cr+1,cc),(cr-1,cc),(cr,cc+1),(cr,cc-1)]:
                if 0 <= nr < n and 0 <= nc < n and (nr,nc) not in visited and grid[nr][nc] == 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return size

    best = 0
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                grid[r][c] = 1                       # flip
                visited = set()
                for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                    if 0 <= nr < n and 0 <= nc < n and (nr,nc) not in visited and grid[nr][nc] == 1:
                        best = max(best, bfs(nr, nc, visited))
                if not visited:
                    best = max(best, 1)
                grid[r][c] = 0                       # undo flip
    return best
'''

OPTIMAL_CODE = '''\
def largestIsland(grid):
    n = len(grid)
    island_size = {}      # label (int >= 2) -> cell count
    label = 2             # start above grid values 0 and 1

    def dfs(r, c, lbl):
        """Flood-fill from (r,c), marking cells with lbl, return count."""
        if r < 0 or r >= n or c < 0 or c >= n:
            return 0
        if grid[r][c] != 1:   # 0 = sea, >=2 = already labeled
            return 0
        grid[r][c] = lbl      # mark: overwrite 1 with the label
        return (1
                + dfs(r+1, c, lbl) + dfs(r-1, c, lbl)
                + dfs(r, c+1, lbl) + dfs(r, c-1, lbl))

    # Phase 1: label every connected island
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:                       # unlabeled land
                island_size[label] = dfs(r, c, label) # DFS -> size
                label += 1

    # Phase 2: try flipping each sea cell
    result = max(island_size.values(), default=0)     # baseline (all-1 case)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen = set()                          # unique island labels among neighbors
                for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 1:
                        seen.add(grid[nr][nc])        # set deduplicates same island
                sz = 1 + sum(island_size[l] for l in seen)
                result = max(result, sz)
    return result
'''

MEMO_CODE = '''\
# Alternative: iterative BFS for Phase 1 (avoids recursion stack overflow)
from collections import deque

def largestIsland_bfs(grid):
    n = len(grid)
    island_size = {}
    label = 2

    def bfs_label(r, c, lbl):
        """Iterative BFS flood-fill."""
        q = deque([(r, c)])
        grid[r][c] = lbl
        size = 0
        while q:
            cr, cc = q.popleft()
            size += 1
            for nr, nc in [(cr+1,cc),(cr-1,cc),(cr,cc+1),(cr,cc-1)]:
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = lbl
                    q.append((nr, nc))
        return size

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                island_size[label] = bfs_label(r, c, label)
                label += 1

    result = max(island_size.values(), default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen = set()
                for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 1:
                        seen.add(grid[nr][nc])
                sz = 1 + sum(island_size[l] for l in seen)
                result = max(result, sz)
    return result
'''

# Solution 1 (Brute Force)
blocks += [
    N.h2("Solution 1 — Brute Force: Flip and BFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each sea cell, simulate what happens if we flip it, then find the largest connected island."),
        N.h4("What Doesn't Work"),
        N.para(
            "Flipping each 0 and re-running full BFS costs O(n²) per candidate cell × O(n²) candidates = O(n⁴). "
            "For n=500 that is 62.5 billion operations — guaranteed TLE."
        ),
        N.h4("The Key Observation"),
        N.para("This brute-force is the starting point only. Its structure is correct but its cost is too high. "
               "Mentioning this approach in an interview shows you understand the problem before optimizing."),
        N.h4("Building the Solution"),
        N.para("For each 0-cell: flip it to 1, run BFS to find the size of any island it connects, track maximum, undo the flip. "
               "Simple but O(n⁴)."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("For each 0-cell:", {"bold": True}), " flip it to 1, run BFS from it to measure island size, undo flip."])),
    N.para(N.rich([("bfs(r, c, visited):", {"bold": True}), " standard BFS that counts all connected 1-cells reachable from (r, c)."])),
    N.para(N.rich([("grid[r][c] = 0 after BFS:", {"bold": True}), " undo the flip so we don't pollute future iterations."])),
    N.divider(),
]

# Solution 2 (Optimal)
blocks += [
    N.h2("Solution 2 — Label Islands + Try Flip (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Why is brute force slow? It re-traverses the same islands repeatedly. Island sizes never change between flip attempts. So: compute them once, look them up in O(1)."),
        N.h4("What Doesn't Work"),
        N.para("Any approach that re-runs DFS/BFS for every candidate flip cell is O(n⁴). The repeated work is the bottleneck."),
        N.h4("The Key Observation"),
        N.para("If we give every island a unique integer label and store its size, then checking a 0-cell takes O(1) per neighbor: "
               "look up grid[neighbor] to get the label, look up island_size[label] to get the size. "
               "Sum unique neighbor island sizes + 1 = total island size after flip."),
        N.h4("Building the Solution"),
        N.para("Phase 1: DFS over all cells. When we find a 1-cell (unlabeled land), flood-fill with the current label (starting at 2), "
               "count cells, store island_size[label]. "
               "Labels start at 2 to avoid collision with grid values 0 and 1.\n\n"
               "Phase 2: For each 0-cell, collect the set of unique island labels from its neighbors. "
               "Sum those island sizes + 1. Track the maximum."),
        N.callout(
            "Analogy: A land surveyor stamps every connected parcel with a lot number and records its area. "
            "Later, for each empty field, they ask: 'If I build here, which adjacent lots do I connect?' "
            "They look up the lot areas in their ledger — no re-measurement needed.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("island_size = {};  label = 2:", {"bold": True}), " initialize the label-to-size dictionary and the label counter. Starting at 2 avoids collision with grid values."])),
    N.para(N.rich([("def dfs(r, c, lbl):", {"bold": True}), " recursive flood-fill. Returns 0 if out of bounds or cell is not 1. Otherwise writes the label, recurses in 4 directions, returns total cell count."])),
    N.para(N.rich([("if grid[r][c] != 1: return 0:", {"bold": True}), " this condition catches both sea cells (0) and already-labeled cells (≥2). Both mean 'stop traversal'."])),
    N.para(N.rich([("grid[r][c] = lbl:", {"bold": True}), " overwrite the grid cell with the label. This marks it as visited AND stores island membership in-place."])),
    N.para(N.rich([("island_size[label] = dfs(r, c, label):", {"bold": True}), " run flood-fill, capture the returned size, store in dict. Then increment label for the next island."])),
    N.para(N.rich([("result = max(island_size.values(), default=0):", {"bold": True}), " baseline result handles grids with no 0-cells (all-ones case). default=0 handles empty grids."])),
    N.para(N.rich([("seen = set():", {"bold": True}), " CRITICAL. Collects unique island labels among the ≤4 neighbors. A set deduplicates when the same island borders the 0-cell from multiple sides."])),
    N.para(N.rich([("if grid[nr][nc] > 1:", {"bold": True}), " checks that the neighbor is a labeled island cell (value ≥ 2), not sea (0)."])),
    N.para(N.rich([("sz = 1 + sum(island_size[l] for l in seen):", {"bold": True}), " +1 for the flipped cell itself. Sum only unique island sizes (no double-counting)."])),
    N.para(N.rich([("result = max(result, sz):", {"bold": True}), " update the global maximum if this flip is better."])),
    N.divider(),
]

# Solution 3 (BFS variant)
blocks += [
    N.h2("Solution 3 — Iterative BFS Labeling (Stack-Safe Variant)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive DFS in Solution 2 can hit Python's recursion limit for large all-land grids. The iterative BFS variant uses an explicit queue and avoids this."),
        N.h4("What Doesn't Work"),
        N.para("Recursive DFS with default Python stack depth (~1000) fails for grids where one island spans > 1000 cells in a chain."),
        N.h4("The Key Observation"),
        N.para("BFS and DFS are interchangeable for flood-fill. Both visit every connected cell exactly once. Replacing the call stack with a deque gives iterative BFS with identical correctness and complexity."),
        N.h4("Building the Solution"),
        N.para("Replace the recursive dfs() with bfs_label() that uses a deque. Phase 2 remains identical. Use this variant when n is large or when the interviewer asks about stack overflow."),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque:", {"bold": True}), " for O(1) popleft (list.pop(0) is O(n))."])),
    N.para(N.rich([("q = deque([(r, c)]);  grid[r][c] = lbl:", {"bold": True}), " seed the queue with the starting cell, immediately label it to prevent re-queueing."])),
    N.para(N.rich([("while q: cr, cc = q.popleft():", {"bold": True}), " process cells in BFS order. Size is incremented for each dequeued cell."])),
    N.para(N.rich([("if grid[nr][nc] == 1:", {"bold": True}), " only queue 1-cells (unlabeled land). Mark them immediately when queued (not when dequeued) to prevent duplicate queueing."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (flip + BFS)", "O(n⁴)", "O(n²)", "TLE for n > ~100"],
        ["Label + Try Flip (DFS)", "O(n²)", "O(n²)", "Interview pick — optimal"],
        ["Label + Try Flip (BFS)", "O(n²)", "O(n²)", "Stack-safe, same complexity"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Algorithms", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Label Islands + Try Flip", {})])),
    N.para(N.rich([("Section: ", {"bold": True}), ("17.1 — Depth First Search (DFS) in DSA_Patterns_and_SubPatterns_Guide.md", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern:\n", {"bold": True}),
            ("• Problem asks to make exactly one edit to a binary grid and maximize connected component size\n"
             "• Repeated DFS/BFS over unchanged components is the bottleneck → precompute sizes\n"
             "• Need to merge sizes of distinct groups that meet at a single boundary cell\n"
             "• Phrase: 'change at most one 0 to 1' or 'connect two regions'", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Foundation DFS for counting connected 1-components; essential building block")])),
    N.bullet(N.rich([("Max Area of Island", {"bold": True}), (" (Medium) — Same as Phase 1 of this problem; find largest island without any flip")])),
    N.bullet(N.rich([("Number of Islands II", {"bold": True}), (" (Hard) — Online Union-Find: each added cell merges islands dynamically; inverse approach")])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}), (" (Medium) — DFS from borders to label safe cells; label + query pattern")])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}), (" (Medium) — Two-phase DFS (one per ocean); 'label first, query second' intuition")])),
    N.bullet(N.rich([("Number of Distinct Islands", {"bold": True}), (" (Medium) — DFS + shape encoding; extends island labeling with signature hashing")])),
    N.bullet(N.rich([("Flood Fill", {"bold": True}), (" (Easy) — Simplest DFS flood-fill from a starting cell; pure island marking")])),
    N.bullet(N.rich([("Minimum Number of Days to Disconnect Island", {"bold": True}), (" (Hard) — Island connectivity analysis; relates to articulation points on grid")])),
    N.para("These problems share the core technique: use DFS/BFS to label or measure connected components, then answer queries in O(1) using precomputed results."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 17.1 (DFS), row: Making A Large Island | Hard | Label Islands + Try Flip", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("making_a_large_island")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("Notion blocks appended.")
print("NOTION OK", PAGE_ID)
