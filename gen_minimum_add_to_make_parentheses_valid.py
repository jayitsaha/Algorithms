"""
gen_minimum_add_to_make_parentheses_valid.py
Notion page builder for LeetCode #921 — Minimum Add to Make Parentheses Valid.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81da-aa8e-ea7a9ff4892c"
SLUG = "minimum_add_to_make_parentheses_valid"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=921,
    pattern="Greedy",
    subpatterns=["Track Open/Close Needed"],
    tc="O(n)",
    sc="O(1)",
    key_insight="One forward scan: track unmatched '(' as open; each ')' either closes an open or increments a close counter.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ─────────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" of ", {}),
        ("'('", {"code": True}),
        (" and ", {}),
        ("')'", {"code": True}),
        (" characters, return the minimum number of parenthesis additions (either ", {}),
        ("'('", {"code": True}),
        (" or ", {}),
        ("')'", {"code": True}),
        (") needed to make the string valid. A valid string has every open paren matched by a close paren in the correct order.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('s = "())" ', {"code": True}),
        ("→ ", {}),
        ("1", {"code": True}),
        (" (need one ", {}),
        ("'('", {"code": True}),
        (' at the start)  |  s = "(((" ', {}),
        ("→ ", {}),
        ("3", {"code": True}),
        (" (need three ", {}),
        ("')'", {"code": True}),
        (" at the end)", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Greedy — One-Pass Counter (Interview Pick) ─────────────────
blocks += [
    N.h2("Solution 1 — Greedy: One-Pass Counter (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "A parenthesis string is valid when every '(' has a matching ')' that comes after it. "
            "At any point during a left-to-right scan, we're tracking a 'debt': how many open parens are waiting for their matching close."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A stack of characters works but uses O(n) space — we store every unmatched '(' on the stack. "
            "We can eliminate the stack entirely by observing that we only ever need to know HOW MANY unmatched '(' exist, not which specific ones."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Scan left to right. Maintain two counters:\n"
            "  • open = number of '(' seen that haven't yet been matched by a ')'\n"
            "  • close = number of ')' seen that had no preceding '(' to match\n\n"
            "When we see '(': open += 1 (new debt created).\n"
            "When we see ')': if open > 0, we match it (open -= 1); otherwise it's unmatched (close += 1).\n\n"
            "The answer is open + close — the total number of characters we need to insert."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize open = 0 (unmatched '(' count) and close = 0 (unmatched ')' count).\n"
            "2. For each character:\n"
            "   - '(' → open += 1\n"
            "   - ')' and open > 0 → open -= 1 (matched!)\n"
            "   - ')' and open == 0 → close += 1 (orphan close)\n"
            "3. Return open + close."
        ),
        N.callout(
            "Analogy: Think of 'open' as an IOU stack — each '(' is 'I owe you a close paren.' "
            "Each ')' either pays off an IOU (open > 0) or creates a reverse IOU (close += 1). "
            "The answer is total unpaid IOUs in both directions.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def minAddToMakeValid(s: str) -> int:\n"
        "    open_count = 0   # unmatched '(' needing a ')'\n"
        "    close_count = 0  # unmatched ')' needing a '('\n"
        "\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            open_count += 1  # new open paren — create debt\n"
        "        else:  # c == ')'\n"
        "            if open_count > 0:\n"
        "                open_count -= 1  # match it with an existing open\n"
        "            else:\n"
        "                close_count += 1  # no open to match — orphan close\n"
        "\n"
        "    return open_count + close_count  # total insertions needed"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("open_count = 0", {"code": True}), (" — Tracks how many '(' we've seen that still need a matching ')'. Each unmatched '(' will need one ')' inserted at the end.", {})])),
    N.para(N.rich([("close_count = 0", {"code": True}), (" — Tracks how many ')' we've encountered with no preceding '(' to match. Each will need a '(' inserted before it.", {})])),
    N.para(N.rich([("for c in s:", {"code": True}), (" — Single left-to-right pass through the string. O(n) time.", {})])),
    N.para(N.rich([("if c == '(':", {"code": True}), (" — Open paren: creates an obligation. We now owe one close paren.", {})])),
    N.para(N.rich([("open_count += 1", {"code": True}), (" — Increment our 'open debt' counter.", {})])),
    N.para(N.rich([("if open_count > 0: open_count -= 1", {"code": True}), (" — Close paren with a waiting open: they match. Cancel one debt. This is the greedy choice — always match the most recent open (like a stack, without the stack).", {})])),
    N.para(N.rich([("else: close_count += 1", {"code": True}), (" — Close paren with no waiting open: it's orphaned. We'll need to insert a '(' somewhere before this position.", {})])),
    N.para(N.rich([("return open_count + close_count", {"code": True}), (" — open_count '(' are stranded without closes; close_count ')' are stranded without opens. Total insertions needed is their sum.", {})])),
    N.divider(),
]

# ── Solution 2: Stack-Based ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Stack-Based (Educational)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "This is the textbook parenthesis-matching approach. Use a stack to track unmatched '(' characters. "
            "When we see ')', either pop a waiting '(' (match) or note an unmatched ')'."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try inserting parens at every position and check validity — O(2^n) approaches. "
            "Even checking validity naively is O(n) per check, making this completely impractical."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A stack naturally models the 'nesting' of parentheses. Each '(' pushed represents an open scope. "
            "Each ')' either closes the innermost scope (pop) or finds nothing to close (unmatched). "
            "The number of insertions = size of stack at end + number of unmatched ')'."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. stack = [] and unmatched_close = 0\n"
            "2. For each char:\n"
            "   - '(' → push to stack\n"
            "   - ')' and stack → pop\n"
            "   - ')' and stack empty → unmatched_close += 1\n"
            "3. Return len(stack) + unmatched_close"
        ),
        N.callout("Note: The stack solution and the counter solution are mathematically identical. The stack stores individual '(' chars, but we only ever care about the count — so we can replace the stack with a single integer.", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minAddToMakeValid(s: str) -> int:\n"
        "    stack = []           # store unmatched '('\n"
        "    unmatched_close = 0  # unmatched ')' count\n"
        "\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            stack.append('(')\n"
        "        elif stack:           # ')' with a waiting '('\n"
        "            stack.pop()\n"
        "        else:                 # ')' with no waiting '('\n"
        "            unmatched_close += 1\n"
        "\n"
        "    return len(stack) + unmatched_close"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), (" — Each element is an unmatched '(' waiting for its close. O(n) space in the worst case (e.g. s = '((((((').", {})])),
    N.para(N.rich([("stack.append('(')", {"code": True}), (" — Push open paren. We could store indices instead of chars, but just '(' suffices since all contents are the same.", {})])),
    N.para(N.rich([("elif stack: stack.pop()", {"code": True}), (" — Close paren matches the most recent open. The stack's LIFO order naturally handles nesting.", {})])),
    N.para(N.rich([("else: unmatched_close += 1", {"code": True}), (" — No open paren available. This ')' is orphaned and needs an inserted '(' before it.", {})])),
    N.para(N.rich([("return len(stack) + unmatched_close", {"code": True}), (" — Remaining stack elements are unmatched '(' (each needs a ')'); unmatched_close ')' each need a '('.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy (Counter)", "O(n)", "O(1)"],
        ["Stack-Based", "O(n)", "O(n)"],
    ]),
    N.para("Both solutions do a single pass. The greedy counter is strictly better on space: O(1) vs O(n) for the stack."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Greedy — at each step make the locally optimal decision (match ')' to an open '(' if possible, else count it as unmatched).", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Track Open/Close Needed — maintain two counters that measure 'debt' in each direction. The answer is the sum of both debts at the end.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Minimum insertions/deletions to make a string valid'\n"
        "• Parenthesis/bracket matching with a twist (not just yes/no but how many)\n"
        "• Single-character state can be summarized as a count (no need to track positions)\n"
        "• Problem involves balancing two opposing quantities (opens vs closes)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Is the string already valid? Stack-based matching, no insertions needed. (#20)", {})])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), (" (Medium) — Remove characters instead of adding them. Need positions, so stack stores indices. (#1249)", {})])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), (" (Medium) — Assign point values to parenthesis nesting. Same scan technique. (#856)", {})])),
    N.bullet(N.rich([("Check if a Parentheses String Can Be Valid", {"bold": True}), (" (Medium) — Some positions are locked; use greedy range scan. (#2116)", {})])),
    N.bullet(N.rich([("Minimum Number of Swaps to Make String Balanced", {"bold": True}), (" (Medium) — Swap parens instead of inserting. Same counter intuition. (#1963)", {})])),
    N.bullet(N.rich([("Longest Valid Parentheses", {"bold": True}), (" (Hard) — Find the longest valid substring. Stack with indices or two-pass counter. (#32)", {})])),
    N.bullet(N.rich([("Minimum Insertions to Balance a Parentheses String", {"bold": True}), (" (Medium) — Each ')' must be matched by two consecutive '(' — variant of this pattern. (#1541)", {})])),
    N.para("These problems share the core technique: scan once, track imbalance state as counters or a stack."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Greedy / Stack-Queue section. Sub-Pattern: Parentheses Matching / Track Open-Close Needed.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks: {len(blocks)}")
