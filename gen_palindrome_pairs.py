"""
gen_palindrome_pairs.py — Rebuild Notion page for Palindrome Pairs (LC #336)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-818c-b43a-f2ac0d02a056"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=336,
    pattern=["Tries"],
    subpatterns=["Trie with Palindrome Check"],
    tc="O(n·k²)",
    sc="O(n·k)",
    key_insight="Split each word at every position; if suffix is palindrome, rev(prefix) is the complement; if prefix is palindrome, rev(suffix) is the complement — hash map gives O(1) lookups.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old content ───────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build blocks ────────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of unique words, return all pairs ", {}),
        ("(i, j)", {"code": True}),
        (" such that the concatenation of ", {}),
        ("words[i] + words[j]", {"code": True}),
        (" is a palindrome, where ", {}),
        ("i != j", {"code": True}),
        (". A palindrome reads the same forwards and backwards.", {}),
    ])),
    N.para("Example: words = [\"abcd\",\"dcba\",\"lls\",\"s\",\"sssll\"] → [[0,1],[1,0],[3,2],[2,4]]"),
    N.para("\"abcd\"+\"dcba\" = \"abcddcba\" ✓ | \"s\"+\"lls\" = \"slls\" ✓ | \"lls\"+\"sssll\" = \"llssssll\" ✓"),
    N.divider(),
]

# ── Solution 1: Brute Force ──
BRUTE_CODE = """\
def palindromePairs_brute(words: list[str]) -> list[list[int]]:
    result = []
    for i in range(len(words)):          # O(n) outer
        for j in range(len(words)):      # O(n) inner -> O(n^2)
            if i != j:
                cat = words[i] + words[j]    # O(k) concat
                if cat == cat[::-1]:         # O(k) palindrome check
                    result.append([i, j])
    return result                        # total: O(n^2 * k)
"""

blocks += [
    N.h2("Solution 1 — Brute Force"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Find all ordered pairs where concatenation is a palindrome. Naive: try every pair."),
        N.h4("What Doesn't Work"),
        N.para("O(n^2 * k) time — for n=10,000 words of length k=10, that's 10^9 operations. Python does ~10^7/s, so this would take ~100 seconds. TLE."),
        N.h4("The Key Observation"),
        N.para("Simple correctness. Every valid pair is tried. No case missed. But no optimization either — we're not exploiting any structure."),
        N.h4("Building the Solution"),
        N.para("Two nested loops over all pairs (i,j) with i≠j. Concatenate and reverse-check. Record hits. Simple but slow."),
        N.callout("Analogy: checking every possible combination in a lock — guaranteed to work, guaranteed to be slow.", "🔒", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(words))", {"code": True}), (" — outer loop over all words", {})])),
    N.para(N.rich([("for j in range(len(words))", {"code": True}), (" — inner loop: pair every word with every other", {})])),
    N.para(N.rich([("if i != j", {"code": True}), (" — skip self-pairing (i==j not allowed by problem)", {})])),
    N.para(N.rich([("cat = words[i] + words[j]", {"code": True}), (" — concatenate pair, O(k) string operation", {})])),
    N.para(N.rich([("if cat == cat[::-1]", {"code": True}), (" — palindrome check: compare string to its reverse, O(k)", {})])),
    N.para(N.rich([("result.append([i, j])", {"code": True}), (" — record valid ordered pair by index", {})])),
    N.divider(),
]

# ── Solution 2: Hash Map (Optimal) ──
HASHMAP_CODE = """\
def palindromePairs(words: list[str]) -> list[list[int]]:
    def is_palin(s: str) -> bool:
        return s == s[::-1]                  # O(k)

    # Build word -> index map for O(1) lookups
    word_map = {w: i for i, w in enumerate(words)}
    result = []

    for i, word in enumerate(words):         # O(n) words
        n = len(word)
        for j in range(n + 1):              # O(k) splits: 0..n inclusive
            left  = word[:j]               # prefix
            right = word[j:]               # suffix

            # Case A: right is palindrome -> need rev(left) before word
            # Pattern: [rev(left)] + [left + right] = palindrome
            if is_palin(right):
                rev_left = left[::-1]
                if rev_left in word_map and word_map[rev_left] != i:
                    result.append([word_map[rev_left], i])

            # Case B: left is palindrome -> need rev(right) after word
            # Pattern: [left + right] + [rev(right)] = palindrome
            # Guard j != n prevents duplicate when j == len(word)
            if j != n and is_palin(left):
                rev_right = right[::-1]
                if rev_right in word_map and word_map[rev_right] != i:
                    result.append([i, word_map[rev_right]])

    return result
"""

blocks += [
    N.h2("Solution 2 — Hash Map + 3-Case Decomposition (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of checking all n^2 pairs, fix word A and ask: what specific word B makes A+B a palindrome? If we can derive B from A in O(k) and look it up in O(1), total becomes O(nk^2)."),
        N.h4("What Doesn't Work"),
        N.para("Sorting doesn't help because palindrome structure is positional. Frequency counting doesn't help because order matters. We need structural decomposition."),
        N.h4("The Key Observation"),
        N.para("For A+B to be a palindrome, split A at any position j into left=A[:j] and right=A[j:]. Two cases: (1) if right is already palindrome, we just need B=rev(left) and it goes BEFORE A. (2) if left is palindrome, we need B=rev(right) and it goes AFTER A. These two cases are exhaustive over all split points."),
        N.h4("Building the Solution"),
        N.para("Step 1: Build word_map for O(1) lookups. Step 2: For each word, try all n+1 split points. Step 3: For each split, check Case A (is right palindrome? look up rev(left)) and Case B (is left palindrome? look up rev(right)). Step 4: Add found pairs, avoiding self-reference and duplicates."),
        N.callout("Analogy: Instead of trying all lock combinations, you look at the back of the lock and derive exactly which key must fit — then check if you have that key.", "🗝️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(HASHMAP_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("word_map = {w: i for i, w in enumerate(words)}", {"code": True}), (" — reverse map from word string to its index, built in O(nk)", {})])),
    N.para(N.rich([("for j in range(n + 1)", {"code": True}), (" — n+1 split points: j=0 (empty left) through j=n (empty right), inclusive", {})])),
    N.para(N.rich([("left, right = word[:j], word[j:]", {"code": True}), (" — partition word at split point j into prefix and suffix", {})])),
    N.para(N.rich([("if is_palin(right)", {"code": True}), (" — Case A: suffix is palindrome (includes empty string, always palindrome)", {})])),
    N.para(N.rich([("rev_left = left[::-1]", {"code": True}), (" — the word we need to find: if rev(left) exists, putting it before 'word' forms palindrome", {})])),
    N.para(N.rich([("if rev_left in word_map and word_map[rev_left] != i", {"code": True}), (" — O(1) lookup: exists AND is a different word (not self)", {})])),
    N.para(N.rich([("result.append([word_map[rev_left], i])", {"code": True}), (" — B goes BEFORE A: pair is [B_index, A_index]", {})])),
    N.para(N.rich([("if j != n and is_palin(left)", {"code": True}), (" — Case B: prefix palindrome, guard j!=n prevents duplicate at boundary", {})])),
    N.para(N.rich([("rev_right = right[::-1]", {"code": True}), (" — word needed after A: rev(right)", {})])),
    N.para(N.rich([("result.append([i, word_map[rev_right]])", {"code": True}), (" — A goes BEFORE B: pair is [A_index, B_index]", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²·k)", "O(1)"],
        ["Hash Map + Split", "O(n·k²)", "O(n·k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Tries (Trie-based word lookup and string matching)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Trie with Palindrome Check — the hash map solution is the pragmatic equivalent; a Trie can replace the hash map for prefix/suffix lookup", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'find all pairs from a word list satisfying a palindrome condition' → split-and-derive pattern; (2) complement lookup needed for each element → hash map or Trie; (3) O(n^2) brute force is too slow → fix one element, derive the other in O(k).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (palindrome check + hash/trie lookup):"),
    N.bullet(N.rich([("Valid Palindrome (LC 125)", {"bold": True}), (" (Easy) — foundation palindrome check with two pointers", {})])),
    N.bullet(N.rich([("Longest Palindromic Substring (LC 5)", {"bold": True}), (" (Medium) — expand-around-center; same palindrome detection core", {})])),
    N.bullet(N.rich([("Palindromic Substrings (LC 647)", {"bold": True}), (" (Medium) — count all palindromic substrings; split-and-check structure", {})])),
    N.bullet(N.rich([("Palindrome Partitioning II (LC 132)", {"bold": True}), (" (Hard) — minimum cuts; DP with palindrome precomputation", {})])),
    N.bullet(N.rich([("Word Search II (LC 212)", {"bold": True}), (" (Hard) — Trie of words + DFS grid traversal; same Tries pattern", {})])),
    N.bullet(N.rich([("Add and Search Word (LC 211)", {"bold": True}), (" (Medium) — Trie with wildcard '.' matching", {})])),
    N.bullet(N.rich([("Group Anagrams (LC 49)", {"bold": True}), (" (Medium) — hash map grouping by canonical structural property", {})])),
    N.para("These problems share the core technique: structural decomposition + hash/Trie-based complement lookup."),
    N.callout("📚 Pattern: Tries — Subpattern: Trie with Palindrome Check. The hash map variant is the standard interview solution; Trie is the conceptual foundation.", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("palindrome_pairs")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
