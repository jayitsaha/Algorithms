"""
Notion page update for: Longest Palindromic Subsequence (#516)
notion_page_id = 39193418-809c-81db-94b3-d3163046c5b7
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Patch the token before importing notion_lib
import notion_lib as N
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

PAGE_ID = "39193418-809c-81db-94b3-d3163046c5b7"
SLUG    = "longest_palindromic_subsequence"

print(f"[1] Setting properties on {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=516,
    pattern="Dynamic Programming",
    subpatterns=["DP: Palindrome", "DP: LCS"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="LPS of s equals LCS(s, reverse(s)); interval DP: if s[i]==s[j], dp[i][j]=dp[i+1][j-1]+2",
    icon="🟡"
)
print("[1] Properties set OK")

print("[2] Wiping old body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"[2] Wiped {n_deleted} blocks")

print("[3] Building body blocks...")
blocks = []

# ─── Problem Statement ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", find the length of the longest subsequence of ", {}),
        ("s", {"code": True}),
        (" that is a palindrome. A subsequence is a sequence derived by deleting some characters (or none) without changing the order of the remaining characters.", {})
    ])),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ('s = "bbbab"', {"code": True}),
            (' → ', {}),
            ("4", {"bold": True}),
            ('. One possible LPS is "bbbb".\n', {}),
            ("Example 2: ", {"bold": True}),
            ('s = "cbbd"', {"code": True}),
            (' → ', {}),
            ("2", {"bold": True}),
            ('. One possible LPS is "bb".', {})
        ]),
        "📋", "blue_background"
    ),
    N.divider()
]

# ─── Solution 1: Interval DP Tabulation ───
blocks += [
    N.h2("Solution 1 — Interval DP Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest subsequence of s that reads the same in both directions. A key observation: any palindromic subsequence is symmetric — the outermost characters either match (and both belong to the palindrome) or don't (and at least one is excluded)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force generates all 2ⁿ subsequences and checks each for palindrome property — O(2ⁿ · n). Hopeless for n > 20. Even a greedy approach fails because local decisions about which character to include can be globally suboptimal."),
        N.h4("The Key Observation"),
        N.para("The LPS of s[i..j] depends only on s[i], s[j], and the LPS of the inner substring s[i+1..j-1]. This is optimal substructure! If s[i]==s[j], both endpoints contribute +2. If not, we optimally skip exactly one endpoint. These two cases cover all possibilities."),
        N.h4("Building the Solution"),
        N.para("Define dp[i][j] = LPS length of s[i..j]. Base case: dp[i][i] = 1. Fill by increasing length (2, 3, ..., n) so dependencies are always ready. Recurrence: if s[i]==s[j], dp[i][j] = dp[i+1][j-1] + 2; else dp[i][j] = max(dp[i+1][j], dp[i][j-1]). Answer: dp[0][n-1]."),
        N.callout("Analogy: Think of building a palindrome from the outside in. If the outer characters match, they frame the palindrome — add them and recurse inward. If not, sacrifice one outer character and check which removal gives the longer inner palindrome.", "🧠", "blue_background")
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.callout(
        N.rich([
            ("Optimal Substructure: ", {"bold": True}),
            ("The LPS of s[i..j] is fully determined by s[i], s[j], and the LPS of s[i+1..j-1]. Any optimal solution for the larger range embeds an optimal solution for the inner range.\n\n", {}),
            ("Overlapping Subproblems: ", {"bold": True}),
            ("A naive recursion for lps(i, j) calls lps(i+1, j), lps(i, j-1), lps(i+1, j-1). These same subproblems appear repeatedly from many parent calls — exponential without caching, O(n²) with memoization/tabulation.", {})
        ]),
        "📐", "gray_background"
    ),
    N.h3("Recurrence Relations"),
    N.code(
        "Base case:  dp[i][i] = 1          # single char is palindrome of length 1\n\n"
        "If s[i] == s[j]:                   # endpoints match\n"
        "    dp[i][j] = dp[i+1][j-1] + 2   # inner LPS + 2 (both endpoints added)\n\n"
        "If s[i] != s[j]:                   # endpoints differ\n"
        "    dp[i][j] = max(dp[i+1][j],     # skip left endpoint\n"
        "                   dp[i][j-1])     # skip right endpoint\n\n"
        "Answer: dp[0][n-1]"
    ),
    N.h3("Code"),
    N.code(
        "def longestPalindromeSubseq(s: str) -> int:\n"
        "    n = len(s)\n"
        "    dp = [[0] * n for _ in range(n)]\n"
        "    \n"
        "    # Base case: single characters\n"
        "    for i in range(n):\n"
        "        dp[i][i] = 1\n"
        "    \n"
        "    # Fill by increasing substring length\n"
        "    for length in range(2, n + 1):\n"
        "        for i in range(n - length + 1):\n"
        "            j = i + length - 1\n"
        "            if s[i] == s[j]:\n"
        "                dp[i][j] = dp[i+1][j-1] + 2\n"
        "            else:\n"
        "                dp[i][j] = max(dp[i+1][j], dp[i][j-1])\n"
        "    \n"
        "    return dp[0][n-1]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(s)", {"code": True}), (" — store string length for repeated use.", {})])),
    N.para(N.rich([("dp = [[0]*n for _ in range(n)]", {"code": True}), (" — create n×n table. dp[i][j] is valid only for j >= i (upper triangle). Cells with j < i are unused (stay 0).", {})])),
    N.para(N.rich([("for i in range(n): dp[i][i] = 1", {"code": True}), (" — base case: every single-character substring is a palindrome of length 1. Fill the diagonal.", {})])),
    N.para(N.rich([("for length in range(2, n+1)", {"code": True}), (" — outer loop grows the substring length from 2 up to n. This guarantees dp[i+1][j-1] (length-2 shorter) and dp[i+1][j], dp[i][j-1] (length-1 shorter) are already computed.", {})])),
    N.para(N.rich([("j = i + length - 1", {"code": True}), (" — the right endpoint is derived from the left endpoint i and the current length.", {})])),
    N.para(N.rich([("if s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2", {"code": True}), (" — endpoints match: both can be the outermost pair of the palindrome. The inner palindrome dp[i+1][j-1] gains +2.", {})])),
    N.para(N.rich([("else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])", {"code": True}), (" — endpoints differ: we cannot use both. Excluding the left gives dp[i+1][j]; excluding the right gives dp[i][j-1]. Take the maximum.", {})])),
    N.para(N.rich([("return dp[0][n-1]", {"code": True}), (" — the LPS of the full string s[0..n-1].", {})])),
    N.callout("Warning: When length==2 and s[i]==s[j], dp[i+1][j-1] = dp[i+1][i]. Since i+1 > i this is an 'empty range' which initializes to 0. So dp[i][j] = 0+2 = 2. Correct — two matching characters form a length-2 palindrome.", "⚠️", "yellow_background"),
    N.divider()
]

# ─── Solution 2: Memoization ───
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: Recursive Thinking with Caching", [
        N.h4("Reframe the Problem"),
        N.para("The same recurrence as tabulation but written recursively. We directly translate the mathematical definition into code and let Python's cache handle avoiding recomputation."),
        N.h4("What Doesn't Work"),
        N.para("Plain recursion without caching recomputes the same (i, j) pairs exponentially. Adding @lru_cache turns this into an O(n²) algorithm."),
        N.h4("The Key Observation"),
        N.para("The recursive structure is naturally expressed: lps(i, j) = lps(i+1, j-1) + 2 if match, else max(lps(i+1, j), lps(i, j-1)). The base cases are i > j (empty range, return 0) and i == j (single char, return 1)."),
        N.h4("Building the Solution"),
        N.para("Define a recursive function dp(i, j) that returns the LPS for s[i..j]. Decorate with @lru_cache. Call dp(0, n-1). The cache automatically handles the O(n²) distinct states.")
    ]),
    N.h3("Code"),
    N.code(
        "def longestPalindromeSubseq(s: str) -> int:\n"
        "    from functools import lru_cache\n"
        "    n = len(s)\n"
        "    \n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i, j):\n"
        "        if i > j:  return 0    # empty range\n"
        "        if i == j: return 1    # single character\n"
        "        if s[i] == s[j]:\n"
        "            return dp(i+1, j-1) + 2\n"
        "        return max(dp(i+1, j), dp(i, j-1))\n"
        "    \n"
        "    return dp(0, n-1)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — memoize dp(i, j) calls. Python stores results keyed by (i, j). At most n² distinct pairs are ever computed.", {})])),
    N.para(N.rich([("if i > j: return 0", {"code": True}), (" — empty range (occurs when length==2 and we recurse to dp[i+1][j-1] = dp[i+1][i] where i+1 > i). Returns 0 correctly.", {})])),
    N.para(N.rich([("if i == j: return 1", {"code": True}), (" — single character base case.", {})])),
    N.para(N.rich([("return dp(i+1, j-1) + 2", {"code": True}), (" — match: extend the inner palindrome by wrapping both endpoints.", {})])),
    N.para(N.rich([("return max(dp(i+1, j), dp(i, j-1))", {"code": True}), (" — no match: try skipping either endpoint, take the best.", {})])),
    N.divider()
]

# ─── Solution 3: LCS Reduction ───
blocks += [
    N.h2("Solution 3 — LCS Reduction (Elegant Alternative)"),
    N.toggle_h3("💡 Intuition: The LCS Connection", [
        N.h4("Reframe the Problem"),
        N.para("LPS(s) = LCS(s, reverse(s)). A palindromic subsequence of s must appear in the same order in both s and reverse(s) — it is by definition a common subsequence of both."),
        N.h4("What Doesn't Work"),
        N.para("This reduction is not immediately obvious and requires a proof sketch. But once you see it, implementing LCS is straightforward and well-understood."),
        N.h4("The Key Observation"),
        N.para("Any palindrome P read forward equals P read backward. So P is a subsequence of s AND a subsequence of reverse(s). Therefore P is a common subsequence of s and reverse(s). Maximizing the length of P is exactly LCS(s, reverse(s))."),
        N.h4("Building the Solution"),
        N.para("Compute t = s[::-1]. Run standard O(n²) LCS DP on (s, t). The LCS length equals the LPS length.")
    ]),
    N.h3("Code"),
    N.code(
        "def longestPalindromeSubseq(s: str) -> int:\n"
        "    t = s[::-1]               # reverse of s\n"
        "    n = len(s)\n"
        "    dp = [[0] * (n+1) for _ in range(n+1)]\n"
        "    \n"
        "    for i in range(1, n+1):\n"
        "        for j in range(1, n+1):\n"
        "            if s[i-1] == t[j-1]:\n"
        "                dp[i][j] = dp[i-1][j-1] + 1\n"
        "            else:\n"
        "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
        "    \n"
        "    return dp[n][n]"
    ),
    N.divider()
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(2ⁿ)", "O(n)", "Infeasible for n > 20"],
        ["Memoization (top-down)", "O(n²)", "O(n²)", "Easy to write; recursive stack overhead"],
        ["Interval DP Tabulation ✓", "O(n²)", "O(n²) → O(n)", "Optimal; space reducible to O(n)"],
        ["LCS Reduction", "O(n²)", "O(n²)", "Elegant; equivalent problem"],
    ]),
    N.divider()
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP: Palindrome, DP: LCS (via reduction)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Longest palindromic subsequence' → Interval DP with dp[i][j] for s[i..j]\n"
        "• 'Optimal something on a substring' (not contiguous) → consider dp[i][j]\n"
        "• 'Minimum operations to make palindrome' → n - LPS(s)\n"
        "• LCS on s and reverse(s) is always an alternative formulation",
        "🔎", "green_background"
    ),
    N.divider()
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Interval DP / Palindrome DP):"),
    N.bullet(N.rich([("Palindromic Substrings", {"bold": True}), (" (Medium) — Count all palindromic substrings; expand around center or DP (#647)", {})])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), (" (Medium) — The foundational LCS DP that LPS directly reduces to (#1143)", {})])),
    N.bullet(N.rich([("Minimum Insertion Steps to Make a String Palindrome", {"bold": True}), (" (Medium) — Answer = n − LPS(s); same DP table (#1312)", {})])),
    N.bullet(N.rich([("Longest Palindromic Substring", {"bold": True}), (" (Medium) — Contiguous version; different technique: expand around center or Manacher's O(n) (#5)", {})])),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), (" (Hard) — Classic Interval DP: dp[i][j] = best score for subarray; fill by length (#312)", {})])),
    N.bullet(N.rich([("Strange Printer", {"bold": True}), (" (Hard) — Interval DP: minimum turns to print a string (#664)", {})])),
    N.bullet(N.rich([("Count Different Palindromic Subsequences", {"bold": True}), (" (Hard) — Count (not length) of distinct palindromic subsequences; harder interval DP (#730)", {})])),
    N.para("These problems share the core technique: define a subproblem on a substring [i, j], fill by increasing length, use the two-endpoint match/no-match recurrence."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → DP: Palindrome, DP: LCS)\nSub-Pattern verified: Guide Section 18", "📚", "gray_background"),
]

# ─── Visual Explainer Embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the DP table filling step by step — watch dp[i][j] get computed for each substring length, with live code highlighting and variable tracking.",
         {"italic": True, "color": "gray"})
    ]))
]

print(f"[3] Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"[3] Blocks appended OK")
print(f"NOTION OK {PAGE_ID}")
