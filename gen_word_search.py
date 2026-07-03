"""Notion updater for Word Search (LeetCode #79)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8116-9a61-e45f4821fb1e"

print("Step 1: Setting page properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=79,
    pattern="Graph",
    subpatterns=["DFS Backtracking"],
    tc="O(m·n·4^L)",
    sc="O(L)",
    key_insight="Mark cells '#' on entry and restore on exit — backtracking ensures each cell is used at most once per path while remaining available for other paths.",
    icon="🟡"
)
print("  Properties set.")

print("Step 2: Wiping existing page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

print("Step 3: Building page body...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an ", {}),
        ("m×n", {"code": True}),
        (" grid of characters ", {}),
        ("board", {"code": True}),
        (" and a string ", {}),
        ("word", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if ", {}),
        ("word", {"code": True}),
        (" exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically). Each cell may only be used once per path.", {})
    ])),
    N.callout("Example: board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = 'ABCCED' → True (path: A(0,0)→B(0,1)→C(0,2)→C(1,2)→E(2,2)→D(2,1))", "📋", "gray_background"),
    N.divider(),
]

# ── Solution 1: DFS with In-Place Backtracking ──
blocks += [
    N.h2("Solution 1 — DFS with In-Place Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a graph (the grid) where each cell is a node. We want to know whether a path exists that visits nodes in an order that spells out the word, visiting each node at most once. This is fundamentally a path-existence search on a graph."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force enumeration of all paths is exponential and can't prune early. BFS finds shortest paths but doesn't naturally track visited-per-path state. We need DFS with backtracking — which prunes immediately when a character mismatches, and un-commits visited cells when a branch fails."),
        N.h4("The Key Observation"),
        N.para("We need cells to be 'in use' only during the current path exploration. After we backtrack from a branch, those cells should be available again. Temporarily replacing a cell's character with '#' (which never appears in the word) handles visited tracking without a separate data structure — the character mismatch check catches '#' automatically."),
        N.h4("Building the Solution"),
        N.para("1. Outer loop: try every cell as a starting point. 2. Recursive DFS: check k == len(word) first (success), then bounds, then character match. If match, save the char, replace with '#', recurse into 4 neighbors, then restore. Return the OR of all 4 directions."),
        N.callout("Analogy: Hiking a maze where you leave chalk marks at each junction. If you reach a dead end, erase your chalk and try a different route. The chalk marks prevent loops within a single attempt but disappear for the next attempt.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r, c, k):
        if k == len(word):          # All characters matched — success!
            return True
        if r < 0 or r >= rows:      # Row out of bounds
            return False
        if c < 0 or c >= cols:      # Column out of bounds
            return False
        if board[r][c] != word[k]:  # Wrong char, or '#' (already visited)
            return False

        temp = board[r][c]          # Save original character
        board[r][c] = '#'           # Mark as visited (in-place)

        found = (dfs(r+1, c, k+1) or   # Explore: down
                 dfs(r-1, c, k+1) or   # Explore: up
                 dfs(r, c+1, k+1) or   # Explore: right
                 dfs(r, c-1, k+1))     # Explore: left (short-circuit OR)

        board[r][c] = temp          # BACKTRACK: always restore
        return found

    for r in range(rows):           # Try every cell as a starting point
        for c in range(cols):
            if dfs(r, c, 0):        # Match from word[0]
                return True
    return False                    # Exhausted all starts — not found
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("rows, cols = len(board), len(board[0])", {"code": True}), (" — store grid dimensions once for O(1) bound checks.", {})])),
    N.para(N.rich([("if k == len(word): return True", {"code": True}), (" — base case checked FIRST: k equals word length means all characters matched. Return True before accessing word[k] (which would be an index error).", {})])),
    N.para(N.rich([("if r < 0 or r >= rows or c < 0 or c >= cols: return False", {"code": True}), (" — bounds check. Any out-of-range coordinate is an immediate fail.", {})])),
    N.para(N.rich([("if board[r][c] != word[k]: return False", {"code": True}), (" — character mismatch fail. Also catches '#' (visited cells) since '#' never equals any word character.", {})])),
    N.para(N.rich([("temp = board[r][c]; board[r][c] = '#'", {"code": True}), (" — save original character, then mark this cell as 'on current path'. The '#' sentinel prevents any future recursive call from reusing this cell in the same path.", {})])),
    N.para(N.rich([("found = dfs(...) or dfs(...) or ...", {"code": True}), (" — short-circuit OR: try all 4 directions, stop as soon as any returns True. Python's lazy evaluation avoids unnecessary work.", {})])),
    N.para(N.rich([("board[r][c] = temp", {"code": True}), (" — THE BACKTRACK: always restore the cell, whether found is True or False. This releases the cell for other paths.", {})])),
    N.para(N.rich([("for r in range(rows): for c in range(cols): if dfs(r, c, 0):", {"code": True}), (" — try every cell as the start of a path. If any returns True, the word exists.", {})])),
    N.divider(),
]

# ── Solution 2: Explicit Visited Set ──
blocks += [
    N.h2("Solution 2 — DFS with Explicit Visited Set"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same path-existence search. Instead of mutating the board to track visited cells, we maintain a separate set of (row, col) tuples that belong to the current path."),
        N.h4("What Doesn't Work"),
        N.para("A global visited set that persists across starting cells won't work — we need visited tracking scoped to each DFS branch. The set is shared as a mutable object and must be explicitly added to / removed from as we enter / exit each cell."),
        N.h4("The Key Observation"),
        N.para("Adding (r, c) before recursing and discarding it after is functionally identical to the '#' trick — both ensure the cell is 'occupied' exactly while on the current path, and 'free' after backtracking."),
        N.h4("Building the Solution"),
        N.para("Same structure as Solution 1, but: check (r,c) in visited instead of board[r][c]=='#'; call visited.add((r,c)) before recursing; call visited.discard((r,c)) as the backtrack step."),
    ]),
    N.h3("Code"),
    N.code("""\
def exist_v2(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    visited = set()  # (r, c) tuples on current path

    def dfs(r, c, k):
        if k == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if (r, c) in visited:       # Already on current path
            return False
        if board[r][c] != word[k]:
            return False
        visited.add((r, c))         # Mark: enter path
        found = any(
            dfs(r + dr, c + dc, k + 1)
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]
        )
        visited.discard((r, c))     # Backtrack: exit path
        return found

    return any(
        dfs(r, c, 0)
        for r in range(rows)
        for c in range(cols)
    )
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = set()", {"code": True}), (" — single set shared across all recursive calls. Contains (r,c) tuples of cells on the CURRENT active path only.", {})])),
    N.para(N.rich([("if (r, c) in visited: return False", {"code": True}), (" — explicit visited check before character check. The order matters: check visited before board[r][c] to avoid accessing a cell we've already committed to this path.", {})])),
    N.para(N.rich([("visited.add((r, c))", {"code": True}), (" — commit this cell to the current path. Equivalent to board[r][c] = '#' in Solution 1.", {})])),
    N.para(N.rich([("visited.discard((r, c))", {"code": True}), (" — the backtrack. Remove from path after all 4 directions are explored. Using discard (not remove) avoids KeyError on empty set.", {})])),
    N.callout("When to use Solution 2 over Solution 1: when the board is read-only or immutable (e.g., passed by reference to multiple concurrent threads, or explicitly stated as const in the problem). Otherwise Solution 1 is preferred — it saves O(L) space for the set.", "⚖️", "gray_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["DFS + In-Place '#' (Solution 1)", "O(m·n·4^L)", "O(L)", "L = word length; stack depth = L"],
        ["DFS + Visited Set (Solution 2)", "O(m·n·4^L)", "O(L)", "Same asymptotically; set has higher constant"],
    ]),
    N.para(N.rich([
        ("Time breakdown: ", {"bold": True}),
        ("m·n", {"code": True}),
        (" starting cells × up to ", {}),
        ("4^L", {"code": True}),
        (" paths of length L from each. In practice, early character mismatches prune most branches dramatically. Space = O(L) recursion stack depth (maximum path length before reaching base case or dead end).", {})
    ])),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — the 2D grid is a graph where cells are nodes and orthogonal adjacencies are edges.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS Backtracking — depth-first search that commits state on entry and un-commits on exit, enabling exhaustive path exploration without permanent side effects.", {})])),
    N.callout("When to recognize this pattern: (1) Grid problem + 'each cell at most once'. (2) 'Find if a path exists' (not shortest). (3) Need to explore ALL possibilities. (4) Building a solution character by character or decision by decision. (5) Whenever you need to mark a resource during recursion and unmark after — that's backtracking.", "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS Backtracking technique:"),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Find all dictionary words in a grid; same DFS backtracking augmented with a Trie for multi-word efficiency (#212)", {})])),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — DFS flood-fill to mark connected land cells; similar grid DFS but no backtracking needed (#200)", {})])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), (" (Medium) — Tree DFS collecting root-to-leaf paths; backtrack by removing last element from the path list (#113)", {})])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), (" (Medium) — Build all valid combinations by choosing/un-choosing elements; classic backtracking template (#39)", {})])),
    N.bullet(N.rich([("N-Queens", {"bold": True}), (" (Hard) — Place queens row by row; backtrack when a conflict is detected; constraint satisfaction via DFS (#51)", {})])),
    N.bullet(N.rich([("Surrounded Regions", {"bold": True}), (" (Medium) — DFS from border 'O' cells to mark safe regions; flip all interior 'O' cells to 'X' (#130)", {})])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), (" (Medium) — Enumerate all paths in a DAG; build path list + backtrack on exit; canonical backtracking template (#797)", {})])),
    N.para("These problems all share the core pattern: DFS that marks state on entry and unmarks on exit, enabling exhaustive but non-redundant path exploration."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 8: Graph Algorithms → Sub-Pattern: DFS Backtracking", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("word_search")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"  Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
