"""
gen_longest_string_chain.py — Notion in-place update for LeetCode #1048 Longest String Chain
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-817b-bcfd-d2ccdec402e5"

# ── 1. Set properties ─────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1048,
    pattern="Dynamic Programming",
    subpatterns=["Sort by Length + DP"],
    tc="O(n·L²)",
    sc="O(n·L)",
    key_insight="Sort words by length, then for each word try all single-char deletions; if the shorter word exists in dp, extend its chain by 1.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ─────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ─────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of words where ", {}),
        ("words[i]", {"code": True}),
        (" consists of lowercase English letters, return the length of the longest string chain. A word ", {}),
        ("A", {"code": True}),
        (" is a predecessor of word ", {}),
        ("B", {"code": True}),
        (" if you can insert exactly one letter anywhere in ", {}),
        ("A", {"code": True}),
        (" (including start and end) to make it equal to ", {}),
        ("B", {"code": True}),
        (". A string chain is a sequence of words w1, w2, …, wk where each word is a predecessor of the next.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ('words = ["a","b","ba","bca","bda","bdca"]  →  Output: 4\n', {}),
            ('Chain: "a" → "ba" → "bda" → "bdca"  (or  "a" → "ba" → "bca" → "bdca")', {}),
        ]),
        "📝", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: DP Tabulation (bottom-up) ─────────────────────────
blocks += [
    N.h2("Solution 1 — Sort by Length + DP Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest sequence of words w1, w2, …, wk where each word differs from the next by exactly one inserted character. The length of words strictly increases by 1 each step. This has a clear dependency structure: the answer for a longer word depends on answers for shorter words."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: compare all pairs of words — O(n²·L) time. For n=1000 words of length 16, that's 16 million operations just for pair comparisons, and you'd still need to find the longest chain in the resulting graph (more work). We need to exploit the structure."),
        N.h4("The Key Observation"),
        N.para("This is structurally identical to the Longest Increasing Subsequence (LIS) problem. In LIS: sort numbers, for each number X find the best smaller number that can precede X, dp[X] = dp[best_smaller] + 1. Here: sort words by length, for each word W find the best shorter word that can precede W, dp[W] = dp[best_predecessor] + 1."),
        N.h4("Building the Solution"),
        N.para("The check 'is A a predecessor of B?' becomes: try deleting each of B's characters one at a time — if any deletion gives a word that exists in our input, A is a predecessor. Since |B| = L, this is O(L) deletions each taking O(L) string slice → O(L²) per word. Sort + hash map + deletion loop = O(n·L²) total."),
        N.callout("Analogy: Think of it as building a word ladder. Each rung is one character longer. Sorting by length gives you the rungs in order. dp[word] tells you how high you can climb to reach that rung.", "🧠", "blue_background"),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal substructure: ", {"bold": True}),
        ("The longest chain ending at word W = 1 + the longest chain ending at W's best predecessor. This is a direct recursive decomposition.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping subproblems: ", {"bold": True}),
        ("Multiple longer words can share the same predecessor (e.g., both 'bca' and 'bda' have 'ba' as a predecessor). Without memoization, we'd recompute dp['ba'] for each. With a hash map, we compute it once.", {}),
    ])),
    N.callout(
        N.rich([
            ("Recurrence:\n", {"bold": True}),
            ("dp[word] = 1   (base case)\n", {"code": True}),
            ("dp[word] = max(dp[word],  dp[word[:i]+word[i+1:]] + 1)\n", {"code": True}),
            ("             for each i in range(len(word))\n", {"code": True}),
            ("             where (word[:i]+word[i+1:]) exists in dp", {"code": True}),
        ]),
        "📐", "gray_background"
    ),
    N.h3("Code"),
    N.code("""def longestStrChain(self, words: List[str]) -> int:
    # Sort by length: ensures predecessors computed before successors
    words.sort(key=len)

    # dp[word] = length of longest chain ending at word
    dp = {}
    best = 1  # every word forms a chain of at least length 1

    for word in words:
        dp[word] = 1  # base case: chain of just this word

        # Try removing each character to find potential predecessors
        for i in range(len(word)):
            prev = word[:i] + word[i+1:]  # delete char at index i

            if prev in dp:  # predecessor exists and is already computed
                dp[word] = max(dp[word], dp[prev] + 1)

        best = max(best, dp[word])

    return best"""),
    N.h3("Line by Line"),
    N.para(N.rich([("words.sort(key=len)", {"code": True}), (" — Sort by word length ascending. Critical: ensures shorter words (predecessors) are always processed before the longer words that need them.", {})])),
    N.para(N.rich([("dp = {}", {"code": True}), (" — Hash map from word string to chain length. Using a dict instead of array because keys are strings not integers.", {})])),
    N.para(N.rich([("dp[word] = 1", {"code": True}), (" — Base case: every word is at minimum a chain of length 1 (just itself). We start here and try to extend.", {})])),
    N.para(N.rich([("prev = word[:i] + word[i+1:]", {"code": True}), (" — Remove character at index i via slice. This is one possible predecessor of 'word'. O(L) per operation.", {})])),
    N.para(N.rich([("if prev in dp:", {"code": True}), (" — Two things happen here: (1) check if 'prev' exists as an input word, and (2) verify its dp value is already computed (guaranteed since prev is shorter and was sorted earlier).", {})])),
    N.para(N.rich([("dp[word] = max(dp[word], dp[prev]+1)", {"code": True}), (" — Extend the chain: dp[prev] chain + current word = dp[prev]+1. Take max over all valid predecessors.", {})])),
    N.para(N.rich([("best = max(best, dp[word])", {"code": True}), (" — Track global maximum. We check after fully processing each word (all its predecessors have been tried).", {})])),
    N.callout("⚠️ Why check 'if prev in dp' instead of 'if prev in word_set'? Both work, but dp only contains already-processed words (shorter ones), so there's no risk of a stale lookup. Using dp is cleaner and self-documenting.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 2: Memoization ───────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DP Memoization (Top-Down)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Express the answer recursively: dp(word) = length of the longest chain ending at word. Base: if no predecessor exists in word_set, return 1. Recursive: 1 + max(dp(prev)) over all valid predecessors."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization would recompute dp(word) every time another longer word tries to use it as a predecessor. With n words sharing common ancestors, this blows up exponentially."),
        N.h4("The Key Observation"),
        N.para("Add a memo dictionary. Once dp(word) is computed, cache it. Subsequent calls with the same word return the cached result in O(1). This transforms exponential recursion into O(n·L²)."),
        N.h4("Building the Solution"),
        N.para("The top-down approach naturally mirrors the recurrence relation. It does not require sorting (the recursion handles ordering automatically — a deeper call for 'prev' completes before the calling word's dp is cached). However, it does require word_set for membership checks."),
    ]),
    N.h3("Code"),
    N.code("""def longestStrChain(self, words: List[str]) -> int:
    word_set = set(words)  # O(1) membership test for predecessors
    memo = {}              # word → longest chain length ending here

    def dp(word: str) -> int:
        if word in memo:
            return memo[word]  # cache hit: already computed

        best = 1  # chain of just this word
        for i in range(len(word)):
            prev = word[:i] + word[i+1:]  # try each single deletion
            if prev in word_set:
                best = max(best, dp(prev) + 1)  # recurse on predecessor

        memo[word] = best  # cache before returning
        return best

    return max(dp(w) for w in words)  # try every word as chain endpoint"""),
    N.h3("Line by Line"),
    N.para(N.rich([("word_set = set(words)", {"code": True}), (" — Build a set for O(1) predecessor existence checks. Unlike the tabulation approach, we can't use dp as the membership oracle here (dp is only populated on-demand).", {})])),
    N.para(N.rich([("if word in memo: return memo[word]", {"code": True}), (" — Memoization check. If we've already computed dp(word) from a previous call, return it immediately in O(1).", {})])),
    N.para(N.rich([("if prev in word_set:", {"code": True}), (" — Only recurse if prev is an actual input word. This prevents infinite recursion (prev is strictly shorter, so recursion terminates).", {})])),
    N.para(N.rich([("memo[word] = best", {"code": True}), (" — Cache the result. Critical: this must happen before returning, not after, to ensure the result is available for future callers.", {})])),
    N.para(N.rich([("return max(dp(w) for w in words)", {"code": True}), (" — We call dp on every word (not just the longest). dp on a shorter word does work too — it might be the endpoint of the longest chain.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DP Tabulation (bottom-up)", "O(n·L²)", "O(n·L)"],
        ["DP Memoization (top-down)", "O(n·L²)", "O(n·L)"],
        ["Brute Force (all pairs)", "O(n²·L)", "O(n)"],
    ]),
    N.para(N.rich([
        ("Where n = number of words, L = max word length (≤ 16 per constraints). ", {}),
        ("O(n·L²) ", {"bold": True}),
        ("= for each of n words, try L deletions each taking O(L) time. With L≤16, this is effectively O(256n) — linear in n.", {}),
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort by Length + DP (structurally a variant of DP: LIS applied to word relationships)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern:\n", {"bold": True}),
            ("• Problem asks for 'longest chain/path/sequence' where each element extends from another\n", {}),
            ("• Each element has a natural size/rank (string length, number value) defining ordering\n", {}),
            ("• The 'can X precede Y?' check is O(poly) — a hash map DP avoids recomputing\n", {}),
            ("• Multiple elements may share the same predecessor (overlapping subproblems)", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same 'longest chain ending here' DP technique:"),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), (" (Medium) — Sort + LIS: dp[i] = 1 + max(dp[j]) for j < i with nums[j] < nums[i]. Canonical template.", {})])),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}), (" (Hard) — Sort by width, then LIS on height. Same 2D chain structure.", {})])),
    N.bullet(N.rich([("Concatenated Words", {"bold": True}), (" (Hard) — Words composed of shorter words from the set; DP + word set dictionary.", {})])),
    N.bullet(N.rich([("Word Break", {"bold": True}), (" (Medium) — Can a string be segmented into dictionary words? DP + hash set.", {})])),
    N.bullet(N.rich([("Delete Operation for Two Strings", {"bold": True}), (" (Medium) — Minimum deletions to make two strings equal; LCS-based DP.", {})])),
    N.bullet(N.rich([("Maximum Length of Pair Chain", {"bold": True}), (" (Medium) — Sort pairs by end value, then LIS-style DP. Identical template on number pairs.", {})])),
    N.bullet(N.rich([("Number of Matching Subsequences", {"bold": True}), (" (Medium) — Match words against a string; word set + DP approach.", {})])),
    N.para("These problems share the same core insight: sort by a 'size' dimension, then use a hash map DP where each element's answer = 1 + best predecessor's answer."),
]

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_string_chain")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
