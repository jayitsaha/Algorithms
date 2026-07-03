"""
gen_distinct_subsequences.py
Notion page rebuild for LeetCode #115 — Distinct Subsequences (Hard)
DP sub-pattern: Count Ways to Form t from s (2D String DP)
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81c4-9ba3-cb8973016d6c"

# ── 1) Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=115,
    pattern="Dynamic Programming",
    subpatterns=["Count Ways (2D String DP)", "DP: LCS"],
    tc="O(m·n)",
    sc="O(n)  (space-optimised 1-D rolling array)",
    key_insight="dp[i][j] = ways to form t[:j] from s[:i]; on match add skip+use paths.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Build body ────────────────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("s", {"code": True}),
        (" and ", {}),
        ("t", {"code": True}),
        (", return the number of distinct subsequences of ", {}),
        ("s", {"code": True}),
        (" which equals ", {}),
        ("t", {"code": True}),
        (". A subsequence is formed by deleting some (or no) characters from ", {}),
        ("s", {"code": True}),
        (" without changing the relative order. Two selections using different index "
         "sets are always counted as distinct, even if they yield the same characters.", {}),
    ])),
    N.para(N.rich([
        ("Example 1:  s = \"rabbbit\",  t = \"rabbit\"  →  3", {"code": True}),
    ])),
    N.para("There are exactly 3 ways to delete one 'b' from 'rabbbit' to get 'rabbit': "
           "delete the 3rd, 4th, or 5th character (all three 'b' positions)."),
    N.para(N.rich([
        ("Example 2:  s = \"babgbag\",  t = \"bag\"  →  5", {"code": True}),
    ])),
    N.divider(),
]

# ── SOLUTION 1 — Recursive Brute Force ───────────────────────────────────────
brute_code = (
    "def numDistinct_brute(s: str, t: str) -> int:\n"
    '    """Exponential brute-force: explore all keep/skip branches."""\n'
    "    def recurse(i, j):\n"
    "        if j == len(t):          # Formed all of t\n"
    "            return 1\n"
    "        if i == len(s):          # Exhausted s before finishing t\n"
    "            return 0\n"
    "        ways = recurse(i + 1, j)      # always skip s[i]\n"
    "        if s[i] == t[j]:              # match: also try using s[i]\n"
    "            ways += recurse(i + 1, j + 1)\n"
    "        return ways\n"
    "    return recurse(0, 0)\n"
)

blocks += [
    N.h2("Solution 1 — Recursive Brute Force (educational baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We walk through s character by character. At each position i in s we are "
               "trying to fill position j in t. The question becomes: how many full "
               "selections of t exist, starting from pair (i, j)?"),
        N.h4("What Doesn't Work at Scale"),
        N.para("Generating all 2^m subsets of s and checking each is O(2^m * n) — "
               "completely infeasible for m = 1000. Recursion without caching hits "
               "the same exponential branching."),
        N.h4("The Key Observation"),
        N.para("At each character of s we have at most two choices: skip it (always valid) "
               "or use it for the current unfilled t-slot (only valid when characters match). "
               "These choices form a binary tree. The answer is the number of leaves where "
               "we successfully fill all of t."),
        N.h4("Building the Solution"),
        N.para("Define recurse(i, j) = ways to form t[j:] using s[i:]. "
               "Base cases: j == len(t) returns 1 (success); i == len(s) returns 0 (ran out). "
               "Always recurse with skip: recurse(i+1, j). On a character match also recurse "
               "with use: recurse(i+1, j+1). Sum both branches."),
        N.callout(
            "Analogy: t has n empty slots to fill left-to-right. Walking through s, "
            "when you see a matching character you may fill the current slot now or "
            "walk past it. Recursion counts all distinct ways to fill every slot.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(brute_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def recurse(i, j):", {"code": True}),
                   (" — helper returning count of ways to form t[j:] using s[i:].", {})])),
    N.para(N.rich([("if j == len(t): return 1", {"code": True}),
                   (" — all t slots filled; this selection is one valid distinct subsequence.", {})])),
    N.para(N.rich([("if i == len(s): return 0", {"code": True}),
                   (" — s exhausted but t unfinished; dead end, contributes 0.", {})])),
    N.para(N.rich([("ways = recurse(i + 1, j)", {"code": True}),
                   (" — unconditionally skip s[i]; j stays the same (t-slot unfilled).", {})])),
    N.para(N.rich([("if s[i] == t[j]: ways += recurse(i + 1, j + 1)", {"code": True}),
                   (" — match: also try using s[i] for t[j]; both i and j advance.", {})])),
    N.para(N.rich([("return ways", {"code": True}),
                   (" — total ways for this (i, j) state.", {})])),
    N.divider(),
]

# ── SOLUTION 2 — Memoisation ─────────────────────────────────────────────────
memo_code = (
    "from functools import lru_cache\n\n"
    "def numDistinct_memo(s: str, t: str) -> int:\n"
    '    """Top-down DP: memoize overlapping (i, j) subproblems."""\n'
    "    @lru_cache(maxsize=None)\n"
    "    def dp(i, j):\n"
    "        if j == len(t): return 1         # all of t matched\n"
    "        if i == len(s): return 0         # s exhausted\n"
    "        ways = dp(i + 1, j)              # skip s[i]\n"
    "        if s[i] == t[j]:\n"
    "            ways += dp(i + 1, j + 1)    # also try using s[i]\n"
    "        return ways\n"
    "    return dp(0, 0)\n"
)

blocks += [
    N.h2("Solution 2 — Top-Down DP with Memoisation"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The brute-force recursion recomputes dp(i, j) many times for the same pair "
               "because different early branching decisions can arrive at the same (i, j) "
               "state. Simply cache each unique (i, j) result."),
        N.h4("The Key Observation"),
        N.para("There are only m*n distinct (i, j) pairs. With caching each is computed "
               "once at O(1) work per pair, giving O(m*n) total time. The recursion "
               "structure is identical to brute force — the only change is @lru_cache."),
        N.h4("Building the Solution"),
        N.para("Wrap recurse in @lru_cache(maxsize=None). Every unique (i, j) is "
               "computed exactly once. Space: O(m*n) cache plus O(m+n) call stack depth."),
        N.callout(
            "Memoisation is the easiest mental step: once you see the recursion, just "
            "add @lru_cache. This converts a clean recursive idea into efficient DP "
            "without restructuring any logic.",
            "🧠", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("numDistinct(s, t) depends only on numDistinct(s[1:], t) and "
         "numDistinct(s[1:], t[1:]) — strictly smaller subproblems.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("Many different selections of early s characters arrive at the same remaining "
         "(i, j) suffix. Without caching the same (i, j) is solved exponentially often.", {}),
    ])),
    N.code(
        "Recurrence:\n"
        "  dp(i, j) = dp(i+1, j)                      if s[i] != t[j]\n"
        "  dp(i, j) = dp(i+1, j) + dp(i+1, j+1)      if s[i] == t[j]\n"
        "\n"
        "Base cases:\n"
        "  dp(i, len(t)) = 1   (matched all of t — success)\n"
        "  dp(len(s), j) = 0   (s exhausted, t unfinished — failure)\n",
        lang="plain text",
    ),
    N.h3("Code"),
    N.code(memo_code),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — caches return value for every unique (i, j) argument pair.", {})])),
    N.para(N.rich([("if j == len(t): return 1", {"code": True}),
                   (" — base case: all t slots matched; 1 valid selection.", {})])),
    N.para(N.rich([("if i == len(s): return 0", {"code": True}),
                   (" — base case: s exhausted before t finished; impossible.", {})])),
    N.para(N.rich([("ways = dp(i + 1, j)", {"code": True}),
                   (" — skip s[i]; count selections that don't use this character.", {})])),
    N.para(N.rich([("if s[i] == t[j]: ways += dp(i + 1, j + 1)", {"code": True}),
                   (" — match: add selections that DO use s[i] for t[j].", {})])),
    N.divider(),
]

# ── SOLUTION 3 — Bottom-Up 2D Tabulation (Interview Pick) ────────────────────
tab_code = (
    "def numDistinct(s: str, t: str) -> int:\n"
    '    """Bottom-up 2D tabulation — canonical interview solution."""\n'
    "    m, n = len(s), len(t)\n"
    "    # dp[i][j] = # ways to form t[:j] using s[:i]\n"
    "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
    "    # Base case: empty t can always be formed (select nothing)\n"
    "    for i in range(m + 1):\n"
    "        dp[i][0] = 1\n"
    "    for i in range(1, m + 1):\n"
    "        for j in range(1, n + 1):\n"
    "            dp[i][j] = dp[i-1][j]           # skip s[i-1] (always)\n"
    "            if s[i-1] == t[j-1]:\n"
    "                dp[i][j] += dp[i-1][j-1]    # also count 'use' branch\n"
    "    return dp[m][n]\n"
)

blocks += [
    N.h2("Solution 3 — Bottom-Up 2D Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of top-down recursion, build the answer from scratch: start from "
               "the simplest subproblems (empty strings) and fill the table iteratively "
               "toward the full problem."),
        N.h4("The Key Observation"),
        N.para("Each cell dp[i][j] depends only on dp[i-1][j] and dp[i-1][j-1] — only "
               "the previous row. We can fill the table row by row, and even compress to "
               "a single 1-D array by traversing j in reverse."),
        N.h4("Building the Solution"),
        N.para("Allocate (m+1)*(n+1) table. Set dp[i][0]=1 for all i. For each row i "
               "(character of s) and column j (character of t): dp[i][j] = dp[i-1][j] "
               "(skip path, always). If s[i-1]==t[j-1] also add dp[i-1][j-1] (use path). "
               "Return dp[m][n]."),
        N.callout(
            "Think of the table as a spreadsheet. Row i summarises 'what can we form "
            "from the first i characters of s?' Each row is computed purely from the "
            "row above — no guessing, no branching, no stack overflow.",
            "🧠", "blue_background"),
    ]),
    N.h3("State Definition & Transitions"),
    N.code(
        "State:  dp[i][j] = # ways to form t[0..j-1] using s[0..i-1]\n"
        "\n"
        "Transition:\n"
        "  dp[i][j] = dp[i-1][j]                  # skip s[i-1] (always valid)\n"
        "  if s[i-1] == t[j-1]:\n"
        "      dp[i][j] += dp[i-1][j-1]            # use s[i-1] for t[j-1]\n"
        "\n"
        "Base cases:\n"
        "  dp[i][0] = 1   for all i    (empty t: exactly 1 way — choose nothing)\n"
        "  dp[0][j] = 0   for j > 0   (empty s: can't form non-empty t)\n",
        lang="plain text",
    ),
    N.h3("Code"),
    N.code(tab_code),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(s), len(t)", {"code": True}),
                   (" — cache string lengths; m indexes rows (s), n indexes columns (t).", {})])),
    N.para(N.rich([("dp = [[0]*(n+1) for _ in range(m+1)]", {"code": True}),
                   (" — (m+1)*(n+1) table; extra row/col for empty-string base cases.", {})])),
    N.para(N.rich([("for i in range(m+1): dp[i][0] = 1", {"code": True}),
                   (" — every s-prefix (including empty) can form empty t in exactly 1 way.", {})])),
    N.para(N.rich([("for i in range(1, m+1):", {"code": True}),
                   (" — outer loop: each character of s, building row i from row i-1.", {})])),
    N.para(N.rich([("    for j in range(1, n+1):", {"code": True}),
                   (" — inner loop: each character of t we are trying to match.", {})])),
    N.para(N.rich([("        dp[i][j] = dp[i-1][j]", {"code": True}),
                   (" — skip s[i-1]: inherit count from the row above (pretend s[i-1] doesn't exist).", {})])),
    N.para(N.rich([("        if s[i-1] == t[j-1]:", {"code": True}),
                   (" — characters match; we CAN use s[i-1] to satisfy t[j-1].", {})])),
    N.para(N.rich([("            dp[i][j] += dp[i-1][j-1]", {"code": True}),
                   (" — add 'use' branch: ways to form t[:j-1] from s[:i-1], "
                    "because using s[i-1] for t[j-1] reduces both pointers by one.", {})])),
    N.para(N.rich([("return dp[m][n]", {"code": True}),
                   (" — bottom-right corner = ways to form all of t from all of s.", {})])),
    N.callout(
        "Common mistake: on a match, writing dp[i][j] = dp[i-1][j-1] alone "
        "(forgetting the skip path dp[i-1][j]). The skip path is ALWAYS included; "
        "the use path is ADDED on top. Skipping the skip path produces wrong answers.",
        "⚠️", "yellow_background"),
    N.divider(),
]

# ── SOLUTION 4 — Space-Optimised 1-D ─────────────────────────────────────────
opt_code = (
    "def numDistinct_1d(s: str, t: str) -> int:\n"
    '    """Space-optimised: single 1-D DP array (iterate j right-to-left)."""\n'
    "    n = len(t)\n"
    "    dp = [0] * (n + 1)\n"
    "    dp[0] = 1           # base: 1 way to form empty t\n"
    "    for ch in s:\n"
    "        # RIGHT-TO-LEFT to avoid using same s-character twice\n"
    "        for j in range(n, 0, -1):\n"
    "            if ch == t[j-1]:\n"
    "                dp[j] += dp[j-1]\n"
    "    return dp[n]\n"
)

blocks += [
    N.h2("Solution 4 — Space-Optimised 1-D DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("In the 2D table, row i depends ONLY on row i-1. So we can keep just one "
               "1-D array and update it in-place, row by row."),
        N.h4("The Key Observation"),
        N.para("When updating dp[j] for the current s-character, we need the OLD dp[j-1] "
               "from before this s-character was processed. Scanning j left-to-right would "
               "overwrite dp[j-1] before we read it. Scanning RIGHT-TO-LEFT reads dp[j-1] "
               "before we update dp[j] — preserving the previous-row value."),
        N.h4("Building the Solution"),
        N.para("Start with dp = [1, 0, 0, ..., 0] of length n+1. For each character ch in s, "
               "loop j from n down to 1. If ch == t[j-1], dp[j] += dp[j-1]. Return dp[n]."),
        N.callout(
            "This is the same right-to-left trick used in 0/1 Knapsack: iterate the "
            "second dimension backwards to avoid using an updated value that should be "
            "from the 'previous row'.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(opt_code),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0]*(n+1);  dp[0] = 1", {"code": True}),
                   (" — single 1-D array; dp[j] = ways to form t[:j] from s seen so far. "
                    "dp[0]=1 because empty t is always achievable.", {})])),
    N.para(N.rich([("for ch in s:", {"code": True}),
                   (" — process each s character (simulates adding row i in 2D table).", {})])),
    N.para(N.rich([("    for j in range(n, 0, -1):", {"code": True}),
                   (" — RIGHT-TO-LEFT so dp[j-1] still holds the previous-iteration value "
                    "when we read it.", {})])),
    N.para(N.rich([("        if ch == t[j-1]: dp[j] += dp[j-1]", {"code": True}),
                   (" — match: add 'use' ways. dp[j] already holds 'skip' value from "
                    "the start of this outer-loop iteration.", {})])),
    N.para(N.rich([("return dp[n]", {"code": True}),
                   (" — final answer: ways to form all of t.", {})])),
    N.divider(),
]

# ── COMPLEXITY TABLE ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Recursion)", "O(2^m)", "O(m+n)  call stack"],
        ["Top-Down Memoisation", "O(m·n)", "O(m·n) cache + O(m+n) stack"],
        ["Bottom-Up 2D Tabulation", "O(m·n)", "O(m·n)"],
        ["Space-Optimised 1-D DP", "O(m·n)", "O(n)  ← optimal"],
    ]),
    N.callout(
        "Interview recommendation: present Solution 3 (2D tabulation) as your primary "
        "answer — it is clear and easy to walk through. Mention Solution 4 (1-D) "
        "as a follow-up when asked 'can you reduce space?'",
        "🎯", "green_background"),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Count Ways (2D String DP) / DP: LCS", {})])),
    N.para("This is a 2D string DP problem structurally identical to the LCS family: "
           "one index walks s, the other walks t, and the recurrence decides what "
           "to do when characters match vs. don't match. Here we COUNT ways instead "
           "of computing a maximum, so the transition adds (instead of max-ing)."),
    N.callout(
        "When to recognise this pattern:\n"
        "• Two strings s and t given; asked to COUNT something (ways, subsequences)\n"
        "• Characters must appear in order (subsequence semantics, not substring)\n"
        "• 'How many distinct ways...' phrasing with characters that repeat\n"
        "• Brute force enumerates all subsets of s — exponential => classic DP signal\n"
        "• Classic 2D state: dp[i][j] = answer for prefixes s[:i] and t[:j]",
        "🔎", "green_background"),
    N.divider(),
]

# ── RELATED PROBLEMS ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 2D string DP / count-ways technique:"),
    N.bullet(N.rich([
        ("Longest Common Subsequence", {"bold": True}),
        (" (Medium) — same dp[i][j] over two strings; maximise length instead of counting.", {}),
    ])),
    N.bullet(N.rich([
        ("Edit Distance", {"bold": True}),
        (" (Hard) — dp[i][j] = min operations to convert s[:i] to t[:j]; three transitions.", {}),
    ])),
    N.bullet(N.rich([
        ("Interleaving String", {"bold": True}),
        (" (Hard) — dp[i][j] = can s1[:i]+s2[:j] interleave to form s3; same 2D prefix structure.", {}),
    ])),
    N.bullet(N.rich([
        ("Shortest Common Supersequence", {"bold": True}),
        (" (Hard) — builds on LCS table to reconstruct the merged shortest string.", {}),
    ])),
    N.bullet(N.rich([
        ("Regular Expression Matching", {"bold": True}),
        (" (Hard) — 2D DP over (s, pattern); match/skip decisions at each cell.", {}),
    ])),
    N.bullet(N.rich([
        ("Wildcard Matching", {"bold": True}),
        (" (Hard) — similar to regex with '?' and '*'; same 2D table fill approach.", {}),
    ])),
    N.bullet(N.rich([
        ("Number of Matching Subsequences", {"bold": True}),
        (" (Medium) — counts words from a list that appear as subsequences of s; "
         "same pointer-advance-on-match logic.", {}),
    ])),
    N.bullet(N.rich([
        ("Count Vowel Substrings of a String", {"bold": True}),
        (" (Easy) — counting subsequences variant; good warm-up for this problem.", {}),
    ])),
    N.para("These problems share the core technique: define dp[i][j] over two string "
           "prefixes, handle match vs no-match transitions, anchor on empty-string base cases."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — "
        "Dynamic Programming, DP: LCS family. "
        "'Count Ways (2D String DP)' is the counting variant of the LCS sub-pattern.",
        "📚", "gray_background"),
    N.divider(),
]

# ── INTERACTIVE EXPLAINER EMBED ───────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("distinct_subsequences")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── 4) Append ────────────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK  {PAGE_ID}  ({len(blocks)} top-level blocks appended)")
