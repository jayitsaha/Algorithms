"""
gen_kth_smallest_element_in_a_sorted_matrix.py
Regenerates the Notion page for LeetCode #378 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811a-83c0-dfd148d30140"

# ── 1) Set properties ────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=378,
    pattern="Heaps",
    subpatterns=["Merge K Sorted"],
    tc="O(k log n)",
    sc="O(n)",
    key_insight="Treat each row as a sorted stream; seed min-heap with column 0 of every row and pop k times.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("n×n", {"bold": True}),
        (" matrix where each row and column is sorted in ascending order, return the ", {}),
        ("k", {"code": True}),
        ("th smallest element in the matrix.\n\n", {}),
        ("Note: ", {"bold": True}),
        ("It is guaranteed that the answer will always exist within the matrix.\n\n", {}),
        ("Example:\n  matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8 → Output: 13\n"
         "  matrix = [[-5]], k = 1 → Output: -5", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Min-Heap (Interview Pick) ─────────────────────
solution1_code = """\
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    # Seed heap with the front of each row-stream: (value, row, col)
    heap = [(matrix[i][0], i, 0) for i in range(n)]
    heapq.heapify(heap)                    # O(n) — build valid min-heap
    for _ in range(k - 1):                 # k-1 pops to discard elements 1..k-1
        val, r, c = heapq.heappop(heap)    # extract global minimum
        if c + 1 < n:                      # advance that row's stream pointer
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    return heapq.heappop(heap)[0]          # kth pop = kth smallest
"""

blocks += [
    N.h2("Solution 1 — Min-Heap Row Streams (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have n sorted lists running in parallel (one per row). You need the globally kth element if all lists were merged. This is precisely the Merge K Sorted Lists problem — just stored in a 2D matrix."),
        N.h4("What Doesn't Work"),
        N.para("Flattening all n² elements and sorting is O(n² log n) and ignores the sorted structure entirely. You'd pass most test cases but get a TLE on large inputs."),
        N.h4("The Key Observation"),
        N.para("The globally smallest element is always matrix[0][0]. After extracting it, its right neighbor (matrix[0][1]) is the next candidate from row 0. A min-heap maintains the current front of each row-stream and always exposes the global minimum."),
        N.h4("Building the Solution"),
        N.para("1. Seed the heap with (matrix[i][0], i, 0) for each row — the front of each stream.\n2. Pop k times. Each pop yields the next global minimum.\n3. After each pop of (val, r, c), push (matrix[r][c+1], r, c+1) if c+1 < n.\n4. The kth popped value is the answer."),
        N.callout(
            "Analogy: Imagine n conveyor belts, each carrying sorted items. A robot always picks from the belt currently showing the smallest item, then that belt advances by one. After k picks, the robot holds the kth smallest item ever seen.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = [(matrix[i][0], i, 0) for i in range(n)]", {"code": True}), (" — Seed with (value, row, col=0) for each row. Tuple comparison in heapq is lexicographic: value is compared first, so heap ordering is by value naturally.", {})])),
    N.para(N.rich([("heapq.heapify(heap)", {"code": True}), (" — Rearranges in-place to satisfy min-heap property. O(n) time. After this, heap[0] is the globally smallest element.", {})])),
    N.para(N.rich([("for _ in range(k - 1):", {"code": True}), (" — We need k total pops. Do k-1 inside the loop (discard), then one final pop outside to return.", {})])),
    N.para(N.rich([("val, r, c = heapq.heappop(heap)", {"code": True}), (" — Extract the current global minimum in O(log n). Heap re-sorts itself (sifts down).", {})])),
    N.para(N.rich([("if c + 1 < n: heapq.heappush(...)", {"code": True}), (" — Advance row r's stream one step right. If col+1 equals n, the stream is exhausted — do nothing. Heap size stays ≤ n.", {})])),
    N.para(N.rich([("return heapq.heappop(heap)[0]", {"code": True}), (" — The kth pop. Extract the value (index [0] of the (val, r, c) tuple). This is the answer.", {})])),
    N.divider(),
]

# ── Solution 2 — Binary Search on Answer ─────────────────────
solution2_code = """\
def kthSmallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    lo, hi = matrix[0][0], matrix[n - 1][n - 1]  # value search range
    while lo < hi:
        mid = (lo + hi) // 2
        count = _count_le(matrix, mid, n)
        if count < k:
            lo = mid + 1   # fewer than k values <= mid, answer is larger
        else:
            hi = mid       # at least k values <= mid, mid could be the answer
    return lo              # lo == hi == kth smallest value (exists in matrix)

def _count_le(matrix: list[list[int]], target: int, n: int) -> int:
    \"\"\"Count values <= target using O(n) staircase walk from bottom-left.\"\"\"
    count, r, c = 0, n - 1, 0
    while r >= 0 and c < n:
        if matrix[r][c] <= target:
            count += r + 1   # all cells in col c, rows 0..r are <= target
            c += 1           # advance right
        else:
            r -= 1           # current cell too large, go up
    return count
"""

blocks += [
    N.h2("Solution 2 — Binary Search on Answer (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of finding the kth element by extraction, ask: 'How many matrix values are ≤ x?' If we can answer that in O(n) time, we can binary search for the exact threshold x where the count first reaches k."),
        N.h4("What Doesn't Work"),
        N.para("Binary searching on indices doesn't work — the matrix is not row-major sorted. We binary search on values instead (within the range [min, max])."),
        N.h4("The Key Observation"),
        N.para("For any candidate value mid, we can count values ≤ mid in O(n) using a staircase walk: start at the bottom-left corner. If current cell ≤ mid, all cells above it in that column are too — add (r+1) and move right. If current cell > mid, move up."),
        N.h4("Building the Solution"),
        N.para("Binary search on value range [matrix[0][0], matrix[n-1][n-1]]. For each mid, count values ≤ mid. If count < k, answer must be > mid (lo = mid+1). Else answer ≤ mid (hi = mid). lo converges to the kth smallest, which must exist in the matrix."),
        N.callout("Why does lo converge to a matrix value? The binary search always moves lo to mid+1 or hi to mid. Since count < k pushes past non-matrix values and count >= k pulls hi down, lo eventually lands on the smallest matrix value with at least k values ≤ it — the kth smallest.", "🔎", "green_background"),
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = matrix[0][0], matrix[n-1][n-1]", {"code": True}), (" — Binary search range covers all possible values in the matrix.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Candidate value (may not exist in matrix).", {})])),
    N.para(N.rich([("count = _count_le(matrix, mid, n)", {"code": True}), (" — O(n) staircase count.", {})])),
    N.para(N.rich([("if count < k: lo = mid + 1", {"code": True}), (" — Too few values ≤ mid; answer must be larger.", {})])),
    N.para(N.rich([("else: hi = mid", {"code": True}), (" — At least k values ≤ mid; mid could be the answer or we can tighten further.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — lo and hi converge to the kth smallest value, which is guaranteed to exist in the matrix.", {})])),
    N.para(N.rich([("count += r + 1; c += 1", {"code": True}), (" — Staircase: all r+1 rows (0..r) in column c are ≤ target; jump right.", {})])),
    N.divider(),
]

# ── Solution 3 — Brute Force ──────────────────────────────────
solution3_code = """\
import heapq

def kthSmallest_brute(matrix: list[list[int]], k: int) -> int:
    # Flatten entire matrix and sort
    flat = sorted(matrix[r][c] for r in range(len(matrix))
                               for c in range(len(matrix)))
    return flat[k - 1]   # k is 1-indexed
"""

blocks += [
    N.h2("Solution 3 — Brute Force: Flatten and Sort"),
    N.toggle_h3("💡 Intuition: Starting Point", [
        N.h4("Reframe the Problem"),
        N.para("If the matrix weren't sorted at all, we'd have no choice but to look at every element. The simplest approach: collect all values, sort them, return the kth."),
        N.h4("What Doesn't Work (For Interview)"),
        N.para("This ignores the sorted structure completely. O(n² log n²) time, O(n²) space. Acceptable for small matrices but won't pass large test cases. Use it only to establish a baseline — then optimize."),
    ]),
    N.h3("Code"),
    N.code(solution3_code),
    N.h3("Line by Line"),
    N.para(N.rich([("flat = sorted(...)", {"code": True}), (" — Collect all n² values into a list and sort. O(n² log n²) time, O(n²) space.", {})])),
    N.para(N.rich([("return flat[k - 1]", {"code": True}), (" — k is 1-indexed, list is 0-indexed.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (Flatten + Sort)", "O(n² log n)", "O(n²)", "Never use in interview"],
        ["Min-Heap (Interview Pick)", "O(k log n)", "O(n)", "Best when k is small; most intuitive"],
        ["Binary Search on Answer", "O(n log(max−min))", "O(1)", "Best space; good when k is large"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Heaps", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Merge K Sorted (primary) · Binary Search on Answer (secondary)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'kth smallest from multiple sorted sources' → min-heap\n"
        "• 'sorted rows AND sorted columns' → row-stream heap traversal\n"
        "• 'sorted matrix, find kth' → this exact problem pattern\n"
        "• 'merge k sorted lists/arrays' → heap with (val, list_id, idx) entries",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Merge K Sorted / Heap technique:"),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), (" (Hard) — Canonical form: heap of (val, list_idx, node). LeetCode #23", {})])),
    N.bullet(N.rich([("Find K Pairs with Smallest Sums", {"bold": True}), (" (Medium) — Seed heap with (nums1[i]+nums2[0], i, 0); same row-stream pattern. LeetCode #373", {})])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), (" (Medium) — Min-heap of size k; pop when size > k. LeetCode #215", {})])),
    N.bullet(N.rich([("Find Median from Data Stream", {"bold": True}), (" (Hard) — Two-heap pattern: max-heap (lower) + min-heap (upper). LeetCode #295", {})])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold": True}), (" (Hard) — Heap tracks current front of k lists simultaneously. LeetCode #632", {})])),
    N.bullet(N.rich([("Search a 2D Matrix II", {"bold": True}), (" (Medium) — Same sorted-matrix structure; O(m+n) staircase search. LeetCode #240", {})])),
    N.para("These problems all exploit the min-heap's ability to efficiently track the global minimum across multiple sorted streams."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Heaps section, Merge K Sorted sub-pattern. Sub-Pattern verified via Guide + Analysis.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("kth_smallest_element_in_a_sorted_matrix")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
