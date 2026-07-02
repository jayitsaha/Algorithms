"""
Notion update script for LeetCode #1838 — Frequency of the Most Frequent Element
Pattern: Sliding Window | Sub-Pattern: Sort + Window Sum Check
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-813d-8933-ffa04089ddd9"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1838,
    pattern="Sliding Window",
    subpatterns=["Sort + Window Sum Check"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort so target = nums[right]; cost = target*size - window_sum; shrink when cost > k.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing thin content ──────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("The frequency of an element is the number of times it occurs in an array. "
         "You have an array "), ("nums", {"code": True}),
        (" and an integer "), ("k", {"code": True}),
        (". In one operation, you can choose an index of "), ("nums", {"code": True}),
        (" and increment the element at that index by "), ("1", {"code": True}),
        (". Return the maximum possible frequency of an element after performing at most "),
        ("k", {"code": True}), (" operations.")
    ])),
    N.callout(
        N.rich([
            ("Example: "), ("nums = [1, 2, 4], k = 5", {"code": True}),
            (" → Answer: "), ("3", {"bold": True}),
            (". Raise 1→4 (cost 3) and 2→4 (cost 2). Total cost = 5 ≤ k. All three become 4.")
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Sort + Sliding Window (Optimal) ───────────────────────────────
blocks += [
    N.h2("Solution 1 — Sort + Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want to pick a group of elements and raise them all to the same value "
            "using at most k total increments. Maximize the size of this group."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: for every pair (target element, subset of elements to raise), "
            "compute cost and check if ≤ k. This is O(2^n) subsets — completely infeasible. "
            "Even the smarter O(n²) approach (fix target, scan left) is too slow for n=10^5."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Since we can ONLY increment (never decrement), the target value for any group "
            "must be its MAXIMUM element — everything else needs to be raised UP to it. "
            "After sorting, the maximum of any window is always nums[right]. "
            "The cost to equalize a window = target × size − window_sum. "
            "This is O(1) with a running sum!"
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort the array (now target = nums[right] for any window). "
            "2. Use a sliding window: expand right, compute cost, shrink left when cost > k. "
            "3. After each right expansion (with shrinks), record the window size. "
            "4. The window invariant — cost ≤ k — is maintained at all times."
        ),
        N.callout(
            "Analogy: You're filling glasses of water to the brim. "
            "The 'tallest glass' sets the level. Shorter glasses cost (tall − short) extra water to fill. "
            "Sort by height, then slide a window: as long as total extra water needed ≤ k, expand the window.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def maxFrequency(nums: list, k: int) -> int:\n"
        "    nums.sort()          # Sort: nums[right] is always the target\n"
        "    left = 0\n"
        "    window_sum = 0\n"
        "    ans = 0\n"
        "    for right in range(len(nums)):\n"
        "        window_sum += nums[right]\n"
        "        # cost = ops needed to raise all elements to nums[right]\n"
        "        while nums[right] * (right - left + 1) - window_sum > k:\n"
        "            window_sum -= nums[left]\n"
        "            left += 1\n"
        "        ans = max(ans, right - left + 1)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), " — Sort ascending. After this, for any window [left, right], nums[right] is the largest element (our target). No element to the left ever needs to decrease."])),
    N.para(N.rich([("left = 0; window_sum = 0; ans = 0", {"code": True}), " — Initialize: left boundary, running window sum (for O(1) cost check), and best answer."])),
    N.para(N.rich([("window_sum += nums[right]", {"code": True}), " — Expand window to include nums[right]. Update running sum in O(1)."])),
    N.para(N.rich([("while nums[right]*(right-left+1) - window_sum > k:", {"code": True}), " — Compute cost. The formula target×size−sum gives the total increments needed to raise every element in the window to nums[right]. If over budget, shrink."])),
    N.para(N.rich([("window_sum -= nums[left]; left += 1", {"code": True}), " — Remove leftmost element from window. This reduces cost by (nums[right] − nums[left]) — the largest per-element cost in the sorted window."])),
    N.para(N.rich([("ans = max(ans, right - left + 1)", {"code": True}), " — After the shrink loop, the window is guaranteed valid (cost ≤ k). Record its size as a candidate answer."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Fix each element as the target, then find how many elements to its left can be raised to that target within budget k."),
        N.h4("What Doesn't Work"),
        N.para("This O(n²) solution is correct but times out for n=10^5 (LeetCode limit). It exists to build intuition for the sliding window optimization."),
        N.h4("The Key Observation"),
        N.para("For each target index i, scan backwards: accumulate cost (target − nums[j]) until over budget. The brute force inner loop is what the sliding window eliminates by reusing previous computation."),
        N.h4("Building the Solution"),
        N.para("Sort. For each i, walk j from i−1 backwards. Sum up costs. Stop when cumulative cost > k."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxFrequency_brute(nums: list, k: int) -> int:\n"
        "    nums.sort()\n"
        "    ans = 1\n"
        "    for i in range(len(nums)):\n"
        "        target = nums[i]\n"
        "        ops = 0\n"
        "        for j in range(i - 1, -1, -1):\n"
        "            ops += target - nums[j]\n"
        "            if ops > k:\n"
        "                break\n"
        "            ans = max(ans, i - j + 1)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(nums)):", {"code": True}), " — Each index i is considered as the target frequency value."])),
    N.para(N.rich([("ops += target - nums[j]", {"code": True}), " — Cost to raise nums[j] to target. Since sorted, target ≥ nums[j] always."])),
    N.para(N.rich([("if ops > k: break", {"code": True}), " — Once cumulative cost exceeds budget, no further elements to the left can be added (they'd only cost more)."])),
    N.para(N.rich([("ans = max(ans, i - j + 1)", {"code": True}), " — Group [j..i] is valid; its size = i − j + 1."])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Sort + Sliding Window (optimal)", "O(n log n)", "O(1)"],
        ["Binary Search on Answer", "O(n log² n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Sort + Window Sum Check (DSA Guide Section 1.5)"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) 'Maximize frequency/count with bounded modifications'. "
             "(2) Only increments or only decrements allowed (asymmetric). "
             "(3) Cost to equalize a group = target × size − sum (linear formula). "
             "(4) After sorting, optimal group is always a contiguous window.")
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Window Sum Check technique:"),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), " (Medium) — Window where (size − max_char_freq) ≤ k; structurally identical invariant (#424)"])),
    N.bullet(N.rich([("Max Consecutive Ones III", {"bold": True}), " (Medium) — Count zeros in window ≤ k; same expand/shrink template (#1004)"])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), " (Medium) — Shortest window with sum ≥ target; dynamic sliding window (#209)"])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), " (Medium) — Count valid windows with product constraint; sliding window (#713)"])),
    N.bullet(N.rich([("Maximum Average Subarray II", {"bold": True}), " (Hard) — Binary search on average + prefix sums; generalizes window sum (#644)"])),
    N.bullet(N.rich([("Minimum Number of Operations to Make Array Continuous", {"bold": True}), " (Hard) — Sort + window to find longest range ≤ n−1; same pattern (#2009)"])),
    N.para("These problems share the core technique: sort, then use a window with a running sum to check a budget constraint in O(1) per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 1.5 (Sliding Window — Dynamic Size)", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("frequency_of_the_most_frequent_element")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
