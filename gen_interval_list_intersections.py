"""
gen_interval_list_intersections.py
Rebuild Notion page for LeetCode #986 Interval List Intersections in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8123-bf59-e11d734b0964"
SLUG    = "interval_list_intersections"

print(f"[1/4] Setting properties on {PAGE_ID} ...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=986,
    pattern="Intervals",
    subpatterns=["Two Pointers on Sorted Intervals"],
    tc="O(m+n)",
    sc="O(k) output",
    key_insight="Advance the pointer whose interval ends first; it cannot contribute to future overlaps.",
    icon="🟡"
)
print("     Properties set OK.")

print("[2/4] Wiping old content ...")
deleted = N.wipe_page(PAGE_ID)
print(f"     Deleted {deleted} blocks.")

print("[3/4] Building body blocks ...")

PROBLEM_STATEMENT = (
    "Given two lists of closed intervals, firstList and secondList, where "
    "firstList[i] = [start_i, end_i] and secondList[j] = [start_j, end_j]. "
    "Each list of intervals is pairwise disjoint and in sorted order. "
    "Return the intersection of these two interval lists. "
    "A closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b. "
    "The intersection of two closed intervals is a set of real numbers that is either empty, "
    "or can be represented as a closed interval. "
    "Example: firstList=[[0,2],[5,10],[13,23],[24,25]], "
    "secondList=[[1,5],[8,12],[15,24],[25,26]] → [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]."
)

SOL1_CODE = '''\
def intervalIntersection(firstList, secondList):
    A, B = firstList, secondList
    i, j, res = 0, 0, []
    while i < len(A) and j < len(B):
        # Intersection candidate: later start, earlier end
        lo = max(A[i][0], B[j][0])
        hi = min(A[i][1], B[j][1])
        # Valid overlap (closed intervals: use <=, not <)
        if lo <= hi:
            res.append([lo, hi])
        # Advance the pointer whose interval ends first
        if A[i][1] <= B[j][1]:
            i += 1
        else:
            j += 1
    return res\
'''

SOL2_CODE = '''\
def intervalIntersection_brute(A, B):
    """O(m*n) brute force — checks every pair, ignores sorted order."""
    res = []
    for a in A:
        for b in B:
            lo = max(a[0], b[0])
            hi = min(a[1], b[1])
            if lo <= hi:
                res.append([lo, hi])
    return res\
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1 ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "You have two sorted streams of intervals. You want every time window "
            "that appears in both. Think of it as merging two sorted sequences "
            "(like merge sort's merge step) — except instead of picking the smaller "
            "element, you're checking whether the current two intervals overlap."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A nested loop (brute force) checks every pair of intervals from A and B: "
            "O(m·n). For m=n=10^4 that's 10^8 operations — too slow. It also ignores "
            "the sorted order, which is free information we should exploit."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Two closed intervals [a,b] and [c,d] overlap iff max(a,c) <= min(b,d). "
            "The intersection is [max(a,c), min(b,d)]. After recording any intersection "
            "(or noting none exists), the interval that ends first is 'exhausted' — "
            "all future intervals in the other list start no earlier than its end, "
            "so it can never contribute to another overlap. Advance that pointer."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Two pointers i=0 (into A) and j=0 (into B). "
            "2. Compute lo=max(A[i][0], B[j][0]) and hi=min(A[i][1], B[j][1]). "
            "3. If lo <= hi, record [lo, hi]. "
            "4. Advance whichever pointer's interval has the smaller end. "
            "5. Repeat until either list is exhausted."
        ),
        N.callout(
            "Analogy: Two train schedules side by side. You run your finger down both "
            "simultaneously. When trains overlap, note the overlap. Whichever train "
            "departs first, flip to its next entry. You never need to look backward.",
            "🚂", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("A, B = firstList, secondList", {"code": True}), " — short aliases for readability."])),
    N.para(N.rich([("i, j, res = 0, 0, []", {"code": True}), " — initialize two pointers (one per list) and empty result."])),
    N.para(N.rich([("while i < len(A) and j < len(B):", {"code": True}), " — stop when either list is exhausted; remaining intervals in the other have no partner."])),
    N.para(N.rich([("lo = max(A[i][0], B[j][0])", {"code": True}), " — intersection must start at or after both intervals start; take the later start."])),
    N.para(N.rich([("hi = min(A[i][1], B[j][1])", {"code": True}), " — intersection must end at or before both intervals end; take the earlier end."])),
    N.para(N.rich([("if lo <= hi:", {"code": True}), " — valid overlap test. Use <= (not <) because intervals are closed — a single shared point is a valid intersection."])),
    N.para(N.rich([("res.append([lo, hi])", {"code": True}), " — record the intersection interval."])),
    N.para(N.rich([("if A[i][1] <= B[j][1]: i += 1 else: j += 1", {"code": True}), " — advance the pointer whose interval ends first. That interval is spent and cannot overlap future intervals in the other list."])),
    N.para(N.rich([("return res", {"code": True}), " — final list of all k intersections. Time O(m+n), auxiliary space O(1), output space O(k)."])),
    N.divider(),
]

# ── Solution 2 ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force O(m·n) (for comparison)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Check every possible pair of intervals (one from A, one from B) and keep those that overlap."),
        N.h4("What Doesn't Work"),
        N.para("This ignores the sorted structure. For large m and n this is too slow (O(m·n))."),
        N.h4("The Key Observation"),
        N.para("The intersection formula max(starts)/min(ends) still applies — we just apply it naively to every pair."),
        N.h4("Building the Solution"),
        N.para("Nested loop: for each a in A, for each b in B, compute lo/hi, record if lo<=hi."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for a in A: for b in B:", {"code": True}), " — O(m·n) nested iteration, no use of sorted order."])),
    N.para(N.rich([("lo, hi = max(a[0],b[0]), min(a[1],b[1])", {"code": True}), " — same intersection formula as the optimal solution."])),
    N.para(N.rich([("if lo <= hi: res.append([lo, hi])", {"code": True}), " — record valid intersections. Correct but too slow for large inputs."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two Pointers (optimal)", "O(m+n)", "O(k) output"],
        ["Brute Force", "O(m·n)", "O(k) output"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Intervals"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Pointers on Sorted Intervals"])),
    N.callout(
        "When to recognize this pattern: Two sorted lists of intervals + 'find what they share' "
        "or 'find when both are busy/free simultaneously'. Also: advance-by-end-pointer pattern "
        "when iterating through merged sorted interval streams.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (two-pointer linear merge on sorted intervals):"),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), " (Medium) — Sort then greedily merge overlapping intervals into one list (#56)"])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), " (Medium) — Insert new interval into sorted non-overlapping list and merge (#57)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Min rooms = max simultaneous overlaps; two-pointer on sorted events (#253)"])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}), " (Hard) — Find gaps across N sorted employee schedules; multi-list merge (#759)"])),
    N.bullet(N.rich([("Meeting Scheduler", {"bold": True}), " (Medium) — Find first available slot for two people — direct application of this problem (#1229)"])),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), " (Medium) — Book events without double-booking; interval overlap detection online (#729)"])),
    N.para("These problems all share the core technique: sorted interval streams + advance-by-end two-pointer."),
    N.divider(),
]

# ── Embed ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"     {len(blocks)} blocks assembled. Appending ...")
N.append_blocks(PAGE_ID, blocks)
print("     Blocks appended OK.")

print("[4/4] Verifying final block count ...")
count = len(N.get_children(PAGE_ID))
print(f"     Notion page now has {count} top-level blocks.")

print(f"\nNOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | blocks={count}")
