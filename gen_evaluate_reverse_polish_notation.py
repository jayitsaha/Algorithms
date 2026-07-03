"""gen_evaluate_reverse_polish_notation.py — Notion page rebuild for LeetCode #150."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8153-ba4f-cfbe8843ec54"
SLUG = "evaluate_reverse_polish_notation"

print(f"Step 1: Setting properties on {PAGE_ID}")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=150,
    pattern="Stacks",
    subpatterns=["Stack Operand/Operator"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push numbers onto a stack; for each operator pop two (b=right, a=left), compute a OP b, push result. Use int(a/b) not a//b for division.",
    icon="🟡",
)
print("Properties set OK")

print("Step 2: Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks")

print("Step 3: Building body blocks...")
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ('You are given an array of strings ', {}),
        ('tokens', {'code': True}),
        (' representing an arithmetic expression in Reverse Polish Notation. Each token is either an integer or one of the operators ', {}),
        ('+', {'code': True}),
        (', ', {}),
        ('-', {'code': True}),
        (', ', {}),
        ('*', {'code': True}),
        (', ', {}),
        ('/', {'code': True}),
        ('. Return the integer that represents the value of the expression. Division truncates toward zero.', {}),
    ])),
    N.para("Examples:"),
    N.para(N.rich([
        ('Input: tokens = ["2","1","+","3","*"]  →  Output: 9', {'code': True}),
    ])),
    N.para(N.rich([
        ('Input: tokens = ["4","13","5","/","+"]  →  Output: 6', {'code': True}),
    ])),
    N.para(N.rich([
        ('Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]  →  Output: 22', {'code': True}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Operand Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to evaluate an expression where operators come after their operands. We scan left-to-right, and an operator always acts on the two most recently seen numbers that haven't been consumed yet."),
        N.h4("What Doesn't Work"),
        N.para("Naive string parsing or recursion risks O(n^2) or deep call-stack issues. We can't look ahead to find operands — we need to defer numbers until their matching operator arrives."),
        N.h4("The Key Observation"),
        N.para("'The two most recently seen, not-yet-consumed numbers' is precisely the LIFO (Last-In, First-Out) contract of a stack. Every time an operator arrives, its two operands are guaranteed to be the top two elements."),
        N.h4("Building the Solution"),
        N.para("Initialize an empty stack. For each token: if it's a number, push it. If it's an operator, pop b (right operand), pop a (left operand), compute a OP b, push result. After all tokens, pop and return the one remaining value."),
        N.callout(
            "Analogy: Think of a running total on an HP RPN calculator. You enter numbers, they stack up. You press an operator, it grabs the top two numbers, computes, and replaces them with the result. Exactly what we implement.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def evalRPN(tokens: list[str]) -> int:
    stack = []
    ops = {'+', '-', '*', '/'}
    for token in tokens:
        if token not in ops:
            stack.append(int(token))
        else:
            b = stack.pop()           # RIGHT operand (top of stack)
            a = stack.pop()           # LEFT operand (second from top)
            if   token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            else:              stack.append(int(a / b))  # truncate toward zero
    return stack.pop()"""),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Initialize the empty operand stack. This is our working memory for numbers awaiting computation."])),
    N.para(N.rich([("ops = {'+', '-', '*', '/'}", {"code": True}), " — A set for O(1) membership testing. Using a set (not a list) avoids ambiguity: negative numbers like \"-3\" are NOT in this set, so they're correctly treated as numbers."])),
    N.para(N.rich([("for token in tokens:", {"code": True}), " — Single left-to-right O(n) pass. Each token is processed exactly once."])),
    N.para(N.rich([("if token not in ops:", {"code": True}), " — Branch: this token is a number (possibly negative, possibly multi-digit). Covers all cases not handled by the operator set."])),
    N.para(N.rich([("stack.append(int(token))", {"code": True}), " — Convert string to int and push. The number waits here until a future operator consumes it."])),
    N.para(N.rich([("b = stack.pop()", {"code": True}), " — Token is an operator. First pop = b = RIGHT operand (most recently pushed). This is the top of the stack."])),
    N.para(N.rich([("a = stack.pop()", {"code": True}), " — Second pop = a = LEFT operand. Critical: for '6 2 -' this gives a=6, b=2, computing 6-2=4 (correct), not 2-6=-4 (wrong)."])),
    N.para(N.rich([("stack.append(int(a / b))", {"code": True}), " — Division uses int(a/b), NOT a//b. Python's // floors toward -infinity; int() truncates toward zero. Only differs for negative results: int(-7/2)=-3, but -7//2=-4."])),
    N.para(N.rich([("return stack.pop()", {"code": True}), " — A valid RPN expression always leaves exactly one value on the stack. This invariant is guaranteed by the structure of valid postfix expressions."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Dispatch Table (Elegant Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same core idea as Solution 1, but instead of a series of if/elif branches, we pre-build a dictionary mapping each operator string to a Python function. This is the 'dispatch table' pattern."),
        N.h4("What Doesn't Work"),
        N.para("The elif chain in Solution 1 works but is verbose. If we needed to add more operators (e.g., '^' for exponentiation), we'd need to add another elif. A dispatch table scales cleanly."),
        N.h4("The Key Observation"),
        N.para("Python functions are first-class objects — we can store them in a dict. operator.add, operator.sub, operator.mul are built-in; division needs a lambda wrapper for the int() truncation."),
        N.h4("Building the Solution"),
        N.para("Build a dict {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': lambda a,b: int(a/b)}. Then the main loop becomes: if token in DISPATCH, pop b and a, call DISPATCH[token](a, b), push result."),
    ]),
    N.h3("Code"),
    N.code("""import operator

def evalRPN(tokens: list[str]) -> int:
    DISPATCH = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': lambda a, b: int(a / b),   # truncate toward zero
    }
    stack = []
    for t in tokens:
        if t in DISPATCH:
            b, a = stack.pop(), stack.pop()  # b=right (top), a=left (second)
            stack.append(DISPATCH[t](a, b))
        else:
            stack.append(int(t))
    return stack[-1]   # or stack.pop() — equivalent"""),
    N.h3("Line by Line"),
    N.para(N.rich([("DISPATCH = {...}", {"code": True}), " — Maps each operator string to a callable. operator.add(a,b) = a+b. Division uses a lambda since we need int() wrapping."])),
    N.para(N.rich([("b, a = stack.pop(), stack.pop()", {"code": True}), " — Python evaluates right-to-left in tuple unpacking, so b gets the first pop (top/right) and a gets the second pop (left). Clean one-liner."])),
    N.para(N.rich([("stack.append(DISPATCH[t](a, b))", {"code": True}), " — Calls the function with a=left, b=right. The dispatch table eliminates the if/elif chain entirely."])),
    N.para(N.rich([("return stack[-1]", {"code": True}), " — Reads the top without removing it. Equivalent to stack.pop() when we don't need the stack afterward."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Operand Stack (S1)", "O(n)", "O(n)"],
        ["Dispatch Table (S2)", "O(n)", "O(n)"],
    ]),
    N.para("Both solutions make a single pass (O(n)) with O(1) per token operation. Space is O(n) in the worst case — all tokens are numbers, none consumed. In realistic balanced expressions, the stack stays proportional to the depth of the expression tree."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks (Stack/Queue Sub-patterns)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Operand/Operator — also known as Expression Evaluation. Numbers are operands that accumulate on the stack; operators consume the top two operands and push a result."])),
    N.callout(
        "When to recognize this pattern: (1) 'evaluate expression' + token array, (2) operator acts on the two most recently seen unused numbers, (3) parentheses/delimiter matching with deferral, (4) any LIFO consume-on-trigger pattern.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Stack Operand/Operator technique:"),
    N.bullet(N.rich([("Basic Calculator", {"bold": True}), " (Hard) — Infix expression with +, −, (, ); two-stack or recursive descent approach. LeetCode #224."])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), " (Medium) — Infix with +, −, *, / and no parentheses; stack with operator precedence handling. LeetCode #227."])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Foundational stack problem: push openers, pop on closer match. LeetCode #20."])),
    N.bullet(N.rich([("Decode String", {"bold": True}), " (Medium) — Nested 'k[encoded_string]' parsing; stack defers partial strings. LeetCode #394."])),
    N.bullet(N.rich([("Asteroid Collision", {"bold": True}), " (Medium) — Stack models pairwise asteroid consumption — same 'top element consumed by trigger' mechanic. LeetCode #735."])),
    N.bullet(N.rich([("Mini-Parser", {"bold": True}), " (Medium) — Nested list parsing with a stack of in-progress NestedIntegers. LeetCode #385."])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String II", {"bold": True}), " (Medium) — Stack of (char, count) pairs; same defer-and-trigger pattern. LeetCode #1209."])),
    N.para("These problems share the core technique: use a stack to defer values and consume/combine them when a trigger token (operator, closer, etc.) arrives."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Section: Stack Operand/Operator (Expression Evaluation)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch the stack grow and shrink, see pop order highlighted, and follow the code panel line-by-line.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
