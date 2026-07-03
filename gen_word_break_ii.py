"""
gen_word_break_ii.py — Notion page rebuild for Word Break II (#140, Hard)
DP + Backtracking with memoization.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-813b-97a8-e57441456045"

# ── 1. Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=140,
    pattern="Dynamic Programming",
    subpatterns=["DP + Backtracking"],
    tc="O(n³)",
    sc="O(n²)",
    key_insight="Memoize reachable start indices; backtrack only from valid split points to reconstruct all sentences.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old content ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and a dictionary of strings ", {}),
        ("wordDict", {"code": True}),
        (", add spaces in ", {}),
        ("s", {"code": True}),
        (" to construct a sentence where each word is a valid dictionary word. "
         "Return all such possible sentences in any order.\n\n"
         "Note that the same word in the dictionary may be reused multiple times in the segmentation.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]\n'
         'Output: ["cats and dog", "cat sand dog"]', {"code": True}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]\n'
         'Output: ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]', {"code": True}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ s.length ≤ 20, 1 ≤ wordDict.length ≤ 1000, "
         "1 ≤ wordDict[i].length ≤ 10. "
         "Guaranteed all inputs are lowercase English letters. "
         "All strings in wordDict are unique.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Memoized Backtracking (Interview Pick) ─────────────────────
SOLUTION_1_CODE = '''\
from functools import lru_cache
from typing import List

def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)                   # O(1) lookup

    @lru_cache(maxsize=None)
    def backtrack(start: int) -> List[str]:
        """Return all valid sentences from s[start:]."""
        if start == len(s):                    # base case: consumed all chars
            return [""]                        # empty sentence suffix

        sentences = []
        for end in range(start + 1, len(s) + 1):          # try every prefix
            word = s[start:end]
            if word in word_set:               # valid word found
                for rest in backtrack(end):    # recurse on remainder
                    if rest:
                        sentences.append(word + " " + rest)
                    else:
                        sentences.append(word) # last word, no trailing space
        return sentences

    return backtrack(0)
'''

blocks += [
    N.h2("Solution 1 — Memoized Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to find ALL ways to split string s into words that each appear in "
            "wordDict. This is not just yes/no (like Word Break I) — we must enumerate "
            "every valid partition and reconstruct the actual sentences."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without memoization is exponential: for a string like 'aaa...a' "
            "with wordDict=['a','aa','aaa'], the call tree explodes because the same suffix "
            "s[start:] is processed from multiple different parent calls. Without caching, "
            "we recompute the same suffix hundreds of times."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The set of all valid sentences starting at index i depends only on i, not on "
            "how we arrived at i. This is the overlapping-subproblem structure that makes "
            "memoization valid. If backtrack(5) returns [\"and dog\"], that answer is the "
            "same regardless of whether we reached index 5 via 'cat' or 'cats'."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Convert wordDict to a set for O(1) lookup.\n"
            "2. Define backtrack(start) = all sentences constructible from s[start:].\n"
            "3. Base case: start == len(s) → return [''] (empty suffix, signals success).\n"
            "4. Try every end from start+1 to len(s). If s[start:end] is a word, recurse "
            "on backtrack(end) and prepend s[start:end] to each result.\n"
            "5. Cache with @lru_cache — identical start indices return instantly on repeat calls."
        ),
        N.callout(
            "Analogy: Imagine splitting a sentence written without spaces. "
            "At each position you try every possible 'next word'. "
            "If you've solved what comes after, you just prepend your word. "
            "Memoization is like writing your solved suffix on a sticky note — "
            "the next caller reads the note instead of solving from scratch.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: DP + Backtracking with Memoization"),
    N.para(
        "This pattern combines two classical techniques:\n\n"
        "• Backtracking: Systematically explore all word splits, abandon branches "
        "that can't form valid sentences.\n"
        "• Memoization (Top-Down DP): Cache the result of backtrack(start) so that "
        "any suffix s[start:] is solved at most once, even if reached from multiple paths.\n\n"
        "Core invariant: backtrack(i) = exhaustive list of all sentences from s[i:]. "
        "This is well-defined because s[i:] determines the result uniquely.\n\n"
        "Why it works: Since backtrack(i) depends only on backtrack(j) for j > i, "
        "the recursion is acyclic and terminates. The cache ensures each suffix is "
        "processed in O(n²) work (n² substrings × O(n) string operations = O(n³) total)."
    ),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("word_set = set(wordDict)", {"code": True}),
                   (" — Convert list to set for O(1) membership tests in the hot loop.", {})])),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   (" — Python decorator that memoizes backtrack by its argument (", {}),
                   ("start", {"code": True}),
                   ("). Same start → same cached result.", {})])),
    N.para(N.rich([("def backtrack(start)", {"code": True}),
                   (" — Returns all valid sentences constructible from ", {}),
                   ("s[start:]", {"code": True}), (". This is the memoized DP state.", {})])),
    N.para(N.rich([("if start == len(s): return ['']", {"code": True}),
                   (" — Base case: we consumed all of ", {}), ("s", {"code": True}),
                   (", so return one 'empty' result signalling a complete valid parse.", {})])),
    N.para(N.rich([("for end in range(start + 1, len(s) + 1)", {"code": True}),
                   (" — Try every possible endpoint for the next word: prefix ", {}),
                   ("s[start:end]", {"code": True}), (". This is O(n) per call.", {})])),
    N.para(N.rich([("if word in word_set", {"code": True}),
                   (" — O(1) hash lookup: is this prefix a valid dictionary word?", {})])),
    N.para(N.rich([("for rest in backtrack(end)", {"code": True}),
                   (" — Recursively get all sentences from the remainder. Cached after first call.", {})])),
    N.para(N.rich([("sentences.append(word + ' ' + rest)", {"code": True}),
                   (" — Prepend current word to each valid continuation (space-separated).", {})])),
    N.para(N.rich([("sentences.append(word)", {"code": True}),
                   (" — When ", {}), ("rest == ''", {"code": True}),
                   (" (last word), no trailing space needed.", {})])),
    N.para(N.rich([("return backtrack(0)", {"code": True}),
                   (" — Start from index 0: all valid sentences for the full string.", {})])),
    N.divider(),
]

# ── Solution 2 — Iterative DP + Path Reconstruction ─────────────────────────
SOLUTION_2_CODE = '''\
from typing import List

def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)
    n = len(s)

    # dp[i] = list of words that end at index i and start from some reachable index
    # Actually: dp[i] = list of (start, word) pairs where s[start:i] is a valid word
    # and start is reachable from index 0
    reachable = [False] * (n + 1)
    reachable[0] = True
    # back[i] = list of start indices j such that s[j:i] is a word and j is reachable
    back = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(i):
            if reachable[j] and s[j:i] in word_set:
                reachable[i] = True
                back[i].append(j)

    # Reconstruct sentences from back-pointer table
    results = []
    def reconstruct(end, sentence):
        if end == 0:
            results.append(" ".join(reversed(sentence)))
            return
        for start in back[end]:
            sentence.append(s[start:end])
            reconstruct(start, sentence)
            sentence.pop()

    if reachable[n]:
        reconstruct(n, [])
    return results
'''

blocks += [
    N.h2("Solution 2 — Iterative DP + Path Reconstruction"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of top-down recursion, we think bottom-up: first determine which "
            "indices i are 'reachable' (s[0:i] can be formed from dict words), then "
            "reconstruct paths through those reachable nodes."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy selection won't work — we can't always pick the longest or shortest "
            "word at each position and guarantee all sentences are found. We need to "
            "explore all branching points."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This is essentially shortest-path enumeration on a DAG: nodes are indices "
            "0..n, and there's an edge from j to i if s[j:i] is a word. We first run BFS/DP "
            "to find which nodes are reachable from 0, then DFS backwards from n "
            "to reconstruct all paths."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build reachable[] array: reachable[i] = True if s[0:i] can be segmented.\n"
            "2. Simultaneously build back[i] = list of j values where s[j:i] is a word and j is reachable.\n"
            "3. Reconstruct by DFS from n back to 0, collecting words in reverse.\n"
            "4. When we reach 0, we've found a valid sentence — join words (reversed)."
        ),
        N.callout(
            "Think of it like a GPS route finder: first mark which intersections "
            "(indices) are reachable, then trace all routes backwards from the destination.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("reachable = [False] * (n + 1)", {"code": True}),
                   (" — DP boolean array. ", {}), ("reachable[i]", {"code": True}),
                   (" = True means ", {}), ("s[0:i]", {"code": True}),
                   (" can be formed using dictionary words.", {})])),
    N.para(N.rich([("back[i].append(j)", {"code": True}),
                   (" — Record that index j is a valid predecessor of i "
                    "(meaning s[j:i] is a word AND j was reachable).", {})])),
    N.para(N.rich([("def reconstruct(end, sentence)", {"code": True}),
                   (" — DFS from ", {}), ("end", {"code": True}), (" back to 0, "
                    "building sentence in reverse by pushing words onto a stack.", {})])),
    N.para(N.rich([("if end == 0", {"code": True}),
                   (" — Reached the start: we have a complete valid segmentation. "
                    "Reverse the word stack and join with spaces.", {})])),
    N.para(N.rich([("sentence.append/pop", {"code": True}),
                   (" — Classic backtracking pattern: add word before recursing, "
                    "remove after to restore state for the next branch.", {})])),
    N.divider(),
]

# ── Solution 3 — Brute Force Recursive (no memo) ────────────────────────────
SOLUTION_3_CODE = '''\
from typing import List

def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)
    results = []

    def backtrack(start: int, path: List[str]):
        if start == len(s):
            results.append(" ".join(path))
            return
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                path.append(word)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return results
'''

blocks += [
    N.h2("Solution 3 — Brute Force Backtracking (No Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest approach: try every word split, recurse on the remainder, "
               "collect results when we reach the end. This is the natural recursive formulation "
               "before any optimization."),
        N.h4("What Doesn't Work"),
        N.para("Without memoization, the same suffix s[i:] can be processed exponentially many times. "
               "For adversarial inputs like s='aaa...a' with wordDict=['a','aa'], "
               "the time complexity is O(2^n) since each character boundary can be a split or not."),
        N.h4("The Key Observation"),
        N.para("This is correct but too slow for large inputs. It IS the algorithm to explain "
               "to an interviewer first, before optimizing to Solution 1 with memoization."),
        N.h4("Building the Solution"),
        N.para("Standard backtracking template: try each option, recurse, undo (path.pop)."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def backtrack(start, path)", {"code": True}),
                   (" — Explore all valid segmentations of ", {}),
                   ("s[start:]", {"code": True}), (", accumulating words in ", {}),
                   ("path", {"code": True}), (".", {})])),
    N.para(N.rich([("if start == len(s): results.append(...)", {"code": True}),
                   (" — Complete segmentation found: join path words with spaces and record.", {})])),
    N.para(N.rich([("path.pop()", {"code": True}),
                   (" — Backtrack: remove last word to try a different split at this position.", {})])),
    N.divider(),
]

# ── Why is This DP? ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🧠 Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
                   ("The set of sentences for ", {}), ("s[0:n]", {"code": True}),
                   (" can be built from sentences for shorter suffixes. "
                    "Specifically: sentences(s) = {w + \" \" + rest : w is a word prefix, rest ∈ sentences(s[len(w):])}. "
                    "Each smaller problem contributes directly to the larger one.", {})])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
                   ("The suffix starting at index ", {}), ("i", {"code": True}),
                   (" may be reached via many different word splits. "
                    "For example with s='catsanddog', index 3 is reached via 'cat' and index 4 via 'cats'. "
                    "Both then need to solve the same suffix 's[3:]'. Without memoization, "
                    "this suffix is reprocessed multiple times.", {})])),
    N.code(
        "# Recurrence relation:\n"
        "# backtrack(i) = [] if no valid split from i\n"
        "#               = [word + ' ' + rest\n"
        "#                  for end in range(i+1, n+1)\n"
        "#                  if s[i:end] in word_set\n"
        "#                  for rest in backtrack(end)]\n\n"
        "# Base case:\n"
        "# backtrack(n) = ['']   (empty string = valid empty sentence)\n\n"
        "# Memoization key: start index i (integer, 0..n)\n"
        "# State space: O(n) states, each storing up to O(2^n) sentences in worst case\n"
        "# Transition: O(n) per state (try all end indices)\n"
        "# Total time: O(n^3) amortized for typical inputs",
        "python"
    ),
    N.callout(
        "Key difference from Word Break I (LC #139): That problem only asks CAN it be done "
        "(boolean DP, O(n²)). This problem asks for ALL ways, so we must enumerate. "
        "The DP here memoizes lists of strings, not a boolean — space can be O(n · 2^n) "
        "in adversarial cases because the OUTPUT itself can be exponential.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (no memo)", "O(2ⁿ)", "O(n) recursion stack"],
        ["Memoized Backtracking (Interview Pick)", "O(n³)", "O(n²) memo + output"],
        ["Iterative DP + Reconstruction", "O(n³)", "O(n²) back-pointer table"],
    ]),
    N.para(
        "Note: If the output itself is exponential (e.g., adversarial inputs), "
        "space is dominated by the result list, not the DP structure. "
        "The O(n³) time bound assumes the number of sentences is polynomial."
    ),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("DP + Backtracking (Memoized Search for Enumeration)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'return ALL valid ...' or 'enumerate all ways'\n"
        "• Naive recursion explores overlapping subproblems (same suffix/subproblem reached many ways)\n"
        "• The answer for position i depends only on answers for positions j > i\n"
        "• Constraint: string length ≤ 20 (small enough for memoized backtracking)\n"
        "• Often a follow-up to a simpler yes/no DP problem (Word Break I → II)",
        "🔎", "green_background"
    ),
    N.para(
        "Verified against DSA_Patterns_and_SubPatterns_Guide.md — "
        "Section 18: Dynamic Programming, Sub-Pattern: DP + Backtracking. "
        "Word Break II is listed as the canonical Hard example of memoized enumeration DP."
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DP + Backtracking / Memoized Enumeration technique:"),
    N.bullet(N.rich([("Word Break (LC #139)", {"bold": True}),
                     (" (Medium) — Simpler yes/no DP version; solve this first before #140", {})])),
    N.bullet(N.rich([("Combination Sum II (LC #40)", {"bold": True}),
                     (" (Medium) — Backtracking over candidates with duplicate handling", {})])),
    N.bullet(N.rich([("Palindrome Partitioning (LC #131)", {"bold": True}),
                     (" (Medium) — Backtrack all ways to partition into palindromes; "
                      "memoize palindrome check", {})])),
    N.bullet(N.rich([("Palindrome Partitioning II (LC #132)", {"bold": True}),
                     (" (Hard) — Min cuts variant; pure DP without enumeration", {})])),
    N.bullet(N.rich([("Restore IP Addresses (LC #93)", {"bold": True}),
                     (" (Medium) — Enumerate all valid IP address splits from digit string", {})])),
    N.bullet(N.rich([("Decode Ways II (LC #639)", {"bold": True}),
                     (" (Hard) — Count (not enumerate) ways to decode with wildcards; "
                      "memoized DP on index", {})])),
    N.bullet(N.rich([("Generate Parentheses (LC #22)", {"bold": True}),
                     (" (Medium) — Enumerate all valid bracket strings; backtracking with state", {})])),
    N.bullet(N.rich([("Unique Paths III (LC #980)", {"bold": True}),
                     (" (Hard) — Enumerate all paths on grid visiting every cell; "
                      "backtracking + bitmask DP", {})])),
    N.bullet(N.rich([("Expression Add Operators (LC #282)", {"bold": True}),
                     (" (Hard) — Enumerate all arithmetic expressions from digit string; "
                      "similar suffix-split backtracking", {})])),
    N.para("These problems share the core technique: memoized (or pruned) backtracking "
           "where the same subproblem recurs from multiple parent calls."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — "
              "Section 18: Dynamic Programming → DP + Backtracking", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("word_break_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Push to Notion ────────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
