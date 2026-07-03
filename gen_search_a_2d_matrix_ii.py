"""
gen_search_a_2d_matrix_ii.py — Notion update for Search a 2D Matrix II (#240)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8158-95e6-d31c2276e622"

# ── 1) Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=240,
    pattern="Binary Search",
    subpatterns=["Start from Corner (2D Matrix Search)"],
    tc="O(m+n)",
    sc="O(1)",
    key_insight="Start at top-right corner — it's row-max and col-min, enabling decisive row/col elimination at every step.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m × n", {"bold": True}),
        (" integer matrix with each row sorted left-to-right and each column sorted top-to-bottom, determine whether a given ", {}),
        ("target", {"code": True}),
        (" exists in the matrix. Return ", {}),
        ("True", {"code": True}),
        (" if it exists, ", {}),
        ("False", {"code": True}),
        (" otherwise.", {})
    ])),
    N.divider()
]

# ── Solution 1 — Corner Walk ──
blocks += [
    N.h2("Solution 1 — Corner Walk (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have a matrix where rows are sorted left-to-right AND columns are sorted top-to-bottom. You need to search for a target in O(m+n) — better than scanning every cell or binary searching each row. The question is: which starting position gives us a binary choice at every step without any ambiguity?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force (O(m×n)) is too slow. Binary search per row (O(m log n)) ignores column sorting. Treating as a flat 1D array fails because rows don't chain — the last element of row i is not necessarily smaller than the first of row i+1."),
        N.h4("The Key Observation"),
        N.para("The top-right corner (row=0, col=n-1) has a unique property: it is simultaneously the MAXIMUM of its row (row sorted left-to-right, this is the rightmost element) and the MINIMUM of its column (column sorted top-to-bottom, this is the topmost element). This means any comparison gives a decisive, unambiguous choice."),
        N.h4("Building the Solution"),
        N.para("At the top-right corner: if curr > target, the target cannot be in this column (all cells below are even larger) — move left. If curr < target, the target cannot be in this row (all cells to the left are even smaller) — move down. If curr == target, we're done. Each step eliminates an entire row or column. At most m+n−1 steps."),
        N.callout("Analogy: Imagine a price list sorted by both row and column. You're at the most expensive in the cheapest column. Too expensive? Go to a cheaper column. Too cheap? Go to a pricier row. You zero in on the exact price.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code("""def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1          # start at top-right corner
    while row < m and col >= 0:
        curr = matrix[row][col]
        if curr == target:
            return True
        elif curr > target:
            col -= 1             # eliminate entire column
        else:
            row += 1             # eliminate entire row
    return False"""),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(matrix), len(matrix[0])", {"code": True}), (" — Get matrix dimensions: m rows, n columns.", {})])),
    N.para(N.rich([("row, col = 0, n - 1", {"code": True}), (" — Initialize pointer at top-right corner: row 0, last column.", {})])),
    N.para(N.rich([("while row < m and col >= 0:", {"code": True}), (" — Continue only while both pointers are within matrix bounds. AND not OR — each boundary is independently meaningful.", {})])),
    N.para(N.rich([("curr = matrix[row][col]", {"code": True}), (" — Read the value at the current pivot position.", {})])),
    N.para(N.rich([("if curr == target: return True", {"code": True}), (" — Exact match found anywhere in our walk — done.", {})])),
    N.para(N.rich([("elif curr > target: col -= 1", {"code": True}), (" — Pivot is too large. Column col is sorted top-to-bottom, so every cell below is ≥ curr > target. Entire column can be discarded — move left.", {})])),
    N.para(N.rich([("else: row += 1", {"code": True}), (" — Pivot is too small. Row row is sorted left-to-right, so every cell to the left is ≤ curr < target. Entire row can be discarded — move down.", {})])),
    N.para(N.rich([("return False", {"code": True}), (" — Exhausted all reachable cells without finding target. It does not exist in the matrix.", {})])),
    N.divider()
]

# ── Solution 2 — Binary Search per Row ──
blocks += [
    N.h2("Solution 2 — Binary Search per Row"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each row is a sorted array. Binary search is the natural tool for searching a sorted array. Apply it row by row."),
        N.h4("What Doesn't Work"),
        N.para("We cannot do a single binary search on the whole matrix because rows don't chain — the end of row i is not necessarily less than the start of row i+1."),
        N.h4("The Key Observation"),
        N.para("Each row is independently sorted, so we can apply bisect.bisect_left on each row. If the position found contains our target, done. Otherwise, try the next row."),
        N.h4("Building the Solution"),
        N.para("Use Python's bisect module for O(log n) per row. Loop over all m rows. Total: O(m log n). This doesn't use column sorting but is simpler to derive under interview pressure. Mention it first, then optimize.")
    ]),
    N.h3("Code"),
    N.code("""import bisect

def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    for row in matrix:
        pos = bisect.bisect_left(row, target)
        if pos < len(row) and row[pos] == target:
            return True
    return False"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for row in matrix:", {"code": True}), (" — Iterate each row (each is a sorted 1D array).", {})])),
    N.para(N.rich([("pos = bisect.bisect_left(row, target)", {"code": True}), (" — Binary search: find leftmost position where target could be inserted. O(log n).", {})])),
    N.para(N.rich([("if pos < len(row) and row[pos] == target:", {"code": True}), (" — Bounds check (pos might be past end) then equality check.", {})])),
    N.callout("This approach ignores column sorting entirely. Mention it as your first idea, then propose the O(m+n) corner walk as the optimization.", "⚠️", "yellow_background"),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Corner Walk (optimal)", "O(m+n)", "O(1)"],
        ["Binary Search per Row", "O(m log n)", "O(1)"],
        ["Brute Force", "O(m×n)", "O(1)"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Start from Corner (2D Matrix Search)", {})])),
    N.callout(
        "When to recognize this pattern: Matrix has BOTH row-wise AND column-wise ascending sort. You need O(m+n) search. You're looking for a cell where one direction increases and another decreases — that's the corner. Signals: 'each row sorted' AND 'each column sorted' together in the same problem.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Search a 2D Matrix", {"bold": True}), (" (Medium) — Fully sorted row-major matrix; binary search as flat 1D array O(log m·n). LeetCode #74.", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — Binary search on value space; count elements ≤ mid using corner walk. LeetCode #378.", {})])),
    N.bullet(N.rich([("Count Negative Numbers in a Sorted Matrix", {"bold": True}), (" (Easy) — Start from bottom-left corner, move right or up to count negatives in O(m+n). LeetCode #1351.", {})])),
    N.bullet(N.rich([("Find a Peak Element II", {"bold": True}), (" (Medium) — 2D matrix binary search on columns for local maximum. LeetCode #1901.", {})])),
    N.bullet(N.rich([("Lucky Numbers in a Matrix", {"bold": True}), (" (Easy) — Element that is minimum in its row and maximum in its column — corner intuition. LeetCode #1380.", {})])),
    N.bullet(N.rich([("Median in Row-Wise Sorted Matrix", {"bold": True}), (" (Hard) — Binary search on value, count ≤ mid per row in O(m log n). Classic interview variant.", {})])),
    N.para("These problems share the same core technique: using the sorted structure of a 2D matrix to eliminate entire rows or columns per comparison."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search (BS: Matrix sub-pattern)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("search_a_2d_matrix_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
