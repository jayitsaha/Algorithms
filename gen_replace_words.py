"""gen_replace_words.py — Notion update for Replace Words (#648)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81da-8291-c9abc2f354e3"

print(f"Updating page {PAGE_ID} ...")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=648,
    pattern="Tries",
    subpatterns=["Trie for Root Lookup"],
    tc="O((D+N)·L)",
    sc="O(D·L)",
    key_insight="Insert all roots into a Trie; first '#' hit during descent = shortest root, guaranteed.",
    icon="🟡",
)
print("Properties set.")

# 2) Wipe old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Rebuild body
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a dictionary of roots and a sentence, replace each word in the sentence with the shortest matching root from the dictionary. If no root is found, keep the word unchanged.\n\n"
         "Example: dictionary = ", {}),
        ('["cat", "bat", "rat"]', {"code": True}),
        (", sentence = ", {}),
        ('"the cattle was rattled by the battery"', {"code": True}),
        (" → ", {}),
        ('"the cat was rat by the bat"', {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Trie (Optimal) ──
TRIE_CODE = '''\
def replaceWords(dictionary, sentence):
    # Phase 1: Build Trie from all roots
    trie = {}
    for root in dictionary:
        node = trie
        for ch in root:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['#'] = True   # end-of-root sentinel

    # Phase 2: Lookup each word
    def lookup(word):
        node = trie
        for i, ch in enumerate(word):
            if ch not in node:
                break           # no root with this prefix
            node = node[ch]
            if '#' in node:
                return word[:i + 1]  # shortest root found
        return word             # no root matched

    return ' '.join(lookup(w) for w in sentence.split())
'''

blocks += [
    N.h2("Solution 1 — Trie (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each sentence word, check: is any dictionary entry a prefix of this word? If yes, replace the word with the shortest such prefix. This is fundamentally a prefix lookup problem."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each sentence word, scan every dictionary root and check if it's a prefix — O(D) checks per word, each O(L). Total O(N·D·L). With a large dictionary this is slow. Hash Set with prefix scan is better (O(N·L²)) but still quadratic in word length."),
        N.h4("The Key Observation"),
        N.para("A Trie stores all roots in a shared prefix tree. Walking the Trie for a word costs O(L) regardless of dictionary size. The first end-of-word marker we encounter during descent is the shallowest (shortest) matching root — no extra comparison needed."),
        N.h4("Building the Solution"),
        N.para("Step 1: Insert each root into the Trie char-by-char, marking the last char with '#'. Step 2: For each sentence word, walk the Trie. At each node check '#' — if present, return word[:i+1]. If the next char is missing, return the full word. Step 3: Join results with spaces."),
        N.callout(
            "Analogy: The Trie is like a phone tree. You dial 2-2-8 (c-a-t) and the system says 'match found!' before you even finish dialing the full number 'cattle'. Short-circuit at the first confirmed match.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(TRIE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("trie = {}", {"code": True}), " — Trie as nested dicts. Key insight: no class needed. {'c':{'a':{'t':{'#':True}}}} is the full encoding."])),
    N.para(N.rich([("node = trie", {"code": True}), " inside the insert loop — reset to Trie root for each new root being inserted."])),
    N.para(N.rich([("if ch not in node: node[ch] = {}", {"code": True}), " — Lazily create child nodes. If 'cat' and 'car' share 'c'→'a', both insertions share that prefix path."])),
    N.para(N.rich([("node['#'] = True", {"code": True}), " — The end-of-root sentinel. '#' cannot collide with any lowercase letter key."])),
    N.para(N.rich([("if ch not in node: break", {"code": True}), " — In lookup: current prefix not in Trie → no root matches this word. Fall through to return the full word."])),
    N.para(N.rich([("if '#' in node: return word[:i+1]", {"code": True}), " — CRITICAL: checked at every depth. The first '#' hit is the shallowest (shortest) root. word[:i+1] is the prefix of length i+1."])),
    N.para(N.rich([("return word", {"code": True}), " — No root matched any prefix of this word → keep it unchanged."])),
    N.para(N.rich([('" ".join(lookup(w) for w in sentence.split())', {"code": True}), " — Split sentence on whitespace, apply lookup to each word, rejoin."])),
    N.divider(),
]

# ── Solution 2 — Hash Set ──
HASH_CODE = '''\
def replaceWords(dictionary, sentence):
    root_set = set(dictionary)   # O(1) membership
    result = []
    for word in sentence.split():
        replacement = word
        for length in range(1, len(word) + 1):
            if word[:length] in root_set:
                replacement = word[:length]  # shortest first
                break
        result.append(replacement)
    return ' '.join(result)
'''

blocks += [
    N.h2("Solution 2 — Hash Set + Prefix Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Store all roots in a set. For each sentence word, try its prefixes from shortest to longest. The first prefix found in the set is the shortest matching root."),
        N.h4("What Doesn't Work"),
        N.para("This approach works but is O(L²) per word: up to L prefixes, each O(L) to slice. For short words it's fine; for long words with many characters, the Trie is asymptotically better."),
        N.h4("The Key Observation"),
        N.para("Python set membership is O(L) for strings (must hash the string). Creating word[:k] is O(k). In the worst case — no root matches — we create L slices of lengths 1 to L, costing 1+2+…+L = O(L²)."),
        N.h4("Building the Solution"),
        N.para("Loop prefix lengths from 1 up to len(word). Check each prefix in the set. Break on first match (shortest root). Simpler code than Trie; useful for small dictionaries or quick implementations."),
    ]),
    N.h3("Code"),
    N.code(HASH_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("root_set = set(dictionary)", {"code": True}), " — Convert list to set for O(1) average-case membership tests (still O(L) to hash the string)."])),
    N.para(N.rich([("for length in range(1, len(word) + 1)", {"code": True}), " — Iterate prefix lengths shortest-first, so the first match is guaranteed shortest."])),
    N.para(N.rich([("if word[:length] in root_set", {"code": True}), " — Slice is O(length) then hash is O(length). Total per check: O(length)."])),
    N.para(N.rich([("break", {"code": True}), " — Stop immediately at the shortest match. Without this break we'd get the longest match."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Build Time", "Query per Word", "Space"],
        ["Hash Set + Prefix Scan", "O(D·L)", "O(L²)", "O(D·L)"],
        ["Trie (Interview Pick)", "O(D·L)", "O(L)", "O(D·L)"],
    ]),
    N.para(N.rich([
        ("D", {"bold": True}), " = dictionary size, ",
        ("N", {"bold": True}), " = words in sentence, ",
        ("L", {"bold": True}), " = average word / root length.",
    ])),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries (BST & Tries — Section 12.2)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie for Root Lookup"])),
    N.callout(
        "When to recognize this pattern: 'replace each word with shortest matching prefix', 'does any dictionary word start this word', 'find all words beginning with X'. Any prefix lookup over a fixed dictionary → Trie.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie technique:"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Build insert/search/startsWith from scratch (#208)"])),
    N.bullet(N.rich([("Design Add and Search Words", {"bold": True}), " (Medium) — Trie + DFS for '.' wildcard matching (#211)"])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), " (Medium) — Trie + DFS collect top-3 suggestions per prefix (#1268)"])),
    N.bullet(N.rich([("Longest Word in Dictionary", {"bold": True}), " (Medium) — Trie + BFS find longest word buildable char-by-char (#720)"])),
    N.bullet(N.rich([("Word Search II", {"bold": True}), " (Hard) — Trie + DFS backtracking on 2D grid (#212)"])),
    N.bullet(N.rich([("Maximum XOR of Two Numbers in an Array", {"bold": True}), " (Medium) — Bit Trie for greedy XOR maximization (#421)"])),
    N.bullet(N.rich([("Remove Sub-Folders from the Filesystem", {"bold": True}), " (Medium) — Trie or Sort + Skip (#1233)"])),
    N.para("These problems all share the core technique: encode strings in a Trie for O(L) prefix operations."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 12.2 (BST & Tries → Trie). Sub-Pattern: Trie for Root Lookup · Source: Guide Section 12.2", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("replace_words")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
