"""
Notion update script for: Find K Pairs with Smallest Sums (#373)
Usage: python3 gen_find_k_pairs_with_smallest_sums.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b0-922e-f519e8fa784a"
SLUG = "find_k_pairs_with_smallest_sums"

# ── 1. Set page properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=373,
    pattern="Heaps",
    subpatterns=["Min Heap BFS"],
    tc="O(k log k)",
    sc="O(k)",
    key_insight="Seed a min-heap with column-0 of each row; each pop expands only the j-direction to avoid duplicates.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build new body ────────────────────────────────────────────────────────
print("Building blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("nums1", {"code": True}),
        (" and ", {}),
        ("nums2", {"code": True}),
        (" sorted in non-decreasing order and an integer ", {}),
        ("k", {"code": True}),
        (", return the ", {}),
        ("k", {"code": True}),
        (" pairs ", {}),
        ("[u1, v1], [u2, v2], ...", {"code": True}),
        (" with the smallest sums, where ", {}),
        ("u", {"code": True}),
        (" is from ", {}),
        ("nums1", {"code": True}),
        (" and ", {}),
        ("v", {"code": True}),
        (" is from ", {}),
        ("nums2", {"code": True}),
        (". Return the pairs in any order.", {}),
    ])),
    N.para(N.rich([
        ("Example: nums1 = [1,7,11], nums2 = [2,4,6], k = 3  →  [[1,2],[1,4],[1,6]]", {"italic": True}),
    ])),
    N.divider(),
]

# ── Solution 1: Min Heap BFS (Optimal) ──
SOLUTION1_CODE = """\
import heapq

def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    heap = []
    # Seed: one entry per row at column 0, cap at k rows
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
    result = []
    while heap and len(result) < k:
        s, i, j = heapq.heappop(heap)       # globally smallest remaining
        result.append([nums1[i], nums2[j]])  # record this pair
        if j + 1 < len(nums2):              # advance frontier rightward
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return result"""

blocks += [
    N.h2("Solution 1 — Min Heap BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Imagine laying out all pair sums as a 2D grid: row i corresponds to nums1[i], column j corresponds to nums2[j], and the cell value is nums1[i] + nums2[j]. Because both arrays are sorted, this grid is monotonically non-decreasing as you move right or down. The top-left cell is always the global minimum. You need to visit cells in increasing order of their value — and you need to stop after k visits."),
        N.h4("What Doesn't Work"),
        N.para("The brute-force approach — generate all m×n pairs, sort by sum, take the first k — is O(mn log mn) in time and O(mn) in space. For large arrays (m = n = 10,000) with small k (e.g., k = 5), you'd compute 100 million pairs just to pick 5. That's deeply wasteful."),
        N.h4("The Key Observation"),
        N.para("The grid is monotone: moving right or down always increases the sum (or keeps it equal). This means the globally smallest unvisited cell is always reachable from one of the 'frontier' cells — cells just past what we've already visited. A min-heap can track this frontier efficiently."),
        N.h4("Building the Solution"),
        N.para("Initialize the frontier: seed the heap with the first column of each row — (nums1[i] + nums2[0], i, 0) for each row i. This represents each row's current minimum. Then repeatedly: pop the minimum from the heap (that's the next globally smallest pair), record it, and push (i, j+1) to advance the frontier one step to the right in that row. By seeding all rows at column 0 and only advancing in the j direction, each cell is visited exactly once."),
        N.callout(
            "Analogy: Think of k sorted streams of water flowing downhill. Each stream (row) starts at its leftmost (smallest) point. You repeatedly take a sip from whichever stream is currently lowest — that's the heap pop. After taking a sip from stream i, advance it one step forward — that's the heap push of (i, j+1).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heapq", {"code": True}), (" — Python's min-heap module. heappush/heappop are O(log n).", {})])),
    N.para(N.rich([("if not nums1 or not nums2: return []", {"code": True}), (" — Guard for empty input. No elements means no pairs.", {})])),
    N.para(N.rich([("heap = []", {"code": True}), (" — The min-heap. Python heapq is a min-heap by default; tuples are compared lexicographically (first by sum).", {})])),
    N.para(N.rich([("for i in range(min(k, len(nums1))):", {"code": True}), (" — Seed at most k rows. Rows beyond k cannot contribute to the k-th result (they'd each need sum ≥ nums1[k], already too large).", {})])),
    N.para(N.rich([("heapq.heappush(heap, (nums1[i]+nums2[0], i, 0))", {"code": True}), (" — Push (sum, row_index, col_index). We store i and j so we can look up the pair and compute the next push.", {})])),
    N.para(N.rich([("while heap and len(result) < k:", {"code": True}), (" — Loop until we have k pairs or the heap is empty (k exceeded total pairs).", {})])),
    N.para(N.rich([("s, i, j = heapq.heappop(heap)", {"code": True}), (" — Extract the globally smallest remaining candidate. Python heappop is O(log n).", {})])),
    N.para(N.rich([("result.append([nums1[i], nums2[j]])", {"code": True}), (" — Record this pair. nums1[i] and nums2[j] are the actual values.", {})])),
    N.para(N.rich([("if j + 1 < len(nums2):", {"code": True}), (" — Check bounds before advancing. If j is already at the last column, no more valid pairs in this row.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (nums1[i]+nums2[j+1], i, j+1))", {"code": True}), (" — Push the next cell in this row (advance j by 1). This is the only expansion — no (i+1, j) push needed since row i+1 is already seeded.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — Returns exactly k pairs (or fewer if total pairs < k).", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOLUTION2_CODE = """\
def kSmallestPairs_brute(nums1, nums2, k):
    pairs = []
    for u in nums1:           # O(m) outer
        for v in nums2:       # O(n) inner: generates all m*n pairs
            pairs.append((u + v, [u, v]))
    pairs.sort()              # O(mn log mn) — dominates
    return [p for _, p in pairs[:k]]"""

blocks += [
    N.h2("Solution 2 — Brute Force Sort (for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest reading of the problem: generate every possible (u, v) pair, compute all their sums, sort by sum, and take the first k."),
        N.h4("What Doesn't Work"),
        N.para("This generates all m*n pairs unconditionally. For large m and n (say 10,000 each), that's 100 million pairs even if k=3. The sorting step alone is O(mn log mn), which is prohibitive."),
        N.h4("The Key Observation"),
        N.para("We don't need to sort all pairs — we only need the k smallest. The brute force is correct but ignores the sorted structure of the input. The heap approach exploits that structure."),
        N.h4("Building the Solution"),
        N.para("Nested loops over all pairs → append (sum, pair) → sort → return first k. Straightforward, but O(mn log mn) time and O(mn) space."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for u in nums1: for v in nums2:", {"code": True}), (" — O(m*n) nested loops generate every possible combination.", {})])),
    N.para(N.rich([("pairs.append((u + v, [u, v]))", {"code": True}), (" — Store (sum, pair) tuple so we can sort by sum.", {})])),
    N.para(N.rich([("pairs.sort()", {"code": True}), (" — Sort all m*n pairs by sum. O(mn log mn) — the bottleneck.", {})])),
    N.para(N.rich([("return [p for _, p in pairs[:k]]", {"code": True}), (" — Unpack and return first k pairs.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Sort", "O(mn log mn)", "O(mn)"],
        ["Min Heap BFS (Optimal)", "O(k log k)", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Heap BFS", {})])),
    N.callout(
        "When to recognize this pattern: Two (or more) sorted arrays/lists and you need the k smallest combinations. "
        "Brute force would generate all combinations then sort. The grid of combinations is monotone (sorted input means "
        "increasing rows and columns). You only need to explore the frontier lazily — that's exactly what a min-heap does.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Min Heap BFS / frontier exploration):"),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — BFS on a 2D monotone grid; identical heap strategy. (#378)", {})])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Heap with one entry per list; pop minimum, push that node's next. (#23)", {})])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Min-heap of size k maintains the k largest seen so far. (#215)", {})])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold": True}), (" (Hard) — Heap tracks current minimum across k sorted lists while advancing the minimum. (#632)", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two heaps (max-heap + min-heap) maintain the running median. (#295)", {})])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), (" (Medium) — Min-heap of size k isolates the most frequent k elements. (#347)", {})])),
    N.para("These problems share the core technique: a min-heap as a priority frontier, extracting the global minimum lazily without generating all candidates upfront."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heap Patterns section. Sub-Pattern: Min Heap BFS. Source: Guide + Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
