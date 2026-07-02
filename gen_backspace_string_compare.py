"""
gen_backspace_string_compare.py
Regenerates the Notion page for LeetCode #844 — Backspace String Compare.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ec-8000-cb6eda721425"

# ── 1) Update properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=844,
    pattern="Two Pointers",
    subpatterns=["Reverse Two Pointers"],
    tc="O(n+m)",
    sc="O(1)",
    key_insight="Scan right-to-left with a skip counter — each '#' increments skip, each erased char decrements it, replacing a stack with an O(1) counter.",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe existing content ──────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3) Rebuild body ───────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("s", {"code": True}),
        (" and ", {}),
        ("t", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if they are equal when both are typed into empty text editors. ", {}),
        ("'#'", {"code": True}),
        (" means a backspace character. Note that after backspacing an empty text, the text will remain empty.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "ab#c", t = "ad#c"', {"code": True}),
        (' → True. Both produce "ac" when typed.', {}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "ab##", t = "c#d"', {"code": True}),
        (' → False. s produces "" (empty), t produces "d".', {}),
    ])),
    N.callout(
        N.rich([("Edge case: ", {"bold": True}), ("'#'", {"code": True}),
                (" at the start of a string is a no-op — nothing to delete.", {})]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# Solution 1 — Stack Simulation
blocks += [
    N.h2("Solution 1 — Stack Simulation (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find out what characters are left on screen after processing each string through a text editor. Think of it as simulating a typewriter: letters land on the page, backspaces erase the last letter."),
        N.h4("What Doesn't Work"),
        N.para("Comparing the raw strings character by character fails because '#' doesn't represent a literal character — it transforms the string. You can't compare 'a' from s with '#' from t and conclude anything useful."),
        N.h4("The Key Observation"),
        N.para("A stack perfectly models a text editor. Push letters onto the stack (they appear on screen). Pop for '#' (backspace erases the last character). If the stack is empty when we see '#', it's a no-op. The stack at the end represents what's on screen."),
        N.h4("Building the Solution"),
        N.para("Run process(s) and process(t) independently, each returning a list. Compare the two lists. Python list equality checks element by element, which is exactly what we want."),
        N.callout("Analogy: Think of the stack as your screen. Push = type a letter, pop = press backspace. The stack contents are exactly what you'd see on the monitor.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def backspaceCompare(s: str, t: str) -> bool:\n"
        "    def process(string):\n"
        "        stack = []\n"
        "        for c in string:\n"
        "            if c != '#':\n"
        "                stack.append(c)      # type the letter\n"
        "            elif stack:\n"
        "                stack.pop()          # backspace: erase last char\n"
        "            # else: '#' on empty screen is a no-op\n"
        "        return stack\n"
        "    return process(s) == process(t)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def process(string):", {"code": True}), (" — helper function that simulates typing a string into a text editor.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — represents the characters currently visible on screen (empty editor).", {})])),
    N.para(N.rich([("if c != '#':", {"code": True}), (" — normal letter: append to the screen.", {})])),
    N.para(N.rich([("elif stack:", {"code": True}), (" — backspace pressed and screen is not empty: pop the last character.", {})])),
    N.para(N.rich([("# else:", {"code": True}), (" — backspace on empty screen: implicit no-op, nothing happens.", {})])),
    N.para(N.rich([("return process(s) == process(t)", {"code": True}), (" — compare the two resulting character lists for equality.", {})])),
    N.divider(),
]

# Solution 2 — Reverse Two Pointers (Interview Pick)
blocks += [
    N.h2("Solution 2 — Reverse Two Pointers (Interview Pick) ✓"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We know stack simulation works. Can we avoid allocating O(n+m) space? We need a way to find the surviving characters without explicitly building a list."),
        N.h4("What Doesn't Work"),
        N.para("Scanning left-to-right doesn't help reduce space — when we encounter '#', we've already stored the character it deletes. We'd still need something to undo that storage."),
        N.h4("The Key Observation"),
        N.para("A '#' always affects the character immediately to its LEFT. If we scan right-to-left, we see the '#' BEFORE the character it would delete. We can keep a count of 'pending deletions' — when we see '#', increment the counter; when we see a real letter, if the counter is positive, this letter is erased (decrement counter). If counter is 0, the letter survives."),
        N.h4("Building the Solution"),
        N.para("Two pointers i and j start at the rightmost index of s and t respectively. Inner while loops advance each pointer leftward past erased characters (using skip counters). When both inner loops break, i and j point to the next surviving characters — compare them. Mismatch or length difference → False. Both exhausted → True."),
        N.callout("Analogy: The skip counter is a 'debt counter.' Each '#' says 'I owe one deletion.' Each subsequent real letter pays off one debt. When debt = 0, the next letter is free (it survives).", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def backspaceCompare(s: str, t: str) -> bool:\n"
        "    i, j = len(s) - 1, len(t) - 1\n"
        "    skip_s = skip_t = 0\n"
        "    while i >= 0 or j >= 0:\n"
        "        # Advance i to next surviving character in s\n"
        "        while i >= 0:\n"
        "            if s[i] == '#':\n"
        "                skip_s += 1; i -= 1\n"
        "            elif skip_s > 0:\n"
        "                skip_s -= 1; i -= 1\n"
        "            else:\n"
        "                break\n"
        "        # Advance j to next surviving character in t\n"
        "        while j >= 0:\n"
        "            if t[j] == '#':\n"
        "                skip_t += 1; j -= 1\n"
        "            elif skip_t > 0:\n"
        "                skip_t -= 1; j -= 1\n"
        "            else:\n"
        "                break\n"
        "        # Compare surviving characters\n"
        "        if i >= 0 and j >= 0:\n"
        "            if s[i] != t[j]:\n"
        "                return False\n"
        "        elif i >= 0 or j >= 0:\n"
        "            return False        # one string has leftover chars\n"
        "        i -= 1; j -= 1\n"
        "    return True"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("i, j = len(s)-1, len(t)-1", {"code": True}), (" — start both pointers at the rightmost index of each string.", {})])),
    N.para(N.rich([("skip_s = skip_t = 0", {"code": True}), (" — counters for pending deletions; one per string.", {})])),
    N.para(N.rich([("while i >= 0 or j >= 0:", {"code": True}), (" — continue while at least one string still has characters.", {})])),
    N.para(N.rich([("if s[i] == '#': skip_s += 1; i -= 1", {"code": True}), (" — backspace: owe one more deletion, move left.", {})])),
    N.para(N.rich([("elif skip_s > 0: skip_s -= 1; i -= 1", {"code": True}), (" — real char but it's been erased: consume one pending deletion, move left.", {})])),
    N.para(N.rich([("else: break", {"code": True}), (" — real surviving character found; stop the inner loop.", {})])),
    N.para(N.rich([("if i >= 0 and j >= 0: if s[i] != t[j]: return False", {"code": True}), (" — both have surviving chars; they must match.", {})])),
    N.para(N.rich([("elif i >= 0 or j >= 0: return False", {"code": True}), (" — one exhausted but other isn't; strings have different surviving lengths.", {})])),
    N.para(N.rich([("i -= 1; j -= 1", {"code": True}), (" — move both pointers left for the next comparison pair.", {})])),
    N.para(N.rich([("return True", {"code": True}), (" — all pairs matched and both exhausted simultaneously.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Stack Simulation", "O(n+m)", "O(n+m)"],
        ["Reverse Two Pointers (optimal)", "O(n+m)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Reverse Two Pointers — scan both strings from right to left, using skip counters to simulate deletion without extra space.", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("(1) Problem involves characters that delete/cancel previous characters. "
             "(2) Stack simulation works but uses O(n) space. "
             "(3) The deletion affects elements to the LEFT of the trigger → scanning right-to-left reveals the trigger before the victim. "
             "(4) Follow-up asks to reduce space from O(n) to O(1).", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Remove All Adjacent Duplicates In String", {"bold": True}), (" (Easy) — Stack-based character removal; same simulation structure (#1047)", {})])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Stack tracks matching brackets; deletion-style reasoning (#20)", {})])),
    N.bullet(N.rich([("Remove Duplicate Letters", {"bold": True}), (" (Medium) — Monotonic stack with greedy character selection (#316)", {})])),
    N.bullet(N.rich([("Decode String", {"bold": True}), (" (Medium) — Stack-based reversal and reconstruction of an encoded string (#394)", {})])),
    N.bullet(N.rich([("Compare Version Numbers", {"bold": True}), (" (Medium) — Two-pointer comparison of two processed strings segment by segment (#165)", {})])),
    N.bullet(N.rich([("String Compression", {"bold": True}), (" (Medium) — Two-pointer in-place write pattern on a character array (#443)", {})])),
    N.para("These problems share the core technique of simulating a stack or using a pointer/counter to track state without explicit extra data structures."),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("backspace_string_compare")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch i and j scan right-to-left, skip counters accumulate and discharge, and surviving characters get compared pair by pair.",
         {"italic": True, "color": "gray"}),
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
