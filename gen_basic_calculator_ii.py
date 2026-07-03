"""
gen_basic_calculator_ii.py
Regenerate Notion page for Basic Calculator II (#227).
Run from the Algorithms directory: python3 gen_basic_calculator_ii.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81d4-b87a-cbdc9bfa8826"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=227,
    pattern="Stacks",
    subpatterns=["Stack + Precedence"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push ±num for +/-; pop+compute for */÷; sum stack at end handles precedence.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old content ─────────────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ───────────────────────────────────────────────────────────
print("Building body blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" representing a valid expression containing non-negative integers, "
         "the operators ", {}),
        ("+ - * /", {"code": True}),
        (", and spaces, evaluate and return the integer result. "
         "Division truncates toward zero (not floor). No parentheses.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ("s = \"3+2*2\"", {"code": True}),
        (" → 7  (2*2=4 first, then 3+4)", {}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ("s = \"14-3/2\"", {"code": True}),
        (" → 13  (3/2=1 truncated, then 14-1)", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Stack + Deferred Addition ──
sol1_code = """\
def calculate(s: str) -> int:
    stack = []          # pending signed addends
    num = 0             # current number being built
    op = '+'            # previous operator (sentinel: '+' for first number)
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)   # handle multi-digit numbers
        if ch in '+-*/' or i == len(s) - 1:
            if op == '+':
                stack.append(num)       # defer: push as positive
            elif op == '-':
                stack.append(-num)      # defer: push as negative
            elif op == '*':
                stack.append(stack.pop() * num)          # resolve now
            elif op == '/':
                stack.append(int(stack.pop() / num))     # truncate toward 0
            op = ch     # save current operator for next iteration
            num = 0     # reset accumulator
    return sum(stack)   # all deferred +/- collapse here
"""

blocks += [
    N.h2("Solution 1 — Stack + Deferred Addition (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to evaluate an arithmetic string respecting operator precedence: "
               "* and / bind tighter than + and -. Reading left-to-right naively ignores this."),
        N.h4("What Doesn't Work"),
        N.para("A simple left-to-right evaluation applies each operator as soon as it's seen. "
               "For '3+2*2' this gives (3+2)*2 = 10. Wrong. We need to ensure 2*2 is computed first."),
        N.h4("The Key Observation"),
        N.para("We can't sum immediately when we see +/-, because the next number might be part "
               "of a chain of * or /. But we CAN resolve * and / immediately, because there's no "
               "higher-precedence operator to worry about. So: defer additions, apply multiplications now."),
        N.h4("Building the Solution"),
        N.para("A stack stores 'pending addends' — signed values waiting to be summed. "
               "For +/-: push the signed number (deferred). For * /: pop the last addend, "
               "compute, push the result (immediately resolved). At the end, sum(stack) "
               "applies all deferred additions. The sentinel op='+' handles the first number uniformly."),
        N.callout(
            "Analogy: Think of the stack as a shopping cart. +/- items go straight in the cart. "
            "For * or /, you pick up the last item you put in, replace it with its combination with "
            "the current item, then put it back. At checkout, you total everything in the cart.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — The accumulator for pending addends; each entry is one signed term waiting to be summed."])),
    N.para(N.rich([("num = 0", {"code": True}), " — Accumulates the current multi-digit number digit by digit."])),
    N.para(N.rich([("op = '+'", {"code": True}), " — Sentinel: acts as if '+' precedes the first number, so the first number is pushed as +num with no special case."])),
    N.para(N.rich([("num = num * 10 + int(ch)", {"code": True}), " — Shifts the existing number left and appends the new digit. '1','4','2' yields 1 then 14 then 142."])),
    N.para(N.rich([("if ch in '+-*/' or i == len(s) - 1:", {"code": True}), " — Fire evaluation when we see an operator OR at the last character (no trailing operator otherwise triggers evaluation of the last number)."])),
    N.para(N.rich([("stack.append(num) / stack.append(-num)", {"code": True}), " — Defer + and - by pushing the signed value. It will be added later in sum(stack)."])),
    N.para(N.rich([("stack.append(stack.pop() * num)", {"code": True}), " — Immediately resolve *: pop the left operand (the pending addend), multiply, push the product."])),
    N.para(N.rich([("stack.append(int(stack.pop() / num))", {"code": True}), " — Resolve /: int() truncates toward zero. Python's // floors toward -inf, which differs for negative values."])),
    N.para(N.rich([("op = ch; num = 0", {"code": True}), " — Save current operator as the next previous op; reset accumulator."])),
    N.para(N.rich([("return sum(stack)", {"code": True}), " — All deferred +/- terms (possibly already composed by * and /) are summed in one shot."])),
    N.divider(),
]

# ── Solution 2: Two-Pass ──
sol2_code = """\
def calculate_two_pass(s: str) -> int:
    # Step 1: tokenize (numbers and operators, skip spaces)
    tokens, i, n = [], 0, len(s)
    while i < n:
        if s[i] == ' ': i += 1; continue
        if s[i].isdigit():
            j = i
            while j < n and s[j].isdigit(): j += 1
            tokens.append(int(s[i:j])); i = j
        else:
            tokens.append(s[i]); i += 1
    # Step 2: resolve all * and / left-to-right
    stack, i = [], 0
    while i < len(tokens):
        if tokens[i] == '*':
            stack.append(stack.pop() * tokens[i+1]); i += 2
        elif tokens[i] == '/':
            stack.append(int(stack.pop() / tokens[i+1])); i += 2
        else:
            stack.append(tokens[i]); i += 1
    # Step 3: resolve + and - with a sign tracker
    result, sign = 0, 1
    for t in stack:
        if t == '+': sign = 1
        elif t == '-': sign = -1
        else: result += sign * t
    return result
"""

blocks += [
    N.h2("Solution 2 — Two-Pass Tokenize (O(n) time, clearer stages)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of handling everything inline, separate parsing from evaluation "
               "into two explicit stages."),
        N.h4("The Key Observation"),
        N.para("If you first tokenize (split into numbers and operators), then make one pass "
               "to eliminate all * and / (replacing them with their result), you're left with "
               "a simple sequence of numbers and + / - operators that can be evaluated trivially."),
        N.h4("Building the Solution"),
        N.para("Tokenize the string. Use a stack to process * and / immediately. "
               "Then walk the result stack, tracking sign, and accumulate the final answer."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Stack + Deferred (Sol 1)", "O(n)", "O(n)", "Single pass, interview pick"],
        ["Two-Pass Tokenize (Sol 2)", "O(n)", "O(n)", "Clearer stages, more code"],
        ["Naïve left-to-right", "O(n)", "O(1)", "WRONG — ignores precedence"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack + Precedence (Guide Section 6.1)"])),
    N.callout(
        "When to recognize this pattern: "
        "\"Evaluate arithmetic string\" · \"Operators with two different precedence levels\" · "
        "\"No parentheses\" · Deferred vs immediate operations. "
        "Add a sign-stack or recursion to handle parentheses (Basic Calculator I/III).",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Stack + Expression Evaluation):"),
    N.bullet(N.rich([("Basic Calculator", {"bold": True}), " (Medium) — Adds parentheses; use a sign-stack for nested context (#224)"])),
    N.bullet(N.rich([("Basic Calculator III", {"bold": True}), " (Hard) — All four operators + parentheses; recursive descent or two stacks (#772)"])),
    N.bullet(N.rich([("Evaluate Reverse Polish Notation", {"bold": True}), " (Medium) — Postfix; no precedence needed, pure operand stack (#150)"])),
    N.bullet(N.rich([("Expression Add Operators", {"bold": True}), " (Hard) — Insert operators into a digit string to hit target value (#282)"])),
    N.bullet(N.rich([("Decode String", {"bold": True}), " (Medium) — Stack for nested bracket expressions with repeat counts (#394)"])),
    N.bullet(N.rich([("Remove Duplicate Letters", {"bold": True}), " (Medium) — Stack maintains greedy ordering constraint (#316)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Foundational bracket-matching with a stack (#20)"])),
    N.para("These problems share the same core technique: a stack to manage deferred vs immediate operations."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6.1 — Stacks & Queues → Basic Stack Operations", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("basic_calculator_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append to Notion ──
print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
