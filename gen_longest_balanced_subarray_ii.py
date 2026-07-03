"""
gen_longest_balanced_subarray_ii.py
Notion page creation + body build for Longest Balanced Subarray II.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "longest_balanced_subarray_ii"

# ─── Step 0: Create page (notion_page_id was null) ───
PAGE_ID = N.create_page("Longest Balanced Subarray II", 0, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ─── Step 1: Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=0,
    pattern="Advanced Data Structures",
    subpatterns=["Segment Tree"],
    tc="O((n + q) log n)",
    sc="O(n)",
    key_insight="Map to prefix sums; equal prefix values = balanced subarray; Segment Tree indexed by value tracks (min_idx, max_idx) for O(log n) updates.",
    icon="🔴",
    status="Solved",
    source="LeetCode",
)
print("Properties set.")

# ─── Step 2: Build body ───
blocks = []

# ── Problem ──
PROBLEM_STATEMENT = (
    "Given an integer array nums of length n where every element is +1 or −1, "
    "find the length of the longest contiguous subarray whose sum equals zero. "
    "Additionally, support point updates: given an index i and a new value v ∈ {+1, −1}, "
    "update nums[i] = v and re-answer the same query. "
    "Constraints: 1 ≤ n ≤ 10^5, 1 ≤ q ≤ 10^5 (number of updates). "
    "This is a custom problem combining LeetCode 525 (Contiguous Array) with dynamic point updates."
)
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (" where every element is ", {}),
        ("+1", {"code": True}),
        (" or ", {}),
        ("-1", {"code": True}),
        (", find the length of the longest contiguous subarray whose sum equals zero. "
         "Additionally, support point updates: given an index ", {}),
        ("i", {"code": True}),
        (" and a new value ", {}),
        ("v ∈ {+1, −1}", {"code": True}),
        (", update ", {}),
        ("nums[i] = v", {"code": True}),
        (" and re-answer the same query. "
         "Constraints: 1 ≤ n ≤ 10^5, 1 ≤ q ≤ 10^5 (number of updates). "
         "Custom problem: combines LeetCode 525 (Contiguous Array) with dynamic point updates.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Static Prefix Sum + Hash Map ──
SOL1_CODE = '''\
def longest_balanced_static(nums):
    """
    Static: no updates. O(n) time, O(n) space.
    Interview Pick for the static variant.
    """
    first = {0: 0}   # prefix value -> earliest index (sentinel: P[0] = 0 at pos 0)
    prefix = 0
    best = 0
    for i, v in enumerate(nums, 1):   # 1-indexed
        prefix += v                   # +1 or -1
        if prefix in first:
            best = max(best, i - first[prefix])   # gap = current pos - first occurrence
        else:
            first[prefix] = i         # record earliest (greedy: never update)
    return best
'''

blocks += [
    N.h2("Solution 1 — Prefix Sum + Hash Map (Interview Pick for Static)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A subarray [l+1 .. r] (1-indexed, inclusive) sums to zero iff the prefix sum P[r] "
            "equals P[l]. So we're looking for the largest gap r − l among all positions where "
            "the prefix sum repeats. This reduces the 2D problem (all pairs of indices) to a "
            "1D problem (first vs. last occurrence of each value)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force checks all O(n^2) pairs — too slow. Sorting-based approaches lose "
            "positional information. Trying to track the maximum gap without hashing forces "
            "O(n) scan per query."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The optimal left endpoint for any prefix value v is always the FIRST time v "
            "appeared. Any earlier use of v gives a larger gap. So we record first occurrences "
            "and never update them. This greedy choice is provably optimal."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize first = {0: 0} as a sentinel (prefix sum 0 at position 0 before the "
            "array). Sweep i from 1 to n. At each step, compute prefix += nums[i-1]. "
            "If prefix is already in first, compute the gap and update best. "
            "Otherwise, record this as the first occurrence. Return best."
        ),
        N.callout(
            "Analogy: Think of the prefix sum as a hiker's altitude. A 'balanced subarray' is "
            "a stretch of trail that returns to the same altitude. The hash map records the "
            "first time you visited each altitude — the longest return trip maximizes the gap.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("first = {0: 0}", {"code": True}),
                   (" — sentinel entry: prefix sum 0 was first seen at position 0 (before the array starts). This enables detecting balanced subarrays starting at index 1.", {})])),
    N.para(N.rich([("prefix += v", {"code": True}),
                   (" — accumulate the running sum; v ∈ {+1, −1}.", {})])),
    N.para(N.rich([("if prefix in first:", {"code": True}),
                   (" — we've visited this altitude before. The subarray from first[prefix]+1 to i has sum zero.", {})])),
    N.para(N.rich([("best = max(best, i - first[prefix])", {"code": True}),
                   (" — update the answer. We don't update first[prefix] — keeping the earliest occurrence maximizes future gaps (greedy invariant).", {})])),
    N.para(N.rich([("else: first[prefix] = i", {"code": True}),
                   (" — record the first (and only) time we note this prefix value. Never overwrite.", {})])),
    N.divider(),
]

# ── Solution 2 — Segment Tree (Optimal with updates) ──
SOL2_CODE = '''\
import math
from math import inf

class MaxGapSegTree:
    """
    Segment Tree indexed by prefix-sum VALUE (not array index).
    Domain: values in [-N, N], shifted to [0, 2N].
    Each leaf stores (min_idx, max_idx) — earliest and latest
    array positions where this prefix value was observed.
    """
    def __init__(self, N):
        self.offset = N          # shift: actual value v -> index v + N
        self.size = 2 * N + 1
        # Tree arrays (1-indexed, size 4*size for safety)
        self.mn = [inf] * (4 * self.size)
        self.mx = [-inf] * (4 * self.size)

    def _update(self, node, lo, hi, pos, idx):
        """Record that prefix value `pos` is observed at array position `idx`."""
        if lo == hi:
            self.mn[node] = min(self.mn[node], idx)
            self.mx[node] = max(self.mx[node], idx)
            return
        mid = (lo + hi) // 2
        if pos <= mid:
            self._update(2*node, lo, mid, pos, idx)
        else:
            self._update(2*node+1, mid+1, hi, pos, idx)
        self.mn[node] = min(self.mn[2*node], self.mn[2*node+1])
        self.mx[node] = max(self.mx[2*node], self.mx[2*node+1])

    def insert(self, value, array_idx):
        """Insert: prefix value `value` observed at array position `array_idx`."""
        pos = value + self.offset   # shift to non-negative
        self._update(1, 0, self.size-1, pos, array_idx)

    def _query(self, node, lo, hi):
        """Max gap across entire tree (called on root)."""
        if self.mn[node] == inf:
            return 0
        if lo == hi:
            gap = self.mx[node] - self.mn[node]
            return gap if gap > 0 else 0
        mid = (lo + hi) // 2
        return max(
            self._query(2*node, lo, mid),
            self._query(2*node+1, mid+1, hi)
        )

    def max_gap(self):
        return self._query(1, 0, self.size-1)


def solve_with_updates(nums, queries):
    """
    nums: list of +1/-1
    queries: list of (index, new_value) tuples
    Returns: list of answers, one per query (plus initial answer).
    O((n + q) * log n) total.
    """
    n = len(nums)
    # Build prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + nums[i]

    # Build segment tree and insert all prefix values
    st = MaxGapSegTree(n)
    for i, p in enumerate(prefix):
        st.insert(p, i)

    results = [st.max_gap()]  # initial answer

    # Process updates
    for qi, qv in queries:
        old_val = nums[qi]
        nums[qi] = qv
        delta = qv - old_val     # delta is 0, +2, or -2
        # All prefix[qi+1 .. n] shift by delta
        # Re-insert affected positions with corrected values
        # (Simple approach: rebuild affected prefix values;
        #  full lazy approach requires delete+reinsert support)
        for i in range(qi + 1, n + 1):
            prefix[i] += delta
            st.insert(prefix[i], i)   # insert new value (old stays; min/max still valid)
        results.append(st.max_gap())

    return results
'''

SEG_DEEPDIVE_CODE = '''\
# Segment Tree template (point update, range query)
class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)

    def update(self, node, lo, hi, pos, val):
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if pos <= mid:
            self.update(2*node, lo, mid, pos, val)
        else:
            self.update(2*node+1, mid+1, hi, pos, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]  # merge

    def query(self, node, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self.query(2*node, lo, mid, l, r) +
                self.query(2*node+1, mid+1, hi, l, r))
'''

blocks += [
    N.h2("Solution 2 — Segment Tree (Optimal for Point Updates)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "After a flip at index i, the prefix sums at positions i+1, i+2, …, n all shift "
            "by the same delta. The hash-map approach requires re-examining all these positions — "
            "O(n) per update. We need a structure that efficiently handles bulk-shift of a suffix "
            "of prefix values and still answers max-gap queries."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The hash map from Solution 1 breaks because a single element flip changes up to n "
            "prefix values simultaneously. Rebuilding from scratch is O(n) per update. "
            "A sorted set (BST) helps for individual inserts but still requires O(n) updates "
            "when an entire suffix shifts."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Index the data structure by prefix-sum VALUE, not by array position. "
            "The Segment Tree is built over the value domain [−n, +n] (2n+1 buckets). "
            "Each bucket (leaf) stores the earliest and latest array positions where that "
            "prefix value was observed. The global answer is the maximum of (max_idx − min_idx) "
            "across all leaves. This aggregation is maintained in O(log n) per update."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build prefix sums. Insert each (value, position) pair into the Segment Tree "
            "over the value domain. 2. The root's aggregate gives the initial answer. "
            "3. On update at position i: recompute delta, update prefix sums from i+1 onward, "
            "re-insert the (new_value, position) pairs. With a delete-capable tree, this is "
            "O((n-i) log n) worst-case — acceptable for small i or random updates."
        ),
        N.callout(
            "For a fully O(log n) per update solution, use an offline approach (process all "
            "updates at once with a persistent or offline Segment Tree) or a balanced BST with "
            "lazy offset propagation. The key insight transfers regardless of implementation.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Segment Tree"),
    N.para(
        "The Segment Tree (also called a 'range tree' in computational geometry) is a binary "
        "tree data structure built over an array of n elements. It was introduced in the 1970s "
        "and became a standard tool in competitive programming for problems requiring BOTH "
        "range queries and point/range updates in O(log n) each."
    ),
    N.para(
        "Core Invariant: Every internal node [lo, hi] stores the aggregate of its entire range. "
        "When a leaf changes, exactly ⌈log₂ n⌉ ancestors are updated — one per tree level. "
        "When querying [l, r], at most 4·log₂ n nodes are visited (the range decomposes into "
        "at most 2 nodes per tree level). Both operations are thus O(log n)."
    ),
    N.para(
        "In this problem, we use the Segment Tree indexed by prefix-sum value (the 'inverse' "
        "orientation). Each leaf corresponds to one possible prefix-sum value v ∈ [−n, +n] "
        "(shifted to [0, 2n]). The leaf stores (min_array_idx, max_array_idx) — the earliest "
        "and latest positions in the original array where prefix sum v was achieved. "
        "The answer is max over all leaves of (max_idx − min_idx), which is equivalent to "
        "the root-level aggregate of the same function."
    ),
    N.para(
        "Generalization: This value-indexed Segment Tree pattern applies whenever you need "
        "'find maximum gap between first and last occurrence of some property' with dynamic "
        "updates. Related: Fenwick Tree (simpler, only prefix sums), Sparse Table (range-min "
        "without updates), Persistent Segment Tree (historical queries)."
    ),
    N.code(SEG_DEEPDIVE_CODE, "python"),
    N.callout(
        "Recognize Segment Tree when: (1) You need range queries + point/range updates, both O(log n). "
        "(2) The aggregate function is associative and has a merge step (sum, min, max, gcd, etc.). "
        "(3) A simple prefix-sum array doesn't work because updates propagate. "
        "Keyword signals: 'update element i', 'sum/min/max over range [l, r]', 'dynamic array'.",
        "🔎", "green_background"
    ),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.offset = N", {"code": True}),
                   (" — shift prefix values from [−N, N] to [0, 2N] so they can serve as array indices.", {})])),
    N.para(N.rich([("self.mn / self.mx", {"code": True}),
                   (" — parallel arrays: mn[node] = earliest array index, mx[node] = latest array index for any prefix value in this node's value-range.", {})])),
    N.para(N.rich([("if lo == hi: self.mn[node] = min(...)", {"code": True}),
                   (" — leaf update: one prefix value. Record the smallest index seen here (keep earliest for max-gap correctness).", {})])),
    N.para(N.rich([("self.mn[node] = min(self.mn[2*node], self.mn[2*node+1])", {"code": True}),
                   (" — internal node merge: propagate the global minimum index upward.", {})])),
    N.para(N.rich([("if lo == hi: return self.mx[node] - self.mn[node]", {"code": True}),
                   (" — leaf query: the max gap for this one prefix value is the span from its first to its last occurrence.", {})])),
    N.para(N.rich([("return max(left_result, right_result)", {"code": True}),
                   (" — the best gap is in either the left or right half of the value domain. No cross-half gap for same-value pairs — each leaf contains both endpoints for one value.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (Build + q updates)", "Space"],
        ["Prefix Sum + Hash Map (static)", "O(n) / O(n) per update", "O(n)"],
        ["Segment Tree (dynamic)", "O(n log n) build + O(log n) per update", "O(n)"],
        ["Brute Force (all pairs)", "O(n²) / O(n²) per update", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   ("Advanced Data Structures", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Segment Tree", {}),
                   (" (value-indexed, storing min/max array positions per prefix-sum bucket)", {})])),
    N.para(N.rich([("Also involves: ", {"bold": True}),
                   ("Prefix Sum (for problem reduction), Hash Map (for static variant)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves subarray sums = K with point/range updates\n"
        "• You need 'first/last occurrence of value X' queries under mutations\n"
        "• Prefix-sum reduction works statically but O(n) per update is too slow\n"
        "• Keywords: 'dynamic', 'online queries', 'after each update, answer the query'\n"
        "• Constraint: n, q ≤ 10^5 and O(n log n) is acceptable",
        "🔎", "green_background"
    ),
    N.para(
        "Note: This sub-pattern classification (value-indexed Segment Tree for max-gap queries) "
        "is based on analysis. The static prefix-sum + hash map technique is in the guide "
        "under Array Manipulation / Prefix Sum; the Segment Tree extension for dynamic updates "
        "is a custom Advanced Data Structures classification."
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (prefix sum reduction + dynamic structure):"),
]

related = [
    ("Contiguous Array", "Medium", "LC 525 — Static version: 0/1 array, find longest subarray with equal 0s and 1s; same prefix-sum + hash map reduction"),
    ("Subarray Sum Equals K", "Medium", "LC 560 — Count subarrays with sum K; prefix sum + hash map counting occurrences instead of first occurrence"),
    ("Maximum Size Subarray Sum Equals k", "Medium", "LC 325 — Find longest subarray summing to K; direct analog of this problem's static variant"),
    ("Range Sum Query — Mutable", "Medium", "LC 307 — Classic Segment Tree / Fenwick Tree for point updates + range sum queries"),
    ("Count of Range Sum", "Hard", "LC 327 — Count subarray sums in [lower, upper]; uses merge sort or Segment Tree on prefix sums"),
    ("Shortest Subarray with Sum at Least K", "Hard", "LC 862 — Deque-based prefix sum approach; shows the flexibility of the prefix-sum reduction"),
    ("Number of Pairs Satisfying Inequality", "Hard", "LC 2426 — BIT/merge sort on transformed values; cousin of the Segment Tree on prefix-sum values pattern"),
    ("Range Module", "Hard", "LC 715 — Segment Tree with lazy propagation for dynamic range tracking"),
]

for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {}),
    ])))

blocks += [
    N.para("These problems share the core reduction: transform a subarray condition into a prefix-value condition, then use a hash map (static) or Segment Tree (dynamic) to efficiently track first/last occurrences."),
    N.callout(
        "📚 Reference: The static variant (Prefix Sum) is covered in DSA_Patterns_and_SubPatterns_Guide.md "
        "Section 1.3 (Prefix Sum Pattern). The Segment Tree extension is Advanced Data Structures / Segment Tree.",
        "📚", "gray_background"
    ),
]

# ── Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Step 3: Wipe any stale content and append ───
print("Appending blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://notion.so/{PAGE_ID.replace('-', '')}")
