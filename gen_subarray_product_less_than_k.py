"""
gen_subarray_product_less_than_k.py
Regenerate Notion page for LeetCode #713 — Subarray Product Less Than K
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8125-bbf9-d5d7acf80a36"
SLUG = "subarray_product_less_than_k"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=713,
    pattern="Sliding Window",
    subpatterns=["Product Window + Count"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Maintain a window whose running product < k; each valid right adds right-left+1 new subarrays.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Build body blocks ───────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of positive integers "),
        ("nums", {"code": True}),
        (" and a positive integer "),
        ("k", {"code": True}),
        (", return the number of contiguous subarrays where the product of all elements is strictly less than "),
        ("k", {"code": True}),
        (". All values in "),
        ("nums", {"code": True}),
        (" are positive integers.")
    ])),
    N.divider()
]

# ── Solution 1 — Sliding Window (Interview Pick) ──
solution1_code = """\
def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0           # No positive-integer product is < 1; prevents infinite loop
    product = 1            # Running product of current window
    left = 0               # Left boundary of sliding window
    count = 0              # Accumulates answer
    for right in range(len(nums)):
        product *= nums[right]          # Expand window to include nums[right]
        while product >= k:             # Window is invalid — shrink from left
            product //= nums[left]      # Remove leftmost element (// avoids float drift)
            left += 1                   # Advance left boundary
        count += right - left + 1      # All subarrays ending at right within valid window
    return count
"""

blocks += [
    N.h2("Solution 1 — Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count every contiguous slice [i..j] of nums where nums[i] × nums[i+1] × … × nums[j] < k. There are O(n²) such slices in total — but we need to count them faster than checking each one."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach tries all O(n²) pairs (i, j), computes the product for each, and counts valid ones. With the early-exit optimization (break when product ≥ k, since products only grow), this is correct but still O(n²) — too slow for n = 30,000."),
        N.h4("The Key Observation"),
        N.para("Because all elements are POSITIVE, the product of a window only grows as the window expands and only shrinks as the window contracts. This monotonicity means: if [left..right] is invalid (product ≥ k), then [left..right+1] is certainly invalid too — but [left+1..right] might be valid. We never need to check both (left, right) AND (left-1, right) separately."),
        N.h4("Building the Solution"),
        N.para("Fix a right endpoint. Maintain the largest window [left..right] with product < k. As right advances, update the product. If invalid, advance left until valid. After fixing the window, count += right - left + 1 — these are all the valid subarrays ending at right (starting anywhere from left to right). Each has a sub-product ≤ the window product < k, so they're all valid without checking individually."),
        N.callout("Analogy: Think of the window as a hose nozzle. You're squeezing content past a pressure limit. When pressure (product) exceeds the limit (k), you release from the back (left) until pressure drops. At every position, you count how many lengths of hose are currently under the limit.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if k <= 1: return 0", {"code": True}), " — Guard: every element is a positive integer (≥1), so any product of one or more elements is ≥1. If k≤1, no product can be strictly less than k. Also prevents an infinite while loop where left would advance forever past right."])),
    N.para(N.rich([("product = 1", {"code": True}), " — Initialize the running product of the current window. Starting at 1 is the multiplicative identity, so the window is empty."])),
    N.para(N.rich([("left = 0", {"code": True}), " — Left boundary of the sliding window. Starts at the beginning of the array."])),
    N.para(N.rich([("count = 0", {"code": True}), " — Accumulates the total number of valid subarrays."])),
    N.para(N.rich([("for right in range(len(nums)):", {"code": True}), " — Move the right pointer forward through every element, expanding the window one step at a time."])),
    N.para(N.rich([("product *= nums[right]", {"code": True}), " — Include nums[right] in the window. The product now represents [left..right]."])),
    N.para(N.rich([("while product >= k:", {"code": True}), " — The window product is too large. We must shrink. Note: we use while, not if, because one shrink step might not be enough (e.g., if a single large element was just included)."])),
    N.para(N.rich([("product //= nums[left]", {"code": True}), " — Remove the leftmost element. Using integer floor division (//) instead of float division (/) prevents floating-point drift from accumulating errors over many multiply/divide cycles."])),
    N.para(N.rich([("left += 1", {"code": True}), " — The left boundary advances past the removed element."])),
    N.para(N.rich([("count += right - left + 1", {"code": True}), " — After the while loop, [left..right] is the longest valid window ending at right. Every subarray ending at right with start ≥ left is also valid (sub-products are smaller). There are right-left+1 such subarrays: [right..right], [right-1..right], …, [left..right]."])),
    N.divider()
]

# ── Solution 2 — Brute Force ──
solution2_code = """\
def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
    count = 0
    n = len(nums)
    for i in range(n):              # Try every starting index
        product = 1
        for j in range(i, n):      # Extend subarray to the right
            product *= nums[j]
            if product >= k:        # Products only grow — safe early exit
                break
            count += 1             # nums[i..j] qualifies
    return count
"""

blocks += [
    N.h2("Solution 2 — Brute Force (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct approach: enumerate every possible (start, end) pair, compute the product, check if it's valid."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) — acceptable for small n (say, ≤1000) but too slow for n = 30,000. It's the right starting point to mention before optimizing."),
        N.h4("The Key Observation"),
        N.para("Once a subarray [i..j] has product ≥ k, any extension [i..j+1] will also have product ≥ k (since nums[j+1] ≥ 1). So we can break the inner loop early — this optimization makes the brute force run in O(n × average_valid_length) rather than strict O(n²) in practice."),
        N.h4("Building the Solution"),
        N.para("Fix i. Extend j rightward, accumulating product. Break as soon as product ≥ k. Each valid (i,j) pair increments the count by 1.")
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — The outer loop fixes the left end of each candidate subarray."])),
    N.para(N.rich([("product = 1", {"code": True}), " — Reset product for each new starting index."])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), " — Inner loop extends the right end of the subarray."])),
    N.para(N.rich([("product *= nums[j]", {"code": True}), " — Include nums[j] in the running product."])),
    N.para(N.rich([("if product >= k: break", {"code": True}), " — Early exit: once product exceeds the threshold, further extension only makes it larger. This avoids checking invalid subarrays."])),
    N.para(N.rich([("count += 1", {"code": True}), " — This specific subarray [i..j] is valid."])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Sliding Window (optimal)", "O(n)", "O(1)"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window (Section 1.5 — Dynamic Size)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Product Window + Count — maintain running product in variable window; count subarrays ending at each right as window size"])),
    N.callout(
        "When to recognize this pattern: 'count contiguous subarrays where product/sum satisfies a bound' + all values positive (ensures monotonicity) + O(n) required. The shrink condition is while aggregate >= threshold, and the counting formula is right - left + 1 after each expansion.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique (Section 1.5 — Sliding Window, Dynamic Size):"),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), " (Medium) — Shrink when sum ≥ target; identical expand/shrink structure, sum instead of product (#209)"])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — Shrink on duplicate character; classic variable window with hash set (#3)"])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), " (Medium) — Count zeros ≤ K in window; same shrink-when-invalid template (#1004)"])),
    N.bullet(N.rich([("Count Number of Nice Subarrays", {"bold": True}), " (Medium) — AtMost(k) − AtMost(k−1) to count exact-k subarrays; the right - left + 1 counting formula appears again (#1248)"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — At most 2 distinct types in window; hash map tracks frequencies (#904)"])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), " (Medium) — Related product problem but Kadane variant — values can be negative, so track both max AND min (#152)"])),
    N.bullet(N.rich([("Subarrays with K Different Integers", {"bold": True}), " (Hard) — AtMost(K) − AtMost(K−1); two simultaneous sliding windows to count exact matches (#992)"])),
    N.para("These problems share the core idea: maintain a window with a valid aggregate, count sub-windows efficiently using the window's length formula."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.5 (Sliding Window — Dynamic Size) · Sub-Pattern: Product Window + Count", "📚", "gray_background"),
    N.divider()
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
