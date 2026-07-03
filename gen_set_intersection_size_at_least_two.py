"""
gen_set_intersection_size_at_least_two.py
Notion page generator for LeetCode #757 - Set Intersection Size At Least Two
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = None  # notion_page_id is null -> create new

if PAGE_ID is None:
    PAGE_ID = N.create_page("Set Intersection Size At Least Two", 757, "Hard", "🔴")
    print(f"Created new page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=757,
    pattern="Greedy",
    subpatterns=["Sort by End + Greedy"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort by end; track two rightmost chosen integers (p, q); place new integers at rightmost positions in interval to maximize future coverage.",
    icon="🔴"
)
print("Properties set.")

# 2) Wipe existing body (fresh page should be empty, but wipe to be safe)
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# 3) Build and append blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("An integer interval ", {}),
        ("[a, b]", {"code": True}),
        (" (for integers ", {}),
        ("a < b", {"code": True}),
        (") represents the set of all integers from ", {}),
        ("a", {"code": True}),
        (" to ", {}),
        ("b", {"code": True}),
        (". Find the minimum size of a set ", {}),
        ("S", {"code": True}),
        (" such that for every interval ", {}),
        ("[a, b]", {"code": True}),
        (" in the given list, the intersection of S with the interval has size at least 2. In other words, at least 2 integers from S must lie within every interval.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("intervals = [[1,3],[1,4],[2,5],[3,5]] → Output: 3. One valid minimum set is {2, 3, 5}. Check: [1,3] contains {2,3}, [1,4] contains {2,3}, [3,5] contains {3,5}, [2,5] contains {3,5}.", {})
    ])),
    N.callout("Difficulty: Hard. The constraint 'at least 2' (instead of 'at least 1') makes this harder than classic interval piercing. You cannot use the same number twice for the same interval.", "🔴", "red_background"),
    N.divider()
]

# ── Solution 1: Greedy (Interview Pick) ──
sol1_code = """def intersectionSizeTwo(intervals):
    # Sort by right endpoint asc; for same end, sort by start desc (narrower first)
    intervals.sort(key=lambda x: (x[1], -x[0]))
    p, q = -1, -1  # Two rightmost integers in S (sentinels initially)
    count = 0       # Size of S (the answer)
    for a, b in intervals:
        if p >= a:
            pass          # Both p and q are inside [a,b] — satisfied, add 0
        elif q >= a:
            p = q         # Only q is inside; add 1 new integer at b
            q = b
            count += 1
        else:
            p = b - 1     # Neither inside; add 2 new integers at b-1 and b
            q = b
            count += 2
    return count"""

blocks += [
    N.h2("Solution 1 — Greedy: Sort by End + Track Two Rightmost (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are placing 'pins' on a number line. Every interval must catch at least 2 pins. We want to minimize total pins used. The key challenge: sharing pins across multiple intervals. A pin placed toward the right end of a tight interval is more likely to also fall inside larger, later intervals."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try every possible integer and greedily pick the one that covers the most unsatisfied intervals. This is O(n * R^2) where R is the value range — far too slow. Also, left-placement of pins (choosing leftmost valid positions) wastes coverage opportunity on future intervals whose left boundaries are larger."),
        N.h4("The Key Observation"),
        N.para("Sort intervals by right endpoint. The interval that ends soonest is the most constrained — if we don't place integers there now, we'll need extra integers later. After placing integers, the two RIGHTMOST ones (p and q) are the only ones that matter for future intervals, since future intervals (with later right endpoints) must start at some value a, and only p and q could be >= a."),
        N.h4("Building the Solution"),
        N.para("1. Sort by (end, -start). 2. Track p < q (two rightmost chosen integers). 3. For each interval [a, b]: if p >= a, both are inside (add 0). If only q >= a, add one integer at b (update p=q, q=b). If neither is inside, add two integers at b-1 and b. 4. Always place at the rightmost positions to maximize future coverage."),
        N.callout("Analogy: Imagine placing thumbtacks on a map to cover all highlighted regions. You always push the tack as far right as possible in each region — that way it's most likely to also cover the next region to the right.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("intervals.sort(key=lambda x: (x[1], -x[0]))", {"code": True}), (" — Sort by right endpoint ascending. For tie in right endpoint, sort by left endpoint descending so that narrower (harder to cover) intervals come before wider ones with the same end.", {})])),
    N.para(N.rich([("p, q = -1, -1", {"code": True}), (" — Initialize the two rightmost chosen integers as sentinels (-1 is below any real interval start, so they won't be 'inside' any interval initially).", {})])),
    N.para(N.rich([("count = 0", {"code": True}), (" — Track total integers added to S (our answer).", {})])),
    N.para(N.rich([("for a, b in intervals:", {"code": True}), (" — Process each interval in sorted order.", {})])),
    N.para(N.rich([("if p >= a: pass", {"code": True}), (" — If the smaller of our two tracked integers (p) is inside [a,b], then the larger (q) is also inside (since q > p >= a). Interval is fully satisfied — add nothing.", {})])),
    N.para(N.rich([("elif q >= a:", {"code": True}), (" — Only q is inside (p < a <= q). The interval has 1 element from S; needs 1 more.", {})])),
    N.para(N.rich([("p = q; q = b; count += 1", {"code": True}), (" — Place one new integer at b (rightmost). Old q becomes new p. Count += 1.", {})])),
    N.para(N.rich([("else: p = b-1; q = b; count += 2", {"code": True}), (" — Neither p nor q is inside [a,b]. Place two integers at b-1 and b. Count += 2.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — Total size of the minimum set S.", {})])),
    N.divider()
]

# ── Solution 2: Brute Force ──
sol2_code = """def intersectionSizeTwo_brute(intervals):
    # For understanding only — too slow for large inputs
    if not intervals:
        return 0
    max_val = max(b for a, b in intervals)
    S = set()

    def uncovered():
        return any(sum(1 for x in S if a <= x <= b) < 2
                   for a, b in intervals)

    while uncovered():
        # Find integer that helps the most unsatisfied intervals
        best = max(
            range(max_val + 1),
            key=lambda x: sum(
                1 for a, b in intervals
                if a <= x <= b and sum(1 for s in S if a <= s <= b) < 2
            )
        )
        S.add(best)

    return len(S)"""

blocks += [
    N.h2("Solution 2 — Brute Force (For Understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of it as a set cover problem: which integers, when added to S, cover the most unsatisfied intervals? We greedily pick the best integer each time."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but O(n * R^2) in the worst case, where R is the value range. For R = 10^9, this is completely impractical."),
        N.h4("The Key Observation"),
        N.para("Even though this is slow, it confirms correctness. The greedy choice of 'best integer' maps to the same insight as the optimal solution: we want integers that cover as many intervals as possible."),
        N.h4("Building the Solution"),
        N.para("Repeatedly check which intervals have fewer than 2 elements from S. For each unsatisfied interval, find the integer (from 0 to max_val) that covers the most such intervals. Add it to S. Repeat until all intervals are satisfied.")
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("max_val = max(b for a,b in intervals)", {"code": True}), (" — Upper bound on integers to try.", {})])),
    N.para(N.rich([("def uncovered()", {"code": True}), (" — Returns True if any interval has fewer than 2 elements from S.", {})])),
    N.para(N.rich([("while uncovered():", {"code": True}), (" — Keep adding integers until all intervals are satisfied.", {})])),
    N.para(N.rich([("best = max(range(max_val+1), key=...)", {"code": True}), (" — Greedily pick the integer that covers the most unsatisfied intervals.", {})])),
    N.para(N.rich([("S.add(best)", {"code": True}), (" — Add chosen integer to S.", {})])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n · R²)", "O(R)"],
        ["Greedy — Sort by End (Optimal)", "O(n log n)", "O(1) extra"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort by End + Greedy", {})])),
    N.callout(
        "When to recognize this pattern: 'Minimum set of integers covering all intervals with at least k elements per interval.' Sort by right endpoint. Track k rightmost chosen integers. Place new integers at rightmost available positions within the current interval.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sort by End + Greedy):"),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Classic interval piercing with k=1; same sort-by-end greedy structure (#452)", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Sort by end, greedily keep non-overlapping intervals to minimize removals (#435)", {})])),
    N.bullet(N.rich([("Remove Covered Intervals", {"bold": True}), (" (Medium) — Sort and track max end to identify which intervals are fully covered (#1288)", {})])),
    N.bullet(N.rich([("Partition Labels", {"bold": True}), (" (Medium) — Track last occurrence as greedy right boundary; extend current partition (#763)", {})])),
    N.bullet(N.rich([("Interval List Intersections", {"bold": True}), (" (Medium) — Two pointers on two sorted interval lists to find pairwise intersections (#986)", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Greedy room allocation with min-heap tracking earliest ending meeting (#253)", {})])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), (" (Medium) — Greedy coverage of index ranges; track current and next reachable boundary (#45)", {})])),
    N.para("These problems share the core technique: sort intervals by right endpoint and make greedy decisions to satisfy each interval with minimal cost."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 16 (Greedy). Sub-Pattern: Sort by End + Greedy.", "📚", "gray_background"),
    N.divider()
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("set_intersection_size_at_least_two")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print("Notion blocks appended.")
print(f"NOTION OK {PAGE_ID}")
