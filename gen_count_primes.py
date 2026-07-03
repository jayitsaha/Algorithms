"""
gen_count_primes.py — Notion page generator for Count Primes (LC #204)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8108-8e8c-d7e0efd00ca0"
SLUG    = "count_primes"

# ── 1) Set properties ─────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 204,
    pattern     = "Math",
    subpatterns = ["Sieve of Eratosthenes"],
    tc          = "O(n log log n)",
    sc          = "O(n)",
    key_insight = "Mark all multiples of each confirmed prime as composite; what remains is prime.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ──────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an integer ", ("n", {"code": True}),
        ", return the number of prime numbers that are strictly less than ", ("n", {"code": True}), "."
    ])),
    N.para("A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. For example: countPrimes(10) = 4 because the primes below 10 are {2, 3, 5, 7}."),
    N.divider(),
]

# ── Solution 1: Sieve of Eratosthenes ─────────────────────────────────
blocks += [
    N.h2("Solution 1 — Sieve of Eratosthenes (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count numbers in [2, n) that have no divisors other than 1 and themselves. Testing each number individually requires O(√i) per number — too slow for n = 10⁶."),
        N.h4("What Doesn't Work"),
        N.para("Trial division (checking each number from 2 to √i for divisibility) gives O(n√n) total. For n = 10⁶, that's roughly 10⁹ operations — a TLE."),
        N.h4("The Key Observation"),
        N.para("If p is prime, then every multiple of p greater than p itself is composite. Instead of discovering this one composite at a time via division, we can mark p², p²+p, p²+2p, … all composite at once. This bulk elimination is far cheaper than individual testing."),
        N.h4("Building the Solution"),
        N.para("Start with is_prime = [True]*n. Mark 0 and 1 False. For each p from 2 to √n: if is_prime[p] is still True, p is confirmed prime; mark all its multiples starting at p² as False. We start at p² because every multiple p·k with k < p has already been marked by the prime factor of k (which is < p). After processing all pivots up to √n, sum(is_prime) is the answer."),
        N.callout("Analogy: Imagine crossing out all even numbers on a number line — at once. Then cross out all multiples of 3 not already crossed. Each pass eliminates a whole arithmetic progression in one sweep.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Sieve of Eratosthenes"),
    N.para(N.rich([
        ("Algorithm Name & Origin: ", {"bold": True}),
        "Sieve of Eratosthenes, invented by Eratosthenes of Cyrene (~276–194 BCE). Solves: 'Generate / count all primes up to N.' Still the standard algorithm 2,200 years later."
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        "When the outer loop reaches pivot p, every prime smaller than p has already run its inner loop. Therefore if is_prime[p] is still True, no prime < p divides p — so p is definitively prime."
    ])),
    N.para(N.rich([
        ("Why start inner loop at p²: ", {"bold": True}),
        "For prime p, the composite p·k where k < p has a prime factor ≤ k < p. That factor's inner loop already marked p·k False. So p² is the first new composite that p's inner loop discovers."
    ])),
    N.para(N.rich([
        ("Why outer loop runs only to √n: ", {"bold": True}),
        "Any composite c ≤ n has at least one prime factor f ≤ √c ≤ √n. Processing all primes up to √n guarantees all composites are marked."
    ])),
    N.para(N.rich([
        ("Time Complexity: ", {"bold": True}),
        "O(n log log n) by Mertens' second theorem: the sum Σ(n/p) over all primes p ≤ n ≈ n·ln(ln(n)). For n=10⁶: ~4n ops vs naïve's ~1000n ops."
    ])),
    N.para(N.rich([
        ("When to Recognize: ", {"bold": True}),
        "'Count/generate all primes up to N', 'multiple primality queries offline', 'find numbers with prime-related properties for N up to 10⁷.'"
    ])),
    N.h3("Code"),
    N.code(
        "def countPrimes(n: int) -> int:\n"
        "    if n < 2: return 0\n"
        "    is_prime = [True] * n\n"
        "    is_prime[0] = is_prime[1] = False\n"
        "    p = 2\n"
        "    while p * p < n:\n"
        "        if is_prime[p]:\n"
        "            for j in range(p * p, n, p):\n"
        "                is_prime[j] = False\n"
        "        p += 1\n"
        "    return sum(is_prime)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if n < 2: return 0", {"code": True}), " — Edge case: no primes exist below 2. Return immediately."])),
    N.para(N.rich([("is_prime = [True] * n", {"code": True}), " — Allocate n booleans, all True ('possibly prime'). Index i represents the number i."])),
    N.para(N.rich([("is_prime[0] = is_prime[1] = False", {"code": True}), " — 0 and 1 are not prime by mathematical convention. Pre-mark them."])),
    N.para(N.rich([("while p * p < n:", {"code": True}), " — Loop only up to √n. If p > √n, p² > n — no multiples to mark within the array."])),
    N.para(N.rich([("if is_prime[p]:", {"code": True}), " — If p was never marked composite, p is confirmed prime. Skip composites entirely."])),
    N.para(N.rich([("for j in range(p*p, n, p):", {"code": True}), " — Inner loop: start at p², step by p. Marks all as-yet-unmarked multiples of p."])),
    N.para(N.rich([("is_prime[j] = False", {"code": True}), " — j is composite (divisible by p, and j > p)."])),
    N.para(N.rich([("return sum(is_prime)", {"code": True}), " — Count all True entries. Python sums booleans as 0/1. Result is number of primes < n."])),
    N.divider(),
]

# ── Solution 2: Naïve Trial Division ──────────────────────────────────
blocks += [
    N.h2("Solution 2 — Naïve Trial Division"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Test each candidate number independently: is i prime?"),
        N.h4("What Doesn't Work"),
        N.para("Testing each divisor from 2 to i-1 is O(i) per number — O(n²) total. Way too slow."),
        N.h4("The Key Observation"),
        N.para("If i is composite, it has a factor f ≤ √i (because if both factors exceed √i, their product exceeds i — contradiction). So we only need to check divisors up to √i."),
        N.h4("Building the Solution"),
        N.para("For each i from 2 to n-1, run trial division up to √i. Count those that pass. O(n√n) total — acceptable for n up to ~10³ but TLEs for n ≥ 10⁶."),
    ]),
    N.h3("Code"),
    N.code(
        "def countPrimes_naive(n: int) -> int:\n"
        "    def is_prime(num):\n"
        "        if num < 2: return False\n"
        "        for d in range(2, int(num**0.5) + 1):\n"
        "            if num % d == 0:\n"
        "                return False\n"
        "        return True\n"
        "    return sum(is_prime(i) for i in range(n))"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def is_prime(num):", {"code": True}), " — Helper: returns True if num is prime."])),
    N.para(N.rich([("for d in range(2, int(num**0.5)+1):", {"code": True}), " — Check all potential divisors up to √num."])),
    N.para(N.rich([("if num % d == 0: return False", {"code": True}), " — d divides num evenly → num is composite."])),
    N.para(N.rich([("return sum(is_prime(i) for i in range(n))", {"code": True}), " — O(n√n) total. TLEs for n ≥ 10⁶."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Trial Division (naïve)", "O(n√n)", "O(1)"],
        ["Sieve of Eratosthenes ✓", "O(n log log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Sieve of Eratosthenes"])),
    N.callout(
        "When to recognize this pattern: "
        "Count or generate all primes up to N. Multiple primality queries with offline pre-computation. "
        "Problems where N is up to 10⁶–10⁷ (sieve fits in ~1–10 MB RAM). "
        "Any problem requiring smallest-prime-factor or divisor-count for all numbers up to N.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Sieve of Eratosthenes / Math):"),
    N.bullet(N.rich([("Ugly Number II", {"bold": True}), " (Medium) — nth number with only prime factors 2, 3, 5; uses sieve-like DP generation (#264)"])),
    N.bullet(N.rich([("Closest Prime Numbers in Range", {"bold": True}), " (Medium) — sieve a range then scan for adjacent primes with minimum gap (#2523)"])),
    N.bullet(N.rich([("Prime Arrangements", {"bold": True}), " (Easy) — permutations where primes sit in prime positions; needs countPrimes as a sub-step (#1175)"])),
    N.bullet(N.rich([("Four Divisors", {"bold": True}), " (Medium) — sieve-like enumeration of numbers with exactly 4 divisors (#1390)"])),
    N.bullet(N.rich([("Count Good Numbers", {"bold": True}), " (Medium) — digit-level prime awareness with fast exponentiation (#1922)"])),
    N.bullet(N.rich([("SPF Sieve + Factor Queries", {"bold": True}), " (Medium) — precompute smallest prime factor sieve for O(log n) factorization per query"])),
    N.para("These problems share the core technique: pre-compute prime structure for [2, N] in bulk, then answer queries in O(1) or O(log n)."),
    N.callout("Reference: Sieve of Eratosthenes is a classical Math algorithm. Classification source: Analysis.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the Sieve visually — use Next/Prev or arrow keys to see each pivot prime eliminate its composites.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
