"""
gen_find_peak_element.py — Notion page update for Find Peak Element (LC #162)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8128-b7c0-ca87cc0c1b41"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=162,
    pattern="Binary Search",
    subpatterns=["Compare with Neighbor"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Follow the uphill slope: if nums[mid] < nums[mid+1], peak is in right half; otherwise it's at mid or left. Invariant: peak always in [lo, hi].",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} existing blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 0-indexed integer array ", {}),
        ("nums", {"code": True}),
        (", find a peak element and return its index. A peak element is an element that is strictly greater than its neighbors. The array has imaginary sentinels ", {}),
        ("nums[-1] = nums[n] = -∞", {"code": True}),
        (". You must write an algorithm that runs in O(log n) time. The array may contain multiple peaks — return the index of any one.", {}),
    ])),
    N.callout(
        N.rich([
            ("Constraint: ", {"bold": True}),
            ("nums[i] != nums[i+1]", {"code": True}),
            (" (no adjacent equal elements). This is what makes binary search provably correct — every midpoint has an unambiguous slope direction.", {})
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 1 — Binary Search (Interview Pick)
SOLUTION_1_CODE = """def findPeakElement(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1          # Invariant: a peak exists in [lo, hi]
    while lo < hi:                       # Loop until window collapses to 1 element
        mid = (lo + hi) // 2             # Midpoint (floor division)
        if nums[mid] < nums[mid + 1]:    # Slope goes UP to the right
            lo = mid + 1                 # Peak in [mid+1, hi]; discard left half
        else:                            # Slope goes DOWN from mid
            hi = mid                     # Peak in [lo, mid]; keep mid (could be peak)
    return lo                            # lo == hi: guaranteed peak"""

blocks += [
    N.h2("Solution 1 — Binary Search: Compare with Neighbor (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find any index where the element is higher than both neighbors. We don't need the maximum — just any local high point. This 'any valid answer' framing is the key hint that binary search might work."),
        N.h4("What Doesn't Work"),
        N.para("Linear scan works in O(n) but the problem explicitly requires O(log n). Sorting doesn't help because we need original indices, and sorting destroys the neighbor relationship. We need to exploit some structure to halve the search space each step."),
        N.h4("The Key Observation"),
        N.para("At any index mid, if nums[mid] < nums[mid+1], the array is going uphill to the right. A finite array can't go uphill forever — it must eventually turn down or reach the boundary (which is -∞). That turning point is a peak. So the right half MUST contain a peak. We can safely discard the left half."),
        N.h4("Building the Solution"),
        N.para("Maintain lo and hi as bounds with the invariant: a peak always exists in [lo, hi]. At each midpoint, compare nums[mid] with nums[mid+1]. If uphill, set lo = mid + 1. If downhill or mid is higher, set hi = mid (NOT mid-1 — mid could be the peak!). When lo == hi, the invariant guarantees that single index is a peak."),
        N.callout("Analogy: Hiking in fog. You can only see one step ahead. Rule: always walk uphill. You're guaranteed to reach a peak — it's a local maximum. Binary search is the turbo version: teleport to the midpoint, ask which way is uphill, and eliminate half the mountain.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("lo, hi = 0, len(nums) - 1", {"code": True}),
        (" — Initialize search window to the full array. Loop invariant established: a peak exists in [lo, hi].", {})
    ])),
    N.para(N.rich([
        ("while lo < hi:", {"code": True}),
        (" — Loop until window collapses to exactly one element. Using strict ", {}),
        ("<", {"code": True}),
        (" (not <=) is critical — with ", {}),
        ("hi = mid", {"code": True}),
        (", using <= would cause an infinite loop when lo == hi.", {})
    ])),
    N.para(N.rich([
        ("mid = (lo + hi) // 2", {"code": True}),
        (" — Midpoint by floor division. No overflow risk in Python. Note: this rounds DOWN, which combined with ", {}),
        ("hi = mid", {"code": True}),
        (" avoids infinite loops (mid < hi when lo < hi).", {})
    ])),
    N.para(N.rich([
        ("if nums[mid] < nums[mid + 1]:", {"code": True}),
        (" — Check the slope from mid to mid+1. If the array is going uphill, a peak must be to the right (the uphill must eventually come down or hit the -∞ boundary).", {})
    ])),
    N.para(N.rich([
        ("lo = mid + 1", {"code": True}),
        (" — Discard mid and everything to its left. The peak is strictly in [mid+1, hi]. Safe because mid < hi guarantees mid+1 <= hi.", {})
    ])),
    N.para(N.rich([
        ("hi = mid", {"code": True}),
        (" — nums[mid] >= nums[mid+1]: the array goes downhill or mid is higher. A peak exists at mid or to its left. Set hi = mid, NOT mid-1, because mid itself could be the answer.", {})
    ])),
    N.para(N.rich([
        ("return lo", {"code": True}),
        (" — lo == hi: the window is a single element. The invariant guarantees this is a peak. Return its index.", {})
    ])),
    N.callout(
        N.rich([
            ("Common Mistake: ", {"bold": True}),
            ("Writing ", {}),
            ("hi = mid - 1", {"code": True}),
            (" discards mid, which could itself be the peak when nums[mid] > nums[mid+1]. Always keep mid in the window with ", {}),
            ("hi = mid", {"code": True}),
            (". Second mistake: using ", {}),
            ("lo <= hi", {"code": True}),
            (" causes infinite loops. Use strict ", {}),
            ("lo < hi", {"code": True}),
            (".", {})
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Linear Scan
SOLUTION_2_CODE = """def findPeakElement(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        left  = nums[i-1] if i > 0 else float('-inf')    # Left sentinel
        right = nums[i+1] if i < n-1 else float('-inf')  # Right sentinel
        if nums[i] > left and nums[i] > right:
            return i  # First peak found"""

blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check every element: is it strictly greater than both neighbors? The imaginary -∞ sentinels mean boundary elements only need to beat one real neighbor."),
        N.h4("What Doesn't Work"),
        N.para("Nothing technically wrong — this is correct and simple. But O(n) fails the stated O(log n) requirement. Use this to verify your binary search solution or explain the problem, not as the final answer."),
        N.h4("The Key Observation"),
        N.para("The first peak found is valid because the problem accepts any peak. Linear scan will always find the leftmost peak, which is perfectly correct."),
        N.h4("Building the Solution"),
        N.para("Iterate through every index i. For each, compute left and right neighbors (using -∞ at boundaries). If nums[i] exceeds both, return i."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("for i in range(n):", {"code": True}),
        (" — Check every index, O(n) total.", {})
    ])),
    N.para(N.rich([
        ("left = nums[i-1] if i > 0 else float('-inf')", {"code": True}),
        (" — Implement the -∞ left sentinel: if i is the first index, its left is -∞, so it only needs to beat the right.", {})
    ])),
    N.para(N.rich([
        ("if nums[i] > left and nums[i] > right:", {"code": True}),
        (" — Both neighbor checks in one condition. Return immediately — any valid peak is acceptable.", {})
    ])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Binary Search (Optimal)", "O(log n)", "O(1)", "Halves search space each iteration; always required"],
        ["Linear Scan (Brute Force)", "O(n)", "O(1)", "Correct; fails stated O(log n) requirement"],
        ["Recursive Binary Search", "O(log n)", "O(log n)", "Call stack depth; prefer iterative version"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Compare with Neighbor", {})])),
    N.para(N.rich([
        ("Key Technique: ", {"bold": True}),
        ("Use slope direction (comparison with adjacent element) as the binary search condition instead of a target value. The loop invariant — a peak always exists in [lo, hi] — justifies each pointer move.", {})
    ])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Looking for a local max/min, not global. (2) 'Find any valid answer' phrasing. (3) O(log n) time required explicitly. (4) Array has structure in sub-regions (e.g., mountain or valley shape). (5) Adjacent elements guaranteed distinct.", {})
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Sub-pattern source: ", {"italic": True}),
        ("DSA_Patterns_and_SubPatterns_Guide.md, Section 9 (Binary Search), table row: 'Find Peak Element | Medium | Compare with Neighbor'", {"italic": True})
    ])),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'Compare with Neighbor' binary search technique:"),
    N.bullet(N.rich([
        ("Peak Index in Mountain Array", {"bold": True}),
        (" (Easy) — Identical technique; guaranteed single peak, guaranteed mountain shape. Simple practice for this pattern. (#852)", {})
    ])),
    N.bullet(N.rich([
        ("Find in Mountain Array", {"bold": True}),
        (" (Hard) — First find peak using this exact technique, then binary search ascending and descending halves separately for the target. (#1095)", {})
    ])),
    N.bullet(N.rich([
        ("Find Minimum in Rotated Sorted Array", {"bold": True}),
        (" (Medium) — Compare mid with rightmost element instead of neighbor to find rotation pivot/minimum without knowing the target. (#153)", {})
    ])),
    N.bullet(N.rich([
        ("Search in Rotated Sorted Array", {"bold": True}),
        (" (Medium) — Compare mid with endpoints to identify which half is sorted, then decide based on target. Same 'slope-based elimination' mindset. (#33)", {})
    ])),
    N.bullet(N.rich([
        ("Find Peak Element II (2D Grid)", {"bold": True}),
        (" (Medium) — Extend to matrix: binary search on columns, for each column take the row maximum. Same guarantee: peak exists in remaining columns. (#1901)", {})
    ])),
    N.bullet(N.rich([
        ("Koko Eating Bananas", {"bold": True}),
        (" (Medium) — Binary search on the answer space (speed value), feasibility check per iteration. Related: 'binary search on unsorted domain'. (#875)", {})
    ])),
    N.para("These problems share the core idea: use a structural property (slope direction, sorted half, feasibility) to eliminate half the search space without knowing the exact target."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9: Binary Search, Sub-Pattern: Compare with Neighbor", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_peak_element")),
    N.para(N.rich([
        ("Step through the binary search algorithm visually — use Next/Prev or arrow keys to see each pointer move and slope decision.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── 4) Append all blocks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
