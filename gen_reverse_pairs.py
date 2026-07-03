"""
gen_reverse_pairs.py — Notion update for Reverse Pairs (LC #493).
Run from the Algorithms directory: python3 gen_reverse_pairs.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-810b-993c-f9a87477b139"

# ── 1) Set page properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=493,
    pattern="Sorting",
    subpatterns=["Merge Sort + Count During Merge"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Count reverse pairs (nums[i] > 2*nums[j], i<j) during merge sort by using a two-pointer sweep over sorted halves before the merge step.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe existing body ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the number of reverse pairs. A ", {}),
        ("reverse pair", {"bold": True}),
        (" is a pair (i, j) where ", {}),
        ("i < j", {"code": True}),
        (" and ", {}),
        ("nums[i] > 2 * nums[j]", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: nums = [1, 3, 2, 3, 1]", {"code": True}),
        (" → Answer: 2. Pairs: (1,4) where 3 > 2×1=2, and (3,4) where 3 > 2×1=2.", {}),
    ])),
    N.callout("Edge Cases: empty array → 0. All same values → usually 0 (3 > 6? No). Negative numbers: 2×(-5)=-10, so -1>-10 is true. In Python: no integer overflow; in Java/C++ use long.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force (Understand the Problem)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count pairs of indices (i, j) where i comes before j and the left element exceeds twice the right element. The most direct reading of the problem IS the algorithm: check every possible pair."),
        N.h4("What Doesn't Work (at Scale)"),
        N.para("For n=50,000, there are ~1.25 billion pairs to check. At ~100M operations/second, that's ~12 seconds — way over the 1–2s time limit. This is the O(n²) barrier we must break."),
        N.h4("The Key Observation"),
        N.para("The brute force tells us exactly what we're looking for. Now we need a smarter way to count pairs in bulk rather than one by one."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer i from 0 to n-1, inner j from i+1 to n-1. If nums[i] > 2*nums[j], increment count. Return count."),
        N.callout("Start with brute force in an interview to show you understand the problem, then explain why it's too slow and propose the O(n log n) approach.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def reversePairs_brute(nums):
    count = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > 2 * nums[j]:
                count += 1
    return count""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = 0", {"code": True}), (" — Accumulate the number of qualifying pairs.", {})])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Outer loop: try every possible left index.", {})])),
    N.para(N.rich([("for j in range(i+1, n):", {"code": True}), (" — Inner loop: try every right index j > i.", {})])),
    N.para(N.rich([("if nums[i] > 2 * nums[j]:", {"code": True}), (" — Check the reverse-pair condition (strict >).", {})])),
    N.para(N.rich([("count += 1", {"code": True}), (" — This pair qualifies; increment.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — O(n²) time, O(1) space. Correct but TLEs.", {})])),
    N.divider(),
]

# ── Solution 2: Merge Sort + Count (Interview Pick) ──
blocks += [
    N.h2("Solution 2 — Merge Sort + Count During Merge (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is generalized inversion counting. A standard inversion is any (i,j) with i<j and nums[i]>nums[j]. Here the threshold is higher: nums[i] must exceed 2×nums[j]. The same strategy that counts inversions efficiently — merge sort — applies here."),
        N.h4("What Doesn't Work"),
        N.para("Brute force O(n²) is too slow. Sorting the array first destroys index ordering — we can't track which i came before which j. We need an approach that respects original ordering while still enabling fast counting."),
        N.h4("The Key Observation"),
        N.para("Merge sort recursively divides the array, sorts each half, then merges. At the merge step, both halves are sorted. With two sorted sequences, a two-pointer can count qualifying pairs in O(n): as the left pointer advances (values increase), the right pointer only moves forward (monotone). This gives O(n) counting per merge level, O(log n) levels → O(n log n) total."),
        N.h4("Building the Solution"),
        N.para("Step 1: Recurse left and right (this sorts each half and counts pairs within). Step 2: Count cross-pairs — for each i in sorted left half, advance j in sorted right half while nums[i] > 2*nums[j]; add j-mid. Step 3: Standard merge (separate from counting). The count and merge steps must NOT be interleaved."),
        N.callout("Analogy: Imagine sorting a deck of cards face-down into two sorted piles. Before shuffling the piles together (merge), you quickly count how many left-pile cards beat twice the value of right-pile cards — scanning through both piles once (two-pointer).", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Modified Merge Sort"),
    N.para(N.rich([
        ("Merge Sort", {"bold": True}),
        (" (von Neumann, 1945) is a divide-and-conquer sort running in O(n log n) time and O(n) space. Its invariant: after ", {}),
        ("merge_count(lo, hi)", {"code": True}),
        (" completes, ", {}),
        ("nums[lo:hi]", {"code": True}),
        (" is sorted ascending, AND all reverse pairs with both indices in [lo, hi) have been counted.", {}),
    ])),
    N.para("The key generalization: ANY condition f(left[i], right[j]) that is monotone in i (i.e., if left[i₁] ≤ left[i₂] and f(left[i₁], right[j]) holds, then f(left[i₂], right[j]) holds) can be counted in O(n) per merge level using this two-pointer pattern. For Reverse Pairs, f = nums[i] > 2*nums[j], which satisfies this monotonicity since left is sorted ascending."),
    N.para("When to recognize: 'Count pairs (i,j) with i<j and comparison-of-values condition' — this is the inversion-counting family. If brute force is O(n²) and a monotone two-pointer exists on sorted data, merge sort + count achieves O(n log n)."),
    N.h3("Code"),
    N.code(
"""def reversePairs(nums):
    def merge_count(lo, hi):
        # Base case: 0 or 1 elements, already "sorted", 0 pairs
        if hi - lo <= 1:
            return 0

        mid = (lo + hi) // 2

        # Recurse: sort each half, count pairs within each half
        count  = merge_count(lo, mid)
        count += merge_count(mid, hi)

        # ── COUNT cross-pairs (BEFORE merging) ──
        # Both halves are now sorted. j scans right half.
        j = mid
        for i in range(lo, mid):
            # Advance j while the pair condition holds
            while j < hi and nums[i] > 2 * nums[j]:
                j += 1
            # All right[mid..j) are valid partners for left[i]
            count += j - mid

        # ── MERGE (separate from counting) ──
        # sorted() here; could also write manual merge for guaranteed O(n)
        nums[lo:hi] = sorted(nums[lo:hi])

        return count

    return merge_count(0, len(nums))""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if hi - lo <= 1: return 0", {"code": True}), (" — Base case: single element has no pairs.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Midpoint, used to split and as start of right half.", {})])),
    N.para(N.rich([("count = merge_count(lo, mid) + merge_count(mid, hi)", {"code": True}), (" — Recurse into both halves; each sorts its subarray and returns its within-half count.", {})])),
    N.para(N.rich([("j = mid", {"code": True}), (" — j starts at the BEGINNING of the right half (index mid, NOT lo).", {})])),
    N.para(N.rich([("for i in range(lo, mid):", {"code": True}), (" — Scan the left half element by element.", {})])),
    N.para(N.rich([("while j < hi and nums[i] > 2 * nums[j]: j += 1", {"code": True}), (" — Advance j as long as the pair condition holds. j never backtracks (monotone).", {})])),
    N.para(N.rich([("count += j - mid", {"code": True}), (" — Elements right[mid..j) all satisfy the condition with left[i]. j-mid counts them.", {})])),
    N.para(N.rich([("nums[lo:hi] = sorted(nums[lo:hi])", {"code": True}), (" — Standard merge: sort the subarray for parent calls. Must come AFTER the count loop.", {})])),
    N.callout("Why count += j - mid (not j - lo)? j starts at mid (the start of the right half). After the while loop, j points to the first right-half element that FAILS the condition. So valid right elements are at [mid, j), which is j - mid elements. Using j - lo would incorrectly include left-half indices.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Merge Sort + Count (Interview Pick)", "O(n log n)", "O(n)"],
        ["BIT / Fenwick Tree", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Merge Sort + Count During Merge", {})])),
    N.callout(
        "When to recognize this pattern: 'Count pairs (i,j) with i<j and f(nums[i], nums[j]) true' — especially when brute force is O(n²) and a monotone two-pointer applies on sorted data. Other signals: 'inversion count', 'count smaller to the right', 'count range sums'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), (" (Hard) — For each i, count j>i where nums[j]<nums[i]; merge sort or BIT (#315)", {})])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), (" (Hard) — Count subarrays whose prefix-sum difference is in [lower, upper]; same merge-sort skeleton (#327)", {})])),
    N.bullet(N.rich([("Global and Local Inversions", {"bold": True}), (" (Medium) — Inversion counting concept; check if inversion count = local count (#775)", {})])),
    N.bullet(N.rich([("Sort an Array", {"bold": True}), (" (Medium) — Master clean merge sort before adding the count layer (#912)", {})])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), (" (Hard) — Divide-and-conquer with non-trivial merge step (#218)", {})])),
    N.bullet(N.rich([("Merge Sorted Array", {"bold": True}), (" (Easy) — Foundational merge operation; understanding it cleanly is essential (#88)", {})])),
    N.para("These problems all share the core insight: merge sort provides sorted sub-sequences at every recursion level, enabling O(n) processing per level instead of O(n²)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section. Sub-pattern: Merge Sort + Count During Merge. Source: Analysis.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("reverse_pairs")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
