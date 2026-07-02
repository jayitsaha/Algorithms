"""
gen_maximum_average_subarray_i.py
Notion IN-PLACE rebuild for Maximum Average Subarray I (LeetCode #643).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8102-a667-db800dc73bbe"
SLUG = "maximum_average_subarray_i"

# ── 1) Set / update page properties ──────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=643,
    pattern="Sliding Window",
    subpatterns=["Maintain Window Sum"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Slide a fixed-size window: add incoming element, subtract outgoing; compare sums and divide by k only once.",
    icon="🟢",
)
print("  Properties OK")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
print("Wiping existing blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

# ── 3) Rebuild body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", find the contiguous subarray of length exactly ", {}),
        ("k", {"code": True}),
        (" that has the maximum average value and return this value. "
         "The answer will be accepted if the calculation error is less than 10⁻⁵.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [1, 12, -5, -6, 50, 3], k = 4  →  Output: 12.75000", {"code": True}),
        (".  Window [12, -5, -6, 50] (indices 1–4) has sum=51, average=12.75.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Sliding Window (Interview Pick) ──
SOL1_CODE = """\
def findMaxAverage(nums: list, k: int) -> float:
    window_sum = sum(nums[:k])            # O(k) setup: sum the first window
    max_sum = window_sum                  # initialize best to first window
    for i in range(k, len(nums)):        # i = new right edge entering window
        window_sum += nums[i] - nums[i - k]   # add incoming, subtract outgoing
        max_sum = max(max_sum, window_sum)     # track best window sum
    return max_sum / k                    # divide once at the end
"""

blocks += [
    N.h2("Solution 1 — Fixed Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to examine every contiguous subarray of length exactly k and find the one with the "
               "highest average. Since k is fixed, maximizing average = maximizing sum (dividing by the same k "
               "preserves the ordering of candidates)."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: for each of the n−k+1 starting positions, sum the next k elements and "
               "compute the average. This is O(k) work per window and O(n·k) total — for n=100,000 and k=50,000 "
               "that is 5 billion operations. TLE on any reasonably-sized input."),
        N.h4("The Key Observation"),
        N.para("Adjacent windows of size k share exactly k−1 elements. Window [i..i+k-1] and window [i+1..i+k] "
               "differ only in: one element leaves on the left (nums[i]) and one element enters on the right "
               "(nums[i+k]). We already have the sum of the old window — why recompute those k−1 shared elements?"),
        N.h4("Building the Solution"),
        N.para("Maintain a running window_sum. Start with the first window's sum. Then for each new right edge i "
               "(from k to n−1): window_sum += nums[i] − nums[i−k]. One addition and one subtraction per step — "
               "O(1). Track max_sum. Return max_sum/k at the very end (divide once, never inside the loop)."),
        N.callout(
            "Analogy: imagine a train of k cars. As the train moves forward one stop, the last car detaches "
            "from the rear and a new car attaches to the front. The 'train weight' updates in O(1) — you don't "
            "re-weigh every car.",
            "🚂", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("window_sum = sum(nums[:k])", {"code": True}),
        ("  — O(k) one-time cost. Sums the first k elements to initialize the window. "
         "This is the only O(k) operation in the entire algorithm.", {}),
    ])),
    N.para(N.rich([
        ("max_sum = window_sum", {"code": True}),
        ("  — The first window is our initial best. We'll only update this when a larger sum is found.", {}),
    ])),
    N.para(N.rich([
        ("for i in range(k, len(nums)):", {"code": True}),
        ("  — i is the index of the new element entering from the right. The window at step i spans "
         "[i-k+1, i]. There are n−k such iterations.", {}),
    ])),
    N.para(N.rich([
        ("window_sum += nums[i] - nums[i - k]", {"code": True}),
        ("  — Slide the window: add nums[i] (entering right edge), subtract nums[i-k] (the element "
         "that just left the left edge). The outgoing index i-k is exactly k positions behind i.", {}),
    ])),
    N.para(N.rich([
        ("max_sum = max(max_sum, window_sum)", {"code": True}),
        ("  — If this new window beats our best, update max_sum. We compare sums, not averages, "
         "because dividing by k is monotone — it doesn't change which sum is larger.", {}),
    ])),
    N.para(N.rich([
        ("return max_sum / k", {"code": True}),
        ("  — Convert the best sum to an average. Only one floating-point division in the entire "
         "function, reducing rounding error and improving clarity.", {}),
    ])),
    N.callout(
        "Warning: A common mistake is using nums[i-k+1] as the outgoing element instead of nums[i-k]. "
        "When the right edge is at i, the window is [i-k+1, i], so the element that left is at i-k "
        "(one step further left than the new left boundary). Drawing the window before coding prevents this.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
SOL2_CODE = """\
def findMaxAverage_brute(nums: list, k: int) -> float:
    max_avg = float('-inf')                      # handles all-negative inputs
    for i in range(len(nums) - k + 1):          # every valid window start
        window_avg = sum(nums[i:i + k]) / k      # O(k) recomputation
        max_avg = max(max_avg, window_avg)
    return max_avg                               # O(n * k) total
"""

blocks += [
    N.h2("Solution 2 — Brute Force"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly check every possible window. For each starting index, sum k elements and compute average."),
        N.h4("What Doesn't Work"),
        N.para("This approach IS correct, but too slow. For n=100,000 and k=50,000 it performs 5 billion "
               "operations, causing TLE on LeetCode. Use only to verify the optimal on small test cases."),
        N.h4("The Key Observation"),
        N.para("This brute force has redundant work — it re-sums shared elements between adjacent windows. "
               "Recognizing this redundancy is exactly what motivates the sliding window optimization in Solution 1."),
        N.h4("Building the Solution"),
        N.para("Iterate over all starting positions i in [0, n−k]. For each i, slice nums[i:i+k], sum it, "
               "divide by k, and compare to max_avg. Return max_avg. O(n·k) time, O(k) for the slice."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("max_avg = float('-inf')", {"code": True}),
        ("  — Initialize to negative infinity so any valid average (including all-negative arrays) beats it.", {}),
    ])),
    N.para(N.rich([
        ("for i in range(len(nums) - k + 1):", {"code": True}),
        ("  — Exactly n−k+1 starting positions. If i goes beyond n−k, the window would exceed the array.", {}),
    ])),
    N.para(N.rich([
        ("window_avg = sum(nums[i:i + k]) / k", {"code": True}),
        ("  — Recomputes the full window sum from scratch every time — O(k) work. "
         "This is the bottleneck that the sliding window eliminates.", {}),
    ])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n·k)", "O(k)", "Correct but TLE on large inputs"],
        ["Sliding Window (optimal)", "O(n)", "O(1)", "O(k) init + O(1) × (n−k) slides"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Maintain Window Sum", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'contiguous subarray of exactly k elements' — fixed window size; "
        "(2) 'maximum/minimum aggregate over every window' — track running best; "
        "(3) k is given as a parameter (not derived from data) — window never resizes; "
        "(4) you notice adjacent windows share k−1 elements — O(1) slide is possible.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
related = [
    ("Maximum Sum of Distinct Subarrays With Length K", "Medium", "Fixed window + distinct-element set constraint (#2461)"),
    ("Sliding Window Maximum", "Hard", "Fixed window max via monotonic deque for O(1) per step (#239)"),
    ("Find All Anagrams in a String", "Medium", "Fixed window with character-frequency matching (#438)"),
    ("Maximum Average Subarray II", "Hard", "Variable window (length ≥ k); binary search on average + prefix sums (#644)"),
    ("Grumpy Bookstore Owner", "Medium", "Fixed window to find best bonus interval of size minutes (#1052)"),
    ("Contains Duplicate II", "Easy", "Fixed window of size k; check for duplicate within distance (#219)"),
    ("Subarray Product Less Than K", "Medium", "Variable window — shrink when product condition breaks (#713)"),
]

blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Maintain Window Sum / Fixed Sliding Window technique:"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {}),
    ])))
blocks += [
    N.para("These problems share the core technique: maintain a running aggregate over a fixed-size window, "
           "updating it in O(1) per step by adding the new right element and removing the old left element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.4 "
              "(Sliding Window — Fixed Size / Maintain Window Sum)", "📚", "gray_background"),
]

# ── Interactive Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
