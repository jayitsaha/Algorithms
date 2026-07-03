"""
Notion IN-PLACE update for:
  Maximum Score From Removing Substrings (#1717, Medium, Greedy)
  Page ID: 39193418-809c-81f3-876b-f8316f174d07
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f3-876b-f8316f174d07"
SLUG    = "maximum_score_from_removing_substrings"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 1717,
    pattern     = "Greedy",
    subpatterns = ["Remove Higher Value First"],
    tc          = "O(n)",
    sc          = "O(n)",
    key_insight = "Always remove the higher-value pair first (greedy), using a stack to handle collapsing adjacencies in O(n).",
    icon        = "🟡",
)
print("Properties set.")

# ── 2) Wipe old bulk body ──────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a string ", ("s", {"code": True}),
        " and two integers ", ("x", {"code": True}), " and ", ("y", {"code": True}),
        ", you can repeatedly remove the substring ", ('"ab"', {"code": True}),
        " (earning ", ("x", {"code": True}), " points) or ", ('"ba"', {"code": True}),
        " (earning ", ("y", {"code": True}),
        " points). After each removal the surrounding characters collapse together, "
        "potentially creating new pairs. Return the maximum total score."
    ])),
    N.divider(),
]

# ── Solution 1 — Two-Pass Greedy Stack (Interview Pick) ──
sol1_code = """\
def maximumGain(s: str, x: int, y: int) -> int:
    if x < y:
        x, y = y, x
        first, second = "ba", "ab"   # swap so first is always higher-value
    else:
        first, second = "ab", "ba"

    def remove(s, pair, score):
        stack, pts = [], 0
        for c in s:
            if stack and stack[-1] == pair[0] and c == pair[1]:
                stack.pop()
                pts += score
            else:
                stack.append(c)
        return ''.join(stack), pts

    s,   pts1 = remove(s, first,  x)  # Pass 1: exhaust high-value pair
    _,   pts2 = remove(s, second, y)  # Pass 2: exhaust low-value pair
    return pts1 + pts2
"""

blocks += [
    N.h2("Solution 1 — Two-Pass Greedy Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We have a string containing 'a' and 'b' characters (plus others). "
            "We can remove any 'a' immediately followed by 'b' (or 'b' followed by 'a') "
            "and the string closes up. We want to maximise total points."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy without ordering fails: if we try to remove whichever pair appears first "
            "in the string, we might consume a high-value 'ab' pair as a low-value 'ba' removal "
            "(by touching the 'b' first from the other direction). "
            "String replacement in a loop is O(n²) — too slow for n=10⁵."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Each 'a' and 'b' can participate in at most ONE removal. "
            "If a character can form either the high-value or low-value pair, "
            "assign it greedily to the high-value pair first. "
            "This is the exchange argument: swapping any low-value assignment to high-value "
            "cannot decrease the score."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Determine which pair scores more and label it 'first'. "
            "2. Use a stack to remove all 'first' pairs in a single O(n) pass — "
            "when top == pair[0] and current char == pair[1], pop and score. Otherwise push. "
            "3. The stack remainder becomes the input for Pass 2, which does the same for 'second'. "
            "4. Total = pts1 + pts2."
        ),
        N.callout(
            "Analogy: Imagine sorting receipts by value before cashing them. "
            "You always cash the highest-value receipt first — the same logic applies here.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if x < y:", {"code": True}), " — Normalise so first pair always has higher (or equal) score. Swap x,y AND pair labels."])),
    N.para(N.rich([("first, second = 'ab', 'ba'", {"code": True}), " — When x ≥ y, 'ab' scores x (higher); 'ba' scores y (lower)."])),
    N.para(N.rich([("def remove(s, pair, score):", {"code": True}), " — Reusable helper for one greedy stack pass. Parameterised so both passes share one implementation."])),
    N.para(N.rich([("stack, pts = [], 0", {"code": True}), " — Fresh stack and local score counter per pass."])),
    N.para(N.rich([("for c in s:", {"code": True}), " — Linear scan: O(n). Each char enters at most once and exits at most once."])),
    N.para(N.rich([("if stack and stack[-1] == pair[0] and c == pair[1]:", {"code": True}), " — Three-way guard: stack is non-empty, its top matches pair[0], and current char matches pair[1]."])),
    N.para(N.rich([("stack.pop(); pts += score", {"code": True}), " — Match found: remove the top (pair[0]), claim the score. The character below the top is now adjacent to the next incoming char — stack handles collapse automatically."])),
    N.para(N.rich([("stack.append(c)", {"code": True}), " — No match yet. Push current char — it waits for a future partner."])),
    N.para(N.rich([("return ''.join(stack), pts", {"code": True}), " — Remaining chars (no target pair survived) + points earned this pass."])),
    N.para(N.rich([("s, pts1 = remove(s, first, x)", {"code": True}), " — Pass 1: exhaust ALL occurrences of the high-value pair from left to right."])),
    N.para(N.rich([(  "_, pts2 = remove(s, second, y)", {"code": True}), " — Pass 2: run same logic on remainder for low-value pair."])),
    N.para(N.rich([("return pts1 + pts2", {"code": True}), " — Sum of both passes is the maximum achievable score."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
sol2_code = """\
def maximumGain_brute(s: str, x: int, y: int) -> int:
    result = 0
    hi_pair = "ab" if x >= y else "ba"
    lo_pair = "ba" if x >= y else "ab"
    hi_pts  = max(x, y)
    lo_pts  = min(x, y)
    for pair, pts in [(hi_pair, hi_pts), (lo_pair, lo_pts)]:
        while pair in s:           # O(n) membership check
            s = s.replace(pair, '', 1)  # O(n) replace
            result += pts
    return result  # Correct but O(n^2) — TLE for large inputs
"""

blocks += [
    N.h2("Solution 2 — Brute Force String Replace (O(n²), intuition only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Directly simulate what the problem describes: keep removing pairs until none remain."),
        N.h4("What Doesn't Work"),
        N.para("Each str.replace() call is O(n); in the worst case we do O(n) removals (e.g., 'ababab...') = O(n²) total. For n=10⁵ this is 10^10 operations — TLE."),
        N.h4("The Key Observation"),
        N.para("This approach is correct and useful for understanding, but a stack lets us do each pass in O(n) by leveraging the fact that each character is pushed and popped at most once."),
        N.h4("Building the Solution"),
        N.para("Order the pairs by descending score (greedy). For each pair, loop: find first occurrence → remove → repeat. Transition to stack for O(n) version."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                  "Time",   "Space",  "Notes"],
        ["Brute Force (str.replace)", "O(n²)",  "O(n)",   "Correct but TLE for n=10⁵"],
        ["Two-Pass Greedy Stack ✓",   "O(n)",   "O(n)",   "Optimal — interview pick"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Remove Higher Value First (Greedy Ordering + Stack Simulation)"])),
    N.callout(
        "When to recognise this pattern: "
        "\"Remove adjacent pair\" → Stack. "
        "\"Two competing operations with different payoffs\" → Greedy: always do the higher-payoff one first. "
        "\"Removal causes new adjacencies\" → Stack models collapse naturally.",
        "🔎", "green_background"
    ),
    N.para(
        "Note: The sub-pattern 'Remove Higher Value First' is based on analysis; "
        "it is a specific application of the Greedy exchange argument combined with Stack simulation."
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Greedy Ordering + Stack Pair Removal):"),
    N.bullet(N.rich([("Remove All Adjacent Duplicates In String", {"bold": True}), " (Easy) — Stack removes 'aa' pairs; same structure without scoring (#1047)"])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String II", {"bold": True}), " (Medium) — Stack with count, remove k-length runs (#1209)"])),
    N.bullet(N.rich([("Minimum String Length After Removing Substrings", {"bold": True}), " (Easy) — Greedy remove 'AB' and 'CD' pairs; minimise length (#2696)"])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), " (Medium) — Assign scores to nested bracket structures via stack (#856)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Core stack matching template that this pattern extends (#20)"])),
    N.bullet(N.rich([("Minimum Number of Swaps to Make String Balanced", {"bold": True}), " (Medium) — Greedy pair counting on brackets (#1963)"])),
    N.para("These problems share the same core technique: stack-based pair matching where order of operations matters."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy + Stack section. Sub-Pattern: Remove Higher Value First.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer (embed) ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
