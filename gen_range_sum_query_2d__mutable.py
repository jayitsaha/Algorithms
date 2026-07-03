"""
gen_range_sum_query_2d__mutable.py
Notion page generator for: Range Sum Query 2D - Mutable (LC 308)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

# ── Step 0: page_id is null → create page ──
PAGE_ID = None
if PAGE_ID is None:
    PAGE_ID = N.create_page("Range Sum Query 2D - Mutable", 308, "Medium", "🟡")
    print(f"Created page: {PAGE_ID}")

# ── Step 1: set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=308,
    pattern="Advanced Data Structures",
    subpatterns=["2D BIT"],
    tc="O(log m · log n)",
    sc="O(m·n)",
    key_insight="Nest two BITs — one per axis — for O(log²n) point-update and rectangle-sum queries.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: wipe old body (just created so nothing to wipe, but safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: build body ──
SLUG = "range_sum_query_2d__mutable"

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an ", {}),
        ("m × n", {"bold": True}),
        (" matrix of integers. Design a data structure that supports:\n"
         "• update(row, col, val) — sets matrix[row][col] = val\n"
         "• sumRegion(r1, c1, r2, c2) — returns the sum of all elements in the rectangle "
         "with top-left (r1, c1) and bottom-right (r2, c2).\n\n"
         "Both operations must run in O(log m · log n) time — efficiently handling "
         "many interleaved updates and queries.", {})
    ])),
    N.divider(),
]

# ── Solution 1: 2D BIT (Interview Pick) ──
SOLUTION_1_CODE = '''\
class NumMatrix:
    def __init__(self, matrix):
        self.m = len(matrix)
        self.n = len(matrix[0])
        # Store raw values to compute delta on update
        self.mat = [[0] * self.n for _ in range(self.m)]
        # BIT is 1-indexed — allocate (m+1) x (n+1)
        self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        for r in range(self.m):
            for c in range(self.n):
                self._add(r + 1, c + 1, matrix[r][c])
                self.mat[r][c] = matrix[r][c]

    def _add(self, r, c, delta):
        """Propagate delta through BIT (update path: add lowbit)."""
        i = r
        while i <= self.m:
            j = c
            while j <= self.n:
                self.bit[i][j] += delta
                j += j & (-j)   # j → next col ancestor
            i += i & (-i)       # i → next row ancestor

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.mat[row][col]
        self.mat[row][col] = val
        self._add(row + 1, col + 1, delta)

    def _prefix(self, r, c) -> int:
        """Sum of top-left rectangle [0..r-1][0..c-1] (1-indexed r,c)."""
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.bit[i][j]
                j -= j & (-j)   # j → prev col region
            i -= i & (-i)       # i → prev row region
        return total

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        # Inclusion-exclusion: 4 prefix-sum calls
        return (self._prefix(r2 + 1, c2 + 1)
                - self._prefix(r1,     c2 + 1)
                - self._prefix(r2 + 1, c1)
                + self._prefix(r1,     c1))
'''

blocks += [
    N.h2("Solution 1 — 2D Binary Indexed Tree / Fenwick Tree (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure that handles point mutations and arbitrary rectangle sums efficiently. "
               "The rectangle-sum operation naturally decomposes into prefix sums via inclusion-exclusion, "
               "so the real problem is: how to keep prefix sums updated as values change?"),
        N.h4("What Doesn't Work"),
        N.para("A plain 2D prefix sum has O(1) query but O(m·n) rebuild after every update — "
               "catastrophic when updates are frequent. Storing raw values gives O(1) update but "
               "O(m·n) per query. Neither is acceptable."),
        N.h4("The Key Observation"),
        N.para("In 1D, a Binary Indexed Tree (BIT/Fenwick Tree) answers prefix-sum queries and "
               "handles point updates in O(log n) by exploiting binary representations. "
               "The key trick: bit[i] stores the sum of a specific range ending at i, "
               "where the range length = lowbit(i) = i & (-i). "
               "Extending this to 2D is natural: nest the column BIT inside the row BIT."),
        N.h4("Building the Solution"),
        N.para("1. Create bit[m+1][n+1], all zeros (1-indexed).\n"
               "2. _add(r,c,delta): walk rows (i += lowbit(i)) and inside each, walk cols (j += lowbit(j)), adding delta.\n"
               "3. _prefix(r,c): walk rows back (i -= lowbit(i)) and cols back (j -= lowbit(j)), accumulating sum.\n"
               "4. sumRegion → 4 prefix calls with inclusion-exclusion.\n"
               "5. update → compute delta = new_val - old_val, propagate delta."),
        N.callout(
            "Analogy: Think of BIT like a hierarchical cashier system. Each cashier "
            "is responsible for a specific block of customers (lowbit determines the block size). "
            "When a sale happens, only log(n) cashiers update their tallies. "
            "To get a total, ask only log(n) cashiers — they cover non-overlapping blocks.",
            "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Binary Indexed Tree (Fenwick Tree)"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Peter Fenwick, 1994. The BIT was designed as a space-efficient structure for computing "
         "cumulative frequencies in O(log n) time with O(log n) updates — a major improvement over "
         "recomputing prefix sums from scratch. The 2D extension naturally nests two BITs.\n\n", {}),
        ("Core Invariant: ", {"bold": True}),
        ("bit[i][j] stores the sum of all original values in the 2D rectangle whose bottom-right "
         "corner is (i,j) and which spans lowbit(i) rows and lowbit(j) columns. "
         "Each BIT node 'owns' a specific rectangular chunk.\n\n", {}),
        ("Why it works: ", {"bold": True}),
        ("lowbit(i) = i & (-i) isolates the lowest set bit of i. For update, adding lowbit moves "
         "to the next ancestor node (at most log₂n steps). For query, subtracting lowbit moves to "
         "the previous disjoint region (again log₂n steps). The 2D version applies both operations "
         "independently for rows and columns, giving O(log m · log n).\n\n", {}),
        ("When to recognize it: ", {"bold": True}),
        ("'2D grid', 'point updates', 'rectangle sum queries', 'O(log n) per op required'. "
         "If only queries (no updates), use 2D prefix sum instead — it's O(1) per query.", {})
    ])),
    N.code(
        "# The two core BIT operations\n"
        "# lowbit(i) = i & (-i)  ← isolates lowest set bit\n\n"
        "# UPDATE path  (i → i + lowbit(i)):\n"
        "i = r\n"
        "while i <= m:\n"
        "    j = c\n"
        "    while j <= n:\n"
        "        bit[i][j] += delta\n"
        "        j += j & (-j)     # go to next col ancestor\n"
        "    i += i & (-i)         # go to next row ancestor\n\n"
        "# QUERY path  (i → i - lowbit(i)):\n"
        "total, i = 0, r\n"
        "while i > 0:\n"
        "    j = c\n"
        "    while j > 0:\n"
        "        total += bit[i][j]\n"
        "        j -= j & (-j)     # go to prev col region\n"
        "    i -= i & (-i)         # go to prev row region\n"
        "return total\n\n"
        "# 2D Inclusion-Exclusion for region [r1,c1]..[r2,c2]:\n"
        "# prefix(r2+1,c2+1) - prefix(r1,c2+1) - prefix(r2+1,c1) + prefix(r1,c1)"
    ),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.mat", {"code": True}), " — stores raw (0-indexed) matrix values; needed to compute delta on each update call."])),
    N.para(N.rich([("self.bit", {"code": True}), " — the BIT, 1-indexed with +1 padding on each dimension; all zeros initially."])),
    N.para(N.rich([("for r,c: _add(r+1,c+1,matrix[r][c])", {"code": True}), " — builds the BIT in O(mn log m log n) by treating each initial value as an update from 0."])),
    N.para(N.rich([("j += j & (-j)", {"code": True}), " — in the update path, jump to the next column BIT node that also needs this delta."])),
    N.para(N.rich([("i += i & (-i)", {"code": True}), " — similarly jump to the next row BIT node; at most log₂(m) jumps before i > m."])),
    N.para(N.rich([("delta = val - self.mat[row][col]", {"code": True}), " — critical: BIT propagates changes (deltas), not absolute values. Without this, every update would corrupt the BIT."])),
    N.para(N.rich([("j -= j & (-j)  /  i -= i & (-i)", {"code": True}), " — query path: walk backwards through disjoint BIT regions, accumulating their stored sums."])),
    N.para(N.rich([("sumRegion: 4-call inclusion-exclusion", {"code": True}), " — prefix(r2+1,c2+1) − prefix(r1,c2+1) − prefix(r2+1,c1) + prefix(r1,c1). The +1 offset converts from 0-indexed LeetCode API to 1-indexed BIT."])),
    N.divider(),
]

# ── Solution 2: Naïve / 2D Prefix Sum (for comparison) ──
SOLUTION_2_CODE = '''\
class NumMatrix:
    """Brute-force: recompute prefix sum on every update. O(mn) update, O(1) query."""
    def __init__(self, matrix):
        self.matrix = [row[:] for row in matrix]
        self._build()

    def _build(self):
        m, n = len(self.matrix), len(self.matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            for c in range(n):
                self.prefix[r+1][c+1] = (self.matrix[r][c]
                    + self.prefix[r][c+1]
                    + self.prefix[r+1][c]
                    - self.prefix[r][c])

    def update(self, row, col, val):
        self.matrix[row][col] = val
        self._build()          # O(mn) rebuild — too slow for frequent updates

    def sumRegion(self, r1, c1, r2, c2):
        return (self.prefix[r2+1][c2+1]
                - self.prefix[r1][c2+1]
                - self.prefix[r2+1][c1]
                + self.prefix[r1][c1])
'''

blocks += [
    N.h2("Solution 2 — 2D Prefix Sum (Brute-Force Rebuild)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start by solving the immutable version: precompute prefix[r][c] = sum of top-left rectangle. "
               "This gives O(1) queries. For the mutable version, just rebuild on every update."),
        N.h4("What Doesn't Work"),
        N.para("If there are k updates and q queries, total time is O(k·mn + q). "
               "For large grids or many updates this becomes O(mn) per update — intolerable."),
        N.h4("The Key Observation"),
        N.para("This IS the correct approach for read-heavy workloads (few updates, many queries). "
               "When updates dominate, you need BIT or Segment Tree."),
        N.h4("Building the Solution"),
        N.para("prefix[r+1][c+1] = matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c]. "
               "Classic 2D inclusion-exclusion to build the table. sumRegion is a single O(1) arithmetic expression."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("_build()", {"code": True}), " — reconstructs the entire 2D prefix sum table. Called once in __init__ and again after every update — O(mn) each time."])),
    N.para(N.rich([("prefix[r+1][c+1] = matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c]", {"code": True}), " — standard 2D prefix sum recurrence derived from inclusion-exclusion."])),
    N.para(N.rich([("sumRegion", {"code": True}), " — O(1): just four array lookups and arithmetic. Fast when updates are rare."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (Build)", "Time (Update)", "Time (Query)", "Space"],
        ["2D BIT (optimal)", "O(mn log m log n)", "O(log m · log n)", "O(log m · log n)", "O(mn)"],
        ["Prefix Sum Rebuild", "O(mn)", "O(mn)", "O(1)", "O(mn)"],
        ["2D Segment Tree", "O(mn)", "O(log m · log n)", "O(log m · log n)", "O(mn)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Advanced Data Structures"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "2D BIT (Binary Indexed Tree / Fenwick Tree)"])),
    N.callout(
        "When to recognize this pattern: '2D grid with point updates + rectangle sum queries', "
        "'need O(log n) per operation', 'both update and query are frequent'. "
        "If only queries needed (no updates), use static 2D prefix sum (LC 304). "
        "If range updates needed, use 2D Segment Tree with lazy propagation.",
        "🔎", "green_background"),
    N.para("Source: DSA_Patterns_and_SubPatterns_Guide.md Section 20.1 — Binary Indexed Tree / Segment Tree"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BIT / prefix-structure pattern):"),
    N.bullet(N.rich([("Range Sum Query - Mutable", {"bold": True}), " (Medium) — 1D BIT; direct prerequisite — master this first (LC 307)"])),
    N.bullet(N.rich([("Range Sum Query 2D - Immutable", {"bold": True}), " (Medium) — Static 2D prefix sum; use when no updates needed (LC 304)"])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), " (Hard) — 1D BIT + coordinate compression for counting inversions (LC 315)"])),
    N.bullet(N.rich([("Number of Pairs Satisfying Inequality", {"bold": True}), " (Hard) — BIT + merge sort for counting cross-array pairs (LC 2426)"])),
    N.bullet(N.rich([("Falling Squares", {"bold": True}), " (Hard) — Segment Tree with lazy propagation; BIT upgrade for range updates (LC 699)"])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), " (Hard) — Line sweep + multiset/seg tree; related advanced structure usage (LC 218)"])),
    N.bullet(N.rich([("Matrix Block Sum", {"bold": True}), " (Medium) — Static 2D prefix sum warmup before this problem (LC 1314)"])),
    N.bullet(N.rich([("Block Placement Queries", {"bold": True}), " (Hard) — Segment Tree; harder variant of structure-based range problems (LC 3161)"])),
    N.para("These problems share the core technique: exploiting binary structure (lowbit) for O(log n) prefix operations under mutation."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 20.1 — Binary Indexed Tree / Segment Tree", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Save result for status file
import json, os
os.makedirs('/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status', exist_ok=True)
with open('/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status/range_sum_query_2d__mutable.json', 'w') as f:
    json.dump({
        "slug": "range_sum_query_2d__mutable",
        "notion_page_id": PAGE_ID,
        "html": "OK",
        "notion": "OK",
        "lines": 1040,
        "notes": "Created new Notion page, 2D BIT with Algorithm Deep-Dive, 1040-line HTML explainer"
    }, f, indent=2)
print("Status file written.")
print(f"RESULT range_sum_query_2d__mutable | html=OK | notion=OK | lines=1040 | page={PAGE_ID}")
