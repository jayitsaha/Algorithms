"""gen_word_break.py — Notion update for Word Break (LeetCode #139)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b7-9e63-c5e303000fcd"

# 1) Set page properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=139,
    pattern="Dynamic Programming",
    subpatterns=["dp[i] = any dp[j] + word match"],
    tc="O(n² · L)",
    sc="O(n)",
    key_insight="dp[i] = True if any dp[j] is True and s[j:i] is in wordDict — reachable positions as stepping stones.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing body
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body blocks
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string "), ("s", {"code": True}),
        (" and a list of strings "), ("wordDict", {"code": True}),
        (", return "), ("true", {"code": True}),
        (" if "), ("s", {"code": True}),
        (" can be segmented into a space-separated sequence of one or more dictionary words. "
         "The same word in the dictionary may be reused multiple times in the segmentation.")
    ])),
    N.para(N.rich([
        ("Example: "), ("s = \"leetcode\"", {"code": True}),
        (", "), ("wordDict = [\"leet\", \"code\"]", {"code": True}),
        (" → "), ("true", {"code": True}),
        (" because \"leet\" + \"code\" = \"leetcode\".")
    ])),
    N.divider(),
]

# Solution 1 — Bottom-Up Tabulation
sol1_code = '''def wordBreak(s, wordDict):
    word_set = set(wordDict)      # O(1) lookup
    n = len(s)
    dp = [False] * (n + 1)       # dp[i] = can s[0:i] be segmented?
    dp[0] = True                  # base case: empty string
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]'''

blocks += [
    N.h2("Solution 1 — Bottom-Up DP / Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of each position 0..n in the string as a stepping stone. You start at position 0 (before the string). You can hop from stone j to stone i if the substring s[j:i] is a dictionary word. The question becomes: can you reach stone n (the end)?"),
        N.h4("What Doesn't Work"),
        N.para("Brute-force recursion tries all possible splits at each position — exponential 2^n time. The same suffixes get re-evaluated from multiple paths. For a string of length 20 this already explodes."),
        N.h4("The Key Observation"),
        N.para("To decide if position i is reachable, we only need to know which earlier positions j are reachable AND whether s[j:i] is in the dictionary. This is optimal substructure: the answer at i depends only on strictly smaller subproblems."),
        N.h4("Building the Solution"),
        N.para("Define dp[i] = True if s[0:i] can be segmented. Base: dp[0] = True (empty string). For each i, try every j < i. If dp[j] is True and s[j:i] is in word_set, set dp[i] = True and stop. Return dp[n]."),
        N.callout("Analogy: Like a river crossing with stepping stones. You're at stone 0. You jump to stone i only if (a) you can reach some intermediate stone j, and (b) there's a valid word-bridge from j to i.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("word_set = set(wordDict)", {"code": True}), (" — convert list to set for O(1) substring membership checks; list lookup is O(k) per query")])),
    N.para(N.rich([("dp = [False] * (n + 1)", {"code": True}), (" — size n+1 so dp[n] covers the full string; dp[i] means 'first i chars segmentable'")])),
    N.para(N.rich([("dp[0] = True", {"code": True}), (" — base case: empty string is always validly segmented (zero words needed)")])),
    N.para(N.rich([("for i in range(1, n + 1)", {"code": True}), (" — build up each end position left to right")])),
    N.para(N.rich([("for j in range(i)", {"code": True}), (" — try every possible start of the last word ending at position i")])),
    N.para(N.rich([("if dp[j] and s[j:i] in word_set", {"code": True}), (" — two conditions: (1) position j is reachable, (2) the substring from j to i is a valid word")])),
    N.para(N.rich([("dp[i] = True; break", {"code": True}), (" — once one valid split is found, mark i reachable and stop trying other j values")])),
    N.para(N.rich([("return dp[n]", {"code": True}), (" — True if the full string s[0:n] can be segmented")])),
    N.divider(),
]

# Solution 2 — Top-Down Memoization
sol2_code = '''def wordBreak(s, wordDict):
    word_set = set(wordDict)
    memo = {}                     # cache: start_index -> bool

    def dp(start):
        if start == len(s):       # used entire string
            return True
        if start in memo:
            return memo[start]
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dp(end):
                memo[start] = True
                return True
        memo[start] = False
        return False

    return dp(0)'''

blocks += [
    N.h2("Solution 2 — Top-Down DP / Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start the recursion from dp(0) = 'can s[0:] be segmented?' At each call, try all prefixes s[start:end] that are in the dictionary, then recurse on dp(end)."),
        N.h4("What Doesn't Work"),
        N.para("Without memoization, dp(end) is called multiple times for the same end index (from different start positions). Memoization caches each start index's answer, reducing calls from exponential to O(n)."),
        N.h4("The Key Observation"),
        N.para("There are only n+1 distinct start indices (0..n). With a cache, each is computed at most once. The memo dictionary maps start_index -> bool."),
        N.h4("Building the Solution"),
        N.para("Write the recursive function naturally: base case (start==n → True), cache hit, then try all words starting at 'start'. If s[start:end] is in dict and dp(end) is True, cache True and return. Otherwise cache False."),
        N.callout("Top-down is often easier to derive — write the recursion first, then add 'if start in memo: return memo[start]' and 'memo[start] = result' around it.", "🧠", "green_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), (" — maps each start index to its bool result; prevents recomputing subproblems")])),
    N.para(N.rich([("if start == len(s)", {"code": True}), (" — base case: we've consumed the entire string with valid words → success")])),
    N.para(N.rich([("if start in memo: return memo[start]", {"code": True}), (" — cache hit; this start was already evaluated; return stored result")])),
    N.para(N.rich([("for end in range(start + 1, len(s) + 1)", {"code": True}), (" — try every possible end of a word starting at 'start'")])),
    N.para(N.rich([("if s[start:end] in word_set and dp(end)", {"code": True}), (" — word is valid AND the remainder is also segmentable?")])),
    N.para(N.rich([("memo[start] = True; return True", {"code": True}), (" — cache success and return immediately (early exit)")])),
    N.para(N.rich([("memo[start] = False; return False", {"code": True}), (" — no valid word starting at 'start' found; cache and return")])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Recursion", "O(2ⁿ)", "O(n) stack"],
        ["Top-Down Memoization", "O(n² · L)", "O(n)"],
        ["Bottom-Up Tabulation ★", "O(n² · L)", "O(n)"],
    ]),
    N.para("n = len(s), L = average word length (for substring hashing). Both DP approaches have identical asymptotic complexity; tabulation avoids recursion overhead."),
    N.divider(),
]

# Why This Is DP
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}),
        ("To determine if s[0:i] can be segmented, we only need to know which positions j < i are reachable and whether s[j:i] is a valid word. The answer at i is fully determined by answers to strictly smaller subproblems.")])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}),
        ("In naive recursion, the same suffix s[k:] may be queried from many different starting calls. With memoization (or tabulation), each of the n+1 positions is computed exactly once.")])),
    N.code("dp[0] = True  # base\ndp[i] = OR { dp[j] AND s[j:i] in word_set  for 0 <= j < i }\nanswer = dp[n]", "python"),
    N.callout("Pattern signal: 'Can the string/array be partitioned into valid pieces from a set?' → 1D boolean DP. If the question were 'count segmentations' → 1D integer DP (same structure, sum instead of OR).", "🔎", "green_background"),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("dp[i] = any dp[j] + word match — 1D boolean reachability DP; each position's answer builds on earlier positions via dictionary word jumps")])),
    N.callout(
        "When to recognize this pattern: (1) 'can the string be segmented/broken/partitioned?', (2) pieces must belong to a dictionary or satisfy a rule, (3) the same substrings appear from multiple paths → overlapping subproblems, (4) boolean answer ('yes/no'). "
        "Extend to integer DP for 'how many segmentations?' or 'minimum words?'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (1D reachability DP / word segmentation):"),
    N.bullet(N.rich([("Word Break II", {"bold": True}), (" (Hard) — return all valid segmentations; same DP + backtracking to reconstruct paths")])),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}), (" (Hard) — minimum cuts to partition into palindromes; dp[i] = min(dp[j]+1) form")])),
    N.bullet(N.rich([("Decode Ways", {"bold": True}), (" (Medium) — count decodings; identical 1D DP structure with position-reachability accumulation")])),
    N.bullet(N.rich([("Concatenated Words", {"bold": True}), (" (Hard) — find words in a list that are formed by concatenating shorter words; calls wordBreak for each candidate")])),
    N.bullet(N.rich([("Interleaving String", {"bold": True}), (" (Medium) — same reachability DP extended to 2D (two source strings instead of one)")])),
    N.bullet(N.rich([("Minimum Cost to Cut a Stick", {"bold": True}), (" (Hard) — interval DP sharing the same optimal-substructure pattern over ranges")])),
    N.para("These problems share the core technique: define dp[i] as a reachable/optimal state at position i, build from dp[0]=base case, use earlier results to fill forward."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18: Dynamic Programming", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("word_break")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
