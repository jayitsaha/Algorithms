"""
gen_merge_strings_alternately.py
Notion update script for LeetCode #1768 Merge Strings Alternately.
Updates the existing page in-place via notion_lib.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8170-b007-ef2cbf6ba6f5"

# ── 1) Properties ──────────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=1768,
    pattern="Two Pointers",
    subpatterns=["Same Direction Interleave"],
    tc="O(m+n)",
    sc="O(m+n)",
    key_insight="Use two forward-moving pointers to zip characters alternately; append tail of longer string after the loop.",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
print("Wiping page...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings ", {}),
        ("word1", {"code": True}),
        (" and ", {}),
        ("word2", {"code": True}),
        (", merge them by adding letters in alternating order, starting with ", {}),
        ("word1", {"code": True}),
        (". If one string is longer than the other, append the additional letters to the end of the merged string.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ('word1 = "abc"', {"code": True}),
        (", ", {}),
        ('word2 = "pqrs"', {"code": True}),
        (' → result = "apbqcrs"', {"code": True}),
        (". After the 3-pair interleave, the 's' tail from word2 is appended.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
SOLUTION_1_CODE = '''\
def mergeAlternately(word1: str, word2: str) -> str:
    i, j = 0, 0        # two forward-moving pointers
    res = []            # list avoids O(n²) string concat
    while i < len(word1) and j < len(word2):
        res.append(word1[i])   # word1 leads each pair
        res.append(word2[j])   # word2 follows immediately
        i += 1
        j += 1
    res.append(word1[i:])  # tail of word1 ("" if exhausted)
    res.append(word2[j:])  # tail of word2 ("" if exhausted)
    return "".join(res)    # O(m+n) linear join\
'''

blocks += [
    N.h2("Solution 1 — Two-Pointer Explicit (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to interleave two strings character by character, starting from index 0 of each, and appending whatever is left from the longer string. Think of it as a zipper: teeth from the left track and right track mesh together one at a time."),
        N.h4("What Doesn't Work"),
        N.para("A single index won't suffice because the two strings advance independently. A naive approach might use Python's zip() but that silently discards the tail from the longer string — you'd need to handle the leftover explicitly anyway."),
        N.h4("The Key Observation"),
        N.para("Use two separate pointers i (into word1) and j (into word2). They both advance at the same pace during the interleave phase. Once either runs out, the loop ends and one slice-based append captures the entire tail in O(1) code (O(k) time)."),
        N.h4("Building the Solution"),
        N.para("Loop while both i < len(word1) AND j < len(word2). Inside, append word1[i] then word2[j], then advance both. After the loop, call res.append(word1[i:]) and res.append(word2[j:]). At most one of these appends will contribute non-empty content — they are mutually exclusive because the loop exits as soon as the shorter string ends."),
        N.callout("Analogy: Two conveyor belts feeding packages alternately onto a single output belt. When one belt empties, the remaining packages on the other belt continue uninterrupted.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("i, j = 0, 0", {"code": True}), (" — Two forward-moving pointers, one per string, both starting at index 0.", {})])),
    N.para(N.rich([("res = []", {"code": True}), (" — Accumulate into a list. Appending to a list is O(1) amortized; concatenating Python strings in a loop is O(n²). The final join is O(m+n).", {})])),
    N.para(N.rich([("while i < len(word1) and j < len(word2):", {"code": True}), (" — Loop continues only while both strings still have characters. The AND condition means the loop exits as soon as either string is exhausted.", {})])),
    N.para(N.rich([("res.append(word1[i])", {"code": True}), (" — Take one character from word1. word1 always leads each pair per the problem specification.", {})])),
    N.para(N.rich([("res.append(word2[j])", {"code": True}), (" — Immediately take one from word2. Together with the word1 append, this forms one interleaved pair.", {})])),
    N.para(N.rich([("i += 1; j += 1", {"code": True}), (" — Advance both pointers. Both move at the same pace through their respective strings.", {})])),
    N.para(N.rich([("res.append(word1[i:])", {"code": True}), (" — Append the remaining tail of word1. If i == len(word1), the slice returns '' (empty string) — safe and harmless.", {})])),
    N.para(N.rich([("res.append(word2[j:])", {"code": True}), (" — Same for word2's tail. At most one of these two tail appends will be non-empty — they are mutually exclusive.", {})])),
    N.para(N.rich([("return ''.join(res)", {"code": True}), (" — Single O(m+n) pass to build the final string from the collected characters.", {})])),
    N.divider(),
]

# ── Solution 2 ──
SOLUTION_2_CODE = '''\
def mergeAlternately(word1: str, word2: str) -> str:
    res = []
    for k in range(max(len(word1), len(word2))):
        if k < len(word1): res.append(word1[k])
        if k < len(word2): res.append(word2[k])
    return "".join(res)\
'''

blocks += [
    N.h2("Solution 2 — Single-Loop with Bounds Checks"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of a while-loop with two pointers, use a single for-loop that counts up to the length of the longer string. At each position k, try to take from word1 (if k is valid) and then from word2 (if k is valid)."),
        N.h4("The Key Observation"),
        N.para("When k exceeds the shorter string's length, only one of the two if-guards fires. This naturally handles the tail — no separate tail-appending code is needed. The loop itself takes care of the remainder."),
        N.h4("Building the Solution"),
        N.para("Loop k from 0 to max(len(word1), len(word2)) - 1. Two independent if-checks ensure no IndexError. For k in the interleave range, both fire. For k in the tail range, only one fires."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("range(max(len(word1), len(word2)))", {"code": True}), (" — Loop runs exactly max(m, n) times — enough to cover all characters in both strings.", {})])),
    N.para(N.rich([("if k < len(word1): res.append(word1[k])", {"code": True}), (" — Guard prevents IndexError. During the tail range of word2 being longer, this guard is false and we skip.", {})])),
    N.para(N.rich([("if k < len(word2): res.append(word2[k])", {"code": True}), (" — Same guard for word2. During word1's tail range, this guard is false.", {})])),
    N.divider(),
]

# ── Solution 3 ──
SOLUTION_3_CODE = '''\
from itertools import zip_longest

def mergeAlternately(word1: str, word2: str) -> str:
    # zip_longest pads the shorter iterable with fillvalue
    return "".join(a + b for a, b in zip_longest(word1, word2, fillvalue=""))\
'''

blocks += [
    N.h2("Solution 3 — zip_longest (Pythonic One-liner)"),
    N.code(SOLUTION_3_CODE, "python"),
    N.para("zip_longest from itertools pairs characters from both strings, filling '' for the shorter one once it's exhausted. The generator expression concatenates each pair, and join assembles the result. All three solutions are O(m+n) time and space."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Pointer Explicit (Interview Pick)", "O(m+n)", "O(m+n)"],
        ["Single-Loop with Bounds Checks", "O(m+n)", "O(m+n)"],
        ["zip_longest", "O(m+n)", "O(m+n)"],
        ["Naïve string concat in loop", "O((m+n)²)", "O(m+n)"],
    ]),
    N.callout("m = len(word1), n = len(word2). The output string of length m+n is unavoidable — any correct algorithm must produce and store m+n characters.", "📐", "gray_background"),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Same Direction Interleave", {})])),
    N.callout(
        "When to recognize this pattern: the problem asks you to interleave two sequences alternately, "
        "merge two sources character-by-character, or 'zip' two iterables. Key signals: "
        "'alternating order', 'merge by adding letters in turns', 'starting with word1'. "
        "Both pointers advance in the same direction (forward), unlike opposite-direction two-pointer problems.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Merge Sorted Array", {"bold": True}), (" (Easy) — Merge two sorted arrays in-place from the back; same-direction two-pointer variant (#88)")])),
    N.bullet(N.rich([("Merge Two Sorted Lists", {"bold": True}), (" (Easy) — Linked list merge; same 'take next' pattern with pointer rewiring (#21)")])),
    N.bullet(N.rich([("Interleaving String", {"bold": True}), (" (Medium) — Can s3 be formed by interleaving s1 and s2? DP on two-pointer state space (#97)")])),
    N.bullet(N.rich([("Shuffle the Array", {"bold": True}), (" (Easy) — Interleave first and second halves of a single array (#1470)")])),
    N.bullet(N.rich([("Move Zeroes", {"bold": True}), (" (Easy) — Same-direction slow/fast write-read pointer pattern (#283)")])),
    N.para("These problems share the same core technique: two pointers advancing in the same forward direction, each consuming from a different source sequence."),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("merge_strings_alternately")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the two pointers i and j advance through word1 and word2, "
         "the result row fill character by character, and the tail being appended at the end.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
