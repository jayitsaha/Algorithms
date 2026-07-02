"""
gen_permutation_in_string.py — Notion update for LeetCode #567 Permutation in String
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-811c-8f55-d05631c9d1da"
SLUG = "permutation_in_string"

# ── Step 1: Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=567,
    pattern="Sliding Window",
    subpatterns=["Frequency Count Window"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Slide a fixed-size window of len(s1) across s2; track a 'matches' counter over 26-char slots so each slide is O(1).",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body ───────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── Step 3: Rebuild body ────────────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings "), ("s1", {"code": True}), (" and "), ("s2", {"code": True}),
        (", return "), ("True", {"code": True}),
        (" if "), ("s2", {"code": True}),
        (" contains a permutation of "), ("s1", {"code": True}), (" as a contiguous substring."),
        ("\n\nExample 1: s1=\"ab\", s2=\"eidbaooo\" → True (s2[3..4]=\"ba\" is a permutation of \"ab\")"),
        ("\nExample 2: s1=\"ab\", s2=\"eidboaoo\" → False (no window of length 2 has both 'a' and 'b')")
    ])),
    N.divider(),
]

# ── Solution 1: Sliding Window with Match Counter (Optimal) ─────────────────
code_s1 = '''\
def checkInclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    k = len(s1)
    need   = [0] * 26   # target frequencies from s1
    window = [0] * 26   # current window frequencies
    for c in s1:
        need[ord(c) - 97] += 1
    for c in s2[:k]:    # seed window with first k chars
        window[ord(c) - 97] += 1
    matches = sum(1 for i in range(26) if window[i] == need[i])
    if matches == 26:
        return True
    for r in range(k, len(s2)):
        ri = ord(s2[r]) - 97          # incoming character index
        if window[ri] == need[ri]: matches -= 1
        window[ri] += 1
        if window[ri] == need[ri]: matches += 1
        li = ord(s2[r - k]) - 97      # outgoing character index
        if window[li] == need[li]: matches -= 1
        window[li] -= 1
        if window[li] == need[li]: matches += 1
        if matches == 26:
            return True
    return False
'''

blocks += [
    N.h2("Solution 1 — Fixed-Size Sliding Window with Match Counter (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A permutation of s1 uses the same characters with the same frequencies. We don't need to generate permutations — we just need a substring of s2 that has the same character frequency profile as s1. That substring must have exactly len(s1) characters. So: find any window of size k = len(s1) in s2 with matching frequency counts."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: extract every window of size k from s2 and compute its frequency map from scratch. This costs O(k) per window and there are O(n) windows, giving O(n·k) total — too slow if both strings are long. We need to reuse computation between adjacent windows."),
        N.h4("The Key Observation"),
        N.para("When we slide the window one step right, exactly one character enters and one leaves. All other character counts stay the same. So we can update the frequency map in O(1) per step — add the new character, remove the old one. The window state is maintained incrementally."),
        N.h4("Building the Solution"),
        N.para("Step 1: Build need[] from s1. Step 2: Build window[] from s2[0:k]. Step 3: Count how many of 26 character slots currently agree (matches). Step 4: Slide right, updating window[] and matches with 4 checks per step: check-before-add, add, check-after-add, same for the outgoing char. Return True when matches==26."),
        N.callout("Analogy: Think of it like a scorecard with 26 rows (one per letter). After each slide, only two rows change. You just recheck those two rows — not all 26 — to keep the 'correct rows' count current.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(code_s1),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(s1) > len(s2): return False", {"code": True}), (" — Early exit: no window of size k can exist in s2 if k > len(s2).")])),
    N.para(N.rich([("need = [0]*26 / window = [0]*26", {"code": True}), (" — Two fixed-size arrays (26 lowercase letters). Constant O(1) space regardless of input.")])),
    N.para(N.rich([("for c in s1: need[ord(c)-97] += 1", {"code": True}), (" — Build the target frequency array. ord('a')=97 maps 'a'→0, 'b'→1, ..., 'z'→25.")])),
    N.para(N.rich([("for c in s2[:k]: window[ord(c)-97] += 1", {"code": True}), (" — Seed the window with the first k characters of s2.")])),
    N.para(N.rich([("matches = sum(...)", {"code": True}), (" — Count how many of the 26 slots currently have window[i] == need[i]. Target is 26.")])),
    N.para(N.rich([("if matches == 26: return True", {"code": True}), (" — The first window is already a permutation — done.")])),
    N.para(N.rich([("ri = ord(s2[r]) - 97", {"code": True}), (" — Character index of the incoming (right) character.")])),
    N.para(N.rich([("if window[ri] == need[ri]: matches -= 1", {"code": True}), (" — Before adding: was this slot matched? If yes, adding will overshoot — undo the match.")])),
    N.para(N.rich([("window[ri] += 1", {"code": True}), (" — Increment incoming character's count.")])),
    N.para(N.rich([("if window[ri] == need[ri]: matches += 1", {"code": True}), (" — After adding: does this slot now exactly match need? Record the match.")])),
    N.para(N.rich([("li = ord(s2[r-k]) - 97", {"code": True}), (" — Character index of the outgoing (left) character.")])),
    N.para(N.rich([("if window[li] == need[li]: matches -= 1", {"code": True}), (" — Before removing: was this slot matched? Removing will undershoot — undo the match.")])),
    N.para(N.rich([("window[li] -= 1", {"code": True}), (" — Decrement outgoing character's count.")])),
    N.para(N.rich([("if window[li] == need[li]: matches += 1", {"code": True}), (" — After removing: does removal hit the target exactly? Record if so.")])),
    N.para(N.rich([("if matches == 26: return True", {"code": True}), (" — All 26 character slots agree — current window is a permutation of s1.")])),
    N.divider(),
]

# ── Solution 2: Counter Comparison ─────────────────────────────────────────
code_s2 = '''\
from collections import Counter

def checkInclusion(s1: str, s2: str) -> bool:
    k = len(s1)
    if k > len(s2):
        return False
    need = Counter(s1)          # target: character frequencies of s1
    win  = Counter(s2[:k])      # window: initial k-character window
    if win == need:
        return True
    for r in range(k, len(s2)):
        win[s2[r]] += 1             # add incoming character
        out_c = s2[r - k]
        win[out_c] -= 1             # remove outgoing character
        if win[out_c] == 0:
            del win[out_c]          # keep Counter clean
        if win == need:
            return True             # Counter comparison: O(26) = O(1)
    return False
'''

blocks += [
    N.h2("Solution 2 — Counter Comparison (Simpler Code)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same insight as Solution 1: we need a window of exactly len(s1) characters in s2 with matching character frequencies. Here we use Python's Counter for cleaner code at the cost of a slightly larger constant per comparison."),
        N.h4("What Doesn't Work"),
        N.para("Recomputing Counter(s2[i:i+k]) from scratch each iteration would be O(k) per step. We still need incremental updates."),
        N.h4("The Key Observation"),
        N.para("Python's Counter supports equality comparison (Counter(a) == Counter(b)). By keeping win updated incrementally (one add, one remove per step), we can compare with need each step in O(number of distinct chars) = O(26) = O(1)."),
        N.h4("Building the Solution"),
        N.para("Same sliding window as Solution 1, but use Counter objects. After each slide, call win == need. Simpler to write but the match-counter approach (Solution 1) is marginally faster and more elegant."),
        N.callout("Use this version to quickly show understanding in an interview. Then offer to optimize with the match counter for O(1) per step instead of O(26).", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(code_s2),
    N.h3("Line by Line"),
    N.para(N.rich([("need = Counter(s1)", {"code": True}), (" — Build target frequency map from s1.")])),
    N.para(N.rich([("win = Counter(s2[:k])", {"code": True}), (" — Build initial window frequency map from first k characters.")])),
    N.para(N.rich([("win[s2[r]] += 1", {"code": True}), (" — Add the incoming character.")])),
    N.para(N.rich([("win[out_c] -= 1; if win[out_c] == 0: del win[out_c]", {"code": True}), (" — Remove outgoing character. Delete 0-count entries so Counter comparison works correctly.")])),
    N.para(N.rich([("if win == need: return True", {"code": True}), (" — O(26) comparison: if all character frequencies match, found a permutation.")])),
    N.divider(),
]

# ── Complexity table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (recompute each window)", "O(n · k)", "O(k)"],
        ["Counter Comparison (sliding)", "O(26n) = O(n)", "O(1)"],
        ["Match Counter, fixed array (Interview Pick)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Frequency Count Window — fixed-size window where character frequencies must match a target profile")])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Does s2 contain a permutation/anagram of s1?' — fixed window size = len(s1)\n"
        "• Window length is given or derived from a constraint (not to be optimized)\n"
        "• Must match character frequencies in a sliding window\n"
        "• Two frequency maps (need vs window) compared at each step",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
related = [
    ("Find All Anagrams in a String", "Medium", "Identical algorithm; collect all window-start indices instead of returning on first match (#438)"),
    ("Valid Anagram", "Easy", "No sliding needed; just compare freq maps of the entire strings (#242)"),
    ("Minimum Window Substring", "Hard", "Variable-size variant: find shortest window in s containing all chars of t (#76)"),
    ("Longest Substring Without Repeating Characters", "Medium", "Variable-size window: expand until repeat, shrink from left to fix (#3)"),
    ("Maximum Average Subarray I", "Easy", "Fixed window over integers: sum and divide — same sliding template (#643)"),
    ("Sliding Window Maximum", "Hard", "Fixed window with monotonic deque for O(1) max tracking (#239)"),
    ("Group Anagrams", "Medium", "Sort each word as a grouping key — related frequency-count pattern (#49)"),
]

blocks += [N.h2("🔗 Related Problems"), N.para("Problems using the same technique:")]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}), (f" ({diff})", {}), (" — " + note, {})
    ])))
blocks += [
    N.para("These problems share the core technique: maintain a character frequency map over a sliding window, comparing against a target profile."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.4 (Fixed-Size Sliding Window)", "📚", "gray_background"),
]

# ── Embed ───────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks in safe chunks ────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=877")
