"""
gen_excel_sheet_column_title.py
Rebuilds the Notion page for LeetCode #168 — Excel Sheet Column Title
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81bb-b768-ca7afd9f790c"

# ── 1) Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=168,
    pattern="Math",
    subpatterns=["Base 26 Conversion"],
    tc="O(log₂₆ n)",
    sc="O(log₂₆ n)",
    key_insight="Decrement n by 1 before each modulo to shift from 1-indexed (A=1…Z=26) to 0-indexed — the only change needed over standard base conversion.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build blocks ──────────────────────────────────────────────────────────

SOL1_CODE = '''\
def convertToTitle(columnNumber: int) -> str:
    result = []
    n = columnNumber
    while n > 0:
        n -= 1                          # shift 1-indexed → 0-indexed
        remainder = n % 26              # extract rightmost digit (0–25)
        result.append(chr(ord('A') + remainder))  # map to 'A'–'Z'
        n //= 26                        # drop the extracted digit
    return ''.join(reversed(result))   # built right-to-left → reverse
'''

SOL2_CODE = '''\
def convertToTitle_recursive(columnNumber: int) -> str:
    if columnNumber == 0:
        return ""
    columnNumber -= 1
    return convertToTitle_recursive(columnNumber // 26) + chr(ord('A') + columnNumber % 26)
'''

SOL3_CODE = '''\
def convertToTitle_string_ops(columnNumber: int) -> str:
    # Brute-force: build a lookup for small n using repeated addition
    # O(n) time — too slow for large n, shown for contrast only
    letters = []
    current = 0
    n = columnNumber
    while n > 0:
        # Simulate counting A, B, ..., Z, AA, AB, ...
        # This is just the same loop in disguise — shown for conceptual contrast
        n -= 1
        letters.append(chr(65 + n % 26))
        n //= 26
    return ''.join(reversed(letters))
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a positive integer ", {}),
        ("columnNumber", {"code": True}),
        (", return its corresponding column title as it appears in an Excel spreadsheet.\n\n"
         "A → 1, B → 2, …, Z → 26, AA → 27, AB → 28, …\n\n"
         "Example: columnNumber = 28 → \"AB\", columnNumber = 701 → \"ZY\", columnNumber = 26 → \"Z\".", {})
    ])),
    N.divider(),
]

# ── Solution 1: Bijective Base-26 Iterative (Interview Pick) ─────────────────
blocks += [
    N.h2("Solution 1 — Bijective Base-26 Iterative (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to convert an integer to a string in a number system where digits are "
            "the 26 letters A–Z (values 1–26). There is no zero digit. This is almost exactly "
            "base-26, just with a 1-indexed alphabet instead of 0-indexed digits."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard base-26 conversion uses digits 0–25, but our system has no digit for 0. "
            "If you naively do n % 26 for n=26, you get 0, which has no corresponding letter — "
            "so a direct translation of base-10 to base-26 fails at multiples of 26."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The bijective numeration trick: subtract 1 from n before each modulo operation. "
            "This temporarily maps A=0, B=1, …, Z=25 so that modulo returns values in 0–25 "
            "instead of 1–26. Map 0 → 'A' using chr(ord('A') + remainder). Then integer-divide "
            "by 26 to remove the extracted digit and repeat."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Start with result = [], n = columnNumber.\n"
            "Step 2: While n > 0: subtract 1 (n -= 1), compute remainder = n % 26, "
            "append chr(ord('A') + remainder), set n = n // 26.\n"
            "Step 3: Return ''.join(reversed(result)) — we collected least-significant digits first."
        ),
        N.callout(
            "Analogy: Think of peeling digits off a number right-to-left in decimal, "
            "but first shifting the whole number down by 1 each time so '26' maps to 'Z' "
            "instead of producing a phantom '0'. Like an odometer that goes from Z straight to AA — "
            "it wraps by incrementing the next position, not by showing a '0' in the current one.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — accumulate output letters (rightmost-first)."])),
    N.para(N.rich([("n = columnNumber", {"code": True}), " — working copy of the input; we consume it digit by digit."])),
    N.para(N.rich([("while n > 0:", {"code": True}), " — keep extracting digits as long as there is remaining value."])),
    N.para(N.rich([("n -= 1", {"code": True}), " — THE KEY STEP. Shifts 1-indexed (A=1) to 0-indexed (A=0) so modulo returns 0–25, not 1–26."])),
    N.para(N.rich([("remainder = n % 26", {"code": True}), " — extract the current rightmost digit (0–25 after the decrement)."])),
    N.para(N.rich([("result.append(chr(ord('A') + remainder))", {"code": True}), " — map 0→'A', 1→'B', …, 25→'Z' and store the letter."])),
    N.para(N.rich([("n //= 26", {"code": True}), " — integer-divide away the digit we just extracted; prepares for the next (more significant) digit."])),
    N.para(N.rich([("return ''.join(reversed(result))", {"code": True}), " — we built right-to-left, so reverse to get most-significant first."])),
    N.divider(),
]

# ── Solution 2: Recursive ─────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive Bijective Base-26"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The same bijective base-26 idea expressed recursively: the column title for n is "
            "the title for (n-1)//26 followed by the letter for (n-1)%26. "
            "Base case: 0 returns empty string."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without the decrement (using n % 26 directly), the recursion hits a remainder of 0 "
            "for multiples of 26, producing an incorrect empty character."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Decrement once at the top of each call — then compute prefix = convertToTitle((n-1)//26) "
            "and suffix = chr('A' + (n-1)%26). Concatenate prefix + suffix."
        ),
        N.h4("Building the Solution"),
        N.para(
            "The recursion mirrors how we read digits left-to-right: the most significant digit "
            "comes from the deep recursive call, and we append the current digit on return. "
            "It's elegant but uses O(log n) call-stack space."
        ),
        N.callout(
            "This approach is preferred if you want to express the solution declaratively without "
            "mutation. Use the iterative approach in interviews — it's clearer for step-by-step explanation.",
            "⚠️", "orange_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if columnNumber == 0: return \"\"", {"code": True}), " — base case: no more digits to extract."])),
    N.para(N.rich([("columnNumber -= 1", {"code": True}), " — same bijective trick: shift to 0-indexed before modulo."])),
    N.para(N.rich([("return convertToTitle_recursive(columnNumber // 26) + ...", {"code": True}),
                   " — recurse on the higher-order digits, then append current digit's letter."])),
    N.para(N.rich([("chr(ord('A') + columnNumber % 26)", {"code": True}), " — maps 0→'A', …, 25→'Z' for current digit."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Iterative (Interview Pick)", "O(log₂₆ n)", "O(log₂₆ n) for result list"],
        ["Recursive", "O(log₂₆ n)", "O(log₂₆ n) call stack + result"],
    ]),
    N.para(
        "log₂₆(n) is the number of digits in the Excel column title. "
        "For n up to 2^31 ≈ 2 billion, this is at most 7 characters (FXSHRXW). "
        "Both solutions are effectively O(1) for any practical input size."
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math — Number Theory / Base Conversion"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Base 26 Conversion (Bijective Numeration)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to convert an integer to a string using an alphabet (A–Z).\n"
        "• Column or position numbering without a zero (bijective).\n"
        "• Any 'what is the Nth item in sequence A, B, …, Z, AA, AB, …' problem.\n"
        "• Whenever standard base conversion gives a spurious '0' result for a valid input.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Excel Sheet Column Number", {"bold": True}),
                     (" (Easy) — Reverse direction: 'ZY' → 701. Uses Horner's method with the same 1-indexed alphabet.")])),
    N.bullet(N.rich([("Integer to Roman", {"bold": True}),
                     (" (Medium) — Convert integer to Roman numeral string. Greedy digit-by-digit extraction.")])),
    N.bullet(N.rich([("Encode and Decode Strings", {"bold": True}),
                     (" (Medium) — Custom encoding scheme using a fixed alphabet.")])),
    N.bullet(N.rich([("Number of Digit One", {"bold": True}),
                     (" (Hard) — Count digit occurrences in a range; same positional-math thinking.")])),
    N.bullet(N.rich([("Count and Say", {"bold": True}),
                     (" (Medium) — Build a string iteratively from a numeric description.")])),
    N.bullet(N.rich([("Base 7", {"bold": True}),
                     (" (Easy) — Standard base conversion to base-7 string; simpler because 0 exists.")])),
    N.bullet(N.rich([("Nth Digit", {"bold": True}),
                     (" (Medium) — Find the Nth digit in the sequence 1,2,3,…; positional arithmetic.")])),
    N.para(
        "These problems share the core technique of extracting digits in a non-standard "
        "numeral system using repeated division/modulo, with careful attention to edge cases "
        "introduced by the specific encoding."
    ),
    N.callout("📚 Sub-pattern: Base 26 Conversion (Bijective Numeration). "
              "See DSA_Patterns_and_SubPatterns_Guide.md — Math section.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("excel_sheet_column_title")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
