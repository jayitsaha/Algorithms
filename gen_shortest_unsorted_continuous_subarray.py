import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8112-975b-e8eb86073482"
SLUG = "shortest_unsorted_continuous_subarray"

print("Step 1: Set properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=581,
    pattern="Monotonic Stack",
    subpatterns=["Find Left/Right Boundaries"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Forward scan finds rightmost element smaller than a preceding max; backward scan finds leftmost element larger than a following min.",
    icon="🟡"
)
print("  Properties set OK")

print("Step 2: Wipe existing blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks")

print("Step 3: Build and append body blocks...")

PROBLEM_STATEMENT = (
    "Given an integer array nums, find the shortest subarray that, if sorted, "
    "makes the entire array sorted in ascending order. Return the length of this "
    "shortest subarray. If the array is already sorted, return 0.\n\n"
    "Example: nums = [2,6,4,8,10,9,15] → answer = 5 (sort indices 1–5).\n"
    "Example: nums = [1,2,3,4] → answer = 0 (already sorted).\n"
    "Example: nums = [1] → answer = 0 (single element).\n\n"
    "Constraints: 1 ≤ nums.length ≤ 10^4, -10^5 ≤ nums[i] ≤ 10^5."
)

SOL1_CODE = """\
def findUnsortedSubarray(nums: list[int]) -> int:
    n = len(nums)
    left, right = -1, -1           # -1 = no disorder found yet
    max_so_far = float('-inf')     # running max from the left
    min_so_far = float('inf')      # running min from the right

    # Forward pass: find right boundary
    for i in range(n):
        if nums[i] < max_so_far:   # element smaller than something before it
            right = i              # rightmost out-of-place element (keep updating)
        max_so_far = max(max_so_far, nums[i])

    # Backward pass: find left boundary
    for i in range(n - 1, -1, -1):
        if nums[i] > min_so_far:   # element larger than something after it
            left = i               # leftmost out-of-place element (keep updating)
        min_so_far = min(min_so_far, nums[i])

    return 0 if right == -1 else right - left + 1
"""

SOL2_CODE = """\
def findUnsortedSubarray(nums: list[int]) -> int:
    sorted_nums = sorted(nums)      # O(n log n) sort; O(n) extra space
    left, right = 0, len(nums) - 1

    # Find first mismatch from the left
    while left < len(nums) and nums[left] == sorted_nums[left]:
        left += 1
    if left == len(nums):
        return 0  # entirely sorted

    # Find first mismatch from the right
    while nums[right] == sorted_nums[right]:
        right -= 1

    return right - left + 1
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Two-Pass Boundary Scan (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're looking for the minimal window of elements that are in the wrong "
            "position. An element is 'in the wrong position' if it's smaller than "
            "something to its left (it should be further left in sorted order), or "
            "larger than something to its right (it should be further right)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Sorting a copy and comparing is O(n log n) and O(n) space — correct but "
            "suboptimal. Brute force (try every subarray, check if sorting it fixes "
            "the whole array) is O(n^3). We want O(n) time and O(1) space."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We can find each boundary independently with a single linear scan:\n"
            "• RIGHT boundary: scan left→right with a running maximum. Any element "
            "smaller than max_so_far is 'out of place' (smaller than something before "
            "it). The LAST such element is the right edge of the disorder.\n"
            "• LEFT boundary: scan right→left with a running minimum. Any element "
            "larger than min_so_far is 'out of place'. The LAST such element "
            "(= leftmost in the array) is the left edge."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize left = right = -1 as sentinels.\n"
            "2. Forward pass: maintain max_so_far. When nums[i] < max_so_far, "
            "update right = i. Update max_so_far each iteration.\n"
            "3. Backward pass: maintain min_so_far. When nums[i] > min_so_far, "
            "update left = i. Update min_so_far each iteration.\n"
            "4. Return 0 if right == -1 (array sorted), else right - left + 1."
        ),
        N.callout(
            "Analogy: Imagine water flowing over the array from left to right — "
            "it fills behind every 'dip' (element smaller than max). The rightmost "
            "dip is the right boundary. Then water flows from right to left, filling "
            "behind every 'hill' (element larger than min). The leftmost hill is "
            "the left boundary.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("left, right = -1, -1", {"code": True}), " — Sentinels. Stay at -1 if no disorder found (→ return 0)."])),
    N.para(N.rich([("max_so_far = float('-inf')", {"code": True}), " — Running maximum; -inf ensures the first element always exceeds it."])),
    N.para(N.rich([("min_so_far = float('inf')", {"code": True}), " — Running minimum; +inf ensures the first element from the right always beats it."])),
    N.para(N.rich([("if nums[i] < max_so_far:", {"code": True}), " — This element is smaller than something that came before it — it must move leftward in sorted order — it's in the disorder window."])),
    N.para(N.rich([("right = i", {"code": True}), " — Keep overwriting; we want the RIGHTMOST such violation (last one wins)."])),
    N.para(N.rich([("max_so_far = max(max_so_far, nums[i])", {"code": True}), " — Update max AFTER the check so we compare against the previous max, not the current element."])),
    N.para(N.rich([("if nums[i] > min_so_far:", {"code": True}), " — This element is larger than something after it — it must move rightward in sorted order — it's in the disorder window."])),
    N.para(N.rich([("left = i", {"code": True}), " — Keep overwriting; scanning backwards, so the LAST update during the scan is actually the LEFTMOST (earliest index) violation."])),
    N.para(N.rich([("return 0 if right == -1 else right - left + 1", {"code": True}), " — If right was never updated, no disorder → 0. Otherwise return inclusive window size (don't forget the +1!)."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Sort and Compare"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The simplest way to know where elements are out of order: compare the array "
            "to a sorted version of itself. The first position where they differ is the "
            "left boundary; the last such position is the right boundary."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This approach is correct but suboptimal: O(n log n) time from sorting and "
            "O(n) extra space for the sorted copy. Use this as the brute-force baseline "
            "in an interview, then propose the O(n)/O(1) solution as the optimization."
        ),
        N.h4("The Key Observation"),
        N.para(
            "sorted(nums) and nums agree at all indices in the sorted prefix and sorted "
            "suffix. The disorder window is exactly the span between the first and last "
            "mismatch positions."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sort a copy. Walk from the left until you hit a mismatch — that's left. "
            "Walk from the right until you hit a mismatch — that's right. "
            "Return right - left + 1 (or 0 if no mismatch found)."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("sorted_nums = sorted(nums)", {"code": True}), " — Create a sorted copy. O(n log n) time, O(n) space."])),
    N.para(N.rich([("while left < len(nums) and nums[left] == sorted_nums[left]: left += 1", {"code": True}), " — Skip the sorted prefix (elements already in their correct position)."])),
    N.para(N.rich([("if left == len(nums): return 0", {"code": True}), " — If we skipped everything, the array was already sorted."])),
    N.para(N.rich([("while nums[right] == sorted_nums[right]: right -= 1", {"code": True}), " — Skip the sorted suffix."])),
    N.para(N.rich([("return right - left + 1", {"code": True}), " — Window between first and last mismatch (inclusive)."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (try every window)", "O(n³)", "O(1)"],
        ["Sort & Compare", "O(n log n)", "O(n)"],
        ["Two-Pass Boundary Scan (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Stack (implicit — running max/min mimics monotone stack top)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Find Left/Right Boundaries — locate the leftmost and rightmost elements that violate sorted order using complementary linear scans."])),
    N.callout(
        "When to recognize this pattern: 'shortest subarray' + 'sorted'; "
        "find span of disorder in a nearly-sorted array; problems where you need "
        "to find leftmost and rightmost violations of a monotone property. "
        "Also: any problem where 'running max from left' or 'running min from right' "
        "helps identify out-of-place elements.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Stack / Boundary Finding):"),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — Uses the 'running max' concept; explicit monotone stack finds next-greater boundary for each element."])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Monotone decreasing stack gives the 'next warmer day' (right boundary) for each element. LC #739."])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Monotone stack finds previous-smaller and next-smaller boundaries. LC #84."])),
    N.bullet(N.rich([("132 Pattern", {"bold": True}), " (Medium) — Backward scan with running minimum; same right-to-left boundary-finding approach. LC #456."])),
    N.bullet(N.rich([("Maximum Width Ramp", {"bold": True}), " (Medium) — Find widest window satisfying an order constraint; complementary two-pass structure. LC #962."])),
    N.bullet(N.rich([("Find First and Last Position of Element in Sorted Array", {"bold": True}), " (Medium) — Binary-search variant of left/right boundary finding. LC #34."])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Two-pass max/min from each direction; structurally identical scan pattern. LC #42."])),
    N.para("These problems share the core technique: locate the leftmost and/or rightmost position satisfying a violation condition using complementary directional scans with a running aggregate (max or min)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Monotonic Stack / Stack-Queue section · Sub-Pattern: Find Left/Right Boundaries", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through both forward and backward passes visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"  Appended {len(blocks)} blocks OK")
print(f"NOTION OK {PAGE_ID}")
