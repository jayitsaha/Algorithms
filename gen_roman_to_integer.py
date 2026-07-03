"""
gen_roman_to_integer.py — Notion page rebuild for Roman to Integer (#13)
HTML: KEPT (889 lines, all markers present — passes resume check)
Notion: wipe + full rebuild
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8163-8e1c-e64805427793"

# ── 1. Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=13,
    pattern="Math",
    subpatterns=["Subtract if Smaller Before"],
    tc="O(n)",
    sc="O(1)",
    key_insight="When a smaller Roman numeral appears before a larger one, subtract it instead of adding.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a Roman numeral string "),
        ("s", {"code": True}),
        (", convert it to an integer. Roman numerals use seven symbols: "),
        ("I", {"code": True}), ("=1, "),
        ("V", {"code": True}), ("=5, "),
        ("X", {"code": True}), ("=10, "),
        ("L", {"code": True}), ("=50, "),
        ("C", {"code": True}), ("=100, "),
        ("D", {"code": True}), ("=500, "),
        ("M", {"code": True}), ("=1000. "),
        ("Subtraction applies when a smaller numeral precedes a larger one "
         "(e.g. IV=4, IX=9, XL=40, XC=90, CD=400, CM=900). "
         "Input is guaranteed valid. Constraints: 1 ≤ s.length ≤ 15, "
         "s contains only [IVXLCDM], 1 ≤ output ≤ 3999."),
    ])),
    N.divider(),
]

# ── Solution 1 — Single Pass with Look-Ahead (Interview Pick) ──────────────────
S1_CODE = '''\
ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
         'C': 100, 'D': 500, 'M': 1000}

def romanToInt(s: str) -> int:
    total = 0
    n = len(s)
    for i in range(n):
        curr = ROMAN[s[i]]
        nxt  = ROMAN[s[i + 1]] if i + 1 < n else 0
        if curr < nxt:
            total -= curr   # subtraction rule
        else:
            total += curr   # addition rule
    return total
'''

blocks += [
    N.h2("Solution 1 — Single Pass with Look-Ahead (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We are summing symbol values left-to-right, but with one twist: "
            "if a symbol is smaller than the symbol that follows it, we subtract "
            "it instead of adding it. Everything else is pure addition."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A pure left-to-right sum ignores the subtraction rule. "
            "A lookup table of every two-character pair (IV, IX, …) requires "
            "special pre-processing and is brittle. "
            "Handling every case explicitly produces long, error-prone code."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The subtraction rule has exactly one trigger: the current symbol's "
            "value is strictly less than the next symbol's value. "
            "When that happens, the current symbol must be subtracted. "
            "In all other cases — including the last symbol — it must be added. "
            "This single comparison replaces all six special pairs."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build a lookup map from character → integer value.\n"
            "2. Iterate through every index i.\n"
            "3. Peek at index i+1 (guard with a bounds check).\n"
            "4. If current < next → subtract current; otherwise add current.\n"
            "5. Return the accumulated total."
        ),
        N.callout(
            "Analogy: Think of a price tag game. When you see a smaller coin "
            "before a bigger one, the smaller coin is a 'discount' that reduces "
            "the total — otherwise it adds to it. Scan left to right, subtract "
            "discounts, add everything else.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(S1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("ROMAN = {...}", {"code": True}),
        (" — maps each Roman character to its integer value; O(1) lookups.")
    ])),
    N.para(N.rich([
        ("total = 0", {"code": True}),
        (" — accumulator that we will add to (or subtract from) as we scan.")
    ])),
    N.para(N.rich([
        ("n = len(s)", {"code": True}),
        (" — cache the length once to avoid repeated calls in the loop.")
    ])),
    N.para(N.rich([
        ("for i in range(n):", {"code": True}),
        (" — visit every character position exactly once.")
    ])),
    N.para(N.rich([
        ("curr = ROMAN[s[i]]", {"code": True}),
        (" — numeric value of the character we are currently examining.")
    ])),
    N.para(N.rich([
        ("nxt = ROMAN[s[i+1]] if i+1 < n else 0", {"code": True}),
        (" — peek at the next symbol; use 0 as a sentinel at the last position "
         "so the comparison always favours addition (curr ≥ 0).")
    ])),
    N.para(N.rich([
        ("if curr < nxt: total -= curr", {"code": True}),
        (" — subtraction rule: this symbol is a 'modifier' (e.g. I in IV); "
         "subtract its value from the total.")
    ])),
    N.para(N.rich([
        ("else: total += curr", {"code": True}),
        (" — standard addition rule: this symbol stands on its own.")
    ])),
    N.para(N.rich([
        ("return total", {"code": True}),
        (" — after the single pass, total holds the correct integer value.")
    ])),
    N.divider(),
]

# ── Solution 2 — Right-to-Left Accumulation ────────────────────────────────────
S2_CODE = '''\
ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
         'C': 100, 'D': 500, 'M': 1000}

def romanToInt(s: str) -> int:
    total = prev = 0
    for ch in reversed(s):
        curr = ROMAN[ch]
        if curr < prev:
            total -= curr
        else:
            total += curr
        prev = curr
    return total
'''

blocks += [
    N.h2("Solution 2 — Right-to-Left Accumulation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Process the string backwards. When travelling right-to-left, the "
            "subtraction rule flips: if the current symbol is smaller than the "
            "previous one we processed (which is actually to the right in the "
            "original string), subtract it."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The left-to-right peek requires a bounds check. Traversing "
            "right-to-left removes that guard entirely — we always have a "
            "'previous' value to compare against (initialised to 0 before "
            "the first character)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When scanning right-to-left, the subtraction rule becomes: "
            "'if current < previous (which we saw to the right), subtract; "
            "otherwise add.' No peek needed — we compare against what we "
            "already processed."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialise total and prev to 0.\n"
            "2. Iterate through the reversed string.\n"
            "3. Compare curr against prev (the symbol immediately to the right).\n"
            "4. Subtract if curr < prev; add otherwise.\n"
            "5. Update prev = curr and continue."
        ),
        N.callout(
            "Elegant because it eliminates the index-bounds guard entirely. "
            "Both solutions are O(n) / O(1) — choose whichever feels more "
            "natural to articulate in an interview.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(S2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("total = prev = 0", {"code": True}),
        (" — total is the answer accumulator; prev tracks the value of the "
         "character to the right of the current position (starts at 0).")
    ])),
    N.para(N.rich([
        ("for ch in reversed(s):", {"code": True}),
        (" — traverse right-to-left; reversed() is O(1) extra space.")
    ])),
    N.para(N.rich([
        ("curr = ROMAN[ch]", {"code": True}),
        (" — look up the integer value of the current character.")
    ])),
    N.para(N.rich([
        ("if curr < prev: total -= curr", {"code": True}),
        (" — the character to the right is larger, so the current one is "
         "a subtraction modifier (e.g. the 'I' in 'IV' when traversing "
         "from right).")
    ])),
    N.para(N.rich([
        ("else: total += curr", {"code": True}),
        (" — normal addition.")
    ])),
    N.para(N.rich([
        ("prev = curr", {"code": True}),
        (" — advance: what was 'current' becomes 'previous' for the next step.")
    ])),
    N.divider(),
]

# ── Solution 3 — Brute Force (Two-Symbol Lookup) ───────────────────────────────
S3_CODE = '''\
def romanToInt(s: str) -> int:
    pairs = {"IV":4,"IX":9,"XL":40,"XC":90,"CD":400,"CM":900}
    singles = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    total, i = 0, 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in pairs:
            total += pairs[s[i:i+2]]
            i += 2
        else:
            total += singles[s[i]]
            i += 1
    return total
'''

blocks += [
    N.h2("Solution 3 — Brute Force (Two-Symbol Pair Lookup)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Handle the six special subtraction pairs (IV, IX, XL, XC, CD, CM) "
            "explicitly with a dictionary lookup, and process all remaining "
            "characters one at a time."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This approach works correctly but requires hardcoding six pairs. "
            "It is more verbose and harder to remember under interview pressure "
            "than the look-ahead approach."
        ),
        N.h4("The Key Observation"),
        N.para(
            "There are exactly six subtraction-pair combinations in the Roman "
            "numeral system. Pre-tabulating them lets us greedily consume "
            "two characters when a pair is spotted, or one character otherwise."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build a 'pairs' dict with all six two-symbol sequences and their values.\n"
            "2. Build a 'singles' dict for the seven symbols.\n"
            "3. Walk with index i; check if s[i:i+2] is a pair.\n"
            "4. If yes, add its value and advance i by 2.\n"
            "5. Otherwise, add the single value and advance i by 1."
        ),
        N.callout(
            "Good for interviews where you want to show you know the six pairs, "
            "but the look-ahead solution is shorter and scales better if the "
            "numeral system were extended.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(S3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("pairs = {...}", {"code": True}),
        (" — the six subtraction two-character sequences mapped to their "
         "net integer values.")
    ])),
    N.para(N.rich([
        ("singles = {...}", {"code": True}),
        (" — individual symbol values as a fallback.")
    ])),
    N.para(N.rich([
        ("while i < len(s):", {"code": True}),
        (" — manual index loop so we can jump by 1 or 2 characters.")
    ])),
    N.para(N.rich([
        ("if i+1 < len(s) and s[i:i+2] in pairs:", {"code": True}),
        (" — try to consume a two-character subtraction pair first.")
    ])),
    N.para(N.rich([
        ("total += pairs[s[i:i+2]]; i += 2", {"code": True}),
        (" — found a pair: add its combined value and skip both characters.")
    ])),
    N.para(N.rich([
        ("else: total += singles[s[i]]; i += 1", {"code": True}),
        (" — no pair: consume a single character normally.")
    ])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Single Pass with Look-Ahead (Interview Pick)", "O(n)", "O(1)"],
        ["Right-to-Left Accumulation", "O(n)", "O(1)"],
        ["Two-Symbol Pair Lookup (Brute Force)", "O(n)", "O(1)"],
    ]),
    N.para(
        "n = length of the input string (at most 15, so effectively O(1) in "
        "practice, but O(n) asymptotically). The ROMAN / singles / pairs "
        "dictionaries have fixed size 7–13 and do not scale with input."
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([
        ("Sub-Pattern(s): ", {"bold": True}),
        ("Subtract if Smaller Before — single-pass rule-based symbol accumulation "
         "with a look-ahead (or right-to-left) comparison to detect subtraction cases.")
    ])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem encodes numbers as sequences of symbols with positional rules.\n"
        "• A smaller token before a larger token has a 'negating' semantic.\n"
        "• A single pass suffices because each symbol (or pair) contributes "
        "independently to a running total.\n"
        "• Keywords: 'Roman numerals', 'symbol encoding', 'look-ahead comparison'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([
        ("Integer to Roman", {"bold": True}),
        (" (Medium, LeetCode #12) — reverse mapping; greedily subtract largest "
         "Roman value from the integer. Direct inverse of this problem.")
    ])),
    N.bullet(N.rich([
        ("Valid Number", {"bold": True}),
        (" (Hard, LeetCode #65) — symbol-sequence validation with stateful "
         "look-ahead; similar single-pass scanning discipline.")
    ])),
    N.bullet(N.rich([
        ("Excel Sheet Column Number", {"bold": True}),
        (" (Easy, LeetCode #171) — convert a column title (positional letter "
         "encoding) to an integer; same left-to-right accumulation with a base-26 "
         "multiplier instead of a subtraction rule.")
    ])),
    N.bullet(N.rich([
        ("Excel Sheet Column Title", {"bold": True}),
        (" (Easy, LeetCode #168) — reverse of #171; analogous to Integer to Roman.")
    ])),
    N.bullet(N.rich([
        ("Basic Calculator", {"bold": True}),
        (" (Hard, LeetCode #224) — evaluate an arithmetic expression by scanning "
         "tokens and deciding add vs. subtract based on sign context — same "
         "underlying 'accumulate with sign' pattern at higher complexity.")
    ])),
    N.bullet(N.rich([
        ("Decode String", {"bold": True}),
        (" (Medium, LeetCode #394) — symbol-sequence decoding with look-ahead "
         "via a stack; exercises the same examine-next-character-to-decide-current-action instinct.")
    ])),
    N.bullet(N.rich([
        ("Score of Parentheses", {"bold": True}),
        (" (Medium, LeetCode #856) — assign values to symbols (parentheses) "
         "using context; single-pass accumulation pattern.")
    ])),
    N.para(
        "These problems share the core technique: scan a symbol sequence "
        "left-to-right, use the current symbol's value (and optionally the "
        "next symbol's value) to decide how much to add or subtract from a "
        "running total."
    ),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — "
        "Math / Number Theory section (Roman Numeral problems cluster).",
        "📚", "gray_background"
    ),
]

# ── Embed ───────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("roman_to_integer")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
