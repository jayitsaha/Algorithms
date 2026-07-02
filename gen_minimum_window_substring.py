"""
gen_minimum_window_substring.py
Notion page builder for LeetCode #76 — Minimum Window Substring.
notion_page_id = null → create fresh page.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812c-b7aa-e1a400d13777"  # Already created
print(f"Using existing page: {PAGE_ID}")

# ── Step 2: Set properties ───────────────────────────────────────
# NOTE: Notion multi_select does not allow commas in option names.
# Using "Expand-Until-Valid Shrink-to-Optimize" (hyphenated) as the subpattern label.
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=76,
    pattern="Sliding Window",
    subpatterns=["Expand-Until-Valid Shrink-to-Optimize"],
    tc="O(|s|+|t|)",
    sc="O(|t|)",
    key_insight="Expand right until all of t is covered (formed==required), then shrink left to minimize; O(1) validity via formed counter.",
    icon="🔴"
)
print("Properties set.")

# ── Step 3: wipe (fresh page has no body) then build ────────────
N.wipe_page(PAGE_ID)

SOLUTION_CODE = """\
def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
    required = len(need)        # distinct chars to satisfy
    window = {}
    formed = 0
    left = 0
    best = float('inf'), 0, 0  # (length, left, right)
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        # Did we just satisfy this char's requirement?
        if c in need and window[c] == need[c]:
            formed += 1
        while formed == required:   # window is valid — shrink
            if right - left + 1 < best[0]:
                best = right - left + 1, left, right
            l = s[left]
            left += 1
            window[l] -= 1
            if l in need and window[l] < need[l]:
                formed -= 1
    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]
"""

BRUTE_CODE = """\
from collections import Counter

def minWindow_brute(s: str, t: str) -> str:
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            win = Counter(s[i:j+1])
            if all(win[c] >= need[c] for c in need):
                if not best or j - i + 1 < len(best):
                    best = s[i:j+1]
    return best
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two strings "),
        ("s", {"code": True}),
        (" and "),
        ("t", {"code": True}),
        (", return the minimum window substring of "),
        ("s", {"code": True}),
        (" such that every character in "),
        ("t", {"code": True}),
        (" (including duplicates) is included in the window. If there is no such substring, return the empty string "),
        ('""', {"code": True}),
        (". The answer is guaranteed to be unique."),
    ])),
    N.para(N.rich([
        ("Example: s=", {}), ('"ADOBECODEBANC"', {"code": True}),
        (", t=", {}), ('"ABC"', {"code": True}),
        (" → Output: ", {}), ('"BANC"', {"code": True}),
        (". Multiple valid windows exist (ADOBEC len 6, BANC len 4) — return the shortest."),
    ])),
    N.divider(),
]

# ── Solution 1 (Optimal) ─────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Sliding Window with formed Counter (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're looking for the shortest contiguous piece of s that acts as a 'superset' of t's character multiset. The window must contain every character t demands, but can hold extras."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries every O(|s|²) substring and checks each in O(|t|) → O(|s|²·|t|). For |s|=10⁵, |t|=10³ that's 10¹³ operations — way too slow."),
        N.h4("The Key Observation"),
        N.para("If we have a valid window [L, R], moving R right can only make it 'more valid' (never break validity). Moving L right can only reduce validity. This monotonicity is the key — we can use two pointers that never go backward: expand R until valid, then advance L to minimize, then expand R again."),
        N.h4("Building the Solution"),
        N.para("1. Build need map from t. 2. Use formed counter: increments only when window[c] reaches need[c] exactly (threshold crossing). 3. When formed==required, window is valid — record minimum, shrink left. 4. When shrinking breaks a requirement, stop and expand again. Each character enters and exits at most once → O(|s|)."),
        N.callout(
            "Analogy: You're collecting stamps. You expand your collection (window) until you have every required stamp. Then you discard duplicates from the oldest acquisitions (shrink left) to keep only the minimum needed set.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("if not t or not s: return \"\"", {"code": True}), (" — Guard: empty input means no window is possible.")])),
    N.para(N.rich([("need = {}; for c in t: need[c]+=1", {"code": True}), (" — Build frequency map of characters required from t.")])),
    N.para(N.rich([("required = len(need)", {"code": True}), (" — Number of DISTINCT characters that must each be fully satisfied.")])),
    N.para(N.rich([("window = {}; formed = 0", {"code": True}), (" — window tracks current window frequencies; formed counts satisfied distinct chars.")])),
    N.para(N.rich([("left = 0; best = (inf, 0, 0)", {"code": True}), (" — Left pointer starts at 0; best records (length, left_idx, right_idx) of smallest valid window.")])),
    N.para(N.rich([("for right in range(len(s)):", {"code": True}), (" — Outer loop expands the window rightward one character at a time.")])),
    N.para(N.rich([("window[c] = window.get(c,0) + 1", {"code": True}), (" — Add the new character to the window's frequency map.")])),
    N.para(N.rich([("if c in need and window[c] == need[c]: formed += 1", {"code": True}), (" — If this character is needed AND we just hit the exact threshold, increment formed. The == (not >=) fires exactly once per 'satisfaction event'.")])),
    N.para(N.rich([("while formed == required:", {"code": True}), (" — Inner loop: window is valid. Try to shrink from the left while maintaining validity.")])),
    N.para(N.rich([("if right-left+1 < best[0]: best = ...", {"code": True}), (" — Record this as the new best if it's smaller than anything seen so far.")])),
    N.para(N.rich([("l = s[left]; left += 1; window[l] -= 1", {"code": True}), (" — Remove the leftmost character from the window and advance left.")])),
    N.para(N.rich([("if l in need and window[l] < need[l]: formed -= 1", {"code": True}), (" — If removing it broke a requirement (count now below need), decrement formed. This exits the while loop.")])),
    N.para(N.rich([("return s[best[1]:best[2]+1]", {"code": True}), (" — Reconstruct the answer string using stored indices. One O(k) slice at the end.")])),
    N.divider(),
]

# ── Solution 2 (Brute Force) ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (All Substrings)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible substring of s and check if it covers t's requirements. Return the shortest that qualifies."),
        N.h4("What Doesn't Work"),
        N.para("This is O(|s|²) substrings × O(|t|) validity check per substring = O(|s|²·|t|). For large inputs this is prohibitively slow, but it's the correct starting point to mention before optimizing."),
        N.h4("The Key Observation"),
        N.para("Counter(substring) >= Counter(t) for each character checks validity. Python's Counter subtraction or all() over need keys makes this readable. Mention this first in an interview to show you understand the problem, then offer to optimize."),
        N.h4("Building the Solution"),
        N.para("Nested loop over all (i, j) pairs. For each, count characters in s[i:j+1] and verify all of t's requirements are met. Track the shortest valid window found."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("need = Counter(t)", {"code": True}), (" — Character frequency requirements from t.")])),
    N.para(N.rich([("for i in range(len(s)):", {"code": True}), (" — Outer loop: try every possible left boundary.")])),
    N.para(N.rich([("for j in range(i, len(s)):", {"code": True}), (" — Inner loop: extend right boundary.")])),
    N.para(N.rich([("win = Counter(s[i:j+1])", {"code": True}), (" — Count all characters in this window. O(j-i) cost.")])),
    N.para(N.rich([("if all(win[c]>=need[c] for c in need):", {"code": True}), (" — Check if every required character has enough copies in the window. O(|t|) cost.")])),
    N.para(N.rich([("if not best or j-i+1 < len(best): best = s[i:j+1]", {"code": True}), (" — Update best if this window is shorter.")])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(|s|² · |t|)", "O(|s| + |t|)"],
        ["Sliding Window (Optimal)", "O(|s| + |t|)", "O(|t|)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sliding Window (Array Manipulation)")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Expand Until Valid, Shrink to Optimize")])),
    N.callout(
        "When to recognize this pattern: 'Minimum/shortest subarray or substring containing all [requirements from t].' Two pointers where right expands to satisfy a condition and left contracts to minimize. O(1) validity check via a formed counter instead of re-scanning the whole window.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (variable sliding window with character frequency):"),
    N.bullet(N.rich([("Find All Anagrams in a String", {"bold": True}), (" (Medium) — Fixed-size window + frequency matching. (#438)")])),
    N.bullet(N.rich([("Longest Substring Without Repeating Characters", {"bold": True}), (" (Medium) — Expand until duplicate, shrink to remove. (#3)")])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), (" (Medium) — Max-freq trick for window validity. (#424)")])),
    N.bullet(N.rich([("Minimum Size Subarray Sum", {"bold": True}), (" (Medium) — Same expand/shrink pattern with numeric sum. (#209)")])),
    N.bullet(N.rich([("Substring with Concatenation of All Words", {"bold": True}), (" (Hard) — Fixed-word-length window with word-frequency map. (#30)")])),
    N.bullet(N.rich([("Minimum Window Subsequence", {"bold": True}), (" (Hard) — Order matters (subsequence not multiset). (#727)")])),
    N.bullet(N.rich([("Longest Substring with At Most K Distinct Characters", {"bold": True}), (" (Medium) — Shrink when distinct count exceeds K. (#340)")])),
    N.para("These problems share the same core technique: two pointers where the window satisfies a condition based on character frequencies, and we toggle between expanding and contracting."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.5 — Sliding Window Dynamic Size", "📚", "gray_background"),
]

# ── Interactive Embed ─────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_window_substring")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
