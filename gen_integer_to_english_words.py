"""
gen_integer_to_english_words.py
Notion in-place update for LeetCode #273 – Integer to English Words
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-819d-9a66-e9965727be94"
SLUG    = "integer_to_english_words"

# ── 1) Set page properties ──────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=273,
    pattern="Recursion",
    subpatterns=["Recursive Grouping by 1000s"],
    tc="O(1)",
    sc="O(1)",
    key_insight="Group digits in threes by scale (Billion/Million/Thousand); convert each 0-999 chunk with a lookup-table helper; skip zero chunks silently.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────────────
print("Building new body...")

PROBLEM_STATEMENT = (
    "Given a non-negative integer num, return its English words representation. "
    "Input is guaranteed to fit in a 32-bit signed integer (0 <= num <= 2^31 - 1). "
    "Example 1: num = 123 -> 'One Hundred Twenty Three'. "
    "Example 2: num = 12345 -> 'Twelve Thousand Three Hundred Forty Five'. "
    "Example 3: num = 1234567 -> 'One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven'."
)

SOLUTION1_CODE = '''\
def numberToWords(num: int) -> str:
    if num == 0:
        return "Zero"

    ones = ["","One","Two","Three","Four","Five","Six","Seven",
            "Eight","Nine","Ten","Eleven","Twelve","Thirteen",
            "Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen"]
    tens = ["","","Twenty","Thirty","Forty","Fifty",
            "Sixty","Seventy","Eighty","Ninety"]

    def helper(n):
        """Convert n in [0, 999] to English words. Returns '' for n=0."""
        if n == 0:   return ""
        if n < 20:   return ones[n]
        if n < 100:  return (tens[n // 10] + " " + ones[n % 10]).strip()
        return (ones[n // 100] + " Hundred " + helper(n % 100)).strip()

    parts = []
    for divisor, name in [(10**9, "Billion"), (10**6, "Million"),
                          (10**3, "Thousand"), (1, "")]:
        chunk = num // divisor
        num  %= divisor
        if chunk:
            w = helper(chunk) + (" " + name if name else "")
            parts.append(w.strip())

    return " ".join(parts)
'''

SOLUTION2_CODE = '''\
def numberToWords_bruteforce(num: int) -> str:
    """
    Brute force: handle every digit position with explicit conditionals.
    This is the "naive" approach — correct but not maintainable.
    Included for comparison only; do NOT use in an interview.
    """
    if num == 0:
        return "Zero"

    ones = ["","One","Two","Three","Four","Five","Six","Seven",
            "Eight","Nine","Ten","Eleven","Twelve","Thirteen",
            "Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen"]
    tens_w = ["","","Twenty","Thirty","Forty","Fifty",
              "Sixty","Seventy","Eighty","Ninety"]

    result = []

    def read_chunk(n):
        """Read a 3-digit chunk into words."""
        if n == 0: return ""
        parts = []
        h = n // 100
        remainder = n % 100
        if h: parts.append(ones[h] + " Hundred")
        if remainder < 20 and remainder > 0:
            parts.append(ones[remainder])
        elif remainder >= 20:
            t, o = remainder // 10, remainder % 10
            parts.append((tens_w[t] + " " + ones[o]).strip())
        return " ".join(parts)

    if num >= 10**9:
        result.append(read_chunk(num // 10**9) + " Billion")
        num %= 10**9
    if num >= 10**6:
        result.append(read_chunk(num // 10**6) + " Million")
        num %= 10**6
    if num >= 10**3:
        result.append(read_chunk(num // 10**3) + " Thousand")
        num %= 10**3
    if num > 0:
        result.append(read_chunk(num))

    return " ".join(result)
'''

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# Solution 1 — Optimal: Recursive Grouping
blocks += [
    N.h2("Solution 1 — Recursive Grouping by 1000s (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The problem seems to require handling every digit position independently — "
            "but that leads to an explosion of cases. Instead, ask: is there a repeating "
            "sub-structure? Yes! Every group of three digits is converted to English the same "
            "way, just with a different scale suffix (Billion, Million, Thousand)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A per-digit conditional approach requires ~100+ branches, has massive duplication "
            "between the hundreds, tens, and ones handling at each scale level, and is nearly "
            "impossible to extend (adding Trillion means rewriting half the code)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "English uses the short scale: numbers group in threes. INT_MAX (~2.1e9) fits in "
            "four groups: Billions, Millions, Thousands, ones. Each group is a 3-digit number "
            "in [0, 999]. If we can convert 0–999 to words, we can convert any 32-bit integer "
            "by applying that converter to each group with the right scale suffix."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Write helper(n) for n in [0,999]. Three sub-cases: (a) n<20 direct lookup, "
            "(b) 20<=n<100 tens+ones lookup with .strip(), (c) 100<=n<1000 ones[n//100]+' Hundred '+helper(n%100). "
            "Step 2: Peel off each thousands group from largest to smallest using integer division "
            "and modulo. Step 3: Skip zero chunks (if chunk: ...). Step 4: Join non-empty parts "
            "with spaces."
        ),
        N.callout(
            "Analogy: Think of it like reading a number on a cheque. "
            "You read the billions group, say 'Billion', then the millions group, say 'Million', etc. "
            "The bank teller only needs to know one sub-routine: how to read any three-digit number.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if num == 0: return 'Zero'", {"code": True}), " — Special case: the only time 'Zero' appears in output. If we let it fall through to the loop, the loop returns '' (empty string), which is wrong."])),
    N.para(N.rich([("ones = [...]", {"code": True}), " — 20 entries, indices 0–19. ones[0]='' (not 'Zero') so helper(0) returns '' silently, preventing spurious 'Zero' tokens inside larger numbers."])),
    N.para(N.rich([("tens = [...]", {"code": True}), " — Indices 0 and 1 are unused placeholders (''); tens[2]='Twenty', tens[3]='Thirty', ..., tens[9]='Ninety'."])),
    N.para(N.rich([("def helper(n):", {"code": True}), " — Converts any integer 0–999 to English. Returns empty string for 0 (not 'Zero')."])),
    N.para(N.rich([("if n < 20: return ones[n]", {"code": True}), " — Direct lookup for 1–19. These are all irregular in English (no arithmetic pattern possible)."])),
    N.para(N.rich([("if n < 100: return (...).strip()", {"code": True}), " — For 20–99: tens[n//10] gives decade word, ones[n%10] gives units word. .strip() removes trailing space when n%10=0 (e.g., n=40 → 'Forty ')."])),
    N.para(N.rich([("return (ones[n//100]+' Hundred '+helper(n%100)).strip()", {"code": True}), " — For 100–999: hundreds digit via ones[], then recurse for the remaining 0–99 part. .strip() handles n%100=0 (e.g., 300 → 'Three Hundred ')."])),
    N.para(N.rich([("for divisor, name in [...]:", {"code": True}), " — Four scale levels from largest to smallest. ones tier has name='' (no label appended)."])),
    N.para(N.rich([("chunk = num // divisor; num %= divisor", {"code": True}), " — Integer division extracts the chunk; modulo removes it from num so the next iteration gets only the remaining part."])),
    N.para(N.rich([("if chunk:", {"code": True}), " — Skip zero chunks entirely. We never output 'Zero Thousand' or 'Zero Million'."])),
    N.para(N.rich([("w = helper(chunk) + (' ' + name if name else '')", {"code": True}), " — Build the group string. For the ones tier (name=''), no scale word is appended."])),
    N.para(N.rich([("return ' '.join(parts)", {"code": True}), " — Join all non-empty scale group strings with a single space to form the final result."])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Explicit Conditional Grouping (Not Recommended)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same problem, but approached by handling each scale level independently with "
            "explicit if-statements rather than a loop. The grouping is the same (Billion, "
            "Million, Thousand, ones), but instead of iterating over a list, we have four "
            "separate if-blocks."
        ),
        N.h4("What Doesn't Work (Why This Is Suboptimal)"),
        N.para(
            "This approach has the same time and space complexity as Solution 1, but is "
            "harder to extend. Adding Trillion requires adding a new if-block and duplicating "
            "the read_chunk logic reference. More importantly, this structure cannot be easily "
            "generalized to variable-length scale systems."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The insight here is the same — group by thousands — but without recognizing "
            "that the four scale levels can be expressed as a list of (divisor, name) pairs "
            "and processed in a loop."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Write a read_chunk(n) helper (same logic as Solution 1's helper). Then write "
            "four if-blocks: if num >= 10^9, process billions; if num >= 10^6, process millions; "
            "etc. Append to result list. Return joined result."
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("read_chunk(n)", {"code": True}), " — Identical functionality to Solution 1's helper: converts 0–999 to words or '' for 0."])),
    N.para(N.rich([("if num >= 10**9:", {"code": True}), " — Explicit billion-tier check. Same logic as the loop iteration with divisor=10^9."])),
    N.para(N.rich([("result.append(read_chunk(num // 10**9) + ' Billion')", {"code": True}), " — Extract billions chunk and append with scale word."])),
    N.para(N.rich([("num %= 10**9", {"code": True}), " — Remove billions from remaining number before processing millions."])),
    N.para(N.rich([("return ' '.join(result)", {"code": True}), " — Same join as Solution 1."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (explicit conditionals)", "O(1)", "O(1)", "Correct but not extensible"],
        ["Recursive Grouping by 1000s (Optimal)", "O(1)", "O(1)", "Clean, extensible, interview-ready"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Recursion"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Recursive Grouping by 1000s"])),
    N.callout(
        "When to recognize this pattern: The input has a hierarchical grouping structure "
        "(thousands, millions, billions). The problem appears to need many cases but actually "
        "has a uniform 3-digit sub-problem repeated across scales. Lookup tables are needed "
        "for irregular base cases (1–19 in English). The output is a structured string built "
        "from repeated application of the same sub-routine.",
        "🔎", "green_background"
    ),
    N.para(
        "Note: 'Recursive Grouping by 1000s' is the specific technique used here — "
        "a number-theory-based recursion where the input is decomposed by powers of 1000 "
        "and each chunk is independently converted. This is classified under Recursion "
        "as the main pattern."
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Excel Sheet Column Title", {"bold": True}), " (Easy) — Number to base-26 letter words using lookup + recursive modular arithmetic; same 'convert digit to name' pattern"])),
    N.bullet(N.rich([("Integer to Roman", {"bold": True}), " (Medium) — Lookup table + greedy scale grouping (thousands, hundreds, tens, ones with special cases for IV, IX, etc.)"])),
    N.bullet(N.rich([("Roman to Integer", {"bold": True}), " (Easy) — Reverse of above; parse scale-grouped representations back to integers"])),
    N.bullet(N.rich([("Number of Digit One", {"bold": True}), " (Hard) — Recursive digit-by-digit counting across scale levels; same thousands-grouping idea"])),
    N.bullet(N.rich([("Basic Calculator", {"bold": True}), " (Hard) — Recursive expression parsing; uses the pattern of decomposing input into sub-problems at each operator level"])),
    N.bullet(N.rich([("Count Good Numbers", {"bold": True}), " (Medium) — Grouping digit positions by type and counting valid configurations at each scale"])),
    N.bullet(N.rich([("Encode and Decode Strings", {"bold": True}), " (Medium) — Structured decomposition of a string using a delimiter/length prefix; similar 'build by parts' output strategy"])),
    N.bullet(N.rich([("Cracking the Safe", {"bold": True}), " (Hard) — Recursive construction of a string from a structured alphabet; uses nested helper functions"])),
    N.para("These problems share the core technique: decompose input into structured groups, convert each group with a sub-routine (often using a lookup table), and combine results."),
    N.callout(
        "📚 Pattern Reference: 'Recursive Grouping by 1000s' — "
        "classify under Recursion when the input is hierarchically structured by powers of 10 "
        "and each level has the same conversion logic.",
        "📚", "gray_background"
    ),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
