"""gen_valid_parenthesis_string.py — Notion update for Valid Parenthesis String (#678)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cb-b5a7-d2ddbea97869"

# ── 1) Set page properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=678,
    pattern="Stacks",
    subpatterns=["Two Counters (Lo/Hi Range)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track range [lo,hi] of possible open-paren counts; '*' widens range; clamp lo≥0; fail if hi<0; return lo==0.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ──
print("Wiping old page content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build body blocks ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (" containing only the characters ", {}),
        ("'('", {"code": True}),
        (", ", {}),
        ("')'", {"code": True}),
        (" and ", {}),
        ("'*'", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if ", {}),
        ("s", {"code": True}),
        (" is valid. The following rules define a valid string: (1) Any left parenthesis ", {}),
        ("'('", {"code": True}),
        (" must have a corresponding right parenthesis ", {}),
        ("')'", {"code": True}),
        (". (2) Any right parenthesis ", {}),
        ("')'", {"code": True}),
        (" must have a corresponding left parenthesis ", {}),
        ("'('", {"code": True}),
        (". (3) Left parenthesis ", {}),
        ("'('", {"code": True}),
        (" must go before the corresponding right parenthesis ", {}),
        ("')'", {"code": True}),
        (". (4) ", {}),
        ("'*'", {"code": True}),
        (" could be treated as a single right parenthesis ", {}),
        ("')'", {"code": True}),
        (", or a single left parenthesis ", {}),
        ("'('", {"code": True}),
        (", or an empty string ", {}),
        ('""', {"code": True}),
        (".", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Lo/Hi Greedy (Interview Pick) ───
sol1_code = """\
def checkValidString(s: str) -> bool:
    lo = hi = 0              # lo = min possible opens, hi = max possible opens
    for c in s:
        if c == '(':
            lo += 1          # '(' always opens a paren (min and max both go up)
            hi += 1
        elif c == ')':
            lo -= 1          # ')' always closes a paren (min and max both go down)
            hi -= 1
        else:                # '*' is a wildcard — expands the range
            lo -= 1          # pessimistic: treat '*' as ')' → lower minimum
            hi += 1          # optimistic:  treat '*' as '(' → raise maximum
        if hi < 0:           # even best case is broken — too many ')'
            return False
        lo = max(lo, 0)      # open count can't logically go negative
    return lo == 0           # some assignment achieves exactly 0 unmatched opens
"""

blocks += [
    N.h2("Solution 1 — Lo/Hi Greedy Range (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The string is valid if you can assign each '*' to '(', ')' or '' such that the resulting pure-parentheses string is balanced. Instead of enumerating all 3^k assignments (exponential), ask: what is the set of possible unmatched open-paren counts reachable at position i?"),
        N.h4("What Doesn't Work"),
        N.para("A single counter works for plain parentheses strings: +1 for '(', -1 for ')'. With '*', we don't know which to do. Trying all assignments is O(3^n). Even DP on (index, open_count) is O(n^2). We need a way to represent the full uncertainty in O(1) space."),
        N.h4("The Key Observation"),
        N.para("At any prefix of the string, the set of achievable open-paren counts forms a contiguous range [lo, hi]. '(' shifts the entire range up by 1. ')' shifts it down by 1. '*' widens it: lo goes down by 1 (star used as ')'), hi goes up by 1 (star used as '('). We never need to track individual counts — just the endpoints of the range."),
        N.h4("Building the Solution"),
        N.para("Initialize lo = hi = 0. For each character, update lo and hi per the rules above. Two guard conditions: (1) clamp lo to 0 — it can never be negative because '*' can always be empty instead of ')'; (2) if hi < 0, the string is broken regardless — return False immediately. At the end, return lo == 0, meaning zero is in the reachable range."),
        N.callout("Analogy: Think of lo and hi as the narrowest and widest possible reading of the string. '(' is unambiguous — all readings shift up. '*' is ambiguous — the optimist reads it as '(', the pessimist as ')'. At the end, if the pessimist can read it as balanced (lo=0), we're done.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("lo = hi = 0", {"code": True}), " — Initialize both counters to 0. Before any character: exactly 0 unmatched opens in any scenario."])),
    N.para(N.rich([("if c == '(':", {"code": True}), " — A '(' is unambiguous. Every possible assignment adds one open paren. lo += 1, hi += 1."])),
    N.para(N.rich([("elif c == ')':", {"code": True}), " — A ')' is unambiguous. Every possible assignment closes one paren. lo -= 1, hi -= 1."])),
    N.para(N.rich([("else: lo -= 1; hi += 1", {"code": True}), " — A '*' can be ')' (pessimistic: lo-1), '(' (optimistic: hi+1), or '' (middle: no change). Net effect: range widens by 1 in each direction."])),
    N.para(N.rich([("if hi < 0: return False", {"code": True}), " — hi is the most optimistic open count. If even the best case is negative, ')' has no possible match anywhere — impossible to recover. Fail immediately."])),
    N.para(N.rich([("lo = max(lo, 0)", {"code": True}), " — Open count cannot be negative. When lo would go below 0, it means we're treating a '*' as ')' that closes a non-existent open — but we can use '' instead. Clamp to 0."])),
    N.para(N.rich([("return lo == 0", {"code": True}), " — lo == 0 means the most pessimistic valid assignment achieves exactly 0 unmatched opens. If lo > 0, every assignment has leftover opens — return False."])),
    N.divider(),
]

# ─── Solution 2: Two Stacks ───
sol2_code = """\
def checkValidString(s: str) -> bool:
    open_st = []   # indices of unmatched '('
    star_st = []   # indices of '*' (potential wildcards)

    for i, c in enumerate(s):
        if c == '(':
            open_st.append(i)
        elif c == '*':
            star_st.append(i)
        else:  # ')'
            # Prefer matching with nearest '(' (greedy)
            if open_st:
                open_st.pop()
            elif star_st:
                star_st.pop()  # use '*' as '(' to match this ')'
            else:
                return False   # no match possible

    # Match remaining '(' with '*' to their right
    while open_st and star_st:
        if open_st.pop() > star_st.pop():
            return False       # '*' must appear AFTER '(' to close it
    return not open_st         # any unmatched '(' remaining?
"""

blocks += [
    N.h2("Solution 2 — Two Stacks (O(n) Space, More Intuitive)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of matching parentheses as pairing up '(' and ')' tokens. A valid string requires every '(' to be paired with a later ')'. With '*', those wildcards can fill in as either token."),
        N.h4("What Doesn't Work"),
        N.para("If we greedily use '*' as '(' every time, we might over-commit and fail to close properly. If we use '*' as ')' every time, we might leave '(' unmatched. We need to be strategic about when to 'spend' a wildcard."),
        N.h4("The Key Observation"),
        N.para("For ')' characters: always prefer to match with the most recent '(' first. Only use a '*' as a backup. This greedy choice is correct because '(' has a fixed position and is harder to satisfy; '*' is more flexible. After the scan, any remaining '(' need a '*' that appears after them (position matters!)."),
        N.h4("Building the Solution"),
        N.para("Use two stacks tracking indices: one for '(' positions, one for '*' positions. Process ')' greedily (match '(' first, then '*'). After the loop, while both stacks non-empty: pop from each and verify the '*' index is greater than the '(' index (the '*' must come after the '(' it closes). Any remaining '(' are unmatched — return False."),
        N.callout("Mnemonic: '(' is picky (must match with something later). '*' is flexible (can be anything). Match the picky ones first.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("open_st = []; star_st = []", {"code": True}), " — Two stacks tracking indices (not values) of unmatched '(' and wildcard '*' characters."])),
    N.para(N.rich([("for i, c in enumerate(s):", {"code": True}), " — We need indices (for the final position comparison), so we enumerate."])),
    N.para(N.rich([("if c == '(': open_st.append(i)", {"code": True}), " — Unmatched open paren: push index onto open stack."])),
    N.para(N.rich([("elif c == '*': star_st.append(i)", {"code": True}), " — Wildcard: push index onto star stack. We'll decide later if it's '(' or ')'."])),
    N.para(N.rich([("if open_st: open_st.pop()", {"code": True}), " — ')' found: greedily match with nearest '(' first (LIFO), consuming that open."])),
    N.para(N.rich([("elif star_st: star_st.pop()", {"code": True}), " — No '(' available: use a '*' as '(' to match this ')'. Also consumed LIFO."])),
    N.para(N.rich([("else: return False", {"code": True}), " — No '(' and no '*' to match this ')' — impossible."])),
    N.para(N.rich([("if open_st.pop() > star_st.pop(): return False", {"code": True}), " — For any remaining '(', it needs a '*' to its RIGHT to act as ')'. If '(' index > '*' index, that '*' came before the '(' and can't close it."])),
    N.para(N.rich([("return not open_st", {"code": True}), " — If open_st is empty, all '(' were matched. If star_st still has items, that's fine — unused wildcards are just empty."])),
    N.divider(),
]

# ─── Complexity ───
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all * assignments)", "O(3^n)", "O(n)"],
        ["DP (memoized recursion)", "O(n²)", "O(n²)"],
        ["Two Stacks", "O(n)", "O(n)"],
        ["Lo/Hi Greedy (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks — parentheses matching variant with wildcards"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Counters (Lo/Hi Range) — greedy range tracking for wildcard parentheses strings"])),
    N.callout(
        "When to recognize this pattern: (1) Parentheses validity check with an ambiguous/flexible character. (2) You'd normally use a single counter, but one character type has multiple interpretations. (3) O(1) space is needed — stacks won't do. (4) 'Check if any assignment of wildcards produces a valid structure.'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Classic single-counter or stack approach; foundation for this problem (#20)"])),
    N.bullet(N.rich([("Minimum Add to Make Parentheses Valid", {"bold": True}), " (Medium) — Track unmatched '(' and ')' separately; same lo/hi reasoning (#921)"])),
    N.bullet(N.rich([("Check if a Parentheses String Can Be Valid", {"bold": True}), " (Medium) — Locked positions variant; direct extension of the lo/hi technique (#2116)"])),
    N.bullet(N.rich([("Minimum Number of Swaps to Make String Balanced", {"bold": True}), " (Medium) — Greedy counter approach; count unmatched brackets (#1963)"])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), " (Medium) — Stack-based; compute value of nested balanced string (#856)"])),
    N.bullet(N.rich([("Longest Valid Parentheses", {"bold": True}), " (Hard) — Stack-based; finding longest valid window (#32)"])),
    N.bullet(N.rich([("Remove Invalid Parentheses", {"bold": True}), " (Hard) — BFS / backtracking; all minimum-removal solutions (#301)"])),
    N.para("These problems all share the core technique of tracking open-paren balance (or a range of balances) as you scan left to right."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stacks section → Parentheses Matching. Sub-Pattern: Two Counters (Lo/Hi Range) — analysis-based classification.", "📚", "gray_background"),
]

# ─── Interactive Explainer embed ───
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("valid_parenthesis_string")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
