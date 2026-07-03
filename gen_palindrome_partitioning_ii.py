"""
gen_palindrome_partitioning_ii.py
Notion in-place update for Palindrome Partitioning II (LeetCode #132, Hard)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d8-b409-fdabf746b43d"
SLUG    = "palindrome_partitioning_ii"

# ── 1) Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=132,
    pattern="Dynamic Programming",
    subpatterns=["Min Cuts + isPalindrome DP"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="Precompute isPal[i][j] in O(n²) by length; then dp[i]=min(dp[j-1]+1) for all j where isPal[j][i].",
    icon="🔴",
    status="Solved",
    source="LeetCode"
)
print("Properties set ✓")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks ✓")

# ── 3) Build body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string "), ("s", {"code": True}),
        (", partition "), ("s", {"code": True}),
        (" such that every substring of the partition is a palindrome. "
         "Return the minimum number of cuts needed for a palindrome partitioning of "), ("s", {"code": True}), (".")
    ])),
    N.para(N.rich([
        ("Example 1: "), ("s = \"aab\"", {"code": True}), (" → Output: "), ("1", {"code": True}),
        (" (partition: [\"aa\",\"b\"])")
    ])),
    N.para(N.rich([
        ("Example 2: "), ("s = \"a\"", {"code": True}), (" → Output: "), ("0", {"code": True}),
        (" (single char is already a palindrome)")
    ])),
    N.para(N.rich([
        ("Example 3: "), ("s = \"ab\"", {"code": True}), (" → Output: "), ("1", {"code": True}),
        (" (partition: [\"a\",\"b\"])")
    ])),
    N.divider(),
]

# ── Solution 1: Two-Pass DP (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Two-Pass DP: isPalindrome Table + MinCuts (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're asked for the minimum number of cuts to split a string into palindromic substrings. Think of it as: which index do we place the LAST cut? If the last cut is before position j, then s[j..i] must be a palindrome, and s[0..j-1] must already be optimally partitioned. This gives us a recurrence on prefixes."),

        N.h4("What Doesn't Work"),
        N.para("Brute force: try every way to split the string. For a string of length n, there are 2^(n-1) possible partitions — exponential. Even with early pruning (skip non-palindrome cuts), the recursion revisits the same prefixes many times."),

        N.h4("The Key Observation"),
        N.para("There are two overlapping sub-problems: (1) Is s[i..j] a palindrome? (2) What's the minimum cuts for s[0..k]? Each of these appears many times in a naive recursion. We can precompute (1) in an O(n²) isPal table filled by increasing substring length, then use those O(1) lookups to fill a dp[] array for (2). This separates the problem cleanly into two independent DP passes."),

        N.h4("Building the Solution"),
        N.para("Step 1: Build isPal[i][j] by increasing length. Base cases: length 1 → always True, length 2 → s[i]==s[j]. Longer: s[i]==s[j] AND isPal[i+1][j-1]. Step 2: dp[i] = min cuts for s[0..i]. If isPal[0][i]: dp[i]=0. Else: dp[i] = i (worst case), then try each j: if isPal[j][i], update dp[i] = min(dp[i], dp[j-1]+1). Return dp[n-1]."),

        N.callout(
            "Analogy: Think of cutting a ribbon into palindrome pieces. To find the minimum cuts for a ribbon of length i+1, consider each possible 'last cut'. If the piece from the cut to the end is a palindrome, we just need the minimum cuts for the remaining left piece (already computed). We pick the best last cut.",
            "🎗️", "blue_background"
        ),
    ]),
]

# Code
blocks += [
    N.h3("Code"),
    N.code("""\
def minCut(s: str) -> int:
    n = len(s)

    # Pass 1: Build isPal[i][j] — fill by increasing substring length
    isPal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:
                isPal[i][j] = True
            elif length == 2:
                isPal[i][j] = (s[i] == s[j])
            else:
                isPal[i][j] = (s[i] == s[j] and isPal[i + 1][j - 1])

    # Pass 2: Build dp[i] = min cuts for s[0..i]
    dp = [0] * n
    for i in range(n):
        if isPal[0][i]:
            dp[i] = 0           # entire prefix is a palindrome
        else:
            dp[i] = i           # worst case: i cuts
            for j in range(1, i + 1):
                if isPal[j][i]:
                    dp[i] = min(dp[i], dp[j - 1] + 1)

    return dp[n - 1]
"""),
]

# Line by line
blocks += [
    N.h3("Line by Line"),
    N.para(N.rich([("isPal = [[False]*n ...]", {"code": True}), (" — n×n boolean table, initialised False; we only write True entries.")])),
    N.para(N.rich([("for length in range(1, n+1)", {"code": True}), (" — Outer loop: iterate over all possible substring lengths 1, 2, 3, ..., n. This fill-order guarantees shorter substrings are computed before longer ones that depend on them.")])),
    N.para(N.rich([("j = i + length - 1", {"code": True}), (" — Compute end index from start index and length.")])),
    N.para(N.rich([("if length == 1: isPal[i][j] = True", {"code": True}), (" — A single character is always a palindrome — base case 1.")])),
    N.para(N.rich([("elif length == 2: isPal[i][j] = (s[i] == s[j])", {"code": True}), (" — A 2-char string is a palindrome iff both chars are equal — base case 2. No inner substring to check.")])),
    N.para(N.rich([("else: isPal[i][j] = (s[i]==s[j] and isPal[i+1][j-1])", {"code": True}), (" — For length ≥ 3: outer characters must match AND the inner substring must already be a palindrome. Because we fill by length, isPal[i+1][j-1] (shorter) is already computed.")])),
    N.para(N.rich([("if isPal[0][i]: dp[i] = 0", {"code": True}), (" — Early exit: if the entire prefix s[0..i] is a palindrome, zero cuts needed. Skip inner loop.")])),
    N.para(N.rich([("dp[i] = i", {"code": True}), (" — Worst-case initialization: for a prefix of length i+1, cutting every character requires exactly i cuts. This is the provable upper bound, tighter than float('inf').")])),
    N.para(N.rich([("for j in range(1, i+1)", {"code": True}), (" — Try every possible position for the 'last cut': j ranges from 1 (cut right after first char) to i (cut right before last char).")])),
    N.para(N.rich([("if isPal[j][i]:", {"code": True}), (" — If the last chunk s[j..i] is a palindrome (O(1) lookup from precomputed table), it's a valid last piece.")])),
    N.para(N.rich([("dp[i] = min(dp[i], dp[j-1] + 1)", {"code": True}), (" — Update: the left part s[0..j-1] needs dp[j-1] cuts (already optimal), plus 1 cut right before j. Take the minimum over all valid j.")])),
    N.para(N.rich([("return dp[n-1]", {"code": True}), (" — Return minimum cuts for the full string s[0..n-1].")])),
    N.divider(),
]

# ── Solution 2: Memoized Recursion ──
blocks += [
    N.h2("Solution 2 — Top-Down Memoized Recursion"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same recurrence as the bottom-up approach, but derived top-down: solve(i) = min cuts for s[0..i]. Base: if isPal[0][i] return 0. Recursive case: try each j, return best(solve(j-1) + 1)."),

        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization revisits the same solve(i) many times — once from every parent call. With memoization, each unique i is computed exactly once."),

        N.h4("The Key Observation"),
        N.para("lru_cache makes the top-down approach as efficient as bottom-up for time complexity (O(n²)), at the cost of recursion stack space. The isPal table is still precomputed first — the same optimization applies."),

        N.h4("Building the Solution"),
        N.para("Precompute isPal the same way. Then write a recursive function solve(i) decorated with @lru_cache. Within it: if isPal[0][i] return 0; otherwise iterate j and recurse solve(j-1)+1. Call solve(n-1)."),

        N.callout("Top-down is often easier to derive intuitively — start from the full problem, think recursively, add cache. Bottom-up is faster in practice (no recursion overhead). For interviews, derive top-down first, then offer to convert to bottom-up.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def minCut_memo(s: str) -> int:
    n = len(s)

    # Precompute isPal (same as Solution 1)
    isPal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:       isPal[i][j] = True
            elif length == 2:     isPal[i][j] = (s[i] == s[j])
            else:                 isPal[i][j] = (s[i] == s[j] and isPal[i+1][j-1])

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(i):
        # min cuts for s[0..i]
        if isPal[0][i]:
            return 0             # entire prefix is palindrome
        best = i                 # worst case
        for j in range(1, i + 1):
            if isPal[j][i]:
                best = min(best, solve(j - 1) + 1)
        return best

    return solve(n - 1)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Python's built-in memoization decorator. Each unique argument i is computed once and cached. Equivalent to a manual dict memo.")])),
    N.para(N.rich([("def solve(i):", {"code": True}), (" — Recursive function returning min cuts for prefix s[0..i].")])),
    N.para(N.rich([("if isPal[0][i]: return 0", {"code": True}), (" — Same early exit as bottom-up: full prefix is palindrome.")])),
    N.para(N.rich([("best = min(best, solve(j-1) + 1)", {"code": True}), (" — Recurse on the left subproblem. Because lru_cache memoizes, solve(j-1) is O(1) on repeated calls.")])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Recursion", "O(2ⁿ · n)", "O(n)", "Exponential — TLE on large inputs"],
        ["DP with inline palindrome check", "O(n³)", "O(n)", "Each palindrome check is O(n) inside O(n²) loops"],
        ["Two-Pass DP (isPal + dp) ✓ Interview Pick", "O(n²)", "O(n²)", "Precompute palindromes, then O(1) lookup in dp loop"],
        ["Top-Down Memoization", "O(n²)", "O(n²)", "Same complexity, recursion overhead, easier to derive"],
        ["Manacher's + 1D DP", "O(n²)", "O(n)", "Best space; Manacher's algorithm is harder to implement"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Min Cuts + isPalindrome DP — 1D min-cuts DP on string prefixes, with O(n²) palindrome precomputation table")])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Minimum cuts / partitions of a string where every piece satisfies property X' → DP on prefixes + precompute X\n"
        "• Palindrome checks inside a DP loop → precompute isPal table to avoid O(n³)\n"
        "• dp[i] depends on dp[j-1] plus checking s[j..i] → interval DP precomputation\n"
        "• Structurally analogous to Word Break: same dp[i] pattern, different valid-piece check",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DP Palindrome sub-pattern):"),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), (" (Medium, #131) — Same isPal precomputation; DFS + backtracking to return all valid partitions")])),
    N.bullet(N.rich([("Longest Palindromic Subsequence", {"bold": True}), (" (Medium, #516) — Interval DP: lps[i][j] = longest palindromic subsequence of s[i..j]")])),
    N.bullet(N.rich([("Longest Palindromic Substring", {"bold": True}), (" (Medium, #5) — Expand-around-center OR the same isPal table approach")])),
    N.bullet(N.rich([("Word Break", {"bold": True}), (" (Medium, #139) — Same dp[i] structure: try all valid last words ending at i; wordSet replaces isPal")])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), (" (Hard, #140) — Backtrack through dp choices to recover all valid sentences")])),
    N.bullet(N.rich([("Minimum Cost to Cut a Stick", {"bold": True}), (" (Hard, #1547) — Interval DP variant: minimize cost of cuts on a stick")])),
    N.para("These problems share the core technique: precompute answers to a helper subproblem (isPalindrome / wordSet membership), then use those O(1) answers in a prefix-length DP to minimize a count."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → DP Palindrome). Sub-Pattern: Min Cuts + isPalindrome DP. Source: Guide Section 18 + Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
