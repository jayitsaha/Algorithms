"""
gen_word_search_ii.py — Notion update for Word Search II (#212, Hard)
Pattern: Tries | Sub-Pattern: Trie + DFS Backtracking
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8195-ac98-cd2ba76e0fde"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=212,
    pattern="Tries",
    subpatterns=["Trie + DFS Backtracking"],
    tc="O(M·N·4·3^(L-1))",
    sc="O(W·L)",
    key_insight="Build a Trie from all words; use it to guide DFS on the board, pruning dead prefixes instantly instead of searching for each word independently.",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"code": True}),
        (" board of characters and a list of strings ", {}),
        ("words", {"code": True}),
        (", return all words in ", {}),
        ("words", {"code": True}),
        (" that can be found in the board. A word must be constructed from letters of sequentially adjacent cells (horizontally or vertically neighbouring). The same letter cell may not be used more than once in a word.", {})
    ])),
    N.para("Example: board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"] → [\"eat\",\"oath\"]"),
    N.divider(),
]

# ── Solution 1: Trie + DFS Backtracking (Interview Pick) ──
SOL1_CODE = '''\
class TrieNode:
    def __init__(self):
        self.children = {}   # letter -> TrieNode
        self.word = None     # complete word string at terminal; None otherwise

def findWords(board, words):
    # Phase 1: Build Trie from all words
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = word  # store full word at terminal for easy retrieval

    ROWS, COLS = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        # Prune: cell already visited OR letter not in Trie prefix
        if ch == '#' or ch not in node.children:
            return
        next_node = node.children[ch]   # descend one Trie level

        if next_node.word:              # complete word found!
            result.append(next_node.word)
            next_node.word = None       # clear to prevent duplicates

        board[r][c] = '#'               # mark visited (in-place backtracking)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                dfs(nr, nc, next_node)
        board[r][c] = ch                # RESTORE — critical backtrack step

        # Trie pruning: if this branch is now empty, remove it
        if not next_node.children:
            del node.children[ch]

    # Phase 2: Start DFS from every board cell
    for r in range(ROWS):
        for c in range(COLS):
            dfs(r, c, root)

    return result
'''

blocks += [
    N.h2("Solution 1 — Trie + DFS Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Find all words from a list that can be traced on a grid by moving through adjacent cells without revisiting any cell. This is Word Search I (finding one word via DFS) extended to many words simultaneously."),
        N.h4("What Doesn't Work"),
        N.para("Running a separate DFS for each word — O(W × M × N × 4 × 3^L) — is too slow for large W or long words. Thousands of DFS passes share no work even when words share prefixes like 'EAT', 'EACH', 'EARTH'."),
        N.h4("The Key Observation"),
        N.para("A Trie encodes all words such that prefix validity is checkable in O(1) per step. If we carry a Trie node during DFS instead of a word index, one DFS pass simultaneously searches all words. When the board letter is not in the current Trie node's children, we prune immediately — no word can continue from here."),
        N.h4("Building the Solution"),
        N.para("1. Build Trie from all words. Each TrieNode has children dict and word field (stores word at terminals). 2. DFS from every board cell, passing the current TrieNode as state. 3. At each cell, descend the Trie. If descent fails → prune. If terminal reached → record word. 4. Mark cells '#' before recursing, restore after (backtracking). 5. Clear word field after recording to prevent duplicates. 6. Delete childless Trie nodes to shrink the search space."),
        N.callout("Analogy: The Trie is like a GPS that knows all destination addresses simultaneously. Instead of driving to check each destination separately, you follow the GPS which prunes invalid turns in real-time — if no word starts with 'ZZ', the GPS says 'stop' the moment you hit 'ZZ' on the board.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("TrieNode.__init__", {"code": True}), " — Two fields: children (letter→TrieNode dict) and word (None at interior nodes, word string at terminals)."])),
    N.para(N.rich([("root = TrieNode()", {"code": True}), " — Trie root represents the empty prefix — all words start here."])),
    N.para(N.rich([("node.word = word", {"code": True}), " — At the terminal TrieNode for each word, we store the complete word string. This lets us retrieve the word without reconstructing it from the path."])),
    N.para(N.rich([("if ch == '#' or ch not in node.children: return", {"code": True}), " — Two pruning conditions: '#' means this cell is already in the current path (visited); ch not in children means no target word continues with this letter from this Trie state."])),
    N.para(N.rich([("next_node = node.children[ch]", {"code": True}), " — Descend one level in the Trie. The Trie node and board path always stay synchronized."])),
    N.para(N.rich([("result.append(next_node.word); next_node.word = None", {"code": True}), " — Record found word, then clear to prevent duplicates if another board path reaches the same terminal."])),
    N.para(N.rich([("board[r][c] = '#'", {"code": True}), " — Mark the current cell visited in-place. '#' is not a letter so it triggers the prune check at the top of DFS."])),
    N.para(N.rich([("board[r][c] = ch", {"code": True}), " — CRITICAL restore step. After all neighbors are explored, put the original letter back so other DFS calls (from different starting cells or paths) see the correct board."])),
    N.para(N.rich([("if not next_node.children: del node.children[ch]", {"code": True}), " — Trie pruning. If a node has no children after all its descendants were found or exhausted, remove it from its parent. This progressively shrinks the Trie, making future DFS calls faster."])),
    N.para(N.rich([("for r, c: dfs(r, c, root)", {"code": True}), " — Launch DFS from every board cell. We must try all starting positions since a word can begin anywhere."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOL2_CODE = '''\
def findWords_brute(board, words):
    """O(W × M × N × 4 × 3^L) — separate DFS per word, no prefix sharing."""
    ROWS, COLS = len(board), len(board[0])

    def exist(word):
        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or r >= ROWS or c < 0 or c >= COLS:
                return False
            if board[r][c] != word[i]:
                return False
            tmp = board[r][c]
            board[r][c] = '#'
            found = any(
                dfs(r + dr, c + dc, i + 1)
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
            )
            board[r][c] = tmp
            return found

        return any(
            dfs(r, c, 0)
            for r in range(ROWS)
            for c in range(COLS)
        )

    return [w for w in words if exist(w)]
'''

blocks += [
    N.h2("Solution 2 — Brute Force: DFS Per Word"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each word, independently search the board using Word Search I logic: try every cell as a starting point, DFS with backtracking."),
        N.h4("What Doesn't Work at Scale"),
        N.para("This is O(W × M × N × 4 × 3^L). For W=100 words, a 10×10 board, L=10 length: ~100 × 100 × 4 × 19683 ≈ 8 billion operations. For the Trie approach: same DFS cost but once, not W times."),
        N.h4("The Key Observation"),
        N.para("No prefix sharing: searching 'EAT' and 'EACH' both traverse E→A independently. The Trie makes 'EAT'/'EACH' share the E→A exploration and only branch at position 3."),
        N.h4("When to Use"),
        N.para("Only use brute force when: W is very small (1-3 words), words are very short, or as a reference implementation to verify correctness of the Trie solution."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def exist(word)", {"code": True}), " — For each word, run a full independent board search."])),
    N.para(N.rich([("if board[r][c] != word[i]: return False", {"code": True}), " — At each step, the board letter must match the current word letter — no Trie guidance, just direct comparison."])),
    N.para(N.rich([("tmp = board[r][c]; board[r][c] = '#'", {"code": True}), " — Same backtracking trick as the Trie solution: mark visited, explore, restore."])),
    N.para(N.rich([("return [w for w in words if exist(w)]", {"code": True}), " — Run exist() for every word, collect those found. Each exist() is an independent O(M×N×4×3^L) search."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (DFS per word)", "O(W·M·N·4·3^(L-1))", "O(L) stack"],
        ["Trie + DFS Backtracking ✓", "O(M·N·4·3^(L-1))", "O(W·L) Trie"],
    ]),
    N.para("W = number of words, M×N = board dimensions, L = max word length. The Trie removes the W factor from the search cost by handling all words in one pass."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie + DFS Backtracking"])),
    N.callout(
        "When to recognize this pattern: (1) 'Find all words from a dictionary on a grid' — Trie + DFS. "
        "(2) Multiple string search where words share prefixes — Trie for O(1) prefix checking. "
        "(3) 'Spell words by moving adjacently on a board' — DFS backtracking + Trie guide. "
        "(4) Boggle-style game problems — same pattern.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie + DFS Backtracking):"),
    N.bullet(N.rich([("Word Search", {"bold": True}), " (Medium) — Single-word DFS without Trie; the simpler predecessor to this problem. Understand this first (#79)"])),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Build the exact data structure used here; essential to master before Word Search II (#208)"])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie with '.' wildcard matching; DFS through multiple Trie branches (#211)"])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), " (Hard) — Trie + DFS/DP to enumerate all ways to segment a string into dictionary words (#140)"])),
    N.bullet(N.rich([("Concatenated Words", {"bold": True}), " (Hard) — Trie lookup to determine if words are composed of shorter dictionary words (#472)"])),
    N.bullet(N.rich([("Stream of Characters", {"bold": True}), " (Hard) — Reversed Trie for suffix matching in a character stream (#1032)"])),
    N.para("These problems all share the core technique: Trie for O(1) prefix/word lookup + DFS/backtracking for path exploration."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Tries. Sub-Pattern: Trie + DFS Backtracking. Source: Analysis (canonical Trie + Backtracking problem).", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("word_search_ii")),
    N.para(N.rich([
        ("Step through the Trie + DFS algorithm visually — watch the board cells highlight as DFS explores, see the Trie node state update with each step, observe backtracking in action. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
