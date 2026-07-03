"""
gen_summary_ranges.py — Notion update for Summary Ranges (LC #228)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819a-9002-ff9938c3fee2"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=228,
    pattern="Intervals",
    subpatterns=["Track Range Start/End"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Record range start; advance while consecutive; emit 'a' or 'a->b' on gap or array end.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──
SOL1_CODE = '''\
def summaryRanges(nums):
    result, n, i = [], len(nums), 0
    while i < n:
        start = nums[i]
        while i + 1 < n and nums[i + 1] == nums[i] + 1:
            i += 1          # extend range while consecutive
        if start == nums[i]:
            result.append(str(start))          # single element
        else:
            result.append(f"{start}->{nums[i]}")  # multi-element
        i += 1              # move past end of this range
    return result
'''

SOL2_CODE = '''\
def summaryRanges(nums):
    result, n = [], len(nums)
    i = 0
    while i < n:
        j = i                           # j scans to find range end
        while j + 1 < n and nums[j + 1] == nums[j] + 1:
            j += 1
        if i == j:
            result.append(str(nums[i]))         # single element
        else:
            result.append(f"{nums[i]}->{nums[j]}")  # multi-element
        i = j + 1                       # jump past entire range
    return result
'''

blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a sorted unique integer array ", {}),
        ("nums", {"code": True}),
        (". A range ", {}),
        ("[a, b]", {"code": True}),
        (" is the smallest sorted list of ranges that cover all the numbers in the array exactly. "
         "That is, each element of nums is covered by exactly one of the ranges, and there is no "
         "integer x such that x is in one of the ranges but not in nums. Return the smallest sorted "
         "list of ranges that cover all the numbers in the array exactly.\n\n"
         "Each range [a, b] should be output as:\n"
         "  \"a->b\" if a != b\n"
         "  \"a\" if a == b", {})
    ])),
    N.para("Example 1: nums = [0,1,2,4,5,7] → [\"0->2\",\"4->5\",\"7\"]"),
    N.para("Example 2: nums = [0,2,3,4,6,8,9] → [\"0\",\"2->4\",\"6\",\"8->9\"]"),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Single-Pass Range Tracker (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find maximal runs of consecutive integers in a sorted array and format them as range strings. The core operation: for any two adjacent sorted unique elements, if their difference is exactly 1, they belong to the same range. If the difference is > 1, they belong to different ranges."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: checking all pairs to find which numbers are consecutive is O(n²) — completely unnecessary. Using a hash set to check for n-1 or n+1 neighbors works but adds O(n) space where O(1) is achievable. Since the input is already sorted, we only need adjacent comparisons."),
        N.h4("The Key Observation"),
        N.para("Because the array is SORTED and UNIQUE, two adjacent elements nums[i] and nums[i+1] are consecutive iff nums[i+1] - nums[i] == 1. That single check tells us everything. We never need to look at non-adjacent elements."),
        N.h4("Building the Solution"),
        N.para(
            "1. Outer loop: set start = nums[i] to mark the beginning of a new range.\n"
            "2. Inner loop: advance i while nums[i+1] == nums[i]+1. When inner loop exits, nums[i] is the range end.\n"
            "3. Emit: if start == nums[i], format as 'start'. Otherwise format as 'start->end'.\n"
            "4. Advance i past the range end; repeat outer loop.\n"
            "Key: the outer+inner loops together advance i by exactly 1 per element — total O(n)."
        ),
        N.callout(
            "Analogy: reading a ruler. Slide your finger right until you hit a break. "
            "Record where the unbroken segment started and where it ended. Write the range. "
            "Start fresh from the next tick.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result, n, i = [], len(nums), 0", {"code": True}), (" — Initialize output list, length cache, and scan pointer.", {})])),
    N.para(N.rich([("while i < n:", {"code": True}), (" — Outer loop: begins a new range on each iteration. Continues until all elements processed.", {})])),
    N.para(N.rich([("start = nums[i]", {"code": True}), (" — Record the start of the current range at position i. This value is remembered until the range is emitted.", {})])),
    N.para(N.rich([("while i+1 < n and nums[i+1] == nums[i]+1:", {"code": True}), (" — Inner loop: extend range while the next element is exactly 1 greater (consecutive). Bounds check first to avoid index error.", {})])),
    N.para(N.rich([("i += 1", {"code": True}), (" — (inside inner loop) Advance i into the range. When inner loop exits, nums[i] is the LAST element of the current consecutive run.", {})])),
    N.para(N.rich([("if start == nums[i]:", {"code": True}), (" — If start equals the current position, the inner loop never ran — this is a single-element range.", {})])),
    N.para(N.rich([("result.append(str(start))", {"code": True}), (" — Single element: format as 'a'.", {})])),
    N.para(N.rich([("result.append(f\"{start}->{nums[i]}\")", {"code": True}), (" — Multi-element: format as 'a->b'. start is range begin, nums[i] is range end.", {})])),
    N.para(N.rich([("i += 1", {"code": True}), (" — (outer loop advance) Move past the end of the just-emitted range. The next outer iteration starts a fresh range.", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Explicit Two-Pointer (i = start index, j = end index)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same logic as Solution 1, but with two explicit index variables: i marks the range start, j scans for the range end. This makes the range boundaries explicit and avoids the 'start == nums[i]' comparison."),
        N.h4("What Doesn't Work"),
        N.para("Nothing fundamentally different — this is a style variant. The single-variable version is slightly more concise; the two-variable version is more readable to beginners because i and j have clear roles."),
        N.h4("The Key Observation"),
        N.para("Using two separate index variables (i for start, j for end) makes the code structurally mirror the problem statement: 'find start, find end, emit range from start to end.' Some interviewers prefer this clarity."),
        N.h4("Building the Solution"),
        N.para(
            "At each outer iteration: set j = i. "
            "Advance j while consecutive. "
            "When j stops: emit nums[i] to nums[j]. "
            "Set i = j + 1 to jump past the entire range. "
            "The comparison is i == j (same index) instead of start == nums[i]."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("j = i", {"code": True}), (" — j starts at i (range start) and scans forward to find the range end.", {})])),
    N.para(N.rich([("while j+1 < n and nums[j+1] == nums[j]+1:", {"code": True}), (" — Extend j while the next element is consecutive.", {})])),
    N.para(N.rich([("if i == j:", {"code": True}), (" — i and j at same position means a single-element range. Same logic as start == nums[i] in Solution 1.", {})])),
    N.para(N.rich([("i = j + 1", {"code": True}), (" — Jump the outer pointer past the entire range. Equivalent to the outer i += 1 in Solution 1 (since inner loop advances i to the range end).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Single-Pass Tracker (S1)", "O(n)", "O(1)", "Optimal; inner+outer loops each element once"],
        ["Two-Pointer (S2)", "O(n)", "O(1)", "Equivalent; more explicit index variables"],
        ["Brute Force (all pairs)", "O(n²)", "O(n)", "Unnecessary given sorted input"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Range Start/End"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Compress consecutive numbers into ranges' → Track start, emit on gap\n"
        "• 'Find runs in sorted unique input' → Adjacent difference check\n"
        "• 'Format intervals from sorted data' → Same range-tracking pattern\n"
        "• Signal: sorted input + 'group consecutive' or 'report ranges' in problem statement",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Missing Ranges", {"bold": True}), (" (Easy) — Find missing ranges between lo and hi; same gap-detection logic (#163)", {})])),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), (" (Medium) — Merge overlapping intervals after sorting by start — classic interval pattern (#56)", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), (" (Medium) — Insert into sorted non-overlapping interval list; boundary tracking required (#57)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Remove minimum intervals to eliminate all overlaps; interval end tracking (#435)", {})])),
    N.bullet(N.rich([("Minimum Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Count intervals sharing an arrow; greedy with interval overlap detection (#452)", {})])),
    N.bullet(N.rich([("Data Stream as Disjoint Intervals", {"bold": True}), (" (Hard) — Maintain disjoint interval set dynamically as numbers stream in (#352)", {})])),
    N.bullet(N.rich([("Find All Lonely Numbers in Array", {"bold": True}), (" (Medium) — Numbers with no adjacent neighbors; same sorted adjacent-difference check (#2150)", {})])),
    N.para("These problems share the core technique: record range start, advance while consecutive, emit on gap or boundary."),
    N.callout("📚 Pattern: Intervals → Sub-Pattern: Track Range Start/End. Single-pass O(n) with O(1) extra space.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("summary_ranges")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
