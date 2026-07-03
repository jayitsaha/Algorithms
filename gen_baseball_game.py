"""
gen_baseball_game.py — Notion update for Baseball Game (LC #682)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81db-be88-ce8f08bc8281"

# ── 1) Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=682,
    pattern="Stacks",
    subpatterns=["Stack Simulation"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Map each operation (int/+/D/C) to a stack push or pop; the stack maintains the valid score record at every step.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are keeping score for a baseball game with a peculiar ruleset. "
         "You are given a list of strings "),
        ("operations", {"code": True}),
        (", where "),
        ("operations[i]", {"code": True}),
        (" is the ith operation you must apply to the record of scores. "
         "Return the sum of all the scores on the record after applying all the operations.\n\n"
         "The four operations:\n"
         "• Integer string (e.g. \"5\") — Push that integer as a new valid score.\n"
         "• \"+\" — Push the sum of the previous two valid scores.\n"
         "• \"D\" — Push double the previous valid score.\n"
         "• \"C\" — Remove (invalidate) the previous valid score.\n\n"
         "Constraints: 1 ≤ operations.length ≤ 1000. Input is always valid (enough entries exist for + and D)."),
    ])),
    N.divider(),
]

# ── Solution 1 (Interview Pick) ──────────────────────────────────────
sol1_code = '''def calPoints(operations: list[str]) -> int:
    record = []                          # stack = valid score history
    for op in operations:
        if op == '+':
            record.append(record[-1] + record[-2])   # sum of last two
        elif op == 'D':
            record.append(record[-1] * 2)             # double the last
        elif op == 'C':
            record.pop()                              # cancel the last
        else:
            record.append(int(op))                   # real score
    return sum(record)                   # total of all valid scores'''

blocks += [
    N.h2("Solution 1 — Stack Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to maintain a mutable history of valid scores, applying four different "
            "rules that always reference the most recently added scores. Reframed: "
            "'build and maintain a list where we can quickly access, add to, and remove from the end.'"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive approach might store all ops and replay them, or use a plain variable. "
            "But '+' needs the last TWO valid scores and 'C' must remove the last one — "
            "a simple variable can't hold this history. An array with random indexing is overkill; "
            "we only ever need the tail."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Every operation ('+', 'D', 'C') refers exclusively to the MOST RECENT entries in the record. "
            "This is the definition of LIFO (Last-In, First-Out) access — exactly what a stack provides. "
            "Each operation maps 1-to-1 to a stack action: integer → push, '+' → read two + push, "
            "'D' → read one + push, 'C' → pop."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Use a list as a stack (record = []).\n"
            "Step 2: For each op:\n"
            "  - Integer string → int(op) and push\n"
            "  - '+' → record[-1] + record[-2], push result\n"
            "  - 'D' → record[-1] * 2, push result\n"
            "  - 'C' → record.pop()\n"
            "Step 3: return sum(record)\n\n"
            "Trace: ops=['5','2','C','D','+']\n"
            "  '5' → push 5 → [5]\n"
            "  '2' → push 2 → [5,2]\n"
            "  'C' → pop   → [5]\n"
            "  'D' → push 10→ [5,10]\n"
            "  '+' → push 15→ [5,10,15]\n"
            "  sum = 30 ✓"
        ),
        N.callout(
            "Analogy: Think of the record as a notepad. Each round you either write a new number, "
            "erase the last number (C), write double the last (D), or write the sum of the last two (+). "
            "At the end, add up everything still on the notepad.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("record = []", {"code": True}), " — Initialize an empty list that serves as our stack of valid scores."])),
    N.para(N.rich([("for op in operations:", {"code": True}), " — Process each operation string left to right in order."])),
    N.para(N.rich([("if op == '+':", {"code": True}), " — Check for the sum operation first."])),
    N.para(N.rich([("record.append(record[-1] + record[-2])", {"code": True}), " — Push the sum of the top two entries. record[-1] is the most recent, record[-2] is one below. Both guaranteed to exist."])),
    N.para(N.rich([("elif op == 'D':", {"code": True}), " — Check for the double operation."])),
    N.para(N.rich([("record.append(record[-1] * 2)", {"code": True}), " — Read the top entry, multiply by 2, push the result as a new valid score."])),
    N.para(N.rich([("elif op == 'C':", {"code": True}), " — Check for the cancel operation."])),
    N.para(N.rich([("record.pop()", {"code": True}), " — Remove the most recent valid score from the record. O(1) from list end."])),
    N.para(N.rich([("else:", {"code": True}), " — If not '+', 'D', or 'C', the operation must be an integer string (e.g. '5' or '-3')."])),
    N.para(N.rich([("record.append(int(op))", {"code": True}), " — Convert the string to an integer and push it as a new valid score."])),
    N.para(N.rich([("return sum(record)", {"code": True}), " — Sum all remaining valid scores in the record. This is O(n) but we're already O(n) overall."])),
    N.divider(),
]

# ── Solution 2 ───────────────────────────────────────────────────────
sol2_code = '''def calPoints(operations: list[str]) -> int:
    record = []
    for op in operations:
        if op[0].lstrip("-").isdigit():      # defensive numeric check
            record.append(int(op))
        elif op == "+" and len(record) >= 2:
            record.append(record[-1] + record[-2])
        elif op == "D" and len(record) >= 1:
            record.append(record[-1] * 2)
        elif op == "C" and len(record) >= 1:
            record.pop()
    return sum(record)'''

blocks += [
    N.h2("Solution 2 — Defensive Stack Simulation"),
    N.toggle_h3("💡 Intuition: Defensive Variant", [
        N.h4("Reframe the Problem"),
        N.para("Same as Solution 1, but adds guard conditions to handle potentially invalid input gracefully."),
        N.h4("What Doesn't Work"),
        N.para("In LeetCode, the input is guaranteed valid so guards are unnecessary. But in production code with unvalidated input, record[-1] or record[-2] can throw IndexError."),
        N.h4("The Key Observation"),
        N.para("Add len checks before + and D, and an isdigit check for the integer branch. The logic is identical to Solution 1 — only the error handling differs."),
        N.h4("Building the Solution"),
        N.para("Use op[0].lstrip('-').isdigit() to detect numeric strings (handles negatives like '-3'). Add len(record) >= 2 guard for +, len >= 1 for D and C. Everything else is the same."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("op[0].lstrip('-').isdigit()", {"code": True}), " — Strips a leading minus sign before checking if the string is a digit. This correctly identifies '-3' as an integer string."])),
    N.para(N.rich([("len(record) >= 2", {"code": True}), " — Guard for '+': ensures at least two entries exist before accessing record[-1] and record[-2]."])),
    N.para(N.rich([("len(record) >= 1", {"code": True}), " — Guard for 'D' and 'C': ensures stack is not empty before accessing or popping."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Stack Simulation (Interview Pick)", "O(n)", "O(n)"],
        ["Defensive Stack Simulation", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks (Stack/Queue patterns — see DSA guide section on stacks)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Simulation — directly model the problem's operations as push/pop on a stack"])),
    N.callout(
        "When to recognize Stack Simulation:\n"
        "• Operations refer to 'the last valid result' or 'the most recent entry'\n"
        "• 'Undo' / 'cancel' the previous action\n"
        "• Each step modifies a running history, not just a running total\n"
        "• Parentheses, bracket matching, expression evaluation",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Stack Simulation technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Push open brackets, pop on matching close; LIFO 'most recent unmatched' tracking (#20)"])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates In String", {"bold": True}), " (Easy) — Push chars, pop when top matches current char; identical stack simulation (#1047)"])),
    N.bullet(N.rich([("Evaluate Reverse Polish Notation", {"bold": True}), " (Medium) — Push operands; on operator, pop two, compute, push result — same 'operate on top' pattern (#150)"])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), " (Medium) — Use stack to handle operator precedence with + − × ÷ (#227)"])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), " (Medium) — Maintain a stack with O(1) minimum retrieval — augmenting the stack invariant (#155)"])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), " (Medium) — Stack-based scoring of nested brackets; similar scoring semantics (#856)"])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Monotonic stack variant; still pushing/popping based on relationships (#739)"])),
    N.para("These problems share the same core technique: use a stack to maintain a running history where recent elements define future computations."),
    N.callout("📚 Reference: Stack Simulation is a sub-pattern of Stack/Queue patterns. See DSA_Patterns_and_SubPatterns_Guide.md Stack section.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("baseball_game")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append ───────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
