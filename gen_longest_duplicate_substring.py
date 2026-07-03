"""
gen_longest_duplicate_substring.py
DSA Pipeline — Notion page builder for LeetCode #1044 Longest Duplicate Substring
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

# ── Step 0: Create page (notion_page_id is null) ──
PAGE_ID = N.create_page("Longest Duplicate Substring", 1044, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1044,
    pattern="String Processing",
    subpatterns=["Binary Search + Rabin-Karp"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Binary search on duplicate length; Rabin-Karp rolling hash makes each feasibility check O(n).",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: Wipe (fresh page, nothing to wipe, but call for safety) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body ──

PROBLEM_STATEMENT = (
    "Given a string s, return the longest substring that appears at least twice. "
    "If no such substring exists, return an empty string \"\". "
    "The two occurrences may overlap."
)

SOL1_CODE = '''\
def longestDupSubstring(s: str) -> str:
    n = len(s)
    MOD = (1 << 61) - 1   # Mersenne prime: 2^61 - 1
    BASE = 131             # Base > 128 (full ASCII range)
    nums = [ord(c) for c in s]  # Convert chars once

    def check(L):
        # Build initial hash for window s[0:L] using Horner's method
        h, power = 0, 1
        for i in range(L):
            h = (h * BASE + nums[i]) % MOD
            power = power * BASE % MOD   # power = BASE^L after loop
        seen = {h: 0}                    # hash -> start index

        for i in range(1, n - L + 1):
            # Roll: remove s[i-1], add s[i+L-1]
            h = (h * BASE - nums[i-1] * power + nums[i+L-1]) % MOD
            if h in seen:
                j = seen[h]
                if s[j:j+L] == s[i:i+L]:    # confirm not a false collision
                    return s[i:i+L]
            seen[h] = i
        return ""

    lo, hi = 1, n - 1
    ans = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        result = check(mid)
        if result:          # length mid is feasible -> try longer
            ans = result
            lo = mid + 1
        else:               # length mid infeasible -> try shorter
            hi = mid - 1
    return ans
'''

SOL2_CODE = '''\
def longestDupSubstring_brute(s: str) -> str:
    n = len(s)
    ans = ""
    # Try all lengths from longest to shortest
    for length in range(n, 0, -1):
        seen = set()
        for i in range(n - length + 1):
            sub = s[i:i+length]    # O(L) slice — the bottleneck
            if sub in seen:
                return sub         # First match = longest duplicate
            seen.add(sub)
    return ""
'''

ROLLING_HASH_TEMPLATE = '''\
# Rabin-Karp Rolling Hash Core Pattern
MOD = (1 << 61) - 1  # Mersenne prime for near-zero collision probability
BASE = 131           # Base > alphabet size

h, power = 0, 1
for i in range(L):                              # Build first window hash
    h = (h * BASE + ord(s[i])) % MOD
    power = power * BASE % MOD                 # power = BASE^L

seen = {h: 0}                                  # hash -> start index
for i in range(1, n - L + 1):                 # Slide the window
    h = (h * BASE - ord(s[i-1]) * power + ord(s[i+L-1])) % MOD
    if h in seen:                              # Potential duplicate
        if s[seen[h]:seen[h]+L] == s[i:i+L]: # Confirm (not collision)
            return s[i:i+L]
    seen[h] = i
'''

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('s = "banana" → "ana" (appears at index 1 and 3, both inclusive). '
         's = "abcd" → "" (all characters distinct, no duplicate substring).')
    ])),
    N.divider()
]

# ── Solution 1: Binary Search + Rabin-Karp (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Binary Search + Rabin-Karp Rolling Hash (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the LONGEST substring repeated at least twice. Instead of checking every "
            "possible substring (O(n²) candidates, each taking O(n) to compare = O(n³) total), "
            "think about the LENGTH of the answer. Binary search lets us ask: for length L, "
            "does ANY window of that length appear twice? This is monotone: if length L works, "
            "length L-1 also works (substring of the duplicate is itself duplicated)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: enumerate all O(n²) substrings, hash them in a set. "
            "Each insertion/lookup takes O(L) for string hashing → O(n³) total. "
            "For n=30,000 that is 27 billion operations — Time Limit Exceeded. "
            "Even O(n²) approaches fail here."
        ),
        N.h4("The Key Observation"),
        N.para(
            "MONOTONE FEASIBILITY: If a duplicate substring of length k exists, then a duplicate "
            "of length k-1 also exists (just take any (k-1)-length prefix of that duplicate). "
            "This binary structure — feasible for all L ≤ answer, infeasible for L > answer — "
            "is the exact condition that makes binary search on the answer applicable."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Binary search on L ∈ [1, n-1]: O(log n) rounds. Each round, run a feasibility "
            "check: slide a window of length L, compute each window's Rabin-Karp rolling hash "
            "in O(1) per step. Store hashes in a set. First collision = duplicate found. "
            "Total: O(log n) × O(n) = O(n log n)."
        ),
        N.callout(
            "Analogy: Finding the tallest person who can fit through a door. Instead of trying "
            "every person one by one, you binary search — try the middle height. If someone of "
            "height mid fits, try taller; if not, try shorter. Rolling hash is like measuring "
            "each person's height in O(1) once you've measured one (just measure the difference).",
            "🧠", "blue_background"
        )
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Rabin-Karp Rolling Hash"),
    N.para(N.rich([
        ("Rabin-Karp Rolling Hash", {"bold": True}),
        (" — Origin: Michael O. Rabin and Richard M. Karp, 1987. Designed for pattern matching "
         "in text in O(n+m) time. The rolling hash mechanism is the key: instead of recomputing "
         "each window's hash from scratch in O(L), we maintain a running polynomial hash and "
         "update it in O(1) as the window slides.")
    ])),
    N.para(
        "Core invariant: For any window [i, i+L), the hash H(i) = Σ s[i+k] × BASE^(L-1-k) mod MOD "
        "for k in [0, L). Rolling update: H(i+1) = (H(i) × BASE − s[i] × BASE^L + s[i+L]) mod MOD. "
        "This preserves the invariant in O(1) — the subtract removes the old leading character's "
        "contribution, the add includes the new trailing character."
    ),
    N.para(
        "Why it works: Polynomial hashing is a ring homomorphism. The hash of a concatenation "
        "is algebraically related to the hashes of its parts. Sliding the window equals "
        "one multiply + one subtract + one add — no traversal of the window needed."
    ),
    N.para(
        "When to recognize it: Fixed-length window comparison, repeated substring detection, "
        "pattern matching in text, any problem where O(1) window-to-window transition is needed."
    ),
    N.code(ROLLING_HASH_TEMPLATE),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(s)", {"code": True}), " — Store string length for reuse."])),
    N.para(N.rich([("MOD = (1 << 61) - 1", {"code": True}), " — 2^61−1 is a Mersenne prime. Large enough that hash collisions occur with probability ~1/MOD ≈ 4×10⁻¹⁹ per comparison."])),
    N.para(N.rich([("BASE = 131", {"code": True}), " — Polynomial base. Must be larger than the alphabet size (128 for ASCII) to give each character a unique contribution."])),
    N.para(N.rich([("nums = [ord(c) for c in s]", {"code": True}), " — Pre-convert characters to integers once. Avoids repeated ord() calls inside the inner loop."])),
    N.para(N.rich([("h, power = 0, 1", {"code": True}), " — Initialize hash and BASE^L. After the initial loop, power = BASE^L (used in the roll step to remove the leading character)."])),
    N.para(N.rich([("h = (h * BASE + nums[i]) % MOD", {"code": True}), " — Horner's method: evaluate polynomial left-to-right. Equivalent to h = s[0]×BASE^(L-1) + ... + s[L-1] but in O(L) total (not O(L²))."])),
    N.para(N.rich([("seen = {h: 0}", {"code": True}), " — Map from hash value to start index of first window with that hash. Used for O(1) collision detection AND O(1) lookup of the earlier occurrence."])),
    N.para(N.rich([("h = (h * BASE - nums[i-1] * power + nums[i+L-1]) % MOD", {"code": True}), " — Rolling update: multiply shifts all existing characters left (×BASE), subtract removes the character that left the window (×power = ×BASE^L), add includes the new character at the right edge."])),
    N.para(N.rich([("if h in seen:", {"code": True}), " — O(1) hash set lookup. A hit means an earlier window had the same hash — potential duplicate."])),
    N.para(N.rich([("if s[j:j+L] == s[i:i+L]:", {"code": True}), " — Confirm the match is real (not a hash collision). In Python, this string comparison is O(L) in the worst case — but real collisions are astronomically rare with MOD=2^61-1."])),
    N.para(N.rich([("lo = mid + 1", {"code": True}), " — Feasible: found a duplicate of length mid. Try to find a longer one by moving lo up."])),
    N.para(N.rich([("hi = mid - 1", {"code": True}), " — Infeasible: no duplicate of length mid. Move hi down — longer lengths impossible, shorter might work."])),
    N.callout(
        "⚠️ Common pitfall: Forgetting that the rolling hash can go negative in C++/Java. "
        "h * BASE - nums[i-1] * power can underflow. Always add MOD before the final % MOD "
        "in languages without Python's arbitrary-precision integers: "
        "h = ((h * BASE - nums[i-1] * power + nums[i+L-1]) % MOD + MOD) % MOD",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Nested Loops + Hash Set"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The most direct interpretation: try every possible substring length from longest "
            "to shortest. For each length, collect all substrings in a set. If any appears twice, "
            "return it. The first match from the longest-first scan gives the answer."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "This is the baseline that DOESN'T scale. It's O(n³): outer loop over length (n), "
            "inner loop over start positions (n), string slice and hash (L). For n=30,000 "
            "this is 27×10⁹ operations — far too slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The bottleneck is the O(L) cost of string hashing inside the inner loop. "
            "Rolling hash removes this by maintaining the hash incrementally."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Enumerate lengths n−1 down to 1. For each, collect all substrings in a set. "
            "First collision is the answer. This gives a correct but slow O(n³) baseline."
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for length in range(n, 0, -1):", {"code": True}), " — Try from longest down to 1. First match is the answer (no need to continue after finding it)."])),
    N.para(N.rich([("sub = s[i:i+length]", {"code": True}), " — Extract substring. This is O(length) in both time and memory — the O(n³) bottleneck."])),
    N.para(N.rich([("if sub in seen: return sub", {"code": True}), " — First duplicate found at this length. Since we scan from longest to shortest, this is the longest duplicate overall."])),
    N.divider()
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n³)", "O(n²)"],
        ["Binary Search + Rolling Hash (Interview Pick)", "O(n log n)", "O(n)"],
        ["Suffix Array + LCP Array", "O(n log n)", "O(n)"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "String Processing"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Binary Search + Rabin-Karp (composite technique — binary search on the answer combined with rolling hash feasibility check)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Find the maximum/minimum LENGTH satisfying a condition' → binary search on answer. "
        "(2) 'Does any fixed-length window appear twice?' → rolling hash check. "
        "(3) Combined: n up to 10^4–10^5, O(n²) is TLE, need O(n log n). "
        "Signal words: 'duplicate', 'repeated', 'longest substring'.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Repeated DNA Sequences", {"bold": True}), " (Medium) — Fixed L=10 rolling hash; find all length-10 substrings appearing 3+ times. Classic Rabin-Karp application (#187)"])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium) — Binary search on eating speed; O(n) greedy feasibility check. Canonical 'binary search on answer' template (#875)"])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), " (Medium) — Binary search on capacity; O(n) greedy feasibility check (#1011)"])),
    N.bullet(N.rich([("Find the Duplicate Number", {"bold": True}), " (Medium) — Binary search on value + count feasibility; or fast/slow pointer (#287)"])),
    N.bullet(N.rich([("Minimum Number of Days to Make m Bouquets", {"bold": True}), " (Medium) — Binary search on number of days; O(n) greedy scan (#1482)"])),
    N.bullet(N.rich([("Longest Happy Prefix", {"bold": True}), " (Hard) — Rolling hash to find longest prefix that is also a suffix; Rabin-Karp on both ends of string (#1392)"])),
    N.bullet(N.rich([("Distinct Substrings (SPOJ)", {"bold": True}), " (Hard) — Count number of distinct substrings; suffix array + LCP or rolling hash approach. Same problem family."])),
    N.para("These problems share the same core technique: binary search on a monotone feasibility function, where the feasibility check runs in O(n) via rolling hash or greedy scan."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search) + Section 2 (String Processing). Sub-pattern: Binary Search + Rabin-Karp (composite — Analysis).", "📚", "gray_background")
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_duplicate_substring")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ──
import json, pathlib
status_dir = pathlib.Path('/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status')
status_dir.mkdir(exist_ok=True)
html_lines = sum(1 for _ in open('/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/longest_duplicate_substring_explainer.html'))
status = {
    "slug": "longest_duplicate_substring",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Binary Search + Rabin-Karp; created fresh Notion page; 1028-line HTML."
}
status_path = status_dir / 'longest_duplicate_substring.json'
status_path.write_text(json.dumps(status, indent=2))
print(f"Status written to {status_path}")
print(f"RESULT longest_duplicate_substring | html=OK | notion=OK | lines={html_lines}")
