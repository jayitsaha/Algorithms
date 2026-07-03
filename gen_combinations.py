"""gen_combinations.py — Notion update for LeetCode #77 Combinations (Backtracking)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81dc-8090-f1e3afc05ed6"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=77,
    pattern="Backtracking",
    subpatterns=["Choose K from N"],
    tc="O(k · C(n,k))",
    sc="O(k)",
    key_insight="Recurse with start=i+1 to enforce increasing order — prevents duplicates without a visited set.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integers ", {}),
        ("n", {"code": True}),
        (" and ", {}),
        ("k", {"code": True}),
        (", return all possible combinations of ", {}),
        ("k", {"code": True}),
        (" numbers chosen from the range ", {}),
        ("[1, n]", {"code": True}),
        (". You may return the answer in any order.", {}),
    ])),
    N.para("Example: n=4, k=2 → [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]] (6 combinations = C(4,2))"),
    N.divider(),
]

# ── Solution 1: Backtracking with Pruning (Interview Pick) ──────────────────
SOL1_CODE = """\
def combine(n: int, k: int) -> list[list[int]]:
    result = []

    def backtrack(start: int, current: list):
        if len(current) == k:
            result.append(current[:])   # COPY — not a reference
            return
        need = k - len(current)         # how many more we need
        limit = n - need + 1            # last valid starting number
        for i in range(start, limit + 1):
            current.append(i)           # CHOOSE
            backtrack(i + 1, current)   # RECURSE: next > i (no reuse, no duplicates)
            current.pop()               # BACKTRACK: undo

    backtrack(1, [])
    return result
"""

blocks += [
    N.h2("Solution 1 — Backtracking with Pruning (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need ALL subsets of size k from {1,…,n}. This is enumeration: there is no single 'best' answer — we want every valid answer. Greedy and DP find one optimum; backtracking finds all answers."),
        N.h4("What Doesn't Work"),
        N.para("Nested loops (k loops for k elements) fail because k is a variable. You can't write a fixed number of nested for-loops when k changes. Brute-force over all 2^n subsets works but generates too many (2^20 = 1M) just to filter by size."),
        N.h4("The Key Observation"),
        N.para("If we always pick the next number strictly greater than the last, every combination is automatically in increasing order — a unique canonical form. Two combinations can only be equal if their sorted forms are equal, and our algorithm produces only sorted forms. So duplicates are structurally impossible."),
        N.h4("Building the Solution"),
        N.para("Start with empty combo, start=1. Try each i from start to limit. Append i, recurse with start=i+1, then pop. The limit = n - need + 1 where need = k - len(current): if the remaining pool [start..n] has fewer than need elements, no valid completion exists — prune early."),
        N.callout("Analogy: Think of it like booking k seats in a row from seat #start onward. You always book the next seat after your last pick. The 'limit' tells you the last row number where you can start — if you start too late, you'll run out of seats before filling all k.", "🎭", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — the output list; will collect all k-size combos."])),
    N.para(N.rich([("def backtrack(start, current):", {"code": True}), " — recursive helper. start = smallest number we may still pick. current = combo built so far (mutable list)."])),
    N.para(N.rich([("if len(current) == k:", {"code": True}), " — base case: combo is complete. We have k numbers."])),
    N.para(N.rich([("result.append(current[:])", {"code": True}), " — append a COPY. current[:] creates a new list. If you append current itself, all stored results will refer to the same (eventually empty) list."])),
    N.para(N.rich([("need = k - len(current)", {"code": True}), " — how many slots we still need to fill."])),
    N.para(N.rich([("limit = n - need + 1", {"code": True}), " — the last valid value for the loop. Starting at limit+1 would leave a pool smaller than need."])),
    N.para(N.rich([("for i in range(start, limit + 1):", {"code": True}), " — try each candidate from start up to limit (inclusive). Without this tight bound we'd waste time on hopeless branches."])),
    N.para(N.rich([("current.append(i)", {"code": True}), " — CHOOSE: add candidate i to the in-progress combination."])),
    N.para(N.rich([("backtrack(i + 1, current)", {"code": True}), " — RECURSE: the next number must be > i (strictly), ensuring no repeats and canonical order."])),
    N.para(N.rich([("current.pop()", {"code": True}), " — BACKTRACK: undo the choice. Restore current to its state before we appended i, so the next loop iteration starts fresh."])),
    N.para(N.rich([("backtrack(1, [])", {"code": True}), " — kick off: pick from 1, empty combo."])),
    N.divider(),
]

# ── Solution 2: No-pruning version (for comparison) ──────────────────────────
SOL2_CODE = """\
def combine_naive(n: int, k: int) -> list[list[int]]:
    result = []
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, n + 1):  # no pruning — loop goes all the way to n
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    backtrack(1, [])
    return result
"""

blocks += [
    N.h2("Solution 2 — Backtracking without Pruning (for comparison)"),
    N.toggle_h3("💡 Intuition: Why Pruning Matters", [
        N.h4("Reframe the Problem"),
        N.para("Same goal. The naive version differs only in the loop bound: it runs range(start, n+1) instead of range(start, limit+1). Both are correct — the naive version just visits some branches that can never complete."),
        N.h4("What Doesn't Work"),
        N.para("For n=4, k=3: the outer loop tries i=4 (start=4, need=3, pool size=1 < 3). This call immediately returns without finding anything — wasted frame. For large n and small k the overhead is small, but for k near n/2 it matters."),
        N.h4("The Key Observation"),
        N.para("Pruning converts the check 'pool_size >= need' from a runtime test into a loop bound. The pruned loop never even enters branches where the pool is too small — zero overhead for those branches."),
        N.h4("Building the Solution"),
        N.para("Identical to Solution 1 except the loop bound. Remove the need/limit lines and change the range to (start, n+1). This is a good starting point in an interview — get it correct first, then add the pruning optimization."),
        N.callout("Derive then optimize: Start with the naive loop bound, confirm correctness, then tighten it. This shows systematic thinking rather than memorizing a formula.", "🔬", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(start, n + 1):", {"code": True}), " — loop runs all the way to n. Correct but visits branches where the remaining pool can't fill k slots (those branches return immediately at the recursive call, wasting a frame)."])),
    N.para("Everything else is identical to Solution 1. The only difference is the loop upper bound."),
    N.callout("Interview tip: Present Solution 2 first as your initial approach, then say 'I can optimize the loop bound to prune hopeless branches' and show Solution 1. This demonstrates both correctness and optimization skills.", "💡", "green_background"),
    N.divider(),
]

# ── Solution 3: itertools (one-liner) ─────────────────────────────────────────
SOL3_CODE = """\
from itertools import combinations

def combine(n: int, k: int) -> list[list[int]]:
    return [list(c) for c in combinations(range(1, n + 1), k)]
"""

blocks += [
    N.h2("Solution 3 — itertools.combinations (Pythonic one-liner)"),
    N.toggle_h3("💡 Intuition: When to Mention This", [
        N.h4("Reframe the Problem"),
        N.para("Python's standard library provides itertools.combinations which does exactly this. It implements the same backtracking logic internally (in C), so it's faster in practice but identical asymptotically."),
        N.h4("What Doesn't Work"),
        N.para("This is not the interview answer — it shows you know Python but not how the algorithm works. However, mentioning it as a cross-check or real-world shortcut after explaining Solution 1 demonstrates language fluency."),
        N.h4("The Key Observation"),
        N.para("itertools.combinations(range(1, n+1), k) generates tuples in lexicographic order. We convert each to a list. Same output, same complexity, more readable for production code."),
        N.h4("Building the Solution"),
        N.para("Import combinations from itertools. Call combinations(range(1, n+1), k) — this produces all k-element subsets in sorted order. Wrap each result in list() since itertools returns tuples."),
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("from itertools import combinations", {"code": True}), " — Python stdlib; no external dependencies."])),
    N.para(N.rich([("combinations(range(1, n+1), k)", {"code": True}), " — generates all k-element tuples from 1..n in increasing order."])),
    N.para(N.rich([("list(c) for c in ...", {"code": True}), " — convert each tuple to a list, since the problem expects list[list[int]]."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (stack + output)"],
        ["Backtracking + Pruning (Sol 1)", "O(k · C(n,k))", "O(k) + O(k · C(n,k))"],
        ["Backtracking Naive (Sol 2)", "O(k · C(n,k)) + pruned frames", "O(k) + O(k · C(n,k))"],
        ["itertools.combinations (Sol 3)", "O(k · C(n,k))", "O(k) + O(k · C(n,k))"],
    ]),
    N.para("C(n,k) = n! / (k! · (n−k)!). For n=20, k=10: C(20,10) = 184,756. Output dominates space: we store k numbers for each of C(n,k) combinations. The call stack is only O(k) deep."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Choose K from N — recursive enumeration of k-element subsets from a fixed universe [1..n], with a start pointer to enforce increasing order and prevent duplicates."])),
    N.callout(
        "When to recognize this pattern: (1) Problem says 'return ALL combinations / subsets of size k'. "
        "(2) No repeated elements within one combination. "
        "(3) Order does not matter in the output. "
        "(4) Output size is exponential (C(n,k)) → must be O(output) time → backtracking is optimal.",
        "🔎", "green_background"
    ),
    N.callout(
        "Choose → Recurse → Backtrack is the universal skeleton: "
        "append candidate, recurse, pop. "
        "This exact pattern appears in Subsets, Permutations, Combination Sum, Letter Combinations.",
        "🧩", "blue_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Choose K from N backtracking pattern:"),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium) — same skeleton but recurse with i (not i+1): numbers may repeat in a combination. (#39)"])),
    N.bullet(N.rich([("Combination Sum II", {"bold": True}), " (Medium) — candidates have duplicates; sort + skip same value at same recursion depth. (#40)"])),
    N.bullet(N.rich([("Combination Sum III", {"bold": True}), " (Medium) — choose exactly k digits 1–9 summing to n; direct extension of this problem. (#216)"])),
    N.bullet(N.rich([("Subsets", {"bold": True}), " (Medium) — all subsets any size; collect at every node not just leaves (no size constraint). (#78)"])),
    N.bullet(N.rich([("Subsets II", {"bold": True}), " (Medium) — subsets with duplicates in input; sort + skip like Combination Sum II. (#90)"])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium) — order matters; no start pointer, use a visited boolean array instead. (#46)"])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium) — same choose-recurse-backtrack skeleton; candidates come from a digit→letters map. (#17)"])),
    N.bullet(N.rich([("Generate Parentheses", {"bold": True}), " (Medium) — backtracking with open/close count constraints rather than a number pool. (#22)"])),
    N.para("These problems all share the three-step Choose → Recurse → Backtrack pattern. The variation is: what are the candidates at each level, and what constraint prunes the search?"),
    N.callout("Pattern insight: The start pointer (for ordered selection) and the visited array (for unordered permutations) are the two main mechanisms for controlling which candidates are available at each recursion depth.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("combinations")),
    N.para(N.rich([
        ("Step through the backtracking algorithm visually — use Next/Prev or arrow keys to see each choose, recurse, and backtrack step.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
