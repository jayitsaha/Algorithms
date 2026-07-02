"""
gen_two_sum.py — Regenerate the Two Sum (#1) Notion page in-place.
Run from the Algorithms directory:
    python gen_two_sum.py
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8111-9dfd-d59f81474c73"
SLUG = "two_sum"

# ── 1. Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1,
    pattern="Hashing",
    subpatterns=["Hash Map (Complement Lookup)", "Two Pointers: Opposite Direction"],
    tc="O(n)",
    sc="O(n)",
    key_insight="For each num, complement = target - num. A hash map gives O(1) lookup of previously seen complements.",
    icon="🟢"
)
print("Properties OK")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build blocks ────────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("target", {"code": True}),
        (", return ", {}),
        ("indices", {"bold": True}),
        (" of the two numbers such that they add up to ", {}),
        ("target", {"code": True}),
        (". You may assume each input has exactly one solution, and you may not use the same element twice. Return the answer in any order.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("nums = [2, 7, 11, 15], target = 9 → [0, 1]", {"code": True}),
            (" because nums[0] + nums[1] = 2 + 7 = 9.", {}),
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# Solution 1 — One-Pass Hash Map
sol1_code = """\
def twoSum(nums: list, target: int) -> list:
    seen = {}                          # hash map: value -> index
    for i, num in enumerate(nums):
        complement = target - num      # the number we need to pair with num
        if complement in seen:         # O(1) lookup — found the pair!
            return [seen[complement], i]
        seen[num] = i                  # store AFTER checking to avoid self-pairing
"""

blocks += [
    N.h2("Solution 1 — One-Pass Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're not looking for any pair — we're looking for a specific complement. For every number x, there's exactly one number that could partner with it: target - x. The question becomes: 'Have I already seen that complement?'"),
        N.h4("What Doesn't Work"),
        N.para("A brute-force O(n²) approach checks every pair with two nested loops. For n=100,000 that's ~5 billion comparisons — far too slow. The inner loop is the bottleneck: it linearly searches for the complement."),
        N.h4("The Key Observation"),
        N.para("If I could look up 'does the complement exist?' in O(1), the entire scan would be O(n). A hash map gives exactly that. Every element we've processed so far can be stored in the map for instant lookup."),
        N.h4("Building the Solution"),
        N.para("Scan left to right. At each element: (1) compute complement = target - num, (2) check the map — if found, done!, (3) otherwise store current element and move on. Critical: check BEFORE storing, or we risk pairing an element with itself."),
        N.callout("Analogy: You're looking for a dance partner with a specific height. Instead of asking everyone in the room one-by-one (O(n) per person), you post a 'looking for height X' board at the entrance and read it as each person arrives — O(1) lookup.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = {}", {"code": True}), (" — Initialize empty hash map. Will store {number_value: array_index} for every element we've processed so far.", {})])),
    N.para(N.rich([("for i, num in enumerate(nums):", {"code": True}), (" — Iterate with both index and value. enumerate gives (0, 2), (1, 7), ... automatically.", {})])),
    N.para(N.rich([("complement = target - num", {"code": True}), (" — Compute the partner we need. If target=9 and num=2, complement=7. Only a 7 can complete this pair.", {})])),
    N.para(N.rich([("if complement in seen:", {"code": True}), (" — O(1) hash map lookup. Python dict membership test is average O(1). No loop needed.", {})])),
    N.para(N.rich([("return [seen[complement], i]", {"code": True}), (" — Return the earlier index (where complement was found) and current index i. The pair is done!", {})])),
    N.para(N.rich([("seen[num] = i", {"code": True}), (" — Store AFTER the check. This ensures we never pair index i with itself. Only elements before i can be in seen when we check.", {})])),
    N.divider(),
]

# Solution 2 — Brute Force
sol2_code = """\
def twoSum(nums: list, target: int) -> list:
    n = len(nums)
    for i in range(n):               # fix the first element
        for j in range(i + 1, n):   # try every element after i
            if nums[i] + nums[j] == target:
                return [i, j]
    # Problem guarantees a solution exists, so we always return above
"""

blocks += [
    N.h2("Solution 2 — Brute Force (Nested Loops)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest interpretation: try every possible pair of indices (i, j) where i < j, and check if the two values sum to target."),
        N.h4("What Doesn't Work at Scale"),
        N.para("For n elements there are n*(n-1)/2 pairs. At n=10,000 that's ~50 million checks. At n=100,000 it's 5 billion. This is too slow for large inputs, but perfectly correct for small ones."),
        N.h4("The Key Observation"),
        N.para("Starting the inner loop at j = i+1 ensures we never check the same pair twice and never pair an element with itself. This is the correct brute force invariant."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer fixes i (first element), inner tries all j > i (second element). Direct sum check. Return immediately when found."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — Outer loop fixes the first element of the potential pair.", {})])),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}), (" — Inner loop starts AFTER i — never before, never equal. Guarantees distinct indices.", {})])),
    N.para(N.rich([("if nums[i] + nums[j] == target:", {"code": True}), (" — Direct sum check. O(1) arithmetic — no hash map needed.", {})])),
    N.divider(),
]

# Solution 3 — Two Pointer (sorted)
sol3_code = """\
# Only valid when input is already SORTED (e.g. LeetCode #167)
def twoSum_sorted(numbers: list, target: int) -> list:
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]   # 1-indexed for #167
        elif s < target:
            left += 1    # sum too small: increase by moving left pointer right
        else:
            right -= 1   # sum too big: decrease by moving right pointer left
"""

blocks += [
    N.h2("Solution 3 — Two-Pointer (Sorted Input Only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("When the input array is sorted, we can use the ordering to our advantage. Start with the widest possible window (leftmost + rightmost), then shrink it based on whether the current sum is too large or too small."),
        N.h4("Why Sorting Enables This"),
        N.para("In a sorted array, moving the left pointer right increases the sum; moving the right pointer left decreases it. This monotonic property means we can make progress in the correct direction at each step without missing any pair."),
        N.h4("The Key Observation"),
        N.para("If left + right sum > target: the right element is too large — move right pointer left. If sum < target: the left element is too small — move left pointer right. If equal: done. We never need to backtrack."),
        N.h4("Building the Solution"),
        N.para("Initialize left=0, right=n-1. Loop while left < right. Compute sum and adjust pointers. O(n) time, O(1) space — better constants than the hash map approach."),
        N.callout("Note: This approach cannot be used for the original #1 (unsorted, need original indices). It is the optimal approach for #167 (Two Sum II — Input Array Is Sorted).", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.h3("Line by Line"),
    N.para(N.rich([("left, right = 0, len(numbers) - 1", {"code": True}), (" — Two pointers: left at smallest element, right at largest.", {})])),
    N.para(N.rich([("s = numbers[left] + numbers[right]", {"code": True}), (" — Compute current sum of the two candidates.", {})])),
    N.para(N.rich([("elif s < target: left += 1", {"code": True}), (" — Sum is too small. Moving left pointer right increases sum (larger left value).", {})])),
    N.para(N.rich([("else: right -= 1", {"code": True}), (" — Sum is too large. Moving right pointer left decreases sum (smaller right value).", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (Nested Loops)", "O(n²)", "O(1)", "Correct; propose first in interview"],
        ["One-Pass Hash Map (optimal)", "O(n)", "O(n)", "Interview pick; handles unsorted, duplicates"],
        ["Two-Pointer (sorted only)", "O(n)", "O(1)", "Best for #167; needs sorted input"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hashing", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Hash Map (Complement Lookup), Two Pointers: Opposite Direction (sorted variant)", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Find two elements summing to X' — complement = target - x, hash map for O(1) lookup. (2) 'Return indices' (not values) — sorting loses original indices, so hash map wins. (3) Inner loop searching linearly — ask 'could a hash map make this O(1)?'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same complement + hash map or two-pointer technique:"),
    N.bullet(N.rich([("Two Sum II – Input Array is Sorted", {"bold": True}), (" (Medium) — Two-pointer from ends, O(1) space since sorted (#167)", {})])),
    N.bullet(N.rich([("3Sum", {"bold": True}), (" (Medium) — Sort + fix one element + two-pointer for the remaining pair (#15)", {})])),
    N.bullet(N.rich([("4Sum", {"bold": True}), (" (Medium) — Two outer fixings + two-pointer; O(n³) (#18)", {})])),
    N.bullet(N.rich([("Two Sum IV – BST Input", {"bold": True}), (" (Easy) — Traverse BST in-order, store seen values in a hash set (#653)", {})])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sums + hash map; count subarrays summing to k (#560)", {})])),
    N.bullet(N.rich([("Continuous Subarray Sum", {"bold": True}), (" (Medium) — Prefix sum modulo + hash map for divisibility (#523)", {})])),
    N.bullet(N.rich([("Max Number of K-Sum Pairs", {"bold": True}), (" (Medium) — Greedy complement counter for pair removal (#1679)", {})])),
    N.para("These problems all share the core technique: store seen values in a hash structure to enable O(1) complement lookup."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Hashing section. Sub-Pattern: Hash Map (Complement Lookup).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ───────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
