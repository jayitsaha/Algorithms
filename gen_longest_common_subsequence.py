"""
gen_longest_common_subsequence.py — Notion update for Longest Common Subsequence (LC #1143)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-817d-8a0b-d63257801dd3"  # existing page — update in-place

# ── 1. Set properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1143,
    pattern="Dynamic Programming",
    subpatterns=["Classic 2D DP (LCS)"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="dp[i][j] = LCS of text1[0..i-1] and text2[0..j-1]; match→diagonal+1, no match→max(up,left).",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────────
blocks = []

# ─── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings "), ("text1", {"code": True}), (" and "),
        ("text2", {"code": True}),
        (", return the length of their "), ("longest common subsequence", {"bold": True}),
        (". A subsequence is derived by deleting some elements (possibly none) without "
         "changing the order of the remaining elements. If no common subsequence exists, return 0.")
    ])),
    N.para(N.rich([
        ("Example: text1 = \"abcde\", text2 = \"ace\" → LCS = \"ace\" → length "),
        ("3", {"bold": True}), (" (pick a,c,e from text1 at positions 0,2,4).")
    ])),
    N.divider(),
]

# ─── Solution 1: 2D Tabulation ─────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — 2D DP Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the longest sequence of characters that appears in both strings "
               "in the same order (but not necessarily contiguous). Think of it as finding the "
               "longest 'thread' you can pull through both strings simultaneously."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: check all 2ᵐ subsequences of text1 against all 2ⁿ subsequences of text2. "
               "Exponential time — completely impractical for strings of length > 20."),
        N.h4("The Key Observation"),
        N.para("The LCS problem has overlapping subproblems. LCS(\"abc\", \"ace\") depends on "
               "LCS(\"ab\", \"ace\") and LCS(\"abc\", \"ac\") — both of which depend on LCS(\"ab\", \"ac\"). "
               "We should compute each subproblem once and cache it: classic DP."),
        N.h4("Building the Solution"),
        N.para("Define dp[i][j] = LCS length of text1[0..i-1] and text2[0..j-1]. "
               "Two cases at each cell: if characters match, extend diagonal by 1. "
               "If not, take the max of ignoring either current character. "
               "Fill row by row. Answer at dp[m][n]."),
        N.callout(
            "Analogy: Like comparing two DNA strands — you slide a pointer through each, "
            "and every time you find a common base you extend your 'shared skeleton.' "
            "The DP table records the best skeleton length for every pair of prefixes.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
        "    m, n = len(text1), len(text2)\n"
        "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
        "    for i in range(1, m + 1):\n"
        "        for j in range(1, n + 1):\n"
        "            if text1[i-1] == text2[j-1]:\n"
        "                dp[i][j] = dp[i-1][j-1] + 1\n"
        "            else:\n"
        "                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
        "    return dp[m][n]",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(text1), len(text2)", {"code": True}),
                   (" — store string lengths for indexing clarity.")])),
    N.para(N.rich([("dp = [[0]*(n+1) for _ in range(m+1)]", {"code": True}),
                   (" — create (m+1)×(n+1) table all zeros. The +1 adds an empty-string row and column "
                    "as base cases: LCS with empty string is always 0.")])),
    N.para(N.rich([("for i in range(1, m+1)", {"code": True}),
                   (" — iterate over text1 characters (1-indexed into dp, so text1[i-1] is the character).")])),
    N.para(N.rich([("for j in range(1, n+1)", {"code": True}),
                   (" — iterate over text2 characters (j-1 maps back to string index).")])),
    N.para(N.rich([("if text1[i-1] == text2[j-1]", {"code": True}),
                   (" — check if current characters from both strings match.")])),
    N.para(N.rich([("dp[i][j] = dp[i-1][j-1] + 1", {"code": True}),
                   (" — characters match: extend the LCS of the shorter prefixes (diagonal) by 1. "
                    "dp[i-1][j-1] is the LCS before considering either current character.")])),
    N.para(N.rich([("dp[i][j] = max(dp[i-1][j], dp[i][j-1])", {"code": True}),
                   (" — characters differ: skip text1[i] (look up = dp[i-1][j]) or "
                    "skip text2[j] (look left = dp[i][j-1]); take the better option.")])),
    N.para(N.rich([("return dp[m][n]", {"code": True}),
                   (" — bottom-right cell holds the LCS of the full text1 and text2.")])),
    N.divider(),
]

# ─── Solution 2: Space-Optimized ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Space-Optimized DP (Rolling Array, O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we avoid storing the entire m×n table? "
               "Each cell dp[i][j] only depends on three predecessors: dp[i-1][j-1] (diagonal), "
               "dp[i-1][j] (above), dp[i][j-1] (left). All three come from either the current row "
               "or the previous row. We never look back more than one row."),
        N.h4("The Key Observation"),
        N.para("We only need two 1D arrays: prev (the previous row) and curr (the current row being built). "
               "After finishing each row, curr becomes the new prev. Space drops from O(m·n) to O(n)."),
        N.h4("Building the Solution"),
        N.para("Use prev[j-1] instead of dp[i-1][j-1] (diagonal). "
               "Use prev[j] instead of dp[i-1][j] (above). "
               "Use curr[j-1] instead of dp[i][j-1] (left). "
               "After each row, slide: prev = curr."),
    ]),
    N.h3("Code"),
    N.code(
        "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
        "    m, n = len(text1), len(text2)\n"
        "    prev = [0] * (n + 1)\n"
        "    for i in range(1, m + 1):\n"
        "        curr = [0] * (n + 1)\n"
        "        for j in range(1, n + 1):\n"
        "            if text1[i-1] == text2[j-1]:\n"
        "                curr[j] = prev[j-1] + 1\n"
        "            else:\n"
        "                curr[j] = max(prev[j], curr[j-1])\n"
        "        prev = curr\n"
        "    return prev[n]",
        "python"
    ),
    N.callout(
        "Space optimization: prev[j-1] is the diagonal (i-1, j-1). "
        "prev[j] is 'above' (i-1, j). curr[j-1] is 'left' (i, j-1). "
        "After each row, slide prev = curr. Same answers, O(n) memory.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ─── Solution 3: Top-Down Memoization ──────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Top-Down Memoization (Recursive + Cache)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think recursively: LCS from position i in text1 and j in text2. "
               "Base case: either string exhausted → return 0. "
               "If characters match, include them and recurse on (i+1, j+1). "
               "Otherwise try both (i+1, j) and (i, j+1) and take the max."),
        N.h4("Why Add Memoization?"),
        N.para("Without memoization, the recursion tree recomputes the same (i,j) sub-problems "
               "exponentially many times. @lru_cache caches every (i,j) result — each of the m×n "
               "pairs is computed exactly once, reducing time from O(2^(m+n)) to O(m·n)."),
    ]),
    N.h3("Code"),
    N.code(
        "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
        "    from functools import lru_cache\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i, j):\n"
        "        # Base case: one string exhausted\n"
        "        if i == len(text1) or j == len(text2):\n"
        "            return 0\n"
        "        # Current characters match — take both, advance both pointers\n"
        "        if text1[i] == text2[j]:\n"
        "            return 1 + dp(i + 1, j + 1)\n"
        "        # Differ — skip one character from either string, take best\n"
        "        return max(dp(i + 1, j), dp(i, j + 1))\n"
        "\n"
        "    return dp(0, 0)",
        "python"
    ),
    N.callout(
        "Why is this DP and not greedy? Because greedily taking the first match doesn't guarantee "
        "the optimal LCS. Example: text1='axbc', text2='abc'. Greedily taking 'a' then 'b' might "
        "miss 'abc' which requires skipping 'x'. DP explores all options and takes the max.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ─── Why This is DP ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("🧠 Why This is Dynamic Programming"),
    N.h3("Optimal Substructure"),
    N.para(
        "The LCS of text1[0..i] and text2[0..j] is determined by the LCS of shorter prefixes. "
        "If text1[i] == text2[j], extend LCS(text1[0..i-1], text2[0..j-1]) by 1. "
        "If not, the LCS is max(LCS(text1[0..i-1], text2[0..j]), LCS(text1[0..i], text2[0..j-1])). "
        "The optimal solution to the whole problem contains optimal solutions to subproblems."
    ),
    N.h3("Overlapping Subproblems"),
    N.para(
        "The same sub-problem LCS(i, j) is needed by multiple larger problems. "
        "For example, LCS(2, 2) is needed when computing LCS(3, 2), LCS(2, 3), AND LCS(3, 3). "
        "Without memoization, these are recomputed exponentially. "
        "The DP table ensures each of the O(m·n) subproblems is computed exactly once."
    ),
    N.code(
        "# The recurrence:\n"
        "# dp[i][j] = LCS length of text1[0..i-1] and text2[0..j-1]\n"
        "#\n"
        "# Base case:\n"
        "# dp[0][j] = 0  (empty text1, any text2 prefix → LCS = 0)\n"
        "# dp[i][0] = 0  (any text1 prefix, empty text2 → LCS = 0)\n"
        "#\n"
        "# Recurrence:\n"
        "# if text1[i-1] == text2[j-1]:  ← characters match\n"
        "#     dp[i][j] = dp[i-1][j-1] + 1\n"
        "# else:                          ← characters differ\n"
        "#     dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n"
        "#\n"
        "# Answer: dp[m][n]",
        "python"
    ),
    N.divider(),
]

# ─── Complexity ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Recursion", "O(2^(m+n))", "O(m+n) stack"],
        ["2D DP Tabulation (Interview Pick)", "O(m·n)", "O(m·n)"],
        ["Space-Optimized Rolling Array", "O(m·n)", "O(n)"],
        ["Top-Down Memoization", "O(m·n)", "O(m·n) + stack"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ──────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Classic 2D DP (LCS)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Two sequences + 'longest/shortest common subsequence' → Classic 2D DP\n"
        "• 'Subsequence' (can skip chars) vs 'substring' (must be contiguous) — key distinction\n"
        "• The match/no-match two-case recurrence appears in Edit Distance, Wildcard Matching\n"
        "• Real-world: Unix diff, git blame, DNA alignment — all use LCS internally",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ────────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Classic 2D DP (LCS) technique:"),
    N.bullet(N.rich([("Edit Distance", {"bold": True}),
                     (" (Hard) — LCS extended with insert/delete/replace costs; identical table shape (#72)")])),
    N.bullet(N.rich([("Shortest Common Supersequence", {"bold": True}),
                     (" (Hard) — SCS length = m + n - LCS; backtrack table to reconstruct (#1092)")])),
    N.bullet(N.rich([("Longest Palindromic Subsequence", {"bold": True}),
                     (" (Medium) — exactly LCS(s, reverse(s)); same recurrence (#516)")])),
    N.bullet(N.rich([("Delete Operation for Two Strings", {"bold": True}),
                     (" (Medium) — min deletions = m + n - 2 × LCS (#583)")])),
    N.bullet(N.rich([("Uncrossed Lines", {"bold": True}),
                     (" (Medium) — geometrically rephrased LCS; identical solution (#1035)")])),
    N.bullet(N.rich([("Minimum ASCII Delete Sum for Two Strings", {"bold": True}),
                     (" (Medium) — weighted LCS where cost = ASCII value of deleted chars (#712)")])),
    N.bullet(N.rich([("Longest Common Substring", {"bold": True}),
                     (" (Medium) — similar table; reset to 0 on mismatch instead of max (#718 variant)")])),
    N.para("These problems share the same core 2D DP table structure: define dp[i][j] over prefixes, "
           "handle match and no-match cases, read answer at dp[m][n]."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → DP: LCS)\n"
        "Sub-Pattern verified: Classic 2D DP (LCS) · Source: Guide Section 18",
        "📚", "gray_background"
    ),
]

# ─── Embed ───────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_common_subsequence")),
    N.para(N.rich([
        ("Step through the 2D DP table fill visually — use Next/Prev or arrow keys. "
         "Each step shows the decision being made (match vs no-match) and why that cell's value is correct.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Append all blocks ────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
