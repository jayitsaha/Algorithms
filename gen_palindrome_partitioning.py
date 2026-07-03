"""
gen_palindrome_partitioning.py
Notion regeneration for LeetCode #131 — Palindrome Partitioning
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812f-8613-ef70e1fe7b57"

# ── Step 1: Set page properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=131,
    pattern="Backtracking",
    subpatterns=["Partition + Check Palindrome"],
    tc="O(n * 2^n)",
    sc="O(n)",
    key_insight="Try every prefix; only recurse when prefix is palindrome. Backtrack (pop) after each recursive call to explore all branches.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe existing page body ──────────────────────────────────────────
print("Wiping existing blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build new page body ───────────────────────────────────────────────
blocks = []

# ── PROBLEM ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", partition ", {}),
        ("s", {"code": True}),
        (" such that every substring of the partition is a palindrome. Return all possible palindrome partitions of ", {}),
        ("s", {"code": True}),
        (".", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('s = "aab"  →  [["a","a","b"], ["aa","b"]]', {"code": True}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ s.length ≤ 16, s consists only of lowercase English letters.", {}),
    ])),
    N.divider(),
]

# ── SOLUTION 1 ────────────────────────────────────────────────────────────────
sol1_code = '''\
def partition(s: str) -> List[List[str]]:
    result, path = [], []
    n = len(s)

    def is_palindrome(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1; r -= 1
        return True

    def backtrack(start):
        if start == n:
            result.append(path[:])   # snapshot — NOT result.append(path)
            return
        for end in range(start, n):
            if is_palindrome(start, end):
                path.append(s[start:end+1])  # choose
                backtrack(end + 1)            # explore
                path.pop()                    # unchoose (backtrack)

    backtrack(0)
    return result\
'''

blocks += [
    N.h2("Solution 1 — Backtracking + Inline Palindrome Check (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para('We need every possible way to "cut" the string into pieces where each piece reads the same forwards and backwards. Think of it as deciding: at each position, where does the next palindrome piece end?'),
        N.h4("What Doesn't Work"),
        N.para('A naive approach — generate all 2^(n-1) possible cuts first, then filter — works but wastes time on invalid partitions. We want to prune non-palindrome branches before recursing.'),
        N.h4("The Key Observation"),
        N.para('If we fix a starting position start, we can try every possible ending position end. If s[start:end+1] is a palindrome, we commit to it and recurse on the rest. If it\'s not, skip — never recurse on that branch. This is the pruning that makes backtracking efficient.'),
        N.h4("Building the Solution"),
        N.para('1. At each call to backtrack(start), loop end from start to n-1. 2. Check if s[start:end+1] is a palindrome using two pointers. 3. If yes: append piece to path, recurse backtrack(end+1), then pop (backtrack). 4. Base case: when start == n, all of s is covered → record path[:]'),
        N.callout(
            'Analogy: Think of a sushi chef slicing a roll. At each position, he tries cutting at every point ahead. He only continues with cuts that produce a valid palindrome piece. If a cut is bad, he skips it without bothering to plate the roll.',
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("result, path = [], []", {"code": True}), (" — result accumulates all valid partitions; path is the current partial partition being constructed.", {})])),
    N.para(N.rich([("def is_palindrome(l, r):", {"code": True}), (" — Two-pointer palindrome check: expand l forward and r backward, compare characters. Stops as soon as a mismatch is found. O(r-l+1) time, O(1) space.", {})])),
    N.para(N.rich([("def backtrack(start):", {"code": True}), (" — The core recursive function. start is the index of the first character of the next piece to place.", {})])),
    N.para(N.rich([("if start == n:", {"code": True}), (" — Base case: we have consumed the entire string. Every character is now covered by palindrome pieces in path.", {})])),
    N.para(N.rich([("result.append(path[:])", {"code": True}), (" — Copy of path, not a reference. path[:] creates a snapshot of the current state. Writing result.append(path) would store a reference that becomes empty after backtracking.", {})])),
    N.para(N.rich([("for end in range(start, n):", {"code": True}), (" — Try every possible end position. The candidate piece is s[start:end+1]. This loop drives all branching in the decision tree.", {})])),
    N.para(N.rich([("if is_palindrome(start, end):", {"code": True}), (" — Pruning step. If the candidate is not a palindrome, skip this branch entirely. Only palindromes enter path.", {})])),
    N.para(N.rich([("path.append(s[start:end+1])", {"code": True}), (" — Choose: commit this palindrome piece to the current partition.", {})])),
    N.para(N.rich([("backtrack(end + 1)", {"code": True}), (" — Explore: handle the remaining suffix of the string starting from end+1.", {})])),
    N.para(N.rich([("path.pop()", {"code": True}), (" — Unchoose: remove the piece we just added so we can try a longer piece in the next loop iteration. This is the backtracking step — without it, the algorithm is broken.", {})])),
    N.divider(),
]

# ── SOLUTION 2 ────────────────────────────────────────────────────────────────
sol2_code = '''\
def partition(s: str) -> List[List[str]]:
    n = len(s)
    # Precompute pal[i][j] = True iff s[i..j] is a palindrome
    pal = [[False] * n for _ in range(n)]
    for i in range(n):
        pal[i][i] = True          # single char is always palindrome
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                pal[i][j] = (s[i] == s[j])
            else:
                pal[i][j] = (s[i] == s[j] and pal[i+1][j-1])

    result, path = [], []

    def backtrack(start):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if pal[start][end]:          # O(1) lookup — the payoff!
                path.append(s[start:end+1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result\
'''

blocks += [
    N.h2("Solution 2 — Backtracking + DP Precomputed Palindrome Table"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para('Same backtracking structure as Solution 1, but we observe that is_palindrome(l, r) gets called many times on the same substrings across different recursive branches. This is repeated work.'),
        N.h4("What Doesn't Work"),
        N.para('Solution 1 re-checks the same substring palindromicity multiple times. For s="aaaa", s[0:3]="aaa" is checked several times across different call paths.'),
        N.h4("The Key Observation"),
        N.para('We can precompute a 2D boolean table pal[i][j] using DP: pal[i][j] = True iff s[i..j] is a palindrome. Base cases: single chars are always palindromes; length-2 substrings are palindromes iff both chars match. For longer: s[i..j] is palindrome iff s[i]==s[j] AND s[i+1..j-1] is palindrome.'),
        N.h4("Building the Solution"),
        N.para('Fill pal bottom-up by increasing substring length. Then the backtracking is identical to Solution 1 except we replace is_palindrome(start, end) with pal[start][end] — an O(1) table lookup.'),
        N.callout(
            'The DP recurrence: pal[i][j] = (s[i] == s[j]) AND pal[i+1][j-1]. Think of it as "if the outer shell matches and the inner core is a palindrome, the whole thing is a palindrome."',
            "🔐", "purple_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("pal = [[False]*n for _ in range(n)]", {"code": True}), (" — O(n²) boolean table. pal[i][j] will be True iff s[i..j] is a palindrome.", {})])),
    N.para(N.rich([("for i in range(n): pal[i][i] = True", {"code": True}), (" — Base case: every single character is trivially a palindrome.", {})])),
    N.para(N.rich([("for length in range(2, n+1):", {"code": True}), (" — Fill by increasing substring length (bottom-up DP). Shorter substrings are computed before longer ones that depend on them.", {})])),
    N.para(N.rich([("pal[i][j] = (s[i]==s[j] and pal[i+1][j-1])", {"code": True}), (" — The DP recurrence: outer chars match AND the inner substring is already a palindrome (precomputed in a prior iteration).", {})])),
    N.para(N.rich([("if pal[start][end]:", {"code": True}), (" — O(1) palindrome check — the payoff for the O(n²) precomputation. In practice significantly faster than Solution 1 for large n.", {})])),
    N.divider(),
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Backtracking + inline check (Interview Pick)", "O(n · 2ⁿ)", "O(n)", "Simple, correct, prunes non-palindromes"],
        ["Backtracking + DP table", "O(n · 2ⁿ)", "O(n²)", "O(1) per palindrome check; faster in practice"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Partition + Check Palindrome", {})])),
    N.callout(
        "When to recognize this pattern: The problem says 'return all possible partitions/subsets/combinations'. You build solutions incrementally. There's a validity constraint (palindrome) that lets you prune invalid branches before recursing. State is a single position index.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Backtracking / Partition technique:"),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}), (" (Hard) — Minimum cuts version; DP instead of backtracking to count minimum splits (#132).", {})])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), (" (Hard) — Same structure: partition string into valid dictionary words, collect all valid ways (#140).", {})])),
    N.bullet(N.rich([("Subsets", {"bold": True}), (" (Medium) — Classic backtracking: generate all 2ⁿ subsets using include/exclude decisions (#78).", {})])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), (" (Medium) — Backtracking with reuse allowed; target sum as pruning constraint (#39).", {})])),
    N.bullet(N.rich([("Restore IP Addresses", {"bold": True}), (" (Medium) — Partition string into 4 valid IP octets; validity check at each recursive level (#93).", {})])),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets", {"bold": True}), (" (Medium) — Backtracking with equality constraint: distribute nums into k equal-sum groups (#698).", {})])),
    N.para("These problems share the same core technique: at each recursive call, iterate over candidate choices, apply a validity check to prune, append valid choices, recurse, then pop (backtrack)."),
    N.callout("📚 Reference: Backtracking pattern — Partition + Check sub-pattern. Follow-up is LeetCode #132 (Hard) which replaces backtracking with DP for the optimization variant.", "📚", "gray_background"),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("palindrome_partitioning")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks (chunked at 40) ─────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
