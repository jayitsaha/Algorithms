"""
gen_minimum_remove_to_make_valid_parentheses.py
Notion in-place update for LeetCode #1249 — Minimum Remove to Make Valid Parentheses
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8195-8ff3-f3c17b0f4d4e"

# ─── 1) Set properties ────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1249,
    pattern="Stacks",
    subpatterns=["Stack Index Tracking"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Track indices (not chars) of unmatched '(' on a stack; unmatched ')' detected immediately; leftover stack = unmatched '('; skip both in output.",
    icon="🟡"
)
print("Properties set.")

# ─── 2) Wipe old body ─────────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ─── 3) Build body ────────────────────────────────────────────────────────────
blocks = []

# === PROBLEM ===
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" of ", {}),
        ("(", {"code": True}),
        (" , ", {}),
        (")", {"code": True}),
        (" and lowercase letters, remove the minimum number of parentheses — ( or ) — so that the resulting string is valid. Return ", {}),
        ("any", {"bold": True}),
        (" valid result. A string is valid if every '(' has a matching ')' to its right and every ')' has a matching '(' to its left.", {}),
    ])),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ('"lee(t(c)ode)"', {"code": True}),
            (' → ', {}),
            ('"lee(t(c)ode)"', {"code": True}),
            (' (already valid). ', {}),
            ('"a(b)c)d("', {"code": True}),
            (' → ', {}),
            ('"a(b)cd"', {"code": True}),
            (' (removed unmatched ) at idx 5 and ( at idx 7).', {}),
        ]),
        "📝", "gray_background"
    ),
    N.divider(),
]

# === SOLUTION 1 — Stack Index Tracking (Interview Pick) ===
blocks += [
    N.h2("Solution 1 — Stack Index Tracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to identify and remove two kinds of 'bad' parentheses: (1) a ')' that arrives when no '(' is open before it — immediately detectable. (2) a '(' that never finds a closing ')' — only known after scanning the whole string. Everything else (letters + matched pairs) stays."),
        N.h4("What Doesn't Work"),
        N.para("Counting unmatched parens tells you how many to remove but not which ones. In '((a)', removing the first or second '(' both give valid results. To build the output string, you need the specific positions — so counting alone is insufficient."),
        N.h4("The Key Observation"),
        N.para("Store indices on the stack, not characters. When we push '(' we push its index. When we pop (match found), both positions are kept. At the end, stack contains exactly the indices of unmatched '(' — these, plus any unmatched ')' collected during the scan, form the complete remove set."),
        N.h4("Building the Solution"),
        N.para("1) stack=[], remove=set(). 2) Scan: '(' → push index; ')' → if stack non-empty pop (match), else add index to remove. 3) remove.update(stack) for leftover unmatched '('. 4) Build output skipping indices in remove."),
        N.callout("Analogy: Imagine you're sorting mail. Each '(' is a letter waiting for a reply (')'). You pile them in a stack (LIFO — newest on top). Each ')' either replies to the top of the pile (pop) or gets marked 'undeliverable' (no sender). Anything still in the pile at the end was never replied to.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minRemoveToMakeValid(s: str) -> str:\n"
        "    stack = []      # indices of unmatched '('\n"
        "    remove = set()  # indices to delete from output\n"
        "\n"
        "    for i, c in enumerate(s):\n"
        "        if c == '(':\n"
        "            stack.append(i)   # push index, not char\n"
        "        elif c == ')':\n"
        "            if stack:\n"
        "                stack.pop()   # matched! keep both chars\n"
        "            else:\n"
        "                remove.add(i) # unmatched ')'\n"
        "\n"
        "    remove.update(stack)  # leftover = unmatched '('\n"
        "\n"
        "    return ''.join(\n"
        "        c for i, c in enumerate(s)\n"
        "        if i not in remove   # O(1) set lookup\n"
        "    )\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Stack to hold indices of opening parens that haven't been matched yet. We store the index (integer), not the character itself, because we need positions to skip during output construction."])),
    N.para(N.rich([("remove = set()", {"code": True}), " — Set of character indices to delete. Using a set (not list) because we check ", ("i not in remove", {"code": True}), " for every index at the end — O(1) per lookup vs O(n) for a list."])),
    N.para(N.rich([("for i, c in enumerate(s):", {"code": True}), " — Process each character with its positional index. Letters are ignored (they always survive). Only '(' and ')' trigger stack operations."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — When we see '(' at position i, push i. This paren is tentatively unmatched — it's waiting for a partner that may come later."])),
    N.para(N.rich([("if stack: stack.pop()", {"code": True}), " — When we see ')' and the stack is non-empty, pop. The '(' whose index was on top is now matched with this ')'. Both survive into the result."])),
    N.para(N.rich([("remove.add(i)", {"code": True}), " — When we see ')' and the stack is empty, there's no available '(' to match. This ')' is unmatched — mark its index for deletion."])),
    N.para(N.rich([("remove.update(stack)", {"code": True}), " — After the scan, any index remaining in the stack is an unmatched '(' (found no closing partner in the whole string). Add all of them to remove."])),
    N.para(N.rich([("''.join(... if i not in remove)", {"code": True}), " — Build the output: one pass through the string, including only characters whose index is not in the remove set."])),
    N.divider(),
]

# === SOLUTION 2 — Two-Pass Counter ===
blocks += [
    N.h2("Solution 2 — Two-Pass Counter"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we avoid the explicit index-tracking stack and set? Yes — if we handle each type of invalid paren in a separate pass."),
        N.h4("The Key Observation"),
        N.para("Pass 1 left-to-right removes unmatched ')': greedily keep ')' only when there's a pending '(' (tracked by a counter). After pass 1, open_count holds the count of unmatched '('. Pass 2 right-to-left skips exactly open_count '(' characters (the rightmost ones, which had no close)."),
        N.h4("Building the Solution"),
        N.para("Pass 1: scan left-to-right, keep '(' always, keep ')' only if open_count > 0 (decrement count), skip excess ')'. Pass 2: scan result right-to-left, keep everything but skip open_count '(' chars (decrement each time). Reverse to restore order."),
    ]),
    N.h3("Code"),
    N.code(
        "def minRemoveToMakeValid(s: str) -> str:\n"
        "    # Pass 1: remove unmatched ')' left-to-right\n"
        "    open_cnt = 0\n"
        "    res = []\n"
        "    for c in s:\n"
        "        if c == '(':\n"
        "            open_cnt += 1\n"
        "            res.append(c)\n"
        "        elif c == ')':\n"
        "            if open_cnt:\n"
        "                open_cnt -= 1\n"
        "                res.append(c)  # matched\n"
        "            # else: unmatched ')' — skip\n"
        "        else:\n"
        "            res.append(c)\n"
        "\n"
        "    # Pass 2: remove open_cnt unmatched '(' right-to-left\n"
        "    ans = []\n"
        "    for c in reversed(res):\n"
        "        if c == '(' and open_cnt > 0:\n"
        "            open_cnt -= 1  # skip this unmatched '('\n"
        "        else:\n"
        "            ans.append(c)\n"
        "\n"
        "    return ''.join(reversed(ans))\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("open_cnt", {"code": True}), " — Counter of pending (unmatched) '(' seen so far in pass 1. When we see ')' and open_cnt > 0, we match them (decrement). When open_cnt == 0, the ')' is unmatched — skip it."])),
    N.para(N.rich([("Pass 2 reversed", {"code": True}), " — After pass 1, open_cnt still holds the count of unmatched '('. Scanning reversed, we skip the first open_cnt '(' we encounter — these are the rightmost unmatched ones (they had no close to their right). Everything else is kept."])),
    N.callout("This approach uses O(1) extra space for counting (beyond the output arrays) and avoids a stack/set entirely. The trade-off: slightly harder to reason about correctness. Solution 1 is clearer for interviews.", "⚡", "yellow_background"),
    N.divider(),
]

# === COMPLEXITY ===
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Stack Index Tracking", "O(n)", "O(n)", "Stack + set, each at most n entries"],
        ["Two-Pass Counter", "O(n)", "O(n)", "Output arrays; no stack/set overhead"],
    ]),
    N.divider(),
]

# === PATTERN CLASSIFICATION ===
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Index Tracking (Parentheses Matching variant)"])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('"make valid parentheses" + need to produce a modified string (not just count) → store indices on stack. '
             '"minimum removal" or "minimum addition" for brackets → balance counting with a stack. '
             'Any time you need LIFO matching of nested bracket characters.', {})
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# === RELATED PROBLEMS ===
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Stack / Parentheses Matching):"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Validate only (no removal); the classic stack-matching template (#20)"])),
    N.bullet(N.rich([("Minimum Add to Make Parentheses Valid", {"bold": True}), " (Medium) — Count how many brackets to INSERT for validity; same balance logic (#921)"])),
    N.bullet(N.rich([("Remove Invalid Parentheses", {"bold": True}), " (Hard) — Find ALL minimum-removal results; uses BFS over possible removal subsets (#301)"])),
    N.bullet(N.rich([("Longest Valid Parentheses", {"bold": True}), " (Hard) — Stack of indices to find the longest valid substring (#32)"])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), " (Medium) — Stack accumulates nested scores as brackets close (#856)"])),
    N.bullet(N.rich([("Check if a Parentheses String Can Be Valid", {"bold": True}), " (Medium) — Greedy two-pass with locked positions (#2116)"])),
    N.para("These problems all rely on the core insight that a stack naturally models the LIFO nesting structure of parentheses."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Stack/Queue) → Parentheses Matching. Sub-Pattern verified: Stack Index Tracking.", "📚", "gray_background"),
]

# === EMBED ===
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_remove_to_make_valid_parentheses")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ─── 4) Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
