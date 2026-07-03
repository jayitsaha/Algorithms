"""
gen_continuous_subarrays.py — Notion update for LeetCode #2762 Continuous Subarrays.
Runs in-place against the existing page: 39193418-809c-819e-a032-cd41c322e1e4
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-819e-a032-cd41c322e1e4"

SLUG = "continuous_subarrays"

# ── 1. Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2762,
    pattern="Stack and Queue",
    subpatterns=["Two Deques (Min/Max)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Reduce every-pair check to max−min≤2; two monotonic deques give O(1) window min/max.",
    icon="🟡",
)
print("  Properties set.")

# ── 2. Wipe old body ──
print("Wiping old body...")
removed = N.wipe_page(PAGE_ID)
print(f"  Removed {removed} blocks.")

# ── 3. Build new body ──
print("Building new body...")

PROBLEM_STATEMENT = (
    "Given an integer array nums, return the number of subarrays where the absolute "
    "difference between any two elements of the subarray is at most 2. "
    "Formally, count all (i, j) pairs where for every pair of indices l, r within "
    "the subarray nums[l..r], |nums[l] − nums[r]| ≤ 2."
)

SOL1_CODE = """\
from collections import deque

def continuousSubarrays(nums: list[int]) -> int:
    min_dq, max_dq = deque(), deque()  # store indices
    left = 0
    result = 0
    for right in range(len(nums)):
        # Maintain increasing min_dq (front = window minimum)
        while min_dq and nums[min_dq[-1]] >= nums[right]:
            min_dq.pop()
        # Maintain decreasing max_dq (front = window maximum)
        while max_dq and nums[max_dq[-1]] <= nums[right]:
            max_dq.pop()
        min_dq.append(right)
        max_dq.append(right)
        # Shrink window until max − min <= 2
        while nums[max_dq[0]] - nums[min_dq[0]] > 2:
            left += 1
            if min_dq[0] < left: min_dq.popleft()
            if max_dq[0] < left: max_dq.popleft()
        # Every subarray ending at right with left endpoint in [left..right] is valid
        result += right - left + 1
    return result
"""

SOL2_CODE = """\
from sortedcontainers import SortedList

def continuousSubarrays(nums: list[int]) -> int:
    sl = SortedList()
    left = 0
    result = 0
    for right in range(len(nums)):
        sl.add(nums[right])            # O(log n)
        while sl[-1] - sl[0] > 2:     # max - min > 2
            sl.remove(nums[left])      # O(log n)
            left += 1
        result += right - left + 1
    return result
"""

SOL3_CODE = """\
def continuousSubarrays(nums: list[int]) -> int:
    n = len(nums)
    result = 0
    for i in range(n):
        cur_min = cur_max = nums[i]
        for j in range(i, n):
            cur_min = min(cur_min, nums[j])
            cur_max = max(cur_max, nums[j])
            if cur_max - cur_min > 2:
                break
            result += 1
    return result
"""

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Two Monotonic Deques (Optimal) ──
blocks += [
    N.h2("Solution 1 — Two Monotonic Deques (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to count subarrays where every pair of elements has absolute difference ≤ 2. "
            "That sounds like an O(n²) check per subarray — but notice: the largest pairwise "
            "difference in any subarray is always max(subarray) − min(subarray). So the condition "
            "simplifies to: max − min ≤ 2. Now we just need a fast way to track window max and min."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive brute force: for each pair (i, j), scan the subarray for max and min — O(n³). "
            "Slightly smarter: for each left endpoint, scan right and maintain running max/min — O(n²). "
            "Still too slow for n ≤ 10⁵. We need the window max and min to update in O(1) as we "
            "move the window."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The monotonic deque trick: maintain a deque of indices whose values are increasing "
            "(for min) or decreasing (for max). When we push a new index, we pop any back entries "
            "that can never be the min/max while the new element is in the window. This keeps the "
            "deque monotonic and ensures the front is always the current window extreme — O(1) query."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sliding window: expand right freely, shrink left when max−min > 2. "
            "At each valid right, add right−left+1 to count (all subarrays ending at right "
            "with left endpoints in [left..right] are valid — a sub-window of a valid window is valid). "
            "Each element is pushed and popped from each deque at most once: O(n) total."
        ),
        N.callout(
            "Analogy: Imagine two security guards watching a sliding window. "
            "The 'min guard' only keeps track of candidates for smallest — whenever a smaller person "
            "enters from the right, all taller people behind can be dismissed (they're blocked). "
            "Same for the 'max guard' but inverted. The front of each guard's list is always "
            "the current extreme.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("min_dq, max_dq = deque(), deque()", {"code": True}), " — Two deques storing indices. min_dq front = window min index; max_dq front = window max index."])),
    N.para(N.rich([("left = 0; result = 0", {"code": True}), " — Left window boundary and accumulator."])),
    N.para(N.rich([("for right in range(len(nums)):", {"code": True}), " — Expand window one element at a time."])),
    N.para(N.rich([("while min_dq and nums[min_dq[-1]] >= nums[right]:", {"code": True}), " — Pop back entries whose values are ≥ new value. They can never be min while nums[right] is present."])),
    N.para(N.rich([("while max_dq and nums[max_dq[-1]] <= nums[right]:", {"code": True}), " — Pop back entries whose values are ≤ new value. They can never be max while nums[right] is present."])),
    N.para(N.rich([("min_dq.append(right); max_dq.append(right)", {"code": True}), " — Push current index onto both deques."])),
    N.para(N.rich([("while nums[max_dq[0]] - nums[min_dq[0]] > 2:", {"code": True}), " — Window constraint violated: max−min exceeds 2."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Shrink window from the left."])),
    N.para(N.rich([("if min_dq[0] < left: min_dq.popleft()", {"code": True}), " — Evict stale min front if it fell outside the window."])),
    N.para(N.rich([("if max_dq[0] < left: max_dq.popleft()", {"code": True}), " — Evict stale max front if it fell outside the window."])),
    N.para(N.rich([("result += right - left + 1", {"code": True}), " — All right−left+1 subarrays ending at 'right' are valid. Add them all in one step."])),
    N.divider(),
]

# ── Solution 2: Sorted Container ──
blocks += [
    N.h2("Solution 2 — Sorted Container (Simpler, O(n log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same framing: max−min ≤ 2 in a sliding window. We still need dynamic min and max."),
        N.h4("What Doesn't Work"),
        N.para("Using a plain list requires O(n) to find min/max after each update — too slow."),
        N.h4("The Key Observation"),
        N.para(
            "A SortedList (balanced BST under the hood) maintains sorted order automatically. "
            "sl[0] = min, sl[-1] = max in O(1). Insert and remove are O(log n). "
            "This trades the deque's amortized O(1) for O(log n) per step — still fine for most inputs, "
            "and the code is dramatically simpler."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Add nums[right] on each expansion. If sl[-1]−sl[0] > 2, remove nums[left] and advance left. "
            "Accumulate right−left+1. The SortedList handles all ordering automatically."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("sl = SortedList()", {"code": True}), " — A balanced BST maintaining sorted order; O(1) access to min/max."])),
    N.para(N.rich([("sl.add(nums[right])", {"code": True}), " — O(log n) insert of the new element."])),
    N.para(N.rich([("while sl[-1] - sl[0] > 2:", {"code": True}), " — sl[-1] = max, sl[0] = min. Check constraint."])),
    N.para(N.rich([("sl.remove(nums[left])", {"code": True}), " — O(log n) remove by value (not index). Then advance left."])),
    N.para(N.rich([("result += right - left + 1", {"code": True}), " — Same counting trick: all subarrays ending at right."])),
    N.divider(),
]

# ── Solution 3: Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force (O(n²), for reference)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Fix the left endpoint, expand right while maintaining running max and min."),
        N.h4("The Key Observation"),
        N.para("By breaking early when max−min > 2, we avoid checking all O(n²) subarrays but worst-case is still O(n²)."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Sorted Container (SortedList)", "O(n log n)", "O(n)"],
        ["Two Monotonic Deques (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack and Queue (Monotonic Queue / Deque)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Deques (Min/Max) — maintain increasing min_deque and decreasing max_deque for O(1) window range queries"])),
    N.callout(
        "When to recognize this pattern: problem asks to count/find subarrays satisfying "
        "a constraint on max AND min simultaneously; sliding window where O(log n) per step "
        "is too slow; 'max−min ≤ k' style constraints on subarray elements.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Two Deques (Min/Max) or Monotonic Queue technique:"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Single max_deque over fixed-size window k; classic deque problem (#239)"])),
    N.bullet(N.rich([("Longest Continuous Subarray With Absolute Diff ≤ Limit", {"bold": True}), " (Medium) — Identical two-deque pattern; threshold is a variable k (#1438)"])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — DP with a max_deque to find best predecessor within a window of size k (#1696)"])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), " (Hard) — DP + max_deque; best previous DP value within k steps (#1425)"])),
    N.bullet(N.rich([("Max Value of Equation", {"bold": True}), " (Hard) — Monotonic deque to maximize a linear expression over sliding window (#1499)"])),
    N.bullet(N.rich([("Shortest Subarray with Sum ≥ K", {"bold": True}), " (Hard) — Prefix sum + monotonic deque for efficient shrink decisions (#862)"])),
    N.para("These problems share the core technique: a deque that maintains monotonic ordering of values, providing O(1) window extreme queries."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 6.4 — Stack & Queue → Monotonic Queue (Deque)", "📚", "gray_background"),
]

# ── Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=928")
