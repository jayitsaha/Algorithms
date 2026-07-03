"""
gen_longest_common_subsequence.py
Rebuilds the Notion page for LCS (LC 1143) in-place.
Sub-pattern: Classic 2D DP (Guide Section 18.6 - String Dynamic Programming)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-817d-8a0b-d63257801dd3"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1143,
    pattern="Dynamic Programming",
    subpatterns=["Classic 2D DP"],
    tc="O(m x n)",
    sc="O(m x n)",
    key_insight="dp[i][j] = LCS of text1[:i] and text2[:j]; match -> diagonal+1, else max(up, left).",
    icon="\U0001f7e1"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body ─────────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    'Given two strings text1 and text2, return the length of their longest common subsequence. '
    'A subsequence is a sequence derived from a string by deleting some (or no) characters '
    'without changing the relative order of the remaining characters. '
    'If there is no common subsequence, return 0.\n\n'
    'Example 1:  text1 = "abcde",  text2 = "ace"  ->  3  ("ace")\n'
    'Example 2:  text1 = "abc",    text2 = "abc"  ->  3  ("abc")\n'
    'Example 3:  text1 = "abc",    text2 = "def"  ->  0'
))
blocks.append(N.divider())

# ── Solution 1 — Bottom-Up Tabulation (Interview Pick) ────────────────────────
blocks.append(N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"))

blocks.append(N.toggle_h3("Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "We need to find the longest sequence of characters that appears in the same relative order "
        "in both strings (not necessarily contiguous). At every pair of positions (i, j) we face a "
        "binary choice: if characters match, we can count this pair and advance both pointers; "
        "if they do not match, we must sacrifice one character from either side. "
        "This optimal-choice-with-overlapping-subproblems structure is the fingerprint of DP."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Brute force: enumerate all 2^m subsequences of text1 and check each against text2 — "
        "O(2^m * n), intractable for m=30. Greedy (always take the earliest matching character) "
        "also fails: an early match can block a longer overall alignment."
    ),
    N.h4("The Key Observation"),
    N.para(
        "LCS(text1[:i], text2[:j]) depends only on strictly smaller subproblems:\n"
        "  If text1[i-1] == text2[j-1]:  LCS = 1 + LCS(text1[:i-1], text2[:j-1])\n"
        "  Otherwise:                     LCS = max(LCS(text1[:i-1], text2[:j]),\n"
        "                                           LCS(text1[:i],   text2[:j-1]))\n"
        "There are only (m+1)*(n+1) unique states, so fill them bottom-up and read dp[m][n]."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Allocate a (m+1) x (n+1) table initialised to 0. "
        "The extra row/column are implicit base cases (empty string has LCS 0 with anything).\n"
        "2. Iterate i from 1..m, j from 1..n. Apply the two-case recurrence.\n"
        "3. Answer is dp[m][n]."
    ),
    N.callout(
        "Analogy: Think of dp[i][j] as 'how long a common thread can I weave using the "
        "first i characters of text1 and first j of text2?' Each cell looks at the three "
        "cells it depends on: diagonal (match), above (skip text1 char), left (skip text2 char).",
        "\U0001f9f5", "blue_background"
    ),
]))

blocks.append(N.h3("Why is This Dynamic Programming?"))
blocks.append(N.para(
    "Optimal Substructure: LCS of two full strings is built from optimal LCS values of their prefixes. "
    "No global information is needed beyond the indices (i, j).\n\n"
    "Overlapping Subproblems: in naive recursion, lcs(i-1, j) and lcs(i, j-1) both call lcs(i-1, j-1). "
    "Without memoisation this leads to exponential recomputation of the same states."
))

blocks.append(N.h3("Recurrence Relation"))
blocks.append(N.code(
    "# Base case\n"
    "dp[0][j] = 0  for all j     (text1 is empty)\n"
    "dp[i][0] = 0  for all i     (text2 is empty)\n"
    "\n"
    "# Recurrence\n"
    "if text1[i-1] == text2[j-1]:\n"
    "    dp[i][j] = dp[i-1][j-1] + 1          # characters match: extend diagonal\n"
    "else:\n"
    "    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # skip from one side, take best",
    lang="python"
))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
    "    m, n = len(text1), len(text2)\n"
    "    # dp[i][j] = LCS length of text1[:i] and text2[:j]\n"
    "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
    "\n"
    "    for i in range(1, m + 1):\n"
    "        for j in range(1, n + 1):\n"
    "            if text1[i - 1] == text2[j - 1]:\n"
    "                dp[i][j] = dp[i - 1][j - 1] + 1\n"
    "            else:\n"
    "                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
    "\n"
    "    return dp[m][n]\n",
    lang="python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("m, n = len(text1), len(text2)", {"code": True}),
    " -- cache string lengths; avoids recomputing in every inner loop iteration."
])))
blocks.append(N.para(N.rich([
    ("dp = [[0] * (n + 1) for _ in range(m + 1)]", {"code": True}),
    " -- (m+1)x(n+1) table, all zeros. Row 0 and column 0 are the base cases: empty prefix has LCS 0."
])))
blocks.append(N.para(N.rich([
    ("for i in range(1, m + 1):", {"code": True}),
    " -- outer loop over text1 characters (1-indexed; text1[i-1] is the actual character)."
])))
blocks.append(N.para(N.rich([
    ("for j in range(1, n + 1):", {"code": True}),
    " -- inner loop over text2 characters. We evaluate every (i, j) pair exactly once."
])))
blocks.append(N.para(N.rich([
    ("if text1[i - 1] == text2[j - 1]:", {"code": True}),
    " -- compare the two current characters. Match triggers the diagonal extension."
])))
blocks.append(N.para(N.rich([
    ("dp[i][j] = dp[i - 1][j - 1] + 1", {"code": True}),
    " -- both characters are part of the LCS. The diagonal cell held the LCS before this pair. Add 1."
])))
blocks.append(N.para(N.rich([
    ("dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])", {"code": True}),
    " -- mismatch. Skip text1[i-1] (look up: dp[i-1][j]) or text2[j-1] (look left: dp[i][j-1]). Take the better."
])))
blocks.append(N.para(N.rich([
    ("return dp[m][n]", {"code": True}),
    " -- bottom-right cell: LCS of the full text1 and text2."
])))
blocks.append(N.callout(
    "Common Mistake: Using dp with m rows and n columns (forgetting the +1). "
    "The 0th row/column must exist as the empty-string base case. "
    "Without them, dp[i-1][j-1] underflows when i=1 or j=1.",
    "⚠️", "yellow_background"
))
blocks.append(N.divider())

# ── Solution 2 — Top-Down Memoization ─────────────────────────────────────────
blocks.append(N.h2("Solution 2 -- Top-Down Memoization"))

blocks.append(N.toggle_h3("Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "The same recurrence can be expressed as a recursive function lcs(i, j) and cached. "
        "Top-down is often easier to derive from the recurrence relation directly -- "
        "you write 'what it means' and let the cache handle efficiency."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Pure recursion without caching: each call branches into two more, producing "
        "O(2^(m+n)) calls. For strings of length 1000 this is astronomically large."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Only m*n unique (i, j) pairs can ever be called. "
        "Python's lru_cache stores each result on first computation -- "
        "every subsequent call is an O(1) dictionary lookup."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Decorate a recursive function with @lru_cache.\n"
        "2. Return 0 at base cases (i==0 or j==0).\n"
        "3. Apply the same two-case recurrence as tabulation.\n"
        "4. Call lcs(m, n) and return the result."
    ),
    N.callout(
        "When to choose memoization vs tabulation:\n"
        "Memoization shines when only a sparse subset of states are reachable. "
        "Tabulation is faster in practice (no recursion overhead, better cache locality). "
        "For interviews, mention both -- it shows you understand the duality.",
        "\U0001f4a1", "green_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "from functools import lru_cache\n"
    "\n"
    "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
    "    m, n = len(text1), len(text2)\n"
    "\n"
    "    @lru_cache(maxsize=None)\n"
    "    def lcs(i: int, j: int) -> int:\n"
    "        if i == 0 or j == 0:\n"
    "            return 0                               # empty prefix\n"
    "        if text1[i - 1] == text2[j - 1]:\n"
    "            return lcs(i - 1, j - 1) + 1         # match: extend diagonal\n"
    "        return max(lcs(i - 1, j), lcs(i, j - 1)) # mismatch: best of up/left\n"
    "\n"
    "    return lcs(m, n)\n",
    lang="python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("@lru_cache(maxsize=None)", {"code": True}),
    " -- memoises results keyed by (i, j). First call computes; subsequent calls return cached value instantly."
])))
blocks.append(N.para(N.rich([
    ("if i == 0 or j == 0: return 0", {"code": True}),
    " -- base case: any comparison with an empty prefix has LCS 0."
])))
blocks.append(N.para(N.rich([
    ("if text1[i-1] == text2[j-1]:", {"code": True}),
    " -- note the -1 offsets: i and j are 1-indexed lengths; actual characters are at index i-1 and j-1."
])))
blocks.append(N.para(N.rich([
    ("return lcs(i-1, j-1) + 1", {"code": True}),
    " -- both characters match: include this pair, shrink both strings by one."
])))
blocks.append(N.para(N.rich([
    ("return max(lcs(i-1,j), lcs(i,j-1))", {"code": True}),
    " -- mismatch: try excluding each character in turn and take the larger LCS."
])))
blocks.append(N.divider())

# ── Solution 3 — Space-Optimised (Two Rows) ─────────────────────────────────
blocks.append(N.h2("Solution 3 -- Space-Optimised Tabulation (Two Rows)"))

blocks.append(N.toggle_h3("Intuition: How to Arrive at This", [
    N.h4("The Key Observation"),
    N.para(
        "dp[i][j] depends only on dp[i-1][j-1], dp[i-1][j], and dp[i][j-1]. "
        "Once we move to row i, all rows before i-1 are forever irrelevant. "
        "We can discard them and keep only two arrays: prev (row i-1) and curr (row i). "
        "This cuts space from O(m*n) to O(n) while keeping time identical."
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    "def longestCommonSubsequence(text1: str, text2: str) -> int:\n"
    "    m, n = len(text1), len(text2)\n"
    "    prev = [0] * (n + 1)   # dp[i-1][*]\n"
    "\n"
    "    for i in range(1, m + 1):\n"
    "        curr = [0] * (n + 1)\n"
    "        for j in range(1, n + 1):\n"
    "            if text1[i - 1] == text2[j - 1]:\n"
    "                curr[j] = prev[j - 1] + 1          # diagonal\n"
    "            else:\n"
    "                curr[j] = max(prev[j], curr[j - 1]) # up / left\n"
    "        prev = curr\n"
    "\n"
    "    return prev[n]\n",
    lang="python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([
    ("prev = [0] * (n + 1)", {"code": True}),
    " -- initialise row 0 (all zeros -- the base case)."
])))
blocks.append(N.para(N.rich([
    ("curr = [0] * (n + 1)", {"code": True}),
    " -- fresh row for each text1 character; curr[0] = 0 is the base case for empty text2 prefix."
])))
blocks.append(N.para(N.rich([
    ("curr[j] = prev[j - 1] + 1", {"code": True}),
    " -- prev[j-1] = dp[i-1][j-1] (diagonal above-left)."
])))
blocks.append(N.para(N.rich([
    ("curr[j] = max(prev[j], curr[j - 1])", {"code": True}),
    " -- prev[j] = dp[i-1][j] (above); curr[j-1] = dp[i][j-1] (left in same row)."
])))
blocks.append(N.para(N.rich([
    ("prev = curr", {"code": True}),
    " -- slide the window: the row we just computed becomes 'previous' for the next iteration."
])))
blocks.append(N.para(N.rich([
    ("return prev[n]", {"code": True}),
    " -- after the final row (i=m), prev holds dp[m][*]. Cell n is the answer."
])))
blocks.append(N.divider())

# ── Complexity ────────────────────────────────────────────────────────────────
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution",                   "Time",         "Space"],
    ["Brute Force (all subseqs.)", "O(2^m x n)",   "O(m)"],
    ["Bottom-Up Tabulation",       "O(m x n)",     "O(m x n)"],
    ["Top-Down Memoization",       "O(m x n)",     "O(m x n) + stack"],
    ["Space-Optimised (2 rows)",   "O(m x n)",     "O(n)"],
]))
blocks.append(N.divider())

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks.append(N.h2("\U0001f3f7️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Classic 2D DP  |  String Dynamic Programming"])))
blocks.append(N.para(
    "Source: Guide Section 18.6 -- String Dynamic Programming. "
    "Sub-pattern label: 'Classic 2D DP' (exact label from the guide table)."
))
blocks.append(N.callout(
    "When to recognise this pattern:\n"
    "* Two strings/sequences, asked for longest/shortest COMMON property.\n"
    "* Subsequence (characters in order, not necessarily contiguous).\n"
    "* At each pair of indices you choose to match or to skip from one side.\n"
    "* Problem constraints fit O(m*n) -- lengths up to ~1000.\n"
    "* If asked to reconstruct the LCS, backtrack through the dp table.",
    "\U0001f50e", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ───────────────────────────────────────────────────────────
blocks.append(N.h2("\U0001f517 Related Problems"))
blocks.append(N.para("Problems using the same Classic 2D DP / String DP technique:"))

related = [
    ("Edit Distance",                    "Medium, LC 72",   "extend the table to count insert/delete/replace ops; three recurrence cases instead of two."),
    ("Longest Palindromic Subsequence",  "Medium, LC 516",  "LCS of the string with its own reverse."),
    ("Shortest Common Supersequence",    "Hard, LC 1092",   "length = m + n - LCS(text1, text2); backtrack for actual string."),
    ("Interleaving String",              "Medium, LC 97",   "2D DP checks whether s3 is a valid interleaving of s1 and s2."),
    ("Distinct Subsequences",            "Hard, LC 115",    "count the number of ways to form t from s; dp[i][j] accumulates counts."),
    ("Delete Operation for Two Strings", "Medium, LC 583",  "min deletions = m + n - 2 * LCS."),
    ("Minimum ASCII Delete Sum",         "Medium, LC 712",  "weighted LCS variant; minimise ASCII sum of deleted characters."),
    ("Wildcard Matching",                "Hard, LC 44",     "2D DP with '?' and '*'; structurally similar table filling."),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        f" ({diff}) -- {note}"
    ])))

blocks.append(N.para(
    "These problems all share the core idea: a 2D DP table indexed by positions in two strings, "
    "filled via match/mismatch recurrences derived from comparing characters."
))
blocks.append(N.callout(
    "\U0001f4da Reference: DSA_Patterns_and_SubPatterns_Guide.md -- Section 18.6 String Dynamic Programming.",
    "\U0001f4da", "gray_background"
))
blocks.append(N.divider())

# ── Interactive Visual Explainer ──────────────────────────────────────────────
blocks.append(N.h2("\U0001f3af Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("longest_common_subsequence")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually -- use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

# ── 4) Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}  -- appended {len(blocks)} top-level blocks.")
