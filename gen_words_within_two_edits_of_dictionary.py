"""
Notion updater for: Words Within Two Edits of Dictionary (LC 2452)
Pattern: Tries | Subpattern: Trie + Edit Distance
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-811e-a8dc-c64be6a2288b"

# ── 1) Set Properties ─────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2452,
    pattern="Tries",
    subpatterns=["Trie + Edit Distance"],
    tc="O((D+Q)·W)",
    sc="O(D·W)",
    key_insight="Build Trie from dictionary; DFS each query tracking mismatch count; prune when edits > 2 since Hamming distance is monotonically non-decreasing.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing page body ────────────────────────────────
print("Wiping old content...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Build new page body ────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given two arrays of strings queries and dictionary — all strings of the same length — "
    "return a list of all queries that differ from any string in dictionary by at most 2 character "
    "substitutions (i.e., Hamming distance ≤ 2). "
    "Return the result in any order."
)

SOL1_CODE = '''\
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.is_end = False  # True if a complete dict word ends here

class Solution:
    def twoEditWords(self, queries: list[str], dictionary: list[str]) -> list[str]:
        # Build Trie from dictionary
        root = TrieNode()
        for word in dictionary:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

        def dfs(node, query, idx, edits):
            # Prune: already too many mismatches — skip entire subtree
            if edits > 2:
                return False
            # Terminal: consumed all query chars — match only if complete dict word
            if idx == len(query):
                return node.is_end
            # Explore each child branch
            for ch, child in node.children.items():
                new_edits = edits + (ch != query[idx])  # +1 on mismatch, +0 on match
                if dfs(child, query, idx + 1, new_edits):
                    return True  # Early exit on first match
            return False

        return [q for q in queries if dfs(root, q, 0, 0)]
'''

SOL2_CODE = '''\
class Solution:
    def twoEditWords(self, queries: list[str], dictionary: list[str]) -> list[str]:
        def hamming(a: str, b: str) -> int:
            """Hamming distance: count position-wise mismatches."""
            return sum(x != y for x, y in zip(a, b))

        result = []
        for q in queries:
            # Check if q is within 2 edits of ANY dictionary word
            if any(hamming(q, d) <= 2 for d in dictionary):
                result.append(q)
        return result

# Time:  O(Q * D * W)  — every query vs every dict word, every char
# Space: O(1)          — no auxiliary data structure
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('queries = ["word","note","ants","wood"], dictionary = ["wood","joke","moat"]\n'
         'Output: ["word","note","wood"]\n'
         '"word" vs "wood" → 1 edit (r↔o); "note" vs "moat" → 2 edits; "wood" is identical.')
    ])),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Trie + DFS with Edit-Distance Pruning (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "All strings have equal length, so full Levenshtein edit distance isn't needed. "
            "Only substitutions count — that's Hamming distance. "
            "We just need to find if any dictionary word has Hamming distance ≤ 2 from the query."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: compare every query against every dictionary word character by character. "
            "O(Q × D × W). Works, but if D and Q are both large and words are long (W up to 100), "
            "this is O(Q × D × 100) — too slow. Also wasteful: if two dictionary words share a prefix "
            "that already mismatches the query 3 times, we're still checking both words fully."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Hamming distance is monotonically non-decreasing. "
            "If we've compared the first d characters and already found 3 mismatches, "
            "no matter what the remaining W-d characters are, the total will be ≥ 3. "
            "So we can prune: once edits > 2, skip the entire subtree. "
            "A Trie groups words by shared prefix — words sharing a prefix share the same "
            "mismatch count for that prefix. Checking once covers all of them."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build a Trie from all dictionary words — one insert per word O(W). "
            "2. For each query, DFS the Trie passing the current mismatch count. "
            "3. At each node, try each child: new_edits = edits + (child_char != query[idx]). "
            "4. If edits > 2 at any point, return False immediately (prune). "
            "5. At depth W with is_end=True and edits ≤ 2: return True (match). "
            "6. Propagate True upward immediately without exploring more branches."
        ),
        N.callout(
            "Analogy: Think of the Trie as a decision tree. Each level is one character position. "
            "Each branch represents one possible character. We carry a 'budget' of 2 mismatches. "
            "The moment we overspend (edits=3), we close that entire subtree — no word down "
            "that path can help us. This is branch-and-bound applied to Hamming distance.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("TrieNode.__init__", {"code": True}), " — Each node stores children (dict of char→node) and is_end flag marking complete dictionary words."])),
    N.para(N.rich([("root = TrieNode()", {"code": True}), " — Create the Trie root with no character. All dictionary words share this entry point."])),
    N.para(N.rich([("for word in dictionary", {"code": True}), " — Insert every dictionary word into the Trie character by character, creating nodes as needed."])),
    N.para(N.rich([("node.is_end = True", {"code": True}), " — Mark the last node of each inserted word, so DFS knows a complete word ends there."])),
    N.para(N.rich([("if edits > 2: return False", {"code": True}), " — The prune. Hamming distance is monotone: once we exceed 2, no path below can ever return to ≤ 2."])),
    N.para(N.rich([("if idx == len(query): return node.is_end", {"code": True}), " — Consumed all query characters. Only accept if this is a complete dictionary word (not just a prefix)."])),
    N.para(N.rich([("new_edits = edits + (ch != query[idx])", {"code": True}), " — Python bool-to-int: True=1 (mismatch), False=0 (match). Elegant one-liner to increment on mismatch."])),
    N.para(N.rich([("if dfs(...): return True", {"code": True}), " — Early exit. Once one match is found, bubble True all the way up without exploring any other branches."])),
    N.para(N.rich([("return [q for q in queries if dfs(root, q, 0, 0)]", {"code": True}), " — Apply the DFS filter to every query. Each query starts a fresh DFS from root with 0 edits."])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Hamming Distance"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Since all strings have equal length, edit distance is just Hamming distance — "
            "count positions where characters differ. No need for full Levenshtein DP."
        ),
        N.h4("What Doesn't Work at Scale"),
        N.para(
            "This is O(Q × D × W). For the given constraints (Q, D ≤ 100, W ≤ 100), "
            "it's fast enough. But at larger scales (millions of words), this would be too slow. "
            "The Trie solution reduces repeated work across words sharing common prefixes."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The sum(x != y for x, y in zip(a, b)) idiom is idiomatic Python for Hamming distance. "
            "It's clean, readable, and correct. Always state this solution first in an interview "
            "before proposing the Trie optimization."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each query, use Python's any() with a generator to check all dictionary words. "
            "any() short-circuits on the first True — no need to check remaining words once a match is found."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("sum(x != y for x, y in zip(a, b))", {"code": True}), " — Hamming distance: zip pairs up characters by position, (x != y) gives True/False (1/0), sum counts mismatches."])),
    N.para(N.rich([("any(hamming(q, d) <= 2 for d in dictionary)", {"code": True}), " — Short-circuit check: stops as soon as one dictionary word is within 2 edits. No need to check remaining words."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(Q · D · W)", "O(1)"],
        ["Trie + DFS (Interview Pick)", "O((D+Q) · W)", "O(D · W)"],
    ]),
    N.para("D = |dictionary|, Q = |queries|, W = word length. Trie build is O(D·W); each query DFS is O(26·W) in worst case with pruning reducing average cost."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie + Edit Distance (Hamming Distance Pruning via DFS)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Fixed-length strings — edit distance reduces to Hamming distance. "
        "(2) 'Within k edits/substitutions of any dictionary word' phrasing. "
        "(3) Multiple queries against a fixed dictionary — build Trie once, query many times. "
        "(4) Need to avoid redundant work across words sharing common prefixes.",
        "🔎", "green_background"
    ),
    N.para(
        "Note: This problem is classified as 'Tries' on LeetCode. The specific sub-pattern "
        "'Trie + Edit Distance' refers to the technique of performing bounded-distance search "
        "through a Trie with DFS pruning — a natural extension of prefix matching to approximate matching."
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie / bounded Hamming distance / DFS with pruning):"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — LC 208: Core Trie insert/search/startsWith. Master this first."])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — LC 211: Trie DFS with wildcard '.' — same DFS branching logic."])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — LC 212: Trie + backtracking DFS on a 2D grid. Classic Trie application."])),
    N.bullet(N.rich([("Edit Distance", {"bold": True}), " (Hard) — LC 72: Full Levenshtein distance with DP. Use when words have different lengths."])),
    N.bullet(N.rich([("Minimum Genetic Mutation", {"bold": True}), " (Medium) — LC 433: BFS with Hamming distance = 1 per step; same equal-length bounded-edit concept."])),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), " (Hard) — LC 127: BFS graph of single-char substitutions; Hamming distance drives edge construction."])),
    N.bullet(N.rich([("Spell Checker", {"bold": True}), " (Medium) — LC 966: Exact match + vowel permutation + edit distance; practical spelling-correction application."])),
    N.para("These problems share the theme of bounded-distance search in a word space. Key unifier: all exploit that equal-length strings allow Hamming distance instead of full Levenshtein, enabling simpler counting and more efficient pruning."),
    N.callout("📚 Reference: Tries pattern — LC tag 'Trie'. Related tags: String, Array, Hash Table.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("words_within_two_edits_of_dictionary")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
