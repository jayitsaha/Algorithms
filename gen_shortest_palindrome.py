"""
gen_shortest_palindrome.py
Regenerate the Notion page for Shortest Palindrome (LeetCode #214, Hard).
notion_page_id is null → create a new page, then set properties and build body.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "shortest_palindrome"
NAME = "Shortest Palindrome"
NUMBER = 214
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "String Processing"
SUBPATTERNS = ["KMP on s + # + reverse(s)"]
TC = "O(n)"
SC = "O(n)"
KEY_INSIGHT = "Build t = s + '#' + rev(s); KMP lps[-1] gives the longest palindromic prefix length."

# ── Step 0: Create page (page_id is null) ──
print("Creating new Notion page...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON
)
print("Properties set.")

# ── Step 2: Wipe existing body (fresh page, likely empty, but safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", you can convert it to a palindrome by adding characters in front of it. "
         "Find and return the shortest palindrome you can find by performing this transformation.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "aacecaaa" → "aaacecaaa" (prepend "a")', {}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "abcd" → "dcbabcd" (prepend "dcb")', {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("0 ≤ s.length ≤ 50,000, s consists of lowercase English letters only.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: KMP (Optimal, Interview Pick) ──
blocks += [
    N.h2("Solution 1 — KMP on s + '#' + reverse(s)  (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We can only add characters to the front of s. Adding the minimum number of "
            "characters means keeping as much of s unchanged as possible. The key observation: "
            "if the beginning of s is already a palindrome, we don't need to touch it. "
            "We only need to mirror the part of s that isn't part of a palindromic prefix."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naive approach: try every prefix from longest to shortest, check if it is a "
            "palindrome. Each palindrome check is O(n), and we try O(n) prefixes → O(n²) total. "
            "For s of length 50,000 this is 2.5 billion operations — TLE."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A prefix of s of length k is a palindrome if and only if s[0..k-1] == rev(s)[-k:]. "
            "In other words, s's prefix of length k must match the last k characters of rev(s). "
            "Finding the LONGEST such k is a 'longest prefix that is also a suffix' question — "
            "exactly what KMP's failure function (LPS array) solves in O(n)!"
        ),
        N.h4("Building the Solution"),
        N.para(
            "Concatenate t = s + '#' + rev(s). The '#' sentinel prevents any prefix match from "
            "extending beyond the boundary between s and rev(s). "
            "Compute the KMP failure function (LPS array) on t. "
            "The last value, lps[-1], is the length of the longest palindromic prefix of s. "
            "The answer is: rev(s[lps[-1]:]) + s. We reverse only the non-palindromic tail and prepend it."
        ),
        N.callout(
            "Analogy: Imagine s is a sentence. You want to find the longest starting portion "
            "that reads the same forwards and backwards (a palindromic prefix). "
            "KMP acts like a smart scanner that finds this match in a single linear pass "
            "by building and reusing a 'self-similarity table' for the combined string.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: KMP Failure Function"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Knuth-Morris-Pratt algorithm (1977). Designed for O(n+m) exact pattern search. "
         "Its core structure, the failure function (also called the LPS or prefix-suffix table), "
         "captures self-similarity: for each position i, lps[i] = the length of the longest "
         "proper prefix of the first (i+1) characters that is also a suffix.", {}),
    ])),
    N.code(
        "# KMP Failure Function template\n"
        "def kmp_failure(t: str) -> list[int]:\n"
        "    n = len(t)\n"
        "    lps = [0] * n          # lps[0] always 0\n"
        "    j = 0                  # length of previous longest prefix-suffix\n"
        "    for i in range(1, n):\n"
        "        while j > 0 and t[i] != t[j]:\n"
        "            j = lps[j - 1] # fall back using lps itself — O(n) amortized!\n"
        "        if t[i] == t[j]:\n"
        "            j += 1\n"
        "        lps[i] = j\n"
        "    return lps"
    ),
    N.para(
        "Core Invariant: j always equals the length of the longest proper prefix of t[0..i-1] "
        "that is also a suffix. The fallback step j = lps[j-1] is the genius: when a mismatch "
        "occurs, we don't restart from zero — we reuse the already-computed overlap. "
        "This gives amortized O(n): j can increase at most n times total, so fallbacks are "
        "also bounded by n."
    ),
    N.para(N.rich([
        ("Why t = s + '#' + rev(s) works for palindromes: ", {"bold": True}),
        ("A palindromic prefix of s of length k satisfies s[0..k-1] == s[0..k-1] reversed. "
         "Reversed, that's exactly the last k characters of rev(s). So s[0..k-1] appears as "
         "both the prefix of t (from the s part) and a suffix of t (from the rev(s) part). "
         "That is precisely what lps measures. The '#' separator ensures no match longer than "
         "len(s) is possible.", {}),
    ])),
    N.para(N.rich([
        ("When to recognize KMP: ", {"bold": True}),
        ('Pattern search in text, "longest prefix = suffix" questions, minimum string period, '
         "shortest palindrome by prepending — any time O(n²) prefix-suffix matching is too slow.", {}),
    ])),
    N.h3("Code"),
    N.code(
        "def shortestPalindrome(s: str) -> str:\n"
        "    if not s:\n"
        "        return s\n"
        "    rev = s[::-1]\n"
        "    t = s + '#' + rev\n"
        "    n = len(t)\n"
        "    lps = [0] * n\n"
        "    j = 0\n"
        "    for i in range(1, n):\n"
        "        while j > 0 and t[i] != t[j]:\n"
        "            j = lps[j - 1]\n"
        "        if t[i] == t[j]:\n"
        "            j += 1\n"
        "        lps[i] = j\n"
        "    longest_pal_prefix = lps[-1]\n"
        "    suffix = s[longest_pal_prefix:]\n"
        "    return suffix[::-1] + s"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not s: return s", {"code": True}), " — edge case guard: empty string is already a palindrome."])),
    N.para(N.rich([("rev = s[::-1]", {"code": True}), " — compute the full reverse of s in O(n)."])),
    N.para(N.rich([("t = s + '#' + rev", {"code": True}), " — combine into one string with the sentinel separator."])),
    N.para(N.rich([("lps = [0] * n", {"code": True}), " — initialize the failure function array; lps[0] is always 0."])),
    N.para(N.rich([("j = 0", {"code": True}), " — j tracks the length of the current matching prefix-suffix."])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), " — i scans forward through t; i=0 is already handled (lps[0]=0)."])),
    N.para(N.rich([("while j > 0 and t[i] != t[j]: j = lps[j-1]", {"code": True}),
                   " — mismatch: fall back to the previous longest matching prefix. This is the KMP 'no backtracking' step."])),
    N.para(N.rich([("if t[i] == t[j]: j += 1", {"code": True}), " — match: extend the prefix-suffix by one character."])),
    N.para(N.rich([("lps[i] = j", {"code": True}), " — record the current prefix-suffix length at position i."])),
    N.para(N.rich([("longest_pal_prefix = lps[-1]", {"code": True}),
                   " — the last lps value gives the length of s's longest palindromic prefix."])),
    N.para(N.rich([("suffix = s[longest_pal_prefix:]", {"code": True}),
                   " — the portion of s beyond the palindromic prefix; these characters must be mirrored."])),
    N.para(N.rich([("return suffix[::-1] + s", {"code": True}),
                   " — prepend the reversed suffix: the minimum characters needed to make s a palindrome."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Try every possible palindromic prefix of s starting from the longest. "
            "Once we find one, the answer is built by prepending the reverse of the remaining suffix."
        ),
        N.h4("What Doesn't Work at Scale"),
        N.para(
            "For each of n positions i (from n down to 0), we check if s[:i] is a palindrome "
            "in O(n). Total: O(n²). This passes for small inputs but is too slow for n=50,000."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We iterate from longest prefix to shortest, so the first palindromic prefix we find "
            "is the longest one. This guarantees minimum characters added."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Loop i from len(s) down to 0. If s[:i] is a palindrome, return reverse(s[i:]) + s. "
            "Worst case i=1 (just the first character 'a' is always a palindrome), so we always find an answer."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def shortestPalindrome(s: str) -> str:\n"
        "    def is_palindrome(t: str) -> bool:\n"
        "        return t == t[::-1]\n"
        "    for i in range(len(s), -1, -1):\n"
        "        if is_palindrome(s[:i]):\n"
        "            return s[i:][::-1] + s\n"
        "    return s  # never reached"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def is_palindrome(t)", {"code": True}), " — helper that checks t == reverse(t) in O(n)."])),
    N.para(N.rich([("for i in range(len(s), -1, -1):", {"code": True}), " — try prefixes from longest to shortest."])),
    N.para(N.rich([("if is_palindrome(s[:i]):", {"code": True}), " — O(n) palindrome check on prefix of length i."])),
    N.para(N.rich([("return s[i:][::-1] + s", {"code": True}), " — found longest palindromic prefix; prepend reverse of remaining suffix."])),
    N.divider(),
]

# ── Solution 3: Rolling Hash ──
blocks += [
    N.h2("Solution 3 — Rabin-Karp Rolling Hash O(n) expected"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of KMP, use polynomial rolling hashes to check 'is s[0..i] a palindrome?' "
            "in O(1) per position. Maintain a forward hash and a backward hash simultaneously."
        ),
        N.h4("The Key Observation"),
        N.para(
            "s[0..i] is a palindrome iff its forward hash equals its backward hash. "
            "We can update both in O(1) per character using polynomial rolling hash math."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Scan s left-to-right. Maintain fwd = polynomial hash of s[0..i]. "
            "Maintain rev_h = polynomial hash of s[0..i] reversed. "
            "When fwd == rev_h, record i+1 as the palindromic prefix length. "
            "After scanning, prepend reverse(s[best:]) to s."
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def shortestPalindrome(s: str) -> str:\n"
        "    base, mod = 26, 10**9 + 7\n"
        "    fwd = rev_h = 0\n"
        "    power = 1\n"
        "    best = 0\n"
        "    for i, c in enumerate(s):\n"
        "        val = ord(c) - ord('a') + 1\n"
        "        fwd = (fwd * base + val) % mod\n"
        "        rev_h = (rev_h + val * power) % mod\n"
        "        power = power * base % mod\n"
        "        if fwd == rev_h:\n"
        "            best = i + 1\n"
        "    return s[best:][::-1] + s"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("fwd", {"code": True}), " — polynomial hash of s[0..i] computed left-to-right."])),
    N.para(N.rich([("rev_h", {"code": True}), " — polynomial hash treating s[0..i] as if read right-to-left (the reverse)."])),
    N.para(N.rich([("power", {"code": True}), " — base^i, used to place each new character at the most-significant position of rev_h."])),
    N.para(N.rich([("if fwd == rev_h:", {"code": True}), " — hashes match → s[0..i] is (very likely) a palindrome. Update best."])),
    N.para(N.rich([("return s[best:][::-1] + s", {"code": True}), " — same answer construction as other approaches."])),
    N.callout(
        "Hash collisions are theoretically possible. For production code, use double hashing "
        "(two different mod/base pairs) to reduce collision probability to near zero.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(n)"],
        ["KMP (Optimal) ✓", "O(n)", "O(n)"],
        ["Rabin-Karp Hash", "O(n) expected", "O(1) extra"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("String Processing", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("KMP on s + '#' + reverse(s)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Shortest/longest palindrome by adding characters to one end'\n"
        "• 'Find the longest palindromic prefix/suffix'\n"
        "• Any problem where you need prefix-of-A to equal suffix-of-B in O(n)\n"
        "• Named algorithm (KMP) signals this is a string-matching technique at its core",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("The sub-pattern 'KMP on s + # + reverse(s)' is a specific technique classified "
         "under KMP / Z-Algorithm in Section 2 of the DSA_Patterns_and_SubPatterns_Guide.md. "
         "The exact label 'KMP on s + # + reverse(s)' is a new classification specific "
         "to this palindrome-prefix reduction.", {"italic": True}),
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (KMP / prefix-suffix matching):"),
    N.bullet(N.rich([("Implement strStr (Needle in Haystack)", {"bold": True}), (" (Easy) — Classic KMP pattern search, same failure function. LeetCode #28.", {})])),
    N.bullet(N.rich([("Repeated Substring Pattern", {"bold": True}), (" (Easy) — KMP LPS detects if s can be formed by repeating a substring. LeetCode #459.", {})])),
    N.bullet(N.rich([("Longest Happy Prefix", {"bold": True}), (" (Hard) — Directly return the KMP failure function's longest prefix-suffix. LeetCode #1392.", {})])),
    N.bullet(N.rich([("Palindrome Pairs", {"bold": True}), (" (Hard) — Find all word pairs whose concatenation is a palindrome; uses reverse matching. LeetCode #336.", {})])),
    N.bullet(N.rich([("Shortest Palindrome (this problem)", {"bold": True}), (" (Hard) — Template: t = s + '#' + rev(s), run KMP, use lps[-1]. LeetCode #214.", {})])),
    N.bullet(N.rich([("Longest Palindromic Substring", {"bold": True}), (" (Medium) — Manacher's algorithm for O(n) palindrome detection in full string. LeetCode #5.", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Sliding window + frequency count; different sub-pattern but same String Processing main pattern. LeetCode #438.", {})])),
    N.para("These problems share the core technique: using KMP's self-similarity table to answer prefix-suffix questions in linear time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 2 (String Processing) → KMP / Z-Algorithm sub-pattern.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Explainer embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the KMP failure function computation — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
