"""
gen_running_sum_of_1d_array.py
Regenerates the Notion page for LeetCode #1480 — Running Sum of 1d Array
in-place: wipes old content and rewrites properties + body.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81fd-adb1-d37932b9ee0e"

# 1) Set page properties
print("Setting properties …")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1480,
    pattern="Array Manipulation",
    subpatterns=["Basic Prefix Sum"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Carry the running total: result[i] = result[i-1] + nums[i]. One left-to-right pass, safe in-place overwrite.",
    icon="🟢"
)

# 2) Wipe old body
print("Wiping old blocks …")
wiped = N.wipe_page(PAGE_ID)
print(f"  Deleted {wiped} blocks.")

# 3) Build new body
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("nums", {"code": True}),
        (", return a running sum of ", {}),
        ("nums", {"code": True}),
        (". The running sum of an array is defined as: ", {}),
        ("runningSum[i] = sum(nums[0] … nums[i])", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [1, 2, 3, 4]  →  [1, 3, 6, 10]", {"code": True}),
        (". Constraints: ", {}),
        ("1 ≤ nums.length ≤ 1000", {"code": True}),
        (", ", {}),
        ("-10^6 ≤ nums[i] ≤ 10^6", {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ── Solution 1: In-Place Prefix Sum (Interview Pick) ─────────────────────────
SOL1_CODE = """\
def runningSum(nums: list[int]) -> list[int]:
    # Start at index 1 — index 0 is already the correct prefix sum (itself).
    for i in range(1, len(nums)):
        # nums[i-1] now holds the running sum up to i-1 (by invariant).
        # Adding it to nums[i] gives the running sum up to i.
        nums[i] += nums[i - 1]
    return nums"""

blocks += [
    N.h2("Solution 1 — In-Place Prefix Accumulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need an array where each element is the sum of all previous elements plus itself. Think of it like a bank balance: after each transaction, record the new total rather than just the amount."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: for each index i, sum nums[0] through nums[i] from scratch. This repeats work — element 0 is summed n times, element 1 is summed n−1 times, etc. Total: O(n²) additions."),
        N.h4("The Key Observation"),
        N.para("result[i] = result[i−1] + nums[i]. Each running sum is just the previous running sum plus the current element. There is a one-step backward dependency — we only ever need the previous total, not the full sum from scratch."),
        N.h4("Building the Solution"),
        N.para("Process left to right starting at index 1. At each step, nums[i-1] already holds the correct running sum (by induction). Overwrite nums[i] with nums[i] + nums[i-1]. One pass, done. Return nums."),
        N.callout(
            N.rich([
                ("Analogy: ", {"bold": True}),
                ("A bank statement shows the running balance after each transaction. To get balance at day i you don't re-add every transaction — you just take yesterday's balance and add today's amount.", {}),
            ]),
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("for i in range(1, len(nums)):", {"code": True}),
        (" — Start loop at index 1. Index 0 is always correct (single-element prefix sum = itself), so we skip it.", {}),
    ])),
    N.para(N.rich([
        ("nums[i] += nums[i - 1]", {"code": True}),
        (" — Add the running sum at i−1 (which is already stored in nums[i−1] by our invariant) to the original value at nums[i]. This produces the correct prefix sum at i.", {}),
    ])),
    N.para(N.rich([
        ("return nums", {"code": True}),
        (" — The array is now fully converted in-place. Every element holds its prefix sum.", {}),
    ])),
    N.callout(
        N.rich([
            ("Invariant: ", {"bold": True}),
            ("After processing index i, every element nums[j] for j ≤ i holds sum(original_nums[0..j]). This is maintained at every step and guaranteed by the left-to-right traversal order.", {}),
        ]),
        "🔐", "blue_background"
    ),
    N.divider(),
]

# ── Solution 2: Explicit Output Array ─────────────────────────────────────────
SOL2_CODE = """\
def runningSum(nums: list[int]) -> list[int]:
    result = [0] * len(nums)   # Separate output; original nums is preserved
    result[0] = nums[0]        # Base case: prefix sum of first element
    for i in range(1, len(nums)):
        result[i] = result[i-1] + nums[i]  # Carry previous running sum
    return result"""

blocks += [
    N.h2("Solution 2 — Explicit Output Array (Input Preserved)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("When to Choose This"),
        N.para("Same algorithm as Solution 1, but allocates a separate result array. Use when the caller requires the original nums array to remain unchanged (e.g., it will be reused later in the program)."),
        N.h4("Trade-off"),
        N.para("Same O(n) time complexity, but O(n) extra space instead of O(1). In an interview, always present the in-place solution first, then offer this as an alternative if the interviewer says 'do not modify the input.'"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.divider(),
]

# ── Solution 3: One-liner ──────────────────────────────────────────────────────
SOL3_CODE = """\
from itertools import accumulate

def runningSum(nums: list[int]) -> list[int]:
    return list(accumulate(nums))
    # accumulate(nums) generates prefix sums lazily in O(n) time, O(n) space."""

blocks += [
    N.h2("Solution 3 — Python One-liner with itertools.accumulate"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Stdlib Shortcut"),
        N.para("Python's itertools.accumulate does exactly this — it generates a running total across an iterable. Wrapping in list() materialises the lazy generator. Mention as a bonus in interviews after implementing the manual solution."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                "Time",   "Space",  "Notes"],
        ["Brute Force (nested sum)", "O(n²)",  "O(n)",  "Recompute each prefix from scratch"],
        ["Explicit Output Array",   "O(n)",   "O(n)",  "Input preserved; clean separation"],
        ["In-Place Accumulation ✓", "O(n)",   "O(1)*", "Optimal; mutates input array"],
        ["itertools.accumulate",    "O(n)",   "O(n)",  "Pythonic; same as Solution 2"],
    ]),
    N.para(N.rich([
        ("* O(1) extra space. The output reuses the input buffer. If the output array is counted separately, it is O(n).", {"italic": True, "color": "gray"}),
    ])),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Basic Prefix Sum", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("Keywords 'running', 'cumulative', 'sum of all elements up to index i'. Any problem asking you to build or query prefix sums. One-directional left-to-right dependency on the previous result.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Prefix Sum):"),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), (" (Easy) — Build prefix array once; answer sum(l, r) in O(1). #303", {})])),
    N.bullet(N.rich([("Find Pivot Index", {"bold": True}), (" (Easy) — Find index where left prefix sum equals right suffix sum. #724", {})])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sum + hash map to count subarrays summing to k. #560", {})])),
    N.bullet(N.rich([("Product of Array Except Self", {"bold": True}), (" (Medium) — Prefix products and suffix products — same accumulation pattern. #238", {})])),
    N.bullet(N.rich([("Contiguous Array", {"bold": True}), (" (Medium) — Convert 0→−1, use prefix sum to find longest zero-sum subarray. #525", {})])),
    N.bullet(N.rich([("Range Addition", {"bold": True}), (" (Medium) — Difference array: inverse of prefix sum for range updates. #370", {})])),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), (" (Medium) — Kadane's algorithm is a prefix-sum variant. #53", {})])),
    N.bullet(N.rich([("Range Sum Query 2D — Immutable", {"bold": True}), (" (Medium) — 2D prefix sums for O(1) rectangle area queries. #304", {})])),
    N.para("These problems share the core technique: accumulate state left-to-right so that each step depends only on the previous accumulated value."),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("running_sum_of_1d_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# 4) Append all blocks
print(f"Appending {len(blocks)} blocks …")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
