"""
Notion update script for LeetCode #792 — Number of Matching Subsequences.
Updates the existing page in-place (no duplicate creation).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81e8-9e45-c1fab67393bc"
SLUG = "number_of_matching_subsequences"

# ── 1. Update properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=792,
    pattern="Hash Tables",
    subpatterns=["Bucket by First Char"],
    tc="O(|s| + total word length)",
    sc="O(total word length)",
    key_insight="Bucket words by next-needed char; scan s once to advance all waiting words simultaneously.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" and an array of strings ", {}),
        ("words", {"code": True}),
        (", return the number of ", {}),
        ("words[i]", {"code": True}),
        (" that are subsequences of ", {}),
        ("s", {"code": True}),
        (". A string ", {}),
        ("w", {"code": True}),
        (" is a subsequence of ", {}),
        ("s", {"code": True}),
        (" if all characters of ", {}),
        ("w", {"code": True}),
        (" appear in ", {}),
        ("s", {"code": True}),
        (" in order (not necessarily consecutively).", {}),
    ])),
    N.para(N.rich([
        ("Example: s = \"abcde\", words = [\"a\",\"bb\",\"acd\",\"ace\"]\n", {}),
        ("Output: 3  (\"a\", \"acd\", \"ace\" are subsequences; \"bb\" is not)", {"color": "gray"}),
    ])),
    N.divider(),
]

# ── Solution 1: Bucket by First Char (optimal) ─────────────────────────────
blocks += [
    N.h2("Solution 1 — Bucket by First Char (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have many words, each needing to be matched against the same string s. The cost of checking each word independently is O(n × |s|) — we rescan s from the beginning for every word. The question is: can we process s just once?"),
        N.h4("What Doesn't Work"),
        N.para("Naive two-pointer per word: for each word, walk a pointer through s matching characters. This is O(|s|) per word, O(n × |s|) total. For n=5000 and |s|=50000, that's 250 million operations — TLE."),
        N.h4("The Key Observation"),
        N.para("When we see character c in s, every word whose next needed character is c can advance simultaneously. Instead of asking 'does this word match s?', flip it: 'which words does this character of s unlock?' This is the batch-processing insight."),
        N.h4("Building the Solution"),
        N.para("Maintain a hash map: waiting[c] = list of (word, next_idx) tuples. Enroll each word in waiting[word[0]] with next_idx=1. Scan s once. For each c in s, collect all entries from waiting[c], clear the bucket, and advance each entry: if next_idx == len(word) → count++; else re-enroll in waiting[word[next_idx]]."),
        N.callout(
            "Analogy: A waiting room with 26 labeled doors. Each word enters through its first-letter door. A caller walks through doors in order (scanning s). When 'c' is announced, everyone in the 'c' room steps forward — done ones leave with a ticket; others immediately re-queue at their next door.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict\n\n"
        "def numMatchingSubseq(s, words):\n"
        "    waiting = defaultdict(list)\n"
        "    for w in words:\n"
        "        waiting[w[0]].append((w, 1))  # store next-index, not current\n"
        "    count = 0\n"
        "    for c in s:\n"
        "        advance = waiting[c]\n"
        "        waiting[c] = []  # CRITICAL: clear before re-inserting\n"
        "        for w, i in advance:\n"
        "            if i == len(w):\n"
        "                count += 1  # word fully matched\n"
        "            else:\n"
        "                waiting[w[i]].append((w, i + 1))  # advance to next char\n"
        "    return count"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("waiting = defaultdict(list)", {"code": True}), (" — 26 implicit lists keyed by character; words will wait here for their next needed char.", {})])),
    N.para(N.rich([("waiting[w[0]].append((w, 1))", {"code": True}), (" — enroll each word; index=1 means 'w[0] will be matched when this bucket fires; w[1] is what I need next.'", {})])),
    N.para(N.rich([("advance = waiting[c]; waiting[c] = []", {"code": True}), (" — atomically collect and clear the bucket. Clearing before re-inserting prevents a word whose next char is also c from being processed twice on the same s-character.", {})])),
    N.para(N.rich([("if i == len(w): count += 1", {"code": True}), (" — index has gone past the last character, meaning all len(w) characters were matched in order. Valid subsequence confirmed.", {})])),
    N.para(N.rich([("waiting[w[i]].append((w, i+1))", {"code": True}), (" — word still has chars to match; re-enroll in the bucket for its next needed character w[i].", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Two-Pointer (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each word, independently check if it is a subsequence of s using two pointers."),
        N.h4("What Doesn't Work"),
        N.para("This works correctly but rescans s from the beginning for every word. For large n and large s, it times out."),
        N.h4("The Key Observation"),
        N.para("Two-pointer subsequence check: walk pointer i through word and pointer j through s. When word[i] == s[j], advance i. If i reaches len(word), the word matched."),
        N.h4("Building the Solution"),
        N.para("Wrap the two-pointer check in a helper, apply it to every word, sum results."),
    ]),
    N.h3("Code"),
    N.code(
        "def numMatchingSubseq_brute(s, words):\n"
        "    def is_subseq(w, s):\n"
        "        i = 0  # pointer into w\n"
        "        for c in s:\n"
        "            if i < len(w) and c == w[i]:\n"
        "                i += 1\n"
        "        return i == len(w)\n"
        "    return sum(is_subseq(w, s) for w in words)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("i = 0", {"code": True}), (" — pointer into w; tracks how many chars of w have been matched so far.", {})])),
    N.para(N.rich([("if i < len(w) and c == w[i]: i += 1", {"code": True}), (" — when s's current char matches w's current needed char, advance the w pointer.", {})])),
    N.para(N.rich([("return i == len(w)", {"code": True}), (" — True if we consumed all of w's characters in order.", {})])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (two-pointer per word)", "O(n × |s|)", "O(1)"],
        ["Bucket by First Char (optimal)", "O(|s| + Σ|wᵢ|)", "O(Σ|wᵢ|)"],
        ["Binary Search (next-char arrays)", "O(|s|·26 + n·|w|·log|s|)", "O(|s|·26)"],
    ]),
    N.divider(),
]

# ── Pattern classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bucket by First Char", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Many subsequence queries against the same string s\n"
        "• Each query has a 'current need' that changes incrementally as it makes progress\n"
        "• Need to batch-process events by trigger value (e.g., 'what fires when c appears?')\n"
        "• Analogous to: event-driven simulation, Aho-Corasick, multi-pointer dispatch",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Is Subsequence", {"bold": True}), (" (#392, Easy) — Two-pointer check for a single word; the fundamental building block for this problem.", {})])),
    N.bullet(N.rich([("Shortest Way to Form String", {"bold": True}), (" (#1055, Medium) — Minimum number of passes over s to build target as a subsequence; similar bucket advance thinking.", {})])),
    N.bullet(N.rich([("Minimum Window Subsequence", {"bold": True}), (" (#727, Hard) — Find shortest substring of s containing t as a subsequence; subsequence matching inside a sliding window.", {})])),
    N.bullet(N.rich([("Longest Common Subsequence", {"bold": True}), (" (#1143, Medium) — Classic DP that builds on the subsequence structure; related conceptually to understanding what a subsequence is.", {})])),
    N.bullet(N.rich([("Distinct Subsequences", {"bold": True}), (" (#115, Hard) — Count the number of ways to form t as a subsequence of s using DP.", {})])),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (#438, Medium) — Sliding window with character hash; similar batch-scan mindset against a single string.", {})])),
    N.para("These problems share the core insight: process a single string s efficiently for multiple queries by batching or pre-processing rather than repeating full scans."),
    N.divider(),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch words advance through buckets as s is scanned character by character.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
