"""
gen_perfect_rectangle.py — Rebuild Perfect Rectangle (LC #391) Notion page in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8190-8844-f81bc72e06f2"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=391,
    pattern="Advanced Data Structures",
    subpatterns=["Corner Count + Area Check"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Sum areas to check for gaps/overlaps; XOR-toggle each rectangle's 4 corners — only the 4 bounding-box outer corners survive with odd count.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old body ──
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3. Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(
        "Given a list of axis-aligned rectangles, each described as [x1, y1, x2, y2] where "
        "(x1, y1) is the bottom-left corner and (x2, y2) is the top-right corner, return true "
        "if all the rectangles together form an exact cover of a rectangular region — "
        "no gaps and no overlaps."
    ),
    N.divider(),
]

# ── Solution 1 — Optimal ──
sol1_code = """\
def isRectangleCover(rectangles):
    total_area = 0
    corners = set()
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for x1, y1, x2, y2 in rectangles:
        total_area += (x2 - x1) * (y2 - y1)
        min_x, max_x = min(min_x, x1), max(max_x, x2)
        min_y, max_y = min(min_y, y1), max(max_y, y2)
        for pt in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
            if pt in corners:
                corners.remove(pt)   # even count: cancel out
            else:
                corners.add(pt)       # odd count: survives

    expected = {
        (min_x, min_y), (min_x, max_y),
        (max_x, min_y), (max_x, max_y),
    }
    bbox_area = (max_x - min_x) * (max_y - min_y)
    return corners == expected and total_area == bbox_area
"""

blocks += [
    N.h2("Solution 1 — Corner Count + Area Check (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "You want to verify that n rectangles tile a larger rectangle perfectly — no gaps, "
            "no overlaps. Think of it as two separate questions: (1) Do the areas add up? "
            "(2) Are the rectangles structurally arranged correctly?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Checking all O(n²) pairs for overlaps and then verifying union-equals-bounding-box "
            "is correct but too slow. An O(n) solution must summarize information without pair-wise "
            "comparison."
        ),
        N.h4("The Key Observation"),
        N.para(
            "In a perfect tiling, every interior corner point is shared by exactly 2 or 4 "
            "rectangles — always an even count, so it cancels out. Only the 4 extreme corners "
            "of the overall bounding box appear exactly once each (odd count — they survive). "
            "This is a parity observation: XOR is the natural tool."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Accumulate total area. 2. Track bounding box (min/max coordinates). "
            "3. XOR-toggle each rectangle's 4 corners: add if new, remove if already seen. "
            "4. After all rectangles, verify that the toggle-set contains exactly the 4 outer "
            "bounding-box corners AND total_area equals bounding-box area."
        ),
        N.callout(
            "Analogy: Think of each rectangle's corner as a vote. Interior corners get paired "
            "votes that cancel. Only the 4 lone outer corners win the election.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, lang="python"),
    N.h3("Line by Line"),
    N.para(N.rich([("total_area = 0", {"code": True}), " — running sum of all sub-rectangle areas."])),
    N.para(N.rich([("corners = set()", {"code": True}), " — XOR-toggle set: odd-count corners survive; even-count corners disappear."])),
    N.para(N.rich([("min_x = min_y = float('inf')", {"code": True}), " — bounding box trackers initialized to extremes."])),
    N.para(N.rich([("for x1, y1, x2, y2 in rectangles:", {"code": True}), " — single pass over every rectangle."])),
    N.para(N.rich([("total_area += (x2-x1)*(y2-y1)", {"code": True}), " — add this rectangle's area."])),
    N.para(N.rich([("min_x, max_x = min(...), max(...)", {"code": True}), " — expand bounding box to encompass this rectangle."])),
    N.para(N.rich([("for pt in [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]:", {"code": True}), " — iterate over all 4 corners of the current rectangle."])),
    N.para(N.rich([("if pt in corners: corners.remove(pt)", {"code": True}), " — corner seen before: even total → cancel (remove)."])),
    N.para(N.rich([("else: corners.add(pt)", {"code": True}), " — first occurrence: odd count → survives (add)."])),
    N.para(N.rich([("expected = {(min_x,min_y), ...}", {"code": True}), " — the 4 extreme outer corners of the bounding box."])),
    N.para(N.rich([("return corners == expected and total_area == bbox_area", {"code": True}), " — both structural and quantitative conditions must hold."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
sol2_code = """\
def isRectangleCover_brute(rectangles):
    # Check all pairs for overlap
    def overlaps(r1, r2):
        x1, y1, x2, y2 = r1
        a1, b1, a2, b2 = r2
        return x1 < a2 and a1 < x2 and y1 < b2 and b1 < y2

    n = len(rectangles)
    for i in range(n):
        for j in range(i + 1, n):
            if overlaps(rectangles[i], rectangles[j]):
                return False

    # Check union equals bounding box (approximate via area)
    total_area = sum((x2-x1)*(y2-y1) for x1,y1,x2,y2 in rectangles)
    min_x = min(r[0] for r in rectangles)
    min_y = min(r[1] for r in rectangles)
    max_x = max(r[2] for r in rectangles)
    max_y = max(r[3] for r in rectangles)
    bbox_area = (max_x - min_x) * (max_y - min_y)
    return total_area == bbox_area
"""

blocks += [
    N.h2("Solution 2 — Brute Force (O(n²)) — Do Not Use in Interview"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct approach: for every pair of rectangles, check if they overlap. Then verify the union exactly covers the bounding box via area comparison."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n²) for the pair-checking loop. For n=10,000 rectangles, this is 50 million checks — too slow."),
        N.h4("The Key Observation"),
        N.para("Note that even with no overlaps verified, area check alone doesn't guarantee structural correctness. This brute force combines both but at prohibitive cost."),
        N.h4("Building the Solution"),
        N.para("Step 1: Check all O(n²) pairs with a helper overlap function. Step 2: Sum areas and compare to bounding box. Return True only if both pass."),
    ]),
    N.h3("Code"),
    N.code(sol2_code, lang="python"),
    N.callout(
        "Note: This brute force is included for educational comparison only. "
        "In an interview, mention it first as the naive approach, then immediately "
        "pivot to the O(n) corner-count + area-check solution.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (pair overlap check)", "O(n²)", "O(1)"],
        ["Corner Count + Area Check (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Advanced Data Structures"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Corner Count + Area Check"])),
    N.callout(
        "When to recognize this pattern: Problem asks whether a set of axis-aligned rectangles "
        "forms a perfect cover (no gaps, no overlaps). You need to validate both the quantitative "
        "(area) and structural (corner parity) properties of a 2D tiling.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("The sub-pattern 'Corner Count + Area Check' is derived from analysis of this specific "
         "geometry problem type. The XOR/toggle technique for parity counting is the key algorithmic insight.",
         {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related techniques:"),
    N.bullet(N.rich([("Rectangle Area II", {"bold": True}), " (Hard) — Compute area of union of rectangles; coordinate compression + sweep line"])),
    N.bullet(N.rich([("Minimum Area Rectangle", {"bold": True}), " (Medium) — Find smallest rectangle from set of points using a hash set"])),
    N.bullet(N.rich([("Minimum Area Rectangle II", {"bold": True}), " (Medium) — Non-axis-aligned; hash by center + diagonal for rectangle detection"])),
    N.bullet(N.rich([("The Skyline Problem", {"bold": True}), " (Hard) — Silhouette of overlapping buildings; sweep line + heap"])),
    N.bullet(N.rich([("Max Points on a Line", {"bold": True}), " (Hard) — Geometric structure detection with hash maps of slopes"])),
    N.bullet(N.rich([("Number of Distinct Islands", {"bold": True}), " (Medium) — Shape encoding via corner/turn sequences; set-based uniqueness"])),
    N.para("These problems share the theme of deriving structural geometric properties from point/corner analysis."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Advanced Data Structures / Corner Count + Area Check", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("perfect_rectangle")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
