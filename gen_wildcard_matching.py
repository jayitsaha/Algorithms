"""
gen_wildcard_matching.py
Regenerate Notion page for Wildcard Matching (LC #44, Hard, DP).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8179-891b-ca4048793295"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=44,
    pattern="Dynamic Programming",
    subpatterns=["2D DP with Star Handling"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="dp[i][j] = first i chars of s match first j chars of p; star case: dp[i][j-1] OR dp[i-1][j]",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old content ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and a pattern ", {}),
        ("p", {"code": True}),
        (", implement wildcard pattern matching with support for ", {}),
        ("?", {"code": True}),
        (" (matches any single character) and ", {}),
        ("*", {"code": True}),
        (" (matches any sequence of characters including empty). The matching must cover the entire string.", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("0 ≤ s.length, p.length ≤ 2000; s and p contain only lowercase English letters, '?', and '*'.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: 2D DP Bottom-Up (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — 2D DP Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to decide if pattern p can fully match string s, where '?' matches exactly one character and '*' matches any sequence (including empty). It's an existence question: does ANY valid matching exist?"),
        N.h4("What Doesn't Work"),
        N.para("Greedy fails because '*' creates ambiguity — we don't know how many characters it should consume. Recursion without memoisation revisits the same (i, j) substring pair exponentially: a pattern like '***a' on a string of n 'a's explodes to O(2^n) calls."),
        N.h4("The Key Observation"),
        N.para("Whether s[0..i-1] matches p[0..j-1] depends only on: the characters s[i-1] and p[j-1], plus three smaller subproblems — dp[i-1][j-1] (diagonal), dp[i][j-1] (left), dp[i-1][j] (above). This is the optimal substructure that unlocks DP."),
        N.h4("Building the Solution"),
        N.para("Define dp[i][j] = True if first i chars of s match first j chars of p. Base: dp[0][0]=True; dp[0][j]=True only if p[0..j-1] is all stars. Fill: for each (i,j), apply the 3-case recurrence. Answer: dp[m][n]."),
        N.callout(
            "Analogy: Think of filling a grid where you're asking 'can I tile these two prefix lengths together?' For a star in p, you have a choice each row: does the star stop here (look left) or keep going (look above)?",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Whether s[0..i-1] matches p[0..j-1] depends only on smaller prefixes — the last characters and dp values of smaller (i,j) pairs. No global context needed beyond the table.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursion on (i, j) would recompute the same (i, j) pair from multiple parent calls — especially when a '*' fans out to dp(i-1,j), dp(i-2,j), etc., each re-calling each other.", {}),
    ])),
    N.code("""\
# Recurrence Relations
dp[0][0] = True
dp[0][j] = dp[0][j-1]  if p[j-1] == '*'  else False

if p[j-1] == s[i-1] or p[j-1] == '?':
    dp[i][j] = dp[i-1][j-1]      # diagonal: both advance

elif p[j-1] == '*':
    dp[i][j] = dp[i][j-1]        # star matches empty (skip)
              or dp[i-1][j]       # star eats s[i-1] (stay at j)

else:
    dp[i][j] = False              # mismatch, no wildcard
"""),
    N.h3("Code"),
    N.code("""\
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                      # empty matches empty

    # Base row: empty s vs pattern prefix
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]        # star can match empty

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
                # dp[i][j-1]: star=empty (skip), dp[i-1][j]: star eats s[i-1]
            elif p[j-1] == s[i-1] or p[j-1] == '?':
                dp[i][j] = dp[i-1][j-1]  # diagonal: both match

    return dp[m][n]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(s), len(p)", {"code": True}), (" — store lengths; used as table dimensions and as loop bounds.", {})])),
    N.para(N.rich([("dp = [[False]*(n+1) ...]", {"code": True}), (" — allocate (m+1)×(n+1) table. Extra row and col (index 0) represent empty prefixes. All start False.", {})])),
    N.para(N.rich([("dp[0][0] = True", {"code": True}), (" — base case: empty string matches empty pattern.", {})])),
    N.para(N.rich([("for j in range(1, n+1): if p[j-1]=='*': dp[0][j]=dp[0][j-1]", {"code": True}), (" — base row: a run of leading stars still matches empty s (chain True forward); any non-star breaks the chain (stays False).", {})])),
    N.para(N.rich([("if p[j-1] == '*':", {"code": True}), (" — star wildcard case. Two sub-cases are OR'd together.", {})])),
    N.para(N.rich([("dp[i][j-1]", {"code": True}), (" — star matches empty string: pattern pointer advances, string pointer stays.", {})])),
    N.para(N.rich([("dp[i-1][j]", {"code": True}), (" — star eats one more char from s: string pointer advances, pattern pointer stays (star can continue matching).", {})])),
    N.para(N.rich([("elif p[j-1]==s[i-1] or p[j-1]=='?':", {"code": True}), (" — direct character match or '?' match: take the diagonal dp[i-1][j-1]. Both pointers advance by 1.", {})])),
    N.para(N.rich([("return dp[m][n]", {"code": True}), (" — the answer: do all m chars of s match all n chars of p?", {})])),
    N.callout(
        "⚠️  Common Mistake — Confusing with Regex Matching (#10): In regex, '*' quantifies the preceding element so you look two columns back (dp[i][j-2]). In wildcard matching, '*' is standalone — you only look one column back (dp[i][j-1]). This is the most common error when switching between the two problems.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Space-Optimised Rolling Array ──
blocks += [
    N.h2("Solution 2 — Space-Optimised DP (O(n) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The 2D table works, but each row only reads from the previous row. Can we discard old rows after we process them?"),
        N.h4("The Key Observation"),
        N.para("dp[i][j] depends only on dp[i-1][j-1], dp[i][j-1], and dp[i-1][j]. All of these are in either the previous row or the current row (to the left). So we only need to keep two rows in memory at a time — rolling prev and curr arrays."),
        N.h4("Building the Solution"),
        N.para("Replace the 2D table with two 1D arrays: prev (representing row i-1) and curr (representing row i). After processing each row, set prev = curr."),
    ]),
    N.h3("Code"),
    N.code("""\
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    prev = [False] * (n + 1)          # represents dp[i-1][*]
    prev[0] = True
    for j in range(1, n + 1):         # base row
        prev[j] = prev[j-1] and p[j-1] == '*'

    for i in range(1, m + 1):
        curr = [False] * (n + 1)      # current row dp[i][*]
        for j in range(1, n + 1):
            if p[j-1] == '*':
                curr[j] = curr[j-1] or prev[j]
                # curr[j-1] = dp[i][j-1] (left in curr)
                # prev[j]   = dp[i-1][j] (above in prev)
            elif p[j-1] == s[i-1] or p[j-1] == '?':
                curr[j] = prev[j-1]   # dp[i-1][j-1] diagonal
        prev = curr

    return prev[n]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = [False]*(n+1); prev[0]=True", {"code": True}), (" — initialize base row (row 0). prev[0]=True for dp[0][0].", {})])),
    N.para(N.rich([("for j in range(1,n+1): prev[j] = prev[j-1] and p[j-1]=='*'", {"code": True}), (" — fill base row: True only for unbroken chain of stars.", {})])),
    N.para(N.rich([("curr = [False]*(n+1)", {"code": True}), (" — fresh row for each i. curr[0] stays False (non-empty s can't match empty p).", {})])),
    N.para(N.rich([("curr[j] = curr[j-1] or prev[j]", {"code": True}), (" — star case using rolling arrays. curr[j-1] = dp[i][j-1] (already computed left neighbor in curr); prev[j] = dp[i-1][j] (above in prev).", {})])),
    N.para(N.rich([("curr[j] = prev[j-1]", {"code": True}), (" — match/? case: diagonal = dp[i-1][j-1] is prev[j-1].", {})])),
    N.para(N.rich([("prev = curr", {"code": True}), (" — advance: curr becomes the new prev for the next row.", {})])),
    N.para(N.rich([("return prev[n]", {"code": True}), (" — after all m rows, prev holds dp[m][*]; prev[n] = dp[m][n] is the answer.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Recursion", "O(2^(m+n))", "O(m+n)", "Revisits (i,j) exponentially"],
        ["2D DP (Interview Pick)", "O(m·n)", "O(m·n)", "Clear, standard approach"],
        ["Space-Optimised DP", "O(m·n)", "O(n)", "Rolling two rows"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("2D DP with Star Handling (2D String DP family)", {})])),
    N.callout(
        "When to recognize this pattern: Two strings where one is a pattern/template with wildcards; 'must match entire string'; wildcard creates ambiguous expansion; 'does any valid matching exist?' → 2D DP on prefix pairs, star case is OR of two cells.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 2D String DP technique:"),
    N.bullet(N.rich([("Regular Expression Matching", {"bold": True}), (" (Hard) — Same 2D DP shape but '*' quantifies the preceding element; dp[i][j-2] for star=empty instead of dp[i][j-1] (#10)", {})])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), (" (Medium) — Classic 2D DP on two strings; diagonal for match, skip for mismatch (#1143)", {})])),
    N.bullet(N.rich([("Edit Distance", {"bold": True}), (" (Medium) — 2D DP; (m+1)×(n+1) table; three operations (insert/delete/replace) each map to a cell neighbor (#72)", {})])),
    N.bullet(N.rich([("Distinct Subsequences", {"bold": True}), (" (Hard) — Count ways t appears as subsequence in s; 2D DP on prefixes (#115)", {})])),
    N.bullet(N.rich([("Interleaving String", {"bold": True}), (" (Medium) — 2D DP to check if s3 is interleaving of s1 and s2 (#97)", {})])),
    N.bullet(N.rich([("Shortest Common Supersequence", {"bold": True}), (" (Hard) — Build on LCS table to reconstruct shortest string containing both s1 and s2 (#1092)", {})])),
    N.para("These problems share the same 2D prefix-based DP state: dp[i][j] answers a question about s[0..i-1] and p[0..j-1], with transitions covering match, mismatch, and wildcard cases."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → 2D String DP). Sub-Pattern: 2D DP with Star Handling.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("wildcard_matching")),
    N.para(N.rich([
        ("Step through the 2D DP table cell by cell — use Next/Prev or arrow keys to see how each cell is computed.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Blocks appended: {len(blocks)}")
