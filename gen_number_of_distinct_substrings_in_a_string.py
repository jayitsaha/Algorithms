"""
gen_number_of_distinct_substrings_in_a_string.py
Regenerates the Notion page for LC #1698 — Number of Distinct Substrings in a String
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8105-a7e8-cc6d12ec69b6"
SLUG = "number_of_distinct_substrings_in_a_string"

# ─── Step 1: Set page properties ───
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1698,
    pattern="String",
    subpatterns=["Suffix Array or Rolling Hash"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="Rolling hash makes each substring window O(1) to hash; Suffix Array+LCP gives distinct = n(n+1)/2+1 − sum(LCP).",
    icon="🟡"
)
print("Properties set OK.")

# ─── Step 2: Wipe old body ───
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── Step 3: Build the new body ───
print("Building blocks...")
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", return the number of ", {}),
        ("distinct", {"bold": True}),
        (" substrings of ", {}),
        ("s", {"code": True}),
        (", including the empty substring.", {}),
    ])),
    N.para(N.rich([
        ("Example: s = ", {}), ('"abab"', {"code": True}),
        (' → 8 distinct substrings: "", "a", "b", "ab", "ba", "aba", "bab", "abab".', {}),
    ])),
    N.para(N.rich([
        ("Example: s = ", {}), ('"aab"', {"code": True}),
        (' → 6. Note "a" appears at index 0 and 1 — count it once.', {}),
    ])),
    N.callout(
        N.rich([("Key Insight: ", {"bold": True}),
                ('A string of length n has n(n+1)/2 + 1 substrings total (including empty). '
                 'The challenge is deduplication. '
                 'Brute force: O(n³). Rolling Hash: O(n²). Suffix Array + LCP: O(n log n).', {})]),
        "💡", "green_background"
    ),
    N.divider(),
]

# ─── Solution 1: Brute Force ───
blocks += [
    N.h2("Solution 1 — Brute Force Hash Set"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to count unique substrings. A set automatically deduplicates. So: enumerate every s[i:j] and add to a set. Answer = len(set)."),
        N.h4("What Doesn't Work (Scale)"),
        N.para("For each of the O(n²) substrings, Python must hash it — which costs O(length) per substring. With lengths from 1 to n, total cost is O(1+2+...+n) per start index = O(n³). Fine for small n; too slow for n > ~1000."),
        N.h4("The Key Observation"),
        N.para("Python's set and frozenset handle string hashing natively. The code is 2 lines using a set comprehension. This is the first solution to propose — simple, correct, readable."),
        N.h4("Building the Solution"),
        N.para('Start with {""}. Nested loops i, j. For each (i,j), add s[i:j]. Return len(seen).'),
        N.callout("Analogy: Keep a notebook of every phrase you encounter; cross out duplicates. At the end, count the remaining unique phrases.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
"""def countDistinct(s: str) -> int:
    n = len(s)
    seen = {""}            # seed with the empty string
    for i in range(n):
        for j in range(i + 1, n + 1):
            seen.add(s[i:j])  # O(j-i) to slice and hash
    return len(seen)""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([('seen = {""}', {"code": True}), (" — Initialize the result set with the empty string. We count it from the start.", {})])),
    N.para(N.rich([("for i in range(n)", {"code": True}), (" — Outer loop: every possible start index for a substring.", {})])),
    N.para(N.rich([("for j in range(i+1, n+1)", {"code": True}), (" — Inner loop: every end index. s[i:j] covers indices [i, j).", {})])),
    N.para(N.rich([("seen.add(s[i:j])", {"code": True}), (" — Extract substring and add to set. Python hashes the string in O(j-i). The set handles deduplication automatically.", {})])),
    N.para(N.rich([("return len(seen)", {"code": True}), (" — Total unique substrings including the empty string.", {})])),
    N.divider(),
]

# ─── Solution 2: Rolling Hash (Interview Pick) ───
blocks += [
    N.h2("Solution 2 — Rolling Hash (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The bottleneck in brute force is hashing each substring fresh in O(length). Can we compute the hash of a new window from the previous window's hash in O(1)?"),
        N.h4("What Doesn't Work"),
        N.para("We cannot just compare substrings directly — that is still O(length) per comparison. We need a numeric fingerprint (hash) that updates cheaply."),
        N.h4("The Key Observation — Polynomial Rolling Hash"),
        N.para('Treat each substring as a polynomial: h(s[i..i+L-1]) = s[i]·BASE^(L-1) + s[i+1]·BASE^(L-2) + ... + s[i+L-1]. When we slide right by one, the new hash is (h_old × BASE − s[i]·BASE^L + s[i+L]) mod MOD — only 3 arithmetic operations, O(1) per slide.'),
        N.h4("Building the Solution"),
        N.para("For each length L from 1 to n: initialize rolling hash, slide window, track seen hashes. Each new hash = new distinct substring. Sum |seen| across all lengths. Add 1 for the empty string."),
        N.callout("Analogy: Instead of spelling out every word to identify duplicates, use the word's Scrabble score as a fast fingerprint. Same score = likely same word. Rolling = update the score in O(1) when you swap one letter at the boundary.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Rabin-Karp Rolling Hash"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Introduced by Rabin and Karp (1987) for pattern matching. Treats strings as polynomials over integer alphabet, evaluated at BASE modulo a prime MOD.", {}),
    ])),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("H(i) = Σ char(s[i+k]) × BASE^(L-1-k) mod MOD for k in [0,L-1]. "
         "Slide update: H(i+1) = (H(i)×BASE − char(s[i])×BASE^L + char(s[i+L])) mod MOD. "
         "Only 3 operations — O(1) per step.", {}),
    ])),
    N.para(N.rich([
        ("Why It Works: ", {"bold": True}),
        ("Two different strings produce the same hash (collision) with probability at most (L-1)/MOD per pair — negligible for large prime MOD (~10⁹). "
         "Double hashing (two (BASE,MOD) pairs) reduces this to ~1/MOD² ≈ 10⁻¹⁸.", {}),
    ])),
    N.para(N.rich([
        ("Recognize When: ", {"bold": True}),
        ("\"distinct substrings\", \"duplicate substrings\", \"pattern matching\", \"longest repeated substring\". "
         "Any sliding-window problem where window identity matters and O(1) update is needed.", {}),
    ])),
    N.code(
"""# Rolling Hash Template
MOD = 10**9 + 7
BASE = 31  # prime; maps 'a'→1, ..., 'z'→26

def rolling_hash_windows(s, L):
    '''Yield hashes of all length-L windows of s.'''
    h = 0
    power = pow(BASE, L, MOD)  # BASE^L mod MOD
    for i in range(len(s)):
        c = ord(s[i]) - ord('a') + 1  # map to [1,26]; avoid 0!
        h = (h * BASE + c) % MOD
        if i >= L:  # window overflowed: roll out leftmost char
            lc = ord(s[i - L]) - ord('a') + 1
            h = (h - lc * power) % MOD
        if i >= L - 1:  # full window formed
            yield h""",
        "python"
    ),
    N.h3("Code"),
    N.code(
"""def countDistinct(s: str) -> int:
    n = len(s)
    MOD = 10**9 + 7
    BASE = 31
    distinct = 1  # count the empty string upfront
    for length in range(1, n + 1):
        seen = set()
        h = 0
        power = pow(BASE, length, MOD)
        for i in range(n):
            c = ord(s[i]) - ord('a') + 1    # 'a'→1, ..., 'z'→26
            h = (h * BASE + c) % MOD        # roll in right char
            if i >= length:                  # roll out left char
                lc = ord(s[i - length]) - ord('a') + 1
                h = (h - lc * power) % MOD
            if i >= length - 1:              # full window formed
                seen.add(h)
        distinct += len(seen)
    return distinct""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("distinct = 1", {"code": True}), (" — Count the empty string immediately so we don't need a special case later.", {})])),
    N.para(N.rich([("for length in range(1, n+1)", {"code": True}), (" — Outer loop over every possible window size from 1 to n.", {})])),
    N.para(N.rich([("seen = set()", {"code": True}), (" — Fresh hash set for this window size only. We reset per length.", {})])),
    N.para(N.rich([("power = pow(BASE, length, MOD)", {"code": True}), (" — Precompute BASE^length once per outer loop. This is the factor needed to roll off the leftmost character.", {})])),
    N.para(N.rich([("c = ord(s[i]) - ord('a') + 1", {"code": True}), (" — Map character to integer in [1,26]. Critical: avoid 0 to prevent spurious collisions (e.g., 'a'=0 would make 'a', 'aa', 'aaa' all hash to 0 in some configurations).", {})])),
    N.para(N.rich([("h = (h * BASE + c) % MOD", {"code": True}), (" — Roll in the new right character: shift polynomial left by one position and add new term.", {})])),
    N.para(N.rich([("if i >= length:", {"code": True}), (" — Window has grown past size L? Time to roll off the leftmost character.", {})])),
    N.para(N.rich([("h = (h - lc * power) % MOD", {"code": True}), (" — Subtract the leftmost character's contribution (its weight is BASE^length). The % MOD handles potential negatives in Python correctly.", {})])),
    N.para(N.rich([("if i >= length - 1: seen.add(h)", {"code": True}), (" — Only record the hash once the window is fully formed (at least L characters). Each new hash = one new distinct substring.", {})])),
    N.para(N.rich([("distinct += len(seen)", {"code": True}), (" — Add the count of unique hashes at this length to the running total.", {})])),
    N.callout(
        N.rich([("⚠️ Hash Collisions: ", {"bold": True}),
                ("Two different substrings might produce the same hash. Use a large prime MOD (10⁹+7 or 10⁹+9) and a prime BASE (31 or 131). "
                 "For production correctness, use double hashing: maintain two (BASE, MOD) pairs and store tuple hashes. "
                 "Collision probability drops to ~1/MOD² ≈ 10⁻¹⁸.", {})]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ─── Solution 3: Suffix Array + LCP ───
blocks += [
    N.h2("Solution 3 — Suffix Array + LCP (Asymptotically Optimal)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Every substring is a prefix of some suffix. If we sort all suffixes lexicographically, adjacent suffixes in sorted order share the most similar prefixes — those are exactly the duplicates to subtract."),
        N.h4("What Doesn't Work"),
        N.para("Rolling hash still requires O(n²) work since we process O(n) windows for each of n lengths. Can we count distinct substrings without looking at every one individually?"),
        N.h4("The Key Observation — Suffix Array Formula"),
        N.para("Total non-empty substrings = n(n+1)/2 (each suffix of length L contributes L substrings). But adjacent sorted suffixes share lcp[i] identical prefixes — those were already counted by the previous suffix. So distinct non-empty = n(n+1)/2 − sum(LCP). Add 1 for the empty string."),
        N.h4("Building the Solution"),
        N.para("Sort suffix start indices. Compute LCP between adjacent pairs. Apply formula. With SA-IS + Kasai's algorithm, this is O(n) SA construction + O(n) LCP = O(n) total (or O(n log n) with simpler SA construction)."),
        N.callout("Analogy: Sort all the pages of a dictionary. Adjacent pages share the most letters at the start (e.g., 'aardvark' and 'aardwolf' both start with 'aard'). The LCP tells us how many prefixes were already counted on the previous page.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Suffix Array + LCP"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Suffix Arrays introduced by Manber & Myers (1993). LCP Array (Kasai's algorithm, 2001) enables linear-time LCP construction from the SA. Together they replace Suffix Trees for most competitive programming needs.", {}),
    ])),
    N.para(N.rich([
        ("Formula: ", {"bold": True}),
        ("distinct_non_empty = Σ (len(sa[i]) − lcp[i]) over all i, where lcp[0]=0. "
         "Each suffix sa[i] of length L contributes L − lcp[i] new prefixes not shared with the previous suffix. "
         "Add 1 for the empty string.", {}),
    ])),
    N.para(N.rich([
        ("Why It Works: ", {"bold": True}),
        ("In the sorted suffix array, adjacent suffixes share the longest possible common prefixes (since they are adjacent in lex order). "
         "lcp[i] = |LCP(sa[i-1], sa[i])| exactly measures how many prefixes of sa[i] were already counted as prefixes of sa[i-1]. "
         "Subtracting prevents double-counting.", {}),
    ])),
    N.para(N.rich([
        ("Recognize When: ", {"bold": True}),
        ("\"Count distinct substrings\", \"longest repeated substring\", \"minimum unique substring\", "
         "or any problem requiring global reasoning over ALL substrings simultaneously. "
         "SA+LCP handles them all in O(n log n).", {}),
    ])),
    N.code(
"""# Suffix Array + LCP — example for s="aab"
# Suffixes: "aab"(0), "ab"(1), "b"(2)
# Sorted:   "aab"(0), "ab"(1), "b"(2)  → sa = [0, 1, 2]
# LCP:      lcp[0]=0, lcp[1]=LCP("aab","ab")=1, lcp[2]=LCP("ab","b")=0
# Formula:  3(4)/2 + 1 - (0+1+0) = 6+1-1 = 6 ✓

def countDistinct(s: str) -> int:
    n = len(s)
    sa = sorted(range(n), key=lambda i: s[i:])  # O(n² log n)
    def lcp(a, b):
        l = 0
        while a+l < n and b+l < n and s[a+l] == s[b+l]:
            l += 1
        return l
    total = n * (n + 1) // 2 + 1  # all possible + empty
    for i in range(1, n):
        total -= lcp(sa[i-1], sa[i])  # subtract shared prefixes
    return total""",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("sa = sorted(range(n), key=lambda i: s[i:])", {"code": True}), (" — Build suffix array by sorting suffix start indices by their suffix string. Simple O(n² log n); SA-IS gives O(n).", {})])),
    N.para(N.rich([("def lcp(a, b)", {"code": True}), (" — Compute Longest Common Prefix of s[a:] and s[b:] by comparing characters one by one. O(n) worst case per pair; Kasai's algorithm computes all LCPs in O(n) total.", {})])),
    N.para(N.rich([("total = n*(n+1)//2 + 1", {"code": True}), (" — Start with the count of ALL possible substrings (each suffix of length L contributes L prefixes; sum = n(n+1)/2) plus 1 for the empty string.", {})])),
    N.para(N.rich([("total -= lcp(sa[i-1], sa[i])", {"code": True}), (" — For each adjacent pair in sorted order, subtract the shared prefix length. These were already counted when processing the previous (smaller) suffix.", {})])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Set", "O(n³)", "O(n²)", "Simple; too slow for n > ~1000"],
        ["Rolling Hash", "O(n²)", "O(n)", "Interview pick; practical and explainable"],
        ["Suffix Array + LCP", "O(n log n)", "O(n)", "Optimal; complex to implement live"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("String Processing", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Suffix Array or Rolling Hash", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ('"Count distinct substrings/subsequences" — use rolling hash (O(n²)) or suffix array (O(n log n)). '
                 '"Longest/shortest repeated substring" — binary search on length + rolling hash. '
                 '"Pattern matching in O(n+m)" — Rabin-Karp rolling hash. '
                 '"Any problem over all O(n²) substrings efficiently" — suffix array + LCP.', {})]),
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}),
                   ("This sub-pattern classification is based on analysis of the algorithm families used. "
                    "The problem uses Rabin-Karp rolling hash or Suffix Array + LCP — both named algorithm structures. "
                    "Not explicitly listed by this exact name in the DSA Patterns Guide.", {"italic": True})])),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using Suffix Array or Rolling Hash:"),
    N.bullet(N.rich([("Longest Duplicate Substring", {"bold": True}), (" (Hard) — Binary search on length + rolling hash to find longest repeated substring (#1044)", {})])),
    N.bullet(N.rich([("Repeated DNA Sequences", {"bold": True}), (" (Medium) — All 10-char substrings appearing more than once; rolling hash + set (#187)", {})])),
    N.bullet(N.rich([("Longest Happy Prefix", {"bold": True}), (" (Hard) — Longest prefix that is also a suffix; rolling hash or KMP failure function (#1392)", {})])),
    N.bullet(N.rich([("Shortest Palindrome", {"bold": True}), (" (Hard) — Find shortest palindrome by prepending; rolling hash on reversed string or KMP (#214)", {})])),
    N.bullet(N.rich([("Find the Index of the First Occurrence in a String", {"bold": True}), (" (Easy) — Rabin-Karp is the classic O(n+m) pattern matching approach (#28)", {})])),
    N.bullet(N.rich([("Count Vowel Substrings of a String", {"bold": True}), (" (Easy) — Same substring enumeration pattern, sliding window + set (#2062)", {})])),
    N.bullet(N.rich([("Number of Pairs of Interchangeable Rectangles", {"bold": True}), (" (Medium) — Deduplication by ratio hash; analogous hash-based grouping (#2001)", {})])),
    N.para("These problems all share the core technique: hash or structurally compare substrings without materializing every pair in O(n) time each."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 2 (String Processing). Sub-Pattern: Suffix Array or Rolling Hash (analysis-based classification).", "📚", "gray_background"),
    N.divider(),
]

# ─── Embed ───
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the Rolling Hash algorithm visually — use Next/Prev or arrow keys to see each window slide and hash update.", {"italic": True, "color": "gray"})])),
]

# ─── Append all blocks ───
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
