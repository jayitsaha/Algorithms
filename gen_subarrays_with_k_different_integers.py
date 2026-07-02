"""
gen_subarrays_with_k_different_integers.py
Update Notion page IN-PLACE for LeetCode #992 — Subarrays with K Different Integers
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c8-abb3-cb72821a797f"
SLUG    = "subarrays_with_k_different_integers"

# ─── 1) Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Hard",
    number      = 992,
    pattern     = "Sliding Window",
    subpatterns = ["AtMost(K) - AtMost(K-1)"],
    tc          = "O(n)",
    sc          = "O(k)",
    key_insight = "exactly(K) = atMost(K) − atMost(K−1); run sliding-window helper twice.",
    icon        = "🔴",
)
print("  Properties OK")

# ─── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

# ─── 3) Rebuild body ──────────────────────────────────────────────────────────
print("Appending new blocks...")
blocks = []

# ── Problem statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the number of ", {}),
        ("good subarrays", {"bold": True}),
        (". A subarray is good if it contains ", {}),
        ("exactly k", {"bold": True}),
        (" different integers.\n\n"
         "Example 1: nums = [1,2,1,2,3], k = 2  →  7\n"
         "Example 2: nums = [1,2,1,3,4], k = 3  →  3\n\n"
         "Constraints: 1 ≤ nums.length ≤ 20000, 1 ≤ nums[i] ≤ nums.length, 1 ≤ k ≤ nums.length", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Brute Force ───────────────────────────────────────────────────
BRUTE_CODE = """\
def subarraysWithKDistinct(nums: list[int], k: int) -> int:
    n = len(nums)
    result = 0
    for i in range(n):                     # start of subarray
        seen = set()
        for j in range(i, n):              # end of subarray
            seen.add(nums[j])
            if len(seen) == k:
                result += 1
            elif len(seen) > k:            # can't get fewer distinct by extending
                break
    return result
"""

blocks += [
    N.h2("Solution 1 — Brute Force (enumerate all subarrays)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need every contiguous subarray that has exactly k distinct numbers. The simplest approach: try every possible start and end index, count distinct values, and record hits."),
        N.h4("What Doesn't Work at Scale"),
        N.para("O(n²) subarrays × O(n) to count distinct each time = O(n³). Even the nested-loop version that reuses a running set is O(n²) — fine for n ≤ 1000 but TLEs at n = 20000."),
        N.h4("The Key Observation"),
        N.para("When we fix the left boundary i and extend j rightward, distinct count is monotonically non-decreasing. So once we exceed k, we can break early — no need to keep extending."),
        N.h4("Building the Solution"),
        N.para("Outer loop fixes i. Inner loop advances j, adds nums[j] to a set, checks count: == k → count it, > k → break. This is the clearest correct baseline to state before optimizing."),
        N.callout("Analogy: Like checking every possible slice of a fruit bowl — stop as soon as you've picked up too many kinds of fruit. Correct, but slow for a huge bowl.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n)", {"code": True}), " — outer loop: fix the subarray's left boundary at every index."])),
    N.para(N.rich([("seen = set()", {"code": True}), " — fresh set for each starting position; tracks distinct values in current subarray."])),
    N.para(N.rich([("for j in range(i, n)", {"code": True}), " — inner loop: extend right boundary from i outward."])),
    N.para(N.rich([("seen.add(nums[j])", {"code": True}), " — add the new element; set automatically ignores duplicates."])),
    N.para(N.rich([("if len(seen) == k", {"code": True}), " — exactly k distinct → this is a good subarray, count it."])),
    N.para(N.rich([("elif len(seen) > k", {"code": True}), " — exceeded k → extending further can only add more distinct values, so break early."])),
    N.divider(),
]

# ── Solution 2 — AtMost Trick (Optimal) ───────────────────────────────────────
OPTIMAL_CODE = """\
def subarraysWithKDistinct(nums: list[int], k: int) -> int:

    def atMost(k: int) -> int:
        count = {}          # frequency map of elements in sliding window
        left = 0            # left boundary of window
        result = 0          # accumulator
        for right in range(len(nums)):
            # Expand: add nums[right] into the window
            count[nums[right]] = count.get(nums[right], 0) + 1
            # Shrink: while window has more than k distinct, move left
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]   # distinct count drops by 1
                left += 1
            # Every subarray ending at right with start in [left..right] is valid
            result += right - left + 1
        return result

    # Exactly K = At Most K − At Most (K-1)
    return atMost(k) - atMost(k - 1)
"""

blocks += [
    N.h2("Solution 2 — AtMost(K) − AtMost(K−1) (Interview Pick) ✓"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Counting subarrays with EXACTLY k distinct integers is awkward with a plain sliding window — when the window has exactly k distinct values, we can't tell whether to expand or shrink. But counting ≤ k distinct is easy with a shrink-when-too-many window."),
        N.h4("What Doesn't Work"),
        N.para("A naive 'exactly k' window: expand right, and when distinct == k, try to count valid subarrays. The issue is the left pointer has no clear stopping rule — the window [left..right] may validly start from many different positions, not just one."),
        N.h4("The Key Observation"),
        N.para("Set subtraction: {subarrays with exactly K distinct} = {subarrays with ≤ K distinct} − {subarrays with ≤ K−1 distinct}. The ≤ K version has a clean sliding window because the invariant is clear: shrink until distinct ≤ k."),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Write atMost(k) using a sliding window. Expand right, add to frequency map. "
            "If distinct count exceeds k, shrink from left (decrement freq, delete key if zero, advance left). "
            "At each right, ALL subarrays [left..right], [left+1..right], ..., [right..right] are valid, "
            "so add (right − left + 1) to result.\n\n"
            "Step 2: The answer is atMost(k) − atMost(k−1). Two O(n) passes = O(n) total."
        ),
        N.callout(
            "Analogy: Count shelves with ≤ 5 books. Count shelves with ≤ 4 books. Subtract — you get shelves with exactly 5 books. "
            "The individual ≤ k counts are easy; the 'exactly k' count falls out of the subtraction.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def atMost(k)", {"code": True}), " — helper that counts subarrays with AT MOST k distinct integers. We call it twice: with k and with k−1."])),
    N.para(N.rich([("count = {}", {"code": True}), " — sliding window frequency map: element → how many times it appears in the current window [left..right]."])),
    N.para(N.rich([("left = 0", {"code": True}), " — left pointer; we only advance it rightward (never back), so overall O(n)."])),
    N.para(N.rich([("count[nums[right]] = count.get(nums[right], 0) + 1", {"code": True}), " — expand window: add new right element to freq map. If unseen, get returns 0."])),
    N.para(N.rich([("while len(count) > k", {"code": True}), " — invariant violation: more than k distinct in window → must shrink."])),
    N.para(N.rich([("count[nums[left]] -= 1", {"code": True}), " — reduce frequency of leftmost element."])),
    N.para(N.rich([("if count[nums[left]] == 0: del count[nums[left]]", {"code": True}), " — if frequency hits 0, remove key entirely so len(count) reflects true distinct count."])),
    N.para(N.rich([("left += 1", {"code": True}), " — advance left boundary. Loop continues until distinct ≤ k again."])),
    N.para(N.rich([("result += right - left + 1", {"code": True}), " — key insight: with left fixed as the minimum valid start, every subarray [i..right] for i in [left..right] is valid. That's right−left+1 subarrays."])),
    N.para(N.rich([("return atMost(k) - atMost(k - 1)", {"code": True}), " — exactly k distinct = at most k − at most k−1. Run helper twice and subtract."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(k)", "TLE for n = 20000"],
        ["AtMost Trick (✓)", "O(n)", "O(k)", "Two linear passes; interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "AtMost(K) − AtMost(K−1) (Variable Sliding Window with set-subtraction trick)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for subarrays/substrings with EXACTLY k of something\n"
        "• Directly tracking 'exactly k' leads to ambiguous window boundaries\n"
        "• The ≤ k version can be cleanly solved with a sliding window\n"
        "• Key trigger: 'exactly K distinct integers/characters in subarray'",
        "🔎", "green_background"
    ),
    N.para("Sub-pattern classification source: Analysis — 'AtMost(K) − AtMost(K−1)' is a well-known technique not listed as a distinct sub-pattern in the guide but categorized under Sliding Window (Variable / Dynamic)."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), " (Medium) — the core atMost helper is the direct solution here"])),
    N.bullet(N.rich([("Count Number of Nice Subarrays", {"bold": True}), " (Medium) — exactly K odd numbers: replace 'distinct' with parity; same atMost trick"])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), " (Medium) — count subarrays using right−left+1; teaches the key counting step inside the window loop"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — exactly 2 distinct types; isomorphic to atMost(2)"])),
    N.bullet(N.rich([("Number of Substrings Containing All Three Characters", {"bold": True}), " (Medium) — at-least variant; complement approach is dual of at-most"])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), " (Hard) — variable window with frequency map; same shrink-when-invalid structure"])),
    N.para("These problems all share the core technique: define a monotone predicate on subarrays, use a sliding window to count efficiently, and apply set arithmetic when 'exactly K' is hard but '≤ K' is easy."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4–1.5 (Sliding Window, Variable/Dynamic)", "📚", "gray_background"),
]

# ── Visual Explainer Embed ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"  Appended {len(blocks)} blocks")
print(f"NOTION OK {PAGE_ID}")
