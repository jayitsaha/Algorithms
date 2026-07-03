"""
gen_ugly_number.py
Notion IN-PLACE update for LeetCode #263: Ugly Number
Run from the Algorithms directory: python3 gen_ugly_number.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-811c-ac84-d2c75c3cdc04"
SLUG = "ugly_number"

print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=263,
    pattern="Math",
    subpatterns=["Divide by 2, 3, 5"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Strip all factors of 2, 3, 5 via repeated division. If n reduces to 1, it is ugly; any other remainder contains a disallowed prime.",
    icon="🟢"
)
print("Properties set OK.")

print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("An ", {}),
        ("ugly number", {"bold": True}),
        (" is a positive integer whose only prime factors are ", {}),
        ("2", {"code": True}), (", ", {}), ("3", {"code": True}), (", and ", {}), ("5", {"code": True}),
        (". Given an integer ", {}), ("n", {"code": True}),
        (", return ", {}), ("true", {"code": True}),
        (" if ", {}), ("n", {"code": True}), (" is an ugly number.", {}),
    ])),
    N.callout(
        N.rich([
            ("Examples — Ugly: ", {"bold": True}),
            "1 (by convention), 6 = 2×3, 12 = 2²×3, 30 = 2×3×5.\n",
            ("Examples — Not Ugly: ", {"bold": True}),
            "14 = 2×7 (7 is not in {2,3,5}), 49 = 7² (only factor is 7)."
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Repeated Division (the only / optimal approach) ──────────
blocks += [
    N.h2("Solution 1 — Repeated Division by 2, 3, 5 (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The question is really asking: does n's prime factorization contain only the primes 2, 3, and 5? We need a way to check membership in the set of 'allowed' prime factors."),
        N.h4("What Doesn't Work"),
        N.para("Trial division of all primes up to sqrt(n) works but is overkill — we don't need to find ALL prime factors, just confirm they are all in {2, 3, 5}. A primality test is also unnecessary."),
        N.h4("The Key Observation"),
        N.para("If a number has only 2s, 3s, and 5s as prime factors, dividing out every 2, every 3, and every 5 will leave exactly 1. If any other prime p divides n, it cannot be removed by dividing by 2, 3, or 5 — so p will persist in n until the end."),
        N.h4("Building the Solution"),
        N.para("Step 1: Guard for n ≤ 0 (ugly numbers are positive by definition). Step 2: While n is divisible by 2, divide by 2. Step 3: While n is divisible by 3, divide by 3. Step 4: While n is divisible by 5, divide by 5. Step 5: Return n == 1."),
        N.callout(
            "Analogy: To verify a recipe uses only salt (2), pepper (3), and olive oil (5), taste out each ingredient one by one. If nothing remains, the recipe was clean. If a mystery flavor persists, something unauthorized was added.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isUgly(n: int) -> bool:\n"
        "    if n <= 0:    return False       # ugly numbers must be positive\n"
        "    for p in (2, 3, 5):\n"
        "        while n % p == 0:\n"
        "            n //= p                 # strip one factor of p\n"
        "    return n == 1                   # 1 = all factors were 2/3/5",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("if n <= 0: return False", {"code": True}),
        " — Ugly numbers are positive integers. Reject 0 and negatives immediately. Without this guard, n=0 causes 0 % 2 == 0 → infinite loop.",
    ])),
    N.para(N.rich([
        ("for p in (2, 3, 5):", {"code": True}),
        " — Iterate over the three allowed prime factors in order. No other primes need to be considered.",
    ])),
    N.para(N.rich([
        ("while n % p == 0:", {"code": True}),
        " — Keep dividing as long as p divides n evenly. This strips ALL factors of p, not just one.",
    ])),
    N.para(N.rich([
        ("n //= p", {"code": True}),
        " — Integer division by p. Since n % p == 0, this is exact (no remainder lost). Each call reduces n strictly.",
    ])),
    N.para(N.rich([
        ("return n == 1", {"code": True}),
        " — After stripping all 2s, 3s, 5s: if n == 1, no foreign prime factors exist → ugly. If n > 1, whatever remains is a prime (or product of primes) not in {2,3,5} → not ugly.",
    ])),
    N.callout(
        "⚠️ Common Mistake: Writing return n == 0 at the end. After all valid divisions, the residue is 1 (ugly) or some integer > 1 (not ugly). Zero never appears as a result.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table(
        [
            ["Solution", "Time", "Space"],
            ["Repeated Division by 2, 3, 5", "O(log n)", "O(1)"],
        ],
        has_col_header=True
    ),
    N.para(N.rich([
        ("Justification: ", {"bold": True}),
        "Each while-loop division strictly reduces n. The total number of divisions is at most log₂(n) + log₃(n) + log₅(n) = O(log n). No extra data structures — O(1) space.",
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math (Number Theory)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Divide by 2, 3, 5", {"code": True}), " — Repeatedly divide by each allowed prime and check if the remainder is 1."])),
    N.callout(
        "When to recognize this pattern: problem says 'only prime factors are X, Y, Z' or 'smooth number'; need to verify prime factorization membership; any 'keep dividing until indivisible, then check residue' structure.",
        "🎯", "green_background"
    ),
    N.para(N.rich([
        ("Source: ", {"bold": True}),
        "DSA_Patterns_and_SubPatterns_Guide.md — Math section, row 1081: Ugly Number → 'Divide by 2, 3, 5'",
    ])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Ugly Number II (#264)", {"bold": True}), " (Medium) — Find the nth ugly number; uses three-pointer DP or min-heap"])),
    N.bullet(N.rich([("Super Ugly Number (#313)", {"bold": True}), " (Medium) — Generalize to k allowed prime factors with min-heap"])),
    N.bullet(N.rich([("Count Primes (#204)", {"bold": True}), " (Medium) — Sieve of Eratosthenes; identify primes (complementary knowledge)"])),
    N.bullet(N.rich([("Happy Number (#202)", {"bold": True}), " (Easy) — 'Transform until fixed point or cycle' divisibility pattern"])),
    N.bullet(N.rich([("Nth Magical Number (#878)", {"bold": True}), " (Hard) — Numbers with only factor a or b; LCM + binary search"])),
    N.bullet(N.rich([("Smallest Number Divisible by k (#1015)", {"bold": True}), " (Medium) — Modular arithmetic and divisibility checks"])),
    N.para("These problems share the core technique of reasoning about a number's prime factorization via repeated divisibility checks."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math (Number Theory) section, Sub-Pattern: Divide by 2, 3, 5 (Guide row 1081).", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Try different inputs (12, 14, 1, 0, 49) to see all code paths.", {"italic": True, "color": "gray"}),
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("Done! Notion page updated successfully.")
print(f"Page: https://www.notion.so/{PAGE_ID.replace('-', '')}")
print(f"HTML: https://jayitsaha.github.io/Algorithms/{SLUG}_explainer.html")
