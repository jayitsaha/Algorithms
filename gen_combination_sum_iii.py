"""gen_combination_sum_iii.py — Notion update for Combination Sum III (#216)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8142-a589-f35c3f7d416d"

# ─── 1. Properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=216,
    pattern="Backtracking",
    subpatterns=["K Numbers Summing to N"],
    tc="O(C(9,k)·k)",
    sc="O(k)",
    key_insight="Backtrack with a start parameter — iterate digits in increasing order to avoid duplicates; break when digit exceeds remaining sum.",
    icon="🟡"
)
print("Properties set.")

# ─── 2. Wipe existing body ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─── 3. Build new body ───────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integers ", {}),
        ("k", {"code": True}),
        (" and ", {}),
        ("n", {"code": True}),
        (", find all valid combinations of exactly ", {}),
        ("k", {"code": True}),
        (" distinct numbers from 1–9 that sum to ", {}),
        ("n", {"code": True}),
        (". Each number may be used at most once. Return the answer in any order.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("k=3, n=7 → [[1,2,4]]  (1+2+4=7)", {"code": True}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("k=3, n=9 → [[1,2,6],[1,3,5],[2,3,4]]", {"code": True}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("2 ≤ k ≤ 9,  1 ≤ n ≤ 60", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Backtracking (Interview Pick) ──
BACKTRACK_CODE = """\
def combinationSum3(k: int, n: int) -> list[list[int]]:
    result = []

    def backtrack(start, combo, remaining):
        # Base case: exactly k numbers summing to n
        if len(combo) == k and remaining == 0:
            result.append(combo[:])   # copy — combo is mutated in-place
            return
        # Prune: already k numbers but wrong sum
        if len(combo) == k:
            return
        for d in range(start, 10):
            # Prune: d overshoots remaining; all larger d also overshoot
            if d > remaining:
                break  # break, not continue — ordering guarantees future d are worse
            combo.append(d)                         # CHOOSE
            backtrack(d + 1, combo, remaining - d)  # EXPLORE (d+1 prevents reuse)
            combo.pop()                             # UNCHOOSE

    backtrack(1, [], n)
    return result
"""

blocks += [
    N.h2("Solution 1 — Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to enumerate all subsets of {1,2,...,9} of size exactly k whose elements sum to n. The problem says 'find all' — this is exhaustive enumeration, not optimization."),
        N.h4("What Doesn't Work"),
        N.para("Greedy won't work — there's no clear local choice that always leads to a global solution. DP can count combinations but won't list them. Brute-force over all 2^9 = 512 subsets works but misses the opportunity to prune early."),
        N.h4("The Key Observation"),
        N.para("If we pick digits in increasing order (each digit strictly greater than the last), every generated combination is automatically sorted. This means each unique set is produced exactly once — no deduplication needed. And if current digit d already exceeds remaining, all larger digits also overshoot, so we can break the loop entirely."),
        N.h4("Building the Solution"),
        N.para("Recurse with three parameters: (1) start — smallest digit we can still use, preventing reuse; (2) combo — digits chosen so far; (3) remaining — sum still needed. At each level, iterate d from start to 9. Break if d > remaining. If len(combo) reaches k: record if remaining==0, else prune. This is the classic backtracking template: Choose → Explore → Unchoose."),
        N.callout("Analogy: Think of choosing toppings at a pizza counter. You walk left-to-right (never go back), picking exactly k toppings that total cost n. You stop browsing the moment a topping costs more than your budget — you know all remaining ones are pricier.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BACKTRACK_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — Accumulator for all valid combinations found during the search."])),
    N.para(N.rich([("def backtrack(start, combo, remaining)", {"code": True}), " — Recursive helper. start: next digit to consider (≥ last chosen, enforcing strictly increasing order). combo: current partial combination (mutable, shared). remaining: sum still needed."])),
    N.para(N.rich([("if len(combo) == k and remaining == 0", {"code": True}), " — Base case: we have exactly k numbers and they sum to n. Valid answer found."])),
    N.para(N.rich([("result.append(combo[:])", {"code": True}), " — Append a COPY. combo is mutated throughout — without [:], all stored 'results' would point to the same eventually-empty list."])),
    N.para(N.rich([("if len(combo) == k: return", {"code": True}), " — Prune: we already have k numbers but remaining ≠ 0 (wrong sum). No point iterating — return immediately."])),
    N.para(N.rich([("for d in range(start, 10)", {"code": True}), " — Iterate candidates from start to 9. Starting from start (not 1) ensures each digit is used at most once and combos are always increasing."])),
    N.para(N.rich([("if d > remaining: break", {"code": True}), " — Overshoot prune. d exceeds the remaining budget. Since d increases each iteration, all future digits also overshoot. BREAK (not continue)."])),
    N.para(N.rich([("combo.append(d)", {"code": True}), " — CHOOSE: add digit d to the current combination."])),
    N.para(N.rich([("backtrack(d + 1, combo, remaining - d)", {"code": True}), " — EXPLORE: recurse with d+1 as the new start (prevents reusing d) and updated remaining."])),
    N.para(N.rich([("combo.pop()", {"code": True}), " — UNCHOOSE: remove d, restoring combo to its state before the choice. Try the next candidate."])),
    N.para(N.rich([("backtrack(1, [], n)", {"code": True}), " — Kick off the search from digit 1 with empty combination and target n."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
BRUTE_CODE = """\
from itertools import combinations

def combinationSum3(k: int, n: int) -> list[list[int]]:
    return [list(c) for c in combinations(range(1, 10), k)
            if sum(c) == n]
"""

blocks += [
    N.h2("Solution 2 — Brute Force via itertools"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simply generate all C(9,k) subsets of size k from {1..9} and filter for those summing to n."),
        N.h4("What Doesn't Work"),
        N.para("This approach visits every subset of size k — it cannot prune branches early the way backtracking does. For k near the middle (k=4 or 5), this is C(9,5)=126 evaluations, which is still tiny, making this acceptable in practice for this specific problem."),
        N.h4("The Key Observation"),
        N.para("Python's itertools.combinations already generates subsets in lexicographic order without repetition. The one-liner is readable and correct. In an interview, propose this first, then offer to optimize with explicit backtracking."),
        N.h4("Building the Solution"),
        N.para("combinations(range(1, 10), k) yields all C(9,k) sorted k-tuples from digits 1–9. Filter by sum == n. Convert to lists."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("combinations(range(1, 10), k)", {"code": True}), " — Generates all C(9,k) subsets of size k from {1..9} in sorted order."])),
    N.para(N.rich([("if sum(c) == n", {"code": True}), " — Filter: only keep subsets whose elements sum to n."])),
    N.para(N.rich([("list(c)", {"code": True}), " — Convert each tuple to a list, as the return type expects list[list[int]]."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (itertools)", "O(C(9,k)·k)", "O(result)", "All subsets then filter; no early exit"],
        ["Backtracking (Interview Pick)", "O(C(9,k)·k)", "O(k)", "Pruning + minimal stack; only O(k) for recursion depth"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "K Numbers Summing to N — exhaustive search over bounded digit set, choosing exactly k elements with sum constraint, using start parameter for deduplication."])),
    N.callout(
        "When to recognize this pattern: Problem says 'find ALL combinations/permutations/subsets satisfying constraint X'. Elements chosen from a bounded set (here digits 1–9), each used at most once. Order within a combination doesn't matter. The start parameter (each recursive call receives the next eligible index) is the key technique that avoids duplicates without a seen-set.",
        "🔎", "green_background"
    ),
    N.callout(
        "Backtracking Template — Choose / Explore / Unchoose:\n  combo.append(d)                   # CHOOSE\n  backtrack(d+1, combo, remaining-d)  # EXPLORE\n  combo.pop()                         # UNCHOOSE\nThis three-step rhythm applies to all backtracking problems.",
        "📐", "gray_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Backtracking / K-Numbers technique:"),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium, #39) — Unlimited reuse of candidates; change backtrack(d+1,...) to backtrack(d,...)."])),
    N.bullet(N.rich([("Combination Sum II", {"bold": True}), " (Medium, #40) — Candidates with duplicates, each used once; need skip-duplicate logic at same recursion depth."])),
    N.bullet(N.rich([("Combinations", {"bold": True}), " (Medium, #77) — All C(n,k) combinations from 1..n, no sum constraint; identical start-parameter template."])),
    N.bullet(N.rich([("Subsets", {"bold": True}), " (Medium, #78) — All subsets of an array; same backtracking template without k/n constraints."])),
    N.bullet(N.rich([("Letter Combinations of Phone Number", {"bold": True}), " (Medium, #17) — Backtracking over character choices per digit position."])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium, #46) — All orderings; backtracking with visited boolean array instead of start parameter."])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), " (Medium, #131) — Backtracking to partition string into palindromic substrings; pruning via palindrome check."])),
    N.para("These problems share the core Choose → Explore → Unchoose template. The key variation is whether elements can be reused (Combination Sum I), candidates have duplicates (Combination Sum II), or order matters (Permutations)."),
    N.callout("📚 Sub-Pattern: K Numbers Summing to N · Source: Analysis (Backtracking section of DSA guide)", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("combination_sum_iii")),
    N.para(N.rich([("Step through the backtracking tree visually — use Next/Prev or arrow keys to see each choose/explore/unchoose/prune step.", {"italic": True, "color": "gray"})])),
]

# ─── 4. Append all blocks ─────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
