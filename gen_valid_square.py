"""
gen_valid_square.py — Notion page builder for LeetCode #593 Valid Square
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8157-b185-ced9bc561c10"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=593,
    pattern="Mathematics & Geometry",
    subpatterns=["Check 4 Equal Sides + 2 Diagonals"],
    tc="O(1)",
    sc="O(1)",
    key_insight="Compute all 6 pairwise squared distances; sorted pattern [s,s,s,s,2s,2s] with s>0 guarantees a square.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given four points in 2D space, ", {}),
        ("p1", {"code": True}), (", ", {}),
        ("p2", {"code": True}), (", ", {}),
        ("p3", {"code": True}), (", ", {}),
        ("p4", {"code": True}),
        (", each represented as ", {}),
        ("[x, y]", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if the four points form a valid (non-degenerate) square, and ", {}),
        ("false", {"code": True}),
        (" otherwise. The points can be given in any order.", {})
    ])),
    N.divider()
]

# ── Solution 1: Sort 6 Distances (Interview Pick) ──
sol1_code = """\
def validSquare(p1, p2, p3, p4):
    def d2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    dists = sorted([
        d2(p1,p2), d2(p1,p3), d2(p1,p4),
        d2(p2,p3), d2(p2,p4), d2(p3,p4)
    ])
    return (dists[0] > 0
            and dists[0] == dists[1]
            and dists[1] == dists[2]
            and dists[2] == dists[3]
            and dists[4] == dists[5])\
"""

blocks += [
    N.h2("Solution 1 — Sort 6 Pairwise Distances (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to verify 4 unordered points form a square. Since order is arbitrary, we cannot assume p1→p2 is a side. Instead, ask: what numbers characterise a square? Answer: the distances between its points."),
        N.h4("What Doesn't Work"),
        N.para("Trying to infer which points are 'adjacent' without knowing the order is fragile. Any of the 4!/8 = 3 distinct labellings could yield a different adjacency assignment, causing false negatives for valid squares."),
        N.h4("The Key Observation"),
        N.para("With 4 points there are exactly C(4,2) = 6 pairwise distances. For a square of side s, these 6 distances always split into exactly 4 equal 'side' distances and 2 equal 'diagonal' distances, regardless of how the points are labelled. The sorted sequence [s,s,s,s,d,d] is an invariant of any square."),
        N.h4("Building the Solution"),
        N.para("1. Compute all 6 squared distances (squared avoids floating-point from sqrt). 2. Sort them. 3. Check: first 4 equal and positive (four equal non-zero sides), last 2 equal (two equal diagonals). By Pythagoras, d = s√2 so d² = 2s² — the diagonal condition is automatically satisfied in a valid square, but we still verify it explicitly to reject rhombuses."),
        N.callout("Analogy: Think of the 6 distances as a fingerprint. A square's fingerprint is always [s,s,s,s,2s,2s] after sorting. No other quadrilateral has this exact fingerprint.", "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def d2(a, b):", {"code": True}), (" — Helper: returns squared Euclidean distance between points a and b. Using dx²+dy² avoids sqrt() and keeps everything in exact integer arithmetic.", {})])),
    N.para(N.rich([("dists = sorted([...])", {"code": True}), (" — Compute all 6 pairwise squared distances across (p1,p2),(p1,p3),(p1,p4),(p2,p3),(p2,p4),(p3,p4) and sort ascending. With 4 points that always yields 6 values = C(4,2).", {})])),
    N.para(N.rich([("dists[0] > 0", {"code": True}), (" — Non-degeneracy guard. Rejects the case where two or more points coincide (distance = 0), which would otherwise pass the equality checks trivially.", {})])),
    N.para(N.rich([("dists[0] == dists[1] == dists[2] == dists[3]", {"code": True}), (" — The four smallest distances must all be equal. These are the four sides of the square. Written as three chained equality checks.", {})])),
    N.para(N.rich([("dists[4] == dists[5]", {"code": True}), (" — The two largest distances must be equal. These are the two diagonals. This rules out rhombuses (equal sides, unequal diagonals) and ensures the shape is a square not just a rhombus.", {})])),
    N.divider()
]

# ── Solution 2: Brute Force Permutations ──
sol2_code = """\
from itertools import permutations

def validSquare(p1, p2, p3, p4):
    def d2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    def is_square(a, b, c, d):
        # a, b, c, d treated as consecutive corners
        return (d2(a,b) == d2(b,c) == d2(c,d) == d2(d,a)  # 4 equal sides
                and d2(a,c) == d2(b,d)                     # 2 equal diagonals
                and d2(a,b) > 0)                            # non-degenerate

    return any(is_square(*perm) for perm in permutations([p1, p2, p3, p4]))\
"""

blocks += [
    N.h2("Solution 2 — Brute Force: Try All Orderings"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A square traversed corner-by-corner has: 4 equal consecutive sides (a→b, b→c, c→d, d→a) and 2 equal diagonals (a→c, b→d). If we could label the corners correctly we could check directly."),
        N.h4("What Doesn't Work"),
        N.para("We don't know the correct labelling, so trying a fixed ordering (p1→p2→p3→p4) will miss valid squares where the input happens to label corners in a scrambled order."),
        N.h4("The Key Observation"),
        N.para("There are only 4! = 24 orderings of 4 points (or 3 geometrically distinct ones up to rotation/reflection). We can simply try all 24 and return True if any ordering passes the square check."),
        N.h4("Building the Solution"),
        N.para("For each permutation (a,b,c,d), check: d2(a,b)==d2(b,c)==d2(c,d)==d2(d,a) (4 equal sides) and d2(a,c)==d2(b,d) (diagonals equal) and d2(a,b)>0 (non-degenerate). Return True if any permutation passes."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("permutations([p1, p2, p3, p4])", {"code": True}), (" — Generates all 24 orderings of the 4 input points.", {})])),
    N.para(N.rich([("d2(a,b)==d2(b,c)==d2(c,d)==d2(d,a)", {"code": True}), (" — Checks that the four consecutive side lengths are equal in this corner ordering.", {})])),
    N.para(N.rich([("d2(a,c)==d2(b,d)", {"code": True}), (" — Checks that the two diagonals (a↔c and b↔d) are equal. In a square a and c are opposite corners, as are b and d.", {})])),
    N.callout("Trade-off: Solution 2 is more intuitive for beginners (explicit geometry) but is wordier. Solution 1 is cleaner and preferred in interviews. Both are O(1) since all inputs are exactly 4 points.", "💡", "green_background"),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sort 6 Distances (Interview Pick)", "O(1)", "O(1)"],
        ["Brute Force — All Permutations", "O(1)", "O(1)"],
    ]),
    N.para("Both solutions are truly O(1) — the input is always exactly 4 points, so the number of operations is fixed regardless of coordinate values."),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Mathematics & Geometry (Section 19 of DSA Patterns Guide)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Check 4 Equal Sides + 2 Diagonals", {})])),
    N.callout(
        "When to recognise this pattern: The problem gives k unordered points and asks if they form a specific geometric shape (square, rectangle, rhombus). When coordinates are integers, always use squared distances. Compute all C(k,2) pairwise distances and check the expected split pattern after sorting.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Check-Distances geometric technique:"),
    N.bullet(N.rich([("Minimum Area Rectangle", {"bold": True}), (" (Medium) — Hash set of points; for each pair of points check if they can be a diagonal of an axis-aligned rectangle (#939)", {})])),
    N.bullet(N.rich([("Minimum Area Rectangle II", {"bold": True}), (" (Medium) — Non-axis-aligned: use center + diagonal length to find rectangles of any orientation (#963)", {})])),
    N.bullet(N.rich([("Valid Triangle Number", {"bold": True}), (" (Medium) — Sort side lengths + two pointers to count valid triangles; triangle inequality check (#611)", {})])),
    N.bullet(N.rich([("Max Points on a Line", {"bold": True}), (" (Hard) — Pairwise slope frequency counting; geometry on point sets (#149)", {})])),
    N.bullet(N.rich([("Check if It Is a Straight Line", {"bold": True}), (" (Easy) — Cross product collinearity check for a set of points (#1232)", {})])),
    N.para("These problems share the core technique: reduce geometry to distance or slope comparisons between point pairs, use squared distances to avoid floating-point, and rely on algebraic invariants (equal sides/diagonals) rather than coordinate geometry."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 19 — Mathematics & Geometry, Sub-pattern: Check 4 Equal Sides + 2 Diagonals", "📚", "gray_background"),
    N.divider()
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_square")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
