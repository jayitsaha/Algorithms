"""
gen_buildings_with_an_ocean_view.py
Notion regeneration script for: Buildings With an Ocean View (LC #1762)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b6-a67d-d2c7a46d8d5f"
SLUG = "buildings_with_an_ocean_view"

# ── Step 1: Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1762,
    pattern="Stack",
    subpatterns=["Monotonic Stack: Next Greater"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Scan right-to-left; building has ocean view iff heights[i] > max_right (tallest to its right).",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing body ──
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ──
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "There are ", ("n", {"code": True}), " buildings in a line. You are given an integer array ",
        ("heights", {"code": True}), " of size ", ("n", {"code": True}),
        " that represents the heights of the buildings in the line. The ocean is to the right of the buildings. "
        "A building has an ocean view if the building can see the ocean without obstructions. "
        "Formally, a building has an ocean view if all the buildings to its right have a strictly smaller height. "
        "Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order."
    ])),
    N.divider(),
]

# ── Solution 1: max_right scan (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Right-to-Left Scan with max_right (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Building i has an ocean view iff heights[i] is strictly greater than max(heights[i+1..n-1]). "
               "We need all such indices sorted ascending. This is a 'suffix maximum' condition."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each building, scan all buildings to its right. O(n²). "
               "Precomputing a suffix max array works in O(n) time but uses O(n) extra space. "
               "We can do even better: O(1) extra space."),
        N.h4("The Key Observation"),
        N.para("If we scan right-to-left (from the ocean inward), we can build the suffix maximum "
               "incrementally as a single variable max_right. By the time we reach index i, "
               "max_right already holds the maximum of everything to i's right — computed for free "
               "as a by-product of the rightward scan."),
        N.h4("Building the Solution"),
        N.para("Start at i = n-1 with max_right = 0. At each i: if heights[i] > max_right, "
               "append i to result. Then update max_right = max(max_right, heights[i]). "
               "Reverse result before returning (collected right-to-left, need ascending)."),
        N.callout("Analogy: Walking inward from the beach. As you walk away from the ocean, you keep "
                  "track of the tallest thing you've seen behind you. If you're taller than everything "
                  "behind you (closer to the ocean), you have a view.", "🏖️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def findBuildings(heights):
    n = len(heights)
    result = []
    max_right = 0
    for i in range(n - 1, -1, -1):
        if heights[i] > max_right:
            result.append(i)
        max_right = max(max_right, heights[i])
    return result[::-1]"""),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(heights)", {"code": True}), " — store length for clarity."])),
    N.para(N.rich([("result = []", {"code": True}), " — collects ocean-view indices (right-to-left during scan, reversed at end)."])),
    N.para(N.rich([("max_right = 0", {"code": True}), " — suffix maximum; 0 because nothing is to the right of the rightmost building."])),
    N.para(N.rich([("for i in range(n - 1, -1, -1)", {"code": True}), " — scan from rightmost building (ocean side) leftward (inland)."])),
    N.para(N.rich([("if heights[i] > max_right", {"code": True}), " — strictly taller than every building to the right → unobstructed ocean view."])),
    N.para(N.rich([("result.append(i)", {"code": True}), " — record this index as an ocean-view building."])),
    N.para(N.rich([("max_right = max(max_right, heights[i])", {"code": True}), " — update suffix max AFTER the check (include current building for future iterations to its left)."])),
    N.para(N.rich([("return result[::-1]", {"code": True}), " — reverse: collected descending order, output must be ascending."])),
    N.callout(
        "Warning: Update max_right AFTER the if-check, not before. "
        "If you update first, you include heights[i] in its own suffix max comparison, "
        "which incorrectly prevents the rightmost building (and others) from ever being counted.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Monotonic Stack ──
blocks += [
    N.h2("Solution 2 — Monotonic Decreasing Stack (O(n) time, O(n) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need buildings that are strictly greater than all buildings to their right. "
               "This is equivalent to: buildings NOT dominated by any building to their right. "
               "A monotonic stack naturally maintains 'dominance' relationships."),
        N.h4("What Doesn't Work"),
        N.para("The max_right approach is simpler and more space-efficient. "
               "The monotonic stack shines when you need to know WHICH building is the first blocker, "
               "not just WHETHER there is a blocker."),
        N.h4("The Key Observation"),
        N.para("Scan right-to-left maintaining a monotonically decreasing stack of heights. "
               "Before pushing heights[i], pop all stack elements ≤ heights[i] — they are dominated "
               "and can never block anything that heights[i] doesn't already block. "
               "After popping, if the stack is empty: no taller building to the right → ocean view."),
        N.h4("Building the Solution"),
        N.para("The stack holds a decreasing sequence of heights from buildings to the right. "
               "Each element is pushed once and popped at most once → O(n) amortized despite the while loop."),
        N.callout("The monotonic stack generalizes: store indices instead of heights if you need "
                  "to find the actual blocking building (useful for view-distance queries).", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def findBuildings(heights):
    stack = []  # monotonically decreasing heights
    result = []
    for i in range(len(heights) - 1, -1, -1):
        # Pop buildings shorter than or equal to current
        while stack and stack[-1] <= heights[i]:
            stack.pop()
        # Empty stack = no taller building to the right
        if not stack:
            result.append(i)
        stack.append(heights[i])
    return result[::-1]"""),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — monotonically decreasing stack of heights seen to the right."])),
    N.para(N.rich([("for i in range(len(heights) - 1, -1, -1)", {"code": True}), " — right-to-left scan."])),
    N.para(N.rich([("while stack and stack[-1] <= heights[i]", {"code": True}), " — pop dominated buildings (≤ current height cannot block us)."])),
    N.para(N.rich([("if not stack", {"code": True}), " — stack empty after popping means no taller building to the right → ocean view."])),
    N.para(N.rich([("stack.append(heights[i])", {"code": True}), " — push current height to maintain decreasing order."])),
    N.para(N.rich([("return result[::-1]", {"code": True}), " — reverse to ascending order."])),
    N.divider(),
]

# ── Solution 3: Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force (O(n²)) — Understand, Don't Submit"),
    N.h3("Code"),
    N.code("""\
def findBuildings(heights):
    n = len(heights)
    result = []
    for i in range(n):
        has_view = all(heights[j] < heights[i] for j in range(i + 1, n))
        if has_view:
            result.append(i)
    return result"""),
    N.para("For each building, use a generator expression to check all buildings to its right. "
           "The inner scan is O(n) per building → O(n²) total. "
           "Correct but too slow for n up to 10^5."),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (extra)"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Monotonic Stack", "O(n) amortized", "O(n)"],
        ["max_right Scan (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack (Monotonic Stack)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Monotonic Stack: Decreasing from Right; Right-to-Left Suffix Scan"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Does building/element i see the ocean/sky from the right?' → right-to-left scan\n"
        "• 'Is element i a suffix maximum?' → track max_right incrementally\n"
        "• 'Find elements that dominate all elements after them' → monotonic decreasing stack\n"
        "• 'Next greater element to the right' → monotonic stack on indices",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Stack / Right-to-Left Scan):"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}),
                     " (Medium) — How many days until a warmer temperature? Next greater element with distances. (#739)"])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}),
                     " (Easy) — For each element, find the next strictly greater to the right. (#496)"])),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}),
                     " (Medium) — Circular array version of next greater. (#503)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}),
                     " (Hard) — Monotonic stack to find previous/next smaller bars. (#84)"])),
    N.bullet(N.rich([("Asteroid Collision", {"bold": True}),
                     " (Medium) — Stack simulation of rightward/leftward asteroids colliding. (#735)"])),
    N.bullet(N.rich([("Number of Visible People in a Queue", {"bold": True}),
                     " (Hard) — How many people can each person see? Same decreasing-from-right technique. (#1944)"])),
    N.para("These problems share the core insight: scan from the relevant direction "
           "and use a monotonic structure to track which elements dominate."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns → "
              "Monotonic Stack: Next Greater / Decreasing from Right", "📚", "gray_background"),
]

# ── Embed section ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
