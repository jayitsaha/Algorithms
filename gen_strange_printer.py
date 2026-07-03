"""
gen_strange_printer.py — Notion update for Strange Printer (#664)
Interval DP problem: dp[i][j] = min turns to print s[i..j]
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-819c-b366-d372704f9e38"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=664,
    pattern="Dynamic Programming",
    subpatterns=["DP: Interval"],
    tc="O(n³)",
    sc="O(n²)",
    key_insight="dp[i][j]=dp[i][j-1] when s[i]==s[j]: extend the stroke for s[i] to cover s[j] for free.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "There is a strange printer with the following two special properties:\n"
    "1. The printer can only print a sequence of the same character each time.\n"
    "2. At each turn, the printer can print new characters starting from and ending at any place, and will cover the original existing characters.\n\n"
    "Given a string s, return the minimum number of turns the printer needs to print it.\n\n"
    "Example 1: s = \"aaabbb\" → 2 (print 'a' over [0..5], then 'b' over [3..5])\n"
    "Example 2: s = \"aba\" → 2 (print 'a' over [0..2], then 'b' at [1..1])\n\n"
    "Constraints: 1 <= s.length <= 100, s consists of lowercase English letters only."
)

SOL1_CODE = '''def strangePrinter(s: str) -> int:
    # Compress consecutive duplicates: "aab" -> "ab"
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1])
    n = len(s)
    if n == 0:
        return 0

    # dp[i][j] = minimum turns to print s[i..j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single character needs 1 turn
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Merge trick: if endpoints match, extend stroke for free
            if s[i] == s[j]:
                dp[i][j] = dp[i][j - 1]
            else:
                # Try all split points
                dp[i][j] = float('inf')
                for k in range(i, j):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])

    return dp[0][n - 1]'''

SOL2_CODE = '''from functools import lru_cache

def strangePrinter(s: str) -> int:
    # Compress consecutive duplicates
    s = ''.join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1])
    n = len(s)

    @lru_cache(maxsize=None)
    def dp(i, j):
        """Min turns to print s[i..j]."""
        if i > j:
            return 0   # empty range
        if i == j:
            return 1   # single character
        if s[i] == s[j]:
            return dp(i, j - 1)   # merge trick
        return min(dp(i, k) + dp(k + 1, j) for k in range(i, j))

    return dp(0, n - 1)'''

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# Solution 1 — Bottom-Up Tabulation
blocks += [
    N.h2("Solution 1 — Bottom-Up Interval DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think of each printer turn as a horizontal paint stroke of one color. "
            "The printer lays down strokes on a canvas, and later strokes overwrite earlier ones. "
            "We want the minimum number of strokes to achieve the final painting. "
            "The question becomes: how can we cover the string with fewest same-color runs?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy fails because local decisions interact globally. "
            "For 'abacaba', naively printing left-to-right wastes turns on characters that could share strokes. "
            "Brute force recursion (try all possible first strokes) leads to exponential time from recomputing identical subproblems."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For any interval s[i..j], there must be some 'boundary' where the left portion's strokes "
            "and the right portion's strokes are independent. This means we can split any interval at any "
            "point k and add the costs. The critical insight: if s[i] == s[j], the stroke that prints s[i] "
            "can EXTEND FOR FREE to also cover position j. The middle characters s[i+1..j-1] will "
            "overwrite the middle part of that stroke — that's fine. So dp[i][j] = dp[i][j-1]."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Define dp[i][j] = min turns to print exactly s[i..j].\n"
            "2. Base: dp[i][i] = 1.\n"
            "3. Fill by increasing interval length (so dependencies are always ready).\n"
            "4. For each [i,j]: if s[i]==s[j], apply merge trick; else try all splits k.\n"
            "5. Answer: dp[0][n-1]."
        ),
        N.callout(
            "Analogy: Think of it like painting a fence. 'aba' — you paint the whole fence red (1 stroke), "
            "then paint the middle section blue (1 stroke). The red at the right end was FREE because it "
            "matched the initial red stroke. Total: 2 strokes, not 3.",
            "🎨", "blue_background"
        ),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(
        "OPTIMAL SUBSTRUCTURE: The minimum cost to print s[i..j] can always be expressed as the sum "
        "of minimum costs for two non-overlapping sub-intervals [i..k] and [k+1..j]. This holds for "
        "every valid split point k. Taking the minimum over all splits gives the global optimum.\n\n"
        "OVERLAPPING SUBPROBLEMS: A naive recursion would compute dp[2][5] multiple times — once "
        "for each parent interval that includes [2..5] as a sub-case. The 2D table stores each result "
        "once, reducing time from exponential to O(n^3)."
    ),
    N.code(
        "# Recurrence:\n"
        "# Base:   dp[i][i] = 1\n"
        "# Merge:  if s[i] == s[j]:  dp[i][j] = dp[i][j-1]  (extend stroke for free)\n"
        "# Split:  else:              dp[i][j] = min(dp[i][k] + dp[k+1][j]) for k in [i, j-1]\n"
        "# Answer: dp[0][n-1]",
        "python"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("s = compress(s)", {"code": True}),
        " — Remove consecutive duplicates. 'aab' becomes 'ab'. Two consecutive same chars always cost 1 turn, so this is a valid preprocessing step."
    ])),
    N.para(N.rich([
        ("dp = [[0]*n for _ in range(n)]", {"code": True}),
        " — Allocate n×n table. We only fill the upper triangle (i <= j). Lower triangle (i > j) is unused."
    ])),
    N.para(N.rich([
        ("dp[i][i] = 1", {"code": True}),
        " — Base case: single characters each need exactly 1 printer turn."
    ])),
    N.para(N.rich([
        ("for length in range(2, n+1):", {"code": True}),
        " — Outer loop over increasing interval lengths ensures all smaller subproblems are already solved when we need them."
    ])),
    N.para(N.rich([
        ("if s[i] == s[j]: dp[i][j] = dp[i][j-1]", {"code": True}),
        " — Merge trick: the stroke printing s[i] can extend to cover s[j] at zero extra cost because they're the same character."
    ])),
    N.para(N.rich([
        ("dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j])", {"code": True}),
        " — For each split point k, combine the costs of the left and right halves. The split divides the interval into two fully independent sub-problems."
    ])),
    N.para(N.rich([
        ("return dp[0][n-1]", {"code": True}),
        " — The answer for the full string s[0..n-1]."
    ])),
    N.callout(
        "WARNING: When s[i] == s[j], do NOT also check all splits. The merge result dp[i][j-1] "
        "is always optimal or better than any split result in this case. Checking splits too is "
        "correct but redundant.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 2 — Top-Down Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same problem, different implementation strategy. Instead of filling the table bottom-up, "
            "we write a recursive function dp(i, j) and let the cache handle reuse."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without the @lru_cache decorator, this recursion is exponential. The cache is the key. "
            "With memoization, each (i, j) pair is computed exactly once."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The recursive structure naturally mirrors the mathematical recurrence. "
            "dp(i, j) calls dp(i, j-1) or dp(i, k) and dp(k+1, j) — always strictly smaller intervals. "
            "No circular dependency, so recursion terminates."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp(i, j) recursively with the same cases as the tabulation approach. "
            "Python's @lru_cache handles memoization automatically — clean and direct."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("@lru_cache(maxsize=None)", {"code": True}),
        " — Python's built-in memoization decorator. Stores the result of dp(i,j) after it's first computed; future calls return instantly."
    ])),
    N.para(N.rich([
        ("if i > j: return 0", {"code": True}),
        " — Empty range (can happen when k=i and we call dp(k+1, j) with k+1 > j) needs 0 turns."
    ])),
    N.para(N.rich([
        ("if s[i] == s[j]: return dp(i, j-1)", {"code": True}),
        " — Same merge trick as tabulation. Recursively solve one shorter interval."
    ])),
    N.para(N.rich([
        ("return min(dp(i,k) + dp(k+1,j) for k in range(i,j))", {"code": True}),
        " — Try all splits and return the minimum. Python generator expression keeps it concise."
    ])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bottom-Up Tabulation (Interview Pick)", "O(n³)", "O(n²)"],
        ["Top-Down Memoization", "O(n³)", "O(n²) + O(n) stack"],
    ]),
    N.para("n = length of s after compression. Both approaches have the same asymptotic complexity. "
           "The three nested loops in tabulation: O(n) lengths × O(n) start positions × O(n) split points. "
           "O(n²) DP states, each taking O(n) to compute."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP: Interval (Interval DP)"])),
    N.callout(
        "When to recognize Interval DP:\n"
        "• Problem operates on a contiguous range (string or array)\n"
        "• Optimal answer for a range depends on optimal answers for sub-ranges\n"
        "• No obvious greedy — the best action at position i depends on what comes at position j (far away)\n"
        "• Keywords: 'minimum operations on substring', 'split/merge range optimally', 'cover/erase interval'\n"
        "• The three-loop skeleton: outer=length, middle=start i, inner=split k",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DP: Interval):"),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), " (Hard, #312) — Max coins bursting balloons; same 3-loop skeleton, 'last to burst' paradigm"])),
    N.bullet(N.rich([("Minimum Cost to Cut a Stick", {"bold": True}), " (Hard, #1547) — Minimize cost of cuts; identical to matrix chain multiplication recurrence"])),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}), " (Hard, #132) — Min cuts for palindrome partitions; interval DP on palindrome sub-checks"])),
    N.bullet(N.rich([("Zuma Game", {"bold": True}), " (Hard, #488) — Min moves to clear color runs; interval DP with grouping adjacent equal elements"])),
    N.bullet(N.rich([("Remove Boxes", {"bold": True}), " (Hard, #546) — Max points removing colored boxes; 3D interval DP extension"])),
    N.bullet(N.rich([("Minimum Score Triangulation of Polygon", {"bold": True}), " (Medium, #1039) — Min product triangulating polygon vertices; interval DP on arcs"])),
    N.bullet(N.rich([("Longest Palindromic Subsequence", {"bold": True}), " (Medium, #516) — Uses same s[i]==s[j] merge trick as this problem"])),
    N.para("These problems share the core insight: cost of processing a range depends on costs of sub-ranges, and the optimal split point must be searched."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → DP: Interval)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("strange_printer")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
