"""
gen_maximum_population_year.py — Notion update for Maximum Population Year (#1854)
Pattern: Prefix Sum / Difference Array (Easy)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8109-b6ec-e70fdf853178"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1854,
    pattern="Prefix Sum",
    subpatterns=["Difference Array"],
    tc="O(n)",
    sc="O(Y)",
    key_insight="Use a difference array over years [1950..2050]; apply birth/death deltas, then scan prefix sums to find the maximum population year.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
print("Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────

# ── PROBLEM ──
blocks = []
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a 2D integer array ", {}),
        ("logs", {"code": True}),
        (" where ", {}),
        ("logs[i] = [birth_i, death_i]", {"code": True}),
        (" represents the birth and death years of the ", {}),
        ("i", {"code": True}),
        ("-th person, return the earliest year with the maximum population. "
         "A person is alive during year ", {}),
        ("y", {"code": True}),
        (" if ", {}),
        ("birth_i <= y < death_i", {"code": True}),
        (". Note: year range is 1950-2050.", {}),
    ])),
    N.divider(),
]

# ── SOLUTION 1 — DIFFERENCE ARRAY (INTERVIEW PICK) ──
sol1_code = """\
def maximumPopulation(logs: list[list[int]]) -> int:
    delta = [0] * 101          # index 0 = year 1950, index 100 = year 2050

    for birth, death in logs:
        delta[birth - 1950] += 1   # person joins at birth year
        delta[death - 1950] -= 1   # person leaves at death year (exclusive)

    max_pop = cur_pop = 0
    best_year = 1950

    for i, d in enumerate(delta):
        cur_pop += d               # running prefix sum = population at year 1950+i
        if cur_pop > max_pop:      # strictly greater -> earliest year wins ties
            max_pop = cur_pop
            best_year = 1950 + i

    return best_year
"""

sol2_code = """\
def maximumPopulation(logs: list[list[int]]) -> int:
    # Brute-force: for each candidate year, count how many people are alive
    best_year = 1950
    best_pop  = 0

    for year in range(1950, 2051):
        pop = sum(1 for b, d in logs if b <= year < d)
        if pop > best_pop:
            best_pop  = pop
            best_year = year

    return best_year
"""

blocks += [
    N.h2("Solution 1 - Difference Array / Prefix Sum (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have a fixed year range [1950, 2050] and a list of [birth, death) intervals. "
            "We need to find which year has the most overlapping intervals. "
            "Rather than counting intervals for every year separately, we want to track "
            "how the population changes as we move year by year."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The naive approach loops over every year 1950-2050 (~101 years) and for each "
            "year counts all people alive in O(n) time - giving O(101 * n). While this is "
            "acceptable here (n <= 100), it does not scale to large year ranges or large n. "
            "We want O(Y + n) where Y = year range width."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A person only changes the population count at two moments: "
            "+1 at their birth year, and -1 at their death year (since death year is exclusive). "
            "Between those two events, the population delta is 0. "
            "So instead of re-counting each year, record these +1/-1 events in a delta array "
            "and compute a running prefix sum over it."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create delta[0..100] where index i = year 1950+i, initialized to 0.\n"
            "2. For each person [birth, death]: delta[birth-1950] += 1, delta[death-1950] -= 1.\n"
            "3. Scan delta left to right, maintaining a running sum cur_pop. "
            "Whenever cur_pop exceeds the current maximum, update best_year.\n"
            "4. Return best_year."
        ),
        N.callout(
            "Analogy: Imagine a timeline of light switches. Each birth flips a switch ON at year B; "
            "each death flips it OFF at year D. Instead of counting how many switches are ON at "
            "every moment, you just record the flip events and scan once.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("delta = [0] * 101", {"code": True}),
                   (" - Allocate 101 buckets for years 1950 through 2050. Index i maps to year 1950+i.", {})])),
    N.para(N.rich([("for birth, death in logs:", {"code": True}),
                   (" - Iterate over each person's [birth, death) interval.", {})])),
    N.para(N.rich([("delta[birth - 1950] += 1", {"code": True}),
                   (" - Record +1 event at birth year: this person joins the living population.", {})])),
    N.para(N.rich([("delta[death - 1950] -= 1", {"code": True}),
                   (" - Record -1 event at death year (exclusive endpoint): person leaves.", {})])),
    N.para(N.rich([("max_pop = cur_pop = 0; best_year = 1950", {"code": True}),
                   (" - Track running population, max seen, and the year of that max.", {})])),
    N.para(N.rich([("for i, d in enumerate(delta):", {"code": True}),
                   (" - Scan every year in order.", {})])),
    N.para(N.rich([("cur_pop += d", {"code": True}),
                   (" - Add the delta (could be +1, -1, or 0). cur_pop now equals population at year 1950+i.", {})])),
    N.para(N.rich([("if cur_pop > max_pop:", {"code": True}),
                   (" - Strictly greater ensures we keep the EARLIEST year when there is a tie.", {})])),
    N.para(N.rich([("max_pop = cur_pop; best_year = 1950 + i", {"code": True}),
                   (" - Update the record-holder.", {})])),
    N.para(N.rich([("return best_year", {"code": True}),
                   (" - Return the earliest year with peak population.", {})])),
    N.divider(),
]

# ── SOLUTION 2 — BRUTE FORCE ──
blocks += [
    N.h2("Solution 2 - Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each year from 1950 to 2050, simply count how many people satisfy birth <= year < death."),
        N.h4("What Doesn't Work"),
        N.para(
            "For small n (n <= 100) and small year range (101 years), this O(101 * n) approach is fine. "
            "But if the year range were 10^9 or n were 10^6, this would be far too slow."
        ),
        N.h4("The Key Observation"),
        N.para("Direct simulation: the definition of alive at year y is birth <= y < death. Just count it directly."),
        N.h4("Building the Solution"),
        N.para("Outer loop: years 1950..2050. Inner loop: all persons. Use sum() with a generator condition."),
        N.callout("Start here in an interview to show correctness, then pivot to the O(n) Difference Array.", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for year in range(1950, 2051):", {"code": True}),
                   (" - Try every candidate year.", {})])),
    N.para(N.rich([("pop = sum(1 for b, d in logs if b <= year < d)", {"code": True}),
                   (" - Count people alive at this year using the problem's inclusive-birth, exclusive-death definition.", {})])),
    N.para(N.rich([("if pop > best_pop:", {"code": True}),
                   (" - Strictly greater preserves earliest year for ties.", {})])),
    N.divider(),
]

# ── COMPLEXITY TABLE ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(Y * n)", "O(1)", "Y=101 year range, n=persons; fine for constraints"],
        ["Difference Array (Optimal)", "O(Y + n)", "O(Y)", "One pass to build delta, one pass to scan"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Difference Array", {})])),
    N.callout(
        "When to recognize this pattern: "
        "Multiple intervals over a bounded numeric range; need the point with max/min overlap; "
        "O(Y + n) beats O(Y * n). Key signals: '+1 at start, -1 at end+1' and 'scan prefix sums'.",
        "🔎", "green_background"
    ),
    N.callout(
        "Algorithm Deep-Dive - Difference Array:\n"
        "A difference array delta[] stores changes in a quantity rather than the quantity itself. "
        "Adding +1 at index l and -1 at index r+1 represents 'increment range [l, r] by 1'. "
        "A single prefix-sum scan over delta reconstructs the actual values at each index. "
        "This transforms O(n * range) range-update problems into O(n + range). "
        "Classic uses: Range Addition (#370), Car Pooling (#1094), Corporate Flight Bookings (#1109).",
        "📐", "blue_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Difference Array / Prefix Sum technique:"),
    N.bullet(N.rich([("Range Addition", {"bold": True}), (" (Medium) - Classic difference array: apply k range updates, return final array. #370", {})])),
    N.bullet(N.rich([("Car Pooling", {"bold": True}), (" (Medium) - Passengers board/exit at stops; use delta array to check capacity. #1094", {})])),
    N.bullet(N.rich([("Corporate Flight Bookings", {"bold": True}), (" (Medium) - Seats reserved for flight ranges; difference array + prefix sum. #1109", {})])),
    N.bullet(N.rich([("My Calendar I", {"bold": True}), (" (Medium) - Detect overlap of booking intervals. #729", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) - Minimum rooms needed = max concurrent meetings (same idea). #253", {})])),
    N.bullet(N.rich([("Number of Flowers in Full Bloom", {"bold": True}), (" (Hard) - Point queries on intervals; difference array + binary search. #2251", {})])),
    N.bullet(N.rich([("Count of Smaller Numbers After Self", {"bold": True}), (" (Hard) - Related interval/count decomposition pattern. #315", {})])),
    N.para("These problems all share the core technique: encode interval start/end events as +1/-1 in a delta array, then recover actual values with a prefix sum scan."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md - Section 1.3 (Prefix Sum Pattern -> Difference Array sub-pattern)", "📚", "gray_background"),
]

# ── EMBED ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_population_year")),
    N.para(N.rich([
        ("Step through the algorithm visually - use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
