"""
gen_plus_one.py — Regenerate the Plus One Notion page in-place.
LeetCode #66 | Easy | Math | Handle Carry
Notion page ID: 39193418-809c-8102-a1c1-f26afc282431
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8102-a1c1-f26afc282431"

# ── 1. Set properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=66,
    pattern="Math",
    subpatterns=["Handle Carry"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Walk digits right-to-left: increment if < 9 (return early), else set to 0 and carry; prepend 1 if carry survives all digits.",
    icon="🟢"
)
print("Properties OK")

# ── 2. Wipe old body ─────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks")

# ── 3. Build new body ─────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a large integer represented as an integer array ",
        ("digits", {"code": True}),
        ", where each ",
        ("digits[i]", {"code": True}),
        " is the ",
        ("i", {"italic": True}),
        "-th digit of the integer (most significant digit first), increment the large integer by one and return the resulting array of digits. The digits do not contain any leading zeros, except for the number 0 itself."
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}), ("digits = [1,2,3]", {"code": True}), " → ", ("Output: [1,2,4]", {"code": True}), " (123 + 1 = 124)\n",
        ("Example 2: ", {"bold": True}), ("digits = [4,3,2,1]", {"code": True}), " → ", ("Output: [4,3,2,2]", {"code": True}), " (4321 + 1 = 4322)\n",
        ("Example 3: ", {"bold": True}), ("digits = [9]", {"code": True}), " → ", ("Output: [1,0]", {"code": True}), " (9 + 1 = 10, array grows)"
    ])),
    N.divider(),
]

# ── Solution 1 — Right-to-Left Carry (Optimal) ───────────────────────
blocks += [
    N.h2("Solution 1 — Right-to-Left Carry Propagation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a number stored as digit array (most-significant-first). We need to add 1. Think of it as grade-school addition: you add 1 to the ones column, handle any carry, and propagate left."),
        N.h4("What Doesn't Work"),
        N.para("Converting the array to a Python int (int(\"\".join(map(str, digits)))) works in Python but breaks in any language with fixed-size integers (Java's int/long overflows). We need a direct digit-manipulation approach that works for arbitrarily large arrays."),
        N.h4("The Key Observation"),
        N.para("Walk right-to-left. If a digit is < 9, incrementing it stays within 0–9 — no carry. Return immediately. If a digit is 9, adding 1 gives 10: write 0, carry 1 to the next digit left. The only case where carry exhausts the entire array is when all digits are 9 (e.g. 999 + 1 = 1000), requiring a new leading 1."),
        N.h4("Building the Solution"),
        N.para("Step 1: Loop i from len(digits)−1 down to 0.\nStep 2: If digits[i] < 9 → digits[i] += 1 → return digits (carry absorbed, done).\nStep 3: If digits[i] == 9 → digits[i] = 0 (carry continues left).\nStep 4: If loop ends without returning → all were 9 → return [1] + digits."),
        N.callout("Analogy: Think of an odometer rolling from 0999 to 1000 — all the 9s flip to 0 and a new leading 1 appears.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def plusOne(digits: list[int]) -> list[int]:
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits       # carry dies here — done
        digits[i] = 0           # 9 + 1 = 10 → write 0, carry left
    return [1] + digits         # all-9s case: prepend new leading 1
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(digits) - 1, -1, -1):", {"code": True}), " — Walk from the last index (ones place) to index 0 (most significant), stepping by -1 each time."])),
    N.para(N.rich([("if digits[i] < 9:", {"code": True}), " — Check if this digit can absorb the carry without overflowing. Digits 0–8 satisfy this; 9 does not."])),
    N.para(N.rich([("digits[i] += 1", {"code": True}), " — Increment the digit. Since it was < 9, the result is at most 9 — no carry generated."])),
    N.para(N.rich([("return digits", {"code": True}), " — Carry absorbed. All digits to the left are unchanged. Return the modified array immediately (early exit)."])),
    N.para(N.rich([("digits[i] = 0", {"code": True}), " — The digit was 9. 9 + 1 = 10: we write the ones digit (0) and carry 1 leftward. The loop continues."])),
    N.para(N.rich([("return [1] + digits", {"code": True}), " — Only reached when all digits were 9 (loop completed without early return). The entire array is now zeros. Prepend 1 to form the new number (e.g., [0,0,0] → [1,0,0,0])."])),
    N.divider(),
]

# ── Solution 2 — Explicit Carry Variable ─────────────────────────────
blocks += [
    N.h2("Solution 2 — Explicit Carry Variable (More Readable)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same as Solution 1, but we make the carry variable explicit. This maps directly onto how general addition algorithms are taught and makes it easy to generalise (e.g., add K instead of 1)."),
        N.h4("What Doesn't Work"),
        N.para("Treating 'add 1' as a special case (which Solution 1 does by checking < 9) can confuse beginners who haven't seen that trick. An explicit carry variable is more readable and directly extensible."),
        N.h4("The Key Observation"),
        N.para("Initialise carry = 1 (the '+1' we are adding). At each digit, sum = digit + carry. The new digit is sum % 10; the new carry is sum // 10. Stop early if carry becomes 0."),
        N.h4("Building the Solution"),
        N.para("This is the standard addition algorithm: total = digit + carry; digit = total % 10; carry = total // 10. If carry == 0 after any step, break early. If carry != 0 after the loop, prepend it."),
        N.callout("Generalisation: change 'carry = 1' to 'carry = k' and this solves 'Add k to Digit Array' (LC #989) with zero code changes.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def plusOne(digits: list[int]) -> list[int]:
    carry = 1                              # treat '+1' as initial carry
    for i in range(len(digits) - 1, -1, -1):
        total = digits[i] + carry          # apply carry to this digit
        digits[i] = total % 10            # ones digit of sum
        carry = total // 10               # tens digit becomes next carry
        if carry == 0:
            break                          # carry died — stop early
    if carry:
        return [carry] + digits            # surviving carry needs new leading digit
    return digits
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("carry = 1", {"code": True}), " — Initialise carry to 1. This represents the '+1' we are adding."])),
    N.para(N.rich([("total = digits[i] + carry", {"code": True}), " — Sum the current digit and the incoming carry. Range: 0 (digit=0, carry=0) to 10 (digit=9, carry=1)."])),
    N.para(N.rich([("digits[i] = total % 10", {"code": True}), " — The ones place of the sum is the new digit value. E.g., total=10 → 10%10=0; total=5 → 5%10=5."])),
    N.para(N.rich([("carry = total // 10", {"code": True}), " — The tens place of the sum becomes the carry for the next iteration. E.g., total=10 → 10//10=1; total=9 → 9//10=0."])),
    N.para(N.rich([("if carry == 0: break", {"code": True}), " — Early exit optimisation: if no carry, remaining digits are unaffected."])),
    N.para(N.rich([("if carry: return [carry] + digits", {"code": True}), " — If carry survived the full loop, a new leading digit is needed. This only happens when all original digits were 9."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Right-to-Left Carry (Solution 1)", "O(n) worst / O(1) avg", "O(1)*"],
        ["Explicit Carry Variable (Solution 2)", "O(n) worst / O(1) avg", "O(1)*"],
        ["Convert to int approach", "O(n)", "O(n)"],
    ]),
    N.para("* O(1) auxiliary space. The all-9s edge case creates an output array of size n+1, but that is the required output, not extra space."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Handle Carry — right-to-left digit traversal with carry propagation"])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Large integer as digit array, perform arithmetic' → carry propagation right-to-left\n"
        "• 'Result might be longer than input' → check if carry survives the full loop\n"
        "• Binary strings / hex strings → same carry logic, different base (mod 2, mod 16)\n"
        "• 'Add two number arrays' → two-pointer from right, propagate carry",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Handle Carry / Math-on-Arrays technique:"),
    N.bullet(N.rich([("Add Binary", {"bold": True}), " (Easy) — Same carry propagation, base 2; two string pointers from right (#67)"])),
    N.bullet(N.rich([("Add Strings", {"bold": True}), " (Easy) — Add two large numbers as numeric strings, two-pointer carry from right (#415)"])),
    N.bullet(N.rich([("Add Two Numbers", {"bold": True}), " (Medium) — Carry propagation on two linked-list digit sequences (#2)"])),
    N.bullet(N.rich([("Add to Array-Form of Integer", {"bold": True}), " (Easy) — Generalised Plus One: add integer k to digit array (#989)"])),
    N.bullet(N.rich([("Multiply Strings", {"bold": True}), " (Medium) — O(nm) carry per digit pair, accumulate into result array (#43)"])),
    N.bullet(N.rich([("Add One Row to Tree", {"bold": True}), " (Medium) — Different domain, but same 'insert at boundary' reasoning (#623)"])),
    N.para("These problems all share the core technique: simulate arithmetic digit-by-digit, propagating carry from the least-significant position."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math section · Sub-Pattern: Handle Carry · Source: Analysis", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("plus_one")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
