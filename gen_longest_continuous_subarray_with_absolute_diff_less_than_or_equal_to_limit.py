"""
Notion page builder for:
  #1438 Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
  Pattern: Monotonic Queue | Subpattern: Two Deques for Range
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8184-b38d-f8f04d88cf13"
SLUG    = "longest_continuous_subarray_with_absolute_diff_less_than_or_equal_to_limit"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1438,
    pattern="Monotonic Queue",
    subpatterns=["Two Deques for Range"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use two monotonic deques (one decreasing for max, one increasing for min) to track window range in O(1); shrink left when max − min > limit.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(
        "Given an integer array nums and an integer limit, return the length of the longest "
        "contiguous subarray such that the absolute difference between any two elements in that "
        "subarray is less than or equal to limit. "
        "Equivalently: find the longest window [left, right] where max(window) − min(window) ≤ limit."
    ),
    N.divider(),
]

# ── Solution 1 — Two Monotonic Deques (Interview Pick) ──
SOL1_CODE = """\
from collections import deque

def longestSubarray(nums: list[int], limit: int) -> int:
    max_dq = deque()   # indices, decreasing values; front = window max index
    min_dq = deque()   # indices, increasing values; front = window min index
    left = result = 0
    for right, val in enumerate(nums):
        # Maintain max_dq: pop back while back value <= current
        while max_dq and nums[max_dq[-1]] <= val:
            max_dq.pop()
        max_dq.append(right)
        # Maintain min_dq: pop back while back value >= current
        while min_dq and nums[min_dq[-1]] >= val:
            min_dq.pop()
        min_dq.append(right)
        # Shrink window while invalid
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            if max_dq[0] < left:
                max_dq.popleft()
            if min_dq[0] < left:
                min_dq.popleft()
        result = max(result, right - left + 1)
    return result
"""

blocks += [
    N.h2("Solution 1 — Two Monotonic Deques (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the longest contiguous subarray where max − min ≤ limit. "
            "At every step, we only need two numbers: the current window's maximum and minimum. "
            "If we can track those two values cheaply as the window grows and shrinks, "
            "a sliding window gives us an O(n) algorithm."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive sliding window with plain max/min variables works for expansion — "
            "just take max(cur_max, new_val). But when we shrink from the left, we might "
            "evict the element that was the current max or min. Then we'd need to re-scan "
            "the entire window to find the new max/min: O(n) per shrink → O(n²) total. "
            "Too slow for n up to 100,000."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A monotonic deque (the same data structure used in Sliding Window Maximum, LC #239) "
            "maintains the running maximum of a window in O(1) amortized per step. "
            "When a new element arrives, we pop dominated elements from the back. "
            "When the window shrinks, we pop stale elements from the front. "
            "We need the maximum AND the minimum, so we use two such deques simultaneously."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. max_dq: stores indices in order of decreasing values. Its front is always "
            "the index of the current window's maximum. Before appending right, pop the back "
            "while nums[back] ≤ nums[right] — those indices can never be the max while right is present. "
            "2. min_dq: stores indices in order of increasing values. Front = window min. "
            "Pop back while nums[back] ≥ nums[right]. "
            "3. After updating both deques, check: if nums[max_dq[0]] − nums[min_dq[0]] > limit, "
            "move left right. Evict stale fronts (index < left) from both deques. "
            "4. Once valid, record right − left + 1."
        ),
        N.callout(
            "Analogy: Imagine two 'leaderboards' — one ranking elements from highest to lowest "
            "(max_dq), one from lowest to highest (min_dq). As new elements enter on the right, "
            "they boot out weaker competitors from the back. As elements leave on the left, "
            "the next-best competitor is already at the front. No re-scanning ever needed.",
            "🏆", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("max_dq = deque()", {"code": True}), " — deque of indices with strictly decreasing values; front always = window max index."])),
    N.para(N.rich([("min_dq = deque()", {"code": True}), " — deque of indices with strictly increasing values; front always = window min index."])),
    N.para(N.rich([("left = result = 0", {"code": True}), " — left pointer of sliding window; result tracks the longest valid window seen."])),
    N.para(N.rich([("for right, val in enumerate(nums):", {"code": True}), " — expand window one element at a time by advancing right."])),
    N.para(N.rich([("while max_dq and nums[max_dq[-1]] <= val: max_dq.pop()", {"code": True}), " — back-pop: any index whose value ≤ val is dominated (val ≥ it and arrives later, so it stays longer in window). Discard safely."])),
    N.para(N.rich([("max_dq.append(right)", {"code": True}), " — right is now the newest and potentially best candidate for max."])),
    N.para(N.rich([("while min_dq and nums[min_dq[-1]] >= val: min_dq.pop()", {"code": True}), " — back-pop: any index whose value ≥ val is dominated for the min role. Discard safely."])),
    N.para(N.rich([("min_dq.append(right)", {"code": True}), " — right is now the newest and potentially best candidate for min."])),
    N.para(N.rich([("while nums[max_dq[0]] - nums[min_dq[0]] > limit:", {"code": True}), " — check validity: if window range exceeds limit, must shrink."])),
    N.para(N.rich([("left += 1", {"code": True}), " — shrink window from the left."])),
    N.para(N.rich([("if max_dq[0] < left: max_dq.popleft()", {"code": True}), " — if the current max index is now out of window, evict it; next front becomes new max."])),
    N.para(N.rich([("if min_dq[0] < left: min_dq.popleft()", {"code": True}), " — same for min: evict stale front."])),
    N.para(N.rich([("result = max(result, right - left + 1)", {"code": True}), " — window is valid; update best answer with current window length."])),
    N.divider(),
]

# ── Solution 2 — SortedList ──
SOL2_CODE = """\
from sortedcontainers import SortedList

def longestSubarray(nums: list[int], limit: int) -> int:
    sl = SortedList()   # maintains sorted order dynamically
    left = result = 0
    for right, val in enumerate(nums):
        sl.add(val)                      # O(log n) insert
        while sl[-1] - sl[0] > limit:   # sl[-1] = max, sl[0] = min in O(1)
            sl.remove(nums[left])        # O(log n) remove by value
            left += 1
        result = max(result, right - left + 1)
    return result
"""

blocks += [
    N.h2("Solution 2 — Sorted Container (O(n log n), Simpler Code)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of manually maintaining deques, delegate the ordering problem to a "
            "sorted data structure. A sorted list keeps elements in order at all times, "
            "so the minimum is always at index 0 and the maximum at index −1."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A Python list with manual sorting is O(n log n) per insert — too slow. "
            "Python's built-in sorted() creates a new list on each step — O(n) per call. "
            "We need a structure that inserts and removes in O(log n) while keeping order."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Python's sortedcontainers.SortedList does exactly this: O(log n) insert, "
            "O(log n) remove, O(1) min/max via sl[0] and sl[-1]. "
            "The sliding window logic is identical — just replace deques with this structure."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Add each new element to the SortedList. While sl[-1] − sl[0] > limit, "
            "remove nums[left] from the list and advance left. Update result each step. "
            "The trade-off: simpler code but O(n log n) instead of O(n)."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("sl = SortedList()", {"code": True}), " — a sorted list that maintains order through all insertions and deletions in O(log n)."])),
    N.para(N.rich([("sl.add(val)", {"code": True}), " — insert the new element in its sorted position in O(log n)."])),
    N.para(N.rich([("sl[-1] - sl[0] > limit", {"code": True}), " — O(1) range check: max is always last element, min is always first."])),
    N.para(N.rich([("sl.remove(nums[left])", {"code": True}), " — O(log n) remove by value (not index). This removes one occurrence of nums[left]."])),
    N.divider(),
]

# ── Solution 3 — Brute Force ──
SOL3_CODE = """\
def longestSubarray(nums: list[int], limit: int) -> int:
    n = len(nums)
    result = 0
    for i in range(n):              # try every left boundary
        cur_max = cur_min = nums[i]
        for j in range(i, n):       # extend right as long as valid
            cur_max = max(cur_max, nums[j])
            cur_min = min(cur_min, nums[j])
            if cur_max - cur_min > limit:
                break               # once violated, extending only worsens
            result = max(result, j - i + 1)
    return result
"""

blocks += [
    N.h2("Solution 3 — Brute Force (O(n²), for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible left boundary i, and for each i extend j as far as we can while max − min ≤ limit."),
        N.h4("What Doesn't Work"),
        N.para("O(n²) is too slow for n up to 100,000. This approach is only useful for understanding the problem and verifying correctness of faster solutions."),
        N.h4("The Key Observation"),
        N.para("Once max − min > limit for a fixed i, extending j can only increase max or decrease min, making things worse. So we can break early. This gives a correct but O(n²) solution."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Sorted Container (SortedList)", "O(n log n)", "O(n)"],
        ["Two Monotonic Deques ✓", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Queue (Stack/Queue section of the DSA Patterns Guide)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Deques for Range — use two monotonic deques simultaneously to track both the window maximum (decreasing deque) and window minimum (increasing deque) for O(1) range queries during sliding window expansion/contraction."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Longest subarray where max − min ≤ k'\n"
        "• 'Sliding window with constraint on the range (not just sum)'\n"
        "• 'Need both window maximum AND minimum in O(1) after each expansion/shrink'\n"
        "• Single monotonic deque handles max or min alone; two deques handle both simultaneously.",
        "🔎", "green_background"
    ),
    N.para(
        N.rich([
            ("Note: ", {"bold": True, "italic": True}),
            ("The 'Two Deques for Range' sub-pattern classification is based on analysis. "
             "The guide lists Monotonic Queue generally (e.g., Sliding Window Maximum); "
             "the two-deque variant for range tracking is a natural extension not explicitly "
             "listed as its own row.", {"italic": True})
        ])
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (monotonic deque / monotonic queue):"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Single max deque, fixed window size k (#239)"])),
    N.bullet(N.rich([("Shortest Subarray with Sum at Least K", {"bold": True}), " (Hard) — Monotonic deque on prefix sums for minimum length (#862)"])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — DP window optimization with max deque (#1696)"])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), " (Hard) — DP + monotonic deque for bounded max sum (#1425)"])),
    N.bullet(N.rich([("Max Value of Equation", {"bold": True}), " (Hard) — Monotonic deque on transformed values y + x (#1499)"])),
    N.bullet(N.rich([("Count Subarrays with Fixed Bounds", {"bold": True}), " (Hard) — Track min/max positions in a single linear pass (#2444)"])),
    N.para("These problems all exploit the property that a monotonic deque gives O(1) max or min of a sliding window, with O(n) total work due to each element entering and leaving at most once."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section → Monotonic Queue sub-pattern.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append in chunks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
