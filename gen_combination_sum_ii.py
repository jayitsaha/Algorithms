"""gen_combination_sum_ii.py — Notion in-place update for Combination Sum II (#40)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-810a-b732-fc56cac64fc6"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=40,
    pattern="Backtracking",
    subpatterns=["Single Use + Skip Dups"],
    tc="O(2^n)",
    sc="O(n)",
    key_insight="Sort + recurse with i+1 (single-use) + skip dup siblings with i>start guard.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a collection of candidate numbers (", {}),
        ("candidates", {"code": True}),
        (") and a target number (", {}),
        ("target", {"code": True}),
        ("), find all unique combinations in ", {}),
        ("candidates", {"code": True}),
        (" where the candidate numbers sum to ", {}),
        ("target", {"code": True}),
        (". Each number in ", {}),
        ("candidates", {"code": True}),
        (" may only be used once in the combination. The solution set must not contain duplicate combinations.", {}),
    ])),
    N.para(N.rich([
        ("Example: candidates=[10,1,2,7,6,1,5], target=8\n", {"bold": True}),
        ("Sorted input: [1,1,2,5,6,7,10]\n", {}),
        ("Output: [[1,1,6],[1,2,5],[1,7],[2,6]]", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────────────
SOL1_CODE = """def combinationSum2(candidates, target):
    candidates.sort()     # Sort: groups dups + enables early break pruning
    results = []

    def backtrack(start, remaining, path):
        if remaining == 0:
            results.append(path[:])  # Copy! path is mutated during backtracking
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:  # Prune: sorted -> all later also too large
                break                       # break, not continue!
            if i > start and candidates[i] == candidates[i-1]:  # Skip dup sibling
                continue                    # i > start (not i > 0) is the critical guard
            path.append(candidates[i])      # Choose
            backtrack(i + 1, remaining - candidates[i], path)  # i+1 = single-use
            path.pop()                      # Unchoose (backtrack)

    backtrack(0, target, [])
    return results"""

blocks += [
    N.h2("Solution 1 — Sort + Backtrack with Duplicate Skip (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to enumerate all subsets of candidates that sum exactly to target, with no index reused and no duplicate subsets in the output. This is a constrained subset-sum enumeration."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach generating all 2^n subsets works but is slow and produces duplicate outputs when candidates contain equal values. We can't use greedy (need all solutions, not just one optimal). DP can count combos but can't enumerate them efficiently."),
        N.h4("The Key Observation"),
        N.para("Two related constraints collapse into one technique: (1) single-use → recurse with i+1 not i. (2) no duplicate combos → sort the array, then at each recursion depth skip any candidate with the same value as the previous sibling. The guard 'i > start' (not 'i > 0') is critical: it allows the same value to appear at deeper recursion levels (different depth), only blocks it as a sibling at the same depth."),
        N.h4("Building the Solution"),
        N.para("Start with the standard backtracking template: choose/explore/unchoose. Modify: (a) advance start to i+1 to enforce single-use, (b) sort and add the skip check for duplicate siblings, (c) add break pruning when the candidate exceeds remaining."),
        N.callout(
            "Analogy: You have a bag of numbered tokens (some duplicated). You want all ways to pick tokens (no replacement) summing to target. Sort the tokens first, then: skip a token if you already tried a token of the same value at this pick-position.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("candidates.sort()", {"code": True}), (" — Sort ascending. Groups equal values adjacently (enables skip rule). Enables early break when candidates[i] > remaining.", {})])),
    N.para(N.rich([("if remaining == 0:", {"code": True}), (" — Base case: this path sums exactly to target. Record it.", {})])),
    N.para(N.rich([("results.append(path[:])", {"code": True}), (" — Append a COPY. Python lists are mutable; if you append path directly all results entries will point to the same mutating object.", {})])),
    N.para(N.rich([("if candidates[i] > remaining: break", {"code": True}), (" — Prune. Since sorted, all subsequent candidates are also too large. break exits the loop; continue would wastefully test each one.", {})])),
    N.para(N.rich([("if i > start and candidates[i] == candidates[i-1]: continue", {"code": True}), (" — Skip duplicate sibling. i > start (not i > 0): allows the same value at deeper levels; only blocks it as a sibling at the same recursion depth.", {})])),
    N.para(N.rich([("path.append(candidates[i])", {"code": True}), (" — Choose: add this candidate to the current combination.", {})])),
    N.para(N.rich([("backtrack(i + 1, ...)", {"code": True}), (" — Recurse with i+1 (not i): single-use — each element position used at most once per combination.", {})])),
    N.para(N.rich([("path.pop()", {"code": True}), (" — Unchoose: remove the candidate we just tried. This backtracking restores path to try the next candidate at this depth.", {})])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────────────
SOL2_CODE = """from collections import Counter

def combinationSum2(candidates, target):
    # Build (value, frequency) pairs sorted by value
    counts = sorted(Counter(candidates).items())
    results = []

    def backtrack(idx, remaining, path):
        if remaining == 0:
            results.append(path[:])
            return
        if idx == len(counts):
            return
        val, freq = counts[idx]
        # Try using 0, 1, 2, ..., up to freq copies of val
        for k in range(0, min(freq, remaining // val) + 1):
            path.extend([val] * k)
            backtrack(idx + 1, remaining - val * k, path)
            if k > 0:
                del path[-k:]   # remove the k values we added

    backtrack(0, target, [])
    return results"""

blocks += [
    N.h2("Solution 2 — Counter-Based (Avoids Skip Rule)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of working on the raw (possibly duplicate) candidates list, work on (value, frequency) pairs. This eliminates the duplicate problem at the data level rather than at the algorithm level."),
        N.h4("What Doesn't Work"),
        N.para("The raw list approach needs the skip-dup guard. Can we avoid it entirely? Yes — by collapsing duplicates into a frequency count up front."),
        N.h4("The Key Observation"),
        N.para("If we group equal candidates together and track how many of each we can use (up to their frequency), we never encounter sibling duplicates. We simply choose 0, 1, 2, ..., freq copies of each distinct value."),
        N.h4("Building the Solution"),
        N.para("Use Counter to get (value, freq) pairs. Sort them by value. At each index, decide how many copies of this value to include (0 to min(freq, remaining//val)). Recurse to the next distinct value."),
        N.callout("This approach is cleaner when there are many duplicates, but slightly harder to derive on the spot in an interview. The Sort+Backtrack solution is more natural.", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sort + Backtrack (Interview Pick)", "O(2^n) worst case", "O(n) recursion stack"],
        ["Counter-Based", "O(2^n) worst case", "O(n) stack + O(k) counter"],
    ]),
    N.para("Both are O(2^n) in the worst case — we explore all subsets. The break pruning (when candidates[i] > remaining) dramatically reduces the constant factor. The sort costs O(n log n) but is dominated by the backtracking."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Single Use + Skip Dups — backtracking with advance-start (single-use), sort, and duplicate-sibling skip", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'find ALL combinations/subsets' (not just count), (2) input may have duplicates and result must be unique, (3) each element used at most once, (4) target sum constraint. The combination of these four signals points directly to Sort + Backtrack with skip-dup guard.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related backtracking technique:"),
    N.bullet(N.rich([("Combination Sum I", {"bold": True}), (" (Medium) — Same structure, but unlimited reuse: recurse with i not i+1; no duplicate input, no skip rule (#39)", {})])),
    N.bullet(N.rich([("Subsets II", {"bold": True}), (" (Medium) — Exact same sort + skip-dup rule; enumerate all subsets instead of target-sum combos (#90)", {})])),
    N.bullet(N.rich([("Combination Sum III", {"bold": True}), (" (Medium) — Exactly k elements from digits 1-9; same single-use + sort pattern, add depth limit (#216)", {})])),
    N.bullet(N.rich([("Permutations II", {"bold": True}), (" (Medium) — Duplicate-skip idea for permutations; uses a visited[] array instead of start index (#47)", {})])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), (" (Medium) — Backtracking with validity check (isPalindrome) instead of sum check; builds partition intuition (#131)", {})])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), (" (Medium) — Core backtracking without dup concern; good entry-level backtracking problem (#17)", {})])),
    N.bullet(N.rich([("Word Break II", {"bold": True}), (" (Hard) — Backtracking with memoization on a string; same choose/explore/unchoose pattern (#140)", {})])),
    N.para("These problems share the core pattern: choose a candidate, recurse deeper, unchoose to try the next."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. Sub-pattern: Single Use + Skip Dups.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("combination_sum_ii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
