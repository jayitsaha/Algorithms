"""gen_meeting_scheduler.py — Rebuild Notion page for LeetCode #1229 Meeting Scheduler."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-816b-b416-eb94de144fd8"

# ── 1. Set properties ────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1229,
    pattern="Intervals",
    subpatterns=["Two Pointers on Sorted Intervals"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort both slot lists, then advance the pointer whose slot ends first; the overlap of the current pair is [max(starts), min(ends)].",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ──────────────────────────────────────────────────────
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} old blocks.")

# ── 3. Build body ────────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the availability time slots arrays ", {}),
        ("slots1", {"code": True}),
        (" and ", {}),
        ("slots2", {"code": True}),
        (" of two people and a meeting ", {}),
        ("duration", {"code": True}),
        (", return the earliest time slot that works for both of them and is of ", {}),
        ("duration", {"code": True}),
        (" long. If there is no common time slot that satisfies the requirements, return an empty array. "
         "A time slot is represented as a pair [start, end] where start < end.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ───────────────────────────────────────────────────────────────
sol1_code = """\
def minAvailableDuration(slots1, slots2, duration):
    slots1.sort()
    slots2.sort()
    i, j = 0, 0
    while i < len(slots1) and j < len(slots2):
        lo = max(slots1[i][0], slots2[j][0])
        hi = min(slots1[i][1], slots2[j][1])
        if hi - lo >= duration:
            return [lo, lo + duration]
        if slots1[i][1] < slots2[j][1]:
            i += 1
        else:
            j += 1
    return []"""

blocks += [
    N.h2("Solution 1 — Sort + Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the earliest time window of length duration that both people are free. "
               "Equivalently: find the earliest pair of intervals (one from each person) "
               "whose intersection is at least duration long, then return the first duration minutes of that intersection."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries every pair of slots — O(n × m). For 1000 slots each that's "
               "1,000,000 comparisons. We need a smarter scan."),
        N.h4("The Key Observation"),
        N.para("If we sort both lists, we can scan them simultaneously. "
               "At any point, the slot that ends first cannot possibly overlap with any later slot "
               "in the other list (later slots start even later). So we discard the earlier-ending slot "
               "and advance that pointer. This is the same pivot used when merging two sorted lists."),
        N.h4("Building the Solution"),
        N.para("Sort both lists. Initialize i=0, j=0. Each iteration: compute the overlap "
               "[max(starts), min(ends)]. If overlap ≥ duration, return [lo, lo+duration]. "
               "Otherwise advance the pointer whose slot ends first. Repeat until one list is exhausted."),
        N.callout(
            "Analogy: Think of two scrolling tape recorders playing events in time. "
            "Whichever tape's current clip ends first, fast-forward it. "
            "Only check for overlap when both tapes are playing simultaneously.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("slots1.sort()  ", {"code": True}),
                   (" — Sort person A's slots by start time in-place. Required for two-pointer correctness.", {})])),
    N.para(N.rich([("slots2.sort()  ", {"code": True}),
                   (" — Sort person B's slots by start time in-place.", {})])),
    N.para(N.rich([("i, j = 0, 0  ", {"code": True}),
                   (" — Two independent pointers, one into each sorted list.", {})])),
    N.para(N.rich([("while i < len(slots1) and j < len(slots2)  ", {"code": True}),
                   (" — Continue only while both lists have unexamined slots.", {})])),
    N.para(N.rich([("lo = max(slots1[i][0], slots2[j][0])  ", {"code": True}),
                   (" — Overlap start: the later of the two starts. "
                    "The shared window can only begin after both people are free.", {})])),
    N.para(N.rich([("hi = min(slots1[i][1], slots2[j][1])  ", {"code": True}),
                   (" — Overlap end: the earlier of the two ends. "
                    "The shared window ends when either person's slot ends.", {})])),
    N.para(N.rich([("if hi - lo >= duration  ", {"code": True}),
                   (" — If the overlap is long enough, we found the answer.", {})])),
    N.para(N.rich([("return [lo, lo + duration]  ", {"code": True}),
                   (" — Return the earliest window of size duration, not the full overlap. "
                    "We're scheduling a meeting, not claiming the entire free block.", {})])),
    N.para(N.rich([("if slots1[i][1] < slots2[j][1]: i += 1  ", {"code": True}),
                   (" — A's slot ends sooner: advance A's pointer. "
                    "A[i] cannot overlap with any future B slots (they start even later).", {})])),
    N.para(N.rich([("else: j += 1  ", {"code": True}),
                   (" — B's slot ends sooner (or tie): advance B's pointer.", {})])),
    N.para(N.rich([("return []  ", {"code": True}),
                   (" — One list exhausted with no valid slot found.", {})])),
    N.callout(
        "Warning: Return [lo, lo+duration], NOT [lo, hi]. "
        "The overlap [lo, hi] may be longer than duration. "
        "The meeting only needs duration minutes starting at the earliest possible time lo.",
        "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2 ───────────────────────────────────────────────────────────────
sol2_code = """\
def minAvailableDuration_brute(slots1, slots2, duration):
    result = None
    for a in slots1:
        for b in slots2:
            lo = max(a[0], b[0])
            hi = min(a[1], b[1])
            if hi - lo >= duration:
                if result is None or lo < result[0]:
                    result = [lo, lo + duration]
    return result or []"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n × m)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible pair of slots — one from each person. For each pair, "
               "compute the intersection and check if it is long enough. Track the earliest valid window."),
        N.h4("What Doesn't Work Here"),
        N.para("This is the naive starting point. It is correct but O(n × m) — fine for small inputs, "
               "too slow when both lists have thousands of slots."),
        N.h4("The Key Observation"),
        N.para("No clever observation is needed: just iterate every combination. "
               "The optimization (Solution 1) comes from noticing that sorting lets you skip unnecessary pairs."),
        N.h4("Building the Solution"),
        N.para("Nested loops. For each (a, b) pair, compute lo and hi. "
               "If hi - lo >= duration, update result with the earliest lo found."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for a in slots1: for b in slots2  ", {"code": True}),
                   (" — O(n × m) pairs checked.", {})])),
    N.para(N.rich([("lo = max(a[0], b[0])  ", {"code": True}),
                   (" — Overlap start between this pair.", {})])),
    N.para(N.rich([("hi = min(a[1], b[1])  ", {"code": True}),
                   (" — Overlap end between this pair.", {})])),
    N.para(N.rich([("if hi - lo >= duration  ", {"code": True}),
                   (" — Valid overlap: record the earliest one seen.", {})])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all pairs)", "O(n × m)", "O(1)"],
        ["Sort + Two Pointers (Interview Pick)", "O(n log n + m log m)", "O(1) extra"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Intervals", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Two Pointers on Sorted Intervals — scan both sorted interval lists simultaneously, "
                    "advancing the pointer whose slot ends first at each step.", {})])),
    N.callout(
        "When to recognize this pattern: "
        "Two sorted interval lists where you need to find overlaps. "
        "'Earliest common free window', 'intersection of two interval lists', "
        "'merge two sorted event streams'. "
        "Key signal: you need to compare intervals from two separate sorted sequences.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Two Pointers on Sorted Intervals):"),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}),
                     (" (Medium) — Find all overlapping pairs from two sorted interval lists; exact same two-pointer scan. #986", {})])),
    N.bullet(N.rich([("Meeting Rooms", {"bold": True}),
                     (" (Easy) — Can one person attend all meetings? Sort + check adjacent overlaps. #252", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}),
                     (" (Medium) — Minimum rooms needed; min-heap of end times. #253", {})])),
    N.bullet(N.rich([("Merge Intervals", {"bold": True}),
                     (" (Medium) — Sort and merge overlapping intervals into disjoint ones. #56", {})])),
    N.bullet(N.rich([("Insert Interval", {"bold": True}),
                     (" (Medium) — Insert a new interval and merge any overlaps. #57", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}),
                     (" (Medium) — Minimum removals so no intervals overlap; greedy on end time. #435", {})])),
    N.bullet(N.rich([("Employee Free Time", {"bold": True}),
                     (" (Hard) — Find gaps in union of all employee schedules; heap-merge k sorted lists. #759", {})])),
    N.para("These problems share the same core technique: sort intervals by start, "
           "scan with pointers advancing the smaller-end slot."),
    N.callout("📚 Pattern: Intervals / Two Pointers on Sorted Intervals. "
              "Generalization to k people: replace two pointers with a min-heap keyed by end time.",
              "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("meeting_scheduler")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
