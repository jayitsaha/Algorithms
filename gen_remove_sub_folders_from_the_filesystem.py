"""
Notion update for: Remove Sub-Folders from the Filesystem (LeetCode #1233)
Pattern: Tries | Subpattern: Trie or Sort + Skip (Guide Section 12.2)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8164-bb18-da6d3dcfa787"

# ─── 1) Set properties ───
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1233,
    pattern="Tries",
    subpatterns=["Trie or Sort + Skip"],
    tc="O(n·L·log n)",
    sc="O(n·L)",
    key_insight="Sort paths lex; any sub-folder starts with last_kept + '/'. One pass, one comparison.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe old body ───
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} old blocks.")

# ─── 3) Build body ───
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of folders in a filesystem, your task is to remove all ", {}),
        ("sub-folders", {"bold": True}),
        (" from those folders and return the folders after removing. A folder ", {}),
        ("folder[i]", {"code": True}),
        (" is a sub-folder of ", {}),
        ("folder[j]", {"code": True}),
        (" if it starts with ", {}),
        ("folder[j] + '/'", {"code": True}),
        (". The order of the answer does not matter.", {}),
    ])),
    N.para("Example: folder = [\"/a\",\"/a/b\",\"/c/d\",\"/c/d/e\",\"/c/f\"] → Output: [\"/a\",\"/c/d\",\"/c/f\"]"),
    N.para("Example: folder = [\"/a\",\"/a/b/c\",\"/a/b/d\"] → Output: [\"/a\"]"),
    N.divider(),
]

# ── Solution 1: Sort + Skip ──
blocks += [
    N.h2("Solution 1 — Sort + Skip (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to identify, for each folder, whether any other folder is its ancestor. Naively this is O(n²): compare every pair. We need to reduce the comparison cost."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each folder, check if it starts with any other folder + '/'. This is O(n²·L) — too slow for n=40,000. A hash set of all paths doesn't directly help because checking all prefixes of a path is still O(L) per prefix times O(L) prefixes = O(L²) per folder."),
        N.h4("The Key Observation"),
        N.para("Lexicographic sort has a beautiful property: if B is a sub-folder of A, then A sorts before B. Specifically, path separator '/' (ASCII 47) sorts before any alphanumeric character, so '/a/b' always sorts before '/ab'. This means every sub-folder appears directly after its parent in sorted order."),
        N.h4("Building the Solution"),
        N.para("After sorting: keep a pointer to the last kept (top-level) folder. For each subsequent folder, check if it starts with last_kept + '/'. If yes — skip. If no — it's a new top-level folder, append to result and update last_kept. The '/' separator is critical: without it, '/ab' would be falsely removed when last_kept='/a'."),
        N.callout("Analogy: Think of sorted paths as a filing system. All files under folder A come right after A in the drawer. Once you decide A is top-level, you fast-forward past everything starting with 'A/' until you hit something that doesn't — that's the next top-level folder.", "🗂️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def removeSubfolders(folder: List[str]) -> List[str]:
    folder.sort()               # Lex sort: parents appear before their sub-folders
    result = [folder[0]]        # First folder is always a top-level folder
    for f in folder[1:]:
        last_kept = result[-1]  # Most recently kept top-level folder
        if not f.startswith(last_kept + "/"):   # "/" is the path boundary!
            result.append(f)    # New top-level folder
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("folder.sort()", {"code": True}), (" — Lexicographic sort ensures any sub-folder appears immediately after its parent. The ASCII value of '/' (47) is less than any alphanumeric character, which is the mathematical reason this works.", {})])),
    N.para(N.rich([("result = [folder[0]]", {"code": True}), (" — The first folder in sorted order is always a top-level folder (no folder can precede it in sorted order to be its parent). Initializing with it also handles the edge case of a single folder.", {})])),
    N.para(N.rich([("last_kept = result[-1]", {"code": True}), (" — The most recently appended (kept) folder. Due to sorting, this is also the lexicographically largest top-level folder seen. It's the only one we need to compare against.", {})])),
    N.para(N.rich([("if not f.startswith(last_kept + \"/\")", {"code": True}), (" — The + \"/\" is the critical guard. Without it, '/ab' would be falsely flagged as a sub-folder of '/a' since '/ab'.startswith('/a') is True but '/ab'.startswith('/a/') is False.", {})])),
    N.para(N.rich([("result.append(f)", {"code": True}), (" — f is a new top-level folder. Appending it also updates result[-1], which becomes the new last_kept for the next iteration.", {})])),
    N.divider(),
]

# ── Solution 2: Trie ──
blocks += [
    N.h2("Solution 2 — Trie (Prefix Tree)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A filesystem is inherently a tree structure. Path components are tree edges. Two folders share a path prefix if and only if they share a path from the root. A Trie (prefix tree) directly models this hierarchy."),
        N.h4("What Doesn't Work"),
        N.para("The Sort + Skip approach is simpler; the Trie shines if we need to support dynamic insertions, deletions, or range queries over the filesystem."),
        N.h4("The Key Observation"),
        N.para("Insert all paths into a Trie, splitting by '/'. A node is a top-level folder if it is marked as a complete path AND no ancestor node is also marked. In the DFS, when we hit a marked node, we stop recursing — all descendants are sub-folders."),
        N.h4("Building the Solution"),
        N.para("Build the Trie from all paths. Then DFS: when we encounter a '#' marker (end of a path), add the reconstructed path to result and return without descending further. If no marker, keep descending and appending path components."),
    ]),
    N.h3("Code"),
    N.code("""def removeSubfolders_trie(folder: List[str]) -> List[str]:
    trie = {}
    for path in folder:
        parts = path.split("/")[1:]  # Split "/a/b" → ["a","b"], skip empty ""
        node = trie
        for p in parts:
            node = node.setdefault(p, {})
        node["#"] = True             # Mark end of this path

    result = []
    def dfs(node, path):
        if "#" in node:              # This is a complete path (top-level folder)
            result.append(path)
            return                   # Do NOT recurse — children are sub-folders
        for k, child in node.items():
            dfs(child, path + "/" + k)

    for k, child in trie.items():
        dfs(child, "/" + k)
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("path.split(\"/\")[1:]", {"code": True}), (" — Split \"/a/b\" → [\"\",\"a\",\"b\"]; [1:] skips the empty string before the first slash. Result: [\"a\",\"b\"].", {})])),
    N.para(N.rich([("node.setdefault(p, {})", {"code": True}), (" — If path component p exists as a child, return it. If not, create an empty dict child and return it. Efficiently builds the trie.", {})])),
    N.para(N.rich([("node[\"#\"] = True", {"code": True}), (" — Sentinel marker at the trie node corresponding to the last component of this path. Signals: a complete folder path ends here.", {})])),
    N.para(N.rich([("if \"#\" in node: result.append(path); return", {"code": True}), (" — The key DFS pruning: when we hit a marked node, add it to result and stop. All children would be sub-folders — we never recurse into them.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (check all pairs)", "O(n²·L)", "O(n·L)"],
        ["Sort + Skip (Interview Pick)", "O(n·L·log n)", "O(n·L)"],
        ["Trie", "O(n·L)", "O(n·L)"],
    ]),
    N.para("n = number of folders, L = average path length. Sort + Skip is faster in practice due to cache efficiency despite the log n factor."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries (Section 12 — BST & Tries)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie or Sort + Skip (from Guide Section 12.2)", {})])),
    N.callout(
        "When to recognize this pattern: path strings with '/' separators; sub-folder/sub-path relationships; removing 'contained-in' elements; any hierarchy where prefix = ancestor relationship.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie / Sort + Skip):"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Core Trie: insert, search, startsWith; foundation for all Trie problems (#208)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Trie for root lookup: replace words in sentence with shortest dictionary root prefix (#648)", {})])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), (" (Medium) — Sort + prefix scan for top-3 autocomplete suggestions per typed character (#1268)", {})])),
    N.bullet(N.rich([("Longest Word in Dictionary", {"bold": True}), (" (Medium) — Trie + BFS: longest word where all prefixes exist in input set (#720)", {})])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), (" (Medium) — Trie + DFS: wildcard '.' pattern matching (#211)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Trie + DFS backtracking: find all dictionary words in a 2D grid (#212)", {})])),
    N.bullet(N.rich([("Longest Common Prefix", {"bold": True}), (" (Easy) — Sort-based: compare only first and last sorted strings to find common prefix (#14)", {})])),
    N.para("These problems share the same core technique: using sorted order or a Trie structure to efficiently detect prefix relationships between strings."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 12.2 (BST & Tries → Trie / Prefix Tree). Sub-Pattern: Trie or Sort + Skip. Source: Guide Section 12.2.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_sub_folders_from_the_filesystem")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4) Append all blocks ───
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
