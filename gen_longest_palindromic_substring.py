"""
gen_longest_palindromic_substring.py
Update Notion page for LC #5 — Longest Palindromic Substring
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81a7-a10e-ed0c997175c4"

print(f"Updating Notion page {PAGE_ID} ...")

# ── 1) Properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=5,
    pattern="String Processing",
    subpatterns=["Expand Around Center", "Palindrome: Expand Around Center"],
    tc="O(n^2)",
    sc="O(1)",
    key_insight="Every palindrome has a center; expand outward from all 2n-1 centers tracking the best.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", return the longest palindromic substring in ", {}),
        ("s", {"code": True}),
        (". A palindrome reads the same forwards and backwards. "
         "If there are multiple answers of the same length, any one is acceptable.", {})
    ])),
    N.divider()
]

# ─── Solution 1: Expand Around Center ─────────────────────────────────
blocks += [
    N.h2("Solution 1 — Expand Around Center (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest contiguous substring that mirrors itself. "
               "The brute force checks all O(n^2) substrings and validates each in O(n) → O(n^3) total. "
               "Too slow for n=1000. We need to avoid re-validating already-checked symmetry."),
        N.h4("What Doesn't Work"),
        N.para("Brute force (try every start/end, check palindrome): O(n^3). "
               "Even O(n^2) DP works but uses O(n^2) space — a 1000×1000 boolean grid."),
        N.h4("The Key Observation"),
        N.para("Every palindrome grows outward from a center. "
               "A single character is always a valid center (odd-length palindromes). "
               "An adjacent pair of identical characters is an even-length center. "
               "There are exactly 2n−1 possible centers (n single chars + n−1 adjacent pairs). "
               "If we expand outward from each center while characters match, "
               "we discover all palindromes in O(n^2) time with O(1) space."),
        N.h4("Building the Solution"),
        N.para("1. Initialize best_start=0, best_len=1 (single char is always valid).\n"
               "2. Write expand(left, right): while in bounds AND s[left]==s[right], left--, right++.\n"
               "3. After the loop, left and right have overstepped by 1. "
               "Valid palindrome: s[left+1:right], length = right-left-1.\n"
               "4. For each index i, call expand(i, i) [odd] and expand(i, i+1) [even].\n"
               "5. Return s[best_start : best_start + best_len]."),
        N.callout(
            "Analogy: Imagine dropping a stone at each position in a pond. "
            "The ripples expand equally in both directions. "
            "We watch how far each ripple spreads before hitting an obstacle (mismatch).",
            "🧠", "blue_background")
    ]),
    N.h3("Code"),
    N.code(
        "def longestPalindrome(s: str) -> str:\n"
        "    if not s:\n"
        "        return \"\"\n"
        "    best_start, best_len = 0, 1\n"
        "\n"
        "    def expand(left, right):\n"
        "        nonlocal best_start, best_len\n"
        "        while left >= 0 and right < len(s) and s[left] == s[right]:\n"
        "            left -= 1\n"
        "            right += 1\n"
        "        # left and right overstepped by 1 each\n"
        "        length = right - left - 1\n"
        "        if length > best_len:\n"
        "            best_start = left + 1\n"
        "            best_len = length\n"
        "\n"
        "    for i in range(len(s)):\n"
        "        expand(i, i)      # odd-length: center at single char\n"
        "        expand(i, i + 1)  # even-length: center between two chars\n"
        "\n"
        "    return s[best_start : best_start + best_len]\n"
        "\n"
        "# Time: O(n^2) — n centers, each expanding up to n/2 steps\n"
        "# Space: O(1) — no DP table, just index variables"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not s: return \"\"", {"code": True}), " — edge case: empty string returns empty immediately."])),
    N.para(N.rich([("best_start, best_len = 0, 1", {"code": True}), " — any single character is a valid palindrome of length 1."])),
    N.para(N.rich([("def expand(left, right):", {"code": True}), " — inner helper; handles one center configuration (odd or even)."])),
    N.para(N.rich([("nonlocal best_start, best_len", {"code": True}), " — allows the helper to update variables in the outer scope."])),
    N.para(N.rich([("while left >= 0 and right < len(s) and s[left] == s[right]:", {"code": True}),
                   " — three conditions: stay in bounds left and right, and characters must match."])),
    N.para(N.rich([("left -= 1; right += 1", {"code": True}), " — expand the palindrome by one character in each direction."])),
    N.para(N.rich([("length = right - left - 1", {"code": True}),
                   " — critical: after loop exit, pointers overstepped by 1 each. Correct length is right - left - 1."])),
    N.para(N.rich([("best_start = left + 1", {"code": True}),
                   " — undo the final left-- overstep to get the true start index of the palindrome."])),
    N.para(N.rich([("expand(i, i)", {"code": True}), " — odd-length expansion: center is a single character at index i."])),
    N.para(N.rich([("expand(i, i + 1)", {"code": True}), " — even-length expansion: center gap is between i and i+1."])),
    N.para(N.rich([("return s[best_start : best_start + best_len]", {"code": True}), " — slice the winning palindrome from the string."])),
    N.divider()
]

# ─── Solution 2: DP Table ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Dynamic Programming (O(n^2) Space)"),
    N.toggle_h3("💡 Intuition: Why DP Works Here", [
        N.h4("Reframe the Problem"),
        N.para("Build a 2D boolean table: dp[i][j] = True if s[i..j] is a palindrome. "
               "A substring is a palindrome if its outer characters match AND the inner substring is also a palindrome."),
        N.h4("The Key Observation"),
        N.para("Recurrence: s[i..j] is a palindrome iff s[i] == s[j] AND dp[i+1][j-1] is True. "
               "Base cases: dp[i][i] = True (single chars) and dp[i][i+1] = (s[i] == s[i+1])."),
        N.h4("Building the Solution"),
        N.para("Fill the table by increasing substring length. For each length from 3 to n, "
               "try all starting positions. When we find dp[i][j]=True, check if it's the longest so far.")
    ]),
    N.h3("Code"),
    N.code(
        "def longestPalindrome(s: str) -> str:\n"
        "    n = len(s)\n"
        "    dp = [[False] * n for _ in range(n)]\n"
        "    start, max_len = 0, 1\n"
        "\n"
        "    # Base case: single characters\n"
        "    for i in range(n):\n"
        "        dp[i][i] = True\n"
        "\n"
        "    # Base case: adjacent pairs\n"
        "    for i in range(n - 1):\n"
        "        if s[i] == s[i + 1]:\n"
        "            dp[i][i + 1] = True\n"
        "            start, max_len = i, 2\n"
        "\n"
        "    # Fill by increasing length\n"
        "    for length in range(3, n + 1):\n"
        "        for i in range(n - length + 1):\n"
        "            j = i + length - 1\n"
        "            if s[i] == s[j] and dp[i + 1][j - 1]:\n"
        "                dp[i][j] = True\n"
        "                if length > max_len:\n"
        "                    start, max_len = i, length\n"
        "\n"
        "    return s[start : start + max_len]\n"
        "\n"
        "# Time: O(n^2), Space: O(n^2) — less preferred than expand approach"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [[False]*n for _ in range(n)]", {"code": True}), " — n×n boolean table; dp[i][j] = is s[i..j] a palindrome?"])),
    N.para(N.rich([("for i in range(n): dp[i][i] = True", {"code": True}), " — every single character is a palindrome."])),
    N.para(N.rich([("if s[i]==s[i+1]: dp[i][i+1]=True", {"code": True}), " — adjacent equal characters form a length-2 palindrome."])),
    N.para(N.rich([("if s[i]==s[j] and dp[i+1][j-1]:", {"code": True}), " — outer characters match AND inner substring is already known palindrome."])),
    N.divider()
]

# ─── Complexity table ──────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all substrings)", "O(n^3)", "O(1)"],
        ["DP Table", "O(n^2)", "O(n^2)"],
        ["Expand Around Center (Interview Pick)", "O(n^2)", "O(1)"],
        ["Manacher's Algorithm", "O(n)", "O(n)"],
    ]),
    N.divider()
]

# ─── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "String Processing"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Expand Around Center (Palindrome: Two Pointer — outward direction)"])),
    N.callout(
        "When to recognize this pattern: "
        "The problem asks for the longest/count of palindromic SUBSTRINGS (not subsequences). "
        "Two pointers that diverge outward (unlike the converging pattern for palindrome validation). "
        "O(1) space constraint favors expand over DP table.",
        "🔎", "green_background"),
    N.divider()
]

# ─── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Expand Around Center technique:"),
    N.bullet(N.rich([("Palindromic Substrings", {"bold": True}), " (Medium) — Count all palindromic substrings; same expand, count instead of track best. (#647)"])),
    N.bullet(N.rich([("Valid Palindrome", {"bold": True}), " (Easy) — Two pointers converging from both ends to verify palindrome. (#125)"])),
    N.bullet(N.rich([("Valid Palindrome II", {"bold": True}), " (Easy) — Allow at most one deletion; expand-based check after mismatch. (#680)"])),
    N.bullet(N.rich([("Longest Palindromic Subsequence", {"bold": True}), " (Medium) — Similar name but solved with DP/LCS, NOT expand. (#516)"])),
    N.bullet(N.rich([("Minimum Insertions to Make String Palindrome", {"bold": True}), " (Hard) — DP on palindrome structure. (#1312)"])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), " (Medium) — Backtracking with palindrome check subroutine. (#131)"])),
    N.para("These problems share the outward-expanding two-pointer pattern centered on a palindrome midpoint."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 2 (String Processing)\n"
              "Sub-Pattern: Palindrome: Expand Around Center", "📚", "gray_background"),
    N.divider()
]

# ─── Interactive Visual Explainer embed ────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_palindromic_substring")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the center pointer, left/right expansion, and best tracker update in real time.",
         {"italic": True, "color": "gray"})
    ]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
