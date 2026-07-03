"""
gen_maximum_width_ramp.py
Notion in-place update for: Maximum Width Ramp (LC #962, Medium)
Pattern: Monotonic Stack | Subpattern: Decreasing Stack + Binary Search
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d0-81b0-c917befadb37"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=962,
    pattern="Monotonic Stack",
    subpatterns=["Decreasing Stack + Binary Search"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Build a decreasing stack of candidate left indices, then scan right-to-left greedily popping to find widest ramp.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing body ──────────────────────────────────────────────
print("Wiping page...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ───────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given an integer array nums, a ramp is a pair (i, j) where i < j and nums[i] <= nums[j]. "
    "Return the maximum width j - i of such a ramp, or 0 if no valid ramp exists."
)

SOL1_CODE = """\
def maxWidthRamp(nums: list[int]) -> int:
    n = len(nums)
    # Phase 1: Build decreasing stack of candidate left endpoints
    stack = []
    for i in range(n):
        if not stack or nums[i] < nums[stack[-1]]:
            stack.append(i)
    # Phase 2: Scan j right-to-left, greedily pop matching candidates
    max_width = 0
    for j in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[j]:
            max_width = max(max_width, j - stack.pop())
    return max_width
"""

SOL2_CODE = """\
def maxWidthRamp_brute(nums: list[int]) -> int:
    max_w = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] <= nums[j]:
                max_w = max(max_w, j - i)
    return max_w
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [6, 0, 8, 2, 1, 5]", {"code": True}),
        (" → answer is 4 (ramp from index 1 to index 5, values 0 ≤ 5).")
    ])),
    N.divider(),
]

# ── Solution 1: Optimal ──────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Monotonic Decreasing Stack + Right Scan (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the widest pair (i, j) where i < j and nums[i] <= nums[j]. "
            "O(n²) brute force checks all pairs. We need to prune: which left endpoints can we discard?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force (check all pairs): O(n²) — TLE for n=50,000. "
            "Binary search on the right endpoint alone: we'd need to know which left endpoints are valid for each j — still O(n log n) without further insight on pruning lefts."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Domination principle: if index a < b and nums[a] <= nums[b], then a dominates b as a left endpoint. "
            "Any j that pairs with b (nums[b] <= nums[j]) also pairs with a (nums[a] <= nums[b] <= nums[j]) at wider width j-a > j-b. "
            "So b is useless — we can prune it. Only keep indices where nums[i] is a new left-to-right minimum."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Phase 1: Scan left-to-right and push index i only when nums[i] is strictly less than the current stack top. "
            "This builds a monotonically decreasing stack of values (stored as indices). "
            "Phase 2: Scan j from right to left. For each j, pop stack entries while nums[stack.top] <= nums[j]. "
            "Record j - popped_index as a candidate width. Scanning right-to-left means the first pop for any stack entry "
            "gives the maximum j (widest ramp) for that left endpoint."
        ),
        N.callout(
            "Analogy: Think of the stack as 'launching pads' sorted by height (leftmost = highest value, rightmost = lowest). "
            "Scanning right-to-left, we look for the widest possible landing for each pad. "
            "Once a pad finds its landing (from the right, so widest), it's retired.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(nums)", {"code": True}), " — store length for loop bounds."])),
    N.para(N.rich([("stack = []", {"code": True}), " — will hold INDICES (not values) of candidate left endpoints."])),
    N.para(N.rich([("if not stack or nums[i] < nums[stack[-1]]:", {"code": True}), " — push only when nums[i] is a new strict minimum. Equal values are already dominated by the earlier index."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — store the index so we can compute width = j - i later."])),
    N.para(N.rich([("for j in range(n - 1, -1, -1):", {"code": True}), " — Phase 2: scan right-to-left. Larger j = wider ramp for any matching left."])),
    N.para(N.rich([("while stack and nums[stack[-1]] <= nums[j]:", {"code": True}), " — ramp condition: nums[i] <= nums[j]. Use <= (not <) because equal values form valid ramps."])),
    N.para(N.rich([("max_width = max(max_width, j - stack.pop())", {"code": True}), " — pop index i, compute width j - i, update global max."])),
    N.para(N.rich([("return max_width", {"code": True}), " — 0 if no ramp was ever found (fully decreasing array)."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (O(n²))"),
    N.toggle_h3("💡 Intuition: The Naive Starting Point", [
        N.h4("Reframe the Problem"),
        N.para("Check every pair (i, j) with i < j. If nums[i] <= nums[j], update the max width."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) — correct but slow. Will TLE for n > ~10,000 on LeetCode."),
        N.h4("The Key Observation"),
        N.para("Present this first in an interview to show you understand the problem, then explain how to optimize."),
        N.h4("Building the Solution"),
        N.para("Nested loops: outer i from 0 to n-1, inner j from i+1 to n-1. Check condition, update max."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(nums)):", {"code": True}), " — outer loop over all possible left endpoints."])),
    N.para(N.rich([("for j in range(i + 1, len(nums)):", {"code": True}), " — inner loop: all right endpoints to the right of i."])),
    N.para(N.rich([("if nums[i] <= nums[j]:", {"code": True}), " — ramp condition check."])),
    N.para(N.rich([("max_w = max(max_w, j - i)", {"code": True}), " — update maximum width seen."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²)", "O(1)", "TLE for large n; good interview starting point"],
        ["Monotonic Stack (Optimal)", "O(n)", "O(n)", "Each index pushed/popped at most once; interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Stack"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Decreasing Stack + Binary Search (right-to-left greedy scan)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Maximize j−i subject to a comparison on nums[i] and nums[j]'\n"
        "• 'Widest', 'maximum distance', 'span' + value comparison constraint\n"
        "• O(n²) brute force works but is too slow — need monotone dominance pruning\n"
        "• One direction (right-to-left or left-to-right) always improves the answer for fixed opposite endpoint",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("The 'Decreasing Stack + Binary Search' sub-pattern label is used here per the problem's canonical classification. "
         "The Phase 2 scan is also described as a greedy right-to-left pop (no explicit binary search needed in the O(n) version).",
         {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same monotonic stack technique:"),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — Classic monotonic stack: next greater to the right of each element."])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Monotonic stack: count days until warmer temperature."])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Decreasing monotonic stack to find left/right boundaries."])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Max-left and max-right boundary pairs; can use monotonic stack."])),
    N.bullet(N.rich([("132 Pattern", {"bold": True}), " (Medium) — Monotonic stack tracking min-so-far for a three-index constraint."])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Monotonic deque for max in a moving window (same decreasing structure)."])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — Monotonic deque for sliding window max in DP transitions."])),
    N.para("These problems share the same core insight: maintain a monotone structure to discard dominated candidates, enabling linear-time solutions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Monotonic Stack section.", "📚", "gray_background"),
]

# ── Visual Explainer embed ────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_width_ramp")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print("Appending blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
