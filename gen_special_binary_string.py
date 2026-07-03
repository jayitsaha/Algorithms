"""gen_special_binary_string.py — Notion page rebuild for LeetCode #761."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8144-a700-cc920f79d54f"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=761,
    pattern="Recursion",
    subpatterns=["Recursive Decomposition"],
    tc="O(n² log n)",
    sc="O(n log n)",
    key_insight="Balance-counter segments the string; recurse on inner, re-wrap, sort descending to maximize.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old content ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a special binary string ", {}),
        ("s", {"code": True}),
        (", return the lexicographically largest string possible after any number of swaps of adjacent special substrings. A ", {}),
        ("special", {"bold": True}),
        (" binary string is one where: (1) every prefix has at least as many 1s as 0s, and (2) the total count of 1s equals the total count of 0s.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Recursive Decomposition (Interview Pick)
blocks += [
    N.h2("Solution 1 — Recursive Decomposition (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Map 1→( and 0→). A special binary string is exactly a valid parenthesization. The task becomes: rearrange adjacent groups of balanced brackets to produce the lexicographically largest string."),
        N.h4("What Doesn't Work"),
        N.para("Trying all permutations of segments is O(k!) — catastrophically slow. Greedy swaps (bubble-sort style) work but are O(n² · n) without the insight. We need to see the recursive structure."),
        N.h4("The Key Observation"),
        N.para("Every maximal special segment has the form '1 + inner + 0'. The inner part is also special. We can only swap segments at the same level — not across different wrappers. So we must recursively maximize inner content first, then sort the wrappers."),
        N.h4("Building the Solution"),
        N.para("Use a balance counter: +1 on '1', -1 on '0'. Each time balance hits 0, we have one complete maximal segment s[i..j]. Strip the outer 1 and 0, recurse on s[i+1:j], re-wrap with '1' and '0', collect. After scanning, sort segments descending (larger lex value = better prefix = larger concatenation). Join and return."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of it as a nested Russian doll. You open each doll (strip '1'+'0'), rearrange the inner dolls recursively, then re-seal (re-wrap) and sort the outer dolls largest-first.", {})]),
            "🪆", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def makeLargestSpecial(s: str) -> str:\n"
        "    count, i = 0, 0\n"
        "    specials = []\n"
        "    for j, c in enumerate(s):\n"
        "        count += 1 if c == '1' else -1\n"
        "        if count == 0:\n"
        "            inner = makeLargestSpecial(s[i+1:j])\n"
        "            specials.append('1' + inner + '0')\n"
        "            i = j + 1\n"
        "    specials.sort(reverse=True)\n"
        "    return ''.join(specials)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("count, i = 0, 0", {"code": True}), (" — balance counter (like tracking open brackets) and the start index of the current segment.", {})])),
    N.para(N.rich([("specials = []", {"code": True}), (" — will collect all maximized top-level segments.", {})])),
    N.para(N.rich([("count += 1 if c == '1' else -1", {"code": True}), (" — '1' is an open bracket (+1), '0' is a close bracket (-1). This is the parentheses analogy in action.", {})])),
    N.para(N.rich([("if count == 0:", {"code": True}), (" — balance returned to 0: the substring s[i..j] is one complete maximal special segment. Time to process it.", {})])),
    N.para(N.rich([("inner = makeLargestSpecial(s[i+1:j])", {"code": True}), (" — strip the outer '1' (at i) and '0' (at j). Recurse on the inner content. Trust the recursive call to maximize it.", {})])),
    N.para(N.rich([("specials.append('1' + inner + '0')", {"code": True}), (" — re-wrap the maximized inner with the outer brackets. This is the key mechanic: strip → recurse → re-wrap.", {})])),
    N.para(N.rich([("i = j + 1", {"code": True}), (" — advance the segment start pointer past the segment we just processed.", {})])),
    N.para(N.rich([("specials.sort(reverse=True)", {"code": True}), (" — sort all segments in descending lexicographic order. Larger segments first = lexicographically largest concatenation.", {})])),
    N.para(N.rich([("return ''.join(specials)", {"code": True}), (" — concatenate in sorted order. This is the answer for this level.", {})])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force (All Permutations, Educational Only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simply try every possible ordering of the top-level maximal special segments and pick the lexicographically largest."),
        N.h4("What Doesn't Work"),
        N.para("This is O(k! * n) where k is the number of top-level segments. For even k=10, that's 3.6 million permutations times string operations. Completely infeasible in practice — only useful for verifying correctness on tiny inputs."),
        N.h4("The Key Observation"),
        N.para("Brute force reveals that the answer IS a permutation of the top-level segments. This motivates the question: can we find the best permutation without trying all of them? Yes — greedy descending sort (Solution 1)."),
        N.h4("Building the Solution"),
        N.para("Find all top-level segments using the same balance scan. Use itertools.permutations to try every ordering. Track the maximum. Return it."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import permutations\n"
        "\n"
        "def makeLargestSpecial_brute(s: str) -> str:\n"
        "    count, i, segs = 0, 0, []\n"
        "    for j, c in enumerate(s):\n"
        "        count += 1 if c == '1' else -1\n"
        "        if count == 0:\n"
        "            segs.append(s[i:j+1])  # store full segment, no recursion\n"
        "            i = j + 1\n"
        "    best = ''\n"
        "    for perm in permutations(segs):   # O(k!) orderings\n"
        "        best = max(best, ''.join(perm))\n"
        "    return best"
    ),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (permutations)", "O(k! · n)", "O(n)"],
        ["Recursive Decomposition ✓", "O(n² log n)", "O(n log n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Recursion", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Recursive Decomposition — balance-counter segmentation with greedy post-sort.", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Problem has nested/recursive structure (brackets, balanced strings, trees). "
             "(2) A 'running balance reaching zero' naturally segments the input. "
             "(3) Optimal substructure: maximize each sub-segment independently, then combine. "
             "(4) 'Rearrange substrings' + recursive definition of valid structure. "
             "(5) The greedy sort argument: A > B lex implies A+B > B+A lex.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (Recursive Decomposition / Nested Structures):"),
    N.bullet(N.rich([("Decode String", {"bold": True}), (" (Medium) — Recursively decode '3[a2[c]]' style nested strings; balance tracks bracket depth (#394)", {})])),
    N.bullet(N.rich([("Different Ways to Add Parentheses", {"bold": True}), (" (Medium) — Recursively split at each operator; all ways to parenthesize (#241)", {})])),
    N.bullet(N.rich([("Scramble String", {"bold": True}), (" (Hard) — Recursively decompose string halves to check scramble relationship (#87)", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Divide by minimum element, recurse on left/right partitions (#84)", {})])),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), (" (Hard) — Interval DP where 'last balloon bursted' defines subproblem; same decompose idea (#312)", {})])),
    N.bullet(N.rich([("Remove Invalid Parentheses", {"bold": True}), (" (Hard) — BFS/recursion removing minimum brackets; same balance analogy (#301)", {})])),
    N.bullet(N.rich([("Longest Valid Parentheses", {"bold": True}), (" (Hard) — Balance counter + DP; 1=open, 0=close pattern (#32)", {})])),
    N.para("These problems share the core technique: use a running balance to detect nested boundaries, decompose into subproblems at each boundary, solve recursively."),
    N.callout("📚 Reference: Analysis — Recursive Decomposition. Also connected to: Stack/Queue → Parentheses Matching (same balance counter); Sorting → Greedy Comparison (same A+B vs B+A argument as LC #179).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("special_binary_string")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
