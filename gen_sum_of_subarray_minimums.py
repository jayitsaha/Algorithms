"""
gen_sum_of_subarray_minimums.py
Regenerates the Notion page for Sum of Subarray Minimums (LC #907) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-816a-a928-e30cc119f847"
SLUG    = "sum_of_subarray_minimums"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=907,
    pattern="Stack / Queue",
    subpatterns=["Monotonic Stack: Previous Smaller", "Left/Right Boundaries"],
    tc="O(n)",
    sc="O(n)",
    key_insight="For each element, count subarrays where it is the minimum using left/right boundary distances from a monotone stack. Contribution = arr[i] × left[i] × right[i].",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
print("Building new content...")

BRUTE_CODE = """\
def sumSubarrayMins(arr):
    # O(n^2) — too slow for large input, but correct
    MOD, total, n = 10**9 + 7, 0, len(arr)
    for i in range(n):
        cur_min = arr[i]          # track rolling minimum
        for j in range(i, n):    # extend right endpoint
            cur_min = min(cur_min, arr[j])
            total = (total + cur_min) % MOD
    return total"""

OPTIMAL_CODE = """\
def sumSubarrayMins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    left  = [0] * n   # left[i]  = # choices for left endpoint
    right = [0] * n   # right[i] = # choices for right endpoint
    stack = []         # monotone increasing stack of indices

    # LEFT PASS: find previous strictly smaller element
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack = []
    # RIGHT PASS: find next smaller-or-equal element
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    # Contribution of arr[i] = arr[i] * left[i] * right[i]
    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD"""

blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an array of integers ", ("arr", {"code": True}),
        ", find the sum of ", ("min(b)", {"code": True}),
        " for every contiguous subarray ", ("b", {"code": True}),
        " of ", ("arr", {"code": True}),
        ". Return the answer modulo 10⁹ + 7.\n\n"
        "Example: arr = [3, 1, 2, 4] → all 10 subarrays have minimums summing to 17."
    ])),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For every pair of indices (i, j) with i ≤ j, we have a subarray arr[i..j]. We want the sum of min(arr[i..j]) over all such pairs."),
        N.h4("What Doesn't Work (Brute Force Itself)"),
        N.para("Enumerating all O(n²) pairs and scanning each subarray for the minimum is O(n³). The O(n²) improvement tracks a rolling minimum as j extends — still too slow for n=3×10⁴ (9×10⁸ operations)."),
        N.h4("The Key Observation"),
        N.para("Tracking the rolling min as we extend the right endpoint is O(1) per step. This gives us O(n²) — correct for small inputs, but we need O(n)."),
        N.h4("Building the Solution"),
        N.para("Outer loop fixes left endpoint i. Inner loop extends j, maintaining cur_min = min(arr[i..j]) at each step. Add cur_min to total each iteration."),
        N.callout("Propose this first in an interview, then say 'we can do better by flipping the perspective from subarrays to elements.'", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD, total, n = 10**9+7, 0, len(arr)", {"code": True}), " — initialize constants; MOD prevents integer overflow in the final answer."])),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — fix the left endpoint of the subarray."])),
    N.para(N.rich([("cur_min = arr[i]", {"code": True}), " — single-element subarray [arr[i]] has min = arr[i]."])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), " — extend right endpoint from i onward."])),
    N.para(N.rich([("cur_min = min(cur_min, arr[j])", {"code": True}), " — rolling minimum: extending by arr[j] can only decrease or keep the minimum."])),
    N.para(N.rich([("total = (total + cur_min) % MOD", {"code": True}), " — accumulate this subarray's minimum contribution."])),
    N.divider(),
]

# ── Solution 2: Monotonic Stack (Optimal) ──
blocks += [
    N.h2("Solution 2 — Monotonic Stack, Contribution Counting (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'what is the minimum of each subarray?', ask: 'for each element arr[i], how many subarrays have arr[i] as their minimum?' If the answer is k, then arr[i] contributes arr[i] × k to the total."),
        N.h4("What Doesn't Work"),
        N.para("Iterating all subarrays is O(n²) at best. We need a smarter decomposition."),
        N.h4("The Key Observation"),
        N.para("For arr[i] to be the minimum of a subarray [L, R], the subarray must not extend past any element smaller than arr[i]. So the number of valid subarrays containing i as the minimum equals left[i] × right[i], where left[i] = distance to the nearest strictly-smaller element on the left (or start of array), and right[i] = distance to the nearest smaller-or-equal element on the right (or end of array). The asymmetric comparison (strictly < vs ≤) prevents double-counting on duplicate values."),
        N.h4("Building the Solution"),
        N.para("A monotone increasing stack finds 'previous strictly smaller' and 'next smaller-or-equal' boundaries in O(n). Two passes: left-to-right for left[], right-to-left for right[]. Then one O(n) summation."),
        N.callout("Analogy: think of each element as a 'valley floor.' Its contribution is the area of the valley it owns — left_reach × right_reach. The monotone stack efficiently finds each valley's walls.", "🏔️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("left = [0]*n; right = [0]*n", {"code": True}), " — arrays to store boundary distances for each index."])),
    N.para(N.rich([("stack = []", {"code": True}), " — monotone increasing stack storing indices (not values)."])),
    N.para(N.rich([("while stack and arr[stack[-1]] >= arr[i]:", {"code": True}), " — LEFT PASS: pop when stack top is greater-than-or-equal (not strictly smaller than current). Using >= ensures equal elements don't block the left boundary incorrectly."])),
    N.para(N.rich([("left[i] = i - stack[-1] if stack else i + 1", {"code": True}), " — if stack has elements, the top is the previous strictly-smaller index. Distance = i - top. If stack is empty, left boundary is the start: distance = i + 1."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — push current index. Stack remains monotone increasing."])),
    N.para(N.rich([("for i in range(n-1, -1, -1):", {"code": True}), " — RIGHT PASS: scan from right to left."])),
    N.para(N.rich([("while stack and arr[stack[-1]] > arr[i]:", {"code": True}), " — pop only when strictly greater (> not >=). This means equal elements are NOT popped — the leftmost equal element 'owns' equal ties, preventing double-counting."])),
    N.para(N.rich([("right[i] = stack[-1] - i if stack else n - i", {"code": True}), " — distance to next smaller-or-equal element, or to end of array."])),
    N.para(N.rich([("return sum(arr[i]*left[i]*right[i] ...) % MOD", {"code": True}), " — each element contributes arr[i] × (# valid left endpoints) × (# valid right endpoints). Sum all and take modulo."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (rolling min)", "O(n²)", "O(1)"],
        ["Monotonic Stack (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack / Queue → Monotonic Stack"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Monotonic Stack: Previous Smaller + Left/Right Boundaries (Contribution Counting)"])),
    N.callout(
        "When to recognize this pattern: 'sum/count across all subarrays' involving min or max → contribution counting. 'Previous smaller/larger element' or 'next smaller/larger element' for each index → monotone stack. Histogram area, stock span, rain water → all use left/right boundary ideas.",
        "🔎",
        "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Monotonic Stack / Contribution Counting technique:"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Next greater element for each day; standard monotone decreasing stack. LeetCode #739."])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — Find next greater element for subset using stack + hash map. LeetCode #496."])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Same left/right smaller-element boundaries; maximize area instead of summing. LeetCode #84."])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Left/right max boundaries; monotone stack is one of three approaches. LeetCode #42."])),
    N.bullet(N.rich([("Sum of Subarray Ranges", {"bold": True}), " (Medium) — Sum of (max−min) for every subarray; apply contribution counting for both max and min. LeetCode #2104."])),
    N.bullet(N.rich([("Maximum Width Ramp", {"bold": True}), " (Medium) — Left/right boundary scanning with monotone decreasing structure. LeetCode #962."])),
    N.para("These problems share the core technique: use a monotone stack to precompute boundary distances for each element, then aggregate contributions in O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section → Monotonic Stack sub-patterns", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
