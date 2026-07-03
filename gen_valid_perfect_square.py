"""
gen_valid_perfect_square.py
Regenerates the Notion page for Valid Perfect Square (LeetCode #367).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-810f-84b3-f7bfa21fe8ed"

# ─── 1. Set page properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=367,
    pattern="Binary Search",
    subpatterns=["BS: On Answer"],
    tc="O(log n)",
    sc="O(1)",
    key_insight="Binary search on candidate k: compare k^2 to num, halving the search space each step.",
    icon="🟢"
)
print("Properties set.")

# ─── 2. Wipe old content ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─── 3. Build body blocks ────────────────────────────────────────────────────
blocks = []

# ── Problem statement
blocks += [
    N.h2("Problem"),
    N.para("Given a positive integer num, return true if num is a perfect square, and false otherwise. "
           "You must not use any built-in library function such as sqrt(). "
           "A perfect square is an integer that equals some integer multiplied by itself: 1=1x1, 4=2x2, 9=3x3, 16=4x4, 25=5x5."),
    N.divider(),
]

# ── Solution 1 — Binary Search on Answer (Interview Pick)
sol1_code = """\
def isPerfectSquare(num: int) -> bool:
    lo, hi = 1, num              # Search range: candidate k in [1, num]
    while lo <= hi:              # Inclusive bounds -- check single-element ranges too
        mid = (lo + hi) // 2    # Integer midpoint (no overflow in Python)
        sq = mid * mid           # sq: the square of our candidate root
        if sq == num:            # Exact match: mid is the integer square root
            return True
        elif sq < num:           # Too small -> search upper half
            lo = mid + 1
        else:                    # Too large -> search lower half
            hi = mid - 1
    return False                 # Exhausted search: no integer root exists"""

blocks += [
    N.h2("Solution 1 — Binary Search on Answer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're looking for an integer k such that k^2 = num. Equivalently: does num have an integer square root? "
               "The forbidden sqrt() constraint hints we must search for it ourselves."),

        N.h4("What Doesn't Work"),
        N.para("Brute force: check k = 1, 2, 3, ... up to sqrt(num). This is O(sqrt(n)) — up to ~46,000 iterations "
               "for a 32-bit number. Correct but slow, and it ignores the monotone structure of k^2."),

        N.h4("The Key Observation"),
        N.para("The function f(k) = k^2 is strictly monotonically increasing for k >= 1. "
               "If mid^2 < num, every k <= mid is also too small — discard the left half. "
               "If mid^2 > num, every k >= mid is also too large — discard the right half. "
               "That's exactly binary search."),

        N.h4("Building the Solution"),
        N.para("Search space: k in [1, num]. At each step compute mid = (lo+hi)//2 and sq = mid*mid. "
               "Three-way compare: (a) sq==num -> return True, (b) sq<num -> lo=mid+1, (c) sq>num -> hi=mid-1. "
               "Loop invariant: if a valid root exists, it remains in [lo, hi]. When lo>hi, return False."),

        N.callout(
            "Analogy: Think of it like 'guess my number' where the host says 'too high' or 'too low.' "
            "Binary search is the optimal strategy — always guess the midpoint. "
            "Here the 'number' is the square root and the 'feedback' is whether mid^2 is too big, too small, or exact.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 1, num", {"code": True}),
                   " — Initialize search bounds. The square root (if it exists) must lie between 1 and num."])),
    N.para(N.rich([("while lo <= hi:", {"code": True}),
                   " — Inclusive bound: ensures we check even when lo=hi (a single remaining candidate might be the answer)."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}),
                   " — Floor-division midpoint. No overflow in Python. In C++/Java use long."])),
    N.para(N.rich([("sq = mid * mid", {"code": True}),
                   " — Compute the square of our candidate. In C++/Java declare sq as long long to avoid overflow."])),
    N.para(N.rich([("if sq == num: return True", {"code": True}),
                   " — Exact match: mid is the integer square root. num is a perfect square."])),
    N.para(N.rich([("elif sq < num: lo = mid + 1", {"code": True}),
                   " — mid is too small. The true root (if any) must be > mid. Move lower bound up."])),
    N.para(N.rich([("else: hi = mid - 1", {"code": True}),
                   " — mid is too large. Move upper bound down."])),
    N.para(N.rich([("return False", {"code": True}),
                   " — Loop ended with lo>hi: search space exhausted, no integer square root exists."])),
    N.divider(),
]

# ── Solution 2 — Odd Number Subtraction
sol2_code = """\
def isPerfectSquare(num: int) -> bool:
    # Uses the identity: k^2 = 1 + 3 + 5 + ... + (2k-1)
    odd = 1
    while num > 0:
        num -= odd    # Subtract 1, then 3, then 5, ...
        odd += 2      # Next odd number
    return num == 0   # Exactly 0 -> was a perfect square"""

blocks += [
    N.h2("Solution 2 — Odd Number Subtraction (O(sqrt n), Math Insight)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every perfect square k^2 equals the sum of the first k odd numbers: 1=1, 4=1+3, 9=1+3+5, "
               "16=1+3+5+7, 25=1+3+5+7+9. This is a well-known mathematical identity."),

        N.h4("What Doesn't Work"),
        N.para("If you don't know this identity, you can't derive this approach — it's more of a mathematical "
               "insight than a systematic technique. In an interview, binary search is the expected first answer."),

        N.h4("The Key Observation"),
        N.para("Subtracting consecutive odd numbers from num until reaching 0 (perfect square) or going "
               "negative (not a perfect square) exactly checks this identity. Each subtraction removes one "
               "square's L-shaped border layer."),

        N.h4("Building the Solution"),
        N.para("Start with odd=1. Subtract 1, then 3, then 5, ... If at any point num=0, it was a perfect square. "
               "If num goes negative, it was not. Simple O(sqrt n) loop."),

        N.callout(
            "Geometric intuition: Each odd number (2k-1) represents a new L-shaped border added to a (k-1)x(k-1) "
            "square to make it kxk. Subtracting these L-shapes one at a time peels the square apart. "
            "If you peel it down to exactly 0, it was a perfect square.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("odd = 1", {"code": True}),
                   " — Start with the first odd number. We will subtract 1, then 3, then 5, then 7, ..."])),
    N.para(N.rich([("while num > 0:", {"code": True}),
                   " — Keep subtracting as long as num hasn't reached 0 or gone negative."])),
    N.para(N.rich([("num -= odd", {"code": True}),
                   " — Remove this odd number. Represents peeling off one L-shaped border of the square."])),
    N.para(N.rich([("odd += 2", {"code": True}),
                   " — Move to next odd number (1 -> 3 -> 5 -> 7 -> ...)."])),
    N.para(N.rich([("return num == 0", {"code": True}),
                   " — If we hit exactly 0: num was k^2 for some k -> True. If negative: not a perfect square -> False."])),
    N.divider(),
]

# ── Solution 3 — Newton's Method
sol3_code = """\
def isPerfectSquare(num: int) -> bool:
    x = num                      # Start with an overestimate
    while x * x > num:           # Refine until x = floor(sqrt(num))
        x = (x + num // x) // 2  # Newton's update for sqrt
    return x * x == num          # Check if floor(sqrt(num)) is exact"""

blocks += [
    N.h2("Solution 3 — Newton's Method (O(log n), Advanced)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Newton's method is a numerical root-finding technique. For finding sqrt(num), we iteratively "
               "refine a guess x using: x_new = (x + num/x) / 2. This converges very quickly to sqrt(num)."),

        N.h4("The Key Observation"),
        N.para("Given a current overestimate x of sqrt(num): if x > sqrt(num), then num/x < sqrt(num). "
               "Their average (x + num/x)/2 is always a better (tighter) overestimate — the arithmetic mean "
               "of an overestimate and an underestimate lies strictly between them."),

        N.h4("Building the Solution"),
        N.para("Start with x=num (a gross overestimate). Repeatedly apply x = (x + num//x)//2 using integer "
               "division. Stop when x*x <= num (x has converged to floor(sqrt(num))). Check x*x == num."),
    ]),
    N.h3("Code"),
    N.code(sol3_code),
    N.h3("Line by Line"),
    N.para(N.rich([("x = num", {"code": True}),
                   " — Initial overestimate. sqrt(num) <= num always holds for num >= 1."])),
    N.para(N.rich([("while x * x > num:", {"code": True}),
                   " — Keep refining as long as x is still an overestimate of sqrt(num)."])),
    N.para(N.rich([("x = (x + num // x) // 2", {"code": True}),
                   " — Newton's update in integer arithmetic. Converges to floor(sqrt(num))."])),
    N.para(N.rich([("return x * x == num", {"code": True}),
                   " — x is now floor(sqrt(num)). Check whether it squares exactly to num."])),
    N.divider(),
]

# ── Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (linear scan)", "O(sqrt n)", "O(1)"],
        ["Odd Number Subtraction", "O(sqrt n)", "O(1)"],
        ["Binary Search on Answer", "O(log n)", "O(1)"],
        ["Newton's Method", "O(log n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "BS: On Answer — binary search over a candidate answer space rather than a sorted array."])),
    N.callout(
        "When to recognize this pattern: (1) The answer is a number in a known bounded range [lo, hi]. "
        "(2) You can write a monotone check function: all k below a threshold satisfy / fail the condition, "
        "all above do the opposite. (3) The problem says 'no built-in sqrt/pow' — implement the search yourself. "
        "(4) Keywords: 'minimize maximum', 'find if X exists without library', 'is k^p equal to n'.",
        "🔎", "green_background"
    ),
    N.callout(
        "Sub-pattern verified against DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search). "
        "'BS: On Answer' is the technique of searching over a candidate answer space. "
        "Also called Parametric Search. Same template as Koko Eating Bananas (#875), Capacity to Ship (#1011), Sqrt(x) (#69).",
        "📚", "gray_background"
    ),
    N.divider(),
]

# ── Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Binary Search on Answer technique:"),
    N.bullet(N.rich([("Sqrt(x)", {"bold": True}),
                     " (#69, Easy) — Return floor(sqrt(x)); identical binary search, return hi at loop end."])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}),
                     " (#278, Easy) — Find first True in monotone bool sequence; same BS skeleton."])),
    N.bullet(N.rich([("Search Insert Position", {"bold": True}),
                     " (#35, Easy) — Find insertion point in sorted array; binary search on position."])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}),
                     " (#875, Medium) — Minimize eating speed k; binary search on speed. Canonical BS-on-answer problem."])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}),
                     " (#1011, Medium) — Same BS-on-answer with a sum-based check function."])),
    N.bullet(N.rich([("Find the Smallest Divisor Given a Threshold", {"bold": True}),
                     " (#1283, Medium) — Minimize divisor such that quotient sum <= threshold; same template."])),
    N.bullet(N.rich([("Perfect Squares (min count)", {"bold": True}),
                     " (#279, Medium) — Related problem on perfect squares but solved with DP/BFS, not binary search."])),
    N.para("These problems all share the same template: binary search on a numeric answer space with a monotone "
           "check function determining which half to eliminate at each step."),
    N.divider(),
]

# ── Interactive Visual Explainer (embed)
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_perfect_square")),
    N.para(N.rich([
        ("Step through the binary search visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} top-level blocks to {PAGE_ID}")
