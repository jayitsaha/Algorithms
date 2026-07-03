"""
gen_max_points_on_a_line.py — Regenerate Notion page for Max Points on a Line (LC #149).
Run from the Algorithms/ directory: python3 gen_max_points_on_a_line.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-810b-9a99-d778c591cc81"
SLUG    = "max_points_on_a_line"

# ── 1) Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=149,
    pattern="Math",
    subpatterns=["Count Slopes per Point"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Fix each point as anchor; group all others by reduced-fraction slope; max bucket + dups + 1 is the collinear count through that anchor.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ──
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ──
PROBLEM_STMT = (
    "Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, "
    "return the maximum number of points that lie on the same straight line.\n\n"
    "Constraints: 1 ≤ points.length ≤ 300, -10⁴ ≤ xi, yi ≤ 10⁴, all points are unique."
)

SOL1_CODE = """\
from math import gcd

def maxPoints(points):
    n = len(points)
    if n <= 2:
        return n
    ans = 0

    for i in range(n):                 # try every point as anchor
        slopes = {}                    # reduced_slope_key -> count
        dups   = 0                     # points identical to anchor
        local_max = 0

        for j in range(i + 1, n):     # only forward to avoid double-counting
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            if dx == 0 and dy == 0:   # duplicate point — on every line
                dups += 1
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g;  dy //= g
            if dx < 0:                 # normalize sign: denominator positive
                dx, dy = -dx, -dy
            key = (dy, dx)
            slopes[key] = slopes.get(key, 0) + 1
            local_max = max(local_max, slopes[key])

        ans = max(ans, local_max + dups + 1)

    return ans"""

SOL2_CODE = """\
from math import gcd
from collections import defaultdict

def maxPoints(points):
    n = len(points)
    if n <= 2:
        return n
    ans = 0

    for i in range(n):                 # try every anchor
        slope_cnt = defaultdict(int)
        dups      = 0

        for j in range(n):             # compare ALL j != i (not just j > i)
            if j == i:
                continue
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            if dx == 0 and dy == 0:
                dups += 1
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g;  dy //= g
            if dx < 0:
                dx, dy = -dx, -dy
            slope_cnt[(dy, dx)] += 1

        local_best = max(slope_cnt.values()) if slope_cnt else 0
        ans = max(ans, local_best + dups + 1)

    return ans"""

SOL3_CODE = """\
# Brute Force: try every pair of points, count collinear third points
# O(n^3) — illustrative only; TLE for large inputs

def maxPoints_brute(points):
    n = len(points)
    if n <= 2:
        return n

    def collinear(p1, p2, p3):
        # Cross product of vectors (p2-p1) and (p3-p1) == 0 means collinear
        return ((p2[0]-p1[0])*(p3[1]-p1[1]) -
                (p2[1]-p1[1])*(p3[0]-p1[0])) == 0

    ans = 2
    for i in range(n):
        for j in range(i+1, n):
            count = 2
            for k in range(n):
                if k != i and k != j and collinear(points[i], points[j], points[k]):
                    count += 1
            ans = max(ans, count)
    return ans"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# ── Solution 1: Optimal — Count Slopes per Anchor (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Count Slopes per Anchor (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Any line has infinitely many points, but every candidate optimal line must pass through "
            "at least two of our n given points. So instead of searching 'all possible lines', we only "
            "need to examine lines defined by pairs of given points — a finite O(n²) search space."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: for every pair (i,j), count how many other points satisfy the collinearity "
            "condition. That's O(n³) — too slow for n=300 (27 million operations). "
            "Float slopes: computing dy/dx as a float fails silently due to IEEE-754 precision "
            "(e.g., 1/3 as float cannot be compared reliably to another 1/3 computed differently)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Fix one point as an 'anchor'. All points collinear with the anchor on the same line "
            "share the same slope from the anchor. If we represent that slope as an exact reduced "
            "integer fraction (dy//gcd, dx//gcd), we can group points by slope using a hash map. "
            "The maximum group size + duplicates + 1 (anchor) = collinear count through anchor. "
            "Trying every point as anchor covers all possible optimal lines."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. For i=0..n-1: create a fresh slopes dict, dups=0, local_max=0.\n"
            "2. For j=i+1..n-1: compute dx, dy. If both 0 → duplicate → dups++.\n"
            "3. Otherwise: g=gcd(|dx|,|dy|); dx//=g; dy//=g. If dx<0, negate both (sign normalize).\n"
            "4. Increment slopes[(dy,dx)] and update local_max.\n"
            "5. ans = max(ans, local_max + dups + 1)."
        ),
        N.callout(
            "Analogy: You're the anchor point. You look in every direction and count how many "
            "friends are exactly in the same direction (same slope). The direction with the most "
            "friends is your best line. You then pass the 'anchor' role to each other person.",
            "🧭", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if n <= 2: return n", {"code": True}),
                   " — 0, 1, or 2 points are always collinear; return immediately."])),
    N.para(N.rich([("for i in range(n):", {"code": True}),
                   " — Try every point as the anchor. We must try all n anchors to guarantee finding the optimal line."])),
    N.para(N.rich([("slopes = {}; dups = 0; local_max = 0", {"code": True}),
                   " — Fresh state per anchor. Slopes map stores direction→count; dups counts identical points."])),
    N.para(N.rich([("for j in range(i + 1, n):", {"code": True}),
                   " — Only compare to later points (j > i). Pair (i,j) is covered when anchor=i; no need to revisit when anchor=j."])),
    N.para(N.rich([("if dx == 0 and dy == 0: dups += 1; continue", {"code": True}),
                   " — Points with zero distance are duplicates. They lie on every line through the anchor, so count separately."])),
    N.para(N.rich([("g = gcd(abs(dx), abs(dy))", {"code": True}),
                   " — Compute GCD to reduce the fraction. Both dx and dy share factor g; dividing gives the lowest-terms representation."])),
    N.para(N.rich([("if dx < 0: dx, dy = -dx, -dy", {"code": True}),
                   " — Normalize sign so denominator is non-negative. This ensures (1,-2) and (-1,2) hash to the same key."])),
    N.para(N.rich([("key = (dy, dx)", {"code": True}),
                   " — Store as tuple (numerator, denominator). Tuples are hashable in Python. Convention: (rise, run)."])),
    N.para(N.rich([("slopes[key] = slopes.get(key, 0) + 1", {"code": True}),
                   " — Increment the bucket for this slope direction."])),
    N.para(N.rich([("local_max = max(local_max, slopes[key])", {"code": True}),
                   " — Track the largest slope bucket seen for this anchor."])),
    N.para(N.rich([("ans = max(ans, local_max + dups + 1)", {"code": True}),
                   " — local_max = other collinear points; dups = identical-coord points; +1 = anchor itself. Update global best."])),
    N.divider(),
]

# ── Solution 2: All-j variant ──
blocks += [
    N.h2("Solution 2 — All-j Variant (Clearer but Slightly Slower)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same anchor strategy, but instead of comparing only j>i, compare all j≠i. "
            "This avoids the j>i optimization and is slightly easier to reason about."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This version does more comparisons per anchor (n-1 instead of n-1-i), "
            "making it O(n²) with a larger constant. For n=300 this is fine but unnecessary."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When we compare all j≠i from each anchor, we never double-count because the result "
            "(local_best + dups + 1) is computed per anchor and the global max is taken. "
            "Duplicate pairs are counted twice from each direction, but that's accounted for correctly."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Same as Solution 1, but the inner loop runs over all j from 0..n-1, skipping j==i. "
            "Use defaultdict(int) for cleaner code. The formula for ans is identical."
        ),
        N.callout("Use Solution 1 in interviews (j>i variant) — it's more efficient and shows you can optimize.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for j in range(n): if j == i: continue", {"code": True}),
                   " — Iterate all j, skip self. Simpler to write than range(i+1,n) but does O(n²) work without the triangle optimization."])),
    N.para(N.rich([("local_best = max(slope_cnt.values()) if slope_cnt else 0", {"code": True}),
                   " — Safely handle the all-duplicates edge case where slope_cnt is empty."])),
    N.divider(),
]

# ── Solution 3: Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force O(n³) — Cross Product"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "For every pair of points (p1, p2), check how many other points p3 are collinear. "
            "Three points are collinear iff the cross product of vectors (p2-p1) and (p3-p1) is zero."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This is O(n³) — three nested loops. For n=300 that's 27 million iterations plus overhead. "
            "LeetCode will TLE. Shown here only to illustrate why we need the HashMap approach."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The cross product check ((p2.x-p1.x)*(p3.y-p1.y) - (p2.y-p1.y)*(p3.x-p1.x)) == 0 "
            "gives exact integer arithmetic — no precision issues. The problem is speed, not correctness."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Fix pair (i,j). For every other k, check collinearity via cross product. Count collinear. "
            "Update global answer. Three loops, simple logic."
        ),
        N.callout("Good for verifying correctness on small inputs during debugging. Never use in an interview.", "⚠️", "red_background"),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Count Slopes per Anchor (j>i)", "O(n²)", "O(n)", "Interview pick — optimal"],
        ["Count Slopes per Anchor (all j)", "O(n²)", "O(n)", "Larger constant; same asymptotic"],
        ["Brute Force Cross Product", "O(n³)", "O(1)", "TLE for n=300"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math (Geometry / Counting)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Count Slopes per Point (anchor + hash map grouping by reduced-fraction slope)"])),
    N.callout(
        "When to recognize this pattern: (1) 'Maximum points on a line / Maximum collinear points' — any phrasing. "
        "(2) Geometric grouping where candidate objects pass through given discrete points. "
        "(3) Need exact rational arithmetic (floats won't work). "
        "(4) 'Count same property from fixed reference' → anchor + HashMap.",
        "🔎", "green_background"
    ),
    N.callout(
        "Key implementation signal: whenever you need to hash a slope/ratio exactly, always use "
        "a reduced (dy//gcd, dx//gcd) integer tuple — never a float. This applies to any problem "
        "involving lines, slopes, or ratios in competitive programming.",
        "📌", "blue_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Number of Boomerangs", {"bold": True}), " (Medium) — Fix each point as center; group others by squared distance. Same anchor + HashMap pattern but with distance instead of slope."])),
    N.bullet(N.rich([("Line Reflection", {"bold": True}), " (Medium) — Find vertical reflection axis for all points. HashMap on x-coordinates."])),
    N.bullet(N.rich([("Check If It Is a Straight Line", {"bold": True}), " (Easy) — Verify all given points collinear using the same slope-equality check; foundational version of this problem."])),
    N.bullet(N.rich([("Minimum Area Rectangle", {"bold": True}), " (Medium) — Fix pairs of points; look for complementary pairs sharing a slope. HashMap over point sets."])),
    N.bullet(N.rich([("Erect the Fence (Convex Hull)", {"bold": True}), " (Hard) — Collinearity via cross product; different goal (convex hull) but same geometric primitives."])),
    N.bullet(N.rich([("Count Points Inside a Circle", {"bold": True}), " (Medium) — Fix center; group by distance. Same anchor-grouping principle."])),
    N.bullet(N.rich([("Minimum Lines to Cover Points", {"bold": True}), " (Hard) — Extension: cover all points with at most k lines. Builds on this problem's slope grouping."])),
    N.para("These problems share the core technique: fix a reference point (anchor), compute a geometric property to every other point, group by that property using a hash map, and extract the maximum group."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math / Geometry section. Sub-pattern: Count Slopes per Point (Analysis classification — not explicitly listed in guide table).", "📚", "gray_background"),
]

# ── Interactive Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append in chunks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
