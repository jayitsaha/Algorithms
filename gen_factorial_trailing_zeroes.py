"""Notion update script for Factorial Trailing Zeroes (#172) — Math / Count Factors of 5."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-811b-8ea4-ed37be5eed70"

# ── 1) Set properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=172,
    pattern="Math",
    subpatterns=["Count Factors of 5"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Each trailing zero needs one pair of (2,5). Fives are scarce: count multiples of 5, 25, 125, ... via n//5 + n//25 + n//125 + ...",
    icon="🟡"
)
print("Properties set OK")

# ── 2) Wipe existing body ──────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ── 3) Build body ─────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para("Given an integer n, return the number of trailing zeroes in n! (n factorial)."),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            "n=5 → 5! = 120 → 1 trailing zero.\n",
            ("Example 2: ", {"bold": True}),
            "n=10 → 10! = 3628800 → 2 trailing zeroes.\n",
            ("Example 3: ", {"bold": True}),
            "n=25 → 25! has 6 trailing zeroes (25 contributes TWO fives).\n",
            ("Constraint: ", {"bold": True}),
            "0 ≤ n ≤ 10⁴. Must run in O(log n) time."
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 — Count Factors of 5 (Interview Pick) ─────────
blocks += [
    N.h2("Solution 1 — Count Factors of 5 (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A trailing zero is produced by multiplying 10 = 2 × 5. So the number of "
            "trailing zeroes equals the number of (2, 5) factor pairs in n!. Since the "
            "prime factorisation of n! contains far more 2s than 5s (every even number "
            "contributes a 2; only multiples of 5 contribute a 5), the limiting factor is "
            "always the count of 5s in the prime factorisation of n!."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Computing n! directly is impossible for large n (factorial of 10000 is "
            "astronomical). Even counting trailing zeroes on the string representation of "
            "the computed factorial overflows standard integer types. We need a purely "
            "mathematical counting approach."
        ),
        N.h4("The Key Observation"),
        N.para(
            "How many times does 5 appear as a prime factor across 1 × 2 × ... × n? "
            "Every multiple of 5 contributes at least one 5. Every multiple of 25 "
            "contributes an extra 5 (because 25 = 5²). Every multiple of 125 contributes "
            "yet another, and so on. So the total count is: "
            "⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ⌊n/625⌋ + ... (until the divisor exceeds n)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Start with divisor = 5. While divisor ≤ n, add n // divisor to our count, "
            "then multiply divisor by 5. This loop runs at most log₅(n) times — about 6 "
            "times for n = 10000. The answer is the final count."
        ),
        N.callout(
            "Analogy: Imagine stacking coins. Every $5 bill contributes 1 coin, every "
            "$25 bill contributes 2 coins (one more than a $5), every $125 bill "
            "contributes 3 coins. Count each denomination separately and add up.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def trailingZeroes(n: int) -> int:\n"
        "    count = 0\n"
        "    divisor = 5\n"
        "    while divisor <= n:\n"
        "        count += n // divisor   # multiples of this power of 5\n"
        "        divisor *= 5            # next power: 25, 125, 625, ...\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("count = 0", {"code": True}),
        " — Running total of factor-5 contributions across all numbers 1…n."
    ])),
    N.para(N.rich([
        ("divisor = 5", {"code": True}),
        " — Start at 5¹ = 5. We'll check 5, 25, 125, 625, … in successive iterations."
    ])),
    N.para(N.rich([
        ("while divisor <= n:", {"code": True}),
        " — Only count powers of 5 that can actually appear in 1…n. Once divisor > n, "
        "n // divisor = 0 anyway, so we stop early."
    ])),
    N.para(N.rich([
        ("count += n // divisor", {"code": True}),
        " — n // divisor gives how many multiples of 'divisor' are in [1, n]. Each such "
        "multiple contributes exactly one additional factor of 5 at this power level."
    ])),
    N.para(N.rich([
        ("divisor *= 5", {"code": True}),
        " — Move to next power of 5. Multiples of 25 were already counted once via "
        "divisor=5; now they get their extra count via divisor=25. This is correct "
        "because ⌊n/5⌋ counts them once, ⌊n/25⌋ adds 1 more for the second factor, etc."
    ])),
    N.para(N.rich([
        ("return count", {"code": True}),
        " — Total number of 5-factor pairs = total trailing zeroes in n!."
    ])),
    N.divider(),
]

# ── Solution 2 — Recursive / Divide Approach ────────────────────
blocks += [
    N.h2("Solution 2 — Recursive Reformulation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Notice that trailingZeroes(n) = ⌊n/5⌋ + trailingZeroes(⌊n/5⌋). "
            "The first term counts direct multiples of 5 up to n. The recursive call "
            "handles the 'double-count' for multiples of 25 (since ⌊25/5⌋ = 5 is itself "
            "a multiple of 5) — exactly what we want."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This is an alternative framing; both iterative and recursive are O(log n). "
            "The recursive version has O(log n) call-stack depth, which is fine in "
            "practice but uses O(log n) space vs. O(1) for the iterative approach."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Dividing n by 5 is equivalent to zooming in: 'among the ⌊n/5⌋ multiples "
            "of 5, how many are themselves multiples of 5 (i.e., multiples of 25)?' "
            "The recursion bottoms out at 0."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base case: n < 5 → return 0 (no multiples of 5). "
            "Recursive step: return n // 5 + trailingZeroes(n // 5)."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def trailingZeroes(n: int) -> int:\n"
        "    if n < 5:\n"
        "        return 0\n"
        "    return n // 5 + trailingZeroes(n // 5)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if n < 5: return 0", {"code": True}),
        " — Base case: no multiples of 5 exist below 5, so no trailing zeroes contributed."
    ])),
    N.para(N.rich([
        ("return n // 5 + trailingZeroes(n // 5)", {"code": True}),
        " — n // 5 counts how many multiples of 5 are in [1, n]. Each of those multiples "
        "may itself be a multiple of 5 — that's handled by the recursive call on n // 5."
    ])),
    N.divider(),
]

# ── Solution 3 — Naive (count by computing) ─────────────────────
blocks += [
    N.h2("Solution 3 — Naive (Why It Fails)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The brute-force approach: multiply all numbers from 1 to n, then count "
            "trailing zeroes in the result. While logically correct for small n, this "
            "fails catastrophically in practice."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "n! grows super-exponentially. For n=1000, n! has over 2500 digits. Python "
            "can handle big integers, but this is astronomically slow and wastes memory. "
            "For n=10000, computing the factorial takes billions of multiplications. "
            "The O(log n) factor-counting approach is 9+ orders of magnitude faster."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This naive approach illustrates WHY the mathematical insight matters in "
            "interviews. Recognizing that you don't need the actual factorial — just "
            "the count of factor-5 contributions — is the core insight tested."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "# DO NOT USE for large n — shown only to contrast with the optimal approach\n"
        "import math\n"
        "def trailingZeroes_naive(n: int) -> int:\n"
        "    factorial = math.factorial(n)   # O(n log n) digit operations, huge memory\n"
        "    count = 0\n"
        "    while factorial % 10 == 0:      # count trailing zeroes one at a time\n"
        "        count += 1\n"
        "        factorial //= 10\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("factorial = math.factorial(n)", {"code": True}),
        " — Computes n! exactly. Correct but wildly impractical for n > a few thousand."
    ])),
    N.para(N.rich([
        ("while factorial % 10 == 0:", {"code": True}),
        " — Counts trailing zeroes by peeling off 10s. Correct but again, working with "
        "a number that may have thousands of digits."
    ])),
    N.callout(
        "This approach is O(n log n) time and O(n) space — fail for large n. "
        "The optimal approach is O(log n) time and O(1) space. Always use Solution 1 in interviews.",
        "⚠️", "red_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Count Factors of 5 (Iterative) — Interview Pick", "O(log n)", "O(1)"],
        ["Recursive Reformulation", "O(log n)", "O(log n) stack"],
        ["Naive Compute Factorial", "O(n log n)", "O(n)"],
    ]),
    N.para(N.rich([
        ("Why O(log n)?", {"bold": True}),
        " The outer loop runs while divisor = 5^k ≤ n, so k ≤ log₅(n). "
        "For n=10⁴, log₅(10000) ≈ 5.7, so the loop runs at most 6 times. "
        "This is extraordinarily fast regardless of how large n is."
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Count Factors of 5"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            "The problem involves n! (factorial) and asks for properties of the result "
            "(digit count, trailing zeroes, divisibility). Computing n! is never the "
            "answer — instead, count prime factor contributions mathematically using "
            "Legendre's formula: sum of ⌊n/p^k⌋ for increasing k."
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Legendre's Formula (generalization): ", {"bold": True}),
        "The exponent of prime p in n! is ∑_{k=1}^{∞} ⌊n/p^k⌋. "
        "For trailing zeroes, p=5 (since 2s always outnumber 5s in n!)."
    ])),
    N.divider(),
]

# ── Algorithm Deep-Dive ───────────────────────────────────────
blocks += [
    N.h2("🔬 Algorithm Deep-Dive: Legendre's Formula"),
    N.para(
        "Adrien-Marie Legendre (1830) proved that the exact power of a prime p dividing "
        "n! equals ∑_{k=1}^{∞} ⌊n/p^k⌋. This series terminates because ⌊n/p^k⌋ = 0 "
        "once p^k > n."
    ),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        "Every multiple of p contributes 1 factor. Every multiple of p² contributes an "
        "additional factor (already counted once above). Every multiple of p³ adds yet "
        "another. Summing across all powers is equivalent to summing the exact power of "
        "p in each number from 1 to n."
    ])),
    N.para(N.rich([
        ("Why Trailing Zeroes = Count of 5s: ", {"bold": True}),
        "10 = 2 × 5. Each trailing zero requires one 2 and one 5. The count of factor-2s "
        "in n! is always ≥ count of factor-5s (because every even number contributes a 2, "
        "while only every fifth number contributes a 5). So 2s are never the bottleneck. "
        "The number of (2,5) pairs = min(#2s, #5s) = #5s."
    ])),
    N.code(
        "# Legendre's formula — count of prime p in n!\n"
        "def prime_power_in_factorial(n: int, p: int) -> int:\n"
        "    count = 0\n"
        "    pk = p\n"
        "    while pk <= n:\n"
        "        count += n // pk\n"
        "        pk *= p\n"
        "    return count\n"
        "\n"
        "# trailingZeroes(n) = min(prime_power_in_factorial(n, 2),\n"
        "#                         prime_power_in_factorial(n, 5))\n"
        "# But we know #2s >> #5s, so always = prime_power_in_factorial(n, 5)"
    ),
    N.para(N.rich([
        ("When to recognize this: ", {"bold": True}),
        "Problems involving n!, prime factorisation of a product, or 'how many times "
        "does n! divide evenly into X' — all use Legendre's formula."
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (prime factor counting / Legendre's formula):"),
    N.bullet(N.rich([
        ("Count Primes", {"bold": True}),
        " (Medium) — Count primes below n using the Sieve of Eratosthenes. (#204)"
    ])),
    N.bullet(N.rich([
        ("Ugly Number II", {"bold": True}),
        " (Medium) — Find nth ugly number (only prime factors 2, 3, 5). (#264)"
    ])),
    N.bullet(N.rich([
        ("Number of Digit One", {"bold": True}),
        " (Hard) — Count occurrences of digit 1 in all numbers from 1 to n. Same "
        "positional-counting technique. (#233)"
    ])),
    N.bullet(N.rich([
        ("Super Pow", {"bold": True}),
        " (Medium) — a^b mod 1337 where b is a large integer. Uses modular arithmetic "
        "with prime factorisation. (#372)"
    ])),
    N.bullet(N.rich([
        ("Preimage Size of Factorial Zeroes Function", {"bold": True}),
        " (Hard) — Binary search + Legendre to find n such that trailingZeroes(n) = k. (#793)"
    ])),
    N.bullet(N.rich([
        ("Greatest Common Divisor of Strings", {"bold": True}),
        " (Easy) — GCD applied to strings; uses modular arithmetic intuition. (#1071)"
    ])),
    N.para(
        "These problems all share the core technique of counting factor contributions "
        "mathematically rather than computing the actual product."
    ),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math section: "
        "\"Count Factors of 5\" sub-pattern. Verified: Guide confirms Factorial Trailing Zeroes "
        "as the canonical example of this sub-pattern.",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ── Interactive Explainer Embed ───────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("factorial_trailing_zeroes")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
