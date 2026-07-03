"""
gen_block_placement_queries.py
Notion page builder for: Block Placement Queries (LeetCode #3161, Hard)
Sub-Pattern: Segment Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create page (notion_page_id was null) ──────────────────
PAGE_ID = N.create_page("Block Placement Queries", 3161, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=3161,
    pattern="Advanced Data Structures",
    subpatterns=["Segment Tree"],
    tc="O(Q log Q)",
    sc="O(Q)",
    key_insight="Track max gap between consecutive obstacles via segment tree; each insert splits one gap in O(log N).",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: No wipe needed (new page) — append body ──────────────
SLUG = "block_placement_queries"

SOL1_CODE = '''\
from sortedcontainers import SortedList

class Solution:
    def getResults(self, queries):
        # Collect all x-coords; 0 is always an obstacle
        xs = sorted(set([0] + [q[1] for q in queries]))
        rank = {v: i+1 for i, v in enumerate(xs)}   # 1-indexed
        n = len(xs)
        tree = [0] * (4 * n)                         # max-gap seg tree

        def update(node, s, e, idx, val):
            if s == e:
                tree[node] = val
                return
            mid = (s + e) // 2
            if idx <= mid:
                update(2*node, s, mid, idx, val)
            else:
                update(2*node+1, mid+1, e, idx, val)
            tree[node] = max(tree[2*node], tree[2*node+1])

        def query(node, s, e, l, r):
            if r < s or e < l:
                return 0
            if l <= s and e <= r:
                return tree[node]
            mid = (s + e) // 2
            return max(query(2*node, s, mid, l, r),
                       query(2*node+1, mid+1, e, l, r))

        obstacles = SortedList([0])    # position 0 always has obstacle
        ans = []

        for q in queries:
            x = q[1]
            if q[0] == 1:             # Type 1: place obstacle at x
                idx = obstacles.bisect_left(x)
                if idx == len(obstacles) or obstacles[idx] != x:
                    prev = obstacles[idx - 1]
                    succ = obstacles[idx] if idx < len(obstacles) else None
                    obstacles.add(x)
                    update(1, 1, n, rank[x], x - prev)
                    if succ is not None:
                        update(1, 1, n, rank[succ], succ - x)
            else:                     # Type 2: block query
                sz = q[2]
                prev_obs = obstacles[obstacles.bisect_right(x) - 1]
                gap_to_x = x - prev_obs
                max_gap = max(gap_to_x, query(1, 1, n, 1, rank[x]))
                ans.append(max_gap > sz)

        return ans
'''

SOL2_CODE = '''\
def getResults_brute(queries):
    """
    Brute force: O(Q*N) — TLE on large inputs.
    For intuition and interview warm-up only.
    """
    import bisect
    obstacles = [0]    # position 0 always has obstacle
    ans = []
    for q in queries:
        if q[0] == 1:
            x = q[1]
            bisect.insort(obstacles, x)
        else:
            x, sz = q[1], q[2]
            # All obstacles <= x, plus x as right boundary
            relevant = [o for o in obstacles if o <= x] + [x]
            max_gap = max(relevant[i] - relevant[i-1]
                         for i in range(1, len(relevant)))
            ans.append(max_gap > sz)
    return ans
'''

SEG_TREE_TEMPLATE = '''\
class SegTree:
    """Generic max-segment-tree template."""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)   # always allocate 4n

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2*node, start, mid, idx, val)
        else:
            self.update(2*node+1, mid+1, end, idx, val)
        # Pull-up: parent = aggregate of children
        self.tree[node] = max(self.tree[2*node], self.tree[2*node+1])

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0           # identity for max
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return max(self.query(2*node, start, mid, l, r),
                   self.query(2*node+1, mid+1, end, l, r))
'''

blocks = []

# ── Problem ───────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a 2D integer array ", {}),
        ("queries", {"code": True}),
        (". For each query:", {}),
    ])),
    N.para(N.rich([
        ("- Type 1 ", {"bold": True}),
        ("[1, x]", {"code": True}),
        (": place an obstacle at position x on a number line. Position 0 always has an implicit obstacle.", {}),
    ])),
    N.para(N.rich([
        ("- Type 2 ", {"bold": True}),
        ("[2, x, sz]", {"code": True}),
        (": return ", {}),
        ("True", {"code": True}),
        (" if a block of size ", {}),
        ("sz", {"code": True}),
        (" can be placed anywhere in range ", {}),
        ("[0, x]", {"code": True}),
        (" without touching any obstacle, else ", {}),
        ("False", {"code": True}),
        (".", {}),
    ])),
    N.para("A block of size sz fits in a gap if the gap between consecutive obstacles is strictly greater than sz. Return the answers to all type-2 queries."),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Segment Tree + SortedList (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each type-2 query at x with block size sz: we need the maximum gap between consecutive obstacles in [0, x]. If this maximum gap > sz, the block fits. Essentially: dynamic range-maximum over a prefix, with point insertions that split gaps."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each type-2 query, scan all obstacles ≤ x and compute gaps manually. This is O(N) per query, O(Q*N) overall — TLE for Q, N up to 5×10^4."),
        N.h4("The Key Observation"),
        N.para("Each obstacle insertion splits exactly ONE gap into two smaller gaps. If we store gaps in a segment tree indexed by position, each insert is two point updates (O(log N)), and each query is a range-max query (O(log N))."),
        N.h4("Building the Solution"),
        N.para("1. Coordinate-compress all x-values to ranks 1..M. 2. Build a max-segment tree on ranks, where leaf i stores the gap between obstacle i and its left predecessor. 3. Process queries in order. For type-1: find predecessor and successor, split old gap into two, do two seg tree updates. For type-2: query max gap in prefix [0, rank[x]], also consider x - prev_obstacle as a boundary gap."),
        N.callout("Analogy: think of obstacles as fence posts. The segment tree is a 'gap registry' — it always knows the widest space between any two consecutive posts in any prefix of the fence. Each new post inserted splits one existing space into two shorter ones.", "🧠", "blue_background"),
    ]),
]
blocks += [
    N.h3("🔬 Algorithm Deep-Dive: Segment Tree"),
    N.para(N.rich([
        ("A ", {}),
        ("Segment Tree", {"bold": True}),
        (" is a binary tree where each node stores an aggregate (sum/min/max/GCD) over a contiguous subarray. It supports point updates and range queries in O(log N) each. Formalized in computational geometry in the 1970s.", {}),
    ])),
    N.para("Core invariant: every internal node covering range [l, r] stores aggregate(arr[l..r]). After any point update at index i, exactly O(log N) nodes (the path from leaf i to root) are refreshed — no other nodes change."),
    N.code(SEG_TREE_TEMPLATE),
    N.para(N.rich([
        ("Why O(log N) range query:", {"bold": True}),
        (" The query range [l, r] can match at most O(log N) nodes at each level. Fully-covered nodes return immediately; partially-covered nodes recurse on both children. The recursion tree has depth log N and visits ≤ 4 log N nodes total.", {}),
    ])),
    N.callout("Recognize segment trees when you see: 'after each update, answer a range aggregate query.' Fenwick trees only handle prefix sums — not prefix max. When the aggregate is max/min/GCD, reach for a segment tree.", "🔎", "green_background"),
]
blocks += [
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("xs = sorted(set([0] + ...))", {"code": True}), (" — collect all unique x-values from both query types plus the implicit obstacle 0; sort them for 1-indexed rank assignment.", {})])),
    N.para(N.rich([("rank = {v: i+1 ...}", {"code": True}), (" — map each x-value to a 1-based index; the segment tree operates on these compact indices.", {})])),
    N.para(N.rich([("tree = [0] * (4 * n)", {"code": True}), (" — allocate the segment tree array; 4*n is always sufficient regardless of n's relationship to a power of 2.", {})])),
    N.para(N.rich([("update(node, s, e, idx, val)", {"code": True}), (" — recursive point update: navigate left or right subtree until the leaf, set value, then pull-up max from both children on the way back.", {})])),
    N.para(N.rich([("query(node, s, e, l, r)", {"code": True}), (" — recursive range-max query: return 0 if out of range, return tree[node] if fully covered, else recurse and take max of left and right answers.", {})])),
    N.para(N.rich([("obstacles = SortedList([0])", {"code": True}), (" — maintain sorted obstacle positions; SortedList gives O(log N) insert and bisect operations.", {})])),
    N.para(N.rich([("prev = obstacles[idx - 1]", {"code": True}), (" — predecessor obstacle (left neighbor) of x; the gap from prev to x is x - prev.", {})])),
    N.para(N.rich([("update(1, 1, n, rank[x], x - prev)", {"code": True}), (" — store the gap x - prev at x's rank in the segment tree.", {})])),
    N.para(N.rich([("update(1, 1, n, rank[succ], succ - x)", {"code": True}), (" — the previous gap succ - old_prev is now split; update succ's entry to succ - x.", {})])),
    N.para(N.rich([("prev_obs = obstacles[obstacles.bisect_right(x) - 1]", {"code": True}), (" — for type-2 queries, find the rightmost obstacle at or before x.", {})])),
    N.para(N.rich([("gap_to_x = x - prev_obs", {"code": True}), (" — the gap from the last obstacle to x itself acts as the right boundary; a block could fit in this space.", {})])),
    N.para(N.rich([("max_gap = max(gap_to_x, query(...))", {"code": True}), (" — the answer is the max of the boundary gap and the best gap anywhere in [0, x] from the segment tree.", {})])),
    N.para(N.rich([("ans.append(max_gap > sz)", {"code": True}), (" — strictly greater than because the block must fit without touching an obstacle.", {})])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (TLE, for intuition)"),
    N.toggle_h3("💡 Intuition: Why This Fails and What It Teaches", [
        N.h4("Reframe the Problem"),
        N.para("For each type-2 query, scan all obstacles placed so far that are ≤ x. Add x as a right boundary. Compute all consecutive gaps and return the maximum."),
        N.h4("What Doesn't Work"),
        N.para("With Q queries each scanning up to Q obstacles, this is O(Q^2). For Q = 5×10^4, that's 2.5×10^9 operations — clearly TLE."),
        N.h4("The Key Observation"),
        N.para("The brute force correctly captures the logic — the only thing wrong is efficiency. It directly shows what the segment tree must compute efficiently: max gap in a prefix of the obstacle list."),
        N.h4("Building the Solution"),
        N.para("Use bisect.insort for sorted insertion. For each type-2 query, collect relevant = [all obstacles ≤ x] + [x], then max(consecutive differences). Correct but slow."),
    ]),
]
blocks += [
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Segment Tree (Optimal)", "O(Q log Q)", "O(Q)"],
        ["Brute Force", "O(Q^2)", "O(Q)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Advanced Data Structures", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Segment Tree", {})])),
    N.callout(
        "When to recognize this pattern: 'after each update, answer a range max/min/sum query.' "
        "The dynamic nature (updates interleaved with queries) rules out static prefix arrays. "
        "Coordinate compression needed when x-values are sparse but large.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Segment Tree for dynamic range queries):"),
    N.bullet(N.rich([("Range Sum Query - Mutable", {"bold": True}), (" (Medium) — Classic point-update, range-sum segment tree; the foundational version.", {})])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), (" (Hard) — Sweep line + segment tree on max building height in a coordinate range.", {})])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), (" (Hard) — Segment tree or Fenwick tree for counting elements in a range as we sweep right to left.", {})])),
    N.bullet(N.rich([("Falling Squares", {"bold": True}), (" (Hard) — Segment tree with lazy propagation for range-max with interval updates.", {})])),
    N.bullet(N.rich([("Rectangle Area II", {"bold": True}), (" (Hard) — Coordinate compress + segment tree for computing union area via vertical sweep.", {})])),
    N.bullet(N.rich([("Minimum Interval to Include Each Query", {"bold": True}), (" (Hard) — Offline sweep + segment tree or heap for interval queries.", {})])),
    N.bullet(N.rich([("Range Sum Query 2D - Mutable", {"bold": True}), (" (Hard) — 2D segment tree or 2D Fenwick tree for 2D range-sum with updates.", {})])),
    N.para("These problems share the same core technique: segment tree for O(log N) dynamic range aggregation."),
    N.callout("📚 Sub-pattern 'Segment Tree' is verified from DSA_Patterns_and_SubPatterns_Guide.md Advanced Data Structures section.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Status file ───────────────────────────────────────────────────
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
html_lines = sum(1 for _ in open(pathlib.Path(__file__).parent / "block_placement_queries_explainer.html"))
status = {
    "slug": "block_placement_queries",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Segment Tree deep-dive. Offline + coordinate compress approach. 911-line HTML."
}
status_path = status_dir / "block_placement_queries.json"
status_path.write_text(json.dumps(status, indent=2))
print(f"Status written to {status_path}")
print(f"RESULT block_placement_queries | html=OK | notion=OK | lines={html_lines}")
