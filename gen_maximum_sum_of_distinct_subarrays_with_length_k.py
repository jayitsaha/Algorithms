"""
gen_maximum_sum_of_distinct_subarrays_with_length_k.py
Notion regeneration for LeetCode #2461 – Maximum Sum of Distinct Subarrays With Length K
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8119-b7c7-f298976b30e5"
SLUG    = "maximum_sum_of_distinct_subarrays_with_length_k"

# ── 1. Set page properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2461,
    pattern="Sliding Window",
    subpatterns=["Sliding Window (Fixed)", "Sum + Distinct Check"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Maintain a freq map in a fixed-size window; len(freq)==k iff all k elements are distinct.",
    icon="🟡",
    status="Solved",
    source="LeetCode",
)
print("Properties set OK")

# ── 2. Wipe old body ──────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks")

# ── 3. Build new body ─────────────────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given an integer array nums and an integer k, return the maximum subarray sum among all "
    "subarrays of length exactly k that contain all distinct elements. Return 0 if no such "
    "subarray exists. A subarray is a contiguous non-empty sequence of elements within an array."
)

SOL1_CODE = """\
def maximumSubarraySum(nums: list[int], k: int) -> int:
    freq = {}
    current_sum = 0
    max_sum = 0
    l = 0
    for r in range(len(nums)):
        # Add incoming element to frequency map and running sum
        freq[nums[r]] = freq.get(nums[r], 0) + 1
        current_sum += nums[r]
        # If window grew beyond k, shrink from the left
        if r - l + 1 > k:
            freq[nums[l]] -= 1
            if freq[nums[l]] == 0:
                del freq[nums[l]]   # keep len(freq) accurate
            current_sum -= nums[l]
            l += 1
        # Valid window: exactly k elements, all distinct
        if r - l + 1 == k and len(freq) == k:
            max_sum = max(max_sum, current_sum)
    return max_sum"""

SOL2_CODE = """\
def maximumSubarraySum(nums: list[int], k: int) -> int:
    # Brute force: O(n*k) — check every window independently
    max_sum = 0
    for i in range(len(nums) - k + 1):
        window = nums[i:i+k]
        if len(set(window)) == k:           # O(k) distinct check
            max_sum = max(max_sum, sum(window))  # O(k) sum
    return max_sum"""

blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Sliding Window (Optimal, Interview Pick) ──────────────────────
blocks += [
    N.h2("Solution 1 — Sliding Window + Frequency Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the maximum sum over all windows of exactly k elements that have no "
            "repeats. Two things must be true simultaneously: window size = k AND all distinct."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A brute-force approach extracts each window, builds a set to check distinctness, "
            "and computes the sum — all O(k) operations per window, totalling O(n·k). "
            "The waste: adjacent windows share k-1 elements, yet we recompute everything "
            "from scratch. If n=10^5 and k=10^4, that's 10^9 operations — too slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We can maintain both the sum and the distinctness check in O(1) per slide. "
            "For the sum: keep a running current_sum — add the incoming element, subtract "
            "the outgoing one. For distinctness: maintain a frequency map (value → count). "
            "After each slide, len(freq) == k iff all k elements in the window are unique."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Use a fixed-size sliding window: right pointer r grows the window, and whenever "
            "the window exceeds size k, we advance left pointer l. After each shrink, check if "
            "the window is valid. Why a freq map instead of a plain set? Because if value v "
            "appears at both the leaving position l AND inside the remaining window, removing v "
            "from a set would incorrectly mark it as absent. The freq map tracks how many copies "
            "of v are in the window — only delete the key when count drops to 0."
        ),
        N.callout(
            "Analogy: imagine a conveyor belt of exactly k items. As a new item rolls on at the "
            "right, the oldest item falls off the left. A tally board tracks how many of each "
            "item type are on the belt. When every type has exactly one count, the belt is "
            "'all distinct'. Only then does the sum matter.",
            "🏭", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = {}", {"code": True}), " — frequency map: value → count within current window [l..r]."])),
    N.para(N.rich([("current_sum = 0", {"code": True}), " — running sum of nums[l..r]; updated O(1) per slide."])),
    N.para(N.rich([("max_sum = 0", {"code": True}), " — best valid-window sum seen. 0 handles 'no valid window' case naturally."])),
    N.para(N.rich([("freq[nums[r]] = freq.get(nums[r], 0) + 1", {"code": True}), " — add the incoming right element to freq map."])),
    N.para(N.rich([("current_sum += nums[r]", {"code": True}), " — update running sum."])),
    N.para(N.rich([("if r - l + 1 > k:", {"code": True}), " — window grew past k; we must remove the leftmost element."])),
    N.para(N.rich([("freq[nums[l]] -= 1", {"code": True}), " — decrement count of the outgoing element."])),
    N.para(N.rich([("if freq[nums[l]] == 0: del freq[nums[l]]", {"code": True}), " — remove the key entirely so len(freq) stays accurate (critical!)."])),
    N.para(N.rich([("current_sum -= nums[l]; l += 1", {"code": True}), " — subtract outgoing element from sum and advance left pointer."])),
    N.para(N.rich([("if r - l + 1 == k and len(freq) == k:", {"code": True}), " — window is exactly k AND every element is distinct (one key per element in freq)."])),
    N.para(N.rich([("max_sum = max(max_sum, current_sum)", {"code": True}), " — valid window! Update best answer."])),
    N.para(N.rich([("return max_sum", {"code": True}), " — 0 if no valid window was ever found."])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each possible starting position, extract the window, check if all distinct, compute the sum."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n·k) — works for small inputs but times out for n up to 10^5 and k up to 10^4."),
        N.h4("The Key Observation"),
        N.para("No optimization here — this is the baseline. Useful to propose first in an interview, then explain why it's inefficient and pivot to the sliding window approach."),
        N.h4("Building the Solution"),
        N.para(
            "Iterate i from 0 to n-k. Slice nums[i:i+k] (O(k)). Check len(set(window)) == k (O(k)). "
            "Compute sum(window) (O(k)). Update max_sum."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(nums) - k + 1):", {"code": True}), " — i is the start index of each window; there are n-k+1 valid windows."])),
    N.para(N.rich([("window = nums[i:i+k]", {"code": True}), " — O(k) slice to extract the window."])),
    N.para(N.rich([("if len(set(window)) == k:", {"code": True}), " — O(k) set construction to check all distinct."])),
    N.para(N.rich([("max_sum = max(max_sum, sum(window))", {"code": True}), " — O(k) sum computation. Entire inner block is O(k) per window."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Sliding Window (optimal)", "O(n)", "O(k)", "Each element added/removed exactly once"],
        ["Brute Force", "O(n·k)", "O(k)", "Recomputes sum/distinctness from scratch per window"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sliding Window (Fixed) · Sum + Distinct Check"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'contiguous subarray/substring of exactly length k' → fixed sliding window; "
        "(2) 'maximize/minimize aggregate over length-k windows' → maintain running aggregate; "
        "(3) 'all elements distinct within window' → freq map, check len(freq)==k. "
        "Key tell: O(n·k) brute force exists but you're told n can be 10^5 → optimize the overlap.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (fixed sliding window + freq map / aggregate):"),
    N.bullet(N.rich([("Maximum Average Subarray I", {"bold": True}), " (Easy) — Fixed window sum, no distinctness. Same sliding sum pattern. (#643)"])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), " (Medium) — Fixed window |p|, freq map matches anagram. (#438)"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Fixed window, track max via monotonic deque. (#239)"])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), " (Medium) — Variable window, expand until duplicate, shrink to remove. (#3)"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — Variable window, at most 2 distinct values; freq map same technique. (#904)"])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), " (Medium) — Variable window; shrink while sum >= target. (#209)"])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), " (Medium) — Variable window counting subarrays. Same expand/shrink skeleton. (#713)"])),
    N.para("These problems share the core technique: maintain an aggregate (sum, max, product) and a validity invariant (distinct, bounded, matching) across a sliding window in O(n) total."),
    N.callout("📚 Source: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4 Sliding Window (Fixed)", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
