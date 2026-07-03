"""
gen_valid_parentheses.py — Notion page for Valid Parentheses (LC #20).
notion_page_id = null → create a new page.
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 0: Create page (notion_page_id was null) ──────────────────────────
PAGE_ID = N.create_page("Valid Parentheses", 20, "Easy", "🟢")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=20,
    pattern="Stacks",
    subpatterns=["Parentheses Matching"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push open brackets onto a stack; each close bracket must match the stack top — order enforces nesting.",
    icon="🟢"
)
print("Properties set.")

# ── Step 2: Build body blocks ──────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. "
         "An input string is valid if: (1) open brackets are closed by the same type of bracket, "
         "(2) open brackets are closed in the correct order, and (3) every close bracket has a corresponding open bracket.", {})
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Stack + Hash Map with Sentinel (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to verify that brackets are both type-matched and order-matched (nested correctly). The key constraint is that the most recently opened bracket must be the first to close — the innermost pair closes before outer pairs."),
        N.h4("What Doesn't Work"),
        N.para("Counting bracket types: track count of '(' and ')', '[' and ']', '{' and '}' and verify equal totals. This fails for '([)]' — counts balance (1 each type), but the ORDER is wrong. We lose positional information when we only count."),
        N.h4("The Key Observation"),
        N.para("The rule 'innermost must close first' is Last-In First-Out (LIFO). If we imagine each open bracket as entering a waiting room, the most recently arrived one must leave first. That's exactly a stack."),
        N.h4("Building the Solution"),
        N.para("1. Build a map: close bracket → expected open partner ({')': '(', ']': '[', '}': '{'}). "
               "2. Scan left to right. If c is an open bracket, push it. If c is a close bracket, pop the top and check it equals matching[c]. Empty stack when we need to pop → fail. At the end, empty stack → valid."),
        N.callout(
            "Analogy: Think of the stack as a 'nesting depth counter with memory.' Each open bracket starts a new level; the close bracket must end exactly the level that is currently open — not any deeper level.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isValid(s: str) -> bool:\n"
        "    matching = {')': '(', ']': '[', '}': '{'}\n"
        "    stack = []\n"
        "    for c in s:\n"
        "        if c in matching:\n"
        "            top = stack.pop() if stack else '#'\n"
        "            if top != matching[c]:\n"
        "                return False\n"
        "        else:\n"
        "            stack.append(c)\n"
        "    return not stack"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("matching = {')': '(', ']': '[', '}': '{'}", {"code": True}), " — Dictionary mapping every close bracket to the exact open bracket it must be paired with. Three keys = three close bracket types. This makes the partnership lookup O(1)."])),
    N.para(N.rich([("stack = []", {"code": True}), " — Empty stack to hold unmatched open brackets. Think of it as 'open brackets waiting for their close partner.'"])),
    N.para(N.rich([("for c in s:", {"code": True}), " — Single left-to-right scan, O(n) iterations total."])),
    N.para(N.rich([("if c in matching:", {"code": True}), " — True iff c is a close bracket (one of ')', ']', '}'). The dict keys are exactly the close brackets."])),
    N.para(N.rich([("top = stack.pop() if stack else '#'", {"code": True}), " — Pop the most recent open bracket. If stack is empty, use sentinel '#' which can never equal any valid open bracket."])),
    N.para(N.rich([("if top != matching[c]:", {"code": True}), " — The popped value must be the correct open partner. '#' also fails here (empty stack case). Both wrong-type and empty-stack failures handled in one branch."])),
    N.para(N.rich([("return False", {"code": True}), " — Mismatch found; no way to salvage the string. Fail early."])),
    N.para(N.rich([("stack.append(c)", {"code": True}), " — c is an open bracket. Push it; a future close bracket will claim it."])),
    N.para(N.rich([("return not stack", {"code": True}), " — If the stack is empty, every open was matched. If not, there are unmatched opens → invalid. 'not []' = True; 'not [\"(\"]' = False."])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Stack with Explicit Guard (Beginner-Friendly)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same core idea — use a stack — but separate the empty-stack check from the mismatch check for clarity. More explicit control flow for readers still learning the pattern."),
        N.h4("What Doesn't Work"),
        N.para("Same as Solution 1: counting types loses order. This solution is a pedagogical variant of the same algorithm, not a different approach."),
        N.h4("The Key Observation"),
        N.para("By checking 'if not stack' separately before popping, we make the empty-stack failure explicit. Same result as the sentinel trick, but two distinct branches instead of one."),
        N.h4("Building the Solution"),
        N.para("Use 'if c in \"([{\"' to detect open brackets (avoids building the matching dict first). On close brackets, check not stack OR stack[-1] != pairs[c]. Then pop. Return stack == 0 at the end."),
        N.callout("Trade-off: more readable but slightly more verbose. In an interview, mention both variants and prefer the sentinel version for conciseness.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def isValid(s: str) -> bool:\n"
        "    stack = []\n"
        "    pairs = {')': '(', ']': '[', '}': '{'}\n"
        "    for c in s:\n"
        "        if c in '([{':\n"
        "            stack.append(c)\n"
        "        else:\n"
        "            if not stack or stack[-1] != pairs[c]:\n"
        "                return False\n"
        "            stack.pop()\n"
        "    return len(stack) == 0"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if c in '([{':", {"code": True}), " — Check if c is one of the three open bracket characters. No dict needed for this direction."])),
    N.para(N.rich([("if not stack or stack[-1] != pairs[c]:", {"code": True}), " — Two failure conditions: stack empty (nothing waiting) OR the top open bracket doesn't match this close bracket."])),
    N.para(N.rich([("stack.pop()", {"code": True}), " — We only reach here if the match was valid. Pop the matched open bracket."])),
    N.para(N.rich([("return len(stack) == 0", {"code": True}), " — Equivalent to 'return not stack'. More explicit for readers who might not know Python's truthiness rules for lists."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Stack + Sentinel (Solution 1)", "O(n)", "O(n)", "Interview pick; elegant empty-stack handling"],
        ["Stack + Explicit Guard (Solution 2)", "O(n)", "O(n)", "More readable for beginners"],
        ["Count types only (wrong)", "O(n)", "O(1)", "Incorrect — fails on ordering"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Parentheses Matching (Push Open, Match Close)"])),
    N.callout(
        "When to recognize this pattern: any problem with nested open/close delimiters where inner must close before outer; "
        "'correctly nested' or 'valid brackets' in the problem statement; multiple delimiter types that must match by type AND order.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Parentheses Matching / Stack technique:"),
]
related = [
    ("Generate Parentheses", "Medium", "Backtracking; build all valid combos with n pairs (#22)"),
    ("Longest Valid Parentheses", "Hard", "Stack + indices to find max length valid substring (#32)"),
    ("Min Add to Make Parentheses Valid", "Medium", "Two counters for unmatched opens and unmatched closes (#921)"),
    ("Min Remove to Make Parentheses Valid", "Medium", "Stack of indices; remove chars at invalid positions (#1249)"),
    ("Score of Parentheses", "Medium", "Stack tracking nesting depth to compute integer score (#856)"),
    ("Basic Calculator", "Hard", "Stack for expression evaluation with arbitrary parentheses (#224)"),
    ("Daily Temperatures", "Medium", "Monotonic stack — same push-and-verify-later principle (#739)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (f" — {note}", {})
    ])))

blocks += [
    N.para("These problems share the same core technique: use a stack to remember context in LIFO order and verify it against a later event."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section · Sub-Pattern: Parentheses Matching", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_parentheses")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
