"""gen_basic_calculator.py — Notion update for Basic Calculator (#224)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8158-8a82-f96f70db44e3"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=224,
    pattern="Stacks",
    subpatterns=["Expression Evaluation", "Stack for Nested Expressions"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push (result, sign) on '(', reset; on ')' flush, pop sign×inner + outer.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string "), ("s", {"code": True}),
        (" representing a mathematical expression containing non-negative integers, "),
        ("+", {"code": True}), (", "), ("-", {"code": True}), (", "),
        ("(", {"code": True}), (", "), (")", {"code": True}),
        (", and spaces, implement a basic calculator to evaluate it and return its integer value. "
         "You may not use the built-in eval() function. "
         "The expression is always valid and there are no division or multiplication operators.")
    ])),
    N.callout(
        N.rich([("Example: "), ("\"1 + (2 - 3)\"", {"code": True}),
                (" → "), ("-4", {"code": True}),
                ("   |   "), ("\"2-(5-6)\"", {"code": True}),
                (" → "), ("3", {"code": True})]),
        "🧮", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: Stack Iterative ────────────────────────────────────────────────
sol1_code = """\
def calculate(s: str) -> int:
    stack = []          # stores (result, sign) pairs at each '('
    result = 0          # running sum at current nesting level
    sign = 1            # next operator: +1=add, -1=subtract
    num = 0             # accumulates current multi-digit integer

    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)   # build multi-digit: '1','2','3' -> 1,12,123
        elif ch in '+-':
            result += sign * num       # FLUSH completed number into result
            num = 0
            sign = 1 if ch == '+' else -1   # record operator as ±1
        elif ch == '(':
            stack.append(result)       # save outer running total
            stack.append(sign)         # save sign applied to sub-expression
            result = 0                 # fresh start inside parens
            sign = 1
        elif ch == ')':
            result += sign * num       # FLUSH last number inside parens
            num = 0
            result *= stack.pop()      # apply outer sign to inner result
            result += stack.pop()      # merge with outer running total
        # ch == ' ': skip silently (no else needed)

    return result + sign * num         # flush any trailing number after loop
"""

intuition1_children = [
    N.h4("Reframe the Problem"),
    N.para("Without parentheses, evaluating '+' and '-' expressions is trivial: scan left-to-right, track the running sum and the sign of each term. Parentheses create nested sub-expressions that must complete before contributing to the outer sum — the challenge is managing that nesting."),
    N.h4("What Doesn't Work"),
    N.para("A simple left-to-right scan fails because when we encounter '-(', we can't subtract anything yet — we don't know the value of the sub-expression. We'd have to look ahead an arbitrary distance. Recursion is one option, but using the program call stack is equivalent to using an explicit stack."),
    N.h4("The Key Observation"),
    N.para("Each open parenthesis creates a new 'frame' with its own running total and sign context. When the parenthesis closes, the inner frame's result is scaled by the outer sign and added to the outer total. This is exactly what a stack does: push on '(', pop on ')'."),
    N.h4("Building the Solution"),
    N.para("Track four variables: result (current-level running sum), sign (next operator), num (current integer being assembled), stack (context across paren boundaries). On '(': push (result, sign), reset both. On ')': flush num, pop sign to scale inner result, pop outer result to add back. The push order matters: result first, then sign (so sign is on top for the first pop)."),
    N.callout("Analogy: Think of parentheses like function calls. Open paren = enter a new function frame. Close paren = return the sub-result to the caller. The stack is the call stack made explicit.", "🧠", "blue_background"),
]

blocks += [
    N.h2("Solution 1 — Stack Iterative (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition1_children),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Will store interleaved (result, sign) values. Each open parenthesis pushes two items; each close pops two."])),
    N.para(N.rich([("result = 0", {"code": True}), " — Running sum for the current nesting level. Starts fresh at 0."])),
    N.para(N.rich([("sign = 1", {"code": True}), " — The operator (+1 or -1) to apply to the next term. Initialized to +1 because the first term is positive."])),
    N.para(N.rich([("num = 0", {"code": True}), " — Accumulates multi-digit integers character by character. Flushed into result on non-digit characters."])),
    N.para(N.rich([("num = num * 10 + int(ch)", {"code": True}), " — Builds multi-digit numbers: seeing '1', '2', '3' in sequence produces 1, then 12, then 123."])),
    N.para(N.rich([("result += sign * num", {"code": True}), " (on operator/close-paren) — The FLUSH operation. Adds the completed number (scaled by current sign) into the running total."])),
    N.para(N.rich([("sign = 1 if ch == '+' else -1", {"code": True}), " — Records the next operator as a multiplier. This lets us apply it to the next term with a single multiplication."])),
    N.para(N.rich([("stack.append(result); stack.append(sign)", {"code": True}), " — Saves the outer context in two pushes. Sign is pushed second so it's on top (first to pop at close paren)."])),
    N.para(N.rich([("result = 0; sign = 1", {"code": True}), " — Resets to a fresh state for the sub-expression. The inner expression starts from scratch."])),
    N.para(N.rich([("result *= stack.pop()", {"code": True}), " — First pop gets the outer sign. Multiplying inner result by this sign applies the -(, +(  context to the entire sub-expression."])),
    N.para(N.rich([("result += stack.pop()", {"code": True}), " — Second pop gets the outer running total. Adding merges the sub-expression into the outer level."])),
    N.para(N.rich([("return result + sign * num", {"code": True}), " — Flushes any trailing number. The last number in the string has no operator after it, so it's never flushed during the loop."])),
    N.divider(),
]

# ── Solution 2: Recursive Descent ─────────────────────────────────────────────
sol2_code = """\
def calculate(s: str) -> int:
    i = 0

    def parse() -> int:
        nonlocal i
        result, sign = 0, 1

        while i < len(s):
            ch = s[i]; i += 1

            if ch.isdigit():
                num = int(ch)
                while i < len(s) and s[i].isdigit():
                    num = num * 10 + int(s[i]); i += 1
                result += sign * num

            elif ch == '+':
                sign = 1
            elif ch == '-':
                sign = -1
            elif ch == '(':
                result += sign * parse()   # recurse for sub-expression
            elif ch == ')':
                break                      # return sub-result to caller

        return result

    return parse()
"""

intuition2_children = [
    N.h4("Reframe the Problem"),
    N.para("An expression with parentheses has a naturally recursive structure: an expression is a sum/difference of terms, and each term can be either a number or a parenthesized sub-expression. Recursive descent directly mirrors this grammar."),
    N.h4("What Doesn't Work"),
    N.para("The iterative stack solution is slightly tricky to get right because push/pop order matters and the flush-before-action rule is easy to forget. A recursive solution can be cleaner to reason about, though it risks Python's recursion limit for extremely deep nesting."),
    N.h4("The Key Observation"),
    N.para("When parse() encounters '(', it recurses — the recursive call handles the sub-expression and returns its value, which is then added to the outer result. When the recursive call hits ')', it breaks and returns. The call stack IS the context stack."),
    N.h4("Building the Solution"),
    N.para("Use a shared index variable i (via nonlocal) to advance through the string globally. When we see '(', call parse() which advances i until it sees ')' and returns the sub-expression value. This cleanly separates the sub-problem."),
]

blocks += [
    N.h2("Solution 2 — Recursive Descent"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", intuition2_children),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("i = 0", {"code": True}), " — Global index into the string, shared across all recursive calls via nonlocal."])),
    N.para(N.rich([("result += sign * parse()", {"code": True}), " — Recursive call for sub-expression. parse() advances i until the matching ')' and returns the sub-expression's value."])),
    N.para(N.rich([("elif ch == ')': break", {"code": True}), " — Signals end of sub-expression. Breaks out of the while loop, returning result to the caller (which was waiting for the ')')."])),
    N.callout("⚠️ Python's default recursion limit is 1000. For inputs with nesting depth > 1000, use the iterative stack solution.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Stack Iterative (Interview Pick)", "O(n)", "O(n)", "Stack depth = nesting depth; no recursion limit risk"],
        ["Recursive Descent", "O(n)", "O(n)", "Clean model; call stack depth = nesting depth; Python limit risk"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks — using a stack to manage nested scope/context."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Expression Evaluation / Stack for Nested Expressions — save (result, sign) on '(', restore and merge on ')'."])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("Parentheses in an expression creating nested sub-problems; "
                 "inner results that combine into outer computations; "
                 "any problem where '(' pushes context and ')' restores it.")]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same technique:")]
related = [
    ("Basic Calculator II", "Medium", "#227 — Adds * and /; operator precedence via stack; no parentheses"),
    ("Basic Calculator III", "Hard", "#772 — Full four operators + parentheses; recursive descent or two-stack"),
    ("Evaluate Reverse Polish Notation", "Medium", "#150 — Postfix notation; single operand stack, no parentheses"),
    ("Valid Parentheses", "Easy", "#20 — Foundation: bracket matching with a stack"),
    ("Decode String", "Medium", "#394 — Nested repetitions k[s]; push/pop on [ ]"),
    ("Mini Parser", "Medium", "#385 — Nested integer structure parsing; stack on [ ]"),
    ("Remove All Adjacent Duplicates II", "Medium", "#1209 — Stack tracks (char, count); pops when count reaches k"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}), (" (", {}), (diff, {}), (") — ", {}), (note, {})
    ])))
blocks += [
    N.para("These problems share the core technique of using a stack to manage nested context, pushing state on opening delimiters and popping/merging on closing ones."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section. Sub-Pattern: Expression Evaluation / Stack for Nested Expressions", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("basic_calculator")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks.")
print("NOTION OK", PAGE_ID)
