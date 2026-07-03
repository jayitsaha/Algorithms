"""
gen_design_search_autocomplete_system.py
Regenerates the Notion page for LeetCode #642 — Design Search Autocomplete System.
notion_page_id = None → create a fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "design_search_autocomplete_system"
NAME = "Design Search Autocomplete System"
NUMBER = 642
DIFFICULTY = "Hard"
ICON = "🔴"
PATTERN = "Design"
SUBPATTERNS = ["Trie + Priority Queue"]
TC = "O(L + S log 3)"
SC = "O(N·L)"
KEY_INSIGHT = "Navigate trie to prefix node in O(L), DFS subtree to collect all matches, min-heap extracts top 3 by (-freq, lex)."

# ── Step 0: Create page (notion_page_id is None) ──────────────────────────────
print("Creating new Notion page...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────────────────
N.set_properties(PAGE_ID,
    difficulty=DIFFICULTY, number=NUMBER,
    pattern=PATTERN, subpatterns=SUBPATTERNS,
    tc=TC, sc=SC, key_insight=KEY_INSIGHT, icon=ICON)
print("Properties set.")

# ── Step 2: Wipe (fresh page has no body, but call for safety) ─────────────────
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} existing blocks.")

# ── Step 3: Build body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character ", {}),
        ("#", {"code": True}),
        ("). Return the top 3 historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than 3 hot sentences, return as many as you can. The returned results should be sorted by their hotness (number of times they have been typed), with ties broken lexicographically (a sentence with smaller ASCII value is returned first). Implement the ", {}),
        ("AutocompleteSystem", {"code": True}),
        (" class with: (1) ", {}),
        ("AutocompleteSystem(sentences, times)", {"code": True}),
        (" — initialize with historical sentences and their search frequencies, and (2) ", {}),
        ("input(c)", {"code": True}),
        (" — accepts the next character c. If c = '#', treat as end of sentence, store it with frequency += 1, reset prefix, return []. Otherwise append c to prefix and return top 3 matching sentences.", {})
    ])),
    N.divider()
]

# ── Solution 1: Trie + Min-Heap (Interview Pick) ───────────────────────────────
blocks += [
    N.h2("Solution 1 — Trie + Min-Heap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is a stateful search system. Each character typed either (a) narrows down matching sentences from history, or (b) ends a sentence (saves it). The core sub-problems are: (1) efficiently find all sentences starting with a given prefix, (2) efficiently rank and return top 3 from those candidates."),
        N.h4("What Doesn't Work"),
        N.para("The naive approach: store sentences in a dict, scan all N sentences on every keystroke to check if they start with the current prefix, then sort. For large N and long prefixes, this is O(N·L) per character — too slow for a real search system that might have millions of historical queries."),
        N.h4("The Key Observation"),
        N.para("A Trie organizes strings by their character-by-character structure. All sentences with the same prefix occupy the same subtree. So 'navigate to the prefix node in O(L) steps, then DFS the subtree' finds all matching sentences without touching irrelevant ones. Combine with a min-heap of size 3 for O(S log 3) ranking — far better than O(S log S) full sort."),
        N.h4("Building the Solution"),
        N.para("1. Build Trie: insert every (sentence, freq) pair. Terminal nodes store sentence + freq.\n2. On input(c) where c ≠ '#': append c to prefix, navigate trie to prefix node, DFS to collect all (−freq, sentence) pairs, call heapq.nsmallest(3, results) to rank.\n3. On input('#'): _insert(self.prefix, 1) — new sentence gets freq=1, existing bumps by 1. Reset prefix = ''."),
        N.callout("Analogy: The trie is like a filing system sorted by first letter, then second letter, etc. When you type 'i lo', you walk directly to the 'i-l-o' drawer and pull out only that drawer's contents — you never touch the 'a', 'b', ..., 'z' drawers at all.", "🗂️", "blue_background")
    ]),
    N.h3("Code"),
    N.code("""import heapq

class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode (dict handles spaces + any char)
        self.sentence = ""      # non-empty marks this as a terminal node
        self.freq = 0           # search frequency for this sentence

class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.root = TrieNode()  # root represents empty prefix
        self.prefix = ""        # accumulates typed chars between '#' resets
        for s, t in zip(sentences, times):
            self._insert(s, t)  # seed with historical data

    def _insert(self, sentence, freq):
        node = self.root
        for c in sentence:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.sentence = sentence    # mark terminal with full sentence text
        node.freq += freq           # += handles re-insertion of existing sentence

    def _dfs(self, node, results):  # collect all sentences in subtree
        if node.sentence:           # this node is a terminal
            results.append((-node.freq, node.sentence))  # negate for min-heap trick
        for child in node.children.values():
            self._dfs(child, results)

    def input(self, c):
        if c == '#':                    # sentence completion signal
            self._insert(self.prefix, 1)
            self.prefix = ""
            return []
        self.prefix += c                # extend current prefix
        node = self.root
        for ch in self.prefix:          # navigate to prefix node
            if ch not in node.children:
                return []              # prefix path broken → no matches
            node = node.children[ch]
        results = []
        self._dfs(node, results)       # collect all sentences in subtree
        # heapq.nsmallest(3, results): O(S log 3) vs O(S log S) for full sort
        return [s for _, s in heapq.nsmallest(3, results)]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode:", {"code": True}), " — Each trie node stores a dict of children (char→node), the sentence string (empty unless this is a terminal), and the frequency count for that sentence."])),
    N.para(N.rich([("self.children = {}", {"code": True}), " — Using a dict (not a 26-element array) is critical: sentences can contain spaces and other characters. The dict is sparse and handles any character set."])),
    N.para(N.rich([("self.prefix = \"\"", {"code": True}), " — Accumulates typed characters between '#' resets. This is the 'current session' state — what the user has typed so far."])),
    N.para(N.rich([("self._insert(s, t)", {"code": True}), " — Seed the trie with all historical sentences and their counts at initialization time. O(sum of sentence lengths) total."])),
    N.para(N.rich([("node.freq += freq", {"code": True}), " — Using += instead of = is crucial: if the user later types this sentence again (via '#'), we increment frequency rather than overwriting it. Works for both new inserts and updates."])),
    N.para(N.rich([("results.append((-node.freq, node.sentence))", {"code": True}), " — We negate frequency because heapq is a min-heap. By storing −freq, the sentence with the HIGHEST frequency becomes the 'smallest' tuple element. Lexicographic tie-breaking comes free from Python's tuple comparison."])),
    N.para(N.rich([("if ch not in node.children: return []", {"code": True}), " — Early exit: if any character in the current prefix has no trie path, no sentence can match. Return empty list immediately."])),
    N.para(N.rich([("heapq.nsmallest(3, results)", {"code": True}), " — Extracts 3 smallest (−freq, sentence) tuples in O(S log 3) time. Much better than sorted()[:3] which is O(S log S). The result is already in desired order: highest freq first, lex-sorted for ties."])),
    N.divider()
]

# ── Solution 2: HashMap + Sort (Brute Force) ───────────────────────────────────
blocks += [
    N.h2("Solution 2 — HashMap + Sort (Brute Force, O(N·L) per input)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Before optimizing, think: what is the simplest possible implementation? We need to store sentences with frequencies, and on each character find all matching ones. A dict maps sentence→freq. For lookup, just iterate all entries."),
        N.h4("What Doesn't Work at Scale"),
        N.para("Iterating all N sentences on every keystroke is O(N·L) where L is the prefix length. For 1 million historical sentences, this is too slow. But for small N (like in the problem examples), it works correctly and is easy to implement."),
        N.h4("The Key Observation"),
        N.para("str.startswith(prefix) is the Python way to check prefix match. Sorting with key=lambda x: (-x[0], x[1]) handles both descending frequency and ascending lexicographic order in a single sort call."),
        N.h4("Building the Solution"),
        N.para("Store counts in a dict. On each input: filter all sentences with startswith, sort by (-freq, sentence), return first 3. On '#': increment count in dict, reset prefix."),
        N.callout("Use this approach if the interviewer asks for the simplest solution first, then evolve to the Trie solution. It demonstrates clean thinking before optimization.", "⚡", "gray_background")
    ]),
    N.h3("Code"),
    N.code("""class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.counts = {}            # {sentence: frequency}
        for s, t in zip(sentences, times):
            self.counts[s] = t
        self.prefix = ""

    def input(self, c):
        if c == '#':
            self.counts[self.prefix] = self.counts.get(self.prefix, 0) + 1
            self.prefix = ""
            return []
        self.prefix += c
        p = self.prefix
        # O(N·L): check every sentence for prefix match
        matches = [(v, k) for k, v in self.counts.items() if k.startswith(p)]
        # O(N log N): sort by (-freq, sentence)
        matches.sort(key=lambda x: (-x[0], x[1]))
        return [s for _, s in matches[:3]]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.counts = {}", {"code": True}), " — Simple dict maps sentence string → integer frequency. No special structure needed for this approach."])),
    N.para(N.rich([("k.startswith(p)", {"code": True}), " — Python's built-in O(|p|) string operation checks if sentence k starts with prefix p. Runs once per sentence per keystroke."])),
    N.para(N.rich([("key=lambda x: (-x[0], x[1])", {"code": True}), " — Python sorts tuples element by element. Negating freq makes high-frequency items sort first. For equal freqs, sentence string provides lexicographic ordering."])),
    N.para(N.rich([("self.counts.get(self.prefix, 0) + 1", {"code": True}), " — .get with default 0 handles new sentences gracefully: they start at 0 + 1 = 1. Existing sentences get incremented."])),
    N.divider()
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Init Time", "input() Time", "Space"],
        ["HashMap + Sort", "O(N)", "O(N·L + N log N)", "O(N·L)"],
        ["Trie + Min-Heap ✓", "O(N·L)", "O(L + S log 3)", "O(N·L)"],
        ["Trie + Cached Top-3", "O(N·L²)", "O(L)", "O(N·L·K)"],
    ]),
    N.para("N = number of sentences, L = average sentence length, S = subtree size (matching sentences). Trie + Heap dominates for large N with frequent queries."),
    N.divider()
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design — stateful data structure supporting multiple operations (AutocompleteSystem class with __init__ + input methods)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie + Priority Queue — Trie for efficient prefix navigation; min-heap for top-K extraction with composite ranking criteria"])),
    N.callout("When to recognize this pattern: (1) 'Design a system' with prefix/autocomplete semantics → Trie. (2) 'Return top K' from large candidates with multi-key ranking → Min-heap of size K. (3) Stateful class with 'accumulate input' + 'commit on delimiter' → prefix + '#' reset pattern.", "🔎", "green_background"),
    N.para("Note: 'Trie + Priority Queue' sub-pattern synthesizes two classical structures for the Design category. The pattern guide's Trie section covers basic operations; the heap combination is classified by analysis."),
    N.divider()
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie prefix lookup and/or top-K heap ranking):"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Core trie operations: insert, search, startsWith — the foundation of this problem (#208)"])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — Use trie to simultaneously search for multiple words in a 2D board (#212)"])),
    N.bullet(N.rich([("Top K Frequent Words", {"bold": True}), " (Medium) — Min-heap with (−freq, word) tuples — identical ranking trick to this problem (#692)"])),
    N.bullet(N.rich([("Kth Largest Element in a Stream", {"bold": True}), " (Medium) — Min-heap of size K to maintain top-K dynamically as new elements arrive (#703)"])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), " (Medium) — Trie or sorted array for prefix suggestions, return top 3 — easier version of this problem (#1268)"])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie with wildcard '.' matching using DFS (#211)"])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), " (Medium) — Use trie to find shortest prefix replacement for words in a sentence (#648)"])),
    N.para("These problems share the trie-as-prefix-index pattern: store strings in a trie, navigate to a prefix node to efficiently access all strings with that prefix."),
    N.callout("📚 Reference: Trie problems cluster in 'Design' and 'String Processing' categories. The top-K heap pattern appears across Heap, Sorting, and Design categories in the DSA Patterns Guide.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | notion_page_id={PAGE_ID}")
