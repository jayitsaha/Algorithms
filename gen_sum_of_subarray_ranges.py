"""
gen_sum_of_subarray_ranges.py
Regenerate Notion page for Sum of Subarray Ranges (LC #2104).
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8117-9d49-d731795134ea"

# ── 1) Set properties ─────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2104,
    pattern="Monotonic Stack",
    subpatterns=["Sum of Max - Sum of Min"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Decompose sum of ranges into sum of maxima minus sum of minima; compute each in O(n) via monotonic stack contribution counting.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build new body ─────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the sum of all subarray ranges. The range of a subarray is the difference between the largest and smallest element in the subarray. There are ", {}),
        ("n(n+1)/2", {"code": True}),
        (" subarrays total.", {}),
    ])),
    N.para("Constraints: 1 <= nums.length <= 1000, -10^9 <= nums[i] <= 10^9."),
    N.divider(),
]

# Solution 1 — Brute Force
blocks += [
    N.h2("Solution 1 — Brute Force (Nested Loops)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every pair (i, j) with i ≤ j, we need the max and min of nums[i..j]. Sum all (max − min). The straightforward reading: iterate every subarray."),
        N.h4("What Doesn't Work"),
        N.para("Computing min and max from scratch for each subarray is O(n³). But if we expand j one step at a time, we can maintain rolling min and max — reducing to O(n²) with O(1) space. Still too slow for n = 10⁵ but correct and easy to implement."),
        N.h4("The Key Observation"),
        N.para("When j advances by one, the new max is max(old_max, nums[j]) and new min is min(old_min, nums[j]). No need to re-scan. This gives O(n²) time."),
        N.h4("Building the Solution"),
        N.para("For each i, set lo = hi = nums[i], then iterate j from i to n−1, updating lo and hi, adding (hi − lo) each step."),
        N.callout("Analogy: Scan a row of temperature readings left to right, recording the daily high/low as you go — O(n) per starting point.", "🌡️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""def subArrayRanges(nums: list[int]) -> int:
    n, ans = len(nums), 0
    for i in range(n):
        lo = hi = nums[i]
        for j in range(i, n):
            lo = min(lo, nums[j])
            hi = max(hi, nums[j])
            ans += hi - lo
    return ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("n, ans = len(nums), 0", {"code": True}), (" — initialize length and running answer to 0.", {})])),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — i is the left boundary of the current subarray.", {})])),
    N.para(N.rich([("lo = hi = nums[i]", {"code": True}), (" — single-element subarray: min = max = nums[i].", {})])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), (" — j extends the right boundary step by step.", {})])),
    N.para(N.rich([("lo = min(lo, nums[j])", {"code": True}), (" — update rolling minimum as we grow the subarray.", {})])),
    N.para(N.rich([("hi = max(hi, nums[j])", {"code": True}), (" — update rolling maximum.", {})])),
    N.para(N.rich([("ans += hi - lo", {"code": True}), (" — add this subarray's range (max − min) to total.", {})])),
    N.divider(),
]

# Solution 2 — Monotonic Stack (Optimal)
blocks += [
    N.h2("Solution 2 — Monotonic Stack: Contribution Counting (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of summing (max − min) over every subarray individually, exploit linearity: sum of (max − min) = sum of maxima − sum of minima. Each part can be computed independently."),
        N.h4("What Doesn't Work"),
        N.para("Naively computing max and min for each subarray is O(n²) at best. We need a way to aggregate across all subarrays faster. The key question shifts from 'what is the min of this subarray?' to 'in how many subarrays is element i the minimum?'"),
        N.h4("The Key Observation"),
        N.para("For element nums[i] to be the minimum of a subarray, that subarray cannot contain any element smaller than nums[i]. The valid subarrays are bounded on the left by the previous element strictly smaller than nums[i], and on the right by the next element ≤ nums[i]. Count = left_span × right_span. Contribution = nums[i] × left_span × right_span."),
        N.h4("Building the Solution"),
        N.para("Step 1: Use a monotonic increasing stack to process elements. When popping index m at time i, right boundary = i, left boundary = new stack top. Compute contribution and add to sumMin. Step 2: Repeat with a monotonic decreasing stack for sumMax. Step 3: Return sumMax − sumMin."),
        N.callout("Analogy: Think of each element 'owning' a stretch of subarrays where it is the minimum. The stack efficiently discovers the exact stretch without checking every subarray explicitly.", "🏗️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def subArrayRanges(nums: list[int]) -> int:
    n = len(nums)

    def sum_of_mins() -> int:
        total, stk = 0, []
        for i in range(n + 1):  # n+1 to include sentinel flush
            while stk and (i == n or nums[stk[-1]] >= nums[i]):
                m = stk.pop()
                left  = m - (stk[-1] if stk else -1)
                right = i - m
                total += nums[m] * left * right
            stk.append(i)
        return total

    def sum_of_maxs() -> int:
        total, stk = 0, []
        for i in range(n + 1):
            while stk and (i == n or nums[stk[-1]] <= nums[i]):
                m = stk.pop()
                left  = m - (stk[-1] if stk else -1)
                right = i - m
                total += nums[m] * left * right
            stk.append(i)
        return total

    return sum_of_maxs() - sum_of_mins()"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n + 1):", {"code": True}), (" — the extra iteration (i = n) acts as a sentinel, flushing all remaining stack elements without special-case code.", {})])),
    N.para(N.rich([("while stk and (i == n or nums[stk[-1]] >= nums[i]):", {"code": True}), (" — pop when the stack top value is ≥ current (for min stack). i == n forces a pop for all remaining elements.", {})])),
    N.para(N.rich([("m = stk.pop()", {"code": True}), (" — m is the element being finalized: we now know its exact left and right boundaries.", {})])),
    N.para(N.rich([("left = m - (stk[-1] if stk else -1)", {"code": True}), (" — distance from m to the previous smaller element (or −1 if none). This is the number of valid left endpoints.", {})])),
    N.para(N.rich([("right = i - m", {"code": True}), (" — distance from m to the current element i (the next ≤ element). Number of valid right endpoints.", {})])),
    N.para(N.rich([("total += nums[m] * left * right", {"code": True}), (" — nums[m] is the minimum of exactly left × right subarrays, so add that contribution.", {})])),
    N.para(N.rich([("nums[stk[-1]] <= nums[i]", {"code": True}), (" — for the max stack, pop when top is ≤ current. This makes nums[i] a new maximum boundary, finalizing the popped element as the maximum of its subarrays.", {})])),
    N.para(N.rich([("return sum_of_maxs() - sum_of_mins()", {"code": True}), (" — the final answer by linearity: sum of ranges = sum of all subarray maxima minus sum of all subarray minima.", {})])),
    N.callout(
        "Duplicate tie-breaking: For sum_of_mins, we pop when nums[top] >= nums[i] (pop equal elements). For sum_of_maxs, pop when nums[top] <= nums[i]. This asymmetry ensures each subarray's minimum is claimed by its rightmost equal element, and maximum by its leftmost — no double-counting.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Nested Loop)", "O(n²)", "O(1)"],
        ["Monotonic Stack (Interview Pick)", "O(n)", "O(n)"],
    ]),
    N.para("Each element is pushed and popped from the stack at most once across the entire loop, giving O(n) amortized. Two passes (mins and maxes) = 2 × O(n) = O(n). Stack uses O(n) space in the worst case (strictly increasing or decreasing array)."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Monotonic Stack", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sum of Max − Sum of Min (Contribution Counting) | Monotonic Stack: Next Greater/Smaller", {})])),
    N.callout(
        "When to recognize this pattern: 'sum of something across all subarrays' + 'involves min/max' + O(n²) brute force exists but n is large → contribution counting with monotonic stack. Also: 'find previous/next smaller/greater for each element' is a direct monotonic stack signal.",
        "🔎", "green_background"
    ),
    N.para("Note: The sub-pattern 'Sum of Max − Sum of Min' is derived from analysis combining the Monotonic Stack pattern with the linearity decomposition trick. The parent sub-problem (sum of subarray minimums only) is LeetCode #907."),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (monotonic stack + contribution counting):"),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium, LC #907) — the sumMin() half of this problem; classic starter for this pattern", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy, LC #496) — classic monotonic stack next-greater lookup", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium, LC #739) — find next warmer day using monotonic stack on indices", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard, LC #84) — area contribution per bar using previous/next smaller; same pop logic", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard, LC #42) — water contribution at each column via boundary distances", {})])),
    N.bullet(N.rich([("Maximum Width Ramp", {"bold": True}), (" (Medium, LC #962) — two-pass monotonic stack approach for span distances", {})])),
    N.para("These problems share the core technique: use a monotonic stack to find, for each element, the nearest element that violates the monotonicity, giving boundary spans in O(n) total."),
    N.callout("📚 Sub-Pattern: Monotonic Stack — Contribution Counting. This combines with the 'sum decomposition' trick: ∑(max − min) = ∑max − ∑min. Recognize whenever you see 'sum of subarray extremes' problems.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sum_of_subarray_ranges")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append in chunks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
