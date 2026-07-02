"""
Notion update script for: Squares of a Sorted Array (LC #977)
Notion page ID: 39193418-809c-8130-843e-c7f4a27799f4
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8130-843e-c7f4a27799f4"

# ── 1) Update properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=977,
    pattern="Two Pointers",
    subpatterns=["Opposite Direction (Abs Compare)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Largest squared value is always at one of the two ends; fill result from back to front.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ───────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" sorted in non-decreasing order, return ", {}),
        ("an array of the squares of each number", {"bold": True}),
        (", also sorted in non-decreasing order.", {})
    ])),
    N.para("Example 1: nums = [-4,-1,0,3,10]  →  [0,1,9,16,100]"),
    N.para("Example 2: nums = [-7,-3,2,3,11]  →  [4,9,9,49,121]"),
    N.para("Constraints: 1 <= nums.length <= 10^4, -10^4 <= nums[i] <= 10^4, nums is sorted in non-decreasing order."),
    N.divider(),
]

# ── Solution 1 — Two Pointers (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Two Pointers, Fill from Back (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the squares of a sorted array, sorted. Squaring changes the sign of negatives, so the simple sort-the-squares approach is O(n log n) and ignores the fact that the input is already sorted. Can we exploit the structure of the input to do it in one O(n) pass?"),
        N.h4("What Doesn't Work"),
        N.para("Squaring in-place and then re-sorting is O(n log n). It discards the existing sorted order. We paid nothing to get sorted input — we should get something back. Also, trying to fill the output from the front requires finding the minimum squared value first, which is hard without scanning everything (the minimum is hidden somewhere near zero in the middle)."),
        N.h4("The Key Observation"),
        N.para("In a sorted array, the largest absolute value is always at one of the two ends — the leftmost element is the most negative (largest abs value on the left), the rightmost is the most positive. So the largest square is always at nums[left] or nums[right]. We can exploit this by filling the output from back to front: always pick the max of the two ends and place it at the current rightmost unfilled slot."),
        N.h4("Building the Solution"),
        N.para("Use three pointers: left = 0, right = n-1 (scanning input), write = n-1 (back of output). Each step: compute ls = nums[left]², rs = nums[right]². If ls >= rs, place ls at result[write] and advance left. Otherwise place rs and decrement right. Always decrement write. When left > right, all n elements are placed."),
        N.callout("Analogy: Think of the negatives (reversed) and the positives as two sorted descending lists of absolute values. Merging two descending lists by always picking the larger head — placed at the back of the result — is the classic merge pattern, applied here implicitly.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def sortedSquares(nums):\n"
        "    n = len(nums)\n"
        "    result = [0] * n                     # pre-allocate output\n"
        "    left, right, write = 0, n - 1, n - 1 # three pointers\n"
        "    while left <= right:\n"
        "        ls = nums[left] ** 2\n"
        "        rs = nums[right] ** 2\n"
        "        if ls >= rs:\n"
        "            result[write] = ls\n"
        "            left += 1\n"
        "        else:\n"
        "            result[write] = rs\n"
        "            right -= 1\n"
        "        write -= 1                        # always move write backward\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(nums)", {"code": True}), " — cache length; used multiple times inside the loop."]), ),
    N.para(N.rich([("result = [0] * n", {"code": True}), " — pre-allocate the output array of the same size; we will overwrite every slot."]), ),
    N.para(N.rich([("left, right, write = 0, n-1, n-1", {"code": True}), " — left and right scan the input from both ends; write fills the output from the rightmost slot backward."]), ),
    N.para(N.rich([("while left <= right:", {"code": True}), " — loop runs exactly n times, once per element. When left crosses right, all elements consumed."]), ),
    N.para(N.rich([("ls = nums[left]**2", {"code": True}), " — square of the leftmost remaining element (candidate for largest on the left)."]), ),
    N.para(N.rich([("rs = nums[right]**2", {"code": True}), " — square of the rightmost remaining element (candidate for largest overall)."]), ),
    N.para(N.rich([("if ls >= rs:", {"code": True}), " — left square wins (ties go to left by convention — either choice is correct)."]), ),
    N.para(N.rich([("result[write] = ls", {"code": True}), " — place the larger square at the current back position."]), ),
    N.para(N.rich([("left += 1", {"code": True}), " — consume the left element; shrink the window from the left."]), ),
    N.para(N.rich([("result[write] = rs; right -= 1", {"code": True}), " — right square wins: place it and shrink the window from the right."]), ),
    N.para(N.rich([("write -= 1", {"code": True}), " — always move the write cursor one slot toward the front — runs after every placement."]), ),
    N.divider(),
]

# ── Solution 2 — Naïve sort ──
blocks += [
    N.h2("Solution 2 — Square and Sort (Simpler, O(n log n))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Just do what the problem says literally: square every number, then sort the result."),
        N.h4("What Doesn't Work"),
        N.para("Nothing 'doesn't work' here — this approach is correct. It is simply suboptimal. It throws away the fact that nums is already sorted and uses an O(n log n) sort when O(n) is achievable."),
        N.h4("The Key Observation"),
        N.para("sorted() on a generator of squares is the Pythonic one-liner. Propose this first in an interview to show you can solve the problem, then optimize to two pointers."),
        N.h4("Building the Solution"),
        N.para("One line: return sorted(x*x for x in nums). Python's sort is Timsort — O(n log n) in the worst case, but highly optimized in practice."),
    ]),
    N.h3("Code"),
    N.code("def sortedSquares(nums):\n    return sorted(x * x for x in nums)"),
    N.h3("Line by Line"),
    N.para(N.rich([("x * x for x in nums", {"code": True}), " — generator expression: lazily produces each square without building a full list first."]), ),
    N.para(N.rich([("sorted(...)", {"code": True}), " — Timsort over the generator, returns a new sorted list. O(n log n) time, O(n) space."]), ),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Two Pointers (Optimal)", "O(n)", "O(n)", "Single pass; O(n) output is unavoidable"],
        ["Square and Sort", "O(n log n)", "O(n)", "Simple code; ignores sorted input"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Two Pointers"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Opposite Direction (Abs Compare)"])),
    N.callout(
        "When to recognize this pattern: sorted input, ask for sorted output of a transformation; "
        "largest value is always at one of the two ends; merging two implicit sorted sequences "
        "(negatives reversed + positives). Key signals: 'sorted array', 'squares', 'absolute value'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (opposite-direction two pointers):"),
    N.bullet(N.rich([("Two Sum II – Input Array is Sorted", {"bold": True}), " (Medium) — left+right converge until they sum to target (#167)"])),
    N.bullet(N.rich([("Merge Sorted Array", {"bold": True}), " (Easy) — fill from back using two read pointers on two sorted arrays (#88)"])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), " (Medium) — opposite pointers, always advance the shorter side to maximize area (#11)"])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), " (Easy) — left/right converge, check character equality (#125)"])),
    N.bullet(N.rich([("3Sum", {"bold": True}), " (Medium) — fix one element, opposite two pointers on the sorted remainder (#15)"])),
    N.bullet(N.rich([("Sort Transformed Array", {"bold": True}), " (Medium) — same fill-from-back idea for a quadratic transformation (#360)"])),
    N.bullet(N.rich([("Reverse String", {"bold": True}), " (Easy) — swap chars with opposing pointers; prototypical opposite-direction example (#344)"])),
    N.para("These problems all share the same insight: the boundary elements (left/right extremes) are the most informative at each step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.2 (Two Pointers Pattern). Sub-pattern: Opposite Direction (Abs Compare).", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("squares_of_a_sorted_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
