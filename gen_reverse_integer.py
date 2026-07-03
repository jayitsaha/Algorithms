"""
gen_reverse_integer.py — Regenerate Notion page for Reverse Integer (LC #7)
Run from the Algorithms directory: python3 gen_reverse_integer.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8120-a612-ea78213e5b89"
SLUG = "reverse_integer"

print(f"[1/4] Setting properties on page {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=7,
    pattern="Math",
    subpatterns=["Check Overflow"],
    tc="O(log x)",
    sc="O(1)",
    key_insight="Peel digits with x%10, build rev with rev*10+digit; check 32-bit bounds after.",
    icon="🟡"
)
print("      Properties set.")

print("[2/4] Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"      Deleted {deleted} blocks.")

print("[3/4] Building new page body...")

# ── Problem statement ──────────────────────────────────────────────────
blocks = []
blocks.append(N.h2("Problem"))
blocks.append(N.para(N.rich([
    ("Given a signed 32-bit integer "), ("x", {"code": True}),
    (", return "), ("x", {"code": True}),
    (" with its digits reversed. If reversing "), ("x", {"code": True}),
    (" causes the value to go outside the signed 32-bit integer range "),
    ("[-2³¹, 2³¹ - 1]", {"code": True}),
    (", return "), ("0", {"code": True}), (".")
])))
blocks.append(N.para(N.rich([
    ("Examples: "),
    ("x = 123", {"code": True}), (" → "), ("321", {"code": True}), (".  "),
    ("x = -120", {"code": True}), (" → "), ("-21", {"code": True}), (".  "),
    ("x = 1534236469", {"code": True}), (" → "), ("0", {"code": True}),
    (" (overflows 2³¹−1 = 2147483647).")
])))
blocks.append(N.divider())

# ── Solution 1 — Digit Reversal with Overflow Check (INTERVIEW PICK) ──
blocks.append(N.h2("Solution 1 — Digit Reversal with Overflow Check (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("We are asked to reverse the order of decimal digits in an integer. Instead of treating x as a black box, think of it as a sequence of base-10 digits. We need a way to read those digits from right to left and assemble them into a new number from left to right."),

    N.h4("What Doesn't Work"),
    N.para("Naively converting to a string works but (1) uses O(log x) space for the string, and (2) requires special sign handling — negative sign is a character, not a digit. Interviewers specifically use this problem to test modulo-arithmetic fluency."),

    N.h4("The Key Observation"),
    N.para("Two arithmetic primitives are all we need: x % 10 gives the rightmost digit (always 0–9 for non-negative x), and x // 10 discards it. Repeating these two operations peels digits off the right of x. Each peeled digit goes onto the right of rev via rev = rev * 10 + digit — shifting existing digits left to make room. This is the reversal."),

    N.h4("Building the Solution"),
    N.para("1. Record sign; work with abs(x) to avoid Python's floor-modulo on negatives.\n2. rev = 0; loop while x != 0: digit = x % 10; x //= 10; rev = rev*10 + digit.\n3. Restore sign: rev *= sign.\n4. Bounds check: return rev if -2**31 <= rev <= 2**31-1 else 0."),

    N.callout(
        "Analogy: Think of the digits as a stack of coins. x is the source stack — you pop from the top (right end) each time. rev is the destination stack — you push each popped coin. After all coins are moved, the destination stack is in reversed order.",
        "🪙", "blue_background"
    )
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    'def reverse(x: int) -> int:\n'
    '    sign = 1 if x >= 0 else -1  # capture sign\n'
    '    x = abs(x)                  # work with positive x\n'
    '    rev = 0\n'
    '    while x != 0:\n'
    '        digit = x % 10          # peel rightmost digit\n'
    '        x //= 10                # discard that digit\n'
    '        rev = rev * 10 + digit  # shift rev left, append digit\n'
    '    rev *= sign                 # restore sign\n'
    '    INT_MIN, INT_MAX = -2**31, 2**31 - 1\n'
    '    return rev if INT_MIN <= rev <= INT_MAX else 0',
    "python"
))

blocks.append(N.h3("Line by Line"))
lines_sol1 = [
    (("sign = 1 if x >= 0 else -1", {"code": True}),
     " — Record the sign as +1 or −1. We need it later to restore the sign of rev."),
    (("x = abs(x)", {"code": True}),
     " — Strip the sign. Python's floor-division makes -123 % 10 = 7 (not -3), so working with abs(x) is essential for correct digit extraction."),
    (("rev = 0", {"code": True}),
     " — Initialize the reversed-number accumulator to 0."),
    (("while x != 0:", {"code": True}),
     " — Continue as long as there are digits left. When x reaches 0 all digits have been consumed."),
    (("digit = x % 10", {"code": True}),
     " — Modulo 10 extracts the least-significant decimal digit (always 0–9 since x ≥ 0)."),
    (("x //= 10", {"code": True}),
     " — Integer division by 10 discards the digit we just extracted. x shrinks by one digit each iteration."),
    (("rev = rev * 10 + digit", {"code": True}),
     " — Multiply rev by 10 (decimal left-shift) to make room, then append the new digit on the right. This is the core reversal step."),
    (("rev *= sign", {"code": True}),
     " — Reapply the original sign. If x was negative, rev becomes negative."),
    (("return rev if INT_MIN <= rev <= INT_MAX else 0", {"code": True}),
     " — 32-bit signed integer range check. If rev would overflow (e.g. reversed 1534236469 = 9646324351 > 2147483647), return 0."),
]
for code_part, explanation in lines_sol1:
    blocks.append(N.para(N.rich([code_part, (explanation, {})])))

blocks.append(N.divider())

# ── Solution 2 — String Reversal (Alternative) ─────────────────────────
blocks.append(N.h2("Solution 2 — String Reversal (Alternative)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("If we convert the integer to a string, reversing it becomes trivial with Python slicing. We just need to handle the negative sign separately."),

    N.h4("What Doesn't Work"),
    N.para("This approach works correctly, but it uses O(log x) extra space for the string. In a strict interview setting, the interviewer will likely ask for the in-place modulo approach after seeing this."),

    N.h4("The Key Observation"),
    N.para("str(abs(x))[::-1] gives us the reversed digit string. int() parses it back. Then we restore the sign and do the bounds check."),

    N.h4("Building the Solution"),
    N.para("1. Handle sign separately.\n2. Convert to string, reverse with slicing, convert back to int.\n3. Reapply sign, check bounds."),

    N.callout("Use this as a stepping stone to explain the approach, then pivot to the modulo solution for the interview answer.", "💡", "yellow_background")
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    'def reverse_string(x: int) -> int:\n'
    '    sign = 1 if x >= 0 else -1\n'
    '    rev = int(str(abs(x))[::-1])  # reverse the digit string\n'
    '    rev *= sign\n'
    '    return rev if -2**31 <= rev <= 2**31 - 1 else 0',
    "python"
))

blocks.append(N.h3("Line by Line"))
lines_sol2 = [
    (("sign = 1 if x >= 0 else -1", {"code": True}), " — Capture sign; we strip it before reversing."),
    (("str(abs(x))[::-1]", {"code": True}), " — Convert to string, reverse with Python slice [start:stop:step=-1], giving the reversed digit sequence."),
    (("int(...)", {"code": True}), " — Parse the reversed digit string back to integer. Leading zeros (from trailing zeros in original) vanish automatically."),
    (("rev *= sign", {"code": True}), " — Restore the sign."),
    (("return rev if -2**31 <= rev <= 2**31 - 1 else 0", {"code": True}), " — Same bounds check as Solution 1. Returns 0 if overflow."),
]
for code_part, explanation in lines_sol2:
    blocks.append(N.para(N.rich([code_part, (explanation, {})])))

blocks.append(N.divider())

# ── Complexity table ────────────────────────────────────────────────────
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space", "Notes"],
    ["Digit Reversal (Modulo) ★ Interview Pick", "O(log x)", "O(1)", "No extra allocations"],
    ["String Reversal", "O(log x)", "O(log x)", "Extra string allocation"],
], has_col_header=True))
blocks.append(N.divider())

# ── Pattern Classification ──────────────────────────────────────────────
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Math — digit manipulation using modulo arithmetic and integer division on a base-10 number.")])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Check Overflow — after computing the mathematical result, verify it fits within the required integer range before returning.")])))
blocks.append(N.callout(
    "When to recognize this pattern:\n"
    "• Problem says 'reverse digits' on a number (not just any array)\n"
    "• Problem mentions '32-bit signed integer' or 'overflow' constraint\n"
    "• Interviewer says 'no string conversion'\n"
    "• Any 'iterate through decimal digits without converting to string'\n"
    "Signal: x % 10 and x // 10 are the two key operations.",
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ────────────────────────────────────────────────────
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same digit-extraction technique (x % 10 loop):"))

related = [
    ("Palindrome Number", "Easy", "Same x%10 loop; reverse only back-half of digits to compare without full reversal"),
    ("Happy Number", "Easy", "Repeated digit-square sum via x%10 loop; cycle detection via Floyd's"),
    ("Plus One", "Easy", "Digit-level arithmetic on an array representation; carry propagation"),
    ("Add Digits", "Easy", "Digital root via iterated digit sum using %10 loop"),
    ("Multiply Strings", "Medium", "Simulate long multiplication digit-by-digit without bignum library"),
    ("Integer to English Words", "Hard", "Peel groups of 3 digits using / and % to translate to word form"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (f" — {note}", {"color": "gray"})
    ])))

blocks.append(N.para("These problems share the core technique: use x % 10 to inspect/extract the last decimal digit and x // 10 to strip it."))
blocks.append(N.callout("📚 Pattern Source: DSA_Patterns_and_SubPatterns_Guide.md — Section: Math / Check Overflow", "📚", "gray_background"))

# ── Embed ───────────────────────────────────────────────────────────────
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for(SLUG)))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
])))

print(f"      Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print(f"      Blocks appended successfully.")

print("[4/4] Done.")
print(f"NOTION OK {PAGE_ID}")
