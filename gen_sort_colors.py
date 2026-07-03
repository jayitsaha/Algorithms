"""
gen_sort_colors.py — Notion update for Sort Colors (#75)
Notion page ID: 39193418-809c-81ca-ab4d-c2192a377180
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ca-ab4d-c2192a377180"

# ─────────────── 1. Set properties ───────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=75,
    pattern="Sorting",
    subpatterns=["Dutch National Flag (3-Way Partition)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Three pointers (lo, mid, hi) partition the array into confirmed-0/unknown/confirmed-2 zones in one pass; only advance mid when element is classified.",
    icon="🟡"
)
print("Properties set.")

# ─────────────── 2. Wipe old body ───────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─────────────── 3. Build body blocks ───────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para("Given an array nums with n objects colored red (0), white (1), or blue (2), sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, blue. You must solve this problem without using the library sort function and in one pass using O(1) extra space."),
    N.para("Example: Input: nums = [2,0,2,1,1,0]  ->  Output: [0,0,1,1,2,2]"),
    N.divider(),
]

# ── Solution 1: Dutch National Flag ──
blocks += [
    N.h2("Solution 1 — Dutch National Flag (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to sort an array in-place where every element is exactly 0, 1, or 2. Because there are only three possible values, we don't need a general comparison sort — we can partition the array directly into three regions by maintaining boundaries for where each value belongs."),
        N.h4("What Doesn't Work"),
        N.para("A library sort works correctly but runs in O(n log n) and uses O(n) auxiliary space. The problem forbids it and asks for one pass with O(1) space. Even counting and filling (two passes) fails the one-pass constraint."),
        N.h4("The Key Observation"),
        N.para("With three distinct values we can always describe the array state using four regions: confirmed-0s on the left, confirmed-1s in the middle-left, unexamined in the middle-right, confirmed-2s on the right. A scan pointer mid moves left to right; each element is immediately routed to its correct region by swapping with a boundary pointer."),
        N.h4("Building the Solution"),
        N.para("Use three pointers: lo (right edge of red zone), mid (scanner), hi (left edge of blue zone). While mid <= hi: if nums[mid]==0, swap with lo and advance both lo and mid (safe because nums[lo] was a confirmed 1); if nums[mid]==1, just advance mid; if nums[mid]==2, swap with hi, retreat hi, but keep mid fixed (the arriving element from hi is unexamined). Total: O(n) single pass, O(1) space."),
        N.callout("Analogy: Imagine physically sorting a shuffled Dutch flag strip. Hold one stripe at a time: red goes to the top, white to the middle, blue to the bottom — but don't peek at what just fell to the middle from the blue stack. That's exactly the algorithm.", "🏳️", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Dutch National Flag"),
    N.para("Origin: Edsger W. Dijkstra, 1976. Named after the Dutch national flag (red-white-blue). Classic 3-way partitioning algorithm."),
    N.para("Core invariant: nums[0..lo-1] = all 0s, nums[lo..mid-1] = all 1s, nums[hi+1..n-1] = all 2s, nums[mid..hi] = unexamined. Every case of the while loop preserves this invariant."),
    N.para("Key subtlety: When swapping a 2 to position hi, do NOT advance mid. The element arriving from hi is unexamined. When swapping a 0 to position lo, advance BOTH lo and mid — nums[lo] was in [lo,mid), guaranteed to be a 1."),
    N.para("Recognition signal: 'Sort or partition array with exactly 3 distinct values in one pass with O(1) space.'"),
    N.code(
        "def sortColors(nums: list[int]) -> None:\n"
        "    lo, mid, hi = 0, 0, len(nums) - 1\n"
        "    while mid <= hi:\n"
        "        if nums[mid] == 0:\n"
        "            nums[lo], nums[mid] = nums[mid], nums[lo]\n"
        "            lo += 1\n"
        "            mid += 1\n"
        "        elif nums[mid] == 1:\n"
        "            mid += 1\n"
        "        else:  # nums[mid] == 2\n"
        "            nums[mid], nums[hi] = nums[hi], nums[mid]\n"
        "            hi -= 1  # do NOT advance mid — arriving element is unexamined"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("lo, mid, hi = 0, 0, len(nums) - 1", {"code": True}),
        (" — Three pointers: lo=right edge of confirmed-0s zone, mid=scan cursor, hi=left edge of confirmed-2s zone. Unknown region = entire array at start.", {}),
    ])),
    N.para(N.rich([
        ("while mid <= hi:", {"code": True}),
        (" — Continue while the unknown region [mid..hi] is non-empty. When mid > hi all elements are classified.", {}),
    ])),
    N.para(N.rich([
        ("if nums[mid] == 0:", {"code": True}),
        (" — Red element found; it belongs in the left zone.", {}),
    ])),
    N.para(N.rich([
        ("nums[lo], nums[mid] = nums[mid], nums[lo]", {"code": True}),
        (" — Move the 0 to the red zone. nums[lo] was a confirmed 1 (inside [lo,mid)), so nums[mid] now holds a known 1.", {}),
    ])),
    N.para(N.rich([
        ("lo += 1; mid += 1", {"code": True}),
        (" — Grow red zone right; the 1 at mid is confirmed, advance scan. Both pointers move.", {}),
    ])),
    N.para(N.rich([
        ("elif nums[mid] == 1:", {"code": True}),
        (" — White element; already in the correct middle zone. No swap needed.", {}),
    ])),
    N.para(N.rich([
        ("mid += 1", {"code": True}),
        (" — Consume the 1 and advance scan. White zone [lo,mid) grows by one.", {}),
    ])),
    N.para(N.rich([
        ("else: # nums[mid] == 2", {"code": True}),
        (" — Blue element; belongs in the right zone.", {}),
    ])),
    N.para(N.rich([
        ("nums[mid], nums[hi] = nums[hi], nums[mid]", {"code": True}),
        (" — Move 2 to the blue zone; element arriving at mid is from unexamined region.", {}),
    ])),
    N.para(N.rich([
        ("hi -= 1", {"code": True}),
        (" — Grow blue zone left. ", {}),
        ("mid is NOT advanced", {"bold": True}),
        (" — the arriving element must be examined on the next iteration.", {}),
    ])),
    N.divider(),
]

# ── Solution 2: Count and Fill ──
blocks += [
    N.h2("Solution 2 — Count and Fill (Two-Pass)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We know the output format: some number of 0s, then some 1s, then some 2s. If we count how many of each exist, we can reconstruct the output directly without any comparisons."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly but requires two passes. If the interviewer specifies 'one pass,' count-and-fill doesn't qualify. Offer it as a simpler starting answer before presenting DNF."),
        N.h4("The Key Observation"),
        N.para("Count frequencies of 0, 1, 2 in one pass. Then overwrite the array in a second pass: write count[0] zeros, count[1] ones, count[2] twos. No comparisons, no swaps — just counting and filling."),
        N.h4("Building the Solution"),
        N.para("Pass 1: iterate over nums and tally each colour. Pass 2: iterate with a write pointer, filling the correct count of each colour in order."),
    ]),
    N.code(
        "def sortColors(nums: list[int]) -> None:\n"
        "    count = [0, 0, 0]\n"
        "    for n in nums:\n"
        "        count[n] += 1          # Pass 1: tally each colour\n"
        "    i = 0\n"
        "    for color in range(3):\n"
        "        for _ in range(count[color]):\n"
        "            nums[i] = color    # Pass 2: overwrite with sorted values\n"
        "            i += 1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = [0, 0, 0]", {"code": True}), (" — Tally array: count[0]=reds, count[1]=whites, count[2]=blues.", {})])),
    N.para(N.rich([("for n in nums: count[n] += 1", {"code": True}), (" — Single pass over input; each element increments its colour bucket.", {})])),
    N.para(N.rich([("for color in range(3):", {"code": True}), (" — Outer loop over colours 0, 1, 2 in sorted order.", {})])),
    N.para(N.rich([("nums[i] = color; i += 1", {"code": True}), (" — Write count[color] copies of the current colour into the array.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Passes"],
        ["Library Sort", "O(n log n)", "O(n)", "N/A"],
        ["Count and Fill", "O(n)", "O(1)", "2"],
        ["Dutch National Flag (optimal)", "O(n)", "O(1)", "1"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting (Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Dutch National Flag (3-Way Partition)", {})])),
    N.callout(
        "When to recognize this pattern: array has exactly 3 distinct values to sort/partition in-place; "
        "'one pass' constraint with O(1) space; need to separate elements into 3 groups by condition. "
        "Also: whenever a quicksort pivot step must handle many equal elements (3-way partition for O(n) on all-duplicate input).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Dutch National Flag / 3-Way Partition):"),
    N.bullet(N.rich([("Move Zeroes", {"bold": True}), (" (Easy) — 2-way DNF: move zeros to end while preserving relative order of non-zeros (#283)", {})])),
    N.bullet(N.rich([("Remove Element", {"bold": True}), (" (Easy) — 2-way partition: remove all occurrences of val in-place, return new length (#27)", {})])),
    N.bullet(N.rich([("Separate Black and White Balls", {"bold": True}), (" (Medium) — Count minimum adjacent swaps to put all 0s left, 1s right (#2149)", {})])),
    N.bullet(N.rich([("Wiggle Sort II", {"bold": True}), (" (Medium) — Extended 3-way partition with alternating interleaved placement (#324)", {})])),
    N.bullet(N.rich([("Partition Array According to Given Pivot", {"bold": True}), (" (Medium) — 3-partition: < pivot, = pivot, > pivot; preserve relative order (#2161)", {})])),
    N.bullet(N.rich([("Sort Array By Parity", {"bold": True}), (" (Easy) — 2-way partition: even numbers before odd (#905)", {})])),
    N.bullet(N.rich([("3-Way Quicksort", {"bold": True}), (" — DNF is the partition step; handles all-equal arrays in O(n) vs O(n^2)", {})])),
    N.para("These problems share the same core technique: maintaining partition boundaries as invariants while a scan pointer processes each element exactly once."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1 (Array Manipulation, Dutch National Flag). Sub-Pattern verified from Guide Section 1.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sort_colors")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─────────────── 4. Append in chunks ───────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion.")
print("NOTION OK", PAGE_ID)
