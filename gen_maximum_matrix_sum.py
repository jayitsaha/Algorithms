"""
gen_maximum_matrix_sum.py — Notion page creation for Maximum Matrix Sum (LC #1975)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# notion_page_id = null → create fresh
PAGE_ID = N.create_page("Maximum Matrix Sum", 1975, "Medium", "🟡")
print(f"Created page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1975,
    pattern="Greedy",
    subpatterns=["Count Negatives Flip Pairs"],
    tc="O(n²)",
    sc="O(1)",
    key_insight="Parity of negative count is invariant; even→flip all, odd→penalty on min-abs cell.",
    icon="🟡"
)
print("Properties set.")

# 2) Build body blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para("You are given an n x n integer matrix. You can multiply any two adjacent elements "
           "(horizontally or vertically adjacent) by -1 any number of times. Return the maximum "
           "possible sum of the matrix's elements after performing such operations."),
    N.divider(),
]

# ── Solution 1 — Greedy (Interview Pick) ──
sol1_code = """\
def maxMatrixSum(matrix: List[List[int]]) -> int:
    total_abs = 0
    neg_count = 0
    min_abs = float('inf')

    for row in matrix:
        for val in row:
            total_abs += abs(val)
            if val < 0:
                neg_count += 1
            min_abs = min(min_abs, abs(val))

    if neg_count % 2 == 0:
        return total_abs
    else:
        return total_abs - 2 * min_abs"""

blocks += [
    N.h2("Solution 1 — Greedy: Count Negatives (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to maximize the sum of a matrix where we can flip the sign of any two "
               "adjacent cells simultaneously, any number of times. Rather than simulating flips, "
               "ask: what is the final optimal configuration, and can we reach it?"),
        N.h4("What Doesn't Work"),
        N.para("Brute-force simulation is exponential — too many possible flip sequences. "
               "Even greedy 'always flip the most negative pair' doesn't directly give the answer "
               "because flipping changes both cells."),
        N.h4("The Key Observation"),
        N.para("Each flip changes the sign of exactly two cells, so the count of negatives "
               "changes by 0 or ±2. The parity (even/odd) of the negative count is invariant. "
               "Also, since the matrix is connected via adjacency, you can move any negative sign "
               "to any other cell by chaining flips."),
        N.h4("Building the Solution"),
        N.para("Given mobility + parity invariant: if neg_count is even, pair them all up and "
               "flip → all cells positive → answer = sum(|val|). If neg_count is odd, one negative "
               "is unavoidable; move it to the cell with min absolute value to minimize penalty. "
               "Correction: total_abs − 2×min_abs (subtract 2× because we switch +min to −min)."),
        N.callout("Analogy: Negatives are like marked tokens on a grid. You can move any token "
                  "anywhere by sliding, but you can never create or destroy an odd number of tokens. "
                  "If you start with 4 tokens, you can collect them all. With 3, one always remains "
                  "— park it on the cheapest cell.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("total_abs = 0", {"code": True}),
                   " — Running sum of absolute values of all cells; represents the ideal sum if all were positive."])),
    N.para(N.rich([("neg_count = 0", {"code": True}),
                   " — Counts cells with negative values."])),
    N.para(N.rich([("min_abs = float('inf')", {"code": True}),
                   " — Tracks the smallest absolute value seen so far; this cell bears the inescapable negative (odd case)."])),
    N.para(N.rich([("total_abs += abs(val)", {"code": True}),
                   " — Always add |val|: we're computing as if every cell were positive."])),
    N.para(N.rich([("if val < 0: neg_count += 1", {"code": True}),
                   " — Count each negative cell."])),
    N.para(N.rich([("min_abs = min(min_abs, abs(val))", {"code": True}),
                   " — Track the globally smallest |val| across the entire matrix."])),
    N.para(N.rich([("if neg_count % 2 == 0: return total_abs", {"code": True}),
                   " — Even negatives: all can be eliminated. Return the full absolute sum."])),
    N.para(N.rich([("else: return total_abs - 2 * min_abs", {"code": True}),
                   " — Odd negatives: one must stay negative. Penalty = 2*min_abs (switching +v to -v changes contribution by 2v)."])),
    N.divider(),
]

# ── Why It Works ──
blocks += [
    N.h2("Why It Works: The Parity Invariant"),
    N.h3("Proof (case analysis on one flip)"),
    N.para("Case 1: both cells positive (+,+) → (−,−): neg_count +2 → parity unchanged."),
    N.para("Case 2: both cells negative (−,−) → (+,+): neg_count −2 → parity unchanged."),
    N.para("Case 3: mixed (+,−) or (−,+): neg_count unchanged → parity unchanged."),
    N.para("Every possible flip falls into one of these three cases. Therefore: starting parity = final parity regardless of operation sequence."),
    N.callout("Mobility: Since the matrix is fully connected via adjacency (any cell can reach any "
              "other by a path of horizontal/vertical steps), you can move any negative to any cell "
              "by chaining flips. Combined with parity: if even → reach all-positive; if odd → "
              "reach exactly-one-negative, placed anywhere. Optimal placement = min-abs cell.",
              "🔐", "gray_background"),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (simulate flips)", "Exponential", "O(n²)"],
        ["Greedy — Count Negatives (optimal)", "O(n²)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Count Negatives Flip Pairs (Guide Section 16)"])),
    N.callout(
        "When to recognize this pattern: (1) 'multiply two adjacent elements by −1 any number of times' "
        "(2) maximizing/minimizing a sum with sign-flip operations "
        "(3) unlimited symmetric operations → look for conservation laws (parity invariant) "
        "(4) operation acts on pairs → parity of count of negatives is preserved.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Count Negatives / Parity Greedy):"),
    N.bullet(N.rich([("Sign of the Product of an Array", {"bold": True}),
                     " (Easy) — Count negatives to determine sign; same parity logic."])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}),
                     " (Medium) — Negative signs interact multiplicatively; track min/max products."])),
    N.bullet(N.rich([("Minimum Cost to Move Chips to Same Position", {"bold": True}),
                     " (Easy) — Even distance moves are free; odd distance costs 1 — parity-based greedy."])),
    N.bullet(N.rich([("Flip Game II", {"bold": True}),
                     " (Medium) — Game theory with sign-flip operations; parity of remaining tokens matters."])),
    N.bullet(N.rich([("Gas Station", {"bold": True}),
                     " (Medium) — Greedy with key invariant: if total surplus >= 0, a valid start exists."])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}),
                     " (Medium) — Greedy: highest-frequency element determines idle gaps in optimal schedule."])),
    N.para("These problems share the core technique: identify an invariant that bounds what "
           "sequences of operations can achieve, then solve the constrained optimization greedily."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 16 (GREEDY), "
              "Sub-Pattern: Count Negatives, Flip Pairs.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_matrix_sum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# 3) Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("Blocks appended.")
print(f"NOTION OK {PAGE_ID}")
