"""
gen_concatenated_words.py — Notion update for Concatenated Words (#472)
Notion page ID: 39193418-809c-813f-a089-cc7138d22539
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813f-a089-cc7138d22539"

# ── 1. Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=472,
    pattern="Tries",
    subpatterns=["Trie + DP"],
    tc="O(n·L²)",
    sc="O(n·L)",
    key_insight="Sort by length, test each word against a growing Trie using Word Break DP before inserting it — prevents self-use while ensuring all valid components are available.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe existing body ──
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build body blocks ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of strings ", {}),
        ("words", {"code": True}),
        (", return all the ", {}),
        ("concatenated words", {"bold": True}),
        (" in the given list of ", {}),
        ("words", {"code": True}),
        (". A ", {}),
        ("concatenated word", {"bold": True}),
        (" is defined as a string that is comprised entirely of at least two shorter words in the given array. The word must be formed by concatenating two or more other words from the list — it cannot use itself.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('words = ["cat","cats","catsdogcats","dog","rat"] → ["catsdogcats"] because "cats"+"dog"+"cats" all exist in the list.', {}),
    ])),
    N.divider(),
]

# ── Solution 1: Trie + DP ──
blocks += [
    N.h2("Solution 1 — Trie + DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each word in the list, ask: can this word be entirely covered by two or more other words from the same list? This is exactly the Word Break problem (#139) — applied to every word as a candidate, with the word itself excluded from its own dictionary."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each word, try every possible split recursively. Without memoization, the number of ways to split a word of length L is O(2^L) — exponential. Even with memoization, probing a hash set for every possible substring word[i:j] costs O(L³) per word (O(L) pairs × O(L) substring copy). On large inputs this is too slow."),
        N.h4("The Key Observation"),
        N.para("Two insights combine: (1) A concatenated word must be strictly longer than each of its components. So if we sort by length and process shortest-first, when testing word W, all valid components are already in our data structure. (2) A Trie lets us do all prefix lookups in a single O(L) walk from each starting position, instead of O(L) separate hash probes."),
        N.h4("Building the Solution"),
        N.para("Sort words by length. Initialize an empty Trie. For each word: (a) run Word Break DP using the Trie for prefix matching — dp[i]=True means word[0:i] is coverable; (b) if dp[n]=True, add to results; (c) insert the word into the Trie for future candidates. The sort+insert-after-test trick elegantly prevents self-use without any extra bookkeeping."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of the Trie as a growing dictionary. Each word gets tested against only the words that came before it (shorter ones). If it can be assembled from those smaller building blocks, it's concatenated. Then it graduates into the dictionary for even longer words to use.", {})]),
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code('''class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def findAllConcatenatedWordsInADict(words):
    words.sort(key=len)           # shortest first: components precede candidates
    root = TrieNode()
    result = []

    def insert(word):
        node = root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def canForm(word):
        n = len(word)
        dp = [False] * (n + 1)
        dp[0] = True              # base: empty prefix is reachable
        for i in range(n):
            if not dp[i]:
                continue          # skip unreachable positions
            node = root
            for j in range(i, n):
                if word[j] not in node.children:
                    break         # Trie dead end — prune
                node = node.children[word[j]]
                if node.is_end:
                    if i == 0 and j == n - 1:
                        continue  # would use entire word as single piece
                    dp[j + 1] = True
        return dp[n]

    for word in words:
        if canForm(word):         # test BEFORE inserting (no self-use)
            result.append(word)
        insert(word)              # now available as component for longer words
    return result'''),
    N.h3("Line by Line"),
    N.para(N.rich([("words.sort(key=len)", {"code": True}), (" — Sort shortest-first so components always precede candidates in processing order.", {})])),
    N.para(N.rich([("root = TrieNode()", {"code": True}), (" — Start with an empty Trie; it grows as each word is inserted after testing.", {})])),
    N.para(N.rich([("insert(word)", {"code": True}), (" — Standard Trie insertion: walk/create nodes for each character, mark the final node with is_end=True.", {})])),
    N.para(N.rich([("dp = [False] * (n + 1); dp[0] = True", {"code": True}), (" — DP array of size n+1. dp[i]=True means word[0:i] can be fully covered by Trie words. dp[0]=True seeds the reachability propagation.", {})])),
    N.para(N.rich([("if not dp[i]: continue", {"code": True}), (" — Skip unreachable positions: no point starting a Trie walk if we can't reach position i.", {})])),
    N.para(N.rich([("node = root; for j in range(i, n):", {"code": True}), (" — Start a fresh Trie walk from the root at each reachable position i. Extend character by character.", {})])),
    N.para(N.rich([("if word[j] not in node.children: break", {"code": True}), (" — Trie dead end: no dictionary word starts with this prefix. Stop early — this is where Trie beats hash probing.", {})])),
    N.para(N.rich([("if node.is_end: dp[j+1] = True", {"code": True}), (" — A complete Trie word ends at j. Mark position j+1 as reachable. The guard (i==0 and j==n-1) prevents counting the whole word as one piece.", {})])),
    N.para(N.rich([("canForm(word) before insert(word)", {"code": True}), (" — The critical ordering: test before inserting. Since the word is not in the Trie during its own test, it cannot satisfy its own DP using itself as a single component.", {})])),
    N.para(N.rich([("return dp[n]", {"code": True}), (" — dp[n]=True means the entire word is covered by Trie words via ≥2 pieces (guaranteed by the sort+insert-after strategy).", {})])),
    N.divider(),
]

# ── Solution 2: DFS + Memo ──
blocks += [
    N.h2("Solution 2 — DFS + Memoization + Set"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same reframe as Solution 1, but approached top-down instead of bottom-up. For a given word, try every possible first-piece (any prefix that is a dictionary word), then recursively check if the suffix can also be covered."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization: the same suffix can appear in many different recursive paths (e.g., for 'catcatcat', the suffix 'catcat' is explored from split 'c'+'atcatcat' and 'cat'+'catcat'). Without memoization, this leads to exponential recomputation."),
        N.h4("The Key Observation"),
        N.para("Each unique (suffix, is_first_call) pair is computed at most once with memoization. There are O(L) unique suffixes and 2 values for is_first, so O(L) memo entries. Each entry does O(L) work (trying each prefix). Total: O(L²) per word."),
        N.h4("Building the Solution"),
        N.para("Use a set for O(1) dictionary lookups. A boolean flag 'first' tracks whether we've consumed any piece yet. If 'not first' and the remaining string is in the word set, we're done (it counts as the last piece). Recurse on each valid prefix split with first=False."),
        N.callout("This approach is simpler to derive from scratch in an interview — start recursive, add memoization, explain the is_first flag. Then mention the Trie+DP optimization if asked.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code('''def findAllConcatenatedWordsInADict(words):
    word_set = set(words)   # O(1) membership
    memo = {}               # (suffix, is_first) -> bool

    def can_form(s, first=True):
        if (s, first) in memo:
            return memo[(s, first)]
        # If we\'ve already used at least one piece and s is a word, done
        if not first and s in word_set:
            return True
        # Try every prefix of s as the next piece
        for i in range(1, len(s)):
            prefix = s[:i]
            if prefix in word_set and can_form(s[i:], False):
                memo[(s, first)] = True
                return True
        return memo.setdefault((s, first), False)

    return [w for w in words if can_form(w)]'''),
    N.h3("Line by Line"),
    N.para(N.rich([("word_set = set(words)", {"code": True}), (" — O(1) average-case membership test. The word itself IS in the set, but the 'first=True' guard prevents using it as a single piece.", {})])),
    N.para(N.rich([("can_form(s, first=True)", {"code": True}), (" — first=True means this is the initial call on the full word; first=False means at least one piece has been consumed.", {})])),
    N.para(N.rich([("if not first and s in word_set: return True", {"code": True}), (" — We've already consumed at least one piece (first=False) and the remaining string is a whole word — valid ending!", {})])),
    N.para(N.rich([("for i in range(1, len(s)): prefix = s[:i]", {"code": True}), (" — Try every possible first-piece length (1 to len(s)-1). range starts at 1 so prefix is non-empty.", {})])),
    N.para(N.rich([("if prefix in word_set and can_form(s[i:], False):", {"code": True}), (" — If the prefix is a dictionary word AND the remaining suffix can also be covered, we have a valid split.", {})])),
    N.para(N.rich([("memo.setdefault((s, first), False)", {"code": True}), (" — Cache False result to avoid recomputing the same suffix+context later.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Recursion", "O(n · 2^L)", "O(L) stack"],
        ["DFS + Memo + Set", "O(n · L²)", "O(n · L) memo"],
        ["Trie + DP (optimal)", "O(n · L²)", "O(n · L) Trie"],
    ]),
    N.para("where n = number of words, L = maximum word length. Both memo and Trie+DP achieve O(n·L²) but the Trie version has better constants due to early Trie branch pruning."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie + DP", {})])),
    N.callout(
        N.rich([
            ("When to recognize Trie + DP: ", {"bold": True}),
            ("(1) 'Can this string be broken into dictionary words?' → Word Break DP. ", {}),
            ("(2) 'Need fast prefix lookup across many starting positions?' → Use Trie. ", {}),
            ("(3) 'Applied to every word in a list with self-exclusion?' → Sort + lazy Trie insert.", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie + DP technique:"),
    N.bullet(N.rich([("Word Break", {"bold": True}), (" (Medium) — Single-word decomposition into dictionary words; the direct sub-problem used in this solution (#139)", {})])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), (" (Hard) — Return all valid decompositions; DFS+Memo on top of the Word Break DP (#140)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Trie guides DFS on a 2D board to find all dictionary words efficiently (#212)", {})])),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Foundational Trie: insert, search, startsWith (#208)", {})])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), (" (Medium) — Trie with wildcard '.' matching via DFS (#211)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Use Trie to replace words with the shortest root prefix (#648)", {})])),
    N.bullet(N.rich([("Palindrome Pairs", {"bold": True}), (" (Hard) — Trie of reversed words to find all concatenated palindromes (#336)", {})])),
    N.para("These problems share the core technique: Trie for O(character) prefix matching + DP/DFS for combinatorial string decomposition."),
    N.callout("📚 Reference: Trie+DP is the canonical technique for 'decompose string into dictionary words' problems. Word Break (#139) is the simpler single-word version; Concatenated Words (#472) applies it at scale to all words as candidates.", "📚", "gray_background"),
]

# ── Visual Explainer embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("concatenated_words")),
    N.para(N.rich([
        ("Step through the Trie+DP walkthrough visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
