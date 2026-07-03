"""
gen_regular_expression_matching.py
Regenerate the Notion page for Regular Expression Matching (LeetCode #10).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81ff-9819-fe65dde105d8"
SLUG    = "regular_expression_matching"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=10,
    pattern="Dynamic Programming",
    subpatterns=["2D DP with Dot and Star"],
    tc="O(m·n)",
    sc="O(m·n)",
    key_insight="dp[i][j]: * gives two choices — zero occurrences (skip x*, look at j-2) or one-more (same j, consume s char). Fill table row by row; answer is dp[m][n].",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and a pattern ", {}),
        ("p", {"code": True}),
        (", implement regular expression matching with support for ", {}),
        (".", {"code": True}),
        (" (matches any single character) and ", {}),
        ("*", {"code": True}),
        (" (zero or more of the preceding element). The match must cover the entire input string — not just a prefix or substring.", {}),
    ])),
    N.para(N.rich([
        ("Examples: ", {"bold": True}),
        ('isMatch("aa","a*") → True, isMatch("ab",".*") → True, isMatch("aab","c*a*b") → True, isMatch("aa","a") → False', {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — 2D Tabulation ──
TABULATION_CODE = """\
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                            # empty pattern matches empty string

    # First row: which patterns can match the empty string?
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]             # x* unit can appear zero times

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]         # option 1: zero occurrences of x*
                if p[j-2] in (s[i-1], '.'):   # predecessor matches current s char?
                    dp[i][j] |= dp[i-1][j]    # option 2: one-or-more, stay at j
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]       # single char match: look diagonal

    return dp[m][n]
"""

blocks += [
    N.h2("Solution 1 — 2D Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are asking: 'Does the entire string s fit the entire pattern p?' At each position pair (i, j), we have a sub-question: 'Does p[0..j-1] match s[0..i-1]?' If we can answer all sub-questions, the full answer is just the bottom-right cell."),
        N.h4("What Doesn't Work"),
        N.para("Recursive brute force tries every possibility without caching — with patterns like '.*.*a', the same sub-problem (i, j) is recomputed exponentially many times, leading to TLE on long inputs."),
        N.h4("The Key Observation"),
        N.para("The * always pairs with its predecessor character. So 'a*' is a two-character unit meaning 'zero or more a\'s'. When we encounter *, we have exactly two independent choices: (1) use zero occurrences — skip the entire x* unit and look two columns back (dp[i][j-2]), or (2) use one-more occurrence — consume one character of s and stay at the same pattern position (dp[i-1][j]). These two cases cover all possibilities."),
        N.h4("Building the Solution"),
        N.para("Define dp[i][j] = True iff p[0..j-1] fully matches s[0..i-1]. Base case: dp[0][0] = True. Fill the first row for patterns matching the empty string (x* units with zero repetitions). Then fill the rest row by row, left to right, applying the two rules. The answer is dp[m][n]."),
        N.callout("Analogy: Think of dp[i-1][j] for 'one-more' as 'I used one s-character but the * can still fire again — stay at the same pattern position.' This is the non-obvious step that trips up many candidates.", "🧠", "blue_background"),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para("Optimal Substructure: dp[i][j] depends only on strictly smaller sub-problems — dp[i-1][j-1], dp[i][j-2], or dp[i-1][j]. Overlapping Subproblems: the naive recursion recomputes match(s[i:], p[j:]) for the same (i,j) pair exponentially many times with patterns like '.*.*'. Memoization or tabulation reduces this to O(m·n) total computations."),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [[False]*(n+1) ...]", {"code": True}), (" — Create (m+1)×(n+1) table. Row index = chars consumed from s. Col index = chars consumed from p.", {})])),
    N.para(N.rich([("dp[0][0] = True", {"code": True}), (" — Base case: empty pattern matches empty string.", {})])),
    N.para(N.rich([("for j in range(1, n+1): if p[j-1]=='*': dp[0][j]=dp[0][j-2]", {"code": True}), (" — Fill first row. Only x* units can match empty string by firing zero times. Propagate left-two steps.", {})])),
    N.para(N.rich([("if p[j-1] == '*':", {"code": True}), (" — Star case: the current pattern char is *, which modifies its predecessor p[j-2].", {})])),
    N.para(N.rich([("dp[i][j] = dp[i][j-2]", {"code": True}), (" — Option 1: use zero occurrences of the x* unit. Skip it entirely, inherit from two columns back.", {})])),
    N.para(N.rich([("if p[j-2] in (s[i-1], '.'):", {"code": True}), (" — Check if the predecessor (p[j-2]) can match the current string character. Note: we check p[j-2], not p[j-1] (which is the star itself).", {})])),
    N.para(N.rich([("dp[i][j] |= dp[i-1][j]", {"code": True}), (" — Option 2: use one more occurrence. Consume s[i-1] but STAY at column j (same x* pattern can fire again). OR-assign so we don't lose a True from option 1.", {})])),
    N.para(N.rich([("elif p[j-1]=='.' or p[j-1]==s[i-1]: dp[i][j]=dp[i-1][j-1]", {"code": True}), (" — Literal or dot: current pattern char matches current string char. Consume both → look diagonally (i-1, j-1).", {})])),
    N.para(N.rich([("return dp[m][n]", {"code": True}), (" — The cell at the bottom-right corner: did the full pattern match the full string?", {})])),
    N.divider(),
]

# ── Solution 2 — Top-Down Memoization ──
MEMO_CODE = """\
from functools import cache

def isMatch(s: str, p: str) -> bool:
    @cache
    def dp(i, j):
        # Base: pattern exhausted → string must also be exhausted
        if j == len(p):
            return i == len(s)
        # Does current pattern char match current string char?
        first = i < len(s) and p[j] in (s[i], '.')
        # Is the next pattern char a '*'?
        if j + 1 < len(p) and p[j + 1] == '*':
            # Two choices: skip x* (zero) or use one-more (if first matches)
            return dp(i, j + 2) or (first and dp(i + 1, j))
        # Single char: must match, advance both
        return first and dp(i + 1, j + 1)

    return dp(0, 0)
"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Recursive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think recursively: 'Can I match s[i:] against p[j:]?' If j reaches the end of p, s must also be exhausted. Otherwise, check if p[j] (or '.') matches s[i], then decide based on whether p[j+1] is a '*'."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes the same dp(i, j) call many times — exponential for pathological patterns like '.*.*.*'."),
        N.h4("The Key Observation"),
        N.para("The look-ahead for '*' (checking p[j+1]) is easier to think about in the recursive form: if we see x* ahead, we either skip it (dp(i, j+2)) or use one occurrence (first match AND dp(i+1, j)). The @cache decorator handles memoization automatically."),
        N.h4("Building the Solution"),
        N.para("Define dp(i, j) to return True if s[i:] matches p[j:]. Use Python's @cache. The function body maps almost directly to the recurrence: base case, first-match check, star handling."),
        N.callout("The top-down form is easier to derive but slightly harder to trace for interviewers. The tabulation form (Solution 1) is usually preferred for interviews because the table filling is tangible and easy to walk through.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@cache", {"code": True}), (" — Python's built-in memoization (Python 3.9+). Caches the result of each (i, j) call, preventing recomputation.", {})])),
    N.para(N.rich([("if j == len(p): return i == len(s)", {"code": True}), (" — Pattern exhausted. The match succeeds only if s is also exhausted (full-string requirement).", {})])),
    N.para(N.rich([("first = i < len(s) and p[j] in (s[i], '.')", {"code": True}), (" — Boolean: can the current pattern char (p[j]) match the current string char (s[i])? Also guards against out-of-bounds (i < len(s)).", {})])),
    N.para(N.rich([("if j+1 < len(p) and p[j+1] == '*':", {"code": True}), (" — Look-ahead: is the NEXT pattern char a '*'? If so, we handle the x* unit now.", {})])),
    N.para(N.rich([("return dp(i, j+2) or (first and dp(i+1, j))", {"code": True}), (" — Two options: skip x* entirely (advance j by 2), OR if current chars match, consume one s-char and stay at j (x* can fire again).", {})])),
    N.para(N.rich([("return first and dp(i+1, j+1)", {"code": True}), (" — No '*' follows: single char match. Both i and j must advance (consume one char each).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time",      "Space"],
        ["Brute Force Recursion", "Exponential","O(m+n) stack"],
        ["Top-Down Memoization",  "O(m·n)",    "O(m·n)"],
        ["2D Tabulation ✓",      "O(m·n)",    "O(m·n)"],
        ["Rolling Array DP",      "O(m·n)",    "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("2D DP with Dot and Star", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Match entire string against pattern with . and *'. (2) A token can represent zero or more characters (star modifier). (3) Two string/pattern indices form the state → (i, j) table. (4) Star gives two choices → OR of two DP cells.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related 2D String DP technique:"),
    N.bullet(N.rich([("Wildcard Matching", {"bold": True}), (" (Hard, #44) — Similar 2D DP but * matches any sequence directly without pairing to a predecessor; slightly simpler recurrence.", {})])),
    N.bullet(N.rich([("Edit Distance", {"bold": True}), (" (Medium, #72) — 2D DP on two strings with insert/delete/replace costs; classic LCS-family problem.", {})])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), (" (Medium, #1143) — Same (i,j) state, diagonal dependency; foundational 2D string DP.", {})])),
    N.bullet(N.rich([("Interleaving String", {"bold": True}), (" (Medium, #97) — 2D DP checking if s3 is an interleaving of s1 and s2.", {})])),
    N.bullet(N.rich([("Distinct Subsequences", {"bold": True}), (" (Hard, #115) — Count the number of ways t appears as a subsequence of s; (i,j) table with one-or-skip choice.", {})])),
    N.bullet(N.rich([("Shortest Common Supersequence", {"bold": True}), (" (Hard, #1092) — Find shortest string containing both s and t as subsequences; builds on LCS.", {})])),
    N.bullet(N.rich([("Minimum ASCII Delete Sum for Two Strings", {"bold": True}), (" (Medium, #712) — Minimize sum of ASCII values of deleted characters to make strings equal.", {})])),
    N.para("These problems share the core technique of defining a 2D state (i, j) over two string/pattern prefixes and filling a table bottom-up."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-Pattern: '2D DP with Dot and Star'.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the DP table cell by cell — use Next/Prev or arrow keys to see exactly how each dp[i][j] is derived.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append in chunks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks.")
print(f"NOTION OK {PAGE_ID}")
