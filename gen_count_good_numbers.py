"""
gen_count_good_numbers.py
Notion in-place update for LC #1922 Count Good Numbers
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813f-ba61-e680befa96bd"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1922,
    pattern="Math",
    subpatterns=["Fast Exponentiation"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="5^ceil(n/2) x 4^floor(n/2) mod 1e9+7; binary exp reduces ~10^15 to 50 iterations.",
    icon="🟡",
)
print("Properties set OK")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("num", {"code": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (", return the count of ", {}),
        ("good digit strings", {"bold": True}),
        (" of length ", {}),
        ("n", {"code": True}),
        (". A digit string is ", {}),
        ("good", {"italic": True}),
        (" if every even-indexed position (0, 2, 4, …) contains an even digit (0, 2, 4, 6, 8) "
         "and every odd-indexed position (1, 3, 5, …) contains a prime digit (2, 3, 5, 7). "
         "Return the answer modulo 10^9 + 7.", {}),
    ])),
    N.callout(
        N.rich([("n can be up to 10^15 — direct loop is TLE. This is a math + fast exponentiation problem.", {})]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 1 — Python Built-in pow (Interview Pick) ─────────────────────
blocks += [
    N.h2("Solution 1 — Python Built-in pow (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each position in the digit string is independent of every other position. "
               "At each even index we choose from {0,2,4,6,8} — 5 options. At each odd index "
               "we choose from {2,3,5,7} — 4 options. The total number of valid strings is "
               "the product of all these independent choices."),
        N.h4("What Doesn't Work"),
        N.para("A naive loop multiplying 5 or 4 into a running product n times would work "
               "logically but is O(n) and TLE for n=10^15 (~3 million seconds at 10^8 ops/s). "
               "Even a simple 'for i in range(n): result = result * (5 if i%2==0 else 4) % MOD' "
               "is too slow."),
        N.h4("The Key Observation"),
        N.para("The answer is 5^e * 4^o mod M where e = ceil(n/2) = (n+1)//2 even positions "
               "and o = floor(n/2) = n//2 odd positions. Computing x^n mod M for large n in O(log n) "
               "is precisely what binary exponentiation does. Python's three-argument pow(x, n, mod) "
               "implements this for free."),
        N.h4("Building the Solution"),
        N.para("1) Count: e=(n+1)//2, o=n//2. "
               "2) Compute pow(5, e, MOD) using binary exp (~50 iterations for n=10^15). "
               "3) Compute pow(4, o, MOD) the same way. "
               "4) Multiply and mod: return (pow5 * pow4) % MOD."),
        N.callout("Analogy: Instead of counting one sheep at a time for 10^15 sheep, we double the group size repeatedly — log2(10^15) ≈ 50 doublings vs 10^15 steps.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def countGoodNumbers(n: int) -> int:
    MOD = 10**9 + 7
    even_count = (n + 1) // 2   # positions 0, 2, 4, ... -> ceil(n/2)
    odd_count  = n // 2          # positions 1, 3, 5, ... -> floor(n/2)
    return (pow(5, even_count, MOD) * pow(4, odd_count, MOD)) % MOD"""),
    N.h3("Line by Line"),
    N.para(N.rich([("MOD = 10**9 + 7", {"code": True}),
                   (" — standard LeetCode modulus; prevents astronomically large intermediate integers.", {})])),
    N.para(N.rich([("even_count = (n + 1) // 2", {"code": True}),
                   (" — ceil(n/2): count of even-indexed positions 0, 2, 4, …", {})])),
    N.para(N.rich([("odd_count = n // 2", {"code": True}),
                   (" — floor(n/2): count of odd-indexed positions 1, 3, 5, …", {})])),
    N.para(N.rich([("pow(5, even_count, MOD)", {"code": True}),
                   (" — three-argument pow uses binary exponentiation internally: O(log n). "
                    "5 choices at each even position.", {})])),
    N.para(N.rich([("pow(4, odd_count, MOD)", {"code": True}),
                   (" — same O(log n) binary exp. 4 prime-digit choices at each odd position.", {})])),
    N.para(N.rich([("return (...) % MOD", {"code": True}),
                   (" — each pow result is already < MOD, but their product may exceed MOD once, "
                    "so we take mod of the product.", {})])),
    N.divider(),
]

# ── Solution 2 — Manual Binary Exponentiation ─────────────────────────────
blocks += [
    N.h2("Solution 2 — Manual Binary Exponentiation (know the internals)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same formula as Solution 1 — 5^e * 4^o mod M. Now we implement the fast "
               "exponentiation ourselves to demonstrate understanding of the algorithm."),
        N.h4("What Doesn't Work"),
        N.para("A simple loop multiplying base by itself exp times is O(n). We need O(log n)."),
        N.h4("The Key Observation"),
        N.para("The key invariant: result * base^exp = original x^n at every step. "
               "We can safely square the base and halve the exponent (when even) without changing "
               "this product. When exp is odd, we first absorb one copy of base into result, "
               "making exp even, then proceed. This processes one binary bit of the exponent per iteration."),
        N.h4("Building the Solution"),
        N.para("Initialize result=1, base=x, exp=n. While exp>0: if exp%2==1, result=result*base%M. "
               "Then base=base*base%M, exp//=2. When exp=0, result holds x^n_original."),
        N.callout("The invariant 'result * base^exp = x^n_original' is the proof of correctness. "
                  "At exp=0: result * 1 = result = answer.", "🔐", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""def fast_pow(x: int, n: int, mod: int) -> int:
    result = 1           # multiplicative identity; invariant: result * x^n = answer
    x %= mod             # reduce base upfront
    while n > 0:
        if n % 2 == 1:   # current LSB is 1 -> absorb this base^(2^k) factor
            result = result * x % mod
        x = x * x % mod  # square base: x -> x^2 -> x^4 -> x^8 ...
        n //= 2           # shift right: process next higher bit
    return result         # n=0 -> result * x^0 = result = x^original_n

def countGoodNumbers(n: int) -> int:
    MOD = 10**9 + 7
    e, o = (n + 1) // 2, n // 2
    return fast_pow(5, e, MOD) * fast_pow(4, o, MOD) % MOD"""),
    N.h3("Line by Line"),
    N.para(N.rich([("result = 1", {"code": True}),
                   (" — accumulator starts at 1 (multiplicative identity). Invariant: result * x^n = final answer.", {})])),
    N.para(N.rich([("x %= mod", {"code": True}),
                   (" — reduce base once. Since (a*b)%M = ((a%M)*(b%M))%M, this is safe.", {})])),
    N.para(N.rich([("if n % 2 == 1:", {"code": True}),
                   (" — if the lowest bit of n is set, this power-of-2 contributes to the answer.", {})])),
    N.para(N.rich([("result = result * x % mod", {"code": True}),
                   (" — absorb this base factor into result. Mod prevents integer explosion.", {})])),
    N.para(N.rich([("x = x * x % mod", {"code": True}),
                   (" — square base: after k iterations, x = original_x^(2^k). This gives us x^(2^k) cheaply.", {})])),
    N.para(N.rich([("n //= 2", {"code": True}),
                   (" — integer divide by 2: shift the exponent right, processing one binary bit per iteration.", {})])),
    N.divider(),
]

# ── Algorithm Deep-Dive ───────────────────────────────────────────────────
blocks += [
    N.h2("🔬 Algorithm Deep-Dive: Binary / Fast Exponentiation"),
    N.para(N.rich([
        ("Algorithm Name: ", {"bold": True}), ("Binary Exponentiation", {}),
        (" (also: Exponentiation by Squaring, Fast Power, Square-and-Multiply)", {}),
    ])),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Known since ancient Indian mathematics (~200 BCE, Pingala). Formalized for computers "
         "in the context of modular arithmetic and RSA cryptography (1970s). "
         "Used in virtually every cryptographic library.", {}),
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("At every iteration, result × base^exp = original x^n. "
         "We start with 1 × x^n and end with x^n × x^0 = x^n. The identity holds throughout.", {}),
    ])),
    N.code("""# Standard binary exponentiation template:
def fast_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:  # if LSB is set (exp is odd)
            result = result * base % mod
        base = base * base % mod
        exp >>= 1    # right-shift (same as exp //= 2)
    return result

# Python shorthand (uses same algorithm internally):
result = pow(base, exp, mod)  # O(log exp)"""),
    N.para(N.rich([
        ("Why It Works: ", {"bold": True}),
        ("We process the binary representation of exp bit by bit. For bit k (value 2^k), "
         "if that bit is 1, we multiply result by base^(2^k). Since exp = sum of bk*2^k, "
         "multiplying those factors gives base^exp. The squaring step gives us base^(2^k) "
         "in k steps instead of 2^k multiplications.", {}),
    ])),
    N.para(N.rich([
        ("Complexity: ", {"bold": True}),
        ("O(log n) time — log2(10^15) ≈ 50 iterations. O(1) space. ", {}),
        ("Generalization: ", {"bold": True}),
        ("Works for any associative operation: matrix multiplication "
         "(→ Fibonacci in O(log n)), polynomial rings, modular inverses via Fermat "
         "(pow(a, MOD-2, MOD) for prime MOD).", {}),
    ])),
    N.callout(
        N.rich([("Recognize fast exp when: ", {"bold": True}),
                ("'return answer mod 10^9+7' + n up to 10^15; x^n with large n; "
                 "linear recurrence for large k via matrix exponentiation.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute force loop", "O(n)", "O(1)", "TLE: n up to 10^15"],
        ["Python pow(x,n,mod) — Sol 1", "O(log n)", "O(1)", "~50 iters for n=10^15; recommended"],
        ["Manual binary exp — Sol 2", "O(log n)", "O(1)", "Same algorithm, shows understanding"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Math", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Fast Exponentiation (Binary Exponentiation, Exponentiation by Squaring)", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("(1) 'return answer mod 10^9+7' appears with large exponents in constraints. "
                 "(2) Count of independent choices over n positions -> multiplication principle -> "
                 "large powers. (3) Constraints say n up to 10^14 or 10^15 -> O(log n) mandatory. "
                 "(4) Any 'compute x^n mod M' subproblem.", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Fast Exponentiation technique:"),
    N.bullet(N.rich([("Pow(x, n) (50)", {"bold": True}),
                     (" (Medium) — Implement fast power directly; handle negative exponents.", {})])),
    N.bullet(N.rich([("Super Pow (372)", {"bold": True}),
                     (" (Medium) — b^p mod 1337 where p is an array of digits; chunked binary exp.", {})])),
    N.bullet(N.rich([("Fibonacci Number (509)", {"bold": True}),
                     (" (Easy) — Standard DP; O(log n) matrix exponentiation extension.", {})])),
    N.bullet(N.rich([("Count Vowels Permutation (1220)", {"bold": True}),
                     (" (Hard) — State transition matrix raised to power n; matrix exponentiation.", {})])),
    N.bullet(N.rich([("Knight Dialer (935)", {"bold": True}),
                     (" (Medium) — Count knight-move sequences of length n; matrix exponentiation.", {})])),
    N.bullet(N.rich([("Numbers At Most N Given Digit Set (902)", {"bold": True}),
                     (" (Hard) — Digit DP; similar counting-with-constraints mindset.", {})])),
    N.para("These problems share the core technique: reduce an exponential counting or recurrence problem to O(log n) via binary exponentiation or matrix exponentiation."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math section, Fast Exponentiation sub-pattern.", "📚", "gray_background"),
]

# ── Visual Explainer Embed ────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("count_good_numbers")),
    N.para(N.rich([
        ("Step through binary exponentiation visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
