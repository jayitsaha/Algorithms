"""
gen_maximum_absolute_sum_of_any_subarray.py
Creates / rebuilds the Notion page for LeetCode #1749 Maximum Absolute Sum of Any Subarray.
notion_page_id was null => create a fresh page first.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create page (notion_page_id was null) ──
PAGE_ID = N.create_page("Maximum Absolute Sum of Any Subarray", 1749, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1749,
    pattern="Array Manipulation",
    subpatterns=["Kadane's Algorithm"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Max |subarray sum| = max(max_subarray_sum, |min_subarray_sum|); run Kadane's twice in one pass.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body (fresh page has none, but safe to call) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Step 3: Build body ──
PROBLEM_STATEMENT = (
    "You are given an integer array nums. Return the maximum absolute sum of any "
    "(possibly empty) subarray of nums. A subarray is a contiguous part of the array. "
    "The absolute sum of a subarray is the absolute value of its total. "
    "Example: nums = [1,-3,2,3,-4] → answer is 5 (subarray [2,3]). "
    "Example: nums = [2,-5,1,-4,3,-2] → answer is 8 (subarray [2,-5,1,-4], sum = -8)."
)

SOL1_CODE = """\
def maxAbsoluteSum(nums: list[int]) -> int:
    max_sum = min_sum = 0       # Global bests; 0 = empty subarray baseline
    curr_max = curr_min = 0     # Running Kadane accumulators
    for num in nums:
        curr_max = max(num, curr_max + num)   # Extend or restart positive
        max_sum  = max(max_sum, curr_max)     # Update global maximum
        curr_min = min(num, curr_min + num)   # Extend or restart negative
        min_sum  = min(min_sum, curr_min)     # Update global minimum
    return max(max_sum, abs(min_sum))         # Larger magnitude wins\
"""

SOL1_LBL = [
    ("max_sum = min_sum = 0", "Global best max and min subarray sums, initialised to 0 (empty subarray)."),
    ("curr_max = curr_min = 0", "Running Kadane accumulators — what's the best/worst we can do ending here."),
    ("for num in nums:", "Single O(n) scan; both Kadane passes run simultaneously."),
    ("curr_max = max(num, curr_max + num)", "Extend the positive run or restart fresh at num — whichever is larger."),
    ("max_sum  = max(max_sum, curr_max)", "Update the global maximum with today's best ending here."),
    ("curr_min = min(num, curr_min + num)", "Extend the negative run or restart fresh — whichever is more negative."),
    ("min_sum  = min(min_sum, curr_min)", "Update the global minimum (most negative subarray sum)."),
    ("return max(max_sum, abs(min_sum))", "The answer is whichever magnitude is larger."),
]

SOL2_CODE = """\
def maxAbsoluteSum(nums: list[int]) -> int:
    prefix = max_p = min_p = 0
    for num in nums:
        prefix += num
        max_p = max(max_p, prefix)
        min_p = min(min_p, prefix)
    return max_p - min_p\
"""

SOL3_CODE = """\
def maxAbsoluteSum(nums: list[int]) -> int:
    result = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            result = max(result, abs(total))
    return result\
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# Solution 1 — Dual Kadane (Interview Pick)
blocks += [
    N.h2("Solution 1 — Dual Kadane's (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the subarray with the largest absolute total. Absolute value means we care about "
            "magnitude, not sign. So the winner is either the subarray with the biggest positive sum "
            "or the subarray with the most negative sum — whichever has greater magnitude."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force tries all O(n²) subarrays — correct but too slow. Taking abs(max_sum) from "
            "a single Kadane pass is WRONG: a deeply negative subarray can have larger magnitude "
            "than any positive subarray."
        ),
        N.h4("The Key Observation"),
        N.para(
            "max |subarray sum| = max(max_subarray_sum, |min_subarray_sum|). This converts the "
            "problem into two independent instances of Kadane's algorithm: one tracking running "
            "maximum, one tracking running minimum."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Kadane's recurrence: max_ending_here[i] = max(nums[i], max_ending_here[i-1] + nums[i]). "
            "If the previous running sum drags us below nums[i], restart. Run the same logic with "
            "min instead of max. Both passes fit in one loop with four updates per element."
        ),
        N.callout(
            "Analogy: Two bank accounts — one tracks your highest balance ever, one tracks your "
            "lowest overdraft ever. At the end, whichever extreme is further from zero is your answer.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kadane's Algorithm"),
    N.para(
        "Kadane's Algorithm (1984): finds the maximum-sum contiguous subarray in O(n) time, O(1) space. "
        "Core invariant: at index i, curr holds the maximum (or minimum) sum of any subarray ENDING AT i. "
        "Decision: is it better to extend the previous subarray (curr + num) or start fresh (num alone)? "
        "If the running sum is negative (for max Kadane) or positive (for min Kadane), restart. "
        "Generalization: run twice to handle absolute value; adapt to circular arrays via total-minus-min."
    ),
    N.code(
        "# Kadane's template (max variant)\ncurr = 0\nbest = 0  # or float('-inf') if empty not allowed\nfor num in nums:\n    curr = max(num, curr + num)\n    best = max(best, curr)\nreturn best",
        "python"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
]

for line, explanation in SOL1_LBL:
    blocks.append(N.para(N.rich([
        (line, {"code": True}),
        (" — " + explanation, {})
    ])))

blocks.append(N.divider())

# Solution 2 — Prefix Sum Spread
blocks += [
    N.h2("Solution 2 — Prefix Sum Spread (Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Any subarray sum = prefix[j] - prefix[i-1]. To maximise |prefix[j] - prefix[i-1]|, "
            "we want the maximum possible difference between any two prefix values."
        ),
        N.h4("The Key Observation"),
        N.para(
            "max |subarray sum| = max(prefix_sums) - min(prefix_sums). This is the largest possible "
            "spread between any two prefix values. Including prefix[0] = 0 handles the empty subarray."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Track the running prefix sum and its extremes in a single pass. No need to store the "
            "full prefix array — just the current value and the extremes seen so far."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.para(
        N.rich([
            ("Why this works: ", {"bold": True}),
            ("prefix[j] - prefix[i] is any subarray sum for i <= j. Including prefix = 0 at the start means "
             "max_p - min_p = max_p - 0 or 0 - min_p or the full spread — all cases covered. Same O(n) time, O(1) space.", {})
        ])
    ),
    N.divider(),
]

# Solution 3 — Brute Force
blocks += [
    N.h2("Solution 3 — Brute Force O(n²)"),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.para("Correct but O(n²) time. Use this to verify solutions during testing, not for submission."),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Dual Kadane's (Interview Pick)", "O(n)", "O(1)"],
        ["Running Prefix Spread", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Kadane's Algorithm — Max of (Max Sum, |Min Sum|)", {})])),
    N.callout(
        "When to recognize this pattern: 'subarray' + 'sum' + 'maximum/minimum' → Kadane's. "
        "'Absolute value' variant → run max AND min Kadane simultaneously. "
        "'Circular' → Kadane + (total - min subarray). "
        "Decision at each step: extend current window or start fresh?",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Kadane's Algorithm technique:"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), (" (Medium) — Classic Kadane, max positive sum only (#53)", {})])),
    N.bullet(N.rich([("Maximum Sum Circular Subarray", {"bold": True}), (" (Medium) — Kadane + circular wrap: max(linear max, total - min subarray) (#918)", {})])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), (" (Medium) — Track both max and min product per step; negatives flip sign (#152)", {})])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sum + hash map; prefix sum intuition shared (#560)", {})])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), (" (Medium) — Kadane variant: extend only when sign alternates (#978)", {})])),
    N.bullet(N.rich([("Maximum Subarray Sum With One Deletion", {"bold": True}), (" (Medium) — Kadane extended with optional deletion DP (#1186)", {})])),
    N.para("These problems all share the core Kadane invariant: the best subarray ending at i depends only on the best ending at i−1."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.6 — Kadane's Algorithm", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_absolute_sum_of_any_subarray")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT maximum_absolute_sum_of_any_subarray | html=OK | notion=OK | page_id={PAGE_ID}")
