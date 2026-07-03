"""
gen_largest_rectangle_in_histogram.py
Notion IN-PLACE update for LeetCode #84 - Largest Rectangle in Histogram
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8165-b944-dcf0a72e1756"

print(f"Updating Notion page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=84,
    pattern="Monotonic Stack",
    subpatterns=["Stack for Left/Right Bounds", "Monotonic Stack: Previous Smaller"],
    tc="O(n)",
    sc="O(n)",
    key_insight="For each bar, its maximum rectangle is bounded by the nearest shorter bar left (new stack top) and right (current i) — found in one pass with a monotonic increasing stack.",
    icon="🔴"
)
print("Properties set OK")

# ── Step 2: Wipe old content ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks")

# ── Step 3: Build body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers "), ("heights", {"code": True}),
        (" representing the histogram's bar heights where the width of each bar is 1, return the area of the largest rectangle in the histogram."),
    ])),
    N.para("Example: heights = [2, 1, 5, 6, 2, 3] → Output: 10 (the rectangle spanning bars at indices 2 and 3, height=5, width=2)."),
    N.divider(),
]

# ── Solution 1: Monotonic Stack (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Monotonic Stack with Sentinel (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of thinking about all O(n²) possible spans, reframe: every optimal rectangle is 'pinned' at the height of some specific bar — the shortest bar in its span. So for each bar i, ask: if I use heights[i] as the rectangle height, what is the maximum width I can extend left and right before hitting a shorter bar? The maximum area for bar i is heights[i] × (right_bound - left_bound - 1)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all (left, right) pairs and computes min(heights[left..right]) × width. With a running minimum, this is O(n²) — too slow for n=100,000. A divide-and-conquer approach (find global min, recurse) gives O(n log n) but is complex to code correctly."),
        N.h4("The Key Observation"),
        N.para("Finding 'previous smaller element' and 'next smaller element' for all bars simultaneously in O(n) is a classic monotonic stack problem. Use an increasing stack: when bar i triggers a pop of bar h, bar i is the next smaller to h's right, and the new stack top after popping is the previous smaller to h's left. Both bounds at once — no second pass needed!"),
        N.h4("Building the Solution"),
        N.para("Maintain a stack of indices with increasing heights. For each bar: if current height < stack top height, pop and compute the rectangle. Repeat until stack is empty or current bar is taller. Then push current index. Add a sentinel bar of height 0 at the end to force-flush remaining bars."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of the stack as a 'skyline waiting room.' Each bar waits in the room until a shorter bar arrives and kicks it out. When kicked out, the bar knows exactly how far it can span: right = the shorter bar that kicked it, left = the next shorter bar still waiting in the room.")]),
            "🏙️", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""\
def largestRectangleArea(heights: list[int]) -> int:
    stack = []       # indices; heights increase bottom→top
    max_area = 0
    n = len(heights)
    for i in range(n + 1):
        h = 0 if i == n else heights[i]  # sentinel at i==n
        while stack and h < heights[stack[-1]]:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            width = i - left - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area"""),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Stack of bar indices. Heights of stacked bars are always increasing (bottom to top). We store indices (not heights) because we need positions to compute width."])),
    N.para(N.rich([("for i in range(n + 1)", {"code": True}), " — Loop one extra iteration to process the sentinel. This simplifies the flush: no separate cleanup loop needed."])),
    N.para(N.rich([("h = 0 if i == n else heights[i]", {"code": True}), " — The virtual sentinel has height 0. Since 0 < any real bar height, it forces all remaining bars in the stack to be popped and computed."])),
    N.para(N.rich([("while stack and h < heights[stack[-1]]", {"code": True}), " — While current bar is shorter than the stack top: the top bar has found its right boundary (current i). Pop it and compute its rectangle."])),
    N.para(N.rich([("height = heights[stack.pop()]", {"code": True}), " — Pop the top index. Its height becomes the rectangle's height (the limiting bar)."])),
    N.para(N.rich([("left = stack[-1] if stack else -1", {"code": True}), " — After popping, the new stack top is the nearest bar shorter than the popped bar, to its left. If stack is empty, use -1 (meaning the rectangle can extend to index 0)."])),
    N.para(N.rich([("width = i - left - 1", {"code": True}), " — The rectangle spans from left+1 to i-1 inclusive. Width = i - left - 1. (Not i - left: the boundary bars at positions left and i are shorter, so excluded.)"])),
    N.para(N.rich([("max_area = max(max_area, height * width)", {"code": True}), " — Update the running maximum if this rectangle is larger."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — Push current index after all pops. Stack remains in increasing-height order."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible (left, right) pair as the rectangle boundaries. For each pair, the rectangle height is the minimum bar in that range. Compute area = min_height × (right - left + 1)."),
        N.h4("What Doesn't Work"),
        N.para("Computing the minimum from scratch for each pair is O(n³) total. With a running minimum tracked as we expand right from each left, we get O(n²) — correct but TLE for large inputs."),
        N.h4("The Key Observation"),
        N.para("As we expand right from a fixed left, the minimum can only decrease or stay the same. We track the running minimum to avoid recomputing it for each (left, right) pair."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer loop for the left boundary, inner loop expands right while tracking the minimum height. Compute area at each step."),
    ]),
    N.h3("Code"),
    N.code("""\
def largestRectangleArea(heights: list[int]) -> int:
    max_area = 0
    n = len(heights)
    for left in range(n):
        min_h = heights[left]          # bottleneck height in [left, right]
        for right in range(left, n):
            min_h = min(min_h, heights[right])
            max_area = max(max_area, min_h * (right - left + 1))
    return max_area"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for left in range(n)", {"code": True}), " — Try every possible left boundary of the rectangle."])),
    N.para(N.rich([("min_h = heights[left]", {"code": True}), " — Initialize the bottleneck height as the left bar's height."])),
    N.para(N.rich([("min_h = min(min_h, heights[right])", {"code": True}), " — As we extend right, the rectangle height can only decrease (limited by the shortest bar in the span)."])),
    N.para(N.rich([("max_area = max(max_area, min_h * (right - left + 1))", {"code": True}), " — Compute area for this (left, right) span and update best."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Monotonic Stack (Interview Pick)", "O(n)", "O(n)"],
        ["Precompute left[]+right[] arrays", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Stack"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack for Left/Right Bounds · Monotonic Stack: Previous Smaller"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Find largest/smallest shape in a histogram or array. (2) For each element, find the nearest element smaller/larger to its left and right. (3) A span's value is determined by the minimum or maximum element within it. (4) 2D problems reducible to repeated 1D histogram sub-problems.")
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the Monotonic Stack: Left/Right Bounds technique:"),
    N.bullet(N.rich([("Maximal Rectangle", {"bold": True}), " (Hard) — Apply histogram algorithm row-by-row on a binary matrix; same core technique (#85)"])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — Water trapped between bars using monotonic stack or two-pointer approach (#42)"])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Find next warmer day for each day; monotonic decreasing stack for 'next greater' (#739)"])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — Contribution of each bar as subarray minimum; previous and next smaller elements (#907)"])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — Classic 'next greater element' using monotonic stack; simpler version of same pattern (#496)"])),
    N.bullet(N.rich([("Online Stock Span", {"bold": True}), " (Medium) — Consecutive days with price ≤ today; stack of (price, span) pairs (#901)"])),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), " (Medium) — Build smallest number by maintaining monotonic increasing stack (#402)"])),
    N.para("These problems share the core technique: a monotonic stack that provides O(1) access to the nearest smaller or larger element, eliminating the need for nested loops."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stack/Queue Patterns → Monotonic Stack: Previous Smaller", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("largest_rectangle_in_histogram")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
