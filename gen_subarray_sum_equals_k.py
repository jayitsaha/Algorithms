"""
gen_subarray_sum_equals_k.py
Regenerates the Notion page for Subarray Sum Equals K (LC #560) in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d9-ae69-e59160f35d33"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=560,
    pattern="Prefix Sum",
    subpatterns=["Prefix Sum + Hash Map"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Any subarray sum = prefix[j] - prefix[i]; store seen prefix sums in a hash map to count in O(n).",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the total number of contiguous subarrays whose sum equals ", {}),
        ("k", {"code": True}),
        (". The array may contain negative integers, zeros, and positive integers. "
         "A subarray is a contiguous non-empty sequence of elements within the array.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ("nums = [1,1,1], k = 2  →  output = 2  (subarrays [1,1] at indices 0..1 and 1..2)\n", {}),
            ("Example 2: ", {"bold": True}),
            ("nums = [1,2,3], k = 3  →  output = 2  (subarrays [3] at index 2 and [1,2] at indices 0..1)", {}),
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force (Nested Loops)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count (i, j) pairs such that nums[i] + nums[i+1] + ... + nums[j] = k. "
               "The most literal translation is to try every possible starting index i and every "
               "possible ending index j ≥ i, computing the sum of each window."),
        N.h4("What Doesn't Work (at Scale)"),
        N.para("This approach is completely correct but scales as O(n²) time — for n=20,000 that's "
               "400 million operations. LeetCode's constraint is n ≤ 20,000, so this will TLE. "
               "We use it to build intuition before deriving the O(n) solution."),
        N.h4("The Key Observation"),
        N.para("For each fixed i, we can extend j one step at a time and maintain a running sum — "
               "no need to recompute from scratch. This keeps the inner loop O(n) instead of O(n²), "
               "making the total O(n²) rather than O(n³)."),
        N.h4("Building the Solution"),
        N.para("Start at each index i. Run j from i to n-1, accumulating nums[j] into current_sum. "
               "Whenever current_sum == k, increment count. Reset current_sum = 0 before each new i."),
        N.callout("Analogy: Like counting how many consecutive chapters of a book total exactly 100 pages "
                  "— you open at each chapter and read forward until you overshoot or hit the target.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def subarraySum_brute(nums: list[int], k: int) -> int:\n"
        "    count = 0\n"
        "    n = len(nums)\n"
        "    for i in range(n):           # start of subarray\n"
        "        curr_sum = 0\n"
        "        for j in range(i, n):   # end of subarray\n"
        "            curr_sum += nums[j]\n"
        "            if curr_sum == k:\n"
        "                count += 1\n"
        "    return count",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = 0", {"code": True}), (" — running total of valid subarrays found.", {})])),
    N.para(N.rich([("for i in range(n)", {"code": True}), (" — outer loop picks the left boundary of the subarray.", {})])),
    N.para(N.rich([("curr_sum = 0", {"code": True}), (" — reset the running sum before each new starting position.", {})])),
    N.para(N.rich([("for j in range(i, n)", {"code": True}), (" — inner loop extends the right boundary one element at a time.", {})])),
    N.para(N.rich([("curr_sum += nums[j]", {"code": True}), (" — accumulate the element; avoids recomputing from i every iteration.", {})])),
    N.para(N.rich([("if curr_sum == k", {"code": True}), (" — if the window [i..j] sums to k, it is a valid subarray; count it.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — total valid subarrays after exhausting all (i, j) pairs.", {})])),
    N.divider(),
]

# ── Solution 2: Prefix Sum + Hash Map (Interview Pick) ────────────────────
blocks += [
    N.h2("Solution 2 — Prefix Sum + Hash Map (Interview Pick) ⭐"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of iterating over subarrays, think in terms of prefix sums. "
               "Define prefix[i] = nums[0] + nums[1] + ... + nums[i]. "
               "The sum of subarray [i..j] = prefix[j] - prefix[i-1]. "
               "We want to count pairs (i, j) where prefix[j] - prefix[i-1] = k, "
               "which rearranges to: prefix[j] - k = prefix[i-1]."),
        N.h4("What Doesn't Work"),
        N.para("Storing the full prefix array and scanning all pairs is still O(n²). "
               "Sliding window fails because nums can contain negatives — shrinking the "
               "left pointer does NOT guarantee the sum decreases. We need a smarter structure."),
        N.h4("The Key Observation — Two Sum in Disguise"),
        N.para("This is exactly the Two Sum pattern! In Two Sum we ask: for each element x, "
               "how many previously seen elements equal (target - x)? Here, for each prefix sum ps, "
               "we ask: how many previously seen prefix sums equal (ps - k)? "
               "A hash map counting occurrences of each prefix sum answers this in O(1) per element."),
        N.h4("Building the Solution"),
        N.para("Seed the map with {0: 1} — this phantom entry represents the prefix sum 'before' "
               "index 0, so subarrays starting at index 0 are handled correctly. "
               "Then iterate: extend prefix_sum by each element, query freq[prefix_sum - k], "
               "add that count to result, then insert prefix_sum into freq. "
               "Querying BEFORE inserting prevents matching the current position with itself."),
        N.callout("Analogy: Imagine a scoreboard that records the running total after each move in a game. "
                  "To find how many 'windows' of moves scored exactly k points, we look back at which "
                  "earlier totals differ from the current total by exactly k. The hash map IS that scoreboard lookup.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Prefix Sum + Complement Lookup"),
    N.para(
        "Origin: The complement lookup trick originates from Two Sum (LC #1, 2011). Applied to prefix sums, "
        "it generalises to counting subarrays with any target sum in O(n) time.\n\n"
        "Core Invariant: At any point in the iteration, freq[v] = the number of indices (including the "
        "phantom -1 boundary) at or before the current index where the prefix sum equals v.\n\n"
        "Why It Works: If prefix[j] = ps and freq[ps - k] = c, then there are exactly c indices i "
        "such that prefix[i] = ps - k, meaning subarray (i+1)..j has sum k. Summing c over all j gives "
        "the total count.\n\n"
        "Critical Ordering: We must read freq[ps - k] BEFORE writing freq[ps]. If we wrote first, "
        "we could match index j with itself (ps - ps = 0 ≠ k in general, but if k=0 and ps=0 it breaks).\n\n"
        "When to Recognize: Any 'count subarrays summing to target' problem where elements can be negative → "
        "prefix sum + hash map. If elements are non-negative and target > 0, sliding window also works."
    ),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict\n\n"
        "def subarraySum(nums: list[int], k: int) -> int:\n"
        "    count = 0\n"
        "    prefix_sum = 0\n"
        "    freq = defaultdict(int)\n"
        "    freq[0] = 1          # phantom boundary: 'before index 0'\n"
        "\n"
        "    for num in nums:\n"
        "        prefix_sum += num                     # extend prefix sum\n"
        "        count += freq[prefix_sum - k]         # how many earlier boundaries give sum k?\n"
        "        freq[prefix_sum] += 1                 # record this prefix sum for future queries\n"
        "\n"
        "    return count",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = 0", {"code": True}), (" — accumulates the number of valid subarrays found.", {})])),
    N.para(N.rich([("prefix_sum = 0", {"code": True}), (" — running sum of all elements seen so far (starts at 0, before any element).", {})])),
    N.para(N.rich([("freq = defaultdict(int)", {"code": True}), (" — maps each prefix sum value to how many times it has appeared.", {})])),
    N.para(N.rich([("freq[0] = 1", {"code": True}), (" — the phantom entry: there is '1 way' to have prefix sum 0 (before the array starts). Without this, subarrays starting at index 0 would never be counted.", {})])),
    N.para(N.rich([("prefix_sum += num", {"code": True}), (" — extend the running prefix sum by the current element.", {})])),
    N.para(N.rich([("count += freq[prefix_sum - k]", {"code": True}),
                   (" — the number of earlier positions where prefix sum equalled (ps - k). Each such position i means subarray (i+1..j) sums to exactly k.", {})])),
    N.para(N.rich([("freq[prefix_sum] += 1", {"code": True}),
                   (" — record the current prefix sum. Done AFTER the lookup to avoid counting the current position as a prior occurrence.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — total valid subarrays.", {})])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",               "Time",   "Space",  "Handles Negatives?"],
        ["Brute Force",            "O(n²)",  "O(1)",   "Yes"],
        ["Prefix Sum + Hash Map",  "O(n)",   "O(n)",   "Yes (best general)"],
    ]),
    N.callout(
        "The O(n) solution is achieved because each element is visited exactly once, and each "
        "hash map operation (lookup + insert) is O(1) amortised. Space is O(n) in the worst case "
        "when all prefix sums are distinct (e.g., strictly increasing array).",
        "⏱️", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum (Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prefix Sum + Hash Map", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to COUNT (not find) subarrays with a specific sum/XOR/product\n"
        "• Elements can be negative (ruling out sliding window)\n"
        "• The phrase 'sum equals k' or 'sum divisible by k' appears\n"
        "• You see 'Two Sum' vibes — find a complement in previously seen values",
        "🔎", "green_background"
    ),
    N.para("Sub-Pattern verified: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.3 (Prefix Sum)."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Prefix Sum + Hash Map technique:"),
    N.bullet(N.rich([("Two Sum", {"bold": True}), (" (Easy) — Blueprint of complement lookup: store seen values, query target - x. Prefix sum is the 2D generalisation. (#1)", {})])),
    N.bullet(N.rich([("Subarray Sums Divisible by K", {"bold": True}), (" (Medium) — Count subarrays where sum mod k = 0; use prefix sum modulo as the hash map key. (#974)", {})])),
    N.bullet(N.rich([("Continuous Subarray Sum", {"bold": True}), (" (Medium) — Subarray sum is a multiple of k; check if prefix mod k repeats. (#523)", {})])),
    N.bullet(N.rich([("Longest Subarray with Sum K", {"bold": True}), (" (Medium) — Maximise length instead of count; store first-seen index per prefix sum. (#325)", {})])),
    N.bullet(N.rich([("Binary Subarrays With Sum", {"bold": True}), (" (Medium) — Binary array, count subarrays with target sum; direct application. (#930)", {})])),
    N.bullet(N.rich([("Count of Range Sum", {"bold": True}), (" (Hard) — Count subarrays with sum in [lower, upper]; requires merge sort on prefix sums. (#327)", {})])),
    N.bullet(N.rich([("Range Sum Query — Immutable", {"bold": True}), (" (Easy) — Precompute prefix sums for O(1) range queries — the foundational technique. (#303)", {})])),
    N.bullet(N.rich([("Number of Subarrays with Bounded Maximum", {"bold": True}), (" (Medium) — Combine prefix sums with range constraints. (#795)", {})])),
    N.para("These problems share the core insight: transform a range-sum question into a complement-lookup question using cumulative sums."),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("subarray_sum_equals_k")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the prefix sum grow, see the hash map fill, and observe exactly when a 'hit' is found.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} blocks to {PAGE_ID}")
