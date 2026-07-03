"""
gen_remove_duplicate_letters.py
Notion IN-PLACE update for LC #316 Remove Duplicate Letters
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8172-96c7-c2f4f609cc78"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=316,
    pattern="Stacks",
    subpatterns=["Monotonic Stack + Seen Set"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Greedy monotonic stack: pop larger chars when they still appear later; seen set prevents duplicates.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a string ", {}),
        ("s", {"code": True}),
        (", remove duplicate letters so that every letter appears once and only once. "
         "You must make sure your result is the smallest in lexicographic order among "
         "all possible results. The relative order of characters must be preserved "
         "(you are selecting a subsequence, not rearranging).", {})
    ])),
    N.callout(
        N.rich([
            ("Example 1: ", {"bold": True}),
            ('s = "bcabc"', {"code": True}),
            (' → ', {}),
            ('"abc"', {"code": True}),
            ('\nExample 2: ', {"bold": True}),
            ('s = "cbacdcbc"', {"code": True}),
            (' → ', {}),
            ('"acdb"', {"code": True})
        ]),
        "📋", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1 — Greedy Monotonic Stack ────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Greedy Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must choose exactly one occurrence of each unique character, "
               "preserving relative order (it's a subsequence). Among all valid "
               "choices, we want the lexicographically smallest result."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: enumerate all valid subsequences and take the minimum. "
               "With n characters, there can be exponentially many valid subsequences. "
               "This is O(n^k) where k is the number of unique characters — far too slow."),
        N.h4("The Key Observation"),
        N.para("We want smaller characters as early as possible. If the current "
               "character c is smaller than the top of our result stack AND the top "
               "still appears later in the string (so removing it won't lose it "
               "permanently), we should remove the top and put c there instead. "
               "This is a greedy improvement."),
        N.h4("Building the Solution"),
        N.para("Scan left-to-right. Maintain: (1) a monotonic stack for the growing "
               "result — kept in non-decreasing order, (2) a seen set to avoid "
               "duplicates, (3) a remaining count map to know if a character still "
               "appears ahead. At each character: decrement remaining, skip if seen, "
               "pop while top > current AND remaining[top] > 0, then push."),
        N.callout(
            "Analogy: imagine sorting a queue where people can step back if someone "
            "smaller arrives — but only if they know they'll get another chance to enter later.",
            "🧠", "blue_background"
        )
    ]),
]

# Code
code_sol1 = """\
def removeDuplicateLetters(s: str) -> str:
    # Pre-count: how many times does each char appear total?
    remaining = {}
    for c in s:
        remaining[c] = remaining.get(c, 0) + 1

    seen = set()   # chars already committed to result
    stack = []     # the result, built greedily

    for c in s:
        remaining[c] -= 1          # consume this occurrence (MUST be first)
        if c in seen:              # already in result — skip duplicate
            continue
        # Greedy pop: while top is larger than c AND top still appears later
        while (stack
               and stack[-1] > c
               and remaining[stack[-1]] > 0):
            seen.discard(stack.pop())   # undo commitment to popped char
        stack.append(c)    # commit
        seen.add(c)

    return ''.join(stack)"""

blocks += [
    N.h3("Code"),
    N.code(code_sol1, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("remaining = {}", {"code": True}), (" — dictionary to count future occurrences of each character.", {})])),
    N.para(N.rich([("for c in s: remaining[c] += 1", {"code": True}), (" — pre-count pass: walk entire string once to fill remaining map.", {})])),
    N.para(N.rich([("seen = set()", {"code": True}), (" — tracks characters already present in the stack/result.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — the result, read bottom-to-top. Also acts as our monotonic stack.", {})])),
    N.para(N.rich([("remaining[c] -= 1", {"code": True}), (" — MUST happen first. Even if we skip this char, it's been consumed from the string.", {})])),
    N.para(N.rich([("if c in seen: continue", {"code": True}), (" — if we already committed to this char, skip. Earlier occurrence is always at least as good.", {})])),
    N.para(N.rich([("while stack and stack[-1] > c and remaining[stack[-1]] > 0", {"code": True}), (" — pop only when: top is larger (gain) AND top appears again later (safe to delay).", {})])),
    N.para(N.rich([("seen.discard(stack.pop())", {"code": True}), (" — pop top, undo its seen commitment so it can be re-added later.", {})])),
    N.para(N.rich([("stack.append(c); seen.add(c)", {"code": True}), (" — commit current char to result.", {})])),
    N.para(N.rich([("return ''.join(stack)", {"code": True}), (" — stack read bottom-to-top is the lexicographically smallest valid subsequence.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force Recursion ────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive Brute Force (Exponential, for intuition)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each step, find the leftmost position where we can safely take "
               "a character: scan until we'd lose a unique character, then take "
               "the smallest character in that prefix. Recurse on the suffix with "
               "that character removed."),
        N.h4("What Doesn't Work (at scale)"),
        N.para("This is O(n^2 * k) in time and O(n) recursion depth. It correctly "
               "produces the answer but is too slow for n > 1000. Useful for "
               "verifying the greedy approach on small inputs."),
        N.h4("The Key Observation"),
        N.para("We can only remove a character at position i if every unique character "
               "still appears in s[i+1:]. Find the smallest such character in the "
               "maximal safe prefix, then recurse."),
        N.h4("Building the Solution"),
        N.para("Track counts. Scan until taking a character would lose a unique char. "
               "Pick the smallest in that window. Remove all copies of it from the "
               "remaining string and recurse."),
    ]),
]

code_sol2 = """\
from collections import Counter

def removeDuplicateLetters_brute(s: str) -> str:
    if not s:
        return s
    cnt = Counter(s)
    pos = 0  # position of best (smallest) character we can safely take
    for i in range(len(s)):
        if s[i] < s[pos]:
            pos = i
        cnt[s[i]] -= 1
        if cnt[s[i]] == 0:
            # s[i] is the last of its kind — we must not go past it
            break
    # Take s[pos], recurse on suffix with all copies of s[pos] removed
    return s[pos] + removeDuplicateLetters_brute(s[pos+1:].replace(s[pos], ''))\
"""

blocks += [
    N.h3("Code"),
    N.code(code_sol2, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not s: return s", {"code": True}), (" — base case: empty string.", {})])),
    N.para(N.rich([("cnt = Counter(s)", {"code": True}), (" — count chars in current remaining string.", {})])),
    N.para(N.rich([("pos = 0", {"code": True}), (" — track position of the best (smallest) character we can safely select.", {})])),
    N.para(N.rich([("if s[i] < s[pos]: pos = i", {"code": True}), (" — update best position when we find a smaller character.", {})])),
    N.para(N.rich([("cnt[s[i]] -= 1; if cnt[s[i]] == 0: break", {"code": True}), (" — stop when we'd skip the last occurrence of some character.", {})])),
    N.para(N.rich([("return s[pos] + recurse(suffix.replace(s[pos],''))", {"code": True}), (" — take the best character, recurse on remaining string with it removed.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy Monotonic Stack (Optimal)", "O(n)", "O(k) — k ≤ 26 unique chars"],
        ["Recursive Brute Force", "O(n² × k)", "O(n) recursion stack"],
    ]),
    N.para("The greedy stack achieves O(n) because each character is pushed and popped "
           "at most once — amortized O(1) per character. The seen set and remaining map "
           "are bounded by the alphabet size k (≤ 26), making space effectively O(1)."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Monotonic Stack + Seen Set — maintain a non-decreasing stack of distinct characters, "
                    "using a remaining-count guard and a seen set to make greedy pop decisions.", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Select a subsequence with uniqueness constraint, "
             "(2) optimize for lexicographic order, "
             "(3) need to 'undo' a previous choice if a better option arrives, "
             "(4) need future data to decide whether undoing is safe → pre-count map.", {})
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Algorithm Note: ", {"bold": True}),
        ("The key invariant is that the stack is always in non-decreasing lexicographic order. "
         "The two-condition pop guard (top > current AND remaining[top] > 0) is what makes "
         "the greedy provably correct: we only postpone a character when we know we won't lose it.", {})
    ])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Monotonic Stack technique:"),
    N.bullet(N.rich([("Smallest Subsequence of Distinct Characters", {"bold": True}),
                     (" (Medium) — Literally the same problem with different wording. LC #1081.", {})])),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}),
                     (" (Medium) — Same monotonic stack pop logic; remove exactly k digits to get smallest number. LC #402.", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}),
                     (" (Easy) — Classic monotonic stack: find next larger element for each item. LC #496.", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}),
                     (" (Medium) — Monotonic stack: for each day, find the next warmer day. LC #739.", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}),
                     (" (Hard) — Monotonic stack with previous-smaller element pattern. LC #84.", {})])),
    N.bullet(N.rich([("Create Maximum Number", {"bold": True}),
                     (" (Hard) — Greedy selection of digits from two arrays using monotonic stack. LC #321.", {})])),
    N.para("These problems all share the core technique: maintain a stack in monotonic order "
           "by popping elements when a 'better' element arrives, subject to problem-specific guards."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stacks section, "
              "Monotonic Stack sub-pattern.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("remove_duplicate_letters")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
