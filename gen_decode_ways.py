"""gen_decode_ways.py — Notion update for Decode Ways (LC #91)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8136-ac9a-d1ab385e9ee1"

# ── Step 1: Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=91,
    pattern="Dynamic Programming",
    subpatterns=["Based on 1 or 2 Digits"],
    tc="O(n)",
    sc="O(1)",
    key_insight="At each position, try 1 digit (if 1–9) or 2 digits (if 10–26); sum counts from valid predecessors via Fibonacci-style DP.",
    icon="🟡",
)
print("Properties set OK")

# ── Step 2: Wipe old body ───────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── Step 3: Build content blocks ────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" containing only digits, return the number of ways to decode it using the mapping ", {}),
        ("'A'=1, 'B'=2, ..., 'Z'=26", {"code": True}),
        (". A '0' digit cannot stand alone and can only appear as the second digit of '10' or '20'.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('"226" → 3', {"code": True}),
        (' because it can be decoded as (2,2,6)→"BBF", (22,6)→"VF", or (2,26)→"BZ".', {}),
    ])),
    N.divider(),
]

# ── Solution 1: Bottom-Up DP (Interview Pick) ──────────────────────────
SOL1_CODE = '''\
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1   # dp[0]=1 (empty seed), dp[1]=1 (first char valid)
    for i in range(2, len(s) + 1):
        curr = 0
        one = int(s[i-1])       # current single digit
        two = int(s[i-2:i])     # current two-digit number
        if 1 <= one <= 9:
            curr += prev1       # single digit valid: A-I
        if 10 <= two <= 26:
            curr += prev2       # pair valid: J-Z
        prev2, prev1 = prev1, curr
    return prev1
'''

blocks += [
    N.h2("Solution 1 — Space-Optimized Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Count all ways to partition a digit string into numbers 1–26, where each number maps to a letter. We don't care which decoding — just how many exist."),

        N.h4("What Doesn't Work"),
        N.para("Brute force tries every possible partition — O(2^n) recursive paths. Many subproblems overlap (decoding 's[0..i-1]' is computed repeatedly for different suffixes), making this exponential."),

        N.h4("The Key Observation"),
        N.para("Every valid decoding ends with either a single-digit letter or a two-digit letter. These cases are mutually exclusive. So dp[i] = (ways ending in single) + (ways ending in pair). Each term inherits from dp[i-1] or dp[i-2] respectively — exactly like Fibonacci!"),

        N.h4("Building the Solution"),
        N.para("Define dp[i] = number of valid decodings of the first i characters. Base: dp[0]=1 (empty = 1 way), dp[1]=1 if first char != '0'. At each i: check single validity (1–9) and pair validity (10–26), adding predecessor counts. Since only two previous values are needed, replace the O(n) array with two rolling variables."),

        N.callout(
            "Analogy: Climbing stairs where each step can be 1 or 2 stairs, but only if the stair is safe (not '0' for single; 10–26 for double). dp[i] = sum of safe ways to reach stair i.",
            "🧠", "blue_background"
        ),
    ]),

    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("dp[i] is fully determined by dp[i-1] and dp[i-2]. The number of decodings of the first i chars depends only on the number of decodings of shorter prefixes.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Naive recursion solves dp(i) multiple times from different calling contexts. Memoization or bottom-up DP ensures each subproblem is solved exactly once.", {}),
    ])),

    N.h3("Recurrence Relation"),
    N.code(
        "dp[0] = 1          # empty prefix: 1 way (seed)\n"
        "dp[1] = 0 if s[0]=='0' else 1\n\n"
        "For i = 2..n:\n"
        "    one = int(s[i-1])      # current single digit\n"
        "    two = int(s[i-2:i])    # current two-digit number\n"
        "    dp[i] = 0\n"
        "    if 1 <= one <= 9:  dp[i] += dp[i-1]   # single valid\n"
        "    if 10 <= two <= 26: dp[i] += dp[i-2]  # pair valid\n"
        "\n# Space optimized: only prev2 and prev1 needed",
        "python"
    ),

    N.h3("Code"),
    N.code(SOL1_CODE, "python"),

    N.h3("Line by Line"),
    N.para(N.rich([("if not s or s[0] == '0':", {"code": True}), (" — Guard clause. Empty string has 0 decodings. Leading '0' has 0 decodings because no letter maps to 0 and '0' cannot start a valid pair (would need to be < 10).", {})])),
    N.para(N.rich([("prev2, prev1 = 1, 1", {"code": True}), (" — Seed the base cases. prev2 = dp[0] = 1 (the empty-string seed that lets two-digit pairs start). prev1 = dp[1] = 1 (first char valid, confirmed by guard).", {})])),
    N.para(N.rich([("curr = 0", {"code": True}), (" — Start current position at 0. Any valid incoming path will add to it.", {})])),
    N.para(N.rich([("one = int(s[i-1])", {"code": True}), (" — Extract the single digit at the current position (note: dp is 1-indexed, s is 0-indexed — s[i-1] is the i-th character).", {})])),
    N.para(N.rich([("two = int(s[i-2:i])", {"code": True}), (" — Extract the two-digit number: the pair ending at position i.", {})])),
    N.para(N.rich([("if 1 <= one <= 9: curr += prev1", {"code": True}), (" — Single digit 1–9 maps to A–I. Valid → inherit all dp[i-1] decodings.", {})])),
    N.para(N.rich([("if 10 <= two <= 26: curr += prev2", {"code": True}), (" — Two-digit pair 10–26 maps to J–Z. Valid → inherit all dp[i-2] decodings.", {})])),
    N.para(N.rich([("prev2, prev1 = prev1, curr", {"code": True}), (" — Slide the rolling window: old prev1 becomes new prev2; curr becomes new prev1.", {})])),
    N.para(N.rich([("return prev1", {"code": True}), (" — After the loop, prev1 holds dp[n] = the total number of valid decodings.", {})])),

    N.callout(
        "⚠️ Common mistake: checking 'two <= 26' without the lower bound. '09' has two=9 which is <10 — the '10 <= two' guard correctly rejects it. Both boundaries are required.",
        "⚠️", "orange_background"
    ),

    N.divider(),
]

# ── Solution 2: Top-Down Memoization ──────────────────────────────────
SOL2_CODE = '''\
def numDecodings(s: str) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        # Base case: consumed all digits — this is one valid complete decode
        if i == len(s):
            return 1
        # Leading zero: no valid decode possible from this position
        if s[i] == '0':
            return 0
        # Single-digit decode (always try since s[i] != '0')
        ways = dp(i + 1)
        # Two-digit decode (if the pair is in range 10–26)
        if i + 1 < len(s) and int(s[i:i+2]) <= 26:
            ways += dp(i + 2)
        return ways

    return dp(0)
'''

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("From position i in the string, how many ways can we decode the suffix s[i:]? A natural recursive formulation: try consuming 1 digit or 2 digits, recurse on the rest."),

        N.h4("What Doesn't Work"),
        N.para("Pure recursion without caching recomputes dp(i) exponentially many times. For position i, the call tree branches up to 2^(n-i) times in the worst case."),

        N.h4("The Key Observation"),
        N.para("dp(i) depends only on dp(i+1) and dp(i+2). The total number of unique subproblems is only n. Caching with @lru_cache reduces exponential recursion to O(n) time."),

        N.h4("Building the Solution"),
        N.para("Define dp(i) = number of ways to decode s[i:]. Base: dp(n)=1 (empty suffix = 1 decode). If s[i]='0', return 0 (dead end). Otherwise recurse on i+1 (single) and optionally i+2 (if pair valid)."),

        N.callout("Top-down is easier to derive from the recurrence but uses O(n) stack + memo space. Bottom-up (Solution 1) achieves O(1) space. Both are O(n) time.", "💡", "blue_background"),
    ]),

    N.h3("Code"),
    N.code(SOL2_CODE, "python"),

    N.h3("Line by Line"),
    N.para(N.rich([("def dp(i: int) -> int:", {"code": True}), (" — Recursive function returning # ways to decode s[i:] (the suffix starting at index i).", {})])),
    N.para(N.rich([("if i == len(s): return 1", {"code": True}), (" — Base case: we consumed all digits successfully. This complete decode contributes 1 path.", {})])),
    N.para(N.rich([("if s[i] == '0': return 0", {"code": True}), (" — A '0' at position i cannot be a single decode (no letter = 0). Dead end.", {})])),
    N.para(N.rich([("ways = dp(i + 1)", {"code": True}), (" — Single-digit decode: s[i] is 1–9 (checked above), so always try consuming just s[i].", {})])),
    N.para(N.rich([("if i+1 < len(s) and int(s[i:i+2]) <= 26:", {"code": True}), (" — Two-digit check: ensure there IS a next character, and the pair s[i:i+2] ≤ 26.", {})])),
    N.para(N.rich([("ways += dp(i + 2)", {"code": True}), (" — Pair decode: s[i:i+2] is valid (10–26). Add decodings of the remaining suffix.", {})])),
    N.para(N.rich([("return dp(0)", {"code": True}), (" — Start from index 0, decoding the full string.", {})])),

    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (no memo)", "O(2^n)", "O(n) stack"],
        ["Top-Down Memoization", "O(n)", "O(n) memo + stack"],
        ["Bottom-Up DP (Interview Pick)", "O(n)", "O(1) rolling vars"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Based on 1 or 2 Digits (Fibonacci-style 1D DP with validity conditions per step)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('"How many ways to decode/parse a digit string?" — especially when each step can consume 1 or 2 elements and validity depends on the value of those elements. The Fibonacci structure (dp[i] from dp[i-1] + dp[i-2]) is the giveaway.', {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (1 or 2 Digit DP / Fibonacci Counting DP):"),
    N.bullet(N.rich([("Decode Ways II", {"bold": True}), (" (Hard) — Same problem but '*' wildcard can be any non-zero digit; multiply valid matches per position. (LC #639)", {})])),
    N.bullet(N.rich([("Climbing Stairs", {"bold": True}), (" (Easy) — Pure Fibonacci DP: dp[i] = dp[i-1] + dp[i-2] with no validity check. Foundational warm-up. (LC #70)", {})])),
    N.bullet(N.rich([("Min Cost Climbing Stairs", {"bold": True}), (" (Easy) — Fibonacci DP with cost: dp[i] = min(dp[i-1], dp[i-2]) + cost[i]. Same structure, different objective. (LC #746)", {})])),
    N.bullet(N.rich([("Word Break", {"bold": True}), (" (Medium) — Generalized: consume 1–k chars per step, validity via dictionary lookup. (LC #139)", {})])),
    N.bullet(N.rich([("Coin Change II", {"bold": True}), (" (Medium) — Count combinations with unlimited coins; 2D DP counting structure. (LC #518)", {})])),
    N.para("These problems share the same core technique: 1D counting DP where each position inherits counts from one or two previous valid states."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), Sub-Pattern: Based on 1 or 2 Digits", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("decode_ways")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
