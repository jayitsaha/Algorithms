"""gen_number_of_islands_ii.py — Notion update for Number of Islands II (LC #305)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ab-a32c-d913281de920"
SLUG = "number_of_islands_ii"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=305,
    pattern="Graph",
    subpatterns=["Online Union Find"],
    tc="O(k·α(mn))",
    sc="O(mn)",
    key_insight="Add land → +1; union with each distinct neighbour component → −1. Online Union-Find with path compression + rank answers each query in O(α(mn)).",
    icon="🔴"
)
print("  Properties set OK")

print("Step 2: Wiping old content...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {n_wiped} blocks")

print("Step 3: Building blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m × n", {"bold": True}),
        (" grid initially filled with water. You receive a list of ", {}),
        ("positions", {"code": True}),
        (" where each position ", {}),
        ("positions[i] = [ri, ci]", {"code": True}),
        (" represents an operation that turns the cell at ", {}),
        ("(ri, ci)", {"code": True}),
        (" into land. Return a list of integers where the ", {}),
        ("k-th", {"italic": True}),
        (" integer is the number of islands after the ", {}),
        ("k-th", {"italic": True}),
        (" operation. An island is a maximal group of ", {}),
        ("1", {"code": True}),
        ("s (land) connected ", {}),
        ("4-directionally", {"bold": True}),
        (" (horizontally or vertically).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Online Union-Find (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Online Union-Find (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count connected components in a grid that grows over time — with an answer required after every single growth step. The challenge is the 'online' requirement: we can't batch all operations and process them together."),
        N.h4("What Doesn't Work"),
        N.para("BFS or DFS from scratch after each addition retraverses all existing land cells — O(mn) per query, O(k·mn) total. For k=10,000 operations on a 1000×1000 grid, that's 10^10 operations. Way too slow."),
        N.h4("The Key Observation"),
        N.para("Land is ONLY added (never removed). This means we only ever merge components — we never split them. This monotone-union property is the hallmark of Union-Find: the only supported operation is join two sets, which is exactly what we need."),
        N.h4("Building the Solution"),
        N.para("Maintain a running island count starting at 0. For each new land cell: (1) if it's already land, skip; (2) otherwise, mark it as land, increment count by +1 (new isolated island); (3) for each of its 4 neighbours that is already land, call union — if their roots differ (truly separate components), decrement count by 1. The invariant: count always equals the number of distinct connected land components."),
        N.callout("Analogy: Think of each land cell as its own country. Adding land = new country (+1). Connecting two countries via land bridge = they merge into one (−1). Bridge to already-same country = no change. Union-Find is the bureaucracy tracking which countries are now unified.", "🌏", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find with Path Compression + Union by Rank"),
    N.para(N.rich([
        ("Union-Find (Disjoint Set Union, DSU)", {"bold": True}),
        (" was formalized in the 1970s (Tarjan, 1975 — path compression; Ackermann, 1928 for the bound). It solves the dynamic connectivity problem: maintain a partition of elements into disjoint sets, supporting two operations in near-O(1): ", {}),
        ("union(a, b)", {"code": True}),
        (" (merge the sets containing a and b) and ", {}),
        ("find(x)", {"code": True}),
        (" (return the canonical representative of x's set).", {}),
    ])),
    N.code(
        "# Core Union-Find template (path compression + union by rank)\n"
        "parent = {}  # sparse: only initialized cells\n"
        "rank = {}\n\n"
        "def find(x):\n"
        "    if parent[x] != x:\n"
        "        parent[x] = find(parent[x])  # path compression\n"
        "    return parent[x]\n\n"
        "def union(a, b):\n"
        "    ra, rb = find(a), find(b)\n"
        "    if ra == rb: return False  # same component\n"
        "    if rank[ra] < rank[rb]: ra, rb = rb, ra  # attach smaller under larger\n"
        "    parent[rb] = ra\n"
        "    if rank[ra] == rank[rb]: rank[ra] += 1\n"
        "    return True  # merger happened"
    ),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("parent[x] points toward the root of x's component. The root satisfies parent[root] = root. Path compression flattens all nodes on the path to point directly at the root — the grouping is unchanged, only the pointer structure is shortened. ", {}),
        ("Union by rank: ", {"bold": True}),
        ("always attach the tree of smaller depth under the tree of larger depth. This keeps tree height at O(log n) in the worst case. Combined with path compression, amortized cost is O(α(n)) per operation — where α is the inverse Ackermann function, ≤ 4 for any practical n.", {}),
    ])),
    N.h3("Code"),
    N.code(
        "from typing import List\n\n"
        "def numIslands2(m: int, n: int, positions: List[List[int]]) -> List[int]:\n"
        "    parent = {}   # flat index -> parent flat index (only for land cells)\n"
        "    rank = {}\n"
        "    count = 0\n"
        "    result = []\n\n"
        "    def find(x):\n"
        "        if parent[x] != x:\n"
        "            parent[x] = find(parent[x])  # path compression\n"
        "        return parent[x]\n\n"
        "    def union(a, b):\n"
        "        ra, rb = find(a), find(b)\n"
        "        if ra == rb:\n"
        "            return False  # already in same component\n"
        "        if rank[ra] < rank[rb]:\n"
        "            ra, rb = rb, ra  # attach smaller tree under larger\n"
        "        parent[rb] = ra\n"
        "        if rank[ra] == rank[rb]:\n"
        "            rank[ra] += 1\n"
        "        return True\n\n"
        "    for r, c in positions:\n"
        "        idx = r * n + c\n"
        "        if idx in parent:          # duplicate: already land\n"
        "            result.append(count)\n"
        "            continue\n"
        "        parent[idx] = idx          # new isolated island\n"
        "        rank[idx] = 0\n"
        "        count += 1                 # always +1 for new land\n"
        "        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            nidx = nr * n + nc\n"
        "            if 0 <= nr < m and 0 <= nc < n and nidx in parent:\n"
        "                if union(idx, nidx):\n"
        "                    count -= 1     # real merger: one fewer island\n"
        "        result.append(count)\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = {}", {"code": True}), (" — sparse dict; keys are flat indices of land cells only. Checking ", {}), ("idx in parent", {"code": True}), (" efficiently tells us whether that cell is land.", {})])),
    N.para(N.rich([("rank = {}", {"code": True}), (" — tracks approximate tree height for each root. Used exclusively in ", {}), ("union()", {"code": True}), (" to decide which root becomes the parent.", {})])),
    N.para(N.rich([("count = 0", {"code": True}), (" — the invariant variable. Always equals the number of distinct connected land components. Updated by +1 on new land and −1 on successful union.", {})])),
    N.para(N.rich([("parent[x] = find(parent[x])", {"code": True}), (" — path compression. Recursively follows parent pointers to the root, then directly sets parent[x] to that root. Future find() calls on x (or its former path members) skip directly to root.", {})])),
    N.para(N.rich([("if rank[ra] < rank[rb]: ra, rb = rb, ra", {"code": True}), (" — union by rank. We want to attach the shallower tree under the deeper one. By swapping ra and rb when ra is shallower, we ensure rb (the shallower) is always attached under ra.", {})])),
    N.para(N.rich([("if rank[ra] == rank[rb]: rank[ra] += 1", {"code": True}), (" — only when two equal-depth trees merge does the resulting tree grow by one level. When attaching a shorter under a taller, taller's depth is unchanged.", {})])),
    N.para(N.rich([("idx = r * n + c", {"code": True}), (" — the 2D-to-1D flattening. Unique since 0 ≤ c < n, so no two cells share the same flat index.", {})])),
    N.para(N.rich([("if idx in parent: result.append(count); continue", {"code": True}), (" — crucial duplicate check. If this cell is already land, the island count doesn't change. We must NOT reinitialize its parent/rank or we corrupt the union structure.", {})])),
    N.para(N.rich([("count += 1", {"code": True}), (" — always increment immediately upon first land-marking. The cell starts as an isolated island regardless of what its neighbours do next.", {})])),
    N.para(N.rich([("if union(idx, nidx): count -= 1", {"code": True}), (" — only decrement when union() returns True, meaning the two cells were in genuinely different components. union() returns False when they already share a root — no change to count.", {})])),
    N.divider(),
]

# ── Solution 2: BFS per Query (Brute Force) ──
blocks += [
    N.h2("Solution 2 — BFS Per Query (Brute Force Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("After each land addition, we need to count islands. The simplest definition: run BFS/DFS over the entire grid and count how many times we start a new traversal."),
        N.h4("What Doesn't Work"),
        N.para("This approach recomputes everything from scratch after each operation, discarding all prior work. For k operations on an mn grid, worst-case is O(k·mn). With large inputs this is TLE."),
        N.h4("The Key Observation"),
        N.para("This is correct and easy to reason about — it's the right starting point to propose in an interview before optimizing. Mention it to show your thought process."),
        N.h4("Building the Solution"),
        N.para("Maintain a boolean grid. For each operation, mark the cell as land. Then run a full BFS/DFS counting connected components. The answer for this operation is the component count."),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "from typing import List\n\n"
        "def numIslands2_bfs(m: int, n: int, positions: List[List[int]]) -> List[int]:\n"
        "    grid = [[0] * n for _ in range(m)]\n"
        "    result = []\n\n"
        "    def bfs_count():\n"
        "        visited = [[False] * n for _ in range(m)]\n"
        "        count = 0\n"
        "        for r in range(m):\n"
        "            for c in range(n):\n"
        "                if grid[r][c] == 1 and not visited[r][c]:\n"
        "                    count += 1\n"
        "                    queue = deque([(r, c)])\n"
        "                    visited[r][c] = True\n"
        "                    while queue:\n"
        "                        cr, cc = queue.popleft()\n"
        "                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:\n"
        "                            nr, nc = cr+dr, cc+dc\n"
        "                            if 0<=nr<m and 0<=nc<n and grid[nr][nc]==1 and not visited[nr][nc]:\n"
        "                                visited[nr][nc] = True\n"
        "                                queue.append((nr, nc))\n"
        "        return count\n\n"
        "    for r, c in positions:\n"
        "        grid[r][c] = 1\n"
        "        result.append(bfs_count())\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("grid[r][c] = 1", {"code": True}), (" — mark the new land. Note: no duplicate check needed here since marking an already-1 cell is idempotent.", {})])),
    N.para(N.rich([("bfs_count()", {"code": True}), (" — full O(mn) scan after each operation. This is the bottleneck: runs once per position, making total time O(k·mn).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Per Query (Brute Force)", "O(k·mn)", "O(mn)"],
        ["Online Union-Find (Optimal)", "O(k·α(mn))", "O(mn)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Online Union Find", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Add edges/nodes online, count connected components after each add'\n"
        "• 'Return answer after each modification (not after all modifications)'\n"
        "• Operations are only ADDITIONS (never removals) — UF can't undo/split\n"
        "• Grid with horizontal/vertical adjacency + growing land regions\n"
        "• 'When does the graph become fully connected?' — stop when count == 1",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Online Union-Find / Dynamic Graph Connectivity):"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — Static version; offline BFS/DFS or UF. LeetCode #200", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium) — Find the edge forming a cycle using UF. LeetCode #684", {})])),
    N.bullet(N.rich([("Number of Provinces", {"bold": True}), (" (Medium) — UF on an adjacency matrix to count components. LeetCode #547", {})])),
    N.bullet(N.rich([("Accounts Merge", {"bold": True}), (" (Medium) — Union emails under the same account by root identity. LeetCode #721", {})])),
    N.bullet(N.rich([("Earliest Moment Everyone Becomes Friends", {"bold": True}), (" (Medium) — Process friendship events online; find first moment UF has 1 component. LeetCode #1101", {})])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), (" (Hard) — Binary search + UF or min-heap; related online grid connectivity. LeetCode #778", {})])),
    N.para("These problems all share the core technique: incrementally merge disjoint sets while maintaining a running count or connectivity query."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 5 (Graph → Union-Find). Sub-Pattern: Online Union Find · Source: Guide Section 5 + Analysis", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"  Built {len(blocks)} blocks total")
print("Step 4: Appending blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("  Blocks appended OK")
print(f"NOTION OK {PAGE_ID}")
