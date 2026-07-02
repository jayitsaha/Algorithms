"""
gen_minimum_size_subarray_sum.py
Regenerate Notion page for LeetCode #209 — Minimum Size Subarray Sum
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ec-95c1-d50fdf78f80e"
SLUG    = "minimum_size_subarray_sum"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=209,
    pattern="Array Manipulation",
    subpatterns=["Shrink When Sum >= Target"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Expand right always; shrink left while sum >= target — all-positive values make this monotonic.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of positive integers ", {}),
        ("nums", {"code": True}),
        (" and a positive integer ", {}),
        ("target", {"code": True}),
        (", return the minimal length of a contiguous subarray of which the sum is greater than or equal to ", {}),
        ("target", {"code": True}),
        (". If there is no such subarray, return ", {}),
        ("0", {"code": True}),
        (" instead.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Sliding Window (Optimal / Interview Pick) ─────────────────────
blocks += [
    N.h2("Solution 1 — Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the shortest contiguous window whose sum reaches target. Think of a physical window you slide across the array — you stretch it to the right to grow the sum, and squeeze it from the left whenever the sum is already large enough."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force O(n²) approach tries every (left, right) pair. For n=10⁵ that's 10¹⁰ operations — exceeds time limits. We need a smarter way to avoid revisiting positions."),
        N.h4("The Key Observation"),
        N.para("All values are positive. This means: extending the window always increases the sum, and shrinking always decreases it. The sum is monotonically dependent on window size. This is the exact property sliding window needs."),
        N.h4("Building the Solution"),
        N.para("Keep a running sum as right sweeps forward. The moment the sum hits target, we've found a valid window — but is it the shortest? Shrink left one step at a time. Since values are positive, each shrink reduces the sum. Keep shrinking while the window is still valid. Each shrink might reveal a shorter answer. Stop shrinking when sum drops below target, then advance right again."),
        N.callout("Analogy: Imagine a rubber band stretched over the array. You pull the right end to reach the target tension. Then you push the left end inward as far as it will go while maintaining at least that tension. The tightest valid stretch for each right position gives the answer.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minSubArrayLen(target: int, nums: List[int]) -> int:\n"
        "    left = 0\n"
        "    curr_sum = 0\n"
        "    min_len = float('inf')\n"
        "    for right in range(len(nums)):\n"
        "        curr_sum += nums[right]\n"
        "        while curr_sum >= target:\n"
        "            min_len = min(min_len, right - left + 1)\n"
        "            curr_sum -= nums[left]\n"
        "            left += 1\n"
        "    return 0 if min_len == float('inf') else min_len"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("left = 0", {"code": True}), (" — Left boundary of the window, starts at the beginning of the array.")])),
    N.para(N.rich([("curr_sum = 0", {"code": True}), (" — Running total of elements inside the current window. Starts at zero since window is empty.")])),
    N.para(N.rich([("min_len = float('inf')", {"code": True}), (" — Best (smallest) valid window length found so far. Infinity signals 'no valid window yet'.")])),
    N.para(N.rich([("for right in range(len(nums)):", {"code": True}), (" — Outer loop: expand the window by advancing the right pointer one step at a time.")])),
    N.para(N.rich([("curr_sum += nums[right]", {"code": True}), (" — Include the element at the right boundary in the running sum.")])),
    N.para(N.rich([("while curr_sum >= target:", {"code": True}), (" — The window sum has reached the target — it's valid. Keep shrinking to find the tightest possible fit.")])),
    N.para(N.rich([("min_len = min(min_len, right - left + 1)", {"code": True}), (" — Record this window's length BEFORE shrinking. The window is valid right now.")])),
    N.para(N.rich([("curr_sum -= nums[left]", {"code": True}), (" — Remove the leftmost element from the running sum to shrink the window.")])),
    N.para(N.rich([("left += 1", {"code": True}), (" — Move left boundary rightward. The window is now one element smaller.")])),
    N.para(N.rich([("return 0 if min_len == float('inf') else min_len", {"code": True}), (" — If min_len never changed, no valid window was found → return 0. Otherwise return the best length.")])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (Mention First in Interview)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest interpretation: try every possible starting point and extend rightward until the sum is enough. Among all valid windows found this way, take the shortest."),
        N.h4("What Doesn't Work"),
        N.para("This approach is O(n²) — for each of n starting positions, we might scan up to n elements. Fine for small n but fails for n=10⁵."),
        N.h4("The Key Observation"),
        N.para("Since all values are positive, once sum >= target for a given left, the shortest valid subarray starting at left is the first right that crosses the threshold. We can break early."),
        N.h4("Building the Solution"),
        N.para("For each left, accumulate from left rightward. Break as soon as sum >= target — that is the shortest window starting at this left. Track the global minimum."),
    ]),
    N.h3("Code"),
    N.code(
        "def minSubArrayLen(target: int, nums: List[int]) -> int:\n"
        "    n, min_len = len(nums), float('inf')\n"
        "    for l in range(n):\n"
        "        total = 0\n"
        "        for r in range(l, n):\n"
        "            total += nums[r]\n"
        "            if total >= target:\n"
        "                min_len = min(min_len, r - l + 1)\n"
        "                break  # No need to extend further from this l\n"
        "    return 0 if min_len == float('inf') else min_len"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for l in range(n):", {"code": True}), (" — Try every possible left boundary.")])),
    N.para(N.rich([("total = 0", {"code": True}), (" — Reset the running sum for each new left position.")])),
    N.para(N.rich([("for r in range(l, n):", {"code": True}), (" — Extend the right boundary from the current left.")])),
    N.para(N.rich([("if total >= target: ... break", {"code": True}), (" — The first r that satisfies the condition gives the shortest window from this l. Break immediately.")])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sliding Window (Optimal)", "O(n)", "O(1)"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Prefix Sum + Binary Search", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Shrink When Sum >= Target (Variable Sliding Window)")])),
    N.callout(
        "When to recognize this pattern: 'contiguous subarray' + 'all positive integers' + "
        "'minimize/maximize window size against a sum threshold' — these three signals together "
        "almost always mean variable sliding window. The positive-only constraint is critical: "
        "without it the monotonic property breaks and sliding window fails.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same shrink-when-valid sliding window technique:"),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), (" (Medium) — Longest window with at most 2 distinct values. Shrink when a third type enters. (#904)")])),
    N.bullet(N.rich([("Minimum Window Substring", {"bold": True}), (" (Hard) — Shrink window once all required characters are covered. (#76)")])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), (" (Medium) — Variable window on product instead of sum; shrink when product >= k. (#713)")])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium) — Shrink when a duplicate enters the window. (#3)")])),
    N.bullet(N.rich([("Maximum Sum Subarray of Size K", {"bold": True}), (" (Easy) — Fixed-size sliding window; simpler variant without shrinking.")])),
    N.bullet(N.rich([("Shortest Subarray with Sum at Least K", {"bold": True}), (" (Hard) — Same problem but with negative numbers. Sliding window breaks; needs monotonic deque. (#862)")])),
    N.bullet(N.rich([("Count Subarrays Where Max Element Appears At Least K Times", {"bold": True}), (" (Medium) — Same shrink structure, different validity condition. (#2962)")])),
    N.para("These problems share the same core template: expand right, shrink left while valid, record the answer."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.4/1.5 Sliding Window (Dynamic) — Subpattern: Shrink When Sum >= Target", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
