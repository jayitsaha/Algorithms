"""
gen_longest_valid_parentheses.py
Regenerates Notion page for LeetCode #32 Longest Valid Parentheses (IN-PLACE).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8160-bd60-dfad76077868"

# ── Step 1: Set page properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=32,
    pattern="Stacks",
    subpatterns=["Stack Index or DP", "Parentheses Matching"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push indices (not chars) onto the stack; seed with -1 sentinel. On ')': pop, then length = i - stack[-1] if stack non-empty, else push i as new wall.",
    icon="🔴",
)
print("Properties set.")

# ── Step 2: Wipe old body ─────────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build new body ────────────────────────────────────────────────────
print("Building page body...")
blocks = []

# ── Problem statement ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a string ",
        ("s", {"code": True}),
        " containing only ",
        ("'('", {"code": True}),
        " and ",
        ("')'", {"code": True}),
        ", return the length of the longest valid (well-formed) parentheses substring.",
    ])),
    N.para("Examples:"),
    N.bullet(N.rich([('s = ")()())"', {"code": True}), " → 4  (the substring ", ('"()()"', {"code": True}), " at indices 1–4)"])),
    N.bullet(N.rich([('s = "(()"', {"code": True}), " → 2  (the substring ", ('"()"', {"code": True}), " at indices 1–2)"])),
    N.bullet(N.rich([('s = "(()())"', {"code": True}), " → 6  (the entire string is valid)"])),
    N.divider(),
]

# ── Solution 1: Stack Index Trick ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Stack Index Trick (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the length of the longest contiguous valid parentheses substring. 'Valid' means every '(' is matched with a ')' and no unmatched brackets break the run."),

        N.h4("What Doesn't Work"),
        N.para("A character-based stack only tells us WHETHER something matched, not how long the valid run is. We'd know pairs exist but couldn't compute substring length efficiently. Brute force checking all O(n²) substrings is O(n³) — too slow."),

        N.h4("The Key Observation"),
        N.para("If we push INDICES instead of characters, after each pop we can measure length as: i - stack[-1]. The stack[-1] after popping represents 'the last unmatched position' — the boundary our valid run started from. This single subtraction captures the full contiguous valid length, including nested and chained pairs."),

        N.h4("Building the Solution"),
        N.para("Seed the stack with [-1] as a sentinel wall at virtual position -1. For '(': push its index. For ')': pop. If stack is non-empty, compute i - stack[-1] as the current valid length. If stack is empty, this ')' is unmatched — push its index as the new wall. This wall pattern correctly handles all cases."),

        N.callout("Analogy: Think of the stack as a tape measure. The sentinel -1 is the starting anchor. Every unmatched bracket becomes a new anchor. When we find a match, we subtract the current anchor position from our current position to get the run length.", "🧠", "blue_background"),
    ]),

    N.h3("Code"),
    N.code("""\
def longestValidParentheses(s: str) -> int:
    stack = [-1]        # sentinel wall before position 0
    max_len = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)       # remember this open bracket's position
        else:
            stack.pop()           # pop matching '(' or the current wall
            if stack:
                # a wall still exists → valid run from wall+1 to i
                max_len = max(max_len, i - stack[-1])
            else:
                # no wall → this ')' is unmatched; becomes new wall
                stack.append(i)
    return max_len
"""),

    N.h3("Line by Line"),
    N.para(N.rich([("stack = [-1]", {"code": True}), " — Initialize with sentinel -1. This virtual wall ensures length = i - (-1) = i+1 for runs starting at index 0."])),
    N.para(N.rich([("max_len = 0", {"code": True}), " — Best valid length seen. Returns 0 if no valid substring exists."])),
    N.para(N.rich([("for i, ch in enumerate(s):", {"code": True}), " — Scan every character with its index. We need both char and position."])),
    N.para(N.rich([("if ch == '(':", {"code": True}), " — Open bracket: save its index for future matching."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — Push the open bracket's index. We'll pop this when the matching ')' arrives."])),
    N.para(N.rich([("stack.pop()", {"code": True}), " — Close bracket: pop. This consumes either a matching '(' index OR the current wall."])),
    N.para(N.rich([("if stack:", {"code": True}), " — If stack is non-empty, a wall still exists — we have a valid run."])),
    N.para(N.rich([("max_len = max(max_len, i - stack[-1])", {"code": True}), " — Length = current position minus the wall. This captures the full contiguous run length."])),
    N.para(N.rich([("else: stack.append(i)", {"code": True}), " — Stack empty after pop = this ')' is unmatched. Push index as new wall."])),
    N.para(N.rich([("return max_len", {"code": True}), " — Return best length found across the entire scan."])),
    N.divider(),
]

# ── Solution 2: Dynamic Programming ──────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Dynamic Programming"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp[i] = length of the longest valid substring ending exactly at position i. Only ')' characters can end a valid substring, so dp[i] = 0 whenever s[i] = '('."),

        N.h4("The Two Cases for ')'"),
        N.para("Case 1: s[i] = ')' and s[i-1] = '(' — direct pair. The valid run extending through this pair = dp[i-2] + 2 (the valid run before the '(' plus 2 for this pair)."),
        N.para("Case 2: s[i] = ')' and s[i-1] = ')' — nested/extended. If dp[i-1] > 0, we have a valid block just before. Jump past it: j = i - dp[i-1] - 1. If s[j] = '(', it matches our current ')'. dp[i] = dp[i-1] + 2 + dp[j-1]."),

        N.h4("Building the Solution"),
        N.para("Fill the dp array left to right. At each position, apply whichever case matches. Return max(dp)."),

        N.callout("dp[j-1] in case 2 picks up any additional valid run that appeared before the opening '(' — this handles chained sequences like '()(())'.", "🧠", "blue_background"),
    ]),

    N.h3("Code"),
    N.code("""\
def longestValidParentheses(s: str) -> int:
    if not s:
        return 0
    dp = [0] * len(s)   # dp[i] = longest valid substring ending at i
    for i in range(1, len(s)):
        if s[i] == ')':
            if s[i - 1] == '(':
                # Case 1: direct pair "…()"
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif dp[i - 1] > 0:
                # Case 2: nested ") ending a valid block"
                j = i - dp[i - 1] - 1   # position of the opening '('
                if j >= 0 and s[j] == '(':
                    dp[i] = dp[i - 1] + 2 + (dp[j - 1] if j > 0 else 0)
    return max(dp)
"""),

    N.h3("Line by Line"),
    N.para(N.rich([("dp = [0] * len(s)", {"code": True}), " — dp[i] = longest valid substring ending exactly at index i. Starts all zeros."])),
    N.para(N.rich([("if s[i] == ')':", {"code": True}), " — Only ')' can end a valid substring; skip all '(' positions."])),
    N.para(N.rich([("if s[i-1] == '(':", {"code": True}), " — Case 1: we found a direct adjacent pair. Chain onto whatever valid run came before the '('."])),
    N.para(N.rich([("dp[i] = (dp[i-2] if i >= 2 else 0) + 2", {"code": True}), " — Extend the valid run ending two positions back by 2 (for this new pair)."])),
    N.para(N.rich([("j = i - dp[i-1] - 1", {"code": True}), " — Case 2: jump past the inner valid block to find the position that should be its opening '('."])),
    N.para(N.rich([("dp[i] = dp[i-1] + 2 + (dp[j-1] if j > 0 else 0)", {"code": True}), " — Inner block length + new pair + any valid run before j."])),
    N.divider(),
]

# ── Solution 3: Two-Pass Counters ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Two-Pass Counters (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Count left and right brackets. When counts balance, we found a valid substring of length 2*right. When right > left (more closes than opens), we must have hit an unmatched ')' — reset both counters."),

        N.h4("Why Two Passes?"),
        N.para("The left-to-right pass misses cases where we have excess '(' — like '(()', we'd accumulate left=2, right=1 and never trigger a balance or reset. The right-to-left pass handles this: it treats excess '(' (from the reversed perspective) as the blocker, resetting when left > right."),

        N.callout("Together, the two passes cover all possible unmatched-bracket scenarios. Neither pass alone is sufficient.", "🧠", "blue_background"),
    ]),

    N.h3("Code"),
    N.code("""\
def longestValidParentheses(s: str) -> int:
    left = right = max_len = 0
    # Left-to-right: catches excess ')' case
    for ch in s:
        if ch == '(': left += 1
        else: right += 1
        if left == right:
            max_len = max(max_len, 2 * right)
        elif right > left:
            left = right = 0   # unmatched ')' → reset
    # Right-to-left: catches excess '(' case
    left = right = 0
    for ch in reversed(s):
        if ch == '(': left += 1
        else: right += 1
        if left == right:
            max_len = max(max_len, 2 * left)
        elif left > right:
            left = right = 0   # unmatched '(' (in reverse) → reset
    return max_len
"""),

    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n³)", "O(n)"],
        ["Stack Index Trick (Interview Pick)", "O(n)", "O(n)"],
        ["Dynamic Programming", "O(n)", "O(n)"],
        ["Two-Pass Counters", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Index or DP, Parentheses Matching"])),
    N.callout(
        "When to recognize this pattern: (1) String contains only '(' and ')'. "
        "(2) You need the LENGTH of valid runs, not just validity. "
        "(3) 'Longest valid' + brackets → push indices. "
        "(4) Need to measure distance between matching elements using index subtraction.",
        "🔎", "green_background"
    ),
    N.para("Note: 'Stack Index' sub-pattern (pushing indices for length measurement) is based on analysis — the guide lists 'Parentheses Matching' for stack problems, but the index-based length computation is a key refinement specific to this problem type."),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (stack-based bracket matching and/or length measurement):"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Basic stack validity check; the foundational bracket problem (#20)"])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), " (Medium) — Stack of indices to find which characters to remove (#1249)"])),
    N.bullet(N.rich([("Score of Parentheses", {"bold": True}), " (Medium) — Stack-based scoring where nesting depth multiplies values (#856)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Monotonic stack where i - stack[-1] computes widths (same index-subtraction idea) (#84)"])),
    N.bullet(N.rich([("Remove Invalid Parentheses", {"bold": True}), " (Hard) — BFS over all possible removals (#301)"])),
    N.bullet(N.rich([("Check if Parentheses String Can Be Valid", {"bold": True}), " (Medium) — Two-pass counter technique, same balance idea (#2116)"])),
    N.para("These problems all share the core technique of using a stack (or counters) to track bracket state and measure structural properties of the sequence."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns section. Sub-Pattern: Parentheses Matching (standard), Stack Index variant (analysis).", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_valid_parentheses")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
