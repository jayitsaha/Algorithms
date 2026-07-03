"""
gen_generate_parentheses.py — Notion IN-PLACE update for Generate Parentheses (LC #22)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813f-aae4-f5ad2fadee88"

# ── 1) Properties ─────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=22,
    pattern="Backtracking",
    subpatterns=["Track Open/Close Counts"],
    tc="O(4^n / sqrt(n))",
    sc="O(n)",
    key_insight="Track open/close counts; add '(' if open<n, add ')' only if close<open — guards ensure every generated string is valid by construction.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given ", {}),
        ("n", {"code": True}),
        (" pairs of parentheses, generate all combinations of well-formed parentheses.\n\n"
         "Example 1: n=3 → [\"((()))\", \"(()())\", \"(())()\", \"()(())\", \"()()()\"]\n"
         "Example 2: n=1 → [\"()\"]\n\n"
         "Constraints: 1 ≤ n ≤ 8", {})
    ])),
    N.divider(),
]

# ── Solution 1 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Backtracking via String Concatenation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are building a string of length 2n character by character. At each position, we make a binary choice: append '(' or append ')'. We want every finished string to be a valid parentheses sequence."),
        N.h4("What Doesn't Work"),
        N.para("Generating all 2^(2n) possible strings and then filtering: for n=8 that's 65,536 strings, but only 1430 are valid — we waste 98% of the work on strings we discard."),
        N.h4("The Key Observation"),
        N.para("We don't need to finish a string to know it's invalid. If at any point close > open, the string CANNOT become valid — no matter what we add after. We can prune this branch immediately."),
        N.h4("Building the Solution"),
        N.para("Track two integers: open (opening brackets placed) and close (closing brackets placed).\n\n"
               "Rule 1: Add '(' if open < n — we still have opening bracket budget.\n"
               "Rule 2: Add ')' if close < open — there is an unmatched '(' to close.\n\n"
               "Base case: when open == n and close == n, the string is complete and valid — append to results.\n\n"
               "Because we pass curr + \"(\" (a new string), each recursive call gets its own copy. No explicit undo needed."),
        N.callout(
            "Analogy: Imagine a bank account for brackets. You start with a budget of n deposits (opening brackets). You can only withdraw (close) when your balance (open - close) is positive. When both budget and balance reach zero simultaneously, you're done.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""def generateParenthesis(n: int) -> list[str]:
    result = []
    def backtrack(curr, open, close):
        if open == n and close == n:
            result.append(curr)
            return
        if open < n:
            backtrack(curr + "(", open + 1, close)
        if close < open:
            backtrack(curr + ")", open, close + 1)
    backtrack("", 0, 0)
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — collect all valid strings; this list is shared across all recursive calls via closure."])),
    N.para(N.rich([("def backtrack(curr, open, close):", {"code": True}), " — curr = string built so far; open = count of '(' placed; close = count of ')' placed."])),
    N.para(N.rich([("if open == n and close == n:", {"code": True}), " — base case: we have used exactly n of each bracket type. The string is complete and valid."])),
    N.para(N.rich([("result.append(curr)", {"code": True}), " — save the complete string. The implicit return causes the call stack to unwind (backtrack)."])),
    N.para(N.rich([("if open < n:", {"code": True}), " — first guard: we still have opening bracket budget left."])),
    N.para(N.rich([("backtrack(curr + \"(\", open + 1, close)", {"code": True}), " — create a new string (no mutation), recurse with one more '(' placed."])),
    N.para(N.rich([("if close < open:", {"code": True}), " — second guard: there is at least one unmatched '(' that we can close."])),
    N.para(N.rich([("backtrack(curr + \")\", open, close + 1)", {"code": True}), " — create a new string with one more ')' placed; recurse."])),
    N.para(N.rich([("backtrack(\"\", 0, 0)", {"code": True}), " — kick off the recursion: empty string, zero of each bracket type placed."])),
    N.divider(),
]

# ── Solution 2 ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Backtracking with Mutable List (Explicit Undo)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same problem, but instead of creating a new string on every recursive call, we use a shared mutable list (path) and explicitly append/pop."),
        N.h4("What Doesn't Work"),
        N.para("If you forget the pop() after the recursive call, the path accumulates characters from previous branches — the results are completely corrupted."),
        N.h4("The Key Observation"),
        N.para("The pop() after each recursive call IS the backtracking. It undoes the last choice so we can try the alternative (add ')' instead of '(', or simply return)."),
        N.h4("Building the Solution"),
        N.para("Use path = [] as a shared buffer. Before recursing, append the character. After the recursive call returns, pop it. Join the list into a string only at the leaf (base case) — much cheaper than string concatenation at every node."),
        N.callout("Why this approach? Each recursive frame shares the same path list via reference. This avoids O(n) string allocations per call — at depth 2n, that's 2n allocations saved. The trade-off: you must remember to pop.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""def generateParenthesis(n: int) -> list[str]:
    result, path = [], []
    def backtrack(open, close):
        if open == n and close == n:
            result.append("".join(path))
            return
        if open < n:
            path.append("(")
            backtrack(open + 1, close)
            path.pop()          # undo: backtrack!
        if close < open:
            path.append(")")
            backtrack(open, close + 1)
            path.pop()          # undo: backtrack!
    backtrack(0, 0)
    return result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("result, path = [], []", {"code": True}), " — result collects finished strings; path is the shared mutable buffer for the current string being built."])),
    N.para(N.rich([("result.append(\"\".join(path))", {"code": True}), " — at the leaf, join the list once to form the string. More efficient than concatenating at every level."])),
    N.para(N.rich([("path.append(\"(\")", {"code": True}), " — mutate the shared path: add '(' as our choice."])),
    N.para(N.rich([("backtrack(open + 1, close)", {"code": True}), " — explore the subtree with this choice."])),
    N.para(N.rich([("path.pop()", {"code": True}), " — UNDO the choice: remove the '(' we just added before trying the next option. This is the literal 'back' in backtracking."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute force (generate all + filter)", "O(2^2n × n)", "O(n)"],
        ["Backtracking — string concat (Solution 1)", "O(4^n / sqrt(n))", "O(n) call stack"],
        ["Backtracking — mutable list (Solution 2)", "O(4^n / sqrt(n))", "O(n) call stack"],
    ]),
    N.para(N.rich([
        ("Note: ", {"bold": True}),
        ("The exact output size is the nth Catalan number Cₙ = C(2n,n)/(n+1), which is O(4^n / sqrt(n)). "
         "Each string has length 2n. So total time is O(Cₙ × n). "
         "For n=3: 5 strings × 6 chars = 30 operations. "
         "For n=8: 1430 strings × 16 chars = 22,880 operations — perfectly tractable.", {})
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Open/Close Counts (count-guard variant of backtracking)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to 'generate all valid combinations' of structured output\n"
        "• Validity at each step can be expressed as simple inequalities on running counts\n"
        "• Two complementary quantities that must stay in balance (open ≥ close, both ≤ n)\n"
        "• Output size is Catalan-number scale (not factorial, not purely exponential)\n"
        "• 'Well-formed', 'balanced', or 'valid sequence' in the problem description",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("The 'Track Open/Close Counts' sub-pattern is a problem-specific variant. "
         "It is classified under Backtracking as the main pattern. "
         "Source: Analysis (problem-specific sub-pattern not explicitly listed as a named entry in DSA_Patterns_and_SubPatterns_Guide.md).", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same core technique (Backtracking — binary decision per position with guard conditions):"),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium) — Backtracking through digit-to-letter map; choose one char per position from a set (#17)"])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium) — Backtracking with a running sum guard; same choose-and-recurse-and-undo pattern (#39)"])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium) — Backtracking with used[] boolean to track available elements; all orderings (#46)"])),
    N.bullet(N.rich([("Subsets", {"bold": True}), " (Medium) — At each element: include or skip; enumerate all 2^n subsets via backtracking (#78)"])),
    N.bullet(N.rich([("Remove Invalid Parentheses", {"bold": True}), " (Hard) — BFS/backtracking with minimum removals; validates same close ≤ open invariant (#301)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Stack-based check enforcing the same 'close never exceeds open' rule (#20)"])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), " (Medium) — Backtracking to enumerate all valid string splits; DFS + prune structure (#131)"])),
    N.para("These problems share the same core technique: make a binary (or k-ary) decision at each step, prune via a guard condition, recurse, then undo the choice (explicit pop) or rely on immutability (string concat)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section. Sub-pattern 'Track Open/Close Counts' is an Analysis classification specific to parentheses-style problems.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("generate_parentheses")),
    N.para(N.rich([
        ("Step through the backtracking algorithm visually for n=3 — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
