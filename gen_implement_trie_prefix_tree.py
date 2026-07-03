"""
gen_implement_trie_prefix_tree.py
Notion in-place update for LeetCode #208 — Implement Trie (Prefix Tree)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8108-8085-f937f8d811a3"

# 1) Set page properties
N.set_properties(PAGE_ID,
    difficulty="Medium",
    number=208,
    pattern="Tries",
    subpatterns=["Node with Children Array/Map"],
    tc="O(m)",
    sc="O(ALPHA * n)",
    key_insight="Every walk is identical: follow one edge per char from root, bail if missing; is_end distinguishes words from prefixes.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build new body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure — a Trie (Prefix Tree) — that supports three operations:\n", {}),
        ("insert(word)", {"code": True}), (" — Insert a word into the trie.\n", {}),
        ("search(word)", {"code": True}), (" — Return ", {}), ("True", {"code": True}),
        (" if the exact word exists in the trie (not just a prefix).\n", {}),
        ("startsWith(prefix)", {"code": True}),
        (" — Return ", {}), ("True", {"code": True}),
        (" if any inserted word starts with the given prefix.", {})
    ])),
    N.divider()
]

# Solution 1 — Optimal (Interview Pick)
sol1_code = '''\
class TrieNode:
    def __init__(self):
        self.children = {}     # char -> TrieNode
        self.is_end   = False  # True if a word ends exactly here

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end   # NOT True — this is the critical distinction

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True  # path exists -> some word has this prefix
'''

blocks += [
    N.h2("Solution 1 — TrieNode + Dict Children (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure where all words that share a prefix share the same initial storage. Think of it as a tree of characters: from the root, each edge represents one character. Any path from root to a marked node spells out a stored word."),
        N.h4("What Doesn't Work"),
        N.para("A hash set handles exact lookup in O(m). But 'does any word start with X?' requires scanning every stored word — O(total characters). There's no structural relationship between words in a hash set. For prefix queries to be O(m), we need prefix sharing baked into the structure."),
        N.h4("The Key Observation"),
        N.para("All words sharing a prefix travel the same initial path in the tree. So prefix lookups are free: just walk the path and check if it exists. The only way to distinguish 'app' (a complete word) from 'app' as a prefix of 'apple' is a boolean flag — is_end — on each node."),
        N.h4("Building the Solution"),
        N.para("Each node stores: (1) a children dict mapping char to TrieNode, (2) is_end=False. The Trie holds only the root. Every operation walks from root one character at a time. insert creates missing nodes and sets is_end=True at the end. search walks and returns node.is_end. startsWith walks and returns True. All three are O(m) where m is the word/prefix length."),
        N.callout(
            "Analogy: A Trie is like a directory tree for words. 'app', 'apple', and 'ape' all share the 'a/p' directory. You don't re-create that directory for each word — you reuse it.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode:", {"code": True}), " — Defines one node. Each node is a branching point in the tree."])),
    N.para(N.rich([("self.children = {}", {"code": True}), " — Dict mapping character → child TrieNode. Grows lazily (only chars we've seen)."])),
    N.para(N.rich([("self.is_end = False", {"code": True}), " — False by default; set True when a complete word ends at this node."])),
    N.para(N.rich([("self.root = TrieNode()", {"code": True}), " — The universal anchor. Every walk starts here. Has no character itself."])),
    N.para(N.rich([("for c in word:", {"code": True}), " — We descend one edge per character."])),
    N.para(N.rich([("if c not in node.children:", {"code": True}), " — If no edge for this character exists, create it (new TrieNode)."])),
    N.para(N.rich([("node = node.children[c]", {"code": True}), " — Move to the child, whether newly created or already existing."])),
    N.para(N.rich([("node.is_end = True", {"code": True}), " — After consuming all chars, mark: a word ends here."])),
    N.para(N.rich([("return node.is_end", {"code": True}), " — In search(): NOT return True. is_end distinguishes words from prefixes. This is the critical line."])),
    N.para(N.rich([("return True", {"code": True}), " — In startsWith(): if we didn't fall off the tree, some word has this prefix. We don't care about is_end."])),
    N.divider()
]

# Solution 2 — Array Children
sol2_code = '''\
class TrieNode:
    def __init__(self):
        self.children = [None] * 26   # fixed 26 slots, a=0 ... z=25
        self.is_end   = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _idx(self, c):
        return ord(c) - ord('a')

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            i = self._idx(c)
            if not node.children[i]:
                node.children[i] = TrieNode()
            node = node.children[i]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            i = self._idx(c)
            if not node.children[i]:
                return False
            node = node.children[i]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            i = self._idx(c)
            if not node.children[i]:
                return False
            node = node.children[i]
        return True
'''

blocks += [
    N.h2("Solution 2 — TrieNode + Fixed Array Children (ASCII-only Optimisation)"),
    N.toggle_h3("💡 Intuition: Fixed Array vs Dict", [
        N.h4("Reframe the Problem"),
        N.para("For ASCII-only lowercase inputs, we know exactly 26 possible characters. Instead of a hash dict, use a fixed array of 26 slots indexed by ord(c) - ord('a'). Slot 0 = 'a', slot 1 = 'b', ..., slot 25 = 'z'."),
        N.h4("What Doesn't Work"),
        N.para("For Unicode inputs, a 26-slot array fails — we'd need arrays of size 65536+ or hash maps. The dict approach handles any alphabet."),
        N.h4("The Key Observation"),
        N.para("Array indexing avoids hashing overhead and has better cache locality. Each node always pre-allocates 26 pointers. This trades memory (26 slots even for rarely-branching nodes) for slightly faster access."),
        N.h4("Building the Solution"),
        N.para("Identical logic to Solution 1, but node.children is a list of 26 Nones. Access via ord(c)-ord('a') index. Null check replaces 'in' dict check."),
        N.callout("Trade-off: Dict is memory-efficient (sparse). Array is cache-friendly (dense). For LeetCode problems with lowercase letters only, both work; array is marginally faster.", "⚖️", "yellow_background")
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.divider()
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",              "Time (insert/search/startsWith)", "Space"],
        ["Dict children (Sol 1)", "O(m) per operation",              "O(ALPHA × total_chars) — only used chars"],
        ["Array children (Sol 2)","O(m) per operation",              "O(26 × total_chars) — all slots pre-allocated"],
    ]),
    N.para("m = length of word or prefix. total_chars = sum of all inserted character counts. The dict version uses less space when branching is sparse; the array version has no hash overhead."),
    N.divider()
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Node with Children Array/Map"])),
    N.callout(
        "When to recognize this pattern: The problem requires prefix-based queries (startsWith, autocomplete, word validation by prefix). You need O(m) prefix lookups independent of the number of stored words. A hash set can't answer 'does any word start with X?' in O(m).",
        "🔎", "green_background"
    ),
    N.divider()
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie technique:"),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie + DFS for '.' wildcard matching using recursive child iteration"])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — Trie of word list + DFS backtracking on grid; prune via Trie to avoid redundant paths"])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), " (Medium) — Trie to find shortest stored root/prefix for each word in a sentence"])),
    N.bullet(N.rich([("Longest Word in Dictionary", {"bold": True}), " (Medium) — BFS on Trie visiting only is_end nodes (word built character by character)"])),
    N.bullet(N.rich([("Map Sum Pairs", {"bold": True}), " (Medium) — Trie storing integer values; sum all values in prefix subtree"])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), " (Medium) — Trie autocomplete returning up to 3 lexicographically smallest words per prefix"])),
    N.bullet(N.rich([("Maximum XOR of Two Numbers in an Array", {"bold": True}), " (Medium) — Binary Trie on bit representation; greedy XOR maximization bit by bit"])),
    N.para("These problems share the same Trie walk pattern: follow one edge per character, bail if missing, check is_end when needed."),
    N.divider()
]

# Interactive embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("implement_trie_prefix_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
