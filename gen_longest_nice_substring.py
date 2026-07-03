"""
gen_longest_nice_substring.py
Notion IN-PLACE update for LeetCode #1763 Longest Nice Substring
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f1-b4e3-ded857345b8a"

# ── 1) Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1763,
    pattern="Divide and Conquer",
    subpatterns=["Divide on Invalid Chars"],
    tc="O(n²) worst / O(n log n) avg",
    sc="O(n)",
    key_insight="Any char missing its case-partner is an invalid wall; divide at it and recurse on both sides.",
    icon="🟢"
)
print("Properties set OK.")

# ── 2) Wipe old body ──
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3) Build body blocks ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("A string s is nice if, for every letter of the alphabet that appears in it, both its lowercase and uppercase versions appear too. For example, "),
        ('"Bb"', {"code": True}),
        (" is nice because both "),
        ("'B'", {"code": True}),
        (" and "),
        ("'b'", {"code": True}),
        (" are present. Given a string "),
        ("s", {"code": True}),
        (", return the longest nice substring of "),
        ("s", {"code": True}),
        (". If there are multiple answers of the same length, return the one that occurs earlier. If there are none, return "),
        ('""', {"code": True}),
        (".")
    ])),
    N.para(N.rich([
        ("Example: s = ", {}),
        ('"YazaAay"', {"code": True}),
        (' → Output: ', {}),
        ('"aAa"', {"code": True}),
        (" — 'z' has no 'Z', so it splits; left side 'Ya' gives nothing; right side 'aAay' splits at 'y' (no 'Y'); 'aAa' is nice (length 3).", {})
    ])),
    N.divider()
]

# ── Solution 1: Divide and Conquer (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Divide and Conquer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest contiguous segment where every character appears in both cases. Think of it as: every character must be 'paired'. Unpaired characters are blockers."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all O(n²) substrings and checks each in O(n) → O(n³) total. Acceptable for tiny n (len ≤ 100 as per constraints), but there's a more elegant insight."),
        N.h4("The Key Observation"),
        N.para("A character whose case-partner is absent from the current substring is an 'invalid' blocking character. No nice substring can span across its position — the nice substring must lie entirely to the left or right of it. This is a guaranteed split point."),
        N.h4("Building the Solution"),
        N.para("1. Base case: len ≤ 1 → return '' (can't form a case pair). 2. Build char_set for the current substring. 3. Scan for the first invalid char (partner absent). 4. Divide there: recurse left and right. 5. Return the longer result (prefer left on ties for earliest occurrence). 6. If no invalid char found, the whole substring is nice — return it."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of invalid characters as walls in a maze. The nice treasure must lie entirely in one room — the wall never belongs to any room. So split at each wall, explore both rooms, keep the bigger find.", {})]),
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(
"""def longestNiceSubstring(s: str) -> str:
    if len(s) <= 1:
        return ""
    char_set = set(s)
    for i, c in enumerate(s):
        if c.swapcase() not in char_set:
            left  = longestNiceSubstring(s[:i])
            right = longestNiceSubstring(s[i+1:])
            if len(left) >= len(right):
                return left
            return right
    return s  # whole string is nice""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(s) <= 1: return \"\"", {"code": True}), (" — Base case: a single character (or empty) can never have its case-partner alongside it, so it's never nice.", {})])),
    N.para(N.rich([("char_set = set(s)", {"code": True}), (" — Collect all characters in the current substring into a set for O(1) membership lookups.", {})])),
    N.para(N.rich([("for i, c in enumerate(s):", {"code": True}), (" — Scan left to right looking for the first invalid character.", {})])),
    N.para(N.rich([("if c.swapcase() not in char_set:", {"code": True}), (" — swapcase() converts 'a'→'A' and 'Z'→'z'. If the partner is absent, c is invalid.", {})])),
    N.para(N.rich([("left = longestNiceSubstring(s[:i])", {"code": True}), (" — Recurse on everything BEFORE the invalid char at index i.", {})])),
    N.para(N.rich([("right = longestNiceSubstring(s[i+1:])", {"code": True}), (" — Recurse on everything AFTER (the invalid char itself is excluded from both halves).", {})])),
    N.para(N.rich([("if len(left) >= len(right): return left", {"code": True}), (" — Use >= (not >) to prefer left on ties — left appears earlier in the original string.", {})])),
    N.para(N.rich([("return s", {"code": True}), (" — If the loop completes without finding any invalid char, the entire current substring is nice. Return it directly.", {})])),
    N.divider()
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force (O(n³))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading: try every possible substring, check if it's nice, keep the longest."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n³) — O(n²) substrings times O(n) to check each. Given LeetCode constraints (n ≤ 100), it actually passes, but it's not the intended elegant solution."),
        N.h4("The Key Observation"),
        N.para("For each substring s[i:j], build a character set and verify every character has its case-partner also in the set. Track the longest qualifying substring."),
        N.h4("Building the Solution"),
        N.para("Two nested loops define start/end. Inner check: build set, verify all chars paired. If nice and longer than current best, update. Use strict > to keep the first (earliest) occurrence when lengths tie."),
    ]),
    N.h3("Code"),
    N.code(
"""def longestNiceSubstring_brute(s: str) -> str:
    best = ""
    for i in range(len(s)):
        for j in range(i+2, len(s)+1):  # min length 2
            sub = s[i:j]
            chars = set(sub)
            if all(c.swapcase() in chars for c in chars):
                if len(sub) > len(best):  # strict > keeps first occurrence
                    best = sub
    return best""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(s)):", {"code": True}), (" — Try every start index for the substring.", {})])),
    N.para(N.rich([("for j in range(i+2, len(s)+1):", {"code": True}), (" — End index (exclusive). Start at i+2 so minimum length is 2 (can't be nice with length 1).", {})])),
    N.para(N.rich([("chars = set(sub)", {"code": True}), (" — Build character set for this candidate substring.", {})])),
    N.para(N.rich([("if all(c.swapcase() in chars for c in chars):", {"code": True}), (" — Nice check: every character in the set must have its case-partner also in the set.", {})])),
    N.para(N.rich([("if len(sub) > len(best): best = sub", {"code": True}), (" — Strict > so only longer substrings update best — preserving the earlier (first) nice substring on ties.", {})])),
    N.divider()
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n³)", "O(n)"],
        ["Divide and Conquer ✓", "O(n²) worst / O(n log n) avg", "O(n) stack"],
    ]),
    N.para("Note: LeetCode constraints are n ≤ 100, so both approaches pass. D&C is the intended elegant solution."),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Divide and Conquer", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Divide on Invalid Chars — find the first character whose case-partner is absent; divide there; recurse on both halves independently.", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) 'Find longest substring with property P'. (2) Certain characters provably cannot appear in any valid answer. (3) Those characters act as guaranteed split walls. (4) The answer must lie entirely on one side of each wall. Compare to QuickSort: pivot partitions but here the 'pivot' is a blocking invalid char.", {})
        ]),
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Longest Nice Subarray", {"bold": True}), (" (Medium, #2401) — Similar 'nice' concept on integers with bitwise AND = 0 condition; sliding window approach.", {})])),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), (" (Medium, #53) — Classic D&C solution: split at midpoint, solve each half, combine by considering cross-midpoint segment.", {})])),
    N.bullet(N.rich([("Make The String Great", {"bold": True}), (" (Easy, #1544) — Remove adjacent chars whose case differs; stack approach on similar case-pairing logic.", {})])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), (" (Medium, #978) — Find longest subarray with alternating comparison signs; D&C or sliding window on 'break points'.", {})])),
    N.bullet(N.rich([("Minimum Cost to Cut a Stick", {"bold": True}), (" (Hard, #1547) — D&C with memoization (interval DP): cut points define recursive sub-problems.", {})])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium, #3) — Invalid char (duplicate) triggers window shrink rather than D&C split; sliding window alternative.", {})])),
    N.para("These problems share the core idea: certain 'blocking' elements partition the search space, and the optimal answer lies entirely within one partition."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Divide and Conquer section. Sub-Pattern: Divide on Invalid Chars.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_nice_substring")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
