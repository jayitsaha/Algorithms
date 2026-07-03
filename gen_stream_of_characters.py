"""
gen_stream_of_characters.py — Notion update for LeetCode #1032 Stream of Characters
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81e8-b5d4-f0714141492d"

# ── 1. Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1032,
    pattern="Tries",
    subpatterns=["Reverse Trie"],
    tc="O(m) per query",
    sc="O(W·L)",
    key_insight="Reverse dictionary words and insert into Trie; maintain active node set per query for O(m) suffix matching.",
    icon="🔴"
)
print("Properties set OK")

# ── 2. Wipe old body ──
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} old blocks")

# ── 3. Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a data structure that accepts a stream of characters and checks, after each character is appended, whether any suffix of the stream matches any word in a given dictionary.\n\n"),
        ("Implement ", {}),
        ("StreamChecker", {"code": True}),
        (" with:\n• ", {}),
        ("StreamChecker(words)", {"code": True}),
        (" — initialises with a list of words.\n• ", {}),
        ("query(letter)", {"code": True}),
        (" — adds ", {}),
        ("letter", {"code": True}),
        (" to the stream and returns ", {}),
        ("True", {"code": True}),
        (" if any suffix of the stream equals a word in the dictionary, ", {}),
        ("False", {"code": True}),
        (" otherwise.", {}),
    ])),
    N.para(N.rich([
        ("Example: words=[\"cd\",\"f\",\"kl\"]. Stream receives 'a','b','c','d','f'.\n"),
        ("• query('a')=False, query('b')=False, query('c')=False\n"),
        ("• query('d')=False  (suffix \"d\" not in words, \"cd\" not yet complete)\n"),
        ("• query('f')=True   (suffix \"f\" matches word \"f\")\n\n"),
        ("Constraints: 1 ≤ words.length ≤ 2000, 1 ≤ words[i].length ≤ 2000, 1 ≤ query calls ≤ 40000.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Reverse Trie + Active Set ──
sol1_code = '''\
class TrieNode:
    def __init__(self):
        self.children = {}     # char -> TrieNode
        self.is_end = False    # True if completes a reversed word

class StreamChecker:
    def __init__(self, words):
        self.root = TrieNode()
        for word in words:
            node = self.root
            for ch in reversed(word):   # insert reversed word
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True
        self.active = {self.root}       # live partial-match nodes

    def query(self, letter: str) -> bool:
        nxt = {self.root}               # always seed root
        for node in self.active:
            if letter in node.children:
                nxt.add(node.children[letter])
        self.active = nxt
        return any(n.is_end for n in nxt)
'''

blocks += [
    N.h2("Solution 1 — Reverse Trie + Active Node Set (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must answer: after each new character, does the stream end with any dictionary word? This is an online suffix-matching problem — we cannot batch all queries; each answer must come immediately per character."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: buffer the full stream, then on each character scan every word checking str.endswith(). O(W·m) per query. For W=2000 words, m=2000 max length, Q=40000 queries → 160 billion character comparisons. Too slow."),
        N.h4("The Key Observation"),
        N.para("Tries match prefixes efficiently. But we need suffix matching — the newest character is always on the right. Insight: if we reverse every dictionary word before inserting into a Trie, then walking the Trie left-to-right with each incoming character exactly corresponds to reading stream suffixes right-to-left. Suffix matching becomes prefix matching."),
        N.h4("Building the Solution"),
        N.para("Insert all reversed words into a Trie. Between queries, maintain an 'active node set' — nodes representing partial matches in progress. On each query: (1) always add root (new match can start), (2) advance every active node via the new character edge, (3) check if any resulting node is a word-end. Dead paths automatically drop off when no edge exists."),
        N.callout(
            "Analogy: Imagine parallel explorers, each walking a different word backwards through the Trie. Every new character either advances each explorer one step or eliminates them. A new explorer spawns from root on every character. If any explorer reaches the end of their word — match!",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Reverse Trie with Active Set"),
    N.para(N.rich([
        ("This technique is a specialisation of multi-pattern matching for the specific case of suffix (not arbitrary substring) matching on an online stream.\n\n"),
        ("Origin: ", {"bold": True}),
        ("Derived from standard Trie prefix-matching; the reversal trick is a common interview-level insight. The more general version is Aho-Corasick (1975) which handles arbitrary substring positions via failure links.\n\n"),
        ("Core invariant: ", {"bold": True}),
        ("The active node set after processing character c[i] contains exactly the Trie nodes reachable by reading the reversed stream from position i backwards for any length 1 ≤ k ≤ m.\n\n"),
        ("Why it works: ", {"bold": True}),
        ("Every suffix of length k ending at position i corresponds to the k-length prefix of the reversed stream-suffix. The Trie stores all reversed words. Walking root→ch1→ch2→... visits exactly those reversed-word prefixes. The active set tracks all simultaneously.\n\n"),
        ("Generalization: ", {"bold": True}),
        ("For arbitrary substring matching (not just suffixes), use Aho-Corasick: build a Trie then add failure links so mismatches jump to the longest matching suffix — handles any position, not just the current end.\n\n"),
        ("Recognize when: ", {"bold": True}),
        ("Online stream + 'does stream END with any word' + multiple patterns → Reverse Trie with active set."),
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("TrieNode.__init__", {"code": True}), " — Two fields: ", ("children", {"code": True}), " maps each character to a child node; ", ("is_end", {"code": True}), " marks whether a complete reversed word ends here."])),
    N.para(N.rich([("__init__ loop", {"code": True}), " — For each word, traverse it in reverse order (", ("reversed(word)", {"code": True}), ") and walk/create Trie nodes. Final node gets ", ("is_end=True", {"code": True}), ". 'cd' → walk 'd','c'; last node at 'c' is marked end."])),
    N.para(N.rich([("self.active = {self.root}", {"code": True}), " — Active set starts with just root. On the very first query, root is present so we immediately try to advance via the first character."])),
    N.para(N.rich([("nxt = {self.root}", {"code": True}), " — Critical: always seed the next active set with root. Every incoming character could be the start of a new word match."])),
    N.para(N.rich([("for node in self.active:", {"code": True}), " — Advance every live partial match. If a node has an edge for ", ("letter", {"code": True}), ", its child becomes part of the next active set. If not, that path silently dies."])),
    N.para(N.rich([("return any(n.is_end for n in nxt)", {"code": True}), " — After advancing, check if any active node is a word-end. If yes, the stream's current suffix matches a dictionary word."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
sol2_code = '''\
class StreamChecker:
    def __init__(self, words):
        self.words = set(words)
        self.buf = []
        self.maxlen = max(len(w) for w in words)

    def query(self, letter: str) -> bool:
        self.buf.append(letter)
        if len(self.buf) > self.maxlen:
            self.buf.pop(0)         # trim oldest chars beyond maxlen
        s = ''.join(self.buf)
        return any(s.endswith(w) for w in self.words)
'''

blocks += [
    N.h2("Solution 2 — Brute Force Buffer + endswith (For Reference)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Keep a rolling buffer of the last m characters (m = max word length). On each query, check if the buffer string ends with any dictionary word."),
        N.h4("What Doesn't Work (at Scale)"),
        N.para("For large inputs this is O(W·m) per query. With W=2000 words and m=2000 max length, each of 40000 queries does up to 4 million character comparisons. Exceeds time limits."),
        N.h4("The Key Observation"),
        N.para("Trimming the buffer to maxlen is a useful optimization even for brute force — we only need the last maxlen characters since no word is longer than that. This reduces space from O(Q) to O(m)."),
        N.h4("Building the Solution"),
        N.para("Append letter to buf. Pop from front if buf exceeds maxlen. Join and check all words with endswith. Straightforward; propose this in an interview before optimizing."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.maxlen", {"code": True}), " — Only need to store the last ", ("maxlen", {"code": True}), " chars. No word can match a suffix longer than the longest word."])),
    N.para(N.rich([("self.buf.pop(0)", {"code": True}), " — Remove oldest character when buffer exceeds maxlen. Keeps space at O(m) not O(Q)."])),
    N.para(N.rich([("any(s.endswith(w) for w in self.words)", {"code": True}), " — Check every dictionary word as a possible suffix of the current buffer. Python's ", ("str.endswith()", {"code": True}), " is O(len(w)) per call."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Build Time", "Per Query", "Space", "Notes"],
        ["Brute Force", "O(W)", "O(W·m)", "O(m + W·L)", "Too slow for large inputs"],
        ["Reverse Trie + Active Set ✓", "O(W·L)", "O(m)", "O(W·L)", "Optimal; classic Trie reversal trick"],
        ["Aho-Corasick", "O(W·L·Σ)", "O(1) amortized", "O(W·L·Σ)", "Overkill for suffix-only; better for substring"],
    ]),
    N.para("W = number of words, L = max word length, m = max word length (same as L), Σ = alphabet size. Q = number of queries."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Reverse Trie — insert reversed words so suffix matching in stream becomes prefix matching in Trie; maintain Active Node Set for simultaneous multi-path tracking."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Characters arrive online (one at a time, cannot batch)\n"
        "• 'Does the stream END with any dictionary word?' → suffix matching\n"
        "• Multiple patterns must be checked simultaneously → Trie for shared prefixes\n"
        "• Need to track multiple partial matches in parallel → active node set\n"
        "• New character arrives at right end of stream → reverse words to align with Trie's left-to-right traversal",
        "🔎", "green_background"
    ),
    N.para("Note: The 'Reverse Trie' sub-pattern is based on analysis — it is a specific technique within the Trie pattern for online suffix-matching scenarios."),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or closely related Trie patterns:"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Foundation: build the core insert/search/startsWith Trie structure (#208)"])),
    N.bullet(N.rich([("Add and Search Word", {"bold": True}), " (Medium) — Trie with wildcard '.' matching using DFS at ambiguous nodes (#211)"])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — Find all dictionary words on a 2D board; Trie prunes the backtracking exponential space (#212)"])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), " (Medium) — Replace each word in a sentence with its shortest dictionary root using Trie prefix lookup (#648)"])),
    N.bullet(N.rich([("Palindrome Pairs", {"bold": True}), " (Hard) — Uses reversed-string Trie trick to find pairs forming palindromes — same reversal insight (#336)"])),
    N.bullet(N.rich([("Design Search Autocomplete System", {"bold": True}), " (Hard) — Online Trie + history tracking for top-3 suggestions per character input (#642)"])),
    N.bullet(N.rich([("Maximum XOR of Two Numbers in Array", {"bold": True}), " (Medium) — Binary Trie; shows Trie generalizes beyond character strings to bit sequences (#421)"])),
    N.para("These problems share the technique of preprocessing a dictionary into a Trie to enable efficient per-character online decisions. The Reverse Trie variant specifically solves the suffix-vs-prefix alignment problem in streaming contexts."),
    N.callout("📚 Pattern: Tries → Reverse Trie sub-pattern. Source: Analysis. Closest guide section: Trie / Data Structure Design patterns.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("stream_of_characters")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
