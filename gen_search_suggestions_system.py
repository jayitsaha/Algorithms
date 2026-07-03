"""
gen_search_suggestions_system.py — Notion update for LeetCode #1268 Search Suggestions System
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81df-925d-c71afc7bc757"
SLUG = "search_suggestions_system"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1268,
    pattern="Tries",
    subpatterns=["Trie + DFS Top 3"],
    tc="O(M·L + N·L)",
    sc="O(M·L)",
    key_insight="Sort products first; cap each Trie node at 3 suggestions — the first 3 words (in sorted order) reaching any node are automatically lex-smallest.",
    icon="🟡"
)
print("Properties set OK")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# 3) Build body blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of strings ", {}),
        ("products", {"code": True}),
        (" and a string ", {}),
        ("searchWord", {"code": True}),
        (". Design a system that suggests at most 3 product names from ", {}),
        ("products", {"code": True}),
        (" after each character of ", {}),
        ("searchWord", {"code": True}),
        (" is typed. Suggested products should have a common prefix with ", {}),
        ("searchWord", {"code": True}),
        (". If there are more than 3 products with a common prefix, return the 3 lexicographically smallest products. Return a list of lists of the suggested products after each character of ", {}),
        ("searchWord", {"code": True}),
        (" is typed.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("products = [\"mobile\",\"mouse\",\"moneypot\",\"monitor\",\"mousepad\"], searchWord = \"mouse\" → ", {}),
        ("[[\"mobile\",\"moneypot\",\"monitor\"],[\"mobile\",\"moneypot\",\"monitor\"],[\"mouse\",\"mousepad\"],[\"mouse\",\"mousepad\"],[\"mouse\",\"mousepad\"]]", {"code": True})
    ])),
    N.divider(),
]

# ── Solution 1: Trie + Cached Suggestions ──
blocks += [
    N.h2("Solution 1 — Trie + Cached Top-3 Suggestions (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each prefix of the searchWord, find the 3 lexicographically smallest products that start with that prefix. The prefix grows by one character each step — this is a classic prefix-lookup problem."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each prefix, scan all M products and collect matches. O(N·M·L) — too slow for large catalogues. We need prefix-indexed access."),
        N.h4("The Key Observation"),
        N.para("A Trie organises words by shared prefixes. If we insert sorted products, the first 3 products to reach any node are the 3 lex-smallest for that prefix. So we can pre-cache suggestions at each node during build time — making lookups O(1) per prefix step."),
        N.h4("Building the Solution"),
        N.para("1. Sort products. 2. Insert each product into the Trie; at each node along the path, append to node.suggestions if len < 3. 3. To answer queries: walk searchWord one char at a time. At each node, read node.suggestions. If a child is missing, emit [] for all remaining chars (dead flag)."),
        N.callout("Analogy: Building a library where every shelf has a sticky note listing the first 3 books alphabetically — you don't search each time, you just read the note.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""class TrieNode:
    def __init__(self):
        self.children = {}       # char -> TrieNode
        self.suggestions = []    # up to 3 lex-smallest products through this node

def suggestedProducts(products: list[str], searchWord: str) -> list[list[str]]:
    products.sort()              # CRITICAL: sort so first 3 insertions = lex-smallest
    root = TrieNode()

    for product in products:
        node = root
        for ch in product:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            if len(node.suggestions) < 3:  # cap at 3
                node.suggestions.append(product)

    result = []
    node = root
    dead = False                 # once off-Trie, all future prefixes are also []
    for ch in searchWord:
        if dead or ch not in node.children:
            dead = True
            result.append([])
        else:
            node = node.children[ch]
            result.append(node.suggestions)

    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("products.sort()", {"code": True}), (" — sort lexicographically BEFORE building the Trie. This is what makes the first-3-cap trick work.", {})])),
    N.para(N.rich([("self.suggestions = []", {"code": True}), (" — each node caches up to 3 product strings; computed once at build time, read in O(1) at query time.", {})])),
    N.para(N.rich([("if len(node.suggestions) < 3:", {"code": True}), (" — we only store the first 3 products to pass through this node. Because products are inserted in sorted order, these are the 3 lex-smallest.", {})])),
    N.para(N.rich([("dead = False", {"code": True}), (" — flag to short-circuit once a prefix has no Trie child. Once dead, all further characters cannot recover a match.", {})])),
    N.para(N.rich([("result.append(node.suggestions)", {"code": True}), (" — reading the pre-cached list; no sorting or DFS at query time. O(1) per step.", {})])),
    N.divider(),
]

# ── Solution 2: Binary Search ──
blocks += [
    N.h2("Solution 2 — Sorted Products + Binary Search"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("In a sorted list, all products sharing a prefix appear consecutively. So instead of building a Trie, we can binary-search for where the prefix-matching products begin, then scan at most 3 items."),
        N.h4("What Doesn't Work"),
        N.para("Linear scan for each prefix is O(M) per prefix. With N prefixes, that is O(N·M) — too slow. We need to jump directly to the first potential match."),
        N.h4("The Key Observation"),
        N.para("bisect_left(products, prefix) finds the first index where a product >= prefix. From that index, we check at most 3 consecutive products for the startswith condition. O(log M + 3) per prefix."),
        N.h4("Building the Solution"),
        N.para("Sort once. For each prefix, binary search for the left boundary, then collect up to 3 matches. This is O(M log M + N·log M) with O(1) extra space."),
    ]),
    N.h3("Code"),
    N.code("""import bisect

def suggestedProducts(products: list[str], searchWord: str) -> list[list[str]]:
    products.sort()              # O(M log M) one-time cost
    result, prefix = [], ""

    for ch in searchWord:
        prefix += ch             # grow prefix one char at a time
        # Binary search: first index where product >= prefix
        i = bisect.bisect_left(products, prefix)
        suggestions = []
        for j in range(i, min(i + 3, len(products))):
            if products[j].startswith(prefix):   # guard: must actually match
                suggestions.append(products[j])
        result.append(suggestions)

    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("bisect.bisect_left(products, prefix)", {"code": True}), (" — finds the leftmost position where prefix could be inserted to keep the list sorted. Products at or after this index are the candidates.", {})])),
    N.para(N.rich([("products[j].startswith(prefix)", {"code": True}), (" — necessary guard: the binary search finds products >= prefix, but not all of them start with prefix. E.g., if prefix='mo', 'mouse' qualifies but a product like 'mz...' would also be >= 'mo' without starting with it.", {})])),
    N.para(N.rich([("min(i + 3, len(products))", {"code": True}), (" — avoid index out of bounds; we check at most 3 items.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Build Time", "Query Time", "Space"],
        ["Trie + Cached Top-3 (Interview Pick)", "O(M·L)", "O(N·L)", "O(M·L)"],
        ["Sort + Binary Search", "O(M log M)", "O(N·log M)", "O(1) extra"],
        ["Brute Force (scan all)", "O(1)", "O(N·M·L)", "O(1)"],
    ]),
    N.para(N.rich([
        ("M", {"bold": True}), (" = number of products, ", {}),
        ("L", {"bold": True}), (" = average product length, ", {}),
        ("N", {"bold": True}), (" = length of searchWord", {})
    ])),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries (Prefix Tree)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie + DFS Top 3 — sort products, insert in order, cache up to 3 suggestions per node; walk prefix at query time for O(1) per step.", {})])),
    N.callout(
        "When to recognise this pattern: 'starts with prefix', 'suggest top K words', 'autocomplete', 'for each character typed'. When you see prefix + top-K in the same problem, think Trie with cached K suggestions per node.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Trie / prefix search):"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), (" (Medium) — Build Trie with insert, search, startsWith (#208)", {})])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), (" (Hard) — Trie + DFS on 2D grid to find all dictionary words (#212)", {})])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), (" (Medium) — Trie with wildcard '.' via DFS (#211)", {})])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), (" (Medium) — Trie finds shortest root prefix for each sentence word (#648)", {})])),
    N.bullet(N.rich([("Longest Word in Dictionary", {"bold": True}), (" (Medium) — Trie DFS; longest word buildable one letter at a time (#720)", {})])),
    N.bullet(N.rich([("Map Sum Pairs", {"bold": True}), (" (Medium) — Trie stores sum of values in subtree for prefix queries (#677)", {})])),
    N.bullet(N.rich([("Palindrome Pairs", {"bold": True}), (" (Hard) — Trie with reversed words to find palindrome concatenations (#336)", {})])),
    N.para("These problems share the same core structure: a Trie for O(L) prefix navigation plus additional information cached at nodes (suggestions, sums, word markers)."),
    N.callout("Reference: Trie / Prefix Tree problems — standard classification under 'Advanced Data Structures: Tries'.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# 4) Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
