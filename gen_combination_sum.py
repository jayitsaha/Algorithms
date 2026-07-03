"""
gen_combination_sum.py — Notion page creator/updater for Combination Sum (#39).
Run from the Algorithms directory: python3 gen_combination_sum.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Page creation (notion_page_id is null → create fresh) ──
PAGE_ID = N.create_page("Combination Sum", 39, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# ── Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=39,
    pattern="Backtracking",
    subpatterns=["Unlimited Use + Start Index"],
    tc="O(N^(T/M))",
    sc="O(T/M)",
    key_insight="Sort candidates, recurse with start=i (same index) for reuse; break when candidate > remaining.",
    icon="🟡",
)
print("Properties set.")

# ── Build body blocks ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of distinct integers "),
        ("candidates", {"code": True}),
        (" and an integer "),
        ("target", {"code": True}),
        (", return a list of all unique combinations of candidates where the chosen numbers sum to "),
        ("target", {"code": True}),
        (". The same number may be chosen from "),
        ("candidates", {"code": True}),
        (" an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.")
    ])),
    N.para(N.rich([
        ("Example: candidates = [2,3,6,7], target = 7 → Output: [[2,2,3],[7]]", {"code": True})
    ])),
    N.divider(),
]

# ── Solution 1: Backtracking with Sort + Prune (Interview Pick) ──
solution1_code = """\
def combinationSum(candidates, target):
    candidates.sort()          # Sort enables early break when candidate > remaining
    results = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])  # Copy! The reference gets mutated by backtracking
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break          # Pruning: sorted → all further candidates also too large
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # start=i allows reuse
            path.pop()         # Unchoose: restore path for next iteration
    backtrack(0, [], target)
    return results
"""

blocks += [
    N.h2("Solution 1 — Backtracking with Sort + Prune (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find all multisets of numbers from candidates that sum to target. A multiset allows repeated elements. We want every distinct multiset, each exactly once."),
        N.h4("What Doesn't Work"),
        N.para("Generating all subsets naively would include every ordering ([2,3] and [3,2] separately) and miss the unlimited-reuse constraint. A DP approach can count combinations but cannot list them without backtracking. Greedy approaches cannot enumerate all possibilities."),
        N.h4("The Key Observation"),
        N.para("If we enforce that our choices are always non-decreasing (by maintaining a start index), then every multiset maps to exactly one sorted sequence. [3,2,2] is never generated because once we choose 3 (index 1), we never look back at 2 (index 0). This makes deduplication free — no post-processing needed."),
        N.h4("Building the Solution"),
        N.para("1. Sort candidates so that candidates[i] > remaining implies all subsequent candidates also exceed remaining. 2. Define backtrack(start, path, remaining). 3. Base case: remaining==0 → append copy. 4. For each candidates[i] from start: if i exceeds remaining, break. Else append, recurse with start=i (same i for reuse), then pop."),
        N.callout("Analogy: Imagine filling a jar to exactly capacity. You pick coins from a tray (sorted smallest first). You can use the same coin multiple times. Once a coin is too large to fit, all larger coins are also too large — stop trying. Record each successful fill.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("candidates.sort()", {"code": True}), " — Sort ascending so we can prune with break. Without sorting, we'd need remainder < 0 check (wasteful — enters calls that overshoot)."])),
    N.para(N.rich([("results = []", {"code": True}), " — Accumulator for all valid combinations."])),
    N.para(N.rich([("if remaining == 0:", {"code": True}), " — Base case: we've hit the target exactly. The current path is a valid combination."])),
    N.para(N.rich([("results.append(path[:])", {"code": True}), " — Copy! Appending the reference path would give every saved result the same (eventually empty) list. path[:] creates a snapshot."])),
    N.para(N.rich([("for i in range(start, len(candidates)):", {"code": True}), " — Only try candidates from index start onward. This enforces non-decreasing order and prevents duplicate combinations."])),
    N.para(N.rich([("if candidates[i] > remaining: break", {"code": True}), " — Early exit. Since sorted, all subsequent candidates also exceed remaining — entire right subtree is pruned."])),
    N.para(N.rich([("path.append(candidates[i])", {"code": True}), " — Choose: add this candidate to the current combination."])),
    N.para(N.rich([("backtrack(i, path, remaining - candidates[i])", {"code": True}), " — Explore: start=i (not i+1!) allows reusing the same element. Remaining decreases by the chosen value."])),
    N.para(N.rich([("path.pop()", {"code": True}), " — Unchoose: remove the last element, restoring path to its state before this iteration. This is the backtracking step."])),
    N.para(N.rich([("backtrack(0, [], target)", {"code": True}), " — Initial call: all candidates available (start=0), empty path, full target."])),
    N.divider(),
]

# ── Solution 2: Brute Force (without sort optimization) ──
solution2_code = """\
def combinationSum_brute(candidates, target):
    results = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        if remaining < 0:       # Prune AFTER overshooting (vs before)
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    backtrack(0, [], target)
    return results
"""

blocks += [
    N.h2("Solution 2 — Backtracking without Prune (Brute Force Baseline)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal, but without the sort-and-break optimization. We still use backtracking with a start index for deduplication."),
        N.h4("What Doesn't Work"),
        N.para("This solution IS correct but slower: it recursively calls backtrack even when candidates[i] > remaining, only detecting the overshoot after the recursive call begins (via remaining < 0). This wastes stack frames."),
        N.h4("The Key Observation"),
        N.para("The brute force version teaches the core template without optimization. Once you understand it, adding sort() and replacing 'remaining < 0: return' with 'candidates[i] > remaining: break' is the only change needed to reach the optimal."),
        N.callout("The brute force is a useful starting point in interviews — propose it first, then optimize. Shows systematic thinking.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if remaining < 0: return", {"code": True}), " — Detects overshoot after the fact. Contrast with optimal: break before entering these calls."])),
    N.para("Everything else is identical to Solution 1 — same backtracking structure, same start index, same copy-on-success. The only difference is WHERE the pruning fires."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Backtracking (no pruning)", "O(N^(T/M)) + overhead", "O(T/M)"],
        ["Backtracking + sort + break (Interview Pick)", "O(N^(T/M))", "O(T/M)"],
    ]),
    N.para("N = number of candidates, T = target, M = smallest candidate. The recursion depth is at most T/M (max times smallest element can fit in target). Output space is additional, proportional to the number of solutions."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Unlimited Use, Start Index"])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("Problem asks for ALL combinations / subsets / arrangements satisfying a condition; elements can be reused; duplicates must be avoided. The 'start index' trick gives non-decreasing ordering, preventing duplicate multisets without a visited set.")]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Backtracking — Unlimited Use / Start Index technique:"),
    N.bullet(N.rich([("Combination Sum II", {"bold": True}), " (Medium) — Each element used at most once; pass i+1 and skip adjacent duplicates (#40)"])),
    N.bullet(N.rich([("Combination Sum III", {"bold": True}), " (Medium) — Exactly k numbers from 1–9 summing to n; add depth limit (#216)"])),
    N.bullet(N.rich([("Combination Sum IV", {"bold": True}), " (Medium) — COUNT the ways (not list); becomes DP unbounded knapsack (#377)"])),
    N.bullet(N.rich([("Subsets", {"bold": True}), " (Medium) — All subsets; same start-index backtracking; save at every node not just leaf (#78)"])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium) — All orderings; no start index; use visited array instead (#46)"])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium) — Backtrack over digit→letters mapping (#17)"])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), " (Medium) — Backtrack over string splits; check palindrome at each step (#131)"])),
    N.para("These problems share the same core technique: systematic path building with choose/explore/unchoose, controlled by a start index to enforce non-decreasing order."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. Sub-pattern: Unlimited Use, Start Index. Source: Analysis.", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("combination_sum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"Notion body appended. PAGE_ID={PAGE_ID}")
print(f"NOTION OK {PAGE_ID}")
