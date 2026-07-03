"""
gen_numbers_at_most_n_given_digit_set.py
Notion page rebuild for:
  902. Numbers At Most N Given Digit Set (Hard)
  Pattern: Dynamic Programming / Digit DP
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-814f-85f2-d47245aeb112"

# ── 1) properties ────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=902,
    pattern="Dynamic Programming",
    subpatterns=["Digit DP"],
    tc="O(log N · |D|)",
    sc="O(log N)",
    key_insight="Count valid numbers by position: for each digit position decide how many free-choice prefixes exist, then check if N itself is reachable.",
    icon="🔴",
)
print("Properties set.")

# ── 2) wipe old body ─────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) rebuild body ──────────────────────────────────────────────────
blocks = []

# ════════════════════════════════════════════════════════
# PROBLEM
# ════════════════════════════════════════════════════════
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted array of digits ", {}),
        ("D", {"code": True}),
        (" (each digit is '1'–'9', no duplicates) and a positive integer ", {}),
        ("N", {"code": True}),
        (", return how many numbers ", {}),
        ("x", {"code": True}),
        (" in the range ", {}),
        ("[1, N]", {"code": True}),
        (" can be formed using the digits in ", {}),
        ("D", {"code": True}),
        (". Every digit of ", {}),
        ("x", {"code": True}),
        (" must be an element of ", {}),
        ("D", {"code": True}),
        (". Note: '0' is never in ", {}),
        ("D", {"code": True}),
        (", and the number of digits in ", {}),
        ("N", {"code": True}),
        (" can be up to 9.", {}),
    ])),
    N.para("Example: D = ['1','3','5','7'], N = 100  →  Answer = 20"),
    N.para("  • 1-digit: 1,3,5,7 → 4 numbers"),
    N.para("  • 2-digit: 11,13,15,17,31,33,35,37,51,53,55,57,71,73,75,77 → 16 numbers"),
    N.para("  • 3-digit ≤ 100: none (smallest 3-digit from D is 111 > 100)"),
    N.para("  Total = 4 + 16 = 20."),
    N.divider(),
]

# ════════════════════════════════════════════════════════
# SOLUTION 1 — Digit DP (Interview Pick)
# ════════════════════════════════════════════════════════
sol1_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para(
        "How many integers ≤ N can be formed using only digits from D?\n"
        "Split by length: numbers shorter than N always qualify (any digit from D at each position).\n"
        "Numbers of exactly the same length as N need careful digit-by-digit comparison."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Brute force: iterate x from 1 to N, check each digit — O(N log N) which explodes for N ~ 10^9.\n"
        "Even memoised recursion is fine, but the closed-form digit DP is direct and O(log N · |D|)."
    ),
    N.h4("The Key Observation"),
    N.para(
        "Count = (numbers with fewer digits than N that use D) + (numbers with exactly len(N) digits, ≤ N, using D).\n"
        "\n"
        "Shorter-length part: for each length k < len(N), every position can be any of |D| digits → |D|^k numbers.\n"
        "\n"
        "Same-length part: walk digit by digit through the decimal representation of N. At each position i:\n"
        "  • All digits in D that are strictly LESS THAN N[i] → we can freely fill the remaining positions → |D|^(remaining) new numbers.\n"
        "  • If N[i] itself is in D → continue to the next position (we're still 'tight' against N).\n"
        "  • If N[i] is NOT in D → no further numbers possible; break.\n"
        "At the end, if we matched every digit of N exactly, add 1 (N itself is valid)."
    ),
    N.h4("Building the Solution"),
    N.para(
        "Step 1: Convert N to its decimal string S.\n"
        "Step 2: Add |D|^1 + |D|^2 + ... + |D|^(len(S)-1) for all shorter lengths.\n"
        "Step 3: Walk through S position by position:\n"
        "          For each digit d in D strictly < S[i]: add |D|^(len(S)-i-1).\n"
        "          If S[i] in D: continue (still tight). Else: break.\n"
        "Step 4: If we reached the end without breaking, N itself is valid — add 1."
    ),
    N.callout(
        "Analogy: Imagine counting licence plates. Shorter plates are always valid. "
        "For plates the same length as the limit, go left-to-right: "
        "if the current digit slot can be anything smaller → count freely; "
        "if it matches the limit exactly → keep walking; if it can't be matched → stop.",
        "🧠", "blue_background"
    ),
]

sol1_code = """\
from typing import List

def atMostNGivenDigitSet(digits: List[str], n: int) -> int:
    S = str(n)            # decimal representation of upper bound
    k = len(S)            # number of digits in N
    D = sorted(digits)    # sorted digit strings
    d = len(D)            # size of digit set

    count = 0

    # ── shorter-length numbers ──
    # For length L (1 to k-1), any digit at any position: d^L numbers.
    power = 1
    for _ in range(k - 1):
        power *= d
        count += power

    # ── same-length numbers (tight against N) ──
    for i, ch in enumerate(S):
        # digits strictly less than S[i]: each gives d^(remaining) free numbers
        remaining = k - i - 1
        free = d ** remaining
        for dig in D:
            if dig < ch:
                count += free
            elif dig == ch:
                break          # stay tight; continue to next position
        else:
            # ch not in D at all — no way to be tight here; stop
            break
    else:
        # Every digit of N was in D — N itself is valid
        count += 1

    return count
"""

sol1_lineby = [
    N.para(N.rich([("S = str(n)", {"code": True}), (" — Convert N to its digit string for position-by-position inspection.", {})])),
    N.para(N.rich([("k = len(S)", {"code": True}), (" — Number of digits in N (upper bound on digit length).", {})])),
    N.para(N.rich([("D = sorted(digits)", {"code": True}), (" — Sort D so we can do ordered comparisons with < in the tight walk.", {})])),
    N.para(N.rich([("power = 1; for _ in range(k-1): power *= d; count += power", {"code": True}), (" — Accumulates |D|^1 + |D|^2 + ... + |D|^(k-1): every number shorter than N is valid.", {})])),
    N.para(N.rich([("for i, ch in enumerate(S):", {"code": True}), (" — Tight walk through N's digits.", {})])),
    N.para(N.rich([("remaining = k - i - 1", {"code": True}), (" — Positions to the right of i; each can be any of d digits.", {})])),
    N.para(N.rich([("free = d ** remaining", {"code": True}), (" — Multiplier: after fixing this prefix, |D|^remaining choices remain.", {})])),
    N.para(N.rich([("if dig < ch: count += free", {"code": True}), (" — Choosing a smaller digit here frees all remaining positions.", {})])),
    N.para(N.rich([("elif dig == ch: break", {"code": True}), (" — Choosing the matching digit keeps us tight; move right (loop continues).", {})])),
    N.para(N.rich([("else: break (for-else on D)", {"code": True}), (" — ch is not in D at all; we cannot stay tight — stop the outer loop.", {})])),
    N.para(N.rich([("else: count += 1 (for-else on S)", {"code": True}), (" — We consumed every digit of N without breaking — N itself is a valid number.", {})])),
]

blocks += [
    N.h2("Solution 1 — Digit DP Tight-Walk (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol1_intuition_children),
    N.h3("🔬 Algorithm Deep-Dive — Digit DP"),
    N.para(
        "Digit DP is a counting technique for problems of the form "
        "\"how many integers in [1, N] satisfy property P?\"\n\n"
        "Origin: classical combinatorics; popularised in competitive programming as 'digit DP'.\n\n"
        "Core invariant: maintain a 'tight' flag — whether the prefix built so far equals "
        "the corresponding prefix of N. Once a digit smaller than N's is chosen, the suffix "
        "is completely free (any combination). Once a digit larger is chosen, the number exceeds N "
        "(invalid). Only when the chosen digit equals N's digit do we stay tight.\n\n"
        "Why it works: the tight constraint partitions the search space into "
        "independent subproblems — free-suffix counts are just powers of |D|, "
        "computable in O(1) per position.\n\n"
        "When to recognise: 'count integers ≤ N with property on individual digits' "
        "— if the property factors cleanly per digit position, digit DP applies."
    ),
    N.code(
        "# Digit DP template\n"
        "# S = str(N); iterate positions; track 'tight'\n"
        "for i, ch in enumerate(S):\n"
        "    for d in digits:\n"
        "        if d < ch:  count += free_count\n"
        "        elif d == ch: break  # stay tight\n"
        "    else: break  # ch not in digits\n"
        "else: count += 1  # N itself valid",
        "python"
    ),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
] + sol1_lineby + [N.divider()]

# ════════════════════════════════════════════════════════
# SOLUTION 2 — Top-Down Memoization
# ════════════════════════════════════════════════════════
sol2_intuition_children = [
    N.h4("Reframe the Problem"),
    N.para(
        "Express the count as a recursive function: "
        "f(pos, tight) = count of valid suffixes starting at position pos, "
        "where tight indicates whether the prefix so far equals N's prefix."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Pure recursion without memoization revisits the same (pos, tight) states repeatedly. "
        "With memoization we store results so each (pos, tight) pair is computed once."
    ),
    N.h4("The Key Observation"),
    N.para(
        "State: (position, is_tight). Since is_tight is boolean and position ≤ 9, "
        "there are at most 18 unique states — memoization overhead is negligible. "
        "Base case: pos == len(S) → return 1 (we built a complete valid number)."
    ),
    N.h4("Building the Solution"),
    N.para(
        "At each (pos, tight):\n"
        "  • Determine the digit upper limit: S[pos] if tight else '9'.\n"
        "  • For each digit d in D that is ≤ upper_limit:\n"
        "      new_tight = tight and (d == upper_limit)\n"
        "      count += f(pos + 1, new_tight)\n"
        "  • Also count numbers shorter than S: handled by calling f(0, False) for each length < k.\n"
        "The memoized version is more general and can be extended to different constraints."
    ),
    N.callout(
        "This approach generalises easily to 'count integers with digit sum divisible by k' "
        "by adding a third dimension to the state: (pos, tight, digit_sum_mod_k).",
        "💡", "green_background"
    ),
]

sol2_code = """\
from typing import List
from functools import lru_cache

def atMostNGivenDigitSet_memo(digits: List[str], n: int) -> int:
    S = str(n)
    k = len(S)
    D = sorted(digits)

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, started: bool) -> int:
        \"\"\"Count valid completions from position pos.
        tight: True if prefix so far == S[:pos]
        started: True if we've placed at least one non-zero digit (handles leading zeros, though D has none)
        \"\"\"
        if pos == k:
            return 1 if started else 0  # complete number only if we started

        result = 0
        # option 1: if not yet started, skip this position (shorter number)
        if not started:
            result += dp(pos + 1, False, False)

        limit = S[pos] if tight else '9'
        for d in D:
            if d > limit:
                break
            new_tight = tight and (d == limit)
            result += dp(pos + 1, new_tight, True)

        return result

    return dp(0, True, False)
"""

sol2_lineby = [
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoize results keyed by (pos, tight, started).", {})])),
    N.para(N.rich([("if pos == k: return 1 if started else 0", {"code": True}), (" — Base case: consumed all positions; valid only if we placed a digit.", {})])),
    N.para(N.rich([("if not started: result += dp(pos+1, False, False)", {"code": True}), (" — Skip position to count shorter numbers (handled implicitly).", {})])),
    N.para(N.rich([("limit = S[pos] if tight else '9'", {"code": True}), (" — Upper bound for this digit slot.", {})])),
    N.para(N.rich([("for d in D: if d > limit: break", {"code": True}), (" — D is sorted; once d exceeds limit, all subsequent are also > limit.", {})])),
    N.para(N.rich([("new_tight = tight and (d == limit)", {"code": True}), (" — Tight only if we're already tight AND chose the exact limiting digit.", {})])),
    N.para(N.rich([("result += dp(pos+1, new_tight, True)", {"code": True}), (" — Recurse with updated tight flag; started=True (placed a digit).", {})])),
]

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", sol2_intuition_children),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
] + sol2_lineby + [N.divider()]

# ════════════════════════════════════════════════════════
# SOLUTION 3 — Brute Force (reference only)
# ════════════════════════════════════════════════════════
sol3_code = """\
# Brute Force — O(N · log N) — TLE for large N, illustrative only
def atMostNGivenDigitSet_brute(digits, n):
    digit_set = set(digits)
    count = 0
    for x in range(1, n + 1):
        if all(c in digit_set for c in str(x)):
            count += 1
    return count
"""

blocks += [
    N.h2("Solution 3 — Brute Force (TLE for large N)"),
    N.toggle_h3("💡 Intuition: Why This Fails", [
        N.h4("Approach"),
        N.para("Iterate x from 1 to N and check each digit against D. Correct but O(N log N) — unusable for N up to 10^9."),
        N.h4("When Useful"),
        N.para("Useful to verify small test cases during development and as a sanity-check oracle."),
    ]),
    N.h3("Code"),
    N.code(sol3_code, "python"),
    N.divider(),
]

# ════════════════════════════════════════════════════════
# WHY IS THIS DP?
# ════════════════════════════════════════════════════════
blocks += [
    N.h2("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("count(pos, tight) depends only on count(pos+1, new_tight) — "
         "each subproblem is independent of how we reached (pos, tight).", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("The same (pos, tight) pair is reached via multiple prefix choices. "
         "Without memoization, we'd recompute it exponentially.", {}),
    ])),
    N.code(
        "# Recurrence\n"
        "dp(pos, tight) = sum over d in D, d <= limit:\n"
        "                    dp(pos+1, tight and d==S[pos])\n"
        "              + (if not tight) |D|^(remaining)   [closed-form for free suffix]\n"
        "\n"
        "Base: dp(k, _) = 1  (completed a valid number)\n"
        "\n"
        "Shorter numbers (length L < k): contribute |D|^L each.",
        "python"
    ),
    N.callout(
        "The tabulation (Solution 1) exploits the structure so cleverly that it computes "
        "the closed-form power directly, eliminating the need for an explicit DP table "
        "while still following the same recurrence logic.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════
# COMPLEXITY
# ════════════════════════════════════════════════════════
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Digit DP Tight-Walk (S1)", "O(log N · |D|)", "O(log N)"],
        ["Top-Down Memoization (S2)", "O(log N · |D|)", "O(log N)"],
        ["Brute Force (S3)", "O(N · log N)", "O(log N)"],
    ]),
    N.para(
        "log N = number of digits in N (≤ 9 for N ≤ 10^9). "
        "|D| ≤ 9. So all digit-DP solutions are effectively O(1) for this problem's constraints."
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════
# PATTERN CLASSIFICATION
# ════════════════════════════════════════════════════════
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Digit DP — count valid integers in [1, N] using per-digit constraints", {})])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Count integers ≤ N satisfying a per-digit condition'\n"
        "• Digit set or digit sum constraints\n"
        "• N is very large (up to 10^9 or 10^18) — brute force impossible\n"
        "• Problem says 'formed from a given set of digits'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ════════════════════════════════════════════════════════
# RELATED PROBLEMS
# ════════════════════════════════════════════════════════
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Digit DP technique:"),
    N.bullet(N.rich([("Count Numbers with Unique Digits", {"bold": True}), (" (Medium) — DP on digit positions, no repeated digit allowed", {})])),
    N.bullet(N.rich([("Number of Digit One", {"bold": True}), (" (Hard) — Count occurrences of digit '1' in all integers ≤ N", {})])),
    N.bullet(N.rich([("Numbers At Most N Given Digit Set", {"bold": True}), (" (Hard) — This problem; canonical digit DP", {})])),
    N.bullet(N.rich([("Non-decreasing Digits", {"bold": True}), (" (Easy) — Construct largest number ≤ N with non-decreasing digits", {})])),
    N.bullet(N.rich([("Digit Count in Range", {"bold": True}), (" (Hard) — Count digits d in [lo, hi]", {})])),
    N.bullet(N.rich([("New 21 Game", {"bold": True}), (" (Medium) — Probability DP with bounded digit-like states", {})])),
    N.bullet(N.rich([("Numbers At Most N Given Digit Set II (variant)", {"bold": True}), (" — Extend to include '0' or allow repeated use", {})])),
    N.para("These problems share the same core technique: walk digit-by-digit through the bound N, maintain a 'tight' flag, and count free-suffix combinations as powers of the digit-set size."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — DP: Digit section", "📚", "gray_background"),
]

# ════════════════════════════════════════════════════════
# EMBED
# ════════════════════════════════════════════════════════
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("numbers_at_most_n_given_digit_set")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) push to Notion ──────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} ({len(blocks)} top-level blocks)")
