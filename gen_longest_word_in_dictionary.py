"""
gen_longest_word_in_dictionary.py
Regenerates the Notion page for LeetCode #720 Longest Word in Dictionary
IN-PLACE using page_id 39193418-809c-81a6-a638-c783b1aac780
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81a6-a638-c783b1aac780"

# ─── 1) Set properties ───
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=720,
    pattern="Tries",
    subpatterns=["Trie + BFS Valid Words"],
    tc="O(sum of word lengths)",
    sc="O(sum of word lengths)",
    key_insight="Build a Trie; BFS only expands from nodes that are complete words, enforcing the full prefix-chain invariant by induction.",
    icon="🟡"
)
print("Properties set OK")

# ─── 2) Wipe old content ───
print("Wiping old page content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

# ─── 3) Build body blocks ───
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of strings ", {}),
        ("words", {"code": True}),
        (" representing an English Dictionary, return the ", {}),
        ("longest word in words", {"bold": True}),
        (" that can be built one character at a time by other words in ", {}),
        ("words", {"code": True}),
        (". If there is more than one possible answer, return the longest word with the smallest lexicographical order. If there is no answer, return an empty string.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ('words = ["w","wo","wor","worl","world"] → "world"', {"code": True}),
            (' because "w"→"wo"→"wor"→"worl"→"world" — every prefix is in the dictionary.', {}),
        ]),
        "📌", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Trie + BFS ──
blocks += [
    N.h2("Solution 1 — Trie + BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a word whose entire 'building sequence' exists in the dictionary. For 'world' to qualify, the words 'w', 'wo', 'wor', 'worl', 'world' must ALL be in the list. This is a prefix-chain constraint."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: For each word W of length n, check if all n prefixes are in a hash set. That's O(N × L × L) — L lookups per word, each taking O(L) time to hash. For large inputs this is too slow."),
        N.h4("The Key Observation"),
        N.para("A Trie PHYSICALLY encodes prefix relationships. If we insert all words into a Trie and mark terminals, then a node at depth D is reachable from root via a valid word-chain if and only if every ancestor node on that path is also a terminal (a complete word). BFS on the Trie, restricted to terminal nodes, naturally enforces this."),
        N.h4("Building the Solution"),
        N.para("1. Insert all words into a Trie, marking each terminal with node.word = word.\n2. Seed BFS with root's children (depth-1 nodes = single-char words).\n3. On each dequeue: if node.word is empty, skip (prefix chain broken). Otherwise update best answer.\n4. Push all children to queue — invalid ones get filtered on dequeue."),
        N.callout("Analogy: Think of the Trie as a ladder where each rung is a word. BFS climbs the ladder, but only steps on rungs that are solid (complete words). If a rung is missing, the rest of that branch is unreachable — we never try to climb past it.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.word = ""      # full word if terminal, else ""

def longestWord(words: list[str]) -> str:
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word  # mark terminal with full word

    res = ""
    queue = deque(root.children.values())
    while queue:
        node = queue.popleft()
        if not node.word:          # not a complete word → skip
            continue
        w = node.word
        if len(w) > len(res) or (len(w) == len(res) and w < res):
            res = w
        queue.extend(node.children.values())
    return res"""),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode:", {"code": True}), " — defines one node per character in the trie. Each node has a children dict (char→child) and a word field."])),
    N.para(N.rich([("self.word = \"\"", {"code": True}), " — stores the full word string at terminal nodes; empty string at non-terminals. This lets us recover the word during BFS without retracing the root path."])),
    N.para(N.rich([("root = TrieNode()", {"code": True}), " — root has no character. It represents the empty prefix. All depth-1 children are single-character words."])),
    N.para(N.rich([("for word in words:", {"code": True}), " — insert each word into the trie by walking/creating one node per character."])),
    N.para(N.rich([("node.word = word", {"code": True}), " — marks the end of a word. We store the FULL string, not just True, so BFS can retrieve it without retracing the path."])),
    N.para(N.rich([("queue = deque(root.children.values())", {"code": True}), " — seeds BFS with all depth-1 nodes. These correspond to single-character words. Single-char words are valid by definition (empty prefix is trivially ok)."])),
    N.para(N.rich([("if not node.word: continue", {"code": True}), " — THIS IS THE KEY LINE. If a node is not a complete word, its prefix chain is broken. We skip it and never expand from it, so its entire subtree is unreachable."])),
    N.para(N.rich([("if len(w) > len(res) or (len(w) == len(res) and w < res):", {"code": True}), " — update best: prefer longer words; break ties by taking the lexicographically smaller one."])),
    N.para(N.rich([("queue.extend(node.children.values())", {"code": True}), " — push ALL children, not just word-end children. Invalid children will be filtered on dequeue by the 'if not node.word: continue' check."])),
    N.divider(),
]

# ── Solution 2: Sort + Hash Set ──
blocks += [
    N.h2("Solution 2 — Sort + Hash Set (Simpler to Code)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to check, for each word, whether all its prefixes are in the dictionary. If we could process shorter words before longer ones, we could build up a 'valid prefix' set incrementally."),
        N.h4("What Doesn't Work"),
        N.para("Without sorting, checking all prefixes of each word requires O(L) set lookups per word. With sorting, we only need to check the IMMEDIATE prefix (length L-1), because all shorter prefixes were already validated when we processed shorter words."),
        N.h4("The Key Observation"),
        N.para("Sort words lexicographically. Shorter words appear before longer ones with the same prefix (e.g., 'wo' before 'wor'). Process words in sorted order: if word[:-1] is in the 'seen' set, then word's entire prefix chain is valid (by induction — its length L-1 prefix was valid, and so were all its prefixes)."),
        N.h4("Building the Solution"),
        N.para("1. Sort words.\n2. Start with seen = {\"\"} (empty string is the valid base).\n3. For each word: if word[:-1] in seen → add word to seen, update result if longer.\n4. Since sorted, first word at any length is lex-smallest — no tie-break needed."),
        N.callout("Sorted order gives tiebreaking for free: the first word of length L we encounter (in sorted order) is always lex-smallest at that length.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def longestWord(words: list[str]) -> str:
    words.sort()           # lex order: shorter before longer extensions
    seen = {""}            # empty str = valid base prefix
    res = ""
    for word in words:
        if word[:-1] in seen:   # immediate prefix validated?
            seen.add(word)      # word is now a valid prefix for longer words
            if len(word) > len(res):  # first at this length = lex smallest
                res = word
    return res"""),
    N.h3("Line by Line"),
    N.para(N.rich([("words.sort()", {"code": True}), " — sorts lexicographically. Crucially, shorter words appear before any of their extensions (e.g., 'w' before 'wo' before 'wor')."])),
    N.para(N.rich([('seen = {""}', {"code": True}), " — includes the empty string as the base case. This allows single-character words to pass the check: word[:-1] = '' which is in seen."])),
    N.para(N.rich([("if word[:-1] in seen:", {"code": True}), " — checks only the immediate prefix (length L-1). If it's valid, then by induction all shorter prefixes were valid too (we processed them earlier in sorted order)."])),
    N.para(N.rich([("if len(word) > len(res):", {"code": True}), " — only update on strictly-longer (not equal). Since we iterate in sorted order, the first word of any given length is already lex-smallest — no need to compare lex order explicitly."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Trie + BFS", "O(Σ|w|)", "O(Σ|w|) for Trie nodes"],
        ["Sort + Hash Set", "O(N log N + Σ|w|)", "O(Σ|w|) for the seen set"],
        ["Brute Force (all prefix checks)", "O(N × L²)", "O(N × L)"],
    ]),
    N.callout("Σ|w| means the sum of all word lengths. For N words of average length L, this is O(N×L). The Trie solution is asymptotically optimal — it processes each character exactly once during insert and at most once during BFS.", "📊", "gray_background"),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Trie + BFS Valid Words — BFS on a Trie restricted to complete-word nodes enforces prefix-chain validity by structural induction."])),
    N.callout(
        N.rich([
            ("When to recognize this pattern:\n", {"bold": True}),
            ("• Problem asks whether a word can be 'built' or 'grown' one char at a time from a dictionary\n", {}),
            ("• Constraint is that every prefix of the answer must also be in the dictionary\n", {}),
            ("• You need to find the 'deepest reachable node' in a prefix structure\n", {}),
            ("• Multiple strings share long common prefixes (Trie amortizes the cost)", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie prefix-chain technique:"),
    N.bullet(N.rich([("208. Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Build the core Trie data structure; prerequisite for all Trie problems."])),
    N.bullet(N.rich([("211. Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie with wildcard '.' search using DFS."])),
    N.bullet(N.rich([("212. Word Search II", {"bold": True}), " (Hard) — Trie + backtracking on a 2D character grid; classic Trie application."])),
    N.bullet(N.rich([("648. Replace Words", {"bold": True}), " (Medium) — Find shortest dictionary root that is a prefix of a given word."])),
    N.bullet(N.rich([("1268. Search Suggestions System", {"bold": True}), " (Medium) — Trie for real-time auto-complete suggestions."])),
    N.bullet(N.rich([("336. Palindrome Pairs", {"bold": True}), " (Hard) — Reversed-word Trie for palindrome pair detection."])),
    N.bullet(N.rich([("421. Maximum XOR of Two Numbers in an Array", {"bold": True}), " (Medium) — Binary Trie traversal for XOR maximization."])),
    N.para("These problems share the core pattern: build a Trie from a string collection, then traverse it structurally (BFS or DFS) to answer queries that would otherwise require O(L) hash-set lookups per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trie section. Sub-pattern: Trie + BFS Valid Words (also known as 'Incremental Word Building')", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_word_in_dictionary")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4) Append blocks ───
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
