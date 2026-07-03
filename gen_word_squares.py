"""gen_word_squares.py — Notion update for Word Squares (#425)."""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8117-8541-cf7a4a968f1f"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=425,
    pattern="Tries",
    subpatterns=["Trie + Backtracking"],
    tc="O(n·L·26^L)",
    sc="O(n·L)",
    key_insight="Symmetry constraint forces each new row's prefix; Trie stores word lists at every node for O(L) prefix queries.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a set of words (without duplicates), return all the ", {}),
        ("word squares", {"bold": True}),
        (" you can build from them. A word square is a sequence of k words where the ", {}),
        ("k-th row and k-th column read the same string", {"bold": True}),
        (". Example: [\"ball\",\"area\",\"lead\",\"lady\"] forms a valid 4×4 word square because col 0 = \"ball\", col 1 = \"area\", col 2 = \"lead\", col 3 = \"lady\".", {})
    ])),
    N.divider(),
]

# ── Solution 1: Trie + Backtracking ────────────────────────────────────────
sol1_code = '''\
from collections import defaultdict

def wordSquares(words):
    n = len(words[0])          # side of the square
    trie = {}

    def insert(word):
        node = trie
        for ch in word:
            node = node.setdefault(ch, {'#': []})
            node['#'].append(word)  # store full word at every prefix node

    def get_words(prefix):
        node = trie
        for ch in prefix:
            if ch not in node:
                return []         # prefix absent → prune
            node = node[ch]
        return node['#']          # O(1) return after O(L) walk

    for word in words:
        insert(word)

    results = []

    def backtrack(step, square):
        if step == n:
            results.append(square[:])   # copy, not reference
            return
        # key constraint: column 'step' must be prefix of row 'step'
        prefix = ''.join(square[i][step] for i in range(step))
        for word in get_words(prefix):
            square.append(word)
            backtrack(step + 1, square)
            square.pop()          # undo (backtrack)

    for word in words:            # try every word as row 0
        backtrack(1, [word])

    return results
'''

sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We need to fill an n×n grid with n words such that row k = column k for every k. Think of it as: place words one row at a time, but each row's first k characters are already determined by what you've placed in previous rows."),
    N.h4("What Doesn't Work"),
    N.para("Trying all permutations of n words (brute force) is O(n!) — with n=50 words, completely intractable. Even scanning all n words for each of n row positions naively is O(n^n · L)."),
    N.h4("The Key Observation"),
    N.para("Symmetry: square[i][j] = square[j][i]. So once k words are placed, the k-th column is partially written — it tells us exactly what prefix the (k+1)-th word must have. This is a prefix constraint, and prefix queries scream 'Trie'."),
    N.h4("Building the Solution"),
    N.para("1. Build a Trie that stores the full word list at every prefix node (not just leaves). 2. For each starting word (row 0), backtrack: compute prefix from column k, query Trie, recurse for each candidate, undo. 3. Prune immediately when get_words returns []."),
    N.callout("Analogy: It's like Sudoku — partial state constrains future choices, and you backtrack when a constraint is violated. The Trie is your 'constraint checker' — it tells you which words are still valid given what's in column k.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Trie + Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("🔬 Algorithm Deep-Dive: Enhanced Trie"),
    N.para(N.rich([
        ("Enhanced Trie (word lists at every node)", {"bold": True}),
        (" — A standard Trie stores a word only at its terminal node. An enhanced Trie also stores the word at every ancestor node. This transforms prefix queries from O(subtree DFS) to O(L walk + O(1) return). Space cost: each word W of length L is stored L times — once at each node on its path. Total: O(n·L) word references, sharing node structure.", {})
    ])),
    N.code("# Standard Trie node: {char: child_node, ...}\n# Enhanced Trie node: {char: child_node, '#': [word1, word2, ...]}\n#\n# insert(\"ball\"):\n#   root['b']['#'] = [..., 'ball']\n#   root['b']['a']['#'] = [..., 'ball']\n#   root['b']['a']['l']['#'] = [..., 'ball']\n#   root['b']['a']['l']['l']['#'] = [..., 'ball']\n#\n# get_words('ba') → walk b→a → return node['#'] = ['ball']  # O(1)"),
    N.para("The invariant: at any point during backtracking with k words placed, square[i][j] = square[j][i] for all i,j < k. Placing word W as row k enforces W[j] = square[j][k] for j < k — which is exactly what the prefix constraint checks."),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(words[0])", {"code": True}), (" — All words have the same length. n is the side length of the square.", {})])),
    N.para(N.rich([("node.setdefault(ch, {'#': []})", {"code": True}), (" — If character ch is not a child of node, create a new node with an empty word list. Return the child node.", {})])),
    N.para(N.rich([("node['#'].append(word)", {"code": True}), (" — Store the full word at this prefix node. Critical: we do this for EVERY node on the path, not just the leaf.", {})])),
    N.para(N.rich([("if ch not in node: return []", {"code": True}), (" — Prefix not in Trie → no words have this prefix → prune this branch immediately.", {})])),
    N.para(N.rich([("prefix = ''.join(square[i][step] for i in range(step))", {"code": True}), (" — Extract column 'step' from the k rows already placed. This is the required prefix for the next word.", {})])),
    N.para(N.rich([("for word in get_words(prefix)", {"code": True}), (" — Iterate only words that start with the required prefix. If list is empty, loop doesn't execute → immediate backtrack.", {})])),
    N.para(N.rich([("square.append(word); backtrack(step+1, square); square.pop()", {"code": True}), (" — Classic backtracking: place → recurse → undo. The pop() restores square to its state before this iteration.", {})])),
    N.para(N.rich([("results.append(square[:])", {"code": True}), (" — Append a COPY of square (not the list itself), because square will be modified by subsequent backtracking.", {})])),
    N.divider(),
]

# ── Solution 2: Prefix Hash Map ─────────────────────────────────────────────
sol2_code = '''\
from collections import defaultdict

def wordSquares(words):
    n = len(words[0])

    # Precompute: prefix → list of words with that prefix
    prefix_map = defaultdict(list)
    for word in words:
        for i in range(n + 1):          # include full word and empty prefix
            prefix_map[word[:i]].append(word)

    results = []

    def backtrack(step, square):
        if step == n:
            results.append(square[:])
            return
        prefix = ''.join(square[i][step] for i in range(step))
        for word in prefix_map.get(prefix, []):
            square.append(word)
            backtrack(step + 1, square)
            square.pop()

    for word in words:
        backtrack(1, [word])

    return results
'''

sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Same as Solution 1 — we need prefix queries for candidate lookup. The question is: what data structure holds the prefix-to-words mapping?"),
    N.h4("What Doesn't Work"),
    N.para("A plain dict keyed by full word doesn't help — we need partial prefix lookups. Sorting doesn't help directly since we're querying arbitrary prefixes."),
    N.h4("The Key Observation"),
    N.para("We can precompute ALL prefixes of ALL words upfront and store them in a hash map. This is O(n·L²) space (each word contributes L+1 prefix strings of average length L/2) but is trivially simple to implement."),
    N.h4("Building the Solution"),
    N.para("For each word, insert it under every prefix (including the empty string and the full word). Then backtracking is identical to Solution 1 — just use prefix_map.get(prefix, []) instead of get_words(prefix)."),
]

blocks += [
    N.h2("Solution 2 — Prefix Hash Map + Backtracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("prefix_map = defaultdict(list)", {"code": True}), (" — Maps prefix string → list of words sharing that prefix.", {})])),
    N.para(N.rich([("for i in range(n+1): prefix_map[word[:i]].append(word)", {"code": True}), (" — word[:0]='', word[:1]=first char, ..., word[:n]=full word. Each word is inserted under n+1 keys. O(n*L^2) total space.", {})])),
    N.para(N.rich([("prefix_map.get(prefix, [])", {"code": True}), (" — O(1) hash lookup. Returns [] if prefix never seen, enabling immediate pruning.", {})])),
    N.para("Trade-off vs Trie: prefix map is simpler to implement and equally fast asymptotically, but uses more memory — O(n·L²) vs O(n·L) — because it stores the actual prefix strings as keys rather than sharing prefix characters through Trie nodes."),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all permutations)", "O(n! · L)", "O(n)"],
        ["Backtrack + linear scan", "O(n^n · L)", "O(n)"],
        ["Prefix Hash Map + Backtrack", "O(n·L·26^L)", "O(n·L²)"],
        ["Trie + Backtrack (Optimal)", "O(n·L·26^L)", "O(n·L)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie + Backtracking", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Find ALL valid arrangements' with prefix constraints linking multiple elements. (2) Symmetry or diagonal constraints in a grid — row k = col k. (3) Repeated prefix queries during search where precomputation pays off. (4) Backtracking where candidate lists are filtered by a shared structure.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie + Backtracking technique:"),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Find all words from a list in a 2D board; Trie prunes DFS paths in real-time (#212)", {})])),
    N.bullet(N.rich([("Palindrome Pairs", {"bold": True}), (" (Hard) — Find all pairs where concatenation is palindrome; Trie for reverse prefix matching (#336)", {})])),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Build the core data structure used in this problem (#208)", {})])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), (" (Medium) — Trie with wildcard '.' matching — backtracking within the Trie itself (#211)", {})])),
    N.bullet(N.rich([("N-Queens", {"bold": True}), (" (Hard) — Place n queens; same backtrack template + constraint propagation (#51)", {})])),
    N.bullet(N.rich([("Sudoku Solver", {"bold": True}), (" (Hard) — Fill grid satisfying row/col/box constraints; backtrack at each cell (#37)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Replace words with shortest root prefix; Trie prefix walk (#648)", {})])),
    N.para("These problems share the same core technique: Trie for fast prefix lookup + backtracking with early pruning."),
    N.callout("📚 Reference: Trie + Backtracking sub-pattern. Key signal: 'all valid arrangements' + prefix constraint linking elements.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed("https://jayitsaha.github.io/Algorithms/word_squares_explainer.html"),
    N.para(N.rich([("Step through the Trie-guided backtracking algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
