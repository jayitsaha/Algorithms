"""
gen_minimum_interval_to_include_each_query.py
Regenerate Notion page for LeetCode #1851 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ef-bacc-e8b3e2df8f5c"

print("Step 1: Set properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1851,
    pattern="Advanced Data Structures",
    subpatterns=["Sort + Heap"],
    tc="O((n+q) log n)",
    sc="O(n+q)",
    key_insight="Sort intervals by l, sort queries with orig index; sweep with a min-heap keyed by interval size; lazy-evict expired entries.",
    icon="🔴"
)
print("  properties set.")

print("Step 2: Wipe old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"  deleted {deleted} blocks.")

print("Step 3: Build new body...")
blocks = []

# ── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a 2D array ", {}),
        ("intervals", {"code": True}),
        (" where ", {}),
        ("intervals[i] = [l, r]", {"code": True}),
        (", and an array ", {}),
        ("queries", {"code": True}),
        (". For each query value ", {}),
        ("q", {"code": True}),
        (", find the ", {}),
        ("smallest interval (by size = r − l + 1)", {"bold": True}),
        (" that contains ", {}),
        ("q", {"code": True}),
        (" (i.e., l ≤ q ≤ r). Return an array of answers; use −1 if no interval contains the query.", {})
    ])),
    N.callout(
        N.rich([("Example: ", {"bold": True}),
                ("intervals=[[1,4],[2,4],[3,6],[4,4]], queries=[2,3,4,5]  →  answers=[3,3,1,4]", {"code": True})]),
        "📌", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Brute Force ────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force (O(n×q)) — for understanding only"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each query q, we need the smallest interval that contains q. The straightforward reading: scan every interval, check if l ≤ q ≤ r, track minimum size."),
        N.h4("What Doesn't Work"),
        N.para("With n, q up to 10^5, O(n × q) = 10^10 operations. This exceeds time limits by ~10000×. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("This brute force is still correct — just too slow. Understanding it clearly helps motivate the optimal approach."),
        N.h4("Building the Solution"),
        N.para("For each query, iterate all intervals, keep a running minimum of size for those that contain the query."),
        N.callout("Analogy: checking every item on a shelf for each customer instead of organizing the shelf first.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minInterval_brute(intervals, queries):\n"
        "    ans = []\n"
        "    for q in queries:\n"
        "        best = float('inf')\n"
        "        for l, r in intervals:\n"
        "            if l <= q <= r:\n"
        "                best = min(best, r - l + 1)\n"
        "        ans.append(best if best < float('inf') else -1)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for q in queries:", {"code": True}), (" — iterate over each query value.", {})])),
    N.para(N.rich([("for l, r in intervals:", {"code": True}), (" — check every interval for containment.", {})])),
    N.para(N.rich([("if l <= q <= r:", {"code": True}), (" — the interval covers the query value.", {})])),
    N.para(N.rich([("best = min(best, r-l+1)", {"code": True}), (" — track smallest valid size.", {})])),
    N.para(N.rich([("ans.append(...)", {"code": True}), (" — append best size or −1.", {})])),
    N.divider(),
]

# ── Solution 2: Sort + Min-Heap (Optimal) ─────────────────────
blocks += [
    N.h2("Solution 2 — Sort + Min-Heap Sweep (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'which intervals cover this query?', flip the perspective: process queries in sorted order so we can incrementally ADD intervals as the query value grows, and REMOVE intervals as they expire."),
        N.h4("What Doesn't Work"),
        N.para("Random order means we can't share work between nearby queries. Sorting is the key that enables the sweep."),
        N.h4("The Key Observation"),
        N.para("If we sort queries and intervals both ascending, then for consecutive queries q1 ≤ q2: every interval added for q1 is still a candidate for q2 (since l ≤ q1 ≤ q2). We only need to ADD new intervals and EVICT expired ones — never re-scan."),
        N.h4("Building the Solution"),
        N.para("Sort intervals by l. Sort queries with original indices. Sweep left to right: for each query, push intervals with l ≤ q, pop expired intervals (r < q) from heap top. Heap is keyed by size → top is the answer."),
        N.callout("Analogy: A store that arranges customers by budget (queries sorted) and products by release date (intervals sorted by l). As budget grows you add more products; you retire products that are too small.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Offline Sweep with Lazy Deletion"),
    N.para(N.rich([
        ("Technique: ", {"bold": True}),
        ("Offline interval queries", {}),
        (". Sort both arrays and sweep, maintaining a heap of 'active' intervals. Lazy deletion means we leave expired entries in the heap and only discard them when they reach the top (amortized O(1) per interval).", {})
    ])),
    N.code(
        "# Template: offline interval sweep\n"
        "# 1. Sort intervals by start\n"
        "# 2. Sort queries (keep orig idx)\n"
        "# 3. Min-heap of (metric_to_minimize, right_endpoint)\n"
        "# 4. For each sorted query:\n"
        "#    a. Add intervals with l <= q\n"
        "#    b. Lazy-evict: pop while heap[0].right < q\n"
        "#    c. heap top = answer"
    ),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("After eviction, every heap entry satisfies l ≤ q (was added) and r ≥ q (not evicted). The min-heap top is the smallest such interval.", {})
    ])),
    N.para(N.rich([
        ("Generalization: ", {"bold": True}),
        ("Works for any 'best interval per query' problem. Change the heap key to optimize a different metric (e.g., key by r for earliest-ending interval).", {})
    ])),
    N.h3("Code"),
    N.code(
        "import heapq\n"
        "\n"
        "def minInterval(intervals, queries):\n"
        "    intervals.sort()                   # sort by l\n"
        "    sorted_q = sorted(enumerate(queries), key=lambda x: x[1])  # sort queries + orig idx\n"
        "    ans = [-1] * len(queries)          # default: -1\n"
        "    heap = []                          # min-heap of (size, right_endpoint)\n"
        "    i = 0                              # interval pointer (never moves backward)\n"
        "\n"
        "    for orig_idx, q in sorted_q:\n"
        "        # Add all intervals that have started\n"
        "        while i < len(intervals) and intervals[i][0] <= q:\n"
        "            l, r = intervals[i]\n"
        "            heapq.heappush(heap, (r - l + 1, r))  # key=size, store r for eviction\n"
        "            i += 1\n"
        "        # Lazy-evict expired intervals (right end < query)\n"
        "        while heap and heap[0][1] < q:\n"
        "            heapq.heappop(heap)\n"
        "        # Record answer\n"
        "        if heap:\n"
        "            ans[orig_idx] = heap[0][0]\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort()", {"code": True}), (" — sort by l (left endpoint); Python sorts tuples lexicographically, so first by l, then r.", {})])),
    N.para(N.rich([("sorted_q = sorted(enumerate(queries), ...)", {"code": True}), (" — attach original index to each query value, then sort by value ascending.", {})])),
    N.para(N.rich([("ans = [-1] * len(queries)", {"code": True}), (" — pre-fill with -1; will be overwritten if a valid interval is found.", {})])),
    N.para(N.rich([("heap = []", {"code": True}), (" — Python's heapq is a min-heap. Each entry: (size, right_endpoint).", {})])),
    N.para(N.rich([("i = 0", {"code": True}), (" — pointer into sorted intervals; monotonically increases — each interval added exactly once.", {})])),
    N.para(N.rich([("while i < len(intervals) and intervals[i][0] <= q:", {"code": True}), (" — add every interval whose left endpoint ≤ current query.", {})])),
    N.para(N.rich([("heapq.heappush(heap, (r-l+1, r))", {"code": True}), (" — push (size, right). Size is the key; right is stored for eviction testing.", {})])),
    N.para(N.rich([("while heap and heap[0][1] < q:", {"code": True}), (" — if heap top's right endpoint is strictly less than q, that interval is expired.", {})])),
    N.para(N.rich([("heapq.heappop(heap)", {"code": True}), (" — discard. The interval [l, r] with r < q cannot contain q.", {})])),
    N.para(N.rich([("ans[orig_idx] = heap[0][0]", {"code": True}), (" — heap[0][0] is the smallest size among all valid intervals covering q. Write to original position.", {})])),
    N.callout(
        N.rich([("⚠️ Common Mistake: ", {"bold": True}), ("Push (r, l, r) instead of (r-l+1, r). This makes the heap return the interval ending earliest, not the smallest. Always key by the quantity you want minimized.", {})]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",          "Space"],
        ["Brute Force",          "O(n × q)",       "O(q)"],
        ["Sort + Min-Heap Sweep", "O((n+q) log n)", "O(n+q)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Advanced Data Structures", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Heap (offline sweep with lazy deletion)", {})])),
    N.callout(
        N.rich([("When to recognize: ", {"bold": True}),
                ("'for each query find the best interval containing it', n and q both large (10^5), offline processing OK → sort both arrays + min-heap sweep + lazy deletion.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same offline sweep + heap technique:"),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — sweep line, min-heap on end times to count concurrent meetings", {})])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), (" (Hard) — sweep line + max-heap; add buildings on enter, remove on exit", {})])),
    N.bullet(N.rich([("Number of Flowers in Full Bloom", {"bold": True}), (" (Hard) — sort + binary search for interval containment queries", {})])),
    N.bullet(N.rich([("My Calendar III", {"bold": True}), (" (Hard) — interval overlap count via sorted structure", {})])),
    N.bullet(N.rich([("Falling Squares", {"bold": True}), (" (Hard) — coordinate compression + sweep for stacked interval queries", {})])),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}), (" (Medium) — two-pointer sweep over two sorted interval arrays", {})])),
    N.bullet(N.rich([("Remove Interval", {"bold": True}), (" (Medium) — interval manipulation with linear sweep", {})])),
    N.para("These problems share the core pattern: sort intervals by start, process events in order, maintain a heap of 'active' intervals."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Advanced Data Structures section, Sort + Heap sub-pattern.", "📚", "gray_background"),
]

# ── Visual Explainer embed ─────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_interval_to_include_each_query")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
