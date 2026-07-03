"""
gen_number_of_digit_one.py
Notion IN-PLACE update for LeetCode #233 — Number of Digit One (Hard)
Pattern: Dynamic Programming | Sub-pattern: Count 1s at Each Position (Digit DP)
Run: python3 gen_number_of_digit_one.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81c5-a370-efe0d08c3f9f"
SLUG    = "number_of_digit_one"

# ── 1. Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=233,
    pattern="Dynamic Programming",
    subpatterns=["Count 1s at Each Position", "Digit DP"],
    tc="O(log n)",
    sc="O(1)",
    key_insight=(
        "For each digit position, count 1s contributed by that place. "
        "Split n into: higher digits (prefix), current digit, lower digits (suffix). "
        "Three cases: digit < 1 → prefix × place; digit = 1 → prefix × place + suffix + 1; "
        "digit > 1 → (prefix+1) × place. Sum across all positions."
    ),
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe existing content ─────────────────────────────────────────────────
print("Wiping old page content...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3. Build blocks ──────────────────────────────────────────────────────────
print("Building page content...")

PROBLEM_STMT = (
    "Given an integer n, count the total number of digit 1s appearing in all "
    "non-negative integers less than or equal to n.\n\n"
    "Example 1: n = 13  →  Output: 6\n"
    "  (1, 10, 11, 12, 13 — 1 appears in: 1, 10, 11 (twice), 12, 13 = 6 times)\n\n"
    "Example 2: n = 0  →  Output: 0\n\n"
    "Constraints: 0 ≤ n ≤ 10⁹"
)

SOL1_CODE = '''\
def countDigitOne(n: int) -> int:
    count = 0
    place = 1          # Current place value: 1, 10, 100, ...

    while place <= n:
        # Split n around current digit position
        prefix = n // (place * 10)   # digits to the LEFT of current position
        digit  = (n // place) % 10   # current digit (0-9)
        suffix = n % place           # digits to the RIGHT of current position

        # Count 1s contributed by this position
        if digit == 0:
            count += prefix * place
        elif digit == 1:
            count += prefix * place + suffix + 1
        else:  # digit >= 2
            count += (prefix + 1) * place

        place *= 10   # move to next higher position

    return count
'''

SOL1_LBL = [
    ("count = 0", "Running total of all 1s found across every digit position."),
    ("place = 1", "Start at the ones position (place=1). Will go 1 → 10 → 100 → …."),
    ("while place <= n:", "Loop while current place value doesn't exceed n (i.e., there are digits here)."),
    ("prefix = n // (place * 10)", "Digits ABOVE the current position. E.g., for n=3141, place=100 → prefix=31."),
    ("digit  = (n // place) % 10", "The CURRENT digit. E.g., n=3141, place=100 → digit=1."),
    ("suffix = n % place", "Digits BELOW the current position. E.g., n=3141, place=100 → suffix=41."),
    ("if digit == 0:", "Current digit is 0: none of the suffix numbers contribute a 1 here."),
    ("count += prefix * place", "Case 0: Only the prefix×place combinations have a 1 at this position."),
    ("elif digit == 1:", "Current digit is exactly 1: partial contribution from suffix."),
    ("count += prefix * place + suffix + 1", "Case 1: prefix×place full cycles PLUS the partial cycle 0..suffix."),
    ("else:  # digit >= 2", "Current digit is ≥2: the current position is 'past' 1, full extra cycle."),
    ("count += (prefix + 1) * place", "Case 2: (prefix+1) full cycles of place all have a 1 at this position."),
    ("place *= 10", "Advance to the next higher position (tens → hundreds → …)."),
    ("return count", "Sum of 1s contributed by every position is the answer."),
]

SOL2_CODE = '''\
from functools import lru_cache

def countDigitOne(n: int) -> int:
    digits = str(n)

    @lru_cache(maxsize=None)
    def dp(pos, tight, count):
        """
        pos:   current digit position (index into digits string)
        tight: True if we must stay <= n's digit at this pos
        count: number of 1s placed so far
        """
        if pos == len(digits):
            return count   # base case: all positions filled

        limit = int(digits[pos]) if tight else 9
        total = 0
        for d in range(0, limit + 1):
            new_tight = tight and (d == limit)
            new_count = count + (1 if d == 1 else 0)
            total += dp(pos + 1, new_tight, new_count)
        return total

    return dp(0, True, 0)
'''

SOL2_LBL = [
    ("digits = str(n)", "Convert n to string so we can index each digit position."),
    ("@lru_cache(maxsize=None)", "Memoize: same (pos, tight, count) state computed at most once."),
    ("def dp(pos, tight, count):", "Recursive function tracking position, tightness constraint, and 1s seen."),
    ("if pos == len(digits): return count", "Base case: processed all positions, return 1s accumulated."),
    ("limit = int(digits[pos]) if tight else 9", "If tight, we can only place digits 0..digits[pos]; otherwise 0..9."),
    ("for d in range(0, limit + 1):", "Try every valid digit for this position."),
    ("new_tight = tight and (d == limit)", "Tight propagates only if we chose exactly the limit digit."),
    ("new_count = count + (1 if d == 1 else 0)", "Increment count if we placed a 1."),
    ("total += dp(pos + 1, new_tight, new_count)", "Recurse: next position, updated tight and count."),
    ("return dp(0, True, 0)", "Start from position 0, constrained to n, with 0 ones placed."),
]

COMPLEXITY_TABLE = [
    ["Solution", "Time", "Space"],
    ["Math (Position Analysis)", "O(log n)", "O(1)"],
    ["Digit DP (Memoization)", "O(log²n × 10)", "O(log²n)"],
]

# ── Intuition toggle children for Solution 1 ─────────────────────────────────
intuition_s1 = [
    N.h4("Reframe the Problem"),
    N.para(
        "Instead of iterating over all numbers 1..n (which is O(n) — too slow for n=10⁹), "
        "ask: 'How many times does digit 1 appear at the ONES position? At the TENS position? "
        "At the HUNDREDS position?' Sum those counts."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Brute force: iterate every number 0..n, count digit 1s in each. "
        "O(n × log n) — for n=10⁹ that's ~30 billion operations. Completely infeasible."
    ),
    N.h4("The Key Observation"),
    N.para(
        "For any digit POSITION with place value P (1, 10, 100, …):\n"
        "• Digits cycle through 0-9 every 10×P numbers.\n"
        "• In each full cycle, digit=1 appears exactly P times (positions P..2P-1).\n"
        "• The number of full cycles = prefix = n // (P × 10).\n"
        "• There may be a PARTIAL cycle depending on the current digit d:\n"
        "   – If d < 1: partial cycle doesn't reach 1 → 0 extra.\n"
        "   – If d = 1: partial cycle hits 1 exactly (suffix+1) times.\n"
        "   – If d > 1: partial cycle fully clears 1 → P extra."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. For each position (ones, tens, hundreds…): compute prefix, digit, suffix.\n"
        "2. Apply the three-case formula to get 1s at this position.\n"
        "3. Sum across all positions → O(log n) total."
    ),
    N.callout(
        "Mnemonic: 'PREFIX × PLACE' is the base. Then digit=1 adds a partial cycle "
        "(suffix+1). digit>1 adds one full extra cycle (another PLACE).",
        emoji="💡", color="gray_background"
    ),
]

# ── Intuition toggle children for Solution 2 ─────────────────────────────────
intuition_s2 = [
    N.h4("Reframe the Problem"),
    N.para(
        "Classic Digit DP framing: we're counting integers in [0, n] satisfying some "
        "property. Here the property is: 'how many 1s appear in the decimal representation?' "
        "We track the running count of 1s as we build numbers digit by digit."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Naive recursion without memoization recomputes the same (position, tight, count) "
        "state exponentially many times. Memoization brings it to polynomial."
    ),
    N.h4("The Key Observation"),
    N.para(
        "State: (pos, tight, count_of_1s_so_far).\n"
        "• pos: which digit position we're filling.\n"
        "• tight: whether our chosen digits so far exactly match n's prefix "
        "(constraining the max digit we can choose here).\n"
        "• count: 1s accumulated so far.\n\n"
        "At the base case (pos == length), return count. "
        "The sum of all base-case returns gives the total."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Convert n to string for easy digit access.\n"
        "2. dp(pos, tight, count): try all valid digits d for this position.\n"
        "3. Propagate tight=True only if d == current limit.\n"
        "4. Recurse and memoize. Start with dp(0, True, 0)."
    ),
]

# ── Algorithm Deep-Dive ───────────────────────────────────────────────────────
algo_deepdive = [
    N.h3("🔬 Algorithm Deep-Dive: Digit DP"),
    N.para(
        "Digit DP is a technique for counting integers in a range [0, N] that satisfy "
        "some digit-based property. The key insight is that we can build numbers digit "
        "by digit from the most significant position, tracking:\n"
        "  • A 'tight' constraint: are the digits chosen so far a prefix of N?\n"
        "  • Any accumulated state needed (here: count of 1s placed so far).\n\n"
        "When tight=True, the maximum digit at the current position is N's digit. "
        "When tight=False (we've already gone below N), all digits 0-9 are free.\n\n"
        "Why it works: the state space is O(positions × 2 × maxCount) = O(log²n), "
        "far smaller than the O(n) brute-force space."
    ),
    N.code(
        "# Digit DP template:\n"
        "# dp(pos, tight, <accumulated state>)\n"
        "#   pos:   index into str(n)\n"
        "#   tight: True → limited by n's digit at pos\n"
        "#   state: whatever we're tracking (count, sum, has_leading_zero, …)\n"
        "# Base: pos == len(digits) → return accumulated state\n"
        "# Loop: d in range(0, limit+1); recurse, memoize",
        lang="python"
    ),
    N.para(
        "Generalization: change the 'state' to track different properties:\n"
        "  • Count of even digits → state = count_even\n"
        "  • Sum of digits → state = running_sum\n"
        "  • Non-decreasing digits → state = last_digit\n"
        "Recognize Digit DP when: 'count integers in [0,N] with property on their digits.'"
    ),
]

# ── Interview strategy ────────────────────────────────────────────────────────
interview_section = [
    N.h3("🎤 Interview Strategy"),
    N.para(
        "Pattern recognition signals:\n"
        "  • 'Count [digit/property] in all numbers from 1 to n'\n"
        "  • n can be up to 10⁸ or 10⁹ → O(n) brute force is too slow\n"
        "  • Digit-by-digit analysis gives O(log n)\n\n"
        "Recommended approach for interviews:\n"
        "  1. State brute force first (O(n log n)) — quickly dismissed.\n"
        "  2. Propose positional analysis: 'Let me count 1s at each place value.'\n"
        "  3. Derive the three cases (d<1, d=1, d>1) from first principles.\n"
        "  4. Code the math solution — O(log n) time, O(1) space — impressive!\n\n"
        "What to say:\n"
        "  'Instead of checking every number, I'll count how many times 1 appears "
        "at each digit position independently. For the tens position, I look at how "
        "many full groups of 100 fit, multiply by 10, then handle the partial group "
        "based on the tens digit being 0, 1, or ≥2.'"
    ),
    N.callout(
        "⚡ Fast path in interviews: the math solution is optimal (O(log n), O(1)) "
        "and easier to explain than digit DP. Mention digit DP as a generalization "
        "if asked about follow-ups (e.g., 'count numbers with digit sum K').",
        emoji="⚡", color="gray_background"
    ),
]

# ── Why DP section ────────────────────────────────────────────────────────────
why_dp = [
    N.h3("📐 Why Is This Dynamic Programming?"),
    N.para(
        "Optimal Substructure: The count of 1s for n-digit numbers depends on "
        "the count for (n-1)-digit numbers (the sub-problems of shorter prefixes).\n\n"
        "Overlapping Subproblems: Many number prefixes lead to identical remaining "
        "states — e.g., numbers 1000-1099 and 2000-2099 both have the same 'last two "
        "digits free, tight=False' sub-problem. Memoization avoids recomputing them.\n\n"
        "The math solution is essentially DP solved analytically: each position's "
        "contribution can be computed in O(1) using the closed-form formula."
    ),
]

# ── Related Problems ──────────────────────────────────────────────────────────
related = [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Digit DP / positional counting technique:"),
    N.bullet(N.rich([("Numbers At Most N Given Digit Set", {"bold": True}), " (Hard) — Classic digit DP, count valid numbers digit by digit with tight constraint."])),
    N.bullet(N.rich([("Count Numbers with Unique Digits", {"bold": True}), " (Medium) — Count integers where no digit repeats; digit DP with 'digits used' bitmask state."])),
    N.bullet(N.rich([("Digit Count in Range", {"bold": True}), " (Hard) — Generalization: count occurrences of digit d in [low, high]; same three-case math."])),
    N.bullet(N.rich([("Non-decreasing Digits", {"bold": True}), " (Medium) — Find largest n with non-decreasing digits; digit DP with 'last digit' state."])),
    N.bullet(N.rich([("Count Special Integers", {"bold": True}), " (Hard) — Digit DP with 'digits seen so far' bitmask; counts integers with unique digits."])),
    N.bullet(N.rich([("Palindrome Numbers Count", {"bold": True}), " (Medium) — Digit DP checking if built number is palindrome; mirrors first-half state."])),
    N.bullet(N.rich([("New 21 Game", {"bold": True}), " (Medium) — Count reachable numbers; related positional counting with sliding window."])),
    N.bullet(N.rich([("Factorial Trailing Zeroes", {"bold": True}), " (Medium) — Count factor 5s in 1..n; same positional/logarithmic counting pattern."])),
    N.para("These problems share the core technique: counting digit occurrences in a range by analyzing each position's contribution independently."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — Dynamic Programming → DP: Digit", emoji="📚", color="gray_background"),
]

# ── Assemble all blocks ───────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1 — Math (Interview Pick)
blocks += [
    N.h2("Solution 1 — Math: Position Analysis (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_s1),
]
blocks += why_dp
blocks += [
    N.h3("Code"),
    N.code(SOL1_CODE, lang="python"),
    N.h3("Line by Line"),
]
for line, explanation in SOL1_LBL:
    blocks.append(N.para(N.rich([(line, {"code": True, "bold": True}), f"  —  {explanation}"])))

blocks += [
    N.callout(
        "⚠️ Order matters: update place *= 10 AFTER using place in the formula. "
        "And note: prefix = n // (place * 10), NOT n // place — common off-by-one.",
        emoji="⚠️", color="yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Digit DP (Memoization)
blocks += [
    N.h2("Solution 2 — Digit DP: Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition_s2),
]
blocks += algo_deepdive
blocks += [
    N.h3("Code"),
    N.code(SOL2_CODE, lang="python"),
    N.h3("Line by Line"),
]
for line, explanation in SOL2_LBL:
    blocks.append(N.para(N.rich([(line, {"code": True, "bold": True}), f"  —  {explanation}"])))

blocks += [
    N.callout(
        "💡 The tight parameter is the key to digit DP correctness. "
        "Once tight becomes False, it stays False — we've gone strictly below n, "
        "so all remaining digits are unconstrained.",
        emoji="💡", color="gray_background"
    ),
    N.divider(),
]

# Interview Strategy
blocks += interview_section
blocks += [N.divider()]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table(COMPLEXITY_TABLE),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Count 1s at Each Position, Digit DP"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Count [digit/property] in all integers from 1 to n'\n"
        "• n can be up to 10⁸–10⁹ (brute force O(n) is too slow)\n"
        "• Answer depends on digit-level structure of numbers\n"
        "• The math solution: split at each place, apply 3-case formula\n"
        "• The DP solution: (pos, tight, accumulated_state) memoization",
        emoji="🎯", color="gray_background"
    ),
    N.divider(),
]

# Related Problems
blocks += related

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the digit-position analysis visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("All blocks appended successfully.")
