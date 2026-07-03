"""
gen_employee_free_time.py
Regenerate the Notion page for Employee Free Time (LeetCode #759).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815f-8451-c521feb6f22d"
SLUG    = "employee_free_time"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=759,
    pattern="Advanced Data Structures",
    subpatterns=["Merge Intervals", "K-Way Merge (Heap)"],
    tc="O(N log K)",
    sc="O(K)",
    key_insight="Gaps in the union of all work intervals = free time; use a min-heap for K-way merge to process intervals in global sorted order in O(N log K).",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("We are given a list of ", {}),
        ("schedule", {"code": True}),
        (", where ", {}),
        ("schedule[i]", {"code": True}),
        (" is a list of non-overlapping ", {}),
        ("Interval", {"code": True}),
        (" objects for the i-th employee, sorted by start time. "
         "Return a list of finite intervals representing the "
         "free time common to all employees — gaps where nobody is working.", {})
    ])),
    N.para(N.rich([
        ("Example: 3 employees with schedules [[1,3],[6,7]], [[2,4]], [[2,5],[9,12]] "
         "→ Answer: [[5,6],[7,9]]. The union of all work is [1,5]∪[6,7]∪[9,12]; "
         "the gaps are [5,6] and [7,9].", {"italic": True})
    ])),
    N.callout(
        "Key observation: free time = gaps in the UNION of all work intervals — not the "
        "intersection of free periods. We don't care which employee is working, only that "
        "someone is.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Solution 1: K-Way Merge (Heap) ─────────────────────────────────────────
SOLUTION_1_CODE = """\
import heapq

def employeeFreeTime(schedule):
    # Min-heap entries: (start, end, emp_index, interval_index)
    heap = []
    for i, emp in enumerate(schedule):
        iv = emp[0]
        heapq.heappush(heap, (iv.start, iv.end, i, 0))

    result = []

    # Bootstrap: pop globally earliest interval, set prev_end
    s, e, ei, ii = heapq.heappop(heap)
    if ii + 1 < len(schedule[ei]):
        nxt = schedule[ei][ii + 1]
        heapq.heappush(heap, (nxt.start, nxt.end, ei, ii + 1))
    prev_end = e

    while heap:
        s, e, ei, ii = heapq.heappop(heap)
        if s > prev_end:          # gap found — nobody working in [prev_end, s]
            result.append(Interval(prev_end, s))
        prev_end = max(prev_end, e)  # extend coverage (handles nested intervals)
        if ii + 1 < len(schedule[ei]):
            nxt = schedule[ei][ii + 1]
            heapq.heappush(heap, (nxt.start, nxt.end, ei, ii + 1))

    return result
"""

blocks += [
    N.h2("Solution 1 — K-Way Merge with Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need gaps in the union of multiple sorted interval lists. "
               "Think of it as: if we could see all intervals sorted globally "
               "by start time, gaps between consecutive merged segments are free time."),
        N.h4("What Doesn't Work"),
        N.para("Naive approach: flatten all N intervals into one list and sort — O(N log N). "
               "This is correct but ignores that each employee's schedule is already sorted. "
               "We're throwing away the pre-sorted structure and re-sorting from scratch."),
        N.h4("The Key Observation"),
        N.para("Each employee's schedule is a sorted list. To get the globally sorted order "
               "across K sorted lists without re-sorting everything, use a min-heap of size K. "
               "This is the K-way merge pattern — the same idea as merging K sorted linked lists."),
        N.h4("Building the Solution"),
        N.para("1. Push the first interval from each employee into the heap (size K). "
               "2. Pop the global minimum (earliest start). Set prev_end = its end. "
               "Push next from that employee. "
               "3. Repeat: pop minimum. If start > prev_end, record gap [prev_end, start]. "
               "Update prev_end = max(prev_end, end). Push next from same employee. "
               "4. Stop when heap empties."),
        N.callout(
            "Analogy: imagine K people each handing you their calendar pages in order. "
            "You always grab the page with the earliest date. A heap lets you always "
            "know who has the next earliest page without looking at all K stacks.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("heap = []", {"code": True}), " — Initialize the min-heap. Will hold at most K entries simultaneously."])),
    N.para(N.rich([("heapq.heappush(heap, (iv.start, iv.end, i, 0))", {"code": True}), " — Seed with first interval from each employee. Tuples compare lexicographically, so heap sorts by start time."])),
    N.para(N.rich([("s, e, ei, ii = heapq.heappop(heap)", {"code": True}), " — Bootstrap: pop the globally earliest interval before the main loop to set prev_end without special-casing None."])),
    N.para(N.rich([("heapq.heappush(heap, (nxt.start, nxt.end, ei, ii + 1))", {"code": True}), " — After each pop, push the next interval from that same employee (if any). Heap stays size ≤ K."])),
    N.para(N.rich([("prev_end = e", {"code": True}), " — Rightmost boundary of all working intervals seen so far. The key tracking variable."])),
    N.para(N.rich([("if s > prev_end:", {"code": True}), " — Gap condition: the new interval starts after our current coverage ends — nobody worked in [prev_end, s]."])),
    N.para(N.rich([("result.append(Interval(prev_end, s))", {"code": True}), " — Record the free-time window. We use prev_end (not prev_start) because that is where coverage ended."])),
    N.para(N.rich([("prev_end = max(prev_end, e)", {"code": True}), " — Extend coverage. max() is critical for nested intervals: if [2,10] comes after [1,5], prev_end stays 10, not shrinks to 5."])),
    N.divider(),
]

# ── Solution 2: Flatten + Sort ─────────────────────────────────────────────
SOLUTION_2_CODE = """\
def employeeFreeTime(schedule):
    # Flatten all intervals from all employees into one list
    all_ivs = sorted(
        [iv for emp in schedule for iv in emp],
        key=lambda x: x.start
    )
    result = []
    prev_end = all_ivs[0].end   # bootstrap with first interval's end
    for iv in all_ivs[1:]:
        if iv.start > prev_end:   # gap found
            result.append(Interval(prev_end, iv.start))
        prev_end = max(prev_end, iv.end)   # extend coverage
    return result
"""

blocks += [
    N.h2("Solution 2 — Flatten and Sort (O(N log N), Simpler)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Ignore the per-employee structure. Treat all N intervals as one big unordered pool. Sort them by start time, then sweep to find gaps."),
        N.h4("What Doesn't Work"),
        N.para("Without sorting, we can't tell if the next interval creates a gap or overlaps. Sorting is the minimum needed to detect gaps."),
        N.h4("The Key Observation"),
        N.para("Once sorted by start time, the merge-intervals algorithm works: maintain prev_end, and any interval whose start exceeds prev_end is a gap."),
        N.h4("Building the Solution"),
        N.para("Flatten all intervals with a list comprehension, sort by start. Bootstrap prev_end with the first end. Sweep: gap if start > prev_end; always update prev_end = max(prev_end, end)."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("sorted([iv for emp in schedule for iv in emp], key=...)", {"code": True}), " — Flatten with a nested list comprehension, then sort by start. O(N log N)."])),
    N.para(N.rich([("prev_end = all_ivs[0].end", {"code": True}), " — Bootstrap: the first interval's end is our starting coverage boundary."])),
    N.para(N.rich([("if iv.start > prev_end:", {"code": True}), " — Same gap condition as Solution 1. The difference: here we sorted everything upfront instead of using a heap."])),
    N.para(N.rich([("prev_end = max(prev_end, iv.end)", {"code": True}), " — Merge overlapping or nested intervals by keeping the maximum right boundary."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Flatten + Sort", "O(N log N)", "O(N)", "Simple; ignores pre-sorted property"],
        ["K-Way Merge (Heap) ✓", "O(N log K)", "O(K)", "Optimal; K = employees, never > N intervals in heap"],
    ]),
    N.callout(
        "N = total intervals across all employees. K = number of employees. "
        "Since K ≤ N, O(N log K) ≤ O(N log N). When K ≪ N (e.g., 10 employees, 1M intervals), "
        "the heap is dramatically faster: log 10 = 3.3 comparisons vs log(1M) = 20 per step.",
        "📊", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Advanced Data Structures"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Merge Intervals + K-Way Merge (Heap)"])),
    N.callout(
        "When to recognize: (1) 'K sorted sources' + 'find global order' → K-way merge with min-heap. "
        "(2) 'Find gaps or free windows in interval union' → merge-intervals sweep. "
        "(3) 'Already sorted per source' → exploit pre-sorted structure, don't re-sort everything. "
        "(4) Problem says heap size K stays constant → O(log K) not O(log N) per step.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Merge Intervals + K-Way Merge):"),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}), " (Medium) — Core pattern: single list, sort by start, sweep to merge (#56)"])),
    N.bullet(N.rich([("Merge K Sorted Lists", {"bold": True}), " (Hard) — Same min-heap K-way merge, linked lists instead of intervals (#23)"])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), " (Medium) — Min-heap on end times to track max concurrent meetings (#253)"])),
    N.bullet(N.rich([("Smallest Range Covering K Lists", {"bold": True}), " (Hard) — K-way merge extended: minimum window spanning all K lists (#632)"])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}), " (Medium) — Merge after inserting one new interval into sorted list (#57)"])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — Greedy removal with sorted sweep; related gap logic (#435)"])),
    N.para("These problems share the core techniques: sorting/merging by start time and tracking the rightmost coverage boundary (prev_end)."),
    N.callout("Sub-Pattern Source: Analysis (Advanced Data Structures / Merge Intervals / K-Way Merge). Verified against DSA_Patterns_and_SubPatterns_Guide.md.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the K-way merge algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
