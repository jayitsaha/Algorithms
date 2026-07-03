"""gen_palindrome_number.py — Notion update for Palindrome Number (LeetCode #9)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b1-9792-c656e04ca9e8"
SLUG = "palindrome_number"

print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=9,
    pattern="Mathematics & Geometry",
    subpatterns=["Reverse Half"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Reverse only the second half of digits and compare with the first half; avoids string conversion and overflow.",
    icon="🟢"
)
print("Properties set.")

print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Build body blocks ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer "), ("x", {"code": True}),
        (", return "), ("true", {"code": True}),
        (" if "), ("x", {"code": True}),
        (" is a palindrome, and "), ("false", {"code": True}),
        (" otherwise. A palindrome reads the same forward and backward. "
         "The follow-up asks: can you solve it without converting the integer to a string?")
    ])),
    N.divider(),
]

# ── Solution 1: Reverse Half (Optimal / Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Reverse Half (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A palindrome number's first half of digits mirrors its second half. "
            "So instead of checking the whole number against its full reverse, "
            "we only need to reverse half the digits and compare with the remaining half."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Converting to a string works (str(x) == str(x)[::-1]) but uses O(n) space "
            "and may violate interview constraints. Reversing the entire number as an integer "
            "risks overflow for numbers near INT_MAX (e.g. 2,147,483,647 reversed would exceed 32-bit range)."
        ),
        N.h4("The Key Observation"),
        N.para(
            "If we peel digits off the right side of x one at a time, building a 'reversed_half', "
            "the loop condition x > reversed_half naturally stops us at the midpoint — "
            "once reversed_half is as large as the remaining x, we've processed exactly half the digits."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Edge cases: negative numbers return False (minus sign can't mirror). "
            "Numbers ending in 0 except 0 itself return False (reversed form would have leading zero). "
            "2. Loop: extract x % 10 (last digit), add to reversed_half (shift left then add), "
            "shrink x with //= 10. Stop when x <= reversed_half. "
            "3. Compare: for even-length, x == reversed_half. "
            "For odd-length, middle digit is ones place of reversed_half — discard with // 10."
        ),
        N.callout(
            "Analogy: Imagine tearing a strip of paper in half. You fold the right half backwards "
            "onto the left half. If all digits align — it's a palindrome. "
            "The key is you only need to fold HALF, not the whole strip.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isPalindrome(x: int) -> bool:\n"
        "    # Edge cases: negative, or trailing zero (but x=0 is valid)\n"
        "    if x < 0 or (x % 10 == 0 and x != 0):\n"
        "        return False\n"
        "    reversed_half = 0\n"
        "    while x > reversed_half:\n"
        "        reversed_half = reversed_half * 10 + x % 10\n"
        "        x //= 10\n"
        "    # Even length: x == reversed_half\n"
        "    # Odd length: middle digit is ones place of reversed_half; drop it\n"
        "    return x == reversed_half or x == reversed_half // 10\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if x < 0 or (x % 10 == 0 and x != 0)", {"code": True}),
        (" — Negative numbers and numbers with a trailing zero (except 0 itself) can never be palindromes.")
    ])),
    N.para(N.rich([
        ("reversed_half = 0", {"code": True}),
        (" — Initialize the accumulator for the reversed second half.")
    ])),
    N.para(N.rich([
        ("while x > reversed_half", {"code": True}),
        (" — Loop while x is still larger (i.e., we haven't reached the midpoint yet).")
    ])),
    N.para(N.rich([
        ("reversed_half = reversed_half * 10 + x % 10", {"code": True}),
        (" — Shift reversed_half left one decimal place, then append the last digit of x.")
    ])),
    N.para(N.rich([
        ("x //= 10", {"code": True}),
        (" — Remove the last digit from x (shrink from the right).")
    ])),
    N.para(N.rich([
        ("return x == reversed_half or x == reversed_half // 10", {"code": True}),
        (" — Even-length: compare directly. Odd-length: drop the middle digit (ones place of reversed_half) before comparing.")
    ])),
    N.divider(),
]

# ── Solution 2: String Conversion (Simpler, for reference) ──
blocks += [
    N.h2("Solution 2 — String Conversion (Simpler)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Convert the integer to a string, then check if the string equals its own reverse. "
            "Python makes this a one-liner with slice notation."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This approach uses O(n) space for the string and its reversed copy. "
            "In interviews where 'no string conversion' is required, this approach is not valid. "
            "However, it is the most readable first step to propose."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For strings, Python's s[::-1] creates a reversed copy in O(n). "
            "Comparing two strings of length n is also O(n). So the total is O(n) time and O(n) space."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Check for negative (immediate False), convert to string, "
            "return whether string equals its reverse."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isPalindrome(x: int) -> bool:\n"
        "    if x < 0:\n"
        "        return False  # Negative numbers are never palindromes\n"
        "    s = str(x)        # Convert integer to string\n"
        "    return s == s[::-1]  # Compare string to its reverse\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if x < 0: return False", {"code": True}),
        (" — Negative numbers are eliminated. Note: trailing zeros don't need a special check here because str(10)[::-1] = '01' != '10'.")
    ])),
    N.para(N.rich([
        ("s = str(x)", {"code": True}),
        (" — Convert integer to its decimal string representation.")
    ])),
    N.para(N.rich([
        ("return s == s[::-1]", {"code": True}),
        (" — Python slice [start:stop:step] with step=-1 creates a reversed copy. Compare for equality.")
    ])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["String Conversion", "O(n)", "O(n)"],
        ["Reverse Half (Optimal)", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Mathematics & Geometry"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Reverse Half"])),
    N.callout(
        "When to recognize this pattern: "
        "\"Check if a number is a palindrome without string conversion.\" "
        "\"Compare two halves of a number digit by digit.\" "
        "Any problem requiring digit-level symmetry check in O(1) space. "
        "The loop condition x > reversed_half is the key — it's a midpoint detector.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Reverse Integer", {"bold": True}), " (Medium) — Same digit-peeling loop; must explicitly check 32-bit signed overflow bounds (#7)"])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), " (Easy) — Same palindrome concept applied to strings with non-alphanumeric characters to skip (#125)"])),
    N.bullet(N.rich([("Happy Number", {"bold": True}), " (Easy) — Digit extraction to sum digit-squares; Floyd's cycle detection to determine convergence (#202)"])),
    N.bullet(N.rich([("Plus One", {"bold": True}), " (Easy) — Work directly with digits; handle carry propagating right to left (#66)"])),
    N.bullet(N.rich([("Count Numbers with Unique Digits", {"bold": True}), " (Medium) — Combinatorics over digit positions; digit-counting structure (#357)"])),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}), " (Medium) — Palindrome check is the core subroutine; DP minimizes cuts (#132)"])),
    N.para("These problems share the same core technique: extracting and manipulating individual decimal digits in-place without conversion to string."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md section 19 — Mathematics & Geometry", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
