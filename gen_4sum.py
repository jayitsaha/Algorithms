"""
gen_4sum.py — Notion update for LeetCode #18 · 4Sum (REGENERATED)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cb-a80c-fcf79c980e79"

# ── 1) Update page properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=18,
    pattern="Two Pointers",
    subpatterns=["Sort + Fix Two + Two Pointers"],
    tc="O(n³)",
    sc="O(1)",
    key_insight="Fix two outer indices via nested loops on a sorted array; collapse two inner pointers to find the complementary pair in O(n). Skip adjacent duplicates for dedup.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build page body ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("target", {"code": True}),
        (", return all unique quadruplets [a, b, c, d] from ", {}),
        ("nums", {"code": True}),
        (" such that ", {}),
        ("a + b + c + d == target", {"code": True}),
        (". Each quadruplet must appear in non-decreasing order and no two quadruplets may be identical.", {}),
    ])),
    N.para("Constraints: 1 ≤ nums.length ≤ 200, -10⁹ ≤ nums[i] ≤ 10⁹, -10⁹ ≤ target ≤ 10⁹."),
    N.divider(),
]

# ── Solution 1: Sort + Fix Two + Two Pointers (Optimal / Interview Pick) ──
SOLUTION1_CODE = '''\
def fourSum(nums: list[int], target: int) -> list[list[int]]:
    nums.sort()
    n, res = len(nums), []

    for i in range(n - 3):
        # Skip duplicate values for i
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        # Pruning: minimum 4-sum from i already exceeds target
        if nums[i] * 4 > target:
            break
        # Pruning: maximum 4-sum from i cannot reach target
        if nums[i] + nums[-1] * 3 < target:
            continue

        for j in range(i + 1, n - 2):
            # Skip duplicate values for j (guard: j > i+1, NOT j > 0!)
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            # Pruning for (i, j) pair
            if nums[i] + nums[j] * 3 > target:
                break
            if nums[i] + nums[j] + nums[-1] * 2 < target:
                continue

            left, right = j + 1, n - 1
            while left < right:
                s = nums[i] + nums[j] + nums[left] + nums[right]
                if s == target:
                    res.append([nums[i], nums[j], nums[left], nums[right]])
                    # Skip duplicates at left and right
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    left += 1
                else:
                    right -= 1

    return res
'''

blocks += [
    N.h2("Solution 1 — Sort + Fix Two + Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need every unique 4-element subset summing to target. Brute force is four nested loops — O(n⁴). The question is: can we use the sorted structure of the array to reduce this?"),

        N.h4("What Doesn't Work"),
        N.para("Pure brute force (four nested loops + set for dedup): O(n⁴) time, O(n) space. For n=200, that's 1.6 billion iterations. Too slow."),

        N.h4("The Key Observation"),
        N.para("If we sort the array, we get two things for free: (1) Two-pointer convergence — in a sorted suffix, moving left right increases the sum, moving right left decreases it, so we can binary-search for pairs in O(n). (2) Deduplication — equal values are adjacent, so we just skip them. Fix two elements with O(n²) nested loops, then run 2Sum II (O(n)) on the remaining suffix. Total: O(n³)."),

        N.h4("Building the Solution"),
        N.para("Sort. Outer loop fixes i (first element). Inner loop fixes j (second element). Two pointers left=j+1 and right=n-1 find pairs. If sum < target, left++. If sum > target, right--. If sum == target, record and skip duplicates. The j dedup guard uses j > i+1 (not j > 0) because j resets to i+1 each outer iteration."),

        N.callout("Analogy: Think of it as 3Sum applied twice. 3Sum fixes one element and two-pointers the rest. 4Sum fixes two elements and two-pointers the rest. The pattern extends to kSum by fixing k-2 elements.", "🧠", "blue_background"),
    ]),

    N.h3("Code"),
    N.code(SOLUTION1_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), " — Sort in-place in O(n log n). This is the foundational step: equal values become adjacent (dedup), smaller values move left (enables two-pointer logic)."])),
    N.para(N.rich([("for i in range(n - 3)", {"code": True}), " — Fix the first element. Stop at n-4 because we need at least 3 more elements after i."])),
    N.para(N.rich([("if i > 0 and nums[i] == nums[i-1]: continue", {"code": True}), " — Skip duplicate i values. We've already explored all quadruplets starting with this same value in the previous iteration."])),
    N.para(N.rich([("if nums[i] * 4 > target: break", {"code": True}), " — Pruning: the smallest possible 4-sum using this i (nums[i] four times) already exceeds target. Since the array is sorted, all future i values will be even larger — break the outer loop entirely."])),
    N.para(N.rich([("for j in range(i+1, n-2)", {"code": True}), " — Fix the second element. Stop at n-3 because we need at least 2 elements after j for left and right."])),
    N.para(N.rich([("if j > i+1 and nums[j] == nums[j-1]: continue", {"code": True}), " — Skip duplicate j. Guard is j > i+1 (not j > 0!) because j resets to i+1 each outer iteration — using j > 0 would incorrectly skip valid quadruplets when nums[i+1] == nums[i]."])),
    N.para(N.rich([("left, right = j+1, n-1", {"code": True}), " — Initialise two pointers on the unseen suffix nums[j+1..n-1]."])),
    N.para(N.rich([("s = nums[i]+nums[j]+nums[left]+nums[right]", {"code": True}), " — Compute the current 4-element sum."])),
    N.para(N.rich([("if s == target:", {"code": True}), " — Hit! Record the quadruplet, skip duplicates at both ends, then advance both pointers."])),
    N.para(N.rich([("while left<right and nums[left]==nums[left+1]: left+=1", {"code": True}), " — Skip over consecutive equal values at left (after a hit) to avoid duplicate quadruplets."])),
    N.para(N.rich([("left += 1; right -= 1", {"code": True}), " — After skipping dups, advance each pointer once more to land on a genuinely new value."])),
    N.para(N.rich([("elif s < target: left += 1", {"code": True}), " — Sum too small: pick a larger left element to increase it."])),
    N.para(N.rich([("else: right -= 1", {"code": True}), " — Sum too large: pick a smaller right element to decrease it."])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────
SOLUTION2_CODE = '''\
def fourSum_brute(nums: list[int], target: int) -> list[list[int]]:
    n = len(nums)
    seen, res = set(), []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    if nums[a] + nums[b] + nums[c] + nums[d] == target:
                        quad = tuple(sorted([nums[a], nums[b], nums[c], nums[d]]))
                        if quad not in seen:
                            seen.add(quad)
                            res.append(list(quad))
    return res
'''

blocks += [
    N.h2("Solution 2 — Brute Force (for understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every combination of 4 indices. Use a set of sorted tuples to avoid duplicates."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n⁴) time and O(n) space for the seen set. For n=200, it requires 1.6 billion iterations. Useful for verifying correctness but far too slow for any real input."),
        N.h4("The Key Observation"),
        N.para("The brute force IS correct — it just doesn't use any structure in the problem. The optimised approach exploits sorting to avoid redundant comparisons."),
        N.h4("Building the Solution"),
        N.para("Four nested loops over distinct indices a < b < c < d. If their sum equals target, sort the tuple and insert it into a seen set to deduplicate. Collect results."),
    ]),

    N.h3("Code"),
    N.code(SOLUTION2_CODE),

    N.h3("Line by Line"),
    N.para(N.rich([("seen, res = set(), []", {"code": True}), " — seen holds sorted tuples to eliminate duplicates; res is the output."])),
    N.para(N.rich([("for a in range(n):", {"code": True}), " — First element index."])),
    N.para(N.rich([("for b in range(a+1, n):", {"code": True}), " — Second element index (strictly after a)."])),
    N.para(N.rich([("for c, d:", {"code": True}), " — Third and fourth indices similarly constrained. Together these four loops enumerate all C(n,4) combinations."])),
    N.para(N.rich([("quad = tuple(sorted(...))", {"code": True}), " — Sort the tuple so that [-1,0,1,0] and [-1,0,0,1] produce the same key in the set."])),
    N.para(N.rich([("if quad not in seen:", {"code": True}), " — O(1) average hash set lookup prevents duplicate output."])),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n⁴)", "O(n)", "n=200 → 1.6B ops; use only for verification"],
        ["Sort + Two Pointers", "O(n³)", "O(1)", "Optimal; interview answer"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Fix Two + Two Pointers", {})])),
    N.callout(
        "When to recognise this pattern: problem asks for k elements summing to target "
        "(k ≥ 2); uniqueness / no-duplicate output required; array can be sorted; "
        "signal phrases: 'unique quadruplets', 'unique triplets', 'sum equals target'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same kSum technique:"),
    N.bullet(N.rich([("Two Sum (#1)", {"bold": True}), (" (Easy) — Hash map base; Two Sum II uses two pointers on sorted array")])),
    N.bullet(N.rich([("3Sum (#15)", {"bold": True}), (" (Medium) — Fix one element + two pointers; direct predecessor to 4Sum")])),
    N.bullet(N.rich([("3Sum Closest (#16)", {"bold": True}), (" (Medium) — Same structure, track minimum absolute difference from target")])),
    N.bullet(N.rich([("3Sum Smaller (#259)", {"bold": True}), (" (Medium) — Count triplets with sum less than target; two-pointer with count trick")])),
    N.bullet(N.rich([("4Sum II (#454)", {"bold": True}), (" (Medium) — Four separate arrays; hash pairs for O(n²) — different problem!")])),
    N.bullet(N.rich([("Combination Sum (#39)", {"bold": True}), (" (Medium) — Subsets summing to target; backtracking with sorted dedup")])),
    N.bullet(N.rich([("kSum (generic)", {"bold": True}), (" (Hard) — Recursive: fix one, call (k-1)Sum(nums, target-nums[i], k-1, i+1)")])),
    N.para("These problems share the same core technique: sort the array, reduce to lower-dimensional sum problems, use two-pointer convergence on sorted suffixes."),
    N.divider(),
]

# ── Interactive Visual Explainer ────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("4sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
