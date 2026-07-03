"""
gen_ugly_number.py — Rebuild Notion page for LeetCode 263 · Ugly Number (Easy)
Math / Divide by 2 3 5 pattern
"""
import notion_lib as N

PAGE_ID = "39193418-809c-811c-ac84-d2c75c3cdc04"
SLUG = "ugly_number"

# ── 1) Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=263,
    pattern="Math",
    subpatterns=["Divide by 2 3 5"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Repeatedly divide by 2, 3, 5; if result is 1, the number is ugly.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("An "), ("ugly number", {"bold": True}),
        (" is a positive integer whose only prime factors are "),
        ("2", {"code": True}), (", "), ("3", {"code": True}), (", and "),
        ("5", {"code": True}), (". Given an integer "), ("n", {"code": True}),
        (", return "), ("True", {"code": True}),
        (" if "), ("n", {"code": True}),
        (" is an ugly number, or "), ("False", {"code": True}), (" otherwise. "
        "Note: 1 is considered an ugly number (it has no prime factors at all).")
    ])),
    N.callout(
        "Examples:\n"
        "  n = 6  -> True   (6 = 2 x 3)\n"
        "  n = 14 -> False  (14 = 2 x 7; 7 is not 2, 3, or 5)\n"
        "  n = 1  -> True   (1 has no prime factors, conventionally included)",
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — Iterative Division (Interview Pick) ──────────────────────────
sol1_code = """\
def isUgly(n: int) -> bool:
    if n <= 0:
        return False
    for prime in (2, 3, 5):
        while n % prime == 0:
            n //= prime
    return n == 1
"""

blocks += [
    N.h2("Solution 1 — Iterative Division (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to check whether n's only prime factors are 2, 3, and 5. "
            "Equivalently: if we strip out all factors of 2, 3, and 5 from n, "
            "is there anything left? If n reduces to 1, it was made entirely of "
            "2s, 3s, and 5s — so it's ugly. If a remainder > 1 remains, some other "
            "prime (7, 11, 13 …) was lurking inside."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute-force factorisation: find all primes up to n and check they're "
            "a subset of {2, 3, 5}. This is overkill and slow for large n. "
            "We don't need a full factorisation — we only care about whether ANY "
            "prime other than 2, 3, 5 divides n."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Division is the inverse of multiplication. If we repeatedly divide by "
            "2 until it no longer divides evenly, we've removed every factor of 2. "
            "Do the same for 3 and 5. Whatever remains must be coprime to all three. "
            "If that remainder is 1, n had ONLY factors from {2, 3, 5}. "
            "If it's anything else (must be >= 7), n is not ugly."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Guard: if n <= 0, return False immediately (definition excludes non-positives).\n"
            "2. For each prime p in (2, 3, 5): while p divides n, divide n by p.\n"
            "3. After all three loops, check n == 1.\n"
            "The order of the three primes doesn't matter; they're independent factors."
        ),
        N.callout(
            "Analogy: Think of n as a bag of marbles coloured Red (2), Blue (3), or Green (5). "
            "We pull out all Red marbles, then all Blue, then all Green. "
            "If the bag is empty (n = 1), it was a valid ugly-number bag. "
            "If marbles of another colour remain, it's not ugly.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if n <= 0: return False", {"code": True}),
                   " — Ugly numbers are positive by definition; handle the edge case first."])),
    N.para(N.rich([("for prime in (2, 3, 5):", {"code": True}),
                   " — Iterate over the three permitted prime factors."])),
    N.para(N.rich([("while n % prime == 0:", {"code": True}),
                   " — Keep dividing as long as this prime divides n evenly."])),
    N.para(N.rich([("n //= prime", {"code": True}),
                   " — Integer division strips out one occurrence of the prime."])),
    N.para(N.rich([("return n == 1", {"code": True}),
                   " — If nothing is left (n reduced to 1), all factors were in {2,3,5} — ugly!"])),
    N.divider(),
]

# ── Solution 2 — Recursive (Teaching Variant) ─────────────────────────────────
sol2_code = """\
def isUgly(n: int) -> bool:
    if n <= 0:
        return False
    if n == 1:
        return True
    if n % 2 == 0:
        return isUgly(n // 2)
    if n % 3 == 0:
        return isUgly(n // 3)
    if n % 5 == 0:
        return isUgly(n // 5)
    return False
"""

blocks += [
    N.h2("Solution 2 — Recursive Division"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Can we define 'ugly' recursively? A number n > 1 is ugly if one of "
            "2, 3, or 5 divides it AND n divided by that prime is also ugly. "
            "The base cases: n = 1 is ugly (empty product); n <= 0 is not ugly."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This is the same logic as Solution 1, written top-down instead of bottom-up. "
            "We peel off one prime factor at a time recursively. Python's recursion depth "
            "is fine here — log2(2^31) ~= 31 recursive calls maximum."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. n <= 0 -> False (base case: invalid).\n"
            "2. n == 1 -> True (base case: reduced completely).\n"
            "3. If 2, 3, or 5 divides n, recurse with n // prime.\n"
            "4. None divide -> False (some other prime factor remains)."
        ),
        N.callout(
            "When to use recursive vs iterative: The recursive version is elegant for "
            "teaching but the iterative version is preferred in interviews because it avoids "
            "call-stack overhead and is easier to reason about for large inputs.",
            "⚠️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if n <= 0: return False", {"code": True}),
                   " — Non-positive numbers are never ugly."])),
    N.para(N.rich([("if n == 1: return True", {"code": True}),
                   " — Base case: 1 is the trivially ugly number (no prime factors at all)."])),
    N.para(N.rich([("if n % 2 == 0: return isUgly(n // 2)", {"code": True}),
                   " — Strip one factor of 2 and recurse; isUgly will handle the rest."])),
    N.para(N.rich([("if n % 3 == 0: return isUgly(n // 3)", {"code": True}),
                   " — Same for 3."])),
    N.para(N.rich([("if n % 5 == 0: return isUgly(n // 5)", {"code": True}),
                   " — Same for 5."])),
    N.para(N.rich([("return False", {"code": True}),
                   " — n > 1 and none of {2,3,5} divide it -> some other prime factor exists."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Solution 1 — Iterative", "O(log n)", "O(1)", "At most log2n + log3n + log5n divisions"],
        ["Solution 2 — Recursive", "O(log n)", "O(log n)", "Stack depth = total divisions <= log2n"],
    ]),
    N.callout(
        "Why O(log n)? Each division by 2 halves n. In the worst case (n = 2^31), "
        "we divide by 2 about 31 times, by 3 about 0 times, by 5 about 0 times. "
        "Total operations <= log2n + log3n + log5n ~= 3 log2n = O(log n).",
        "📐", "gray_background"
    ),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Divide by 2 3 5 (Iterative Factorisation)"])),
    N.callout(
        "When to recognise this pattern:\n"
        "• Problem asks to check if a number belongs to a set defined by its prime factors.\n"
        "• 'Only prime factors are …' or 'product of primes from set S' in the problem statement.\n"
        "• Related: Ugly Number II (generate), Super Ugly Number, Count Primes.\n"
        "Signal: small, fixed set of allowed primes -> repeated division is optimal.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same prime-factorisation / iterative-division technique:"),
    N.bullet(N.rich([("Ugly Number II", {"bold": True}),
                     " (Medium) — Generate the nth ugly number; extends to min-heap / DP."])),
    N.bullet(N.rich([("Super Ugly Number", {"bold": True}),
                     " (Medium) — Generalise to an arbitrary set of primes; min-heap approach."])),
    N.bullet(N.rich([("Count Primes", {"bold": True}),
                     " (Medium) — Sieve of Eratosthenes; related prime-factor thinking."])),
    N.bullet(N.rich([("Perfect Squares", {"bold": True}),
                     " (Medium) — DP with math insight; similar 'reduce by allowed set' idea."])),
    N.bullet(N.rich([("Happy Number", {"bold": True}),
                     " (Easy) — Repeatedly apply a numeric transform and check for a target."])),
    N.bullet(N.rich([("Number of Steps to Reduce a Number to Zero", {"bold": True}),
                     " (Easy) — Repeated halving/decrement; same iterative reduction mindset."])),
    N.bullet(N.rich([("Factorial Trailing Zeroes", {"bold": True}),
                     " (Medium) — Count factors of 5; directly related prime-factor counting."])),
    N.para("These problems share the core technique: iteratively reduce n using allowed operations "
           "and check what remains."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math section (Iterative factorisation / "
        "Divide by primes sub-pattern). Ugly Number is the canonical example of this technique.",
        "📚", "gray_background"
    ),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append ─────────────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} top-level blocks to {PAGE_ID}")
