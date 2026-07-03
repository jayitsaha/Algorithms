"""
gen_design_add_and_search_words_data_structure.py
Notion page update for LeetCode #211 — Design Add and Search Words Data Structure
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8110-a365-e91e8f52ef5c"
SLUG = "design_add_and_search_words_data_structure"

# ─── 1. Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=211,
    pattern="Tries",
    subpatterns=["Trie + DFS for Wildcards"],
    tc="O(m) addWord, O(26^d * m) search",
    sc="O(N * m)",
    key_insight="Trie stores words by shared prefixes; wildcard '.' triggers recursive DFS over all existing children",
    icon="🟡",
)
print("Properties set.")

# ─── 2. Wipe existing body ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Build body blocks ─────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure that supports adding new words and finding if a string matches any previously added string.\n\n", {}),
        ("Implement the ", {}), ("WordDictionary", {"code": True}), (" class:\n", {}),
        ("• ", {}), ("WordDictionary()", {"code": True}), (" — Initializes the object.\n", {}),
        ("• ", {}), ("addWord(word)", {"code": True}), (" — Adds word to the data structure.\n", {}),
        ("• ", {}), ("search(word)", {"code": True}),
        (" — Returns true if any stored string matches word, where ", {}),
        ("'.'", {"code": True}), (" matches any letter. Otherwise returns false.", {}),
    ])),
    N.callout(N.rich([
        ("Example:\n", {"bold": True}),
        ("addWord(\"bad\"), addWord(\"dad\"), addWord(\"mad\")\n", {"code": True}),
        ("search(\"pad\") → False\n", {"code": True}),
        ("search(\"bad\") → True\n", {"code": True}),
        ("search(\".ad\") → True   # '.' matches b, d, or m\n", {"code": True}),
        ("search(\"b..\") → True   # two '.' each match any char", {"code": True}),
    ]), "📝", "gray_background"),
    N.divider(),
]

# ── Solution 1: Trie + Recursive DFS ──
SOL1_CODE = """\
class TrieNode:
    def __init__(self):
        self.children = {}   # char → TrieNode (only inserted letters are keys)
        self.is_end = False  # True if a complete word ends at this node

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()  # root = empty prefix; all paths start here

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True  # mark end of this word

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return node.is_end  # consumed all chars — is this a word endpoint?
            ch = word[i]
            if ch == '.':
                # Wildcard: branch into all existing children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True  # short-circuit on first success
                return False
            else:
                # Literal: follow exactly this edge (or fail if missing)
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], i + 1)
        return dfs(self.root, 0)
"""

blocks += [
    N.h2("Solution 1 — Trie + Recursive DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure for storing strings and matching patterns where '.' is a wildcard. This is a hybrid problem: part dictionary (store/retrieve strings efficiently), part pattern matching (handle wildcards). Ask: what structure organizes strings so wildcard matching stays tractable?"),
        N.h4("What Doesn't Work"),
        N.para("A hash set or hash map is perfect for exact matching in O(1), but breaks for wildcards. To match '.ad' against a set, you'd have to check every stored word character by character — O(n×m) per search where n is the number of words. That's essentially brute force."),
        N.h4("The Key Observation"),
        N.para("A Trie naturally groups words by shared prefixes. At any node in the Trie, the node's children represent the set of letters that appear next in some stored word. For a wildcard '.', instead of guessing which letter might match, we just try ALL existing children. This bounds the search to paths that were actually inserted — the Trie prunes dead ends automatically."),
        N.h4("Building the Solution"),
        N.para("1) TrieNode with children dict and is_end bool. 2) addWord: walk letter by letter creating nodes, mark is_end at the end — standard Trie insert, O(m). 3) search with recursive DFS: literal char → follow that edge; '.' → try every child; base case → return is_end. The recursive structure mirrors the trie structure perfectly."),
        N.callout("Analogy: think of the Trie as a directory tree. addWord creates folders along a path and marks the last one as a 'file'. search('.ad') opens the root, sees folders b, d, m (the wildcard tries all three), goes into each, follows 'a' and 'd', and checks if 'bad'/'dad'/'mad' are marked as files.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode:", {"code": True}), (" — Defines the building block. ", {}), ("children", {"code": True}), (" is a dict mapping chars to child nodes; only letters actually inserted appear as keys.", {})])),
    N.para(N.rich([("self.is_end = False", {"code": True}), (" — Boolean flag. When set to True, this node marks the endpoint of a complete stored word. Critical for distinguishing 'ba' from 'bad'.", {})])),
    N.para(N.rich([("self.root = TrieNode()", {"code": True}), (" — The root node represents the empty prefix. Every word path starts here. The root character is conceptually empty.", {})])),
    N.para(N.rich([("for ch in word:", {"code": True}), (" — addWord iterates character by character through the word, one Trie level per character.", {})])),
    N.para(N.rich([("if ch not in node.children:", {"code": True}), (" — If the edge for this character doesn't exist, create it. If it already exists (shared prefix), reuse it.", {})])),
    N.para(N.rich([("node = node.children[ch]", {"code": True}), (" — Move the current pointer one level deeper along the just-created or already-existing edge.", {})])),
    N.para(N.rich([("node.is_end = True", {"code": True}), (" — After consuming all characters, mark this node as a word endpoint. Inserting the same word twice is safe — it just re-marks the same node.", {})])),
    N.para(N.rich([("def dfs(node, i):", {"code": True}), (" — Recursive search helper. ", {}), ("node", {"code": True}), (" is the current Trie position; ", {}), ("i", {"code": True}), (" is the current index into the query word.", {})])),
    N.para(N.rich([("if i == len(word): return node.is_end", {"code": True}), (" — BASE CASE. We've consumed all query characters. Return True only if a complete word ends exactly here.", {})])),
    N.para(N.rich([("if ch == '.':", {"code": True}), (" — Wildcard branch: iterate ALL children. We call ", {}), ("node.children.values()", {"code": True}), (" (the child nodes, not the keys/chars) and recurse.", {})])),
    N.para(N.rich([("if dfs(child, i + 1): return True", {"code": True}), (" — Short-circuit OR logic: if any branch returns True, propagate True immediately without exploring remaining siblings.", {})])),
    N.para(N.rich([("if ch not in node.children: return False", {"code": True}), (" — Literal branch: if the required edge doesn't exist, this path was never inserted — fail immediately.", {})])),
    N.para(N.rich([("return dfs(node.children[ch], i + 1)", {"code": True}), (" — Follow the exact edge for the literal char and recurse one level deeper.", {})])),
    N.para(N.rich([("return dfs(self.root, 0)", {"code": True}), (" — Kick off DFS from the root at position 0. The closure captures ", {}), ("word", {"code": True}), (" from the outer ", {}), ("search", {"code": True}), (" method.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOL2_CODE = """\
class WordDictionary:
    def __init__(self):
        self.words = []  # flat list of all stored words

    def addWord(self, word: str) -> None:
        self.words.append(word)  # O(1) insert

    def search(self, word: str) -> bool:
        # For each stored word, check character by character
        for w in self.words:
            if len(w) != len(word):
                continue
            match = True
            for i in range(len(word)):
                if word[i] != '.' and word[i] != w[i]:
                    match = False
                    break
            if match:
                return True
        return False
    # Time: O(n * m) per search where n = words count, m = word length
    # This is the brute-force baseline to state before proposing Trie
"""

blocks += [
    N.h2("Solution 2 — Brute Force List Scan (Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest approach: just store all words in a list, then for each search, compare the query against every stored word character by character — treating '.' as a wildcard that matches anything."),
        N.h4("What Doesn't Work"),
        N.para("addWord is O(1), but search is O(n × m) where n is the total number of stored words and m is word length. For a large dictionary with many searches, this is unacceptably slow."),
        N.h4("The Key Observation"),
        N.para("This works correctly and is easy to implement. Use it to establish correctness in an interview before proposing the Trie optimization."),
        N.h4("Building the Solution"),
        N.para("Store words in a list. For search: filter by length first (quick O(1) check), then compare character by character allowing '.' to match anything."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "addWord", "search (literal)", "search (with d wildcards)", "Space"],
        ["Brute Force (List)", "O(1)", "O(n × m)", "O(n × m)", "O(n × m)"],
        ["Trie + DFS (Optimal)", "O(m)", "O(m)", "O(26^d × m)*", "O(N × m)"],
    ]),
    N.para("* d = number of '.' wildcards in the query. In practice, DFS only follows existing Trie edges so the branching factor is bounded by actual stored words, not a full 26 at every level."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie + DFS for Wildcards", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("'Design word dictionary with wildcard search' • Pattern matching where '.' matches exactly one char • Any problem combining prefix-organized storage (Trie) with backtracking search (DFS) • 'add strings, search with wildcards' API design", {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie + DFS for Wildcards technique:"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Foundation problem: standard Trie insert/search/startsWith without wildcards (#208)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Trie + DFS on a 2D board to find all dictionary words simultaneously (#212)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Trie to find and replace words with their shortest prefix (#648)", {})])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), (" (Medium) — Trie + DFS to collect top-3 word suggestions per typed prefix (#1268)", {})])),
    N.bullet(N.rich([("Wildcard Matching", {"bold": True}), (" (Hard) — '*' matches zero-or-more chars — requires DP, not Trie (#44)", {})])),
    N.bullet(N.rich([("Regular Expression Matching", {"bold": True}), (" (Hard) — '.' and '*' combined — classic DP/NFA problem (#10)", {})])),
    N.para("These problems share the core technique: a Trie organizes stored strings by shared prefixes; recursive DFS handles pattern characters by branching at wildcards and following exact edges at literals."),
    N.callout("📚 Sub-Pattern: Trie + DFS for Wildcards — Source: Analysis (Trie section in DSA patterns guide; wildcard DFS is the natural extension when '.' appears in queries)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print(f"NOTION OK {PAGE_ID}")
