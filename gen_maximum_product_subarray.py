"""
gen_maximum_product_subarray.py
Notion page rebuild for: Maximum Product Subarray (#152)
Page ID: 39193418-809c-8165-8146-c8eaf0bce8d8
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8165-8146-c8eaf0bce8d8"

# ── 1. Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=152,
    pattern="Kadane's Algorithm",
    subpatterns=["Track Max and Min Product"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track both running max and min products; negatives can flip the minimum into the new maximum when multiplied by another negative.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ────────────────────────────────────────────────────
print("Wiping existing blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3. Build the body ────────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "Given an integer array nums, find a contiguous subarray (containing at least one number) "
    "which has the largest product, and return the product.\n\n"
    "Example 1: nums = [2,3,-2,4] → 6 ([2,3] gives the max product)\n"
    "Example 2: nums = [-2,0,-1] → 0 (result cannot be 2, since [-2,-1] is not a subarray that avoids 0)\n\n"
    "Constraints: 1 <= nums.length <= 2×10^4, -10 <= nums[i] <= 10, product guaranteed to fit in a 32-bit integer."
)

SOL1_CODE = """\
def maxProduct(nums: list[int]) -> int:
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num,
                      max_prod * num,
                      min_prod * num)
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    return result"""

SOL2_CODE = """\
def maxProduct(nums: list[int]) -> int:
    # Brute Force O(n^2)
    result = nums[0]
    for i in range(len(nums)):
        prod = 1
        for j in range(i, len(nums)):
            prod *= nums[j]
            result = max(result, prod)
    return result"""

SOL3_CODE = """\
def maxProduct(nums: list[int]) -> int:
    # Prefix Products: scan left-to-right AND right-to-left simultaneously.
    # Zeros reset the running product. Max of both scans is the answer.
    result = nums[0]
    left_prod = right_prod = 1
    n = len(nums)
    for i in range(n):
        left_prod  = nums[i]   * (left_prod  if left_prod  != 0 else 1)
        right_prod = nums[n-1-i] * (right_prod if right_prod != 0 else 1)
        result = max(result, left_prod, right_prod)
    return result"""

blocks = []

# ── Problem statement ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Dual Kadane's ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Dual Kadane's: Track Max & Min Product (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "This is Maximum Subarray (LeetCode #53) but with products instead of sums. "
            "Kadane's algorithm should apply — but products have a crucial difference we must handle."
        ),
        N.h4("What Doesn't Work (Why Plain Kadane's Fails)"),
        N.para(
            "Standard Kadane's restarts the running value when it becomes negative, because a "
            "negative sum always worsens things. But with products, a large negative running product "
            "can flip to a large positive if we encounter another negative element. We cannot safely "
            "discard the running min — it is a future opportunity."
        ),
        N.h4("The Key Observation"),
        N.para(
            "At each index i, the best product of any subarray ending at i is one of exactly three "
            "candidates: (1) the element alone (start fresh), (2) max_prod_prev × element (extend "
            "the running maximum), (3) min_prod_prev × element (flip the running minimum — wins "
            "when element is negative). The same logic applies to the running minimum."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Seed max_prod = min_prod = result = nums[0].\n"
            "2. For each remaining element, compute all three candidates simultaneously "
            "(use a tuple to avoid reading a freshly-updated value).\n"
            "3. max_prod = max(candidates), min_prod = min(candidates).\n"
            "4. result = max(result, max_prod) — track global best across all positions.\n"
            "5. Return result."
        ),
        N.callout(
            "Analogy: Think of a see-saw. max_prod and min_prod sit at opposite ends. "
            "When a negative element arrives, the heavier end instantly becomes the lighter "
            "and vice versa. Tracking both ends means you always know which will be on top "
            "after the next flip.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kadane's Algorithm (Adapted for Products)"),
    N.para(
        "Origin: Joseph Kadane, 1984. Original purpose: find maximum sum subarray in O(n)/O(1).\n\n"
        "Core invariant: After processing index i, max_prod holds the maximum product of any "
        "contiguous non-empty subarray ending exactly at index i.\n\n"
        "Why the standard algorithm needs adaptation: For sums, the running value is monotone "
        "with respect to sign — adding a negative always makes it smaller. For products, "
        "multiplying by a negative reverses the ordering. The maximum can become the minimum "
        "and vice versa in a single step. We therefore maintain BOTH extremes simultaneously.\n\n"
        "Generalization: This dual-tracker pattern applies to any operation where the ordering "
        "can reverse: products (sign flips), XOR (parity flips), etc."
    ),
    N.code(
        "# The three-candidate pattern (core of adapted Kadane's for products):\n"
        "candidates = (num, max_prod * num, min_prod * num)\n"
        "new_max = max(candidates)\n"
        "new_min = min(candidates)\n"
        "# 'num' alone = restart fresh subarray\n"
        "# 'max_prod * num' = extend the running maximum\n"
        "# 'min_prod * num' = potentially flip the minimum to a new maximum"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("max_prod = min_prod = result = nums[0]", {"code": True}),
                   " — Seed all three variables with the first element. Chained assignment sets them all to the same value. This also covers the single-element case."])),
    N.para(N.rich([("for num in nums[1:]:", {"code": True}),
                   " — Iterate from the second element onward. We already handled index 0 with the initialization."])),
    N.para(N.rich([("candidates = (num, max_prod * num, min_prod * num)", {"code": True}),
                   " — Compute all three candidate products using OLD values of both max_prod and min_prod. The tuple ensures both old values are read before either is overwritten."])),
    N.para(N.rich([("max_prod = max(candidates)", {"code": True}),
                   " — Best product of any contiguous subarray ending at the current index."])),
    N.para(N.rich([("min_prod = min(candidates)", {"code": True}),
                   " — Worst (most negative) product ending here. Stored because it may flip to the new maximum on the next negative element."])),
    N.para(N.rich([("result = max(result, max_prod)", {"code": True}),
                   " — Update the global best. The final answer might come from any position, not just the last."])),
    N.para(N.rich([("return result", {"code": True}),
                   " — The maximum product over all possible contiguous subarrays."])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Try All Subarrays"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible contiguous subarray, compute its product, and track the maximum. Guaranteed correct; guaranteed slow."),
        N.h4("What Doesn't Work"),
        N.para("O(n²) time — 400 million operations for n=20,000. Will time out on LeetCode test cases."),
        N.h4("The Key Observation"),
        N.para("Use this approach to build intuition and verify your optimal solution on small inputs. Mention it as your 'naive' solution before optimizing in an interview."),
        N.h4("Building the Solution"),
        N.para("Outer loop fixes start index i. Inner loop extends from i to every possible end j, multiplying each new element in. Track the running product and compare to result."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = nums[0]", {"code": True}),
                   " — Start with the first element as the default best (a single-element subarray is always valid)."])),
    N.para(N.rich([("for i in range(len(nums)):", {"code": True}),
                   " — Try every possible start index i."])),
    N.para(N.rich([("prod = 1", {"code": True}),
                   " — Reset the running product for each new start position."])),
    N.para(N.rich([("for j in range(i, len(nums)):", {"code": True}),
                   " — Extend the subarray from start i to every possible end j."])),
    N.para(N.rich([("prod *= nums[j]", {"code": True}),
                   " — Extend subarray by one element; equivalent to computing product of nums[i..j]."])),
    N.para(N.rich([("result = max(result, prod)", {"code": True}),
                   " — Update global best with the current subarray's product."])),
    N.divider(),
]

# ── Solution 3: Prefix Products ───────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Prefix Products: Left and Right Scans"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The maximum product subarray either ends at some position from the left "
            "or ends at some position from the right. If we scan both directions and track "
            "running products, the global maximum must appear in one of the two scans."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A running left-to-right product 'accumulates' all elements from the start. "
            "A zero resets it. A running right-to-left product does the same from the end. "
            "Together, they cover every possible subarray's product because the maximum-product "
            "subarray either starts near the left or is better approached from the right "
            "(especially with an odd number of negatives)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Run left_prod and right_prod in parallel (or two separate passes). "
            "Reset to 1 when the running product becomes 0. "
            "Track the maximum of both running products across all positions."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("left_prod  = nums[i]   * (left_prod  if left_prod  != 0 else 1)", {"code": True}),
                   " — Extend left-to-right running product. Reset to 1 (neutral element for multiplication) when it reaches 0."])),
    N.para(N.rich([("right_prod = nums[n-1-i] * (right_prod if right_prod != 0 else 1)", {"code": True}),
                   " — Same for right-to-left. Index n-1-i processes from the end."])),
    N.para(N.rich([("result = max(result, left_prod, right_prod)", {"code": True}),
                   " — The global best is updated from either scan direction at each step."])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Dual Kadane's (Optimal)", "O(n)", "O(1)"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Prefix Products", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Kadane's Algorithm (Array — subarray optimization)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Max and Min Product (Dual Kadane's variant)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'subarray' + 'maximum' or 'minimum' + 'product'\n"
        "• Input contains both positive and negative integers\n"
        "• O(n)/O(1) is required\n"
        "• The operation (product) can reverse ordering on sign change\n"
        "• 'Find contiguous subarray with largest X' for any X that can be negative",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
rel1 = " (Medium, #53) — classic Kadane approach with sums; no min tracking needed since sums do not flip on sign change"
rel2 = " (Medium, #238) — prefix and suffix product arrays; same decomposition thinking, no division allowed"
rel3 = " (Easy, #628) — sort and compare two candidates; same insight that two negatives improve the product"
rel4 = " (Medium, #713) — sliding window with product tracking; shrink when product exceeds threshold"
rel5 = " (Medium) — exact same dual tracker, but return min_prod instead of max_prod"
rel6 = " (Hard, #1856) — monotonic stack to find subarray minimum times sum; harder variant"
rel7 = " (Medium, #713 variant) — two-pointer window expands/contracts on product constraint"
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (dual tracking for sign-reversible operations):"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), rel1])),
    N.bullet(N.rich([("Product of Array Except Self", {"bold": True}), rel2])),
    N.bullet(N.rich([("Maximum Product of Three Numbers", {"bold": True}), rel3])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), rel4])),
    N.bullet(N.rich([("Minimum Product Subarray", {"bold": True}), rel5])),
    N.bullet(N.rich([("Maximum Subarray Min-Product", {"bold": True}), rel6])),
    N.bullet(N.rich([("Count Subarrays with Product Less Than K", {"bold": True}), rel7])),
    N.para("These problems share the same core technique: maintaining running extremes to handle sign changes in multiplication."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.6 Kadane Algorithm", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_product_subarray")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
