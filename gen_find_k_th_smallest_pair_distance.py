import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a6-b73e-fb48307cbd90"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=719,
    pattern="Binary Search",
    subpatterns=["Binary Search + Count Pairs"],
    tc="O(n log n + n log W)",
    sc="O(1)",
    key_insight="Binary search on the answer: count pairs with distance ≤ mid using two-pointer sweep; shrink range until converged.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe ────────────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the k-th smallest distance among all the pairs ", {}),
        ("nums[i]", {"code": True}),
        (" and ", {}),
        ("nums[j]", {"code": True}),
        (" where ", {}),
        ("0 ≤ i < j < n", {"code": True}),
        (". The distance of a pair (i, j) is |nums[i] − nums[j]|.", {}),
    ])),
    N.para("Example: nums = [1, 3, 1], k = 1 → All distances: (1,3)→2, (1,1)→0, (3,1)→2. Sorted: [0,2,2]. Answer = 0."),
    N.para("Constraints: n up to 10,000; values up to 1,000,000. Generating all O(n²) pairs is TLE."),
    N.divider(),
]

# ── Solution 1: Optimal — Binary Search on Answer
sol1_code = '''\
def smallestDistancePair(nums: list[int], k: int) -> int:
    nums.sort()                         # sort in-place for two-pointer count
    n = len(nums)
    lo, hi = 0, nums[-1] - nums[0]     # distance search space

    while lo < hi:
        mid = (lo + hi) // 2

        # Count pairs with distance <= mid (two-pointer, O(n))
        count = i = 0
        for j in range(n):
            while nums[j] - nums[i] > mid:
                i += 1
            count += j - i              # indices i..j-1 pair with j

        if count >= k:
            hi = mid                    # answer could be <= mid; keep mid
        else:
            lo = mid + 1               # answer > mid; exclude mid

    return lo                           # smallest d where count(d) >= k'''

blocks += [
    N.h2("Solution 1 — Binary Search on Answer + Two-Pointer Count (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the k-th smallest value in the set of all pair distances. With n=10,000 there are ~50M pairs — too many to list. Instead, ask a different question: 'For a given distance d, how many pairs have distance ≤ d?' If we can answer that efficiently, we can binary search for the exact answer."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: generate all C(n,2) pairs, compute distances, sort, index. Time O(n² log n), space O(n²). For n=10,000 this is 50M operations and 400MB — TLE and MLE."),
        N.h4("The Key Observation"),
        N.para("The count function count_pairs(d) = #{(i,j): nums[j]−nums[i] ≤ d} is MONOTONE in d. As d grows, count never decreases. This monotonicity is the prerequisite for binary search on the answer: we find the smallest d where count(d) ≥ k."),
        N.h4("Building the Solution"),
        N.para("1. Sort nums — makes all differences non-negative and enables two-pointer counting. 2. Binary search over [0, max−min]. 3. For each mid, count pairs in O(n) with a sliding window: right pointer j scans right; left pointer i advances when diff > mid. All indices i..j-1 are valid left partners for j (add j−i to count). 4. Converge: hi=mid when count≥k; lo=mid+1 when count<k. Return lo."),
        N.callout("Analogy: Like finding the median of a sorted list. You don't need to see the list — you just need to count 'how many elements are ≤ x' for successive guesses of x. That count function is monotone, so binary search works.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), (" — sort in-place; required so differences are non-negative and two-pointer counting works correctly.", {})])),
    N.para(N.rich([("lo, hi = 0, nums[-1] - nums[0]", {"code": True}), (" — distance search space. lo=0 (if duplicates, distance can be 0). hi=max−min (largest possible distance after sorting).", {})])),
    N.para(N.rich([("while lo < hi", {"code": True}), (" — binary search until converged. When lo==hi, we've pinpointed the exact answer.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — candidate distance threshold. Floor division ensures mid < hi when lo < hi, preventing infinite loops.", {})])),
    N.para(N.rich([("count = i = 0", {"code": True}), (" — initialize pair count and left pointer. Crucially, i is NOT reset inside the for loop — it carries over across j iterations (amortized O(n)).", {})])),
    N.para(N.rich([("for j in range(n):", {"code": True}), (" — j is the right pointer of the sliding window. It fixes the right (larger) element of each pair.", {})])),
    N.para(N.rich([("while nums[j] - nums[i] > mid: i += 1", {"code": True}), (" — shrink the window from the left until the difference is within threshold. i only moves right, never resets.", {})])),
    N.para(N.rich([("count += j - i", {"code": True}), (" — elements at indices i, i+1, ..., j-1 all form valid pairs with j (distance ≤ mid). There are exactly j−i such pairs.", {})])),
    N.para(N.rich([("if count >= k: hi = mid", {"code": True}), (" — enough pairs have dist ≤ mid; answer could be mid or smaller. Keep mid as a candidate by setting hi=mid (not mid−1).", {})])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — too few pairs; answer is definitely > mid. Raise lo to mid+1.", {})])),
    N.para(N.rich([("return lo", {"code": True}), (" — when lo==hi, this is the smallest d where count(d) ≥ k, which is exactly the k-th smallest pair distance.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force
sol2_code = '''\
from itertools import combinations

def smallestDistancePair_brute(nums: list[int], k: int) -> int:
    # Generate all pair distances
    distances = sorted(abs(a - b) for a, b in combinations(nums, 2))
    return distances[k - 1]  # k is 1-indexed'''

blocks += [
    N.h2("Solution 2 — Brute Force: Generate All Pairs (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest interpretation: list every pair, compute every distance, sort, pick the k-th. Use itertools.combinations for clean pair generation."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n² log n) time and O(n²) space. For n=10,000, that's 50 million pairs and sorting 50 million numbers. LeetCode TLEs at n≈3000."),
        N.h4("The Key Observation"),
        N.para("Useful as a correctness baseline to verify the optimal solution. Conceptually simple to derive — but never use in an interview as the final answer."),
        N.h4("Building the Solution"),
        N.para("Use combinations(nums, 2) to yield all (i,j) pairs without repeating. Compute |a−b| for each. Sort all distances. Return distances[k−1] (0-indexed)."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("combinations(nums, 2)", {"code": True}), (" — generates all C(n,2) unique pairs (a,b). For n=6, that's 15 pairs.", {})])),
    N.para(N.rich([("sorted(abs(a-b) for a,b in ...)", {"code": True}), (" — generator for all distances, sorted in ascending order. O(n² log n) total.", {})])),
    N.para(N.rich([("return distances[k-1]", {"code": True}), (" — k is 1-indexed, so the k-th smallest is at index k−1.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (generate + sort pairs)", "O(n² log n)", "O(n²)"],
        ["Binary Search on Answer (optimal)", "O(n log n + n log W)", "O(1)"],
    ]),
    N.para("W = nums[-1] − nums[0] ≤ 10⁶. log W ≈ 20. So the optimal is effectively O(20n) after sorting — extremely fast in practice."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search on Answer (BS on Value), Two-Pointer Sliding Window (for counting)", {})])),
    N.callout(
        "When to recognize this pattern: 'k-th smallest of an implicitly huge set' (pairs, subsequences, etc.) where enumerating all elements is O(n²) or worse. The key is a monotone predicate: 'count(d) ≥ k' flips from false to true exactly once as d increases. The counting step must be O(n) or O(n log n) — here it's O(n) via two-pointer after sorting.",
        "🔎",
        "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using Binary Search on Answer (monotone predicate):"),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — BS on eating speed; count piles completable per hour ≤ H", {})])),
    N.bullet(N.rich([("Capacity To Ship Packages Within D Days", {"bold": True}), (" (Medium) — BS on ship capacity; count days needed", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a Sorted Matrix", {"bold": True}), (" (Medium) — BS on value; count elements ≤ mid per row using two pointers", {})])),
    N.bullet(N.rich([("Smallest Range Covering Elements from K Lists", {"bold": True}), (" (Hard) — BS + count on sorted merged structure", {})])),
    N.bullet(N.rich([("Median of Two Sorted Arrays", {"bold": True}), (" (Hard) — BS on partition point; implicit k-th smallest", {})])),
    N.bullet(N.rich([("Find the K-th Smallest Sum of a Matrix With Sorted Rows", {"bold": True}), (" (Hard) — same BS-on-answer template, more complex counting", {})])),
    N.bullet(N.rich([("Maximum Average Subarray II", {"bold": True}), (" (Hard) — BS on the average value; feasibility check per candidate", {})])),
    N.bullet(N.rich([("Minimize Max Distance to Gas Station", {"bold": True}), (" (Hard) — BS on distance; count stations needed", {})])),
    N.para("These problems share the template: binary search the answer, verify with a monotone O(n) or O(n log n) feasibility check."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9: Binary Search → 'BS on Answer' sub-pattern", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_k_th_smallest_pair_distance")),
    N.para(N.rich([
        ("Step through the binary search visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append ──────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
