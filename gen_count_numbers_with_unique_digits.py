"""
gen_count_numbers_with_unique_digits.py
Notion rebuild for LeetCode #357 — Count Numbers with Unique Digits
Pattern: Dynamic Programming / Permutation Count
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-901e-f2afb0839196"
SLUG = "count_numbers_with_unique_digits"

# ── 1. Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=357,
    pattern="Dynamic Programming",
    subpatterns=["Permutation Count"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Count d-digit unique-digit numbers via permutation math: 9 × 9 × 8 × … × (10-d+1), then sum for each length from 1 to n.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
N.wipe_page(PAGE_ID)
print("Page wiped.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (", return the count of all numbers with unique digits, ", {}),
        ("x", {"code": True}),
        (", where ", {}),
        ("0 <= x < 10^n", {"code": True}),
        (". A number has unique digits if no digit repeats. For example, "
         "12 has unique digits, but 11 does not.", {}),
    ])),
    N.callout(
        "Edge case: n = 0 → only 0 → answer is 1. "
        "n ≥ 10 → all 10 digits are used; impossible to have 11-digit unique-digit numbers, "
        "so the answer is capped at the same value as n = 10.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 1 — Brute Force Enumeration ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force Enumeration"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count integers in [0, 10^n) where every digit is different. "
               "The simplest idea: check every single integer and test if its digits are all unique."),
        N.h4("What Doesn't Work"),
        N.para("For n = 5 we'd test 100,000 numbers; for n = 9 we'd test a billion. "
               "While 10^n grows quickly, for n ≤ 9 the brute force is technically feasible but slow and inelegant. "
               "It tells us nothing about the structure of the problem."),
        N.h4("The Key Observation"),
        N.para("We can check uniqueness in O(d) time by converting a number to its digit string "
               "and checking whether len(set(digits)) == len(digits). "
               "This is the direct check approach."),
        N.h4("Building the Solution"),
        N.para("Iterate x from 0 to 10^n - 1. For each x, convert to string, "
               "check if all digits are unique via a set comparison. Increment counter if unique. "
               "Return counter."),
        N.callout("Analogy: You're manually inspecting every house on the street looking for houses "
                  "where every room is a different colour. Correct, but very slow for large streets.",
                  "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        """def countNumbersWithUniqueDigits_brute(n: int) -> int:
    count = 0
    for x in range(10 ** n):
        s = str(x)
        if len(set(s)) == len(s):
            count += 1
    return count""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count = 0", {"code": True}), " — initialise our tally of unique-digit numbers."])),
    N.para(N.rich([("for x in range(10 ** n)", {"code": True}),
                   " — iterate over every integer from 0 up to (but not including) 10^n."])),
    N.para(N.rich([("s = str(x)", {"code": True}),
                   " — convert the integer to its digit string for easy character inspection."])),
    N.para(N.rich([("if len(set(s)) == len(s)", {"code": True}),
                   " — a set of characters removes duplicates; if the set length equals the string "
                   "length, every character is unique."])),
    N.para(N.rich([("count += 1", {"code": True}), " — this number qualifies; tally it."])),
    N.para(N.rich([("return count", {"code": True}),
                   " — return the final count after checking all numbers."])),
    N.divider(),
]

# ── Solution 2 — DP / Permutation Counting (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 2 — Permutation Counting DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of checking each number, ask: how many d-digit numbers (1 ≤ d ≤ n) "
               "have all unique digits? Then sum those counts and add 1 for the number 0."),
        N.h4("What Doesn't Work"),
        N.para("Brute force is O(10^n × n) — too slow for large n. "
               "We need to count valid numbers by reasoning about their digit structure, not by enumeration."),
        N.h4("The Key Observation"),
        N.para("A d-digit number with unique digits is formed by choosing digits without repetition: "
               "• The leading digit (position 1) can be 1–9 → 9 choices (no leading zero). "
               "• Position 2 can be 0–9 except the first digit → 9 choices. "
               "• Position 3 has 8 remaining choices. "
               "• … "
               "• Position d has (10 - d + 1) choices. "
               "So the count of d-digit unique-digit numbers = 9 × 9 × 8 × 7 × … × (10 - d + 1)."),
        N.h4("Building the Solution"),
        N.para("Start with ans = 1 (for x = 0). "
               "For d from 1 to min(n, 10): multiply out the permutation formula for d digits "
               "and add it to ans. We stop at d = 10 because with 11 digits you'd have to repeat "
               "(only 10 distinct digits exist)."),
        N.callout("Analogy: You're assigning distinct jersey numbers to team members. "
                  "First player picks from 9 non-zero options; every subsequent player picks "
                  "from the pool minus what's already taken. The product of choices is the count of "
                  "valid assignments — no need to enumerate them all.",
                  "🧠", "blue_background"),
    ]),
    N.h3("🔬 Why is This Dynamic Programming?"),
    N.para("This problem exhibits both pillars of DP:"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   ("The count of n-digit unique-digit numbers can be built from the count for "
                    "(n-1)-digit numbers plus new d-digit contributions.")])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   ("The permutation product f(d) = 9 × 9 × 8 × … × (10 - d + 1) is computed "
                    "iteratively; each step reuses the previous multiplier rather than recomputing from scratch.")])),
    N.code(
        """# Recurrence relations:
# unique(1)  = 9                          (single non-zero digit)
# unique(d)  = 9 * unique_suffix(d-1)     where
# unique_suffix(k) = choices for positions 2..d = 9 * 8 * ... * (10 - k)
# ans(n) = 1 + sum(unique(d) for d in 1..min(n, 10))""",
        "python"
    ),
    N.h3("Code"),
    N.code(
        """def countNumbersWithUniqueDigits(n: int) -> int:
    if n == 0:
        return 1

    ans = 10          # all 1-digit numbers 0-9 are unique
    unique_digits = 9 # count of d-digit unique numbers so far (d=1 gives 9: 1-9)
    available = 9     # digits still available for the next position

    for d in range(2, min(n, 10) + 1):
        unique_digits *= available  # multiply by remaining choices
        ans += unique_digits        # add d-digit unique numbers
        available -= 1             # one fewer digit available

    return ans""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if n == 0: return 1", {"code": True}),
                   " — base case: only x = 0 qualifies when n = 0."])),
    N.para(N.rich([("ans = 10", {"code": True}),
                   " — start with 10, accounting for all 1-digit numbers: 0 through 9 "
                   "(each is trivially unique)."])),
    N.para(N.rich([("unique_digits = 9", {"code": True}),
                   " — for d = 1, there are 9 non-zero 1-digit unique numbers (1-9); "
                   "we'll use this to build up counts for longer numbers."])),
    N.para(N.rich([("available = 9", {"code": True}),
                   " — after fixing the leading digit (9 choices), the second position "
                   "has 9 remaining choices (0-9 minus the first digit)."])),
    N.para(N.rich([("for d in range(2, min(n, 10) + 1)", {"code": True}),
                   " — iterate over digit lengths 2 up to min(n, 10). We cap at 10 "
                   "because no 11-digit number can have all unique digits."])),
    N.para(N.rich([("unique_digits *= available", {"code": True}),
                   " — extend the permutation product by one more position; "
                   "'available' is the number of unchosen digits for this position."])),
    N.para(N.rich([("ans += unique_digits", {"code": True}),
                   " — add the count of d-digit unique-digit numbers to our running total."])),
    N.para(N.rich([("available -= 1", {"code": True}),
                   " — each additional digit position has one fewer choice."])),
    N.para(N.rich([("return ans", {"code": True}),
                   " — return the total count across all lengths 0 through n."])),
    N.callout(
        "Why start ans = 10 and unique_digits = 9? "
        "We handle d = 1 specially: all 10 single-digit numbers are valid (0-9). "
        "But the permutation formula for d = 1 would give 9 (leading digit only, no 0). "
        "Starting ans = 10 includes 0, and setting unique_digits = 9 seeds the recurrence "
        "for the loop which multiplies by 'available' each iteration.",
        "⚠️", "yellow_background"
    ),
    N.callout(
        "Extensions: "
        "• Count numbers with all distinct digits in [l, r] → use the same DP up to each bound. "
        "• Count with a specific digit disallowed → adjust the initial choices. "
        "• Generalise to base-b numbers → replace 9 and 10 with b-1 and b.",
        "🎯", "green_background"
    ),
    N.divider(),
]

# ── Solution 3 — Memoization (Top-Down) ──────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Memoization (Top-Down Recursive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Express the count recursively: f(d) = count of d-digit unique-digit numbers. "
               "f(d) = 9 * f_suffix(d-1) where f_suffix(k) = number of ways to pick k more "
               "digits (non-leading) from the remaining pool."),
        N.h4("The Key Observation"),
        N.para("The recursive structure mirrors the permutation product. "
               "Since each subproblem (choices for remaining positions) is independent of the "
               "specific digits already chosen, we can memoize on just the length."),
        N.h4("Building the Solution"),
        N.para("Write a recursive helper that tracks how many digits have been placed. "
               "Cache results by (digits_placed, available_choices) — or equivalently by (d, available). "
               "Sum the memoized counts for each length from 0 to n."),
    ]),
    N.h3("Code"),
    N.code(
        """from functools import lru_cache

def countNumbersWithUniqueDigits_memo(n: int) -> int:
    @lru_cache(maxsize=None)
    def dp(digits_placed: int, available: int) -> int:
        \"\"\"Returns count of unique-digit tails of length digits_placed,
        given 'available' digit choices remaining.\"\"\"
        if digits_placed == 0:
            return 1
        # At this position: available choices, then recurse for the rest
        return available * dp(digits_placed - 1, available - 1)

    ans = 1  # count x = 0
    for d in range(1, min(n, 10) + 1):
        # Leading digit: 9 choices (1-9), remaining d-1 positions: 9, 8, ...
        ans += 9 * dp(d - 1, 9)
    return ans""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   " — memoize the recursive function so repeated subproblems (same digits_placed, "
                   "same available) are computed only once."])),
    N.para(N.rich([("def dp(digits_placed, available)", {"code": True}),
                   " — returns the number of valid suffixes of length digits_placed "
                   "when there are 'available' digit choices at the current position."])),
    N.para(N.rich([("if digits_placed == 0: return 1", {"code": True}),
                   " — base case: an empty suffix has exactly 1 way to be formed (do nothing)."])),
    N.para(N.rich([("return available * dp(digits_placed - 1, available - 1)", {"code": True}),
                   " — multiply current choices by sub-choices; "
                   "available decrements because one digit is now used."])),
    N.para(N.rich([("ans += 9 * dp(d - 1, 9)", {"code": True}),
                   " — 9 choices for the leading (non-zero) digit, then dp handles the rest "
                   "starting with 9 remaining choices for position 2."])),
    N.divider(),
]

# ── Complexity table ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Enumeration", "O(10^n × n)", "O(n)"],
        ["Permutation Counting DP (Bottom-Up)", "O(n)", "O(1)"],
        ["Memoization (Top-Down)", "O(n)", "O(n) cache"],
    ]),
    N.para("The bottom-up DP runs a loop up to min(n, 10), which is O(1) in practice "
           "(at most 9 iterations). Even calling it O(n) is generous — it is essentially constant."),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Permutation Count"])),
    N.callout(
        "When to recognize this pattern: "
        "• Problem asks 'count numbers with property X in range [0, 10^n)'. "
        "• The property depends on digit composition, not digit order. "
        "• You can enumerate valid numbers by counting digit choices combinatorially "
        "  (leading × non-leading permutations). "
        "• Similar signal to DP Digit problems (Numbers At Most N Given Digit Set, etc.).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Permutation Count / Digit DP technique:"),
    N.bullet(N.rich([("Numbers At Most N Given Digit Set", {"bold": True}),
                     (" (Hard) — digit DP with a restricted digit set; same combinatorial reasoning.")])),
    N.bullet(N.rich([("Number of Digit One", {"bold": True}),
                     (" (Hard) — count how many times digit 1 appears across [1, n]; "
                      "requires positional digit DP.")])),
    N.bullet(N.rich([("Digit Count in Range", {"bold": True}),
                     (" (Hard) — generalise digit occurrence count to any digit in [lo, hi].")])),
    N.bullet(N.rich([("Count Vowels Permutation", {"bold": True}),
                     (" (Hard) — count strings of length n following vowel adjacency rules; "
                      "same permutation-product DP structure.")])),
    N.bullet(N.rich([("New 21 Game", {"bold": True}),
                     (" (Medium) — counting valid sequences under sum constraints; "
                      "combinatorial DP in a different domain.")])),
    N.bullet(N.rich([("Unique Morse Code Words", {"bold": True}),
                     (" (Easy) — counting distinct encodings; simpler combinatorial counting.")])),
    N.bullet(N.rich([("Permutations", {"bold": True}),
                     (" (Medium) — generate all permutations; the combinatorial identity behind "
                      "this problem's counting formula.")])),
    N.para("These problems share the core technique: reason about valid choices at each position "
           "and multiply (or sum products) rather than enumerate."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), "
              "Sub-section: DP: Digit / Permutation Count.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
