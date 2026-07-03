"""
gen_find_the_length_of_the_longest_common_prefix.py
Rebuilds the Notion page for LeetCode #3043 in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81bf-8612-e8d84a498902"
SLUG = "find_the_length_of_the_longest_common_prefix"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=3043,
    pattern="Tries",
    subpatterns=["Trie Intersection"],
    tc="O((m+n)·d)",
    sc="O(m·d)",
    key_insight="Insert all arr1 numbers digit-by-digit into a Trie; query each arr2 number to find the deepest matching path.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two arrays of integers "), ("arr1", {"code": True}), (" and "), ("arr2", {"code": True}),
        (", return the length of the longest common prefix shared between any number from "),
        ("arr1", {"code": True}), (" and any number from "), ("arr2", {"code": True}),
        (", when the integers are compared digit by digit from the leftmost digit."),
    ])),
    N.para(N.rich([
        ("Example: "), ("arr1 = [1, 10, 100], arr2 = [1000]", {"code": True}),
        (" → Answer: "), ("3", {"bold": True}),
        (" (\"100\" is the longest common digit prefix, shared by 100 and 1000)."),
    ])),
    N.divider(),
]

# Solution 1: Trie (optimal)
trie_code = '''\
class TrieNode:
    def __init__(self):
        self.children = {}          # digit char ('0'-'9') -> TrieNode

def longestCommonPrefix(arr1, arr2) -> int:
    root = TrieNode()

    # Build phase: insert all arr1 numbers into the Trie
    for num in arr1:
        node = root
        for ch in str(num):             # walk digits left to right
            if ch not in node.children:
                node.children[ch] = TrieNode()  # create missing node
            node = node.children[ch]    # advance into child

    # Query phase: check each arr2 number against the Trie
    best = 0
    for num in arr2:
        node = root
        length = 0
        for ch in str(num):
            if ch in node.children:     # digit path exists in Trie
                node = node.children[ch]
                length += 1             # one more prefix character matched
            else:
                break                   # no arr1 number shares a longer prefix
        best = max(best, length)
    return best
'''

blocks += [
    N.h2("Solution 1 — Trie (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest digit prefix shared between ANY pair (arr1[i], arr2[j]). Convert integers to digit strings — now it's a string prefix problem across two sets."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: compare every pair (arr1[i], arr2[j]) as strings — O(m·n·d). With m=n=50,000 and d=10, that's 25 billion digit comparisons. Far too slow."),
        N.h4("The Key Observation"),
        N.para("A Trie encodes ALL prefixes of all arr1 numbers in one tree. After building it (O(m·d)), each arr2 number can be queried in O(d) time — we just walk the tree and count matching steps. Total: O((m+n)·d) instead of O(m·n·d)."),
        N.h4("Building the Solution"),
        N.para("Phase 1 (Build): Insert each arr1 number digit-by-digit. Shared prefixes reuse existing Trie nodes — no duplication. Phase 2 (Query): Walk each arr2 number through the Trie. Count consecutive digit matches until a digit has no child. Track the global maximum count across all queries."),
        N.callout("Analogy: The Trie is like a phone directory sorted by digit. Inserting '100' creates the 1→0→0 path. Any query starting with '1', '10', or '100' will match that path up to its length — without re-reading every stored number.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(trie_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("class TrieNode", {"code": True}), " — Minimal node with a children dict mapping digit characters to child nodes. No end-of-word flag needed since we only measure depth."])),
    N.para(N.rich([("root = TrieNode()", {"code": True}), " — Single root node; root of all digit prefix paths."])),
    N.para(N.rich([("for num in arr1 → node = root", {"code": True}), " — Each arr1 number starts a fresh insertion from the root."])),
    N.para(N.rich([("for ch in str(num)", {"code": True}), " — Convert integer to string, then walk characters left-to-right (most-significant digit first)."])),
    N.para(N.rich([("if ch not in node.children → create TrieNode()", {"code": True}), " — Only create a new node if this digit path doesn't already exist. Existing paths are reused (numbers sharing a prefix share nodes)."])),
    N.para(N.rich([("node = node.children[ch]", {"code": True}), " — Advance into the child — whether newly created or existing."])),
    N.para(N.rich([("for num in arr2 → length = 0", {"code": True}), " — Each arr2 number is a fresh query. Reset length counter."])),
    N.para(N.rich([("if ch in node.children → length += 1", {"code": True}), " — Digit found in Trie → one more prefix character matches. Advance."])),
    N.para(N.rich([("else: break", {"code": True}), " — Digit not found → no arr1 number shares a longer prefix. Stop immediately."])),
    N.para(N.rich([("best = max(best, length)", {"code": True}), " — Update global maximum after each arr2 query."])),
    N.divider(),
]

# Solution 2: HashSet
hashset_code = '''\
def longestCommonPrefix(arr1, arr2) -> int:
    # Collect every prefix of every arr1 number
    prefixes = set()
    for num in arr1:
        s = str(num)
        for i in range(1, len(s) + 1):
            prefixes.add(s[:i])       # adds "1", "10", "100" for num=100

    best = 0
    for num in arr2:
        s = str(num)
        for i in range(len(s), 0, -1):     # check longest prefix first
            if s[:i] in prefixes:          # O(1) hash set lookup
                best = max(best, i)
                break                      # found best match for this number
    return best
'''

blocks += [
    N.h2("Solution 2 — HashSet of All arr1 Prefixes"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same insight — we need all arr1 prefixes available for O(1) lookup. Instead of a Trie tree, store them all in a flat hash set."),
        N.h4("What Doesn't Work"),
        N.para("Without pre-computing prefixes, each arr2 query must scan all arr1 numbers — O(m) per query."),
        N.h4("The Key Observation"),
        N.para("Explicitly enumerate every prefix of every arr1 number and add to a set. For 100 we add '1', '10', '100'. Then for each arr2 number, check its prefixes longest-first until we hit a match."),
        N.h4("Building the Solution"),
        N.para("For each arr1 number s of length L, generate L prefix strings s[:1], s[:2], ..., s[:L] and add to a Python set. For each arr2 number, iterate i from len(s) down to 1 and check if s[:i] is in the set. First hit gives the best match for this arr2 number."),
    ]),
    N.h3("Code"),
    N.code(hashset_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("prefixes.add(s[:i])", {"code": True}), " — String slice s[:i] creates a new string object each time. For '100': '1', '10', '100'. All three added to the set."])),
    N.para(N.rich([("for i in range(len(s), 0, -1)", {"code": True}), " — Iterate from longest prefix to shortest. Checking longest first means we break as soon as we find any match — no need to try shorter prefixes after."])),
    N.para(N.rich([("if s[:i] in prefixes", {"code": True}), " — O(1) average hash set lookup. The string s[:i] is hashed and checked."])),
    N.callout("Trade-off vs Trie: The HashSet approach is simpler to code (no custom class) but creates O(m·d) string objects during the build phase, each requiring hashing and storage. The Trie reuses shared prefix nodes, so its memory footprint can be smaller when many arr1 numbers share long prefixes.", "⚖️", "yellow_background"),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(m·n·d)", "O(1)", "TLE for large arrays"],
        ["HashSet of Prefixes", "O((m+n)·d)", "O(m·d)", "Simple; string object overhead"],
        ["Trie (Interview Pick)", "O((m+n)·d)", "O(m·d)", "Canonical; efficient node reuse"],
    ]),
    N.para(N.rich([("m, n", {"code": True}), " = array sizes; ", ("d", {"code": True}), " = max digits per number (≤ 10 for 32-bit integers). Since d is bounded by a small constant, all O((m+n)·d) solutions are effectively ", ("O(m+n)", {"code": True}), " — linear in array size."])),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Tries"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Trie Intersection — building a Trie from one array and querying it with another to find cross-array prefix matches."])),
    N.callout("When to recognize this pattern: The problem asks for the longest common PREFIX between ANY pair drawn from two different arrays/sets. One array acts as the 'dictionary' (build the Trie), the other as 'queries'. Whenever you see 'prefix' + 'cross-array matching' + large inputs → Trie Intersection.", "🔎", "green_background"),
    N.para(N.rich([("Note: ", {"italic": True}), "The sub-pattern 'Trie Intersection' is based on problem analysis — the specific two-array prefix-query pattern is not explicitly listed by this name in the guide, but maps to the Tries section (Section 13)."])),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Trie / prefix technique:"),
    N.bullet(N.rich([("Implement Trie (Prefix Tree)", {"bold": True}), " (Medium) — Build the canonical Trie data structure with insert, search, and startsWith (#208)"])),
    N.bullet(N.rich([("Longest Word in Dictionary", {"bold": True}), " (Medium) — Trie + BFS/DFS to find the longest word where every prefix also exists in the dictionary (#720)"])),
    N.bullet(N.rich([("Search Suggestions System", {"bold": True}), " (Medium) — Trie + prefix walk to generate top-3 autocomplete suggestions per input character (#1268)"])),
    N.bullet(N.rich([("Replace Words", {"bold": True}), " (Medium) — Trie to look up the shortest dictionary root that prefixes each word in a sentence (#648)"])),
    N.bullet(N.rich([("Design Add and Search Words Data Structure", {"bold": True}), " (Medium) — Trie with wildcard '.' support using DFS backtracking (#211)"])),
    N.bullet(N.rich([("Longest Common Prefix (string array)", {"bold": True}), " (Easy) — Simpler version on a single array; Trie or sort-based solution (#14)"])),
    N.bullet(N.rich([("Maximum XOR of Two Numbers in an Array", {"bold": True}), " (Medium) — Binary Trie where each bit level is a node; greedy opposite-bit query to maximize XOR (#421)"])),
    N.para("These problems all share the Trie's core power: O(d) insert and O(d) prefix-query, enabling operations that would otherwise require O(n·d) brute-force comparisons."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 13: Tries. Sub-pattern: Trie Intersection (analysis-based classification).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks added: {len(blocks)}")
