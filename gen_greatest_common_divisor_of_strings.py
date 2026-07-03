"""
gen_greatest_common_divisor_of_strings.py
Notion regeneration for LC 1071: Greatest Common Divisor of Strings (Easy)
Pattern: Math | Sub-Pattern: GCD of Lengths
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8114-8ee9-e32bf4f94be0"
SLUG = "greatest_common_divisor_of_strings"

# ─── 1. Properties ────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1071,
    pattern="Math",
    subpatterns=["GCD of Lengths"],
    tc="O((m+n) * log(min(m,n)))",
    sc="O(m+n)",
    key_insight="A divisor string t exists iff str1+str2 == str2+str1; then t = str1[:gcd(len1,len2)].",
    icon="🟢",
)
print("Properties set.")

# ─── 2. Wipe old body ─────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─── 3. Build blocks ──────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("str1", {"code": True}),
        (" and ", {}),
        ("str2", {"code": True}),
        (', find the largest string ', {}),
        ("t", {"code": True}),
        (" that divides both strings. A string ", {}),
        ("t", {"code": True}),
        (" divides ", {}),
        ("s", {"code": True}),
        (' if ', {}),
        ("s == t + t + ... + t", {"code": True}),
        (' (i.e., ', {}),
        ("s", {"code": True}),
        (' can be formed by concatenating ', {}),
        ("t", {"code": True}),
        (' one or more times). Return the largest ', {}),
        ("t", {"code": True}),
        (' that divides both ', {}),
        ("str1", {"code": True}),
        (' and ', {}),
        ("str2", {"code": True}),
        ('. If no such string exists, return ', {}),
        ('""', {"code": True}),
        ('.', {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Concatenation + GCD Length (Optimal / Interview Pick) ──
sol1_code = '''\
from math import gcd

def gcdOfStrings(str1: str, str2: str) -> str:
    # Key check: if a divisor exists, both orderings of concat must agree
    if str1 + str2 != str2 + str1:
        return ""
    # The length of the GCD string equals gcd of the two lengths
    g = gcd(len(str1), len(str2))
    return str1[:g]
'''

blocks += [
    N.h2("Solution 1 — Concatenation Check + GCD Length (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the longest string t such that str1 = t * a and str2 = t * b "
            "for some positive integers a and b. Think of it as: both strings are made "
            "by repeating the same 'tile' — find the longest such tile."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try every prefix of str1 and check if it divides str2. "
            "This is O(min(m,n) * (m+n)) and misses the elegant mathematical structure. "
            "It also doesn't immediately tell us whether any common divisor exists."
        ),
        N.h4("The Key Observation"),
        N.para(
            "If t divides both str1 and str2, then str1 + str2 must equal str2 + str1. "
            "Why? Both sides equal t repeated (a+b) times in the same way. Conversely, "
            "if str1+str2 == str2+str1, a common divisor MUST exist. Once we know it "
            "exists, the length of the largest divisor is gcd(len(str1), len(str2)) — "
            "exactly the mathematical GCD applied to string lengths."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Check str1 + str2 == str2 + str1. If not, return \"\". "
            "Step 2: Compute g = gcd(len(str1), len(str2)). "
            "Step 3: Return str1[:g]. The first g characters of str1 are guaranteed "
            "to be the divisor (since str1 is itself a multiple of the divisor starting at index 0)."
        ),
        N.callout(
            "Analogy: Like finding the largest ruler that measures both a 12 cm and 8 cm rod "
            "exactly — that's a ruler of gcd(12,8)=4 cm. The 'ruler' here is the repeated string tile.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("from math import gcd", {"code": True}), " — Import Python's built-in GCD function (Euclidean algorithm, O(log min(m,n)))."])),
    N.para(N.rich([("if str1 + str2 != str2 + str1:", {"code": True}), " — Necessary and sufficient condition: a common divisor string exists if and only if concatenating in both orders yields the same string. If they differ, no t can divide both."])),
    N.para(N.rich([("return \"\"", {"code": True}), " — No common divisor exists; return empty string."])),
    N.para(N.rich([("g = gcd(len(str1), len(str2))", {"code": True}), " — The length of the GCD string equals the GCD of the two lengths, by the same logic as integer GCD. Euclidean algorithm runs in O(log min(m,n))."])),
    N.para(N.rich([("return str1[:g]", {"code": True}), " — Slice the first g characters. Since str1 is a multiple of the divisor and the divisor starts at index 0, this is always the correct answer."])),
    N.divider(),
]

# ── Solution 2 — Brute Force Prefix Check ──
sol2_code = '''\
def gcdOfStrings_brute(str1: str, str2: str) -> str:
    def divides(t, s):
        # Check if t divides s (s is t repeated k times)
        if len(s) % len(t) != 0:
            return False
        k = len(s) // len(t)
        return t * k == s

    # Try all prefixes of the shorter string, largest first
    shorter = str1 if len(str1) <= len(str2) else str2
    for length in range(len(shorter), 0, -1):
        candidate = shorter[:length]
        if divides(candidate, str1) and divides(candidate, str2):
            return candidate
    return ""
'''

blocks += [
    N.h2("Solution 2 — Brute Force Prefix Check"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Directly translate the definition: try every possible length for t, "
            "starting from the longest, and check whether it actually divides both strings."
        ),
        N.h4("What Doesn't Work (at scale)"),
        N.para(
            "This is O(min(m,n) * (m+n)) — feasible for small inputs but the constant "
            "factor is high. The elegant mathematical insight of Solution 1 is absent, "
            "making this harder to extend or verify."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The divisor must be a prefix of both strings. Trying all prefix lengths "
            "of the shorter string in decreasing order guarantees we find the largest first."
        ),
        N.h4("Building the Solution"),
        N.para(
            "For each length from min(len(str1), len(str2)) down to 1: take that prefix "
            "as a candidate. Check if repeating it matches both str1 and str2. Return the "
            "first (longest) match, or \"\" if none found."
        ),
        N.callout(
            "Use this approach to double-check your Solution 1 during an interview — "
            "it's simple to state and verify, even if not optimal.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def divides(t, s):", {"code": True}), " — Helper: check if t divides s exactly."])),
    N.para(N.rich([("if len(s) % len(t) != 0:", {"code": True}), " — If length doesn't divide evenly, t cannot tile s."])),
    N.para(N.rich([("return t * k == s", {"code": True}), " — Repeat t exactly k times and compare; O(len(s)) per check."])),
    N.para(N.rich([("for length in range(len(shorter), 0, -1):", {"code": True}), " — Try from longest possible down to length 1."])),
    N.para(N.rich([("candidate = shorter[:length]", {"code": True}), " — The candidate divisor string."])),
    N.para(N.rich([("if divides(candidate, str1) and divides(candidate, str2):", {"code": True}), " — If it divides both, this is the GCD string (we return immediately — longest first)."])),
    N.para(N.rich([("return \"\"", {"code": True}), " — No common divisor found."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Concat Check + GCD Length (Optimal)", "O((m+n) · log(min(m,n)))", "O(m+n)"],
        ["Brute Force Prefix Check", "O(min(m,n) · (m+n))", "O(min(m,n))"],
    ]),
    N.para(
        "Space O(m+n) for Solution 1 comes from creating the two concatenated strings for comparison. "
        "The GCD computation itself is O(1) space. Solution 2's space is O(min(m,n)) for the candidate string."
    ),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Math"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "GCD of Lengths — apply the Euclidean GCD to string lengths after verifying a common tiling exists via concatenation commutativity."])),
    N.callout(
        "When to recognize this pattern: "
        "• The problem asks for a 'largest common unit' in strings. "
        "• The word 'divides' is used for strings (s = t repeated k times). "
        "• You see two string lengths and think about their GCD. "
        "• Checking str1+str2 == str2+str1 is the universal litmus test for string divisibility.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (GCD / LCM reasoning on strings or sequences):"),
    N.bullet(N.rich([("Repeated String Match", {"bold": True}), " (Medium) — How many times must you repeat str1 to contain str2? Uses ceiling division: ceil(len(str2)/len(str1))."])),
    N.bullet(N.rich([("String Rotation", {"bold": True}), " (Easy) — Is s2 a rotation of s1? Check if s2 is a substring of s1+s1 (same concat trick)."])),
    N.bullet(N.rich([("Repeated Substring Pattern", {"bold": True}), " (Easy) — Does s consist of a repeated substring? Same divisibility structure: check if s = t*k for some t."])),
    N.bullet(N.rich([("Find the Index of the First Occurrence in a String", {"bold": True}), " (Easy) — String matching; uses the same idea of tiling/substring containment."])),
    N.bullet(N.rich([("Count and Say", {"bold": True}), " (Medium) — String construction by pattern; related in that the output has a structural relationship to the input."])),
    N.bullet(N.rich([("Longest Common Prefix", {"bold": True}), " (Easy) — Find the longest prefix shared by all strings; related because the answer is bounded by the GCD of lengths structurally."])),
    N.para("These problems share the core technique: reducing a string structure problem to arithmetic on lengths (GCD, LCM, divisibility), often with a concatenation check as the existence test."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Math / Number Theory section (GCD of Lengths sub-pattern).", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks built: {len(blocks)}")
