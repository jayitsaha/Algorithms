"""
gen_interleaving_string.py
Notion page rebuild for: Interleaving String (LeetCode #97)
Pattern: Dynamic Programming / 2D DP on Both Strings
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f6-a0a3-e43f87a600d3"

# ── 1. Properties ────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=97,
    pattern="Dynamic Programming",
    subpatterns=["2D DP on Both Strings", "LCS-Style DP"],
    tc="O(m × n)",
    sc="O(m × n) → O(n) with rolling row",
    key_insight="dp[i][j] = True iff s3[:i+j] can be formed by interleaving s1[:i] and s2[:j]; "
                "check character match + prior state.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old page body...")
removed = N.wipe_page(PAGE_ID)
print(f"  Removed {removed} blocks.")

# ── 3. Build body ────────────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "Given strings s1, s2, and s3, return true if s3 is formed by an interleaving of s1 and s2.\n"
    "An interleaving of two strings s and t is a configuration where s and t are divided into n and m "
    "substrings respectively, such that:\n"
    "  s = s1 + s2 + ... + sn\n"
    "  t = t1 + t2 + ... + tm\n"
    "  |n - m| <= 1\n"
    "  The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...\n"
    "Note: a + b is the concatenation of strings a and b.\n"
    "Constraint: 0 <= s1.length, s2.length <= 100; s3.length == s1.length + s2.length."
)

SOL1_CODE = '''\
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    # dp[i][j] = can s3[:i+j] be formed by interleaving s1[:i] and s2[:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True  # empty strings -> empty s3 is trivially valid

    # Fill first column: only using s1
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]

    # Fill first row: only using s2
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]

    # Fill rest of table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Take from s1: prior state was dp[i-1][j], s1[i-1] must match s3[i+j-1]
            from_s1 = dp[i-1][j] and s1[i-1] == s3[i+j-1]
            # Take from s2: prior state was dp[i][j-1], s2[j-1] must match s3[i+j-1]
            from_s2 = dp[i][j-1] and s2[j-1] == s3[i+j-1]
            dp[i][j] = from_s1 or from_s2

    return dp[m][n]
'''

SOL1_LINE_BY_LINE = [
    ("m, n = len(s1), len(s2)", "Cache string lengths to use throughout DP."),
    ("if m + n != len(s3): return False", "Quick sanity check — interleaving uses ALL characters of s1 and s2, so lengths must sum to len(s3)."),
    ("dp = [[False]*(n+1) for _ in range(m+1)]", "Allocate (m+1) × (n+1) boolean table. Extra row/col allow clean base-case indexing."),
    ("dp[0][0] = True", "Base case: empty s1 and empty s2 → empty s3. Trivially valid."),
    ("dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]", "First column: using only s1 characters. Valid if prior prefix was valid AND current s1 char matches s3 at same position."),
    ("dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]", "First row: using only s2 characters. Same logic as above, symmetric."),
    ("from_s1 = dp[i-1][j] and s1[i-1] == s3[i+j-1]", "Interior cell, option A: the i+j-th character of s3 was contributed by s1[i-1]. Only possible if dp[i-1][j] was valid."),
    ("from_s2 = dp[i][j-1] and s2[j-1] == s3[i+j-1]", "Interior cell, option B: the i+j-th character was contributed by s2[j-1]. Only possible if dp[i][j-1] was valid."),
    ("dp[i][j] = from_s1 or from_s2", "Cell is reachable if EITHER option works — take the logical OR."),
    ("return dp[m][n]", "Bottom-right corner = answer: can all of s1 and s2 form all of s3?"),
]

SOL2_CODE = '''\
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    # Space-optimised: only need current and previous row
    dp = [False] * (n + 1)
    dp[0] = True

    # Initialise first row (only using s2)
    for j in range(1, n + 1):
        dp[j] = dp[j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m + 1):
        # Update dp[0] for this row (only using s1)
        dp[0] = dp[0] and s1[i-1] == s3[i-1]
        for j in range(1, n + 1):
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
                    (dp[j-1] and s2[j-1] == s3[i+j-1])

    return dp[n]
'''

SOL2_LINE_BY_LINE = [
    ("dp = [False] * (n + 1)", "Single 1-D array of length n+1. We'll overwrite it row by row, so O(n) space total."),
    ("dp[0] = True", "Base case for first row (empty prefix of s1, empty prefix of s2 → empty s3 is valid)."),
    ("dp[j] = dp[j-1] and s2[j-1] == s3[j-1]", "Initialize first row: build j-character s3 using only the first j characters of s2."),
    ("dp[0] = dp[0] and s1[i-1] == s3[i-1]", "Update leftmost cell of current row: using only s1 up to index i-1."),
    ("dp[j] = (dp[j] and s1[i-1] == ...) or (dp[j-1] and s2[j-1] == ...)", "Compact rolling update. dp[j] now represents dp[i][j]. dp[j] (old) is dp[i-1][j]; dp[j-1] (just updated) is dp[i][j-1]."),
    ("return dp[n]", "Final answer lives at dp[n] after processing all m rows."),
]

SOL3_CODE = '''\
from functools import lru_cache

def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    @lru_cache(maxsize=None)
    def dp(i, j):
        """Can s3[:i+j] be formed by interleaving s1[:i] and s2[:j]?"""
        if i == 0 and j == 0:
            return True
        k = i + j  # index into s3
        option_s1 = (i > 0 and dp(i-1, j) and s1[i-1] == s3[k-1])
        option_s2 = (j > 0 and dp(i, j-1) and s2[j-1] == s3[k-1])
        return option_s1 or option_s2

    return dp(m, n)
'''

SOL3_LINE_BY_LINE = [
    ("@lru_cache(maxsize=None)", "Python's built-in memoization: the first time dp(i, j) is computed its result is cached; subsequent calls return the cached value in O(1)."),
    ("def dp(i, j)", "i = how many chars we've used from s1; j = from s2. Together they index position i+j in s3."),
    ("if i == 0 and j == 0: return True", "Base case: both strings exhausted → s3 is also exhausted → True."),
    ("k = i + j", "Current position in s3 (0-indexed: s3[k-1] is the character we need to match at this step)."),
    ("option_s1 = (i > 0 and dp(i-1, j) and s1[i-1] == s3[k-1])", "Try taking s1[i-1]: only valid if we have chars left in s1, the sub-problem dp(i-1, j) was feasible, AND the character matches."),
    ("option_s2 = (j > 0 and dp(i, j-1) and s2[j-1] == s3[k-1])", "Try taking s2[j-1]: symmetric check for s2."),
    ("return option_s1 or option_s2", "Valid if either choice works."),
    ("return dp(m, n)", "Ask: can we consume all of s1 (m chars) and all of s2 (n chars) to form s3?"),
]

COMPLEXITY_TABLE = [
    ["Solution", "Time", "Space"],
    ["2D Tabulation (Interview Pick)", "O(m × n)", "O(m × n)"],
    ["1-D Rolling Array", "O(m × n)", "O(n)"],
    ["Top-Down Memoization", "O(m × n)", "O(m × n) call stack + cache"],
]

RELATED = [
    ("Edit Distance", "Hard", "2D DP on two strings — classic LCS-family"),
    ("Longest Common Subsequence", "Medium", "Same 2D table structure, different recurrence"),
    ("Distinct Subsequences", "Hard", "2D DP counting ways to match a pattern in a string"),
    ("Regular Expression Matching", "Hard", "2D DP with wildcard transitions"),
    ("Wildcard Matching", "Hard", "2D DP; '?' and '*' instead of interleaving"),
    ("Shortest Common Supersequence", "Hard", "2D DP building merged string from two inputs"),
    ("Scramble String", "Hard", "DP on substrings of two strings with splits"),
    ("Longest Common Substring", "Medium", "2D DP — variant where subarray must be contiguous"),
]

RECURRENCE_CODE = """\
# Recurrence relation for Interleaving String
# dp[i][j] = True if s3[:i+j] can be formed by interleaving s1[:i] and s2[:j]

# Base cases:
dp[0][0] = True
dp[i][0] = dp[i-1][0] AND s1[i-1] == s3[i-1]   (use only s1)
dp[0][j] = dp[0][j-1] AND s2[j-1] == s3[j-1]   (use only s2)

# General recurrence:
dp[i][j] = (dp[i-1][j] AND s1[i-1] == s3[i+j-1])   # take from s1
          OR (dp[i][j-1] AND s2[j-1] == s3[i+j-1])  # take from s2

# Answer: dp[m][n]
"""

# ── Build blocks ─────────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: 2D Tabulation (Interview Pick) ────────────────────────────────
blocks += [
    N.h2("Solution 1 — 2D Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Forget 'interleaving' for a moment. Think of it as a decision at every character of s3: "
            "did this character come from s1 or from s2? We need to find ONE consistent assignment "
            "such that reading from s1 preserves its order and reading from s2 preserves its order."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A greedy approach fails: if s3[k] matches both s1[i] and s2[j], we don't know which "
            "to consume without looking ahead. Backtracking explores every branch in O(2^(m+n)) time — "
            "far too slow for strings of length 100."
        ),
        N.h4("The Key Observation"),
        N.para(
            "At any point in building s3, the state is fully described by (i, j): how many characters "
            "we've used from s1 and s2 respectively. Given (i, j), the position in s3 is always i+j "
            "(deterministic). So there are only (m+1)*(n+1) distinct states — perfect for DP."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp[i][j] = True if s3[:i+j] can be formed by interleaving s1[:i] and s2[:j].\n"
            "Base: dp[0][0] = True.\n"
            "Transition: dp[i][j] is True if either:\n"
            "  (A) dp[i-1][j] was True AND s1[i-1] == s3[i+j-1]  (take from s1)\n"
            "  (B) dp[i][j-1] was True AND s2[j-1] == s3[i+j-1]  (take from s2)\n"
            "Fill row by row. Answer is dp[m][n]."
        ),
        N.callout(
            "Analogy: Think of two queues at a coffee shop merging into one line. "
            "dp[i][j] asks: is there a valid merge of the first i people from queue-1 "
            "and first j people from queue-2 that matches the first i+j people in the "
            "combined line?",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Why Is This Dynamic Programming?"),
    N.para(
        "Optimal Substructure: if dp[i][j] is True, it relies on either dp[i-1][j] or dp[i][j-1] "
        "being True — subproblems directly feed the parent.\n"
        "Overlapping Subproblems: a naive recursive solution would recompute dp(i, j) from multiple "
        "paths (e.g., (i+1,j)→(i,j) and (i,j+1)→(i,j)). Memoization or tabulation saves each state once."
    ),
    N.code(RECURRENCE_CODE, lang="python"),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
]
for line, explanation in SOL1_LINE_BY_LINE:
    blocks.append(N.para(N.rich([(line, {"code": True}), f" — {explanation}"])))
blocks.append(N.divider())

# ── Solution 2: 1-D Rolling Array ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — 1-D Rolling Array (Space-Optimised)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "In Solution 1, computing row i only needs row i-1. We never go back further. "
            "So we can collapse the (m+1)×(n+1) table into a single array of length n+1, "
            "overwriting it row by row."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naively reusing the same 1D array bottom-to-top can overwrite values we still need "
            "on the same pass. The key is that dp[j] (old) plays the role of dp[i-1][j], "
            "and dp[j-1] (already updated in the current pass) plays dp[i][j-1]. "
            "This happens to work left-to-right."
        ),
        N.h4("The Key Observation"),
        N.para(
            "When we update dp[j] in-place left-to-right:\n"
            "  dp[j] (before update) = dp[i-1][j]  (from previous row)\n"
            "  dp[j-1] (just updated) = dp[i][j-1]  (from current row)\n"
            "So the standard 2D update can be written directly over the 1-D array!"
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialise dp of length n+1 using only s2 (first row of 2D table). "
            "Then iterate over each row i of s1, updating dp[0] first (using only s1), "
            "then updating dp[j] for j from 1 to n using the compact recurrence."
        ),
        N.callout(
            "Space trick: same technique used in 0/1 Knapsack, Edit Distance, and LCS — "
            "whenever the 2D recurrence only looks left and up, a rolling 1D array suffices.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
]
for line, explanation in SOL2_LINE_BY_LINE:
    blocks.append(N.para(N.rich([(line, {"code": True}), f" — {explanation}"])))
blocks.append(N.divider())

# ── Solution 3: Top-Down Memoization ────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Top-Down Memoization (Recursive + Cache)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Start from the recursive formulation: 'Can I form s3[:i+j] using s1[:i] and s2[:j]?' "
            "This maps directly to dp(i, j). Call it from dp(m, n) and recurse down."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion (without cache) is exponential — each call branches into two sub-calls, "
            "leading to O(2^(m+n)) total calls with massive repeated computation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "There are only (m+1)*(n+1) unique (i, j) pairs. Adding @lru_cache means each pair "
            "is computed at most once, giving O(m*n) total work — same as tabulation."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Write the recursive function dp(i, j) with the natural base case and recurrence. "
            "Decorate with @lru_cache. Call dp(m, n). Python handles the rest."
        ),
        N.callout(
            "Interview tip: Top-down is easier to derive in a whiteboard setting because it "
            "mirrors the problem definition. Convert to bottom-up only if the interviewer asks "
            "for space optimisation.",
            "🎤", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE),
    N.h3("Line by Line"),
]
for line, explanation in SOL3_LINE_BY_LINE:
    blocks.append(N.para(N.rich([(line, {"code": True}), f" — {explanation}"])))
blocks.append(N.divider())

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table(COMPLEXITY_TABLE),
    N.para(
        "All three approaches share O(m × n) time because there are exactly (m+1)(n+1) states "
        "and each is computed in O(1). The rolling-array solution reduces space from O(m × n) "
        "to O(n) by keeping only two logical rows at a time."
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "2D DP on Both Strings, LCS-Style DP"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks whether/how string s3 can be assembled from two source strings s1, s2 "
        "while preserving order in each.\n"
        "• State = (i, j): characters consumed from each source, position in target is i+j.\n"
        "• Any 'merge two sequences with ordering constraints' problem.\n"
        "• Table dimensions = lengths of the two input strings (2D DP on both strings).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related 2D DP on two strings technique:"),
]
for name, diff, note in RELATED:
    blocks.append(N.bullet(N.rich([(name, {"bold": True}), f" ({diff}) — {note}"])))
blocks += [
    N.para("These problems share the same core technique: filling a 2D DP table where each cell "
           "depends on the cells directly above it (taking from one string) or to its left "
           "(taking from the other string)."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — "
        "Section 18: Dynamic Programming → 18.3 DP on Strings (LCS family)",
        "📚", "gray_background"
    ),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("interleaving_string")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append ────────────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
