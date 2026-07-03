"""
gen_find_smallest_letter_greater_than_target.py
Notion IN-PLACE update for LeetCode #744 — Find Smallest Letter Greater Than Target
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812a-8402-f30d933c8046"

# ── 1) Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=744,
    pattern="Binary Search",
    subpatterns=["Upper Bound"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Upper-bound binary search: find first index where letters[i] > target; wrap with lo % n.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks.")

# ── 3) Build body blocks ──────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted array of characters ", {}),
        ("letters", {"code": True}),
        (" and a character ", {}),
        ("target", {"code": True}),
        (", return the smallest letter in ", {}),
        ("letters", {"code": True}),
        (" that is lexicographically greater than ", {}),
        ("target", {"code": True}),
        (". The letters wrap around — if no letter in ", {}),
        ("letters", {"code": True}),
        (" is greater than ", {}),
        ("target", {"code": True}),
        (", return ", {}),
        ("letters[0]", {"code": True}),
        (".", {}),
    ])),
    N.para("Constraints: letters has at least 2 characters, all lowercase English letters, sorted in non-decreasing order. target is a lowercase English letter."),
    N.divider(),
]

# ─── Solution 1: Upper-Bound Binary Search ────────────────────────────────────
sol1_code = """\
def nextGreatestLetter(letters: list, target: str) -> str:
    lo, hi = 0, len(letters)   # hi = n (not n-1) to support wrap case
    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1       # mid is <= target: not valid, search right
        else:
            hi = mid           # mid > target: valid candidate, search left
    return letters[lo % len(letters)]  # lo%n wraps index n to 0"""

blocks += [
    N.h2("Solution 1 — Upper-Bound Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a sorted list of letters. We want the first one that comes strictly after 'target' in the alphabet. If none exists, wrap around to the first letter. This is not a lookup — it's a boundary search."),
        N.h4("What Doesn't Work"),
        N.para("A linear scan from left to right works but runs in O(n) — it ignores the fact that the array is sorted. For n up to 10^4, this is acceptable, but it misses an important optimization. Any time you see 'sorted array + find boundary', you should reach for binary search."),
        N.h4("The Key Observation"),
        N.para("We want the leftmost index where letters[i] > target. This is the classic upper-bound query: 'find the first position where a monotone predicate becomes true.' On sorted data, binary search finds this in O(log n)."),
        N.h4("Building the Solution"),
        N.para("Set lo=0, hi=n (length, not n-1 — this allows hi to reach n if all letters are <= target). In each iteration, inspect mid. If letters[mid] <= target: mid is not valid, go right (lo=mid+1). If letters[mid] > target: mid is valid but might not be the leftmost, so search left (hi=mid). Loop terminates when lo==hi. Return letters[lo % n] — modulo handles the wrap: if lo==n then lo%n=0."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}),
                    ("Imagine standing at the middle of a library shelf sorted A–Z. You want the first book whose title starts after 'H'. If the middle book starts with 'J', it works but maybe 'I' is to your left — check left. If the middle starts with 'F', it's too early — move right. When your search window collapses to a single book, that's your answer.", {})]),
            "📚", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 0, len(letters)", {"code": True}), (" — Initialize boundaries. hi=n (not n-1) so the range [lo, hi) can extend past the last index, representing 'all letters exhausted — wrap around'.", {})])),
    N.para(N.rich([("while lo < hi:", {"code": True}), (" — Loop until the search space collapses to a single point. When lo==hi, we have our answer.", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Integer midpoint. In Python, no overflow risk. This is always < hi.", {})])),
    N.para(N.rich([("if letters[mid] <= target:", {"code": True}), (" — letters[mid] is at or before target — not a valid answer. Discard mid and everything left of it.", {})])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), (" — Move lo past mid. The answer must be strictly to the right.", {})])),
    N.para(N.rich([("hi = mid", {"code": True}), (" — letters[mid] > target: mid is valid, but we keep searching left to find something smaller that also beats target. Keep mid inside the window.", {})])),
    N.para(N.rich([("return letters[lo % len(letters)]", {"code": True}), (" — If lo==n, all letters were <= target, so wrap: n%n=0 gives letters[0]. Otherwise lo%n=lo (unchanged).", {})])),
    N.divider(),
]

# ─── Solution 2: Linear Scan ──────────────────────────────────────────────────
sol2_code = """\
def nextGreatestLetter(letters: list, target: str) -> str:
    for ch in letters:
        if ch > target:
            return ch
    return letters[0]  # wrap: no letter beat target"""

blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simply iterate through the sorted array. The first character we encounter that is strictly greater than target is our answer, because the array is sorted (smallest to largest)."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly, but it's O(n). It doesn't exploit the sorted property. For small inputs it's perfectly fine, but for large n, binary search is strictly better."),
        N.h4("The Key Observation"),
        N.para("Because the array is sorted, the first element that beats target is also the smallest such element. No sorting or post-processing needed — just return on first match."),
        N.h4("Building the Solution"),
        N.para("Scan left to right. Return the first character ch where ch > target. If we reach the end without finding one, return letters[0] (the wrap)."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for ch in letters:", {"code": True}), (" — Iterate left to right. Array is sorted so earliest valid match is smallest.", {})])),
    N.para(N.rich([("if ch > target:", {"code": True}), (" — Check strictly greater. Equal letters (target in array) are not returned.", {})])),
    N.para(N.rich([("return ch", {"code": True}), (" — First character that beats target. Because we go left to right on sorted data, this is the minimum.", {})])),
    N.para(N.rich([("return letters[0]", {"code": True}), (" — Loop completed with no match: all letters are <= target. Wrap to the beginning.", {})])),
    N.divider(),
]

# ─── Complexity Table ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Linear Scan", "O(n)", "O(1)"],
        ["Upper-Bound Binary Search (Interview Pick)", "O(log n)", "O(1)"],
        ["bisect.bisect_right one-liner", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Upper Bound (BS: First/Last Occurrence)", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("Sorted array or search space + looking for the FIRST index where a condition is true (strictly greater, not-less-than, predicate becomes True). "
                 "The tell is 'strictly greater than X' or 'first position satisfying Y'. "
                 "Also: any circular/wrap problem on sorted data where you need the next-greater neighbor.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Upper Bound / BS: First/Last Occurrence):"),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}), (" (Easy) — Identical upper-bound template; returns where target would be inserted to keep array sorted. LeetCode #35.", {})])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), (" (Easy) — Find the first version where isBadVersion() returns True; same hi=n, hi=mid structure. LeetCode #278.", {})])),
    N.bullet(N.rich([("Find First and Last Position of Element in Sorted Array", {"bold": True}), (" (Medium) — Applies both lower-bound (first occurrence) and upper-bound (last occurrence). LeetCode #34.", {})])),
    N.bullet(N.rich([("Sqrt(x)", {"bold": True}), (" (Easy) — Find largest k where k² ≤ x using binary search on the answer. LeetCode #69.", {})])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — Binary search on the answer value (eating speed), not array indices. LeetCode #875.", {})])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — Binary search on ship capacity; feasibility check per candidate. LeetCode #1011.", {})])),
    N.para("These problems share the same core technique: binary search with a monotone predicate, converging lo and hi to the leftmost valid position."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search → BS: First/Last Occurrence). Sub-Pattern verified: Upper Bound — Guide Section 9.", "📚", "gray_background"),
]

# ─── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_smallest_letter_greater_than_target")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4) Append all blocks ──────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
