"""
gen_design_in_memory_file_system.py
Regenerates Notion page for LeetCode #588 — Design In-Memory File System.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "design_in_memory_file_system"
NAME = "Design In-Memory File System"
NUMBER = 588
DIFFICULTY = "Hard"
ICON = "🔴"

# ── Step 0: Create page (notion_page_id is null) ──
print("Creating new Notion page...")
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern="Design",
    subpatterns=["Trie of Directories"],
    tc="O(L) per operation",
    sc="O(N·L) total nodes",
    key_insight="Model a filesystem as a Trie where each node is a directory (content='') or file (content≠''); a single _walk helper with create=True/False serves all four operations.",
    icon=ICON,
)
print("Properties set.")

# ── Step 2: Wipe old body (fresh page has no body, wipe is safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body blocks ──
blocks = []

# ─── Problem ───
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design an in-memory file system that supports four operations:\n\n", {}),
        ("ls(path)", {"code": True}),
        (" — If ", {}),
        ("path", {"code": True}),
        (" is a file, return a list containing only that file name. If it is a directory, return the list of its direct contents sorted in lexicographic order.\n\n", {}),
        ("mkdir(path)", {"code": True}),
        (" — Create the directory and all its parent directories if they do not exist. Similar to the Unix command ", {}),
        ("mkdir -p", {"code": True}),
        (".\n\n", {}),
        ("addContentToFile(filePath, content)", {"code": True}),
        (" — If the file at ", {}),
        ("filePath", {"code": True}),
        (" does not exist, create that file with its content. If it exists, append the content to the file.\n\n", {}),
        ("readContentFromFile(filePath)", {"code": True}),
        (" — Return the full content of the file at ", {}),
        ("filePath", {"code": True}),
        (".\n\nAll paths are absolute (start with '/') and all directory/file names consist of lowercase letters and digits.", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Trie of Nodes (Optimal, Interview Pick) ───
blocks += [
    N.h2("Solution 1 — Trie of Nodes (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to store and retrieve named entities arranged in a parent-child hierarchy, where children are identified by name segments split from a path string. This is exactly a dictionary tree — each node owns a dict mapping child names to child nodes."),
        N.h4("What Doesn't Work"),
        N.para("Storing full paths as keys in a flat dictionary makes ls(/a) require scanning all keys for the prefix '/a/' — O(N·L). It also makes directory structure implicit rather than structural, breaking ls semantics."),
        N.h4("The Key Observation"),
        N.para("A filesystem path is like a word in a Trie — but each 'character' is a full name segment separated by '/'. The Trie structure gives us O(L) traversal, O(k log k) child listing, and automatic prefix sharing. One TrieNode class handles both files (content ≠ '') and directories (content = '')."),
        N.h4("Building the Solution"),
        N.para("1. Design TrieNode with children dict + content string.\n2. Write _walk(path, create) to split path, filter empty strings, traverse with optional node creation.\n3. ls: walk, check content (file vs dir), return appropriately.\n4. mkdir: walk with create=True.\n5. addContentToFile: walk with create=True, append content.\n6. readContentFromFile: walk, return content."),
        N.callout("Analogy: A string Trie uses single chars as edge labels. This filesystem Trie uses full names. Same traversal logic, different alphabet size (unbounded names vs. 26 letters).", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "class TrieNode:\n"
        "    def __init__(self):\n"
        "        self.children = {}   # name -> TrieNode\n"
        "        self.content = \"\"   # empty = dir, non-empty = file\n"
        "\n"
        "class FileSystem:\n"
        "    def __init__(self):\n"
        "        self.root = TrieNode()  # always-present root '/'\n"
        "\n"
        "    def _walk(self, path, create=False):\n"
        "        \"\"\"Traverse path from root; create missing nodes if create=True.\"\"\"\n"
        "        parts = [x for x in path.split('/') if x]  # drop leading ''\n"
        "        node = self.root\n"
        "        for p in parts:\n"
        "            if create:\n"
        "                node.children.setdefault(p, TrieNode())\n"
        "            node = node.children[p]\n"
        "        return node\n"
        "\n"
        "    def ls(self, path: str):\n"
        "        node = self._walk(path)\n"
        "        if node.content:  # non-empty content → it's a file\n"
        "            return [path.split('/')[-1]]\n"
        "        return sorted(node.children.keys())\n"
        "\n"
        "    def mkdir(self, path: str):\n"
        "        self._walk(path, create=True)\n"
        "\n"
        "    def addContentToFile(self, filePath: str, content: str):\n"
        "        node = self._walk(filePath, create=True)\n"
        "        node.content += content  # += handles both create and append\n"
        "\n"
        "    def readContentFromFile(self, filePath: str) -> str:\n"
        "        return self._walk(filePath).content\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode:", {"code": True}), " — Defines a single node type representing either a directory or a file in the filesystem tree."])),
    N.para(N.rich([("self.children = {}", {"code": True}), " — A dict mapping child name strings (e.g., 'a', 'readme.txt') to their TrieNode objects. Empty dict = leaf node."])),
    N.para(N.rich([("self.content = \"\"", {"code": True}), " — The file's content, or empty string for a directory. This dual-purpose field elegantly distinguishes files from dirs."])),
    N.para(N.rich([("self.root = TrieNode()", {"code": True}), " — The always-present root node representing '/'. Created in __init__ before any operations."])),
    N.para(N.rich([("parts = [x for x in path.split('/') if x]", {"code": True}), " — Splits '/a/b/c' into ['a','b','c']. Filters the leading empty string that split produces from the leading '/'."])),
    N.para(N.rich([("node.children.setdefault(p, TrieNode())", {"code": True}), " — Creates a new child node only if 'p' does not already exist. setdefault is atomic and avoids an if-not-in check."])),
    N.para(N.rich([("node = node.children[p]", {"code": True}), " — Descend into the child. After setdefault, this is guaranteed to succeed whether the node was just created or already existed."])),
    N.para(N.rich([("if node.content:", {"code": True}), " — Checks if the final node is a file. Non-empty string is truthy in Python. This is the ls 'file case' edge condition."])),
    N.para(N.rich([("return [path.split('/')[-1]]", {"code": True}), " — For a file, ls returns a list with just the filename. [-1] extracts the last path component (the filename itself)."])),
    N.para(N.rich([("return sorted(node.children.keys())", {"code": True}), " — For a directory, return all direct child names in sorted (lexicographic) order as required by the problem."])),
    N.para(N.rich([("node.content += content", {"code": True}), " — Append content to file. On first write: '' + 'hello' = 'hello'. On subsequent writes: 'hello' + ' world' = 'hello world'. += is uniform for both cases."])),
    N.divider(),
]

# ─── Solution 2: Flat HashMap ───
blocks += [
    N.h2("Solution 2 — Flat HashMap (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("What if we ignore structure? Store directories as a set of path strings and files as a dict from path to content. All queries then become string prefix searches."),
        N.h4("What Doesn't Work"),
        N.para("ls requires scanning ALL stored paths for those starting with the query prefix. If N paths are stored with average length L, ls is O(N·L). With millions of files this becomes prohibitively slow."),
        N.h4("The Key Observation"),
        N.para("Simple to implement correctly, and fine for small datasets. Useful as a stepping stone in an interview to demonstrate correctness before optimizing to the Trie approach."),
        N.h4("Building the Solution"),
        N.para("Keep dirs as a set and files as a dict. For ls, scan both collections for strings starting with path+'/'. Extract the next component after the prefix. For mkdir, add each prefix path to dirs. For addContentToFile, register parent dirs then store/append content in files dict."),
    ]),
    N.h3("Code"),
    N.code(
        "class FileSystem:\n"
        "    def __init__(self):\n"
        "        self.dirs = {'/'}    # set of existing directory paths\n"
        "        self.files = {}      # filePath -> content string\n"
        "\n"
        "    def ls(self, path):\n"
        "        if path in self.files:\n"
        "            return [path.rpartition('/')[2]]\n"
        "        prefix = path if path == '/' else path + '/'\n"
        "        children = set()\n"
        "        for p in list(self.dirs) + list(self.files):  # O(N) scan\n"
        "            if p.startswith(prefix):\n"
        "                rest = p[len(prefix):]\n"
        "                children.add(rest.split('/')[0])\n"
        "        return sorted(children)\n"
        "\n"
        "    def mkdir(self, path):\n"
        "        parts = path.split('/')\n"
        "        for i in range(2, len(parts) + 1):\n"
        "            self.dirs.add('/'.join(parts[:i]))\n"
        "\n"
        "    def addContentToFile(self, fp, content):\n"
        "        parent = fp.rpartition('/')[0] or '/'\n"
        "        self.mkdir(parent)\n"
        "        self.files[fp] = self.files.get(fp, '') + content\n"
        "\n"
        "    def readContentFromFile(self, fp):\n"
        "        return self.files[fp]\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.dirs = {'/'}  ", {"code": True}), " — Start with root directory. Every mkdir will add paths to this set."])),
    N.para(N.rich([("prefix = path if path == '/' else path + '/'", {"code": True}), " — Special-case root: prefix is '/' itself. For other dirs: append '/' to avoid matching '/abc' when searching for '/a'."])),
    N.para(N.rich([("for p in list(self.dirs) + list(self.files):", {"code": True}), " — Scan ALL known paths. This is the O(N) bottleneck compared to the Trie's O(1) child lookup."])),
    N.para(N.rich([("rest.split('/')[0]", {"code": True}), " — After stripping the prefix, take the first segment. This gives the direct child name, ignoring deeper nesting."])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "ls Time", "mkdir Time", "addContent Time", "Space"],
        ["Flat HashMap", "O(N·L)", "O(L)", "O(L)", "O(N·L)"],
        ["Trie of Nodes (optimal)", "O(L + k log k)", "O(L)", "O(L)", "O(N·L)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design — Problems asking you to implement a data structure or system API from scratch."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie of Directories — A Trie where edge labels are full name strings (not single characters), used to represent hierarchical namespace structures like filesystems, package paths, or DNS labels."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Design a filesystem / directory structure' — always a Trie\n"
        "• 'Hierarchical keys with prefix queries' — Trie beats flat map\n"
        "• 'List direct children efficiently' — Trie gives O(1) child access after traversal\n"
        "• Paths sharing long prefixes — Trie avoids redundant storage\n"
        "• The problem involves walk/navigate + create-on-demand semantics",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie, Design, or Directory-style traversal):"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Core Trie DS: insert, search, startsWith. Foundation for all Trie problems. (#208)"])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie with '.' wildcard: DFS at each wildcard node. (#211)"])),
    N.bullet(N.rich([("Design File System", {"bold": True}), " (Medium) — Simpler FS: create(path, value) + get(path). Same Trie approach without ls. (#1166)"])),
    N.bullet(N.rich([("Design Search Autocomplete System", {"bold": True}), " (Hard) — Trie where each node stores top-k suggestions ranked by frequency. (#642)"])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — Trie + DFS backtracking: place the Trie into the board search. (#212)"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Classic design problem: OrderedDict or doubly linked list + hash map. Different pattern, same design interview category. (#146)"])),
    N.bullet(N.rich([("Design HashMap", {"bold": True}), " (Easy) — Build a hash map from scratch; understand open addressing vs. chaining. (#706)"])),
    N.para("These problems share the core technique of structural tree traversal for hierarchical data. The Trie-of-Directories pattern appears whenever paths or hierarchical namespaces must be navigated efficiently."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Design section\nSub-Pattern: Trie of Directories · Source: Analysis", "📚", "gray_background"),
]

# ─── Interactive Visual Explainer ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Step 4: Append blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Step 5: Write status file ──
import json
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": 1090,
    "notes": "Fresh page created. Trie of Directories. 14-step interactive walkthrough."
}
status_path = os.path.join(os.path.dirname(__file__), ".status", f"{SLUG}.json")
os.makedirs(os.path.dirname(status_path), exist_ok=True)
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)

print(f"RESULT {SLUG} | html=OK | notion=OK | lines=1090")
