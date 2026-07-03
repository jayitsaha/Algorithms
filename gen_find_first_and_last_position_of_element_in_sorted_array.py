"""
gen_find_first_and_last_position_of_element_in_sorted_array.py
Regenerates the Notion page for LeetCode #34 in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b8-9380-f8d5ccd9f96f"
SLUG    = "find_first_and_last_position_of_element_in_sorted_array"

# ── 1. Set properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 34,
    pattern     = "Binary Search",
    subpatterns = ["Two Binary Searches"],
    tc          = "O(log n)",
    sc          = "O(1)",
    key_insight = "Run binary search twice—once biased left (find first), once biased right (find last). When target found, save index and keep narrowing instead of returning.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of integers ", {}),
        ("nums", {"code": True}),
        (" sorted in non-decreasing order, find the starting and ending position of a given ", {}),
        ("target", {"code": True}),
        (" value. If ", {}),
        ("target", {"code": True}),
        (" is not found in the array, return ", {}),
        ("[-1, -1]", {"code": True}),
        (". You must write an algorithm with ", {}),
        ("O(log n)", {"code": True}),
        (" runtime complexity.", {}),
    ])),
    N.para("Example 1: nums = [5,7,7,8,8,10], target = 8  →  [3, 4]"),
    N.para("Example 2: nums = [5,7,7,8,8,10], target = 6  →  [-1, -1]"),
    N.para("Example 3: nums = [], target = 0  →  [-1, -1]"),
    N.divider(),
]

# ── Solution 1 — Brute Force ──
blocks += [
    N.h2("Solution 1 — Brute Force: Linear Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need two indices: the leftmost and rightmost positions of the target. Scanning left-to-right, we track the first time we see the target and keep updating 'last seen' on every hit."),
        N.h4("What Doesn't Work (and Why We Need Better)"),
        N.para("The linear scan is correct but runs in O(n). The problem explicitly requires O(log n), which rules it out. However, stating this brute force first in an interview is good practice — it shows you understand the problem before optimizing."),
        N.h4("The Key Observation"),
        N.para("When we scan left-to-right, the first hit is the first position and the last hit (overwriting on every match) is the last position. Simple and correct, but O(n)."),
        N.h4("Building the Solution"),
        N.para("Initialize first = last = -1. Iterate: if v == target, set first = i on first hit, always update last = i. Return [first, last]."),
        N.callout("This is the 'say brute force first' approach. State it, give its complexity, then transition: 'Since the array is sorted and we need O(log n), binary search is the right tool.'", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def searchRange(nums, target):
    first = last = -1
    for i, v in enumerate(nums):
        if v == target:
            if first == -1:
                first = i      # Set first only on the very first hit
            last = i           # Always update last; final value is rightmost
    return [first, last]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("first = last = -1", {"code": True}), " — Start pessimistic: target not found yet."])),
    N.para(N.rich([("for i, v in enumerate(nums)", {"code": True}), " — Scan every element with its index."])),
    N.para(N.rich([("if v == target", {"code": True}), " — Check if current element matches target."])),
    N.para(N.rich([("if first == -1: first = i", {"code": True}), " — Only set first on the very first match; subsequent matches don't overwrite it."])),
    N.para(N.rich([("last = i", {"code": True}), " — Update last on every match; after the loop it holds the rightmost index."])),
    N.para(N.rich([("return [first, last]", {"code": True}), " — If no match, both are still -1."])),
    N.divider(),
]

# ── Solution 2 — Two Binary Searches (Interview Pick) ──
blocks += [
    N.h2("Solution 2 — Two Binary Searches (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The problem is really: find the LEFT BOUNDARY of the target block, and find the RIGHT BOUNDARY. Binary search excels at finding boundaries in sorted data."),
        N.h4("What Doesn't Work"),
        N.para("Standard binary search returns as soon as it finds the target — giving 'a' position, not 'the first' or 'the last'. In [1,2,2,2,3] with target=2, standard BS might return index 2 (middle); correct first is 1, correct last is 3."),
        N.h4("The Key Observation"),
        N.para("When you find the target at mid, there might be more target values to the left (for first) or right (for last). Don't return — save the index and keep narrowing the window in the direction you care about. The last saved index when the window collapses is the true boundary."),
        N.h4("Building the Solution"),
        N.para("Write one helper function find_boundary(go_left). When nums[mid]==target: save result=mid, then either right=mid-1 (go_left=True) or left=mid+1 (go_left=False). Non-match cases are identical to standard binary search. Call this helper twice."),
        N.callout("Analogy: Searching a dictionary for all pages containing 'binary'. You find one — but you keep flipping left (going backward) to find the FIRST page, or right to find the LAST page. You don't stop at the first hit.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def searchRange(nums, target):
    def find_boundary(go_left):
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid           # Save this index as a boundary candidate
                if go_left:
                    right = mid - 1    # Keep searching left for an earlier occurrence
                else:
                    left = mid + 1     # Keep searching right for a later occurrence
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    first = find_boundary(go_left=True)
    if first == -1:
        return [-1, -1]               # Short-circuit: target not in array
    last = find_boundary(go_left=False)
    return [first, last]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("def find_boundary(go_left)", {"code": True}), " — Single helper handles both searches; boolean flag controls direction on match."])),
    N.para(N.rich([("left, right = 0, len(nums) - 1", {"code": True}), " — Each call starts with the full array search space."])),
    N.para(N.rich([("result = -1", {"code": True}), " — Pessimistic default; returned unchanged if target never found."])),
    N.para(N.rich([("while left <= right", {"code": True}), " — Standard binary search loop; continues until window collapses."])),
    N.para(N.rich([("mid = left + (right - left) // 2", {"code": True}), " — Safe midpoint computation (avoids integer overflow in Java/C++)."])),
    N.para(N.rich([("if nums[mid] == target: result = mid", {"code": True}), " — Match found. Save it as the best boundary candidate so far."])),
    N.para(N.rich([("if go_left: right = mid - 1", {"code": True}), " — Finding first: discard mid and everything right of it; search left half only."])),
    N.para(N.rich([("else: left = mid + 1", {"code": True}), " — Finding last: discard mid and everything left of it; search right half only."])),
    N.para(N.rich([("elif nums[mid] < target: left = mid + 1", {"code": True}), " — Target must be to the right; discard left half."])),
    N.para(N.rich([("else: right = mid - 1", {"code": True}), " — nums[mid] > target; discard right half."])),
    N.para(N.rich([("return result", {"code": True}), " — After loop, result holds the leftmost or rightmost index, or -1."])),
    N.para(N.rich([("if first == -1: return [-1, -1]", {"code": True}), " — Short-circuit: if target absent, skip the second search entirely."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",           "Time",     "Space", "Notes"],
        ["Brute Force (Scan)", "O(n)",     "O(1)",  "Violates the O(log n) constraint"],
        ["Two Binary Searches","O(log n)", "O(1)",  "Optimal; 2 × O(log n) = O(log n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Binary Searches (BS: First/Last Occurrence)"])),
    N.callout(
        "When to recognize this pattern: sorted array + O(log n) constraint + need a range/boundary rather than just any occurrence. Signals: 'find first/last position', 'find range of element', 'count occurrences in sorted array'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Two Binary Searches / boundary technique:"),
]
related = [
    ("First Bad Version", "Easy", "#278 — Find leftmost version where isBadVersion() is true; classic leftward boundary search"),
    ("Search Insert Position", "Easy", "#35 — Find target or insertion point; bisect_left pattern"),
    ("Find Minimum in Rotated Sorted Array", "Medium", "#153 — Binary search for the rotation boundary"),
    ("Search in Rotated Sorted Array", "Medium", "#33 — Binary search with a sorted-half check; extends boundary idea"),
    ("Kth Smallest in Sorted Matrix", "Medium", "#378 — Binary search on value; use boundary count per mid"),
    ("Count of Smaller Numbers After Self", "Hard", "#315 — Binary search boundary logic per element"),
    ("Find Peak Element", "Medium", "#162 — Boundary search where slope sign changes"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {}),
    ])))
blocks += [
    N.para("These problems share the core technique: modify binary search termination to find the extreme (leftmost or rightmost) occurrence rather than any occurrence."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search → BS: First/Last Occurrence). Sub-pattern: Two Binary Searches. Source: Guide Section 9.", "📚", "gray_background"),
]

# ── Embed ──
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
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
