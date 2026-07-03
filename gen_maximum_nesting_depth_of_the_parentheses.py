"""
gen_maximum_nesting_depth_of_the_parentheses.py
Regenerate the Notion page for LC #1614 in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81f2-ab50-fb19770ccd8a"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1614,
    pattern="Stacks",
    subpatterns=["Track Max Open Count"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Replace an explicit stack with a single integer counter; the stack's size IS the nesting depth.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a valid parenthesization string ", {}),
        ("s", {"code": True}),
        (", return the maximum nesting depth of its parentheses. "
         "The nesting depth is the maximum number of open brackets that are simultaneously open "
         "at any point while reading the string left-to-right.", {})
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('s = "(1+(2*3)+((8)/4))+1"', {"code": True}),
        (" → output ", {}),
        ("3", {"code": True}),
        (". The deepest nesting is the inner ", {}),
        ("((8)/4)", {"code": True}),
        (" group which reaches depth 3.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Counter (Interview Pick) ─────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Open Counter (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the maximum number of open parentheses active simultaneously. "
               "Think of it as: scan left-to-right, count how many '(' you have opened but not yet closed. "
               "The peak value of that running count is the answer."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach might count all '(' and all ')' independently and compare — "
               "but that gives the total, not the maximum simultaneous depth. "
               "Adjacent groups like '()()' each contribute depth 1 individually, not 2 total."),
        N.h4("The Key Observation"),
        N.para("The stack used in classic parentheses matching stores individual '(' characters "
               "— but they are ALL identical. We never inspect a specific element; we only check "
               "the stack's length. So the stack can be replaced by a single integer counter that "
               "tracks the same length. This reduces space from O(n) to O(1)."),
        N.h4("Building the Solution"),
        N.para("Initialize open = 0 and max_open = 0. "
               "For each character: on '(', increment open FIRST (depth increases at this bracket), "
               "then update max_open = max(max_open, open). "
               "On ')', decrement open (closing cannot create a new max). "
               "Return max_open."),
        N.callout(
            "Analogy: An elevator floor counter. '(' = go up, ')' = go down. "
            "Ask: what is the highest floor ever reached? "
            "You only need to track 'current floor' and 'highest floor seen' — no memory of every floor change.",
            "🏢", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def maxDepth(s: str) -> int:\n"
        "    open = 0        # running count of unmatched open brackets\n"
        "    max_open = 0    # peak depth seen — this is our answer\n"
        "    for c in s:\n"
        "        if c == '(':           # new open bracket\n"
        "            open += 1          # increment FIRST: depth is now the new value\n"
        "            max_open = max(max_open, open)  # then check for new peak\n"
        "        elif c == ')':         # matching close bracket\n"
        "            open -= 1          # strictly less than before — can't be a new max\n"
        "    return max_open            # peak depth across the entire string"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("open = 0", {"code": True}), (" — running count of unmatched open brackets; starts at zero since nothing is open yet.", {})])),
    N.para(N.rich([("max_open = 0", {"code": True}), (" — tracks the peak value of open across all steps; this is our final answer.", {})])),
    N.para(N.rich([("for c in s:", {"code": True}), (" — single left-to-right pass over every character; O(n) total.", {})])),
    N.para(N.rich([("if c == '(':", {"code": True}), (" — only act on open brackets. Digits, operators, letters are skipped.", {})])),
    N.para(N.rich([("open += 1", {"code": True}), (" — depth increases. We increment BEFORE updating max so we capture the new (higher) depth.", {})])),
    N.para(N.rich([("max_open = max(max_open, open)", {"code": True}), (" — after incrementing, check if the new depth exceeds the previous peak.", {})])),
    N.para(N.rich([("elif c == ')':", {"code": True}), (" — only act on close brackets. Using elif (not else) is safer for strings with other characters.", {})])),
    N.para(N.rich([("open -= 1", {"code": True}), (" — depth decreases. A close bracket can never produce a new maximum, so no max update.", {})])),
    N.para(N.rich([("return max_open", {"code": True}), (" — the maximum simultaneous open count encountered; equals the maximum nesting depth.", {})])),
    N.divider(),
]

# ── Solution 2 — Boolean Arithmetic ───────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Boolean Arithmetic (Pythonic)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same as Solution 1, but expressed more compactly using Python's bool-to-int coercion."),
        N.h4("Key Observation"),
        N.para("In Python, (c == '(') evaluates to 1 if True, 0 if False. "
               "So (c == '(') - (c == ')') gives +1 for '(', -1 for ')', 0 for everything else — "
               "exactly the delta we need to apply each step."),
        N.h4("Building the Solution"),
        N.para("Combine the update into one line: depth += (c == '(') - (c == ')'), "
               "then ans = max(ans, depth). "
               "Note: taking max after ')', depth is already lower — no new peak possible — so this is still correct."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxDepth(s: str) -> int:\n"
        "    depth, ans = 0, 0\n"
        "    for c in s:\n"
        "        depth += (c == '(') - (c == ')')  # +1, -1, or 0\n"
        "        ans = max(ans, depth)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("depth += (c == '(') - (c == ')')", {"code": True}),
                   (" — one expression handles all three cases: open bracket (+1), close bracket (-1), other (0).", {})])),
    N.para(N.rich([("ans = max(ans, depth)", {"code": True}),
                   (" — safe to call after every character. After ')', depth is lower so no new peak. After other chars, depth is unchanged.", {})])),
    N.divider(),
]

# ── Solution 3 — Explicit Stack ────────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Explicit Stack (Brute Force / Interview Starting Point)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Use the classic parentheses matching pattern: push on '(', pop on ')'. "
               "The stack's length at any moment equals the current nesting depth."),
        N.h4("What Doesn't Work (for space)"),
        N.para("This approach is O(n) space — in the worst case s = '((((...)))))' the stack grows to n/2 elements. "
               "Not ideal when O(1) space is achievable."),
        N.h4("Key Observation"),
        N.para("Every element pushed onto the stack is identical: just '('. "
               "We only ever check len(stack), never inspect individual elements. "
               "This is the realization that unlocks the O(1) counter optimization."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxDepth(s: str) -> int:\n"
        "    stack, max_depth = [], 0\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            stack.append('(')  # push\n"
        "            max_depth = max(max_depth, len(stack))  # length = current depth\n"
        "        elif c == ')':\n"
        "            stack.pop()        # pop matching open bracket\n"
        "    return max_depth"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Explicit Stack", "O(n)", "O(n)"],
        ["Counter (Optimal) ✓", "O(n)", "O(1)"],
        ["Boolean Arithmetic", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Track Max Open Count (related: Parentheses Matching)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "• Problem asks for maximum 'nesting depth', 'level', or 'simultaneously open' count. "
        "• A stack solution is obvious, but every pushed element is identical (only the count matters). "
        "• Paired open/close tokens with incrementally changing depth. "
        "• 'Remove brackets to limit depth to k' — greedy scan with depth tracking.",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("'Track Max Open Count' is a refinement of Parentheses Matching not explicitly listed in the guide. "
         "The core insight — replacing a stack of identical elements with an integer — is the distinguishing technique.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (stack → counter, or depth tracking with parentheses):"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Classic stack matching; check if every bracket has a valid partner (#20)", {})])),
    N.bullet(N.rich([("Remove Outermost Parentheses", {"bold": True}), (" (Easy) — Track open count; omit characters at depth 0 and the outermost close (#1021)", {})])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), (" (Medium) — Depth-based scoring; value doubles with each nesting level (#856)", {})])),
    N.bullet(N.rich([("Minimum Add to Make Parentheses Valid", {"bold": True}), (" (Medium) — Track open imbalance and unmatched close with two counters (#921)", {})])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), (" (Medium) — Stack of unmatched indices; remove them at the end (#1249)", {})])),
    N.bullet(N.rich([("Check if a Parentheses String Can Be Valid", {"bold": True}), (" (Medium) — Range of possible depths with wildcard characters (#2116)", {})])),
    N.bullet(N.rich([("Longest Valid Parentheses", {"bold": True}), (" (Hard) — Unmatched bracket positions bound valid windows; hardest extension of this family (#32)", {})])),
    N.para("These problems share the core technique: scanning parentheses left-to-right with a running counter (or stack) tracking depth or balance."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stacks/Queues → Parentheses Matching. "
              "Sub-pattern 'Track Max Open Count' is classified here from analysis as a space-optimized specialization.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_nesting_depth_of_the_parentheses")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
