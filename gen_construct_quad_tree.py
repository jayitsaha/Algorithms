"""
gen_construct_quad_tree.py — Notion updater for LeetCode #427 Construct Quad Tree
Follows AGENT_BRIEF.md Step 3 pattern exactly.
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-817b-90d6-f93f0ffa22f9"

# ── 1) Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=427,
    pattern="Divide and Conquer",
    subpatterns=["Recursive Quadrant Division"],
    tc="O(n² log n)",
    sc="O(log n)",
    key_insight="A uniform region becomes a leaf; a mixed region divides into four equal quadrants and recurses.",
    icon="🟡"
)
print("Properties OK")

# ── 2) Wipe existing body ──────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3) Build blocks ────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("n×n", {"bold": True}),
        (" matrix ", {}),
        ("grid", {"code": True}),
        (" of ", {}),
        ("0", {"code": True}),
        ("s and ", {}),
        ("1", {"code": True}),
        ("s, construct a Quad Tree representation. Each node has ", {}),
        ("isLeaf", {"code": True}),
        (" (True if all values in its region are the same) and ", {}),
        ("val", {"code": True}),
        (" (the uniform value for leaves; 1 by convention for internal nodes). "
         "Internal nodes always have exactly four children: topLeft, topRight, "
         "bottomLeft, bottomRight — each covering one equal quadrant. "
         "n is guaranteed to be a power of 2.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Naive Recursion
blocks += [
    N.h2("Solution 1 — Naive Recursion (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to build a tree where every node represents a rectangular subgrid. A subgrid is 'done' (a leaf) if it's all-0 or all-1. Otherwise, it's an internal node whose children handle the four equal sub-regions. This structure screams recursion."),
        N.h4("What Doesn't Work"),
        N.para("An iterative approach has no natural order to process subgrid dependencies. You'd need to track which subgrids depend on which — effectively re-implementing a recursion stack manually. Pure recursion is the right model here."),
        N.h4("The Key Observation"),
        N.para("At every level, the decision is binary: uniform (leaf, stop) or mixed (split into four and recurse). The grid is guaranteed to be a power of 2 in size, so halving always yields integers. The recursion depth is exactly log₂(n)."),
        N.h4("Building the Solution"),
        N.para("Define solve(r, c, n): for the n×n subgrid starting at (r,c), scan all n² cells. If all equal → return leaf. Otherwise compute half = n//2 and recurse on four quadrants. Base case: n=1 is always a leaf."),
        N.callout("Analogy: Like a recursive photocopier that first checks if a page is all-white or all-black (collapses to one 'blank' or 'filled' symbol), and only zooms in to split pages that have both.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def construct(grid):
    def solve(r, c, n):
        if n == 1:
            return Node(grid[r][c], True)
        val = grid[r][c]
        uniform = all(
            grid[r+i][c+j] == val
            for i in range(n) for j in range(n))
        if uniform:
            return Node(val, True)
        half = n // 2
        return Node(1, False,
            solve(r,      c,      half),
            solve(r,      c+half, half),
            solve(r+half, c,      half),
            solve(r+half, c+half, half))
    return solve(0, 0, len(grid))"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("solve(r, c, n)", {"code": True}), (" — recursive helper: build the quad tree node for the n×n region at top-left (r, c).", {})])),
    N.para(N.rich([("if n == 1", {"code": True}), (" — base case: a single cell is always a leaf node with val = that cell's value.", {})])),
    N.para(N.rich([("val = grid[r][c]", {"code": True}), (" — reference value: we'll check if every cell in this region equals this first cell.", {})])),
    N.para(N.rich([("uniform = all(...)", {"code": True}), (" — O(n²) scan of all cells in the subgrid. Uniform → return leaf immediately, no further recursion.", {})])),
    N.para(N.rich([("half = n // 2", {"code": True}), (" — split each dimension. Since n is a power of 2, this always yields an integer.", {})])),
    N.para(N.rich([("return Node(1, False, tl, tr, bl, br)", {"code": True}), (" — mixed region → internal node. val=1 by convention (ignored for internal nodes).", {})])),
    N.divider(),
]

# Solution 2 — Prefix Sum Optimization
blocks += [
    N.h2("Solution 2 — Prefix Sum Optimization (Optimal, Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The bottleneck in Solution 1 is the O(n²) uniformity check per call. We need to check: 'are all values in region (r, c, size) the same?' This is equivalent to asking: 'does the sum of 1s equal 0 (all zeros) or equal size² (all ones)?'"),
        N.h4("What Doesn't Work"),
        N.para("Scanning the subgrid every time is O(n²) per call. With O(n² log n) recursive calls in the worst case, naive scanning gives O(n⁴) total — too slow for large grids."),
        N.h4("The Key Observation"),
        N.para("A 2D prefix sum lets us answer 'how many 1s are in any rectangular subgrid?' in O(1). Build it once in O(n²). Then every uniformity check in every recursive call costs O(1) instead of O(n²). This is the standard 2D range sum technique: pre[i][j] = sum of all grid values in the rectangle from (0,0) to (i-1,j-1)."),
        N.h4("Building the Solution"),
        N.para("Build a (n+1)×(n+1) prefix table (1-indexed). Formula: pre[i][j] = grid[i-1][j-1] + pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1]. Query sum(r,c,sz) = pre[r+sz][c+sz] - pre[r][c+sz] - pre[r+sz][c] + pre[r][c]. Then in solve(): if sum=0 → leaf(0), if sum=sz² → leaf(1), else divide."),
        N.callout("Mnemonic: 'Count once, query forever.' Build the prefix sum once, then any uniformity check is just 4 array lookups.", "🧠", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def construct(grid):
    n = len(grid)
    # Build 2D prefix sum (1-indexed)
    pre = [[0]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            pre[i][j] = (grid[i-1][j-1]
                + pre[i-1][j] + pre[i][j-1]
                - pre[i-1][j-1])

    def rsum(r, c, sz):
        r2, c2 = r + sz, c + sz
        return pre[r2][c2] - pre[r][c2] - pre[r2][c] + pre[r][c]

    def solve(r, c, sz):
        s = rsum(r, c, sz)
        if s == 0:       return Node(0, True)
        if s == sz * sz: return Node(1, True)
        h = sz // 2
        return Node(1, False,
            solve(r,   c,   h), solve(r,   c+h, h),
            solve(r+h, c,   h), solve(r+h, c+h, h))

    return solve(0, 0, n)"""
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("pre = [[0]*(n+1) for _ in range(n+1)]", {"code": True}), (" — 1-indexed (n+1)×(n+1) prefix table. Border of zeros simplifies boundary math.", {})])),
    N.para(N.rich([("pre[i][j] = grid[i-1][j-1] + pre[i-1][j] + pre[i][j-1] - pre[i-1][j-1]", {"code": True}), (" — standard 2D inclusion-exclusion prefix formula. Adds above + left, subtracts double-counted top-left corner.", {})])),
    N.para(N.rich([("rsum(r, c, sz)", {"code": True}), (" — query the count of 1s in the sz×sz region at (r,c) using four prefix lookups. O(1).", {})])),
    N.para(N.rich([("if s == 0", {"code": True}), (" — all zeros (no 1s in region) → return leaf with val=0.", {})])),
    N.para(N.rich([("if s == sz * sz", {"code": True}), (" — every cell is 1 (count equals total cells) → return leaf with val=1.", {})])),
    N.para(N.rich([("h = sz // 2", {"code": True}), (" — compute half-size for the four quadrants.", {})])),
    N.para(N.rich([("return Node(1, False, ...)", {"code": True}), (" — mixed region: internal node with val=1 (convention) and four recursive children.", {})])),
    N.callout(
        "Warning: Internal node val=1 is a convention. The problem says val for internal nodes can be anything — the tree structure is what matters. Don't confuse this with leaf val.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Complexity Table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Recursion", "O(n⁴)", "O(log n)"],
        ["Prefix Sum + Recursion (optimal)", "O(n² log n)", "O(n²) prefix + O(log n) stack"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Divide and Conquer (Section 8.2 of guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Recursive Quadrant Division", {})])),
    N.callout(
        "When to recognize this pattern: "
        "• 'Build a spatial tree from a 2D grid' "
        "• 'Uniform subregion becomes a single node' "
        "• 'Divide into 4 equal parts and recurse' "
        "• Powers-of-2 grid size, hierarchical decomposition",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Recursive Quadrant Division / Divide and Conquer):"),
    N.bullet(N.rich([("Logical OR of Two Quad Trees", {"bold": True}), (" (Medium, #558) — Merge two quad trees with OR logic; same recursive node-by-node structure", {})])),
    N.bullet(N.rich([("Maximum Binary Tree", {"bold": True}), (" (Medium, #654) — Find max element, recurse on left/right subarrays; same D&C skeleton", {})])),
    N.bullet(N.rich([("Convert Sorted List to BST", {"bold": True}), (" (Medium, #109) — Find midpoint, recurse on two halves; D&C on 1D structure", {})])),
    N.bullet(N.rich([("Longest Nice Substring", {"bold": True}), (" (Easy, #1763) — Divide on invalid chars and recurse; same Section 8.2 pattern", {})])),
    N.bullet(N.rich([("Range Sum Query 2D — Immutable", {"bold": True}), (" (Medium, #304) — The 2D prefix sum technique used to optimize quad tree uniformity checks", {})])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), (" (Hard, #327) — Merge-sort D&C; count target ranges while merging sorted halves", {})])),
    N.para("These problems share the core idea: divide a spatial structure into equal parts, solve each independently, combine — and stop early when a region is already solved."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 8.2 (Recursion & Divide and Conquer). Sub-Pattern: Recursive Quadrant Division · Source: Guide Section 8.2", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("construct_quad_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ───────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
