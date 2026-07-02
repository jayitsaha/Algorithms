"""gen_maximum_subarray.py — Notion update for Maximum Subarray (LC #53)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8100-a04c-ead73c26b6f6"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=53,
    pattern="Array Manipulation",
    subpatterns=["Classic Kadane"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Negative running sums are dead weight — restart at the next element whenever extending would give a worse result.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} existing blocks.")

# ── 3) Build body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", find the subarray with the largest sum and return its sum. A subarray is a contiguous part of the array. The array contains at least one element.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [−2, 1, −3, 4, −1, 2, 1, −5, 4]", {"code": True}),
        (" → Output: ", {}),
        ("6", {"code": True}),
        (", from subarray [4, −1, 2, 1].", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Kadane's (Interview Pick) ──
KADANE_CODE = """\
def maxSubArray(nums: list[int]) -> int:
    curr_sum = nums[0]    # Best subarray sum ending here; seed with first element
    max_sum  = nums[0]    # Global best; same seed handles all-negative arrays
    for num in nums[1:]:  # Start at index 1 — index 0 is already seeded
        curr_sum = max(num, curr_sum + num)  # Restart here or extend — whichever wins
        max_sum  = max(max_sum, curr_sum)    # Did we just beat the global record?
    return max_sum
"""

blocks += [
    N.h2("Solution 1 — Kadane's Algorithm (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the contiguous slice of the array with the highest sum. We can't cherry-pick elements — no gaps allowed. The question becomes: at every position, should we extend our current window or start fresh?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries every (start, end) pair — O(n²). For n = 10⁵ that's 10¹⁰ operations. We need a smarter way to avoid recomputing overlapping subproblems."),
        N.h4("The Key Observation"),
        N.para("A negative running sum always hurts whatever comes after it. If curr_sum is negative going into the next element, extending would give a smaller result than just taking that element alone. So the local decision is: max(num, curr_sum + num)."),
        N.h4("Building the Solution"),
        N.para("Maintain two variables: curr_sum = best subarray ending exactly here; max_sum = best seen globally. At each position, update curr_sum with the extend-or-restart decision, then update max_sum if curr_sum is a new record. Initialize both to nums[0] (not 0!) for all-negative correctness."),
        N.callout("Analogy: Imagine a salesperson whose running commission balance can go negative. Whenever the balance is negative, it's better to start fresh next month than to carry that deficit forward.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kadane's Algorithm"),
    N.para("Kadane's Algorithm was presented by Joseph Kadane in 1984. It solves the maximum subarray problem in O(n) time, O(1) space — provably optimal for a comparison-based model."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("After processing index i, curr_sum = maximum sum of any subarray ending at exactly index i.", {}),
    ])),
    N.para(N.rich([
        ("Why it works: ", {"bold": True}),
        ("The optimal answer subarray ends at some index r. At every index, the invariant holds by induction (trivially at index 0; at index i, curr_sum = max(nums[i], prev_curr + nums[i]) satisfies the invariant). So when the scan reaches r, curr_sum captures the optimal value.", {}),
    ])),
    N.para(N.rich([
        ("Generalization: ", {"bold": True}),
        ("Kadane's extends naturally to maximum product (track max AND min), circular arrays (combine with total−min), and k-deletion variants (run left and right passes).", {}),
    ])),
    N.para(N.rich([
        ("Recognize when: ", {"bold": True}),
        ("'Maximum/minimum sum of a contiguous subarray' → Kadane's. The key signal is that the local decision at each position depends only on the immediately previous position's optimal value.", {}),
    ])),
    N.h3("Code"),
    N.code(KADANE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("curr_sum = nums[0]", {"code": True}), (" — Initialize the best-ending-here tracker to the first element. Using nums[0] (not 0) ensures all-negative arrays return the largest single element, not 0.", {})])),
    N.para(N.rich([("max_sum = nums[0]", {"code": True}), (" — Initialize the global maximum to the same value. Both start at the same seed.", {})])),
    N.para(N.rich([("for num in nums[1:]:", {"code": True}), (" — Start the loop at index 1; index 0 is already accounted for in the initialization.", {})])),
    N.para(N.rich([("curr_sum = max(num, curr_sum + num)", {"code": True}), (" — The heart of Kadane's: either extend the current subarray (curr_sum + num) or restart here (num alone). If curr_sum was negative, extending gives a worse result, so we restart.", {})])),
    N.para(N.rich([("max_sum = max(max_sum, curr_sum)", {"code": True}), (" — If the current ending-here value beats our global record, update it.", {})])),
    N.para(N.rich([("return max_sum", {"code": True}), (" — After scanning all elements, max_sum holds the answer.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
BRUTE_CODE = """\
def maxSubArray_brute(nums: list[int]) -> int:
    best = nums[0]           # Correct seed: not -inf, not 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best
"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible contiguous subarray by enumerating all start index i and end index j pairs. Compute the sum of each and track the global maximum."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) — too slow for n > 10⁴. Shown here for conceptual clarity and as the starting point before optimizing to Kadane's."),
        N.h4("The Key Observation"),
        N.para("This brute force visits every subarray exactly once. It is correct but wasteful — many sums are recomputed. Kadane's eliminates this redundancy by maintaining a running sum."),
        N.h4("Building the Solution"),
        N.para("Outer loop fixes the start index. Inner loop extends the end index and maintains a running total. No sorting or hashing needed — just nested iteration."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("best = nums[0]", {"code": True}), (" — Seed with the first element, not 0. All-negative arrays need the best single element as the answer, not 0.", {})])),
    N.para(N.rich([("for i in range(len(nums)):", {"code": True}), (" — Outer loop: fix the start index.", {})])),
    N.para(N.rich([("total = 0", {"code": True}), (" — Reset the running sum for each new start.", {})])),
    N.para(N.rich([("for j in range(i, len(nums)):", {"code": True}), (" — Inner loop: extend the end index from i onward.", {})])),
    N.para(N.rich([("total += nums[j]", {"code": True}), (" — Accumulate the sum for subarray [i..j].", {})])),
    N.para(N.rich([("best = max(best, total)", {"code": True}), (" — Track the global maximum across all subarrays.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",           "Time",     "Space",  "Notes"],
        ["Brute Force",        "O(n²)",    "O(1)",   "All start/end pairs; TLE for large n"],
        ["Divide & Conquer",   "O(n log n)","O(log n)","Elegant, not optimal"],
        ["Kadane's (Optimal)", "O(n)",     "O(1)",   "Single scan — interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Classic Kadane (Kadane's Algorithm)", {})])),
    N.callout(
        "When to recognize this pattern: 'maximum/minimum sum of a contiguous subarray'; "
        "local decision at each position depends only on the previous position's optimal value; "
        "extend-or-restart greedy choice applies.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Classic Kadane):"),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), (" (Medium) — Track both max AND min; negatives flip sign (#152)", {})])),
    N.bullet(N.rich([("Maximum Sum Circular Subarray", {"bold": True}), (" (Medium) — Kadane's on original + total-minus-min trick (#918)", {})])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), (" (Medium) — Kadane's with alternating sign condition (#978)", {})])),
    N.bullet(N.rich([("Maximum Subarray Sum with One Deletion", {"bold": True}), (" (Medium) — Forward + backward Kadane to skip one element (#1186)", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock", {"bold": True}), (" (Easy) — Reframe as max subarray of price differences (#121)", {})])),
    N.bullet(N.rich([("Maximum Absolute Sum of Any Subarray", {"bold": True}), (" (Medium) — max(Kadane's, −Kadane's on negated) (#1749)", {})])),
    N.para("These problems share the same core technique: local extend-or-restart decision at each element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 1.6 — Kadane's Algorithm", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_subarray")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
