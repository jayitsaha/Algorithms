"""
Notion update script for Trapping Rain Water (#42)
Regenerates the page IN-PLACE via notion_lib.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8154-a032-ff74833f1d59"

# ── Step 1: Update page properties ──────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=42,
    pattern="Two Pointers",
    subpatterns=["Opposite Direction (Max Heights)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Process the shorter side: left_max or right_max is the binding constraint, no look-ahead needed.",
    icon="🔴"
)
print("  Properties OK")

# ── Step 2: Wipe existing content ────────────────────────────────────────
print("Wiping existing blocks...")
n_wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {n_wiped} blocks")

# ── Step 3: Build content blocks ─────────────────────────────────────────
print("Building content blocks...")
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("height", {"code": True}),
        (" of ", {}),
        ("n", {"code": True}),
        (" non-negative integers representing an elevation map where the width of each bar is 1, "
         "compute how much water it can trap after raining.", {})
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("height = [0,1,0,2,1,0,1,3,2,1,2,1]", {"code": True}),
        (" → Output: 6", {})
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("height = [4,2,0,3,2,5]", {"code": True}),
        (" → Output: 9", {})
    ])),
    N.para("Constraints: n == height.length, 0 <= n <= 2×10⁴, 0 <= height[i] <= 10⁵"),
    N.divider(),
]

# ── Solution 1: Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each column i, water forms a horizontal surface. That surface is bounded from above by the shorter of the tallest wall to the left and the tallest wall to the right. Water = min(max_left, max_right) − height[i], or 0 if negative."),
        N.h4("What Doesn't Work"),
        N.para("There is no shortcut that avoids knowing both the left max and the right max for each position. Any correct solution must compute these two values for every column."),
        N.h4("The Key Observation"),
        N.para("For each column independently scan left to find the max and scan right to find the max. This is O(n) per column → O(n²) total. Correct but slow."),
        N.h4("Building the Solution"),
        N.para("Loop i from 1 to n−2. At each i: compute left_max as max(height[0..i]), right_max as max(height[i..n-1]). Add max(0, min(left_max, right_max) − height[i]) to total."),
        N.callout("Analogy: For each valley, measure how tall the left hill is (walk left) and how tall the right hill is (walk right). The shorter hill sets the water level.", "🏔️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def trap_brute(height: list) -> int:
    n, total = len(height), 0
    for i in range(1, n - 1):
        left_max = max(height[:i+1])
        right_max = max(height[i:])
        total += min(left_max, right_max) - height[i]
    return total"""),
    N.h3("Line by Line"),
    N.para(N.rich([("n, total = len(height), 0", {"code": True}), (" — initialize length and accumulator.", {})])),
    N.para(N.rich([("for i in range(1, n-1)", {"code": True}), (" — first/last columns can never trap water (no wall on one side).", {})])),
    N.para(N.rich([("left_max = max(height[:i+1])", {"code": True}), (" — tallest wall from index 0 to i (inclusive), O(n) scan.", {})])),
    N.para(N.rich([("right_max = max(height[i:])", {"code": True}), (" — tallest wall from index i to end, O(n) scan.", {})])),
    N.para(N.rich([("total += min(left_max, right_max) - height[i]", {"code": True}), (" — shorter boundary sets water level; subtract ground height. Always ≥ 0 because left_max ≥ height[i] and right_max ≥ height[i].", {})])),
    N.divider(),
]

# ── Solution 2: Prefix/Suffix Arrays ──
blocks += [
    N.h2("Solution 2 — Prefix/Suffix Arrays · O(n) time · O(n) space"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The brute force is slow because it recomputes maxima on every iteration. Can we precompute them?"),
        N.h4("What Doesn't Work"),
        N.para("We cannot precompute in one pass because the left max and right max run in opposite directions. We need two separate passes."),
        N.h4("The Key Observation"),
        N.para("Build lmax[i] = max(height[0..i]) left-to-right in one pass. Build rmax[i] = max(height[i..n-1]) right-to-left in another pass. Then answer each column in a third pass. Total: three O(n) passes."),
        N.h4("Building the Solution"),
        N.para("lmax[i] = max(lmax[i-1], height[i]). rmax[i] = max(rmax[i+1], height[i]). Final: sum(min(lmax[i], rmax[i]) - height[i] for all i)."),
        N.callout("This solution is conceptually the clearest and should be described before jumping to the two-pointer approach in an interview.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def trap_arrays(height: list) -> int:
    n = len(height)
    if n == 0:
        return 0
    lmax, rmax = [0] * n, [0] * n
    lmax[0] = height[0]
    for i in range(1, n):
        lmax[i] = max(lmax[i-1], height[i])
    rmax[-1] = height[-1]
    for i in range(n-2, -1, -1):
        rmax[i] = max(rmax[i+1], height[i])
    return sum(min(lmax[i], rmax[i]) - height[i] for i in range(n))"""),
    N.h3("Line by Line"),
    N.para(N.rich([("lmax[0] = height[0]", {"code": True}), (" — seed: the only left max at index 0 is height[0] itself.", {})])),
    N.para(N.rich([("lmax[i] = max(lmax[i-1], height[i])", {"code": True}), (" — extend the running max one step right.", {})])),
    N.para(N.rich([("rmax[-1] = height[-1]", {"code": True}), (" — seed from the right end.", {})])),
    N.para(N.rich([("rmax[i] = max(rmax[i+1], height[i])", {"code": True}), (" — extend the running max one step left.", {})])),
    N.para(N.rich([("sum(min(lmax[i], rmax[i]) - height[i] ...)", {"code": True}), (" — each column now has its exact left and right max available in O(1).", {})])),
    N.divider(),
]

# ── Solution 3: Two Pointers (Interview Pick) ──
blocks += [
    N.h2("Solution 3 — Two Pointers · O(n) time · O(1) space (Interview Pick) ✓"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The prefix/suffix approach computes both full arrays before using any value. But we only ever use lmax[i] and rmax[i] together at step i. Can we compute them on demand?"),
        N.h4("What Doesn't Work"),
        N.para("We cannot compute the left max and right max for an arbitrary index in O(1) without precomputation — unless we commit to a specific order of processing."),
        N.h4("The Key Observation"),
        N.para("The binding constraint at any position is whichever of left_max or right_max is SMALLER. So: start from both ends, always process whichever side currently has the shorter wall. That side's running max is provably the binding constraint — we need not examine the other side at all."),
        N.h4("Building the Solution"),
        N.para("left=0, right=n-1, left_max=right_max=0. While left < right: if height[left] <= height[right], update left_max then add left_max - height[left] to total, advance left. Else update right_max, add right_max - height[right], retreat right."),
        N.callout("Key proof: when height[left] <= height[right], the right side is at least height[right] >= height[left]. So the global right max for position left is also >= height[left] >= left_max... meaning left_max IS the binding constraint. Safe to compute without seeing what lies between the pointers.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def trap(height: list) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    total = 0
    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            total += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            total += right_max - height[right]
            right -= 1
    return total"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if not height: return 0", {"code": True}), (" — guard against empty input.", {})])),
    N.para(N.rich([("left, right = 0, len(height) - 1", {"code": True}), (" — initialize pointers at both ends.", {})])),
    N.para(N.rich([("left_max = right_max = 0", {"code": True}), (" — running maximum from each side; both start at 0.", {})])),
    N.para(N.rich([("while left < right", {"code": True}), (" — loop until pointers meet; each iteration advances exactly one pointer by 1.", {})])),
    N.para(N.rich([("if height[left] <= height[right]", {"code": True}), (" — left is shorter or equal; left_max is the binding constraint.", {})])),
    N.para(N.rich([("left_max = max(left_max, height[left])", {"code": True}), (" — MUST update max first. Guarantees left_max >= height[left], so next line is always >= 0.", {})])),
    N.para(N.rich([("total += left_max - height[left]", {"code": True}), (" — water above this column; 0 when column is itself the current max (a wall).", {})])),
    N.para(N.rich([("left += 1", {"code": True}), (" — move inward; this column is permanently settled.", {})])),
    N.para(N.rich([("right_max / right -= 1", {"code": True}), (" — symmetric: update right running max, add water, retreat right.", {})])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Prefix/Suffix Arrays", "O(n)", "O(n)"],
        ["Two Pointers (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Array Manipulation / Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Opposite Direction (Max Heights)", {})])),
    N.callout(
        "When to recognize this pattern: The answer at each position depends on a left boundary and right boundary. We can make a greedy decision — always process the weaker side — eliminating the need to precompute full prefix/suffix arrays. Signals: 'compute something bounded by min of two maxima', 'O(1) space required', 'squeeze from both ends'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (opposite-direction two pointers, max tracking):"),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), (" (Medium) — maximize area = width × min(height[left], height[right]); same pointer squeeze logic (#11)", {})])),
    N.bullet(N.rich([("Two Sum II — Input Array Is Sorted", {"bold": True}), (" (Medium) — classic opposite-direction two-pointer on sorted array (#167)", {})])),
    N.bullet(N.rich([("3Sum", {"bold": True}), (" (Medium) — fix one element, two-pointer on sorted remainder (#15)", {})])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), (" (Easy) — left/right pointers converge comparing characters (#125)", {})])),
    N.bullet(N.rich([("Trapping Rain Water II", {"bold": True}), (" (Hard) — 3D elevation grid; BFS from boundary using min-heap instead of two pointers (#407)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — monotonic stack finds left/right bounding walls for each bar; related elevation problem (#84)", {})])),
    N.bullet(N.rich([("Sort Colors", {"bold": True}), (" (Medium) — Dutch National Flag; different flavor of two-pointer but same opposite-direction squeeze (#75)", {})])),
    N.para("These problems share the pattern of computing answers constrained by maxima (or minima) at both ends."),
    N.divider(),
]

# ── Visual Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("trapping_rain_water")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys to see each pointer advance and water accumulate column by column.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Built {len(blocks)} blocks")

# ── Step 4: Append all blocks ────────────────────────────────────────────
print("Appending blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("  Blocks OK")

print(f"\nNOTION OK {PAGE_ID}")
