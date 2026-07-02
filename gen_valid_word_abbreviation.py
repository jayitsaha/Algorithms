"""
gen_valid_word_abbreviation.py
Notion in-place update for LeetCode #408 Valid Word Abbreviation.
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8180-81b1-f7ef45e4e8ec"

# 1) Update page properties
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=408,
    pattern="Two Pointers",
    subpatterns=["Two Pointers with Skip"],
    tc="O(n+m)",
    sc="O(1)",
    key_insight="Two pointers: decode skip numbers from abbr and leap i forward; reject leading zeros; both must exhaust.",
    icon="🟢"
)
print("Properties set.")

# 2) Wipe the old content
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# 3) Rebuild the page body
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("word", {"code": True}),
        (" and an abbreviation string ", {}),
        ("abbr", {"code": True}),
        (", return ", {}),
        ("True", {"code": True}),
        (" if ", {}),
        ("abbr", {"code": True}),
        (" is a valid abbreviation of ", {}),
        ("word", {"code": True}),
        (". A valid abbreviation replaces one or more consecutive letters with a number representing the count of skipped letters. Numbers cannot have leading zeros.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('word="substitution", abbr="s10n"', {"code": True}),
        (" → True  (s + skip 10 + n). ", {}),
        ('word="apple", abbr="a2e"', {"code": True}),
        (' → False  (skip 2 lands at "l", not "e").', {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Two Pointers with Skip (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to check if abbr 'describes' word correctly. Think of it as a cursor walking through word — some steps move one character at a time (letter match), and some jump multiple steps at once (skip number). This is inherently a two-cursor problem."),
        N.h4("What Doesn't Work"),
        N.para("Brute force — generating all 2^n possible abbreviations of word and checking if abbr appears — is O(2^n) time and space, completely impractical. Regex works but hides edge cases inside library internals and still uses O(n) space for the pattern string."),
        N.h4("The Key Observation"),
        N.para("abbr[j] is either a digit or a letter. If it's a letter, word[i] must match it exactly. If it's a digit, we parse the full integer (possibly multi-digit) and jump i forward by that count. Two cases, handled greedily, left to right."),
        N.h4("Building the Solution"),
        N.para("Maintain i (position in word) and j (position in abbr). Walk j through abbr. For digits: accumulate n = n*10 + int(abbr[j]) until no more digits, then i += n. For letters: verify word[i] == abbr[j], then i++, j++. After the loop: both i and j must equal their respective lengths."),
        N.callout(
            "Analogy: Imagine following map directions — 'go 10 blocks then turn left.' The number tells you how many blocks to skip; you don't check each block individually. When the directions say a street name, you verify you're on the right street.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def validWordAbbreviation(word: str, abbr: str) -> bool:\n"
        "    i, j = 0, 0\n"
        "    while i < len(word) and j < len(abbr):\n"
        "        if abbr[j].isdigit():\n"
        "            if abbr[j] == '0':  # leading zero forbidden\n"
        "                return False\n"
        "            n = 0\n"
        "            while j < len(abbr) and abbr[j].isdigit():\n"
        "                n = n * 10 + int(abbr[j])\n"
        "                j += 1\n"
        "            i += n  # leap i forward by skip count\n"
        "        else:\n"
        "            if word[i] != abbr[j]:  # letter mismatch\n"
        "                return False\n"
        "            i += 1\n"
        "            j += 1\n"
        "    return i == len(word) and j == len(abbr)  # both must be exhausted"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("i, j = 0, 0", {"code": True}), (" — Two pointers: i walks word, j walks abbr.", {})])),
    N.para(N.rich([("while i < len(word) and j < len(abbr):", {"code": True}), (" — Continue as long as both strings have remaining characters.", {})])),
    N.para(N.rich([("if abbr[j].isdigit():", {"code": True}), (" — Branch on whether current abbr character is a digit or letter.", {})])),
    N.para(N.rich([("if abbr[j] == '0': return False", {"code": True}), (" — Leading zero is forbidden by the problem spec; reject immediately.", {})])),
    N.para(N.rich([("n = n * 10 + int(abbr[j]); j += 1", {"code": True}), (" — Accumulate the full integer one digit at a time (handles multi-digit numbers like 10, 127).", {})])),
    N.para(N.rich([("i += n", {"code": True}), (" — Jump i forward by n positions, skipping n word characters at once.", {})])),
    N.para(N.rich([("if word[i] != abbr[j]: return False", {"code": True}), (" — Letter in abbr must exactly match corresponding letter in word.", {})])),
    N.para(N.rich([("i += 1; j += 1", {"code": True}), (" — Both matched; advance both pointers past the matched character.", {})])),
    N.para(N.rich([("return i == len(word) and j == len(abbr)", {"code": True}), (" — CRITICAL: both must be fully exhausted. If either has trailing characters, it's invalid.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two Pointers with Skip (optimal)", "O(n+m)", "O(1)"],
        ["Regex matching", "O(n+m)", "O(n)"],
        ["Brute Force (enumerate all abbreviations)", "O(2^n)", "O(2^n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two Pointers with Skip", {})])),
    N.callout(
        "When to recognize this pattern: Two sequences must be matched in sync, but one contains compressed 'skip' tokens that advance the other pointer by a variable amount. The skip amount is encoded in the token itself and must be parsed on-the-fly. Both sequences must be fully consumed for a valid match.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Generalized Abbreviation", {"bold": True}), (" (Medium) — Generate all valid abbreviations via backtracking; uses the same definition of validity (#320)", {})])),
    N.bullet(N.rich([("Minimum Unique Word Abbreviation", {"bold": True}), (" (Hard) — Shortest abbreviation not matching any dictionary word; uses this check as a subroutine (#411)", {})])),
    N.bullet(N.rich([("Backspace String Compare", {"bold": True}), (" (Easy) — Two pointers from the back; '#' causes a skip backwards; same 'one pointer can jump' spirit (#844)", {})])),
    N.bullet(N.rich([("Is Subsequence", {"bold": True}), (" (Easy) — Two pointers where word-pointer only advances on match; no encoded skip (#392)", {})])),
    N.bullet(N.rich([("Wildcard Matching", {"bold": True}), (" (Hard) — '*' skips any sequence, '?' skips one character; DP or two-pointer (#44)", {})])),
    N.bullet(N.rich([("Word Abbreviation", {"bold": True}), (" (Hard) — Build minimal unique abbreviations for a list; uses this validation as building block (#527)", {})])),
    N.bullet(N.rich([("Compare Version Numbers", {"bold": True}), (" (Medium) — Parse numbers from two strings simultaneously; same integer-accumulation inner loop (#165)", {})])),
    N.para("These problems share the same core technique: two-pointer sync with variable-length jumps encoded in one of the sequences."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Two Pointers section", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_word_abbreviation")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
