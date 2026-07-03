"""gen_powx_n.py — Notion update for Pow(x, n) (LeetCode #50)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8133-bd14-efa9c2729e2a"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=50,
    pattern="Recursion",
    subpatterns=["Binary Exponentiation"],
    tc="O(log n)",
    sc="O(log n)",
    key_insight="x^n = (x^(n/2))^2 — halve exponent each step for O(log n) multiplications; odd n needs one extra factor of x.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement "), ("pow(x, n)", {"code": True}),
        (", which calculates "), ("x", {"code": True}),
        (" raised to the power "), ("n", {"code": True}),
        (" (i.e., xⁿ). "), ("n", {"code": True}),
        (" can be negative: x⁻ⁿ = 1/xⁿ. You may not use Python's built-in "),
        ("**", {"code": True}), (" operator or "), ("math.pow", {"code": True}), ("."),
    ])),
    N.divider(),
]

# ── Solution 1: Recursive Binary Exponentiation ──
blocks += [
    N.h2("Solution 1 — Recursive Binary Exponentiation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to compute x^n efficiently. Brute force multiplies x by itself n times — O(n) operations. For n near 2 billion, that's billions of multiplications. We need to exploit structure."),
        N.h4("What Doesn't Work"),
        N.para("The naive loop (multiply x, n times) is O(n). A slightly better but still wrong approach: call myPow(x, n//2) twice and multiply. This makes TWO recursive calls of identical size — creating an exponential call tree that is again O(n) total work. The fix: compute half ONCE and reuse it."),
        N.h4("The Key Observation"),
        N.para("x^n = (x^(n/2))^2. If we already know x^(n/2), we need just ONE more multiplication to get x^n. Halving the problem at each step gives O(log n) depth. For odd n: n = 2k+1, so x^n = (x^k)^2 * x — one extra factor of x."),
        N.h4("Building the Solution"),
        N.para("1. Base: n=0 → return 1. 2. Negative n: return myPow(1/x, -n). 3. Compute half = myPow(x, n//2) ONCE. 4. Even n: return half*half. 5. Odd n: return half*half*x. Each call reduces n by half → O(log n) depth, O(1) work per level."),
        N.callout("Analogy: Like binary search, we halve the problem at each step. For n=10: 10→5→2→1→0, four levels deep, four squarings. That's log₂(10) ≈ 3.3 levels.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def myPow(x: float, n: int) -> float:
    if n == 0:
        return 1
    if n < 0:
        return myPow(1 / x, -n)
    half = myPow(x, n // 2)   # compute ONCE — critical!
    if n % 2 == 0:
        return half * half
    else:
        return half * half * x"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if n == 0:", {"code": True}), " — base case: x⁰ = 1 by definition. Terminates recursion."])),
    N.para(N.rich([("if n < 0: return myPow(1/x, -n)", {"code": True}), " — negative exponent: x^(-n) = (1/x)^n. Flip the base, make n positive. After this line, n is always ≥ 0 in all recursive calls."])),
    N.para(N.rich([("half = myPow(x, n // 2)", {"code": True}), " — CRITICAL: compute the sub-result ONCE and store it. Calling myPow twice would create two independent recursion trees of size n/2 each — doubling the work at every level — giving O(n) total, same as brute force."])),
    N.para(N.rich([("if n % 2 == 0: return half * half", {"code": True}), " — for even n, x^n = (x^(n/2))^2. One multiplication combines two identical sub-results."])),
    N.para(N.rich([("else: return half * half * x", {"code": True}), " — for odd n = 2k+1: x^(2k+1) = (x^k)^2 * x. We need one extra factor of x beyond the squared half."])),
    N.divider(),
]

# ── Solution 2: Iterative ──
blocks += [
    N.h2("Solution 2 — Iterative Fast Power (O(1) space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recursive solution uses O(log n) call stack space. We can eliminate the stack by processing the bits of n iteratively from LSB to MSB."),
        N.h4("The Key Observation"),
        N.para("n = 13 = 1101 in binary = 2^0 + 2^2 + 2^3. So x^13 = x^1 * x^4 * x^8. We iterate through bits: when bit k is 1, multiply the current power of x (x^(2^k)) into the result. We get x^(2^k) by squaring x at each step."),
        N.h4("Building the Solution"),
        N.para("Start with result=1, x=base. Loop: if n&1 (LSB set), result *= x. Then square x (x *= x) to double the represented power. Then right-shift n (n //= 2). Repeat until n=0."),
    ]),
    N.h3("Code"),
    N.code("""def myPow(x: float, n: int) -> float:
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n % 2 == 1:   # LSB is 1: include current x^(2^k)
            result *= x
        x *= x           # x = x^(2^(k+1)) for next iteration
        n //= 2          # shift right through bits of n
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("result = 1.0", {"code": True}), " — accumulator that will collect the product of selected powers of x."])),
    N.para(N.rich([("if n % 2 == 1: result *= x", {"code": True}), " — if current bit of n is 1, this power of x (currently x^(2^k)) contributes to the answer."])),
    N.para(N.rich([("x *= x", {"code": True}), " — square x: after iteration k, x holds x^(2^(k+1)), ready for the next bit."])),
    N.para(N.rich([("n //= 2", {"code": True}), " — right-shift n by one bit; we've processed the LSB."])),
    N.callout("This is the 'square-and-multiply' algorithm used in RSA and cryptographic protocols. Reading the binary representation of n and multiplying in the appropriate powers of x.", "🔐", "gray_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Loop", "O(n)", "O(1)"],
        ["Recursive Fast Power (Interview Pick)", "O(log n)", "O(log n) — call stack"],
        ["Iterative Fast Power", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Recursion (Divide and Conquer)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Binary Exponentiation — halve the exponent each step, square the result, handle odd remainder with one extra factor."])),
    N.callout(
        "When to recognize: 'compute x^n efficiently' — whenever you see exponentiation with large n. Also: repeated squaring of any associative operation (matrix multiply, modular multiply). Signal: O(n) is too slow, n can be 2^31.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Exponentiation / Divide & Conquer on exponents):"),
    N.bullet(N.rich([("Super Pow", {"bold": True}), " (Medium) — Modular fast exponentiation with a multi-digit exponent array (#372)"])),
    N.bullet(N.rich([("Fibonacci Number", {"bold": True}), " (Easy) — O(log n) via matrix exponentiation using fast power (#509)"])),
    N.bullet(N.rich([("Count Vowels Permutation", {"bold": True}), " (Hard) — Matrix exponentiation on vowel-state transitions (#1220)"])),
    N.bullet(N.rich([("Sqrt(x)", {"bold": True}), " (Easy) — Related: integer square root via binary search; both exploit O(log n) halving (#69)"])),
    N.bullet(N.rich([("Majority Element", {"bold": True}), " (Easy) — Divide and conquer; same O(log n) halving structure applied to arrays (#169)"])),
    N.bullet(N.rich([("Merge Sort", {"bold": True}), " (Medium) — Canonical divide-and-conquer; O(log n) recursive depth by halving the array size"])),
    N.para("These problems share the core insight: halving the input at each step drives complexity to O(log n)."),
    N.callout("Reference: Binary Exponentiation (Fast Power / Square-and-Multiply) — Knuth, TAOCP Vol. 2, Section 4.6.3. Also the foundation of RSA and modular arithmetic in competitive programming.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("powx_n")),
    N.para(N.rich([
        ("Step through the recursion call stack visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks added: {len(blocks)}")
