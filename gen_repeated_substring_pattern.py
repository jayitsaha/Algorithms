"""gen_repeated_substring_pattern.py — Notion rebuild for LC #459 Repeated Substring Pattern."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ee-8476-f72844635dfe"

# ── 1) Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=459,
    pattern="String Processing",
    subpatterns=["KMP Failure Function", "String Rotation (s+s Trick)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="If s has period p, it appears in (s+s)[1:-1]; equivalently, lps[-1]=L and n%(n-L)==0 via KMP.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string "),
        ("s", {"code": True}),
        (", check if it can be constructed by taking a substring of it and appending multiple copies of the substring together. "
         "Return "), ("True", {"code": True}),
        (" if possible, "), ("False", {"code": True}), (" otherwise.")
    ])),
    N.divider(),
]

# ── Solution 1: s+s Trick ─────────────────────────────────────────────────────
sol1_code = '''\
def repeatedSubstringPattern(s: str) -> bool:
    return s in (s + s)[1:-1]\
'''

sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We need to know if string s is 'periodic' — built by repeating some shorter block. Equivalently: can we write s = p × k for some substring p and integer k ≥ 2?"),
    N.h4("What Doesn't Work"),
    N.para("Trying every possible period length p (from 1 to n//2) and checking if s[:p] repeated n/p times equals s is correct but O(n²) — the inner string comparison is O(n) and we try up to O(n) divisors."),
    N.h4("The Key Observation"),
    N.para("If s has period p (repeating unit of length p), then the string (s+s) contains s at position p — a 'rotated' occurrence. The rotation by p recovers s exactly. Conversely, if s appears in (s+s) anywhere other than position 0 and n, that position gives us a valid period."),
    N.h4("Building the Solution"),
    N.para("Form doubled = (s + s)[1:-1] — we strip one char from each end to remove the trivial matches at index 0 (s itself) and index n (s again). Then check: is s in doubled? Python's 'in' uses an O(n) optimised search. One line."),
    N.callout("Analogy: Think of s+s as a circular band. A period p means there's a seam at position p where the pattern 'restarts'. Slicing off endpoints removes the two obvious seams (at 0 and n), leaving only the real ones.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — s+s Concatenation Trick (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("s + s", {"code": True}),
        (" — concatenate s with itself, making a string of length 2n")
    ])),
    N.para(N.rich([
        ("[1:-1]", {"code": True}),
        (" — strip the first and last character. This removes the trivial match at index 0 (s itself) and index n (s again). Now only 'rotated' occurrences remain, which correspond to real periods.")
    ])),
    N.para(N.rich([
        ("s in ...", {"code": True}),
        (" — Python's membership test for strings internally uses an O(n) algorithm. If s appears anywhere in the trimmed doubled string, s has a valid repeating period.")
    ])),
    N.divider(),
]

# ── Solution 2: KMP Failure Function ─────────────────────────────────────────
sol2_code = '''\
def repeatedSubstringPattern(s: str) -> bool:
    n = len(s)
    lps = [0] * n           # failure function array
    length = 0              # current prefix-suffix border length
    i = 1                   # lps[0] = 0 always; start at 1
    while i < n:
        if s[i] == s[length]:   # extend border
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:        # mismatch: fall back via lps (KEY KMP step)
            length = lps[length - 1]
        else:                   # mismatch, length=0: no border here
            lps[i] = 0
            i += 1
    L = lps[-1]             # longest border of entire string
    period = n - L          # candidate minimal period length
    return L > 0 and n % period == 0\
'''

sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("We want the 'minimal period' of s. The KMP failure function reveals this directly: lps[i] stores the longest proper prefix of s[0..i] that is also a suffix. The final value lps[n-1] encodes how much of the beginning overlaps with the end — and that overlap gap is the period."),
    N.h4("What Doesn't Work"),
    N.para("We can't just check lps[-1] != 0. The border existing doesn't guarantee the string tiles evenly. Example: 'abaab' has lps[-1]=2, period candidate=3, but 5%3≠0 — so it's not a repeated pattern."),
    N.h4("The Key Observation"),
    N.para("If the string has a 'border' of length L (a prefix that equals a suffix), the period is n-L. A string tiles perfectly with that period if and only if the period divides n evenly. The KMP fallback step (length = lps[length-1]) allows O(n) amortized computation by reusing already-known prefix information."),
    N.h4("Building the Solution"),
    N.para("Compute lps in one pass (O(n)). Read lps[-1]=L. Period = n-L. Check L>0 (non-trivial border) and n%(n-L)==0 (even tiling). Both conditions together are necessary and sufficient."),
    N.callout("KMP was invented in 1977 by Knuth, Morris, and Pratt. The failure function's O(n) guarantee comes from an amortized argument: 'length' can increase at most n times total, so even though it may decrease multiple times per step, the total decreases across the whole algorithm are also bounded by n.", "🔬", "gray_background"),
]

blocks += [
    N.h2("Solution 2 — KMP Failure Function (Algorithm Deep-Dive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("🔬 Algorithm Deep-Dive: KMP Failure Function"),
    N.para("Origin: Knuth-Morris-Pratt (1977). Class: string pattern matching and periodicity analysis. The failure function lps[i] = length of longest proper prefix of s[0..i] that is also a suffix."),
    N.code('''\
# KMP Failure Function Template
def build_lps(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1
    while i < n:
        if s[i] == s[length]:
            length += 1; lps[i] = length; i += 1
        elif length > 0:
            length = lps[length - 1]  # KEY: don't increment i here
        else:
            lps[i] = 0; i += 1
    return lps
# Periodicity check: lps[-1]=L → period=n-L → periodic iff n%(n-L)==0 and L>0\
'''),
    N.para("Core invariant: lps[i] = longest proper border of s[0..i]. The fallback length = lps[length-1] reuses already-computed information — we never re-read a character, giving O(n) amortized. Recognize when: 'does a prefix also appear as a suffix?', 'does this string have a repeating period?', 'implement fast substring search'."),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("lps = [0] * n", {"code": True}), (" — initialize failure function. lps[0]=0 always (no proper prefix).")])),
    N.para(N.rich([("length = 0; i = 1", {"code": True}), (" — length tracks current border size; i scans from position 1.")])),
    N.para(N.rich([("if s[i] == s[length]", {"code": True}), (" — characters match: we can extend the current border by 1. Increment both length and i.")])),
    N.para(N.rich([("elif length > 0: length = lps[length-1]", {"code": True}), (" — KEY fallback: mismatch but we had a partial border. Don't advance i. Instead, try the next-shorter border, which is lps[length-1] — already computed, reused here.")])),
    N.para(N.rich([("else: lps[i] = 0; i += 1", {"code": True}), (" — mismatch with length=0: no border possible at i. Set lps[i]=0 and move on.")])),
    N.para(N.rich([("L = lps[-1]; period = n - L", {"code": True}), (" — read final border length; compute minimal period candidate.")])),
    N.para(N.rich([("return L > 0 and n % period == 0", {"code": True}), (" — L>0 ensures we have a non-trivial border; n%period==0 ensures the period tiles s perfectly.")])),
    N.divider(),
]

# ── Solution 3: Brute Force ───────────────────────────────────────────────────
sol3_code = '''\
def repeatedSubstringPattern(s: str) -> bool:
    n = len(s)
    for p in range(1, n // 2 + 1):    # period must be <= n//2
        if n % p == 0:                  # period must divide n
            if s[:p] * (n // p) == s:   # tile and compare
                return True
    return False\
'''

sol3_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para("Try every possible length for the repeating unit, from 1 up to n//2 (since it must repeat at least twice). For each valid divisor, tile and compare."),
    N.h4("What Doesn't Work (to lead to the optimisations)"),
    N.para("This approach is O(n × d(n)) where d(n) is the number of divisors — typically O(n log n) but O(n sqrt(n)) worst case. We propose this as the baseline, then optimise."),
    N.h4("The Key Observation"),
    N.para("Only divisors of n are valid period lengths. We skip non-divisors with the n%p==0 check. The inner comparison s[:p]*(n//p)==s is O(n)."),
    N.h4("Building the Solution"),
    N.para("Enumerate divisors p of n from 1 to n//2. For each, construct the repeated tile and compare. Return True on first match."),
]

blocks += [
    N.h2("Solution 3 — Brute Force (Baseline to Mention First)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol3_intuition_children),
    N.h3("Code"),
    N.code(sol3_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for p in range(1, n // 2 + 1)", {"code": True}), (" — try every period length from 1 to n//2 inclusive (must repeat at least twice).")])),
    N.para(N.rich([("if n % p == 0", {"code": True}), (" — valid period must divide n; skip p that don't (e.g., p=2 for n=9 is skipped).")])),
    N.para(N.rich([("if s[:p] * (n // p) == s", {"code": True}), (" — tile the first p characters n/p times and compare to s. O(n) per check.")])),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n log n)", "O(n)"],
        ["s+s Trick", "O(n)", "O(n)"],
        ["KMP Failure Function", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("String Processing")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("KMP Failure Function; String Rotation (s+s Trick)")])),
    N.callout(
        "When to recognize this pattern: 'Does this string consist of a single block repeated k≥2 times?' "
        "or 'What is the minimal repeating unit in a string?' "
        "Signal words: 'repeated', 'period', 'prefix = suffix overlap'. "
        "KMP failure function is the go-to tool for string periodicity questions.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same KMP Failure Function / string periodicity technique:"),
    N.bullet(N.rich([("Find the Index of the First Occurrence in a String", {"bold": True}),
                     (" (Easy) — Classic KMP full string search, uses the same failure function")])),
    N.bullet(N.rich([("Longest Happy Prefix", {"bold": True}),
                     (" (Hard) — Literally asks you to compute lps[-1] and return s[:lps[-1]]")])),
    N.bullet(N.rich([("Shortest Palindrome", {"bold": True}),
                     (" (Hard) — Build lps on s+'#'+reverse(s); the KMP failure value reveals the longest palindrome prefix")])),
    N.bullet(N.rich([("Repeated String Match", {"bold": True}),
                     (" (Medium) — Find minimum repetitions of a so that b is a substring; uses period math and KMP search")])),
    N.bullet(N.rich([("Longest Duplicate Substring", {"bold": True}),
                     (" (Hard) — Binary search on length + rolling hash (Rabin-Karp), related string technique")])),
    N.bullet(N.rich([("KMP / Implement strStr", {"bold": True}),
                     (" — Building and applying the full KMP pattern match using lps")])),
    N.para("These problems share the core technique: prefix-suffix border analysis via the KMP failure function reveals periodicity, palindrome, or pattern structure in O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 2 — String Processing, Sub-Pattern: KMP / Z-Algorithm", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("repeated_substring_pattern")),
    N.para(N.rich([
        ("Step through the KMP failure function computation visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks sent: {len(blocks)}")
