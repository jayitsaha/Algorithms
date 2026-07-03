"""
gen_removing_stars_from_a_string.py
Notion IN-PLACE update for LeetCode #2390 — Removing Stars From a String
Pattern: Stacks · Subpattern: Stack Pop on Star
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81ba-8269-c18756238185"

# ── 1. Set page properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2390,
    pattern="Stacks",
    subpatterns=["Stack Pop on Star"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Use a stack: push letters, pop on star — the top is always the closest surviving character to the left.",
    icon="🟡",
)
print("Properties set OK")

# ── 2. Wipe existing body ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Rebuild body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a string ", {}),
        ("s", {"code": True}),
        (", which contains lowercase English letters and stars (", {}),
        ("*", {"code": True}),
        ("). In one operation, you choose a star in ", {}),
        ("s", {"code": True}),
        (", remove the closest non-star character to its left, and remove the star itself. Return the string after all stars have been removed. The input is guaranteed to be valid: enough non-star characters always exist to the left of every star.", {}),
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('s = "leet**cod*e" → "lecoe"  ', {}),
        ("(t erased, then e erased, then d erased)", {"italic": True}),
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('s = "erase***" → ""  ', {}),
        ("(all characters erased by the three trailing stars)", {"italic": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Stack (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Stack / List Buffer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We are simulating a text editor. Characters type a letter; stars press Backspace. What data structure models a text editor's current document? A stack — push letters onto it, pop (backspace) on a star."),
        N.h4("What Doesn't Work"),
        N.para('A naive string approach like res = res[:-1] when we see a star is O(n) per operation because Python strings are immutable — each slice creates a brand-new string object. In the worst case (n/2 stars), this is O(n²) total: too slow for n up to 100,000.'),
        N.h4("The Key Observation"),
        N.para('The problem says each star deletes "the closest non-star character to its LEFT." The stack top is always the most recently pushed (i.e., leftmost-surviving) character. Popping the top is exactly the correct operation — no searching, no indexing.'),
        N.h4("Building the Solution"),
        N.para("1) Initialize an empty list (our stack). 2) For each character c in s: if c is a letter, append it; if c is '*', pop the top. 3) Join the list into a string and return."),
        N.callout(
            "Analogy: Think of the stack as the cursor buffer in a text editor. Letters type a character (append); stars press Backspace (pop). The buffer at the end is the final typed text.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def removeStars(s: str) -> str:\n"
        "    stack = []\n"
        "    for c in s:\n"
        "        if c == '*':\n"
        "            stack.pop()\n"
        "        else:\n"
        "            stack.append(c)\n"
        "    return \"\".join(stack)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = []", {"code": True}), " — Initialize empty list as our mutable character buffer / stack."])),
    N.para(N.rich([("for c in s:", {"code": True}), " — Single left-to-right scan over the input. O(n) iterations total."])),
    N.para(N.rich([("if c == '*':", {"code": True}), " — Detect the star (backspace) character."])),
    N.para(N.rich([("stack.pop()", {"code": True}), " — Remove the top element (most recent survivor). O(1) amortized. The problem guarantees the stack is non-empty here."])),
    N.para(N.rich([("stack.append(c)", {"code": True}), " — Add this letter to the survivors. It becomes the new top. O(1) amortized."])),
    N.para(N.rich([('"".join(stack)', {"code": True}), " — Read the stack left-to-right (bottom-to-top) to produce the final string. O(n). Called only once."])),
    N.divider(),
]

# ── Solution 2 — String Slice (Slow, educational) ──
blocks += [
    N.h2("Solution 2 — String Slice Loop (O(n²) — do NOT use in interviews)"),
    N.toggle_h3("💡 Intuition: Why This Feels Natural but Fails", [
        N.h4("Reframe the Problem"),
        N.para("If you treat the result as a growing string, a star means 'cut the last character off'. This directly maps to res = res[:-1]."),
        N.h4("What Doesn't Work"),
        N.para("Python strings are immutable. res[:-1] creates a brand-new string every time. On a 100K character input with 50K stars, that is 50K allocations of average 50K characters — roughly 2.5 billion character copies."),
        N.h4("The Key Observation"),
        N.para("The root cause is mutability. Switching from a string to a list gives O(1) pop and the same O(1) append, solving the performance issue entirely."),
        N.h4("Building the Solution"),
        N.para("Start with res = ''. For each character, either concatenate or slice. Return res. Correct but O(n²)."),
    ]),
    N.h3("Code"),
    N.code(
        "def removeStars(s: str) -> str:\n"
        "    res = \"\"\n"
        "    for c in s:\n"
        "        if c == '*':\n"
        "            res = res[:-1]   # O(n) — new string allocation each time!\n"
        "        else:\n"
        "            res += c         # Also O(n) in general\n"
        "    return res"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("res = ''", {"code": True}), " — Immutable string accumulator. Every modification creates a new object."])),
    N.para(N.rich([("res = res[:-1]", {"code": True}), " — Slice off last character. Allocates a new string of length len(res)−1. O(n) per call."])),
    N.para(N.rich([("res += c", {"code": True}), " — String concatenation. Also O(n) in general because strings are immutable."])),
    N.callout(
        "Use this solution only to illustrate the naive approach and then explain why the stack version is O(n). Never submit it for large inputs.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["String Slice Loop", "O(n²)", "O(n)"],
        ["Stack / List Buffer ✓", "O(n)", "O(n)"],
        ["Two-pointer in-place (follow-up)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stacks"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Stack Pop on Star"])),
    N.callout(
        "When to recognize this pattern: (1) 'Delete the closest / nearest character to the left' — the stack top is always that character. (2) 'Simulate backspace / undo' — stack models document state. (3) A special trigger character (star, bracket, duplicate) causes removal of the most recently added element.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Stack Pop on Star / Backspace technique:"),
    N.bullet(N.rich([("Backspace String Compare", {"bold": True}), " (Easy) — Compare two strings after processing '#' as backspace — identical push/pop pattern (#844)"])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String", {"bold": True}), " (Easy) — Pop if stack top equals current char, else push (#1047)"])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), " (Easy) — Push openers, pop on closer, verify top matches — bracket matching variant (#20)"])),
    N.bullet(N.rich([("Asteroid Collision", {"bold": True}), " (Medium) — Push right-moving asteroids; pop on left-moving collision with a smaller right-mover (#735)"])),
    N.bullet(N.rich([("Min Remove to Make Valid Parentheses", {"bold": True}), " (Medium) — Stack tracks unmatched bracket indices; remove them from result (#1249)"])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates II", {"bold": True}), " (Medium) — Stack stores (char, count); pop group when count reaches k (#1209)"])),
    N.bullet(N.rich([("Decode String", {"bold": True}), " (Medium) — Stack of (string, repeat count) handles nested bracket expansion (#394)"])),
    N.para("These problems share the same core technique: a stack whose top always represents the closest surviving / most recent element, and a trigger character that causes a pop rather than a push."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue Patterns section · Sub-Pattern: Stack Pop on Star", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("removing_stars_from_a_string")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks queued: {len(blocks)}")
