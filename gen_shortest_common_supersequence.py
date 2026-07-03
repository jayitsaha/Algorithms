#!/usr/bin/env python3
"""
gen_shortest_common_supersequence.py
Regenerate Notion page for Shortest Common Supersequence (LeetCode #1092).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c2-87b1-ef88cfef07c5"
SLUG    = "shortest_common_supersequence"

# ── 1) Properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1092,
    pattern="Dynamic Programming",
    subpatterns=["LCS + Reconstruction"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="Build LCS DP table then backtrack to reconstruct SCS: LCS chars written once, unique chars from each string added separately.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────
print("Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {n_deleted} blocks.")

# ── 3) Build page body ─────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("str1", {"code": True}),
        (" and ", {}),
        ("str2", {"code": True}),
        (", return the shortest string that has both ", {}),
        ("str1", {"code": True}),
        (" and ", {}),
        ("str2", {"code": True}),
        (" as subsequences. If there are multiple valid strings, return any of them.", {}),
    ])),
    N.para("Example: str1 = \"abac\", str2 = \"cab\" → Output: \"cabac\" (length 5 = 4+3−2)."),
    N.divider(),
]

# ── Solution 1: LCS DP + Reconstruction ──
SOL1_CODE = '''\
def shortestCommonSupersequence(str1: str, str2: str) -> str:
    m, n = len(str1), len(str2)

    # Phase 1: Build LCS DP table
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Phase 2: Reconstruct SCS by backtracking
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:          # LCS char: write once
            result.append(str1[i-1])
            i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:      # came from above: str1's char
            result.append(str1[i-1])
            i -= 1
        else:                                # came from left: str2's char
            result.append(str2[j-1])
            j -= 1
    result.extend(str1[:i])   # drain remaining str1
    result.extend(str2[:j])   # drain remaining str2
    return ''.join(reversed(result))
'''

blocks += [
    N.h2("Solution 1 — LCS DP + Backtracking Reconstruction (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the shortest string containing both str1 and str2 as subsequences. Equivalently: what characters must we write, and what characters can we 'share' between the two strings?"),
        N.h4("What Doesn't Work"),
        N.para("Naive concatenation (str1 + str2) is always valid but never optimal — it ignores the fact that characters shared by both strings only need to appear once in the supersequence."),
        N.h4("The Key Observation"),
        N.para("Characters in the LCS of str1 and str2 can serve double duty — written once, they satisfy both strings simultaneously. So: SCS_length = m + n − LCS_length. The challenge is building the actual string, not just finding its length."),
        N.h4("Building the Solution"),
        N.para("Step 1: Fill the LCS DP table (dp[i][j] = LCS length of str1[:i] and str2[:j]). Step 2: Backtrack from dp[m][n]. At each step: if characters match, write once and advance both pointers (LCS character). If they don't match, follow the direction of the larger neighbor — that string's character must appear separately in the SCS. Drain leftovers and reverse."),
        N.callout("Analogy: Merging two sorted lists — you always pick from one side at a time, but when both have the same element, you pick it once and advance both. That's exactly what LCS reconstruction does.", "🧠", "blue_background"),
    ]),
]

blocks += [
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("LCS(str1[:i], str2[:j]) is derived from LCS(str1[:i-1], str2[:j-1]), LCS(str1[:i-1], str2[:j]), and LCS(str1[:i], str2[:j-1]).", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive LCS would recompute the same (i, j) pairs exponentially many times. The 2D table caches each in O(1).", {}),
    ])),
]

blocks += [
    N.h3("Recurrence Relations"),
    N.code(
        "dp[i][j] = dp[i-1][j-1] + 1              if str1[i-1] == str2[j-1]\n"
        "dp[i][j] = max(dp[i-1][j], dp[i][j-1])   otherwise\n\n"
        "SCS_length = m + n - dp[m][n]",
        lang="plain text"
    ),
]

blocks += [
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(str1), len(str2)", {"code": True}), (" — store lengths; m for str1, n for str2.", {})])),
    N.para(N.rich([("dp = [[0]*(n+1) for _ in range(m+1)]", {"code": True}), (" — (m+1)×(n+1) table; row 0 and col 0 are base cases (LCS with empty string = 0).", {})])),
    N.para(N.rich([("if str1[i-1] == str2[j-1]:", {"code": True}), (" — characters at current positions match.", {})])),
    N.para(N.rich([("dp[i][j] = dp[i-1][j-1] + 1", {"code": True}), (" — extend the LCS diagonally; both characters consumed.", {})])),
    N.para(N.rich([("dp[i][j] = max(dp[i-1][j], dp[i][j-1])", {"code": True}), (" — mismatch; skip one character from either string and take the better LCS.", {})])),
    N.para(N.rich([("i, j = m, n", {"code": True}), (" — start backtrack at bottom-right of the table (full strings).", {})])),
    N.para(N.rich([("if str1[i-1] == str2[j-1]:", {"code": True}), (" — LCS character: it is shared by both strings, write it once in the SCS.", {})])),
    N.para(N.rich([("i -= 1; j -= 1", {"code": True}), (" — both pointers advance since this character is consumed from both.", {})])),
    N.para(N.rich([("elif dp[i-1][j] >= dp[i][j-1]:", {"code": True}), (" — cell came from 'above' (str1 pointer advanced in the LCS fill), so str1's character is unique here.", {})])),
    N.para(N.rich([("result.extend(str1[:i]); result.extend(str2[:j])", {"code": True}), (" — one pointer hit 0; drain remaining chars from the other string.", {})])),
    N.para(N.rich([("return ''.join(reversed(result))", {"code": True}), (" — we built the list in reverse order (from the end); flip to get the correct SCS.", {})])),
    N.callout(
        "⚠️ Why >= not > in the mismatch branch? When dp[i-1][j] == dp[i][j-1] (tie), both directions lead to equally good LCS paths. Using >= breaks ties by preferring str1. Either choice is correct — the SCS will have the same length regardless.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Naive Concatenation ──
SOL2_CODE = '''\
def shortestCommonSupersequence_naive(str1: str, str2: str) -> str:
    # str1 is a prefix (and thus a subsequence) of str1 + str2
    # str2 is a suffix (and thus a subsequence) of str1 + str2
    # Valid, but always length m+n — never optimal unless LCS is empty.
    return str1 + str2
'''

blocks += [
    N.h2("Solution 2 — Naive Concatenation (Brute Force Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every string is trivially a subsequence of itself. So str1 + str2 always works: str1 is the prefix (a subsequence), str2 is the suffix (a subsequence)."),
        N.h4("What Doesn't Work"),
        N.para("It's valid but never minimal. It completely ignores the fact that shared characters can be written once. If LCS_length > 0, we can always do better."),
        N.h4("The Key Observation"),
        N.para("This baseline is only optimal when the two strings share no common characters at all (LCS = empty). In that case, m + n − 0 = m + n = concatenation length. But the problem doesn't guarantee that."),
        N.h4("Building the Solution"),
        N.para("Trivially return str1 + str2. Use this to establish the upper bound, then explain why the LCS-based approach beats it."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("return str1 + str2", {"code": True}), (" — str1 is a subsequence of str1+str2 (it's the full prefix); str2 is a subsequence (the full suffix). Length = m+n. Only optimal if LCS is empty.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Naive Concatenation", "O(m+n)", "O(m+n)"],
        ["LCS DP + Reconstruction (Interview Pick)", "O(m·n)", "O(m·n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("LCS + Reconstruction (DP: LCS variant)", {})])),
    N.callout(
        "When to recognize this pattern: Two strings + 'shortest string containing both as subsequences' → 2D LCS DP. "
        "Any problem asking to reconstruct the actual path through a DP table (not just its value) → backtracking from bottom-right to top-left.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same LCS + Reconstruction technique:"),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), (" (Medium) — The prerequisite; same DP table, just return dp[m][n]. #1143", {})])),
    N.bullet(N.rich([("Edit Distance", {"bold": True}), (" (Medium) — 2D DP on two strings; min insertions + deletions = m + n − 2·LCS. #72", {})])),
    N.bullet(N.rich([("Distinct Subsequences", {"bold": True}), (" (Hard) — Count ways to form t as a subsequence of s; same DP shape. #115", {})])),
    N.bullet(N.rich([("Interleaving String", {"bold": True}), (" (Medium) — 2D DP checking if s3 is a valid interleaving of s1 and s2. #97", {})])),
    N.bullet(N.rich([("Delete Operation for Two Strings", {"bold": True}), (" (Medium) — Min deletions to make both strings equal = m + n − 2·LCS. #583", {})])),
    N.bullet(N.rich([("Minimum ASCII Delete Sum for Two Strings", {"bold": True}), (" (Medium) — Weighted LCS: minimize sum of deleted characters' ASCII values. #712", {})])),
    N.para("These problems all share the core technique: 2D DP on (prefix of str1) × (prefix of str2), with recurrence based on character equality."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → DP: LCS)", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the LCS fill and backtracking reconstruction — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
