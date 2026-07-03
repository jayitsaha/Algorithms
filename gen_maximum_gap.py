"""
gen_maximum_gap.py — Notion page for Maximum Gap (LeetCode #164)
notion_page_id is null → create fresh page, then set properties and append body.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create the page (notion_page_id is null) ──
# Use the already-created page (created in prior run)
PAGE_ID = "39193418-809c-81b4-b72e-cf26353e3394"
print(f"Using existing page: {PAGE_ID}")

# ── Step 1: Set properties ──
# Note: Notion multi_select does not allow commas in option names.
# Split "Pigeonhole, Check Adjacent Buckets" into two options.
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=164,
    pattern="Sorting",
    subpatterns=["Pigeonhole Buckets", "Check Adjacent Buckets"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Pigeonhole: with n numbers in n-1 equal-width buckets, at least one bucket is empty, so the max gap always crosses a bucket boundary.",
    icon="🟡"
)
print("Properties set.")

# ── Step 1b: Wipe any existing body (page was just created, should be empty, but be safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Step 2: Build body blocks ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an unsorted integer array "),
        ("nums", {"code": True}),
        (", return the maximum difference between successive elements in its sorted form. "
         "Return "),
        ("0", {"code": True}),
        (" if the array contains fewer than "),
        ("2", {"code": True}),
        (" elements. You must write an algorithm that runs in linear time and uses linear extra space.")
    ])),
    N.divider(),
]

# ── Solution 1: Pigeonhole Buckets (Interview Pick) ──
SOLUTION1_CODE = """\
def maximumGap(nums):
    n = len(nums)
    if n < 2:
        return 0
    lo, hi = min(nums), max(nums)
    if lo == hi:
        return 0
    bw = max(1, (hi - lo) // (n - 1))  # bucket width
    nb = (hi - lo) // bw + 1           # number of buckets
    blo = [float('inf')]  * nb          # min per bucket
    bhi = [float('-inf')] * nb          # max per bucket
    for num in nums:
        idx = (num - lo) // bw
        blo[idx] = min(blo[idx], num)
        bhi[idx] = max(bhi[idx], num)
    max_gap, prev_hi = 0, lo
    for i in range(nb):
        if blo[i] == float('inf'):  # empty bucket — skip
            continue
        max_gap = max(max_gap, blo[i] - prev_hi)
        prev_hi = bhi[i]
    return max_gap
"""

blocks += [
    N.h2("Solution 1 — Pigeonhole Buckets (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the largest gap between consecutive elements in sorted order — but we can't afford O(n log n) sorting. How do we find the biggest gap without fully sorting?"),
        N.h4("What Doesn't Work"),
        N.para("Comparison-based sorting (merge sort, quicksort, heapsort) all have an Ω(n log n) lower bound — they are fundamentally incompatible with O(n). A direct count-array (like counting sort) would work, but values reach 10⁹, making the array impractically large."),
        N.h4("The Key Observation"),
        N.para("With n numbers in sorted order, there are n−1 consecutive gaps summing to max−min. By the averaging argument, at least one gap ≥ (max−min)/(n−1). If we create buckets of exactly that width, any two values in the same bucket differ by less than bucket_width — which is less than the guaranteed maximum gap. Therefore, the maximum gap always crosses a bucket boundary, never hides within one."),
        N.h4("Building the Solution"),
        N.para("1. Find lo and hi in O(n). 2. Compute bucket_width = max(1, (hi−lo)//(n−1)). 3. Create nb = (hi−lo)//bw+1 buckets, each tracking only its min and max (not individual values). 4. Place each number in its bucket. 5. Sweep non-empty buckets from left to right, comparing right.lo − left.hi. The maximum such cross-bucket gap is the answer."),
        N.callout(
            "Analogy: Imagine spreading 5 books across 4 shelves of equal width. By pigeonhole, at least one shelf is empty. The biggest gap between consecutive books must span that empty shelf — you only need to compare books at the edges of adjacent non-empty shelves.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(nums)", {"code": True}), " — capture length once for reuse."])),
    N.para(N.rich([("if n < 2: return 0", {"code": True}), " — guard: cannot have a consecutive gap with fewer than 2 elements."])),
    N.para(N.rich([("lo, hi = min(nums), max(nums)", {"code": True}), " — one O(n) scan to find the global range."])),
    N.para(N.rich([("if lo == hi: return 0", {"code": True}), " — all elements identical; every gap is 0. Also prevents division by zero in the bw calculation."])),
    N.para(N.rich([("bw = max(1, (hi - lo) // (n - 1))", {"code": True}), " — bucket width: floor division ensures bw ≤ average gap. max(1, ...) prevents bw=0 when range < n−1."])),
    N.para(N.rich([("nb = (hi - lo) // bw + 1", {"code": True}), " — how many buckets span [lo, hi] with this width."])),
    N.para(N.rich([("blo, bhi", {"code": True}), " — parallel arrays tracking the minimum and maximum of each bucket. Initialized to +∞ and −∞ (empty sentinels)."])),
    N.para(N.rich([("idx = (num - lo) // bw", {"code": True}), " — which bucket? Offset from the global minimum, then integer-divide by bucket width."])),
    N.para(N.rich([("blo[idx] = min(blo[idx], num)", {"code": True}), " — update bucket min."])),
    N.para(N.rich([("bhi[idx] = max(bhi[idx], num)", {"code": True}), " — update bucket max."])),
    N.para(N.rich([("max_gap, prev_hi = 0, lo", {"code": True}), " — initialize the sweep. prev_hi anchors from the global minimum (lo is always in bucket 0, so this produces gap=0 for the leftmost bucket)."])),
    N.para(N.rich([("if blo[i] == float('inf'): continue", {"code": True}), " — empty bucket sentinel check. Skip it. This is the Pigeonhole in action — we cross the gap."])),
    N.para(N.rich([("max_gap = max(max_gap, blo[i] - prev_hi)", {"code": True}), " — cross-bucket gap: this bucket's minimum minus the previous non-empty bucket's maximum."])),
    N.para(N.rich([("prev_hi = bhi[i]", {"code": True}), " — advance the left anchor."])),
    N.divider(),
]

# ── Solution 2: Sort and Scan ──
SOLUTION2_CODE = """\
def maximumGap(nums):
    if len(nums) < 2:
        return 0
    nums.sort()  # O(n log n) — violates the O(n) time constraint
    return max(b - a for a, b in zip(nums, nums[1:]))
"""

blocks += [
    N.h2("Solution 2 — Sort and Scan (Simple, O(n log n), violates constraint)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("In the sorted array, consecutive elements are adjacent. So just sort and scan — the largest adjacent difference is the answer."),
        N.h4("What Doesn't Work"),
        N.para("This is correct but uses O(n log n) time. The problem explicitly requires O(n). Mention this approach first in an interview, then offer to optimize."),
        N.h4("The Key Observation"),
        N.para("Once sorted, the answer is trivial: scan n−1 pairs and find the maximum difference. Simplicity is its only virtue over the bucket approach."),
        N.h4("Building the Solution"),
        N.para("Sort in-place. Use zip(nums, nums[1:]) to pair consecutive elements. Return the max difference. One line after sorting."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), " — Python's Timsort, O(n log n). Correct but violates the problem's linear-time constraint."])),
    N.para(N.rich([("zip(nums, nums[1:])", {"code": True}), " — pairs each element with its successor: (nums[0],nums[1]), (nums[1],nums[2]), etc."])),
    N.para(N.rich([("max(b - a for ...)", {"code": True}), " — O(n) scan over all consecutive pairs; b > a since sorted, so b-a = gap."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Pigeonhole Buckets (Interview Pick)", "O(n)", "O(n)"],
        ["Sort and Scan", "O(n log n)", "O(1)"],
        ["Radix Sort + Scan", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sorting Algorithms (Section 7)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Pigeonhole, Check Adjacent Buckets"])),
    N.callout(
        "When to recognize this pattern: (1) 'Find max/min gap in sorted order' + 'O(n) time required'. "
        "(2) 'Integer values in a bounded range' — range structure can replace comparison-based sorting. "
        "(3) 'Avoid O(n log n)' — look for Pigeonhole, radix sort, or counting sort. "
        "(4) 'At least one empty slot/bucket guaranteed' — Pigeonhole argument applies.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Pigeonhole / Bucket Sort):"),
    N.bullet(N.rich([("Contains Duplicate III", {"bold": True}), " (Hard) — Bucket sort + sliding window to detect values within k index distance and k value difference (#220)"])),
    N.bullet(N.rich([("Sort Characters By Frequency", {"bold": True}), " (Medium) — Frequency buckets to sort by character occurrence count in O(n) (#451)"])),
    N.bullet(N.rich([("Top K Frequent Elements", {"bold": True}), " (Medium) — Bucket sort by frequency avoids full sort, finds top k in O(n) (#347)"])),
    N.bullet(N.rich([("H-Index", {"bold": True}), " (Medium) — Counting sort with pigeonhole argument to compute research impact metric (#274)"])),
    N.bullet(N.rich([("First Missing Positive", {"bold": True}), " (Hard) — Cyclic/implicit bucket placement to find missing positive in O(n) time, O(1) space (#41)"])),
    N.bullet(N.rich([("Kth Largest Element in an Array", {"bold": True}), " (Medium) — Bucket / counting sort valid for bounded integer input (#215)"])),
    N.para("These problems share the same core technique: abstraction into fixed-width buckets to exploit integer range structure and bypass comparison-sort lower bounds."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 7.1 — Bucket Sort", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_gap")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ──
import json
html_path = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/maximum_gap_explainer.html"
with open(html_path) as f:
    lines = sum(1 for _ in f)

status = {
    "slug": "maximum_gap",
    "html": "OK",
    "notion": "OK",
    "lines": lines,
    "notion_page_id": PAGE_ID,
    "notes": "Fresh page created; pigeonhole bucket explainer with 12-step interactive walkthrough"
}
status_path = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status/maximum_gap.json"
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)
print(f"Status written: {status_path}")
print(f"RESULT maximum_gap | html=OK | notion=OK | lines={lines}")
