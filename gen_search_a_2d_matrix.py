"""
gen_search_a_2d_matrix.py — Notion page rebuild for LeetCode #74 Search a 2D Matrix
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8178-9fe4-f629a26bf5d6"

print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=74,
    pattern="Binary Search",
    subpatterns=["BS: Matrix"],
    tc="O(log mn)",
    sc="O(1)",
    key_insight="Treat the 2D matrix as a flattened 1D sorted array; map virtual index mid to (mid//n, mid%n).",
    icon="🟡"
)
print("Properties set.")

print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

print("Building new body...")
blocks = []

# ── Problem ──
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    "Given an m×n integer matrix where each row is sorted in ascending order, and the first "
    "integer of each row is greater than the last integer of the previous row, return true if "
    "target exists in the matrix, false otherwise. Constraints require an O(log mn) solution."
))
blocks.append(N.divider())

# ── Solution 1: Virtual 1D Binary Search ──
blocks.append(N.h2("Solution 1 — Virtual 1D Binary Search (Interview Pick)"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "We need to efficiently search a 2D grid for a target. The key is to notice that "
        "the two properties together — sorted rows, and each row starts after the previous ends — "
        "make the entire matrix logically equivalent to a single sorted array of length m×n. "
        "The 2D structure is just a cosmetic packaging of a 1D sorted sequence."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Brute-force scanning every cell is O(mn) — unacceptable. Scanning rows linearly to find "
        "the candidate row, then binary searching within it, is O(m + log n). Better, but still "
        "not optimal. We can do O(log mn) by treating the entire matrix as one sorted sequence."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Reading the matrix row-by-row from top-left to bottom-right produces a globally sorted "
        "sequence. So we can binary search over 'virtual indices' 0 through m*n-1, converting "
        "each midpoint to (row, col) via integer division and modulo. This is the base-n number "
        "system: row = mid // n, col = mid % n."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1) Set lo=0, hi=m*n-1. 2) Compute mid=(lo+hi)//2. 3) Convert: row=mid//n, col=mid%n. "
        "4) Compare matrix[row][col] with target. 5) Adjust lo or hi, or return True. "
        "6) If loop ends without finding, return False."
    ),
    N.callout(
        "Analogy: Imagine the matrix is a book where each page (row) is numbered sequentially. "
        "Finding page 5 in a 4-column book: page 5 = chapter 5//4=1, position 5%4=1 within that chapter. "
        "Binary search finds the right page without reading every page.",
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("🔬 Algorithm Deep-Dive: Binary Search on Virtual Index Space"))
blocks.append(N.para(
    "Binary search is a general technique for finding an element in a sorted sequence in O(log n) time. "
    "The key invariant: if the target exists, it always lies within the range [lo, hi]. Each iteration "
    "eliminates half the remaining candidates. The virtual index trick extends this to 2D by establishing "
    "a bijection between flat indices and matrix cells — every virtual index maps to exactly one cell, "
    "and vice versa. Because the bijection preserves sorted order (the sequence is globally sorted), "
    "the correctness of binary search on flat indices guarantees correctness on the matrix."
))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def searchMatrix(matrix, target):\n"
    "    if not matrix or not matrix[0]:\n"
    "        return False\n"
    "    m, n = len(matrix), len(matrix[0])\n"
    "    lo, hi = 0, m * n - 1\n"
    "    while lo <= hi:\n"
    "        mid = (lo + hi) // 2\n"
    "        row, col = mid // n, mid % n\n"
    "        val = matrix[row][col]\n"
    "        if val == target:\n"
    "            return True\n"
    "        elif val < target:\n"
    "            lo = mid + 1\n"
    "        else:\n"
    "            hi = mid - 1\n"
    "    return False"
))

blocks.append(N.h3("Line by Line"))
lines = [
    ("if not matrix or not matrix[0]:", "Guard: return False immediately for empty matrix or empty rows."),
    ("m, n = len(matrix), len(matrix[0])", "Extract dimensions: m = number of rows, n = number of columns."),
    ("lo, hi = 0, m * n - 1", "Set virtual index bounds: lo at first element, hi at last (m*n-1, NOT m*n)."),
    ("while lo <= hi:", "Standard binary search loop — runs at most ⌈log₂(mn)⌉ iterations."),
    ("mid = (lo + hi) // 2", "Midpoint of current virtual range. Integer division avoids overflow issues."),
    ("row, col = mid // n, mid % n", "Project to 2D: divide by COLUMNS (n), not rows. row=quotient, col=remainder."),
    ("val = matrix[row][col]", "Read the actual matrix cell at the projected coordinates."),
    ("if val == target: return True", "Exact match found — target exists in the matrix."),
    ("elif val < target: lo = mid + 1", "Mid element is too small → everything at indices ≤ mid is also too small; search right half."),
    ("else: hi = mid - 1", "Mid element is too large → everything at indices ≥ mid is also too large; search left half."),
    ("return False", "Loop ended with lo > hi — target was not found in any virtual index position."),
]
for line, explanation in lines:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {})
    ])))

blocks.append(N.divider())

# ── Solution 2: Two-Phase Binary Search ──
blocks.append(N.h2("Solution 2 — Two-Phase Binary Search"))
blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("Decompose the 2D search into two independent 1D binary searches. First find which row could contain the target (using row boundaries), then search within that specific row."),
    N.h4("What Doesn't Work"),
    N.para("A naive linear scan of rows to find the candidate row is O(m), which is suboptimal. We can binary search the rows too."),
    N.h4("The Key Observation"),
    N.para("Each row has a known range [matrix[r][0], matrix[r][-1]]. We can binary search over rows to find the one whose range brackets the target. Then binary search within it. Same asymptotic complexity as Solution 1, but expressed as two separate searches."),
    N.h4("Building the Solution"),
    N.para("Phase 1: Binary search rows using first/last element boundaries. Phase 2: Binary search within the candidate row. Use Python's while-else to cleanly handle 'no valid row found'."),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def searchMatrix(matrix, target):\n"
    "    m, n = len(matrix), len(matrix[0])\n"
    "    top, bot = 0, m - 1\n"
    "    while top <= bot:\n"
    "        row = (top + bot) // 2\n"
    "        if matrix[row][0] <= target <= matrix[row][-1]:\n"
    "            break  # target is in range of this row\n"
    "        elif target < matrix[row][0]:\n"
    "            bot = row - 1\n"
    "        else:\n"
    "            top = row + 1\n"
    "    else:\n"
    "        return False  # no valid row found\n"
    "    lo, hi = 0, n - 1\n"
    "    while lo <= hi:\n"
    "        mid = (lo + hi) // 2\n"
    "        if matrix[row][mid] == target: return True\n"
    "        elif matrix[row][mid] < target: lo = mid + 1\n"
    "        else: hi = mid - 1\n"
    "    return False"
))

blocks.append(N.divider())

# ── Complexity ──
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space", "Notes"],
    ["Brute Force (scan all)", "O(mn)", "O(1)", "Unacceptable for large matrices"],
    ["Row scan + row binary search", "O(m + log n)", "O(1)", "Suboptimal row finding"],
    ["Virtual 1D Binary Search (S1)", "O(log mn)", "O(1)", "Interview pick — single search"],
    ["Two-Phase Binary Search (S2)", "O(log m + log n) = O(log mn)", "O(1)", "Same complexity, two searches"],
    ["Staircase (for LC #240)", "O(m + n)", "O(1)", "Use when cross-row guarantee absent"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BS: Matrix (Treat as 1D Array)"])))
blocks.append(N.callout(
    "When to recognize this pattern: 'Search in a sorted 2D matrix' — especially when the problem "
    "states both that each row is sorted AND each row starts after the previous row ends. "
    "This cross-row property is the signal that the matrix is globally sorted and can be treated "
    "as a 1D sorted sequence for binary search.",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same Binary Search pattern:"))
related = [
    ("Search a 2D Matrix II", "Medium", "Only row+col sorted, not globally → staircase O(m+n) instead (#240)"),
    ("Binary Search", "Easy", "Classic 1D template — master this before extending to 2D (#704)"),
    ("Search in Rotated Sorted Array", "Medium", "Binary search with decision logic adapted for rotation (#33)"),
    ("Find Minimum in Rotated Sorted Array", "Medium", "Locate pivot using binary search, same half-elimination logic (#153)"),
    ("Koko Eating Bananas", "Medium", "Binary search on answer space rather than array position (#875)"),
    ("First Bad Version", "Easy", "Binary search to find the first element satisfying a condition (#278)"),
    ("Capacity to Ship Packages Within D Days", "Medium", "Binary search for minimum feasible capacity (#1011)"),
    ("Search Insert Position", "Easy", "Standard binary search returning insertion point (#35)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}), f" ({diff}) — {note}"
    ])))
blocks.append(N.para("These problems share the same core technique: binary search with clever boundary elimination."))
blocks.append(N.callout(
    "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search → BS: Matrix",
    "📖", "gray_background"
))

# ── Interactive Explainer ──
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("search_a_2d_matrix")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
