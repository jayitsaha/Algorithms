"""
gen_edit_distance.py — Notion page builder for Edit Distance (LC 72)
DP problem: Insert/Delete/Replace (LCS-family, 2D tabulation + memoization)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-810a-9dd7-c39f1a362956"

# ── 1) Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=72,
    pattern="Dynamic Programming",
    subpatterns=["DP: LCS"],
    tc="O(m × n)",
    sc="O(m × n)",
    key_insight="dp[i][j] = min edits to convert word1[:i] to word2[:j]; each cell depends on the cell above, left, and diagonal.",
    icon="🟡"
)

# ── 2) Wipe old content ───────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"  Wiped {wiped} blocks")

# ── 3) Build body ─────────────────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("word1", {"code": True}),
        (" and ", {}),
        ("word2", {"code": True}),
        (", return the minimum number of operations required to convert ", {}),
        ("word1", {"code": True}),
        (" to ", {}),
        ("word2", {"code": True}),
        (". You have three operations available: insert a character, delete a character, "
         "or replace a character.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ('word1 = "horse", word2 = "ros" → 3 operations\n'
             'horse → rorse (replace h with r)\nrorse → rose (delete r)\nrose → ros (delete e)', {}),
        ]),
        "📝", "gray_background"
    ),
    N.divider(),
]

# ── SOLUTION 1: Bottom-Up DP (Tabulation) — Interview Pick ───────────────────
TABULATION_CODE = '''\
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[i][j] = min edits to convert word1[:i] -> word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i          # delete all i chars from word1
    for j in range(n + 1):
        dp[0][j] = j          # insert all j chars of word2

    # Fill table row by row
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                # Characters match — no operation needed
                dp[i][j] = dp[i-1][j-1]
            else:
                # Take the cheapest of the three operations
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete from word1
                    dp[i][j-1],    # insert into word1
                    dp[i-1][j-1],  # replace in word1
                )

    return dp[m][n]
'''

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the minimum number of single-character edits (insert, delete, replace) "
            "to turn one string into another. Think of it as two fingers crawling along the two "
            "strings simultaneously: at each position, decide the cheapest action."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy doesn't work — locally cheap moves can be globally expensive. "
            "Brute-force recursion without memoization is O(3^(m+n)) because every character "
            "position branches into 3 choices."
        ),
        N.h4("The Key Observation"),
        N.para(
            "If we know the minimum edits for every pair of prefixes "
            "(word1[:i], word2[:j]) we can build the answer for longer prefixes in O(1). "
            "Specifically:\n"
            "• If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]  (free — no edit)\n"
            "• Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n"
            "  — dp[i-1][j]: delete word1[i-1]\n"
            "  — dp[i][j-1]: insert word2[j-1] into word1\n"
            "  — dp[i-1][j-1]: replace word1[i-1] with word2[j-1]"
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Create a (m+1) × (n+1) table. Row 0 = 'insert j chars', Col 0 = 'delete i chars'.\n"
            "2. Fill left-to-right, top-to-bottom.\n"
            "3. Each cell looks diagonally up-left (replace), up (delete), left (insert).\n"
            "4. Answer is in dp[m][n]."
        ),
        N.callout(
            "Analogy: Imagine two rulers sliding along the strings. At each intersection, "
            "you check: do the current characters match (free!), or pick the cheapest of "
            "delete/insert/replace from the three neighboring cells.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Wagner-Fischer Algorithm"),
    N.para(
        "Edit Distance is solved by the Wagner-Fischer algorithm (1974). "
        "It fills a 2D DP table where dp[i][j] = Levenshtein distance between "
        "the first i characters of word1 and the first j characters of word2.\n\n"
        "Core invariant: dp[i][j] holds the EXACT minimum edit distance for the "
        "pair of prefixes (word1[:i], word2[:j]). Because we fill row-by-row, "
        "every cell only references already-computed cells.\n\n"
        "Why it works: The three cases cover ALL ways to align the strings at "
        "position (i, j). There is no 4th case — every alignment either uses the "
        "last character of both strings (match/replace) or discards the last char "
        "of one string (delete/insert).\n\n"
        "Recognized when: 'minimum operations to transform string A to string B' "
        "with insert/delete/replace. Classic NLP metric (spell checking, diff tools, DNA alignment)."
    ),
    N.h3("Code"),
    N.code(TABULATION_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("m, n = len(word1), len(word2)", {"code": True}),
                   (" — capture both lengths; table dimensions are (m+1) × (n+1).", {})])),
    N.para(N.rich([("dp = [[0] * (n + 1) for _ in range(m + 1)]", {"code": True}),
                   (" — allocate (m+1) rows x (n+1) cols. The +1 accounts for the empty-prefix base cases.", {})])),
    N.para(N.rich([("for i in range(m + 1): dp[i][0] = i", {"code": True}),
                   (" — to convert word1[:i] to '' we must delete i characters.", {})])),
    N.para(N.rich([("for j in range(n + 1): dp[0][j] = j", {"code": True}),
                   (" — to convert '' to word2[:j] we must insert j characters.", {})])),
    N.para(N.rich([("for i in range(1, m + 1): for j in range(1, n + 1):", {"code": True}),
                   (" — nested loop fills the table in dependency order (top-left → bottom-right).", {})])),
    N.para(N.rich([("if word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]", {"code": True}),
                   (" — characters already match; inherit cost from diagonal (no operation needed).", {})])),
    N.para(N.rich([("dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])", {"code": True}),
                   (" — characters differ; add 1 for the operation, then take the minimum "
                    "of delete (row above), insert (cell left), replace (diagonal).", {})])),
    N.para(N.rich([("return dp[m][n]", {"code": True}),
                   (" — bottom-right corner holds the answer for the full strings.", {})])),
    N.divider(),
]

# ── SOLUTION 2: Top-Down DP (Memoization) ────────────────────────────────────
MEMO_CODE = '''\
from functools import lru_cache

def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    @lru_cache(maxsize=None)
    def dp(i, j):
        # Base cases: one string exhausted
        if i == 0: return j   # insert remaining j chars
        if j == 0: return i   # delete remaining i chars

        if word1[i-1] == word2[j-1]:
            return dp(i-1, j-1)   # characters match — free

        return 1 + min(
            dp(i-1, j),    # delete word1[i-1]
            dp(i, j-1),    # insert word2[j-1]
            dp(i-1, j-1),  # replace word1[i-1]
        )

    return dp(m, n)
'''

blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Write the recurrence as a recursive function dp(i, j) = min edits to "
            "align word1[:i] with word2[:j]. Call it from (m, n) and let it recurse. "
            "Cache results so each (i, j) pair is computed only once."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion (no cache) revisits the same (i, j) subproblems "
            "exponentially. The same (i, j) pair appears many times in the recursion tree."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The memoization approach is identical in logic to tabulation — same "
            "recurrence, same complexity — but we derive it top-down from the full "
            "problem. Python's @lru_cache handles the cache automatically."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Define dp(i, j) recursively.\n"
            "2. Base cases: dp(0, j) = j (insert), dp(i, 0) = i (delete).\n"
            "3. If characters match, return dp(i-1, j-1).\n"
            "4. Else return 1 + min(three recursive calls).\n"
            "5. @lru_cache memoizes automatically — no explicit table needed."
        ),
        N.callout(
            "Trade-off: Memoization is easier to derive (write what you mean), "
            "but tabulation avoids Python recursion depth limits and is slightly faster "
            "due to no call-stack overhead. For interviews, either is acceptable.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — Python decorator that memoizes the inner function. "
                    "Caches all (i, j) calls automatically.", {})])),
    N.para(N.rich([("if i == 0: return j", {"code": True}),
                   (" — word1 is exhausted; need j insertions to produce word2[:j].", {})])),
    N.para(N.rich([("if j == 0: return i", {"code": True}),
                   (" — word2 is exhausted; need i deletions to empty word1[:i].", {})])),
    N.para(N.rich([("if word1[i-1] == word2[j-1]: return dp(i-1, j-1)", {"code": True}),
                   (" — last characters match; no operation needed, recurse on smaller prefixes.", {})])),
    N.para(N.rich([("return 1 + min(dp(i-1,j), dp(i,j-1), dp(i-1,j-1))", {"code": True}),
                   (" — same three-way min as tabulation: delete / insert / replace.", {})])),
    N.para(N.rich([("return dp(m, n)", {"code": True}),
                   (" — kick off recursion from the full problem; cache fills in lazily.", {})])),
    N.divider(),
]

# ── SOLUTION 3: Space-Optimized (O(n) space) ──────────────────────────────────
SPACE_OPT_CODE = '''\
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # Only keep two rows: previous and current
    prev = list(range(n + 1))   # base case: dp[0][j] = j

    for i in range(1, m + 1):
        curr = [i] + [0] * n    # base case: dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]          # diagonal
            else:
                curr[j] = 1 + min(
                    prev[j],    # delete  (row above)
                    curr[j-1],  # insert  (cell left, already computed)
                    prev[j-1],  # replace (diagonal)
                )
        prev = curr

    return prev[n]
'''

blocks += [
    N.h2("Solution 3 — Space-Optimised (Rolling Array)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Row i of the DP table only depends on row i-1 (and the cell to the left). "
            "We can throw away older rows and keep just two: 'previous' and 'current'."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Each cell dp[i][j] looks at dp[i-1][j] (one row up), dp[i][j-1] (same row, "
            "already computed), and dp[i-1][j-1] (diagonal, save before overwriting). "
            "Two 1D arrays of size n+1 replace the full (m+1)×(n+1) matrix."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize prev = [0, 1, 2, ..., n] (the base-case first row).\n"
            "2. For each row i, build curr starting with curr[0] = i.\n"
            "3. Fill curr[j] using prev[j-1] (diagonal), prev[j] (delete), curr[j-1] (insert).\n"
            "4. After each row, set prev = curr."
        ),
        N.callout(
            "Space drops from O(m × n) to O(n). Time stays O(m × n). "
            "In interviews, mention this optimization after presenting the standard 2D solution.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SPACE_OPT_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("prev = list(range(n + 1))", {"code": True}),
                   (" — first row of the DP table: converting '' to word2[:j] costs j insertions.", {})])),
    N.para(N.rich([("curr = [i] + [0] * n", {"code": True}),
                   (" — start of row i: converting word1[:i] to '' costs i deletions.", {})])),
    N.para(N.rich([("curr[j] = prev[j-1]", {"code": True}),
                   (" — match: inherit diagonal value (prev[j-1] was dp[i-1][j-1]).", {})])),
    N.para(N.rich([("1 + min(prev[j], curr[j-1], prev[j-1])", {"code": True}),
                   (" — delete uses prev[j] (above), insert uses curr[j-1] (left), "
                    "replace uses prev[j-1] (diagonal).", {})])),
    N.para(N.rich([("prev = curr", {"code": True}),
                   (" — discard the old row; the current row becomes 'previous' for next iteration.", {})])),
    N.para(N.rich([("return prev[n]", {"code": True}),
                   (" — after processing all rows, prev holds the last row and prev[n] = dp[m][n].", {})])),
    N.divider(),
]

# ── WHY IS THIS DP? ───────────────────────────────────────────────────────────
RECURRENCE = """\
dp[i][j] = 0                                   if i == 0 and j == 0
         = j                                   if i == 0
         = i                                   if j == 0
         = dp[i-1][j-1]                        if word1[i-1] == word2[j-1]
         = 1 + min(dp[i-1][j],                 # delete
                   dp[i][j-1],                 # insert
                   dp[i-1][j-1])               # replace    otherwise
"""

blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(
        "Edit Distance has both hallmarks of DP:"
    ),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The minimum edits for (word1[:i], word2[:j]) is determined by "
         "minimum edits for its sub-problems (smaller prefixes). We combine "
         "sub-problem solutions optimally via the 3-way min.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive solution recomputes dp(i-1, j-1) many times — "
         "once from dp(i, j) directly, but also via dp(i-1, j) and dp(i, j-1). "
         "Memoization/tabulation eliminates this repetition.", {}),
    ])),
    N.h3("Recurrence Relations"),
    N.code(RECURRENCE, lang="plain text"),
    N.callout(
        N.rich([
            ("Key insight: ", {"bold": True}),
            ("The diagonal cell dp[i-1][j-1] corresponds to 'replace'. "
             "If characters match, it's a FREE move (0 cost). "
             "The up cell dp[i-1][j] = delete word1's char. "
             "The left cell dp[i][j-1] = insert word2's char into word1.", {}),
        ]),
        "🔐", "blue_background"
    ),
    N.divider(),
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Bottom-Up Tabulation (Interview Pick)", "O(m × n)", "O(m × n)"],
        ["Top-Down Memoization", "O(m × n)", "O(m × n) + O(m+n) recursion stack"],
        ["Space-Optimised (Rolling Array)", "O(m × n)", "O(n)"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP: LCS (2D string DP, prefix pairs)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Minimum operations to transform string A to string B'\n"
        "• Operations involve insert / delete / replace on characters\n"
        "• Two strings → think 2D DP table over prefix pairs\n"
        "• 'Levenshtein distance' or 'edit distance' in the problem statement\n"
        "• Related: Longest Common Subsequence shares the same 2D prefix-pair structure",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Sub-pattern verified: ", {"bold": True}),
        ("Guide Section 18 (Dynamic Programming) — DP: LCS family. "
         "Edit Distance is a classic extension of LCS where the LCS table becomes "
         "an edit-cost table.", {}),
    ])),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 2D string DP / LCS technique:"),
    N.bullet(N.rich([
        ("Longest Common Subsequence", {"bold": True}),
        (" (Medium) — same 2D table; dp[i][j] = LCS length instead of edit cost", {}),
    ])),
    N.bullet(N.rich([
        ("Delete Operation for Two Strings", {"bold": True}),
        (" (Medium) — min deletions = m + n - 2 * LCS(word1, word2); edit distance variant", {}),
    ])),
    N.bullet(N.rich([
        ("Minimum ASCII Delete Sum for Two Strings", {"bold": True}),
        (" (Medium) — weighted delete variant; same table, sum ASCII values instead of count", {}),
    ])),
    N.bullet(N.rich([
        ("One Edit Distance", {"bold": True}),
        (" (Medium) — check if exactly 1 edit apart; greedy on differing character", {}),
    ])),
    N.bullet(N.rich([
        ("Shortest Common Supersequence", {"bold": True}),
        (" (Hard) — build string containing both; reconstruct path through same DP table", {}),
    ])),
    N.bullet(N.rich([
        ("Distinct Subsequences", {"bold": True}),
        (" (Hard) — count ways word2 appears as subseq of word1; 2D DP over prefix pairs", {}),
    ])),
    N.bullet(N.rich([
        ("Interleaving String", {"bold": True}),
        (" (Medium) — 2D DP over two strings; dp[i][j] = can word1[:i] + word2[:j] form s[:i+j]", {}),
    ])),
    N.bullet(N.rich([
        ("Wildcard Matching / Regular Expression Matching", {"bold": True}),
        (" (Hard) — 2D DP matching pattern against string; similar cell-fill structure", {}),
    ])),
    N.para(
        "These problems share the core technique: define dp[i][j] over prefix pairs of two "
        "strings and fill a 2D table using a recurrence that looks at the current characters "
        "and previously computed sub-problems."
    ),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — Dynamic Programming", "📚", "gray_background"),
    N.divider(),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("edit_distance")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
