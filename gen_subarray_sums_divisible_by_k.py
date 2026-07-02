"""
gen_subarray_sums_divisible_by_k.py
Regenerate Notion page for LeetCode #974 — Subarray Sums Divisible by K
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8176-a2b8-d8346483c76a"
SLUG = "subarray_sums_divisible_by_k"

print(f"[1/4] Setting properties on {PAGE_ID} ...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=974,
    pattern="Prefix Sum",
    subpatterns=["Prefix Sum + Modulo + Hash Map"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Two prefix sums with same remainder mod k mean the subarray between them is divisible by k; seed seen={0:1} to handle subarrays starting at index 0.",
    icon="🟡"
)
print("   Properties set OK.")

print(f"[2/4] Wiping existing page body ...")
wiped = N.wipe_page(PAGE_ID)
print(f"   Wiped {wiped} blocks.")

print(f"[3/4] Building and appending blocks ...")

SOLUTION_1_CODE = """def subarraysDivByK(nums: list[int], k: int) -> int:
    seen = {0: 1}           # seed: virtual prefix sum=0 before start
    rem, count = 0, 0       # rem = running prefix remainder, count = answer
    for x in nums:
        rem = (rem + x) % k             # extend prefix, keep remainder only
        count += seen.get(rem, 0)       # prior same-remainder positions = new subarrays
        seen[rem] = seen.get(rem, 0) + 1  # record this position's remainder
    return count"""

SOLUTION_2_CODE = """def subarraysDivByK_brute(nums: list[int], k: int) -> int:
    n, count = len(nums), 0
    for i in range(n):          # start index
        total = 0
        for j in range(i, n):  # extend subarray
            total += nums[j]
            if total % k == 0:
                count += 1
    return count"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "), ("nums", {"code": True}),
        (" and an integer "), ("k", {"code": True}),
        (", return the number of non-empty subarrays that have a sum divisible by "), ("k", {"code": True}), (".\n\n"),
        ("Constraints: 1 <= nums.length <= 30,000  |  -10,000 <= nums[i] <= 10,000  |  2 <= k <= 10,000. "
         "The array can contain negative integers, which requires careful handling of Python vs C++ modulo semantics.")
    ])),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Prefix Sum + Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count pairs (j, i) where nums[j+1..i] sums to a multiple of k. "
               "Restate using prefix sums: sum(j+1..i) = prefix[i] - prefix[j]. "
               "For this to be divisible by k: (prefix[i] - prefix[j]) % k == 0, "
               "which is equivalent to prefix[i] % k == prefix[j] % k. "
               "So the problem becomes: for each index i, how many earlier indices j share the same prefix-sum remainder?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all O(n^2) pairs — for n=30,000 that is 900 million operations, giving TLE. "
               "Even with prefix sums precomputed in an array, checking all pairs of same-remainder indices is still O(n^2). "
               "We need a way to count matching remainder indices without visiting each one."),
        N.h4("The Key Observation"),
        N.para("The math identity (prefix[i] - prefix[j]) % k == 0 <=> prefix[i] % k == prefix[j] % k "
               "means we only need to group prefix positions by their remainder mod k. "
               "When we reach position i with remainder r, every prior position with remainder r "
               "contributes exactly one valid subarray. A hash map counting occurrences of each remainder "
               "gives us this count in O(1) per step — no need to revisit prior positions at all."),
        N.h4("Building the Solution"),
        N.para("1. Seed seen = {0: 1} — the virtual position before index 0 has prefix sum 0, remainder 0. "
               "This allows subarrays starting from index 0 to be counted when we later hit rem=0.\n"
               "2. Scan each element x. Update rem = (rem + x) % k.\n"
               "3. Add seen.get(rem, 0) to count — these are the prior same-remainder positions.\n"
               "4. Then (after counting!) record: seen[rem] = seen.get(rem, 0) + 1.\n"
               "5. Return count. Each step is O(1), total time O(n), space O(k)."),
        N.callout(
            "Analogy: Think of remainder classes as colour lanes on a highway. All prefix sums "
            "with the same colour belong to the same lane. Any two positions in the same lane form "
            "a valid subarray between them. The hash map counts how many lane-mates we've already passed.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = {0: 1}", {"code": True}),
                   " — Seed the hash map. The virtual prefix sum before index 0 is 0, remainder 0. "
                   "Without this, subarrays starting at index 0 would never be counted."])),
    N.para(N.rich([("rem, count = 0, 0", {"code": True}),
                   " — rem tracks the running prefix-sum modulo k; count is our running answer."])),
    N.para(N.rich([("for x in nums:", {"code": True}),
                   " — Single O(n) pass. We never need to go back or look ahead."])),
    N.para(N.rich([("rem = (rem + x) % k", {"code": True}),
                   " — Extend prefix sum by x, keep only the remainder. Python % always returns non-negative (even for negative x). In C++/Java use: ((rem + x) % k + k) % k."])),
    N.para(N.rich([("count += seen.get(rem, 0)", {"code": True}),
                   " — Every prior position with this same remainder forms a valid subarray with the current position. Defaults to 0 if this remainder is new."])),
    N.para(N.rich([("seen[rem] = seen.get(rem, 0) + 1", {"code": True}),
                   " — Record this position AFTER counting. If you swap order (record before count), you'd count the current position as its own prior match — an off-by-one bug."])),
    N.para(N.rich([("return count", {"code": True}),
                   " — All valid subarrays have been counted. Return the total."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Brute Force (O(n^2), for understanding only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading: for every pair (i, j) with i <= j, compute sum(nums[i..j]) and check if it is divisible by k. Enumerate all subarrays."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n^2) time. For n=30,000 the constraint implies roughly 900 million iterations, which will TLE on any platform with a 2-second time limit."),
        N.h4("The Key Observation"),
        N.para("Even in brute force, accumulate the inner sum incrementally (add nums[j] at each inner step) rather than re-computing from scratch. This avoids an O(n^3) approach but is still O(n^2)."),
        N.h4("Building the Solution"),
        N.para("Outer loop over start i. Inner loop extends j, accumulating total. When total % k == 0, count += 1. Simple, correct, but too slow for production constraints."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — Try every possible starting index i."])),
    N.para(N.rich([("total = 0", {"code": True}), " — Reset running sum for each new starting position."])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), " — Extend subarray from start i to end j."])),
    N.para(N.rich([("total += nums[j]", {"code": True}), " — Add current element — O(1) per step (no re-summation from i each time)."])),
    N.para(N.rich([("if total % k == 0:", {"code": True}), " — Check divisibility directly."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n^2)", "O(1)"],
        ["Prefix Sum + Hash Map (optimal)", "O(n)", "O(min(n, k))"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Prefix Sum (Array Manipulation — Section 1.3)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Prefix Sum + Modulo + Hash Map"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count subarrays' (not find) with a sum condition\n"
        "• Condition involves divisibility by k or sum modulo k\n"
        "• Array may contain negative numbers\n"
        "• These three signals together uniquely identify this sub-pattern.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Prefix Sum + Hash Map / Modulo):"),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), " (Medium) — Exact target instead of divisibility; prefix hash map of exact sums rather than remainders (#560)"])),
    N.bullet(N.rich([("Continuous Subarray Sum", {"bold": True}), " (Medium) — Same divisibility by k, but length must be >= 2; need earliest-index map (#523)"])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), " (Hard) — Count prefix pairs where difference is in [lower, upper] range; merge sort or BIT (#327)"])),
    N.bullet(N.rich([("Find Pivot Index", {"bold": True}), " (Easy) — Prefix + suffix sums; same prefix-accumulation idea (#724)"])),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), " (Easy) — Build prefix array once, O(1) per query (#303)"])),
    N.bullet(N.rich([("Subarray Sums Divisible by K (variant)", {"bold": True}), " — What if k=1? Every subarray qualifies. What if k > sum of entire array? Only whole-array subarrays can match."])),
    N.para("These problems share the same core technique: prefix sums + a hash map that groups positions by a property of their prefix sum to enable O(1) counting per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 (Array Manipulation -> Prefix Sum Pattern). Sub-Pattern: Prefix Sum + Modulo + Hash Map.", "📚", "gray_background"),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"   Appended blocks (total block defs: {len(blocks)}).")
print(f"[4/4] Notion update complete.")
print(f"NOTION OK {PAGE_ID}")
