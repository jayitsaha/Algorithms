"""
gen_number_of_distinct_islands.py
Regenerates the Notion page for LeetCode #694 Number of Distinct Islands in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d6-ae0d-f8bc325e0a97"

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=694,
    pattern="Graph Algorithms",
    subpatterns=["DFS + Shape Hash"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Record each island's cell offsets relative to its anchor during DFS; identical offset-tuples = same shape. Store in a set.",
    icon="🟡"
)
print("  Properties OK")

# ── 2. Wipe existing body ──────────────────────────────────────────────────────
print("Wiping page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks")

# ── 3. Build body ─────────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary grid where ", {}),
        ("1", {"code": True}),
        (" = land and ", {}),
        ("0", {"code": True}),
        (" = water, return the number of distinct island shapes. "
         "Two islands are the same shape if one can be translated (not rotated or reflected) "
         "to exactly overlap the other.", {})
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("grid = [[1,1,0,1,1],[1,0,0,0,1],[0,0,0,1,0],[1,1,0,0,0]] → 3. "
             "The top-left and bottom-left islands are the same L-shape; top-right is a different shape; "
             "(2,3) is a single cell.", {})
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: DFS + Offset Tuple ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — DFS + Relative Offset Tuple (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count connected groups of 1s (islands), but deduplicate ones with the same geometry. "
               "The challenge is: how do we tell if two islands at different positions have the same shape?"),
        N.h4("What Doesn't Work"),
        N.para("Comparing absolute coordinates fails — the same L-shape at (0,0) and at (5,3) has completely "
               "different coordinates. Comparing all pairs of islands is O(n²) and too slow."),
        N.h4("The Key Observation"),
        N.para("If we subtract the starting cell's (r, c) from every cell we visit during DFS, all coordinates "
               "become relative to the island's anchor. Two islands with the same shape will always produce "
               "identical relative-offset sequences — regardless of where they sit on the grid."),
        N.h4("Building the Solution"),
        N.para("1. DFS from each unvisited land cell (r0, c0) — the anchor.\n"
               "2. For each cell (r, c) visited, record offset (r - r0, c - c0) in DFS order.\n"
               "3. Convert the list to a tuple and add to a Python set.\n"
               "4. The set deduplicates identical shapes automatically. Return its size."),
        N.callout("Analogy: imagine stamping each island onto paper, cutting it out, and sliding them on top of each other. "
                  "If they overlap perfectly, they're the same shape — and their relative-offset fingerprints will match.",
                  "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numDistinctIslands(grid):\n"
        "    rows, cols = len(grid), len(grid[0])\n"
        "    seen_shapes = set()\n"
        "\n"
        "    def dfs(r, c, r0, c0, shape):\n"
        "        if r < 0 or r >= rows or c < 0 or c >= cols:\n"
        "            return\n"
        "        if grid[r][c] != 1:\n"
        "            return\n"
        "        grid[r][c] = 0                          # flood-fill: mark visited\n"
        "        shape.append((r - r0, c - c0))         # relative offset from anchor\n"
        "        dfs(r+1, c, r0, c0, shape)             # explore down\n"
        "        dfs(r-1, c, r0, c0, shape)             # explore up\n"
        "        dfs(r, c+1, r0, c0, shape)             # explore right\n"
        "        dfs(r, c-1, r0, c0, shape)             # explore left\n"
        "\n"
        "    for r in range(rows):\n"
        "        for c in range(cols):\n"
        "            if grid[r][c] == 1:\n"
        "                shape = []\n"
        "                dfs(r, c, r, c, shape)\n"
        "                seen_shapes.add(tuple(shape))   # list → tuple (hashable)\n"
        "\n"
        "    return len(seen_shapes)",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("seen_shapes = set()", {"code": True}),
                   (" — Will store canonical shape tuples; set deduplication handles counting.", {})])),
    N.para(N.rich([("def dfs(r, c, r0, c0, shape)", {"code": True}),
                   (" — Recursive DFS. r0, c0 = the island's anchor (starting cell).", {})])),
    N.para(N.rich([("if r < 0 or ... or grid[r][c] != 1: return", {"code": True}),
                   (" — Base cases: out of bounds OR water/already visited. Both are terminal.", {})])),
    N.para(N.rich([("grid[r][c] = 0", {"code": True}),
                   (" — Flood-fill: mark this cell visited by overwriting with 0. No separate visited set needed.", {})])),
    N.para(N.rich([("shape.append((r - r0, c - c0))", {"code": True}),
                   (" — The key line. Translates absolute (r, c) into anchor-relative offset. Same shape → same offsets.", {})])),
    N.para(N.rich([("dfs(r+1,c,...); dfs(r-1,c,...); dfs(r,c+1,...); dfs(r,c-1,...)", {"code": True}),
                   (" — Explore all 4 directions. Fixed order = deterministic visit sequence = canonical signature.", {})])),
    N.para(N.rich([("seen_shapes.add(tuple(shape))", {"code": True}),
                   (" — Convert list to tuple (lists aren't hashable). The set auto-deduplicates identical tuples.", {})])),
    N.para(N.rich([("return len(seen_shapes)", {"code": True}),
                   (" — Set size = number of geometrically distinct island shapes.", {})])),
    N.callout("Time O(m·n): each cell visited at most once via DFS. Space O(m·n): call stack + shape set.",
              "⏱️", "gray_background"),
    N.divider(),
]

# ── Solution 2: Direction-Path Encoding ────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS + Direction-Path Encoding (More Robust)"),
    N.toggle_h3("💡 Intuition: Why Direction Paths Are More Robust", [
        N.h4("Reframe the Problem"),
        N.para("The offset-tuple approach works well in practice but has a theoretical weakness: "
               "two different shapes could produce the same set of relative offsets visited in different "
               "DFS traversal orders. This edge case is rare but real."),
        N.h4("The Key Observation"),
        N.para("Instead of recording WHERE we went (coordinates), record HOW we got there: "
               "the sequence of directions taken during DFS. Add a 'B' (backtrack) marker whenever "
               "DFS returns to a parent — this uniquely encodes the branching structure of the traversal."),
        N.h4("Building the Solution"),
        N.para("Label each direction: D=down, U=up, R=right, L=left. Before each recursive call, "
               "append the direction label. After the call returns, append 'B' (backtrack). "
               "The resulting sequence is an unambiguous encoding of the island's DFS traversal tree."),
        N.callout("Think of it as recording the route through a maze: 'go right, go down, backtrack, go right' "
                  "uniquely describes the maze structure regardless of where the maze is located.",
                  "🧭", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numDistinctIslands(grid):\n"
        "    rows, cols = len(grid), len(grid[0])\n"
        "    seen = set()\n"
        "    DIRS = [(1,0,'D'), (-1,0,'U'), (0,1,'R'), (0,-1,'L')]\n"
        "\n"
        "    def dfs(r, c, path):\n"
        "        grid[r][c] = 0                          # mark visited\n"
        "        for dr, dc, label in DIRS:\n"
        "            nr, nc = r + dr, c + dc\n"
        "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n"
        "                path.append(label)              # direction taken\n"
        "                dfs(nr, nc, path)\n"
        "                path.append('B')                # backtrack marker (critical!)\n"
        "\n"
        "    for r in range(rows):\n"
        "        for c in range(cols):\n"
        "            if grid[r][c] == 1:\n"
        "                path = []\n"
        "                dfs(r, c, path)\n"
        "                seen.add(tuple(path))\n"
        "    return len(seen)",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("path.append(label)", {"code": True}),
                   (" — Record direction ('D'/'U'/'R'/'L') before recursing into a neighbor.", {})])),
    N.para(N.rich([("path.append('B')", {"code": True}),
                   (" — After returning from a recursive call, append backtrack marker. "
                    "Without this, branching structures like T-shapes would be mis-identified.", {})])),
    N.para(N.rich([("seen.add(tuple(path))", {"code": True}),
                   (" — The direction-path sequence is a canonical, unambiguous shape fingerprint.", {})])),
    N.callout("Why 'B' matters: without backtrack markers, visiting 'D then R' from a branch looks the same "
              "whether you went D-then-R in a straight line or D-branch-R. The 'B' after each recursive return "
              "distinguishes these cases.",
              "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS + Offset Tuple (Interview Pick)", "O(m·n)", "O(m·n)"],
        ["DFS + Direction Path", "O(m·n)", "O(m·n)"],
        ["Brute Force (compare all pairs)", "O((m·n)²)", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Algorithms", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS + Shape Hash", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• '2D binary grid' + '4-directionally connected groups' → DFS island pattern\n"
        "• 'Distinct shapes' or 'same up to translation' → canonical encoding + set\n"
        "• 'How many unique structures?' in a grid → hash each structure's signature\n"
        "• When you need to deduplicate geometric/structural patterns → encode as hashable key",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS + Shape Hash / Island DFS):"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}),
                     (" (Medium) — Base island DFS count; prerequisite for this problem. #200", {})])),
    N.bullet(N.rich([("Number of Distinct Islands II", {"bold": True}),
                     (" (Hard) — Same problem but also count rotations/reflections as equal. #711", {})])),
    N.bullet(N.rich([("Max Area of Island", {"bold": True}),
                     (" (Medium) — DFS to measure island size rather than count shapes. #695", {})])),
    N.bullet(N.rich([("Making a Large Island", {"bold": True}),
                     (" (Hard) — Label islands, then try flipping one water cell. #827", {})])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}),
                     (" (Medium) — DFS from borders to identify capturable 'O' regions. #130", {})])),
    N.bullet(N.rich([("Pacific Atlantic Water Flow", {"bold": True}),
                     (" (Medium) — DFS from two edges to find dual-reachable cells. #417", {})])),
    N.bullet(N.rich([("Flood Fill", {"bold": True}),
                     (" (Easy) — Foundational DFS grid flood pattern. #733", {})])),
    N.para("These problems share the core DFS + flood-fill technique on 2D grids; "
           "this problem adds the shape-hashing layer on top."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 17.1 "
              "(Graph Algorithms → Depth First Search → DFS + Shape Hash)",
              "📚", "gray_background"),
]

# ── Embed ───────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_distinct_islands")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
