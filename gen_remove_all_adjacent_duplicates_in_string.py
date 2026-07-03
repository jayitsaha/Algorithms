"""
gen_remove_all_adjacent_duplicates_in_string.py
Notion IN-PLACE update for LeetCode #1047 — Remove All Adjacent Duplicates In String
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8168-a71c-f2a875ed6572"
SLUG = "remove_all_adjacent_duplicates_in_string"

# ── 1. Properties ──────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1047,
    pattern="Stacks",
    subpatterns=["Stack Character Match"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use a stack as a deduplication buffer: push if top != c, pop if top == c (adjacent duplicate). Single pass.",
    icon="🟢"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────────

BRUTE_CODE = '''\
def removeDuplicates_brute(s: str) -> str:
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(s) - 1:
            if s[i] == s[i+1]:
                s = s[:i] + s[i+2:]
                changed = True
            else:
                i += 1
    return s
# Time: O(n^2) — up to n/2 passes of O(n) each
# Space: O(n) — intermediate strings'''

STACK_CODE = '''\
def removeDuplicates(s: str) -> str:
    stack = []
    for c in s:
        if stack and stack[-1] == c:
            stack.pop()       # adjacent duplicate — both removed
        else:
            stack.append(c)   # no match — character survives
    return "".join(stack)
# Time: O(n) — single pass, each char pushed/popped at most once
# Space: O(n) — stack holds at most n chars'''

blocks = []

# ── Problem ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given a string ", ("s", {"code": True}),
        ", repeatedly remove adjacent duplicate characters until no two adjacent characters are equal. "
        "Return the final string.\n\n"
        "Example 1: Input: s = \"abbaca\" → Output: \"ca\"\n"
        "Explanation: 'bb' removed → \"aaca\". Then 'aa' removed → \"ca\".\n\n"
        "Example 2: Input: s = \"azxxzy\" → Output: \"ay\"\n"
        "Explanation: 'xx' removed → \"azzy\". Then 'zz' removed → \"ay\".\n\n"
        "Constraints: 1 <= s.length <= 10^5. s consists of lowercase English letters."
    ])),
    N.divider(),
]

# ── Solution 1: Brute Force ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Brute Force: Repeated Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to keep removing adjacent pairs until none remain. The most literal interpretation: scan the string, remove any pair you find, then restart from the beginning (or from the position of removal)."),
        N.h4("What Doesn't Work"),
        N.para("This works but is slow. Each pass removes at least one pair but may only find one pair deep in the string, requiring another full pass. Worst case: 'aabb...zz' has n/2 pairs each requiring an O(n) scan = O(n^2) total."),
        N.h4("The Key Observation"),
        N.para("The brute force is correct but inefficient. Its weakness: it re-checks characters it has already verified as non-duplicate after a removal. We need a way to skip re-checking."),
        N.h4("Building the Solution"),
        N.para("Scan left to right. For each index i, if s[i] == s[i+1], remove both characters (slice the string), mark that a change happened, and restart. Repeat until no changes occur in a full pass."),
        N.callout("Analogy: playing whack-a-mole — you hit one mole (pair), but another pops up nearby, and you have to scan the whole board again.", "🔨", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("changed = True", {"code": True}), " — sentinel flag; set True to enter the loop initially."])),
    N.para(N.rich([("while changed:", {"code": True}), " — loop until a complete pass found no adjacent duplicate."])),
    N.para(N.rich([("if s[i] == s[i+1]:", {"code": True}), " — found adjacent pair at index i."])),
    N.para(N.rich([("s = s[:i] + s[i+2:]", {"code": True}), " — remove both chars via slicing; creates new O(n) string."])),
    N.para(N.rich([("changed = True", {"code": True}), " — flag that something changed; will need another pass."])),
    N.divider(),
]

# ── Solution 2: Stack (Interview Pick) ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("When processing each character, we only need to know one thing: what was the last surviving character to the left? If it matches the current character, they're adjacent duplicates and both die. If not, the current character joins the survivors."),
        N.h4("What Doesn't Work with Brute Force"),
        N.para("The brute force re-scans already-clean characters after each removal. This is wasteful — those characters haven't changed. We need a data structure that remembers exactly one thing: the most recent survivor."),
        N.h4("The Key Observation"),
        N.para("A stack gives us O(1) access to the most recent survivor (the top). When a cascade happens — removing one pair exposes another — the stack handles it automatically: after a pop, the new top is the previous survivor, ready to be compared with the next character."),
        N.h4("Building the Solution"),
        N.para("Initialize an empty stack. For each character c: if stack is not empty and stack[-1] == c, pop (both c and the top are removed). Otherwise, push c. The stack's invariant: no two adjacent elements are equal. Final answer = ''.join(stack)."),
        N.callout("Analogy: a stack of plates. If the new plate matches the top plate's color, both shatter (pop). Otherwise, the new plate is added to the stack. The final stack of plates is your answer.", "🍽️", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(STACK_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Python list as stack: append()=push, pop()=pop, [-1]=top access. All O(1)."])),
    N.para(N.rich([("for c in s:", {"code": True}), " — single left-to-right pass, O(n) total. Each character processed exactly once."])),
    N.para(N.rich([("if stack and stack[-1] == c:", {"code": True}), " — short-circuit: check stack is not empty before accessing top. Then check if top equals current char."])),
    N.para(N.rich([("stack.pop()", {"code": True}), " — pop the top. The current char c is NOT pushed — both the top and c are eliminated. Two characters removed with one pop."])),
    N.para(N.rich([("stack.append(c)", {"code": True}), " — no match: c survives. Push onto stack as new top."])),
    N.para(N.rich([("return \"\".join(stack)", {"code": True}), " — O(n) string construction. Never use += in a loop (O(n^2)). The stack IS the final deduplicated string."])),
    N.callout(
        "Stack Invariant: At every step, no two adjacent characters in the stack are equal. "
        "This guarantees correctness — the stack always represents the fully-reduced prefix of processed characters.",
        "🔐", "blue_background"
    ),
    N.callout(
        "Common Mistake: Forgetting the 'stack and' guard. If stack is empty, stack[-1] raises IndexError. "
        "Always write: if stack and stack[-1] == c — the 'and' short-circuits safely.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Repeated Scan)", "O(n²)", "O(n)"],
        ["Stack (Interview Pick)", "O(n)", "O(n)"],
        ["In-place Write Pointer (C++/Java)", "O(n)", "O(1) extra"],
    ]),
    N.para("The stack solution processes each character exactly once — each char is pushed at most once and popped at most once, giving O(2n) = O(n) time. Space is O(n) for the stack in the worst case (no duplicates, entire string survives)."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Character Match"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Repeatedly remove adjacent pairs until none remain' → Stack\n"
        "• 'Cascade: removing one pair can expose a new pair' → Stack\n"
        "• 'Undo/cancel the most recent surviving element based on new input' → Stack\n"
        "• Problems involving bracket matching, backspace simulation, string reduction → Stack",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Stack Character Match technique:"),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String II", {"bold": True}), " (Medium) — Remove k consecutive duplicates; use stack of (char, count) pairs. (#1209)"])),
    N.bullet(N.rich([("Backspace String Compare", {"bold": True}), " (Easy) — Simulate '#' as backspace using a stack; compare resulting strings. (#844)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Classic stack: push open brackets, pop and verify on matching close. (#20)"])),
    N.bullet(N.rich([("Asteroid Collision", {"bold": True}), " (Medium) — Stack-based collision simulation; same cancel-on-match structure. (#735)"])),
    N.bullet(N.rich([("Minimum Remove to Make Valid Parentheses", {"bold": True}), " (Medium) — Stack tracks unmatched bracket indices; remove them from string. (#1249)"])),
    N.bullet(N.rich([("Decode String", {"bold": True}), " (Medium) — Stack-based string reconstruction with nested repetition patterns. (#394)"])),
    N.bullet(N.rich([("Zuma Game", {"bold": True}), " (Hard) — Complex cascade variant: groups of 3+ trigger removal. (#488)"])),
    N.para("These problems share the core technique: use a stack to maintain the current 'surviving' state and compare new input against the stack top."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stacks → Stack Character Match", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the cascade in action at steps 6-9 when 'abba' annihilates itself.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
