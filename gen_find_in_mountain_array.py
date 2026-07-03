"""
gen_find_in_mountain_array.py
Notion IN-PLACE update for LeetCode #1095 — Find in Mountain Array
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8115-9683-cf739ee3ba0c"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1095,
    pattern="Binary Search",
    subpatterns=["Find Peak + Two Searches"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Mountain = ascending + peak + descending: run three binary searches; flip comparisons on descending side; search left first for minimum index.",
    icon="🔴"
)
print("Properties set ✓")

# ── 2. Wipe old body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks ✓")

# ── 3. Build blocks ────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an interface ", {}),
        ("MountainArray", {"code": True}),
        (" where you may call ", {}),
        ("mountainArr.get(index)", {"code": True}),
        (" and ", {}),
        ("mountainArr.length()", {"code": True}),
        (". A mountain array strictly increases to a peak, then strictly decreases. "
         "Find the minimum index ", {}),
        ("i", {"code": True}),
        (" such that ", {}),
        ("mountainArr.get(i) == target", {"code": True}),
        (". Return ", {}),
        ("-1", {"code": True}),
        (" if no such index exists.", {})
    ])),
    N.para("Constraints: 3 ≤ mountainArr.length() ≤ 10000. Calls to get() are limited, enforcing O(log n)."),
    N.divider(),
]

# ── Solution 1 (Interview Pick) ────────────────────────────────────────────
SOLUTION_CODE = '''\
def findInMountainArray(target: int, mountainArr) -> int:
    n = mountainArr.length()

    # Phase 1: Find the peak index
    lo, hi = 0, n - 1
    while lo < hi:                             # strict: need mid+1 valid
        mid = (lo + hi) // 2
        if mountainArr.get(mid) < mountainArr.get(mid + 1):
            lo = mid + 1                       # ascending slope -> peak is right
        else:
            hi = mid                           # descending or at peak -> go left
    peak = lo                                  # lo == hi == peak index

    # Phase 2: Binary search ascending side [0..peak]
    lo, hi = 0, peak
    while lo <= hi:
        mid = (lo + hi) // 2
        val = mountainArr.get(mid)
        if val == target:
            return mid                         # leftmost result guaranteed
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    # Phase 3: Binary search descending side [peak..n-1]
    lo, hi = peak, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = mountainArr.get(mid)
        if val == target:
            return mid
        elif val < target:
            hi = mid - 1                      # FLIPPED: smaller -> go left
        else:
            lo = mid + 1                      # FLIPPED: larger -> go right

    return -1
'''

blocks += [
    N.h2("Solution 1 — Triple Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You can only access this array through a constrained API. The mountain structure is the key: it's secretly two sorted arrays joined at a peak. Binary search requires monotonicity — and we have two monotonic halves."),
        N.h4("What Doesn't Work"),
        N.para("Linear scan (O(n) get() calls) exceeds the call budget for large inputs. Any approach that modifies or sorts the array is impossible since we only have a get() interface. We need O(log n)."),
        N.h4("The Key Observation"),
        N.para("A mountain array = ascending half + peak + descending half. Each half is a sorted (monotonic) sequence. Binary search works on any monotonic sequence. So: find the split point (peak), then apply binary search to each half — with one important flip on the descending side."),
        N.h4("Building the Solution"),
        N.para("Step 1: Locate the peak using adjacent-element comparison. Step 2: Standard ascending binary search on [0..peak] — if found, return immediately (leftmost by construction). Step 3: Descending binary search on [peak..n-1] with flipped comparisons — return if found. If neither: return -1."),
        N.callout(
            "Analogy: Imagine hiking a mountain searching for a waypoint. First find the summit (peak). Then scan down the east slope, and if not found, scan down the west slope. Check east first — if the waypoint exists on both slopes, east is always closer to the trailhead (lower index).",
            "🧠", "blue_background"
        ),
    ]),
]

blocks += [
    N.h3("Code"),
    N.code(SOLUTION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = mountainArr.length()", {"code": True}), (" — cache the length; avoids repeated API calls. Each call to length() also counts toward the budget.", {})])),
    N.para(N.rich([("lo, hi = 0, n-1", {"code": True}), (" — peak search spans the entire array initially.", {})])),
    N.para(N.rich([("while lo < hi:", {"code": True}), (" — strict inequality ensures mid+1 is always a valid index (mid < hi, so mid+1 ≤ hi ≤ n-1).", {})])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — integer midpoint; no overflow risk in Python.", {})])),
    N.para(N.rich([("if get(mid) < get(mid+1): lo = mid+1", {"code": True}), (" — ascending slope detected: peak is strictly to the right of mid. Safe to skip mid.", {})])),
    N.para(N.rich([("else: hi = mid", {"code": True}), (" — descending or at the peak: mid itself could be the peak. We do NOT set hi=mid-1 because that would skip the actual peak.", {})])),
    N.para(N.rich([("peak = lo", {"code": True}), (" — at loop exit, lo == hi == the peak index.", {})])),
    N.para(N.rich([("lo, hi = 0, peak", {"code": True}), (" — reset for ascending side search.", {})])),
    N.para(N.rich([("while lo <= hi:", {"code": True}), (" — inclusive bounds for standard binary search.", {})])),
    N.para(N.rich([("if val == target: return mid", {"code": True}), (" — found on ascending side → this is the minimum index (all descending-side indices are larger).", {})])),
    N.para(N.rich([("elif val < target: lo = mid+1", {"code": True}), (" — target is larger, ascending order means it's to the right.", {})])),
    N.para(N.rich([("else: hi = mid-1", {"code": True}), (" — target is smaller, go left.", {})])),
    N.para(N.rich([("lo, hi = peak, n-1", {"code": True}), (" — reset for descending side.", {})])),
    N.para(N.rich([("elif val < target: hi = mid-1", {"code": True}), (" — FLIPPED. On descending side, smaller values are to the right. If get(mid) is too small, the target (larger) is to the LEFT. Move hi left.", {})])),
    N.para(N.rich([("else: lo = mid+1", {"code": True}), (" — FLIPPED. If get(mid) is too large, target (smaller) is to the RIGHT on descending side. Move lo right.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — target not present on either side.", {})])),
    N.divider(),
]

# ── Solution 2 (Brute Force, for context) ─────────────────────────────────
BRUTE_CODE = '''\
def findInMountainArray_brute(target: int, mountainArr) -> int:
    n = mountainArr.length()
    for i in range(n):
        if mountainArr.get(i) == target:
            return i   # returns first (leftmost) occurrence
    return -1
'''

blocks += [
    N.h2("Solution 2 — Linear Scan (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simplest possible idea: check every index from left to right, return the first match."),
        N.h4("What Doesn't Work"),
        N.para("This calls get() up to n=10,000 times. The problem enforces a call budget (approximately 100 calls per test). O(n) calls will exceed this limit and result in a wrong answer or TLE."),
        N.h4("The Key Observation"),
        N.para("The brute force is correct but not efficient enough. Mention it to the interviewer first, then offer to optimize. This shows methodical thinking."),
        N.h4("Building the Solution"),
        N.para("Just iterate i from 0 to n-1. Return i when a match is found. Because we go left to right, the first match is automatically the minimum index."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Why It's Too Slow"),
    N.para("Time: O(n) get() calls. Space: O(1). For n=10,000 and a call limit of ~100, this fails. Shows correctness but not the required efficiency."),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "get() Calls"],
        ["Triple Binary Search (optimal)", "O(log n)", "O(1)", "≤ 3 ⌈log₂ n⌉"],
        ["Linear Scan (brute force)", "O(n)", "O(1)", "Up to n"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Find Peak + Two Searches (BS on Bitonic Array)", {})])),
    N.callout(
        "When to recognise this pattern: Array is mountain/bitonic (one peak, strictly mono each side). Access is constrained via API. Need O(log n) budget. Must find the minimum index among possible matches. Key signals: 'mountain array', 'get() interface', 'minimum index'.",
        "🔎", "green_background"
    ),
    N.para("Note: 'Find Peak + Two Searches' is a specialisation of Binary Search for bitonic arrays. The sub-pattern is verified from the DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search) and personal analysis."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (peak finding + binary search on monotonic segments):"),
    N.bullet(N.rich([("852 — Peak Index in a Mountain Array", {"bold": True}), (" (Easy) — Phase 1 in isolation; pure peak-finding binary search using adjacent comparison", {})])),
    N.bullet(N.rich([("162 — Find Peak Element", {"bold": True}), (" (Medium) — Find any local peak in an array with adjacent comparison; core peak-search pattern", {})])),
    N.bullet(N.rich([("153 — Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium) — Binary search on non-standard structure with conditional direction", {})])),
    N.bullet(N.rich([("33 — Search in Rotated Sorted Array", {"bold": True}), (" (Medium) — Multi-segment binary search with comparison direction flip", {})])),
    N.bullet(N.rich([("34 — Find First and Last Position of Element in Sorted Array", {"bold": True}), (" (Medium) — Multiple binary searches on same array for boundary positions", {})])),
    N.bullet(N.rich([("1011 — Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — Binary search on answer space (different variant)", {})])),
    N.para("These problems share the core technique: decompose a non-uniformly-sorted structure into monotonic segments, then apply binary search per segment."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search. Sub-pattern: BS on Bitonic / Mountain Arrays.", "📚", "gray_background"),
]

# ── Visual Explainer embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_in_mountain_array")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion ✓")
print(f"NOTION OK {PAGE_ID}")
